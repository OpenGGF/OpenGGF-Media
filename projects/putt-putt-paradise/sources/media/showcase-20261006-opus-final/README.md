# Putt Putt Paradise: final real-route captures with game audio (r5, 2026-10-06)

Source footage for `../promo-opus-20261006/final-verified/`. Recorded from
`feature/ai-putt-putt-paradise` at `09d5ed2a22db4b759cfd955233ab35df2837b147`, which is the PR branch
with develop `f4b40f5026988c5152eb2ae1fadaaf7c648f5618` (Slay the Robotnik PR 211) merged in, and
online wire protocol schema 6. `build-snapshot.json` holds the build:
- engine Java SHA-256 `e54abff6…`;
- golf main Java SHA-256 `73d3ddc7…`;
- jar `55c6e3fc…`;
- class-snapshot tree `40a2506d…`.

Four scenarios are recorded headless from
the production `GameLoop` with the real headless SMPS audio backend, one lossless 320x224 PNG and
one 800-frame 48 kHz stereo PCM packet per 60 Hz row:

| Directory | Scenario | Title rows | Course rows | Result |
|---|---|---|---|---|
| `ehz1-practice` | Sonic, Emerald Hill 1, one whole-shot rewind | 488 | 4923 | holes out |
| `ehz2-practice` | Tails, Emerald Hill 2 | 540 | 7851 | holes out |
| `local-match` | Sonic vs Tails, both holes, pass-the-pad readiness | 363 | 31771 | match complete |
| `online/online-host`, `online/online-guest` | two JVMs over the mod's direct TCP room on 127.0.0.1:20502 | 370 / 427 | 4985 each | 6 turns incl. a guest rewind |

Outcomes:
- **EHZ1.** Sonic, act index 0. The first lie is at course row 56. The rewind is requested at 285,
  the reverse presentation covers rows 290–360, and the course is restored at 400. He holes out at
  4443.
- **EHZ2.** Tails, act index 1 on every row. He holes out at 7371 in 25 strokes.
- **Local match.** Both holes; the match completes at row 31291.
- **Online.** 4985 lockstepped rows. The guest rewinds its second chip; reverse presentation covers
  rows 1988–2030 on both peers.

Row counts, WAV hashes and PNG-set hashes are in `native-manifest.json`; the build each capture
ran is in its `provenance.json`.

## How a row is recorded
`source/GolfPromoCapture.java` (driven by `capture_runs.py`, and by `capture_online.py` for the two
online JVMs) registers the single SDK-validated jar through `ModContext`, then:
- **Title rows** run the production `TITLE_SCREEN` mode: `GameLoop.initializeTitleScreenMode`, then
  `GameLoop.step` per row with keyboard taps. START takes the engine's own route: menu-music fade,
  screen fade, Sonic 2 `TITLE_CARD` mode, fresh course load. `title-rows.csv` logs the mode and fade
  state of every title row.
- **Course rows** call `GameLoop.step` with logical Genesis input from a BizHawk-format script
  (`input.script`, compiled to `input.bk2`).
- **Every row**, title or course, then calls `Engine.presentOuterAudioFrame` once (the same call the
  live display loop makes) and drains exactly one packet from a `LiveCaptureAudioHandle`.
  `*.wav.rows.json` proves one 800-frame packet per row.
- `audio-requests.csv` is a read-only log of the music/SFX IDs the game asked for on each row.
- The driver never writes player or world state, never hydrates from a trace and never places
  sounds by timestamp.

Two harness-only setup steps, both documented in the source:
- `HeadlessGameBoot` loads a level before the title, which a real launch does not. That level's
  armed `Level_PlayBgm` countdown is drained before recording starts (phase `boot` in the request
  log), so the title starts from the same audio state as a real launch.
- Captures read the class snapshot `engine-classes/` and `engine-classpath.snapshot.txt`, never
  the worktree's `target/`, so a concurrent Maven run cannot race them. `capture_runs.py` refuses
  to run unless the sources, snapshot and jar still match `build-snapshot.json`.
