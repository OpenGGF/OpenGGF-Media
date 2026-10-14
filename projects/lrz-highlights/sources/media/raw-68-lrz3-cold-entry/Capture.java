import com.openggf.tools.GameplayCaptureSession;
import com.openggf.debug.playback.Bk2MovieLoader;
import com.openggf.graphics.ScreenshotCapture;
import com.openggf.game.GameServices;
import java.nio.file.*;
/** Fresh LRZ boss-act entry, original movie controls, explicit initial fire shield and 37 rings. */
public class Capture {
 public static void main(String[] args) throws Exception {
  Path root=Path.of(args[0]); Files.createDirectories(root.resolve("frames"));
  var movie=new Bk2MovieLoader().loadMovieOrInputLog(Path.of("/home/farrell/code/projects/OpenGGF/docs/BizHawk-2.11-linux-x64/Movies/s3k-sonic-tails-complete-emeralds.bk2"));
  var settings=new GameplayCaptureSession.Settings(320,"sonic","tails","off",null,null,null,null,false,false,null,null,37);
  try(var session=new GameplayCaptureSession(settings);var states=Files.newBufferedWriter(root.resolve("state.csv"));var objects=new java.io.PrintWriter(root.resolve("objects.csv").toFile())) {
   session.boot(Path.of("/home/farrell/code/projects/OpenGGF/s3k.gen"),22,0,settings);
   session.player().giveShield(com.openggf.game.ShieldType.FIRE);
   states.write(GameplayCaptureSession.stateHeader());states.newLine();
   objects.println("frame,slot,type,x,y,code,timer,subtype");
   for(int frame=0;frame<1500;frame++) {
    var input=movie.getFrame(428867+frame);session.step(input);
    states.write(session.stateLine(frame,input));states.newLine();
    for(var o:GameServices.level().getObjectManager().getActiveObjects()) {
     if(!(o instanceof com.openggf.game.sonic3k.objects.LrzAutoscrollObjectInstance))continue;
     objects.print(frame+","+((com.openggf.level.objects.AbstractObjectInstance)o).getSlotIndex()+","+o.getClass().getSimpleName()+","+o.getX()+","+o.getY());
     for(String key:new String[]{"code","timer","subtype"}) {var f=o.getClass().getDeclaredField(key);f.setAccessible(true);objects.print(","+f.get(o));}
     objects.println();
    }
    ScreenshotCapture.savePNG(session.render(),root.resolve(String.format("frames/%05d.png",frame)));
    if(session.player().getDead()) break;
   }
  }
 }
}
