# Lava Reef bring-up media index

Highlights reel: `reel/lrz-bring-up-highlights.mp4` (129.95 s, 1920x1080/60, silent, 18 chapters with animated title cards).
Rebuild with `python3 reel/build_reel.py`; the edit list and chapter map are beside it.

Clips are numbered in delivery order. Raw captures keep their `raw-NN-*` directory and are never
overwritten; the input log for each is under `inputs/`. Rows 00-28 were delivered before this
index existed and are described by their own filenames.

| Clip | File | What it shows |
| --- | --- | --- |
| 00a | `00a-lrz1-baseline-before-work.mp4` | lrz1 baseline before work |
| 00b | `00b-lrz2-baseline-before-work.mp4` | lrz2 baseline before work |
| 00c | `00c-lrz3-baseline-before-work.mp4` | lrz3 baseline before work |
| 02 | `02-lrz1-parallax-before-after.mp4` | lrz1 parallax before after |
| 05 | `05-lrz1-lava-block-before-after.mp4` | lrz1 lava block before after |
| 06 | `06-lrz1-rock-sprites-before-after.mp4` | lrz1 rock sprites before after |
| 07 | `07-lrz1-animated-lava-before-after.mp4` | lrz1 animated lava before after |
| 08 | `08-lrz1-dash-elevator-before-after.mp4` | lrz1 dash elevator before after |
| 09 | `09-lrz1-rock-sprites-in-front-of-player-before-after.mp4` | lrz1 rock sprites in front of player before after |
| 10 | `10-lrz1-button-opens-door-before-after.mp4` | lrz1 button opens door before after |
| 11 | `11-lrz1-big-door-before-after.mp4` | lrz1 big door before after |
| 12 | `12-lrz1-shooting-trigger-door-before-after.mp4` | lrz1 shooting trigger door before after |
| 13 | `13-lrz1-cold-route-door-opened.mp4` | lrz1 cold route door opened |
| 14 | `14-lrz1-corkscrew-before-after.mp4` | lrz1 corkscrew before after |
| 15 | `15-lrz1-sinking-rock-before-after.mp4` | lrz1 sinking rock before after |
| 16 | `16-lrz1-wall-ride-before-after.mp4` | lrz1 wall ride before after |
| 17 | `17-lrz1-falling-spike-before-after.mp4` | lrz1 falling spike before after |
| 18 | `18-lrz1-fireball-launcher-before-after.mp4` | lrz1 fireball launcher before after |
| 19 | `19-lrz1-lava-fall-before-after.mp4` | lrz1 lava fall before after |
| 20 | `20-lrz1-swinging-spike-ball-before-after.mp4` | lrz1 swinging spike ball before after |
| 21 | `21-lrz1-smashing-spike-platform.mp4` | lrz1 smashing spike platform |
| 22 | `22-lrz1-grinding-spike-ball.mp4` | lrz1 grinding spike ball |
| 23 | `23-lrz1-spike-ball-breaks-loose.mp4` | lrz1 spike ball breaks loose |
| 24 | `24-lrz1-rock-crusher.mp4` | lrz1 rock crusher |
| 25 | `25-lrz1-iwamodoki.mp4` | lrz1 iwamodoki |
| 26 | `26-lrz1-toxomister.mp4` | lrz1 toxomister |
| 27 | `27-lrz1-fireworm.mp4` | lrz1 fireworm |
| 28 | `28-lrz1-toxomister-mist-catches.mp4` | lrz1 toxomister mist catches |
| 29 | `29-lrz1-miniboss-arrival-and-arms.mp4` | The act 1 miniboss arena, from a declared setup at `($2C00,$600)` with 355 rings (`inputs/lrz1-miniboss-arrival-v1.txt`, `raw-40-lrz1-miniboss-arrival`, frames 40-470). Sonic drops onto the arena floor at `y $7AD` -- the height the recorded run stands at -- runs right, and the camera locks at `($2C00,$710)`, the pair native holds for the whole fight. Two seconds later the miniboss theme comes in and the drill's two arms unroll link by link from under the floor, one either side, each with its firing hand on the end. Frames 260 (nothing out yet) and 380 (both arms fully out, a shot in the air) were looked at before publishing. |
| 30 | `30-lrz1-miniboss-takes-a-hit.mp4` | The drill takes a hit. Positioned entry at `($2C00,$600)` with 355 rings (`inputs/lrz1-miniboss-fight-v7.txt`, `raw-44-lrz1-miniboss-hit`, frames 900-1060). The drill drops and slams at `x 11488`, Sonic lands on its solid top, jumps, and the insta-shield pass reaches its 32x32 touch box: `collision_property` goes 6 to 5 at `V_int_run_count 972` (capture frame 971) with `collision_flags` cleared, and `sub_78C14` restores the byte 32 frames later. The decrement itself is not a `state.csv` column; it was read from a temporary `lrz.drill.probe` print on the same input, reverted before this capture, which reproduces the run's trajectory frame for frame. Frames 960, 970 and 975 were looked at. Two caveats, both recorded in the plan: only one hit lands in this script, so this is the hit and its flash window and not the whole fight; and frames 963-971 of the raw capture repeat although `state.csv` has the player moving. |
| 31 | `31-lrz1-miniboss-hand-destroyed-and-arm-peels.mp4` | The right hand takes its fourth hit and its whole arm peels away. Positioned entry at `($2C00,$600)` with 355 rings and all seven emeralds (`inputs/lrz1-miniboss-full-fight-v13.txt`, `raw-45-lrz1-miniboss-full-fight`, frames 1110-1270). Super Sonic taps jump every 34 frames from the right wall; the hand's `collision_property` falls 4 to 3 to 2 to 1 to 0 at `V_int_run_count` 273, 618, 1124 and 1156 -- one hit per pass the hand makes through jump height, two on the third -- and `sub_78CF4`'s `loc_78D2C` then flags the drill's `$38`. Frames 1140 (both arms out), 1160 (the right arm breaking) and 1230 (the right arm gone, only the left chain left, one spark still in the air) were looked at before publishing. The hand counts were read from a temporary `lrz.drill.probe` print, reverted before this capture. |
| 32 | `32-lrz1-miniboss-defeated.mp4` | The drill takes its sixth hit and the fight ends. Same capture, frames 1830-2060. `collision_property` goes 3 to 2 to 1 to 0 at `V_int_run_count` 1821, 1853 and 1885 -- three hits inside one 95-frame slam window, which is what `sub_78C14`'s `$20` invulnerability allows -- and the drill fades, breaks up and hands over to the end-of-act sign. Frames 1900 (the drill still slammed and flashing) and 1960 (the arena empty) were looked at. **The whole fight takes no damage at all**: `state.csv` has zero `hurt` frames across 4600, because the run transforms into Super Sonic at frame 170, which is what the recorded native run does at its own row 24174. |
| 33 | `33-lrz1-results-and-the-act-change.mp4` | The results screen, and the act changing underneath it. Same capture, frames 2265-2450. The act word flips on frame **2305**: the player's x goes 11560 to 296 and the camera 11264 to 0, both exactly `-$2C00`, and the floor becomes act 2's crystal while the results panel stays on screen -- the seamless change the ROM does with no title card. Frames 2350 and 3400 were looked at. **The lava filling the background is act 2's own and not act 1 residue**, corrected 2026-09-19: a native BizHawk capture of the same movie frames (`native-lrz2-bg/run1`, movie frames 415532-416433 = trace rows 25549-26450) draws the same lava at the same `Camera_Y_pos` `$710`, and a direct `$901` load forced to that camera draws it too. What the clip does show as a gap is the palette -- native keeps the act 1 miniboss palette here until the camera passes `$2C0`, where `loc_78B08` installs `Pal_LRZ2` -- and, at the time it was filmed, a player who could not walk afterwards. Clip 34 is that walk. |
| 34 | `34-lrz-act-change-walks-into-act-2.mp4` | The player walks in act 2 after the change. Positioned entry at `($2C00,$600)` with 355 rings and all seven emeralds (`inputs/lrz1-act-change-walk-v14.txt`, `raw-46-lrz-act-change-walk`, frames 3150-3900). The results tally ends, control returns, and a right-held Sonic leaves `x 296` and runs to `x 2357` across act 2's crystal floor with the act 2 background behind him. Before `4dd0844b6` he stayed at 296 for 900 frames with every control flag clear: `loc_56CAA` carries the arena's `Camera_max_X_pos` across the change with `$2C00` subtracted, and `Obj_EndSignControlDoStart`'s `Change_Act2Sizes` -- which Lava Reef was not running -- is what replaces it. Frames 3500 (crossing the lava-backed stretch) and 3800 (standing in act 2 proper) were looked at. The palette gap above is still open: `loc_78AA8`'s two camera releases and their `Pal_LRZ2` write are not implemented, so the act 2 blocks read blue here where native reads gold until the camera passes `$2C0`. |
| 35 | `35-lrz-act-2-takes-its-palette-at-2c0.mp4` | Act 2 takes its own colours where the ROM gives them, not at the act change. Same positioned entry and input as clip 34 (`inputs/lrz1-act-change-walk-v14.txt`, `raw-49-lrz-act-change-palette`, frames 3380-3760). The blocks are the miniboss palette's gold until `Camera_X_pos` reaches `$2C0` on frame **3539**, where `loc_78B08` writes `Camera_min_X_pos = $2C0` and copies `Pal_LRZ2` over palette line 1 and `Pal_LRZMiniboss3` over lines 2 and 3; from there they are act 2's blue. `Load_Level` copies the layout and no palette, which is why the fight's own colours cross the act change at all. Frames 3420 (gold, the signpost still standing), 3538 and 3541 (the swap, two frames apart) and 3700 (blue, the player running) were looked at; the gold half matches the native capture's own `f416433.png`. |
| 36 | `36-lrz2-native-route-flame-thrower.mp4` | Act 2 played on the recorded run's own controller, and the first flame thrower on it. `inputs/lrz1-fight-then-native-act2-v2.txt` is the miniboss fight truncated at the act-change frame with the `lrz` fixture's own input column from row 25558 appended, so everything after the change is the native's controller and not an authored route (`raw-51-lrz2-native-route`, frames 4360-4780). Sonic spindashes out of the change, runs the lava corridor and climbs the shaft at `x $AA8` that a right-held player only walks into. The jet across the top of frame 4450 is `$29`'s, the first act 2 object of this campaign seen firing. Frames 4450 (the flames) and 4700 (the climb, rings ahead) were looked at. The same input drives the route frontier measurement: Player 1 matches the fixture exactly for 923 rows from the change. |