- Practice and local runs wait for the mod's real first lie (`neutralLie` in the controller's own
  snapshot, read-only) and then for row 120 before the first input (`lie-open` and `course-ready`
  in `events.csv`).

## Checks
- **Build binding.**
  - `jar-source-check.json`: the jar is byte-identical (125/125 classes and the manifest) to a fresh
    `javac --release 21` of the committed golf sources against `engine-classes/`.
  - `jar-sdk-validate.log`: `ggfmod validate` exits 0 with 10 `NON_API_ENGINE_REFERENCE` warnings and
    no errors.
  - `capture_runs.py` re-hashes sources, jar and class snapshot after the last capture.
- **Act, title card and rewind.**
  - EHZ2 runs on act index 1 for every row (`state.csv`).
  - The ROM title text exits before the first lie (row 56), and does not come back after the
    whole-shot rewind (EHZ1 rows 285 to 400).
- **Rewind sound** (`rewind_audio_check.py`, `*/rewind-audio.json`).
  - Each rewind row's 800-sample packet is reversed and located in the recorded forward shot audio.
  - EHZ1: 70 of 71 voiced packets are sample-exact reversals, walking back one row per row from
    forward row 284 to 215. All 70 are int16-identical on both channels.
  - Online: 41 of 43 host packets and 41 of 42 guest packets match the same way, from forward row
    1981 back to 1941. Each peer reverses its own heard audio.
  - The unmatched packets are each rewind's first one or two rows, where the replay cross-fades in.
  - The f3 captures, made before reverse audio existed, match 0 of 70.
- **Against the previous builds.**
  - Every PNG row and WAV of all five captures is byte-identical to the 82a (pre-merge) captures
    (compare their native manifests).
  - `state-comparison-vs-82a.json`: 0 mismatched rows; events identical.
  - `state-comparison-vs-f3.json`: EHZ2 and the local match are identical to f3. EHZ1 differs in one
    row and online is shifted one row after the rewind. That is the extra final reverse packet the
    82a fix shows before restoring.
- **Physics against r4.** `state-comparison.json` aligns each run with the r4 direct-entry run at
  its anchor event.
  - EHZ1 and the online host: 0 mismatched rows; events identical.
  - EHZ2: identical through shot 1, then a 1 px difference from row 911. Same 25 strokes; the ball
    holes out 6 rows later.
  - The local match: identical through hole 1; hole 2 differs.
  - The real route is not r4's direct level load, so these differences are expected.
  - The guest's columns follow its own Tails sprite, not the active golfer.
- **Audio.** `*/audio-qc.json` covers per-row AC and DC, flat runs and discontinuities.
  - No flat or DC-stuck stretch occurs anywhere in play.
  - The only silent runs are the 18 rows of native silence under the title card, and the 79 rows
    after the Stage Clear jingle ends.
  - The integrated AC level is about −27 to −30 dBFS in every capture. The r4 host and practice
    captures that this replaces had long DC-flat stretches.

## Rebuild
1. Build with `python3 examples/putt-putt-paradise/build.py` in the worktree.
2. Copy `target/classes` to `engine-classes/` and the jar to `source/`.
3. Write `build-snapshot.json` (digests as recorded) and copy `engine-classpath.txt` to
   `engine-classpath.snapshot.txt`, then run `python3 check_jar_source.py`.
4. Run `python3 capture_runs.py` to capture all four scenarios.
5. Run `python3 compare_states.py [ref-dir out.json]`, `audio_qc.py <dirs>`,
   `rewind_audio_check.py ehz1-practice` and
   `rewind_audio_check.py online/online-host shot-1 guest-rewind-request` (and the guest), then
   `native_manifest.py`.

`_superseded-f3/` and `_superseded-82a/` hold the earlier verified captures, kept unchanged.
`native-manifest.json` covers only the current five.

ROM: user-supplied Sonic 2 REV01, SHA-1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`. It is never
copied. No ROM bytes are in any file here other than rendered pixels and audio.
