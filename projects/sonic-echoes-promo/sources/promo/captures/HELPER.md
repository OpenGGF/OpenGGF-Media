# Shared capture helper

Test-only source: `examples/sonic-echoes/src/test/java/echoes/PromoCaptureMod.java`.
From checkout root with the assigned JAVA_HOME, run:

```sh
python3 /home/james/tmp/sonic-echoes-promo/captures/HELPER_BUILD.py
```

This reuses engine `target/classes` and `target/examples-classpath.txt`; it compiles main mod sources plus the test helper into an isolated temporary jar, changes only that jar's entrypoint, and never touches the distributed jar. Build output: `/home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-capture.jar`.

Invoke normal queued GameplayCaptureTool with:

```sh
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -q -Dmse=off \
 -Dopenggf.headless.gl=surfaceless-egl \
 -Dechoes.capture.room=1-2 \
 -Dechoes.capture.session=/absolute/shot/session.csv \
 -Dopenggf.saveRoot=/absolute/shot/save \
 exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool \
 "-Dexec.args=--game s2 --rom '/absolute/existing-sonic2.gen' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-capture.jar --zone ehz --act 1 --width 400 --every 1 --input /absolute/shot/inputs.txt --no-video --out-dir /absolute/shot"
```

Omit `echoes.capture.room` for a title/hub chain. Add `--title-screen --interactive-pacing` for title chains. Use every=1 and capture-from=0: the test wrapper samples each rendered frame after the ordinary mod step, without gameplay writes. Input columns contain logical direction/jump heldMask, Genesis face-button actionHeldMask and Start separately. Echo slots and fracture events are zero-based; `who` is live or echo0…echo4. Shards lists placement indices. Stars use 1–3 (Clear, Par, Shards).

Nonfinal reference loops must be padded with neutral input to the room loopFrames and then **12 more neutral frames** for the automatic commit/rewind hold. This avoids mapping the mod-only Echo verb onto a Genesis face button. A loop with no initial movement must use its authored U start. Native launch events observe the native upward impulse at spring contact or following seesaw support; badnik kills observe native destruction and identify the nearest active body within 64 px. These contact event labels should be visually checked at reported frames. Gate events track the room's channel condition (physical overlap safety can keep an already-open gate open).

Proof: a-helper-proof, four PNGs and four exactly aligned state/session rows, frame 3 visually inspected (whole HUD, visible Sonic and terrain), no desktop or audio device. Java 25, base 5fca08819f. More complete title/loop alignment is being checked in Worker A's shots.

Extended proof: title probe `a1-chain/probe` completed 2,375 rows; session/state player and camera coordinates agree on every row, including title → hub → room → clear → hub. Stable wrapper identity is cached (required by the owner-bound callback limit). Title observation unwraps the owner proxy read-only. Grounded stationary echoes with neutral current replay input are `holding`, including neutral padding before timeout.

## Tight authored-loop commits

Worker B also supplies `examples/sonic-echoes/src/test/java/echoes/PromoActionCaptureMod.java`. Build it with `HELPER_BUILD.py --actions`; use `a-helper-proof/promo-actions.jar` and `-Dechoes.capture.actions=0:100:ECHO,1:165:ECHO` (example for Two Hands). Each action follows the ordinary RoomActions → RoomSession command path, at the given native loop/frame; no positions, recordings or world values are injected. Insert **13 neutral rows** after each authored loop: one command row plus twelve rewind-hold rows. Final A takes use this bridge to keep inputs tight, rather than waiting for timeout. InputLogAuthorTool still authors all Genesis input. Action schedules appear in each exact command/NOTES. `hubSelected` is an extra title/hub evidence column in latest jars.

Known existing main-mod limit: long timeout-padded runs can exhaust owner callback identities through EchoesMod.Module.getLevelEventProvider creating wrappers (~3400 rows in 2-4 shard replay). Final compact takes avoid it. No distributed source was changed.
