# S3K Death Egg bring-up media (feature/ai-s3k-dez-bring-up)

Sonic 3 & Knuckles Death Egg: `$B00`, `$B01` and the final-boss act `$1700`.
**Not Sonic 2's Death Egg.** Owning plan:
`docs/architecture/plans/2026-09-17-s3k-dez-bring-up.md`.

Clips: `sh make_clips.sh` (sources and frame ranges inside). Reel:
`reel/s3k-dez-bring-up-highlights.mp4` (79.15 s, 1920x1080/60, silent, 12 chapters with animated title cards).
Rebuild with `python3 reel/build_reel.py`; the edit list and chapter map are beside it.
All captures are silent; SFX and music claims are test-backed, never capture-backed.

| Source | Commit | Setup | Status |
| --- | --- | --- | --- |
| `raw-00-baseline-before-work/b00-act1` | `035e48a58` | `GameplayCaptureTool`, S3K zone 11 act 1, Sonic + Tails, cold load, `inputs/baseline-run-right.txt` (40 neutral, 600 Right, 40 neutral), 320 px | baseline, never overwrite |
| `raw-00-baseline-before-work/b01-act2` | `035e48a58` | same, zone 11 act 2 (direct load) | baseline, never overwrite |
| `raw-00-baseline-before-work/1700-final-boss` | `035e48a58` | same, zone 23 act 1 (`$1700`) | baseline, never overwrite |
| `raw-01-presentation-320` | `4e7655bf9` | same input, `$B00`, 320 px, slice 1 landed | current |
| `raw-02-presentation-800` | `4e7655bf9` | same input, `$B00`, 800 px | current |
| `before-01-scroll` | `4e7655bf9` + one-line revert | `Sonic3kScrollHandlerProvider`'s `ZONE_DEZ` case commented out, so the zone falls back to `SwScrlS3kDefault`; reverted and rebuilt immediately | before-shot only |
| `before-02-palette` | `4e7655bf9` + one-line revert | `Sonic3kPaletteCycler`'s `case 0x0B` body removed; reverted and rebuilt immediately | before-shot only |
| `before-03-aniplc` | `4e7655bf9` + one-line revert | `Sonic3kPatternAnimator.resolveAniPlcAddr` returns `-1` for `ZONE_DEZ`; reverted and rebuilt immediately | before-shot only |

## Clips

| Clip | Frames | Shows |
| --- | --- | --- |
| `01a-dez-static-background-before-after.mp4` | 150-450 | Left: the background sliding at camera/4 and tearing away from the foreground, leaving a black gap at the right. Right: `PlainDeformation` holding it still. |
| `01b-dez-anpal-console-cycles-before-after.mp4` | 120-420 | Left: the console and pillar colours frozen at the loaded palette. Right: `AnPal_DEZ1`'s three channels cycling lines 3 and 4. |
| `01c-dez-aniplc-machinery-tiles-before-after.mp4` | 120-420 | Left: the machinery tiles static. Right: the eight `AniPLC_DEZ` scripts animating them. |
| `01d-dez-presentation-800-wide.mp4` | 150-450 | The same stretch at 800 px: the static background fills the wide viewport with no edge gap. |

Each clip runs 300 frames (5 s at 60 fps), well over the 30-frame lead-in and lead-out minimum.
Every "before" build disabled exactly one registration in an uncommitted edit that was reverted
and recompiled before the next capture; `git status` was clean afterwards each time.

## What the baselines show

- `b00-act1`: cold `$B00` loads, the intro run plays, Sonic reaches x `$1B5` in 680 frames and
  picks up 3 rings. The background scrolls at a quarter of the camera speed — that is
  `SwScrlS3kDefault`, and it is wrong: `DEZ1_BackgroundInit` clears `Camera_X/Y_pos_BG_copy`
  and `PlainDeformation` never rewrites them, so the native background does not move at all.
  No palette cycling and no animated tiles run.
- `b01-act2`: direct `$B01` load at centre `$140,$3AC`. Same wrong background.
- `1700-final-boss`: the real DEZ3 layout, art and palette load (the Earth backdrop renders),
  but the players are placed from the Start Location file at centre `$60,$70` instead of
  `loc_7FD9E`'s `$30,$CD`, there is no arena floor object, and Sonic falls out of the level and
  dies at frame 98. No title card.

Read `state.csv` before opening any frame; it names the frame to look at.

## After slice 1

`raw-01`/`raw-02` at `4e7655bf9` show the background held still and in register, the console
palette cycling and the machinery tiles animating, at both 320 and 800 px. The `$B01` and
`$1700` baselines are unchanged by slice 1 beyond the same background and animation fixes.

## Slice 2 — reverse gravity (seeded flag)

