# S2 Competition highlights for James

A 73.8 s personal reel (2026-11-09): "Remember that competition branch I accidentally deleted? So I
rebuilt it." Sonic 2's two-player Competition mode, rebuilt in OpenGGF (PR #273), shown as the
engine plays it:

- Title, then the 2P menu, then the EHZ title card, in one take.
- Player 1's and player 2's act-1 runs, with the two-player signpost.
- A labelled engine vs native BizHawk split of the same route rows.
- Act results and Casino Night's slot machine.
- The 1-1 tie fading to white into the competitive special stage, which uses the one-player
  stage's slowdown approximation.

## Revision v1 (final, delivered)

- Sources: [`sources/`](sources/).
  - `capture.sh` records the three frozen routes, with engine audio, at the engine commit.
  - `prep.py` cuts the shot frames and audio.
  - `edit.py` is the promo_kit edit, with its brief in the docstring.
  - `shots.py` is the edit list.
  - `finish.sh` is the final mux: -1.8 dB and chapters.
  - `chapters.txt` lists the chapters.
  - `provenance.json` records the source commit, routes, measurements and limits.
- Rebuild:
  1. Run `capture.sh <dir>`.
  2. Run `python3 prep.py`.
  3. Run `python3 edit.py` to write the soundtrack.
  4. Run `python3 <OpenGGF>/tools/media/promo_kit.py render edit.py`.
  5. Run `finish.sh`.

  The edit imports promo_kit from the OpenGGF worktree path at the top of `edit.py`; relocate that
  path to your checkout. Captures need a supplied S2 REV01 ROM.
- External: captures, frames, audio, the native BizHawk frames and the finished film; see
  `catalog/assets.csv`.
- Limits: the frozen routes run one player at a time, so the reel never claims a simultaneous
  race. Sound was checked by measurement only, and motion by per-cut contact sheets.
