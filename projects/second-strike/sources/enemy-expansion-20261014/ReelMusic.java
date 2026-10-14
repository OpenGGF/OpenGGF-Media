/* Native AIZ soundtrack stem for the Second Strike short reel, a8221fb7d.
 * The existing production audio owner advances SMPS. No external music/SFX;
 * gameplay is held after boot so no attack/ring effects contaminate the bed.
 */
import com.openggf.tools.GameplayCaptureSession;
import com.openggf.game.GameServices;
import java.nio.file.*;
import javax.sound.sampled.*;
public class ReelMusic {
 public static void main(String[] args)throws Exception {
  Path out=Path.of(args[0]);Files.createDirectories(out);
  var settings=new GameplayCaptureSession.Settings(320,"sonic","","off",null,0x1BC0,0x3B0);
  int rate;Path pcm=out.resolve("music.pcm");
  try(var session=new GameplayCaptureSession(settings)) {
   session.enableAudio();session.boot(Path.of(args[1]),0,0,settings);session.step(null);
   var audio=GameServices.audio();audio.stopAllSfx();rate=audio.outputSampleRate();
   try(var capture=audio.beginLiveCaptureAudio(60);var raw=Files.newOutputStream(pcm)){
    short[] samples=new short[capture.maxStereoFramesPerPacket()*2];
    for(int frame=0;frame<900;frame++){
     session.loop().presentOuterFrame(false,false);
     int count=capture.drainPresentationFrame(samples)*2;byte[] bytes=new byte[count*2];
     for(int i=0;i<count;i++){bytes[i*2]=(byte)samples[i];bytes[i*2+1]=(byte)(samples[i]>>>8);}raw.write(bytes);
    }
   }
  }
  var format=new AudioFormat(rate,16,2,true,false);
  try(var in=new AudioInputStream(Files.newInputStream(pcm),format,Files.size(pcm)/4)){AudioSystem.write(in,AudioFileFormat.Type.WAVE,out.resolve("music.wav").toFile());}
  Files.delete(pcm);System.out.println("Native music stem:900presentations at60Hz");
 }
}
