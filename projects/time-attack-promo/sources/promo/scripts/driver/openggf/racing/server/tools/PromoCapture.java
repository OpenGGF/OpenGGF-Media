package openggf.racing.server.tools;

import com.openggf.audio.AudioManager;
import com.openggf.audio.LiveCaptureAudioHandle;
import com.openggf.control.MenuInput;
import com.openggf.data.Rom;
import com.openggf.debug.playback.*;
import com.openggf.game.GameMode;
import com.openggf.game.GameServices;
import com.openggf.mods.run.CharacterLooks;
import com.openggf.mods.run.DeterminismFingerprint;
import com.openggf.mods.run.RunArea;
import com.openggf.net.client.DirectJoinAddress;
import com.openggf.net.client.LobbyPosePublisher;
import com.openggf.net.client.RaceClient;
import com.openggf.net.ghost.GhostFrame;
import com.openggf.net.identity.PlayerIdentity;
import com.openggf.net.protocol.ControlMessage;
import com.openggf.tools.TimeAttackVideoCaptureTool;
import com.openggf.version.AppVersion;
import openggf.timeattack.mp.LobbyAreas;

import java.io.*;
import java.lang.reflect.Field;
import java.net.ServerSocket;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.function.BooleanSupplier;

import static org.lwjgl.glfw.GLFW.*;

/**
 * PROMO FIXTURE (ta-promo-a, 2026-10-23; not committed). Display-free capture driver for the
 * Time Attack promo, assembled from TimeAttackCapacityVideoTool and TimeAttackLobbyVideoTool.
 * Drives the real Engine first boot and Time Attack UI with physical key events; writes every
 * presentation frame losslessly (FFV1, 320x224, 60 fps), the live SMPS mix as 48 kHz PCM and a
 * per-frame state.csv with stage labels.
 *
 * Modes:
 *   race  OUT ROOT ROUTE WINDOW clean|death intl|bots PLAYERS
 *     A master relay room of named protocol peers (PromoPeers). The live player joins through
 *     Browse, races GHZ1 from the maintained ghz1_fullrun.bk2 controller movie (from row 840),
 *     and in "death" first holds Right into the first badnik (a natural death on 0 rings), skips
 *     the death with jump, waits out the fast restart's 3-2-1 and then plays the movie. "clean"
 *     continues through the round end, the vote and the voted round's launch.
 *   lobby OUT ROOT GAME [profile]
 *     A hosted LAN room's lobby level with three peers (names/looks below) whose lobby presence
 *     replays the live player's recent poses at an offset (as TimeAttackLobbyVideoTool). With
 *     "profile": the first-run name prompt is typed one code point at a time, and the PROFILE page
 *     cycles look presets to Ember and saves before the player readies and runs.
 */
public final class PromoCapture {
    static final String HERO = "疾風の刃";
    static final int HERO_LOOK = 0x006E; // LookPresets "Ember"
    static final List<PromoPeers.Rival> RIVALS = List.of(
            new PromoPeers.Rival("Nguyễn Hoa", 0x04C2),      // Emerald
            new PromoPeers.Rival("Дмитрий", 0x022E),         // Crimson
            new PromoPeers.Rival("Ωμέγα", 0x0AA0),           // Teal
            new PromoPeers.Rival("소닉팬", 0x0A6E),            // Rose
            new PromoPeers.Rival("Zoë Ñandú", 0x0E46),       // Violet
            new PromoPeers.Rival("风之子", 0x00CE),            // Gold
            new PromoPeers.Rival("Çağrı Öztürk", 0x0E62),    // Azure
            new PromoPeers.Rival("Łukasz", 0x0AAA));         // Silver

    private final Path out;
    private final TimeAttackVideoCaptureTool capture;
    private final Process encoder;
    private final OutputStream video;
    private final OutputStream pcm;
    private final BufferedWriter states;
    private final LiveCaptureAudioHandle audio;
    private final short[] samples;
    private final byte[] sampleBytes;
    private long started;
    private String stage = "boot";
    private Object session;
    private String extraState = "";

