# Knuckles cold LRZ1 to direct Hidden Palace

Origin: S&K level completion campaign, 2026-09-25, candidate after dd3db3d61.
Native320, ordinary solo Knuckles, donor off, no position/shield/ring/emerald seed.
Canonical inputs: src/test/resources/routes/s3k/lrz-knuckles-cold-hpz-320.{script,bk2}.
52659 input frames, zero deaths, no follower. Real HPZ load at52418; final1075/748,0rings.
Input provenance: branch155/variant-0 prefix52419 plus240 Right; earlier alternatives in ../campaign-20260925-knuckles-input/README.md.

Independent capture command from the campaign worktree (Java21, DISPLAY=:0):
```sh
java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main knuckles --sidekick none --input src/test/resources/routes/s3k/lrz-knuckles-cold-hpz-320.bk2 --frames 52659 --capture-from 47762 --stills 50124,51813,52180,52300,52418,52658 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-knuckles-cold-hpz-fixed-320
```

All52419 source rows match fresh playback on x,y,xvel,yvel,gspeed,air,rolling,hurt,dead,rings,cam_x,cam_y; all52659 fresh rows contain0 deaths/followers. Video4897 frames at60fps,81.616667seconds, full ffmpeg decode passes. Stills inspected at52180 (final step),52300 (exit approach),52418 (expected load fade black),52658 (playable HPZ). This is engine route/presentation evidence, not native pixel parity.

This is the post-fix capture after the explicit balance-floor-probe correction. The earlier capture is superseded. All52419 source rows still match. Full route test passes81 restore/replay windows. Post-fix stills inspected at50124 and52658.
