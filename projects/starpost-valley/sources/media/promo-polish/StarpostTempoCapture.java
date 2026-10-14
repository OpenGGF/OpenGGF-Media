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
public class StarpostTempoCapture {
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
    Object scene=com.openggf.mods.code.OwnedSceneFactory.unwrap((com.openggf.mods.scene.ModScene)field(loop.modSceneHost,"scene")),shell=field(scene,"shell");
    Map<Integer,List<String>> script=new TreeMap<>();
    for(String line:Files.readAllLines(Path.of(a[4]))) {
        line=line.split("#",2)[0].trim(); if(line.isEmpty())continue;
        String[] pair=line.split(":",2);
        script.computeIfAbsent(Integer.parseInt(pair[0]),k->new ArrayList<>()).add(pair[1]);
    }
    Set<String> held=new HashSet<>(); Map<Integer,List<String>> releases=new HashMap<>();
    int heldBefore=0, actionBefore=0;
    boolean autoFish=false;
    GameMode oldMode=loop.getCurrentGameMode();
    try(var csv=new PrintWriter(Files.newBufferedWriter(out.resolve("state.csv")));
        var audio=GameServices.audio().beginLiveCaptureAudio(60);
        var pcm=new java.io.DataOutputStream(Files.newOutputStream(out.resolve("audio.raw")))) {
     short[] samples=new short[audio.maxStereoFramesPerPacket()*2];
     csv.println("frame,stage,mode,x,y,gspeed,air,rings,wallet,clock,camx,camy,input");
     for(int f=0;f<Integer.parseInt(a[5]);f++) {
      AbstractPlayableSprite p=(AbstractPlayableSprite)GameServices.camera().getFocusedSprite();
      for(String key:releases.getOrDefault(f,List.of())) held.remove(key);
      for(String command:script.getOrDefault(f,List.of())) {
       if(command.startsWith("jump=")) {
        String jump=command.substring(5).replace('_',' ');
        if(!loop.modSceneHost.debugJump(jump))throw new AssertionError("debug at "+f+": "+jump);
       } else if(command.startsWith("state=")) {
        String jump=command.substring(6).replace('_',' ');
        if(!(boolean)scene.getClass().getMethod("debugJump",String.class).invoke(scene,jump))throw new AssertionError(jump);
       } else if(command.equals("auto=fish")) { autoFish=true;
       } else if(command.startsWith("place=")) {
        int x=Integer.parseInt(command.substring(6));
        com.openggf.sprites.NativePositionOps.writeXPosResetSubpixel(p,x);
        p.setXSpeed((short)0);p.setGSpeed((short)0);p.setYSpeed((short)0);
        GameServices.camera().updatePosition(true);
       } else if(command.equals("exit")) {
        GameServices.level().requestActExit(ActExit.LEFT,Map.of());
       } else if(command.startsWith("hold=")) held.add(command.substring(5));
       else if(command.startsWith("release=")) held.remove(command.substring(8));
       else {held.add(command);releases.computeIfAbsent(f+2,k->new ArrayList<>()).add(command);}
      }
      int mask=0,action=0;
      for(String key:held) switch(key) {
       case "left" -> mask|=AbstractPlayableSprite.INPUT_LEFT;
       case "right" -> mask|=AbstractPlayableSprite.INPUT_RIGHT;
       case "up" -> mask|=AbstractPlayableSprite.INPUT_UP;
       case "down" -> mask|=AbstractPlayableSprite.INPUT_DOWN;
       case "enter","space","z" -> {mask|=AbstractPlayableSprite.INPUT_JUMP;action|=InputActionMasks.ACTION_A;}
       case "x" -> action|=InputActionMasks.ACTION_B;
       case "tab" -> {}
       default -> {int keycode=key.length()==1?Character.toUpperCase(key.charAt(0)):0;
        if(keycode>0)loop.getInputHandler().handleKeyEvent(keycode,org.lwjgl.glfw.GLFW.GLFW_PRESS);}
      }
      if(autoFish && loop.getCurrentGameMode()==GameMode.LEVEL) {
       Object activity=field(scene,"activities"),lake=call(activity,"lake");
       if(lake!=null) {
        Object bar=call(lake,"bar");
        if(bar!=null) {
         if((float)field(bar,"bubble")+(float)field(bar,"bubbleSpeed")*4>(float)field(bar,"fish")) action|=InputActionMasks.ACTION_B;
        } else if((int)field(field(lake,"line"),"state")==3) action|=InputActionMasks.ACTION_B;
       }
      }
      loop.getInputHandler().setLogicalOverride(LogicalInputSnapshot.ofPlayers(
       PlayerInputState.of(mask,mask&~heldBefore,action,action&~actionBefore,false,held.contains("tab")),PlayerInputState.neutral()));
      heldBefore=mask;actionBefore=action;
      loop.step();
      if(f==10 || f==160 || f==300) {
       var smps=(com.openggf.audio.session.SmpsDriverSession)field(GameServices.audio(),"shadowSmpsSession");
       int pace=smps.captureSnapshot().musicTempoPercent();
       if(pace!=65)throw new AssertionError("Starpost tempo="+pace);
       System.out.println("Tempo witness: frame="+f+" mode="+loop.getCurrentGameMode()+" percent="+pace);
      }

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
      Object game=field(shell,"game");
      csv.printf("%d,%s,%d,%d,%d,%s,%s,%s,%d,%d,%d%n",f,loop.getCurrentGameMode(),
       p==null?0:p.getCentreX(),p==null?0:p.getCentreY(),p==null?0:p.getGSpeed(),p!=null&&p.getAir(),
       game==null?0:field(game,"rings"),game==null?"TITLE":call(field(game,"calendar"),"clock"),
       GameServices.camera().getX(),GameServices.camera().getY(),mask);
     }
    }
    if(!kit.findings().isEmpty())throw new AssertionError(kit.findings());

    System.out.println("Promo capture complete: no creator faults");
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
