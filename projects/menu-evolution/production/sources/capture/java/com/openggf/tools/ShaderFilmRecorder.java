package com.openggf.tools;

import com.openggf.Engine;
import com.openggf.control.InputHandler;
import com.openggf.game.GameServices;
import com.openggf.graphics.RgbaImage;
import com.openggf.graphics.ScreenshotCapture;
import com.openggf.graphics.shaderlib.DisplayShaderPickerController;
import com.openggf.graphics.shaderlib.DisplayShaderPresetRef;
import com.openggf.graphics.shaderlib.DisplayShaderSelectionModel;
import com.openggf.mods.scene.host.SceneSurface;
import com.openggf.sprites.playable.AbstractPlayableSprite;
import com.openggf.debug.playback.Bk2FrameInput;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.glFinish;

/**
 * Menu evolution promo (2026-10-29): records every frame of Sonic 2 Emerald Hill 1 with the
 * in-game display shader picker opened, navigated and closed by a scripted key timeline.
 *
 * <p>Purpose: a moving old/new comparison of the picker over real gameplay. The same source
 * compiles against {@code 2f9ca84b1} and {@code d823ce643}. {@link GameplayCaptureSession} owns
 * boot (real EHZ1 start, Sonic alone), stepping, the world render, EGL and the no-device audio
 * backend. The picker is each tree's production {@code DisplayShaderPickerController}, drawn by
 * that tree's own {@code Engine.renderDisplayShaderPickerOverlay()} through a draw-only Engine
 * facade (never initialised or run), as the trees' own OverlayDesignCaptureTool does. While the
 * picker is open gameplay is not stepped, matching the engine (modal picker frames skip
 * {@code GameLoop.step()}). The three library entries are display data only: nothing is scanned,
 * downloaded or activated.
 *
 * <p>Inputs: {@code <take-file> <output-dir> <s1> <s2-rom> <s3k> [ignored]}. Take headers:
 * {@code frames}, {@code preroll}, {@code run-from}/{@code run-to} (frames with RIGHT held), {@code brake=1}
 * (after the run, LEFT only while ground speed is still positive);
 * events: {@code <frame> <F8|UP|DOWN|ENTER|ESC> [hold]}. Writes native PNG frames, events.csv and
 * state.csv (player x/y per frame). Surfaceless EGL only, DISPLAY/WAYLAND_DISPLAY unset.
 */
public final class ShaderFilmRecorder {
    private static final Map<String, Integer> KEYS = Map.of("F8", GLFW_KEY_F8, "UP", GLFW_KEY_UP,
            "DOWN", GLFW_KEY_DOWN, "ENTER", GLFW_KEY_ENTER, "ESC", GLFW_KEY_ESCAPE, "RIGHT", GLFW_KEY_RIGHT,
            "LEFT", GLFW_KEY_LEFT);

    private ShaderFilmRecorder() { }

