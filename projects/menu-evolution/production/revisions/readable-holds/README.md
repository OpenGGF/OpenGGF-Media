# ROAD TO 9, readable-holds cut (menu-evolution revision `readable-holds`)

Re-edited 2026-10-29 by Claude Opus 5.5 (xhigh, fast mode off) from the hill-climb story sources after the
user's review: "great work but some of the screens are a bit rushed. lots of info on the screen that gets
flashed up too quickly to ingest" and "some of the screens transition as soon as they finish animating,
too". Same story, Super Sonic bed, look and moving menus. No video was slowed down or stretched; every
frame is rendered again from the original sources.

The final render also carries the user's next request, "Hubs & Dialogs showing 9 everywhere, but the final
scores have 8.5. None of this rounding crap; I want those spacing and icon scores at 9!": an engine follow-up
earned those 9s by design (`ca3d04a1d`, `55d9fec81`; audit at `56c9aed13`), and the last chapter now shows the
follow-up's exact A1 Hub row and its fresh capture. The first render, with the finish-pass row, is kept as
`superseded/pre-hub-criteria/` (see its README); the two are pixel-identical before frame 2826 and their audio
is bit-identical.

**Deliverable:** `final/menu-evolution-readable-holds.mp4` (1920x1080, 60 fps, H.264 + AAC stereo 48 kHz,
14 chapters) and the lossless master `final/menu-evolution-readable-holds-master.mkv` (FFV1 + PCM, the same
chapters). 56.300 s (3,378 frames). Hashes: `provenance/deliverables.json`. The first film, the Super Sonic cut
and the hill-climb story cut are unchanged (hashes re-verified).

## Reading holds, before and after

Each dense screen now runs orient -> reveal -> settled read -> transition. A settled hold is the time from
the first frame of the finished state to the first frame that changes, measured on a frozen render: footage
and background are held still, so any difference is editorial animation (`edit.py reads`,
`sources/promo/reads.json`; the accepted cut measured the same way by `old_holds.py`).

| Screen | Accepted cut | This cut | What the viewer reads |
|---|---|---|---|
| The ask | 0.23 s | 2.02 s | the opening line over the six round-0 menus |
| Step 1, six groups | 0.35 s | 2.03 s | the step and six labels on their menus |
| Rubric | 0.02 s | 2.30 s | the step and the seven criterion names (cells are heat colour) |
| Overall | (same screen) | 2.38 s | "OVERALL: ONE JUDGMENT, NOT AN AVERAGE." and six numbers |
| Target | 0.02 s | 2.03 s | "STEP 3: EVERY GROUP TO 8 OR BETTER." |
| Round 4 | 0.10 s | 2.33 s | six overall scores and "CLOSE. NOT 8 YET." |
| 27 families | 0.02 s | 2.13 s | the board at 8, the three below framed |
| All 27 at 8 | 1.25 s | 2.12 s | the slam |
| The turn | 1.35 + 1.33 s | 2.98 s | "THEN WE RAISED THE BAR." / ROAD TO 9 / "9 MEANS PRODUCTION POLISH." |
| Pass 1 | 1.33 s | 2.25 s | the quote and HUB 8.5, 0 / 27 |
| Fresh review | 0.75 s | 2.17 s | "A FRESH AI REVIEW LOWERED THE SCORES.", HUB 8, four red tiles |
| Structure | 0.20 s | 2.23 s | the quote, HUB 9, 13 / 27 |
| Sent back | 0.17 s | 2.08 s | "ANOTHER REVIEW SENT ONE 9 BACK." and the Editor projects tile |
| Finish | 0.08 + 0.02 s | 2.67 s | SETTINGS 9, 26 / 27, "TIME ATTACK: ONE KEY HINT LEFT" |
| 27 / 27 and criteria | 0.53 s | 2.88 s | 27 / 27 AT 9 OVERALL, the follow-up kicker, the hub's seven criteria ("was 8.5" under two), "THE HUB: 9 ON EACH CRITERION." |
| Delivered six groups | not measured | 1.52 s | five moving delivered menus and the hub's follow-up still, labelled as in chapter 1 |
| End card | 1.48 s | 2.93 s | title, line, URL, status, credit, disclaimer |

Exact frames: the table in `edit.py`'s docstring and `reads.json`. Pictures of every state at its settle,
+1 s, +2 s, last held frame and first changed frame (from the master): `review/reads-{a,b,c}.png`.
The delivered-wall hold is short on purpose: its labels were read in chapter 1 and the wall keeps moving
under the end card, which then holds 2.93 s.

