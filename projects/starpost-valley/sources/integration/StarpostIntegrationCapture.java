package com.openggf;

import com.openggf.configuration.*;
import com.openggf.control.*;
import com.openggf.game.*;
import com.openggf.game.patch.*;
import com.openggf.game.session.*;
import com.openggf.graphics.*;
import com.openggf.mods.testing.ModTestKit;

import com.openggf.sprites.playable.AbstractPlayableSprite;
import com.openggf.tools.HeadlessGameBoot;
import java.nio.file.*;
import java.io.PrintWriter;
import java.util.*;
import static org.lwjgl.opengl.GL11.*;

/** Integration witness: real GameLoop input, terrain, scene menus and retained town session. */
public class StarpostIntegrationCapture {
 public static void main(String[] a) throws Exception {
  Path out=Files.createDirectories(Path.of(a[3]));
  try(var boot=new HeadlessGameBoot(400,224)) {
   var c=GameServices.configuration();
   c.setSessionOverride(SonicConfiguration.SONIC_1_ROM,Path.of(a[1]).toAbsolutePath().toString());
   c.setSessionOverride(SonicConfiguration.DISPLAY_ASPECT,"WIDE_16_9");
   c.setSessionOverride(SonicConfiguration.S3K_SKIP_INTROS,true);
   c.setSessionOverride(SonicConfiguration.TEST_MODE_ENABLED,false);
   c.setSessionOverride(SonicConfiguration.DEBUG_VIEW_ENABLED,false);
   c.setSessionOverride(SonicConfiguration.LIVE_REWIND_ENABLED,false);
   c.setSessionOverride(SonicConfiguration.AUDIO_ENABLED,true);
   c.resolveDisplayAspect();
   GameLoop loop=boot.boot(Path.of(a[0]),0,0);
   try(var kit=ModTestKit.openTrusted(Path.of(a[2]),out.resolve("storage"),
     LogicalRomResolver.fromRomManager(GameServices.rom()),c,List.of())) {
    GameModule root=GameServices.module();
    GameModule effective=kit.launch(root,new GameplayLaunchRequest("s3k","sonic",List.of()));
    ModSubsystem.current().installRewindClassResolver(kit.rewindClassResolver());
    var source=StockGameDataSources.pinned(GameServices.rom().getRom(),root);
    SessionManager.clear();
    var active=SessionManager.openGameplaySession(root,effective,source,null);
    GameplaySessionFactory.attachManagers(active,EngineServices.current(),new com.openggf.camera.Camera(c));
    loop.setGameplayMode(active); GameModuleRegistry.setCurrent(effective);
    var team=GameplayTeamBootstrap.registerActiveTeam(effective,GameServices.sprites(),c);
    GameServices.camera().setFocusedSprite(team.mainSprite());
    int zone=effective.getZoneRegistry().resolveZoneKey(new ZoneKey.Mod("starpost-valley","valley")).orElseThrow();
    loop.setGameMode(GameMode.LEVEL); GameServices.level().loadZoneAndAct(zone,0);
    GameServices.level().skipPendingInitialTitleCardPresentation();
    if(!ModSceneLauncher.openStartupScene(loop,c,0,GameServices.graphics(),400,224)) throw new AssertionError("no scene");
    if(!loop.modSceneHost.debugJump("new sonic")||!loop.modSceneHost.debugJump("close")) throw new AssertionError("no game");
    // Positioned start on the farm; every valley movement and door/gate interaction uses input.
    if(!loop.modSceneHost.debugJump("farm 1200 30")) throw new AssertionError("no farm start");
    Object scene=com.openggf.mods.code.OwnedSceneFactory.unwrap((com.openggf.mods.scene.ModScene)field(loop.modSceneHost,"scene")),shell=field(scene,"shell"),game=field(shell,"game");
    int stage=0,age=0,heldBefore=0;
    GameMode oldMode=loop.getCurrentGameMode();
    try(var csv=new PrintWriter(Files.newBufferedWriter(out.resolve("state.csv")));
        var audio=GameServices.audio().beginLiveCaptureAudio(60);
        var pcm=new java.io.DataOutputStream(Files.newOutputStream(out.resolve("audio.raw")))) {
     short[] samples=new short[audio.maxStereoFramesPerPacket()*2];
     csv.println("frame,stage,mode,x,y,gspeed,air,rings,wallet,clock,camx,camy,input");
     for(int f=0;f<2400;f++) {
      AbstractPlayableSprite p=(AbstractPlayableSprite)GameServices.camera().getFocusedSprite();
      int mask=0,action=0;
      if(stage==0 && age>=40 && age<150 && age%20==0) action=InputActionMasks.ACTION_A;
      if(stage==0 && age>50) mask=AbstractPlayableSprite.INPUT_RIGHT;
      if(stage==1 && age>45) mask=walking(p,896);
      if(stage==2 && age==1) mask=AbstractPlayableSprite.INPUT_UP;
      if(stage==3 && age==60) action=InputActionMasks.ACTION_B;
      if(stage==4 && age>40) mask=walking(p,150);
      if(stage==5 && age==1) mask=AbstractPlayableSprite.INPUT_UP;
      loop.getInputHandler().setLogicalOverride(LogicalInputSnapshot.ofPlayers(
       PlayerInputState.of(mask,mask&~heldBefore,action,action,false,false),PlayerInputState.neutral()));
      heldBefore=mask;
      loop.step();

      if(loop.getCurrentGameMode()==GameMode.MOD_SCENE || !loop.ownsGameplayFadeLifecycle())loop.resolveFadeManager().update();
      if(loop.getCurrentGameMode()!=oldMode) {
       oldMode=loop.getCurrentGameMode();
       if(oldMode==GameMode.LEVEL) GameServices.level().skipPendingInitialTitleCardPresentation();
      }
      var graphics=GameServices.graphics(); var level=GameServices.level();
      graphics.runPendingRenderThreadTasks();glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
      if(loop.getCurrentGameMode()==GameMode.MOD_SCENE) {
       ModSceneLauncher.draw(loop,graphics,graphics.getProjectionMatrixBuffer());
      } else {level.setClearColor();glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
       level.drawWithSpritePriority(GameServices.sprites(),true);}
      graphics.flush();loop.resolveFadeManager().render();glFinish();
      HeadlessGameBoot.presentHeadlessOuterAudioFrame();
      int stereoFrames=audio.drainPresentationFrame(samples);
      for(int sample=0;sample<stereoFrames*2;sample++)pcm.writeShort(Short.reverseBytes(samples[sample]));
      ScreenshotCapture.savePNG(ScreenshotCapture.captureFramebuffer(400,224),out.resolve(String.format("%04d.png",f)));
      p=(AbstractPlayableSprite)GameServices.camera().getFocusedSprite();
      csv.printf("%d,%d,%s,%d,%d,%d,%s,%d,%s,%s,%d,%d,%d%n",f,stage,loop.getCurrentGameMode(),
       p==null?0:p.getCentreX(),p==null?0:p.getCentreY(),p==null?0:p.getGSpeed(),p!=null&&p.getAir(),
       level.getLevelGamestate()==null?0:level.getLevelGamestate().getRings(),field(game,"rings"),call(field(game,"calendar"),"clock"),
       GameServices.camera().getX(),GameServices.camera().getY(),mask);
      age++;
      if(stage==0 && loop.getCurrentGameMode()==GameMode.LEVEL) {stage=1;age=0;}
      else if(stage==1 && age>45 && arrived(p,896)) {stage=2;age=0;}
      else if(stage==2 && loop.getCurrentGameMode()==GameMode.MOD_SCENE) {stage=3;age=0;}
      else if(stage==3 && loop.getCurrentGameMode()==GameMode.LEVEL) {stage=4;age=0;}
      else if(stage==4 && age>40 && arrived(p,150)) {stage=5;age=0;}
      else if(stage==5 && loop.getCurrentGameMode()==GameMode.MOD_SCENE) {stage=6;age=0;}
      else if(stage==6 && age>80) break;
      if(f==2399)throw new AssertionError("stalled at stage "+stage+" x="+(p==null?0:p.getCentreX()));
     }
    }
    if(!kit.findings().isEmpty())throw new AssertionError(kit.findings());
    if(!(boolean)call(call(shell,"screen"),"onFarm"))throw new AssertionError("not home");
    System.out.println("Round trip complete: no creator faults; same game, farm resumed");
    loop.modSceneHost.cleanup();
   }
  }
 }
 static boolean arrived(AbstractPlayableSprite p,int target) {return p!=null&&Math.abs(target-p.getCentreX())<=5&&Math.abs(p.getGSpeed())<154&&!p.getAir();}
 static int walking(AbstractPlayableSprite p,int target) {
  if(p==null)return 0;
  int distance=target-p.getCentreX(),direction=Integer.signum(distance);
  double speed=p.getGSpeed()/256.0;
  if(Math.signum(speed)==direction&&speed*speed>Math.abs(distance)-3)direction=-direction;
  return direction<0?AbstractPlayableSprite.INPUT_LEFT:direction>0?AbstractPlayableSprite.INPUT_RIGHT:0;
 }
 static Object field(Object o,String name)throws Exception {var f=o.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(o);}
 static Object call(Object o,String name)throws Exception {return o.getClass().getMethod(name).invoke(o);}
}
