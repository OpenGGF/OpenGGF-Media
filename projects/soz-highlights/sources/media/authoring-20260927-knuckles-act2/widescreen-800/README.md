# Knuckles SOZ2 widescreen route authoring

Uncertified exploratory 800px cold route, Knuckles solo, donor off, intro enabled.
Engine source49586cd86. No player/position/ring seed. Recorded controller input only.
The saved14168-frame route reaches the moving pillar at(7936,1520) with41 rings.
It has not yet passed a fresh uninterrupted replay or rewind certification.

Changes from the native recording: leave first light before Sandworm contact;
align upper ledge takeoff; turn before giant ring; keep Left through the first
vertical wrap; re-press jump before the next wall grab; let Knuckles land before
charging the quarter-pipe spindash; glide early from the lower wall to the pillar.
The native320 canonical route remains separate and unchanged.

Continuation starts with native input15345 (jump/glide left from the pillar).
Use the existing branch author with SOZ_AUTHOR_WIDTH=800. The selected input is
replayable from cold; no checkpoint dump is needed. Source/inputs alone are
reproduction evidence, not native emulator parity.

Latest exploratory frontier: `past-spikes-29445`, alive at(19893,1260) with3 rings.
This includes the real cork release, light pull, lower rock/door, upper push switch
and spike-edge crossing. The final crossing uses a neutral stop after dodging
the Skorp projectile, then a stationary jump/glide from x19416. Resume with
native input30077. Fresh replay and rewind verification remain pending.

## Completed route

The exploratory milestones above are preserved as authoring history. The completed
35,440-input route is in `../../campaign-20260927-knuckles-cold-act2-clear-800/`.
An independent frozen-input cold replay passed: 48 whole-world replay windows,
18 semantic events, real outgoing-history isolation, and playable LRZ at 35517.
The fresh 35,619-frame capture has no deaths. Both canonical input assets are
committed in `38f799053` with the permanent native/800px tests, both passing.
The integrated work is pushed to develop, and the task worktree was removed.
The original 320px recording remains unchanged.
