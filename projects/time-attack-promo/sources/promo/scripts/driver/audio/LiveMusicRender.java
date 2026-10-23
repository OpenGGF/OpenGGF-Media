// Promo audio fix (ta-promo-a, 2026-10-23): renders a ROM song through LiveSceneMusic, the
// production-paced session (60 Hz service + DAC idle loop with the game's own physical policy).
// FmSfxRenderTool's direct-read legacy path never enables the S3K DAC, so its renders lack drums.
// Usage: LiveMusicRender <s3k.gen> <hex music id> <seconds> <out.wav>
import com.openggf.data.Rom;
import com.openggf.game.sonic3k.audio.Sonic3kAudioProfile;
import com.openggf.mods.scene.host.music.LiveSceneMusic;
import java.io.*;
import java.nio.*;
import java.nio.file.Files;
import java.nio.file.Path;

public final class LiveMusicRender {
    public static void main(String[] a) throws Exception {
        Rom rom = new Rom();
        if (!rom.open(a[0])) throw new IllegalStateException("ROM did not open: " + a[0]);
        int rate = 48_000;
        int frames = (int) (Double.parseDouble(a[2]) * rate);
        short[] pcm = new short[frames * 2];
        try (LiveSceneMusic music = new LiveSceneMusic("s3k", Integer.parseInt(a[1], 16),
                new Sonic3kAudioProfile(), rom, rate)) {
            music.render(pcm, frames);
        }
        ByteBuffer b = ByteBuffer.allocate(44 + pcm.length * 2).order(ByteOrder.LITTLE_ENDIAN);
        b.put("RIFF".getBytes()).putInt(36 + pcm.length * 2).put("WAVEfmt ".getBytes()).putInt(16)
                .putShort((short) 1).putShort((short) 2).putInt(rate).putInt(rate * 4)
                .putShort((short) 4).putShort((short) 16).put("data".getBytes()).putInt(pcm.length * 2);
        for (short v : pcm) b.putShort(v);
        Files.write(Path.of(a[3]), b.array());
    }
}