    PromoCapture(Path out, Path root) throws Exception {
        this.out = out.toAbsolutePath();
        Files.createDirectories(this.out);
        capture = new TimeAttackVideoCaptureTool(this.out, root, 320, 224);
        encoder = new ProcessBuilder("ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "rawvideo", "-pixel_format", "rgba", "-video_size", "320x224", "-framerate", "60",
                "-i", "pipe:0", "-vf", "vflip", "-c:v", "ffv1", "-level", "3", "-g", "1", "-pix_fmt", "bgr0",
                this.out.resolve("video.mkv").toString())
                .redirectError(this.out.resolve("encoder.log").toFile()).start();
        video = new BufferedOutputStream(encoder.getOutputStream(), 4 * 1024 * 1024);
        pcm = new BufferedOutputStream(Files.newOutputStream(this.out.resolve("audio.pcm")));
        audio = AudioManager.getInstance().beginLiveCaptureAudio(60);
        samples = new short[audio.maxStereoFramesPerPacket() * 2];
        sampleBytes = new byte[samples.length * 2];
        states = Files.newBufferedWriter(this.out.resolve("state.csv"));
        states.write("frame,stage,mode,session,x,y,dead,extra\n");
        Files.writeString(this.out.resolve("audio-rate.txt"), audio.sampleRate() + "\n");
    }

    /** Called after every presentation: video, audio, state, 60 Hz wall pacing. */
    void record() {
        try {
            int frame = (int) capture.frameNumber();
            var camera = GameServices.cameraOrNull();
            var player = camera == null || capture.engine().getCurrentGameMode() != GameMode.LEVEL
                    ? null : camera.getFocusedSprite();
            int count = audio.drainPresentationFrame(samples) * 2;
            for (int i = 0; i < count; i++) {
                sampleBytes[2 * i] = (byte) samples[i];
                sampleBytes[2 * i + 1] = (byte) (samples[i] >>> 8);
            }
            pcm.write(sampleBytes, 0, count * 2);
            video.write(capture.pixels());
            states.write(frame + "," + stage + "," + capture.engine().getCurrentGameMode() + ","
                    + (session == null ? "" : call(session, "state")) + ","
                    + (player == null ? -1 : player.getCentreX()) + "," + (player == null ? -1 : player.getCentreY())
                    + "," + (player != null && player.getDead()) + "," + extraState + "\n");
            if (started == 0) started = System.nanoTime() - frame * 1_000_000_000L / 60;
            long remaining = started + frame * 1_000_000_000L / 60 - System.nanoTime();
            if (remaining > 0) TimeUnit.NANOSECONDS.sleep(remaining);
        } catch (Exception failure) { throw new RuntimeException(failure); }
    }

    void chapter(String name) throws IOException {
        stage = name.replace(',', ' ');
        System.out.println("stage=" + name + " frame=" + capture.frameNumber());
        Files.writeString(out.resolve("chapters.csv"), capture.frameNumber() + "," + stage + "\n",
                StandardOpenOption.CREATE, StandardOpenOption.APPEND);
    }

    void await(BooleanSupplier ready, int frames, String what) throws Exception {
        for (int i = 0; !ready.getAsBoolean() && i < frames; i++) capture.frame();
        if (!ready.getAsBoolean()) throw new IllegalStateException("timed out: " + what + " at " + stage);
    }

    Object openScene() throws Exception {
        capture.openTimeAttack();
        Object ownedScene = field(field(capture.engine().getGameLoop(), "modSceneHost"), "scene");
        Object scene = com.openggf.mods.code.OwnedSceneFactory.unwrap((com.openggf.mods.scene.ModScene) ownedScene);
        session = field(scene, "session");
        return scene;
    }

    String state() {
        try { return call(session, "state").toString(); } catch (Exception e) { throw new RuntimeException(e); }
    }

