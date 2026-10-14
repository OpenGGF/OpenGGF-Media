package com.openggf.tests;
import com.openggf.tools.*;import com.openggf.game.*;import com.openggf.graphics.*;import com.openggf.debug.playback.*;import java.nio.file.*;
public class CaptureSwitch { public static void main(String[] args)throws Exception {
 var settings=new GameplayCaptureSession.Settings(400,"sonic","tails","off",null,0x4808,0x5AC);Path out=Path.of(args[1]);Files.createDirectories(out);
 try(var session=new GameplayCaptureSession(settings)){session.boot(Path.of(args[0]),8,1,settings);GameServices.level().consumePendingInitialProcessSpritesPass();session.player().setRingCount(99);
 var lines=Files.readAllLines(Path.of(args[2]));for(int frame=0;frame<lines.size()-1;frame++){String[] f=lines.get(frame+1).split(",");int mask=Integer.parseInt(f[8]);session.step(new Bk2FrameInput(frame,mask,(mask&16)!=0?1:0,false,""));
 if(frame>=240&&frame<=270&&frame%5==0)ScreenshotCapture.savePNG(session.render(),out.resolve(frame+".png"));
 if(frame==260)System.out.println("CAPTURE_POSITION="+session.player().getCentreX()+","+session.player().getCentreY()+" expected="+f[1]+","+f[2]);}
 }
}}
