// Purpose: positioned native presentation capture and ROM spawn/score scouting.
// Inputs: built jar, verified ROM, declared mode/zone/act, roundtripped controller log.
// Origin: MICA & TALON promo phase 2, 2026-11-10. No comparison trace input.
// 2026-11-11 production variant: -Dpromo.rings / -Dpromo.timer declare HUD rings and level timer (frames).
// 2026-11-11 redo: -Dpromo.width selects the engine view width (320 default, 400 widescreen).
import com.openggf.tools.*;
import com.openggf.game.*;
import com.openggf.graphics.*;
import com.openggf.debug.playback.*;
import java.nio.file.*;
import static org.lwjgl.opengl.GL11.*;
public class PromoCapture {
 public static void main(String[] a)throws Exception {
 String mode=a[0];Path out=Path.of(a[1]);Files.createDirectories(out.resolve("frames"));
 int zone=Integer.parseInt(a[4]),act=Integer.parseInt(a[5]);
 Integer x=a.length>6?Integer.valueOf(a[6]):null,y=a.length>7?Integer.valueOf(a[7]):null;
 var set=new GameplayCaptureSession.Settings(Integer.getInteger("promo.width",320),"mica-and-talon:mica",(mode.equals("probe")||mode.equals("hero"))?"":"mica-and-talon:talon","off",null,x,y,null,false,false,null,null,false,Integer.getInteger("promo.rings",70),false,false);
 try(var s=new GameplayCaptureSession(set)) {
 s.applyMod(Path.of(a[2]));s.boot(Path.of(a[3]),zone,act,set);
 if(System.getProperty("promo.timer")!=null)s.declareTimer(Long.getLong("promo.timer"));
 if(mode.equals("scout")) {for(int i=0;i<120;i++){s.step(null);s.renderFrame();}for(var ob:GameServices.level().getObjectManager().getActiveObjects())System.out.println("ACTIVE "+ob.getClass()+" "+ob.getSpawn());for(var o:GameServices.level().getObjectManager().getAllSpawns())System.out.println(o);return;}
 for(int i=0;i<120 && !(mode.equals("probe")||mode.equals("hero"));i++)s.step(null);
 if(mode.equals("halfpipe")) {
 com.openggf.sprites.NativePositionOps.writeXPosPreserveSubpixel(s.player(),3568);com.openggf.sprites.NativePositionOps.writeYPosPreserveSubpixel(s.player(),150);s.player().setRingCount(70);GameServices.camera().updatePosition(true);

 ((com.openggf.game.CheckpointState)GameServices.level().getObjectManager().getObjectServices().checkpointState()).clear();
 var spawn=GameServices.level().getObjectManager().getAllSpawns().stream().filter(o->o.objectId()==0x79 && o.x()==3568).findFirst().orElseThrow();
 GameServices.level().getObjectManager().createDynamicObject(()->new com.openggf.game.sonic2.objects.CheckpointObjectInstance(spawn,"ROM starpost component entry"));
 }
 com.openggf.Engine engine=null;
 if(mode.equals("continue")) {
 var st=GameServices.gameState();while(st.getLives()>0)st.loseLife();st.addContinue();st.addContinue();st.addContinue();
 GameServices.level().requestGameOverExit(GameOverExit.CONTINUE_SCREEN);
 for(int i=0;i<120&&s.loop().getCurrentGameMode()!=GameMode.CONTINUE_SCREEN;i++){s.step(null);s.renderFrame();}
 } else if(mode.equals("ending")) {
 s.loop().closePresence();engine=new com.openggf.Engine();engine.setInputHandler(new com.openggf.control.InputHandler());
 var bind=com.openggf.Engine.class.getDeclaredMethod("bindGameplayMode",com.openggf.game.session.GameplayModeContext.class);bind.setAccessible(true);bind.invoke(engine,com.openggf.game.session.SessionManager.getCurrentGameplayMode());
 var reshape=com.openggf.Engine.class.getDeclaredMethod("reshape",int.class,int.class);reshape.setAccessible(true);reshape.invoke(engine,320,224);GameServices.graphics().setProjectionMatrixBuffer(engine.getProjectionMatrixBuffer());
 GameServices.fade().cancel();GameServices.level().requestCreditsTransition();engine.getGameLoop().step();
 }
 var movie=a.length>8?new Bk2MovieLoader().loadMovieOrInputLog(Path.of(a[8])):null;
 int count=movie==null?(mode.equals("ending")?6000:480):movie.getFrameCount();
 var csv=new StringBuilder(GameplayCaptureSession.stateHeader()+",score\n");
 var draw=com.openggf.Engine.class.getDeclaredMethod("draw");draw.setAccessible(true);
 for(int i=0;i<count;i++) {
 var input=movie==null?null:movie.getFrame(i);
 if(engine==null)s.step(input);else { if(engine.getGameLoop().getCurrentGameMode()!=GameMode.ENDING_CUTSCENE)break;engine.getGameLoop().step(); }
 csv.append(s.stateLine(i,input)).append(',').append(GameServices.gameState().getScore()).append('\n');
 if(mode.equals("probe"))continue;
 RgbaImage im;
 if(mode.equals("continue")) {
 glClearColor(0,0,0,1);glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);GameServices.graphics().resetForFixedFunction();GameServices.camera().setX((short)0);GameServices.camera().setY((short)0);s.loop().getContinueScreenProvider().draw();GameServices.graphics().flushScreenSpace();glFinish();im=ScreenshotCapture.captureFramebuffer(320,224);
 }else if(engine!=null){glDisable(GL_SCISSOR_TEST);engine.getGameLoop().getEndingProvider().setClearColor();glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);draw.invoke(engine);GameServices.graphics().flushScreenSpace();glFinish();im=ScreenshotCapture.captureFramebuffer(320,224);}
 else im=s.render();
 ScreenshotCapture.savePNG(im,out.resolve("frames/%06d.png".formatted(i)));
 }
 Files.writeString(out.resolve("state.csv"),csv);
 }
 }
}
