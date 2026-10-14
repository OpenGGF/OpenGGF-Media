package com.openggf.mods.code;

import com.openggf.Engine;
import com.openggf.GameLoop;
import com.openggf.configuration.*;
import com.openggf.debug.playback.*;
import com.openggf.game.*;
import com.openggf.game.mode.*;
import com.openggf.game.patch.*;
import com.openggf.game.session.*;
import com.openggf.graphics.ScreenshotCapture;
import com.openggf.io.*;
import com.openggf.tools.*;
import java.io.*;
import java.net.URLClassLoader;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.*;
import java.util.*;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

/**
 * Putt Putt Paradise promo capture with synchronized game audio, 2026-10-06 (Opus polish round).
 * Inputs: ROM, SDK-validated mod jar, fresh output directory, scenario
 * (ehz1-practice | ehz2-practice | local-match | online-host | online-guest), optional PNG stride
 * (default 1 = every 60 Hz row). The online scenarios are two separate JVMs joined by the mod's
 * real direct TCP room on localhost; capture_online.py steps them one row at a time over stdin
 * ("STEP n BUTTONS", "EVENT name", "QUIT") and reads one STATE line per command.
 *
 * Every outer row uses the production clocks: GameLoop.step for gameplay (title rows drive the
 * creator title provider), then exactly one Engine.presentOuterAudioFrame (outer-frame audio
 * presentation in its resolved mode, then the audio manager's frame finish), then exactly one
 * drain of that packet from a LiveCaptureAudioHandle. The live-recording lease is the one the
 * engine rebinds across presentation rebuilds (level loads, act changes), so one recording
 * spans the title, the course and any whole-shot restore. Audio therefore comes from the real headless
 * SMPS backend, row-synchronous with the PNG/state rows; pause and held rows present in the same
 * resolved mode the live engine would use. Logical Genesis input drives the course; the driver
 * never writes player/world state, hydrates from a trace or places sounds by timestamp.
 * The ordinary capture launcher deliberately disables creator code, so this wrapper registers
 * the single validated jar through ModContext, exactly like the earlier showcase capture.
 */
public final class GolfPromoCapture {
    private final Path out;
    private final GameLoop loop;
    private final GameplayFrameController controller;
    private final com.openggf.graphics.shaderlib.RewindVhsEffectPass rewindEffect =
            new com.openggf.graphics.shaderlib.RewindVhsEffectPass();
    private final BufferedWriter state, events;
    private final List<String> script = new ArrayList<>();
    private final Pcm gameplayAudio;
    private final int stride;
    private Bk2FrameInput previous;
    private int frame;
    private int lastLoft;

