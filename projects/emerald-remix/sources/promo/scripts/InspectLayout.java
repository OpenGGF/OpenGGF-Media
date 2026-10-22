/* Emerald Remix promo capture reconnaissance, 2026-10-22.
 * Reads loaded object positions/identities only. No gameplay state changes. */
import com.openggf.tools.GameplayCaptureSession;
import com.openggf.game.GameServices;
import java.nio.file.Path;
public class InspectLayout {
 public static void main(String[] a) throws Exception {
  var settings=new GameplayCaptureSession.Settings(400,"sonic","none","off",null,null,null,null,false,false,null,null,false,null,false);
  try(var s=new GameplayCaptureSession(settings)) {
   if(!a[0].equals("stock")) s.applyMod(Path.of(a[0]));
   s.boot(Path.of(a[1]),Integer.parseInt(a[2]),0,settings);
   var lm=GameServices.level();var level=lm.getCurrentLevel();
   System.out.println("IDENTITY module="+GameServices.module().getClass().getName()+" zone="+lm.getCurrentZone()+" act="+lm.getCurrentAct());
   for(var o:level.getObjects()) if(o.objectId()==6 || o.objectId()==0x41 || o.objectId()==0x0D)System.out.println("OBJECT id="+o.objectId()+" x="+o.x()+" y="+o.y()+" subtype="+o.subtype());
  }
 }
}
