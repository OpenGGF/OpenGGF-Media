# Putt Putt Paradise — public promo (Opus edit, 2026-10-06)

A 50-second, mute-friendly 1920×1080 promo. The current render is a **DRAFT**
made from the v4 captures, and every frame carries the label "DRAFT · v4 footage".
It must not be published. v4 has the idle-Tails visibility defect, so the edit
uses only moving Tails shots plus Tails' crouch/charge, which v4 renders.
The final version is the same script run on corrected v5 captures.

## Files

| File | What |
|---|---|
| `render_promo.py` | Renderer. It checks the sources, composes frames with Pillow, encodes with x264 and verifies the result |
| `promo-manifest.json` | Edit decision list: segments, native 60 Hz source ranges, captions, transitions and card text |
| `source-lock.json` | SHA-256 of the gameplay-state rows (`state.csv`) for every selected range, plus `events.csv` hashes, taken from v4 |
| `verify_fidelity.py` | Samples clean frames from every gameplay range. Checks that the footage is unaltered, uses integer nearest-neighbour scaling and plays at normal speed (frame k → k+1) |
| `promo-opus-v4-draft.mp4` | Draft render |
| `*.edl.json` / `*.chapters.csv` | Resolved timeline: output frames/seconds ↔ source native frames, mkv frames and seconds |
| `*.verify.json` / `*.fidelity.json` | Container/cadence/decode checks and pixel-fidelity checks |
| `*.cuts.png` | Contact sheet of each segment's first clean frame, middle and mid-transition |
| `analysis/` | Working contact sheets used to choose moments (`sheet.py`) |

## Usage

```sh
cd /home/farrell/scratch/gameplay-captures/putt-putt-paradise-20261005/promo-opus-20261006
# draft (v4)
python3 render_promo.py --source-root ../showcase-20261006-polish --tag v4
# final, after corrected captures exist as <root>/ehz1-sonic-rewind-final-v5 etc.
python3 render_promo.py --source-root <root> --tag v5 --final
python3 verify_fidelity.py promo-opus-v5.mp4 promo-opus-v5.edl.json
```

- `--check-only` validates the sources against the lock without rendering.
- `--dir ehz1=/abs/path` (or `local=` / `ehz2=`) overrides one scenario directory
  when the names do not follow `<scenario>-<tag>`.
- `--final` drops the DRAFT label. The script refuses `--final` for tag v4.
- If the replacement captures have a different gameplay timeline, the lock check
  fails and names the affected range. Re-cut the manifest in that case.
  `--allow-state-drift` renders anyway and stamps "UNLOCKED TIMELINE" on the output.
  Use `--lock` only to deliberately re-baseline.
- `--preview 40,300,...` writes PNG stills of the listed output frames only.
- Requirements: Python 3 with Pillow, and FFmpeg with libx264 and FFV1 decode.
  It also needs these Fira Sans fonts:
  `/usr/share/fonts/TTF/FiraSansCompressed-{Heavy,ExtraBold}.ttf` and
  `FiraSansCondensed-{SemiBold,Book,Medium}.ttf`. A render takes about 45 s
  on this host.

## Intent and structure

The edit opens on action with no logo first, and introduces each feature with
one short caption. The left gutter holds a numbered feature card. The right
gutter holds a feature checklist that ticks off as the video goes. Gameplay is
always the real 320×224 image scaled exactly 4× (3× in the split screen, 2× in
the engine card), with the HUD untouched. Every output frame advances one
source frame, so there are no slow-mo, speed-up or freeze frames. Transitions
include a golf-ball iris, a brand-stripe wipe, a push and a flash, and both
clips keep playing through every transition. Captures are silent and the promo
has no audio track.

| Out (s) | Chapter | Source (native 60 Hz frames, end exclusive) | Source mkv seconds |
|---|---|---|---|
| 0.00–3.10 | Hook: "What if Sonic was the golf ball?" | ehz1 1714–1900 (waterfall run at top speed) | 28.567–31.667 |
| 2.90–5.07 | "…or Tails?" (flash) | ehz2 316–446 (Tails airborne chip) | 5.267–7.433 |
| 4.67–7.87 | Title (stripes): in-engine title menu | ehz1 title.mkv frames 0–96 | 0.000–3.200 |
| 7.53–12.10 | Putt → roll → VHS rewind → back on tee (iris) | ehz1 120–394 (power 123–183, shot 214, rewind request 285, VHS 290–359, restored 360) | 2.000–6.567 |
| 11.83–17.40 | Chip loft → SPIN hit point → power → launch (push) | ehz1 776–1110 (SPIN 803–863, POWER 864–924, release 955) | 12.933–18.500 |
| 17.00–18.93 | Real physics 1 (stripes) | ehz1 2694–2810 | 44.900–46.833 |
| 18.67–20.40 | Real physics 2, Tails (push) | ehz2 844–948 | 14.067–15.800 |
| 20.20–21.60 | Real physics 3, arch (flash) | ehz1 2846–2930 | 47.433–48.833 |
| 21.27–23.83 | Real physics 4, EHZ2 corkscrew (iris) | ehz2 7176–7330 | 119.600–122.167 |
| 23.43–25.93 | Sonic or Tails, split 3× (stripes) | left ehz1 2376–2526 / right ehz2 3296–3446 | 39.600–42.100 / 54.933–57.433 |
| 25.67–28.33 | Two players: Sonic (push) | local 140–300 | 2.333–5.000 |
| 28.07–32.73 | Two players: Tails (push) | local 600–880 (SPIN 583–643, POWER 644–704, release 735) | 10.000–14.667 |
| 32.33–35.83 | Online card: real title menu with HOST/JOIN highlighted | ehz1 title.mkv 0–105 | 0.000–3.500 |
| 35.50–39.53 | Finale: chip to the flag, scorecard (iris) | ehz1 4288–4530 (hole-complete 4443) | 71.467–75.500 |
| 39.13–44.80 | Built on OpenGGF card + 2× footage | ehz1 1324–1664 | 22.067–27.733 |
| 44.47–49.97 | End card / CTA (iris, 0.5 s fade-out) | original graphics | — |

`*.chapters.csv` is the authoritative copy of these times.

## Accuracy guardrails

- Online is presented on its own card over the real title menu. The card says
  online is a supported feature and that the footage shows practice and local
  play. No local footage is labelled as online.
- The engine card and end card say: alpha, mod API is a pre-release candidate,
  not yet released, no download yet. They also say the user's own Sonic 2 ROM
  supplies the art and none is included, give the source link
  https://github.com/OpenGGF/OpenGGF, and carry a SEGA non-affiliation note.
  The OpenGGF repository is GPL-3.0, which is the basis for "open-source".
- Avoided v4 idle-Tails frames: the local turn handover (native 479–582 AIM)
  and all Tails AIM/idle stretches. The Tails ranges used are airborne, rolling
  or in the SPIN/POWER crouch, which v4 renders visibly.
- All non-footage art is original geometric/typographic graphics. No ROM
  graphics are extracted or redrawn.
