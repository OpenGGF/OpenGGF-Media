# Tails cold DEZ2 clear — 2026-09-25

Engine presentation, not native pixel parity. Runtime commit bac660ab4 plus new test/input resources.
Cold DEZ1, ordinary Tails alone, native 320, no donor/position/ring/emerald/timer setup.
Canonical input: src/test/resources/routes/s3k/dez2-tails-solo-incoming-clear-320.bk2.
62588 steps, actual final load62467, no deaths/follower. All62468 author-prefix rows
match20 state fields. Video59000–62587,3588 frames at60fps,59.8s; full decode passed.
Inspected60520 inverted boss column and62587 actual incoming floor.62467 is the
expected black load boundary; it is not a missing-player rendering diagnosis.
One focused test passed with56 full-registry restore/45-input replay windows,
all eight boss hits and the incoming history reset/seek. Final fight remains open.

Capture: GameplayCaptureTool --game s3k --rom /home/farrell/code/projects/OpenGGF/s3k.gen --zone dez --act 1 --main tails --sidekick none --width 320 --donor off --input src/test/resources/routes/s3k/dez2-tails-solo-incoming-clear-320.bk2 --frames 62588 --capture-from 59000 --stills 59520,60520,62467 --out-dir /home/farrell/Videos/OGGF/s3k-dez-bring-up/campaign-20260925-tails-cold-act2-clear-320
