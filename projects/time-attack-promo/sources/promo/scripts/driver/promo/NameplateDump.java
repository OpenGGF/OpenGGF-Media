package promo;

import com.openggf.mods.ui.NameFont;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.nio.file.*;
import java.util.List;

/**
 * PROMO FIXTURE (ta-promo-a, 2026-10-23; not committed). Dumps strings drawn by the engine's own
 * NameFont (Fusion Pixel 10px + Unifont fallback, the ghost-nameplate face) as 1x white-on-clear
 * PNG masks, so the promo can enlarge the game's exact glyph pixels.
 * Args: OUT_DIR then lines "key=text".
 */
public final class NameplateDump {
    public static void main(String[] args) throws Exception {
        Path out = Path.of(args[0]);
        Files.createDirectories(out);
        StringBuilder index = new StringBuilder();
        for (String arg : List.of(args).subList(1, args.length)) {
            String key = arg.substring(0, arg.indexOf('=')), text = arg.substring(arg.indexOf('=') + 1);
            int[] extent = NameFont.extent(text);
            int w = Math.max(1, NameFont.width(text)), h = extent[1] - extent[0] + 1;
            BufferedImage img = new BufferedImage(w + 2, h, BufferedImage.TYPE_INT_ARGB);
            NameFont.glyphs(text, 0, -extent[0], (x, y, rw, rh) -> {
                for (int yy = y; yy < y + rh; yy++)
                    for (int xx = x; xx < x + rw; xx++)
                        if (xx >= 0 && yy >= 0 && xx < img.getWidth() && yy < img.getHeight()) img.setRGB(xx, yy, 0xFFFFFFFF);
            });
            ImageIO.write(img, "png", out.resolve(key + ".png").toFile());
            index.append(key).append('\t').append(w).append('\t').append(-extent[0]).append('\t').append(text).append('\n');
        }
        Files.writeString(out.resolve("index.tsv"), index.toString());
    }
}