    public static void main(String[] args) throws Exception {
        if (!SurfacelessEglContext.requested() || System.getenv("DISPLAY") != null
                || System.getenv("WAYLAND_DISPLAY") != null)
            throw new IllegalStateException("Requires surfaceless EGL with DISPLAY and WAYLAND_DISPLAY unset");
        Path takeFile = Path.of(args[0]), out = Path.of(args[1]), rom = Path.of(args[3]).toAbsolutePath();
        int frames = 300, preroll = 60, runFrom = 0, runTo = 0, width = 320, brake = 0;
        List<int[]> events = new ArrayList<>();
        for (String raw : Files.readAllLines(takeFile)) {
            String line = raw.replaceAll("#.*", "").trim();
            if (line.isEmpty()) continue;
            if (line.contains("=")) {
                String[] kv = line.split("=", 2);
                int v;
                try { v = Integer.parseInt(kv[1].trim()); } catch (NumberFormatException e) { continue; }
                switch (kv[0].trim()) {
                    case "frames" -> frames = v;
                    case "preroll" -> preroll = v;
                    case "run-from" -> runFrom = v;
                    case "run-to" -> runTo = v;
                    case "width" -> width = v;
                    case "brake" -> brake = v;
                    default -> { }
                }
                continue;
            }
            String[] p = line.split("\\s+");
            events.add(new int[] {Integer.parseInt(p[0]), KEYS.get(p[1]), p.length > 2 ? Integer.parseInt(p[2]) : 5});
        }
        Path frameDir = Files.createDirectories(out.resolve("frames"));
        List<String> log = new ArrayList<>(List.of("frame,kind,detail"));
        List<String> state = new ArrayList<>(List.of("frame,picker_open,stepped,x,y,ground_speed"));
        var settings = new GameplayCaptureSession.Settings(width, "sonic", "", "off", null, null, null);
        try (var session = new GameplayCaptureSession(settings)) {
            session.boot(rom, 0, 0, settings);
            if (!(GameServices.audio().getBackend() instanceof com.openggf.audio.NullAudioBackend))
                throw new IllegalStateException("Capture must retain NullAudioBackend");
            for (int i = 0; i < preroll; i++) session.step(null);
            float[] projection = SceneSurface.projection(width, 224);
            Field instance = Engine.class.getDeclaredField("instance");
            instance.setAccessible(true);
            Object previousEngine = instance.get(null);
            var engine = new Engine();
            field(engine, "projectionWidth").setDouble(engine, width);
            field(engine, "realHeight").setDouble(engine, 224);
            System.arraycopy(projection, 0, (float[]) field(engine, "matrixBuffer").get(engine), 0, 16);
            var picker = new DisplayShaderPickerController(new DisplayShaderSelectionModel(List.of(
                    new DisplayShaderPresetRef(DisplayShaderPresetRef.Kind.GLSL, "crt/scanlines.glsl", Path.of("shaders/crt/scanlines.glsl")),
                    new DisplayShaderPresetRef(DisplayShaderPresetRef.Kind.GLSL, "crt/aperture-grille.glsl", Path.of("shaders/crt/aperture-grille.glsl")),
                    new DisplayShaderPresetRef(DisplayShaderPresetRef.Kind.GLSL, "lcd/handheld.glsl", Path.of("shaders/lcd/handheld.glsl")))),
                    GLFW_KEY_F8);
            field(engine, "displayShaderPickerController").set(engine, picker);
            Method draw = Engine.class.getDeclaredMethod("renderDisplayShaderPickerOverlay");
            draw.setAccessible(true);
            InputHandler input = new InputHandler();
            List<int[]> releases = new ArrayList<>();
            try {
                for (int f = 0; f < frames; f++) {
                    for (var it = releases.iterator(); it.hasNext(); ) {
                        int[] r = it.next();
                        if (r[0] == f) { input.handleKeyEvent(r[1], GLFW_RELEASE); log.add(f + ",release," + r[1]); it.remove(); }
                    }
                    for (int[] e : events) {
                        if (e[0] != f) continue;
                        input.handleKeyEvent(e[1], GLFW_PRESS);
                        log.add(f + ",press," + e[1]);
                        releases.add(new int[] {f + Math.max(1, e[2]), e[1]});
                    }
                    boolean wasOpen = picker.isOpen();
                    var action = picker.update(input, DisplayShaderPresetRef.OFF);
                    boolean modal = wasOpen || picker.isOpen()
                            || action.type() != DisplayShaderPickerController.ActionType.NONE;
                    if (action.type() != DisplayShaderPickerController.ActionType.NONE)
                        log.add(f + ",action," + action.type());
                    input.update();
                    if (!modal) {
                        int mask = f >= runFrom && f < runTo ? AbstractPlayableSprite.INPUT_RIGHT : 0;
                        // brake=1: after the run, hold LEFT only while Sonic still moves right (a skid to a stop).
                        if (brake != 0 && f >= runTo && session.player().getGSpeed() > 0)
                            mask = AbstractPlayableSprite.INPUT_LEFT;
                        session.step(new Bk2FrameInput(f, mask, 0, false, ""));
                    }
                    session.renderFrame();
                    GameServices.graphics().resetForFixedFunction();
                    if (picker.isOpen()) draw.invoke(engine);
                    GameServices.graphics().flushScreenSpace();
                    glFinish();
                    RgbaImage image = ScreenshotCapture.captureFramebuffer(width, 224);
                    ScreenshotCapture.savePNG(image, frameDir.resolve(String.format("%05d.png", f)));
                    var p = session.player();
                    state.add(f + "," + picker.isOpen() + "," + !modal + "," + p.getCentreX() + "," + p.getCentreY()
                            + "," + p.getGSpeed());
                }
            } finally {
                try { ((AutoCloseable) field(engine, "displayShaderPickerRenderer").get(engine)).close(); }
                catch (NoSuchFieldException oldOwner) { /* the pre-redesign picker has no separate renderer */ }
                instance.set(null, previousEngine);
            }
            if (!(GameServices.audio().getBackend() instanceof com.openggf.audio.NullAudioBackend))
                throw new IllegalStateException("Drawing replaced the no-device backend");
        }
        Files.write(out.resolve("events.csv"), log);
        Files.write(out.resolve("state.csv"), state);
        System.out.println("recorded " + frames + " frames (EHZ1 shader picker) to " + out);
    }

    private static Field field(Object owner, String name) throws ReflectiveOperationException {
        Field field = owner.getClass().getDeclaredField(name);
        field.setAccessible(true);
        return field;
    }
}
