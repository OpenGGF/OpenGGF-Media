# S3K ending highlights — provisional

57 seconds; silent1600×520; gameplay uses nearest-neighbor logical2× scaling.

Sonic/Tails are declared native ending scene entries. Knuckles uses the maintained actual final-fight BK2 from input0, then neutral. This editorial reel does not prove an uninterrupted cold campaign or native pixel parity. Formal lifecycle/restore/pixel qualification remains pending.

| Reel seconds | Chapter | Source input interval (end exclusive) | Source film seconds |
| --- | --- | --- | --- |
| 0–6 | Sonic - Tornado rescue | 600–960 | 10–16 |
| 6–13 | Sonic - reunion | 3400–3820 | 170/3–191/3 |
| 13–21 | Tails - AIZ Master Emerald restoration | 3800–4280 | 190/3–214/3 |
| 21–27 | Tails - Super reunion | 4496–4856 | 1124/15–1214/15 |
| 27–33 | ROM credits | 6240–6600 | 104–110 |
| 33–37 | Sonic - post-credit banner | 13260–13500 | 221–225 |
| 37–41 | Knuckles - powered flight with Master Emerald | 9052–9292 | 238/15–298/15 |
| 41–45 | Knuckles - turning plane and departure | 9292–9532 | 298/15–358/15 |
| 45–53 | Knuckles - Mecha and Master Emerald terminal | 22300–22780 | 710/3–734/3 |
| 53–57 | Return to the title screen | 24460–24700 | 818/3–830/3 |

Inputs map to source time by `native input = capture_from +60×source seconds`; CSV frame is submitted input index, not VInt. Sparse7.5fps inputs duplicate to15fps; no speed change or invented interpolation.

Reproduce with `python3 assemble.py --root <task-source-root>`. `chapters.edl.json` records relative videos/CSVs, exact rational intervals, source/movie/jar hashes and setup labels. `media-verification.json` records the checked output, chapters, dimensions and full xerror decode.

Known source negative: the current Tails film has full-center mask grain at inputs2500–3700 because physicalcamera0 differs from render-copy608. This is recorded in the EDL and diagnosed separately; the selected later scenes do not document that defect. A corrected owner/capture is pending. The initial Knuckles wide flanks intentionally mask beyond the native320 window.
