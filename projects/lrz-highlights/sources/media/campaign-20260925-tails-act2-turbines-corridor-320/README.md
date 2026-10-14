# Tails LRZ2 turbines and middle corridor

Fresh uninterrupted cold LRZ1 playback on c8f265822; native320, Tails solo, donor off, no gameplay overrides. Input is now preserved as src/test/resources/routes/s3k/lrz-tails-cold-act2-middle-320.bk2, 41922 ordinary frames. Records37300–41921:4622frames/60fps/77.033333seconds.

All41922 state rows match branch138 variant0 on12 fields (x/y, x/y velocity, ground speed, rings, death, mapping, camera x/y, sidekick presence and priority), zero differences/deaths. Final5497/1008,1ring. Full ffmpeg decode passed; stills37590,39221,41921 inspected. TestLrzTailsColdRouteCapture#coldTailsRestoresActTwoTraversalToTheMiddleCorridor passes25 full-registry restore/45-frame replay spots, one test, no failures/errors/skips. No complete-act or native-pixel-parity claim.

Command from task worktree: DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --input /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-branch138/variant-0.bk2 --frames 41922 --capture-from 37300 --stills 37431,37590,37900,39221,39611,41445,41921 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-act2-turbines-corridor-320

Route, test and matrix committed locally as ae21cd421. Campaign integration/push remains pending.
