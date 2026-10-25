/*
 * Display-free capture of OpenGGF's Stageplay editors for the "Day Off" v2 promo
 * (sp-promo-a, 2026-10-24; engine develop 81f25c89f, OpenGGF-Editor main dd5ee43).
 *
 * Revision of EditorCapture.java for the redesigned compact forms: rows are found by field key
 * (forms) or action label (lists) instead of fixed indices; level positions are chosen with the
 * in-level picker (held arrow keys with the native acceleration, Shift one-pixel moves, floor
 * snapping, Enter); F1 details and F2 numeric entry are used where the editor offers them.
 * Every workspace call goes to the production StageplayEditorSession (offscreen LIVE preview,
 * route worker, ground queries, export). Input goes through an owned InputHandler; nothing
 * touches a desktop. Frames are drawn as the engine draws them (preview in the chrome's game
 * viewport, the chrome including the picker, then the HUD modal) and piped losslessly to FFmpeg.
 *
 * Usage (surfaceless EGL, DISPLAY/WAYLAND_DISPLAY unset):
 *   java --enable-native-access=ALL-UNNAMED -Dopenggf.headless.gl=surfaceless-egl \
 *     -cp ENGINE_JAR EditorCapture2.java SCRIPT OUT.mkv EVENTS.json SCENE S1 S2 S3K
 * SCENE should live in a neutral directory (the editor shows absolute scene/export paths).
 * EVENTS.json records the output frame of every beat with the scene frame, menu, status and route.
 */
import com.openggf.audio.AudioManager;
import com.openggf.configuration.SonicConfiguration;
import com.openggf.control.InputHandler;
import com.openggf.data.RomManager;
import com.openggf.editor.*;
import com.openggf.editor.hud.EditorHudRuntime;
import com.openggf.editor.project.EditorProjectMenu;
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
import java.lang.reflect.*;
import java.nio.ByteBuffer;
import java.nio.file.*;
import java.util.*;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

public class EditorCapture2 {
    static final int W = 1920, H = 1080;
    static StageplayEditorSession session;
    static EditorWindowChrome chrome;
    static EditorProjectMenuRenderer modal;
    static StageplayWorkspace ws;
    static Video video;
    static boolean desktop;
    static final List<Map<String, Object>> events = new ArrayList<>();
    static final InputHandler input = new InputHandler();
    static Path sceneRoot;