**Every clip below seeds `Reverse_gravity_flag` ($FFFFF7C6) itself**, through
`GameplayCaptureTool --reverse-gravity`, which is declared capture setup and not something
the running game does: the ROM's writers are `Obj_DEZGravitySwitch` ($58),
`Obj_DEZTeleporter` ($59) and `Obj_DEZGravitySwap` ($5B), and those arrive in the Death Egg
object slice. Without the seed none of this is reachable in normal play yet.

All are S3K zone 11 act 2, Sonic solo, cold load at the act's own start position, captured
with `--reverse-gravity`; inputs in `inputs/`, 40 neutral frames of lead-in and lead-out.

| Clip | Commit | Frames | Shows | Read it in `state.csv` |
| --- | --- | ---: | --- | --- |
| `020-inverted-run-320/capture.mp4` | `8f5da1c8a` | 320 | Sonic falls *up* out of the act start, lands on the ceiling and runs along it, drawn upside down | `yvel` positive while `y` **falls** 940 to 777 (frames 0-40); `air` clears at frame 58 on y=723; runs x=334 to x=437 before the wall |
| `021-inverted-jump-320/capture.mp4` | `8f5da1c8a` | 242 | Two ceiling jumps: the inverted player launches *down* the screen, away from the surface it stands on, and falls back up onto it | frame 100 `yvel` = -1664 with `y` **rising** 718 to 748, `rolling` set; regrounded y=723 by frame 140; repeated at frame 142 |
| `022-inverted-roll-320/capture.mp4` | `8f5da1c8a` | 300 | Rolling along the ceiling. Down is pressed **alone** at frame 90 while ground speed is still high, because `SonicKnux_Roll` refuses the roll if left or right is held | `rolling` 1 for frames 90-106 at `gspeed` 684; and `y` reads **718** while rolling against 723 standing — the centre moved −5, which is `Player_DoRoll`'s reverse-gravity `subi.w #2*5` visible in the capture. The first take pressed Down after the wall had killed `ground_vel` and never rolled, which `state.csv` showed before any frame was opened |
| `023-camera-look-pans-320/capture.mp4` | `8f5da1c8a` | 460 | The look pans, reversed. Holding Up walks the camera **down** the screen and holding Down walks it **up** — the opposite of upright, and the opposite limits | Up held frames 40-210: `cam_y` 627 to 695. Down held frames 220-390: `cam_y` 627 to 527 |
| `020-inverted-run-528/capture.mp4` | `8f5da1c8a` | 320 | The same inverted run at 528 px: the wide viewport shows more of the ceiling the player is standing under | lands frame 47, same ceiling y=723, same final x=437 |

The run clips stop at x=437 because that is where the act-start ceiling meets a wall; that is
the terrain, not a stall in the physics. A longer inverted run needs a flat-ceiling stretch
that has not been measured yet — the one corridor measured for the tests (x=$1ACC) is flat for
only ±16 px.

## Part 10 (2026-09-18) — four groups with no clip, and why

The groups that landed on 2026-09-18 — lost rings (`c7fe5443b`), the four shields
(`5aedf369f`), the CPU sidekick respawn and carry (`42b95dcde`) and solid objects
(`24d14f342`) — have **no clips**, because none of them can be staged with the seeds
`GameplayCaptureTool` has today.

Each needs game state the tool cannot set up:

| Group | What a clip would need | Why it is not seedable |
| --- | --- | --- |
| Lost rings | a ring count and a hit, while inverted | no `--rings` seed and no scripted damage; a badnik would have to be met on a route that also has the flag set |
| Shields | a shield, while inverted | no `--shield` seed; the monitor would have to be found and broken on an inverted route |
| Sidekick respawn and carry | Tails dead off-screen, or carrying Sonic, while inverted | needs a two-character route long enough for the CPU to lose and regain the leader |
| Solid objects | an inverted player meeting a solid object | the act-start inverted run stops at x=437 on a wall (see the part-9 note above); no solid object has been measured within reach of it |

This is recorded rather than worked around: a clip that does not actually show the behaviour
is worse than none. Two things would unblock all four — slice 3's `$58`/`$59`/`$5B` writers,
which make reverse gravity reachable in normal play so an ordinary route reaches rings,
monitors and platforms with the flag set, or a small set of capture seeds (`--rings`,
`--shield`) beside the existing `--emeralds` and `--reverse-gravity`.

## 2026-09-18 — still unstaged, and what changed

Slice 3's `$5B` `Obj_DEZGravitySwap` landed, so `Reverse_gravity_flag` is now reachable from
ordinary play for the first time. That removes the *engine* half of the blocker recorded above,
but not the capture half: `GameplayCaptureTool` still needs a player route that reaches one of
the eleven act 2 `$5B` sites (x `$0700`-`$3100`, y `$0340`-`$0940`), which is act 2 cold-route
work that has not been done. The unstaged clips listed above stand unchanged; the ones needing
rings, a hit or a shield also still need `--rings` and `--shield` seeds.