    /** Types a name one code point every {@code gap} frames through the GLFW char path. */
    void typeName(String name, int gap) throws Exception {
        name.codePoints().forEach(cp -> {
            try {
                MenuInput.handleCharEvent(capture.input(), cp);
                capture.frames(gap);
            } catch (Exception e) { throw new RuntimeException(e); }
        });
    }

    // ------------------------------------------------------------------ race
    private PromoPeers peers;
    private Bk2Movie movie;
    private Bk2FrameInput previous;
    private int movieFrame;
    private boolean driving, movieOn, naturalFinish;
    private int deathPhase; // death: 0 holding right, 1 dead, 2 skipped, 3 countdown seen, 4 movie
    private int deadFrames;

    void race(Path root, Path routeFile, int window, boolean death, boolean bots, int players) throws Exception {
        String fp = fingerprint(root, "s1");
        List<PromoPeers.Rival> rivals = new ArrayList<>();
        for (int i = 0; i < players - 1; i++) {
            rivals.add(bots ? new PromoPeers.Rival(i == 0 ? "Capture Host" : String.format(Locale.ROOT, "Bot %03d", i), -1)
                    : RIVALS.get(i));
        }
        String heroName = bots ? "Capture Player" : HERO;
        peers = new PromoPeers(out.resolve("server"), Path.of("identity"), heroName, fp, rivals,
                bots ? "Full Capacity Time Attack" : "Green Hill Sprint",
                TimeAttackRouteTool.read(routeFile), !bots);
        peers.fill();
        Path settings = out.resolve("profile/saves/mods/time-attack/settings.txt");
        Files.createDirectories(settings.getParent());
        Files.writeString(settings, "displayName=" + heroName + "\n" + (bots ? "" : "lookBase=" + String.format("%03X", HERO_LOOK) + "\n")
                + "masterUrl=" + peers.endpoint() + "\nmasterTrustInsecure=false\nminimap=true\n");
        movie = new Bk2MovieLoader().load(root.resolve("src/test/resources/traces/s1/ghz1_fullrun/ghz1_fullrun.bk2"));
        capture.beforeFrame(ignored -> beforeRace(death));
        capture.afterFrame(ignored -> { if (namesRelay) afterLobby(); else afterRace(); record(); });

        openScene();
        chapter("Time Attack setup");
        capture.frames(60);
        for (int i = 0; i < 3; i++) capture.tap(GLFW_KEY_DOWN);
        for (int i = 0; i < 3; i++) { capture.tap(GLFW_KEY_RIGHT); capture.frames(8); }
        for (int i = 0; i < 4; i++) capture.tap(GLFW_KEY_DOWN);
        capture.tap(GLFW_KEY_ENTER);
        await(() -> state().equals("BROWSING"), 1200, "server browser");
        chapter("Server browser");
        capture.frames(120);
        capture.tap(GLFW_KEY_ENTER);
        await(() -> state().equals("LOBBY"), 1200, "lobby");
        await(() -> peers.connectedCount() == peers.botCount() + 1, 900, "full roster");
        chapter("Lobby");
        if (namesRelay) {
            area = LobbyAreas.forGame("s1").area();
            names = true;
            OFFSETS = new int[] {-0x90, 0x24, -0x6C, 0x48, -0x48, 0x6C, -0x24, 0x90};
            DELAYS = new int[8];
            for (int i = 0; i < 8; i++) DELAYS[i] = 6 + 8 * (Math.abs(OFFSETS[i]) / 0x24 - 1);
            await(() -> safeLobbyRun(), 900, "the lobby level");
            lobbyPubs.addAll(peers.lobbyPublishers());
            for (var pub : lobbyPubs) pub.beginStream();
            streaming = true;
            await(() -> lobbyGhosts() == 8, 900, "eight lobby ghosts");
            capture.frames(120);
            capture.tap(GLFW_KEY_ENTER); // AUTO ready: Enter hides the menu
            chapter("Names: walk to the middle");
            capture.key(GLFW_KEY_RIGHT, true);
            for (int i = 0; i < 400; i++) {
                var cam = GameServices.cameraOrNull();
                var p = cam == null ? null : cam.getFocusedSprite();
                if (p != null && p.getCentreX() >= 0xA8) break;
                capture.frame();
            }
            capture.key(GLFW_KEY_RIGHT, false);
            capture.frames(90);
            chapter("Names: line-up");
            for (int j = 0; j < 4; j++) {
                capture.key(GLFW_KEY_SPACE, true); capture.frames(8); capture.key(GLFW_KEY_SPACE, false);
                capture.frames(88);
            }
            chapter("Names: turn and back");
            capture.key(GLFW_KEY_LEFT, true); capture.frames(10); capture.key(GLFW_KEY_LEFT, false);
            capture.frames(80);
            capture.key(GLFW_KEY_RIGHT, true); capture.frames(10); capture.key(GLFW_KEY_RIGHT, false);
            capture.frames(120);
            chapter("Names: end");
            return;
        }
        if (!bots) {
            capture.frames(60);
            String[] hello = {"Chúc may mắn!", "Удачи!", "Καλή τύχη!", "화이팅!"};
            for (int i = 0; i < hello.length; i++) { peers.chat(i, hello[i]); capture.frames(40); }
            capture.frames(120);
        } else {
            capture.frames(120);
            capture.tap(GLFW_KEY_UP);
            capture.tap(GLFW_KEY_UP);
            chapter("Lobby pages");
            for (int i = 0; i < 40; i++) capture.tap(GLFW_KEY_RIGHT);
            capture.frames(60);
        }
        peers.startRound(window);
        chapter("Round countdown");
        await(() -> state().equals("RACING"), 1200, "the race launch");
        driving = true;
        await(() -> capture.engine().getCurrentGameMode() == GameMode.LEVEL, 1200, "ROM level");
        chapter("Race level");
        if (death) {
            await(() -> deathPhase >= 1, 900, "the death");
            chapter("Death");
            await(() -> deathPhase >= 3, 900, "the restart countdown");
            chapter("Restart countdown");
            await(() -> deathPhase >= 4, 600, "the restart go");
            chapter("Restart go");
            capture.frames(900);
            return;
        }
        await(() -> naturalFinish, 6000, "natural finish");
        chapter("Finish");
        await(() -> peers.roundEnded(), 60 * (window + 30), "round end");
        chapter("Round end");
        if (bots) { capture.frames(600); return; }
        await(() -> !peers.voteOptions().isEmpty(), 60 * 20, "vote offer");
        chapter("Vote");
        capture.frames(200);
        capture.tap(GLFW_KEY_2);
        chapter("Hero voted");
        await(() -> peers.voteResult() != null, 60 * 20, "vote result");
        chapter("Vote result");
        await(() -> peers.nextRoundSent(), 600, "next round");
        driving = false;
        movieOn = false;
        await(() -> state().equals("RACING"), 1200, "next race");
        chapter("Next race launch");
        capture.frames(600);
    }