## What was simplified or removed

Reveals got faster (2-4 frame cascades instead of half beats) so the time goes to reading, and screens carry
one idea at a time:
- Rubric: the 5 / 7 / 9 scale line (9 is defined at the turn) and "one judgment, not an average" under the
  column (now the headline of its own beat, cells dimmed). Criterion names are 38 px on two tiers, whole words.
- The loop: no longer its own chapter ending on a lit step; a static strip under the rounds pane, with only the
  lit step moving. "STEP 3 · THE HILL CLIMB" and the loop dots are gone.
- Time Attack 5.5 -> 8 still comparison and its "also:" footnotes; "GOAL MET" / "STEP 3 DONE" and the date
  pill on the slam; "AT 9: 0 / 27" on the turn; "THEN WE RAISED THE BAR" as its own screen (now the turn's top line).
- Road to 9: the captions that repeated each audit quote; the 27-tile board's numbers and row labels (colour and
  the counter carry it); the "?" trace-plate tile and its footnote; the notices' 8 -> 8.5 tile; the lobby still.
- The derived "12": while the sent-back tile and its pill are on screen the counter is hidden; it returns at 26,
  the finish-pass matrix's own total.

Added for clarity, not decoration: "EACH TILE: ONE FAMILY'S OVERALL SCORE" on the big board, and "27 / 27 AT 9
OVERALL" on the slam, because the user read the all-9 tiles as rounded criteria.

## The final criteria row and the hub follow-up

The 27 / 27 chapter shows A1 Hub from the audit's "Hub and Dialogs spacing and icons to 9 (2026-10-29)"
follow-up matrix at `56c9aed13` (`origin/feature/ai-menu-design-review`, PR 236): typography, hierarchy,
spacing, colour, icons, consistency and clarity all 9, overall 9. Under the kicker "THE HUB AFTER A SPACING AND
ICON FOLLOW-UP · 29 OCT", spacing and icons are framed with "was 8.5" beneath them, as the matrix marks them, and
the line reads "THE HUB: 9 ON EACH CRITERION." Only the hub is claimed: A5 Help's colour stays 8.5 and families
outside A1-A7 keep their finish-pass entries, so the film says nothing about every criterion of every family.
The history is not rewritten: the climb, the 8.5s and the finish pass stay as they were, and the follow-up is
labelled as one. The row, markers and line come only from `sources/promo/result-row.json` (a test render with
an altered file changed only that block).

The follow-up was code (`ca3d04a1d` rhythm and icons, `55d9fec81` dot fill; `d889277f6` and `56c9aed13` are
documentation), captured clean at `d6771c478` (the tree of `55d9fec81`). Its before/final captures change the
hub states and none of the other five wall groups' representative states (Settings 0.00 %, Locate 0.17 % of
pixels), so the delivered wall keeps five `d823ce643` moving takes and its hub cell is now the follow-up's
static native capture `hub-criteria-nine-20261029/final/320/hub/01-hub.png` at 2x, labelled "HUB & DIALOGS ·
FOLLOW-UP STILL". It is a still, not a new moving take.

## Music

