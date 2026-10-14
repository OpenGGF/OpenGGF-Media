# Review: LRZ seamless act change `$900` -> `$901` (commit `1730f258a`)

Independent read-only review. No build was run; every claim below is from the
worktree `/home/farrell/code/projects/OpenGGF/.worktrees/ai-lrz-bring-up` and
`/home/farrell/code/projects/OpenGGF/docs/skdisasm/sonic3k.asm`.

The single fact that governs most of the findings: **ROM `Load_Level`
(sonic3k.asm:38747-38761) copies `$1000` words of layout into
`Level_layout_header` and does nothing else.** It does not touch camera bounds,
Object RAM, the ring table, or any routine byte. That is precisely why
`loc_56CAA` has to clear five level variables by hand, and it is what makes
`ObjectSurvivalPolicy.ALL_LIVE_SST` the right choice here.

---

## 1. SEVERITY: blocker — `jsr (Offset_ObjectsDuringTransition)` is not modelled; every carried object stays in act-1 coordinates

`Sonic3kLRZEvents.java:216-236` (`requestAct2Reload`) builds the request with
`.cameraOffset(-ACT2_REBASE_X, 0)` and **no** `playerOffset(...)` and **no**
`romWorldObjectOffsetRange(...)`, leaving `objectOffsetPolicy` at its default
`CARRIED_OBJECTS` (`SeamlessLevelTransitionRequest.java:382`) and
`playerOffsetX` at `0` (`SeamlessLevelTransitionRequest.java:375`).

`LevelActTransitionExecutor.offsetCarriedObjectsForTransition`
(`LevelActTransitionExecutor.java:281-314`) reads **`request.playerOffsetX()`**,
not `cameraOffsetX()`, and under `CARRIED_OBJECTS` it only calls
`instance.onCarriedAcrossSeamlessTransition(...)`, whose default in
`ObjectInstance.java:250-251` is a no-op. So with `ALL_LIVE_SST` selected
(`Sonic3kLRZEvents.java:224-225`) every surviving act-1 object is carried into
act 2 and left at its act-1 X, about `$2C00` to the right of the player.

