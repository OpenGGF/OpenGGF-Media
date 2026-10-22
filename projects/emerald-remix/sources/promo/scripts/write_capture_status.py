#!/usr/bin/env python3
"""Capture-stage handoff for Emerald Remix, 2026-10-22; records observed files/commands, no edit/render."""
import hashlib,json
from pathlib import Path
P=Path('/home/farrell/Videos/OGGF/emerald-remix-promo')
R=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
source_names=['remix-triple-final','stock-double-final','remix-opening-final','stock-opening-final','clover-route-final','clover-tail-final','stock-titlecard-reference']
commands=[json.loads(x) for x in (P/'scripts/commands.jsonl').read_text().splitlines()]
lines=['''# Emerald Remix promo — capture-stage handoff

Updated 2026-10-22. Revised plan and gameplay capture stage delivered, with **one unresolved source defect: Clover Valley's native title card is garbled**. The card is retained as a diagnostic and must be repaired/recaptured before composition. All other planned gameplay sources and per-clip contact sheets are present. No promo has been composed or rendered.

## Current plan and preserved material

The current plan is **`edit.py`'s one-line brief fields + `BEAT_SHEET_REVISED.md`** (61.367 s provisional beat grid). All earlier files remain: `BRIEF.md`, `RESEARCH.md`, `BEAT_SHEET.md`, `SHOT_LIST.csv`, `CAPTURE_PLAN.md`, `design/review.html` and the exact old status in `STATUS.planning-session.md` are **superseded**. The prior research and unchanged `audio/` EHZ 2P bed/analysis are retained useful inputs. Existing `scripts/write_plan.py` regenerates the old plan; do not run it over the current files. `coaching/` was not read or changed.

The user's eight criticisms are addressed in the brief/sheet: strongest motion on frame zero; stock/remix comparisons; ROM title-card letterforms; native Clover announcement rather than a caption; purposeful proof instead of momentum/discovery padding; full bleed with comparison layouts; flash/stinger/slam and banded chapter wipe; a readable invitation end card without Java or ROM revision requirements. The native card implementation defect is exposed rather than disguised with editorial text.

## Source and scope

- Worktree: `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`; branch `feature/ai-promo-skill-coaching`; source/compiled SHA `f11ad311fa66016a1729435db21de655aa153600`.
- Git status was clean before work and remains clean. No source edits, branch switches, fetch/pull, commits or pushes. No OpenGGF-Media access/writes. This user-requested production-only scope supersedes repository integration/archive defaults.
- Rebuilt here: `JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 examples/emerald-remix/build.py`. Success; Java 25 compilation and mod validator **0 findings**. No engine test suite ran; captures are bounded gameplay/render evidence, not ROM parity or whole-route certification.
- Supplied existing ROM path unchanged: `<checkout>/s2.gen`; CRC32 `7B905383`; SHA-1 `8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9`. No ROM files/links created, copied or altered.
- Mod: `target/emerald-remix/emerald-remix.jar`; SHA-256 `de1817fbf2950bf565b28c0f334f1de22b45cbd9e57a0cd8cba3cadf2e09e280` (unchanged from planning build).
- Java 25, owned surfaceless EGL pbuffer, `DISPLAY` and `WAYLAND_DISPLAY` removed, default silent `NullAudioBackend` confirmed in boot evidence. No desktop input or audio device used. One capture per JVM.
- Captures use `GameplayCaptureTool`; every controller script was compiled by `InputLogAuthorTool` into BK2 and round-tripped through the production loader. No velocity/ring/clock seeds, invulnerability, debug completion or asset edits. Positioned starts are disclosed below. Initial sampled scouts are reconnaissance only; every editing source is stride 1 at 60 Hz.
- `scripts/capture-config.yaml` preserves the isolated preferences copied into this checkout's `target/promo-capture-prefs/config.yaml`; `-Duser.dir` selects that root. It sets the normal mod-card preference false and points ROM discovery at the assigned checkout. It changes no user preferences.

## Retained editing sources

Each directory contains lossless `frames/`, measured `state.csv`, silent `capture.mp4`, `provenance.json`, `source-review.json` and `contact-sheet.png`. MP4s are raw source previews, not promo renders. PNGs are **400×224**; MP4s are integer 3× **1200×672 / 60 fps**. All seven have complete frame sequences, matching MP4 frame counts and successful full decodes; **zero hurt/dead frames**. The garbled card is a visual failure despite these mechanical checks.

| Source under `captures/` | Frames / duration | Entry and use |
|---|---|---|
| `remix-triple-final` | 900 / 15.000 s | Positioned centre (3904,600), upstream of first spiral; settle → four native spindash revs → right. Three crests and an exit, no hidden state/speed write. |
| `stock-double-final` | 650 / 10.833 s | Matched stock positioned centre (9024,600); same initial controller input, then jump the stock run-out spring after the second twist. |
| `remix-opening-final` | 900 / 15.000 s | Cold EHZ1; jump the added monitor and later lower-route pocket. No seeds. |
| `stock-opening-final` | 900 / 15.000 s | Cold stock EHZ1; same input through f329, then a stock-specific badnik jump. No seeds. |
| `clover-route-final` | 1400 / 23.333 s | Cold mod registry zone 11, act 1; actual mod level assets and native events. The first card interval is **rejected**; clear gameplay follows f145. Spring, ring pickups, upper landing, checkpoint and signpost/results observed. |
| `clover-tail-final` | 520 / 8.667 s | Separate positioned centre (3456,480), right only; fresh run-out for the end card, native finish under the planned final fade. |
| `stock-titlecard-reference` | 240 / 4.000 s | Cold stock EHZ card into play; native letterform, banner and palette reference only. Not a substitute Clover card. |

## CSV-selected source ranges

All ranges are **[in, out)** in source frames at 60 fps, no retiming. These are capture-stage picks; no EDL or compositor shots have been instantiated. The cold open deliberately quotes the later hero. Separate direct loads/positioned excerpts must not imply uninterrupted EHZ2 → Clover progression.

| Beat-sheet use | Source and range | Observed reason / contact sheet |
|---|---|---|
| Cold open, b0–4 | `remix-triple-final` [94,231) | Already entering the first crest; all three and the exit read in 137 frames. `contact-00094-00230.png`. |
| Comparison, b4–12 | Both corkscrew sources [48,318) | Identical charge/release approach; first two crests line up with a +5120 stock X offset, then remix has a third. Stock-only jump begins f180 after its double; no identical-input claim beyond that. Stock pane leaves before its finish becomes idle. `stock-double-final/contact-00048-00317.png`; remix `contact-00048-00452.png` covers this plus continuation. |
| Remix expansion, b12–16 | `remix-triple-final` [318,453) | Continue moving source as the comparison expands full bleed, rather than holding the stock pane. |
| Title, b16–24 | `remix-opening-final` [0,270) | Native moving opening beneath the planned title impact; do not use static scenery. |
| Full hero, b24–40 | `remix-triple-final` [48,588) | Complete charge/release → three linked twists → clean run-out. Corkscrew crossings lie roughly f90–224. 540 frames, no hurt/death. `contact-00048-00587.png`. |
| Route proof, b40–61 | Both opening sources [160,869) | Shared opening becomes visibly different around f220: remix Act 2 hill/ledge versus stock quarter-pipe/bridge. Continue native trajectories through different lower-route sequences. Both selections are damage-free; about 0.5 s trailing handle. Each `contact-00160-00868.png`. |
| Clover native announcement, b61–69 | `clover-route-final` [0,270) **BLOCKED** | Normal card entry/exit into play captured, but zone letters are corrupt. Keep `contact-00000-00269.png` as diagnostic. Repair/recapture, do not put a caption over it. |
| Clover action, b69–85 | `clover-route-final` [270,810) | Continuous hills → monitor bounce → spring hop/launch → upper ring line → landing and run-out. Launch f530–531: yvel −2560 / −2504; upper landing f601 (air 1→0, y380); rings 21→30 across launch/upper route. `contact-00270-00809.png`. |
| Clover finish, b85–97 | Same source [810,1215) | Exact continuation, no repeated action: step jump at f820, final hills, signpost spin, native results request. Boot log observes signpost X5016 and results total ring bonus 500 (50 rings). `contact-00810-01214.png`. |
| End card, b97–109 | `clover-tail-final` [30,435) | 4.75 s of moving run-out then its native finish during the intended final 2 s fade; no frozen-frame padding or clip loop. `contact-00030-00434.png`. |

Clover runtime identity was checked through the actual mod-loaded boot: registry zone 11 / act 0 (CLI act 1), `PreparedModZone` level, native internal zone 64 and `Loading letters for zone: CLOVER VALLEY`; layout readback finds its spring (1832,568) and signpost (5016,544). `captures/inspect-clover.txt` and per-source boot evidence retain that distinction. JSON zone 64 is not the CLI registry index.

Pixel review: inspected the numbered sheets for both opening routes, both corkscrew sources, spring approach/launch/upper landing, final step/finish, native EHZ card and end-card run-out. Player and terrain are present and supporting surfaces line up in those sampled frames. This is **not** a complete 1× moving playback or final-scale motion/aesthetic approval. Those checks remain for the edit stage; no final film codec/audio/transition quality claim is made.

## Exact commands and reproduction

All commands ran from the assigned checkout. `scripts/commands.jsonl` is the complete exact argv/cwd/environment record, including initial scouts and layout readback. Each source's `provenance.json` also has its literal Java command/classpath, ROM/mod/input hashes, entry and selected boot evidence. The driver rejects an existing output directory; use a new take name if reproducing.

Build was as recorded above. Inputs used by final sources were authored with:

```bash
''']
for n in ['corkscrew-dash','stock-corkscrew-clean','remix-route04','stock-opening02','clover-route05','clover-tail-run','corkscrew-run']:
 lines.append(f'python3 {P}/scripts/capture.py author {n}\n')
