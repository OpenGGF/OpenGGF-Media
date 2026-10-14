# Knuckles cloud spindash escape

Production cold LRZ1, native320, solo Knuckles, donor off, no position/state seeds.
Input: ../campaign-20260925-knuckles-branch039/variant-0.bk2 (10570 input rows).
Executed10560 frames; rendered movie9900–10559,660frames at60fps,11seconds.
GameplayCaptureTool arguments: --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main knuckles --sidekick none --input ../campaign-20260925-knuckles-branch039/variant-0.bk2 --frames 10560 --capture-from 9900 --stills 9943,9950,10038,10559.

Before: real spindash9943–9950 retained forced landing anim34; attached cloud killed at10038.
After: animation9 at9943, attached cloud removed; no deaths in10560rows; final9847/2796 with13rings.
Inspected9943still and10559still; ffprobe660frames/60fps/11s and complete ffmpegdecode pass.
Source: working candidate after6e54f338a, glide landing animation ownership correction.
Not native pixel parity or a completed Knuckles route.
