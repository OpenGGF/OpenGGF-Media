# S3K ending highlights — integration pending

61 seconds; silent1600×520; gameplay uses nearest-neighbor logical2× scaling.

Sonic/Tails are declared native ending scene entries. Knuckles uses the maintained actual final-fight BK2 from input0, then neutral. Focused lifecycle, rewind and rendered owner checks pass; combined integration smoke/guards remain pending. These editorial excerpts do not prove an uninterrupted cold campaign or native pixel parity.

| Reel seconds | Chapter | Source input interval (end exclusive) | Source film seconds |
| --- | --- | --- | --- |
| 0–6 | Sonic - Tornado rescue | 600–960 | 10–16 |
| 6–13 | Sonic - reunion | 3400–3820 | 170/3–191/3 |
| 13–17 | Tails - native screen departure | 2000–2240 | 100/3–112/3 |
| 17–25 | Tails - AIZ Master Emerald restoration | 3800–4280 | 190/3–214/3 |
| 25–31 | Tails - Super reunion | 4496–4856 | 1124/15–1214/15 |
| 31–37 | ROM credits | 6240–6600 | 104–110 |
| 37–41 | Sonic - post-credit banner | 13260–13500 | 221–225 |
| 41–45 | Knuckles - powered flight with Master Emerald | 9052–9292 | 238/15–298/15 |
| 45–49 | Knuckles - turning plane and departure | 9292–9532 | 298/15–358/15 |
| 49–57 | Knuckles - Mecha and Master Emerald terminal | 22300–22780 | 710/3–734/3 |
| 57–61 | Return to the title screen | 24460–24700 | 818/3–830/3 |

Inputs map to source time by `native input = capture_from +60×source seconds`; CSV frame is submitted input index, not VInt. Sparse7.5fps inputs duplicate to15fps; no speed change or invented interpolation.

Reproduce with `python3 assemble.py --root <task-source-root>`. `chapters.edl.json` records relative videos/CSVs, exact rational intervals, source/movie/jar hashes and setup labels. `media-verification.json` records checked output, chapters, dimensions and full xerror decode.

The new Tails source uses final frozen jar ed152e71, source d1a298ec; its corrected departure is shown at reel13–17. The previous a302 film/reel preserve the known center-grain negative. Sonic/Knuckles sources remain the coherent b2af films on unchanged qualified owners. Wide Knuckles flight flanks intentionally mask beyond the native320 window.

Final feature reference: `c2103d5f73abd58788af3efb6bf6773da296fc33`. Capture jars/source digests remain their original earlier immutable snapshots; see the source index for final-build reproduction and the organization-only source distinction.
