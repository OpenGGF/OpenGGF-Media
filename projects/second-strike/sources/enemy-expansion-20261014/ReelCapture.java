/* Positioned Second Strike reel capture, originating delivered engine a8221fb7d.
 * Inputs: name, output, engine ROM, creator jar. Uses ordinary GameLoop and ROM art;
 * Caterkiller explicitly seeds apparent act0 for inherited fire continuation.
 * Capture setup is supplementary presentation, not a cold route/parity oracle.
 */
import com.openggf.tools.*;
import com.openggf.game.GameServices;
import com.openggf.debug.playback.Bk2MovieLoader;
import com.openggf.graphics.ScreenshotCapture;
import java.nio.file.*;
import java.io.*;
import java.util.Locale;
import javax.sound.sampled.*;

public class ReelCapture {
 public static void main(String[] args) throws Exception {
  String name=args[0]; Path out=Path.of(args[1]), rom=Path.of(args[2]), mod=Path.of(args[3]);
  if(Files.exists(out.resolve("state.csv"))) throw new IllegalStateException("Existing take preserved");
  Files.createDirectories(out.resolve("frames"));
  boolean cata=name.equals("caterkiller");
  int width=cata?800:name.equals("plant")?528:320;
  int x=cata?2180:name.equals("plant")?0x1D60:0x1BC0;
  int y=cata?830:name.equals("plant")?0x26C:0x3B0;
  int frames=360;
  String script=cata?"360 -":"24 -; 12 A; 324 -";
  Files.writeString(out.resolve("input.script"),script+"\n");
  InputLogAuthorTool.author(script,out.resolve("input.bk2"),"s3k");
  var movie=new Bk2MovieLoader().loadMovieOrInputLog(out.resolve("input.bk2"));
  var settings=new GameplayCaptureSession.Settings(width,"sonic","","off",null,x,y,null,false,false,null,null,false,20,false);
  Path pcm=out.resolve("audio.pcm"); int sampleRate;
  try(var session=new GameplayCaptureSession(settings);
      var state=Files.newBufferedWriter(out.resolve("state.csv"));
      var objects=Files.newBufferedWriter(out.resolve("objects.csv"))) {
   session.applyMod(mod); session.enableAudio(); session.boot(rom,0,cata?1:0,settings);
   if(cata)GameServices.level().setApparentAct(0);
   var audio=GameServices.audio(); sampleRate=audio.outputSampleRate();
   state.write(GameplayCaptureSession.stateHeader()+",physical_act,apparent_act\n");
   objects.write("frame,type,x,y\n");
   try(var capture=audio.beginLiveCaptureAudio(60); var raw=Files.newOutputStream(pcm)) {
    short[] samples=new short[capture.maxStereoFramesPerPacket()*2];
    for(int frame=0;frame<frames;frame++) {
     var input=movie.getFrame(frame);session.step(input);session.loop().presentOuterFrame(false,false);
     int count=capture.drainPresentationFrame(samples)*2;
     byte[] bytes=new byte[count*2];for(int i=0;i<count;i++){bytes[i*2]=(byte)samples[i];bytes[i*2+1]=(byte)(samples[i]>>>8);}raw.write(bytes);
     state.write(session.stateLine(frame,input)+","+(cata?1:0)+","+GameServices.level().getApparentAct()+"\n");
     for(var object:GameServices.level().getObjectManager().getActiveObjects()) {
      String type=object.getClass().getSimpleName();
      if(type.contains("Caterkiller")||type.contains("Guard")||type.contains("Artillery")||type.contains("Committed"))
       objects.write(frame+","+type+","+object.getX()+","+object.getY()+"\n");
     }
     ScreenshotCapture.savePNG(session.render(),out.resolve("frames").resolve(String.format(Locale.ROOT,"%05d.png",frame)));
    }
   }
  }
  var format=new AudioFormat(sampleRate,16,2,true,false);
  try(var in=new AudioInputStream(Files.newInputStream(pcm),format,Files.size(pcm)/4)) {
   AudioSystem.write(in,AudioFileFormat.Type.WAVE,out.resolve("audio.wav").toFile());
  }
  Files.delete(pcm);
  Files.writeString(out.resolve("setup.txt"),"Delivered engine a8221fb7d5eb48f5bb199602227ec6ab4bbbf945; 7277cef4 evidence-only successor.\n"
   +"Positioned supplementary capture; native physics, normal GameLoop/input, original ROM. 60fps, stride1, native stereo PCM.\n"
   +"name="+name+" width="+width+" x="+x+" y="+y+" physical_act="+(cata?1:0)+" apparent_act="+(cata?0:0)+"\n"
   +"Declared incoming rings20; no invulnerability, debug damage, object injection or trace hydration.\n"
   +(cata?"Inherited fire continuation apparent_act0 is explicitly seeded before first native step; not cold-entry proof.\n":""));
  System.out.println("Captured "+name+" frames="+frames+" rate="+sampleRate);
 }
}