    public static void main(String[] args) throws Exception {
        String script = args[0];
        Path out = Path.of(args[1]).toAbsolutePath(), eventsOut = Path.of(args[2]).toAbsolutePath();
        Path scene = Path.of(args[3]).toAbsolutePath().normalize();
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
            desktop = "desktop".equals(System.getProperty("capture.chrome"));
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
                if (!chrome.setActive(true)) throw new IllegalStateException("Editor chrome unavailable");
                try {
                    switch (script) {
                        case "route" -> routeBeats(document, scene);
                        case "tour" -> tourBeats(document, scene);
                        case "desktop-route" -> desktopRouteBeats(document, scene);
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
            public StageplayGround.Report ground(StageplayDocument d, Path root, int frame, StageplayGround.Batch batch) throws IOException { return session.ground(d, root, frame, batch); }
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

    static final double DEST_X = 5860;                 // the loop destination column; Y comes from the floor snap

    /** Plan route: pick the destination in the level, Walk fails with a reason, Run / Hard / Left succeeds. */
    static void routeBeats(StageplayDocument d, Path scene) throws Exception {
        int entry = shotStart(d, "loop");
        ws.selectActor("sonic");
        ws.seek(entry);
        event("loop shot entry, Sonic selected");
        hold(40);
        ws.invoke(Action.ROUTE_HELPER);
        requireMenu("Plan route");
        event("route form open");
        hold(60);
        selectField("x");
        hold(16);
        press(GLFW_KEY_ENTER);                                    // Position: opens the level picker
        if (!ws.pickingPosition()) throw new IllegalStateException("Picker did not open: " + ws.status());
        event("picker open at " + pickerAt());
        hold(30);
        pickTo(DEST_X, 600);
        event("picker at destination: " + pickerAt());
        hold(70);
        press(GLFW_KEY_ENTER);                                    // confirm: writes the form's Position only
        if (ws.pickingPosition()) throw new IllegalStateException("Picker did not confirm");
        event("picked " + ws.menu().values().get("x") + ", " + ws.menu().values().get("y"));
        hold(50);
        // Advanced: the same 419-frame attempt window as v1 (it leaves the planner budget for its Run check).
        selectField("#section:Advanced"); hold(10);
        press(GLFW_KEY_ENTER); hold(24);
        selectField("frames"); hold(10);
        press(GLFW_KEY_ENTER); hold(10);
        for (int i = 0; i < 6; i++) { press(GLFW_KEY_BACKSPACE); hold(1); }
        typeText("419");
        hold(8);
        press(GLFW_KEY_ENTER);
        requireNoMenuError();
        event("attempt frames " + ws.menu().values().get("frames"));
        hold(30);
        selectSubmit();
        hold(14);
        press(GLFW_KEY_ENTER);                                    // Find route (Walk defaults)
        requireNoMenuError();
        event("walk plan submitted");
        awaitRoute(StageplayRouteJob.Phase.FAILED, 6);
        event("walk plan failed: " + ws.status());
        hold(170);                                                // the red cross and the side panel's result
        ws.invoke(Action.ROUTE_HELPER);                           // Route result: actions on the failure
        event("route result menu: " + ws.menu().title());
        hold(70);
        press(GLFW_KEY_F1);                                       // full planner explanation
        event("route details: " + ws.menu().helpText().replace('\n', ' '));
        hold(220);
        press(GLFW_KEY_ESCAPE);                                   // close details, back to the actions
        hold(20);
        selectAction("Plan another route");
        hold(14);
        press(GLFW_KEY_ENTER);
        requireMenu("Plan route");
        event("route form reopened");
        hold(24);
        selectField("x");
        hold(10);
        press(GLFW_KEY_ENTER);                                    // pick the same spot again
        if (!ws.pickingPosition()) throw new IllegalStateException("Picker did not reopen");
        hold(16);
        pickTo(DEST_X, 600);
        hold(30);
        press(GLFW_KEY_ENTER);
        event("picked again " + ws.menu().values().get("x") + ", " + ws.menu().values().get("y"));
        hold(24);
        cycleTo("travelSpeed", "Run"); hold(16);
        cycleTo("endingAction", "Hard Stop"); hold(16);
        cycleTo("endingFacing", "Left"); hold(36);
        selectSubmit();
        hold(14);
        press(GLFW_KEY_ENTER);
        requireNoMenuError();
        event("run plan submitted");
        awaitRoute(StageplayRouteJob.Phase.READY, 6);
        event("run plan proposed: " + ws.status());
        hold(80);
        ws.invoke(Action.CAMERA_MODE);
        event("camera mode: pan along the proposed line");
        panCamera(-120, 0, 70);
        hold(30);
        panCamera(560, 0, 230);
        hold(70);
        ws.invoke(Action.ROUTE_HELPER);
        event("route actions open: " + ws.menu().title());
        hold(60);
        selectAction("Check inputs and apply route");
        hold(10);
        press(GLFW_KEY_ENTER);
        event("apply requested");
        awaitApplied();
        if (ws.menu().isOpen()) ws.menu().close();
        event("route applied: " + ws.status());
        hold(30);
        ws.invoke(Action.CAMERA_MODE);                            // leave camera mode: authored framing
        event("authored framing restored");
        hold(40);
        event("play");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 340; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        event("play stopped at scene frame " + ws.controller().frame());
        hold(60);
        StageplayStore.write(scene.resolveSibling("route-applied.stageplay"), ws.controller().document());
    }

    /** The tour over the finished scene: sets, cast, Free/Puppet, keys, camera, dialogue, voice, export. */
    static void tourBeats(StageplayDocument d, Path scene) throws Exception {
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
        ws.invoke(Action.SCENE_CHANGES);
        event("scene changes menu: " + actionLabels());
        hold(30);
        for (int i = 1; i < ws.menu().actionEntries().size() && i <= 5; i++) { selectActionIndex(i); hold(18); }
        hold(60);
        ws.menu().close();
        hold(20);
        hudKey(GLFW_KEY_DOWN); hold(25); hudKey(GLFW_KEY_DOWN); hold(25); hudKey(GLFW_KEY_DOWN); hold(25);
        hudKey(GLFW_KEY_ENTER);
        event("cast: " + ws.controller().selectedActorId() + " selected");
        hold(40);
        // Free -> Puppet: the native patrol reaches the edge and the director keeps it there.
        ws.seek(225);
        event("patrol approaches the edge (Free)");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 205; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        event("held as a Puppet at scene frame " + ws.controller().frame());
        hold(20);
        ws.invoke(Action.OBJECTS);
        event("object cast menu: " + actionLabels());
        hold(60);
        selectAction("Motobug"); hold(15); press(GLFW_KEY_ENTER);
        event("Motobug menu: " + ws.menu().title() + " " + actionLabels());
        hold(40);
        selectAction("Mode / position / animation keys"); hold(12); press(GLFW_KEY_ENTER);
        event("Motobug mode keys: " + actionLabels());
        hold(40);
        selectAction("327"); hold(70);
        press(GLFW_KEY_ENTER);
        event("PUPPET key form: " + ws.menu().title() + " " + ws.menu().values());
        hold(140);
        ws.menu().close();
        ws.invoke(Action.OBJECTS);
        selectAction("World commands"); hold(12); press(GLFW_KEY_ENTER);
        event("world commands: " + actionLabels());
        hold(40);
        for (int i = 1; i <= 3; i++) { selectActionIndex(i); hold(25); }
        hold(50);
        ws.menu().close();
        // Camera: the push-in key, then play across it.
        ws.seek(shotStart(d, "patrol") + 439);
        ws.invoke(Action.CAMERA_KEY);
        event("camera menu: " + ws.menu().title());
        hold(40);
        selectAction("Set camera key"); hold(10); press(GLFW_KEY_ENTER);
        event("camera key form: " + ws.menu().values());
        hold(130);
        ws.menu().close();
        ws.seek(350);
        event("play the push-in");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 150; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        // Dialogue: Sonic's line form.
        ws.invoke(Action.DIALOGUE);
        event("dialogue lines");
        hold(30);
        selectAction("1145: Sonic"); hold(30);
        press(GLFW_KEY_ENTER); hold(30);
        selectAction("Edit line, timing and panel"); hold(10); press(GLFW_KEY_ENTER);
        event("Sonic line form: " + ws.menu().values());
        hold(150);
        ws.menu().close();
        // Voices: the Motobug's line menu -> its voice (default Patrol Buzz) and the preset list.
        ws.invoke(Action.DIALOGUE);
        hold(20);
        selectAction("1290: Motobug"); hold(30);
        press(GLFW_KEY_ENTER); hold(24);
        selectAction("Speaker voice"); hold(12); press(GLFW_KEY_ENTER);
        event("Motobug voice form: " + ws.menu().title() + " " + ws.menu().values());
        hold(130);
        selectField("tone"); hold(16);
        press(GLFW_KEY_ENTER);                                    // BUZZ -> PRESETS: the fifteen audition voices
        event("tone -> " + (ws.menu().isOpen() ? ws.menu().title() + " " + actionLabels() + " " + ws.menu().values() : "closed"));
        hold(40);
        if (ws.menu().isOpen() && ws.menu().title().equals("Voice presets")) {
            for (int i = 1; i <= 4; i++) { selectActionIndex(i); hold(14); }
            hold(60);
        }
        ws.menu().close();
        // The Motobug's line in the preview, with its pointer (voice plays in forward playback).
        ws.seek(shotStart(d, "loop") + 440);
        event("play the Motobug's reply");
        ws.invoke(Action.PLAY);
        for (int i = 0; i < 130; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        // Two-way: export the screenplay, then the import form.
        ws.invoke(Action.EXPORT_SCREENPLAY);
        ws.menu().setValue("path", scene.resolveSibling("day-off.screenplay.json").toString());
        event("export screenplay form");
        hold(80);
        selectSubmit(); hold(10); press(GLFW_KEY_ENTER);
        event("screenplay exported: " + ws.status());
        hold(60);
        ws.invoke(Action.IMPORT_SCREENPLAY);
        ws.menu().setValue("path", scene.resolveSibling("day-off.screenplay.json").toString());
        event("import screenplay form");
        hold(90);
        ws.menu().close();
        // Export film.
        ws.seek(0);
        ws.invoke(Action.EXPORT);
        if (ws.menu().isOpen()) {
            ws.menu().setValue("out", scene.resolveSibling("day-off.mkv").toString());
            event("export film form");
            hold(90);
            selectSubmit(); hold(10); press(GLFW_KEY_ENTER);
        }
        event("export started: " + ws.status());
        hold(150);
        long deadline = System.nanoTime() + 900_000_000_000L;
        String result = null;
        while (result == null && System.nanoTime() < deadline) { Thread.sleep(1000); result = session.pollExport(); }
        if (result == null) throw new IllegalStateException("Editor film export did not finish");
        ws.setStatus(result);
        event("export finished (wait not recorded): " + result);
        hold(150);
    }

    /** Desktop: the same request from the before-route scene (values set through the shared form), apply, play. */
    static void desktopRouteBeats(StageplayDocument d, Path scene) throws Exception {
        int entry = shotStart(d, "loop");
        ws.selectActor("sonic");
        ws.seek(entry);
        event("desktop: loop shot entry");
        hold(40);
        ws.invoke(Action.ROUTE_HELPER);
        requireMenu("Plan route");
        var m = ws.menu();
        m.setValue("x", "5860"); m.setValue("y", "620");                 // the in-engine pick
        m.setValue("travelSpeed", "Run"); m.setValue("endingAction", "Hard Stop"); m.setValue("endingFacing", "Left");
        event("desktop: route form " + m.values());
        hold(60);
        m.submit();
        requireNoMenuError();
        awaitRoute(StageplayRouteJob.Phase.READY, 6);
        event("desktop: route proposed: " + ws.status());
        hold(200);
        ws.invoke(Action.ROUTE_HELPER);
        hold(30);
        selectAction("Check inputs and apply route");
        press(GLFW_KEY_ENTER);
        awaitApplied();
        if (ws.menu().isOpen()) ws.menu().close();
        event("desktop: route applied");
        hold(40);
        ws.invoke(Action.PLAY);
        event("desktop: play");
        for (int i = 0; i < 340; i++) { ws.tick(new InputHandler()); frame(); }
        ws.stop();
        hold(40);
        StageplayStore.write(scene.resolveSibling("desktop-route-applied.stageplay"), ws.controller().document());
    }

    // ------------------------------------------------------------------ picker
    static String pickerAt() {
        var p = ws.positionPicker();
        return p == null ? "-" : String.format("%.0f,%.0f snap=%s floor=%s", p.x(), p.y(), p.snap(),
                p.floor() == null ? "none" : String.format("%.0f/%d", p.floor().y(), p.floor().surfaceY()));
    }

    /** Move the crosshair with held arrows (native acceleration), then Shift one-pixel moves, to (tx, ty). */
    static void pickTo(double tx, double ty) throws Exception {
        var p = ws.positionPicker();
        // Coarse: hold toward the target while it is far, releasing early so the last approach is visible.
        int keyX = tx > p.x() ? GLFW_KEY_RIGHT : GLFW_KEY_LEFT;
        input.handleKeyEvent(keyX, GLFW_PRESS);
        int guard = 0;
        while (Math.abs(tx - ws.positionPicker().x()) > 28 && guard++ < 600) pickerTick();
        input.handleKeyEvent(keyX, GLFW_RELEASE);
        pickerTick();
        hold(12);
        int keyY = ty > ws.positionPicker().y() ? GLFW_KEY_DOWN : GLFW_KEY_UP;
        if (Math.abs(ty - ws.positionPicker().y()) > 28) {
            input.handleKeyEvent(keyY, GLFW_PRESS);
            guard = 0;
            while (Math.abs(ty - ws.positionPicker().y()) > 28 && guard++ < 600) pickerTick();
            input.handleKeyEvent(keyY, GLFW_RELEASE);
            pickerTick();
            hold(8);
        }
        // Fine: Shift + arrow, one pixel per tick.
        input.handleKeyEvent(GLFW_KEY_LEFT_SHIFT, GLFW_PRESS);
        fine(tx, true);
        fine(ty, false);
        input.handleKeyEvent(GLFW_KEY_LEFT_SHIFT, GLFW_RELEASE);
        pickerTick();
        if (Math.round(ws.positionPicker().x()) != Math.round(tx)) throw new IllegalStateException("Picker missed x: " + pickerAt());
    }

    static void fine(double target, boolean horizontal) throws Exception {
        for (int guard = 0; guard < 400; guard++) {
            double at = horizontal ? ws.positionPicker().x() : ws.positionPicker().y();
            if (Math.round(at) == Math.round(target)) return;
            int key = horizontal ? (target > at ? GLFW_KEY_RIGHT : GLFW_KEY_LEFT) : (target > at ? GLFW_KEY_DOWN : GLFW_KEY_UP);
            input.handleKeyEvent(key, GLFW_PRESS);
            pickerTick();
            input.handleKeyEvent(key, GLFW_RELEASE);
            pickerTick();
        }
    }

    /** One tick with the current held-key state, drawn. */
    static void pickerTick() throws Exception {
        input.refreshLogicalSnapshot();
        ws.tick(input);
        input.update();
        frame();
    }

    // ------------------------------------------------------------------ menus
    static Method formRows; static Field selected;

    static int selectedIndex() throws Exception {
        if (selected == null) { selected = EditorProjectMenu.class.getDeclaredField("selected"); selected.setAccessible(true); }
        return selected.getInt(ws.menu());
    }

    @SuppressWarnings("unchecked")
    static List<Object> rows() throws Exception {
        if (formRows == null) { formRows = EditorProjectMenu.class.getDeclaredMethod("formRows"); formRows.setAccessible(true); }
        return (List<Object>) formRows.invoke(ws.menu());
    }

    static Method rowField, rowSection;
    /** Row is a private record of EditorProjectMenu; its accessors need setAccessible. */
    static String rowKey(Object row) throws Exception {
        if (rowField == null) {
            rowField = row.getClass().getDeclaredMethod("field"); rowField.setAccessible(true);
            rowSection = row.getClass().getDeclaredMethod("section"); rowSection.setAccessible(true);
        }
        var field = (EditorProjectMenu.Field) rowField.invoke(row);
        if (field != null) return field.key();
        return "#section:" + rowSection.invoke(row);
    }

    /** Moves the highlight to a form field by key, one row per step, drawing each step. */
    static void selectField(String key) throws Exception {
        var rows = rows();
        int target = -1;
        for (int i = 0; i < rows.size(); i++) if (rowKey(rows.get(i)).equals(key)) target = i;
        if (target < 0) {
            var keys = new ArrayList<String>(); for (var r : rows) keys.add(rowKey(r));
            throw new IllegalStateException("No row " + key + " in " + ws.menu().title() + ": " + keys);
        }
        moveTo(target);
    }

    static void selectSubmit() throws Exception { moveTo(rows().size()); }

    static void selectAction(String prefix) throws Exception {
        var entries = ws.menu().actionEntries();
        for (int i = 0; i < entries.size(); i++) if (entries.get(i).label().startsWith(prefix)) { moveTo(i); return; }
        throw new IllegalStateException("No action " + prefix + " in " + ws.menu().title() + ": " + actionLabels());
    }

    static void selectActionIndex(int index) throws Exception { moveTo(index); }

    static void moveTo(int target) throws Exception {
        for (int guard = 0; guard < 80 && selectedIndex() != target; guard++) {
            press(selectedIndex() < target ? GLFW_KEY_DOWN : GLFW_KEY_UP);
            hold(6);
        }
        if (selectedIndex() != target) throw new IllegalStateException("Could not reach row " + target);
    }

    static String actionLabels() {
        var labels = new ArrayList<String>();
        for (var a : ws.menu().actionEntries()) labels.add(a.label());
        return labels.toString();
    }

    /** Enter cycles a choice field, so the form shows each value in turn. */
    static void cycleTo(String key, String value) throws Exception {
        selectField(key);
        for (int guard = 0; guard < 10 && !value.equals(ws.menu().values().get(key)); guard++) {
            press(GLFW_KEY_ENTER);
            hold(14);
        }
        if (!value.equals(ws.menu().values().get(key))) throw new IllegalStateException(key + " did not reach " + value + ": " + ws.menu().values().get(key));
        event("set " + key + " = " + value);
    }

    static void requireMenu(String title) {
        if (!ws.menu().isOpen() || !ws.menu().title().equals(title))
            throw new IllegalStateException("Expected menu " + title + " but found " + (ws.menu().isOpen() ? ws.menu().title() : "none") + "; status " + ws.status());
    }

    static void requireNoMenuError() {
        if (ws.menu().error() != null) throw new IllegalStateException("Menu error: " + ws.menu().error());
    }

    /** HUD-level keys (cast rows, timeline) go through the chrome, as the engine routes them. */
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

    static void press(int key) throws Exception {
        input.handleKeyEvent(key, GLFW_PRESS);
        input.refreshLogicalSnapshot();
        ws.tick(input);
        input.update();
        input.handleKeyEvent(key, GLFW_RELEASE);
        input.update();
    }

    static Method append;
    /** InputHandler's text queue is package-private; the capture feeds it as GLFW's char callback would. */
    static void typeText(String text) throws Exception {
        if (append == null) { append = InputHandler.class.getDeclaredMethod("appendMenuCodepoint", int.class); append.setAccessible(true); }
        for (char c : text.toCharArray()) {
            append.invoke(input, (int) c);
            input.refreshLogicalSnapshot();
            ws.tick(input);
            input.update();
            hold(5);
        }
    }

    static void panCamera(double dx, double dy, int frames) throws Exception {
        double zoom = ws.directorCamera().zoom();
        for (int i = 0; i < frames; i++) {
            double t0 = smooth(i / (double) frames), t1 = smooth((i + 1) / (double) frames);
            ws.moveCamera((t1 - t0) * dx * zoom, (t1 - t0) * dy * zoom, 1);
            frame();
        }
    }

    static double smooth(double t) { return t * t * (3 - 2 * t); }

    static void awaitRoute(StageplayRouteJob.Phase phase, int framesPerPoll) throws Exception {
        long deadline = System.nanoTime() + 180_000_000_000L;
        while (System.nanoTime() < deadline) {
            ws.tick(new InputHandler());
            var update = session.pollRoute();
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
        if (!desktop && ws.menu().isOpen()) {
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
        e.put("menu", ws.menu().isOpen() ? ws.menu().title() : "");
        e.put("picking", ws.pickingPosition());
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