## 2026-09-22 continuation

`37-lrz2-turbine-ride-and-release.mp4` (6 seconds, 960×672, 60 fps, silent)
comes from `raw-55-turbine-approach-320-20260922`. Declared positioned entry at
`($F80,$390)` above the real `$32:$00` placement `($F80,$448)`; gravity carries
Sonic into its upper capture band after the first 30 frames. Three rotations,
a fresh jump at frame 240, then the downward release and landing. Input:
`inputs/lrz2-turbine-approach-20260922-v2.txt`. The frame-240 velocity is +2172;
that is a bottom-half release, not a failed upward jump. State CSV checked and
frames 30/240 inspected. Full video decode passed. Native comparison is open.

The initial positioned-inside-band demonstrations are retained as `raw-52`
(320), `raw-53` (800), and `raw-54` (S1 donor, 400); those release upward on
frame 180 at velocity -2928. They demonstrate the other release half but lack
an approach. Each source has `provenance.json`; revision is `715b46176` plus the
uncommitted turbine slice. The existing highlights reel is not refreshed yet.

## 2026-09-22 chained platforms and native corroboration

`38-lrz2-chained-platform-ride.mp4` (8 seconds, 960×672, 60 fps, silent)
uses `raw-57-chain-80-320-20260922`: positioned at `(15C0,A50)`, 99 rings,
480 neutral frames. Sonic lands on the safe top and rides down and back up.
State CSV has zero hurt/dead frames; frame 120 was inspected. The first attempt
`raw-56-chain-81-320-20260922` encounters the placed flame thrower and is diagnostic,
not the showcase. These captures are not cold-route completions.

