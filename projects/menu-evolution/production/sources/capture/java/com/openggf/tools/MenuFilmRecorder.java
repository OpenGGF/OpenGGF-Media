package com.openggf.tools;

import com.openggf.ModSubsystem;
import com.openggf.configuration.SonicConfiguration;
import com.openggf.configuration.SonicConfigurationService;
import com.openggf.control.InputHandler;
import com.openggf.game.LegalDisclaimerScreen;
import com.openggf.game.MasterTitleScreen;
import com.openggf.game.NativeModNoticeScreen;
import com.openggf.graphics.FadeManager;
import com.openggf.graphics.ScreenshotCapture;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

/**
 * Menu evolution promo (2026-10-29): records every presentation frame of a real engine menu
 * driven by a scripted key timeline, for a moving old/new comparison film.
 *
 * <p>Purpose: one native-resolution PNG per 60 Hz frame plus {@code events.csv} (every scripted
 * key edge and every UI audio cue the hub emitted, with its frame). The same source compiles
 * unchanged against the pre-redesign tree ({@code 2f9ca84b1}) and the delivered menus
 * ({@code d823ce643}); both expose the hub constructor with an {@code AudioSink}, the mod manager
 * factory and the startup notices used here. Nothing is restyled: each frame is the production
 * {@code draw()} of that tree.
 *
 * <p>Inputs: {@code <take-file> <output-dir> <s1-rom> <s2-rom> <s3k-rom> [mods-dir]}. The take file
 * holds {@code key=value} headers ({@code setup}, {@code width}, {@code frames}, {@code preroll},
 * {@code realtime-ms}) and {@code <frame> <KEY> [hold-frames]} events. Setups: {@code hub},
 * {@code hub-missing-s2} (S2 points at an absent file; {@code roms.directory} is a synthetic folder of
 * empty placeholder files, so the locator lists no real ROMs or user paths), {@code mods} (copies of
 * the mods directory installed through the production boot loader), {@code legal},
 * {@code native-notice}. ROMs are read in place by absolute path and never copied.
 *
 * <p>Linux only: surfaceless EGL with DISPLAY/WAYLAND_DISPLAY unset; fails before any boot
 * otherwise. Audio is never opened: cues are logged, not played. Scratch configuration, mod copies
 * and the synthetic folder are deleted on exit.
 */
public final class MenuFilmRecorder {
    private record Event(int frame, int key, int hold) { }

    private static final Map<String, Integer> KEYS = Map.ofEntries(
            Map.entry("UP", GLFW_KEY_UP), Map.entry("DOWN", GLFW_KEY_DOWN),
            Map.entry("LEFT", GLFW_KEY_LEFT), Map.entry("RIGHT", GLFW_KEY_RIGHT),
            Map.entry("ENTER", GLFW_KEY_ENTER), Map.entry("ESC", GLFW_KEY_ESCAPE),
            Map.entry("SPACE", GLFW_KEY_SPACE), Map.entry("TAB", GLFW_KEY_TAB),
            Map.entry("F1", GLFW_KEY_F1), Map.entry("BACKSPACE", GLFW_KEY_BACKSPACE));

    private static final List<Path> OWNED = new ArrayList<>();
    private static final List<String> LOG = new ArrayList<>();
    private static int currentFrame = -1;

    private MenuFilmRecorder() { }

