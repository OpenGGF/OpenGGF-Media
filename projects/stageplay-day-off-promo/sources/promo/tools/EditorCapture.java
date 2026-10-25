/*
 * Display-free capture of OpenGGF's in-engine Stageplay editor (HUD chrome) driving a real
 * scene, for the "Day Off" promo (sp-promo-a, 2026-10-24).
 *
 * Mirrors Engine.java's Stageplay workspace host: every workspace call goes to the production
 * StageplayEditorSession (offscreen LIVE preview worker, route planning worker, apply). The
 * editor is driven through its own workspace actions, menu fields and synthetic key events on
 * an owned InputHandler; nothing touches a desktop. Frames are drawn exactly as
 * TestStageplayRouteOverlayPictures draws them (preview in the chrome's game viewport, chrome,
 * then the modal menu when open) and piped losslessly to FFmpeg at 60 fps.
 *
 * Usage (surfaceless EGL, DISPLAY/WAYLAND_DISPLAY unset):
 *   java --enable-native-access=ALL-UNNAMED -Dopenggf.headless.gl=surfaceless-egl \
 *     -cp ENGINE_JAR EditorCapture.java SCRIPT OUT.mkv EVENTS.json SCENE S1 S2 S3K
 * SCRIPT names a beat sequence below ("route", "tour", ...). EVENTS.json records the output
 * frame of every beat with the scene frame, workspace status and route state.
 */
import com.openggf.audio.AudioManager;
import com.openggf.configuration.SonicConfiguration;
import com.openggf.control.InputHandler;
import com.openggf.data.RomManager;
import com.openggf.editor.*;
import com.openggf.editor.hud.EditorHudRuntime;
import com.openggf.editor.project.EditorProjectMenuRenderer;
import com.openggf.editor.stageplay.StageplayWorkspace;
import com.openggf.editor.stageplay.StageplayWorkspace.Action;
import com.openggf.game.GameServices;
import com.openggf.stageplay.*;
import com.openggf.stageplay.editor.*;
import com.openggf.stageplay.route.*;
import com.openggf.tools.HeadlessGameBoot;
import org.lwjgl.system.MemoryUtil;

import java.io.*;
import java.nio.ByteBuffer;
import java.nio.file.*;
import java.util.*;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

public class EditorCapture {
    static final int W = 1920, H = 1080;
    static StageplayEditorSession session;
    static EditorWindowChrome chrome;
    static EditorProjectMenuRenderer modal;
    static StageplayWorkspace ws;
    static Video video;
    static final List<Map<String, Object>> events = new ArrayList<>();
    static final InputHandler input = new InputHandler();
    static Path sceneRoot;

