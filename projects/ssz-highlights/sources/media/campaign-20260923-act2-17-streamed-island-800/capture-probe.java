import com.openggf.tools.GameplayCaptureSession;
import com.openggf.game.GameServices;
import com.openggf.game.sonic3k.runtime.SszZoneRuntimeState;
import com.openggf.graphics.ScreenshotCapture;
import java.nio.file.*;
class SszSecondIslandVideoProbe {
 public static void main(String[] args) throws Exception {
  int width=Integer.parseInt(args[0]);
  Path out=Path.of(args[1]);Files.createDirectories(out);
  var settings=new GameplayCaptureSession.Settings(width,"knuckles","","off",null,null,null,"0000000",false,false,410766,null);
  try(var session=new GameplayCaptureSession(settings)) {
   session.boot(Path.of("/home/farrell/code/projects/OpenGGF/s3k.gen"),10,1,settings);
   session.player().setDebugMode(true);
   for(int i=0;i<300;i++)session.step(null);
   var state=(SszZoneRuntimeState)GameServices.zoneRuntimeState();
   state.setEndingRunning(true);state.setForegroundRoutine(8);state.setEventsFg4(0xFF00);state.setSpecialVIntRoutine(4);
   GameServices.camera().setScrollLocked(true);
   int prior=-1; boolean secondSeed=false;
   var log=Files.newBufferedWriter(out.resolve("state.csv")); log.write("frame,stage,camera_y,drift,remaining\n");
   for(int frame=0;frame<5000;frame++) {
    session.step(null);
    int stage=state.foregroundRoutine();
    if(stage==16 && !secondSeed) { state.setEventsFg4(0xFF); secondSeed=true; }
    log.write(frame+","+stage+","+GameServices.camera().getY()+","+state.cloudDrift()+","+state.endingPlane().remaining()+"\n");
    if(stage!=prior || frame%100==0)System.out.println("ISLAND "+frame+" stage="+stage+" camera="+GameServices.camera().getY()+" cloud="+state.cloudOffsetFixed()+" signal="+state.eventsFg4());
    if(frame>=1400)ScreenshotCapture.savePNG(session.render(),out.resolve(String.format("%05d.png",frame)));
    prior=stage;
    if(stage==24 && GameServices.camera().getY()==0x804 && GameServices.level().getObjectManager().activeObjectsOfType(com.openggf.game.sonic3k.objects.SszAct2CameraController.class).isEmpty())break;
   }
   log.close();
  }
 }
}
