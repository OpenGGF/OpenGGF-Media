# Tails LRZ2 lower-door route — 2026-09-25

Fresh cold replay on aa5ce2094, native320, Tails solo, donor off; no position, rings, shield or emerald overrides. Input: ../campaign-20260925-tails-branch171/variant-0.bk2 (56062 inputs). Capture frames53245–56061:2817 frames,60fps,46.95s. All56062 CSV rows match authoring on x,y,xvel,yvel,gspeed,air,hurt,dead,rings,cam_x,cam_y,high_priority; zero differences and zero deaths. Final11965/1776,16rings. Inspected stills55375,55500,56061. ffprobe frame count/rate verified and full ffmpeg decode passed. Not native pixel parity or rewind certification of the extension.

Command (task worktree):
```bash
DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --donor off --input /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-branch171/variant-0.bk2 --frames 56062 --capture-from 53245 --stills 55375,55500,56061 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-act2-lower-door-320
```
