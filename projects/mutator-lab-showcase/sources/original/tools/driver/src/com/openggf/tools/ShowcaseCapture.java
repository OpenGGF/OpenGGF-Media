package com.openggf.tools;

/*
 * ShowcaseCapture — scratch recording adapter for the complete Mutator Lab showcase
 * (task mutator-complete-showcase-20261010, source 379b6641323853f61851943fb7aadd5e7a389e01).
 *
 * Two stepping modes over the production GameplayCaptureSession boot/render path:
 *  - canonical (default): byte-for-byte the MutatorGameplayCaptureTool loop (session.step = one
 *    native tick per input frame via the logical override, presentOuterFrame, PNG per frame).
 *  - paced (-Dshowcase.paced=true): the interactive Engine order per presentation frame —
 *    held keys through the production InputHandler/InputBindingFactory (no logical override),
 *    UI fade update when the loop does not own it, GameLoop.stepPresentationFrame() (Mutator
 *    Game Speed pacing owner), Engine.presentOuterAudioFrame, one PNG and one 800-frame PCM
 *    packet per presentation frame. Never retimes, never edits speed or gameplay state.
 * Adds observe2.csv (lives, level frame counter, vint, admitted level/player/pacing policies,
 * checkpoint index, monitors, stage providers) and monitors.csv. Observation only.
 */
import com.openggf.Engine;
import com.openggf.InputBindingFactory;
import com.openggf.configuration.SonicConfiguration;
import com.openggf.control.InputHandler;
import com.openggf.debug.playback.*;
import com.openggf.game.CheckpointState;
import com.openggf.game.GameMode;
import com.openggf.game.GameServices;
import com.openggf.game.mutators.GameplayMutatorPacing;
import com.openggf.game.mutators.GameplayMutatorPolicySource;
import com.openggf.game.mutators.LevelMutatorPolicySource;
import com.openggf.game.session.SessionManager;
import com.openggf.game.session.WorldSessionPolicyAccess;
import com.openggf.graphics.ScreenshotCapture;
import com.openggf.level.objects.AbstractBadnikInstance;
import com.openggf.level.objects.AbstractMonitorObjectInstance;
import com.openggf.level.rings.LostRingObjectInstance;
import com.openggf.sprites.playable.AbstractPlayableSprite;
import com.openggf.sprites.playable.PlayableSpriteInternalAccess;
import com.openggf.tools.GameplayCaptureSession;
import com.openggf.tools.GameplayCaptureTool;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;
import static org.lwjgl.glfw.GLFW.GLFW_RELEASE;