    public static void main(String[] args) throws Exception {
        if (args.length < 5) throw new IllegalArgumentException(
                "usage: MenuFilmRecorder <take-file> <output-dir> <s1-rom> <s2-rom> <s3k-rom> [mods-dir]");
        if (!SurfacelessEglContext.requested() || System.getenv("DISPLAY") != null
                || System.getenv("WAYLAND_DISPLAY") != null)
            throw new IllegalStateException("Requires surfaceless EGL with DISPLAY and WAYLAND_DISPLAY unset");
        Path takeFile = Path.of(args[0]);
        Path out = Path.of(args[1]);
        Path s1 = Path.of(args[2]).toAbsolutePath(), s2 = Path.of(args[3]).toAbsolutePath(),
                s3k = Path.of(args[4]).toAbsolutePath();
        Path modsSource = args.length > 5 ? Path.of(args[5]) : null;
        for (Path rom : List.of(s1, s2, s3k))
            if (!Files.isRegularFile(rom)) throw new IllegalArgumentException("Missing ROM " + rom);
        if (Files.exists(out.resolve("frames"))) throw new IllegalArgumentException("Output exists: " + out);

        Map<String, String> head = new LinkedHashMap<>();
        List<Event> events = new ArrayList<>();
        for (String raw : Files.readAllLines(takeFile)) {
            String line = raw.replaceAll("#.*", "").trim();
            if (line.isEmpty()) continue;
            if (line.contains("=")) { String[] kv = line.split("=", 2); head.put(kv[0].trim(), kv[1].trim()); continue; }
            String[] p = line.split("\\s+");
            Integer key = KEYS.get(p[1]);
            if (key == null) throw new IllegalArgumentException("Unknown key " + p[1]);
            events.add(new Event(Integer.parseInt(p[0]), key, p.length > 2 ? Integer.parseInt(p[2]) : 5));
        }
        String setup = head.getOrDefault("setup", "hub");
        int width = Integer.parseInt(head.getOrDefault("width", "320"));
        int frames = Integer.parseInt(head.getOrDefault("frames", "300"));
        int preroll = Integer.parseInt(head.getOrDefault("preroll", "60"));
        int realtime = Integer.parseInt(head.getOrDefault("realtime-ms", "8"));
        Path frameDir = Files.createDirectories(out.resolve("frames"));

        GLFWErrorCallback.createPrint(System.err).set();
        glfwInitHint(GLFW_PLATFORM, GLFW_PLATFORM_NULL);
        try {
            if (!glfwInit()) throw new IllegalStateException("Unable to initialize GLFW");
        } finally {
            glfwInitHint(GLFW_PLATFORM, GLFW_ANY_PLATFORM);
        }
        try (var egl = SurfacelessEglContext.create(width, 224, true)) {
            GL.createCapabilities();
            float[] projection = new org.joml.Matrix4f().ortho2D(0, width, 0, 224).get(new float[16]);
            Path temp = owned(Files.createTempDirectory("menu-film"));
            SonicConfigurationService config = SonicConfigurationService.createStandalone(temp);
            config.setConfigValue(SonicConfiguration.TEST_MODE_ENABLED, false);
            config.setConfigValue(SonicConfiguration.SONIC_1_ROM, s1.toString());
            config.setConfigValue(SonicConfiguration.SONIC_2_ROM, s2.toString());
            config.setConfigValue(SonicConfiguration.SONIC_3K_ROM, s3k.toString());
            config.setConfigValue(SonicConfiguration.ROMS_DIRECTORY, temp.resolve("no-roms").toString());
            com.openggf.configuration.PendingRestart.captureAtStart(config);
            InputHandler input = new InputHandler(com.openggf.InputBindingFactory.supplier(config));

            Frame draw;
            Runnable update;
            Runnable cleanup = () -> { };
            switch (setup) {
                case "legal", "native-notice" -> {
                    FadeManager fades = new FadeManager();
                    if (setup.equals("legal")) {
                        LegalDisclaimerScreen legal = new LegalDisclaimerScreen(fades);
                        legal.initialize();
                        legal.setViewportWidth(width);
                        legal.setProjectionMatrix(projection);
                        update = () -> { fades.update(); legal.update(input); };
                        draw = legal::draw;
                    } else {
                        NativeModNoticeScreen notice = new NativeModNoticeScreen(fades,
                                com.openggf.mods.NativeUnsupportedMods.noticeLines(
                                        List.of("Sonic Echoes", "Starfall Frontier", "Infinite Sonic"), Integer.MAX_VALUE));
                        notice.initialize();
                        notice.setViewportWidth(width);
                        notice.setProjectionMatrix(projection);
                        update = () -> notice.update(input);
                        draw = notice::draw;
                    }
                }
                default -> {
                    if (setup.equals("hub-missing-s2")) {
                        Path library = Files.createDirectories(Path.of("/tmp/menu-film/Library/Genesis/Original cartridges"));
                        owned(Path.of("/tmp/menu-film"));
                        for (String dir : List.of("Backups", "Translations"))
                            Files.createDirectories(library.resolve(dir));
                        for (int i = 1; i <= 12; i++)
                            Files.writeString(library.resolve(String.format("Cartridge %02d.gen", i)), "placeholder");
                        Files.writeString(library.resolve("Read me.txt"), "placeholder");
                        config.setConfigValue(SonicConfiguration.SONIC_2_ROM, library.resolve("Sonic 2.gen").toString());
                        config.setConfigValue(SonicConfiguration.ROMS_DIRECTORY, library.toString());
                    }
                    MasterTitleScreen screen = new MasterTitleScreen(config,
                            new com.openggf.game.launch.LaunchProfileStore(config),
                            cue -> LOG.add(currentFrame + ",cue," + cue.name()));
                    if (setup.equals("mods")) {
                        if (modsSource == null) throw new IllegalArgumentException("mods setup needs a mods directory");
                        installMods(copyMods(modsSource));
                        screen.setModManagerScreenFactory(font -> ModSubsystem.current().createManager(font));
                    }
                    screen.initialize();
                    update = () -> screen.update(input);
                    draw = () -> {
                        screen.setViewportWidth(width);
                        screen.setProjectionMatrix(projection);
                        screen.draw();
                    };
                    cleanup = screen::cleanup;
                }
            }
            // Pre-roll: settle fades and background reads (logos, folder listings, mod scans) in real time.
            for (int i = 0; i < preroll; i++) { update.run(); input.update(); Thread.sleep(10); }

            List<int[]> releases = new ArrayList<>();
            for (int f = 0; f < frames; f++) {
                currentFrame = f;
                for (var it = releases.iterator(); it.hasNext(); ) {
                    int[] r = it.next();
                    if (r[0] == f) { input.handleKeyEvent(r[1], GLFW_RELEASE); LOG.add(f + ",release," + name(r[1])); it.remove(); }
                }
                for (Event e : events) {
                    if (e.frame() != f) continue;
                    input.handleKeyEvent(e.key(), GLFW_PRESS);
                    LOG.add(f + ",press," + name(e.key()));
                    releases.add(new int[] {f + Math.max(1, e.hold()), e.key()});
                }
                update.run();
                input.update();
                glViewport(0, 0, width, 224);
                glClearColor(0, 0, 0, 1);
                glClear(GL_COLOR_BUFFER_BIT);
                draw.draw();
                glFinish();
                ScreenshotCapture.captureAndSavePNG(width, 224, frameDir.resolve(String.format("%05d.png", f)));
                if (realtime > 0) Thread.sleep(realtime);
            }
            cleanup.run();
            List<String> csv = new ArrayList<>(List.of("frame,kind,detail"));
            csv.addAll(LOG);
            Files.write(out.resolve("events.csv"), csv);
            Files.writeString(out.resolve("take.txt"), "setup=" + setup + "\nwidth=" + width + "\nframes=" + frames
                    + "\npreroll=" + preroll + "\nrealtime-ms=" + realtime + "\nsource=" + takeFile.toAbsolutePath()
                    + "\njava=" + System.getProperty("java.version") + "\n");
            System.out.println("recorded " + frames + " frames (" + setup + ", " + width + ") to " + out);
        } finally {
            glfwTerminate();
            deleteOwned();
        }
    }