## 2026-09-18 — slice 3 clips, filmed from real `$5B` triggers

Setup for all three: `GameplayCaptureTool`, S3K zone 11 act 2, **positioned entry**
(`--x/--y`, which is declared capture setup) next to a placed `$5B`, `inputs/030-*.txt` /
`inputs/031-*.txt`, 40-50 neutral frames of lead-in and 45-60 of lead-out. **No
`--reverse-gravity` seed**: the flag is written by the object, which is the whole point.

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `030-gravity-swap-flip-320/capture.mp4` | `04a1e84f7`+ | 320 | `--x 0x19E0 --y 0x08CC`, the unflipped `$5B` at x=`$1A40` y=`$08C0` | Sonic walks right into the trigger, gravity flips, he falls *up*, lands on the ceiling, jumps inverted and rolls along it | Flip at **frame 104, x=`$1A44`** — one frame past the trigger: `air` 0→1, `yvel` grows +`$38`/frame (56, 112, 168) while `y` **decreases** 2252→2248. Inverted jump at 130: `yvel` −1381 and `y` **increases** 2213→2217→2220. Grounded inverted roll frames 198-216, `y`=2030 rolling against 2035 standing — the −5 of `Player_DoRoll`'s reverse-gravity `subi.w #2*5` |
| `030-gravity-swap-flip-528/capture.mp4` | same | 528 | same | The same run at a wide viewport | Frame-identical to the 320 take at frames 104, 130, 204 and 230: same x, y, yvel, air, rolling |
| `031-gravity-swap-rings-320/capture.mp4` | same | 320 | `--x 0x2790 --y 0x066C`, the **X-flipped** `$5B` at x=`$2640` y=`$0640` | Sonic runs *left* along the ring line, collects three rings, then crosses the flipped trigger right-to-left — the direction that **sets** the flag on a flipped placement — and carries the rings inverted | Rings 0→3 by frame 96. Flip at **frame 151, x=`$2636`**: `air` 0→1, `yvel` 56/112/168 while `y` falls 1612→1611→1610. `rings` stays 3 across the flip |
| `032-gravity-swap-knuckles-320/capture.mp4` | same | 320 | as `030`, `--main knuckles` | The same flip and inverted roll as Knuckles | Flips on the same frame 104 at the same x=`$1A44`; rolls at `y`=2030 against 2035 standing, ending 3 px short of Sonic on his own radii |