`native-traversal-20260922/run1` resumes the original BK2 at its own frame-415400
save and observes through 422900 without RAM writes. 9593 object observations include
1734 chain samples and 134 captured-player turbine samples. All 134 turbine Y offsets
match the ROM table; native releases at 419598/419717/419831 have Y velocities
-1944/-3072/-3012. Chained-platform roots at 422436 and 422859 begin their diagonal
with Y fraction 0x73F8, corroborating signed DIVS remainder handling. Native images
f419600 and f422620 inspected. This is behavior corroboration, not matched pixel
certification. The reusable exporter is now tools/bizhawk/capture_lrz_traversal_reference.lua.

Clip 39: raw-58-knuckles-exit-320-20260922, positioned Knuckles at (3FC8,D0),
60 right + 300 neutral frames. Actual B3 placement requests HPZ; state CSV and
frame 120 show the receiving level, with zero hurt/dead frames. Six-second
clip, full decode checked. This is a positioned transition, not cold completion.

Clip 40: raw-59-boulder-320-20260922, positioned Sonic+Tails at (3880,1C0),
37 rings, right with repeated 20-frame jumps. The actual cutscene raises the camera,
Knuckles pushes the boulder, riders are captured and LRZ3 loads at frame 693.
The next destination screen event restores rings. The selected first 720 frames
(12 seconds) have no hurt/death; frames 320 and 400 inspected and full MP4 decoded.
The remaining raw frames enter the unfinished boss act and contain a later hurt.
No cold-route or pixel-parity claim. The source predates a rewind-only final-holder
correction; ordinary playback is unchanged.