    @FunctionalInterface private interface Frame { void draw() throws Exception; }

    private static String name(int key) {
        return KEYS.entrySet().stream().filter(e -> e.getValue() == key).map(Map.Entry::getKey).findFirst().orElse("?");
    }

    private static Path owned(Path dir) { OWNED.add(dir); return dir; }

    private static void deleteOwned() {
        for (Path root : OWNED) {
            if (!Files.exists(root)) continue;
            try (var walk = Files.walk(root)) {
                for (Path p : walk.sorted(Comparator.reverseOrder()).toList()) Files.deleteIfExists(p);
            } catch (java.io.IOException ignored) {
                // Scratch roots only; the recording never depends on removing them.
            }
        }
    }

    private static Path copyMods(Path source) throws Exception {
        Path copy = owned(Files.createTempDirectory("menu-film-mods"));
        try (var files = Files.list(source)) {
            for (Path p : files.filter(f -> f.toString().endsWith(".jar")).toList())
                Files.copy(p, copy.resolve(p.getFileName()));
        }
        return copy;
    }

    private static void installMods(Path root) {
        var policy = new com.openggf.ExternalContentPolicy(com.openggf.ExternalContentMode.NORMAL);
        ModSubsystem.SessionAudioBoundary silent = new ModSubsystem.SessionAudioBoundary() {
            @Override public void install(com.openggf.audio.StreamedMusicPort port) { }
            @Override public void clear() { }
        };
        ModSubsystem.installAtBoot(policy, ModSubsystem.normalBootLoader(() -> root,
                com.openggf.io.ModInputLimits.production(), com.openggf.StockMusicDomains::containsSupported,
                silent));
    }
}
