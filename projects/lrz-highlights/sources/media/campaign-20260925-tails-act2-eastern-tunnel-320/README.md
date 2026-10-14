# Tails LRZ2 eastern climb and lower tunnel

Fresh cold replay on42fa53430, native320, Tails solo, donor off, no gameplay-state overrides. Source: ../campaign-20260925-tails-branch162/variant-0.bk2,53245 ordinary inputs from LRZ1. Records49600–53244:3645 frames at60fps,60.75seconds. Full ffmpeg decode passes. All53245 CSV rows match authoring on12 fields (position, velocities, ground speed, rings, death, mapping, camera, sidekick presence, priority); zero differences/deaths. Final8724/1270,10rings. Stills50153,51282,53244 inspected; final fresh PNG is pixel-identical to the branch-authoring PNG.

The black BG patch at the final tunnel is also visible in the preexisting BizHawk reference ../campaign-20260924-native-act2-floor/far-east/f425500.png. Its CSV has player8751/1274,camera8591/1146; engine final player8724/1270,camera8580/1174. Host metadata verifies ROM SHA1CFBF98C36C776677290A872547AC47C53D2761D6, exit0, no failures. This corroborates that background feature at nearby geometry; it is not exact pixel parity or a matched Tails/clock reference.

Act2 remains incomplete. The committed rewind fixture ends41922; this later section's replay spots are still pending.

Command from task worktree: DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --input /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-branch162/variant-0.bk2 --frames 53245 --capture-from 49600 --stills 50153,50632,51282,52492,53244 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-act2-eastern-tunnel-320

Matrix evidence committed locally aa5ce2094. No integration/push yet.
