package openggf.racing.server.tools;

import com.openggf.mods.run.CharacterLooks;
import com.openggf.net.client.GhostStreamPublisher;
import com.openggf.net.client.MasterClient;
import com.openggf.net.client.RaceClient;
import com.openggf.net.client.RaceConnection;
import com.openggf.net.identity.PlayerIdentity;
import com.openggf.net.protocol.ControlMessage;
import openggf.racing.server.master.MasterConfig;
import openggf.racing.server.master.MasterServer;
import openggf.timeattack.mp.VoteTrackPools;

import java.net.URI;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.*;

/**
 * PROMO FIXTURE (ta-promo-a, 2026-10-23; not committed). A copy of TimeAttackVideoPeers with
 * named, coloured protocol peers for the Time Attack promo film. Every peer is an authenticated
 * loopback protocol client on a real master relay; its ghost replays a recorded ROM-backed GHZ1
 * route (TimeAttackRouteTool) retimed by a cosmetic schedule. Peers are not people, not ROM
 * simulations and their finishes are synthetic.
 *
 * Differences from the original: names/looks per peer; the room carries the default S1 vote pool
 * (as a hosting client's room does); peers advance on wall frames after the countdown (not on the
 * live player's executed steps); a tighter swirl schedule keeps the pack near the camera; after the
 * round ends peers vote (staggered) and the room owner starts the voted round.
 */
public final class PromoPeers implements AutoCloseable {
    public record Rival(String name, int colour) { }

    private final MasterServer server;
    private final LoopbackSourceProxy proxy;
    private final Path root;
    private final String fingerprint;
    private final String liveName;
    private final List<Rival> rivals;
    private final List<Peer> peers = new ArrayList<>();
    private final List<MasterClient> masters = new ArrayList<>();
    private final TimeAttackRouteTool.Route route;
    private final boolean tightPack;
    private final Map<Integer, ControlMessage.StandingsRow> standings = new HashMap<>();
    private final String roomName;
    private String room;
    private long countdown;
    private long lastHeartbeat;
    private int elapsed = -1;
    private int roundEnds;
    private List<String> voteOptions = List.of();
    private long voteOfferedAt;
    private String voteResult;
    private boolean nextRoundSent;
    private int[] voteChoice;
    private boolean closed;
    private ControlMessage.RoundConfig nextConfig;

    private static final class Peer {
        final RaceConnection connection;
        final GhostStreamPublisher publisher;
        final int index;
        boolean started, sentFinish, voted;
        int generated, sourceFrame, firstInput = -1;
        int members;
        final Set<Integer> memberSlots = new HashSet<>();
        Peer(RaceConnection connection, int index) {
            this.connection = connection;
            publisher = new GhostStreamPublisher(connection::sendBinary);
            this.index = index;
        }
    }

    public PromoPeers(Path root, Path liveIdentity, String liveName, String fingerprint, List<Rival> rivals,
                      String roomName, TimeAttackRouteTool.Route route, boolean tightPack) throws Exception {
        this.root = root;
        this.fingerprint = fingerprint;
        this.liveName = liveName;
        this.rivals = List.copyOf(rivals);
        this.roomName = roomName;
        this.route = Objects.requireNonNull(route);
        this.tightPack = tightPack;
        int players = rivals.size() + 1;
        MasterConfig config = new MasterConfig(0, null, null, true, "identities.db", 0,
                UUID.randomUUID().toString(), 48, 10, 14, 50, 8, 8, false,
                2, 4, 30, 20, 30, 10000, 60);
        server = MasterServer.start(config, root.resolve("master"));
        proxy = new LoopbackSourceProxy(server.port(), players + 16);
        PlayerIdentity live = PlayerIdentity.loadOrCreate(liveIdentity);
        master(live, liveName).close();
    }

    public URI endpoint() { return URI.create("ws://127.0.0.1:" + proxy.port() + "/master"); }

    private MasterClient master(PlayerIdentity identity, String name) throws Exception {
        MasterClient client = MasterClient.connect(endpoint(), identity, name, fingerprint, null).get(20, TimeUnit.SECONDS);
        masters.add(client);
        CompletableFuture<Void> promoted = new CompletableFuture<>();
        server.execute(() -> {
            try { server.establishForTest(identity.fingerprint()); promoted.complete(null); }
            catch (Throwable failure) { promoted.completeExceptionally(failure); }
        });
        promoted.get(10, TimeUnit.SECONDS);
        return client;
    }

