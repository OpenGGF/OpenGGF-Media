package com.openggf.tools;
import com.openggf.tools.*;
import com.openggf.game.GameServices;
import com.openggf.game.session.SessionManager;
import com.openggf.debug.playback.*;
import com.openggf.game.sonic3k.objects.bosses.SszMechaSonicObjectInstance;
import java.nio.file.*;
import java.util.*;
/** Temporary controller author: authentic cold prefix, snapshot-forked button trials, no gameplay writes. */
public class SszSoloMechaLookaheadProbe {
 static String buttons(Bk2FrameInput in){
  var a=new ArrayList<String>();int m=in.p1InputMask();
  if((m&1)!=0)a.add("U");if((m&2)!=0)a.add("D");if((m&4)!=0)a.add("L");if((m&8)!=0)a.add("R");
  if((in.p1ActionMask()&1)!=0)a.add("A");if((in.p1ActionMask()&2)!=0)a.add("B");if((in.p1ActionMask()&4)!=0)a.add("C");return a.isEmpty()?"-":String.join("+",a);
 }
 static SszMechaSonicObjectInstance boss(){return GameServices.level().getObjectManager().activeObjectsOfType(SszMechaSonicObjectInstance.class).stream().findFirst().orElse(null);}
 static Bk2FrameInput button(GameplayCaptureSession s,int frame,int policy,Bk2FrameInput prior){
  var p=s.player();var b=boss(); int target=6720;
  if(b!=null&&b.getCollisionProperty()>0){
   int[] offsets={0,-24,24,-48,48,0,0,0,0,0,0,0};
   target=b.getX()+offsets[policy];
   if(policy==5)target=6720;
   if(policy==6)target=6584;
   if(policy==7)target=6856;
   if(policy==8)target=p.getCentreX()<b.getX()?6584:6856;
   if(policy==9)target=b.getX()+(p.getCentreX()<b.getX()?-24:24);
   if(policy>=10)target=6720;
  }
  double desired=Math.max(-4,Math.min(4,(target-p.getCentreX())/8.0));
  int direction=p.getXSpeed()/256.0>desired+0.2?4:p.getXSpeed()/256.0<desired-0.2?8:0;
  boolean held=prior!=null&&prior.p1ActionMask()!=0;
  int action=b!=null&&b.getCollisionProperty()>0&&(p.getAir()?held:!held)?1:0;
  if(policy==10) {direction=2; action=held?0:1;}
  if(policy==11) {direction|=2;action=0;}
  return new Bk2FrameInput(frame,direction,action,false,"");
 }
 static double score(GameplayCaptureSession s,int hpBefore,int ringsBefore){
  if(s.player().getDead())return -1000000;
  var b=boss();int hp=b==null?0:b.getCollisionProperty();
  return (hpBefore-hp)*10000+Math.min(3,s.player().getRingCount())*150-(s.player().isHurt()?100:0)
    -(b==null?0:Math.min(250,Math.abs(b.getX()-s.player().getCentreX())))*0.03;
 }
 public static void main(String[] args)throws Exception{
  Path output=Path.of(args[0]); var movie=new Bk2MovieLoader().loadMovieOrInputLog(Path.of(args[1]));int prefix=Integer.parseInt(args[2]);
  var settings=new GameplayCaptureSession.Settings(320,"sonic","","off",null,null,null);
  StringBuilder script=new StringBuilder(),states=new StringBuilder(GameplayCaptureSession.stateHeader()+"\n");
  try(var s=new GameplayCaptureSession(settings)){
   s.boot(Path.of("/home/farrell/code/projects/OpenGGF/s3k.gen"),10,0,settings);Bk2FrameInput prior=null;int f=0;
   for(;f<prefix;f++){prior=movie.getFrame(f);s.step(prior);s.render();script.append("1 ").append(buttons(prior)).append('\n');states.append(s.stateLine(f,prior)).append('\n');}
   for(;f<prefix+10000&&!s.player().getDead()&&GameServices.level().getCurrentZone()==10;){
    var registry=SessionManager.getCurrentGameplayMode().getRewindRegistry();var saved=registry.capture();var oldInput=prior;
    int hp=boss()==null?0:boss().getCollisionProperty();int rings=s.player().getRingCount();double best=-Double.MAX_VALUE;int chosen=0;
    for(int policy=0;policy<12;policy++){
     registry.restore(saved);s.restoreInputHistory(oldInput);var prev=oldInput;
     for(int n=0;n<180;n++) {prev=button(s,f+n,policy,prev);s.step(prev);s.render();if(s.player().getDead()||GameServices.level().getCurrentZone()!=10)break;}
     double value=score(s,hp,rings);if(value>best){best=value;chosen=policy;}
    }
    registry.restore(saved);s.restoreInputHistory(oldInput);prior=oldInput;
    for(int n=0;n<30;n++,f++) {prior=button(s,f,chosen,prior);s.step(prior);s.render();script.append("1 ").append(buttons(prior)).append('\n');states.append(s.stateLine(f,prior)).append('\n');if(s.player().getDead()||GameServices.level().getCurrentZone()!=10){f++;break;}}
    System.out.println("CHOICE frame="+f+" policy="+chosen+" score="+best+" hp="+(boss()==null?-1:boss().getCollisionProperty())+" rings="+s.player().getRingCount());
    Files.writeString(Path.of(output+".script"),script);Files.writeString(Path.of(output+".csv"),states);
   }
  }
  InputLogAuthorTool.author(script.toString(),Path.of(output+".bk2"),"s3k");
 }
}