lines.append('''```

Exact capture-driver commands for the retained sources (the driver launches the production CLI, never a substitute renderer):

```bash
''')
for n in source_names:
 m=json.loads((P/'captures'/n/'provenance.json').read_text());a=m['argv'];val=lambda flag:a[a.index(flag)+1]
 script=Path(val('--input')).stem
 opts=[]
 if '--x' in a:opts+=['--x',val('--x'),'--y',val('--y')]
 if '--mod' not in a:opts+=['--stock']
 if '--title-card' in a:opts+=['--title-card']
 opts+=['--video']
 lines.append(f'python3 {P}/scripts/capture.py capture {n} {script} {val("--zone")} {val("--frames")} {val("--every")} '+ ' '.join(opts)+'\n')
lines.append('''```

For clarity, the exact common Java launch shape expanded by that driver is:

```bash
CHECKOUT=/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach
CP="$CHECKOUT/target/classes:$(cat "$CHECKOUT/target/examples-classpath.txt")"
env -u DISPLAY -u WAYLAND_DISPLAY JAVA_HOME=/usr/lib/jvm/java-25-openjdk \
  /usr/lib/jvm/java-25-openjdk/bin/java --enable-native-access=ALL-UNNAMED -Xmx2g \
  -Djava.awt.headless=true -Dopenggf.headless.gl=surfaceless-egl \
  -Duser.dir="$CHECKOUT/target/promo-capture-prefs" -cp "$CP" \
  com.openggf.tools.GameplayCaptureTool \
  --game s2 --rom "$CHECKOUT/s2.gen" --zone ZONE --act 1 \
  --width 400 --main sonic --sidekick none --input INPUT_BK2 \
  --frames FRAME_BUDGET --every 1 --fps 60 --out-dir NEW_TAKE_DIR \
  --scale 3 [--mod "$CHECKOUT/target/emerald-remix/emerald-remix.jar"] \
  [--x CENTRE_X --y CENTRE_Y] [--title-card]
```

Uppercase fields above explain the shape; the seven literal commands and JSON argv supply exact values. `--stock` and `--video` are **driver-only switches**, not GameplayCaptureTool flags. The driver implements stock by omitting `--mod`, and video by omitting `--no-video`. Input authoring uses the same compiled classpath with `com.openggf.tools.InputLogAuthorTool --script <script> --out <bk2> --game s2`.

Contact-sheet command, run for every clip after reading its CSV:

```bash
target/promo-planning-venv/bin/python /home/farrell/Videos/OGGF/emerald-remix-promo/scripts/contact_sheet.py <clip-directory> [in-frame last-inclusive-frame]
```

`inspect_sources.py` checked contiguous PNG numbering, source intervals, no hurt/death, ffprobe dimensions/fps/frame counts/no audio and `ffmpeg -v error -xerror -i <capture.mp4> -f null -` for the six main sources. The native stock-card reference received the same probe/decode checks separately. Python syntax was parsed without generating bytecode. Checks were run once; changed selections regenerated their affected sheets without repeating unchanged video decodes.

## Problems, rejected takes and remaining work

- **Clover native card is not usable.** Default `mods.skipModZoneTitleCards: true` silently skips the presentation (`clover-scout01` log: `Skipping unsupported title card for mod zone 11`). Turning it off in the isolated preference root activates the native card, but the loaded CLOVER VALLEY art is drawn with corrupt/incorrect letter positions. Source inspection explains a likely cause: `TitleCardMappings.getZoneFrame(11)` falls back to the stock EHZ mapping, while `TitleCardManager.loadZoneLetters` loads the mod name. Captured f50 is visibly garbled; successful CLI completion is not success here. Engine/card repair and a fresh card→play capture are open. No engine fix was made or card fabricated in this capture-only assignment.
- The capture skill lists `--title-card` but does not mention the mod-card skip preference or the unsupported custom glyph mapping. `--title-card` alone therefore does not deliver the requested Clover card. Record this in future tool/docs work; no repository docs were changed here.
- Stock EHZ's native card renders correctly. Sampled f50 palette: blue `(48,87,206)` / `#3057CE`, yellow `#FFFF00`, red `#FF0000`, white `#FFFFFF`. The brief now uses these real sampled values. ROM alphabet extraction/redrawing for EMERALD REMIX (including X) is deferred with composition, rather than substituting a system TTF.
- Pure right input stops at the remix's added monitor (`remix-scout01`), then the lower route can stall/die (`remix-scout02/03`). Timed native jumps produce the clean retained cold opening. A short runway before the spiral loses the required speed and falls to the lower path (`remix-corkscrew-scout01`); an earlier positioned start also misses the upper route (`...scout03`). The retained native spindash approach has enough speed and traverses all three, with no speed writes or immunity. It stays rolled during the twists; do not describe it as upright running animation.
- Several Clover scouts stop at the stepped floor or spring side; the final script hops onto the spring, shows its actual upward impulse and lands above. The first positioned end-card scout started on a steep incline and crawled; rejected in favour of the flat run-out. All 22 reconnaissance clips remain identified as superseded in provenance, with CSVs and per-clip sheets. Do not edit sparse scouts at 60 fps or silently promote them.
- One source-study `sed` path for `TestEmeraldRemix` was stale; the current test is `src/test/java/com/openggf/mods/code/TestEmeraldRemix.java`. No test bot or its damage immunity was used. The existing NumPy/Pillow venv worked; no new global Python packages were installed. EGL and ffmpeg succeeded without display fallback. No new Maven/temp-file error or capture crash occurred.
- Music listening/downbeat confirmation, native alphabet/logo extraction, editorial stinger rendering/mixing, compositor implementation, 1× motion review, final typography/transition/audio/codec checks and any later archive work remain outside this stop point. The existing music WAVs/analysis were not rewritten.

No task-owned processes, command sessions or agents remain running at handoff; no workers were created. Build/capture execution and source inspection occurred; aggregate elapsed/execution timing was not measured, and no test-queue wait is claimed. Repository outputs are limited to ignored `target/`; production assets and scripts remain here. **Stop: captures and contact sheets only.**
''')
(P/'STATUS.md').write_text(''.join(lines))
# Brief palette is now measured rather than an unfulfilled sampling instruction.
f=P/'edit.py';s=f.read_text().replace('Sonic 2 title-card blue, yellow, red and white; sample final RGB from the captured native card rather than a generic brand palette.', 'Native stock card f50: blue #3057CE, yellow #FFFF00, red #FF0000, white #FFFFFF; sampled from the captured Sonic 2 presentation.')
f.write_text(s)
print(P/'STATUS.md')