ROM settles it: `loc_56CAA` line **sonic3k.asm:115365** `jsr
(Offset_ObjectsDuringTransition).l` with `d0 = $2C00`, `d1 = 0`. The routine
(sonic3k.asm:104166-104181) walks `Dynamic_object_RAM+object_size` up to
`Breathing_bubbles`, tests `render_flags` bit 2, and does `sub.w d0,x_pos(a1)` /
`sub.w d1,y_pos(a1)`. The commit message claims this ("subtracts `$2C00` from
... every live object"); the diff does not do it.

The engine already has the exact mechanism: `ObjectOffsetPolicy.ROM_WORLD_OFFSET_RANGE`
(`SeamlessLevelTransitionRequest.java:286-292`), used by the FBZ precedent at
`Sonic3kFBZEvents.java:729-730` with `romWorldObjectOffsetRange(4, 94)`. Those
bounds are the same ROM span: `sonic3k.constants.asm:303-311` puts Player_1 at
slot 0, Player_2 at 1, `Reserved_object_3` at 2, `Dynamic_object_RAM` at 3..92,
and `Breathing_bubbles` at 94, so `Dynamic_object_RAM+object_size` = slot 4 and
the `dbf` count ends exclusive at 94.

**Change:** add to the builder in `Sonic3kLRZEvents.requestAct2Reload`
```java
.playerOffset(-ACT2_REBASE_X, 0)
.romWorldObjectOffsetRange(4, 94)
```
and drop the player writes from `LrzActTransitionHandoff.transferAfterTargetInit`
(`LrzActTransitionHandoff.java:63-71`), which `applySeamlessOffsets`
(`LevelManager.java:3893-3930`) then performs at the ROM's own point. Note that
screen-space owners (results, title card) are correctly excluded for free:
`participatesInRomWorldTransitionOffset()` defaults false
(`ObjectInstance.java:258-260`), which is the engine's model of `btst #2,render_flags`.

---

## 2. SEVERITY: defect — the post-transition camera **Y** bounds are not carried; the arena Y lock is released

`requestAct2Reload` sets `postTransitionMinX/MaxX` and their targets
(`Sonic3kLRZEvents.java:228-231`) and nothing for Y.
`LevelActTransitionExecutor.java:228-229` calls
`restoreCameraBoundsForCurrentLevel(cam)` — which installs LRZ2's *level
descriptor* min/max X and Y and recomputes vertical wrap
(`LevelManager.java:3831-3849`) — and only then applies the overrides, so X is
restored from the request and **Y is left at LRZ2's level bounds**.

ROM: `Load_Level` writes no camera words at all (sonic3k.asm:38747-38761), and
`loc_56CAA` subtracts only from `Camera_X_pos`, `Camera_X_pos_copy`,
`Camera_min_X_pos`, `Camera_max_X_pos` (sonic3k.asm:115366-115369). The Y
bounds therefore keep the LRZ1 miniboss-arena values across the change — which
is the whole point of "the two camera releases that follow the act change are
still to come" in the changelog. All three precedents pass Y explicitly:
`Sonic3kFBZEvents.java:721-722,726-728` (carried unchanged),
`Sonic3kCNZEvents.java:883-886` (offset), `SozAct1Events.java:143` (pinned).

**Change:** add
`.postTransitionMinY(cam.getMinY()).postTransitionMaxY(cam.getMaxY())
.postTransitionMinYTarget(cam.getMinYTarget()).postTransitionMaxYTarget(cam.getMaxYTarget())`
so the pre-change Y bounds survive, mirroring FBZ.

---

## 3. SEVERITY: defect — `runtimeArtAdmissionPolicy` is left at `IMMEDIATE`, so LRZ2's enemy art is admitted on the reload frame

The LRZ builder passes no policy, so it is `RuntimeArtAdmissionPolicy.IMMEDIATE`
(`SeamlessLevelTransitionRequest.java:355-356`).
`Sonic3kObjectArtProvider.prepareRuntimeArtForActTransition`
(`Sonic3kObjectArtProvider.java:1044-1078`) then calls `scheduleEnemyKosArt(...)`
and, for `IMMEDIATE`, `consumeRuntimeArtAdmission(lease, ownerKind)` in the same
call — i.e. the engine runs `LoadEnemyArt` for `$901` during the swap.

`loc_56CAA` runs `Load_Level` and `LoadSolids` only (sonic3k.asm:115359-115360).
`Load_Level` loads no art (sonic3k.asm:38747-38761). All three seamless-act-change
precedents pass `TITLE_OWNER`: `SozAct1Events.java:139`,
`Sonic3kCNZEvents.java:866`, `Sonic3kFBZEvents.java:713`.

There is a real reason the commit could not simply copy them: **LRZ requests no
in-level title card at all** — `grep requestInLevelTitleCard` over
`Sonic3kLRZEvents.java` is empty, and `showInLevelTitleCard(false)` is set
(`Sonic3kLRZEvents.java:223`), so a `TITLE_OWNER` lease would never be consumed.
That is finding 4.

**Change:** land the act-2 in-level title card (finding 4) and switch to
`.runtimeArtAdmissionPolicy(RuntimeArtAdmissionPolicy.TITLE_OWNER)`. If the
title card is deliberately deferred, say so in the commit and in
`docs/S3K_KNOWN_DISCREPANCIES.md`-adjacent notes — an undocumented `IMMEDIATE`
reads as an oversight, not a decision.

---

## 4. SEVERITY: defect — no act-2 title card is requested, unlike every precedent

`Obj_Results` reaches `st (Events_fg_5)` only after `addq.b #2,routine(a0)`
(sonic3k.asm:62613-62622), i.e. inside the results sequence that also produces
the next act's title card. SOZ models that explicitly
(`SozAct1Events.java:148-155`, `requestInLevelTitleCard(8,1,...)`); CNZ tunes it
(`Sonic3kCNZEvents.java:878`); FBZ owns it through its own path. LRZ does
neither, so `$901` begins with no title card and, per finding 3, no title owner
for the art lease.

**Change:** add the `$901` in-level title-card request on the first act-2 pass,
as `SozAct1Events.updateSeamlessEntry` does, then move the admission policy.

---

## 5. SEVERITY: risk — `Clear_Switches` is executed *after* `Load_Level`, not before

`loc_56CAA` order is `jsr (Clear_Switches)` at **sonic3k.asm:115355**, then
`clr.b (LRZ_rocks_routine)` at :115356, then `jsr (Load_Level)` at :115359. The
implementation runs `Sonic3kLevelTriggerManager.reset()` inside
`LrzActTransitionHandoff.transferAfterTargetInit`
(`LrzActTransitionHandoff.java:59`), which the executor invokes at
`LevelActTransitionExecutor.java:251-253` — after the level load, after
`initLevelEventsForCurrentZoneAct()` (:235) and after
`reinitializeZoneFeaturesForActTransition()` (:246). Any trigger bit an act-2
initializer sets during those steps is wiped.

The FBZ precedent gets the order right: `Sonic3kFBZEvents.java:738-741` calls
`Sonic3kLevelTriggerManager.reset()` *before*
`applySynchronousScreenEventTransition(request)`, with a comment citing the same
ROM ordering.

**Change:** move the `Sonic3kLevelTriggerManager.reset()` call out of the
handoff and into `requestAct2Reload` immediately before
`levelManager().applySynchronousScreenEventTransition(...)`.

---

## 6. SEVERITY: risk — the `Events_fg_5` consumption gate is "any stage but `$C`", where the ROM's is "stage 0 only"

`LRZ1_BackgroundEvent` dispatches on `Events_routine_bg` through a four-entry
index (sonic3k.asm:115264-115271) and only the stage-0 entry, `loc_56BD2`,
contains `tst.w (Events_fg_5).w` (sonic3k.asm:115274-115275). Stages `$4`
(`loc_56C6E`) and `$8` (`loc_56C88`) never look at the word.

`Sonic3kLRZEvents.advanceSeamlessActChange` (`Sonic3kLRZEvents.java:148-160`)
checks `backgroundRoutine() == BG_STAGE_ACT_CHANGE` and otherwise arms on
`eventsFg5() != 0` whatever the stage is. Today this cannot misfire, because
`setBackgroundRoutine` is only ever called with `BG_STAGE_ACT_CHANGE`
(`Sonic3kLRZEvents.java:182`) or `0` (`LrzActTransitionHandoff.java:55`) — the
ROM's stages 4 and 8 are unimplemented. It becomes wrong the moment they land.

**Change:** make the arm branch explicit: `if (lrz.backgroundRoutine() != 0)
return false;` before the `eventsFg5()` test.

---

## 7. SEVERITY: risk — `setEventsFg5` has no zone/act guard, so it can latch a flag into the Lava Reef boss state

`Sonic3kLevelEventManager.setEventsFg5ForActTransition` calls
`lrzEvents.setEventsFg5(true)` unconditionally (diff, `Sonic3kLevelEventManager.java:1828-1830`),
and `Sonic3kLRZEvents.setEventsFg5` (`Sonic3kLRZEvents.java:243-248`) writes
`0xFFFF` into whatever `LrzZoneRuntimeState` is current. That state is shared
with the boss act: `Sonic3kLevelEventManager.isLavaReef` is true for
`ZONE_LRZ_BOSS_HPZ` act 0 (`Sonic3kLevelEventManager.java:472-475,516-518`).
`advanceSeamlessActChange` does guard on `zoneIndex() != ZONE_LRZ || act != 0`
(`Sonic3kLRZEvents.java:149-151`), so nothing fires — but the flag is left set,
is captured in rewind (`LrzZoneRuntimeState.java:308`), and is never cleared
except by `loc_56BD2`'s own path.

ROM's own gate is in `Obj_Results`: `tst.b (Apparent_act) / bne` and the
`Apparent_zone` exclusions (sonic3k.asm:62615-62622) — a zone/act gate, not a
per-handler one.

**Change:** guard the setter the same way the reader is guarded:
`if (lrz != null && lrz.zoneIndex() == Sonic3kZoneIds.ZONE_LRZ && lrz.actIndex() == 0)`.

---

## 8. SEVERITY: risk — the `act2ArtJobOrdinal < 0` fallback changes the act without the art and without the wait

`applyActChangeWhenArtIsReady` (`Sonic3kLRZEvents.java:200-216`) begins:
```java
if (lrz.act2ArtJobOrdinal() < 0) { requestAct2Reload(null); return; }
```
That path skips `tst.b (Kos_modules_left) / bne.s loc_56D16`
(sonic3k.asm:115347-115348) entirely and hands `null` art to the handoff, whose
`applySecondaryArt` then returns immediately
(`LrzActTransitionHandoff.java:84-86`) — so `ArtKosM_LRZ2_Secondary` at
`tiles_to_bytes($090)` (sonic3k.asm:115286-115287) is never uploaded and act 2
runs with act-1 patterns in that range. Nothing in normal play reaches it
(`armActChange` always sets the ordinal), but a restore or an exception between
arm and claim does, and the failure is silent and visual.

**Change:** treat it as the invariant violation it is — throw, or re-queue the
module and stay on stage `$C` — rather than performing a half act change.

---

## 9. SEVERITY: note — `CAPTURE_BYTES` arithmetic is correct

`LrzZoneRuntimeState.java:44-45` now reads
`S3kScreenShake.captureBytes() + 2 * Integer.BYTES + 20 * Short.BYTES`.
`captureBytes()` (`LrzZoneRuntimeState.java:290-315`) issues exactly two
`putInt` (`appliedScreenShakeOffset`, `act2ArtJobOrdinal`) and twenty
`putShort` (fifteen pre-existing through `domePlatformPhase`, the new
`eventsFg5`, and the four `cameraStored*`). `restoreBytes`
(`LrzZoneRuntimeState.java:318-347`) reads them back in the same order. The old
`Integer.BYTES + 19 * Short.BYTES` was likewise exact, so the `+6` is right.
No finding.

---

## 10. SEVERITY: note — the hardware-timing handle *is* resolvable after a rewind restore, and LRZ follows the SOZ precedent

`hardwareTiming().pendingHandle(KOS_MODULE_QUEUE, ordinal).orElseThrow()`
(`Sonic3kLRZEvents.java:207-210`) is the sanctioned rebind:
`HardwareTimingService.pendingHandle` (`HardwareTimingService.java:315-333`)
is documented as "rewind owners use this after the timing ledger has been
restored so their transient queue facade can bind to the original job without
submitting replacement work", and `HardwareTimingService` is itself
`RewindSnapshottable<HardwareTimingSnapshot>` (`HardwareTimingService.java:20`,
`capture()` :425, `restore()` :442-461, which keeps live jobs rather than
recreating them). `Sonic3kSOZEvents.claimReadyResources`
(`Sonic3kSOZEvents.java:313-321`) does exactly the same thing with the same
`orElseThrow()`, with the comment "Rebind from captured ordinals every pass: no
stale facade survives rewind."

One real difference from SOZ: SOZ rebinds at the **top of every update pass**
(`Sonic3kSOZEvents.java:98`), so a restore always reconciles. LRZ only rebinds
when `backgroundRoutine() == BG_STAGE_ACT_CHANGE`, which is fine because the
ordinal and the stage are captured together — but it means finding 8's fallback
is the only handling of a lost job, and it is the wrong one.

---

## 11. SEVERITY: note — `markSynchronousSeamlessTransitionBoundary()` placement matches SOZ

`Sonic3kLRZEvents.java:237-240` calls it immediately after
`applySynchronousScreenEventTransition` returns, guarded by `hasRuntime()` —
character for character what `SozAct1Events.java:146` does. It resolves to
`gameplayMode.markRewindBoundary(RewindBoundary.SEAMLESS_LEVEL_TRANSITION)`
(`LevelManager.java:4682-4687`), a timeline cut so no rewind can cross from act
2 back into act 1's object/level graph. FBZ marks it later
(`Sonic3kFBZEvents.java:693`) because FBZ has a native tail *after* the reload;
LRZ's tail (the `-$2C00` rebase) runs inside the transition via the handoff, so
marking immediately is right.

Two small caveats, neither a defect: `advanceRockSpriteWindow()`
(`Sonic3kLRZEvents.java:129`) still runs on the act-2 state after the boundary
is marked, inside the same frame; and `suppressLevelLoadRewindBoundary` is
correctly omitted — its only consumer,
`LevelManager.resetRewindBufferAfterLevelBoundary` (`LevelManager.java:499-505`),
has no callers anywhere in `src/main`, and `loadActTransitionLevelData`
(`LevelManager.java:700-737`) never marks `LEVEL_LOAD`. FBZ setting it
(`Sonic3kFBZEvents.java:733`) is inert.

---

## 12. SEVERITY: note — the five `loc_56CAA` level variables, and the trigger/anim halves of `Clear_Switches`

Answering question 1 and question 2 directly.

| ROM variable (sonic3k.asm) | Engine owner | Reset by `RELOAD_TARGET_LEVEL`? |
|---|---|---|
| `Dynamic_resize_routine` (:115350) | `AbstractLevelEventManager.eventRoutine` via `getDynamicResizeRoutine()` (`Sonic3kZoneEvents.java:222-238`); LRZ hard-returns 0 (`LrzZoneRuntimeState.java:91`) | Yes — `initLevelEventsForCurrentZoneAct()` (`LevelActTransitionExecutor.java:235`) -> `AbstractLevelEventManager.initLevel` zeroes `eventRoutineFg/Bg` (`AbstractLevelEventManager.java:104-118`); LRZ has no resize machine to begin with |
| `Object_load_routine` (:115351) | `ObjectManager` placement cursor | Yes — a **new** `ObjectManager` is constructed from `level.getObjects()` and reset (`LevelManager.java:3968-4008`) |
| `Rings_manager_routine` (:115352) | `RingManager` | Yes — a **new** `RingManager` over `level.getRings()`, reset at `postOffsetCameraX` (`LevelManager.java:4039-4045`, cameraX computed at `LevelActTransitionExecutor.java:213`) |
| `Boss_flag` (:115353) | `AbstractLevelEventManager.bossActive` (`AbstractLevelEventManager.java:83`) | Yes — `initLevel` sets `bossActive = false` (`AbstractLevelEventManager.java:111`) |
| `Respawn_table_keep` (:115354) | `PersistentRespawnState` / `ObjectPlacementController` | Yes, and the worry is unfounded — the engine has no persistent table to keep. `PersistentRespawnState.java:14-32` states the model: "The engine rebuilds a fresh `ObjectPlacementController` on reload, so it instead captures this state at stage entry and re-establishes it before return placement." The only re-establishment path is the big-ring/bonus snapshot, gated on `bigRingReturnRespawnState != null` (`LevelTransitionCoordinator.java:975-1006`), which is null here. `Ring_status_table` likewise dies with the old `RingManager`. |

Because `Load_Level` clears none of these (sonic3k.asm:38747-38761), the ROM
must clear them explicitly and the engine gets the same end state from the
rebuild. **No change needed for finding 12's table.**

`Clear_Switches` (sonic3k.asm:104284-104291) clears `$20` bytes from
`Level_trigger_array`, and `sonic3k.constants.asm:699-700` does put
`Anim_Counters ds.b $10` immediately after `Level_trigger_array ds.b $10`, so
the second half is the animated-tile phase counters. **They are reset by the
reload**, and correctly so: `LevelActTransitionExecutor.java:165` calls
`initAnimatedContent()` -> `initAnimatedPatterns()`
(`LevelManager.java:1850-1868`) -> `Sonic3k.getOrCreateLevelAnimationManager`
(`Sonic3k.java:222-236`), whose cache key is `levelAnimationLevel == level`;
the reload installs a new `Level`, so a new `Sonic3kLevelAnimationManager` and
a new `Sonic3kPatternAnimator` are built with `actIndex = 1`. The constructor
then seeds `lastLrzBg1Phase/lastLrzBg2Phase` from
`seedsLrzAnimationCounters(zone, act)` (`Sonic3kPatternAnimator.java:296-300,
1919-1928`), which is act-0 only — matching its own ROM citation: "`Animate_Init`:
`$900` (sonic3k.asm:56411-56414) and `$1600` (56458-56461) write `-1` to
`Anim_Counters+1` and `+3`. `$901` is absent from that list, so it runs with the
counters the level load cleared." The shared `Sonic3kGlobalAnimationState`
carried into the new manager holds only ring timer/frame, the AIZ vine angle and
the palette fade timer — none of them `Anim_Counters`. **No finding.**

---

## 13. SEVERITY: defect — `TestS3kLrzSeamlessActChangeHeadless`: two assertions pass vacuously, and the one weakening that hides something real

The test is not a rubber stamp — `assertEquals(1, after.actIndex())`,
`assertTrue(sawArmedStage)`, the in-loop `assertEquals(0, now.eventsFg5())`, the
trigger-array clear and the `maxX` equality all have teeth. Specifically the
trigger assertion is real: `Sonic3kLevelTriggerManager.reset()` is otherwise
only called from `Sonic3kGameModule.onLevelLoad()`
(`Sonic3kGameModule.java:520-525`), which is a full-load-profile hook that
`loadActTransitionLevelData` never runs.

Three problems:

**(a) vacuous — `assertEquals(0, after.backgroundRoutine(), "clr.w (Events_routine_bg)...")`.**
`after` is a brand-new `LrzZoneRuntimeState` created by
`installZoneRuntimeState` (`Sonic3kLevelEventManager.java:516-518`) during
`initLevelEventsForCurrentZoneAct`, whose `backgroundRoutine` field defaults to
`0`. Deleting `state.setBackgroundRoutine(0)` from
`LrzActTransitionHandoff.java:55` cannot fail this test. The same is true of
`setEventsFg5(0)`, `setAct2ArtJobOrdinal(-1)`, `setRocksRoutine(0)` and
`setRocksWindow(0,0)` on lines 52-56 — all five writes land on fields that are
already at those values. **Change:** assert the handoff by dirtying the *new*
state's fields before the handoff runs (a test hook, or a `@Test` on the
handoff record with a pre-dirtied state), or accept that the ROM's clears are
unobservable here and delete the assertion rather than let it read as coverage.

