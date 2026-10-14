# Typing of the Hedgehog first promo plan (task directory, never repository media)

Origin: first promo request, 2026-10-10. Assigned worktree `feature/ai-typing-hedgehog-promo`,
base `9fee32aad`. No repository edits, commits, pushes or merges. The other mod worktree is
never built or edited. All task media and helpers live here.

Target: about 75–100 s; final edit 99.9 s, 1920×1080 at 60 fps, H.264 yuv420p + AAC,
48 kHz stereo, two-pass normalization to -14 LUFS / -1 dBTP. The principal reference is
Flappy Tails: trailer text slams, overshoot, white cut flashes, short impact zoom/shake,
a half-speed keyboard moment, fictional character reviews, four bosses, and a title payoff.
Cards render at 400×224, upscale 5× nearest, then crop 40 px horizontally / 20 vertically.

The trailer introduces a Typing of the Dead-style example mod: words attached to approaching
badniks become homing strikes. Mistakes scatter letter-rings; type them to win rings back.
Show the school and progression, then let Robotnik talk, ask questions and attack. End with
the mod name, its OpenGGF example status, the own-ROM requirement, and independent fan status.
No Sega endorsement or ROM build recipe is shown. Fictional reviews are marked on screen.

## Source recordings

- `caps/ghz`: Sonic 1 Green Hill 3, Arcade, seed 7, Normal, demo typing, No-Fail, clean voices.
- `caps/ehz`: Sonic 2 Emerald Hill 2, same setup. Spindash, native travel, keyboard keys,
  homing, monitors, animal rescue, letter-rings, WAVE CLEAR, drill boss and voiced talk-back.
- `caps/fz`: Sonic 1 Final Zone, Arcade boss-only forward course; words on all four pillars,
  crushers, plasma and BOSS DEFEATED.
- `caps/dez`: Sonic 2 Death Egg, Arcade boss-only forward course; rocket fist, targeting sensor,
  slam, bombs, twelve hits, defeat and rank tally.
- `caps/hub`: S3K-host hub, captured with ExampleModCapture, `--width 400 --height 224
  --scale 5 --every 0 --audio audio.wav --video capture.mp4`. Actual title/announcer, the
  S1/S2/S3K Story maps, Tails' school and drills, Boss Rush, heat map and a sample rank reward.
  The hub debug `demo` command creates a sample profile; this is clearly a feature tour,
  not a claim of achievements from these demo runs. S3K map includes the actual incomplete
  course notice; no playable S3K course is claimed or fabricated.

All course footage is recaptured at 60 Hz. Existing fixes-*.mp4 films only guided selection;
none is an edit input. The course driver wraps GameplayCaptureSession / production GameLoop,
enables the normal HeadlessSmpsAudioBackend before boot, and records one engine presentation
packet per rendered frame. `outputSampleRate()` supplies the capture rate. Each native-speed
frame has exactly 800 stereo frames = 3,200 PCM bytes at 48 kHz / 60 Hz, measured for every
source. It stops before the course-to-hub hand-back retires the audio producer. Hub records
its own actual scene audio. The TYPE TO SURVIVE card also uses the mod's shipped announcer
voice as editorial narration; game footage always keeps its own synchronous audio.

The sole half-speed shot is labelled SLOW MOTION: 84 source frames become 168 output frames;
its measured 48 kHz PCM is pitched/slowed to match, then returned to 48 kHz. Every other shot
keeps original tick speed. There is no assumed 44.1 kHz conversion. A blue, ROM-style trailer
caption panel covers the blinking DEMO - PRESS ANY KEY label on every gameplay shot. It does
not conceal word plates, the keyboard or boss instructions. The large title-card letters
are extracted from the supplied S3K ROM using Flappy's CardFont; small captions use the
mod's own original plate face. No generated promotional art replaces actual mod footage.

## Decisions and rejected captures

ExampleModCapture's startup-scene harness accepts the hub script but does not follow its
startStockAct/relaunch request into gameplay. GameplayCaptureTool has no audio flag. Therefore
use the task-local PromoCourseCapture driver rather than fake, substitute or post-sync game
audio. This is a promo-specific helper, not an engine or mod change.

Direct BOSS_RUSH skipped Final Zone's native arena entry/presentation and left its player
invisible. Rejected both final-boss trial recordings, recaptured via Arcade's boss-only
forward rails, and visually checked Sonic, words and the arena. Preserve only the successful
sources; the tooling now chooses the valid course path. Native state CSV rings are not the
mod's virtual ring count; visual HUD and letter-ring frames own that feature selection.

Initial GHZ/EHZ recordings reached the hub hand-back and retired their capture lease. Their
valid gameplay PCM and frames were intact. Kept those frames, removed the one hand-back
video packet, muxed by the exact PCM frame count, and corrected the driver to stop before
that boundary. All final source clocks match exactly. No broken hand-back frame is edited.

