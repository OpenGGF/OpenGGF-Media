package flappytails;
import com.openggf.data.Rom;
import com.openggf.game.sonic3k.Sonic3kGameModule;
import com.openggf.mods.scene.*;
import com.openggf.mods.scene.art.*;
import com.openggf.mods.scene.host.SceneRomArtFactory;
import java.nio.file.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
/** First Typing of the Hedgehog promo (2026-10-10): extracts ROM title lettering using
 * the established Flappy CardFont. Inputs: own S3K ROM, output dir. Task-local, no assets
 * committed or runtime fallbacks. Produces transparent individual glyph PNGs and rings. */
public class PromoGlyphs {
 static void save(SceneImage im,Path p)throws Exception {BufferedImage b=new BufferedImage(im.width(),im.height(),BufferedImage.TYPE_INT_ARGB);b.setRGB(0,0,im.width(),im.height(),im.pixels(),0,im.width());ImageIO.write(b,"png",p.toFile());}
 public static void main(String[] a)throws Exception {
  Rom r=new Rom();r.open(a[0]);var rom=SceneRomArtFactory.forModule(new Sonic3kGameModule(),r);
  CardFont font=CardFont.load(rom);var field=CardFont.class.getDeclaredField("letters");field.setAccessible(true);
  SceneImage[] glyphs=(SceneImage[])field.get(font);Path out=Path.of(a[1]);Files.createDirectories(out);
  for(int i=0;i<26;i++)if(glyphs[i]!=null)save(glyphs[i],out.resolve(""+(char)('A'+i)+".png"));
  int[] pal=new PaletteAssembly().rom(rom,0x0A8A3C,0,16).rom(rom,0x0A8B7C,16,48).build();
  var rings=rom.sprites(StockSceneArt.S3K_RING.request(rom),pal);for(int i=0;i<rings.frameCount();i++)save(rings.frame(i).image(),out.resolve("ring-"+i+".png"));
  System.out.println("ROM glyphs extracted to "+out);
 }
}
