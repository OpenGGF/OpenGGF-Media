# Tails lower DEZ2 gravity pad — 2026-09-25

Cold DEZ1 entry, ordinary solo Tails, native320, donoroff, no position/ring/emerald
seeds. Source: `src/test/resources/routes/s3k/dez2-tails-solo-lower-gravity-pad-320.bk2`
in `/home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion`.
47140 inputs, no deaths/follower. All47140 state rows match author branch064v0
on12 fields. The pending-contact rewind fix and verified route are committed as `41d7cb05f` (base `b7d7ee91f`).

Video: inputs46550–47139,590frames at60fps,9.833333seconds. Full ffmpeg decode
passes; stills46581 (occupied inverted pad),46681 (normal-gravity landing after
jump-off/return),47065 (lower bridge) inspected. Engine presentation evidence,
not native pixel matching or Act2 completion.

After compiling, Java21/DISPLAY=:0:
```bash
java -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool \
 --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone dez --act 1 \
 --width 320 --main tails --sidekick none --donor off \
 --input src/test/resources/routes/s3k/dez2-tails-solo-lower-gravity-pad-320.bk2 \
 --frames 47140 --capture-from 46550 --stills 46581,46681,47065 --out-dir NEW_OUTPUT_DIRECTORY
```

The cold Tails route test passes12 whole-registry restore/45-input replay spots.
73 focused gravity/art/Sonic-route checks,60 Tails-route/loading checks and5
rewind guards pass, all0skip. Two short pending-contact cases failed before the
fix: restore incorrectly cleared queued press/occupied flags and changed the
next gravity-pad update. Combined campaign broad verification remains owed.
