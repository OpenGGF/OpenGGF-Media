# Ordinary solo Sonic cold DEZ ending — 2026-09-25

Source worktree: `/home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion`,
runtime `c03dc4170`; route verification committed as `9bc91e469`.
Native320, ordinary Sonic alone, donor off, cold DEZ1, no state seeds.
ROM `/home/farrell/code/projects/OpenGGF/s3k.gen`, SHA1 CFBF98C36C776677290A872547AC47C53D2761D6.
Input: `src/test/resources/routes/s3k/dez-sonic-solo-cold-ending-320.bk2`,64477 frames.
Actual ending load64476, zone13/act1 at96/300, no deaths or follower.
Final core defeated58059; escape ship defeated64190.

Video55000–64476:9477 frames,60fps,157.95s. Full decode passes.
All64477 rows match the author on20 recorded state columns (input text excluded).
Stills58060 and58813 inspected. This is engine presentation, not native pixel parity.

Reproduce after compilation from the source worktree with Java21 and DISPLAY=:0:
```bash
java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool \
  --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone dez --act 1 \
  --width 320 --main sonic --sidekick none --donor off \
  --input src/test/resources/routes/s3k/dez-sonic-solo-cold-ending-320.bk2 \
  --frames 64477 --capture-from 55000 --stills 58060,58813,64190,64476 --out-dir NEW_OUTPUT_DIRECTORY
```

`TestDezIncomingFinalRouteCapture#coldOrdinarySoloSonicClearsAllFinalPhasesAndLoadsEnding`
passes68 immediate full-registry restore/45-input replay windows, all finger/core/ship
health and actual ending load assertions.1 test,0 failures/errors/skips,1:55 Maven.
The campaign broad verification, integration and push remain outstanding.
