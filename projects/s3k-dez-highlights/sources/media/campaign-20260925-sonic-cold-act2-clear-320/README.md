# Sonic solo cold DEZ2 completion — 2026-09-25

Source worktree: `/home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion`,
capture base `cc07626d9`; validated rewind repairs and route test committed as `b7d7ee91f`.
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

`TestDezSoloActTwoColdRouteCapture` passes103 complete-registry immediate restore
and45-input replay windows, all8 real boss hits, actual53721 load, live-history
reset at the load and frame-zero seek confined to the destination. Final focused
run:1 test,0 failures/errors/skips,1:08 Maven. Earlier checks exposed and repaired
attracted-ring SST restore ordering/stale slot release, and released Robotnik/door
references to their deleted boss. Combined campaign broad verification is still owed.

The final fight is a separate obligation: the exploratory continuation clears
fingers and hits the core once, then reaches the9:59 timer limit. Do not describe
this clip as an ordinary ending completion.
