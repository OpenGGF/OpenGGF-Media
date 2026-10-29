/*
 * Super Sonic cut (menu-evolution, 2026-10-29): identity probe for the bed. Loads engine music 0x93 through
 * the production Sonic2SmpsLoader from the S2 REV01 ROM given as argv[0] and prints its ROM offset, decompressed
 * length and first 12 header bytes, to compare with Supersonic_Header in s2disasm "96 - Super Sonic.asm"
 * (voice pointer, smpsHeaderChan $06,$03, smpsHeaderTempo $01,$FA). Compile against the d823ce643 classpath:
 *   javac -d target/recut-probe -cp "target/classes:$(cat target/cp.txt)" HeaderProbe.java
 *   java -cp "target/recut-probe:target/classes:$(cat target/cp.txt)" HeaderProbe <S2 REV01 ROM>
 * Output at d823ce643: offset=fcbbc len=755 header=F6 15 06 03 01 FA CB 15 00 00 B0 13
 */
import com.openggf.data.Rom;
import com.openggf.game.sonic2.audio.smps.Sonic2SmpsLoader;
public class HeaderProbe {
  public static void main(String[] a) throws Exception {
    Rom rom = new Rom(); rom.open(a[0]);
    Sonic2SmpsLoader l = new Sonic2SmpsLoader(rom);
    byte[] d = l.loadMusic(0x93).getData();
    StringBuilder s = new StringBuilder();
    for (int i = 0; i < 12; i++) s.append(String.format("%02X ", d[i] & 0xFF));
    System.out.println("offset=" + Integer.toHexString(l.findMusicOffset(0x93)) + " len=" + d.length + " header=" + s);
  }
}
