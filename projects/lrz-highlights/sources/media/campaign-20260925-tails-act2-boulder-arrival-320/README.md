# Tails cold LRZ2 completion and boss-act arrival

2026-09-25, runtime4dd304319 plus test/input-only additions. Native320, Tails solo, donor off, ordinary cold LRZ1 entry; no gameplay-value overrides. Canonical input src/test/resources/routes/s3k/lrz-tails-cold-act2-clear-320.bk2 contains59712 frames. Real boulder handoff loads zone22/act0 at59511. Endpoint296/1200,one earned ring,zero deaths. The arrival white flash remains active at endpoint (intentional; subsequent boss act not completed here).

All59712 state rows match branch183 variant0 on x,y,xvel,yvel,gspeed,air,hurt,dead,rings,cam_x,cam_y,high_priority: zero differences. Capture58259–59711:1453frames,60fps,24.216667seconds. ffprobe verified; full ffmpeg decode passed. Stills59100 (Knuckles/boulder),59400 (boulder carries Tails),59711 (arrival flash) inspected. Engine presentation evidence, not native pixel parity.

Command from campaign worktree:
```bash
DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --donor off --input src/test/resources/routes/s3k/lrz-tails-cold-act2-clear-320.bk2 --frames 59712 --capture-from 58259 --stills 58753,59100,59400,59711 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-act2-boulder-arrival-320
```
