package com.openggf.tools;

import com.openggf.configuration.SonicConfiguration;
import com.openggf.configuration.SonicConfigurationService;
import com.openggf.control.InputHandler;
import com.openggf.game.MasterTitleScreen;
import com.openggf.graphics.TexturedQuadRenderer;
import org.lwjgl.BufferUtils;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.lang.reflect.Field;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

/**
 * Menu evolution promo (2026-10-29): records every frame of the OpenGGF 0.5 game-select title
 * ({@code MasterTitleScreen} at tag {@code v0.5.20260411}, {@code 77c6364ce}) under a scripted key
 * timeline.
 *
 * <p>Compatibility harness, recorded as such: 0.5 has no display-free context owner, so this
 * helper package carries a verbatim copy of d823ce643's {@code SurfacelessEglContext} (EGL setup
 * only). 0.5's screen sets its projection from a running {@code Engine}; with no Engine, the
 * recorder hands the same 320x224 orthographic matrix to the screen's own renderer by reflection.
 * Update/draw order and input edges follow 0.5's {@code GameLoop.step()} / {@code Engine.draw()}.
 * The screen, its PNG art, clouds, font and colours are 0.5's own; nothing is restyled. 0.5's
 * navigation sounds were TODO stubs, so this era is silent by construction.
 *
 * <p>Inputs: {@code <take-file> <output-dir> <s1-rom> <s2-rom> <s3k-rom> [ignored]}; take headers
 * {@code frames}, {@code preroll}; events {@code <frame> <LEFT|RIGHT|ENTER> [hold]}. Writes native
 * 320x224 PNG frames and events.csv. Run with surfaceless EGL and no DISPLAY/WAYLAND_DISPLAY,
 * from a scratch working directory (0.5 reads config.json from there, falling back to its
 * bundled defaults; nothing is saved).
 */
public final class V05TitleRecorder {
    private static final Map<String, Integer> KEYS = Map.of("LEFT", GLFW_KEY_LEFT, "RIGHT", GLFW_KEY_RIGHT,
            "ENTER", GLFW_KEY_ENTER);

    private V05TitleRecorder() { }

    public static void main(String[] args) throws Exception {
        if (!SurfacelessEglContext.requested() || System.getenv("DISPLAY") != null
                || System.getenv("WAYLAND_DISPLAY") != null)
            throw new IllegalStateException("Requires surfaceless EGL with DISPLAY and WAYLAND_DISPLAY unset");
        Path takeFile = Path.of(args[0]), out = Path.of(args[1]);
        int frames = 300, preroll = 30;
        List<int[]> events = new ArrayList<>();
        for (String raw : Files.readAllLines(takeFile)) {
            String line = raw.replaceAll("#.*", "").trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("frames=")) frames = Integer.parseInt(line.substring(7));
            else if (line.startsWith("preroll=")) preroll = Integer.parseInt(line.substring(8));
            else if (!line.contains("=")) {
                String[] p = line.split("\\s+");
                events.add(new int[] {Integer.parseInt(p[0]), KEYS.get(p[1]), p.length > 2 ? Integer.parseInt(p[2]) : 5});
            }
        }
        Path frameDir = Files.createDirectories(out.resolve("frames"));
        SonicConfigurationService config = SonicConfigurationService.getInstance();
        config.setConfigValue(SonicConfiguration.SONIC_1_ROM, Path.of(args[2]).toAbsolutePath().toString());
        config.setConfigValue(SonicConfiguration.SONIC_2_ROM, Path.of(args[3]).toAbsolutePath().toString());
        config.setConfigValue(SonicConfiguration.SONIC_3K_ROM, Path.of(args[4]).toAbsolutePath().toString());

        GLFWErrorCallback.createPrint(System.err).set();
        glfwInitHint(GLFW_PLATFORM, GLFW_PLATFORM_NULL);
        if (!glfwInit()) throw new IllegalStateException("Unable to initialize GLFW");
        List<String> log = new ArrayList<>(List.of("frame,kind,detail"));
        try (var egl = SurfacelessEglContext.create(320, 224, true)) {
            GL.createCapabilities();
            MasterTitleScreen screen = new MasterTitleScreen();
            screen.initialize();
            Field rf = MasterTitleScreen.class.getDeclaredField("renderer");
            rf.setAccessible(true);
            TexturedQuadRenderer renderer = (TexturedQuadRenderer) rf.get(screen);
            float[] projection = new org.joml.Matrix4f().ortho2D(0, 320, 0, 224).get(new float[16]);
            InputHandler input = new InputHandler();
            for (int i = 0; i < preroll; i++) { screen.update(input); input.update(); }
            List<int[]> releases = new ArrayList<>();
            ByteBuffer pixels = BufferUtils.createByteBuffer(320 * 224 * 4);
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
                screen.update(input);
                input.update();
                glViewport(0, 0, 320, 224);
                glClearColor(0, 0, 0, 1);
                glClear(GL_COLOR_BUFFER_BIT);
                renderer.setProjectionMatrix(projection);
                screen.draw();
                glFinish();
                pixels.clear();
                glReadPixels(0, 0, 320, 224, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
                BufferedImage img = new BufferedImage(320, 224, BufferedImage.TYPE_INT_RGB);
                for (int y = 0; y < 224; y++) for (int x = 0; x < 320; x++) {
                    int i = ((223 - y) * 320 + x) * 4;
                    img.setRGB(x, y, ((pixels.get(i) & 0xFF) << 16) | ((pixels.get(i + 1) & 0xFF) << 8) | (pixels.get(i + 2) & 0xFF));
                }
                ImageIO.write(img, "png", frameDir.resolve(String.format("%05d.png", f)).toFile());
            }
            screen.cleanup();
        } finally {
            glfwTerminate();
        }
        Files.write(out.resolve("events.csv"), log);
        System.out.println("recorded " + frames + " frames (0.5 title) to " + out);
    }
}
