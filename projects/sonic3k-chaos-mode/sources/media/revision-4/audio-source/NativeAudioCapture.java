package com.openggf.tools;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.openggf.Engine;
import com.openggf.audio.AudioManager;
import com.openggf.audio.AudioRequestObserver;
import com.openggf.audio.AudioAdmissionObserver;
import com.openggf.audio.ChannelType;
import com.openggf.audio.driver.SfxContentionObserver;
import com.openggf.audio.driver.SmpsDriverServiceObserver;
import com.openggf.audio.synth.ChipWriteObserver;
import com.openggf.configuration.SonicConfiguration;
import com.openggf.debug.playback.Bk2MovieLoader;
import com.openggf.game.GameModuleRegistry;
import com.openggf.game.GameServices;
import com.openggf.graphics.ScreenshotCapture;
import com.openggf.mods.code.ExampleModHarness;

import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * External Chaos reel audio boundary, 2026-10-14. Borrows the maintained
 * ExampleModCapture/ExampleModHarness scene and capture loop, adding only
 * diagnostic counters. Scene creators still submit through ctx.audio().
 * The ghost mode uses GameplayCaptureSession's ordinary presentation input,
 * rendering and audio owners. It observes admissions; it never chooses them.
 * Compile into the task worktree's target/ under the inherited scheduler lease.
 */
public final class NativeAudioCapture {
    private static final ObjectMapper JSON = new ObjectMapper();

