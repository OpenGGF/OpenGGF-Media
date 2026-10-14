# Mutator Lab gameplay promo — result (opus_gameplay_promo_r1, run e0603654)

## Deliverables (absolute root `/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3`)
- `out/mutator-lab-gameplay-promo.mp4` — 52.22 s, 1920×1080 60 fps CFR (3133 frames), H.264 High
  yuv420p, AAC-LC 48 kHz stereo 192k, faststart, 8 embedded chapters, −16.8 LUFS integrated.
  46,156,939 bytes, SHA-256 `4a6eef10d51dd6e0412c9e2bc2c2f470dde4b05b7b02e33db45dd94082a17a97`.
- `out/mutator-lab-gameplay-promo-thumb.png` (1280×720, the 173-ring burst), SHA-256 `9ce533c7…0f62f`.
- `out/chapters.json` — edit map: every segment's take, exact source frame range, captions, chips.
- `out/verify-cadence.json`, `captures/final-audit.json` — verification evidence.
- `recipe/README.md` + `recipe/build_promo.py` — reusable shoot/edit/verify recipe.
- `captures/final-*` — the seven source takes (PNG per frame, `audio.wav`, `state.csv`,
  `observe.csv`, `badniks.csv`, `input.txt`, authored script, preference seed, receipt).
- The rejected expansion reel is untouched in its own task root.

## What the film shows (all moving native gameplay; menus only as cause → effect)
| t (s) | Beat | Evidence from native owners (`observe.csv`) |
|---|---|---|
| 0–3.5 | Cold open: 173-ring burst (S1), 300% stomp into the sky (S1), 211-ring burst (S3K) | see beats below |
| 3.5–5.5 | Title over S3K 25%-gravity soar | — |
| 5.5–15.5 | **Ringfall full inventory + ring-scaled Big Head** (S1 Green Hill): in-take Lab edit toggles *Drop full inventory* → Resume; three monitor bounces bank 143→173 rings; a Motobug hit; 173 real rings burst out; head drops to 100%; Sonic scrambles back to 52–57 rings as the head regrows to 152–157% | policy flips at f203; hurt f711: held 173, spilled 173 (32 slotted + 141 slotless); head 200→100→157%; final 57 rings |
| 15.5–17.5 | Matched contrast, same input: native spill 32 vs full inventory 173 | native take hurt f527: spilled 32, recollected 13 |
| 17.5–29.5 | **Violent Explosions** (S1 Spring Yard): in-take edit 150→300%, cap 12→16 px/tick → Resume; five chained badnik stomps (3 Crabmeats, 2 Buzz Bombers), each a −16 px/tick launch, combo 100/200/500/1000/1000 = 2800 | policy f246 = 300%/4096; kills f383/526/678/819/972, y_vel +1416…+4416 → −4096 |
| 27.5–29.5 | Matched contrast: native bounce vs 300% bounce from the same stomp | native kill f136: +1416 → −1472 |
| 29.5–37.8 | **Live toggle** (S2 Emerald Hill): normal jump → Gravity on, slider 100→25% (“Saved. Applies when you choose Resume”) → moon jump mid-run → switch off → normal jump | gravity 25 admitted f346, back to 100 f694; jump apex ~56 px vs ~300 px |
| 37.8–43.4 | **LOAD scope challenge** (S3K Angel Island): rings collected → No Rings (“Pending restart or death”) → Restart from act start → the same slope reloads without rings → zero-ring Rhinobot hit is fatal | restart at ~f540; 0 rings thereafter; dead f1364 |
| 43.4–49.9 | **Stack everything** (S3K): Lab list with Gravity 25%, Ringfall full, Big Head, Violent Explosions active → soar → Rhinobot → 211-ring burst → scramble | hurt f752: held 211, spilled 211 (32 + 179 slotless) |
| 49.9–52.2 | Outro card over moving Green Hill play | — |

Runtime: menus 7.4 s (14%); moving gameplay 85% including the title/outro cards drawn over
moving play (77% excluding them). Breadth: Sonic 1 (Green Hill, Spring Yard), Sonic 2 (Emerald
Hill), Sonic 3 & Knuckles (Angel Island). Audio is each take's own native music/SFX/menu cues.

## Source change (worktree `.worktrees/ai-mutators-gameplay-promo`, HEAD `964d8210b`, clean)
- `f5650a144 feat(mutators): let Ringfall drop the full inventory` — default-off LIVE checkbox;
  `MutatorPolicy.Ringfall.fullInventory` (+ compat ctor, pin +3 additive entries);
  `GameplayMutatorPolicy.ringfallFullInventory`; coordinator latches count + beyond-native flag
  (deferred queue + rewind snapshot); first 32 rings keep native slots/order, the rest are real
  slotless Obj37 continuations bounded by the 999 counter; extra 48-ring fan cycles rotate.
  Engine seams via unannotated `RingManagerInternalAccess` (no `RingManager` API growth).
  Docs: example README, modding guide, compatibility notes, validation matrix, dated plan, 0.7 changelog.