    public void fill() throws Exception {
        int players = rivals.size() + 1;
        for (int index = 0; index < rivals.size(); index++) {
            Rival rival = rivals.get(index);
            String look = rival.colour() < 0 ? ""
                    : CharacterLooks.withBaseColour("s1", "sonic", rival.colour()).encode();
            PlayerIdentity identity = PlayerIdentity.loadOrCreate(root.resolve("bot-" + index));
            MasterClient master = master(identity, rival.name());
            if (room == null) {
                room = master.createRoom(new ControlMessage.RoomDescriptor(roomName,
                        "s1", 0, 0, "LOCKED", "sonic", players, false), "RELAY", 0, fingerprint,
                        VoteTrackPools.forGame("s1")).get(20, TimeUnit.SECONDS).roomId();
            }
            RaceConnection connection = master.joinRoom(room, identity, rival.name(), look, fingerprint)
                    .get(20, TimeUnit.SECONDS);
            peers.add(new Peer(connection, index));
            connection.sendControl(new ControlMessage.SelectCharacter("sonic"));
            pump();
        }
    }

    public void startRound(int seconds) {
        peers.getFirst().connection.sendControl(new ControlMessage.SetReadyRule("AUTO"));
        peers.getFirst().connection.sendControl(new ControlMessage.RoundConfigure(
                new ControlMessage.RoundConfig("s1", 0, 0, seconds, "LOCKED", "sonic")));
    }

    public void chat(int peer, String text) { peers.get(peer).connection.sendControl(new ControlMessage.Chat(text)); }

    /** One wall frame of presentation (60 Hz). */
    public void tick() throws Exception {
        if (countdown != 0 && System.currentTimeMillis() >= countdown) { elapsed++; publish(); }
        vote();
        pump();
    }

    /** Swirling pack: each runner's offset from the recorded timing, in frames. */
    private int sourceFrame(int runner, int t) {
        if (!tightPack) return GhostPackSchedule.sourceFrame(runner, t, route.frames().size());
        int pair = runner / 2;
        double sign = runner % 2 == 0 ? 1 : -1;
        // No drift: the pack swirls within about half a second of the recorded timing all race.
        double phase = (runner % 8) * Math.PI / 4;
        double amplitude = 8 + (runner % 4) * 9;
        double period = 640 + (runner % 5) * 130;
        double offset = amplitude * (Math.sin(2 * Math.PI * t / period + phase) - Math.sin(phase));
        return Math.clamp((int) Math.floor(t + sign * offset), 0, route.frames().size() - 1);
    }

    private int admitted(int runner, int t, int previous) {
        int target = Math.min(sourceFrame(runner, t), previous + 2);
        var before = route.frames().get(previous);
        int max = com.openggf.net.hub.TrackValidationProfile.GLOBAL_SPEED_CEILING_PX_PER_FRAME;
        while (target > previous) {
            var after = route.frames().get(target);
            if (Math.abs(after.x() - before.x()) <= max && Math.abs(after.y() - before.y()) <= max) return target;
            target--;
        }
        return previous;
    }

    private void publish() {
        for (Peer peer : peers) {
            if (!peer.started) {
                peer.connection.sendControl(new ControlMessage.AttemptStart(1));
                peer.publisher.beginAttempt(1);
                peer.started = true;
            }
            if (peer.sentFinish) continue;
            int source = admitted(peer.index, elapsed, peer.sourceFrame);
            peer.sourceFrame = source;
            if (peer.firstInput < 0 && source >= route.firstInput()) peer.firstInput = peer.generated;
            peer.publisher.onFrame(route.frames().get(source));
            peer.generated++;
            if (source == route.frames().size() - 1) {
                peer.publisher.finishAttempt();
                int first = peer.firstInput, finish = peer.generated - 1;
                peer.connection.sendControl(new ControlMessage.AttemptFinish(1, finish - first,
                        first, finish, "ab".repeat(32),
                        HexFormat.of().formatHex(peer.publisher.streamHashSha256()), null));
                peer.sentFinish = true;
            }
        }
    }

    /** Staggered votes: most peers back the second option, a few the others; the owner starts the result. */
    private void vote() {
        if (voteOptions.isEmpty() || voteResult != null) {
            if (voteResult != null && !nextRoundSent && nextConfig != null) {
                peers.getFirst().connection.sendControl(new ControlMessage.RoundConfigure(nextConfig));
                nextRoundSent = true;
            }
            return;
        }
        long since = System.currentTimeMillis() - voteOfferedAt;
        int[] choice = {1, 0, 1, 2, 1, 1, 0, 1};
        for (Peer peer : peers) {
            if (peer.voted) continue;
            if (since >= 1500L + peer.index * 650L) {
                int option = Math.min(choice[peer.index % choice.length], voteOptions.size() - 1);
                peer.connection.sendControl(new ControlMessage.TrackVote(voteOptions.get(option)));
                peer.voted = true;
            }
        }
    }

