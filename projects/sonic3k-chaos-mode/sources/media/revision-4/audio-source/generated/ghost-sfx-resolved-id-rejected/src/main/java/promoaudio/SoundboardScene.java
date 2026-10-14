package promoaudio;
import com.openggf.mods.scene.ModScene;
import com.openggf.mods.scene.SceneCanvas;
import com.openggf.mods.scene.SceneContext;
/** Native scene audio only; generated schedule comes from accepted capture events. */
public final class SoundboardScene implements ModScene {
    private static final int MUSIC = -1;
    private final int[] FRAMES = {124,139,601,650,665,729,748,748,767,776,784,792,800,808,816,824,832,840,848,856,856,873,896,896,904,904,912,912,919,920,920,928,928,936,936,944,944,952,952,960,960,968,968,976,976,981,983,984,984,989,996,1024,1024,1032,1040,1047,1048,1076,1111,1168,1175};
    private final int[] IDS = {52,51,146,98,146,146,185,53,138,168,168,168,168,168,168,168,168,168,168,168,168,138,168,168,168,168,168,168,146,168,168,168,168,168,168,168,168,168,168,168,168,168,168,168,168,52,146,168,168,51,52,168,168,168,168,146,168,162,146,217,146};
    private int frame, next;
    @Override public void enter(SceneContext ctx) {
        if (MUSIC >= 0) ctx.audio().playMusic(MUSIC);
        else ctx.audio().stopMusic();
    }
    @Override public void update(SceneContext ctx) {
        while (next < FRAMES.length && FRAMES[next] == frame)
            ctx.audio().playSfx(IDS[next++]);
        frame++;
    }
    @Override public void draw(SceneContext ctx, SceneCanvas canvas) { canvas.clear(0); }
}
