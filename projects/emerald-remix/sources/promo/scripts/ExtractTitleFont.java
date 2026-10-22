/* Emerald Remix promo 2026-10-22: dump native S2 ROM title-card alphabet.
 * Inputs: verified REV01 ROM, output dir. Uses production Nemesis decompressor,
 * TitleCardManager LETTER_OFFSETS/SIZES and ZONE mapping; column-major tiles.
 * No disassembly art or system-font replacement. */
import com.openggf.data.Rom;
import com.openggf.level.Pattern;
import com.openggf.util.PatternDecompressor;
import com.openggf.game.sonic2.constants.Sonic2Constants;
import java.nio.file.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
public class ExtractTitleFont {
 public static void main(String[] a)throws Exception {
  Rom rom=new Rom();if(!rom.open(a[0]))throw new Exception("ROM open failed");
  Pattern[] base=PatternDecompressor.nemesis(rom,Sonic2Constants.ART_NEM_TITLE_CARD_ADDR,"Promo title base");
  Pattern[] letters=PatternDecompressor.nemesis(rom,Sonic2Constants.ART_NEM_TITLE_CARD2_ADDR,"Promo title alphabet");
  int[] offsets={0,4,8,12,-1,16,20,24,28,30,34,38,42,-1,-1,48,52,56,60,64,68,72,76,82,86,-1};
  int[] sizes={4,4,4,4,4,4,4,4,2,4,4,4,6,4,4,4,4,4,4,4,4,4,6,4,4,4};
  Path out=Path.of(a[1]);Files.createDirectories(out);StringBuilder font=new StringBuilder();
  for(int k=0;k<26;k++){
   char ch=(char)('A'+k);int off=offsets[k];Pattern[] src=letters;
   if(off<0){src=base;off=switch(ch){case 'E'->0;case 'N'->4;case 'O'->8;case 'Z'->12;default->throw new Exception();};}
   int w=sizes[k]/2*8; BufferedImage img=new BufferedImage(w,16,BufferedImage.TYPE_INT_ARGB);
   font.append("= ").append(ch).append('\n');
   for(int y=0;y<16;y++){for(int x=0;x<w;x++){
    int colour=src[off+(x/8)*2+y/8].getPixel(x%8,y%8);boolean ink=colour!=0;
    // Preserve every source palette index, including the native black/grey bevel.
    font.append(colour==0?'.':Character.forDigit(colour,16));
    int rgb=switch(colour){case 1->0x000000;case 6->0xffffff;case 7->0xb6b6b6;case 8->0x929292;default->0;};
    img.setRGB(x,y,ink?(0xff000000|rgb):0);
   }font.append('\n');}ImageIO.write(img,"png",out.resolve(ch+".png").toFile());
  }
  Files.writeString(out.resolve("s2-title-font.txt"),font.toString());rom.close();
  System.out.println("Extracted A-Z: base="+base.length+" alphabet="+letters.length+" patterns");
 }
}