    private void beforeRace(boolean death) {
        try {
            peers.tick();
            if (!driving || naturalFinish || capture.engine().getCurrentGameMode() != GameMode.LEVEL) return;
            Object coordinator = call(session, "coordinator");
            if (coordinator == null) return;
            Object runtime = field(session, "runtime");
            if (death && deathPhase < 4) {
                var camera = GameServices.cameraOrNull();
                var player = camera == null ? null : camera.getFocusedSprite();
                boolean hold = (boolean) call(coordinator, "holdGameplay");
                switch (deathPhase) {
                    case 0 -> {
                        if (!hold) capture.key(GLFW_KEY_RIGHT, true);
                        if (player != null && player.getDead()) { deathPhase = 1; capture.key(GLFW_KEY_RIGHT, false); }
                    }
                    case 1 -> {
                        deadFrames++;
                        if (deadFrames == 42) capture.key(GLFW_KEY_SPACE, true);
                        if (deadFrames == 44) { capture.key(GLFW_KEY_SPACE, false); deathPhase = 2; }
                    }
                    case 2 -> {
                        if (runtime != null && (int) call(runtime, "countdownDigit") > 0) deathPhase = 3;
                    }
                    case 3 -> {
                        if (runtime != null && (int) call(runtime, "countdownDigit") == 0) { deathPhase = 4; movieOn = true; movieFrame = 0; previous = null; }
                    }
                    default -> { }
                }
                if (deathPhase < 4) return;
            }
            if (!(boolean) call(coordinator, "holdGameplay")) movieOn = true;
            if (movieOn) {
                Bk2FrameInput current = movieFrame + 840 < movie.getFrameCount() ? movie.getFrame(movieFrame + 840)
                        : new Bk2FrameInput(0, 0, 0, false, 0, 0, false, "neutral");
                capture.input().setLogicalOverride(RecordedInputSnapshots.fromBk2(current, previous));
                previous = current;
                movieFrame++;
            }
        } catch (Exception failure) { throw new RuntimeException(failure); }
    }

