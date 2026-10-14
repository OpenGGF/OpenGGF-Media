# Cold Act 2 authored route attempts

All recordings start cold at (320, 940) through production startup. No gameplay state is written after boot. Exact full input logs permit replay from boot; failed tails and later retries are separate recordings.

## Connected milestones

- Capsule, ghosts, first sand corridors, checkpoint 3, light switch, and vine.
- First moving rock, swinging platform, and rappel wire.
- Pillar and spring staircase, loop and return-spring route, checkpoint 4.
- Upper cork, vertical wrap, lower passage, lower cork, rising-room switches and exit platforms.
- Sand-room exit at frame 19019 in `authored-act2-lower-exit-spikes` (center 10807, 364).
- Second wire, lower left passage, light reset, and second moving-rock track.

The upper platform exit initially appeared blocked. Read-only inspection found a moving pillar; holding Left through its opening resolved it. No engine change was required. The lower exit guide needed input recovery and a separate jump over retracting spikes. The second rock needs a second jump from the switch top after opening its gate.

These are bounded traversal attempts, not Act 2 completion. Runtime is the compiled bfce36a2c branch (root 306d7fe0f plus final wire swing correction); newer integration changes are outside this capture evidence.

| Attempt | Rows | Last center | Checkpoint | Dead |
|---|---:|---|---:|---:|
| authored-act2-beyond-ring | 8097 | 3339, 940 | 1 | 0 |
| authored-act2-current-route | 4517 | 3892, 828 | 1 | 0 |
| authored-act2-junction-route | 7890 | 5804, 941 | 3 | 0 |
| authored-act2-lower-exit-manual | 18407 | 10357, 343 | 4 | 0 |
| authored-act2-lower-exit-spikes | 19599 | 11607, 1345 | 4 | 1 |
| authored-act2-lower-guide | 17306 | 10357, 312 | 4 | 0 |
| authored-act2-main-corridor | 4296 | 3093, 940 | 1 | 0 |
| authored-act2-pillar-wait | 10836 | 8811, 361 | 4 | 0 |
| authored-act2-plane-audit | 5494 | 3009, 1857 | 1 | 0 |
| authored-act2-platform-exit-audit | 8466 | 7179, 1202 | 3 | 0 |
| authored-act2-platform-exit-audit-2 | 8366 | 7218, 1202 | 3 | 0 |
| authored-act2-platform-exit-audit-3 | 8466 | 7179, 1202 | 3 | 0 |
| authored-act2-platform-exit-audit-4 | 8366 | 7218, 1202 | 3 | 0 |
| authored-act2-post-room-drop | 20357 | 11967, 1226 | 4 | 1 |
| authored-act2-post-room-left | 20742 | 11271, 1857 | 4 | 0 |
| authored-act2-rock-ride | 6156 | 5538, 912 | 3 | 0 |
| authored-act2-rock-ride-2 | 6111 | 5454, 588 | 3 | 0 |
| authored-act2-rock-ride-3 | 6582 | 6004, 684 | 3 | 1 |
| authored-act2-rock-ride-4 | 6448 | 5941, 858 | 3 | 0 |
| authored-act2-rock-ride-5 | 6793 | 6389, 1582 | 3 | 0 |
| authored-act2-sandfall-ascent | 5494 | 4109, 684 | 1 | 0 |
| authored-act2-sandfall-jump | 5229 | 4961, 1701 | 1 | 0 |
| authored-act2-second-rock | 21809 | 11511, 1860 | 4 | 0 |
| authored-act2-second-rock-gate | 21805 | 11485, 1833 | 4 | 0 |
| authored-act2-upper-light | 11752 | 8372, 1859 | 4 | 1 |
| authored-act2-upper-route | 4822 | 5418, 1484 | 1 | 0 |
| authored-act2-wire-approach | 6700 | 6389, 752 | 3 | 0 |
| authored-act2-wire-approach-2 | 6674 | 6264, 646 | 3 | 0 |
| authored-act2-wire-approach-3 | 6735 | 6217, 698 | 3 | 0 |
| authored-act2-wire-platform | 8596 | 7163, 1452 | 3 | 0 |
| authored-act2-wrap-left | 13806 | 8693, 1388 | 4 | 0 |

## Further connected progress (runtime bfce36a2c)

`authored-act2-second-rock-gate-2` reaches the second rock, third wire, vertical wrap and the pillar junction; its tail dies in quicksand after an under-speed pillar jump. `authored-act2-pillar-crossing` corrects that approach using a running left jump. `authored-act2-fourth-wire` replays that connected prefix, catches the fourth wire, and reaches checkpoint 5 by frame 25468. It ends alive after 26869 inputs at center 14101/872, below the loop near 0x3800. These are attempts, not completion evidence. Each directory contains the full independently replayable Input Log.txt, per-frame state.csv and sparse PNGs.

The next directory, `authored-act2-integrated-replay`, uses integrated runtime a66e14bf5 to replay the connected prefix before additional route authoring. The older captured route does not certify that newer runtime.


## Final current-runtime cold Act2 route (2026-09-16)

`authored-act2-current-boss/Input Log.txt` is the successful full 32432-input route, independently replayed on 819d99cc1. The first 29931 inputs traverse cold Act2 to the real end boss; the remaining inputs naturally defeat it, open the capsule, finish results and load LRZ1, retaining 180 destination frames. Frozen asset: `src/test/resources/routes/s3k/soz2-cold-sonic-tails.bk2`. Dense independently asserted replay: `act2-native-320-final`.

Current authoring folders are sparse still sequences: every30 executed frames plus command boundaries; CSV and controller log are dense. Their `cadence.md` describes playback semantics. Rejected tails remain attempts, never completion evidence. The final successful BK2 is authoritative; it includes preserved failed maneuvers recovered through ordinary inputs.

Milestones (input counts, before next input): first rock7035, first wire7925, checkpoint410855, upper cork12000, verticalwrap12595, lower cork14645, lowerroomexit18556, secondwire19110, secondrock21605, thirdwire21984, fourthwire24180, checkpoint525458, latevinelaunch27373, upperplatform27841, upperledge28010, finalcork28120, finalshaft29851, actualendboss29931. Optional lower late rock/switchB branch is bypassed through the native upper route and remains outside this route proof.
