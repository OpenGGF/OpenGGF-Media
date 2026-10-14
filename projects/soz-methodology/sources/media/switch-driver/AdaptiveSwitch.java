package com.openggf.tests;
import com.openggf.tools.*;import com.openggf.game.*;import com.openggf.game.sonic3k.runtime.*;import com.openggf.graphics.*;import com.openggf.debug.playback.*;import java.nio.file.*;
public class AdaptiveSwitch { public static void main(String[] args)throws Exception {
 for(int jumpX:new int[]{0x48F0,0x48F8,0x48FC}){var settings=new GameplayCaptureSession.Settings(400,"sonic","tails","off",null,0x4808,0x5AC);Path out=Path.of(args[1],Integer.toHexString(jumpX));Files.createDirectories(out);
 try(var session=new GameplayCaptureSession(settings);var csv=Files.newBufferedWriter(out.resolve("state.csv"))){session.boot(Path.of(args[0]),8,1,settings);GameServices.level().consumePendingInitialProcessSpritesPass();session.player().setRingCount(99);int phase=0,timer=0,maxX=0;
 csv.write("frame,x,y,gspeed,air,spin,charge,input,phase\n");
 for(int frame=0;frame<500;frame++){var p=session.player();int mask=8;
 if(phase==0&&SozZoneRuntimeState.trigger(11)==128&&++timer>=60){phase=1;timer=0;}
 switch(phase){case 1:mask=timer++==0?24:8;if(timer>2&&!p.getAir()&&p.getCentreY()<0x5A0){phase=2;mask=4;}break;
 case 2:if(p.getGSpeed()>0)mask=4;else if(p.getGSpeed()<0)mask=8;else{mask=2;phase=3;timer=0;}break;
 case 3:mask=2;if(++timer>=1){phase=4;timer=0;}break;
 case 4:mask=2|((timer&1)==0?16:0);if(++timer>=2){phase=5;timer=0;}break;
 case 5:if(timer<20)mask=timer++==0?8:24;if(!p.getAir()&&p.getCentreX()>=0x4870&&p.getCentreY()>=0x5A0){phase=6;timer=0;mask=2;}break;
 case 6:mask=2;if(++timer>=1){phase=7;timer=0;}break;
 case 7:mask=2|((timer&1)==0?16:0);if(++timer>=12){phase=8;timer=0;}break;
 case 8:if(p.getCentreX()>=jumpX){phase=9;timer=0;mask=24;}break;
 case 9:mask=24;if(++timer>=20){phase=10;}break;}
 session.step(new Bk2FrameInput(frame,mask,(mask&16)!=0?1:0,false,""));maxX=Math.max(maxX,p.getCentreX());
 csv.write(frame+","+p.getCentreX()+","+p.getCentreY()+","+p.getGSpeed()+","+p.getAir()+","+p.getSpindash()+","+SozZoneRuntimeState.trigger(11)+","+mask+","+phase+"\n");
 if(frame>=240&&frame<=300&&frame%5==0)ScreenshotCapture.savePNG(session.render(),out.resolve(frame+".png"));
 if(p.getDead()||p.getCentreX()>0x4A40)break;
 }System.out.println("ADAPTIVE "+Integer.toHexString(jumpX)+" maxX="+Integer.toHexString(maxX));}
 }
}}
