# LRZ cold widescreen upper-route progress — 2026-09-28

Runtime develop f46863ed0, unchanged throughout this authoring turn. Native
Sonic+Tails,800px,donor off,cold LRZ1; no position/ring/clock seeds.

capture-input.script/bk2 contains13,225 ordinary inputs. Fresh GameplayCaptureTool
replay matches every state.csv field on all13,225 rows, zero deaths. Final Sonic
(8444,1071),128rings. Video shows10645–13224:2580frames,60fps,1600x448,43seconds.
Full ffmpeg decode passed;11180/12980/13224 stills inspected. This is forward
route/presentation evidence, not new rewind certification or a full act clear.
The existing committed first-crusher route retains its40two-cycle rewind checks.

The new inputs preserve the earned shield past the first crusher by waiting
outside the falling debris. The late spike-platform crossing eventually costs
that shield, but no death/rings. Other changes adapt moving-platform approaches,
activate the remote upper-door button and escape a Toxomister cloud by spindash.
The supposedly redundant native recovery near9990–10170 was NOT redundant: it
presses the remote button at5444,912. Full-height jumps land on top; releasing
jump early creates its required side contact. Door5664 moves860→796 when open.
No runtime changes were made to accommodate controller inputs.

upper-left-prefix.script/bk2 extends to13,650 inputs and reaches(8437,813),
zero deaths in authoring, on the ledge above the next rising platform. It has NOT
had a fresh independent replay or new whole-registry certification yet. This is
the latest stable authoring checkpoint, matching native route position16533.
A continuation from native16534 onward is in target/lrz-wide-arena-approach-20260928;
inspect its result before choosing it. All probes start cold and use ordinary
controls; branch-tool snapshots are only for trying alternate inputs.

Useful main-workspace scratch: target/lrz-native-high-section-20260928 has the
native state.csv through18000; target/lrz-wide-top-platform-phase-20260928/variant-1
reaches the late platform; target/lrz-wide-late-platform-exit-20260928/variant-0
reaches the upper-left ledge. Earlier failed candidates remain diagnostic only.

Reproduce capture with PROJECT_ROOT/CAPTURE_ROOT/NEW_CAPTURE_ROOT set:
DISPLAY=:0 java -cp "target/classes:$(cat target/resume-capture-classpath.txt)" \
 com.openggf.tools.GameplayCaptureTool --game s3k --rom "$PROJECT_ROOT/s3k.gen" \
 --zone lrz --act 1 --width 800 --main sonic --sidekick tails \
 --input "$CAPTURE_ROOT/capture-input.bk2" --frames 13225 --capture-from 10645 \
 --scale 2 --out-dir "$NEW_CAPTURE_ROOT"

Continuation result: target/lrz-wide-arena-approach-20260928/variant-0 is a
rejected suffix: it dies at15333,(8732,945). Resume from the preserved13,650-input
upper-left prefix, not that failed endpoint. No process remains running from
this authoring turn. Main develop remains f46863ed0, already pushed; no source
edits or task worktree were created during this extension.
