# Corrected player gravity mirror — 2026-09-25

Source worktree: `/home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion`,
player-render correction committed as `c03dc4170` (base `41d7cb05f`).
ROM: `/home/farrell/code/projects/OpenGGF/s3k.gen`, locked-on SHA1
`CFBF98C36C776677290A872547AC47C53D2761D6`.

Cold DEZ1, native320, ordinary Sonic alone, donor off, no position/ring/emerald/boss
seeds. `route.bk2` has53842 inputs. Actual final-stage load:53721. No deaths or
follower. All53722 authored-prefix rows match the independent column author on
12 fields. The additional120 neutral inputs reach final-stage auto-run with12 rings.

`capture.mp4`: inputs48250–53841 inclusive,5592 frames at60fps,93.2seconds.
Full ffmpeg decode passes; stills49680 (active fight),53400 (defeat),53841 (arrival)
inspected. This is engine presentation evidence, not native pixel parity.

Reproduction after compilation (Java21, DISPLAY=:0):
```bash
java -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool \
  --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone dez --act 1 \
  --width 320 --main sonic --sidekick none --donor off \
  --input src/test/resources/routes/s3k/dez2-sonic-solo-incoming-clear-320.bk2 \
  --frames 53842 --capture-from 48250 --stills 49680,53400,53841 --out-dir NEW_OUTPUT_DIRECTORY
```


The previous draw helper XORed the animation's already mirrored orientation.
All53842 CSV rows match the original capture across all recorded columns.
The corrected still49680 visibly inverts Sonic; old still49680 was upright.
Full5592-frame video decode passes,60fps,93.2s.

Focused verification:139 tests passed,0 failures/errors/skips, including both
cold DEZ2 route/replay methods. Campaign broad verification/integration remains owed.
