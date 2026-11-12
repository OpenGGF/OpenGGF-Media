// Purpose: the positioned capture host (hosts/positioned) plus per-frame POWERED-FORM STATE in state.csv, for the
//   leader and the first sidekick: Super flag, SuperState, powered tier, ring count, and whether the level timer
//   is paused (the ROM's Update_HUD_timer == 0, which is what makes a Super form revert at a boss kill or signpost).
//   Same loop as GameplayCaptureTool: step, state line, render, PNG, every frame. Nothing is painted over a frame.
// Inputs (argv): mode(ignored) outDir jar|- rom zoneIndex actIndex x y inputLog
// Props: promo.main, promo.sidekick, promo.emeralds, promo.rings, promo.timer (frames), promo.score, promo.stock.
// Extra columns: score, timer_paused, p1_super, p1_state, p1_tier, sk_super, sk_state, sk_tier, sk_rings
// Origin: MICA & TALON promo redo, lead review of the draft, 2026-11-12.
// 2026-11-12 stage B: audio.wav through hosts/common/PromoAudio (SFX only, music volume 0).
import com.openggf.tools.*;
import com.openggf.game.*;
import com.openggf.graphics.*;
import com.openggf.debug.playback.*;
import com.openggf.sprites.playable.AbstractPlayableSprite;
import java.nio.file.*;

public class PromoCapture {
    static String state(AbstractPlayableSprite p) {
        if (p == null) return ",,";
        var c = p.getSuperStateController();
        return (p.isSuperSonic() ? 1 : 0) + "," + (c == null ? "none" : c.getState()) + "," + (p.poweredTier() == null ? "" : p.poweredTier());
    }

    public static void main(String[] a) throws Exception {
        Path out = Path.of(a[1]);
        Files.createDirectories(out.resolve("frames"));
        boolean stock = Boolean.getBoolean("promo.stock");
        int zone = Integer.parseInt(a[4]), act = Integer.parseInt(a[5]);
        Integer x = Integer.valueOf(a[6]), y = Integer.valueOf(a[7]);
        String main = System.getProperty("promo.main", stock ? "sonic" : "mica");
        String side = System.getProperty("promo.sidekick", "none");
        String mainKey = stock ? main : "mica-and-talon:" + main;
        String sideKey = side.equals("none") ? "" : stock ? side : "mica-and-talon:" + side;
        var set = new GameplayCaptureSession.Settings(320, mainKey, sideKey, "off", null, x, y,
                System.getProperty("promo.emeralds"), false, false, null, null, false,
                Integer.getInteger("promo.rings"), false, false);
        try (var s = new GameplayCaptureSession(set)) {
            PromoAudio.enable(s);                 // SFX-only stem: synthesis on, music volume 0
            if (!stock) s.applyMod(Path.of(a[2]));
            s.boot(Path.of(a[3]), zone, act, set);
            if (System.getProperty("promo.timer") != null) s.declareTimer(Long.getLong("promo.timer"));
            int declared = Integer.getInteger("promo.score", 0);
            if (declared > 0) GameServices.gameState().addScore(declared);
            var movie = new Bk2MovieLoader().loadMovieOrInputLog(Path.of(a[8]));
            var au = PromoAudio.begin(out);
            int every = Integer.getInteger("promo.png.every", 1);   // 0 = state only (fast probes)
            var csv = new StringBuilder(GameplayCaptureSession.stateHeader()
                    + ",score,timer_paused,p1_super,p1_state,p1_tier,sk_super,sk_state,sk_tier,sk_rings\n");
            for (int i = 0; i < movie.getFrameCount(); i++) {
                var input = movie.getFrame(i);
                s.step(input);
                au.frame(s.loop(), true);
                AbstractPlayableSprite sk = null;
                for (var c : GameServices.sprites().getRegisteredSidekicks()) if (c != s.player()) { sk = c; break; }
                var ls = s.player().currentLevelState();
                csv.append(s.stateLine(i, input)).append(',').append(GameServices.gameState().getScore())
                        .append(',').append(ls != null && ls.isTimerPaused() ? 1 : 0)
                        .append(',').append(state(s.player())).append(',').append(state(sk))
                        .append(',').append(sk == null ? "" : sk.getRingCount()).append('\n');
                if (every > 0 && i % every == 0) ScreenshotCapture.savePNG(s.render(), out.resolve("frames/%06d.png".formatted(i)));
            }
            au.close();
            Files.writeString(out.resolve("state.csv"), csv);
        }
    }
}
