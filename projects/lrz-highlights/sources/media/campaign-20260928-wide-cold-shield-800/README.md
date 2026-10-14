# LRZ cold widescreen route progress — 2026-09-28

Runtime: develop 1ba376a380c1fb62673eaba284c3bf3cdacdc7d9. No runtime changes.
Native Sonic + Tails, donor off, 800px, cold LRZ1, no position/ring/clock seeds.

capture-input.script/bk2 contains 5,900 ordinary controller inputs. Fresh
GameplayCaptureTool replay matched every CSV field on all 5,900 author rows,
zero deaths. Video shows inputs 2900–5899: 3,000 frames, 60fps, 1600x448,
50 seconds. Full ffmpeg decode passed; shield/elevator stills 4630/5230 inspected.
This is partial route evidence, not an Act1 clear, rewind certification or ROM
pixel-parity claim. Existing native320 full-zone route remains unchanged.

The native input first diverges in leader motion at3063: native bounces on the
Toxomister at4224,856, wide does not. Read-only lifetime probe observes the wide
badnik removed at2293, with rolling Tails at4212,857 and Sonic far above at4226,364.
The revised inputs clear the first button/corkscrew, westbound ledges, yellow
spring, upper gap by spindash jump, earned shield and elevator. No physics changes.

next-door-prefix.script/bk2 extends to6,243 inputs, opening the following lower
door (Sonic3708,1839). This extension is authoring evidence only, not independently
replayed yet. Next obstacle: crusher passage; target/lrz-wide-crusher-20260928
has two additional candidates, both alive but not through the passage. Keep
working from the cold prefix rather than teleporting past the obstacle.

Reproduce video from project root:
DISPLAY=:0 java -cp "target/classes:$(cat target/resume-capture-classpath.txt)" \
 com.openggf.tools.GameplayCaptureTool --game s3k --rom "$PROJECT_ROOT/s3k.gen" \
 --zone lrz --act 1 --width 800 --main sonic --sidekick tails \
 --input "$CAPTURE_ROOT/capture-input.bk2" --frames 5900 --capture-from 2900 \
 --scale 2 --out-dir "$NEW_CAPTURE_ROOT"
