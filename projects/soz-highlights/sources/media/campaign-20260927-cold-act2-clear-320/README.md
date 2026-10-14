# SOZ2 cold Sonic + Tails completion, 2026-09-27

Runtime base: 7a00b2915defee9e5cdd4f9d5da74e708cf82769.
Source delivery: d08120593 (feature/ai-soz-cold-route-replay); runtime gameplay unchanged.
Native 320px, Sonic + Tails, donor off, cold entry with intro enabled.
No position, ring, object, event or trace-state seeds. The canonical frozen input
is src/test/resources/routes/s3k/soz2-cold-sonic-tails.bk2 (31417 inputs).

Fresh TestSozColdAct2Capture, stride1, capture-from27000. Every input is rendered;
only the final section is saved. Input Log.txt and state.csv retain the full cold
route. All31417 state rows agree with the successful author run on movement,
ring, animation, camera, zone/act and boss-health fields. See milestones.txt for
eight natural hits, capsule, results and LRZ. This is engine reachability and
visual evidence, not emulator parity or another character/width certification.

Video: inputs27000..31416 inclusive,4417 frames at60fps,3x nearest-neighbour scale
(960x672). Full ffmpeg decode verified. Final switch approach begins the clip;
boss entry22.93s, first hit28.33s, final hit51.03s, capsule56.05s, LRZ70.60s.
