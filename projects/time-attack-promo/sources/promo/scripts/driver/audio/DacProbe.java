// Promo audio fix (ta-promo-a, 2026-10-23): LiveSceneMusic's construction with a chip-write
// observer, to count DAC enables/sample bytes on the production-paced path. Optional FM6 mute
// renders the same song without FM6/DAC so the drums can be isolated by subtraction.
// Usage: DacProbe <s3k.gen> <hex music id> <seconds> <fmMask hex> <out.wav>
import com.openggf.audio.session.*;
import com.openggf.audio.smps.*;
import com.openggf.audio.synth.ChipWriteObserver;
import com.openggf.data.Rom;
import com.openggf.game.sonic3k.audio.Sonic3kAudioProfile;
import java.nio.*;
import java.nio.file.*;

public final class DacProbe {
    public static void main(String[] a) throws Exception {
        Rom rom = new Rom();
        if (!rom.open(a[0])) throw new IllegalStateException(a[0]);
        int rate = 48_000, id = Integer.parseInt(a[1], 16);
        int frames = (int) (Double.parseDouble(a[2]) * rate);
        var profile = new Sonic3kAudioProfile();
        var loader = profile.createSmpsLoader(rom);
        var data = loader.loadMusic(id);
        var dac = loader.loadDacData();
        var handlers = new SmpsCoordFlagHandlerOwner(new SmpsCoordFlagRuntimeState());
        profile.configurePresentationCoordFlagHandlers(handlers);
        var base = profile.getSequencerConfig();
        var config = SmpsConfigBinding.bind(base,
                () -> base.getCoordFlagHandler() == null ? null : handlers.handlerFor("s3k"));
        long[] n = new long[3]; boolean[] on = {false};
        ChipWriteObserver obs = new ChipWriteObserver() {
            public void onYm2612Write(int port, int reg, int v) {
                if (port == 0 && reg == 0x2B) { on[0] = (v & 0x80) != 0; n[on[0] ? 0 : 1]++; }
                if (port == 0 && reg == 0x2A && on[0]) n[2]++;
            }
            public void onPsgWrite(int v) { }
        };
        short[] pcm = new short[frames * 2];
        try (var stream = new OwnedSmpsAudioStream("s3k", 0, new SmpsPhysicalDevice.Settings(rate, false),
                profile.smpsPhysicalPolicy(), obs,
                new SmpsDriverSessionConfiguration(profile.smpsStatefulCommandPolicy()))) {
            var driver = stream.logicalDriver();
            driver.setRegion(SmpsSequencer.Region.NTSC);
            stream.applyChannelMasks(Integer.parseInt(a[3], 16), 0);
            var seq = new SmpsSequencer(data, dac, driver, () -> { }, config);
            seq.setSampleRate(rate);
            seq.setFallbackVoiceData(data);
            driver.addSequencer(seq, false);
            short[] packet = new short[((rate + 59) / 60) * 2];
            int off = 0;
            for (long f = 0; off < frames; f++) {
                int avail = (int) (((f + 1) * rate / 60) - (f * rate / 60));
                stream.serviceAndRenderFrame(packet, avail);
                int c = Math.min(avail, frames - off);
                System.arraycopy(packet, 0, pcm, off * 2, c * 2);
                off += c;
            }
        }
        System.out.printf("dac enables=%d disables=%d bytes-while-enabled=%d%n", n[0], n[1], n[2]);
        ByteBuffer b = ByteBuffer.allocate(44 + pcm.length * 2).order(ByteOrder.LITTLE_ENDIAN);
        b.put("RIFF".getBytes()).putInt(36 + pcm.length * 2).put("WAVEfmt ".getBytes()).putInt(16)
                .putShort((short) 1).putShort((short) 2).putInt(rate).putInt(rate * 4)
                .putShort((short) 4).putShort((short) 16).put("data".getBytes()).putInt(pcm.length * 2);
        for (short v : pcm) b.putShort(v);
        Files.write(Path.of(a[4]), b.array());
    }
}