public final class ShowcaseCapture {
    public static void main(String[] argv) throws Exception {
        var a = GameplayCaptureTool.Arguments.parse(argv);
        if (!"surfaceless-egl".equals(System.getProperty("openggf.headless.gl")))
            throw new IllegalArgumentException("surfaceless-egl required; no display fallback");
        boolean paced = Boolean.getBoolean("showcase.paced");
        Bk2Movie movie = a.input() == null ? null : new Bk2MovieLoader().loadMovieOrInputLog(a.input());
        int scriptFrames = movie == null ? 0 : Math.max(0, movie.getFrameCount() - a.inputStart());
        int total = a.frames() != null ? a.frames() : a.settle() + scriptFrames;
        Path out = a.outDir(), frames = out.resolve("frames");
        Files.createDirectories(frames);
        var settings = new GameplayCaptureSession.Settings(a.width(), a.mainCharacter(), a.sidekickCharacter(),
                a.donor(), null, a.startX(), a.startY(), a.emeralds(), a.titleCard(), a.completeSpecialStage(),
                a.vIntRunCount(), a.cameraXSub(), a.starPost(), a.rings(), a.reverseGravity());
        int zone = GameplayCaptureTool.ZoneIds.resolve(a.game(), a.zone());
        int dead = -1;
        try (var session = new GameplayCaptureSession(settings);
             var state = Files.newBufferedWriter(out.resolve("state.csv"), StandardCharsets.UTF_8);
             var obs = Files.newBufferedWriter(out.resolve("observe.csv"), StandardCharsets.UTF_8);
             var obs2 = Files.newBufferedWriter(out.resolve("observe2.csv"), StandardCharsets.UTF_8);
             var bads = Files.newBufferedWriter(out.resolve("badniks.csv"), StandardCharsets.UTF_8);
             var mons = Files.newBufferedWriter(out.resolve("monitors.csv"), StandardCharsets.UTF_8)) {
            bads.write("frame,class,x,y"); bads.newLine();
            mons.write("frame,class,x,y"); mons.newLine();
            if (a.mod() != null) session.applyMod(a.mod());
            if (a.audio()) session.enableAudio();
            session.boot(a.rom(), zone, a.act(), settings);
            var loop = session.loop();
            var config = GameServices.configuration();
            InputHandler input = null;
            int[] keys = null;
            if (paced) {
                input = new InputHandler(InputBindingFactory.supplier(config));
                loop.setInputHandler(input);
                keys = new int[] { config.getInt(SonicConfiguration.UP), config.getInt(SonicConfiguration.DOWN),
                        config.getInt(SonicConfiguration.LEFT), config.getInt(SonicConfiguration.RIGHT),
                        config.getInt(SonicConfiguration.P1_A), config.getInt(SonicConfiguration.P1_B),
                        config.getInt(SonicConfiguration.P1_C), config.getInt(SonicConfiguration.START) };
                if (input.hasLogicalOverride() || loop.externalFrameOrInputOwnerActive())
                    throw new IllegalStateException("paced capture requires interactive input ownership");
            }
            boolean[] held = new boolean[8];
            var audio = GameServices.audio();
            try (var capture = a.audio() ? audio.beginLiveCaptureAudio(a.fps()) : null;
                 var pcm = a.audio() ? new BufferedOutputStream(Files.newOutputStream(out.resolve("audio.pcm"))) : OutputStream.nullOutputStream()) {
                short[] samples = capture == null ? new short[0] : new short[capture.maxStereoFramesPerPacket() * 2];
                state.write(GameplayCaptureSession.stateHeader()); state.newLine();
                obs.write("frame,mode,rings,score,lost_rings,lost_rings_slotless,lost_rings_collectible,head_scale,gravity_pct,"
                        + "ringfall_pct,ringfall_cap,ringfall_full,rebound_pct,rebound_cap,badniks,x,y,xvel,yvel,air,hurt,dead,cam_x,cam_y,near_badnik,near_dx,near_dy");
                obs.newLine();
                obs2.write("frame,mode,paused,lives,level_frame,vint,stealth_body,stealth_appendage,stealth_effects,head_scale,"
                        + "no_rings,no_checkpoints,no_special,no_bonus,removed_monitors,speed_pct,audio_follows,checkpoint_idx,"
                        + "monitors,bonus_type,special_provider,rings,x,y,dead,pcm_frames,logical_override");
                obs2.newLine();
                for (int f = 0; f < total; f++) {
                    int si = f - a.settle();
                    Bk2FrameInput in = movie != null && si >= 0 && si < scriptFrames ? movie.getFrame(si + a.inputStart()) : null;
                    int pcmFrames = 0;
                    if (!paced) {
                        session.step(in);
                        if (a.audio()) {
                            loop.presentOuterFrame(false, false);
                            int n = capture.drainPresentationFrame(samples);
                            pcmFrames = n;
                            for (int i = 0; i < n * 2; i++) { pcm.write(samples[i] & 255); pcm.write((samples[i] >>> 8) & 255); }
                        }
                    } else {
                        int m = in == null ? 0 : in.p1InputMask(), act = in == null ? 0 : in.p1ActionMask();
                        boolean[] want = { (m & AbstractPlayableSprite.INPUT_UP) != 0, (m & AbstractPlayableSprite.INPUT_DOWN) != 0,
                                (m & AbstractPlayableSprite.INPUT_LEFT) != 0, (m & AbstractPlayableSprite.INPUT_RIGHT) != 0,
                                (act & 1) != 0, (act & 2) != 0, (act & 4) != 0, in != null && in.p1StartPressed() };
                        for (int k = 0; k < 8; k++) if (want[k] != held[k]) {
                            input.handleKeyEvent(keys[k], want[k] ? GLFW_PRESS : GLFW_RELEASE); held[k] = want[k];
                        }
                        if (input.hasLogicalOverride() || loop.externalFrameOrInputOwnerActive())
                            throw new IllegalStateException("canonical/external ownership appeared mid-capture");
                        // Same omitted-title presentation boundary as the canonical capture driver.
                        if (!a.titleCard()) GameServices.level().skipPendingInitialTitleCardPresentation();
                        var ui = GameServices.graphics().getUiRenderPipeline();
                        if (ui != null && !loop.ownsGameplayFadeLifecycle()) ui.updateFade();
                        loop.stepPresentationFrame();
                        if (a.audio()) {
                            Engine.presentOuterAudioFrame(loop, false, false);
                            int n = capture.drainPresentationFrame(samples);
                            pcmFrames = n;
                            for (int i = 0; i < n * 2; i++) { pcm.write(samples[i] & 255); pcm.write((samples[i] >>> 8) & 255); }
                        }
                    }
                    state.write(session.stateLine(f, in)); state.newLine();
                    obs.write(observe(session, f)); obs.newLine();
                    obs2.write(observe2(session, f, pcmFrames, input)); obs2.newLine();
                    var lmb = GameServices.levelOrNull();
                    var omb = lmb == null ? null : lmb.getObjectManager();
                    if (omb != null) {
                        for (var b : omb.activeObjectsOfType(AbstractBadnikInstance.class))
                            if (!b.isDestroyed()) { bads.write(f + "," + b.getClass().getSimpleName() + "," + b.getX() + "," + b.getY()); bads.newLine(); }
                        for (var b : omb.activeObjectsOfType(AbstractMonitorObjectInstance.class))
                            if (!b.isDestroyed()) { mons.write(f + "," + b.getClass().getSimpleName() + "," + b.getX() + "," + b.getY()); mons.newLine(); }
                    }
                    if (f >= a.captureFrom() && (f - a.captureFrom()) % a.every() == 0)
                        ScreenshotCapture.savePNG(render(session), frames.resolve(String.format(Locale.ROOT, "%05d.png", f)));
                    if (session.player().getDead()) {
                        if (dead < 0) dead = f;
                        if (a.stopOnDeath() && f >= dead + a.deathGrace()) break;
                    }
                }
                if (paced) for (int k = 0; k < 8; k++) if (held[k]) input.handleKeyEvent(keys[k], GLFW_RELEASE);
            }
            if (a.audio()) {
                Path raw = out.resolve("audio.pcm");
                var fmt = new javax.sound.sampled.AudioFormat(audio.outputSampleRate(), 16, 2, true, false);
                try (var ais = new javax.sound.sampled.AudioInputStream(Files.newInputStream(raw), fmt, Files.size(raw) / 4)) {
                    javax.sound.sampled.AudioSystem.write(ais, javax.sound.sampled.AudioFileFormat.Type.WAVE, out.resolve("audio.wav").toFile());
                }
                Files.delete(raw);
            }
        }
        System.out.println("done frames=" + total + " death=" + dead + " paced=" + paced + " out=" + out);
    }