## Rebuild

Prerequisites: Java 21, Maven, ffmpeg/ffprobe, Python with Pillow, NumPy and SciPy (task-local `.venv/`; `rebuild.sh` creates it if absent), and native
GL/display access already working for these captures. The own ROMs stay at their existing
absolute root paths. No ROM copying, renaming or links.

- `./rebuild.sh --from-captures`: reuse preserved ROM glyphs and regenerate background stills, cards, assembly,
  contact sheet, shot list and automated verification from preserved captures.
- `./rebuild.sh --capture`: also compile/test-compile the assigned worktree, build the example
  jar, and recapture all five sources before assembly.
- `./capture.sh ghz|ehz|fz|dez|hub`: recapture an individual source.
- `.venv/bin/python make_promo.py`: assemble from prepared assets; `--resume` is only for known
  unchanged intermediate shots during this edit, and is not required for clean rebuilds.
- `.venv/bin/python verify_promo.py`: inspect exact clocks, format, full decode, loudness and waveform
  timing. Does not replace watching the final output.

The complete shot list lives in `out/shot-list.txt` and `out/shot-list.json`; the latter also
records source in-times and edit effects. Final verification lives in `out/verification.json`.

## Final shot list

```text
000.00-001.20 one
001.20-002.40 keyboard
002.40-004.40 survive
004.40-007.40 Title logo and announcer
007.40-011.10 Sonic 2 spindash: 3-2-1 START
011.10-014.70 Sonic 1 run and roll launch
014.70-016.90 GET READY while travelling
016.90-020.90 Closing badniks and typed homing strikes
020.90-024.10 Keyboard lights and chained bounces
024.10-026.90 Keyboard impact: labelled half speed
026.90-028.20 letters
028.20-031.40 Letter rings to recover
031.40-034.40 Monitors and animal rescue
034.40-036.40 WAVE CLEAR
036.40-037.40 school
037.40-038.60 Sonic 1 Story chapter map
038.60-039.80 Sonic 2 Story chapter map
039.80-041.00 Sonic 3 and Knuckles Story map
041.00-044.00 Tails welcomes you to Typing School
044.00-047.30 Boss Training drill
047.30-049.30 Records: per-key heat map
049.30-050.90 Boss Rush selection
050.90-053.90 reviews
053.90-055.00 back
055.00-059.50 Robotnik voiced taunt typed back
059.50-063.60 Robotnik trivia window
063.60-064.80 boss
064.80-068.60 Green Hill wrecking-ball dodge
068.60-071.90 Emerald Hill drill car charge
071.90-075.40 HIT ROBOTNIK S PILLAR: four words
075.40-077.80 Final Zone crushers and plasma
077.80-078.80 climax
078.80-081.50 Death Egg rocket fist
081.50-084.50 Death Egg targeting-sensor slam
084.50-087.00 Death Egg bombs
087.00-090.00 Twelfth hit and BOSS DEFEATED
090.00-093.20 Rank tally
093.20-094.90 Rank A and record reward
094.90-099.90 end
```

## Observed validation

Java 21 `mvn -Dmse=off compile test-compile` and the example jar build completed.
No engine/mod code was changed, so no engine test suite was run for this media edit.
The shell scripts pass `sh -n`, Python sources compile, and the Java task driver compiles.
`verify_promo.py` passes full decode, exact 60 Hz/48 kHz source clocks, target codecs and
frame count. Eight waveform cross-correlations at cuts before and after slow motion
show zero lag (correlations above 0.989), independently checking A/V sync.
Final encoded AAC measures -14.16 LUFS integrated and -1.00 dBTP true peak. No all-black frames were detected.
The final was played from beginning to end at rate 1 in the collaborative browser and
reviewed with timestamped frame sheets: no debug overlay, black bars, void strips or
prominent attract-demo label appear. The only deliberate gameplay slow-down is labelled.
The new close-up keyboard shot was also replayed after its last framing refinement.

The only omitted footage is playable S3K courses: the supplied mod currently has four
forward rails (S1 GHZ/FZ and S2 EHZ/DEZ). Its actual S3K Story map is shown instead.
All selected sources have real game audio, including the shipped voice cast.

The captured edit is self-contained: `assets/` preserves the original mod plate face and
TYPE TO SURVIVE narration, and `glyphs/` preserves the decoded ROM card letters. The
`--from-captures` rebuild needs neither the worktree nor a new engine build. `--capture`
uses the assigned worktree and refreshes these source assets. A clean
`./rebuild.sh --from-captures` run completed successfully. The final Green Hill in-time
was refined to 137.9 s to remove the preceding quiz; its reassembled audio/video was
rechecked and the revised boss cut replayed. Intermediate renders and consumed scout
sheets/logs were removed; source captures and final verification are preserved.