    /** 16-bit little-endian stereo PCM; one drained packet per presented outer row. */
    static com.openggf.audio.LiveCaptureAudioHandle lease;
    /** Read-only request log: which ROM music/SFX IDs the game actually asked for on each row. */
    static BufferedWriter requests; static String audioPhase = "boot"; static int audioRow;
    static final class Pcm implements Closeable {
        final Path path; final DataOutputStream raw; final short[] packet;
        final int rate; long frames; final List<Integer> rowFrames = new ArrayList<>();
        Pcm(Path path, int rate) throws IOException {
            this.path = path; this.rate = rate; packet = new short[lease.maxStereoFramesPerPacket() * 2 + 16];
            raw = new DataOutputStream(new BufferedOutputStream(Files.newOutputStream(path.resolveSibling(path.getFileName() + ".raw"))));
        }
        void presentAndDrain(GameLoop loop) throws IOException {
            Engine.presentOuterAudioFrame(loop, false, false);
            int count = lease.drainPresentationFrame(packet);
            var bytes = ByteBuffer.allocate(count * 4).order(ByteOrder.LITTLE_ENDIAN);
            for (int i = 0; i < count * 2; i++) bytes.putShort(packet[i]);
            raw.write(bytes.array()); frames += count; rowFrames.add(count);
        }
        @Override public void close() throws IOException {
            raw.close();
            Path rawPath = path.resolveSibling(path.getFileName() + ".raw");
            long dataBytes = Files.size(rawPath);
            try (var wav = new DataOutputStream(new BufferedOutputStream(Files.newOutputStream(path)))) {
                var header = ByteBuffer.allocate(44).order(ByteOrder.LITTLE_ENDIAN);
                header.put("RIFF".getBytes()).putInt((int) (36 + dataBytes)).put("WAVE".getBytes()).put("fmt ".getBytes())
                        .putInt(16).putShort((short) 1).putShort((short) 2).putInt(rate).putInt(rate * 4)
                        .putShort((short) 4).putShort((short) 16).put("data".getBytes()).putInt((int) dataBytes);
                wav.write(header.array());
                Files.copy(rawPath, wav);
            }
            Files.delete(rawPath);
            var distinct = new TreeSet<>(rowFrames);
            Files.writeString(path.resolveSibling(path.getFileName() + ".rows.json"),
                    "{\"rows\": " + rowFrames.size() + ", \"stereo_frames\": " + frames + ", \"rate\": " + rate
                            + ", \"frames_per_row\": " + distinct + "}\n");
        }
    }

