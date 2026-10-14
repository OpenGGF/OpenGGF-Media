# Native audio source for the Chaos reel

Origin: the 2026-10-14 revision4 correction. Production code remains unchanged;
the Chaos pool remains unchanged. The creator soundboard borrows the archived
Slay the Robotnik and Flappy Tails workflow and uses only `ctx.audio()`.
`NativeAudioCapture.java` is an engine-boundary capture wrapper, compiled into
the owned worktree's `target/`, never packaged as creator code.

`render_audio.py` holds one normal exclusive shared scheduler lease around
compilation, native capture, encoding and comparison. Children inherit its OS
lease descriptors. Native process IDs and UTC intervals go into production
provenance; temporary compiler/capture output stays in the worktree's `target/`.

HCZ2 music04 runs for 120 seconds through the normal profile-owned presentation
producer, preserving its native introduction and loops. DAC proof observes the
native `2Bh=80h` enable and nonconstant physical `DAC_STREAM` data strobes to
`2Ah`, then compares a DAC-only output projection with an all-muted control.
Existing mute diagnostics affect only rendered channel output; they do not
write DAC control registers or replace samples.

The original exporter was unsuitable: `FmSfxRenderTool` uses the legacy physical
policy and sample-owned direct reads. S3K disables DAC on sequencer admission;
its enable is owned by the native idle-loop hook after `serviceForward`. Direct
reads bypass that hook. Changing the physical policy alone would not repair
that cadence boundary. A maintained exporter fix is separate from this reel.

Ghost admissions come from a fresh exact-input, seed22, exact-JAR DEZ1 replay.
Native act0 corresponds to the original CLI act1. Every state/input CSV row and
the selected RGB interval must match the earlier picture before the schedule
can be used. Only actual accepted driver SFX are replayed, in source-frame
order, through a music-stopped creator soundboard. Its full-source-timeline WAV
uses 800 stereo samples per 60Hz presentation, with origin frame0 and no offset.

Raw requests can be stateful. S3K `zPlaySound_CheckRing` toggles raw ring request
`33h` between admitted `33h` and `34h`; admitted IDs are observations, not replay
commands. The source log pairs each raw SFX request with its accepted driver
admission by source frame and order. The isolated soundboard submits that raw
request and must reproduce all 61 resolved admissions exactly. A rejected
resolved-ID soundboard differed at frame139 and is retained separately; the
SFX-only retry reuses the already qualified native replay and never rerenders
the HCZ bed or its controls.

The first direct ghost helper used literal sidekick `none`, while the maintained
CLI translates `--sidekick none` to an empty native roster code. The strict CSV
comparison rejected its unintended sidekick at frame0. Its raw folder was
overwritten by the corrected retry before the preservation request was read;
it is not retained as a separate master. The corrected replay matched all1200
CSV rows and the selected342 RGB frames. The successful music helper snapshot
predates only this direct ghost roster correction and retains its exact SHA.

This isolated audio is **ROM SFX rendered from captured accepted events**. It is
not a stem recovered from the old mixed PCM, nor shipped-ROM parity evidence.
No DEZ music, artist percussion, guessed ghost arrival, charge or death cue is
inserted. Root's mixer keeps the HCZ bed unbroken and trims the isolated SFX at
the same selected source interval as the ghost picture.
