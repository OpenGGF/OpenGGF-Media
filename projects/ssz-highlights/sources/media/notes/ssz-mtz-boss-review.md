# Review: `Obj_SSZMTZBoss` port (SSZ act 1 Metropolis recreation)

Worktree `/home/farrell/code/projects/OpenGGF/.worktrees/ai-ssz-bring-up`, reviewed against
`/home/farrell/code/projects/OpenGGF/docs/skdisasm/sonic3k.asm`. Read-only review; nothing
was built or run.

## Verdict

The engine side is unusually good. I re-derived `sub_7AEB0` instruction by instruction and the
port has it right, including the two things most likely to be wrong: which `GetSineCosine` output
is used at each of the three lookups (sine every time for the x and y terms, cosine of `$2E` only
for the depth), and the `move.w d0,d5` low-word truncation of each `muls.w`. `sub_7AF5A`'s four
buckets, `loc_7ADA2`'s seven-not-eight orbs, `sub_7AC06`'s `$1F` frame accounting, the
`bset #6 / beq` two-turn rule, `loc_7AFA4`'s net `+$18` gravity and `$180` clamp, `loc_7B02A`'s
`neg` before `asr`, the `$11 -> $F` collision-size change, the `$87 / $C6 / $DA` bytes and the
64 + 120 frame escape all check out. The problems are in the test and in the prose. Two of them
are blocking: one assertion contradicts the port's own correct recoil model and must fail, and
the one test that claims to nail down the depth sort is a tautology that recomputes the production
branch from the production output and so cannot disagree with it. Fix those two, tighten the four
SHOULD FIX items, and this is landable.

## Findings

1. **BLOCKING — the laser-interval assertion contradicts the recoil, and must fail.**
   `src/test/java/com/openggf/tests/TestS3kSszMtzArenaHeadless.java:505-509` asserts consecutive
   shots are `LASER_INTERVAL` (`$1E` = 30) frames apart. `loc_7AA44` (sonic3k.asm:163340-163344)
   is `tst.b $33(a0) / beq.s loc_7AA52 / subq.b #1,$33(a0) / bra.w loc_7A8E4` — while the
   `move.b #$10,$33(a0)` recoil runs, the whole `off_7AA60` dispatch is skipped, so `sub_7AB56`'s
   `subi.w #1,(SSZ_MTZ_boss_laser_timer).w` does **not** tick. The real gap is `$10 + $1E` = 46
   frames. The port models this correctly
   (`SszMtzBossObjectInstance.java:637-640` returns before the `laserState` switch), so the port
   is right and the expectation is wrong. As written the test either fails on this assertion or —
   if the shots do not clear the camera inside the wider gap so `seen` never returns to 0 — fails
   earlier on `assertEquals(LASER_SHOTS, firedOnFrame.size())` at line 502. Expect
   `LASER_RECOIL_FRAMES + LASER_INTERVAL`.

2. **BLOCKING — `theOrbRingSortsItselfFrontAndBackFromTheCosineOfItsAngle` cannot disagree.**
   `TestS3kSszMtzArenaHeadless.java:320-336` computes `expectedPriority` and `expectedFrame` from
   `orb.depthForTest()` using the same `depth >= 0` / `depth < DEPTH_BAND` / `depth >= -DEPTH_BAND`
   branch structure and the same `PRIORITY_*` constants that `SszMtzBossOrbChild.sortByDepth()`
   (`SszMtzBossOrbChild.java:337-355`) uses. Invert a sign, swap two buckets or swap `$80` and
   `$380` in production and the expectation moves with it. The test's own javadoc (line 294) says
   "it is asserted as the exact table" — it is not; the table is re-derived in the test from the
   production value. `sub_7AF5A` (sonic3k.asm:163836-163862) is a literal table and should be
   asserted as one: drive an orb to a known `$2E`, assert the ROM depth value, then assert
   `mapping_frame 0 / priority $80` for `d0 >= $C`, `1 / $100` for `0 <= d0 < $C`, `1 / $300` for
   `-$C <= d0 < 0`, `2 / $380` for `d0 < -$C`, each as a literal. The `sawFront && sawBack` and
   `mixedAtOnce` checks below it are fine but only prove the ring turns.