Read-only native-boulder-20260922/run1 observes movie frames 423000–428800 from
the original movie's own save. Boulder creation is 428255; camera flag 1 at428373,
flag 3 at428385, push flag 7 at428426, airborne routine at428447, first rider capture
at428475, and StartNewLevel1600 at428800. Eight screenshot observations advance an
extra frame, so those rows are absent from state.csv; no row is relabelled.


Clip 41: raw-62-lrz3-platform-art, positioned fresh load selecting the native
LRZ3 checkpoint branch (Sonic+Tails, 320px, no donor). Original BK2 input index
434068 (zero based), 37 starting rings. First 300 frames / five seconds show
approach, jump and landing on a generated platform, then departure; no hurt/dead
rows in this excerpt. Frames 180 and native 434249 were inspected for platform
art/palette. Full source dies at frame 334; this is not a completed route or a
strict replay. Raw 61 exposed an art registration error and is superseded.
Raw 60 showed presentation before the platforms existed. Assembly: assemble-41.py.

- 42-lrz3-platform-emergence.mp4 — 15 seconds, raw63 frames0–899; ROM priority-4 lava masks enabled, platform priority5→3 preserved; no hurt/death. Supersedes clip41. Positioned checkpoint start; unfinished boss encounter.

## 43 — LRZ boss first cycle (September 22)

`43-lrz3-boss-first-cycle.mp4`: 20 seconds, raw65 frames 1450–2649, original speed, silent. Shows boss emergence, mines, lava tilt and three scripted hits. No hurt/death in this excerpt; full raw65 later dies before results. Uncommitted implementation on `3fbb61e7c`, positioned checkpoint input. One native stalled frame is absent; not strict parity. Reproduce with `assemble-43.py`.