The super-sonic-cut's Super Sonic render (same file, sha256 checked by `edit.py master`), as one continuous
excerpt: bed beat 16 (the A section's second phrase, a downbeat hit) to 10.1 frames after the G-major stab on
bed beat 152, in the rest after it: the accepted cut's own ending point, one loop later. 136 beats at 146.48
BPM. ALL 27 AT 8 lands on the B downbeat; the end card rides the last intro riff into the stab. No splice,
no re-render, no time stretch; no other music.

## Sources and rebuild

```
sources/promo/edit.py          the edit: brief, beat sheet and reading-hold table in its docstring; scores,
                               schedule, source intervals, cues; check, reads, readsheet, master, mp4 commands
sources/promo/result-row.json  the final criteria row (the one block to replace from a newer verified source)
sources/promo/reads.json       measured reading holds (edit.py reads)
sources/promo/review.py        motion (holds marked), strips, exact pixels, loudness, stereo, stingers, intervals
sources/promo/old_holds.py     the accepted cut's holds, measured the same way (before/after record)
sources/promo/identity.py      pixel identity of the takes against the audit's captures (unchanged probe)
sources/promo/{chapters.txt,edl.csv,cues.json}   chapter map, per-shot source intervals, UI cue placements
sources/archive/make_revision_payload.py        the OpenGGF-Media payload builder for this revision
provenance/                    base, request, score source, reused inputs and stills with hashes; deliverables
review/                        reading-hold sheets, consecutive-frame strips at every transition
superseded/pre-hub-criteria/   the first render (finish-pass row): film, master, its sources, provenance, review
```

Paths: `OPENGGF_WORKTREE` (a tree with `tools/media/promo_kit.py` at `c7d66bbf9` or later, unchanged),
`MENU_EVIDENCE` (default the production root's parent) and the production root two levels above this revision.
Python with numpy 2.5.4 + Pillow 13.0.0: `edit.py check`, `READ_CHECK=1 edit.py reads`, `edit.py master`,
`edit.py mp4`, `edit.py readsheet <master>`. No engine code changed, nothing was recaptured.

## Checks (measured on the final files)

- ffprobe: both 1920x1080, 60/1, 3,378 frames counted, 56.300 s; MP4 H.264 High yuv420p (BT.709 matrix, TV
  range; transfer and primaries read as untagged, as in the earlier cuts) + AAC LC 48 kHz stereo; master FFV1
  bgr0 + PCM s16le; the same 14 chapters in both (0, 5.117, 11.467, 14.133, 19.450, 22.933, 25.400, 29.083,
  32.250, 35.633, 39.317, 41.783, 45.883, 52.217 -> 56.300 s).
- Full decodes `ffmpeg -v error -xerror` of MP4 and master: exit 0.
- Reproducibility: the final `edit.py` renders 9 sampled frames (including the result block and the wall)
  identical to the master; the master's PCM is bit-identical to the superseded render's, whose PCM matched the
  edit's mix within 1 LSB. Against the superseded render, sampled frames 0-2826 are identical; only the result
  block (rows 308-720) and the hub cell differ.
- Reading holds: all 17 states settled (no editorial pixel changes between settle and transition, sampled
  every 10 frames plus the 30 frames before each settle and 16 after each transition); holds above.
- Source intervals (`review.py edl`): 24/24 take intervals inside their takes, stills present. The Mod manager
  pane ends at take frame 144, before the take's next ENTER (158); the shortest take (legal, 420) is never run out.
- Pixels (`review.py pixels` on the master): 18/18 sampled panes are exact integer nearest-neighbour copies (2x
  wall cells of both eras including the follow-up hub still, 4x Mod manager and legal notice, 3x stills and
  delivered Settings, the mark-up 1:1). `edit.py master` refuses a hub still whose hash differs from the row file.
- Identity (`identity.py`): unchanged from the hill-climb story (Mod manager 0.00 %, legal 0.41 % = the prompt
  blink, Settings 0.01 % against the finish pass).
- Motion (`review.py motion` on the MP4): no frozen runs (the background drifts and the menus move); mean change
  per frame 0.28 inside the reading holds vs 3.09 elsewhere (480x270). Strips at 22 transitions and score events
  (`strips-d.png` re-made for the changed ending; a-c and `reads-a/b` are unchanged sections).
- Sound (AAC, ebur128): integrated -14.8 LUFS, true peak -1.5 dBTP (AAC gain -0.8 dB). Chapters -15.9 to
  -13.4 LUFS. L/R within 0.40 dB in every chapter; after the bed cut the peak is 0.00003 (about -90 dBFS).
  Stingers against the bed (loudest 100 ms): Blip -7.8 to +9.1 dB, Swish -8.4 to -3.5, Beep -6.9 to +1.7,
  Tally End +2.6 to +4.4, Spindash +3.9, Giant Ring +3.7, UI tones +3.4 to +12.4 dB; all centred; no
  `sound_balance` warnings. `edit.py check`: no warnings (6 shots, mean 9.4 s; the board changes inside them).

Limits: sound was checked by measurement only; nobody listened to the mix. Motion and readability were
reviewed through frozen-render measurements, frame sheets and strips, not by real-time viewing; "readable in
2-3 s" is a design target, not a tested reading speed. Several proofs are the review's still captures because
no moving captures of those passes exist; they are labelled as captures. Scores are subjective design
judgments from captures, not usability measurements. The user's acceptance is not recorded here.

## Archive payload

`archive-payload/` (built by `sources/archive/make_revision_payload.py`) holds the additive OpenGGF-Media
payload for project `menu-evolution`: this revision's text sources under
`projects/menu-evolution/production/revisions/readable-holds/`, the updated project index, the revision's
external asset index and catalog fragments (sources, assets, the project row and the README table row). Film,
master, review images, the superseded render and the follow-up still stay external and are hashed (the still
under the existing `menu-evolution/design-review-evidence` root); the bed, takes, SFX, UI tones and earlier
capture stills are already catalogued and are only referenced, so no new root is added.