3. **SHOULD FIX — the orb javadoc contradicts its own code and the ROM on the launch delay.**
   `SszMtzBossOrbChild.java:52` says the orb leaves with "no collision at all for `$3C` frames".
   `loc_7ADB2` writes `move.b #$87,collision_flags(a1)` (sonic3k.asm:163697), `loc_7AE22` never
   touches it, and `loc_7AFA4` only writes `$C6` once the countdown goes negative — so a launched
   orb is `$87`, i.e. `Touch_ChkHurt` harmful, for all 61 delay frames, and `$C6` (poppable) only
   afterwards. The code at `SszMtzBossOrbChild.java:168` and `:359-361` is correct; the prose is
   not, and it is exactly the kind of comment that gets "fixed" into a real bug later.

4. **SHOULD FIX — `loc_7AC4A` is dropped on a false justification.**
   `SszMtzBossObjectInstance.java:170-175` says `sub_7AC06` "rewrites `2(a1)` — the high byte of
   `_unkFA84` — on a hit and on a player death; nothing in this engine reads that byte". With
   `a1 = _unkFA82`, `2(a1)` **is** `_unkFA84`, and this engine does model that word:
   `SszZoneRuntimeState.backgroundCameraDelta()`, whose own javadoc cites `loc_6607E`, and which
   `MoveSprite_SSZBGAdjust` reads with `move.w (_unkFA84).w,d0 / add.w d0,x_pos(a0)`
   (sonic3k.asm:134357). `loc_7A7C4`'s third byte (`move.b #3,(a2)+`) seeds `_unkFA84 = $0300`
   and is also dropped. The drop is probably safe, because `loc_6607E` (sonic3k.asm:134393)
   rewrites `_unkFA84` from the camera delta every frame — but that is the reason to write down.
   The stated one is false, which under invariant 2/3 is worse than the omission.

5. **SHOULD FIX — the orb's `index` is captured for rewind but cannot be restored.**
   `SszMtzBossOrbChild.java:146` declares `private final int index`, it is put into `RewindExtra`
   (`:198-205`, `:212`), and `restoreRewindState` (`:218-248`) never assigns it — it cannot, the
   field is final. `recreateForRewind` (`:194-196`) always constructs with index 0. After a
   recreate all seven orbs report `indexForTest() == 0`, which is what the sort test reads at
   `TestS3kSszMtzArenaHeadless.java:303-306` to check the `byte_7AE14` seeding. Either drop
   `index` from the extra (the angles it seeds are separately captured, so nothing else needs it)
   or make the field non-final and restore it.

6. **SHOULD FIX — the `bset #6,$2E(a0) / beq` two-turn rule has no test.**
   `loc_7A874` (sonic3k.asm:163171-163177) is the subtlest branch in the object: `bset` sets Z
   from the *old* bit, so the first turn takes `beq.s loc_7A8DA` and only the second advances
   `$26` and arms `y_vel -$100`. `markTurn()` (`SszMtzBossObjectInstance.java:530-534`) has it
   right, but `thePatrolTurnsAtItsTwoLimitsAndHoversFourPixels`
   (`TestS3kSszMtzArenaHeadless.java:258-288`) breaks out of its loop the moment the phase changes
   and never counts reversals. A port that advanced on the first turn passes every test in this
   file. Assert: exactly two direction reversals before `STATE_PATROL -> STATE_RISE`, and that the
   phase is still `STATE_PATROL` immediately after the first one.

