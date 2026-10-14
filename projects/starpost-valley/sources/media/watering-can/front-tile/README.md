# Facing-tile watering — 2026-10-11

Watering targets the adjacent field column in the farmer's facing direction.
The cursor and droplets use that plot; the pour remembers row/column/direction
and ends if the farmer turns away. The selected can waters ripe crops rather
than harvesting them and cannot open placed chests. Other actions use their
existing underfoot selection. Tails fans onward from the first facing plot.

## Reproduce the gameplay

`StarpostWateringCapture.java` is the preceding production driver extended with
read-only observation of the actual target, underfoot wet state and wet plots.
It uses `HeadlessGameBoot`/`GameLoop.step`, native 400×224/60 Hz PNGs, state/farm
CSV and 48 kHz signed little-endian stereo PCM, 800 stereo samples per frame.
The input-only `farm-go=` steering and seeded debug setup are described in the
parent README. These showcase takes do not certify a full-year/arbitrary-seed
run or ROM parity. No observation rows supply gameplay state.

```bash
WT=/home/farrell/code/projects/OpenGGF/.worktrees/ai-starpost-valley
TASK=/home/farrell/Videos/OGGF/starpost-valley/watering-can/front-tile
CP="$WT/target/test-classes:$WT/target/classes:$(cat "$WT/target/test-classpath.txt")"
javac --release 21 -cp "$CP" -d "$TASK/classes" "$TASK/StarpostWateringCapture.java"
# Run from a fresh isolated cwd, with existing absolute ROM paths:
java -cp "$TASK/classes:$CP" com.openggf.StarpostWateringCapture \
 '<absolute S3K ROM>' '<absolute S1 ROM>' "$TASK/mods" \
 '<fresh absolute take directory>' "$TASK/grow-can-forward.txt" 2190
# The isolated check uses front-tile-check.txt and 280 frames.
```

`../../promo-polish/grow-can-forward/` (cwd `run/`) contains the final take.
It waters row/column targets 1.0, 1.1, 1.2, 2.2, 2.1, 2.0, 3.0, 3.1 and 3.2 at
frames 533, 629, 725, 821, 917, 1013, 1109, 1205 and 1301. Charges descend 9→1.
At 1330, exactly the nine planted plots are wet. First/last columns are reached
by standing to their side. Native input walks between plots and reverses each
row; it never teleports between watering spots. Harvest still starts at 1730.

`check/` (cwd `check-fixed-run/`) shows the same dry column 2 watered facing
right at 57 and left at 172, while the already-wet underfoot cells stay as they
were. At 115 a wet retry has the same nine charges and no new prop; at 244 an
empty-can refusal leaves the target dry with no prop. Both the long take and
isolated check complete with zero creator faults. The initial isolated setup
pointed at already-wet demo cells, so it did not establish a pour; its input,
CSV and picture are retained in `check-initial-wet/` and the matching script/log.
The corrected dry-column-2 take supplies the evidence.

## Final media

`watering-preview.mp4` is a continuous six-second excerpt from long-take frames
528–887, including right- and left-facing pours. It preserves native gameplay
and SFX speed, scales pixels by exactly three to 1200×672 with nearest-neighbour
and includes the can bar icon. Full error-fatal MP4 decode passes.

The main trailer uses the new farming picture and SFX, with unchanged 65%
pitch-preserved score, seasonal slices, transition cues and edit timing.
`edit-before-forward.py`/`previous-trailer.mp4` retain the preceding revision.
All source cuts and PCM/frame counts pass the renderer's metadata checks.
`render.log` confirms 6385 frames/106.416667 seconds. Full error-fatal MP4 decode
passes; ffprobe confirms 1920×1080/60 fps, H.264 and stereo 48 kHz AAC.
`loudness.log` measures −16.7 LUFS integrated, 3.7 LU range, −1.8 dBFS true peak.
The export and both canonical playback copies have SHA-256
`4096f005542c6a7dbf17a7a6d41b359fb4c33b91474bfaaf7ab6618929f43df8`.

## Code validation

The new scene regression fails on the preceding `87f73c31d` at the ahead-plot
assertion. On the corrected example, queued lean Starpost scene/example checks
pass six JUnit tests without failures/errors/skips, plus 197 creator cases.
Packaging reports zero creator findings. Scene cases use actual X press/release,
all three farmers/both facings/three within-tile offsets, field edges and locked
land, wet/empty/untilled/occupied targets, planting and refill. The final edge
fixture explicitly clears underfoot cover so a bad fallback could succeed.
The existing year-of-screens smoke remains green. Proportionate focused
validation replaces the 3091-class fallback ordinary run; no shared engine
production/timing/physics/public API changes are included. Earlier broad/guard
results remain historical evidence in PR #220's design, not new passes.

The final scene-test fixture compiles directly. `bounds/` (220 frames, input
`bounds.txt`, cwd `bounds-run/`) exercises clear tilled underfoot soil at both
the first-column outside target and last-open-column target. Frames 55/115
show no spent charges, no prop and dry underfoot cells. Frame 184 shows the
first tile watered legally from beside the field: exactly one wet tile and
nine charges, with a pour. The capture has zero creator faults. `clear=row,col`
authors only those explicit initial plot conditions, not subsequent gameplay.

Production code did not change after the six-test/197-creator pass. This final
fixture-only strengthening is verified by compilation and the production take.
Two extra Maven requests were cancelled before admission behind an unrelated
serial baseline; no extra JUnit pass is claimed. A temporary detached cowtree
excluded unrelated engine edits; its accounted copies/outputs are removed.

Committed as `7169f91e17358d973d3b2d10a4130687c3951025` on `feature/ai-starpost-valley` (PR #220).
The temporary detached verification checkout is removed; the unrelated engine
edit remains untouched in the original feature worktree.

The concurrently pushed parent `a6a698293` contains the separate canonical-S2
source-guard correction. It retains the value `s2` and the exact host-ROM
comparison; its design evidence is preserved. The watering commit changes six
task files only. The original feature worktree is clean after both commits.
