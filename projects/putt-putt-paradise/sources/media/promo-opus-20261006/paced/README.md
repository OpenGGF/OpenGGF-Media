# Putt Putt Paradise promo: paced cut (2026-10-06)

This cut responds to the user's feedback on `../promo-opus-v5.mp4`: "looks amazing but
doesn't leave long enough on each section. very rushed". It runs 88.47 s, up from
49.97 s. It keeps the same look, typography, iris/stripe/push/flash transitions and order.
It has fewer cuts, each held longer: 14 segments instead of 16, and 3 physics shots of
about 4 s each instead of 4 shots of 1.4–2.6 s.

Every gameplay range is real contiguous native footage played at normal speed, with no holds.
The online card's extra length comes from an original HOST⇄JOIN graphic (2.5 s) shown
before the unaltered 4 s title-menu clip. The menu clip is not frozen or looped.

## Files
| File | What |
|---|---|
| `promo-opus-paced.mp4` | The render: 1920×1080, 30 fps, 2654 frames, H.264, silent, 14 chapters |
| `promo-manifest-paced.json` | Edit decision list (native 60 Hz ranges, captions, cards, transitions) |
| `source-lock-paced.json` | SHA-256 of every selected v5 `state.csv` range and of each `events.csv` |
| `render_promo_paced.py` | Copy of `../render_promo.py` with the online lead graphic, manifest-driven engine/end timing and paced defaults. The original is unchanged |
| `verify_fidelity.py` | Copy of the original fidelity checker that also checks the title-menu clips |
| `promo-opus-paced.{edl.json,chapters.csv,verify.json,fidelity.json,cuts.png}` | Resolved timeline, container/cadence/decode check, pixel fidelity and contact sheet |
| `render-paced.log`, `fidelity-paced.log` | Run logs |
| `analysis/` | Contact sheets used to choose ranges (`sheet.py`) |

## Reproduce
```sh
cd /home/farrell/scratch/gameplay-captures/putt-putt-paradise-20261005/promo-opus-20261006/paced
python3 render_promo_paced.py --source-root ../../showcase-20261006-tails --tag v5 --final --out promo-opus-paced.mp4
python3 verify_fidelity.py promo-opus-paced.mp4 promo-opus-paced.edl.json
```

`promo-opus-paced.chapters.csv` is authoritative for the times.