- `964d8210b feat(tools): render offscreen captures without a display connection` — opt-in
  `-Dopenggf.headless.gl=surfaceless-egl` (Mesa surfaceless EGL pbuffer, GLFW null platform),
  fails closed; default hidden-window path unchanged; tools/media README + gameplay-capture skill.
  Needed because Xvfb is absent and the existing capture boot required a display connection.

Focused validation (queued, `-Dmse=off`, ROM paths supplied, 0 skips):
118 tests green — `TestLevelRingfallIntegration`, `TestLevelLostRingSpawnCoordinator` (31/31 also
isolated), `TestSurfacelessEglContext`, `HeadlessGameBootTest`, `TestHeadlessGameBootAudioIdentity`,
`TestHiddenGlCaptureSessionFailureCleanup`, mandatory `TestS3kAiz1SkipHeadless`,
`TestSonic3kLevelLoading` (both), `TestSonic3kBootstrapResolver`, `TestSonic3kDecodingUtils`; earlier
run of the same tree: `TestMutatorExpandedPolicies`, `TestModApiSignatureSurface`, `TestModApiPinPolicy`,
`TestExampleMutatorsPackage`, `TestLostRingObjectInstance`, `TestLostRingRewindGenericRestore`,
`TestLostRingTouchOrdering`, `TestRingManager`, `TestRingManagerRewindSnapshot`. This is focused
validation, not a broad/full run. Stock behavior is unchanged by construction (beyond-native branches
unreachable without the option); recommendation to root: the change-based category run for PR215
should include these categories plus guards; no full suite launched here.
Pre-existing hazard found and fixed in the test fixture: `TestLevelLostRingSpawnCoordinator` erred
31/31 in isolation (its `setUp` relied on a gameplay runtime left by an earlier class).

## Authenticity and disclosed setup
- Input-only: authored controller scripts; no state writes during a take. Physics/inventory/kills/
  policy are read from native owners. Policies were admitted through the real Lab menu (Resume) in
  the hero, chain, live, No Rings and finale takes; seeded preference files set only the starting
  choices. The in-take menu versions reproduce the seeded runs exactly, shifted by the pause length
  (hero: +184 frames, same 173-ring spill, same 57 final; chain: +247 frames, same five kills).
- Disclosed on screen: Green Hill takes start positioned at (0x1180, 0x300) with **140 carried-in
  rings** (33 collected on camera → 173); the S3K finale starts at the act start with **200
  carried-in rings** (11 collected → 211). Spring Yard, Emerald Hill and the No Rings take start
  at the act start with no seeding.
- A recorded EHZ1 trace BK2 was tried for a fully real ring budget and rejected: it desyncs at trace
  row 153 under a fresh boot (Coconuts encounter differs), so it was not used.
- Captions describe only what is shown; Game Speed is not depicted (the capture tick is canonical).

## Verification
Full `-xerror` decode clean; every cut boundary inspected; 117 sampled game-area crops match their
exact source frames (0 mismatches, after flattening the engine framebuffer alpha that otherwise
exposed the blurred margin during the S3K restart fade); audio cross-correlation vs the exact
frame-locked PCM: 0 ms lag at 9 windows (corr ≥ 0.998); CFR 60/1 with 3133 frames.

## Limits
- Full-inventory spill: touch still collects one ring per frame (native); S3K's native 63-entry
  collision-response list still bounds touchable spilled objects per frame (S3K recollection 26 of 211).
  S1/S2 truncation on native slot exhaustion still applies to the first 32.
- `tools/media` surfaceless path is Linux/Mesa; promo captures used the iGPU radeonsi driver.
- Observed tool issue (not fixed): `GameplayCaptureTool --zone` S1 names map to the wrong zones
  (`lz`→Marble, `mz`→Spring Yard, `slz`→Labyrinth, `syz`→Star Light: ROM zone ids used as engine order).
- Scratch probes (`tools/driver` PromoCapture/LayoutProbe, sweep, audit) are not promoted into the repo.

## Parent acceptance

The replacement footage was reviewed against the native CSVs and actual encoded frames. The root corrected one caption to “No rings. One hit is fatal.” because the scene shows a death with lives remaining. All source ranges, native PCM, menus and gameplay are unchanged. The revised output decoded fully (exit 0), with 3,133 video frames at 60 fps, 48 kHz stereo and eight chapters. The original edit remains under `out/review-r1/`. Root source follow-ups passed 43 focused tests without skips and SDK artifact verification; normal broad validation remains pending.