    public static void main(String[] args) throws Exception {
        String script = args[0];
        Path out = Path.of(args[1]), eventsOut = Path.of(args[2]), scene = Path.of(args[3]).toAbsolutePath();
        String s1 = args[4], s2 = args[5], s3k = args[6];
        sceneRoot = scene.getParent();
        var document = StageplayStore.read(scene);
        try (var boot = new HeadlessGameBoot(W, H, 320, 224, 320, 224)) {
            boot.setBootToTitle(true);
            boot.boot(Path.of(s2), 0, 0);
            var config = GameServices.configuration();
            config.setSessionOverride(SonicConfiguration.SONIC_1_ROM, s1);
            config.setSessionOverride(SonicConfiguration.SONIC_2_ROM, s2);
            config.setSessionOverride(SonicConfiguration.SONIC_3K_ROM, s3k);
            // -Dcapture.chrome=desktop selects OpenGGF Editor's ImGui chrome (desktop repo on the class path).
            boolean desktop = "desktop".equals(System.getProperty("capture.chrome"));
            EditorWindowChrome selected = desktop
                    ? (EditorWindowChrome) Class.forName("com.openggf.editor.desktop.ImGuiEditorChrome").getDeclaredConstructor().newInstance()
                    : new EditorHudRuntime();
            try (var s = new StageplayEditorSession(GameServices::module, RomManager.getInstance(), AudioManager.getInstance());
                 var m = new EditorProjectMenuRenderer(); var v = new Video(out)) {
                session = s; chrome = selected; modal = m; video = v;
                ws = new StageplayWorkspace(host(document));
                ws.activate();
                var level = new LevelEditorController();
                chrome.init(new EditorWindowChrome.Host() {
                    public LevelEditorController controller() { return level; }
                    public void dispatch(EditorInputHandler.Action action) { }
                    public List<EditorCommandPalette.HostCommand> commands() { return List.of(); }
                    public StageplayWorkspace stageplay() { return ws; }
                }, 1);
                if (!chrome.setActive(true)) throw new IllegalStateException("HUD chrome unavailable");
                try {
                    switch (script) {
                        case "route" -> routeBeats(document, out.getParent());
                        case "tour" -> tourBeats(document, scene, out.getParent());
                        case "desktop-tour" -> desktopTourBeats(document, scene);
                        case "desktop-route" -> desktopRouteBeats(document, out.getParent());
                        default -> throw new IllegalArgumentException("Unknown script " + script);
                    }
                    event("end");
                } finally { chrome.close(); }
            }
        } finally {
            Files.writeString(eventsOut, toJson(events));
        }
    }

    static StageplayWorkspace.Host host(StageplayDocument document) {
        return new StageplayWorkspace.Host() {
            public StageplayDocument initialDocument() { return document; }
            public Path initialAssetRoot() { return sceneRoot; }
            public void validate(StageplayDocument d, Path root) throws IOException { session.validate(d, root); }
            public StageplayTimeline.Frame resolvePreview(StageplayDocument d, Path root, int frame) throws IOException { return session.resolvePreview(d, root, frame); }
            public StageplayTimeline.Frame resolvePreview(StageplayDocument d, Path root, StageplayTimeline.Frame frame) throws IOException { return session.resolvePreview(d, root, frame); }
            public List<com.openggf.stageplay.runtime.StageplayObjectInspection> objectInspection() { return session.objectInspection(); }
            public void refreshResources() { session.release(); }
            public void play(StageplayDocument d, Path root, int frame) throws IOException { session.play(d, root, frame); }
            public void present(StageplayDocument d, int frame) { session.present(d, frame); }
            public void stop() { session.stop(); }
            public void export(StageplayDocument d, Path source, Path output) throws IOException { session.export(d, source, output); }
            public Set<com.openggf.game.CharacterDefinition.MovementAbility> movementAbilities(StageplayDocument.Actor a, Path root) throws IOException { return session.movementAbilities(a, root); }
            public void startRoute(StageplayDocument d, Path root, StageplayRouteRequest r) throws IOException { session.startRoute(d, root, r); }
            public StageplayRouteJob.Update pollRoute() { return session.pollRoute(); }
            public void requestRouteApply(StageplayDocument d, Path root) throws IOException { session.requestRouteApply(d, root); }
            public void cancelRoute() { session.cancelRoute(); }
        };
    }

    // ------------------------------------------------------------------ beats
    static int shotStart(StageplayDocument d, String id) {
        for (var change : d.sceneChanges()) if (change.id().startsWith(id + ".")) return change.frame();
        return 0;
    }

    // Player route form rows (StageplayWorkspace.routeForm): actor, x, y, frames, starting action,
    // travel speed, ending action, ending facing, nodes, ticks, millis, then the submit row.
    static final Map<String, Integer> ROUTE_ROWS = Map.of("x", 1, "y", 2, "frames", 3, "startingAction", 4,
            "travelSpeed", 5, "endingAction", 6, "endingFacing", 7, "submit", 11);

