# SSZ Green Hill boss — review 02 (applied-review pass)

Read-only review of the uncommitted tree in `.worktrees/ai-ssz-bring-up`.
Authority: `/home/farrell/code/projects/OpenGGF/docs/skdisasm/sonic3k.asm`
(`Obj_SSZGHZBoss` at :162576, the shared helpers at :176901-:180860).
No build, no test run — every verdict below is a static reading of the ROM text
against the diff.

## Headline

Two of the diff's load-bearing new claims are **false**, and they were reached by
searching only `Obj_SSZGHZBoss`. The bit that settles both is in the shared touch
response, `Touch_Enemy.checkhurtenemy`, **sonic3k.asm:20922**:

```
	tst.b	boss_hitcount2(a1)	; = collision_property, $29
	...
	move.b	collision_flags(a1),$25(a1)
	move.b	#0,collision_flags(a1)
	subq.b	#1,boss_hitcount2(a1)
	bne.s	.bossnotdefeated
	bset	#7,status(a1)		; <-- the ship DOES get status bit 7
```

## Findings

1. **HIGH — `loc_7A568`'s `btst #7,status(a1)` is NOT dead code.** sonic3k.asm:20922
   sets `status` bit 7 on the boss (`a1` = the object whose `boss_hitcount2` just hit
   zero) on the killing hit. The emitter therefore takes `loc_7A59A /
   Delete_Current_Sprite` on the frame after the kill, exactly as the pre-change code
   did. The new Javadoc in `SszGhzBossShieldChild`, the new `s3k-known-bugs.md` entry
   "…Emitter Is Deleted Where The ROM Leaks It", and plan-doc section F are all wrong,
   and the code comment "Not loc_7A568's btst #7,status(a1): that branch is dead" is a
   mis-citation of correct behaviour. Check 5: **wrong**.

2. **HIGH — the six links do not ride the escape out.** Same bit. `loc_7A428`/`loc_7A4D0`
   end `Child_Draw_Sprite_FlickerMove` and `loc_7A514` ends
   `Child_DrawTouch_Sprite_FlickerMove`; both read `btst #7,status(a1)` on `parent3`
   (sonic3k.asm:178114 / :178136) and both branch to `loc_849D8`, which does
   `bset #7,status(a0)` / `move.l #Obj_FlickerMove,(a0)` / **`clr.b collision_flags(a0)`**
   / `Set_IndexedVelocity`. So at the killing hit the chain converts to flickering
   scatter debris, cascading one link per frame down `parent3`, and the ball **loses its
   `$8F` hitbox immediately**. The diff removed the chain deletion from `onDefeatStarted`
   and now keeps six rigidly-orbiting links with a live HURT box through the whole
   ~183-frame escape. Check 8: the narrow claim ("`loc_7A5EC` clears no `$38` bit 6 and
   deletes no chain") is **right**; the conclusion drawn from it ("so the six links ride
   the escape out with the ship") is **wrong**, and the change is a behavioural
   regression against the ROM, not a fix. `TestS3kSszGhzArenaHeadless`'s new
   `assertEquals(6, boss.chainForTest().size(), "nothing in loc_7A5EC deletes the
   chain…")` pins the wrong behaviour.

3. **MEDIUM — the escape is one frame shorter than the ROM, and the plan doc says
   otherwise.** Derivation: `loc_7A5EC` → `BossDefeated` (:180822) `move.w #$3F,$2E`;
   the code pointer only changes for the *next* frame, so `Wait_FadeToLevelMusic`
   (:179656) runs 64 times (63 → -1), its 64th execution reaching `loc_85674` (:179662)
   which arms `$2E = (2*60)-1 = $77` and tail-calls `loc_7A3CE`; `loc_7A3E6` then runs
   120 times (119 → -1), its 120th reaching `loc_7A3F8`'s `st (Events_bg+$00).w`.
   ROM total from the killing frame = 64 + 120 = **$40 + $78 = 184**. The engine burns
   one `Wait_FadeToLevelMusic` decrement inside the killing frame (the test's own
   `assertEquals(0x3E, boss.waitTimerForTest())` documents this), so it delivers **183**,
   and the test asserts `0x3F + 0x78` = 183. The plan-doc entry B claims the test asserts
   "a literal `$40 + $78`" — it does not. Check 2: `$2E = $3F` and 100 points **right**
   (`HUD_AddToScore` at :17645 adds `d0` directly, so `moveq #100` is 100, not 1000);
   the asserted total is **wrong by one frame**.

4. **MEDIUM — the test Javadoc on `theShipSpawnsAndDropsTheChainAtTheSameWorldPositionAtEveryWidth`
   states the opposite of the code it guards.** It says the two camera reads "do not want
   `Sonic3kSSZEvents.nativeFramedCameraX`" and that "reframing them would move the drop
   trigger to the right of the spawn"; the diff reframes both (boss line 483, events line
   361) and plan-doc section H records that reading as killed. Stale comment left in the
   changed file.