**(b) vacuous — `assertTrue((short) fixture.camera().getX() < 0x0200)` and, separately, the `minX` equality.**
The test writes `setMinX($2C00)` and `setMaxX($2C00)`, so
`postTransitionMinX == postTransitionMaxX == 0`. With the live bounds collapsed
to a single point the camera is pinned to X=0 by the clamp on the next update
**whatever `cameraOffset` did**, so the camera-X assertion cannot fail. And
`(minXBefore - REBASE_X) & 0xFFFF == 0` is indistinguishable from LRZ2's own
level `minX`, which `restoreCameraBoundsForCurrentLevel` (`LevelManager.java:3835`)
would install if `postTransitionMinX` were deleted. The `maxX` assertion is the
only one of the four that survives deletion of the builder call, because LRZ2's
level `maxX` is not 0.

**(c) the weakening that hides something real —
`assertTrue((player.getCentreX() & 0xFFFF) < 0x0200)`** in place of
`assertEquals((playerXBefore - REBASE_X) & 0xFFFF, ...)`. The comment blames
"act 2's left boundary", but with `minX` forced to 0 there is nothing to clamp
against, so the exact value should hold. More importantly, a range check at the
same left edge is exactly what cannot distinguish *the player was moved by
`$2C00`* from *the player was moved by roughly `$2C00`*, and it is the
assertion an agent would reach for after fitting rather than deriving the
constant. **Change:** restore exact equality, and if it then fails, that failure
is the finding.