    /**
     * session.render() plus Engine.drawSpecialStage's order for SPECIAL_STAGE frames after the entry fade-to-white
     * (GameplayCaptureSession draws only level planes there): screen-space camera origin, stage viewport,
     * provider draw, flush, fade pass. Presentation only.
     */
    private static com.openggf.graphics.RgbaImage render(GameplayCaptureSession session) {
        var loop = session.loop();
        var ss = loop.getCurrentGameMode() == GameMode.SPECIAL_STAGE ? loop.getActiveSpecialStageProvider() : null;
        if (ss == null || ss.isEntryFadeToWhiteActive()) return session.render();
        var graphics = GameServices.graphics();
        graphics.runPendingRenderThreadTasks();
        ss.setClearColor();
        org.lwjgl.opengl.GL11.glClear(org.lwjgl.opengl.GL11.GL_COLOR_BUFFER_BIT | org.lwjgl.opengl.GL11.GL_DEPTH_BUFFER_BIT);
        GameServices.camera().setX((short) 0);
        GameServices.camera().setY((short) 0);
        ss.setSpecialStageViewport(com.openggf.game.SpecialStageViewport.fromLogicalWidth(session.width()));
        ss.draw();
        graphics.flush();
        var ui = graphics.getUiRenderPipeline();
        if (ui != null) ui.renderFadePass();
        org.lwjgl.opengl.GL11.glFinish();
        return ScreenshotCapture.captureFramebuffer(session.width(), GameplayCaptureSession.HEIGHT);
    }