## 2026-09-18 — the `$58` pad, once it had art

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `033-gravity-switch-pad-320/capture.mp4` | `37b092774` | 320 | `GameplayCaptureTool`, S3K zone 11 act 2, positioned entry `--x 0x1BE0 --y 0x0690`, the unflipped `$58` pad at x=`$1C40` y=`$06B8`; `inputs/033-gravity-switch-pad.txt` (45 neutral, 30 Right, 1 A, 55 Right, 160 neutral). No `--reverse-gravity` seed | Sonic runs at the pad, hops the 15 px onto it — the pad is a `$1B`-wide solid whose top sits above the floor, so a walk into its side is a push, not a press — the pad sinks, and four updates later gravity flips and he falls *up* to the ceiling | Lands on the pad at **frame 107** (`air` 1→0, y=1692, feet at 1711 against the pad's 1712 top). **Frame 108** `air` back to 1 with `yvel` 0: `sub_48B40`'s rider release. Toggle at **frame 111**: `yvel` then climbs +`$38`/frame (56, 112, 168) while `y` **falls** 1692→1491, the reverse-gravity signature. Lands inverted on the ceiling at **frame 152** and runs right along it. Frames looked at: 100 (pad drawn, armed, unoccupied), 107 (Sonic standing on it), 130 (pressed pose while he falls upward mirrored) |

The pad is the first `$58` clip: before this commit it was invisible, so a clip would have
shown Sonic standing on nothing and then falling upward for no visible reason.

## 2026-09-18 — the `$5A` gravity tube, and what the capture found

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `035-gravity-tube-320/capture.mp4` | `e9b54292b` | 320 | `GameplayCaptureTool`, S3K zone 11 act 2, positioned entry `--x 0x19E0 --y 0x08CC`; `inputs/035-gravity-tube.txt` (45 neutral, 200 Right, 60 neutral). No `--reverse-gravity` seed | Sonic runs right into the **co-located `$5B` + `$5A` pair** at `$1A40,$08C0` — the placement table has the swap at record 263 and the tube at record 264, same x, same y — so the trigger flips gravity in the tube's own mouth | Nineteen frames of `air` alternating 1/0 with `y` pinned at 2252 (frames 109-127), then a clean inverted fall: `yvel` 56, 112, 168 … 1176 while `y` drops 2252 → 2206, landing on the ceiling at **frame 149** and running right along it |

**The alternation is recorded, not explained.** It is what the capture shows, it survives the
per-frame ride hold added in `e9b54292b` byte for byte over frames 99-159, and the ROM reading
suggests it may be faithful: `sub_48F12`'s mount has no `Status_InAir` test (:95216-95252), so a
player the inverted gravity lifts off the tube is re-mounted the next frame by
`RideObject_SetRide`'s `Player_TouchFloor`. **Kill condition:** a native BizHawk capture of a
player crossing `$1A40,$08C0` under reverse gravity either shows the same alternation, in which
case it is faithful and the note becomes a positive record, or it does not, in which case the
mount's re-entry is an engine bug. No native capture of that site was taken this session.

**The sidekick clip is still not filmable, and the reason has moved.** `GameplayCaptureTool`
now does teleport the whole team on a positioned entry (`257059dd3`), and the seed is confirmed
applied — instrumenting `getRegisteredSidekicks()` at the seed point reads 1 on the first step
and 0 at boot, which is why the first version of the seed moved nobody. With the seed working,
Tails is *still* absent from every frame of a 291-frame capture at the `$1A40` site (checked at
5, 160 and 280); the take was inspected and deleted rather than shipped. Something downstream
of the seed keeps him out of that corridor. **Kill condition:** log the registered sidekick's
`x`/`y` on each of the first 60 frames of that capture; either it never leaves the act start —
the seed is being undone — or it is in the corridor and the sprite is hidden or culled.

**Two clips that could not be filmed, with the reason measured rather than assumed.**

- **Sidekick Tails under reverse gravity.** `--x/--y` teleports the *leader only*; the
  sidekick stays at the act's start position ~6000 px away and does not catch up inside a
  282-frame capture. The take was made, inspected (no Tails in frame at 30, 170 or 270,
  HUD reads `SONIC` with one life icon) and deleted rather than shipped. This needs the
  cold act 2 route or a tool that teleports the whole team.
- **Rings + a hit + the lost-ring spill, a shield, and a solid-object ride.** Decoding
  `DEZ2_Sprites` and `DEZ2_Rings` around all eleven `$5B` sites: no monitor (`$26`) and no
  ring within `$180` px of six of them; the only concrete hurt blocks in the act are one
  `$6A` at `$1B40,$06D8` and five `$6B` at `y=$0FE0`, the nearest being 256 px across and
  488 px up from the nearest trigger, through terrain served by objects that are still
  placeholders; and every `$5B` site's own neighbour is a `$5A` gravity tube, which slice 3
  has not implemented. So these three are blocked on **slice 3's remaining objects and the
  act 2 route**, not on the flag being unreachable — that part is now fixed.

A correction to the earlier note in this file and in the plan: the `$5B` sites are **not**
"in open corridor with no terrain within ±32 px". Every one of the eleven has flat floor
about `$1F` below the trigger centre, flat across at least ±64 px, and that floor is
*inside* the trigger's `±$20` Y band — which is exactly why a walking player crosses it.

## 2026-09-18 — the sidekick blocker: the native park is the entrance, not act 2

The kill condition recorded above assumed one of two answers. The native rows settle it before
any capture is taken. Sampling `sidekick_x`/`sidekick_y` out of
`src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/ssz/physics.csv.gz`:

| Native row | Player | Sidekick | Sidekick air |
| ---: | --- | --- | ---: |
| 19500 (act 1, still walking) | `0140,07DC` | `0120,07E0` | 0 |
| 19600 (mid entrance ride) | `0140,0370` | `7F00,FFF9` | 1 |
| 19772 (control handed back) | `0140,03AC` | `7F00,FFF9` | 1 |
| 19800 (free play, 28 frames later) | `0125,03AC` | `0139,0301` | 1 |
| 20163, 20400, 20800, 21500 | … | `032C,03B1`, `0426,05F0`, `04B5,053D`, `0C42,03B8` | — |

`$7F00` with `object_control $81` and `Status_InAir` is **`sub_13ECA`** (sonic3k.asm:26800-26810):
`Tails_CPU_idle_timer` and `Tails_CPU_flight_timer` to 0, `Tails_CPU_routine` to 2, then
`x_pos = $7F00`, `y_pos = 0`. It is the CPU sidekick's *despawn*, and routine 2 is the state that
flies him back on screen — which is exactly what row 19800 shows, Tails dropping in from
`y = $0301` above a player standing at `$03AC`.

**Verdict: Tails is not legitimately absent from a `$B01` entry.** He is parked for the duration
of the scripted entrance only, and is back in play 28 frames after control returns. A positioned
act 2 capture skips the entrance entirely, so there is nothing in the ROM that should keep him
out of the `$1A40` corridor. The blocker is ours, and the remaining kill condition — log the
registered sidekick's `x`/`y` on each of the first 60 frames of the capture — is still the next
step, but it is now looking for a bug rather than deciding whether one exists.

## 2026-09-18 — the `$61` gravity puzzle, and what could not be filmed

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `036-gravity-puzzle-320/capture.mp4` | `ff1f6e977` | 320 | `GameplayCaptureTool`, S3K zone 11 act **1**, positioned entry `--x 0x2690 --y 0x07C0`, directly above the one act 1 `$61` placement at `$2690,$0840`; `inputs/036-gravity-puzzle.txt` (40 neutral, 25 Right, 30 neutral, 25 Left, 70 neutral, 40 Right, 55 neutral) | Sonic falls onto the puzzle's `SolidObjectFull2` top, rides the whole sine bob standing on it, walks about on the shaft, then walks off the right edge and falls away | Lands at **frame 36**, `air` 1→0, y=2094. The bob then carries him 2094 → 2107 → 2088 → 2054 → 2018 → **1980** and back, the full `GetSineCosine >> 2` swing, with `y_vel` 0 throughout — he is standing on it, not falling. Leaves the top at **frame 228** (`air` 0→1) at x=9908, just past the box's `$26B3` right face. Lead-in 36 frames, lead-out 57 |

**The launch and the panel markers could not be filmed, and the reason is a blocked corridor,
not the object.** The `$61` placement sits in mid-air inside the `$5F` turbine corridor: the
nearest floor is at y=2348, 236 px below its solid box, so nothing can walk into its side. The
ROM route to it is the corridor's blow, and in the engine that blow **stops dead at x≈`$2636`**
against level terrain, at every steered height:

| Start | Input held | Stops at | Steering |
| --- | --- | --- | --- |
| `0x2500,0x0840` | none | x=9773 (`$262D`), frame 56 | — |
| `0x2500,0x0840` | Up | x=9773, y=2037 | `y_vel` reaches `-584`: the up steering works |
| `0x2500,0x0840` | Down | x=9773, y=2189 | `y_vel` reaches `+609`: the down steering works |

So `$5F`'s steering is confirmed working in the production loop (its unit tests set the input
directly and could not have shown this), and the obstruction is something else. The two `$60`
`Obj_DEZBumperWall` placements at `$2600` (y `$07C0` and `$08C0`) bracket the corridor exactly
where the player jams and are **still placeholders**, which is the first thing to rule in or out.
Until that is resolved, `$61`'s `loc_49850` launch and its six `MHZ_pollen_counter` markers have
no reachable site and stay unfilmed.

