# MICA & TALON production promo — draft checkpoint (2)

Draft: `checkpoint2/draft-16x9.mp4` — 95.37 s, 1920×1080, 60 fps, H.264 High, yuv420p, AAC LC 320k 48 kHz,
7 chapters (MP4 chapter track), full decode `ffmpeg -xerror` exit 0. Edit: `edit/edit.py`. Branch
`feature/ai-mt-promo-production` @ `b088fae95b` (no tooling changes to the repo).

## Lead review 1 → changes

1. Lock-up: "MICA & TALON" in Fira Sans Compressed Heavy, white caps, 1/14-size navy outline, hard shadow, +tracking,
   yellow "&", on the S2-card band (red tab, yellow strip) with motion in/out; title drop and end card. The band on
   the title drop now runs full width so the native menu rows are covered whole. Chapter headers use the same face
   (the card glyphs broke "HOMING"/"TALON" the same way).
2. Half-pipe: new neutral-steer take `captures/halfpipe-run` (MICA leads, TALON behind, centred) from src 740 at
   1.0× so the pipe curve and the turn read; Blue Sphere unchanged. Every split, triptych and grid cell checked on
   frames for its subject.
3. Cold open: the stock-art Tornado is on screen at x<~80 for title src 412–510 (sprite diff). The camera pushes to
   1.6× on MICA's face with the left edge ≥ x96 by src 408 and holds through the wink, so it never enters.
4/5. S1 results fault and the Competition/reels omission go into the provenance limits (below; README at final).
6. S2 homing: one clean lock-on strike — now in **Aquatic Ruin** (Whisp, `captures/arz1-whisp-a`).
7. Stingers re-levelled; `check` and measurements below.
8. Variety: ARZ homing close-up (bars 16–19) and **Chemical Plant** TALON flight (top strip, bars 24–27) replace
   the two EHZ shots. Carry is now a 2.0× crop with HUD and lives fully out.

## `promo_kit.py check`

```
pacing: {'shots': 19, 'mean_shot_s': 5.02, 'busiest_window_cuts': 5, 'cuts_in_last_window': 2,
         'seconds': 95.37, 'longest_bare_s': 0, 'busiest_window_captions': 0}
```
No warnings (stinger-balance and bare-stretch checks included).

## Loudness (measured on the encoded AAC, ffmpeg `ebur128=peak=true`)

- Whole film: **−14.0 LUFS integrated, true peak −2.5 dBTP, LRA 2.2 LU** (two-pass linear loudnorm; no limiter needed).
- Sections: 0–11.15 s −14.7 LUFS / −3.4 dBTP · 11.15–39.02 −14.3 / −2.5 · 39.02–65.50 −13.6 / −4.2 ·
  65.50–89.18 −14.0 / −2.7 · 89.18–95.37 −13.3 / −3.1. No step larger than 1.1 LU across chapter boundaries.

## Stingers (level vs bed under it, over the stinger's active length; all centred, L−R 0.0 dB)

| Out frame | Event (source frame) | ROM SFX | vs bed |
|---|---|---|---|
| 334 | title-drop flash (graphic punctuation) | S3K $B3 Big Ring | −6.8 dB |
| 734 / 751 / 773 / 942 | MGZ2 kills: hero-mgz2 #65/#82/#104/#273 (score change + yvel −1280 rebound) | S3K $B4 Explode | −7.0…−7.6 |
| 1043 / 1053 | S1 GHZ2 chain #60/#70 (score 100→300) | S3K $B4 | −7.5 / −7.3 |
| 1127 | S2 EHZ2 strike #281 | S2 $C1 Explosion | −5.0 |
| 1210 | S3K AIZ strike: aiz-hero #70 (draft render used #75, 5 frames late — fixed in edit) | S3K $B4 | −7.2 |
| 1419 | ARZ Whisp strike #138 | S2 $C1 | −6.5 |
| 4181 | Gilded transformation start, gilded #51, on the downbeat | S3K $9F Super Transform | −11.0 (long soft tail; kit balance check passes) |
| 4224 | Instagib impact gilded #94 (draft used #95, 1 frame late — fixed in edit) | S3K $B4 | −8.1 |
| 5351 | iris into the end card (graphic punctuation) | S3K $B3 | −8.1 |

Sound was checked by measurement only; nothing was listened to.

## Viewer pass

`checkpoint2/viewer-pass.md` (one row per 4 s). Contact sheets: `draft-contact-1fps.jpg`.

## Queued for the final (after your reply)

- Sync fixes above (already in the edit); raise $9F to ~3.0 gain; add S2 $CF Signpost on the climax signpost
  trigger (gilded-clear #360, MICA x crosses the Obj0D spawn x 10816).
- Vertical 1080×1920 cut, archive, README with limits:
  - S1 results card: act oval renders over "HAS / PASSED / SCORE"; identical with stock Sonic at the same position
    and input (`checkpoint1/s1-results-mica-vs-stock.png`, control capture `captures/ghz-clear-stock-control`). S1
    shown to the signpost only.
  - Competition: S3K player-select still cycles stock portraits; `GameplayCaptureTool` throws in the arena draw
    (`Native arena has no published VInt registers`). Slot reels need a positioned slot setup not built. Both omitted.
  - S2 has no multi-badnik chain in ~20 positioned probes; one lock-on strike shown.
  - S3K title Tornado fly-by is unreplaced stock art; cropped out.
  - Positioned starts / declared rings+timer throughout; half-pipe, continue and ending via debug component hosts.

Stopping here for review.
