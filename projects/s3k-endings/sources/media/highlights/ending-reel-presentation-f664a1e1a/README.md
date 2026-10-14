# S3K ending presentation highlights — integration pending

61 seconds; silent 1600×520 at 15fps; nearest-neighbor logical 2× gameplay. [Watch the reel](s3k-ending-highlights-presentation-repair-provisional.mp4).

Chapters 1–6 use the qualified Sonic Chaos320 and Tails Super800 presentation excerpts from source `70c09903`, immutable jar `ed7dc650`, repair commit `f664a1e1a`. They are declared native ending scene entries with inventory present before the first native object pass. Chapters 7–12 retain the unaffected historical credits, banner and Knuckles flight/terminal/title films from source `b2af901c`, jar `a302e015`; their full original provenance remains in the task archive. Knuckles follows the actual maintained final-fight BK2 from input0, then neutral.

The parent integration merge is `7df0c44cb`; this reel is not a recapture of that merged runtime or a claim of latest-integrated pixel parity. Focused graph/art/palette/rewind and affected lifecycle checks are qualified. Combined integration smoke/guards remain lead-owned and pending. Editorial cuts do not prove an uninterrupted cold campaign or whole-scene native parity.

| Reel seconds | Chapter | Source | Native input interval (end exclusive) | Source film seconds |
| --- | --- | --- | --- | --- |
| 0–6 | Sonic - Tornado rescue / Master Emerald | Repair Sonic Chaos320 | 1100–1460 | 10/3–28/3 |
| 6–13 | Sonic - IslandLift departure | Repair Sonic Chaos320 | 1620–2040 | 12–19 |
| 13–17 | Tails - IslandLift departure | Repair Tails Super800 | 2920–3160 | 101/3–113/3 |
| 17–23 | Tails - AIZ Master Emerald restoration | Repair Tails Super800 | 3820–4180 | 146/3–164/3 |
| 23–27 | Tails - AIZ restoration hold / palette cycles | Repair Tails Super800 | 4240–4480 | 167/3–179/3 |
| 27–31 | Tails - Super reunion | Repair Tails Super800 | 4520–4760 | 181/3–193/3 |
| 31–37 | ROM credits | Historical Sonic incomplete320 | 6240–6600 | 104–110 |
| 37–41 | Sonic - post-credit banner | Historical Sonic incomplete320 | 13260–13500 | 221–225 |
| 41–45 | Knuckles - powered flight with Master Emerald | Historical Knuckles Super800 | 9052–9292 | 238/15–298/15 |
| 45–49 | Knuckles - turning plane and departure | Historical Knuckles incomplete800 | 9292–9532 | 298/15–358/15 |
| 49–57 | Knuckles - Mecha and Master Emerald terminal | Historical Knuckles incomplete800 | 22300–22780 | 710/3–734/3 |
| 57–61 | Return to the title screen | Historical Knuckles incomplete800 | 24460–24700 | 818/3–830/3 |

Native input maps to film time as `capture_from + 60 × source_seconds`. New excerpts start at input900, every4; historical Sonic starts at0/every4, Knuckles at8100/every8. CSV frame is submitted input index, not VInt. Input0 can run initial native setup without advancing VInt. Native60-input playback is preserved: historical 15/2fps images duplicate to15fps with no interpolation or speed change. Wide films retain native-window flank masking.

Reproduce with `python3 assemble.py --root <task-source-root>`. The existing full source archive stays at the task root; no source movies are duplicated here. `chapters.edl.json` records exact rational intervals, frame/input mappings, per-chapter setup labels and video/CSV/jar/source hashes. `source-index.snapshot.json` pins the source archive metadata used for authoring; the [live task index](../../ending-capture-index.json) may later gain the final reachable pushed-develop reproduction target while historical hashes remain unchanged.

`media-verification.json` records the output and assembler/EDL hashes, exact chapter times, full xerror decode, per-chapter decoded frame variation and temporal/cut samples. Three temporal sheets show 10/50/90% of all twelve chapters; two cut sheets show both sides of all eleven boundaries. Earlier reels and their negative/corrected source evidence remain intact.
