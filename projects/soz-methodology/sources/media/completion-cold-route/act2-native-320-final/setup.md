# Cold SOZ2 → Lava Reef ordinary-input capture

Runtime baseline: 819d99cc1, fixed-input test added locally. Native 320×224 Sonic + Tails, donor off, cold SOZ2 entry; startup lifecycle consumed before input frame 0. No teleports or gameplay-state writes after boot.

Asset: src/test/resources/routes/s3k/soz2-cold-sonic-tails.bk2, 32432 frames. First 1500 inputs extracted from s3k-sonic-tails-complete-emeralds.bk2 at zero-based offset 365809; remainder authored through observed controller feedback, with final suffix from SozEndBossVictoryRoute. Original movie enters seamlessly; this cold route is reachability evidence, not native parity. Trace values never supplied gameplay state.

Cadence: frames/00000.png onward, one image per executed input, 60 fps playback. state.csv records every input and resulting state, zone/act, boss HP, capsule and results. milestones.txt records verified victory events. destination.png is final LRZ state. Test: TestSozColdAct2Capture, soz.cold.act2.stride=1.

Coverage: connected route through ghosts/capsule, timed doors, sandfalls, plane crossing, rocks, rappel wires, switches, both rising-sand cork rooms, upper late route, final cork, boss, capsule/results and actual LRZ load. Optional lower late rock/switch-B branch is not traversed.

Observed dense verification:1 test,0 failures/errors/skips;137.1s test time, Maven2:35. Natural hit frames30265,30469,30517,30562,30836,30868,31092,31141; results31420, capsule31465, results finished32007, LRZ load32252. Final frame32431: P1381/946, alive; destination visibly inspected.

Frozen test/asset commit: de765d83d. Follow-up sparse replay passed1 test,0 failures/errors/skips (4.747s), explicitly asserting player control and object control are released in LRZ. capture.mp4 uses60fps,3x nearest-neighbour960×672,H.264, two encoding threads; full32432frames.
