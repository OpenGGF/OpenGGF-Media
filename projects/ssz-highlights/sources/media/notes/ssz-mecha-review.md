# Boundary review — 28e7afeef, SSZ Mecha Sonic (act 1)

Reviewer: independent boundary review. Branch `feature/ai-ssz-bring-up`,
worktree `/home/farrell/code/projects/OpenGGF/.worktrees/ai-ssz-bring-up`.
ROM authority: `/home/farrell/code/projects/OpenGGF/docs/skdisasm/sonic3k.asm`
plus `sonic3k.lst` and `sonic3k.constants.asm`.

Files judged: `SszMechaSonicObjectInstance.java`, `SszMechaSonicTrailChild.java`,
the `updateMechaSpawner` branch of `SSZHPZTeleporterObjectInstance.java`,
`TestS3kSszMechaSpawnHeadless.java`. Supporting hunks in `Sonic3kConstants`,
`Sonic3kPlcArtRegistry` and `SszZoneRuntimeState` were read for corroboration.

The deliberately-absent items (`loc_7B81A` beyond `sub_7D35A`, the `loc_7C9BA`
child, `Obj_MechaSonic_Sparks`) are not reported as defects. Two notes below
concern consistency with their absence.

---

## Blocking

### B1. `loc_7B35A`'s `PalLoad_Line1 Pal_SSZGHZMisc` is not implemented

ROM `loc_7B35A` (sonic3k.asm:164230-164240), on both acts:

```
lea   (Pal_SSZGHZMisc).l,a1
jsr   (PalLoad_Line1).l
```