7. **NOTE — the launch animation is a frame early, and the launch frame's mapping frame is wrong.**
   ROM never calls `Animate_Sprite` on the launch frame (`loc_7AE22` ends at `loc_7AE9C`); the
   first call is on launch+1, where `anim != next_anim` zeroes `anim_frame_duration`, the
   `subq.b #1` makes it negative and `byte_7B233`'s leading `dc.b 3` is loaded with frame 2. Each
   script entry therefore holds four frames starting at launch+1. `SszMtzBossOrbChild.java:273-275`
   pre-seeds `animStep = 0 / animTimer = 3 / mappingFrame = 2` on the launch frame itself — where
   `sortByDepth()` then overwrites `mappingFrame` with the depth frame — and `animateLaunch()`
   decrements from launch+1, so every entry lands one frame early and `BOUNCE_GATE_FRAME` (frame
   8, the `cmpi.b #8,mapping_frame(a0)` gate in `loc_7B02A`) is reached a frame early too.

8. **NOTE — `Load_PLC` is never issued at either end.** `FIGHT_PLC = 0x7B` and `LEVEL_PLC = 0x32`
   (`SszMtzBossObjectInstance.java:148-149`) are declared and unused; `loc_7A6DC`'s
   `moveq #$7B,d0 / Load_PLC` and `loc_7ACA4`'s `moveq #$32,d0` have no counterpart. The reviewed
   `SszGhzBossObjectInstance.java:112-120` carries the same gap *with* a javadoc explaining that
   the engine has no runtime decompression queue and registers sheets at level load instead. Copy
   that explanation onto these two constants.

9. **NOTE — `Child6_CreateBossExplosion` (subtype 4) is not spawned.** `loc_7AD3A`
   (sonic3k.asm:163597+) creates it before `jmp (BossDefeated)`. `onDefeatStarted()`
   (`SszMtzBossObjectInstance.java:802-811`) does not, and `usesDefeatSequencer()` is false, so
   no explosion appears at all. Same as the GHZ sibling, so presumably a known gap, but it is a
   visible one.

10. **NOTE — `bset #4,$38(a0)` in `loc_7ACA4` is not modelled.** Harmless: `$38` was cleared at
    `loc_7AD3A` and every orb has popped by then, so nothing reads the bit.

11. **NOTE — the orbs' self-deletion is a divergence the test enshrines.**
    `SszMtzBossOrbChild.java:252-255` deletes the orb when the parent is destroyed. In ROM an orb
    still in `loc_7AE22` is never popped by `_unkFA88` (`sub_7B0C2` is only reached from
    `loc_7AFA4` and `loc_7B02A`), so after `loc_7ACA4`'s `Go_Delete_Sprite` those orbs keep
    orbiting a zeroed slot at the level origin. The engine choice is the sane one, but
    `TestS3kSszMtzArenaHeadless.java:561-562` asserts it with a ROM-flavoured message
    ("nothing is left of the ring once the ship's slot is freed") that the ROM does not support.

12. **NOTE — the palette restore is not the ROM's restore.** `loc_7ACA4` copies
    `Target_palette_line_2` back into `Normal_palette_line_2`, i.e. the snapshot the init took.
    `restoreLevelPaletteLine()` (`SszMtzBossObjectInstance.java:979-995`) reloads `Pal_SSZ1` from
    `PAL_POINTERS`. Identical unless something else wrote line 2 during the fight.

13. **NOTE — `START_GROUP` is dead.** `SszMtzBossOrbChild.java:71` mirrors `byte_7AE1B` into a
    public constant nothing uses. The comment is right that nothing reads `$40(a1)`; the constant
    itself is then noise.

14. **NOTE — `usesS3kTouchSpecialPropertyResponse()` carries a side effect `loc_103FA` has not.**
    `ObjectTouchResponseController.java:162-179` runs, for any S3K `SPECIAL` touch, a block that
    teleports `nativeP2` onto the object and forces its animation to 2 when the leader is
    Knuckles. `Touch_Special` / `loc_103FA` (sonic3k.asm:21162-21194) does only
    `addq.b #1,collision_property(a1)` (twice for the sidekick). Worth confirming that this shared
    path is intended for a `$C6` orb before the fight ships with Knuckles + Tails.

