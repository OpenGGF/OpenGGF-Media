// Purpose: positioned native gameplay capture with a DECLARED SCORE, beside the declared rings, timer and
//   emeralds that GameplayCaptureTool already takes. The tool has no score flag, so a mid-act positioned start
//   reads SCORE 0. The score is added after boot through GameStateManager.addScore, the public call gameplay
//   itself uses; the HUD then draws it natively. Nothing is painted over a frame.
//   Otherwise this mirrors GameplayCaptureTool's loop exactly: step, state line, render, PNG, every frame.
// Inputs (argv): mode(ignored) outDir jar|- rom zoneIndex actIndex x y inputLog
// Props: promo.main (mica|talon|<stock key>), promo.sidekick (talon|mica|<stock key>|none), promo.emeralds,
//   promo.rings, promo.timer (frames), promo.score, promo.stock=true (no mod, stock keys).
// Origin: MICA & TALON promo redo, lead review of the storyboard, 2026-11-12.
// 2026-11-12 stage B: audio.wav through hosts/common/PromoAudio (SFX only, music volume 0).
import com.openggf.tools.*;
import com.openggf.game.*;
import com.openggf.graphics.*;
import com.openggf.debug.playback.*;
import java.nio.file.*;

public class PromoCapture {
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
            var csv = new StringBuilder(GameplayCaptureSession.stateHeader() + ",score\n");
            for (int i = 0; i < movie.getFrameCount(); i++) {
                var input = movie.getFrame(i);
                s.step(input);
                au.frame(s.loop(), true);
                csv.append(s.stateLine(i, input)).append(',').append(GameServices.gameState().getScore()).append('\n');
                if (every > 0 && i % every == 0) ScreenshotCapture.savePNG(s.render(), out.resolve("frames/%06d.png".formatted(i)));
            }
            au.close();
            Files.writeString(out.resolve("state.csv"), csv);
        }
    }
}
