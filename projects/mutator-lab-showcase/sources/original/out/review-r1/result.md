# Mutator Lab — complete gameplay showcase (task mutator-complete-showcase-20261010)

Root: `/home/farrell/scratch/agent-tmp/claude/mutator-complete-showcase-20261010`

## Deliverables
- `out/mutator-lab-complete-showcase.mp4` — 90.217 s, 1920×1080, H.264 High yuv420p, 60/1 CFR (5,413 frames,
  every PTS delta 256/15360), AAC-LC 48 kHz stereo 192k, faststart, 14 chapters, loudnorm −16 LUFS.
  86,523,685 bytes, SHA-256 `2eef605bcfb9097b84036f1f2e76ed3c7ba7074add00ecd1638bfea2a9d5fb4f`.
- `out/mutator-lab-complete-showcase-thumb.png` (1280×720, outro card listing all 11), SHA-256 `83a4a529…cbfa`.
- `out/chapters.json` — every segment: take path, exact frame range, crop, audio sample range, captions, chips, menu flag.
- `out/verify.json` — verification evidence. `recipe/build_showcase.py` + `recipe/README.md` — reproducible edit.
- New source takes: `captures/final-*` (11 takes: PNG per frame, `audio.wav`, `state.csv`, `observe.csv`,
  `observe2.csv`, `badniks.csv`, `monitors.csv`, `input.txt`, authored script, prefs seed, `receipt.json`).
- Accepted 52 s film and all seven prior final takes are untouched (read in place from the e0603654 root).

## Structure (menus 12.6 s = 14%; everything else moving native play)
| t (s) | Chapter | Source |
|---|---|---|
| 0–6.1 | Cold open: 173-ring burst, invisible Sonic, double speed, 300% stomp, 211-ring burst | old + new |
| 6.1–8.6 | Title over S3K stacked soar | old |
| 8.6–20.1 | Ringfall full inventory + ring-scaled Big Head, native 32 vs 173 split | old (unchanged ranges) |
| 20.1–31.4 | Violent Explosions 300% five-badnik chain + native split | old |
| 31.4–39.7 | Gravity live toggle 100→25→off | old |
| 39.7–48.6 | Game Speed: 100% run → Lab on/200%/audio follows → 2 ticks/frame; 50/100/200 trio | new |
| 48.6–55.2 | Stealth over fixed 200% Big Head: on → invisible rings + Masher → off | new |
| 55.2–61.1 | No Powerups: per-type, only Invincibility checked → real restart → split | new |
| 61.1–66.7 | No Rings restart (caption "No rings. One hit is fatal.") | old |
| 66.7–71.2 | No Checkpoints: post → death → post; on → death → act start | new |
| 71.2–76.1 | No Special Stages (S1 giant ring) stock vs switched off | new |
| 76.1–80.8 | No Bonus Stages (S3K only) stock vs switched off | new |
| 80.8–87.2 | Stack everything finale | old |
| 87.2–90.2 | Outro card, all 11 names, “bonus stages exist only in S3&K” | old frames |

## Eleven-row coverage (native observations; frames are source-take frames)
| Mutator | Game / take | Visible native change | Proof (CSV / frames) |
|---|---|---|---|
| Gravity | S2 EHZ1 `final-s2-live` (old) | jump apex ~56 px → ~300 px at 25%, back after off | observe.csv gravity_pct 100→25 f346, →100 f694 |
| Ringfall | S1 GHZ1 `final-ghz-hero` (old) | full inventory 173 spilled vs native 32 | hurt f711 lost 173 (32 slot + 141 slotless); native take 32 |
| Big Head | old hero (ring-scaled 200→100→157) + new `final-stealth` (fixed 200%) | head scales with rings / fixed large head | old observe head_scale; new observe2 head_scale 200 throughout |
| Stealth | S2 EHZ1 `final-stealth` | body+head invisible, rings/HUD/kill still happen; returns when off | observe2 stealth_body true f269–672, false f862; rings 0→8 f451–555, Masher score 100 f536; menu R f152/f745 |
| No Powerups | S1 GHZ1 `final-np` | Invincibility monitor (0x5D6) gone after restart; ten-ring monitor (0x248) remains | run 1: ring monitor powerup f183, invincibility powerup f396; menu check f784, restart A f936; run 2 removed=[INVINCIBILITY], ring powerup f1240, 0 monitor rows at x=1494 after f1000 (244 before) |
| No Checkpoints | S3K AIZ1 `final-nc` | 1st death respawns at the post; after switch-on, 2nd death reloads act start | cp2 f50; dead f173, lives 3→2, respawn (0x2778,0x25C) f325; no_checkpoints LOAD admitted at death reload; dead f653, lives 2→1, reload (0x13A0,0x41A) cp −1 f805 |
| No Rings | S3K AIZ1 `final-aiz-norings` (old) | ringless hill after restart; zero-ring hit fatal (lives remain) | old observe rings 0 after restart, dead f1364 |
| Game Speed | S3K AIZ1 `final-speed-*` (interactive pacing) | 2 native ticks per presented frame at 200%; 0.5 at 50%; HUD time diverges | observe2 level_frame per presented frame: 50% +0.5, 100% +1, 200% +2; live take lf 220 frozen in menu, +2/frame from f616, speed 200 audio_follows true; pcm 800/frame all |
| No Special Stages | S1 GHZ1 `final-ss-stock` / `final-ss-deny` | stock: giant ring flash → S1 Special Stage; off: pass through, act clear, GHZ2 | stock mode SPECIAL_STAGE (Sonic1SpecialStageProvider) f1364; deny no_special true f203, never SPECIAL_STAGE, TITLE_CARD f1559, GHZ2 LEVEL f1710 |
| No Bonus Stages (S3K only) | S3K AIZ1 `final-bonus-stock` / `final-bonus-deny` | stock: bonus stars → Slot Machine; off: no bonus stars spawn, keep running | stock log "Requesting bonus stage entry: SLOT_MACHINE", BONUS_STAGE f317; deny no_bonus true f193, post cp2 f234, never BONUS (starpost `shouldSpawnBonusStars` refuses spawn) |
| Violent Explosions | S1 SYZ1 `final-syz-chain` (old) | −16 px/tick stomp launches vs native −1472 | old observe rebound 300/4096, five kills |

