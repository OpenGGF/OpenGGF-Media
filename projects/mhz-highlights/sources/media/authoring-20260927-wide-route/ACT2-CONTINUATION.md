# Incomplete 800px MHZ2 continuation

Base 5ff400010 plus feature/ai-mhz-wide-route camera fix. Fixed P1 inputs, Sonic solo, 800px, donor off. Cold MHZ1 start; no gameplay seeds.

- act2-upper-14010: 14,010 inputs. Alive at x8693,y1196 with10 rings; upper spike/step before the next badnik.
- act2-upper-alternative-13980: alternate upper-curl timing; alive just before reaching the same upper ledge.
- act2-lower-15884: 15,884 inputs. Alive at x9274,y1714 with4 rings, lower valley under mushroom cap at(9312,1680). Earlier attempts fall here after upper badnik damage. The big visual mushroom is a cap/platform, not the tall catapult owner.

Use GameplayInputBranchTool with game s3k, zone mhz, act1, width800, sonic, none and the named prefix count. Scripts are verified button-identical to their source prefixes. These are authoring checkpoints, not completed Act2 evidence or permanent tests.

Known traversal details: the first upper mushroom near x2012 needs braking and waiting; pulley right-hand grip needs repeated Down presses. The lower loop atx8200 returns left; keep the curve's direction until the top is flat, then stop nearx7896. The spring/swing-bar stack reaches two sticky vines at(7880,1344) and(7896,1480). Charging while outside the lower vine's capture window only releases the upper one; the lower vine captures after the dash and needs its own spindash. The apparent horizontal wind was this retained sticky pull, not a phase-dependent airflow. Waiting did not improve it.

The current code fix and complete Act1 input are committed separately from these exploratory prefixes. Native complete input remains src/test/resources/routes/s3k/mhz2-sonic-incoming-320.bk2. Generate its state CSV with GameplayCaptureTool when needed; do not preserve regenerable raw probe logs.

- act2-upper-cap-16000: 16,000 inputs, farther lower-route alternative. It bounces from the lower cap at(9312,1680) onto the moving cap near(9267,1601); endpoint is airborne near(9274,1500), four rings. Holding Right immediately hits the wall nearx9397 and drops back to the valley. Try retaining the upper cap for another higher bounce before moving right, or resume one of the upper-path prefixes. No runtime bug established.

Integrated runtime commit: a2fad9a79; documentation/check record:043d86212.

2026-09-27 follow-up on unchanged develop 6088735c8:
- The lower cap alternatives (third bounce, earlier run-up, jump and spindash) all remain west of x9397. This is a breakable-wall group at x9424/9456/9488,y1568, not a ledge to jump over: solid terrain continues above it. A correctly released right-facing dash reaches x9393,y1596 with xvel2042, rolling, then contact stops it. ROM loc_215B2/loc_215E0 gates ordinary Sonic on the wall's pushing bit, roll animation and speed $480; airborne roll alone is insufficient without the fire-shield bypass. Do not weaken the wall gates to rescue these inputs.
- The earlier upper prefix at14010 is x8693,y1196. Simple jumps, backing up and spindashes have not yet cleared that approach reliably. A read-only replay enumerating ALL active MhzStickyVineObjectInstance owners found none at this prefix, so do not attribute this later stall to the vines previously cleared nearx7896. Jump trajectories receive leftward terrain corrections near y1130 despite positive x velocity; compare the successful native-width path before treating this as a physics defect.
- These are failed authoring alternatives, not new correctness claims. Temporary candidate CSVs, images and read-only probe sources are under the main checkout's target/mhz2-wide-* and target/mhz-active-vine-probe. No production code was changed for them. A fresh native320 route-map replay is the next comparison.

- act2-upper-cleared-15037: NEW PREFERRED prefix, 15,037 inputs, x13900,y1820,61 rings, alive. The native320 path jumps at x8530 with incoming speed440; the old wide path waited until x8565 and lost all speed against the step. Branch at13885, release A for2 frames, hold R+A30 frames, then eight20R/20R+A pairs and800R clears the upper route. This is an input correction; there were no active sticky vines at the old14010 stall and no physics change. Prefix still needs uninterrupted final replay and rewind certification.

- act2-pulley-top-18987: NEW PREFERRED farther prefix, 18,987 inputs, x14270,y908,8 rings, alive, attached to the fully raised late pulley. A Right+jump release can catch the opposite handle atx14370; a second jump edge releases again. The all-Right continuation stayed on that opposite handle. Repeated30R/30R+A reaches the final catapult vicinity atx14998,y1059 with11 rings, but must stop on the mushroom rather than repeatedly jump past it. Temporary target/mhz2-wide-upper-final has those suffixes.

- act2-final-catapult-22138: farther input sequence, 22,138 inputs, 11 rings, survives repeated final-catapult launches at x14938. Branch at input21477 (after21476) to steer Right toward the upper exit: next row is x14938,y646,vy-1256; prior branches stayed neutral to map the cycle, with apexy493. The exact BK2 length is22138. Stop starting more rendered exploratory runs while the shared broad ordinary tests finish. The successful upper-passage fresh capture at campaign-20260927-wide-upper-passage-800 has14,400 state rows exactly matching the authored branch, zero deaths;560 video frames at60fps and clean full decode.