    private void afterRace() {
        try {
            if (!driving || session == null) { extraState = "connected=" + peers.connectedCount(); return; }
            Object runtime = field(session, "runtime");
            int digit = runtime == null ? 0 : (int) call(runtime, "countdownDigit");
            if (runtime != null && !naturalFinish && movieOn && (boolean) call(runtime, "isAttemptFinished")) {
                naturalFinish = true;
                capture.input().clearLogicalOverride();
            }
            StringBuilder ghosts = new StringBuilder();
            var camera = GameServices.cameraOrNull();
            if (runtime != null && camera != null) {
                @SuppressWarnings("unchecked")
                var list = (List<com.openggf.mods.run.GhostPose>) call(runtime, "ghosts");
                for (var ghost : list) {
                    if (!ghost.slotId().startsWith("net:")) continue;
                    ghosts.append(' ').append(ghost.nameplate() == null ? "?" : ghost.nameplate().replace(' ', '_').replace(';', '_'))
                            .append('@').append(ghost.pose().centreX() - camera.getX()).append(':')
                            .append(ghost.pose().centreY() - camera.getY()).append(':')
                            .append(String.format(Locale.ROOT, "%.2f", ghost.opacity()));
                }
            }
            extraState = "movie=" + movieFrame + " death=" + deathPhase + " digit=" + digit + " finish=" + naturalFinish
                    + " rank=" + peers.liveRank() + " finishes=" + peers.sentFinishes()
                    + " cam=" + (camera == null ? "" : camera.getX() + ":" + camera.getY()) + " ghosts=" + ghosts.toString().trim().replace(' ', ';');
        } catch (Exception failure) { throw new RuntimeException(failure); }
    }

    // ------------------------------------------------------------------ lobby
    private static final String[] LOBBY_NAMES = {"Nguyễn Hoa", "Дмитрий", "소닉팬"};
    private static final int[] LOBBY_COLOURS = {0x04C2, 0x022E, 0x0A6E};
    private static int[] DELAYS = {24, 48, 72};
    private static int[] OFFSETS = {-0x30, 0x38, 0x70};
    private String[] botNames = LOBBY_NAMES;
    private int[] botColours = LOBBY_COLOURS;
    private final List<RaceClient> lobbyBots = new ArrayList<>();
    private final List<LobbyPosePublisher> lobbyPubs = new ArrayList<>();
    boolean namesRelay;

    private boolean safeLobbyRun() {
        try { return session != null && (boolean) call(session, "lobbyRunActive") && GameServices.cameraOrNull() != null; }
        catch (Exception e) { throw new RuntimeException(e); }
    }
    private final ArrayDeque<GhostFrame> history = new ArrayDeque<>();
    private boolean streaming;
    private RunArea area;

    private boolean names;

