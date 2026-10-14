# Cold Knuckles SOZ Act 2 clear — 2026-09-27

Fresh fixed-input production replay on uncommitted `feature/ai-soz-knuckles-act2`, base `58001b58e`. Native 320px, Knuckles solo, donation off, intro enabled. No position/ring/emerald seed and no trace hydration. All inputs from cold entry were rendered; the video is the final 9,394 frames (inputs26,100–35,493), a156.566667s excerpt at60fps, scaled3× to960×672. The original input script/BK2, complete stateCSV and command provenance are alongside the movie.

The excerpt shows the cork releasing sand/floor, light switch, rock-held door, upper switch positioning and spike/wall crossing, final switch/drop, eight-hit fight, capsule/results and playable Lava Reef arrival. It is engine visual evidence, not a synchronized native pixel-parity comparison.

Independent checks:
- `TestSozColdAct2Capture` fresh replay:1test,0failures/errors/skips, eight natural hits, capsule, results, destination control/visible palettes.35,494 observed inputs, no deaths; finalLRZ1 at(331,1969),3rings.
- Temporary candidate of existing `TestSozColdRouteCapture`:1test,0failures/errors/skips;48 traversal/destination 45-input whole-world restore/replay windows (including 11 named puzzle points) plus 18 semantic events; outgoing timeline isolation; playableLRZ at35,392. This candidate still needs its row/input promoted after the frozen broad run.
- MP4 reports9394frames,60/1fps and156.566667seconds; complete ffmpeg decode passed. Sampled images inspected for cork/light, spike clearance, first/final boss hits, capsule andLRZ arrival.

Movie offsets: cork~0:20; light0:33.5; upper spike clearance1:03; first hit1:37.6; final hit2:13.1; capsule2:21.7; LRZ2:33.6. `milestones.txt` uses original cold input indices.

Integration and final commit provenance pending. Other viewport/donor and native-presentation obligations remain in the SOZ Act2 coverage matrix.

Source integration: `49586cd86` on develop; integrated verification completed and pushed.

Delivery: runtime `49586cd86`, wide-route tests/inputs `38f799053`, pushed to develop.
Integrated full ordinary: 25,086 tests, no failures/errors, 29 reviewed skips;
guards: 672 tests, no failures/errors/skips. Permanent native/800px SOZ checks:
2 tests, no failures/errors/skips, 48 replay windows plus 18 semantic events each.
Task worktree and local branch removed after preserving final evidence.