15. **NOTE — a test name promises an assertion it does not make.**
    `theDescentIsOnePixelAFrameAndTurnsToFaceThePlayerAtFourTwoZero`
    (`TestS3kSszMtzArenaHeadless.java:225-249`) never asserts the facing;
    `loc_7A800`'s `move.w (Player_1+x_pos).w,d0 / cmp.w (SSZ_MTZ_boss_X_pos).w,d0 / blo.s` and the
    `bset #7,$2E / bset #0,render_flags` pair go unchecked.

16. **NOTE — the three-shot loop is fragile.** `TestS3kSszMtzArenaHeadless.java:477-501` only
    registers a fire when `seen` has fallen back to 0, i.e. when both shots of the previous pair
    have left the camera. At `Camera_X $1660` / 320 wide, with `x_vel $400` and the trailing shot
    holding 9 frames on the nose, that is roughly 30 frames against a 46-frame gap (finding 1).
    It works, but with little margin. Counting spawns rather than transitions would be steadier.

## What I verified, and what I could not

**Verified against the disassembly (all bullets in the brief):**

- `sub_7AEB0` arithmetic — correct in the port. `$2F` is written once (`move.b #$40,$2F(a1)`) and
  never advanced, so the first `GetSineCosine` is always `sin($40) = $100`. `moveq #0,d1` then
  `move.b $38(a1),d1` destroys the cosine, so the radius scalar is the **sine**; `move.w d0,d5` /
  `move.w d0,d4` keep the low word of `muls.w`, which the port's `(short)(unit * armX)` matches.
  At the second lookup `x_pos` takes `d0` (sine of `$2E`) and `$3A(a0)` takes `d1` (cosine of
  `$2E`) — so **yes, the depth `sub_7AF5A` sorts on is the cosine term**, as the port has it. At
  the third lookup `y_pos` takes `d0`, the sine of `$41` (or `$42` while the ship's `$3B` is set).
  I also checked the one real hardware hazard here: `move.b $3A(a1),d2` does not clear d2's upper
  byte, so the stale high byte of the previous frame's `y_pos` survives into `muls.w d3,d2` — it
  is harmless, because `$100 * ((stale<<8) + armY)` leaves only `armY<<8` in the low word that the
  later `muls.w d0,d2` reads. The port's `(short)` truncation reproduces this by construction.
- `sub_7AF5A` — four buckets, three mapping frames, all four sign/magnitude branches correct in
  `sortByDepth()`. (The *test* for it is finding 2.)
- `loc_7ADA2` — seven, not eight. `movea.l a0,a1` plus `bra.s loc_7ADB2` skips the allocate on the
  first pass, `moveq #7-1,d3` gives seven iterations, and `byte_7AE14` is seven bytes. The
  allocated slot is orb 0 and there is no separate controller. The port matches.
- `sub_7AC06`'s `cmpi.b #$1F,$1C(a0)` — correct. `sub_7ACF2` sets `$1C = $20` and then, in the
  same execution, `btst #0` (bit clear at `$20`, so the shipped `addi.w #2*2` row) and
  `subq.b #1,$1C` leave it at `$1F`. The hit frame really does end at `$1F`, and it can only be
  `$1F` once. `updateHitWindow()`'s `return … == 0x1F` after the decrement is the right shape.
- `bset #6,$2E(a0) / beq` in `loc_7A874` — the port's claim is correct: `bset` sets Z from the old
  bit, so the first turn branches away and only the second advances `$26` and sets `y_vel -$100`.
  `markTurn()` returns the old value. (Untested — finding 6.)
- `loc_7AFA4` — `MoveSprite` (sonic3k.asm:36032) adds the *old* `y_vel` to the position and then
  `addi.w #$38,y_vel`; the routine's own `subi.w #$20` leaves net `+$18` a frame, as the port
  says. The clamp is `cmpi.w #$180,y_vel / blt.s loc_7AFD0 / move.w #$180,y_vel` — a cap on
  downward speed, which is the sense `if (yVel >= TERMINAL) yVel = TERMINAL` has.
- `loc_7B02A` — `neg.w d0` then `asr.w #2` is what the port does, and the order matters for
  negative values; `add.w $38(a0),d0` with the `$42C` stored at the landing; `cmpi.w #$42C,d0`
  unsigned. `$3C` is **not** reloaded at the landing, and `$DA` is indeed unreachable: the
  `$3C` delay expires on the 61st airborne frame, while a `-$400` launch under `+$18` net gravity
  with a `$180` terminal speed keeps the orb in the air for well over 90 frames. The port's
  comment on that is right.
- Collision bytes — `$11` at `loc_7A72C`, `$F` at `sub_7ACF2`'s restore (so the ship's box does
  shrink permanently after its first hit), `$87` while orbiting **and** through the launch delay,
  `$C6` after it, and `$DA` a `$C0` byte whose size `$1A` is absent from `Touch_Special`'s list
  (`$7,$6,$A,$C,$15,$16,$17,$18,$21`, sonic3k.asm:21162-21183) and therefore inert. All modelled.
  One engine aside: `ObjectTouchResponseController.decodeCategory` returns `SPECIAL` for *any*
  `$C0` byte in S3K mode before the size list is consulted, so `$DA` would not in fact be inert
  here — moot, since it is unreachable.