    /** names mode: all eight rivals spread in a line, the hero mid-line; jumps ripple outwards. */
    void namesLobby(Path root, String gameId) throws Exception {
        names = true;
        botNames = RIVALS.stream().map(PromoPeers.Rival::name).toArray(String[]::new);
        botColours = RIVALS.stream().mapToInt(PromoPeers.Rival::colour).toArray();
        // Offsets left to right; the delay grows with distance from the hero, so a jump ripples outwards.
        OFFSETS = new int[] {-0x90, 0x24, -0x6C, 0x48, -0x48, 0x6C, -0x24, 0x90};
        DELAYS = new int[8];
        for (int i = 0; i < 8; i++) DELAYS[i] = 6 + 8 * (Math.abs(OFFSETS[i]) / 0x24 - 1);
        lobby(root, gameId, false);
    }

    private void namesParade() throws Exception {
        for (RaceClient bot : lobbyBots) bot.sendControl(new ControlMessage.SetReady(true));
        capture.frames(20);
        capture.tap(GLFW_KEY_ENTER); // READY UP
        capture.frames(20);
        capture.tap(GLFW_KEY_ENTER); // hide the menu
        chapter("Names: walk to the middle");
        capture.key(GLFW_KEY_RIGHT, true);
        for (int i = 0; i < 400; i++) {
            var cam = GameServices.cameraOrNull();
            var p = cam == null ? null : cam.getFocusedSprite();
            if (p != null && p.getCentreX() >= 0xA8) break;
            capture.frame();
        }
        capture.key(GLFW_KEY_RIGHT, false);
        capture.frames(90);
        chapter("Names: line-up");
        for (int j = 0; j < 4; j++) {
            capture.key(GLFW_KEY_SPACE, true); capture.frames(8); capture.key(GLFW_KEY_SPACE, false);
            capture.frames(88);
        }
        chapter("Names: turn and back");
        capture.key(GLFW_KEY_LEFT, true); capture.frames(10); capture.key(GLFW_KEY_LEFT, false);
        capture.frames(80);
        capture.key(GLFW_KEY_RIGHT, true); capture.frames(10); capture.key(GLFW_KEY_RIGHT, false);
        capture.frames(120);
        chapter("Names: end");
    }

