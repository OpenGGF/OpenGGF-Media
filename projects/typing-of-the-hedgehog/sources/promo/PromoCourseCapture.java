import com.openggf.tools.GameplayCaptureSession;
import com.openggf.tools.HeadlessGameBoot;
import com.openggf.game.GameServices;
import com.openggf.configuration.SonicConfiguration;
import java.nio.file.*;
import java.nio.*;
import java.io.*;

/** Typing of the Hedgehog first promo (2026-10-10): task-local synchronous course recorder.
 * Inputs: ROM, packaged mod, zone, act, ticks, output directory. Every production step is
 * followed by one outer audio presentation and one video frame. PCM rate is queried from
 * AudioManager; no audio device, substitute music, or fixed 44.1 kHz assumption is used.
 * Origin: feature/ai-typing-hedgehog-promo at 9fee32aad. All outputs stay in the promo task dir.
 */
public final class PromoCourseCapture {
  public static void main(String[] a) throws Exception {
    Path out=Path.of(a[5]); Files.createDirectories(out);
    var settings=new GameplayCaptureSession.Settings(400,"sonic","","off",null,null,null);
    try(var session=new GameplayCaptureSession(settings)) {
      GameServices.configuration().setSessionOverride(SonicConfiguration.AUDIO_ENABLED,true);
      session.applyMod(Path.of(a[1])); session.boot(Path.of(a[0]),Integer.parseInt(a[2]),Integer.parseInt(a[3]),settings);
      var audio=GameServices.audio(); int rate=audio.outputSampleRate(), fps=audio.presentationFrameRate();
      if(fps!=60) throw new IllegalStateException("Promo requires 60 Hz, got "+fps);
      int ticks=Integer.parseInt(a[4]);
      audio.beginCaptureMode(rate,fps);
      Process encoder=new ProcessBuilder("ffmpeg","-loglevel","error","-y","-f","rawvideo","-pixel_format","bgra","-video_size","400x224","-framerate","60","-i","pipe:0","-vf","scale=2000:1120:flags=neighbor","-c:v","libx264","-preset","fast","-crf","16","-threads","4","-pix_fmt","yuv420p",out.resolve("video-only.mp4").toString()).redirectError(ProcessBuilder.Redirect.INHERIT).start();
      short[] pcm=new short[(rate/fps+64)*2]; ByteBuffer b=ByteBuffer.allocate(400*224*4).order(ByteOrder.LITTLE_ENDIAN);
      long samples=0;
      try(var video=new BufferedOutputStream(encoder.getOutputStream(),1<<20);var wav=new Wav(out.resolve("audio.wav"),rate);var csv=Files.newBufferedWriter(out.resolve("state.csv"))) {
        csv.write(GameplayCaptureSession.stateHeader()+"\n");
        for(int t=0;t<ticks;t++) {
          session.step(null);
          // Course completion closes its gameplay audio producer on the hub hand-back.
          // End this course recording before that boundary; hub footage is recorded separately.
          if(!session.stateLine(t,null).contains(",LEVEL,")) break;
          HeadlessGameBoot.presentHeadlessOuterAudioFrame();
          csv.write(session.stateLine(t,null)+"\n");
          var image=session.render(); b.clear(); for(int p:image.pixels()) b.putInt(p); video.write(b.array());
          int frames=audio.drainCaptureFrame(pcm); if(frames!=rate/fps) throw new IllegalStateException("Audio packet "+t+": "+frames);
          wav.write(pcm,frames*2); samples+=frames;
          if(t%600==0) System.out.println("frame "+t+"/"+ticks);
        }
      } finally { audio.endCaptureMode(); }
      if(encoder.waitFor()!=0) throw new IllegalStateException("encoder failed");
      Files.writeString(out.resolve("clock.json"),"{\"ticks\":"+(samples/(rate/fps))+",\"fps\":"+fps+",\"sampleRate\":"+rate+",\"stereoPcmFrames\":"+samples+",\"pcmBytesPerTick\":"+(rate/fps*4)+"}\n");
      Process mux=new ProcessBuilder("ffmpeg","-loglevel","error","-y","-i",out.resolve("video-only.mp4").toString(),"-i",out.resolve("audio.wav").toString(),"-c:v","copy","-c:a","aac","-b:a","256k","-ar","48000","-ac","2","-shortest",out.resolve("capture.mp4").toString()).inheritIO().start();
      if(mux.waitFor()!=0) throw new IllegalStateException("mux failed");
      Files.delete(out.resolve("video-only.mp4"));
      System.out.println("Captured "+(samples/(rate/fps))+" frames; PCM "+rate+" Hz "+samples+" stereo frames");
    }
  }
  static class Wav implements AutoCloseable {
    final RandomAccessFile f; final int rate; long bytes=0;
    Wav(Path p,int r)throws Exception {rate=r;f=new RandomAccessFile(p.toFile(),"rw");f.setLength(0);f.write(new byte[44]);}
    void write(short[] s,int n)throws Exception {byte[] b=new byte[n*2]; for(int i=0;i<n;i++){b[2*i]=(byte)s[i];b[2*i+1]=(byte)(s[i]>>8);}f.write(b);bytes+=b.length;}
    void le(int v)throws Exception {f.writeInt(Integer.reverseBytes(v));}
    public void close()throws IOException {try{f.seek(0);f.writeBytes("RIFF");le((int)bytes+36);f.writeBytes("WAVEfmt ");le(16);f.writeShort(Short.reverseBytes((short)1));f.writeShort(Short.reverseBytes((short)2));le(rate);le(rate*4);f.writeShort(Short.reverseBytes((short)4));f.writeShort(Short.reverseBytes((short)16));f.writeBytes("data");le((int)bytes);}catch(Exception e){throw new IOException(e);}finally{f.close();}}
  }
}