- **44-lrz3-boss-clear-and-hpz.mp4** — 37.5 s: opening cycle, final hit, capsule/results, playable Hidden Palace entry. Source raw-67, 7,300 frames, no hurt/death. Positioned fresh checkpoint, initial fire shield and 37 rings, Sonic + Tails, native donor, 320px; authored controller input after frame 1450. Not cold-entry or strict parity evidence. Native HPZ entrance corroborated in native-hpz-entry-20260922/run1.

- **45-lrz3-flash-and-missiles.mp4** — full 25 s / 1,500-frame raw-68 fresh boss-act entry: falling approach, Death Egg flash, missile release and first autoscroll section. Initial fire shield and 37 rings, Sonic + Tails, 320px native donor. No hurt/death; full decode passed. Native extra unchanged frame 429070 and inherited V-int phase remain parity caveats.

## 46 — Fresh LRZ boss act through bonus return, boss and Hidden Palace

`46-lrz3-cold-route-through-hpz.mp4` is a 53.17-second selection from
`raw-69-lrz3-cold-completion/capture.mp4` (12820 continuous frames). Native Sonic
+ Tails, 320px, fresh default position, declared initial fire shield and 37 rings.
The capture reaches Hidden Palace at frame 12700 with no hurt/death. Inputs use
the original BK2 cold approach, re-align its checkpoint continuation when the
live bonus-stage return completes, then use authored mine/capsule/exit controls.
`InputLog.txt`, `Capture.java`, `state.csv`, `provenance.json` and `assemble-46.py`
preserve setup and chapter intervals. This replaces the earlier checkpoint
footage as current route evidence after correcting the false ScreenInit teleport
and bonus-return camera ordering. It is reachability evidence, not strict parity.


## Miniboss runtime art queue — 2026-09-23

`miniboss-art-queue-20260923-320/capture.mp4` and
`miniboss-art-queue-20260923-800/capture.mp4` are fresh 600-frame positioned
arrival checks for `80d67c7fb`, replaying `inputs/lrz1-miniboss-arrival-v1.txt`.
Start ($2C00,$600), solo Sonic, 355 rings. The boss now submits its native module
and explosion art at the owning routine. Both videos decode; frame 380 native
and frame 500 wide inspected. Native-width has no hurt/death frames; wide has
88 hurt frames and no deaths. This is not equivalent combat or cold-route evidence.

### 2026-09-23 correction / centered arena

The old arrival and runtime-art movies at ($2C00,$600) skip the priority marker. Use `miniboss-centered-20260923-320/capture.mp4` and `miniboss-centered-20260923-800-v2/capture.mp4` for the corrected approach and centered presentation, validated at e76abdb1b05b83d8f84ee5e670602a366af72ec6. The intermediate `miniboss-centered-20260923-800` is rejected because it moved arm anchors. See each final directory’s provenance and CSV.


## Post-miniboss palette ramp — 2026-09-23

`campaign-20260923-postboss-palette-320-probe/capture.mp4` and `campaign-20260923-postboss-palette-800/capture.mp4`: real miniboss/results/Act2 route from corrected ($2B70,$750) entry,355rings/sevenChaosEmeralds at boot, solo/donoroff. Film3000..4199 of4200passes; zero hurt/death/follower rows. Thirteen ROM palette rows now fade the lava after results. Full decode and listed provenance stills inspected. Native-width whole-registry replay passes; wider replay pending in campaign audit. Not cold traversal or native pixel certification. Left scenery revealed by negative wide camera remains a separate gap.

Final timer-order refresh: `campaign-20260923-postboss-palette-800-v2/capture.mp4` supersedes the prior800clip. All4200CSV rows/1200PNGs byte-identical; full decode passes. Both-width route replays and native whole-ramp color/timer corroboration now pass. Native sources/analysis are under `native-postboss-palette-20260923/`.

Finite foreground follow-up: `campaign-20260923-finite-left-edge-800/capture.mp4` removes unrelated wrapped terrain from negative-camera margins. Native3201200PNGs unchanged; wide359frames differ only outside the latched foreground extent,4200gameplay rows unchanged. Boundaries remain visibly abrupt; wider scene continuity is still presentation work, not certified by this rendering fix.