    private static String observe2(GameplayCaptureSession s, int f, int pcmFrames, InputHandler input) {
        var p = s.player();
        var loop = s.loop();
        var lm = GameServices.levelOrNull();
        var om = lm == null ? null : lm.getObjectManager();
        var world = SessionManager.getCurrentWorldSession();
        var lp = world == null ? null : WorldSessionPolicyAccess.getService(world, LevelMutatorPolicySource.class);
        var level = lp == null ? null : lp.policy();
        var gp = world == null ? null : WorldSessionPolicyAccess.getService(world, GameplayMutatorPolicySource.class);
        var pacing = world == null ? null : WorldSessionPolicyAccess.getService(world, GameplayMutatorPacing.class);
        var pol = p == null ? null : PlayableSpriteInternalAccess.mutatorPolicy(p);
        var gs = GameServices.gameStateOrNull();
        int monitors = 0;
        if (om != null) for (var m : om.activeObjectsOfType(AbstractMonitorObjectInstance.class)) if (!m.isDestroyed()) monitors++;
        String cp = "";
        if (lm != null && lm.getCheckpointState() instanceof CheckpointState c) cp = String.valueOf(c.getLastCheckpointIndex());
        var ctx = SessionManager.getCurrentGameplayMode();
        var bonus = ctx == null ? null : ctx.getActiveBonusStageProvider();
        String removed = level == null ? "" : level.removedMonitorContents().stream().map(Enum::name).sorted()
                .reduce((x, y) -> x + "|" + y).orElse("");
        var speed = gp == null ? null : gp.policy();
        return String.join(",", String.valueOf(f), String.valueOf(loop.getCurrentGameMode()), String.valueOf(loop.isPaused()),
                gs == null ? "" : String.valueOf(gs.getLives()), lm == null ? "" : String.valueOf(lm.getFrameCounter()),
                om == null ? "" : String.valueOf(om.getVblaCounter()),
                pol == null ? "" : String.valueOf(pol.suppressBody()), pol == null ? "" : String.valueOf(pol.suppressAppendage()),
                pol == null ? "" : String.valueOf(pol.suppressAttachedEffects()), pol == null ? "" : String.valueOf(pol.headScalePercent()),
                level == null ? "" : String.valueOf(level.noRings()), level == null ? "" : String.valueOf(level.noCheckpoints()),
                level == null ? "" : String.valueOf(level.noSpecialStages()), level == null ? "" : String.valueOf(level.noBonusStages()),
                removed, speed == null ? "" : String.valueOf(speed.gameplaySpeedPercent()),
                speed == null ? "" : String.valueOf(speed.audioFollowsSpeed()), cp, String.valueOf(monitors),
                bonus == null ? "" : String.valueOf(bonus.getActiveType()),
                loop.getCurrentGameMode() == GameMode.SPECIAL_STAGE && loop.getActiveSpecialStageProvider() != null
                        ? loop.getActiveSpecialStageProvider().getClass().getSimpleName() : "",
                p == null ? "" : String.valueOf(p.getRingCount()), p == null ? "" : String.valueOf(p.getCentreX()),
                p == null ? "" : String.valueOf(p.getCentreY()), p == null ? "" : String.valueOf(p.getDead() ? 1 : 0),
                String.valueOf(pcmFrames), input == null ? "canonical" : String.valueOf(input.hasLogicalOverride()));
    }

    // Copied from MutatorGameplayCaptureTool.observe (private there) so observe.csv keeps its schema.
    private static String observe(GameplayCaptureSession s, int f) {
        var p = s.player();
        var lm = GameServices.levelOrNull();
        var om = lm == null ? null : lm.getObjectManager();
        int lost = 0, slotless = 0, collectible = 0, badniks = 0, nearDx = 0, nearDy = 0;
        String near = null;
        String ringfall = ",,", rebound = ",";
        if (om != null) {
            for (var r : om.activeObjectsOfType(LostRingObjectInstance.class)) {
                if (r.isDestroyed()) continue;
                lost++; if (r.getSlotIndex() < 0) slotless++; if (r.isLostRingCollectible()) collectible++;
            }
            for (var b : om.activeObjectsOfType(AbstractBadnikInstance.class)) {
                if (b.isDestroyed()) continue;
                badniks++;
                if (p != null) {
                    int dx = b.getX() - p.getCentreX(), dy = b.getY() - p.getCentreY();
                    if (near == null || Math.abs(dx) + Math.abs(dy) < Math.abs(nearDx) + Math.abs(nearDy)) {
                        near = b.getClass().getSimpleName(); nearDx = dx; nearDy = dy;
                    }
                }
            }
            var svc = om.getObjectServices();
            var src = svc == null ? null : WorldSessionPolicyAccess.getService(svc.worldSession(), GameplayMutatorPolicySource.class);
            if (src != null) {
                var g = src.policy();
                ringfall = g.ringfallPercent() + "," + g.ringfallCap() + "," + (g.ringfallFullInventory() ? 1 : 0);
                rebound = g.defeatReboundPercent() + "," + g.defeatVerticalCap();
            }
        }
        var pol = p == null ? null : PlayableSpriteInternalAccess.mutatorPolicy(p);
        var gs = GameServices.gameStateOrNull();
        var cam = GameServices.camera();
        String mode = String.valueOf(s.loop().getCurrentGameMode());
        return f + "," + mode + "," + (p == null ? "" : p.getRingCount()) + "," + (gs == null ? "" : gs.getScore()) + ","
                + lost + "," + slotless + "," + collectible + "," + (pol == null ? "" : pol.headScalePercent()) + ","
                + (pol == null ? "" : pol.dryAirGravityPercent()) + "," + ringfall + "," + rebound + "," + badniks + ","
                + (p == null ? ",,,,,," : p.getCentreX() + "," + p.getCentreY() + "," + p.getXSpeed() + "," + p.getYSpeed() + ","
                + (p.getAir() ? 1 : 0) + "," + (p.isHurt() ? 1 : 0) + "," + (p.getDead() ? 1 : 0)) + ","
                + (cam == null ? "," : cam.getX() + "," + cam.getY()) + ","
                + (near == null ? ",," : near + "," + nearDx + "," + nearDy);
    }
}