    /** The route sequence: Walk fails with advice, Run/Hard stop/Face left traces the loop, Apply, Play. */
    static void routeBeats(StageplayDocument d, Path outDir) throws Exception {
        int entry = shotStart(d, "loop");
        ws.selectActor("sonic");
        ws.seek(entry);
        event("loop shot entry, Sonic selected");
        hold(45);
        ws.invoke(Action.CAMERA_MODE);
        event("camera mode: look left to Sonic's spawn");
        panCamera(-175, 0, 60);
        hold(40);
        openRouteForm();
        hold(40);
        typeField(ROUTE_ROWS.get("x"), "5860"); hold(16);
        typeField(ROUTE_ROWS.get("y"), "621"); hold(16);
        typeField(ROUTE_ROWS.get("frames"), "419"); hold(40);
        submitRow(ROUTE_ROWS.get("submit"));
        event("walk plan submitted");
        awaitRoute(StageplayRouteJob.Phase.FAILED, 6);
        event("walk plan failed: " + ws.status());
        hold(240);                                   // review the failed attempt on the picture
        ws.invoke(Action.ROUTE_HELPER);              // route status menu: Cancel / Plan another / Back
        menuRow = 0;
        event("route status menu: " + ws.menu().title());
        hold(150);
        selectRow(1);
        hold(10);
        press(GLFW_KEY_ENTER);                       // Plan another route
        menuRow = 0;
        if (!ws.menu().isOpen()) throw new IllegalStateException("Route form did not reopen: " + ws.status());
        event("route form reopened");
        hold(30);
        typeField(ROUTE_ROWS.get("x"), "5860"); hold(10);
        typeField(ROUTE_ROWS.get("y"), "621"); hold(10);
        typeField(ROUTE_ROWS.get("frames"), "419"); hold(20);
        cycleTo(ROUTE_ROWS.get("travelSpeed"), "travelSpeed", "Run"); hold(20);
        cycleTo(ROUTE_ROWS.get("endingAction"), "endingAction", "Hard Stop"); hold(20);
        cycleTo(ROUTE_ROWS.get("endingFacing"), "endingFacing", "Left"); hold(40);
        submitRow(ROUTE_ROWS.get("submit"));
        event("run plan submitted");
        awaitRoute(StageplayRouteJob.Phase.READY, 6);
        event("run plan proposed: " + ws.status());
        hold(90);
        event("pan along the proposed line");
        panCamera(470, 0, 210);
        hold(90);
        ws.invoke(Action.ROUTE_HELPER);
        menuRow = 0;
        event("route actions open");
        hold(60);
        press(GLFW_KEY_ENTER);                       // "Check inputs and apply route"
        event("apply requested");
        awaitApplied();
        ws.menu().close();
        event("route applied: " + ws.status());
        hold(30);
        ws.invoke(Action.CAMERA_MODE);               // leave camera mode: the draft framing is discarded
        event("authored framing restored");
        hold(40);
        event("play");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 340; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        event("play stopped at scene frame " + ws.controller().frame());
        hold(60);
        StageplayStore.write(outDir.resolve("route-applied.stageplay"), ws.controller().document());
    }

    /** Pans the unkeyed draft camera by world pixels at zoom 1, drawing every frame. */
    static void panCamera(double dx, double dy, int frames) throws Exception {
        double zoom = ws.directorCamera().zoom();
        for (int i = 0; i < frames; i++) {
            double t0 = smooth(i / (double) frames), t1 = smooth((i + 1) / (double) frames);
            ws.moveCamera((t1 - t0) * dx * zoom, (t1 - t0) * dy * zoom, 1);
            frame();
        }
    }

    static double smooth(double t) { return t * t * (3 - 2 * t); }

