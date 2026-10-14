# Sky Sanctuary bring-up media

Highlights reel: `reel/ssz-bring-up-highlights.mp4` (125.83 s, 1920x1080/60, silent, 16 chapters with animated title cards).
Rebuild with `python3 reel/build_reel.py`; the edit list and chapter map are beside it.

Captures from `GameplayCaptureTool` on the production path
(`HeadlessGameBoot` + `GameLoop.step()`), Sonic at 320 unless a row says otherwise, entered
through `--star-post` so the positioned start is not overridden by the arrival script. Clips are
encoded by `make_clip.sh` at 60 fps, 3x nearest-neighbour, with at least 30 frames of lead-in and
lead-out. Raw directories are never overwritten once a clip is cut from them.

| Clip | Raw | Feature | Frame to look at |
| --- | --- | --- | --- |
| `01-ssz-arrival-beam-sonic-tails.mp4` | `raw-01-arrival-sonic-tails` | The teleporter arrival and Tails' own beam | — |
| `02a-ssz-knuckles-beam-and-death-egg.mp4` | `raw-02-knuckles-cutscene-bridge` | Cutscene Knuckles' beam and the Death Egg rising | — |
| `02b-ssz-bridge-releases-the-route.mp4` | `raw-03-knuckles-cutscene-bridge-walk` | The button, the bridge and the walk across it | — |
| `04a/04b-ssz-sky-and-roaming-clouds-*.mp4` | `raw-04`, `raw-05` | The act-1 sky, its oscillator and the five roaming clouds, at 320 and 800 | — |
| `05-ssz-cloud-band-before-after.mp4` | `raw-06-ssz1-cloud-window-after` | The cloud band, before and after the `$1C00` window fix | — |
| `06-ssz-floating-platform-dips.mp4` | `raw-07-ssz-floating-platform` | `$7F` dipping under a standing player | — |
| `07-ssz-column-breaks-into-eight.mp4` | `raw-08-ssz-collapsing-column` | `$7E` breaking into its eight `word_46618` pieces | — |
| `08-ssz-teleporter-pad-launch.mp4` | `raw-09-ssz-teleporter-pad-launch` | `$79` charging and launching | — |
| `09-ssz-diagonal-walkway-collapses.mp4` | `raw-10-ssz-diagonal-walkway` | `$7B` sliding along its own slope as it goes | 75 |
| `10-ssz-bouncy-cloud-throws-the-player.mp4` | `raw-11-ssz-bouncy-cloud` | `$7D` squashing under Sonic and throwing him with the four `word_466C8` puffs | 68 |
| `11-ssz-elevator-bar-catches-and-swings.mp4` | `raw-12-ssz-elevator-bar` | `$7A` catching Sonic from above and hanging him on its swing (mapping frame `$E5`) | 120 |
| `12-ssz-rotating-post-spins-the-player.mp4` | `raw-13-ssz-rotating-platform` | `$76` holding Sonic on top and walking him through `byte_468C4`'s twelve poses | 200 |
| `13-ssz-swinging-carrier-arc.mp4` | `raw-14-ssz-swinging-carrier` | `$75`'s jointed arc, drawn from its `(subtype & 3) + 6` segments | 200 |
| `14-ssz-retracting-spring-extends.mp4` | `raw-15-ssz-retracting-spring` | `$74` folded flat, extending as Sonic enters its `$60` box, folding away as he leaves | 78, 85, 95 |
| `15-ssz-eggrobo-releases-and-converts.mp4` | `raw-23-ssz-eggrobo-releaser` | `$A0:$04` letting animals go as a harmless invisible marker, then taking `ObjDat3_919A6` and becoming a robot that hurts | 30, 66, 74 |
| `16-ssz-death-restarts-at-the-star-post.mp4` | `raw-27-ssz-death-and-restart` | A death in act 1 and the restart at the declared star post, with the act's flags rebuilt from scratch | 77, 150, 220 |
| `17-ssz-green-hill-recreation-ball-and-chain.mp4` | `raw-28-ssz-ghz-boss` | The Green Hill arena closing, `Obj_SSZGHZBoss` dropping in, and its six-link ball and chain paying out and sweeping | 330, 420, 600, 900 |
| `18-ssz-green-hill-ball-and-chain-hurts.mp4` | `raw-29-ssz-ghz-ball-hurts` | The same fight after the slice-5 review: the ball carries `ObjDat3_7A678`'s `$8F` box for the whole swing and kills a standing player. Filmed with `--star-post --x 0x200 --y 0x7C8`, which is the only way a positioned capture of this arena works — see Owed below | 150, 250, 330, **361** (the ball on top of Sonic, the frame he is hit), 400 |
| `19-ssz-metropolis-orb-ring.mp4` | `raw-31-ssz-mtz-fight` | The upper arena closing, `Obj_SSZMTZBoss` descending from `($1700,$300)` with the Mecha Sonic head on it, and its seven-orb ring turning around it — orbs passing in front of the ship and behind it as `sub_7AF5A` re-sorts them. At 318 an orbiting orb kills a ring-less Sonic: `loc_7ADB2` gives every orb `collision_flags $87`, a `Touch_ChkHurt` byte, so the ring hurts whether the player is attacking or not. Filmed with `--star-post --x 0x1700 --y 0x420` | 215 (the ship and its ring entering), 260 (the ring turning), **318** (the orb on Sonic, the frame he is killed) |
| `20-ssz-metropolis-orb-launched-by-a-hit.mp4` | `raw-34-ssz-mtz-chase` | The first hits of the Metropolis fight. `sub_7AC06` arms the `$20` window, the ship sets `$39(a0)`, and the first orb to update takes it and leaves the ring — `loc_7AE22`'s `y_vel -$400` with the `+/-$80` horizontal term clamped inside `[$16A0,$1760)`. It keeps `loc_7ADB2`'s `$87` for its `$3C`-frame delay, opening out of the ring's grey sphere through the launch animation's frames 2 to 8 as it goes, then `loc_7AFA4` writes `$C6`, it falls to the `$42C` floor and bounces. Filmed with `--star-post --x 0x1700 --y 0x420 --rings 355` | 417 (the orb leaving the ring at the clamp edge), 441 (opened, mid-arc), 490 (on the arena floor), 706 |
| `21-ssz-metropolis-laser-pass.mp4` | `raw-35-ssz-mtz-laser` | The laser pass, which runs exactly once in the fight: `collision_property 8` against `$3C = 7` means the seventh hit spends the last arm cycle and `loc_7AA02` writes `$26 = $E`. `sub_7AB56` then fires `ChildObjDat_7AB80`'s pair three times, `$1E` frames apart, the trailing shot held eight frames on the nose before `loc_7ABCE` gives it `x_vel -$400`. Same input as `raw-34` up to frame 1720, then the player stops attacking and backs off so an eighth hit does not end the fight first | 1745 (the first pair leaving the nose), 1800 (two shots crossing the arena together), 1855 |
| `22-ssz-metropolis-defeat-and-gated-pad.mp4` | `raw-34-ssz-mtz-chase` | The eighth hit at frame 1737, the `$64` of score, the ship leaving to the right, and then the `$79:$F6` pad the defeat ungates: the leader stands on it at 2113, `loc_456F4` draws him in and lifts him 1 px every other tick from 2195, and at 2257 the launch proper takes him 929 px up out of the arena at 16 px a frame, `min_Y -$100` / `max_Y $1000` and the camera wrapping past zero behind him. The pad's own `$20` of rise is over before the leader reaches it and is not what this clip shows | 1737 (the killing hit), 2205 (the charge lifting him), 2260 (the launch), 2369 (the top, `y $51`) |
| `23-ssz-mecha-sonic-entry-and-attacks.mp4` | `raw-38-ssz-mecha-line1` | Mecha Sonic, the act's third fight. The `$79` pad at `($1A40,$670)` allocates him once the final arena's lock has eased the camera to `$5C0`; he comes in from the right as a spinning ball at eight pixels a frame (`loc_7B308`'s `x_vel -$800`), runs clean off the left, waits `$3F` frames and comes back along the top at four (`loc_7B41C`), then drops to the floor and works through `byte_7B62E`'s cycle of dashes, jumps and ground pounds. Which of his frames hurt and which can be hit changes with the animation, from `byte_7D2FC`. Filmed with `--star-post --x 0x1A40 --y 0x670 --rings 355` | 200 (the entry), 268 (an orbiting pass hurting Sonic), 330 (the return along the top), 430 (on the floor), 560 (a ground dash) |

## Owed

- **Closed: the Metropolis fight is filmed.** `19` stopped at the orb that killed a ring-less
  Sonic. `--rings`, ported from the Lava Reef campaign's `b35f59d33`, seeds the count a route
  carried in, and clips `20`, `21` and `22` are the whole fight from the first hit to the pad
  launch. Two things a later capture of this arena should reuse. The leader must not be standing
  under `$1700` while the ship descends: at `DESCENT_FLOOR_Y $420` the ring sweeps below the
  `$42C` floor and the first hurt spends the entire seeded bank, since a hurt zeroes it and the
  scattered rings are mostly not recovered. And the fight ends too fast to film the laser pass in
  the same run — the eighth hit lands within about 30 frames of the seventh, so `21` is a
  deliberate branch of `raw-34`'s input at frame 1720 that stops attacking for 240 frames.

- **Mecha Sonic's defeat is not on film, because it is not implemented.** Clip `23` is his entry
  and his attack loop; `loc_7B81A`'s post-defeat graph is stage 2 of slice 7 and is recorded as
  known bug #42. The `$79` pad's own explosion is driven by `TestS3kSszMechaSpawnHeadless` and is
  not visible in `23` either — at this camera the pad sits where the green column meets the floor.

- **Two earlier Mecha captures are kept as the before pictures.** `raw-36-ssz-mecha-fight` has him
  drawn in the level's own line 1 (he reads orange) because `loc_7B35A`'s
  `PalLoad_Line1 Pal_SSZGHZMisc` was missing; `raw-37-ssz-mecha-palette` has the palette loaded but
  the draw still forcing line 0. `raw-38` is the first with both right.

- **The arm-raise cycles are still not called out in a clip.** They are in `22`'s lead-in and in
  `20`, but no clip is cut to the `$68` arm extension itself, and nothing on film distinguishes
  the raised ring from the resting one. `TestS3kSszMtzArenaHeadless` covers it.


- **A positioned capture of Sky Sanctuary act 1 needs `--star-post`, not `--x/--y`.** Recorded here
  because two attempts were wasted on it. `--x 0x200 --y 0x7C8` and `--y 0x860` both drop the
  leader through the arena floor and settle it at `($100,$C4C)`: `SSZ1_ScreenInit` runs a scripted
  intro on the no-star-post path that overrides the teleport outright, and `Obj_57C1E` then writes
  Player 1 to `Camera_Y + $65`. `GameplayCaptureSession` says so in the comment on its `starPost`
  branch. With `--star-post` the leader settles on the arena floor at `$86C` — the same place the
  native rows and `TestS3kSszGhzArenaHeadless` put it — and both boss gates fire.

- **`$A0` EggRobo fly-by and fighter in one shot.** Clip `15` shows the animal releaser, not the
  nibble-0/nibble-2 pairing. The pairing is covered by tests; what is not filmed is the two objects
  together. Measured obstacle: the fly-by descends only about `$1A` px before turning upward, and
  every nibble-2 partner hovers at a Y that is off the top of the screen from the ledge the player
  has to stand on to load it (group 6 measured: objects at `$C80`, player `$CEC`, camera `$C8C`).
  Raws `raw-17`, `raw-19`, `raw-20` (group 6), `raw-18` (group 1) and `raw-21` (group 4) are the
  attempts. Next: a one-frame right tap on the `$7B` walkway at `($15D0,$CEC)` so the fighter's
  load window opens before the player steps off the ledge.

- **Known bug #41 before/after.** Owed at a camera where a background column actually carries
  structure: background row 13, columns 17-22, i.e. camera X around `$858`-`$B58` with wrapped
  camera Y around `$520`-`$59F`. The `$7B` walkway camera is not that place — the cartridge shows
  flat sky there too.

## 2026-09-22 campaign refresh

- `raw-39-mecha-trail-restored/capture.mp4`: ca23d7413, 900 frames/15 seconds, native Sonic solo at a declared final-pad checkpoint with 355 rings. Correct four-frame dash art/palette/high priority. State CSV, input and provenance beside video. Frame 58 shows the small streaks at Mecha’s feet. Full decode verified. Entry/attack loop only; results and launch footage remain owed.
- The historical claim above that Mecha defeat is unimplemented is superseded by the branch merge and `1f12b2eb0`: defeat now allocates production results and the results reaches the end flag. The launch is still open.


## 24 — Mecha results, collapse, spiral and Death Egg entry (2026-09-22)

[32-second launch excerpt](24-ssz-collapse-spiral-to-dez.mp4), frames 2500–4439
of [the continuous 80-second run](raw-40-mecha-launch-hyper/capture.mp4).
Native Sonic solo, 320px, donor off; declared star-post `$1A40,$670`, 355 rings,
Super Emerald array `3333333`. Hyper is activated through controller input.
The recorded input clears Mecha, real results trigger the launch, and DEZ1
loads (first destination camera row 4223). No deaths across 4800 frames.
Input, state CSV and provenance are beside the full capture. Both videos
passed complete ffmpeg decoding; the excerpt contains 1940 frames at 960x672.
Frames 3300/3500 show spiral depth ordering; 4000 shows foreground Death Egg;
4700 shows DEZ1. This is checkpoint-route/visual evidence, not a cold full-act
or strict native-parity claim. The intermediate render without the Death Egg
was replaced after correcting column scroll values from absolute to deltas.

- `raw-41-mtz-defeat-explosions/capture.mp4`: refreshed 12-second Metropolis defeat and exit-pad capture, source frames 1680–2399. Same declared checkpoint/rings/input as raw-34, now with ROM explosion artwork. Frame 1770 shows the bursts; zero deaths over 2400 stepped frames. Full decode passed. See local provenance JSON for source hashes.

- `raw-42-mecha-defeat-sparks/capture.mp4`: 1000 frames (16.67 seconds), source 1600–2599, Mecha defeat palette/sparks through results. Declared Hyper checkpoint setup from raw-40; zero deaths over 2600 steps. Frame 1805 shows the flash and spark. Full decoding passed; source hashes in provenance.

- `25-mecha-defeat-sparks-and-dez-launch.mp4`: updated 49-second excerpt from raw-43 (source 1500–4439), showing defeat palette/sparks, results, collapse, spiral, jump and DEZ1 after the secondary collision owner was added. Full source is 4800 frames, zero deaths; destination at 4223. Same declared Hyper checkpoint setup. Both source and excerpt passed decoding.

- 2026-09-23 arrival palette/missile progress: [320](campaign-20260923-arrival-missiles-320/capture.mp4), [800](campaign-20260923-arrival-missiles-800/capture.mp4). 1500 input-driven frames; film300..1499; no hurt/death; full decode verified. Cloud/mask/trail children still omitted. Exact command and hashes in each provenance.json.

- 2026-09-24 initial Death Egg children: [320](campaign-20260924-arrival-children-320/capture.mp4), [800](campaign-20260924-arrival-children-800/capture.mp4). Replaces the incomplete-child arrival clips. 1500 input-driven frames, zero hurt/death, full decode verified. Native observations: native-arrival-20260924/run2; comparison.json identifies corrected accumulator source and verified landing/palette/timers.

- 2026-09-24 cold staircase fix: [320](campaign-20260924-cold-staircase-320/capture.mp4), [800](campaign-20260924-cold-staircase-800/capture.mp4). Cold2779frames, film2480..2778. Both0deaths;320has34hurt rows and800zero. Inputs saved in the task tree; full decode and still2750 reviewed. Not full-act completion.

- 2026-09-24 cold first replica arena: [320](campaign-20260924-cold-ghz-320/capture.mp4), [800 comparison](campaign-20260924-cold-ghz-800/capture.mp4). 4473 cold input frames; film2779..4472. Native320 reaches arena/boss creation,37rings,0deaths. Wide stays alive but stops earlier at(2047,2540); not wide completion. Both fully decode. Production test checks four full-registry replay boundaries.

- 2026-09-24 cold first replica defeat and transport: [320](campaign-20260924-cold-first-replica-320/capture.mp4). 5827 cold steps, film4473..5826,0deaths/120hurt rows. Defeats GHZ replica and reaches upper pad(512,1420),0rings. Six full-registry replay checks and15focused tests pass. Full decode and frames5100/5600 reviewed. Not full-act or wide completion.

- 2026-09-24 restored Eggmobiles: [GHZ320](campaign-20260924-ghz-eggmobile-320/capture.mp4), [GHZ800](campaign-20260924-ghz-eggmobile-800/capture.mp4), [MTZ320](campaign-20260924-mtz-eggmobile-320/capture.mp4), [MTZ800](campaign-20260924-mtz-eggmobile-800/capture.mp4). Positioned checkpoint,40rings,450steps,film150..449. All decode,0deaths,frame250 reviewed. Corrects missing body registration; old head-only films are not visual acceptance.
- `campaign-20260924-cold-middle-320` is superseded: the input relied on a prematurely culled swinging bar. Current input follows the restored bar and upper walkway; see carrier-fix-320.

- 2026-09-24 [corrected carrier route](campaign-20260924-carrier-fix-320/capture.mp4):7912cold steps,film5827..7911,0deaths,25rings at(5045,1196). Full decode passes; frame7076 shows the preserved rider bar. Supersedes the lower-path middle clip.
