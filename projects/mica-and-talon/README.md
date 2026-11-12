# MICA & TALON Mod Showcase

**Current: pacing revision, 2026-11-12** (mod commit `47e1826b80`, build `5313360296`, develop
`4f885afbd6`; 124.0 s, 16:9 and designed 9:16 cuts; the owner's music from its start with one fade; game sound from
each take's own SFX-only audio). Local archive only; not pushed. Sound checked by measurement only.

- [README: source and commits, owner feedback, sound, cards, what is not filmed as it ships, 1.0 clips, rebuild](sources/revision-20261112/README.md)
- [Edit: brief, tracked bar grid and both cuts](sources/revision-20261112/edit/edit.py), [cards](sources/revision-20261112/edit/cards.py)
- [Shot index](sources/revision-20261112/out/shot-index.csv), [chapters](sources/revision-20261112/out/chapters.txt), [verification](sources/revision-20261112/out/verification.json),
  [game-sound levels](sources/revision-20261112/out/sfx-levels.json), [takes check](sources/revision-20261112/out/takes-check.json)
- Reviews: [pacing storyboard data](sources/revision-20261112/checkpoint4/plan.json), [probe results](sources/revision-20261112/checkpoint5/probes.json)
- [External hashes](external-hashes-revision-20261112.json): masters, review pages, frames, state CSVs, take audio, the bed, mascot
  cut-outs, fonts and the owner's music (name + SHA-256 only; no WAV is in this repository).

## Superseded: promo redo, delivered 2026-11-12

The 124 s cut the owner reviewed (OpenGGF `1e0faac123`, placed ROM stingers). Its takes now live in
`captures-old-art-1e0faac123/` in the task folder: `captures/` there was renamed when the revision was shot, so every `captures/...`
path in [its external hashes](external-hashes-redo-20261112.json) resolves under that folder. Same files, same hashes.

- [README: source, music decision, what is not filmed as it ships, the 9:16 cut, review history, rebuild](sources/redo-20261112/README.md)
- [Edit: brief, tracked bar grid and both cuts](sources/redo-20261112/edit/edit.py)
- [Shot index (every capture on screen: entry kind, declared setup, frames used, command)](sources/redo-20261112/out/shot-index.csv),
  [chapters](sources/redo-20261112/out/chapters.txt), [viewer pass](sources/redo-20261112/out/viewer-pass.md),
  [verification](sources/redo-20261112/out/verification.json), [check](sources/redo-20261112/out/promo_kit-check.txt),
  [stinger levels](sources/redo-20261112/out/stinger-levels.json)
- Edit as it stood at each review: [storyboard](sources/redo-20261112/checkpoint1/edit-at-storyboard.py),
  [draft](sources/redo-20261112/checkpoint2/edit-at-draft.py), [climax check](sources/redo-20261112/checkpoint3/edit-at-climax-check.py)
- [External hashes](external-hashes-redo-20261112.json): videos, review pages, frames, state CSVs, PCM, fonts and the
  owner's music (name + SHA-256 only; the WAV is not in this repository).

## Superseded: production promo, 2026-11-11

Superseded by the redo after the owner's feedback (zoom at the start, spliced music, features not shown).
OpenGGF `b088fae95b`, 95.4 s, 16:9 and designed 9:16 cuts.

- [Production README: sources, music edit, disclosures, known limits, rebuild, review history](sources/production-20261111/README.md)
- [Edit: brief, beat sheet and compositor](sources/production-20261111/edit/edit.py)
- [Shot index (every capture: entry kind, declared setup, command)](sources/production-20261111/out/shot-index.csv),
  [chapters](sources/production-20261111/out/chapters.txt), [viewer pass](sources/production-20261111/out/viewer-pass.md),
  [verification](sources/production-20261111/out/verification.json), [check](sources/production-20261111/out/promo_kit-check.txt),
  [stinger levels](sources/production-20261111/out/stinger-levels.txt)
- Checkpoints with lead reviews: [storyboard](sources/production-20261111/checkpoint1/STORYBOARD.md),
  [draft](sources/production-20261111/checkpoint2/CHECKPOINT2.md)
- [External hashes](external-hashes-production-20261111.json): videos, frames, state CSVs, PCM, fonts and the owner's
  music (name + SHA-256 only; the WAV is not in this repository).

## Superseded: 2026-11-10 showcase ("a very rough cut" per the owner)

Final pass recorded against engine a64655fe97 on 2026-11-10. Local archive for lead publication after user review; no upload or push. The carry shot uses the carry fix (integration b8c105a986), captured by the lead after the final lane stopped; see the review history. The TOGETHER chapter shows the real carry.

- [Final brief, review history, qualifications and rebuild instructions](sources/final/README.md)
- [Editable brief/beat sheet/compositor](sources/final/edit/edit.py)
- [Selected source intervals](sources/final/selected-shots.csv), [capture inventory](sources/final/shot-list.csv), [chapter map](sources/final/chapters.json)
- [Viewer pass](sources/final/viewer-pass.md), [encoded verification](sources/final/verification.json)
- [Retained phase-2 handoff](sources/phase2/handoff.md) — superseded picture; retained methods and review context.
- [External hashes](external-hashes.json) and repository catalog locate large recordings, lossless frames, PCM and other dependencies. They remain local external files, not GitHub downloads.

No stock Sonic/Tails art in selected final footage. ROMs, extracted glyphs/audio, videos, frame sequences, bulk state, build jars and installed environments are excluded from this commit. Obtain your own ROMs. OpenGGF-derived source retains GPL-3.0; this archive grants no rights to Sega assets or third-party dependencies. Sound checked by measurement only.
