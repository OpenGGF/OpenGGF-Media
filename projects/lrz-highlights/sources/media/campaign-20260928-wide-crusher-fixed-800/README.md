# LRZ cold widescreen crusher correction — 2026-09-28

Source d1d7ec602; integrated into develop as25609a0ab. Destination verification passed22cases,0failures/errors/skips,1m59.
Pushed develop f46863ed0; task worktree and fully merged local branch removed. Native Sonic+Tails,800px,donor off,
cold LRZ1,6853 controller inputs, no position/ring/clock seeds.

Video: inputs5600–6852,1253 frames,60fps,1600x448,20.883333 seconds. Full ffmpeg
decode passed; stills6300/6500/6800 inspected. The complete independent capture
CSV and final helper-repair replay match every field on all6853 rows, zero
deaths. Final Sonic position4157,1841,99rings: beyond the former blocked wall.

The ROM crusher waits for Camera_X to reach$EA0 before allocating its collapse
timer. At800px the visible camera stopped at3640 behind Sonic's physical wall,
so it never reached3744. The correction uses the centered native320 camera
window, preserving the ROM player bounds and gradual camera release. It also
captures the explosion helper's timers and rebinds the owner-restored RNG;
otherwise restoring in that phase loses explosion children and changes RNG.

Candidate checks:88 initial camera/domain/S3K stability tests passed. Final
object/native-full-route/wide-route command22passed,0skips,1m55; wide route has
40 full-registry checkpoints with two45-input replay cycles. Four relevant
rewind guards passed in a fresh JVM,0skips. This is focused validation, not a
full suite/guard pass. The native53047-input full-zone HPZ clear still passes.
The rest of the wide cold route and native scene parity remain open.

Reproduce from project root, setting PROJECT_ROOT/CAPTURE_ROOT/NEW_CAPTURE_ROOT:
DISPLAY=:0 java -cp "target/classes:$(cat target/resume-capture-classpath.txt)" \
 com.openggf.tools.GameplayCaptureTool --game s3k --rom "$PROJECT_ROOT/s3k.gen" \
 --zone lrz --act 1 --width 800 --main sonic --sidekick tails \
 --input "$CAPTURE_ROOT/route.bk2" --frames 6853 --capture-from 5600 \
 --scale 2 --out-dir "$NEW_CAPTURE_ROOT"