    /** The editor tour over the complete film scene, opened from its .stageplay file. */
    static void tourBeats(StageplayDocument d, Path scene, Path outDir) throws Exception {
        ws.open(scene);
        int ledge = shotStart(d, "ledge"), pull = ledge + 440;
        ws.selectActor("sonic");
        ws.seek(pull);
        event("pull-back frame (matches film frame " + pull + ")");
        hold(150);
        event("rewind");
        int steps = 75;
        for (int i = 1; i <= steps; i++) { ws.seek((int) Math.round(pull * (1 - smooth(i / (double) steps)))); frame(); }
        event("scene start");
        hold(50);
        // Sets: three games' native levels, joined by authored cuts and transitions.
        ws.invoke(Action.SCENE_CHANGES); menuRow = 0;
        event("scene changes menu");
        hold(30);
        for (int i = 1; i <= 5; i++) { selectRow(i); hold(18); }
        hold(60);
        ws.menu().close();
        // Cast: four performers from three games.
        hold(20);
        hudKey(GLFW_KEY_DOWN); hold(25); hudKey(GLFW_KEY_DOWN); hold(25); hudKey(GLFW_KEY_DOWN); hold(25);
        hudKey(GLFW_KEY_ENTER);
        event("cast: Motobug selected");
        hold(40);
        // Free -> Puppet: the native patrol reaches the edge and the director keeps it there.
        ws.seek(225);
        event("patrol approaches the edge (Free)");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 205; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        event("held as a Puppet at scene frame " + ws.controller().frame());
        hold(20);
        ws.invoke(Action.OBJECTS); menuRow = 0;
        event("object cast menu");
        hold(70);
        selectRow(6); hold(15); press(GLFW_KEY_ENTER); menuRow = 0;   // Motobug / moto
        event("Motobug role menu");
        hold(40);
        selectRow(1); hold(12); press(GLFW_KEY_ENTER); menuRow = 0;   // Mode / position / animation keys
        event("Motobug mode keys");
        hold(40);
        selectRow(1); hold(20); selectRow(2); hold(70);
        press(GLFW_KEY_ENTER); menuRow = 0;                           // the PUPPET key form
        event("PUPPET key form");
        hold(120);
        ws.menu().close();
        ws.invoke(Action.OBJECTS); menuRow = 0;
        selectRow(5); hold(12); press(GLFW_KEY_ENTER); menuRow = 0;   // World commands / removals
        event("world commands");
        hold(40);
        for (int i = 1; i <= 3; i++) { selectRow(i); hold(25); }
        hold(50);
        ws.menu().close();
        // Camera: the push-in key, then play across it.
        ws.seek(shotStart(d, "patrol") + 439);
        ws.invoke(Action.CAMERA_KEY); menuRow = 0;
        event("camera menu at the push-in key");
        hold(40);
        press(GLFW_KEY_ENTER); menuRow = 0;                           // Set camera key: shows this key's values
        event("camera key form (zoom 2)");
        hold(120);
        ws.menu().close();
        ws.seek(350);
        event("play the push-in");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 150; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        // Dialogue: Sonic's line, its skin, and its typing in the preview.
        ws.invoke(Action.DIALOGUE); menuRow = 0;
        event("dialogue lines");
        hold(30);
        int sonicLine = 3 + indexOfDialogue(d, "Uh... aren't you supposed to be chasing me?");
        for (int i = 1; i <= Math.min(sonicLine, 9); i++) { selectRow(i); hold(6); }
        selectRow(sonicLine); hold(30);
        press(GLFW_KEY_ENTER); menuRow = 0; hold(30);
        press(GLFW_KEY_ENTER); menuRow = 0;                           // Edit line, timing and panel
        event("Sonic line form");
        hold(140);
        ws.menu().close();
        ws.invoke(Action.DIALOGUE_SKINS); menuRow = 0;
        event("dialogue decorations");
        hold(90);
        ws.menu().close();
        int line = shotStart(d, "loop") + 300;
        ws.seek(line);
        event("play Sonic's line");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 170; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        // Two-way: export the screenplay, then the import form.
        ws.invoke(Action.EXPORT_SCREENPLAY); menuRow = 0;
        ws.menu().setValue("path", scene.resolveSibling("day-off.screenplay.json").toString());
        event("export screenplay form");
        hold(80);
        selectRow(1); hold(10); press(GLFW_KEY_ENTER);
        event("screenplay exported: " + ws.status());
        hold(60);
        ws.invoke(Action.IMPORT_SCREENPLAY); menuRow = 0;
        ws.menu().setValue("path", scene.resolveSibling("day-off.screenplay.json").toString());
        event("import screenplay form");
        hold(90);
        ws.menu().close();
        // Export film.
        ws.seek(0);
        ws.invoke(Action.EXPORT);
        if (ws.menu().isOpen()) {
            menuRow = 0;
            ws.menu().setValue("out", outDir.resolve("day-off.editor-export.mkv").toString());
            event("export film form");
            hold(90);
            selectRow(1); hold(10); press(GLFW_KEY_ENTER);
        }
        event("export started: " + ws.status());
        hold(150);
        // Engine.update() polls the exporter and shows its result as the workspace status.
        long deadline = System.nanoTime() + 900_000_000_000L;
        String result = null;
        while (result == null && System.nanoTime() < deadline) { Thread.sleep(1000); result = session.pollExport(); }
        if (result == null) throw new IllegalStateException("Editor film export did not finish");
        ws.setStatus(result);
        event("export finished (wait not recorded): " + result);
        hold(150);
    }