Starting the player nearer the puzzle does not work either: at `--x 0x2640` the `$5F` object is
off-screen to the left and never spawns, so the player simply falls to the floor.

## 2026-09-18 — `$A4` `Obj_Spikebonker`, the badnik the act 2 route named

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `037-spikebonker-320/capture.mp4` | `133c984c8` | 320 | `GameplayCaptureTool`, S3K zone 11 act **2**, positioned entry `--x 0x0310 --y 0x0398`, just outside the `$60` detection range of the `$A4` at `$0380,$03B0` subtype `$20`; `inputs/037-spikebonker.txt` (300 neutral) | The mace robot hovering on its `Swing_UpAndDown` beat and patrolling its `subtype * 2` legs above and right of a standing Sonic, mace swinging under it | Sonic is still at x=784 y=1004 on every frame, so everything moving in the picture is the badnik. Frames looked at: 60 (body high, mace out to its left) and 200 (body low, mace beneath it) |

**What this clip is not.** It shows the patrol and the hover, not the slam and not the
destruction. Two attempts at those from a positioned entry failed for reasons worth recording
rather than retrying blind: starting Sonic at `$0350` puts him inside the mace's reach with zero
rings and he is dead by frame 90 (which is itself evidence the `$9A` hurt box is live), and
jumping at the badnik from `$0310` bounces him left off terrain at x≈817 before he reaches it.
The act 2 route is the vehicle for both — it already drives a player into this badnik and
destroys it, which is what moved the frontier from 390 to 472 frames — so the slam and kill
belong in a route-driven capture once one exists, not in another positioned entry.

## Slice 4 — traversal objects and badniks