    private NativeAudioCapture() { }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) throw new IllegalArgumentException("scene or ghost mode required");
        Map<String, String> options = new LinkedHashMap<>();
        for (int i = 1; i < args.length; i += 2) {
            if (i + 1 >= args.length || !args[i].startsWith("--"))
                throw new IllegalArgumentException("Expected --option value");
            options.put(args[i].substring(2), args[i + 1]);
        }
        switch (args[0]) {
            case "scene" -> scene(options);
            case "ghost" -> ghost(options);
            default -> throw new IllegalArgumentException("Unknown mode " + args[0]);
        }
    }

    private static Path path(Map<String, String> options, String key) {
        String value = options.get(key);
        if (value == null) throw new IllegalArgumentException("Missing --" + key);
        return Path.of(value).toAbsolutePath().normalize();
    }

    private static int frames(Map<String, String> options) {
        int value = Integer.parseInt(options.getOrDefault("frames", "0"));
        if (value < 1 || value > 18_000) throw new IllegalArgumentException("Bounded frame count required");
        return value;
    }

    private static void configureAudio() {
        var config = GameServices.configuration();
        config.setSessionOverride(SonicConfiguration.AUDIO_ENABLED, true);
        config.setSessionOverride(SonicConfiguration.REGION, "NTSC");
        config.setSessionOverride(SonicConfiguration.FPS, 60);
        config.setSessionOverride(SonicConfiguration.AUDIO_INTERNAL_RATE_OUTPUT, false);
        config.setSessionOverride(SonicConfiguration.DAC_INTERPOLATE, false);
        config.setSessionOverride(SonicConfiguration.FM6_DAC_OFF, false);
        config.setSessionOverride(SonicConfiguration.AUDIO_FM_CORE, "accurate");
    }

    private static void requireClock(AudioManager audio) {
        if (audio.outputSampleRate() != 48_000 || audio.presentationFrameRate() != 60)
            throw new IllegalStateException("Requires normal 48kHz/60Hz presentation clock, got "
                    + audio.outputSampleRate() + "/" + audio.presentationFrameRate());
    }

    private static void scene(Map<String, String> options) throws Exception {
        Path out = path(options, "out"), build = path(options, "build");
        Path rom = path(options, "rom"), mod = path(options, "mod");
        int count = frames(options);
        String projection = options.getOrDefault("projection", "full");
        if (!List.of("full", "dac-only", "all-muted").contains(projection))
            throw new IllegalArgumentException("Unsupported output projection");
        boolean sfxOnly = Boolean.parseBoolean(options.getOrDefault("sfx-only", "false"));
        Files.createDirectories(out);
        System.setProperty(com.openggf.game.save.SavePaths.ROOT_PROPERTY, out.resolve("saves").toString());
        try (HeadlessGameBoot boot = new HeadlessGameBoot(400, 224, 400, 224)) {
            configureAudio();
            boot.boot(rom, 0, 0);
            try (ExampleModHarness harness = ExampleModHarness.build(mod, build)) {
                var effective = harness.apply(GameServices.module());
                GameModuleRegistry.setCurrent(effective);
                AudioManager audio = GameServices.audio();
                requireClock(audio);
                Diagnostics observed = new Diagnostics(!sfxOnly, sfxOnly);
                try (var diagnosticLease = audio.acquireDiagnosticObservers(observed.observers())) {
                    // This is the exact scene/audio path used by Slay and Flappy.
                    harness.open(effective, out.resolve("saves"), 400, 224, true);
                    if (!projection.equals("full")) {
                        for (int channel = 0; channel < 5; channel++)
                            if (!audio.isMuted(ChannelType.FM, channel)) audio.toggleMute(ChannelType.FM, channel);
                        for (int channel = 0; channel < 4; channel++)
                            if (!audio.isMuted(ChannelType.PSG, channel)) audio.toggleMute(ChannelType.PSG, channel);
                        // FM6's physical channel5 is also the DAC output window.
                        if (projection.equals("all-muted") && !audio.isMuted(ChannelType.FM, 5))
                            audio.toggleMute(ChannelType.FM, 5);
                    }
                    try (var capture = audio.beginLiveCaptureAudio(60);
                         Wav wav = new Wav(out.resolve("audio.wav"), 48_000)) {
                        short[] samples = new short[capture.maxStereoFramesPerPacket() * 2];
                        for (int frame = 0; frame < count; frame++) {
                            observed.frame = frame;
                            harness.tick();
                            HeadlessGameBoot.presentHeadlessOuterAudioFrame();
                            int samplesPerChannel = capture.drainPresentationFrame(samples);
                            if (samplesPerChannel != 800) throw new IllegalStateException("Unexpected packet cadence");
                            wav.write(samples, samplesPerChannel * 2);
                        }
                    }
                    if (sfxOnly && observed.musicPresentServices != 0)
                        throw new IllegalStateException("SFX-only soundboard retained a music sequencer");
                    if (harness.findings().values().stream().anyMatch(findings -> !findings.isEmpty()))
                        throw new IllegalStateException("Soundboard mod findings: " + harness.findings());
                    observed.write(out.resolve("observed.json"), count, projection);
                }
            }
        }
    }

    private static void ghost(Map<String, String> options) throws Exception {
        Path out = path(options, "out"), rom = path(options, "rom");
        Path mod = path(options, "mod"), inputFile = path(options, "input");
        int count = frames(options);
        Files.createDirectories(out.resolve("frames"));
        System.setProperty(com.openggf.game.save.SavePaths.ROOT_PROPERTY,
                path(options, "saves").toString());
        var movie = new Bk2MovieLoader().loadMovieOrInputLog(inputFile);
        if (movie.getFrameCount() < count) throw new IllegalArgumentException("Input log is too short");
        for (int index = 0; index < count; index++)
            MutatorGameplayCaptureTool.PresentationInput.validate(movie.getFrame(index));
        // Exact v3 ghost recipe: native DEZ1, solo Sonic, no position/ring writes.
        // The CLI normalizes --sidekick none to the empty native roster code.
        var settings = new GameplayCaptureSession.Settings(400, "sonic", "", "off",
                null, null, null);
        try (GameplayCaptureSession session = new GameplayCaptureSession(settings);
             var state = Files.newBufferedWriter(out.resolve("state.csv"))) {
            session.applyMod(mod);
            configureAudio();
            session.enableAudio();
            // CLI act1 corresponds to native act0, exactly as GameplayCaptureTool parses it.
            session.boot(rom, GameplayCaptureTool.ZoneIds.resolve("s3k", "dez"), 0, settings);
            AudioManager audio = GameServices.audio();
            requireClock(audio);
            Diagnostics observed = new Diagnostics(false, false);
            try (var diagnosticLease = audio.acquireDiagnosticObservers(observed.observers());
                 var input = MutatorGameplayCaptureTool.PresentationInput.install(session.loop());
                 var capture = audio.beginLiveCaptureAudio(60);
                 Wav wav = new Wav(out.resolve("audio.wav"), 48_000)) {
                short[] samples = new short[capture.maxStereoFramesPerPacket() * 2];
                state.write(GameplayCaptureSession.stateHeader());
                state.newLine();
                for (int frame = 0; frame < count; frame++) {
                    observed.frame = frame;
                    var row = movie.getFrame(frame);
                    session.stepPresentation(row, input);
                    Engine.presentOuterAudioFrame(session.loop(), false, false);
                    int samplesPerChannel = capture.drainPresentationFrame(samples);
                    if (samplesPerChannel != 800) throw new IllegalStateException("Unexpected packet cadence");
                    wav.write(samples, samplesPerChannel * 2);
                    state.write(session.stateLine(frame, row));
                    state.newLine();
                    ScreenshotCapture.savePNG(session.render(),
                            out.resolve("frames").resolve(String.format("%05d.png", frame)));
                }
                observed.write(out.resolve("observed.json"), count, "unmodified full native capture");
            }
        }
    }

    private static final class Diagnostics implements ChipWriteObserver, SfxContentionObserver {
        private final boolean physical;
        private final boolean checkNoMusic;
        private final List<Map<String, Object>> events = new ArrayList<>();
        private final List<Map<String, Object>> driverAdmissions = new ArrayList<>();
        private final boolean[] dacValues = new boolean[256];
        private final int[] latch = {-1, -1};
        private int frame = -1;
        private long order;
        private long dacEnableWrites, dacDisableWrites, nativeDacDataWrites;
        private long musicPresentServices;

        Diagnostics(boolean physical, boolean checkNoMusic) {
            this.physical = physical;
            this.checkNoMusic = checkNoMusic;
        }

        private Map<String, Object> event(String kind) {
            Map<String, Object> event = new LinkedHashMap<>();
            event.put("source_frame", frame);
            event.put("order", order++);
            event.put("kind", kind);
            events.add(event);
            return event;
        }

        AudioManager.DiagnosticObserverSet observers() {
            SmpsDriverServiceObserver services = !checkNoMusic ? SmpsDriverServiceObserver.NONE
                    : new SmpsDriverServiceObserver() {
                        @Override public void onServiceEnd(ServiceEvent event,
                                com.openggf.audio.rewind.SmpsDriverSnapshot snapshot) {
                            if (snapshot.sequencers().stream().anyMatch(entry -> !entry.sfx()
                                    && entry.snapshot().tracks().stream().anyMatch(track -> track.active())))
                                musicPresentServices++;
                        }
                    };
            return new AudioManager.DiagnosticObserverSet((kind, id) -> {
                Map<String, Object> event = event("request");
                event.put("request_class", kind.name());
                event.put("requested_id", id);
            }, decision -> {
                Map<String, Object> event = event("request-admission");
                event.put("requested_id", decision.context().requestedSoundId());
                event.put("resolved_id", decision.result().resolvedSoundId());
                event.put("accepted", decision.result().accepted());
                event.put("reason", decision.result().reason().name());
            }, services, this, this);
        }

        @Override public void onSfxAdmitted(Admission admitted) {
            var source = admitted.source();
            var descriptor = source.descriptor();
            Map<String, Object> event = event("driver-admitted-sfx");
            event.put("resolved_id", descriptor.id());
            event.put("descriptor_kind", descriptor.kind().name());
            event.put("admission_ordinal", source.admissionOrdinal());
            event.put("special_sfx", source.specialSfx());
            event.put("accepted", true);
            driverAdmissions.add(event);
        }

        @Override public void onYm2612Write(int port, int register, int value) {
            if (port == 0 && register == 0x2B) {
                if ((value & 0x80) != 0) dacEnableWrites++;
                else dacDisableWrites++;
            }
        }

        @Override public void onPsgWrite(int value) { }
        @Override public boolean observesPhysicalWrites() { return physical; }

        @Override public void onYm2612BusWrite(long cycle, int busPort, int value,
                PhysicalWriteOrigin origin) {
            int port = busPort >> 1;
            if ((busPort & 1) == 0) latch[port] = value & 255;
            else if (port == 0 && latch[port] == 0x2A && origin == PhysicalWriteOrigin.DAC_STREAM) {
                nativeDacDataWrites++;
                dacValues[value & 255] = true;
            }
        }

        void write(Path path, int frames, String projection) throws IOException {
            int distinct = 0;
            for (boolean value : dacValues) if (value) distinct++;
            Map<String, Object> report = new LinkedHashMap<>();
            report.put("source_frames", frames);
            report.put("sample_rate", 48_000);
            report.put("frame_rate", 60);
            report.put("samples_per_presentation", 800);
            report.put("output_projection", projection);
            report.put("dac_enable_2b80_writes", dacEnableWrites);
            report.put("dac_disable_2b00_writes", dacDisableWrites);
            report.put("native_streamed_2a_writes", nativeDacDataWrites);
            report.put("native_streamed_2a_distinct_values", distinct);
            report.put("music_present_service_snapshots", musicPresentServices);
            report.put("events", events);
            report.put("driver_admitted_sfx", driverAdmissions);
            JSON.writerWithDefaultPrettyPrinter().writeValue(path.toFile(), report);
        }
    }

    private static final class Wav implements AutoCloseable {
        private final Path path;
        private final int rate;
        private final OutputStream output;
        private final byte[] scratch = new byte[4096];
        private long samples;

        Wav(Path path, int rate) throws IOException {
            this.path = path;
            this.rate = rate;
            output = new BufferedOutputStream(Files.newOutputStream(path));
            output.write(new byte[44]);
        }

        void write(short[] data, int length) throws IOException {
            if ((length & 1) != 0 || length * 2 > scratch.length)
                throw new IllegalArgumentException("Expected one bounded stereo packet");
            for (int index = 0; index < length; index++) {
                scratch[index * 2] = (byte) data[index];
                scratch[index * 2 + 1] = (byte) (data[index] >>> 8);
            }
            output.write(scratch, 0, length * 2);
            samples += length;
        }

        @Override public void close() throws IOException {
            output.close();
            try (RandomAccessFile file = new RandomAccessFile(path.toFile(), "rw")) {
                long dataSize = samples * 2;
                if (dataSize > 0xFFFFFFFFL - 36) throw new IllegalStateException("RIFF size exceeded");
                file.seek(0);
                file.writeBytes("RIFF"); little(file, (int) dataSize + 36);
                file.writeBytes("WAVEfmt "); little(file, 16);
                file.writeShort(Short.reverseBytes((short) 1));
                file.writeShort(Short.reverseBytes((short) 2));
                little(file, rate); little(file, rate * 4);
                file.writeShort(Short.reverseBytes((short) 4));
                file.writeShort(Short.reverseBytes((short) 16));
                file.writeBytes("data"); little(file, (int) dataSize);
            }
        }

        private static void little(RandomAccessFile file, int value) throws IOException {
            file.writeInt(Integer.reverseBytes(value));
        }
    }
}