`runInit` (SszMechaSonicObjectInstance.java:382-415) performs the RNG seed, the
box, the position and the song fade, but never loads the palette, and
`S3kPaletteOwners.java` has no Mecha Sonic owner (it has `SSZ_GHZ_BOSS` and
`SSZ_MTZ_BOSS` for the two preceding fights, both of which are exactly this
`PalLoad_Line1` call). Both new `StandaloneArtEntry` rows in
`Sonic3kPlcArtRegistry.java` register on palette line 1
(`ObjSlot_MechaSonic`'s `make_art_tile(ArtTile_MechaSonic,1,1)` and
`ObjDat3_7D402`'s line 1), so Mecha Sonic and his after-images will draw with
whatever line 1 holds when he arrives — in act 1 that is `Pal_SSZMTZOrbs`,
loaded by the immediately preceding MTZ fight.

Correct behaviour: on the boss's init, load `Pal_SSZGHZMisc`
(`word_7D842.data`, sonic3k.asm:167565) into palette line 1 through the
existing `S3kPaletteOwners` mechanism. This is a visible, whole-fight colour
divergence and it is not among the gaps recorded under known bug #42.

---

## Should fix

### S1. The init frame skips `sub_7D312` and `sub_7D2D8`

ROM `Obj_SSZEndBoss` (sonic3k.asm:164162-164172) is unconditional:

```
jsr   SSZEndBoss_Index(pc,d1.w)
lea   sub_7D35A(pc),a4
bsr.w sub_7D312
bsr.w sub_7D2D8
```

`updateBossLogic` (SszMechaSonicObjectInstance.java:369-379) returns early on
the init frame:

```java
if (!initExecuted) { runInit(vIntRunCount); initExecuted = true; return; }
```

so `applyCollisionByte()` does not run for routine 0. `loc_7B308` has just set
`mapping_frame` 2, so the ROM's `sub_7D2D8` writes `byte_7D2FC[2]` = `$09` on
that same frame, while the Java leaves the `$23` that `runInit` assigned at
line 391. One frame of the wrong collision size. (`sub_7D312` is a no-op that
frame because `collision_flags` is non-zero, so only the byte is affected.)

Correct behaviour: run the tail on every frame including the init frame —
i.e. fall through to `applyHitAndFlash(); applyCollisionByte();` instead of
returning.

### S2. On-screen half-height is keyed to `y_radius`, and the `ObjSlot` bytes are mis-cited

`ObjSlot_MechaSonic` (sonic3k.asm:167135-167141) ends `dc.b $20,$20,0,$23`.
`SetUp_ObjAttributesSlotted` (sonic3k.asm:178884-178888) consumes those as
`width_pixels`, `height_pixels`, `mapping_frame`, `collision_flags` — **not**
`y_radius`/`x_radius`. `y_radius` is `$1E` and is never written by that
routine; the ROM only ever sets it at `loc_7B484` (`$1F`) and `loc_7B5E8`
(`$F`).

SszMechaSonicObjectInstance.java:97-99 labels the bytes
"y_radius, x_radius, frame, collision_flags", and line 338
`getOnScreenHalfHeight()` returns the mutable `yRadius`. The ROM's on-screen
extent is `height_pixels`, a constant `$20`, so the Java's cull box shrinks to
`$F` for the whole jump/attack graph.

Correct behaviour: return the fixed `$20` (`height_pixels`) from
`getOnScreenHalfHeight()`, keep `yRadius` for floor checks only, initialise it
to 0 rather than `$20`, and fix the comment. `HALF_WIDTH = $20` happens to be
right (it is `width_pixels`), but for the wrong stated reason.

### S3. `onDefeatStarted` writes state `sub_7D35A` does not write

ROM `sub_7D35A` (sonic3k.asm:167090-167106) writes exactly: the code pointer,
`routine` 0, `$34 = loc_7B858`, `status` bit 6, `clr.b (Update_HUD_timer).w`,
`$2E = $7F`, 100 points, `bclr #7,render_flags(a0)`, and one
`Child6_CreateBossExplosion` child with subtype 4.

SszMechaSonicObjectInstance.java:774-784 additionally sets
`anim.mappingFrame = 0x0E`, `xVel = 0`, `yVel = 0` and clears the trail bit.
None of those appear in `sub_7D35A`, and the method's own javadoc
(lines 763-772) enumerates the routine's writes without them. `mapping_frame`
`$E` in particular is an invented sprite change on the defeat frame; the only
`$E` in this neighbourhood is `cmpi.b #$E,mapping_frame(a1)` at
sonic3k.asm:166051, which belongs to a different child. It also omits
`bclr #7,render_flags` and the `Update_HUD_timer` clear.

Correct behaviour: write only what `sub_7D35A` writes, or state in the comment
which writes are engine bookkeeping and why.

### S4. No test exercises anything past routine 8

`theAttackChoiceIsAFixedEightEntryCycleAndNotARandomDraw`
(TestS3kSszMechaSpawnHeadless.java:230-244) asserts only that two `public
static final int[]` constants hold the values of `byte_7B62E`/`byte_7B636`. It
never boots a level and never calls `onJump`; deleting the entire attack graph
from production would leave it green. The same is true of the first half of
`theCollisionByteIsTheMappingFrameTableAndNotAState` (lines 206-216).

The live cases reach routine 4, 6 and 8 only. Routines `$0A`–`$28` —
`loc_7B484`'s RNG branch, the two landings, both dashes, the ground pound, the
slam-and-backstep chain, the final hop, `loc_7D216`, `MoveSprite_LightGravity`,
`ObjHitFloor_DoRoutine` and the `$F4` callback dispatch — have no coverage at
all. The commit message's "the split that shows the live cases reach
production" is true of the entry only and reads as broader than it is.

Correct behaviour: drive the graph to at least one landing and one of each of
the three `byte_7B636` attacks, asserting ROM literals (`$1F`/`$F` `y_radius`,
`$820`/`-$20`, `$780`, `-$900`, `-$640`, the `$3B` cycle order), before this
counts as a delivered boss under the level-test standard.

### S5. Trail-child coverage omits the two subtype paths the commit says were corrected

`theTrailChildrenStepTheirSubtypesByTwoSoTheRowsLineUp` (lines 278-296) covers
only `ChildObjDat_7D47A`'s pair (subtypes 0 and 2, rows 0 and 1). The
`loc_7C8FE` `addq.b #4` pair from `ChildObjDat_7D486` (subtypes 4 and 6, rows 2
and 3) and `loc_7B70E`'s `move.b #8,subtype(a1)` (row 4) — the paths the commit
message says the RED run corrected — are untested, because nothing reaches
routine `$10` or `$1E`. Rows 2, 3 and 4 of `byte_7D24C` (sonic3k.asm:166946)
are asserted nowhere.

---

## Observations

### O1. Trail child refreshes position after the delete check, ROM refreshes before

ROM `loc_7C91C` (sonic3k.asm:166071-166081) is
`Animate_RawNoSSTMultiDelay`, then `Refresh_ChildPositionAdjusted`, then the
two parent tests. SszMechaSonicTrailChild.java:147-156 animates, then tests the
parent and returns, and only refreshes position when it survives. No visible
effect (the child is not drawn on its delete frame), but the order is inverted.

### O2. `x_vel` is not wrapped to a word where `y_vel` is

`moveSpriteWithGravity` (SszMechaSonicObjectInstance.java:822) wraps with
`(short)`, matching `addi.w #$38,y_vel(a0)`. The three dash accumulators
(`xVel += xAccel` at lines 553, 612, 699) do not, where the ROM's
`add.w d0,x_vel(a0)` is a word add. Unreachable in practice — `loc_7D216`
turns the boss long before `$820 - n*$20` could wrap — but the asymmetry is
a latent hazard if a future change removes the boundary.

### O3. `services().rng()` is null-guarded in `runInit` and not in `onChooseLanding`

Line 387 guards `services().rng() != null`; line 488 calls
`services().rng().nextWord()` unguarded. Either the guard is unnecessary or
line 488 can NPE in the same harness the guard exists for.

### O4. Boss spawn position is the pad's, where `AllocateObject` gives a blank slot

`SSZHPZTeleporterObjectInstance.updateMechaSpawner` constructs the boss with
`new ObjectSpawn(x, y, ...)` at the pad's `($1A40,$670)`. The ROM's plain
`AllocateObject` leaves `x_pos` at 0 until `loc_7B308` runs. `loc_45AB0`'s
`cmp.w x_pos(a0),d0 / bhi` would see 0 (not higher than `$1A40`) and arm the
explosion immediately; the Java sees `$1A40` (also not higher) and does the
same. The two agree only because the boss always initialises before the pad's
first `loc_45AB0` frame in both. Worth a comment, since it is load-bearing.

### O5. `loc_7B39C`'s two extra allocations are absent

ROM `loc_7B39C` (sonic3k.asm:164198-164201) creates the `ChildObjDat_7D474`
(`loc_7C9BA`) child and then tail-jumps `AllocateObject`, consuming a second
slot that is never written. Both are absent here. `loc_7C9BA` is recorded under
known bug #42, but the bare `jmp (AllocateObject).l` is not, and slot order
decides sibling execution and RNG draw order. Consistent with #42's scope, but
name it there.

### O6. `_unkFAB0` is written and never read

`setBossCeilingY` is called from `runInit` and `bossCeilingY()` has no caller.
Correct — act 1's `SSZEndBoss_Index` graph never reads `_unkFAB0` — but worth a
line saying so, since it looks like a dropped consumer.

### O7. Dead helper

`allActive(Class<?>)` at TestS3kSszMechaSpawnHeadless.java:362 is unused.

---

## Claims checked against the ROM

Verified correct:

- **Branch polarity.** `loc_7B544` (`beq` → negate on bit **set**),
  `loc_7B64E` (`bne` → negate on bit **clear** — the ROM really is asymmetric
  with `loc_7B544`, and the Java copies both faithfully), `loc_7B5E8`
  (`bne` → `+$200` on bit set), `loc_7B754` and `loc_7B790`
  (`tst.w x_vel` / `bmi` → keep positive when `x_vel` is negative),
  `loc_7B57A` (`bhs` → bit stays set when `Camera_X+$A0 >= x_pos`),
  `loc_7B3E6` (`blo` → return when `Camera_X-$20 < x_pos`),
  `loc_7B44A` (`bhs`), `loc_7B63A`/`loc_7B804` (`bpl`), `loc_7B6A0`/`loc_7B6EE`
  (`bmi`/`beq` on `d1`), `loc_45AB0` (`bhi`).
- **`loc_7D216`.** `x_vel >= 0` → `_unkFAB6`, `bls` → fire when
  `limit <= x_pos`; `x_vel < 0` → `_unkFAB4`, `bhs` → fire when
  `limit >= x_pos`. Both correct at lines 851-858.
- **`loc_7B484`'s `bclr` polarity.** `bmi` on the random word takes the long
  branch; otherwise `bclr #4,(_unkFAB8).w` and `bne` on the **old** bit.
  `clearCutsceneFlag` returns the old bit and is only called on the positive
  draw. Correct, and the inline comment's reading is right.
- **Camera arithmetic.** `loc_7B308` is three accumulating `addi.w` on X
  (`$20` → `$120` → `$160`) and two on Y (`$30` → `$A0`); `loc_7B41C` is one
  `addi.w #$40`. Constants at lines 104-112 and 123 match exactly.
- **16.16 position and `lsl.l #8`.** `getX()/getY()` are the high word;
  `posX += xVel << 8` matches `ext.l`/`lsl.l #8`/`add.l`.
- **Gravity.** `MoveSprite` is `$38`, `MoveSprite_LightGravity` is `$20`, and
  both read the **old** `y_vel` into the position before adding gravity;
  `moveSpriteWithGravity` (lines 819-825) does the same. Per-routine
  assignment checked for all of `loc_7B3E6`, `7B44A`, `7B4DA`, `7B5AC`,
  `7B63A`, `7B67C`, `7B6A0`, `7B6DA`, `7B6EE`, `7B77E`, `7B7BA`, `7B804`.
- **`clr.w $16(a0)` / `clr.w $12(a0)`.** Per `sonic3k.constants.asm:15-16`
  `x_pos` is `$10` and `y_pos` `$14` as longs, so `$12` and `$16` are the
  sub-pixel words. `posX &= 0xFFFF0000` / `posY &= 0xFFFF0000` are right (this
  is the one place a reviewer would expect `y_radius` at `$1E` to be confused
  with `$16`, and it is not).
- **Order.** Routine → `sub_7D312` → `sub_7D2D8` matches (except S1). The
  within-routine order of `loc_7B308`, `loc_7B41C`, `loc_7B484`, `loc_7B4EC`,
  `loc_7B5C2`, `loc_7B70E`, `loc_7B7EC` matches instruction for instruction,
  including `bset #2,$38` before `CreateChild6_Simple` and the children being
  created before `x_pos` is written.
- **`Obj_Wait` twice in a frame.** `loc_7B478`/`loc_7B748` are
  `jsr Animate_RawMultiDelay` then `jmp (Obj_Wait)`, and
  `Animate_RawMultiDelay`'s `$F4` command (`loc_84600`) calls `$34` via a
  `jsr`-reachable `jmp`, so the ROM itself can run `$34` twice in one frame and
  re-reads `$34` each time. The Java reproduces this exactly (`animate()` then
  `objWait()`, both routed through `runCallback()` reading the live field).
  Not a defect.
- **`Set_Raw_Animation` vs bare `move.l`.** Only `loc_7B5E8` uses
  `Set_Raw_Animation`; `setRawAnimation` is used there and nowhere else.
  `loc_7B484` and `loc_7B4EC` clear both counters explicitly before the bare
  write, and the Java does too.
- **Child tables.** `ChildObjDat_7D47A` is `dc.w 1`, which `dbf` runs **twice**
  — the Java and the test both get this right. `_7D480` is `dc.w 1-1` (one) and
  `_7D486` is `dc.w 2-1` (two). `CreateChild6_Simple`'s `addq.w #2,d2` against
  `sub_7D236`'s `add.w d0,d0` on four-byte rows: subtypes 0/2/4/6/8 map to rows
  0-4 with no overlap. `byte_7D24C`'s five rows transcribe correctly into
  `CHILD_TABLE`, including the two `dc.w $300` priorities.
  `Refresh_ChildPositionAdjusted` negates `child_dx` on the **parent's**
  `render_flags` bit 0; the Java matches.
- **`byte_7D2FC`.** All 22 bytes transcribe correctly; `$86` at 3-6, `$00` at
  `$F`. `sub_7D2D8`'s `btst #6,status` skip and `$38` bit 7 `ori #$80` both
  modelled.
- **Art addresses.** `sonic3k.lst` confirms `ArtUnc_MechaSonic` `$175A9E`,
  `ArtKosM_MechaSonicExtra` `$17F738`, `Map_MechaSonic` `$1853AA`,
  `Map_MechaSonicExtra` `$18561E`, `DPLC_MechaSonic` `$185852`.
  `$175A9E + $56E0 = $17B17E` matches the next label. `DPLCPtr_MechaSonic` is
  at `$7D4D6` and `DPLC_MechaSonic` has 22 frame entries, agreeing with
  `byte_7D2FC`'s length.
- **Animation script addresses.** `byte_7D4DE`, `_7D4EF`, `_7D523`, `_7D541`,
  `_7D54A`, `_7D596`, `_7D59B`, `_7D5A2`, `_7D65F` all match their use sites.
  The `$7D4D0` block start over-reads `ChildObjDat_7D4D0`/`DPLCPtr_MechaSonic`
  by 14 bytes, which is harmless; `$1C0` covers `byte_7D65F`.
- **RNG.** `Random_Number` appears exactly once in `Obj_SSZEndBoss`'s graph, at
  `loc_7B484`. `loc_7B2DC`'s seed is
  `move.l (V_int_run_count).w,(RNG_seed).w`, and `runInit` takes
  `vIntRunCount` — the right clock.
- **The pad.** `loc_45A72`'s `$32` countdown, `loc_45A84`'s
  `Camera_Y_pos == Camera_max_Y_pos` gate with no player test, the plain
  `AllocateObject`, `move.w a1,(_unkFAA4).w` **and** `$30(a0)`, `st $2E(a0)`,
  and `loc_45AB0`'s `$20` frames plus explosion child — all match.
- **Rewind.** `SszZoneRuntimeState`'s `CAPTURE_BYTES` grew by three shorts and
  all three are written and read in the right order. The boss and child extras
  cover every mutable field I could find.

Claim **not** supported by the ROM:

- Commit message: "Set_Raw_Animation clears anim_frame and anim_frame_timer
  where a bare move.l #script,$30(a0) does not, **which is four of this
  graph's five script changes**." The act-1 graph has eight `$30(a0)` writes —
  `loc_7B41C`, `loc_7B484`, `loc_7B4CA`, `loc_7B4EC`, `loc_7B520`,
  `loc_7B57A`, `loc_7B5C2` bare, and `loc_7B5E8` via `Set_Raw_Animation` —
  plus two more from the `$F8` script command in `byte_7D4DE` and
  `byte_7D54A`. The distinction drawn is correct; the count is not. The code
  itself is right, so this is a commit-message defect only.

## Routines checked

Read line by line and compared against the Java: `Obj_SSZEndBoss`,
`SSZEndBoss_Index`, `loc_7B2DC`, `loc_7B308`, `loc_7B35A`, `loc_7B39C`,
`loc_7B3E6`, `loc_7B41C`, `loc_7B44A`, `loc_7B462`, `loc_7B484`, `loc_7B4CA`,
`loc_7B4DA`, `loc_7B4EC`, `loc_7B520`, `loc_7B53E`, `loc_7B544`, `loc_7B57A`,
`loc_7B5AC`, `loc_7B5C2`, `loc_7B5E8`, `byte_7B62E`, `byte_7B636`,
`loc_7B63A`, `loc_7B64E`, `loc_7B67C`, `loc_7B698`, `loc_7B6A0`, `loc_7B6C0`,
`loc_7B6DA`, `loc_7B6EE`, `loc_7B70E`, `loc_7B748`, `loc_7B754`, `loc_7B77E`,
`loc_7B790`, `loc_7B7BA`, `loc_7B7D6`, `loc_7B7EC`, `loc_7B804`, `sub_7D2D8`,
`byte_7D2FC`, `sub_7D312`, `sub_7D35A`, `loc_7D216`, `sub_7D236`,
`byte_7D24C`, `ObjSlot_MechaSonic`, `SetUp_ObjAttributesSlotted`,
`CreateChild6_Simple`, `loc_7C8FE`, `loc_7C902`, `loc_7C91C`,
`Refresh_ChildPositionAdjusted`, `MoveSprite`, `MoveSprite2`,
`MoveSprite_LightGravity`, `Obj_Wait`, `ObjHitFloor_DoRoutine`,
`Set_Raw_Animation`, `Animate_RawMultiDelay` (including `off_845D8`,
`loc_845E4`, `loc_845F2`, `loc_84600`), `loc_45A66`, `loc_45A72`, `loc_45A84`,
`loc_45AB0`, `ChildObjDat_7D474/_7D47A/_7D480/_7D486`, and the animation
scripts `byte_7D4DE` through `byte_7D5A2`.

Not reached:

- `loc_7B3AC` (act 2 only; the Java has no `case 2`, correct for this scope).
- `loc_7B81A`'s graph, `loc_7C9BA`, `Obj_MechaSonic_Sparks` — excluded by the
  brief.
- `AbstractBossInstance`'s touch/hit ordering, so the **phase** of the
  `$20`-frame window relative to `sub_7D312`'s same-frame `subq.b #1` is
  unverified. `getInvulnerabilityDuration()` returns `$20`, which is right;
  whether the first decrement lands on the hit frame as it does in the ROM
  I could not confirm without reading the base class's update order.
- `ObjectTerrainUtils.checkFloorDist` fidelity to `ObjCheckFloorDist`
  (pre-existing shared code).
- `S3kRawAnimation.animateMultiDelay` is pre-existing; I read it far enough to
  confirm the `$F8` target is `script + signed byte` (matching
  `lea (a1,d1.w),a1`) and that `anim_frame` is cleared after the `$F4`
  callback. It also sets `anim_frame_timer = 0` before the callback where the
  ROM leaves the wrapped value; both reach the same next-frame outcome.
- `Perform_DPLC` / `StandaloneArtEntry` plumbing, the rewind guard and
  coverage-baseline files, `CHANGELOG.0.7.md` and the plan/validation docs.
- Nothing was built or run; this is a static review.
