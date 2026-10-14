package com.openggf.mods.code;

import com.openggf.GameLoop;
import com.openggf.configuration.*;
import com.openggf.debug.playback.*;
import com.openggf.game.*;
import com.openggf.game.mode.*;
import com.openggf.game.patch.*;
import com.openggf.game.session.*;
import com.openggf.graphics.*;
import com.openggf.io.*;
import com.openggf.tools.*;
import java.nio.file.*;
import java.net.URLClassLoader;
import java.io.*;
import java.util.*;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

/** Reproducible final-mod showcase, 2026-10-06. Inputs: ROM, validated jar, output, act, character, mode.
 * The ordinary capture launcher intentionally disables creator code, so this explicit capture
 * wrapper registers this jar through ModContext and supplies it to HeadlessGameBoot as its sole
 * capture patch. All subsequent course rows use GameLoop.step and logical Genesis input.
 * No world/player writes, trace hydration or simulated video frames are used.
 */
public final class GolfVisibilityProbe {
    private final Path out;
    private final GameLoop loop;
    private final GameplayFrameController controller;
    private final com.openggf.graphics.shaderlib.RewindVhsEffectPass rewindEffect =
            new com.openggf.graphics.shaderlib.RewindVhsEffectPass();
    private final BufferedWriter state;
    private final List<String> script = new ArrayList<>();
    private final BufferedWriter events;
    private Bk2FrameInput previous;
    private int frame;
    private int lastLoft;

