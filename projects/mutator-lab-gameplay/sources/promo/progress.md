# Mutator Lab gameplay promo — progress (opus_gameplay_promo_r1)

Run e0603654-55a0-4717-897c-3d93d1137ff3 · workspace `.worktrees/ai-mutators-gameplay-promo`
(branch `feature/ai-mutators-gameplay-promo`, base 3d0a47bdc).

## What the prior films taught (frames inspected: review-prior/sheet-1..5.png)

- Rejected expanded reel (sheet-5): a slide deck. Title card, three title screens,
  ten option pages with side-panel prose, standing Sonic, static 0/25/50/100/150 head
  grids, outro card. Effects (Ringfall, Violent Explosions, Gravity, No Rings) were
  only *described*. Nothing makes you want to play.
- Post Two Ambush (sheet-2) works: the game frame is always the subject, one 2–4 word
  action caption under it ("Watch the tell", "Locked — move!", "Too slow…"), a 6x
  REPLAY close-up for the key moment, retry/fail as story.
- Sitar Hero (sheet-1): every shot moving, one-line caption bar, variety across games.
- Multigame (sheet-3): a single strong idea shown visually (three worlds, one pad).
- Earlier mutators promo (sheet-4): matched native-vs-mutated jump is the right
  instinct; the kill was too small to read.

## Selling points to SHOW (not caption)

1. Chaos you can dial: drop *every* ring you carry (new full-inventory Ringfall) and
   chase the storm back up while a ring-scaled Big Head shrinks and regrows.
2. Badniks become launch pads: Violent Explosions multiplies the native defeat rebound
   — chain kills through an enemy-dense stretch.
3. Stack them: low gravity + amplified rebound + big head = absurd soaring arcs;
   matched native-vs-mutated contrast from the same input.
4. Live tweaks: pause, slide a value, Resume, the very next jump changes; switch off.
5. Challenge variants: No Rings via a real act restart (LOAD scope) — the ring lines
   are gone and one hit is fatal.
6. Real Sonic 1, 2 and 3&K from your ROMs, native music/SFX.

## Storyboard (target ~60–75 s, ≥80 % moving gameplay)

| # | Beat | Game/area | Content | Menu? |
|---|---|---|---|---|
| 0 | Cold open | S2 EHZ1 | the full-inventory spill burst at its peak (2–3 s) | no |
| 1 | Title | over moving ring storm | "MUTATOR LAB" + "11 mutators · Sonic 1·2·3&K" (≤2 s) | no |
| 2 | Grow | S2 EHZ1 real route | real collection montage, HUD 10→100, head grows to 200 % | no |
| 3 | Pop | S2 EHZ1 | real hit at ~100 rings → every ring bursts out, head snaps small | no |
| 4 | Regrow | S2 EHZ1 | scramble through the storm, HUD climbs, head swells | no |
| 5 | Contrast | matched | native 32 vs full inventory (same input), labelled | no |
| 6 | Explosions | densest badnik stretch found by probe | approach / hit / launch ×N, then kill chain | brief insert: 300 % slider |
| 7 | Stack | S2/S1 | low gravity + rebound + head: native vs mutated from the same input | no |
| 8 | Live toggle | any | pause → gravity slider → Resume → floaty jump → back to 100 % | quick |
| 9 | Challenge | S1/S3K | No Rings → Restart → ring lines gone → one hit = death | quick |
| 10 | Outro | moving | short end card over gameplay | no |

## Feasibility notes / blockers found

- **Display-free capture**: GameplayCaptureTool's HeadlessGameBoot creates a hidden
  GLFW window, which needs DISPLAY/WAYLAND (forbidden). Xvfb is not installed.
  GLFW's null platform cannot find an EGL window config on Mesa surfaceless.
  Verified a direct surfaceless-EGL pbuffer context via LWJGL's generic JNI
  (`tools/egltest/EglJni.java`, no display env): radeonsi GL 4.6 core, GL_BACK
  readback OK. Plan: opt-in `-Dopenggf.headless.gl=surfaceless-egl` in
  HeadlessGameBoot that fails closed (never falls back to a display).
- **Uncapped Ringfall**: the 32 ceiling is in `RingManager.LostRingPool`
  (`Math.min(ringCount, MAX_LOST_RINGS)`), the coordinator basis
  (`Math.min(held, 32)`), the 32-entry mirror and the deferred-queue reservation.
  Plan: explicit `fullInventory` component (default false, compat ctor) on
  `MutatorPolicy.Ringfall` + GameplayMutatorPolicy; extras beyond the native 32
  run as existing slotless logical Obj37 continuations (never claim native SST
  slots), latched with the count in the deferred queue + rewind snapshot; extra
  48-ring cycles interleave between native fan angles so they do not stack.
  Limits: S3K's native 63-entry Collision_response_list still bounds per-frame
  touch candidates; touch still collects one ring per frame (native rts).
- Ring budget: S2 EHZ1 full-run BK2 (trace fixture input) collects 102 rings
  hit-free (10 @ f1065 … 100 @ f4732, x=$283F). Plan: replay it input-only with
  Big Head (presentation-only) then author the hit/recollection continuation.

## Log
- 2026-10-10 00:3x UTC: prior films inspected; storyboard written; implementation next.
- 2026-10-10 ~00:40 UTC: full-inventory Ringfall + surfaceless EGL implemented; focused tests green.
- ~01:00–01:40: routes found by CSV-first sweeps (GHZ monitor chain + Motobug hit; SYZ five-stomp chain;
  S2 live gravity; S3K No Rings restart; S3K stacked finale). EHZ1 trace BK2 rejected (desync at row 153).
- ~01:45: commits f5650a144, 964d8210b (hooks passed); finals re-shot from clean head 964d8210b.
- ~02:30: edit rendered; fixes during verification: concat duplicate frame (separate video/PCM concat,
  setpts CFR), engine framebuffer alpha (flatten to RGB). Final 52.22 s; 0 cadence mismatches; 0 ms A/V lag.
  Result: promo-result.md / promo-result.json.
