# Cold widescreen SSZ first replica and transport

Source b5a9990d1, integrated and pushed as develop bdb318227; column-debris
parent-lifetime fix. Native Sonic+Tails,800px,donor off,cold SSZ1 entry, no seeds.
GameplayCaptureTool: --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k
--zone ssz --act 1 --width 800 --main sonic --sidekick tails --input input.bk2
--frames 9914 --capture-from 6000 --scale 2 --stills 6300,7951,9500,9913.

All9914 state.csv rows match the independently exported controller branch across
all recorded fields. Zero deaths;46 rings at the final upper platform,512/1420,
Tails present. GHZ killing hit at7951. Movie source6000–9913,3914frames,
1600x448,60fps,65.233seconds;ffmpeg full decode succeeds. Engine presentation
and cold reachability evidence, not synchronized native-emulator parity.

Destination verification:90 focused tests, no failures/errors/skips. The new
permanent first-replica fixture separately passes40 whole-registry checkpoints,
each with two restore/forward cycles; its test/fixture integration is pending.

Checkpoint update: first-replica fixture d27dd37c7 integrated as 19bc3ad239; destination TestSszWidePairedColdRouteCapture passed (1 test, 0 failures/errors/skips, 40 two-cycle rewind windows). Verification recorded in dfd74e979. Full paired widescreen clear remains unfinished; restart inputs and findings are in the sibling campaign-20260928-wide-pair-resume directory.