5. **MEDIUM — `assertEquals(0x20, boss.hitWindowForTest() + 1 > 0x20 ? 0x20 :
   boss.hitWindowForTest() + 1, "move.b #$20,$20(a0) armed the window")` accepts two
   different values.** It passes for `hitWindow == $1F` and for `$20`. That is exactly
   the distinction the flash parity depends on (`$20` even → shipped row on the first
   window frame), so the one assertion that could pin the parity deliberately refuses to.
   Check 10 hit.

6. **MEDIUM — `sawNormal` in `oneRealHitFlashesThreePaletteWordsFromTheShippedRow`
   may be unable to disagree.** The "normal" row `$8,$866,$222` is, by the diff's own
   known-bugs entry, plausibly already what line 0 colours 7/14/15 hold before the fight
   ("which is the reading the table itself suggests"). If so, `sawNormal` is true with
   zero palette writes. The assertion needs a pre-hit sample of `flashColors()` asserted
   *different* from `FLASH_NORMAL_ROW`, or it proves nothing.

7. **MEDIUM — mis-cited collision category.** `assertEquals(0xC0 | 0x0F,
   boss.getCollisionFlags(), "ObjDat_SSZGHZBoss's dc.b $1C,$20,$A,$F is collision_flags
   $F, category BOSS")`. `ObjDat_SSZGHZBoss` (:162976) is `dc.b $1C,$20,$A,$F` and
   `SetUp_ObjAttributes3` (:176907) writes that last byte to `collision_flags`, whose
   top two bits are the category (`sonic3k.constants.asm:35`). `$0F` has category `%00`
   = **enemy**, not boss — `Touch_ChkValue` (:20773) branches `%00 → Touch_Enemy`, and
   the boss-ness comes from `boss_hitcount2` being non-zero, not from the category. The
   engine's `0xC0` is `%11` (`Touch_Special`, the starpost category). The engine
   convention may be pre-existing, but the assertion message asserts a ROM fact that is
   not in the ROM.

8. **LOW — `assertEquals(0, links.getFirst().xFixedForTest() & 0xFFFF, "Refresh_ChildPosition
   is move.w …")` cannot disagree.** The root's low word is initialised to 0
   (`spawn.x() << 16`) and every write in `SszGhzBossChainLinkChild` preserves it
   (`updateDrop`'s masked add, `updateSwing`'s `| (x & 0xFFFF)`). No code path can make
   it non-zero, so the assertion is an identity on the implementation. Check 10 hit.

9. **LOW — `assertFalse(((Object) emitter) instanceof TouchResponseProvider, "word_7A65A's
   last byte is 0…")` is a statement about the Java class hierarchy, constant across
   runs and independent of every frame the test stepped.** The test is named
   `…AndCannotHurtAnything` but never puts a player on the emitter. Check 10 hit.

10. **LOW — the chain-drop position window is four times wider than it needs to be.**
    `(boss.getX() & 0xFFFF) <= CHAIN_DROP_X && > CHAIN_DROP_X - 4`. `x_vel = -$100` is
    exactly 1 px/frame from an even `$270`, so the drop frame lands exactly on `$200`;
    `assertEquals(0x200, …)` would be the honest form. Appears twice.

11. **LOW — `assertTrue(turns >= 2, …)` and `assertTrue(sawFraction, …)`** are
    existential lower bounds over 1200 and 600 samples respectively. Weak but not
    tautological; noted, not blocking.

12. **LOW — no release of `S3kPaletteOwners.SSZ_GHZ_BOSS_HIT_FLASH`.** `writeFlashRow`
    is the only reference in the whole tree; nothing relinquishes the claim when the
    `$20` window closes. If `applyContiguousPatch` is a persistent claim rather than a
    per-frame submission, the known-bugs entry's description of the deviation is
    backwards. Unverified — I did not read the registry's lifetime semantics.

13. **LOW — the vertical spawn read is not reframed.** `Sonic3kSSZEvents` line 362 still
    uses raw `camera.getY() + SPAWN_CAMERA_Y_OFFSET` while X now goes through
    `nativeFramedCameraX`. Harmless at 320x224 and 800x(same height), and both widths the
    test exercises share a height, so it is untested rather than wrong.

## The checks that came out clean

- **Check 1 — frame accounting: the number is right, one sentence of the prose is wrong.**
  `Obj_SSZGHZBoss` ends `jmp (PalLoad_Line1)` and never reaches `Obj_Wait`, so the init
  execution costs no wait frame — **right**. `Obj_Wait` (:177949) is
  `subq.w #1,$2E / bmi loc_84892 / rts`, so from `$1F` it goes negative on the **32nd**
  decrement — **right**. But `loc_7A294` does **not** "spend a whole frame": `loc_84892`
  is `movea.l $34(a0),a1 / jmp (a1)`, a tail call inside that same 32nd frame, and
  `loc_7A294` installs `loc_7A29C` and `rts` there. The arithmetic is unaffected —
  1 init + 32 wait executions, first `off_7A2B4` dispatch on **init + 33** — and the
  implementation's `initExecuted`/`dispatcherInstalled` pair produces exactly 33, as
  does `FRAMES_FROM_INIT_TO_FIRST_DISPATCH = 0x1F + 2`. Fix the sentence, keep the count.
