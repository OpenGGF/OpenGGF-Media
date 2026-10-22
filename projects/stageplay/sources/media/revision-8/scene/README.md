# Wait for me — revision eight scene delivery

Final take: `take-3/`. It contains a 26-second story and eight-second native ride
tail, all at 60 Hz. Bundled scene commit: `4ddc82071` on
`stageplay-scene-revision`. Runtime jar was built from integration base
`1a5ae4adf487efe224f466f936d7fd8a8eded2e5`; scene changes do not modify Java.
Revision seven remains immutable. No push, merge or parent compositor render occurs here.

`manifest.json` is the handoff contract. All asset paths are relative to this
directory. `paths.story` preserves dialogue plus original combined music/SFX;
`paths.clean` and `paths.comparison` have MUSIC_STOP at zero. The main edit must
ignore movie audio and use `paths.sfx` / `paths.comparisonSfx` plus one continuous
`paths.music` bed. `paths.dialogueSfx` supplies a dialogue picture with music stopped.
`paths.cleanWithMusic` preserves the alternative original combined clean source.

`storyFrames=1560`, `totalFrames=2040`; interval ends are exclusive throughout.
`native` and `captured` record dimensions, not scale instructions. `events` are
observed native support changes; command frames are distinguished in provenance.
`comparisonMeasurements` retains native apex/landing measurements; `comparison`
contains concise compositor copy. `tutorialNotes` partition the single complete
clean pass. The proposed A/B interval is 180–450 in both takes (4.5 seconds each),
including approach, jump and landing. Default compositor duration is 75 seconds:
26 story + 6 paused rehearsal + 26 continuous notes + 9 A/B + 8 new tail.

Performance: Sonic crouches for 45 native frames when he recognizes his mistake.
Tails can fly; crossing together is a choice. “Three!” begins at 1135 and completes
at 1140, one frame before Sonic's native takeoff. Both actors remain on placement
166 throughout the tail; its native Y ranges 1936–1999. Camera offset Y stays zero,
zoom one. No physics positions/velocities, sprite poses or jumps are fabricated.

The only A/B input change is Sonic's first JUMP holdFrames 20 → 8. Both attempts
land on placement 166. The shorter hold's native apex is 20.34375 pixels lower and
landing is eight frames earlier (285 vs 293). Same approach and camera rules;
resolved camera pixels follow the different trajectory. This is a bounded route
experiment, not a pathfinder or level completion.

## Evidence and audio qualification

- `scene-checks.json`: every-frame native world/actors/puppets/camera equality
  across four story/clean/music variants, exact platform events, no hurt/death/wait
  timeout, all-frame body/panel/support envelopes and generator/source equality.
- `media-checks.json`: all six MKVs fully decoded using FFmpeg `-xerror`; frame
  counts, 640×448 dimensions, 60/1 cadence, stereo 48k audio and complete stream
  hashes. Music-stop and combined variants have identical decoded video pixels;
  story/clean native-SFX PCM matches exactly. The A/B has its own distinct stem.
- `audio-qualification.json`: bounded pre-jump/tail RMS/DC/AC windows and owner
  inspection. MUSIC_STOP closes SMPS music and stops streamed foreground music;
  no later music cues exist. First ten capture frames are exactly zero; first
  nonzero PCM is at frame 13. Native DEZ lightning requests repeated SFX 0x79.
  At 24–25 seconds RMS 290 includes mean DC 287; AC RMS is only 44. Thus near-99%
  nonzero PCM is not evidence of music. Native ambience and a DC floor remain.
  No per-sample source attribution, physical listening or perceived mix claim.
- `review-contact-arcs.png` and `review-comparison.png`: selected rendered contacts,
  jump apices, native reactions, count timing and tail. Inspected as images;
  full 1× motion review belongs to parent. Conservative body envelopes clear
  panels by at least 7.269 px, viewport by 2.708 px and supports clear panels by
  30 px. These are geometric bounds, not exact accessory/pointer pixel masks.
- `engine/identity.json` and manifest provenance: source/jar/ROM hashes and build
  identity. The supplied ROM is used directly and never copied or linked.

`wait-for-me-standalone.mp4` was produced once before parent requested no further
standalone encoding. It is the 26-second combined source at 1280×896, fully decoded;
parent owns final editorial encoding and review. No additional standalone encode
or compositor render is needed. `continuous-music.wav` is one uninterrupted
96-second DEZ2 ROM track 23 rendered with this runtime, without LIVE objects/SFX.

## Reproduce in a fresh external directory

Requires Java 25, FFmpeg/FFprobe, Python 3 and Pillow. Use the matching supplied
ROM path; never create a ROM link/copy. Install hooks in the isolated checkout.
The engine was built exactly once with:

```bash
JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 tools/testing/maven_queue.py -Dmse=off package -DskipTests
```

Copy the matching packaged jar under `engine/` and preserve its SHA256. Set paths:

```bash
export JAVA_HOME=/usr/lib/jvm/java-25-openjdk
export STAGEPLAY_ENGINE=/path/to/isolated/OpenGGF
export STAGEPLAY_JAR=/absolute/path/to/scene/engine/OpenGGF-1a5ae4ad.jar
export STAGEPLAY_ROM='/home/farrell/code/projects/OpenGGF/Sonic and Knuckles & Sonic 3 (W) [!].gen'
python3 direct_scene.py --out-dir take-3
for name in story clean story-sfx clean-sfx comparison-hold8 music-bed; do
  python3 capture.py --engine "$STAGEPLAY_ENGINE" --jar "$STAGEPLAY_JAR" --rom "$STAGEPLAY_ROM" --script "take-3/$name.screenplay.json"
done
python3 verify_scene.py
python3 verify_media.py
python3 qualify_audio.py
python3 review_frames.py
python3 publish_manifest.py --engine "$STAGEPLAY_ENGINE" --rom "$STAGEPLAY_ROM"
```

`capture.py` calls the production compile/simulate/render CLI and refuses take
replacement. It removes DISPLAY/WAYLAND_DISPLAY and Java option injection; CLI
selects surfaceless EGL and capture installs the offline no-device backend. No
interactive desktop/audio launch. The source generator uses exclusive creation.
The manifest publisher checks files/identities then publishes via atomic hard link,
refusing replacement. Keep old input takes, choose a fresh directory for revisions.

`verify_media.py` only extracts missing WAVs; its already-existing standalone is
checked but no further standalone encode is part of this handoff. Python syntax,
portable structural validation, generator/source matching and `git diff --check`
also passed. No JUnit/engine tests, baseline or broad/full suites were run: this
is scene content, with compile/native simulation/rendering as authorized checks.
No public-release or ROM-parity claim is made. Full motion/audio perception, final
edit metering, publication and integration remain parent-owned.

## Rejected takes

- `take-1/`: input sources preserved. A 44-pixel-high top panel failed compile
  because the longer Tails line overflowed. No render/simulation claimed.
- `take-2/`: 48-pixel panels compiled; story and hold8 simulations preserved. An
  all-frame envelope check caught the boast overlapping Sonic's first jump arc.
  Final take ends that line at 235, before takeoff 241. No rejected movies exist.
- `take-3/`: accepted input/simulation/rendering take. The initially considered
  eight-second A/B excerpt was shortened editorially to 4.5 seconds per arm;
  measured trajectory and source take remain unchanged.

All jobs are finished. Worktree stays clean at the scene commit for parent
integration and cleanup; external assets remain here. No runtime blocker emerged.
