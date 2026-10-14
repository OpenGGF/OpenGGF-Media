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
public class StarpostWateringCapture {
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
    float[] farmGoal=null;
    GameMode oldMode=loop.getCurrentGameMode();
    try(var csv=new PrintWriter(Files.newBufferedWriter(out.resolve("state.csv")));
        var farmCsv=new PrintWriter(Files.newBufferedWriter(out.resolve("farm.csv")));
        var audio=GameServices.audio().beginLiveCaptureAudio(60);
        var pcm=new java.io.DataOutputStream(Files.newOutputStream(out.resolve("audio.raw")))) {
     short[] samples=new short[audio.maxStereoFramesPerPacket()*2];
     csv.println("frame,stage,mode,x,y,gspeed,air,rings,wallet,clock,camx,camy,input");
     farmCsv.println("frame,screen,farmer,x,feet,facing_left,water_charges,watering_age,pouring,selected,target_row,target_column,target_watered,underfoot_watered,watered_tiles");
     for(int f=0;f<Integer.parseInt(a[5]);f++) {
      AbstractPlayableSprite p=(AbstractPlayableSprite)GameServices.camera().getFocusedSprite();
      for(String key:releases.getOrDefault(f,List.of())) held.remove(key);
      for(String command:script.getOrDefault(f,List.of())) {
       if(command.startsWith("jump=")) {
        farmGoal=null;
        String jump=command.substring(5).replace('_',' ');
        if(!loop.modSceneHost.debugJump(jump))throw new AssertionError("debug at "+f+": "+jump);
       } else if(command.startsWith("state=")) {
        String jump=command.substring(6).replace('_',' ');
        if(!(boolean)scene.getClass().getMethod("debugJump",String.class).invoke(scene,jump))throw new AssertionError(jump);
       } else if(command.startsWith("farm-go=")) {
        var goal=command.substring(8).split(",");farmGoal=new float[]{Float.parseFloat(goal[0]),Float.parseFloat(goal[1])};
       } else if(command.startsWith("clear=")) {
        String[] cell=command.substring(6).split(",");Object model=field(field(shell,"game"),"farm");
        Object plot=model.getClass().getMethod("raw",int.class,int.class).invoke(model,Integer.parseInt(cell[0]),Integer.parseInt(cell[1]));
        plot.getClass().getField("tilled").setBoolean(plot,true);plot.getClass().getField("cover").setInt(plot,0);
        plot.getClass().getField("watered").setBoolean(plot,false);plot.getClass().getField("crop").set(plot,null);
        plot.getClass().getField("object").set(plot,null);
       } else if(command.startsWith("charges=")) {
        Object g=field(shell,"game");var water=g.getClass().getDeclaredField("waterCharges");water.setAccessible(true);water.setInt(g,Integer.parseInt(command.substring(8)));
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
      if(farmGoal!=null && loop.getCurrentGameMode()==GameMode.MOD_SCENE) {
       Object screen=field(shell,"screen");
       if(screen!=null && screen.getClass().getSimpleName().equals("PlayScreen")) {
        Object runner=field(field(screen,"farm"),"runner");
        int dx=farmWalk((float)field(runner,"x"),(float)field(runner,"speed"),farmGoal[0],0.1875f);
        int dy=farmWalk((float)field(runner,"depth"),(float)field(runner,"depthSpeed"),farmGoal[1],0.25f);
        if(dx<0)mask|=AbstractPlayableSprite.INPUT_LEFT;else if(dx>0)mask|=AbstractPlayableSprite.INPUT_RIGHT;
        if(dy<0)mask|=AbstractPlayableSprite.INPUT_UP;else if(dy>0)mask|=AbstractPlayableSprite.INPUT_DOWN;
       }
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
      Object screen=field(shell,"screen");
      if(screen!=null && screen.getClass().getSimpleName().equals("PlayScreen")) {
       Object farm=field(screen,"farm"), runner=field(farm,"runner");
       var pouring=farm.getClass().getDeclaredMethod("pouring");pouring.setAccessible(true);
       var targetMethod=farm.getClass().getDeclaredMethod("actionPlot");targetMethod.setAccessible(true);
       int[] target=(int[])targetMethod.invoke(farm), under=(int[])call(farm,"plotUnderfoot");
       Object model=field(game,"farm");
       var getPlot=model.getClass().getMethod("plot",int.class,int.class);
       Object targetPlot=target==null?null:getPlot.invoke(model,target[0],target[1]);
       Object underPlot=under==null?null:getPlot.invoke(model,under[0],under[1]);
       List<String> wet=new ArrayList<>();
       for(int row=0;row<5;row++)for(int col=0;col<(int)call(model,"open");col++) {
        Object cell=getPlot.invoke(model,row,col);if((boolean)field(cell,"watered"))wet.add(row+"."+col);
       }
       farmCsv.printf("%d,PlayScreen,%s,%s,%s,%s,%s,%d,%s,%s,%s,%s,%s,%s,%s%n",f,field(game,"farmer"),
        field(runner,"x"),call(farm,"feetY"),field(runner,"facingLeft"),field(game,"waterCharges"),
        (long)field(shell,"ticks")-(long)field(farm,"wateredAt"),pouring.invoke(farm),
        call(field(game,"inventory"),"selectedId"),target==null?"":target[0],target==null?"":target[1],
        targetPlot==null?"":field(targetPlot,"watered"),underPlot==null?"":field(underPlot,"watered"),String.join(";",wet));
      }
     }
    }
    if(!kit.findings().isEmpty())throw new AssertionError(kit.findings());

    System.out.println("Promo capture complete: no creator faults");
    loop.modSceneHost.cleanup();
   }
  }
 }
 // Input steering from observed live farm state only; never assigns game positions or velocities.
 static int farmWalk(float position,float speed,float target,float friction) {
  float distance=target-position;
  if(Math.abs(distance)<0.35f)return 0;
  if(Math.signum(speed)==Math.signum(distance) && Math.abs(distance)<=Math.abs(speed)+speed*speed/(2*friction))return 0;
  return distance<0?-1:1;
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