All three use the same input, `inputs/038-040-neutral300.txt` (300 neutral frames), because each
object acts on its own clock: the player is a stationary witness and everything that moves in the
picture is the object. Setup for all three: `GameplayCaptureTool`, positioned entry (`--x/--y`,
declared capture setup), no seeds of any kind.

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `038-retracting-spring-320.mp4` | `7e301e1b9` | 320 | S3K zone 11 act **2**, `--x 0x04B0 --y 0x0430`, directly above `DEZ2_Sprites` record 8, the `$5D` at `$04B0,$04C0` subtype `$02` | Sonic falls onto the piston, is flung straight back up, comes down and is flung again — two full bounces against the Earth backdrop | **Frame 34** is the launch and it is exact to the ROM: `y` goes 1181 → **1195** (`$04AB`) in one frame, which is `SolidObjectTop_1P`'s landing snap to `$04A3` plus `sub_22F98`'s `addq.w #8,y_pos(a1)`, and `yvel` goes 1176 → **−2560** (`−$A00`), the `word_4808A` word subtype `$02` selects. That is the same `$04AB` / `$F600` pair the native run shows at row 20245. Second launch at **frame 139**, landing between them at **89**. Lead-in 34 frames, lead-out 161. Frames looked at: 33 (standing on the piston, about to be launched) |
| `039-energy-bridge-320.mp4` | `7e301e1b9` | 320 | S3K zone 11 act **2**, `--x 0x0480 --y 0x0370`, above `DEZ2_Sprites` record 6, the `$55` at `$0480,$03E8` subtype `$01` | Sonic lands on the lit bridge, stands on it while its two sparks slide right and wrap, and then the bridge goes out from under him and he falls | Lands at **frame 31** at `y` **971** (`$03CB`, `loc_1E45A`'s new-landing `objY − d3 − y_radius − 1`) and settles to **972** (`$03CC`, `MvSonicOnPtfm`'s riding formula) — the one-pixel step the route's rows 20300/20301 also show. At **frame 94** `air` flips 0 → 1 with `yvel` still **0**: that is `sub_47EE8`'s `bclr Status_OnObj / bset Status_InAir` and nothing else, and gravity only starts on 95. Dies on the fall at 159. Frames looked at: 60 (riding, the two sparks visible to his left) and 100 (sparks gone, falling) |
| `040-chainspike-800.mp4` | `7e301e1b9` | **800** | S3K zone 11 act **1**, `--x 0x2FA0 --y 0x0390`, on the floor left of `DEZ1_Sprites` record 355, the `$A5` at `$3080,$03B8` subtype `$00` | The spike robot charging left out of its rest, decelerating to a stop short of Sonic, waiting, and charging back — twice in 300 frames | Sonic is at x=12192 y=912 on **every** frame with `air` 0, `hurt` 0 and `dead` 0, so everything moving is the badnik. 800 px was chosen deliberately: the charge covers about 153 px and the 320 px half-screen is 160, so at native width any framing that shows the badnik's rest position also puts Sonic inside its reach. Frames looked at: 60 (at rest, four spikes out) and 120 (charged left, nearer) |

**Three things these clips do not show, with the reason.**

1. **The `$5D` piston's extension stroke.** It extends only while Player 1 is a full `$20`
   *below* it (`loc_480D4`, :94116-94117), and all thirteen placements hang over open space, so a
   positioned entry cannot park a player underneath one. A rider is inside the dead band and
   holds it wherever it was. The stroke is asserted frame by frame in
   `TestS3kDezRetractingSpringHeadless`; it has no filmable site.
2. **The `$55` bridge lighting back up.** The capture ends with the fall, because the drop at
   `$0480,$03E8` has nothing under it and the player dies at `y` 1413. Showing the bridge return
   needs a site with a floor below it, or a route that walks off before the window ends.
3. **The `$A5` slam and the hit.** `sub_91E7E` needs a player within `$10` px horizontally, which
   at zero rings is a death, and the act 2 placement at `$0480,$05B0` is below what a positioned
   entry can reach alive — the drop from the energy bridge above it dies at 1413. The route
   already drives a player into one (native row 20389 is the hurt rebound, four rings lost), so
   the hit belongs in a route-driven capture, the same conclusion `037` reached for the
   Spikebonker's slam.

## Slice 4 — the sidekick blocker, closed

`GameplayCaptureTool` could not film a team at a positioned entry, and the reason was in the tool,
not the engine. `state.csv` now carries three more columns — `sk_present,sk_x,sk_y`, read from
`getRegisteredSidekicks()` so a suppressed sidekick still reports a position instead of vanishing
from the log — and they answered the open kill condition on the first run.

**What they showed.** At a Death Egg act 2 positioned entry the seed lands correctly on frame 0
(sidekick at `1168,1076`, one `$20` behind the leader) and the sidekick's own registration puts
him back at the act's **level start**, `288,944` = `$0120,$03B0`, on the very next frame. From
there he walks right at about a pixel a frame, which is why every earlier team capture looked
like a solo one: Tails was real, registered and hundreds of pixels away.

**The fix is two lines.** The seed stopped re-applying after its first success; it now writes for
the whole four-step window, and it runs *after* `loop.step()` rather than before it, so the
position in each frame's state line is the seeded one. Measured after: sidekick at `1168,1072`
from frame 0 and beside the leader for the rest of the run.

