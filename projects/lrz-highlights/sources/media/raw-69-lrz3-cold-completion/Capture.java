import com.openggf.tools.GameplayCaptureSession;
import com.openggf.debug.playback.Bk2MovieLoader;
import com.openggf.graphics.ScreenshotCapture;
import java.nio.file.*;
/** Replays authored controller input from fresh LRZ boss-act entry with a fire shield. */
public class Capture {
 public static void main(String[] args) throws Exception {
  Path root=Path.of(args[0]); Files.createDirectories(root.resolve("frames"));
  var movie=new Bk2MovieLoader().loadMovieOrInputLog(root.resolve("InputLog.txt"));
  var settings=new GameplayCaptureSession.Settings(320,"sonic","tails","off",null,null,null,null,false,false,null,null,37);
  try(var session=new GameplayCaptureSession(settings);var states=Files.newBufferedWriter(root.resolve("state.csv"))) {
   session.boot(Path.of("/home/farrell/code/projects/OpenGGF/s3k.gen"),22,0,settings);
   session.player().giveShield(com.openggf.game.ShieldType.FIRE);
   states.write(GameplayCaptureSession.stateHeader());states.newLine();
   for(int frame=0;frame<12820;frame++) {
    var input=movie.getFrame(frame);session.step(input);
    states.write(session.stateLine(frame,input));states.newLine();
    ScreenshotCapture.savePNG(session.render(),root.resolve(String.format("frames/%05d.png",frame)));
   }
  }
 }
}
