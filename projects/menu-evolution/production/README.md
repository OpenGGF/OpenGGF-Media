# ROAD TO 9: OpenGGF menu evolution promo (menu-evolution)

Produced 2026-10-29 by Claude Opus 5.5 (xhigh) for the request "a promo video of the old menu vs
the new one. Could even include the old 0.5 menu", then steered to "film it like a action movie
montage, with various numbers slowly climbing".

**Deliverable:** `final/menu-evolution-promo.mp4` (1920x1080, 60 fps, H.264 + AAC stereo 48 kHz,
10 chapters) and the lossless master `final/menu-evolution-master.mkv` (FFV1 RGB + PCM, same
chapters). Duration 87.333 s (5,240 frames). Hashes: `provenance/deliverables.json`.

## What the film is

A training montage for the engine's menus. Three real eras, each recorded frame by frame from its
own production menu code with scripted keys, never restyled:

| Era | Source | What it shows |
|---|---|---|
| OpenGGF 0.5 | tag `v0.5.20260411` = `77c6364ce` | the game-select title (the only menu 0.5 had; silent) |
| Before | develop `2f9ca84b1` (27 Oct 2026) | the 0.7 hub and the menus scored in design-review round 0 |
| Now | `d823ce643` (29 Oct 2026) | the delivered menus |

The climbing numbers are only recorded values: the design review's own scores (1-10, subjective
capture-based judgments, not usability or performance measurements) from
`docs/architecture/audits/2026-10-27-menu-design-review.md` at `d823ce643`, the version 0.5 -> 0.7,
and the number of menu families at 9 per pass (0 -> 13 -> 26 -> 27). Each value, its round, date and
section are in `sources/promo/edit.py` (`SCORES`). The end card names the source and says they are
judgments. Individual criteria of some families remain 8.5; the film claims 9 overall only.

The brief, beat sheet and every creative reason are in the docstring of `sources/promo/edit.py`.
Chapters: `sources/promo/chapters.txt`; edit list with source intervals: `sources/promo/edl.csv`;
UI sound cue placements: `sources/promo/cues.json`.

## Layout

```
sources/capture/capture.py          era-aware take runner (compiles the recorders against each tree)
sources/capture/java/...            MenuFilmRecorder, ShaderFilmRecorder (pre and now)
sources/capture/java05/...          V05TitleRecorder + verbatim d823ce643 SurfacelessEglContext (0.5 shim)
sources/capture/takes/*.take        input recipes on the bed's beat grid (explore-* = exploration takes)
sources/promo/edit.py               the edit (promo_kit compositor), brief, beat sheet, scores, audio prep
sources/promo/review.py             motion / transition-strip / exact-pixel / loudness checks
sources/promo/pairsheet.py          era-pair contact sheets of a take
sources/promo/revisions/            edit snapshots r2, r3 (r3 = final)
clips/<era>/<take>/                 native 320x224 PNG per 60 Hz frame + events.csv, provenance.json,
                                    take.txt (state.csv for the EHZ1 takes)
audio/music, audio/sfx              ROM renders (canonical S2 REV01, FmSfxRenderTool --paced)
audio/ui                            HostUiSfx tones synthesised by `edit.py prep`
audio/candidates                    other S2 beds rendered and measured while choosing (unused)
provenance/                         source-map.json (commits, ROM ids, fonts, tools), deliverables.json
review/                             contact sheets and frame strips used in review
final/                              film, master, revisions/r1 review copy
archive-payload/                    bounded OpenGGF-Media payload (project menu-evolution) + catalog rows
```

## Rebuild

1. Build the three trees. Historical trees are `git archive` exports (no extra checkouts) compiled
   with `mvn -Dmse=off -q -DskipTests compile dependency:build-classpath -Dmdep.outputFile=target/cp.txt`
   under a worktree's `target/eras/{v05,pre}`; the current tree uses
   `python3 tools/testing/maven_queue.py -Dmse=off -q -DskipTests package` plus the same classpath goal.
   JDK 25 throughout (0.5 compiles at release 21).
2. Record: `python3 sources/capture/capture.py <era> <take>...` (Linux, surfaceless EGL, no display;
   set `OPENGGF_WORKTREE`). Takes used: `v05 v05-title`; `pre shader hub mods settings-pre locate
   dialogs legal`; `new shader hub mods settings-new locate dialogs legal`. `clips/<era>/settings` is a
   symlink to the era's settings take.
3. Audio: `FmSfxRenderTool --game s2 --rom <S2 REV01> --rate 48000 --paced` with `--music 82`, `ba`,
   `96` and `--sfx cd c5 e0 bc ab c3` into `audio/music` and `audio/sfx`; then `edit.py prep`.
4. Edit (Python with numpy + Pillow; `OPENGGF_WORKTREE` points at a tree with `tools/media/promo_kit.py`):
   `edit.py check`, `edit.py sheet 60`, `edit.py master`, `edit.py mp4`.

ROMs are read in place by absolute path from the original root and are never copied or linked.

## Capture notes and limits

