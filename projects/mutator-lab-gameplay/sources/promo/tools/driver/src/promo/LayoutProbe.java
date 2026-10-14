package promo;

/*
 * LayoutProbe — dumps an act's ring placements and object spawns (with registry names) to CSV
 * so promo shots can be planned on real layouts (task e0603654). Boots through
 * GameplayCaptureSession on the display-free GL path; reads the loaded Level only.
 * Args: game romPath zoneName act(1-based) outDir
 */
import com.openggf.game.GameServices;
import com.openggf.tools.GameplayCaptureSession;
import java.nio.file.*;
import java.util.Locale;

public final class LayoutProbe {
    public static void main(String[] a) throws Exception {
        String game = a[0]; Path rom = Path.of(a[1]); String zone = a[2]; int act = Integer.parseInt(a[3]) - 1;
        Path out = Path.of(a[4]); Files.createDirectories(out);
        var settings = new GameplayCaptureSession.Settings(320, "sonic", "", "off", null, null, null, null, false,
                false, null, null, false, null, false);
        String cls = switch (game) { case "s3k" -> "com.openggf.game.sonic3k.constants.Sonic3kZoneIds";
            case "s1" -> "com.openggf.game.sonic1.constants.Sonic1Constants"; default -> "com.openggf.game.sonic2.Sonic2LevelEventManager"; };
        int z = zone.matches("\\d+") ? Integer.parseInt(zone) : Class.forName(cls).getField("ZONE_" + zone.toUpperCase(Locale.ROOT)).getInt(null);
        try (var s = new GameplayCaptureSession(settings)) {
            s.boot(rom, z, act, settings);
            var level = GameServices.level().getCurrentLevel();
            var reg = GameServices.module().createObjectRegistry();
            var sb = new StringBuilder("x,y\n");
            for (var r : level.getRings()) sb.append(r.x()).append(',').append(r.y()).append('\n');
            Files.writeString(out.resolve("rings.csv"), sb);
            var ob = new StringBuilder("x,y,id,subtype,name\n");
            for (var o : level.getObjects())
                ob.append(o.x()).append(',').append(o.y()).append(',').append(String.format("%02X", o.objectId())).append(',')
                  .append(String.format("%02X", o.subtype())).append(',').append(reg.getPrimaryName(o.objectId())).append('\n');
            Files.writeString(out.resolve("objects.csv"), ob);
            var p = s.player();
            Files.writeString(out.resolve("start.txt"), p.getCentreX() + "," + p.getCentreY() + "\n");
        }
    }
}
