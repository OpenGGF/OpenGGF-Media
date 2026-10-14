# Tails LRZ Act 2 first climb

Fresh uninterrupted cold playback on bc5e57709, native 320px, Tails solo, donor off. Starts at LRZ Act1; no position, ring, clock or other gameplay override. Full input: ../campaign-20260925-tails-branch117/variant-0.bk2 (36361 frames). The video records34128–36360, after replaying all of Act1 and the seamless handoff.

2233 frames at60fps,37.216667seconds. Full ffmpeg decode passed. All36361 CSV rows match authoring on12 fields: x/y, x/y velocity, ground speed, rings, death, mapping frame, camera x/y, sidekick presence and sprite priority. Zero differences and deaths; final x3786/y1329,11 rings. Stills35467,35938,36360 inspected.

This demonstrates the opening lower route and the turn back left into the upper climb. It is partial Act2 traversal evidence, not a complete-act, rewind certification or native-pixel-parity claim. Act1 route and51 replay spots are already committed separately. The next rising-platform climb is still being authored.

Command: DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main tails --sidekick none --input /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-branch117/variant-0.bk2 --frames 36361 --capture-from 34128 --stills 34827,35467,35847,35938,36360 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-tails-act2-first-climb-320
