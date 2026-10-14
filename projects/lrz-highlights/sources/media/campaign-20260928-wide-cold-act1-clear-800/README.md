# LRZ cold widescreen Act 1 clear — 2026-09-28

Runtime: develop f46863ed002e359137cbe268bea819d204de9dc7. Native Sonic+Tails, donor off, 800px, cold Act1 start, no gameplay seeds. All 25,650 inputs in capture-input.script/bk2 independently replay with zero deaths and every state.csv field matches the authoring probe.

Six drill hits: 19333, 19385, 20201, 22796, 23298, 23797. Defeated at23797. Seamless Act2 rebase at24349. Results and camera release finish; final Sonic (2357,1980), zero rings, Tails present. The full fixed-input route is being integrated with two-cycle full-registry rewind checks and live-history isolation in feature/ai-lrz-wide-act1-clear.

capture.mp4 shows inputs18500–25649 inclusive: 7,150 frames,60fps,1600×448,119.166667s. ffprobe metadata checked and full ffmpeg decode passes. Stills19335,23797,24349,25350 inspected. This is engine presentation evidence, not native pixel parity. All input/state data is retained here.

The complete route's first rewind run exposed an identity-only comparison of freshly decoded title-card Pattern tiles at24750. A separate cold probe found256 different identities but zero differing pixels. The comparison-helper fix changes no forward gameplay or rendering. The115 full-route two-cycle rewind windows and40 independent crusher windows pass. Completed ordinary lane:25146 tests,0failures/errors,29 inspected skips. Final guards:672 tests,0failures/errors/skips. Source074dafe84; merge46666b019. Destination114 tests pass, zero failures/errors/skips. Pushed develop c901b9a0f (delivery record), source074dafe84, integration46666b019.

Continuation: the route is at the ordinary Act2 climb at(2357,1980), the same endpoint as the native Act1 clear. The complete coldwide chain is now frozen in lrz-boss-sonic-tails-cold-hpz-800 and filmed in campaign-20260928-wide-cold-boss-hpz-800.

Historical authoring continuation, superseded by the complete Act2/boss fixtures: act2-upper-prefix.script/bk2 has28,070 inputs, zero deaths, final(3819,556),14 rings. A64-frame wait clears the first flamethrower. Earlier jumping, a short second hop, waiting120 frames on the third platform, and a grounded-window jump with a180-frame lift wait reach the upper platforms. The second turbine must release during its strong upward launch phase (input27889), not at its visually highest pose; the latter gives only -1440 velocity and misses the ledge. All actions use ordinary controls; no engine changes. Resume from this prefix using the native-width route around33280, whose ledge position matches.