    public void pump() throws Exception {
        if (proxy.failure() != null) throw proxy.failure();
        long now = System.currentTimeMillis();
        if (now - lastHeartbeat >= 3000 && !peers.isEmpty()) {
            for (Peer peer : peers) peer.connection.sendControl(new ControlMessage.Ping(now));
            lastHeartbeat = now;
        }
        for (Peer peer : peers) {
            for (RaceClient.InboundEvent event : peer.connection.drainInbound()) {
                switch (event) {
                    case RaceClient.Control control -> {
                        switch (control.message()) {
                            case ControlMessage.RoomState state -> {
                                peer.memberSlots.clear();
                                state.players().forEach(player -> peer.memberSlots.add(player.slot()));
                                peer.members = peer.memberSlots.size();
                            }
                            case ControlMessage.PlayerUpsert upsert -> {
                                peer.memberSlots.add(upsert.player().slot());
                                peer.members = peer.memberSlots.size();
                            }
                            case ControlMessage.PlayerLeft left -> {
                                peer.memberSlots.remove(left.slot());
                                peer.members = peer.memberSlots.size();
                            }
                            case ControlMessage.RoundStart start -> {
                                if (peer.index == 0) {
                                    countdown = start.countdownEndsAtHubMillis();
                                    elapsed = -1;
                                    voteOptions = List.of();
                                    voteResult = null;
                                }
                            }
                            case ControlMessage.StandingsDelta delta -> observe(delta.rows());
                            case ControlMessage.StandingsPage page -> observe(page.rows());
                            case ControlMessage.RoundEnd end -> { observe(end.finalStandings()); if (peer.index == 0) roundEnds++; }
                            case ControlMessage.TrackVoteOffer offer -> {
                                if (peer.index == 0) { voteOptions = offer.trackKeys(); voteOfferedAt = System.currentTimeMillis(); }
                            }
                            case ControlMessage.TrackVoteResult result -> {
                                if (peer.index == 0) {
                                    voteResult = result.trackKey();
                                    String[] parts = voteResult.split(":");
                                    nextConfig = new ControlMessage.RoundConfig(parts[0], Integer.parseInt(parts[1]),
                                            Integer.parseInt(parts[2]), 120, "LOCKED", "sonic");
                                }
                            }
                            case ControlMessage.Kick kick -> throw new IllegalStateException("bot kicked: " + kick.reason());
                            default -> { }
                        }
                    }
                    case RaceClient.Disconnected gone -> throw new IllegalStateException("bot disconnected: " + gone.reason());
                    default -> { }
                }
            }
            if (!peer.connection.isOpen()) throw new IllegalStateException("bot socket closed");
        }
    }

    private void observe(List<ControlMessage.StandingsRow> rows) { rows.forEach(row -> standings.put(row.slot(), row)); }

    /** Lobby presence publishers, one per peer (TYPE_LOBBY_FRAMES on the relay connection). */
    public List<com.openggf.net.client.LobbyPosePublisher> lobbyPublishers() {
        List<com.openggf.net.client.LobbyPosePublisher> list = new ArrayList<>();
        for (Peer peer : peers) list.add(new com.openggf.net.client.LobbyPosePublisher(peer.connection::sendBinary));
        return list;
    }

    public int connectedCount() { return peers.isEmpty() ? 0 : peers.getFirst().members; }
    public int botCount() { return peers.size(); }
    public int sentFinishes() { return (int) peers.stream().filter(peer -> peer.sentFinish).count(); }
    public boolean roundEnded() { return roundEnds > 0; }
    public int roundEnds() { return roundEnds; }
    public List<String> voteOptions() { return voteOptions; }
    public String voteResult() { return voteResult; }
    public boolean nextRoundSent() { return nextRoundSent; }
    public int liveRank() { return standings.values().stream().filter(row -> row.displayName().equals(liveName))
            .mapToInt(ControlMessage.StandingsRow::rank).findFirst().orElse(0); }

    @Override public void close() throws Exception {
        if (closed) return;
        closed = true;
        for (Peer peer : peers) try { peer.connection.close(); } catch (Exception ignored) { }
        for (MasterClient master : masters) try { master.close(); } catch (Exception ignored) { }
        try { server.close(); } catch (Exception ignored) { }
        try { proxy.close(); } catch (Exception ignored) { }
    }
}
