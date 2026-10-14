package board;
import com.openggf.mods.scene.*;
/**
 * One sound effect per 90-tick slot, music stopped: slot n starts at tick 30 + 90 n. The debug
 * command {@code music:XX} instead plays music id XX (hex) from the next tick.
 */
public final class Board implements ModScene, DebuggableScene {
    private static final String IDS = "B4,35,33,9F,BA,5B,B3,65,B6,AB,63,CC,B9,B0,68,6A,AF,BC";
    private long t;
    private int music = -1;
    private boolean started;
    @Override public void enter(SceneContext ctx) { ctx.audio().stopMusic(); }
    @Override public void update(SceneContext ctx) {
        t++;
        if (music >= 0) {
            if (!started) { ctx.audio().playMusic(music); started = true; }
            return;
        }
        if (t >= 30 && (t - 30) % 90 == 0) {
            String[] ids = IDS.split(",");
            int n = (int) ((t - 30) / 90);
            if (n < ids.length) ctx.audio().playSfx(Integer.parseInt(ids[n], 16));
        }
    }
    @Override public void draw(SceneContext ctx, SceneCanvas canvas) { canvas.clear(0); }
    @Override public boolean debugJump(String command) {
        if (!command.startsWith("music:")) return false;
        music = Integer.parseInt(command.substring(6), 16);
        return true;
    }
}