**(d) the test cannot see finding 1 at all.** There is no assertion that any
carried object moved, and no assertion that `ArtKosM_LRZ2_Secondary` landed at
tile `$090` — the two things the ROM lines `:115365` and `:115286-115287`
specify and the two things the implementation gets wrong or leaves unverified.
**Change:** spawn or locate one live world-space object before signalling and
assert its centre X moved by exactly `-$2C00`; assert one pattern at tile `$090`
differs from its pre-change value.

**(e) note on the cited measurement.** The comment says "the measured pair is
`($2C00,$710)`" and then writes `minX = maxX = $2C00`. A `maxX` of `$710`
below a `minX` of `$2C00` is not a camera bound pair, and neither number
reaches the test as written. Whatever was measured, the values the test uses
are not it — either cite the measurement that produced `$2C00/$2C00` or drop
the sentence. (Per the memory rule: a measured fact needs the commit it was
measured at.)

**(f) `theArmedStageIsTheRomsOwnIndexEntry`** asserts a test-local constant
equals the production constant. It pins `0x0C` against accidental edits, which
is worth something, but it is not evidence about `LRZ1_BackgroundEvent_Index`;
the index's fourth entry at sonic3k.asm:115270 is what makes `$C` right, and no
test reads the ROM. Leave it, but do not count it.