Combinations shown: Big Head 200% fixed + Stealth (Stealth hides the head); Game Speed 200% + audio follows;
per-type monitor selection; old Ringfall full + ring-scaled head; old four-way S3K stack; LIVE (Resume) vs LOAD
(restart/death) boundaries both on screen.

## Disclosed setup (also on screen)
- Positioned starts (declared before input): S1 GHZ1 (0x2100,0x370) + 50 rings (special); S3K AIZ1 star-post ledge
  (0x2740,0x250) + 25 rings (bonus) / 0 rings (No Checkpoints). Old: GHZ hero 140 rings, S3K finale 200 rings.
- Stealth, No Powerups and the Game Speed takes start at the act start with no seeding.
- Settings: preference seeds set only starting choices (Big Head 200% fixed; No Powerups all unchecked & off;
  speed 50/100/200 for the trio). Every toggle shown in film was made in-take through the real Lab menu.
- Natural entry: both stage entries are natural native touches (giant ring / bonus stars) after a positioned start;
  no explicit production entry request was used. Already-admitted-permit behaviour was not filmed.
- Game Speed method: scratch adapter steps `GameLoop.stepPresentationFrame()` once per presented frame with keys
  through the production `InputHandler` (no logical override), Engine fade/audio order
  (`Engine.presentOuterAudioFrame`), one PNG + 800 PCM frames per presented frame. No retiming. Other new takes use
  the canonical one-tick-per-frame path identical to `MutatorGameplayCaptureTool` (extra observation columns only).
- Special Stage frames: `GameplayCaptureSession` draws only level planes in SPECIAL_STAGE, so the adapter applies
  Engine.drawSpecialStage's order (screen-space camera origin, stage viewport, provider draw) — presentation only.

## Verification
- Full `-xerror` decode exit 0; 5,413 frames = chapters total; CFR 60/1, single PTS delta.
- 243 game-area crops (every panel, 3 per segment) matched exact source frames: 0 mismatches.
- Pre-loudnorm edit PCM equals the selected source sample ranges for all 76 segments (4,257,288 stereo frames,
  excluding 481-frame boundary fades); 800 PCM frames per presented frame in every take.
- AAC vs pre-loudnorm cross-correlation: 0 ms lag at 12 windows, corr ≥ 0.998.
- Every new segment's first/middle/last output frame inspected (work/fa.png, fb.png, fc.png).
- Determinism: each final take reproduced its exploratory candidate byte-for-byte (state/observe2/audio).

## Provenance / process
- Source: `.worktrees/ai-mutators-complete-showcase` @ `379b6641323853f61851943fb7aadd5e7a389e01`, clean;
  build-only `examples/example-mutators/build.py`; jar SHA-256 `9e5cdddab1ac…5fb3` (matches prior); no engine tests run.
- Display-free: DISPLAY/WAYLAND_DISPLAY/XDG_SESSION_TYPE/XAUTHORITY unset, `-Dopenggf.headless.gl=surfaceless-egl`,
  ALSOFT null, isolated saveRoot/user.dir per take, original ROMs by absolute path.
- 75 bounded capture JVMs, all exit 0, recorded (PID/start ticks/argv) in
  `~/.local/state/temporary-agents/mutator-complete-showcase-20261010/manifest.json` (state completed); none running.
- Adapter: `tools/driver/src/com/openggf/tools/ShowcaseCapture.java` (class SHA-256 `efc80db8…e806`), scratch only;
  root may consider promoting the paced mode + special-stage render as a maintained capture option.

## Limitations
- Speed "audio follows" is evidenced by the admitted policy and a zero-crossing proxy (≈1.6× higher), not a pitch analysis.
- The S3K bonus-star difference is small on screen (tiny orbiting stars); the caption and split labels carry it.
- S1 stock giant-ring results card shows zero bonuses before the Special Stage (engine behaviour, cut past).
- Exploratory captures pruned to CSV/scripts; lessons in recipe/README.md.