    /** OpenGGF Editor (desktop): the same scene and frames, with its inspector and timeline. */
    static void desktopTourBeats(StageplayDocument d, Path scene) throws Exception {
        ws.open(scene);
        int ledge = shotStart(d, "ledge"), pull = ledge + 440, island = shotStart(d, "island");
        ws.selectActor("sonic");
        ws.seek(pull);
        event("desktop: pull-back frame " + pull);
        hold(150);
        ws.selectActor("knuckles");
        ws.seek(island + 360);
        event("desktop: Knuckles gliding, inspector shows native ability state");
        hold(150);
        ws.seek(island + 300);
        event("desktop: play Knuckles' entrance");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 240; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        hold(60);
    }

    /** Desktop route: plan Run / Hard stop / Face left on the before-scene, review, apply, play. */
    static void desktopRouteBeats(StageplayDocument d, Path outDir) throws Exception {
        int entry = shotStart(d, "loop");
        ws.selectActor("sonic");
        ws.seek(entry);
        event("desktop: loop shot entry");
        hold(40);
        openRouteForm();
        hold(20);
        typeField(ROUTE_ROWS.get("x"), "5860"); hold(8);
        typeField(ROUTE_ROWS.get("y"), "621"); hold(8);
        typeField(ROUTE_ROWS.get("frames"), "419"); hold(10);
        cycleTo(ROUTE_ROWS.get("travelSpeed"), "travelSpeed", "Run"); hold(10);
        cycleTo(ROUTE_ROWS.get("endingAction"), "endingAction", "Hard Stop"); hold(10);
        cycleTo(ROUTE_ROWS.get("endingFacing"), "endingFacing", "Left"); hold(20);
        submitRow(ROUTE_ROWS.get("submit"));
        awaitRoute(StageplayRouteJob.Phase.READY, 6);
        event("desktop: route proposed: " + ws.status());
        hold(200);
        ws.invoke(Action.ROUTE_HELPER); menuRow = 0;
        hold(30);
        press(GLFW_KEY_ENTER);
        awaitApplied();
        ws.menu().close();
        event("desktop: route applied");
        hold(40);
        ws.invoke(Action.PLAY);
        event("desktop: play");
        for (int i = 0; i < 340; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        hold(40);
        StageplayStore.write(outDir.resolve("desktop-route-applied.stageplay"), ws.controller().document());
    }

    static int indexOfDialogue(StageplayDocument d, String text) {
        for (int i = 0; i < d.dialogue().size(); i++) if (d.dialogue().get(i).text().equals(text)) return i;
        throw new IllegalArgumentException("No dialogue " + text);
    }

    /** HUD-level keys (page tabs, cast rows) go through the chrome, as the engine routes them. */
    static void hudKey(int key) throws Exception {
        input.handleKeyEvent(key, GLFW_PRESS);
        input.refreshLogicalSnapshot();
        chrome.update(input);
        ws.tick(input);
        input.update();
        input.handleKeyEvent(key, GLFW_RELEASE);
        input.update();
        frame();
    }

    // ------------------------------------------------------------------ helpers
    static int menuRow;

    static void openRouteForm() throws Exception {
        ws.invoke(Action.ROUTE_HELPER);
        if (!ws.menu().isOpen()) throw new IllegalStateException("Route form did not open: " + ws.status());
        menuRow = 0;
        event("route form open");
    }

    /** Moves the menu highlight to a row with Down presses, drawing each step. */
    static void selectRow(int row) throws Exception {
        while (menuRow < row) { press(GLFW_KEY_DOWN); menuRow++; hold(7); }
        while (menuRow > row) { press(GLFW_KEY_UP); menuRow--; hold(7); }
    }

    /** Enter opens the field's text editor; Backspace clears it; digits are typed; Enter accepts. */
    static void typeField(int row, String text) throws Exception {
        selectRow(row);
        press(GLFW_KEY_ENTER); hold(10);
        for (int i = 0; i < 8; i++) { press(GLFW_KEY_BACKSPACE); hold(2); }
        for (char c : text.toCharArray()) { typeCodepoint(c); ws.tick(input); input.update(); hold(5); }
        hold(8);
        press(GLFW_KEY_ENTER); hold(6);
        event("typed row " + row + " = " + text);
    }

    static java.lang.reflect.Method append;
    /** InputHandler's text queue is package-private; the capture feeds it as GLFW's char callback would. */
    static void typeCodepoint(int codepoint) throws Exception {
        if (append == null) {
            append = InputHandler.class.getDeclaredMethod("appendMenuCodepoint", int.class);
            append.setAccessible(true);
        }
        append.invoke(input, codepoint);
    }

    /** Enter cycles a choice field, so the form shows each value in turn. */
    static void cycleTo(int row, String key, String value) throws Exception {
        selectRow(row);
        for (int guard = 0; guard < 6 && !value.equals(ws.menu().values().get(key)); guard++) {
            press(GLFW_KEY_ENTER);
            hold(14);
        }
        if (!value.equals(ws.menu().values().get(key))) throw new IllegalStateException(key + " did not reach " + value);
        event("set " + key + " = " + value);
    }

    static void submitRow(int row) throws Exception {
        selectRow(row);
        hold(10);
        press(GLFW_KEY_ENTER);
        requireNoMenuError();
    }

    static void press(int key) throws Exception {
        input.handleKeyEvent(key, GLFW_PRESS);
        input.refreshLogicalSnapshot();
        ws.tick(input);
        input.update();
        input.handleKeyEvent(key, GLFW_RELEASE);
        input.update();
    }

    static void requireNoMenuError() {
        if (ws.menu().error() != null) throw new IllegalStateException("Menu error: " + ws.menu().error());
    }

    static void awaitRoute(StageplayRouteJob.Phase phase, int framesPerPoll) throws Exception {
        long deadline = System.nanoTime() + 180_000_000_000L;
        while (System.nanoTime() < deadline) {
            ws.tick(new InputHandler());
            var update = session.pollRoute();
            if (update != null && (System.nanoTime() / 2_000_000_000L) % 2 == 0 && video.count % 30 == 0)
                System.err.println("ROUTE " + update.phase() + " " + update.message());
            if (update != null && update.phase() == phase) return;
            if (update != null && update.phase() == StageplayRouteJob.Phase.FAILED && phase != StageplayRouteJob.Phase.FAILED)
                throw new IllegalStateException("Route failed: " + update.message());
            hold(1);
            Thread.sleep(20L * framesPerPoll);
        }
        throw new IllegalStateException("Route worker did not reach " + phase);
    }

    static void awaitApplied() throws Exception {
        long deadline = System.nanoTime() + 120_000_000_000L;
        while (System.nanoTime() < deadline) {
            ws.tick(new InputHandler());
            if (ws.routeOverlay() != null && ws.routeOverlay().applied()) return;
            hold(1);
            Thread.sleep(40);
        }
        throw new IllegalStateException("Route did not apply: " + ws.status());
    }

    static void hold(int frames) throws Exception { for (int i = 0; i < frames; i++) frame(); }

    static void frame() throws Exception {
        chrome.update(new InputHandler());
        var doc = ws.controller().document();
        int[] viewport = chrome.gameViewport(W, H, W, H, doc.width(), doc.height());
        glViewport(0, 0, W, H);
        glDisable(GL_SCISSOR_TEST);
        glClearColor(0, 0, 0, 1);
        glClear(GL_COLOR_BUFFER_BIT);
        glViewport(viewport[0], viewport[1], viewport[2], viewport[3]);
        session.draw(ws.previewDocument(), ws.previewFrame(), ws.assetRoot(), f -> { throw new RuntimeException(f); });
        chrome.render(W, H, W, H);
        if (ws.menu().isOpen()) {
            glViewport(0, 0, W, H);
            int menuWidth = Math.round(W * 224f / H);
            modal.render(ws.menu(), new org.joml.Matrix4f().ortho2D(0, menuWidth, 0, 224).get(new float[16]), menuWidth);
        }
        video.frame();
    }

    static void event(String label) {
        var e = new LinkedHashMap<String, Object>();
        e.put("outputFrame", video.count);
        e.put("label", label);
        e.put("sceneFrame", ws.controller().frame());
        e.put("menuOpen", ws.menu().isOpen());
        var overlay = ws.routeOverlay();
        e.put("route", overlay == null ? "" : overlay.title() + (overlay.applied() ? " (applied)" : ""));
        e.put("status", ws.status());
        events.add(e);
        System.err.println("EVENT " + e);
    }

    static String toJson(List<Map<String, Object>> list) {
        var b = new StringBuilder("[\n");
        for (int i = 0; i < list.size(); i++) {
            b.append("  {");
            int j = 0;
            for (var entry : list.get(i).entrySet()) {
                if (j++ > 0) b.append(", ");
                b.append('"').append(entry.getKey()).append("\": ");
                Object v = entry.getValue();
                if (v instanceof Number || v instanceof Boolean) b.append(v);
                else b.append('"').append(String.valueOf(v).replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", " ")).append('"');
            }
            b.append(i + 1 < list.size() ? "},\n" : "}\n");
        }
        return b.append("]\n").toString();
    }

    static final class Video implements AutoCloseable {
        final Process process; final OutputStream pipe; int count;
        final ByteBuffer buffer = MemoryUtil.memAlloc(W * H * 4); final byte[] bytes = new byte[W * H * 4];
        Video(Path file) throws IOException {
            process = new ProcessBuilder("ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", W + "x" + H,
                    "-r", "60", "-i", "pipe:0", "-vf", "vflip", "-c:v", "ffv1", "-level", "3", "-pix_fmt", "bgr0",
                    file.toString()).redirectError(ProcessBuilder.Redirect.INHERIT).start();
            pipe = new BufferedOutputStream(process.getOutputStream(), 1 << 22);
        }
        void frame() throws IOException {
            glFinish();
            buffer.clear();
            glPixelStorei(GL_PACK_ALIGNMENT, 1);
            glReadPixels(0, 0, W, H, GL_RGBA, GL_UNSIGNED_BYTE, buffer);
            buffer.get(bytes);
            pipe.write(bytes);
            count++;
        }
        public void close() throws Exception {
            pipe.close();
            if (process.waitFor() != 0) throw new IOException("ffmpeg failed");
            MemoryUtil.memFree(buffer);
        }
    }
}
