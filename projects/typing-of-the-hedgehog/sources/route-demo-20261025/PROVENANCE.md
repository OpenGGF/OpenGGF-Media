# Source, setup and observed evidence

## Revision and build

Actual engine/SDK build: `d3fa3d519f6acb7285d538b5f972807036f1019e` on develop.
Typing delivery is ancestor `0df2ac12962c809c512602747f2ed984250c67d5`.
The only intervening production change is the multiplayer radial Quick Chat;
Typing, Stageplay and the shared native steering source trees are unchanged.
The SDK build properties and engine `version.properties` report `d3fa3d519`.
The dirty marker reflects pre-existing submodule/untracked work; no engine or
Typing source was edited for this demo. Captures use the freshly packaged engine
and matching SDK, not an older jar.

Build artifact SHA-256 identities (external; never committed here):

- Engine: `46b9fbc192861d174355303af3a361f9070f90787effb7c698196bfc836c8019`.
- SDK: `26aa1e28ee2fbe7a2163da18a1a4c4dfc15c2037ddc94fb16305b8cf98bdbdde`.
- Typing mod: `5d5484f5393ef2bf41ab68df6b009e06c68fc7803fbb9ddd3d839200283c4cae`.

An initial `--skip-engine` mod build reused a stale `examples-classpath.txt`
containing LWJGL 3.3.3 and failed with `MemoryUtil.memFree(ShortBuffer)` missing.
Its prematurely submitted capture failed before loading the absent mod jar.
The corrected artifact-only build above completed, then the fresh 1,800-frame
capture completed successfully. No engine workaround or dependency edit was made.
The preliminary cut's inaccurate `0df2ac129` source end card was corrected in
`route-demo-current.mp4`; the earlier film and compositor remain labelled rejected.

## Original ROMs

Runtime bytes come only from the supplied ROMs. Confirmed identities:

- S1 World REV01: CRC32 `AFE05EEE`, SHA-1 `69e102855d4389c3fd1a8f3dc7d193f8eee5fe5b`.
- S2 World REV01: CRC32 `7B905383`, SHA-1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`.

Neither ROM bytes nor extracted game artwork/audio is in this source archive.

## Stageplay sources

Both films are authored shot `rehearsal`, 640×280, native Sonic, no donor/sidekick,
420 frames. Shot entry places Sonic at the authored anchor and `CLEAR_OBJECTS`
retires placed objects; rings and native terrain remain. This is staged terrain
rehearsal, not an uninterrupted stock-start run or ROM-parity certification.
Camera keys affect presentation only; actor movement comes from generated native
input commands. Linux uses surfaceless EGL, with DISPLAY/WAYLAND_DISPLAY unset;
Stageplay audio is synthesized offline. Final assembly discards source audio.

- GHZ1 anchor `(5100,686)`, target `(5860,621)`, Walk start, Run travel, Hard Stop,
  final Left. Planner: VERIFIED, 24 expanded nodes, 1,519 simulated ticks. The
  observed path follows the loop. First grounded, within-tolerance settled sample
  is frame 269; final centre `(5856.34375,620.640625)`, ground speed zero.
- EHZ1 anchor `(100,656)`, target `(400,624)`, Walk start/travel, Gentle Stop,
  final Left. Planner: VERIFIED, 22 nodes, 1,395 ticks. First settled sample is
  frame 245; final centre `(397.75390625,624.61328125)`, ground speed zero.

Each attempt uses 419 frames, 1,024 nodes, 120,000 ticks and 60,000 milliseconds
as bounds. The result reports fresh linear native-world verification. Separate
`simulate` exports every native sample, 420 per source; all have hurt/dead false.
The video's SETTLED label requires grounded state, X tolerance 6, Y tolerance 12
and absolute ground speed ≤0.25; early ARRIVED alone is not presented as settled.
The small overview displays actual observed planner points, not a search animation.

## Actual Typing source

Fresh `GameplayCaptureTool` capture of S2 Hill Top Act 2: width 400, height 224,
Sonic alone, no donor, 1,800 frames, every frame drawn and captured at 60 Hz.
No positioned CLI seeds, artificial controller movie or desktop keyboard input.
The mod selects its short course section during native entry. The selected-section
world is held while its isolated native player rehearses/runs between fights.
This is not Stageplay's complete search being called by the live course: both
share the numeric native direction/braking kernel, while Typing owns corridor
rehearsal, combat checkpoints and continuation.

The exact isolated preference recipe is in `capture_typing.py`: ARCADE,
zero-based zone 4 / act 1, NORMAL, seed 5, standard dictionary, capitals and
punctuation off, bossStars 1, No-Fail on, slow motion off, voice off, demo on,
demoRows 0. The built-in attract typist enters ordinary typing events at 9–15
rows per character. No-Fail does not solve words; demo mode saves no results.
The final film declares attract typing and No-Fail throughout this chapter.
Audio capture is disabled; headless boot owns the no-device backend.

Measured CSV: 1,800 LEVEL rows, no hurt/death. Initial running interval 234–280
moves X 2816→2842. The continuation interval 1492–1527 moves X 2842→2869;
frame 1500 visibly shows GO and running, and frame 1700 shows the next wave.
The CSV has no course-phase or word fields, so these are observed intervals,
not claimed exact combat phase boundaries. The final excerpt retains frames
234–1799 at 1×, including the wave and continuation without an intervening cut.

## Edit and verification

`assemble.py`, `edit-list.json` and `chapters.ffmeta` define the current edit.
Integer nearest-neighbour scaling preserves source aspect ratios: Stageplay 2×,
Typing 3×, padded to 1280×720. Titles, telemetry and route overview are editorial
annotations. The opening holds an actual source still for three seconds; the
final explanation card lasts two seconds. Moving footage retains 60 fps / 1×.

Final probe: H.264/yuv420p, 1280×720, 60/1 fps, 2,501 frames, 41.683333 seconds,
five ordered chapters, no audio track. Full FFmpeg `-xerror` decode passed on the
corrected final. Decoded moving views, route entry/loop/slope/settled poses,
Typing words/homing/GO/next wave and cut endpoints were inspected. Both source
movies show nonblank terrain and Sonic, and both actual route replays settle.
Browser-player automation was unavailable: two T3 snapshot calls timed out with
`Preview automation snapshot timed out after 15000ms`, and isolated IAB was not
available. Browser playback is not claimed; frame/cadence/decoder verification
and the native telemetry above are the completed checks. No claim is made for
interactive editor clicking, live search visualization, hardware pads, continuous
stock-act completion or native boss-AI parity.