---

## 14. SEVERITY: note — things I checked and found correct, one line each

- `ObjectSurvivalPolicy.ALL_LIVE_SST` is right: `Load_Level` does not clear
  `Dynamic_object_RAM` (sonic3k.asm:38747-38761), so every live SST genuinely
  survives. (The comment at `LevelManager.java:3916-3918` claiming "ROM
  `Load_Level` clears `Dynamic_object_RAM`" is wrong, but it predates this commit
  and only guards `forceAirOnStaleObjectSupportLoss`, which LRZ correctly omits.)
- `deferRingInitializationToLevelUpdate` is not needed: `LevelActTransitionExecutor.java:213-215`
  already passes the **post-offset** camera X to `rebuildManagersForActTransition`,
  so `ringManager.reset(cameraX)` (`LevelManager.java:4043`) windows on act-2
  coordinates.
- `preserveOffsetCameraPosition(true)` is right — it suppresses
  `cam.updatePosition(true)` at `LevelActTransitionExecutor.java:230-232`, which
  would re-centre on the player and undo the explicit ROM write.
- `preserveMusic(true)` / `preserveLevelGamestate(true)` /
  `showInLevelTitleCard(false)` / `deactivateLevelNow(false)` match all three
  precedents.
- `LrzZoneRuntimeState.act2ArtJobOrdinal` is declared `long` in the accessors
  and stored as `int` (`LrzZoneRuntimeState.java:76,272-279`); ordinals are
  session counters so the narrowing is safe in practice, but the signature says
  `long` and the field says `int` — pick one.
- `applySecondaryArt` (`LrzActTransitionHandoff.java:87-104`) uses
  `Arrays.copyOfRange` past the end for a non-multiple-of-32 payload, which
  zero-pads silently rather than throwing. Cosmetic.

---

## Questions I could not answer

- **None outright**, but two answers are bounded by "no build was run":
  - Finding 1 is read from the code paths, not observed failing. I could not run
    `TestS3kLrzSeamlessActChangeHeadless` to show a carried object stranded at
    act-1 X, because the task forbids Maven. The code path is unambiguous
    (`offsetCarriedObjectsForTransition` reads `playerOffsetX()`, which is 0), but
    the failing observation is owed.
  - Finding 13(b)'s claim that LRZ2's level `minX` is 0 is inferred from act-2
    starting at low X after a `-$2C00` rebase; I did not decode the LRZ2 level
    size entry. If LRZ2's `minX` is non-zero, that assertion is not vacuous —
    the reasoning for `maxX` is unaffected.