| Clip | Commit | Width | Setup | Shows | Evidence in `state.csv` |
| --- | --- | ---: | --- | --- | --- |
| `041-gravity-swap-tails-320.mp4` | `d773b92d7`+ | 320 | S3K zone 11 act **2**, `--sidekick tails`, positioned entry `--x 0x19E0 --y 0x08CC` next to the unflipped `$5B` at `$1A40,$08C0`; `inputs/030-gravity-swap-flip.txt`. **No `--reverse-gravity` seed** — the flag is written by the placed object | Sonic and Tails walk right into the trigger together, gravity reverses, both fall *up*, and both run along the ceiling inverted | Tails is at `1168,1072` on frame 0 and stays beside the leader: `6592,2252` at 0, `6665,2254` at 100, and `7171,2030` at 225 against the leader's `7221,2035` — he goes inverted with him and settles on the ceiling two pixels above. Frames looked at: 240 (both drawn mirrored against the ceiling) |


## 2026-09-22 turbine-room corrections

- `042-turbine-controller-lifetime-320/capture.mp4`: intermediate lifetime-only fix;
  cleared the old freeze but incorrectly passed closed gates. Superseded.
- `043-turbine-puzzle-contacts-320/capture.mp4`: 10 seconds, neutral input, repeated
  airborne puzzle bounces, zero deaths.
- `044-turbine-puzzle-contacts-800/capture.mp4`: 6 seconds at 800 px, real wide
  contact/closed-gate behavior, zero deaths.
- `045-turbine-six-panels-320/capture.mp4`: 20 seconds, positioned `$2500,$840`,
  native Sonic solo, six-panel steering and exit. Input `inputs/045-turbine-six-panels.txt`.
- `046-turbine-six-panels-800/capture.mp4` and `047-turbine-six-panels-800/capture.mp4`:
  controller attempts, **not completed wide routes** despite the directory names.
  Both remain behind the gate. Full decode passes; zero deaths.

All are positioned engine captures, not native parity or cold act routes. The
controller-authoring probe's reported wide completion did not reproduce in the
recorded run, even after adding render calls. Only the actual recordings support
visual claims. The final test checks actual camera width and independently checks
closed-gate bounce at 320/800; the full six-panel controller regression is 320.

- `050-lightning-and-shock-floor-320/capture.mp4`: 300 frames / five seconds, zero deaths, placed lightning visible at frame 90. Positioned at $700,$7A0 with seven rings. `048` immediate-death attempt and `049` off-viewport attempt are not accepted visual evidence.

- `051`–`054` conveyor capture attempts: not accepted footage. State logs show grounded carry at positioned starts; foreground obscures Sonic, or the higher entry lands outside the carry window. No forced priority change was used. Route-based visual follow-up remains open.

- `057-torpedo-launcher-320/capture.mp4`: seven seconds, 420 frames, zero deaths. Positioned $490,$78C with seven rings, held jumps bring the first launcher into view; projectile moves right between frames 125 and 135. `055` drops the launcher above the viewport; `056` short jumps do not raise the camera enough. Neither is firing evidence.

- `058-staircase-rise-320/capture.mp4` and `059-staircase-rise-800/capture.mp4`: positioned $ED0,$610 with seven rings, 360 frames each, zero damage/deaths. Sonic lands, waits and rises on the four-section staircase. Both fully decoded; phase frame 160 inspected. Engine footage, not native parity or a cold route.

- `060-hover-machine-320/capture.mp4` and `061-hover-machine-800/capture.mp4`: six seconds of placed hover-machine lift, neutral input at `$5B8,$890`, seven rings; 360 frames each, no hurt/death. Both full decode and frame 90 inspection passed. Positioned engine evidence only.

- `062-hang-carrier-320/capture.mp4` (480 frames) and `063-hang-carrier-800/capture.mp4` (430): grab, rise to ceiling, finite leftward travel and jump release. Positioned `$801,$894`, 7 rings, input `inputs/062-hang-carrier.txt`. No deaths; 320 clip includes a post-release hazard hit. Full decode and ride-frame inspection passed.

- `067-curved-energy-approach-320/capture.mp4` and `069-curved-energy-approach-800-fixed/capture.mp4`: 504 frames, no damage/deaths; positioned `$700,$910` with seven rings, input `inputs/067-curved-energy-approach.txt`. Lit curve traversed into hanging carrier; all player position/velocity rows agree across widths. Full decode and traversal-frame inspection passed.
- Curve investigations: 064 stationary phase switch, 065 low-momentum partial climb/rollback, 066 off-phase arrival, 068 pre-fix wide early-retirement failure. Do not present these as successful curve traversal.

## Floating platforms / LRZ correction (after 8a58aafbc)

070 is a rejected pre-fix entry: it misses the platform and hits hazards. 071 and 072 start at DEZ2 ($1540,$790) and ride the actual horizontal platform for 420 frames (7 seconds), at 320/800. All player position/velocity rows match, zero hurt/death rows; full decode and frame 120 inspected. 073 shows the corresponding LRZ2 fix at ($F50,$4E0), 420 frames, zero hurt/death rows, full decode and frame 120 inspected. Neutral input, Sonic, no donor or sidekick, seven initial rings. Positioned engine footage, not cold-route or native parity evidence. Per-directory provenance records source hashes.

