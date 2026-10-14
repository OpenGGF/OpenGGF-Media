# Expanded Mutator Lab promo — opus_expansion_promo_r1

Provider: Claude Opus 5.5, no rate limit encountered. Media-only stage.

## Deliverables
- Video: `out/mutator-lab-expanded-promo.mp4` — 81.4 s, H.264 High 1920x1080/60 yuv420p,
  AAC-LC 48 kHz stereo 192k, faststart, 26.6 MB, SHA-256 `2d10f259…7d6e34`.
- Thumbnail: `out/mutator-lab-expanded-promo-thumb.png` (1280x720, S1 0 vs 100 rings head).
- Chapter/segment manifest: `out/chapters.json` (source capture + frame range per segment, per-segment RMS).
- Recipe: `recipe/build_promo.py` (`python3 -I recipe/build_promo.py`, ffmpeg/magick only, ~80 s).

Absolute root: `/home/farrell/scratch/agent-tmp/codex/mutator-lab-expansion-5c24f4a5-76e8-47c7-bc47-4173173d5caa/opus-expansion-promo/`

## Timeline
| Start | Chapter | Content |
|---|---|---|
| 0:00 | Intro | Title card over blurred S3K title, AIZ music |
| 0:03.5 | Three games | S1, S2, S3K title-screen Mutator Lab hub (native audio) |
| 0:11 | Catalogue | Live Gravity slider edit, then all 10 other native option pages, one caption each naming the effect + scope |
| 0:30 | Native play | S1 GHZ Big Head fixed 150% |
| 0:34.6 | LIVE vs LOAD | Play held → Stealth / Game Speed edits → Resume (Sonic hidden) → Load: Restart |
| 0:48 | Sonic 2 | EHZ Big Head, Stealth |
| 0:55 | Sonic 3 & Knuckles | AIZ Big Head + stock ball fallback; Stealth hides leader, Tails visible |
| 1:02 | Ring-scaled head | 3 games × (off, 0/25/50/100/150 starting inventory = 100/125/150/200/200% clamped), then S3K rings earned in play 0→11 with LIVE menu "111% at 11 rings" |
| 1:17 | Outro | Defaults off · LIVE on Resume · LOAD on restart · JVM boot-prepared jar · your ROMs |

Pixels: 4x nearest-neighbour (grid crops 3x). All 11 names appear on screen.

## Verification
- `ffprobe`: as above, 4882 video frames; full `ffmpeg -xerror -f null` decode exit 0.
- Loudness −15.4 LUFS, peak −1.4 dBFS (edit-level loudnorm only; no product audio change).
- Frames inspected: first (title fade-in), middle 40.7 s (S1 Stealth, HUD running), last (outro),
  every segment midpoint, plus post-fix S2 grid and S3K earned-rings frames. The first render showed
  a missing "→" glyph and HUD in the S2 crop. Both were fixed and re-rendered before these checks.

## Provenance and identity
- Final source `1136bf343f57` (verified clean HEAD, read-only). Build tree `345ec13b2`, not rebuilt.
  Creator jar re-hashed `a77d49b2…428f9d56`.
- No new captures. Footage comes from retained Opus R3 offscreen GameplayCaptureTool runs:
  - ring-head/title captures used the final jar a77d49b2 and the engine classes from
    7655c0d8 plus 27 dirty polish files;
  - play-03/explore-04 used jar eadb858e and 7655c0d8 plus 14 dirty files.
  - Neither is relabelled as a compiled-1136 run.
- Rejected: s2-explore-01-badnav and all desktop window captures (historical). Cue clips were used
  only as SFX evidence.

## Scope honesty
Shown on screen: three-game hub, catalogue, fixed Big Head, stock fallback on curled art,
LIVE Resume, Stealth in all three games, LOAD restart, and the ring-scaled head (starting
inventory labelled as inventory, plus real in-play collection).

Captions only, using the native option page: Gravity's effect in play (play runs used 100%),
Ringfall, No Powerups filtering, No Checkpoints, No Rings, Game Speed (the capture tool runs one
tick per frame, and the caption says so), No Special and No Bonus Stages (the S1 page shows
Unavailable), Violent Explosions, and ring-loss shrink.

Audio is the captures' own native PCM. Menu SFX contribution comes from the polish authored-vs-neutral
PCM controls. In the promo the cues sit under the music. One confirm transient was measured
(`work/s1-live-press-rms.json`). No speaker, hardware input or window claims.

## Processes and cleanup
- All ffmpeg/magick runs were foreground and have exited. No ffmpeg or GameplayCapture processes
  remain. No JVM, display, sink or watcher was created.
- Intermediates were deleted. Kept: recipe, outputs, inspection sheets (`work/sheets`) and the
  RMS json. No cleanup blocker.
- No PR, push, source, test or main changes. Root owns the PR215 update.
