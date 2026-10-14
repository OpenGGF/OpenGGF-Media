import com.openggf.audio.driver.SmpsDriver;
import com.openggf.audio.session.LegacyCompatibilitySmpsPhysicalPolicy;
import com.openggf.audio.session.OwnedSmpsAudioStream;
import com.openggf.audio.session.SmpsPhysicalDevice;
import com.openggf.audio.smps.AbstractSmpsData;
import com.openggf.audio.smps.DacData;
import com.openggf.audio.smps.SmpsSequencer;
import com.openggf.audio.synth.ChipWriteObserver;
import com.openggf.data.Rom;
import com.openggf.game.sonic2.audio.Sonic2SmpsSequencerConfig;
import com.openggf.game.sonic2.audio.smps.Sonic2SmpsLoader;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/**
 * Promo soundtrack stem renderer for the Putt Putt Paradise promo (2026-10-06, intro-audio lane).
 *
 * <p>Renders Sonic 2 music and sound effects from a user-supplied Sonic 2 ROM through OpenGGF's
 * own SMPS driver (Sonic2SmpsLoader + Sonic2SmpsSequencerConfig, NTSC tempo, accurate FM core),
 * one isolated driver session per stem, exactly as {@code com.openggf.tools.audio.PsgSfxRenderTool}
 * and the test-side {@code AudioReferenceGenerator} do. Nothing is downloaded and no disassembly
 * data is read. Compiled and run OUTSIDE the repository against its {@code target/classes}.
 *
 * <pre>
 *   java -cp target/classes:BUILD S2PromoAudioRender --rom S2.gen --out DIR [--rate 48000] \
 *        music:96:12 music:81:100 sfx:B5 ...
 * </pre>
 * music:ID:SECONDS renders up to SECONDS (stopping early when a non-looping track ends);
 * sfx:ID renders until the effect completes (max 6 s). IDs are hex Sonic 2 sound IDs.
 * Output: DIR/s2-music-XX.wav / DIR/s2-sfx-XX.wav (16-bit stereo PCM) and a line per stem on stdout.
 */
public final class S2PromoAudioRender {
    public static void main(String[] args) throws IOException {
        String romPath = null;
        Path out = null;
        double rate = 48_000.0;
        java.util.List<String> jobs = new java.util.ArrayList<>();
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--rom" -> romPath = args[++i];
                case "--out" -> out = Path.of(args[++i]);
                case "--rate" -> rate = Double.parseDouble(args[++i]);
                default -> jobs.add(args[i]);
            }
        }
        if (romPath == null || out == null || jobs.isEmpty()) {
            System.err.println("usage: --rom S2.gen --out DIR [--rate hz] music:ID:SECONDS|sfx:ID ...");
            System.exit(2);
        }
        Rom rom = new Rom();
        if (!rom.open(romPath)) {
            System.err.println("failed to open ROM " + romPath);
            System.exit(1);
        }
        Sonic2SmpsLoader loader = new Sonic2SmpsLoader(rom);
        DacData dac = loader.loadDacData();
        Files.createDirectories(out);
        for (String job : jobs) {
            String[] p = job.split(":");
            boolean music = p[0].equals("music");
            int id = Integer.parseInt(p[1], 16);
            double seconds = music ? Double.parseDouble(p[2]) : 6.0;
            AbstractSmpsData data = music ? loader.loadMusic(id) : loader.loadSfx(id);
            if (data == null) {
                System.err.println(job + ": did not load");
                System.exit(1);
            }
            short[] pcm = render(data, dac, rate, (int) (seconds * rate), !music);
            Path file = out.resolve(String.format(Locale.ROOT, "s2-%s-%02x.wav", p[0], id));
            writeWav(file, pcm, (int) rate);
            int peak = 0;
            for (short s : pcm) {
                peak = Math.max(peak, Math.abs((int) s));
            }
            System.out.printf(Locale.ROOT, "%s %s %.3fs peak=%d%n", job, file.getFileName(), pcm.length / 2 / rate, peak);
        }
    }

    private static short[] render(AbstractSmpsData data, DacData dac, double rate, int maxFrames, boolean sfx) {
        try (OwnedSmpsAudioStream stream = new OwnedSmpsAudioStream("s2", 0,
                new SmpsPhysicalDevice.Settings(rate, false),
                LegacyCompatibilitySmpsPhysicalPolicy.INSTANCE, ChipWriteObserver.NONE)) {
            SmpsDriver driver = stream.logicalDriver();
            driver.setRegion(SmpsSequencer.Region.NTSC);
            SmpsSequencer seq = new SmpsSequencer(data, dac, driver, () -> { }, Sonic2SmpsSequencerConfig.CONFIG);
            seq.setSampleRate(rate);
            seq.setSfxMode(sfx);
            driver.addSequencer(seq, sfx);
            short[] samples = new short[maxFrames * 2];
            short[] chunk = new short[2 * 400];
            int frames = 0;
            while (frames < maxFrames && !driver.isComplete()) {
                int n = Math.min(400, maxFrames - frames);
                stream.read(chunk, n * 2);
                System.arraycopy(chunk, 0, samples, frames * 2, n * 2);
                frames += n;
            }
            // a short tail so releases ring out after the sequence ends
            int tail = Math.min(maxFrames - frames, (int) (0.25 * rate));
            for (int t = 0; t < tail; t += 400) {
                int n = Math.min(400, tail - t);
                stream.read(chunk, n * 2);
                System.arraycopy(chunk, 0, samples, frames * 2, n * 2);
                frames += n;
            }
            return java.util.Arrays.copyOf(samples, frames * 2);
        }
    }

    private static void writeWav(Path path, short[] pcm, int rate) throws IOException {
        ByteBuffer b = ByteBuffer.allocate(44 + pcm.length * 2).order(ByteOrder.LITTLE_ENDIAN);
        b.put("RIFF".getBytes()).putInt(36 + pcm.length * 2).put("WAVE".getBytes());
        b.put("fmt ".getBytes()).putInt(16).putShort((short) 1).putShort((short) 2).putInt(rate)
                .putInt(rate * 4).putShort((short) 4).putShort((short) 16);
        b.put("data".getBytes()).putInt(pcm.length * 2);
        for (short s : pcm) {
            b.putShort(s);
        }
        Files.write(path, b.array());
    }
}