- **Check 3 — hit flash: right on every point.** `Normal_palette_line_2 = Normal_palette+$20`
  (sonic3k.constants.asm:768), so `word_7A622`'s `+$0E/$1C/$1E` are **line 0**, colours
  7, 14, 15 — the line `make_art_tile(ArtTile_RobotnikShip,0,0)` draws on. `btst #0,$20(a0)
  / bne loc_7A5D4` leaves `d0 = 0` on **odd** counter values, so odd frames write row 0
  (`$8,$866,$222`) and even frames add the offset. `lea word_7A628(pc,d0.w),a2` makes
  `addi.w #2*2,d0` a **byte** displacement of 4 = two words in, giving `$222,$888,$CCC`;
  `2*3` = 6 bytes = three words gives `$888,$CCC,$EEE`. **Parity**: `sub_7A5A0` arms
  `$20(a0) = $20` and only decrements *after* `sub_7A614`, so the **first** window frame
  reads an even counter and writes the shipped flash row — which is what
  `(invulnerabilityTimer & 1) != 0 ? NORMAL : SHIPPED` before the decrement produces.
  Correct, subject to finding 5 (the test declines to pin the armed value).
- **Check 4 — right.** `SetUp_ObjAttributes3` (:176907) writes the 4th byte to
  `collision_flags`: `ObjDat3_7A678` `8,8,0,$8F` → `$8F` (`%10` = harmful);
  `ObjDat3_7A660` `8,8,2,0` and `_7A66C` `8,8,3,0` → 0; `word_7A65A` `8,4,6,0` → **0**,
  the emitter is harmless. Only `loc_7A514` ends `Child_DrawTouch_Sprite_FlickerMove`
  (the only one of the two with `Add_SpriteToCollisionResponseList`). Neither routine
  skips frames *while the parent's `status` bit 7 is clear* — but see finding 2: it is
  not clear for the whole fight, only until the killing hit.
- **Check 6 — right, all of it.** `subi.b #$40 / cmpi.b #-$80 / bhs` reverses on every
  angle with `(a-$40)&$FF < $80`, i.e. `[$40,$BF]`. Walked from 0 with step +1: flip at
  `$40` landing on `$3F`, descent through 0 and `$FF` down to `$C0`, flip at `$BF`
  landing on `$C0`, ascent back. Visited = `[$C0,$FF] ∪ [$00,$40] ∪ {$BF}`; excluded
  interior **`[$41,$BE]`**; `$40`, `$BF`, `$C0` all visited. `sls` sets `d1 = $FF` on
  Low-or-Same, i.e. `$3C <= $40`; `bset #3,$38(a1)` fires when `d1 == 0`, so **unflipped
  → the `$BF` end, flipped → the `$40` end**. `updateSwing`'s
  `flipped ? lowOrSame : !lowOrSame` matches.
- **Check 7 — right.** `MoveSprite_CircularSimple` (:178424) is `move.l x_pos(a1),d2 /
  add.l d0,d2 / move.l d2,x_pos(a0)` for both axes; `Refresh_ChildPosition` (:177281) is
  `move.w`. `$100 << 16 >> 4 = $00100000` = 16.0 px, `>> 3 = $00200000` = 32.0 px, and
  `loc_7A4EC` sets `$3A = 4` while `loc_7A544` sets `$3A = 3`. `MoveSprite2` (:36053)
  applies no gravity, so the test's "exactly `$20` px in `$20` frames" is sound.
- **Check 9 — the rest of the citations hold.** `loc_7A446`'s `#$1A,child_dy` and
  `#1,$3A`; `loc_7A482`/`loc_7A496` as root routines 4 and 6; `loc_7A4EC`/`loc_7A500`
  for subtypes 2-8; `CreateChild9_TreeList` (:177210) numbering subtypes by 2 and setting
  `$44 = boss` for every link; `ChildObjDat_7A69E`'s `dc.b $1E,0` via `CreateChild1_Normal`;
  `loc_7A568`'s `btst #6,$38(a1)` and `btst #0,(V_int_run_count+3).w` every-other-frame
  skip; `loc_57686`'s `Camera_min_X_pos = Camera_max_X_pos = $160` and `loc_576E8`'s
  allocation gate at `Camera_Y_pos == $7C0`; `BossDefeated` at :180822. The
  `nativeFramedCameraX` arithmetic checks out numerically: `DeadzoneGeometry.rightEdge`
  is `width/2`, so `800/2 - 320/2 = $F0` and `$70 + $F0 = $160`.

## Not completed

None of the ten checks was blocked, but two are partial:

- **Check 12 (palette-owner lifetime)** — I did not read
  `S3kPaletteWriteSupport.applyContiguousPatch`'s ownership semantics, so whether the
  known-bugs entry describes the deviation in the right direction is unverified.
- **Everything is static.** I ran no tests and no build (read-only brief), so every
  statement about what an assertion *does* is a reading of its source, not an observed
  pass or fail. In particular findings 3, 5 and 6 predict test outcomes rather than
  reporting them.