    void lobby(Path root, String gameId, boolean profile) throws Exception {
        area = LobbyAreas.forGame(gameId).area();
        int port;
        try (ServerSocket socket = new ServerSocket(0)) { port = socket.getLocalPort(); }
        Path settings = out.resolve("profile/saves/mods/time-attack/settings.txt");
        Files.createDirectories(settings.getParent());
        Files.writeString(settings, (profile ? "" : "displayName=" + HERO + "\nlookBase=" + String.format("%03X", HERO_LOOK) + "\n")
                + "hostPort=" + port + "\nminimap=true\n");
        String fp = fingerprint(root, gameId);
        capture.afterFrame(ignored -> { afterLobby(); record(); });
        Object scene = openScene();
        Object menu = field(scene, "state");
        if (profile) {
            chapter("Name prompt");
            capture.frames(50);
            typeName(HERO, 14);
            capture.frames(40);
            capture.tap(GLFW_KEY_ENTER);
            capture.frames(40);
        }
        chapter("Time Attack menu");
        capture.frames(30);
        for (int i = 0; i < 4 && !gameId.equals(call(menu, "currentGameId")); i++) { capture.tap(GLFW_KEY_RIGHT); capture.frames(6); }
        for (int i = 0; i < 3; i++) capture.tap(GLFW_KEY_DOWN);
        capture.tap(GLFW_KEY_RIGHT);
        for (int i = 0; i < 4; i++) capture.tap(GLFW_KEY_DOWN);
        capture.tap(GLFW_KEY_ENTER);
        await(() -> state().equals("LOBBY"), 1200, "the lobby");
        chapter("Lobby level loading");
        await(() -> capture.engine().getCurrentGameMode() == GameMode.LEVEL, 1200, "the lobby level");
        String invite = ((String) call(session, "lanInvite")).replace("HOST_IP", "127.0.0.1");
        DirectJoinAddress address = DirectJoinAddress.parse(invite, 0);
        for (int i = 0; i < botNames.length; i++) {
            PlayerIdentity identity = PlayerIdentity.loadOrCreate(out.resolve("bots/bot-" + i));
            String look = CharacterLooks.withBaseColour(gameId, "sonic", botColours[i]).encode();
            RaceClient client = RaceClient.connect(address.uri(), identity, botNames[i], look, fp,
                    address.certificateSha256(), address.hostFingerprint()).get(20, TimeUnit.SECONDS);
            lobbyBots.add(client);
            LobbyPosePublisher pub = new LobbyPosePublisher(client::sendBinary);
            lobbyPubs.add(pub);
            pub.beginStream();
            if (names) capture.frames(45); // stay inside the LAN host's per-address handshake rate
        }
        streaming = true;
        await(() -> lobbyGhosts() == botNames.length, 600, "lobby ghosts");
        if (names) { namesParade(); return; }
        capture.frames(200);
        chapter("Menu over the lobby level");
        capture.frames(60);
        if (profile) {
            // Focus order: READY, START, RULE, CHAT, PROFILE, LEAVE (players/history above).
            for (int i = 0; i < 4; i++) { capture.tap(GLFW_KEY_DOWN); capture.frames(6); }
            chapter("Profile focus");
            capture.frames(30);
            capture.tap(GLFW_KEY_ENTER);
            chapter("Profile page");
            capture.frames(40);
            for (int i = 0; i < 8; i++) { capture.tap(GLFW_KEY_LEFT); capture.frames(i < 7 ? 22 : 50); } // Classic -> Silver ... -> Ember, one per 150-BPM beat
            for (int i = 0; i < 5; i++) { capture.tap(GLFW_KEY_DOWN); capture.frames(5); }
            capture.frames(20);
            capture.tap(GLFW_KEY_ENTER); // SAVE
            chapter("Profile saved");
            capture.frames(60);
            for (int i = 0; i < 4; i++) { capture.tap(GLFW_KEY_UP); capture.frames(6); }
        }
        for (RaceClient bot : lobbyBots) bot.sendControl(new ControlMessage.SetReady(true));
        capture.frames(30);
        capture.tap(GLFW_KEY_ENTER); // READY UP
        capture.frames(40);
        chapter("Everyone ready");
        capture.tap(GLFW_KEY_ENTER); // hide the menu
        chapter("Menu hidden, running");
        capture.key(GLFW_KEY_RIGHT, true);
        for (int i = 0; i < 170; i++) {
            if (i % 45 == 10) capture.key(GLFW_KEY_SPACE, true);
            if (i % 45 == 20) capture.key(GLFW_KEY_SPACE, false);
            capture.frame();
        }
        capture.key(GLFW_KEY_SPACE, false);
        capture.key(GLFW_KEY_RIGHT, false);
        capture.key(GLFW_KEY_LEFT, true);
        capture.frames(130);
        capture.key(GLFW_KEY_LEFT, false);
        capture.frames(70);
        capture.tap(GLFW_KEY_ENTER); // menu back
        chapter("Menu back");
        capture.frames(50);
        capture.tap(GLFW_KEY_DOWN);  // START ROUND
        capture.frames(12);
        capture.tap(GLFW_KEY_SPACE);
        chapter("Round start hand-over");
        await(() -> state().equals("RACING"), 1200, "the race run");
        await(() -> capture.engine().getCurrentGameMode() == GameMode.LEVEL, 1200, "the race level");
        capture.frames(320);
        chapter("Race level");
    }

