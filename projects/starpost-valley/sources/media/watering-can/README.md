# Starpost Valley watering can — 2026-10-11

Original 16×13 pixel-art can, a matching hotbar icon, three tilted poses and
falling droplets. It is drawn for 32 scene ticks after successful watering,
mirrored about the front hand and hidden on departure/movement/jump/charge.
Sonic, Tails and Knuckles keep their existing abilities and watering rules.
The saved item key remains `water_shield`; visible wording says WATERING CAN.

## Production capture

`StarpostWateringCapture.java` launches the packaged example with the real
`HeadlessGameBoot`/`GameLoop.step`, at native 400×224/60 Hz. Each take stores PNGs,
actual `state.csv`, a new accurately headed `farm.csv` and 48 kHz signed
little-endian stereo PCM (800 stereo samples/frame). The CSV observes state; it
does not drive gameplay. `farm-go=x,depth` authors directional controller input
and coasts to a plot using observed live position/speed; it never assigns farm
positions or velocities. The underlying debug commands seed scene/calendar/field
setups. `charges=0` authors the explicit empty-can precondition.

Worktree: `/home/farrell/code/projects/OpenGGF/.worktrees/ai-starpost-valley`,
updated-base merge `cc494b520c9c05a17560aeffb036de1d4508e74e` plus the watering
presentation change. `mods/starpost-valley.jar` is the final creator-validated
package. The captures predate only the final pond-hint wording correction, which
does not affect their picture, behavior or sound. No bundled ROM art was added.

Compile and run with Java 21 (use a fresh isolated cwd to avoid player saves):

```bash
WT=/home/farrell/code/projects/OpenGGF/.worktrees/ai-starpost-valley
TASK=/home/farrell/Videos/OGGF/starpost-valley/watering-can
CP="$WT/target/test-classes:$WT/target/classes:$(cat "$WT/target/test-classpath.txt")"
javac -cp "$CP" -d "$TASK/classes" "$TASK/StarpostWateringCapture.java"
# Run from a new isolated directory, supplying existing absolute S3K and S1 ROMs:
java -cp "$TASK/classes:$CP" com.openggf.StarpostWateringCapture \
 '<absolute S3K ROM>' '<absolute S1 ROM>' "$TASK/mods" \
 '<fresh absolute take directory>' "$TASK/grow-can-walk.txt" 2190
```

The final trailer take is `../promo-polish/grow-can-walk/`, launched from
`walk-run/`. All 2,190 frames complete with zero creator faults. It spends nine
charges exactly once per watered plot, at frames 534, 630, 726, 822, 918, 1014,
1110, 1206 and 1302. The first two pours have at most 1.079 pixels of movement
per frame. It uses input-only walking between watering spots. Source 1730 shows
nine grown crops before the harvest. Music is disabled for captured SFX; the
trailer mix supplies its continuous pitch-preserved 65% score.

`../promo-polish/grow-can/` and `grow-can.txt` retain the first take used to
inspect hand alignment for Sonic (frame 545), Tails (1758) and Knuckles (1848).
The initial attempted left setup had selected an empty slot after harvesting,
so it did not establish a successful left pour. `left-and-empty.txt` corrects
that setup: `left-and-empty/` (210 frames) shows an actual
left-facing pour at frame 69, a wet retry with unchanged nine charges at 100,
and an empty-can refusal after 150 with no new prop. Both complete without
creator faults. Input and reflection are capture preparation/evidence only.
These are seeded showcase takes, not a full-year, arbitrary-seed or ROM-parity
certification.

## Media and verification

`watering-preview.mp4` is a continuous six-second excerpt from final source
frames 528–887. It preserves native gameplay speed, includes the can on the bar
and in Sonic's hand, and uses the source ROM effects at normal speed. The
1200×672 export scales native pixels by exactly three with nearest-neighbour.

`../promo-polish/edit.py` and regenerated `edit.json` incorporate the fresh
farming picture and SFX; unchanged source chapters and score retain the prior
trailer polish. `previous-trailer.mp4` and `edit-before-can.py` preserve that
revision. `render.log` confirms 6,385 frames/106.416667 seconds. Final error-fatal
MP4 decode passes, as do all cut ranges and PCM/frame counts. `loudness.log`
records −16.7 LUFS, 3.7 LU range and −1.8 dBFS true peak. All three playback
copies have SHA-256
`911817a4a09fd3ba5363e116b56c24a2e82a2354f1f799b4714e1b242afebef2`.

The integrated engine checks pass: 127 focused JUnit cases without skips,
197 Starpost and 83 Three Islands creator cases, and 674 structural guards.
Final mod packaging and strict creator validation report zero findings. The
ordinary broad suite was not rerun for this bounded presentation change; prior
baseline failures remain documented on PR #220 and in the dated design.

Committed and pushed as `87f73c31dbd5763eb62e2bbba3ae24a98a4b8ce7` on
`feature/ai-starpost-valley` (PR #220); the updated-base merge is also included.
Repository precommit, prepush and explicit CI push-policy checks pass.
Consumed task Maven diagnostics were removed after their results were recorded.