## Tilting bridge (after 6b7055cea)

074 (320) and 075 (800): DEZ1 actual bridge at ($480,$970), Sonic positioned above its first section at ($410,$930), seven initial rings, neutral input, no donor or sidekick. Both record 480 frames / eight seconds, zero hurt/death rows; all player position/velocity rows match. Full decode, frame-280 tilt and 320 frame-420 floor release inspected. Positioned engine route, not cold traversal or native parity.

- 076/077: initial widescreen background candidates; superseded by final clips below.
- 078-interior-widescreen-final/capture.mp4: Act 1, 800px, one central structure with reflected ROM walls, six seconds, zero hurt/death.
- 079-planet-widescreen-final/capture.mp4: Act 2, 800px, single extended planet curve, six seconds, zero hurt/death.
- 080-background-widths: frame-120 checks at 320/352/400/528 for both acts. Native images match earlier captures exactly. All final outputs validated at f759da908; positioned presentation checks, not cold-route or native parity.

- 081/082 horizontal Act-1 and 083 vertical Act-1: neutral-input attempts encounter nearby hazards; not shared as clean rides.
- 084-conveyor-pad-vertical-controlled/ride-excerpt.mp4: three seconds (frames 0–179) of controlled vertical travel, zero hurt/death in excerpt. Full source later takes damage at 209 and dies at 384. Authored input retained.
- 085-conveyor-pad-act2-horizontal/capture.mp4: five seconds of Act-2 horizontal pad and torpedo hazard, 43 hurt rows, zero death. Full decode and frames 120/240 inspected.
- All conveyor-pad captures validate ffe39535a and demonstrate components, not completed cold routes.

- 086-lift-pad-320 and 087-lift-pad-800: seven seconds each of lift ride, held pause, jump release and return. 420 frames, zero hurt/death, identical player rows across widths. Full decode and phase stills inspected; validated 408b95256. Positioned component checks, not cold-route/native parity.

- 088/089: 900-frame matching circular-tunnel segments at 320/800, no hurt/death; stop just before release.
- 090-light-tunnel-circle-exit-800/capture.mp4: 18 seconds through the circular path and exit, no hurt/death; full decode and circle/exit stills inspected.
- 091-light-tunnel-sine-up-800/traversal-excerpt.mp4: eight seconds through the upward sine path and release, no hurt/death in frames 0–479. Full ten-second source takes a post-release hazard hit at 539, no death. Both decoded. Validated a427d8a03; positioned engine footage, not cold/native parity.

## DEZ miniboss and Act 2 transport — 81768e6ee

093/094: 15-second opening at 320/800, positioned ($3740,$2E0), 20 rings, neutral input; 88 hurt rows, no deaths, matching player states. 098/099: 4000-frame solo controller-driven completion at 800/320; 200 rings and seven Super Emeralds, real collision damage through both eight-hit phases, results, reload, floor collapse and launch to Act 2 landing. No hurt/death/follower rows. 098 includes a fully decoded 42-second defeat-and-transport.mp4 excerpt. Per-directory provenance records source hashes. Engine footage, not cold-route or native parity proof. Results leave the wide screen later; first player divergence is at reload.

092 is a rejected low entry which never crossed the camera gate. 095 is an incomplete stationary attack. 096/097 are rejected roster-mismatched controller replays and do not demonstrate completion, despite directory names. The final 098/099 use the corrected solo setup.

## Gravity boss encounter — 7a324bdd4

100/101: 900-frame neutral opening at 800/320. 102/103: 6830-frame controller runs, recording frames 6250–6829 (last hit, breakup, escape). Declared DEZ2 start ($34B0,$300), 200 rings; defeat runs have seven Super Emeralds and solo authored input. All zero hurt/death. Native and wide player states first differ at 6346, after killing hit 6344; parity unclaimed. 103 loads the incomplete $1700 destination; 102 ends during the fade, with the longer probe confirming the load.


## Incoming DEZ2 → final → DDZ (2026-09-23, b6c1147a2 + campaign edits)

116-incoming-final-through-ddz-320/capture.mp4: final escape combat and real DDZ flight, frames19200..21101. 117-dez2-to-final-handoff-320/capture.mp4: gravity-boss exit and final-arena entry, frames6300..7349. Positioned solo200rings/sevenSuperEmeralds boot, no reseed at either load. Full native input replay no deaths, author CSV exact; eight whole-registry replay spots pass. Both videos fully decoded; selected stills inspected. Provenance/inputs alongside. Not cold act traversal or native parity.

118-incoming-final-through-ddz-800/capture.mp4: wide independently authored incoming chain, frames19200..21108. All20869 author rows match independent replay;21109 total rows, zero deaths/followers. Full decode and stills20582/21050 inspected. Same declared positioned setup and limits as116. Two-width full-registry route test passes.
