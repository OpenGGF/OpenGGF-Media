# MICA & TALON phase 2 — local delivery

Branch `feature/ai-mt-promo-2`, source `605ccd8765`. No commits, stash, ROM changes, upload or archive. Phase-1 files preserved. The requested build passed with package validation 0 findings. Build-generated untracked mapping JSONs were retained under `build-generated/`; checkout is clean.

## Outputs and review

- `out/master-16x9.mp4`: 1920×1080, 60 Hz, 84.8 s.
- `out/master-9x16.mp4`: independently composed 1080×1920, 60 Hz, 84.8 s; stacked comparisons and 2×4 grid.
- `edit/wide/sheet-0.png` and `edit/vertical/sheet-0.png`: one sample per four seconds.
- `viewer-pass.md`: one review row per four seconds; sampled visual review, not a full listening pass.
- `out/homing-proof.jpg`, `homing-events.json`: actual MGZ2 native-frame evidence.
- `shot-list.csv`: all attempts; `selected-shots.csv`: selected intervals with per-take provenance links. The eight-screen chapter uses exact 3× native subject crops, rather than claiming that eight full native viewports fit in 1080p. Data Select holds its final captured card after source EOF.

Sound checked by measurement only. There are no editorial jump sounds. The two ring accents alternate native S3K $33/$34; Giant Ring $B3 supplies the title slam. All were rendered paced through the engine SMPS driver, against the prepared DAC-enabled LBZ1 bed. Per-stinger checks compare 100 ms levels to the bed; final AAC loudness/true-peak logs accompany both masters.

## New evidence

MGZ2: the same roundtripped input gives airborne score transitions 100 at 65, 300 at 82, 800 at 104, with three distinct native Mantis defeats visible. Actual recapture retains score in CSV. Cold open uses frames 15–168, and the homing beat uses 0–175, both before first hurt at183. No fewer-than-three claim is used.

Half-pipe: `halfpipe-cleared-post` is **debug positioned ROM-starpost component entry**, not a cold route. The initial positioned boots had already activated/omitted the post before the ring seed could qualify it. The capture host reveals the level, repositions to (3568,150), declares 70 rings, clears old checkpoint activation, and reinstantiates the original ROM Obj79 at its original (3568,170). The controller jumps at150, actual native star touch enters SPECIAL_STAGE at165; no `enterSpecialStage` or stage-mode setter is called. MICA leads; TALON follows with his own art and name. This setup is more invasive than a plain positioned start and must remain disclosed in the archive.

Continue: native S2 continue provider, with declared zero lives and three continues, then normal stepping/drawing. Ending: the integration-test Engine binding and `requestCreditsTransition` debug entry; normal production provider thereafter. Only the TALON Tornado section at2700+ is selected. Native stock photo cards are deliberately excluded. Ending `state.csv` retains the original capture session's inactive LEVEL-mode observation; that column does not describe the separately bound Engine ending loop. It must not be used as reachability evidence.

Gilded climax: `gilded-clear-low` is one continuous positioned EHZ1 take, MICA plus TALON, 70 declared rings/all emeralds. Score reaches300 from two badnik defeats before the native signpost and MICA GOT THROUGH ACT1 results. No splice between combat and results. Initial setup is (9000,780); edit starts at70 and lasts900 source frames.

Custom TALON HUD verified in flight source; team portraits verified in seeded S3K save slots. The unused No Save portrait still contains stock characters and is cropped out. The only intentional stock hero reference retained is the lead-required native-pose-to-redraw editorial comparison. These captures certify selected views, not all game surfaces or parity.

## Swappable slots / remaining limits

- **Carry:** unavailable at capture checkpoint: `bugfix/ai-mt-carry-plc` still pointed to `3aac15eb45`. The exact phase-1 carry input is recaptured in `captures/phase2/carry` and still fails missing host mappings. Team run occupies the designed carry slot; the film makes no carry claim. When fixed, rerun `capture_all.py --only carry --take carry-fixed` against its separately built checkout, inspect CSV/frames, then point the team beat to that take and choose its real in-point.
- **Title:** the native-letter editorial MICA/TALON treatment remains the placeholder, as requested. No stock title-screen hero is used. The long name hold is the weakest remaining pacing beat; replace it when title art is delivered.
- No archive/upload was performed: the lead owns that after final art integration.

## Exact re-render command

From `/home/farrell/scratch/agent-tmp/mt-promo-20261110/phase2` after replacing the selected take or changing its `clip()` reference/in-point:

```sh
venv/bin/python render_all.py --checkout /mnt/LinuxData/T3/worktrees/OpenGGF/t3-66af4c18 --take phase2
```

This performs checks, contact sheets, both full renders, AAC mastering, ffprobe, true-peak analysis and complete decodes. The final edit itself contains the corrected opening. `repair_prefix.py` records the bounded correction to the wide render already in flight; fresh renders need no patch. Prepared `fonts/`, `music/`, and `venv/` are symlinks to the preserved phase-1 kit. All scene paths are under this `phase2/` root. Original captures contain every-frame PNGs, inputs and provenance. No repository files were committed.

## Delivered-file verification

- master-16x9.mp4: [1920, 1080], 60/1 fps, 84.800000 s; full decode exit 0; AAC measured -18.86 LUFS and -3.25 dBTP. promo_kit check: no warnings.
- master-9x16.mp4: [1080, 1920], 60/1 fps, 84.800000 s; full decode exit 0; AAC measured -18.88 LUFS and -3.00 dBTP. promo_kit check: no warnings.

Both checks: 13 shots, mean 6.52 s; busiest 20 s window five cuts, last window one; longest bare stretch 0 s; max caption density two. See `verification.json`, raw ffprobe/decode/loudness logs and `out/contact-wide.jpg` / `out/contact-vertical-encoded.jpg` (sampled from actual encoded deliverables).