- Every pane is an exact integer nearest-neighbour copy of its source frame (4x panes, 2x grid/wall
  cells); 13/13 sampled panes compared pixel-exact against the source PNGs in the lossless master.
- Old and new takes share one key timeline; where the redesign reordered rows (Settings), each era's
  take presses the keys needed for the same goal on the same beats (`settings-pre` / `settings-new`).
- The cold open and title run Sonic 2 Emerald Hill 1 from its real start, Sonic alone, RIGHT held,
  then a skid to a stop (state.csv); while the picker is open gameplay is not stepped, as in the
  engine. Gameplay state is identical between the two eras frame for frame. The picker's three library
  entries are display data only.
- The mod manager uses copies of the user's two installed mod jars (Eggman's Sky, Sample Flappy),
  installed through the production boot loader into a temporary root. Locate ROM browses a synthetic
  folder of empty placeholder files (no real ROMs or user paths); "This file does not contain Sonic 2"
  is the engine's real verdict on such a file.
- 0.5 compatibility harness: 0.5 has no display-free context owner, so its recorder carries a
  verbatim copy of `d823ce643`'s `SurfacelessEglContext` and hands the screen renderer the
  320x224 projection 0.5's Engine would have set. The 0.5 clouds are randomised per run by 0.5 itself.
- The S3K image used for hub card art is the non-canonical local dump: UI evidence only.
- The pre-redesign Mod manager shows the real 2f9 page; its "Current pattern windows" line is shown as
  the tree draws it with the production allocator.
- Hub navigation sounds are the engine's `HostUiSfx` tones (byte-identical in both eras),
  re-synthesised from that source's formula at the logged cue frames; menus inside the shader picker
  emitted no cues. The 0.5 era is silent because 0.5's sounds were TODO stubs.

## Review record

- Revision 1 (`final/revisions/r1-menu-evolution.mp4`, review copy of the r1 master): structure
  kept; weaknesses found in its frame strips: cross-faded "double"
  digits during score rolls, a flat payoff (wall stayed dim, only the digits whitened), the hero
  starting mid-navigation, and Sonic hit by Coconuts under the title (fixed by a recorded skid).
- Revision 2 (`revisions/edit.r2.py`): crisp slot roll, payoff slam -> top-margin banner -> the six
  menus relight one by one, Giant Ring iris into the delivered hub, carousel slide that bookends the
  0.7 prologue. Master not retained (superseded only by revision 3's fade).
- Revision 3 (`revisions/edit.r3.py`): the payoff banner fades over 8 frames before the iris. Its first
  MP4 (`final/revisions/r3a-ui-gain-1.6.mp4`) measured a 3.7 LU rise into the first rep caused only by
  UI-tone density; revision 3b (`revisions/edit.r3b.py` = `edit.py`, final) re-mixed the engine UI tones
  from gain 1.6 to 1.1 (audio-only: `edit.py remix`, video stream copied), leaving a 2.6 LU rise.

Viewer pass (final, every ~4 s: what is new on screen):

| s | On screen |
|---|---|
| 0-4 | Emerald Hill run; F8 opens the old picker, debug text printed over the HUD |
| 4-8 | the before/now divider sweeps in a framed picker; "SAME GAME. NEW MENUS." |
| 8-11 | ROAD / TO / 9 pops (spindash release, tally ka-ching on the 9) |
| 11-18 | 0.5 game select (barely visible selection pulse), push to the 0.7 hub, version pill rolls 0.5 -> 0.7 |
| 18-25 | Round 0: four old menus drop in with their scores, the scores named as judgments |
| 25-35 | Libraries: bracket rows and a text trust page; score ticks 3.5 -> 9 as the divider sweeps; switches, trust card, Details |
| 35-49 | Settings (calm section): toggle, climb 5.5 -> 9, whole labels in groups, value change, save prompt with old -> new |
| 49-60 | Pickers (the groove returns): ROM? on every row vs icons and scroll bar; wrong file; climb 4 -> 9; error card |
| 60-70 | Hub and dialogs: help, quit prompt, setup; the smallest climb 6.5 -> 9 |
| 70-77 | wall of six new menus pops; dims; families at 9 tally 0 -> 13 -> 26 |
| 77-80 | 27 / 27 slam on Got an Emerald; banner; the menus relight one by one |
| 80-87 | Giant Ring iris into the delivered hub (its own title theme), end card, fade |

Measured on the final files: full decodes of MP4 and master with `ffmpeg -v error -xerror` exit 0;
1920x1080, 60/1, 5,240 frames, 87.333 s; H.264 High yuv420p BT.709 TV range, AAC 48 kHz stereo;
10 chapters in both; AAC integrated -14.2 LUFS, true peak -1.4 dBTP (per-chapter -16.5 to -12.8 LUFS,
all <= -1.4 dBTP); L/R balanced; no frozen runs; 13/13 sampled panes pixel-exact integer copies.

Sound was checked by measurement only (levels, stinger balance, stereo, true peak); nobody listened
to the mix. Motion was reviewed through consecutive-frame strips at every transition and score tick
plus per-frame change measurements, not by real-time viewing.