- `loc_7A7C4`'s six bytes — `$10,0,3,0,1,0` over `_unkFA82..$87`. Only the first word is modelled
  (`$1000`, correct); see finding 4 for the rest.
- The escape, frame for frame — `BossDefeated` sets `$2E = $3F`; `Wait_FadeToLevelMusic` returns
  on 63 decrements and on the 64th goes negative into `loc_85674`, which sets `$2E = $77` and
  tail-calls `loc_7AC7A` in that same frame (routine to `loc_7AC92`, `x_vel $400`, `y_vel 0`, no
  move). `loc_7AC92` then moves on 119 frames and goes negative on the 120th into `loc_7ACA4`.
  Total 184 = `$40 + $78`. `updateEscape()` reproduces this exactly, and the test's
  `assertEquals(0x40 + 0x78, framesToBeaten)` is a genuine, falsifiable ROM number.
- The rest of `off_7A7F0` — I walked all eight arms plus `off_7AA60`'s three and `sub_7AB56`
  against the port line by line. Every comparison sense (`blo`/`bhs`/`blt`), every velocity
  literal, the `or.w` zero test at `loc_7A92C`, the `bchg #7` at `loc_7AACE`, the recoil's skip of
  `loc_7A8DA`, and the `& 0xFFFF` wrap on the laser timer when it runs past zero are right.

**Could not verify:**

- Nothing was executed — no Maven, no test run. Every finding above is from reading. In
  particular finding 1 is an argument from the ROM and the port, not an observed failure.
- The native frame numbers quoted throughout the port and test javadocs (6156, 6189, 6190, 6651,
  6715 in the `hpz` segment of `s3k-sonic-tails-complete-emeralds`). I had no access to those
  rows. Their internal arithmetic is consistent with the ROM (33 = `$1F + 2`, 64 = `$3F + 1`).
- `TrigLookupTable.SINCOSLIST` actually being S3K's `sine.bin`.
- `nativeFramedCameraX`, `eventsBgByte` signedness, `eggRoboFlyByPassed`'s bit convention, and
  `spawnChild`/`ObjectRefId` relink mechanics — shared surfaces already settled by the reviewed
  Green Hill sibling, which this port follows.
- Whether the `Refresh_ChildPositionAdjusted` dx-negation convention the laser and head children
  use matches the engine's `renderFlipped`; the port is at least self-consistent with the sibling.