    private void afterLobby() {
        try {
            for (RaceClient bot : lobbyBots) bot.drainInbound();
            var camera = GameServices.cameraOrNull();
            var player = camera == null || capture.engine().getCurrentGameMode() != GameMode.LEVEL ? null : camera.getFocusedSprite();
            boolean lobbyLevel = session != null && (boolean) call(session, "lobbyRunActive");
            if (player != null && lobbyLevel) {
                history.addLast(new GhostFrame(player.getCentreX(), player.getCentreY(), player.getMappingFrame(),
                        player.getRenderHFlip(), player.getRenderVFlip(), false, player.getPriorityBucket(), player.isHighPriority()));
                while (history.size() > 120) history.removeFirst();
                if (streaming) {
                    List<GhostFrame> recent = List.copyOf(history);
                    for (int b = 0; b < lobbyPubs.size() && recent.size() > 0; b++) {
                        GhostFrame source = recent.get(Math.max(0, recent.size() - 1 - DELAYS[b]));
                        int x = Math.clamp(source.x() + OFFSETS[b], area.minX() + 0x18, area.maxX() + 0x120);
                        lobbyPubs.get(b).onFrame(new GhostFrame(x, source.y(), source.mappingFrame(),
                                !names && b == 1 ? !source.hFlip() : source.hFlip(), source.vFlip(), false,
                                source.priorityBucket(), source.highPriority()));
                    }
                }
            }
            extraState = "ghosts=" + lobbyGhosts() + " menu=" + (session != null && (boolean) call(session, "lobbyMenuShown"));
        } catch (Exception failure) { throw new RuntimeException(failure); }
    }

    @SuppressWarnings("unchecked")
    private int lobbyGhosts() {
        try {
            if (session == null) return 0;
            Object coordinator = call(session, "coordinator");
            if (coordinator == null) return 0;
            return ((List<Object>) call(coordinator, "lobbyGhosts")).size();
        } catch (Exception e) { throw new RuntimeException(e); }
    }

    // ------------------------------------------------------------------ plumbing
    static String fingerprint(Path root, String gameId) throws Exception {
        String file = switch (gameId) {
            case "s1" -> "Sonic The Hedgehog (W) (REV01) [!].gen";
            case "s2" -> "Sonic The Hedgehog 2 (W) (REV01) [!].gen";
            default -> "Sonic and Knuckles & Sonic 3 (W) [!].gen";
        };
        try (Rom rom = new Rom()) {
            if (!rom.open(root.resolve(file).toString())) throw new IOException(gameId + " ROM not available");
            return new DeterminismFingerprint(AppVersion.get(), rom.calculateChecksum()).asString();
        }
    }

    static Object field(Object target, String name) throws Exception {
        Class<?> type = target.getClass();
        while (type != null) {
            try {
                Field field = type.getDeclaredField(name);
                field.setAccessible(true);
                return field.get(target);
            } catch (NoSuchFieldException e) { type = type.getSuperclass(); }
        }
        throw new NoSuchFieldException(name);
    }

    static Object call(Object target, String name) throws Exception {
        var method = target.getClass().getDeclaredMethod(name);
        method.setAccessible(true);
        return method.invoke(target);
    }

    void close() throws Exception {
        capture.beforeFrame(ignored -> { });
        capture.afterFrame(ignored -> { });
        for (RaceClient bot : lobbyBots) try { bot.close(); } catch (Exception ignored) { }
        states.close();
        audio.close();
        pcm.close();
        video.close();
        if (!encoder.waitFor(60, TimeUnit.SECONDS)) encoder.destroyForcibly();
        capture.close();
        if (peers != null) peers.close();
    }

    public static void main(String[] args) throws Exception {
        String mode = args[0];
        Path out = Path.of(args[1]), root = Path.of(args[2]).toAbsolutePath();
        PromoCapture tool = new PromoCapture(out, root);
        boolean ok = false;
        try {
            if (mode.equals("namesrelay")) {
                tool.namesRelay = true;
                tool.race(root, Path.of(args[3]), 120, false, false, 9);
            } else if (mode.equals("race")) {
                tool.race(root, Path.of(args[3]), Integer.parseInt(args[4]), args[5].equals("death"),
                        args[6].equals("bots"), Integer.parseInt(args[7]));
            } else if (mode.equals("names")) {
                tool.namesLobby(root, args[3]);
            } else {
                tool.lobby(root, args[3], args.length > 4 && args[4].equals("profile"));
            }
            ok = true;
        } finally {
            try { tool.close(); } finally {
                Files.writeString(tool.out.resolve("result.txt"), "success=" + ok + "\nframes=" + tool.capture.frameNumber() + "\n");
            }
        }
        System.exit(0);
    }
}
