# Mutator Lab gameplay promo — reusable recipe

All commands run from this output root. Nothing touches a display, desktop input or audio device.

## 1. Build the source (once)
Original takes used `.worktrees/ai-mutators-gameplay-promo` at `964d8210b`.
The accepted commits are now on the retained `.worktrees/ai-mutators-prototype`
branch at `379b6641323853f61851943fb7aadd5e7a389e01`; the fully merged promo
worktree was removed. New-shoot helpers default to the retained worktree and
accept `OPENGGF_PROMO_ENGINE_ROOT` for another checkout. Build there before new takes:
`python3 tools/testing/maven_queue.py -q -Dmse=off test-compile` then
`python3 examples/example-mutators/build.py` → `target/example-mutators/example-mutators.jar`
(SHA-256 `9e5cdddab1ac04fa96cc9d3f494a4240c5e2936f8ffa3d20b2db7318d1075fb3`).
The drivers are now maintained in the engine, so new takes need no scratch-driver
compilation. Original driver sources and wrappers remain under `tools/driver/src/`
and `recipe/historical-driver-wrappers/` to preserve historical provenance.

## 2. Shoot (display-free)
`sh tools/finals.sh` runs the seven final takes. Each goes through `tools/cap.py`:
- seeds an isolated preference root from `inputs/*.json` (written by `tools/prefs.py`);
- compiles `inputs/**/*.script` with `InputLogAuthorTool`;
- runs `com.openggf.tools.MutatorGameplayCaptureTool` (the production `GameplayCaptureSession` loop: one native tick per
  input frame, PNG every frame, offline PCM per outer frame, identical `state.csv`) plus
  `observe.csv` (score, spilled rings incl. slotless, admitted head scale/gravity/ringfall/rebound,
  badniks, positions) and `badniks.csv`;
- environment: `DISPLAY`, `WAYLAND_DISPLAY`, `XDG_SESSION_TYPE`, `EGL_PLATFORM`, `LD_LIBRARY_PATH`
  removed; `-Dopenggf.headless.gl=surfaceless-egl`, `java.awt.headless`, `ALSOFT_DRIVERS=null`;
- registers PID/start ticks in the run manifest and writes `receipt.json` (head, dirty, jar hash, argv).

ROMs (original filenames in the main checkout, SHA-1 verified): S1 REV01 `69E10285…`, S2 REV01
`8BCA5DCE…`, S3&K `CFBF98C3…`. Zone flag note: in this engine `--game s1 --zone mz` loads
Spring Yard (`lz`→Marble, `slz`→Labyrinth, `syz`→Star Light: the S1 ROM zone ids are used as engine zone order).

Audit before looking at pictures: `python3 -I tools/audit.py final-…` → `captures/final-audit.json`.

## 3. Edit
`python3 -I recipe/build_promo.py` (ffmpeg only) → `out/mutator-lab-gameplay-promo.mp4`,
`out/chapters.json` (every segment's take and exact frame range). Segments are exact frame ranges;
audio is the same take's PCM samples `[start*800, end*800)`; video and PCM are concatenated
separately and re-timed `setpts=N/60/TB` so the film is CFR and frame-locked. Frames are flattened to
RGB (the engine framebuffer alpha is not displayed). 4× / 3× nearest scaling only.

## 4. Verify
- `ffmpeg -v error -xerror -i out/mutator-lab-gameplay-promo.mp4 -f null -`
- `python3 -I tools/verify_final.py` → `out/verify-cadence.json` (game-area crops vs source frames)
- `python3 -I tools/check_av.py` (final AAC vs exact pre-loudnorm PCM cross-correlation)

To iterate on a route: `python3 -I tools/sweep.py PREFIX GAME ZONE ACT PREFS FROMFRAME -- 'script' …`
runs variants three at a time and prints kills/hurts/deaths. `tools/layout.sh GAME ZONE ACT` dumps
an act's ring and object placements (`com.openggf.tools.LevelLayoutDumpTool`) for planning.

## Maintained capture and layout tools

The original source takes retain their historical driver receipts. For new takes,
use `com.openggf.tools.MutatorGameplayCaptureTool` on the engine classpath in
place of `promo.PromoCapture`; use `com.openggf.tools.LevelLayoutDumpTool` in
place of `promo.LayoutProbe`. Both reject a missing surfaceless backend before
opening a session. They still require the display-free environment and isolated
preferences described above. Root compared 760 hero frames with the promoted
driver: every PNG, state/observation/badnik row and offline PCM prefix was byte
identical. The revised edit changes only the zero-ring fatal-hit caption.
