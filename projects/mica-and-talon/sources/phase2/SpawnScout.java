// Purpose: locate ROM-placed checkpoints/enemies for positioned capture authoring.
// Inputs: current engine classpath, original ROM, freshly built mod; no state injection.
import com.openggf.tools.*;
import com.openggf.game.*;
import java.nio.file.*;
public class SpawnScout {
 public static void main(String[]args)throws Exception {
 var s=new GameplayCaptureSession.Settings(320,"mica-and-talon:mica","","off",null,1800,540,null,false,false,null,null,false,32,false,false);
 try(var session=new GameplayCaptureSession(s)) {
 session.applyMod(Path.of(args[1]));session.boot(Path.of(args[0]),0,0,s);
 for(var o:GameServices.level().getObjectManager().getAllSpawns())
 if(o.objectId()==0x79 || o.objectId()==0x9D || o.objectId()==0x98 || o.objectId()==0x9C)
 System.out.println(o);
 }
 }
}
