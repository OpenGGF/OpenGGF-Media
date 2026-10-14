# Tails full cold Lava Reef chain through HPZ

2026-09-25. Runtime f7815a1de plus test/input-only additions. Native320, solo Tails, donor off; ordinary cold LRZ1 entry without position, shield, ring or emerald overrides. Canonical input: src/test/resources/routes/s3k/lrz-tails-cold-hpz-320.{script,bk2},68977 inputs. Fire shield earned from the placed monitor;12rings retained without hurt from62400 through boss/capsule/results/exit. HPZ loads68856; endpoint393/2800,3rings,player control. Zero deaths over all68977 rows.

Independent GameplayCaptureTool replay matches the authoring CSV on all68977 rows and12fields (x,y,xvel,yvel,gspeed,air,hurt,dead,rings,cam_x,cam_y,high_priority),zero differences. Captured62173–68976:6804frames,60fps,113.4s. ffprobe verified and full ffmpeg decode passed. Inspected62460 (earned fire shield/descent),63300 (arena/lava pool),67600 (defeat),68400 (results),68976 (playable HPZ). Engine presentation evidence, not matched native pixel parity.

Controller authoring used target/TailsLrzColdBossFightProbe.java, a Tails-solo adaptation of the existing LrzColdBossFightProbe. It observes live player/object positions to choose controller presses and records them; it does not inject gameplay values. Its output was compacted into the preserved script and regenerated through InputLogAuthorTool with byte-identical input payload. The independent replay above uses only those fixed inputs.

Command from campaign worktree:
```bash
DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --donor off --input src/test/resources/routes/s3k/lrz-tails-cold-hpz-320.bk2 --frames 68977 --capture-from 62173 --stills 62460,63300,67600,68400,68976 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-cold-boss-hpz-320
```
