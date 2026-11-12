// Purpose: SFX-only audio for the custom capture hosts, recorded the way GameplayCaptureTool --audio --no-music
//   records it: synthesis on and music volume 0 for the session (GameplayCaptureSession.enableAudio and
//   silenceMusic, before boot), then one presentation packet drained per outer frame after each step.
//   Warm-up frames are presented and drained too, but not written, so nothing queues up for frame 0.
// Use: PromoAudio.enable(session) before boot; au = PromoAudio.begin(outDir) after boot;
//   au.frame(loop, write) after every step; au.close() writes outDir/audio.wav (16-bit stereo).
// Props: promo.audio=false turns it off; promo.music=true keeps the music (control run for the RMS check).
// Origin: MICA & TALON promo redo, stage B of the 2026-11-12 revision.
import com.openggf.GameLoop;
import com.openggf.audio.LiveCaptureAudioHandle;
import com.openggf.game.GameServices;
import com.openggf.tools.GameplayCaptureSession;
import java.io.*;
import java.nio.file.*;

public final class PromoAudio implements AutoCloseable {
    private static final boolean ON = !"false".equals(System.getProperty("promo.audio"));
    private final Path out;
    private final LiveCaptureAudioHandle capture;
    private final OutputStream pcm;
    private final short[] buf;
    private final int rate;

    public static void enable(GameplayCaptureSession s) {
        if (!ON) return;
        s.enableAudio();
        if (!Boolean.getBoolean("promo.music")) s.silenceMusic();
    }

    public static PromoAudio begin(Path outDir) throws IOException {
        return new PromoAudio(outDir);
    }

    private PromoAudio(Path outDir) throws IOException {
        out = outDir;
        if (!ON) { capture = null; pcm = null; buf = null; rate = 0; return; }
        var audio = GameServices.audio();
        rate = audio.outputSampleRate();
        if (audio.presentationFrameRate() != 60) throw new IllegalStateException("audio presentation rate is not 60");
        capture = audio.beginLiveCaptureAudio(60);
        if (capture.frameRate() != 60 || capture.sampleRate() != rate) throw new IllegalStateException("audio clock differs");
        buf = new short[capture.maxStereoFramesPerPacket() * 2];
        pcm = new BufferedOutputStream(Files.newOutputStream(out.resolve("audio.pcm")));
    }

    public void frame(GameLoop loop, boolean write) throws IOException {
        if (!ON) return;
        loop.presentOuterFrame(false, false);
        int n = capture.drainPresentationFrame(buf) * 2;
        if (write) for (int i = 0; i < n; i++) { pcm.write(buf[i] & 255); pcm.write((buf[i] >>> 8) & 255); }
    }

    @Override public void close() throws IOException {
        if (!ON) return;
        capture.close();
        pcm.close();
        Path raw = out.resolve("audio.pcm");
        var format = new javax.sound.sampled.AudioFormat(rate, 16, 2, true, false);
        try (var in = new javax.sound.sampled.AudioInputStream(Files.newInputStream(raw), format, Files.size(raw) / 4)) {
            javax.sound.sampled.AudioSystem.write(in, javax.sound.sampled.AudioFileFormat.Type.WAVE, out.resolve("audio.wav").toFile());
        }
        Files.delete(raw);
    }
}
