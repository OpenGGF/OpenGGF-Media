package com.openggf.tools;

import com.openggf.debug.playback.Bk2FrameInput;
import com.openggf.debug.playback.Bk2Movie;
import com.openggf.debug.playback.Bk2MovieLoader;
import com.openggf.game.GameServices;
import com.openggf.game.session.SessionManager;
import com.openggf.graphics.ScreenshotCapture;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

/**
 * Tries controller scripts from one cold-replayed prefix using engine-owned rewind state.
 * Origin: S&K bring-up, LRZ2 route authoring, 2026-09-24. No ROM/trace state is injected.
 * Inputs: ROM, game, zone, one-based act, width, main, sidekick, BK2, prefix length,
 * output directory, then one or more InputLogAuthorTool scripts. Each result includes
 * the complete prefix in its script/BK2/CSV; PNGs sample the candidate every30 frames.
 * The SOZ cold-route repair (2026-09-27) added read-only riding/standing owners
 * to distinguish actual contact from apparent overlap in sampled screenshots.
 * A chosen candidate still needs a fresh uninterrupted replay and route certification.
 */
@com.openggf.tests.rules.RequiresRom(com.openggf.tests.rules.SonicGame.SONIC_3K)
@org.junit.jupiter.api.condition.EnabledIfSystemProperty(named="soz.knuckles.author",matches=".+")
public final class TestSozKnucklesAuthor {
    @org.junit.jupiter.api.Test void author() throws Exception {
        run(Path.of(System.getProperty("s3k.rom.path")), "s3k", 8, 1,
            new GameplayCaptureSession.Settings(320,"knuckles","","off",null,null,null),
            Path.of(System.getProperty("soz.knuckles.input","src/test/resources/routes/s3k/soz1-cold-knuckles.bk2")),
            Integer.getInteger("soz.knuckles.prefix",0),Path.of(System.getProperty("soz.knuckles.author")),
            Files.readAllLines(Path.of(System.getProperty("soz.knuckles.candidates"))));
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 11) {
            throw new IllegalArgumentException("Usage: GameplayInputBranchTool ROM GAME ZONE ACT WIDTH "
                    + "MAIN SIDEKICK INPUT PREFIX OUT_DIR SCRIPT [SCRIPT ...]");
        }
        var settings = new GameplayCaptureSession.Settings(Integer.parseInt(args[4]), args[5],
                "none".equalsIgnoreCase(args[6]) ? "" : args[6], "off", null, null, null);
        run(Path.of(args[0]), args[1], GameplayCaptureTool.ZoneIds.resolve(args[1], args[2]),
                Integer.parseInt(args[3]) - 1, settings, Path.of(args[7]), Integer.parseInt(args[8]),
                Path.of(args[9]), List.of(args).subList(10, args.length));
    }

    static void run(Path rom, String game, int zone, int act, GameplayCaptureSession.Settings settings,
                    Path input, int prefix, Path output, List<String> candidates) throws Exception {
        var loader = new Bk2MovieLoader();
        var baseMovie = loader.loadMovieOrInputLog(input);
        String baseScript = prefixScript(baseMovie, prefix);
        if (candidates.isEmpty()) throw new IllegalArgumentException("No candidate scripts");
        if (settings.startX() != null || settings.startY() != null) {
            throw new IllegalArgumentException("Branch authoring requires a cold entry");
        }
        Files.createDirectories(output);
        try (var existing = Files.list(output)) {
            if (existing.findAny().isPresent()) {
                throw new IllegalArgumentException("Output directory is not empty: " + output);
            }
        }
        Path capture = System.getProperty("soz.knuckles.capture") == null ? null
                : Path.of(System.getProperty("soz.knuckles.capture"));
        int captureFrom = Integer.getInteger("soz.knuckles.captureFrom", 0);
        if (capture != null) Files.createDirectories(capture.resolve("frames"));
        var prefixRows = new StringBuilder(GameplayCaptureSession.stateHeader()).append('\n');
        try (var session = new GameplayCaptureSession(settings)) {
            GameServices.configuration().setSessionOverride(com.openggf.configuration.SonicConfiguration.S3K_SKIP_INTROS,false);
            session.boot(rom, zone, act, settings);
            GameServices.level().consumePendingInitialProcessSpritesPass();
            Files.writeString(output.resolve("placed.txt"), GameServices.level().getCurrentLevel().getObjects().stream()
                    .filter(o -> o.x() >= 5000 && o.x() < 6500).map(Object::toString).collect(java.util.stream.Collectors.joining("\n")));
            org.junit.jupiter.api.Assertions.assertEquals("knuckles",session.player().characterKey().persisted());
            for (int frame = 0; frame < prefix; frame++) {
                var pad = baseMovie.getFrame(frame);
                session.step(pad);
                var prefixPicture = session.render();
                if (capture != null && frame >= captureFrom)
                    ScreenshotCapture.savePNG(prefixPicture, capture.resolve("frames/frame-%06d.png".formatted(frame)));
                prefixRows.append(session.stateLine(frame, pad)).append('\n');
                if (session.player().getDead()) {
                    throw new IllegalStateException("Cold prefix died at input " + frame);
                }
            }
            var registry = SessionManager.getCurrentGameplayMode().getRewindRegistry();
            var checkpoint = registry.capture();
            var checkpointLevel = GameServices.level().getCurrentLevel();
            var checkpointMode = session.loop().getCurrentGameMode();
            if (checkpointMode != com.openggf.game.GameMode.LEVEL) {
                throw new IllegalStateException("Branch checkpoint must be in LEVEL mode: " + checkpointMode);
            }
            var previousInput = prefix == 0 ? null : baseMovie.getFrame(prefix - 1);
            var objects = new StringBuilder();
            for (var object : GameServices.level().getObjectManager().getActiveObjects()) {
                if (object.getSpawn() != null
                        && Math.abs(object.getX() - session.player().getCentreX()) <= 512) {
                    objects.append(object.getClass().getSimpleName()).append(' ')
                            .append(object.getX()).append(',').append(object.getY())
                            .append(" spawn=").append(object.getSpawn()).append('\n');
                }
            }
            Files.writeString(output.resolve("prefix-objects.txt"), objects, StandardOpenOption.CREATE_NEW);
            for (int i = 0; i < candidates.size(); i++) {
                if (!checkpointWorldIsActive(session, checkpointLevel, checkpointMode)) {
                    throw new IllegalStateException("Previous candidate left the checkpoint world or mode; "
                            + "start a fresh probe rather than restoring across a load boundary");
                }
                registry.restore(checkpoint);
                session.restoreInputHistory(previousInput);
                String script = baseScript + candidates.get(i) + '\n';
                Path stem = output.resolve("variant-" + i);
                Files.writeString(Path.of(stem + ".script"), script, StandardOpenOption.CREATE_NEW);
                InputLogAuthorTool.author(script, Path.of(stem + ".bk2"), game);
                var movie = loader.loadMovieOrInputLog(Path.of(stem + ".bk2"));
                var rows = new StringBuilder(prefixRows);
                var mechanism = new StringBuilder("frame,trigger5,door_y,top_bit,lrb_bit,pushing,trigger11,rock_x,rock_y,rock_phase\n");
                var contacts = new StringBuilder("frame,riding,standing\n");
                com.openggf.game.sonic3k.objects.SozEndBossVictoryRoute bossController = null;
                if (Boolean.getBoolean("soz.knuckles.boss")) {
                    var ctor=com.openggf.game.sonic3k.objects.SozEndBossVictoryRoute.class.getDeclaredConstructor(int.class,int.class,int.class,boolean.class);
                    ctor.setAccessible(true);
                    var parameters=candidates.get(i).split("#")[1].trim().split(" +");
                    bossController=ctor.newInstance(Integer.parseInt(parameters[0]),Integer.parseInt(parameters[1]),Integer.parseInt(parameters[2]),Boolean.parseBoolean(parameters[3]));
                    var target=com.openggf.game.sonic3k.objects.SozEndBossVictoryRoute.class.getDeclaredMethod("targetCapsule");
                    target.setAccessible(true);target.invoke(bossController);
                }
                var authoredTail = new ArrayList<Bk2FrameInput>();
                var bossRows = new StringBuilder("frame,x,y,hp,capsule,zone,act,boss_x,boss_y\n");
                for (int frame = prefix; frame < movie.getFrameCount(); frame++) {
                    var pad = bossController == null ? movie.getFrame(frame) : bossController.input(frame-prefix,session.player());
                    authoredTail.add(pad);
                    session.step(pad);
                    var picture = session.render();
                    if (capture != null && frame >= captureFrom)
                        ScreenshotCapture.savePNG(picture, capture.resolve("frames/frame-%06d.png".formatted(frame)));
                    rows.append(session.stateLine(frame, pad)).append('\n');
                    if (bossController != null) {
                        var bosses = GameServices.level().getObjectManager().activeObjectsOfType(com.openggf.game.sonic3k.objects.SozEndBossInstance.class);
                        var caps = GameServices.level().getObjectManager().activeObjectsOfType(com.openggf.game.sonic3k.objects.SozEndBossEggCapsule.class);
                        bossRows.append(frame).append(',').append(session.player().getCentreX()).append(',').append(session.player().getCentreY())
                            .append(',').append(bosses.isEmpty()?-1:bosses.getFirst().getCollisionProperty()).append(',').append(com.openggf.game.sonic3k.objects.SozColdRouteObservations.capsuleOpened())
                            .append(',').append(GameServices.level().getCurrentZone()).append(',').append(GameServices.level().getCurrentAct()).append(',').append(bosses.isEmpty()?-1:bosses.getFirst().getX()).append(',').append(bosses.isEmpty()?-1:bosses.getFirst().getY()).append('\n');
                    }
                    appendContacts(contacts, frame, session);
                    if (session.player().isHurt() && session.player().getInvulnerableFrames() >= 0x77) {
                        for (var nearby : GameServices.level().getObjectManager().getActiveObjects()) {
                            if (Math.abs(nearby.getX()-session.player().getCentreX()) < 100
                                    && Math.abs(nearby.getY()-session.player().getCentreY()) < 100)
                                System.out.printf("DAMAGE frame=%d player=%d,%d object=%s %d,%d%n", frame,
                                    session.player().getCentreX(),session.player().getCentreY(),nearby.getClass().getSimpleName(),nearby.getX(),nearby.getY());
                        }
                    }
                    mechanism.append(frame).append(',').append(com.openggf.game.sonic3k.runtime.SozZoneRuntimeState.trigger(5)).append(',');
                    for (var obj : GameServices.level().getObjectManager().getActiveObjects()) {
                        if (obj instanceof com.openggf.game.sonic3k.objects.SozDoorObjectInstance && obj.getSpawn().subtype() == 5)
                            mechanism.append(obj.getY());
                    }
                    mechanism.append(',').append(session.player().getTopSolidBit()).append(',')
                            .append(session.player().getLrbSolidBit()).append(',').append(session.player().getPushing())
                            .append(',').append(com.openggf.game.sonic3k.runtime.SozZoneRuntimeState.trigger(11)).append(',');
                    for(var obj:GameServices.level().getObjectManager().getActiveObjects()) {
                        if(obj instanceof com.openggf.game.sonic3k.objects.SozPushableRockObjectInstance
                                && obj.getSpawn().x()==18288) {
                            var phase=obj.getClass().getDeclaredField("phase");phase.setAccessible(true);
                            mechanism.append(obj.getX()).append(',').append(obj.getY()).append(',').append(phase.getInt(obj));
                        }
                    }
                    mechanism.append('\n');
                    boolean terminal = session.player().getDead()
                            || !checkpointWorldIsActive(session, checkpointLevel, checkpointMode);
                    if ((frame - prefix) % 30 == 0 || frame == movie.getFrameCount() - 1 || terminal) {
                        ScreenshotCapture.savePNG(picture, Path.of(stem + "-" + frame + ".png"));
                        System.out.printf("variant=%d input=%d x=%d y=%d dead=%s%n", i, frame,
                                session.player().getCentreX(), session.player().getCentreY(),
                                session.player().getDead());
                    }
                    if (terminal) break;
                }
                if (bossController != null) {
                    var tailMovie=new Bk2Movie(null,"",java.util.Map.of(),authoredTail,0);
                    String actual=baseScript+prefixScript(tailMovie,authoredTail.size());
                    Files.writeString(Path.of(stem+".script"),actual);
                    InputLogAuthorTool.author(actual,Path.of(stem+".bk2"),game);
                    Files.writeString(Path.of(stem+"-boss.csv"),bossRows);
                }
                Files.writeString(Path.of(stem + ".csv"), rows, StandardOpenOption.CREATE_NEW);
                Files.writeString(Path.of(stem + "-contacts.csv"), contacts, StandardOpenOption.CREATE_NEW);
                Files.writeString(Path.of(stem + "-mechanism.csv"), mechanism, StandardOpenOption.CREATE_NEW);
            }
        }
    }

    private static void appendContacts(StringBuilder rows, int frame, GameplayCaptureSession session) {
        var objects = GameServices.level().getObjectManager();
        var player = session.player();
        var riding = objects.getRidingObject(player);
        rows.append(frame).append(',');
        if (riding != null) {
            rows.append(riding.getClass().getSimpleName()).append('@')
                    .append(riding.getX()).append(':').append(riding.getY());
        }
        rows.append(',');
        for (var object : objects.getActiveObjects()) {
            // Non-solid display siblings can share a spawn-derived latch key with
            // their parent. Report only physical solid candidates, not that alias.
            if (object instanceof com.openggf.level.objects.SolidObjectProvider
                    && objects.hasObjectStandingBit(player, object)) {
                rows.append(object.getClass().getSimpleName()).append('@')
                        .append(object.getX()).append(':').append(object.getY()).append(';');
            }
        }
        rows.append('\n');
    }

    /**
     * A giant-ring special stage changes GameLoop mode while retaining the outgoing
     * Level object. Its active mode is outside this gameplay registry checkpoint;
     * restoring that registry alone would mix worlds. Stop at either boundary.
     */
    static boolean checkpointWorldIsActive(GameplayCaptureSession session,
            com.openggf.level.Level level, com.openggf.game.GameMode mode) {
        return GameServices.level().getCurrentLevel() == level
                && session.loop().getCurrentGameMode() == mode;
    }

    static String prefixScript(Bk2Movie movie, int prefix) {
        if (prefix < 0 || prefix > movie.getFrameCount()) {
            throw new IllegalArgumentException("Prefix outside input movie: " + prefix);
        }
        var result = new StringBuilder();
        String previous = null;
        int count = 0;
        for (int i = 0; i < prefix; i++) {
            var frame = movie.getFrame(i);
            if (frame.debugModeTogglePressed() || frame.debugShiftDown() || frame.debugControlDown()
                    || frame.debugAltDown() || frame.debugSuperDown()) {
                throw new IllegalArgumentException("Debug input is not controller-only: " + i);
            }
            String buttons = buttons(frame.p1InputMask(), frame.p1ActionMask(), frame.p1StartPressed())
                    + " / " + buttons(frame.p2InputMask(), frame.p2ActionMask(), frame.p2StartPressed());
            if (!buttons.equals(previous) && count != 0) {
                result.append(count).append(' ').append(previous).append('\n');
                count = 0;
            }
            previous = buttons;
            count++;
        }
        if (count != 0) result.append(count).append(' ').append(previous).append('\n');
        return result.toString();
    }

    private static String buttons(int directions, int actions, boolean start) {
        var held = new ArrayList<String>();
        String[] directionNames = {"U", "D", "L", "R"};
        String[] actionNames = {"A", "B", "C"};
        for (int i = 0; i < directionNames.length; i++) {
            if ((directions & (1 << i)) != 0) held.add(directionNames[i]);
        }
        for (int i = 0; i < actionNames.length; i++) {
            if ((actions & (1 << i)) != 0) held.add(actionNames[i]);
        }
        if (start) held.add("S");
        return held.isEmpty() ? "-" : String.join("+", held);
    }
}