    private GolfVisibilityProbe(Path out, GameLoop loop) throws Exception {
        this.out = out; this.loop = loop;
        if (GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_EFFECT)) {
            rewindEffect.prewarm(320, 224, 320, 224);
        }
        controller = GameServices.module().gameplayFrameController();
        if (controller == null) throw new IllegalStateException("Missing actual mod controller");
        Files.createDirectories(out.resolve("frames"));
        state = Files.newBufferedWriter(out.resolve("state.csv"));
        events = Files.newBufferedWriter(out.resolve("events.csv"));
        state.write("rewind_intensity,rewind_speed,frame,character,act,width,x,y,xvel,yvel,gspeed,air,rolling,dead,cam_x,cam_y,stage,owner,turn,score,status,input\n");
        events.write("frame,event\n");
    }

    private Object call(Object object, String method) throws Exception { return object.getClass().getMethod(method).invoke(object); }
    private Object meter() throws Exception { return call(controller, "shotState"); }
    private Object match() throws Exception { return call(controller, "matchState"); }
    private String stage() throws Exception { return call(meter(), "stage").toString(); }
    private String status() throws Exception { return call(match(), "status").toString(); }
    private void event(String value) throws Exception { events.write(frame + "," + value + "\n"); events.flush(); System.out.println("EVENT " + frame + " " + value); }
    private void step(int frames, String buttons) throws Exception {
        script.add(frames + " " + buttons);
        Path fragment = out.resolve("fragment.txt");
        InputLogAuthorTool.author(frames + " " + buttons, fragment, "s2");
        var movie = new Bk2MovieLoader().loadMovieOrInputLog(fragment);
        for (int i = 0; i < frames; i++) {
            var input = movie.getFrame(i);
            loop.getInputHandler().setLogicalOverride(RecordedInputSnapshots.fromBk2(input, previous));
            previous = input;
            GameServices.level().skipPendingInitialTitleCardPresentation();
            loop.step();
            var p = GameServices.camera().getFocusedSprite();
            if (java.util.Set.of(479,480,540,582,583,644,645,705,706,1377,1378).contains(frame)) {
                var scene = GameServices.level().captureScene(frame+90000, com.openggf.game.presentation.PlayerPresentationPose.nativePose());
                System.out.println("VISIBILITY frame="+frame+" code="+p.getCode()+" stage="+stage()+" anim="+p.getAnimationId()+" mapping="+p.getMappingFrame()+" hidden="+p.isHidden()+" blink="+p.shouldRefreshRenderFlagThisFrame()+" body="+(p.getSpriteRenderer()!=null)+" tail="+(p.getTailsTailsController()==null?"null":p.getTailsTailsController().captureRewindState())+" tiles="+scene.tiles().stream().filter(t->t.layer()==com.openggf.game.presentation.ScenePresentationFrame.Layer.PLAYER).toList());
            }
            var m = match();
            String ledger = m == null ? "" : call(m, "golfers").toString().replace(',', ';');
            state.write(loop.liveRewindEffectIntensity() + "," + loop.liveRewindEffectSpeed() + "," + frame + "," + p.getCode() + "," + GameServices.level().getCurrentAct() + ","
                    + GameServices.camera().getWidth() + "," + p.getCentreX() + "," + p.getCentreY() + ","
                    + p.getXSpeed() + "," + p.getYSpeed() + "," + p.getGSpeed() + "," + p.getAir() + ","
                    + p.getRolling() + "," + p.getDead() + "," + GameServices.camera().getX() + ","
                    + GameServices.camera().getY() + "," + stage() + "," + (m == null ? -1 : call(m, "activePlayer")) + ","
                    + (m == null ? -1 : call(m, "turnSequence")) + ",\"" + ledger + "\"," + (m == null ? "" : call(m, "status")) + "," + buttons + "\n");
            // Full motion at 30fps: two executed 60Hz presentation rows per PNG.
            if (frame % 2 == 0) render(out.resolve("frames").resolve(String.format("%06d.png", frame / 2)));
            frame++;
        }
    }
    private void render(Path png) throws Exception {
        var graphics = GameServices.graphics();
        GameServices.level().setClearColor(); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        graphics.runPendingRenderThreadTasks();
        if (!controller.drawScene()) GameServices.level().drawWithSpritePriority(GameServices.sprites(), true);
        graphics.flush(); graphics.resetForFixedFunction(); controller.drawOverlay(); graphics.flushScreenSpace();
        boolean effectPair = loop.liveRewindEffectIntensity() > 0 && !Files.exists(out.resolve("rewind-raw.png"));
        if (effectPair) {
            glFinish(); ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), out.resolve("rewind-raw.png"));
        }
        if (GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_EFFECT)) {
            rewindEffect.apply(loop.liveRewindEffectIntensity(), loop.liveRewindEffectSpeed(),
                    com.openggf.graphics.shaderlib.RewindVhsEffectPass.REWIND_SCROLL_DIRECTION,
                    GameServices.configuration().getBoolean(SonicConfiguration.LIVE_REWIND_VHS_TEAR_BANDS),
                    320, 224, graphics.getViewportX(), graphics.getViewportY(),
                    graphics.getViewportWidth(), graphics.getViewportHeight());
        }
        glFinish(); ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), png);
        if (effectPair) ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), out.resolve("rewind-vhs.png"));
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
        rewindEffect.dispose(); state.close(); events.close(); Files.deleteIfExists(out.resolve("fragment.txt"));
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
    private static void tap(TitleScreenProvider title, com.openggf.control.InputHandler input, int key) {
        input.handleKeyEvent(key, GLFW_PRESS); input.refreshLogicalSnapshot(); title.update(input); input.update();
        input.handleKeyEvent(key, GLFW_RELEASE); input.refreshLogicalSnapshot(); title.update(input); input.update();
    }
    public static void main(String[] args) throws Exception {
        Path rom = Path.of(args[0]), jar = Path.of(args[1]), out = Path.of(args[2]);
        int act = Integer.parseInt(args[3]); String character = args[4]; boolean local = args[5].equals("local");
        boolean smoke = args.length > 6 && args[6].equals("smoke");
        Files.createDirectories(out);
        try (var loader = new URLClassLoader(new java.net.URL[]{jar.toUri().toURL()}, GolfVisibilityProbe.class.getClassLoader());
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
            cfg.setSessionOverride(SonicConfiguration.AUDIO_ENABLED, false);
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
                var title = GameServices.module().getTitleScreenProvider(); title.initialize();
                var input = new com.openggf.control.InputHandler();
                Path titleFrames = out.resolve("title-frames"); Files.createDirectories(titleFrames);
                for (int i = 0; i < (smoke ? 2 : 240); i++) {
                    title.update(input); input.update();
                    if (i % 2 == 0) {
                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        GameServices.graphics().resetForFixedFunction(); title.draw(); GameServices.graphics().flushScreenSpace(); glFinish();
                        ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(320, 224), titleFrames.resolve(String.format("%06d.png", i / 2)));
                    }
                }
                if (local) tap(title, input, GLFW_KEY_DOWN);
                tap(title, input, GLFW_KEY_ENTER);
                if (character.equals("tails")) tap(title, input, GLFW_KEY_RIGHT);
                if (!local) {
                    tap(title, input, GLFW_KEY_DOWN); if (act == 1) tap(title, input, GLFW_KEY_RIGHT);
                }
                // Move through the real creator menu to Ready, retaining default rewind rules.
                var focus = title.getClass().getMethod("focusedField");
                while (!focus.invoke(title).toString().equals("START")) tap(title, input, GLFW_KEY_DOWN);
                tap(title, input, GLFW_KEY_ENTER);
                if (!title.isExiting()) throw new IllegalStateException("Title did not launch");
                GameServices.level().loadZoneAndAct(0, act); // The ordinary title-to-course load restores its ROM palettes.
                var capture = new GolfVisibilityProbe(out, loop);
                try {
                    capture.step(120, "-"); capture.event("course-ready");
                    if (smoke) { capture.shot(1, 0, 30); capture.step(180, "-"); }
                    else if (local) {
                        capture.shot(1, 0, 30); capture.finishShot(); capture.step(60, "-");
                        capture.shot(1, 40, 60); capture.finishShot(); capture.step(60, "-");
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
                        capture.step(120, "-");
                    }
                } finally { capture.close(); }
            }
        }
    }
}