    private GolfPromoCapture(Path out, GameLoop loop, int stride) throws Exception {
        this.out = out; this.loop = loop; this.stride = stride;
        if (GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_EFFECT)) rewindEffect.prewarm(320, 224, 320, 224);
        controller = GameServices.module().gameplayFrameController();
        if (controller == null) throw new IllegalStateException("Missing actual mod controller");
        Files.createDirectories(out.resolve("frames"));
        state = Files.newBufferedWriter(out.resolve("state.csv"));
        events = Files.newBufferedWriter(out.resolve("events.csv"));
        gameplayAudio = new Pcm(out.resolve("gameplay.wav"), GameServices.audio().outputSampleRate());
        state.write("rewind_intensity,rewind_speed,frame,character,act,width,x,y,xvel,yvel,gspeed,air,rolling,dead,cam_x,cam_y,stage,owner,turn,score,status,input,readiness,ready_owner,audio_frames\n");
        events.write("frame,event\n");
    }

    private Object call(Object object, String method) throws Exception { return object.getClass().getMethod(method).invoke(object); }
    private Object meter() throws Exception { return call(controller, "shotState"); }
    private Object match() throws Exception { return call(controller, "matchState"); }
    private Object readiness() throws Exception { return call(controller, "readinessState"); }
    private String stage() throws Exception { return call(meter(), "stage").toString(); }
    private String status() throws Exception { return call(match(), "status").toString(); }
    private String readyPhase() throws Exception { return call(readiness(), "phase").toString(); }
    private void event(String value) throws Exception { events.write(frame + "," + value + "\n"); events.flush(); System.out.println("EVENT " + frame + " " + value); }
    private void step(int frames, String buttons) throws Exception {
        script.add(frames + " " + buttons);
        Path fragment = out.resolve("fragment.txt");
        InputLogAuthorTool.author(frames + " " + buttons, fragment, "s2");
        var movie = new Bk2MovieLoader().loadMovieOrInputLog(fragment);
        for (int i = 0; i < frames; i++) {
            var input = movie.getFrame(i);
            audioPhase = "gameplay"; audioRow = frame;
            loop.getInputHandler().setLogicalOverride(RecordedInputSnapshots.fromBk2(input, previous));
            previous = input;
            GameServices.level().skipPendingInitialTitleCardPresentation();
            loop.step();
            gameplayAudio.presentAndDrain(loop);
            var p = GameServices.camera().getFocusedSprite();
            var m = match();
            String ledger = m == null ? "" : call(m, "golfers").toString().replace(',', ';');
            state.write(loop.liveRewindEffectIntensity() + "," + loop.liveRewindEffectSpeed() + "," + frame + "," + p.getCode() + "," + GameServices.level().getCurrentAct() + ","
                    + GameServices.camera().getWidth() + "," + p.getCentreX() + "," + p.getCentreY() + ","
                    + p.getXSpeed() + "," + p.getYSpeed() + "," + p.getGSpeed() + "," + p.getAir() + ","
                    + p.getRolling() + "," + p.getDead() + "," + GameServices.camera().getX() + ","
                    + GameServices.camera().getY() + "," + stage() + "," + (m == null ? -1 : call(m, "activePlayer")) + ","
                    + (m == null ? -1 : call(m, "turnSequence")) + ",\"" + ledger + "\"," + (m == null ? "" : call(m, "status")) + "," + buttons
                    + "," + readyPhase() + "," + call(readiness(), "owner") + "," + gameplayAudio.rowFrames.getLast() + "\n");
            if (frame % stride == 0) render(out.resolve("frames").resolve(String.format("%06d.png", frame / stride)));
            frame++;
        }
    }
    private void render(Path png) throws Exception {
        var graphics = GameServices.graphics();
        GameServices.level().setClearColor(); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        graphics.runPendingRenderThreadTasks();
        if (!controller.drawScene()) GameServices.level().drawWithSpritePriority(GameServices.sprites(), true);
        graphics.flush(); graphics.resetForFixedFunction(); controller.drawOverlay(); graphics.flushScreenSpace();
        if (GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_EFFECT)) {
            rewindEffect.apply(loop.liveRewindEffectIntensity(), loop.liveRewindEffectSpeed(),
                    com.openggf.graphics.shaderlib.RewindVhsEffectPass.REWIND_SCROLL_DIRECTION,
                    GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_TEAR_BANDS),
                    320, 224, graphics.getViewportX(), graphics.getViewportY(),
                    graphics.getViewportWidth(), graphics.getViewportHeight());
        }
        glFinish(); ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), png);
    }
    private static Object field(Object object, String name) throws Exception {
        var field = object.getClass().getDeclaredField(name); field.setAccessible(true); return field.get(object);
    }
    private static Object declared(Object object, String method) throws Exception {
        var m = object.getClass().getDeclaredMethod(method); m.setAccessible(true); return m.invoke(object);
    }
    /** Orchestrated online rows: one command, the requested rows, then one STATE line. */
    private void serve() throws Exception {
        try (var commands = new BufferedReader(new InputStreamReader(System.in))) {
            for (String line; (line = commands.readLine()) != null;) {
                String[] command = line.trim().split("\s+");
                if (command[0].equals("QUIT")) break;
                if (command[0].equals("EVENT")) event(command[1]);
                else if (command[0].equals("STEP")) step(Integer.parseInt(command[1]), command[2]);
                else throw new IllegalArgumentException("Unknown command " + line);
                Object room = call(controller, "roomState"), online = field(controller, "online");
                Object status = online == null ? null : declared(online, "shotStatus");
                Object m = match();
                System.out.println("STATE|frame=" + frame + "|ready=" + (room != null && (boolean) call(room, "ready"))
                        + "|held=" + (room == null || (boolean) call(room, "held")) + "|owner=" + (room == null ? -1 : call(room, "owner"))
                        + "|phase=" + (status == null ? "NONE" : call(status, "phase")) + "|stage=" + stage()
                        + "|readiness=" + readyPhase() + "|status=" + (m == null ? (room != null && (boolean) call(room, "ended") ? "ENDED" : "REMOTE") : call(m, "status"))
                        + "|turn=" + (room == null || call(room, "remoteTurnOpened") == null ? -1 : call(call(call(room, "remoteTurnOpened"), "id"), "turn"))
                        + "|hud=" + call(call(controller, "hudShotView"), "stage"));
                System.out.flush();
            }
        } finally { close(); lease.close(); }
    }
    /** Incoming golfer: let the handoff card read, then one fresh A row and its release. */
    private void readyIfHeld(int showRows) throws Exception {
        if (!readyPhase().equals("WAITING")) return;
        event("handoff-" + call(readiness(), "owner"));
        step(showRows, "-"); step(1, "A"); step(1, "-");
        if (!readyPhase().equals("NONE")) throw new IllegalStateException("Ready press was not accepted");
        event("ready-" + call(readiness(), "owner"));
        step(40, "-"); // TEE OFF! reads before the golfer aims.
    }
    private void shot(int direction, int loft, int power) throws Exception {
        lastLoft = (int) call(meter(), "elevationDegrees");
        event("aim-" + direction + "-" + loft + "-" + power);
        step(1, "-"); step(1, direction < 0 ? "L" : "R");
        if (loft > lastLoft) step(loft - lastLoft, "U");
        if (loft < lastLoft) step(lastLoft - loft, "D");
        lastLoft = loft;
        step(1, "-"); step(1, "A");
        if (stage().equals("SPIN")) { step(60, "-"); step(1, "A"); }
        step(power, "-"); step(1, "A"); event("shot-committed");
    }
    private void finishShot() throws Exception {
        for (int n = 0; n < 3700 && status().equals("PLAYING"); n++) {
            step(1, "-");
            if (stage().equals("AIM")) { event("next-turn"); return; }
        }
        if (!status().equals("PLAYING")) event("hole-complete");
        else throw new IllegalStateException("Shot did not terminate");
    }
    private void close() throws Exception {
        rewindEffect.dispose(); state.close(); events.close(); gameplayAudio.close(); requests.flush(); Files.deleteIfExists(out.resolve("fragment.txt"));
        var compressed = new ArrayList<String>();
        String last = null; int count = 0;
        for (String line : script) {
            int at = line.indexOf(' '); int n = Integer.parseInt(line.substring(0, at)); String input = line.substring(at + 1);
            if (!input.equals(last) && last != null) { compressed.add(count + " " + last); count = 0; }
            last = input; count += n;
        }
        if (last != null) compressed.add(count + " " + last);
        String recipe = String.join("\n", compressed) + "\n";
        Files.writeString(out.resolve("input.script"), recipe);
        InputLogAuthorTool.author(recipe, out.resolve("input.bk2"), "s2");
    }

    /** Title rows: the creator menu advances one presentation tick, then the same audio boundary. */
    private static final class Title implements Closeable {
        final TitleScreenProvider title; final com.openggf.control.InputHandler input = new com.openggf.control.InputHandler();
        final GameLoop loop; final Path frames; final Pcm audio; final BufferedWriter log; final int stride; int row;
        Title(GameLoop loop, Path out, int stride) throws IOException {
            this.loop = loop; this.stride = stride;
            title = GameServices.module().getTitleScreenProvider(); title.initialize();
            frames = Files.createDirectories(out.resolve("title-frames"));
            audio = new Pcm(out.resolve("title.wav"), GameServices.audio().outputSampleRate());
            log = Files.newBufferedWriter(out.resolve("title-events.csv")); log.write("frame,key\n");
        }
        void rows(int count) throws IOException { for (int i = 0; i < count; i++) row(-1); }
        void tap(int key, int after) throws IOException { row(key); rows(after); }
        void row(int key) throws IOException {
            audioPhase = "title"; audioRow = row;
            if (key >= 0) { input.handleKeyEvent(key, GLFW_PRESS); log.write(row + "," + key + "\n"); }
            input.refreshLogicalSnapshot(); title.update(input); input.update();
            if (key >= 0) input.handleKeyEvent(key, GLFW_RELEASE);
            audio.presentAndDrain(loop);
            if (row % stride == 0) {
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                GameServices.graphics().resetForFixedFunction(); title.draw(); GameServices.graphics().flushScreenSpace(); glFinish();
                ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), frames.resolve(String.format("%06d.png", row / stride)));
            }
            row++;
        }
        void focus(String field) throws Exception {
            var focus = title.getClass().getMethod("focusedField");
            for (int i = 0; i < 12 && !focus.invoke(title).toString().equals(field); i++) tap(GLFW_KEY_DOWN, 12);
            if (!focus.invoke(title).toString().equals(field)) throw new IllegalStateException("Menu field " + field);
        }
        @Override public void close() throws IOException { audio.close(); log.close(); }
    }

    public static void main(String[] args) throws Exception {
        Path rom = Path.of(args[0]), jar = Path.of(args[1]), out = Path.of(args[2]);
        String scenario = args[3]; int stride = args.length > 4 ? Integer.parseInt(args[4]) : 1;
        int act = scenario.equals("ehz2-practice") ? 1 : 0;
        String character = scenario.equals("ehz2-practice") ? "tails" : "sonic";
        boolean local = scenario.equals("local-match");
        boolean host = scenario.equals("online-host"), guest = scenario.equals("online-guest");
        if (guest) character = "tails";
        Files.createDirectories(out);
        try (var loader = new URLClassLoader(new java.net.URL[]{jar.toUri().toURL()}, GolfPromoCapture.class.getClassLoader());
             var assets = ModAssetRoot.jar(jar.getParent(), jar, ModInputLimits.production())) {
            var registration = new ModContext("putt-putt-paradise", "s2", assets);
            ((GgfMod)loader.loadClass("paradise.PuttPuttParadiseMod").getConstructor().newInstance()).register(registration);
            var plan = registration.freeze();
            var boundary = new ModFaultBoundary(Map.of(), new com.openggf.mods.ModRuntimeFindingStore(),
                    owners -> new com.openggf.mods.ModStateSaveResult.Saved(), owners -> { });
            GamePatch capturePatch = new GamePatch() {
                public String id() { return "capture:golf"; }
                public String displayName() { return "Explicit golf capture"; }
                public Set<LogicalRom> romPrerequisites() { return Set.of(LogicalRom.S2); }
                public List<String> providedMainCharacters() { return List.of(); }
                public String baseGameId() { return "s2"; }
                public boolean activatesFor(GameplayLaunchRequest request) { return true; }
                public GameModule apply(GameModule base, PatchContext context) {
                    GameModule result = new ModBackedGamePatch(plan, boundary).apply(base, context);
                    for (var patch : plan.explicitPatches()) result = patch.apply(result, context);
                    return result;
                }
            };
            var base = EngineContext.fromLegacySingletonsForBootstrap();
            var cfg = SonicConfigurationService.createStandalone(out.resolve("config"));
            cfg.setSessionOverride(SonicConfiguration.MAIN_CHARACTER_CODE, character);
            cfg.setSessionOverride(SonicConfiguration.SIDEKICK_CHARACTER_CODE, "");
            cfg.setSessionOverride(SonicConfiguration.DISPLAY_ASPECT, "NATIVE_4_3");
            cfg.setSessionOverride(SonicConfiguration.DISPLAY_SHADER_SELECTION, "OFF");
            cfg.setSessionOverride(SonicConfiguration.DISPLAY_COLOR_PROFILE, "RAW_RGB");
            cfg.setSessionOverride(SonicConfiguration.AUDIO_ENABLED, true);
            cfg.setSessionOverride(SonicConfiguration.TEST_MODE_ENABLED, false);
            cfg.setSessionOverride(SonicConfiguration.DEBUG_VIEW_ENABLED, false);
            cfg.setSessionOverride(SonicConfiguration.LIVE_REWIND_ENABLED, false);
            cfg.setSessionOverride(SonicConfiguration.LIVE_REWIND_VHS_EFFECT, true);
            cfg.setSessionOverride(SonicConfiguration.LIVE_REWIND_VHS_TEAR_BANDS, true);
            var resolver = new ModuleResolutionService(List.of(new RegisteredPatch(new PatchOwner.BuiltIn("capture:golf"),
                    "capture:golf", capturePatch, 0)), PatchEnablement.ALL_ENABLED,
                    LogicalRomResolver.fromRomManager(base.roms()), cfg);
            var engine = new EngineContext(cfg, base.graphics(), base.audio(), base.roms(), base.profiler(),
                    base.debugOverlay(), base.playbackDebug(), base.romDetection(), base.crossGameFeatures(), resolver);
            try (var boot = new HeadlessGameBoot(320, 224, engine)) {
                var loop = boot.boot(rom, 0, act);
                var audio = GameServices.audio();
                if (!audio.getBackend().getClass().getSimpleName().contains("Headless"))
                    throw new IllegalStateException("Real headless SMPS backend not installed: " + audio.getBackend());
                requests = Files.newBufferedWriter(out.resolve("audio-requests.csv"));
                requests.write("phase,row,class,id\n");
                audio.setRequestObserver((kind, id) -> {
                    try { requests.write(audioPhase + "," + audioRow + "," + kind + ",0x" + Integer.toHexString(id).toUpperCase() + "\n"); }
                    catch (IOException failure) { throw new UncheckedIOException(failure); }
                });
                lease = audio.beginLiveCaptureAudio(audio.presentationFrameRate());
                if (lease.sampleRate() != audio.outputSampleRate() || lease.frameRate() != 60)
                    throw new IllegalStateException("Unexpected capture clock " + lease.sampleRate() + "/" + lease.frameRate());
                System.out.println("AUDIO rate=" + audio.outputSampleRate() + " fps=" + audio.presentationFrameRate()
                        + " backend=" + audio.getBackend().getClass().getName());
                try (var title = new Title(loop, out, stride)) {
                    title.rows(100); // Banner drop, panel rise, ROM menu music.
                    if (local) {
                        title.tap(GLFW_KEY_DOWN, 30); title.tap(GLFW_KEY_ENTER, 40);
                        title.focus("PLAYER_TWO"); title.rows(16); title.focus("START"); title.rows(10);
                    } else if (host || guest) {
                        // Host Online Match / Join Online Match with the default 127.0.0.1:20502 room.
                        for (int i = 0; i < (host ? 2 : 3); i++) title.tap(GLFW_KEY_DOWN, 16);
                        title.tap(GLFW_KEY_ENTER, 30);
                        if (guest) title.tap(GLFW_KEY_RIGHT, 24);
                        title.focus("PORT"); title.rows(30); title.focus("START"); title.rows(10);
                    } else {
                        // Browse the four modes, peek at online Join setup, then choose Practice.
                        for (int i = 0; i < 3; i++) title.tap(GLFW_KEY_DOWN, 16);
                        title.tap(GLFW_KEY_ENTER, 70); title.tap(GLFW_KEY_ESCAPE, 20);
                        for (int i = 0; i < 3; i++) title.tap(GLFW_KEY_UP, 12);
                        title.tap(GLFW_KEY_ENTER, 30);
                        if (character.equals("tails")) title.tap(GLFW_KEY_RIGHT, 24);
                        title.focus("ACT"); if (act == 1) title.tap(GLFW_KEY_RIGHT, 24);
                        title.focus("START"); title.rows(10);
                    }
                    title.tap(GLFW_KEY_ENTER, 20);
                    if (!title.title.isExiting()) throw new IllegalStateException("Title did not launch");
                }
                GameServices.level().loadZoneAndAct(0, act); // The ordinary title-to-course load restores its ROM palettes.
                var capture = new GolfPromoCapture(out, loop, stride);
                try {
                    if (host || guest) { capture.serve(); return; }
                    capture.step(120, "-"); capture.event("course-ready");
                    if (local) {
                        int[][][] routes = {{{1,0,30},{1,40,60},{1,0,45},{1,0,60},{1,0,60},{1,0,60},{-1,0,2},{1,60,60},{1,20,60},{1,60,60}},
                                {{1,40,60},{1,0,60},{-1,0,15},{1,20,60},{1,60,30},{1,60,30},{-1,0,15},{1,75,60},{1,20,60},{1,20,30},{1,0,30},{1,40,60},{1,0,60},{1,60,60},{1,20,45},{-1,0,2},{1,0,30},{-1,0,2},{1,60,45},{1,75,45},{-1,0,4},{-1,0,4},{1,75,30},{1,40,60},{1,0,60},{1,0,60}}};
                        int[][] next = new int[2][2];
                        for (int shots = 0; shots < 120 && capture.status().equals("PLAYING"); shots++) {
                            capture.readyIfHeld(80);
                            int hole = (int) capture.call(capture.match(), "actIndex"), owner = (int) capture.call(capture.match(), "activePlayer");
                            var route = routes[hole];
                            if (next[hole][owner] >= route.length) throw new IllegalStateException("Route exhausted P" + (owner + 1) + " hole " + (hole + 1));
                            var s = route[next[hole][owner]++];
                            capture.shot(s[0], s[1], s[2]); capture.finishShot();
                            if (capture.status().equals("PLAYING") && capture.call(capture.meter(), "stage").toString().equals("AIM")
                                    && (int) capture.call(capture.match(), "actIndex") != hole) {
                                capture.event("hole-advanced");
                                for (int n = 0; n < 900 && !capture.readyPhase().equals("WAITING"); n++) capture.step(1, "-");
                            }
                        }
                        if (!capture.status().equals("COMPLETE")) throw new IllegalStateException("Local match did not complete");
                    } else {
                        if (act == 0) {
                            capture.shot(1, 0, 60); capture.step(100, "-");
                            if (!capture.stage().equals("WATCH")) throw new IllegalStateException("Intro shot already resolved");
                            capture.event("rewind-request");
                            capture.step(1, "S"); capture.step(1, "-"); capture.step(1, "D"); capture.step(1, "-"); capture.step(1, "A");
                            capture.step(110, "-");
                            var undo = ((com.openggf.game.rewind.RewindSnapshottable<?>) capture.controller).capture();
                            if (!capture.stage().equals("AIM") || !((java.util.List<?>)capture.call(capture.call(undo, "allowance"), "usedPerHole")).get(0).equals(1))
                                throw new IllegalStateException("Intro did not perform a whole-shot rewind");
                            capture.event("rewind-restored");
                        }
                        int[][] route = act == 0 ? new int[][]{{1,0,30},{1,40,60},{1,0,45},{1,0,60},{1,0,60},{1,0,60},{-1,0,2},{1,60,60},{1,20,60},{1,60,60}}
                                : new int[][]{{1,40,60},{1,0,60},{-1,0,15},{1,20,60},{1,60,30},{1,60,30},{-1,0,15},{1,75,60},{1,20,60},{1,20,30},{1,0,30},{1,40,60},{1,0,60},{1,60,60},{1,20,45},{-1,0,2},{1,0,30},{-1,0,2},{1,60,45},{1,75,45},{-1,0,4},{-1,0,4},{1,75,30},{1,40,60},{1,0,60},{1,0,60}};
                        for (var shot : route) { capture.shot(shot[0], shot[1], shot[2]); capture.finishShot(); if (!capture.status().equals("PLAYING")) break; }
                        if (!capture.status().equals("COMPLETE")) throw new IllegalStateException("Cold route did not complete");
                    }
                    capture.step(480, "-"); // Stage Clear jingle, scorecard drop and tally.
                    capture.event("capture-end");
                } finally { if (!host && !guest) { capture.close(); lease.close(); } }
            }
        }
    }
}
