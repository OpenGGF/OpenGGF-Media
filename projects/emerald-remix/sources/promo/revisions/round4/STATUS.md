# Emerald Remix promo — coached revision

2026-10-22. Working checkout: `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`, branch `feature/ai-promo-skill-coaching`, source **`c6d96fb37ac372663a3a4b284945e064d58e1eea`**. Production root: `/home/farrell/Videos/OGGF/emerald-remix-promo/`.

**Complete through the requested rough-cut stop point.** Final whole cut and all nine changed-section/context previews are rendered, verified and available below. Full-size compositor and final encoded frames were inspected. No repository changes, commits, pushes, separate mastering stage or OpenGGF-Media operations.

## Why this revision exists

The user's feedback on the preceding 41-second cut:

> "it's use of palettes with the text is horrible, particularly around the drop shadow"

> "the video is just very... boring. I know that the mod is just minor changes to existing levels and a new tileset for the other, but it's just very lazy with long stretches of level showcased without any accompanyment."

The causes were the flattened ROM glyph palette, added thin navy/red effects, and footage used as filler: the updated checker found 14.0 s of bare Clover and 4.4 s of bare hero footage. This revision changes both causes.

## What changed, and what the viewer sees

- **Stock Sonic 2 type, including its actual shading.** `ExtractTitleFont.java` now retains ROM palette indices instead of turning every nonzero pixel white. Sampled `captures/stock-titlecard-reference/frames/00062.png`: index 6 white, 1 black, 7 `#B6B6B6`, 8 `#929292`; card blue `#3057CE`. The black shadow is **already embedded in the ROM glyph at +2,+2 native pixels**. `BitmapFont.render(..., shades=SHADES, outline=None, drop=None)` therefore adds no second shadow or outline. Removed yellow recolouring, the red drop and the mask-wide shine. Fixed-size integer-scale glyphs slide into place; the captured picture still supplies the title slam.
- **The construction becomes a beat.** Four new beats show the actual double and single corkscrew pieces arriving separately and joining under **CUT FROM YOUR ROM**, then **ONE TRIPLE**. The true 768/384-pixel division comes from the recipe. `prepare_revision.py` assembles the world-aligned foreground from existing capture columns, avoiding the actor/HUD; only the two large track components remain. This is an editorial art diagram, not a fake editor feature or gameplay capture.
- **The hero remains one complete run.** **NOW RUN IT** invites the viewer in, then clears before the triple's strongest animation. Source 65–335 is still native speed, unrolled and uninterrupted. The cold open still quotes its best poses. ONE/TWO/THREE comparison and title flash/C3 stinger/26-frame slam remain.
- **Clover's originality gets a visual cause.** **A ZONE DRAWN BY CODE** accompanies a row-by-row scan of the exact 16×16 clover returned by the mod's `decor_pixel("clover",x,y)` function, enlarged at a fixed 18×. PIXEL RULE identifies an art graphic. The generator reads no ROM. It is not a filmed editor operation or a claim that the game generates the art live.
- **Every Clover bar advances the invitation.** Native card-style entrance → generated-art reveal → **TAKE THE HIGH ROAD** on the spring → **FOLLOW THE GOLD** on the upper ring trail → **ONE MORE LEAP** on the step jump → **HOW FAST CAN YOU GO** over the last crest → **YOUR TURN** at the signpost. A subtle 4.5% compositor punch and ROM CC spring cue land on the observed source f435 / output f1553; no fake ring tally or invented collection sounds.
- **Readability corrections from full-size review.** All practical lower captions sit above the life counter; comparison labels avoid the HUD; Clover's red tab begins to the right of every top HUD digit. The end of the 400px Clover capture reveals terrain beyond the act's native right bound and an offscreen-exit pose. The final five beats use a **held** crop `(cx=160, cy=89.6, zoom=1.25)`, with no retiming or camera travel, so Sonic exits the cropped view and the top HUD rows remain intact. No engine fix or recapture was attempted.

The promise is **your ROM, rearranged — then somewhere entirely new**. The added assembly makes the cut **43.366667 s / 2602 frames**, 1920×1080, 60 Hz. Clover source 100–1079 is still continuous across the held-crop boundary. The separate fresh end-card run is disclosed. No loops, freezes or time warps were added. Positioned corkscrew/end-card entries and direct-load openings/Clover retain their original provenance; there is no claim of one continuous EHZ-to-Clover playthrough.

## Current deliverables

- `out/emerald-remix-rough.mp4` — complete revised rough, 2602 frames.
- `edit.py` — editable brief and authoritative timeline.
- `BEAT_SHEET_REVISED.md` and `chapters.json` — frame/source map and accompaniment beats.
- `previews/` — full-size, 60 Hz, corresponding audio mix: `cold-open.mp4`, `comparison.mp4`, `title-drop.mp4`, `remix-build-run.mp4`, `clover-entrance.mp4`, `clover-pixels.mp4`, `clover-high-road.mp4`, `clover-finish.mp4`, `end-card.mp4`. Exact [in,out) ranges in `previews/ranges.json`.
- `build/sheet-0.png` — 30-frame / half-second sampling; `build/frame-*.png` — full-size layout and boundary checks. These are diagnostics, not the video review itself.
- `design/native-card-treatment.png`, `design/revision/type-sampling.json`, `design/rom-title-font/` — palette/reference evidence and regenerated native alphabet.
- `design/revision/rom-triple-art.png`, `clover-pixel-function.png` — actual art used in the two new editorial graphics.

## Check output and verification

Final `promo_kit.py check edit.py` output:

```text
pacing: {'shots': 9, 'mean_shot_s': 4.82, 'busiest_window_cuts': 6, 'cuts_in_last_window': 2, 'seconds': 43.37, 'longest_bare_s': 0}
```

`e.check()` returns **`[]`**, with **no bare-stretch warning**, gap, overrun or pacing warning. `longest_bare_s: 0` means no stretch exceeds the checker's four-second threshold; it does not assert an overlay on every frame. The closing crop is one additional editorial shot; there are only two cuts in the last 20 seconds.

Final held-crop render: **probe and complete decode passed for the whole cut and all nine previews**, with exact frames, dimensions, FPS and audio assertions. `scripts/verify_revision.py` exited 0 on the final exports. Syntax passed for `edit.py` and every `scripts/*.py`.

| Export | Frames | Seconds |
|---|---:|---:|
| Whole rough | 2602 | 43.366667 |
| cold-open | 180 | 3.000000 |
| comparison | 418 | 6.966667 |
| title-drop | 306 | 5.100000 |
| remix-build-run | 441 | 7.350000 |
| clover-entrance | 170 | 2.833333 |
| clover-pixels | 300 | 5.000000 |
| clover-high-road | 310 | 5.166667 |
| clover-finish | 445 | 7.416667 |
| end-card | 427 | 7.116667 |

Every export is 1920×1080, 60/1, stereo 48 kHz. Final encoded AAC measurement: **−13.2 LUFS integrated, 1.5 LU loudness range, −1.7 dBFS true peak**. These are observations of the unchanged rough-mix processing; no separate master was made.

Review: inspected the full-size title, both comparisons, assembly arrivals/join, Clover header, pixel scan, spring, caption/character clearance, finish crop and end card. Also extracted and inspected final encoded **1920×1080** frames 935/1260/1410/2095 (`build/encoded-*.png`). Played the final complete 43.366667-second file at **1×**, 1920×1080 video in a 1920×1116 browser viewport, reaching `ended=true` with no media error or midstream stall. Browser telemetry reported **30 dropped frames out of 2602**, concentrated at startup (93 presented at media t=2 s, then roughly 120 per two-second sample). Thus the browser review is bounded, not a claim of perfect delivery cadence. Full ffmpeg decode covered all encoded frames. Agent review used visual snapshots during playback plus full-size frames; physical hearing and human aesthetic acceptance are not claimed.

Native type evidence: eight reference letters (E/M/R/A/L/D/H/I) have palette-exact ink matches against frame 62. M's transparent padding overlaps neighbouring native glyphs, so the comparator checks its actual ink rather than demanding empty neighbouring pixels. Re-running the Java extraction and asset-preparation script reproduced the font, final track matte and generator decoration **byte-for-byte**. Every font role reports `ok`; practical URL/status/disclaimer remain Fira Sans Condensed Bold Italic.

No engine tests were run: this revision changes only production files outside the repository and ignored Java helper output under this checkout's `target/`. Existing gameplay takes were reused unchanged. This is media validation, not a new ROM-parity or gameplay-completion certification.

## Exact commands

Commands below are shell-reproducible forms of the actual absolute-path invocations. No command commits, pushes or archives. Build/run cwd is the assigned checkout unless a command explicitly changes to the production directory. Existing compiled engine classes were reused; the local font helper was rebuilt with JDK 25 into this checkout's `target/`.

```bash
CHECKOUT=/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach
PROD=/home/farrell/Videos/OGGF/emerald-remix-promo
PY="$CHECKOUT/target/promo-planning-venv/bin/python"
KIT="$CHECKOUT/tools/media/promo_kit.py"
cd "$PROD"
python3 scripts/extract_title_font.py
"$PY" scripts/prepare_revision.py
python3 scripts/render_spring.py
"$PY" scripts/update_revision_docs.py
"$PY" "$KIT" check edit.py
"$PY" "$KIT" fonts
"$PY" "$KIT" frames edit.py 200 470 620 845 890 925 1000 1260 1410 1510 1590 1700 1830 1960 2095 2330
"$PY" "$KIT" frames edit.py 470 620 855 900 935 1260 1410 1590 1700 1830 1960 2095 2330
"$PY" "$KIT" frames edit.py 1260 1350 1553 2115
"$PY" "$KIT" frames edit.py 935
"$PY" "$KIT" frames edit.py 2029 2095 2115 2175
"$PY" scripts/render_previews.py
"$PY" scripts/render_previews.py clover-entrance clover-pixels
"$PY" scripts/render_previews.py remix-build-run
"$PY" scripts/render_previews.py clover-finish end-card
"$PY" "$KIT" sheet edit.py 30
"$PY" "$KIT" render edit.py
"$PY" scripts/verify_revision.py
```

The initial sheet used step 60, then the review sheet step 30. Whole renders were repeated only after new matte/framing corrections; the same output path is the current cut, not multiple candidates. Previews were repeated only for affected sections after those corrections. Font regeneration was additionally wrapped in a SHA-256 before/after assertion (font text, final track art, generator clover); it passed.

`extract_title_font.py` runs these exact JVM tools and input paths, with `CP` equal to `target/classes` plus the contents of `target/examples-classpath.txt`:

```bash
/usr/lib/jvm/java-25-openjdk/bin/javac -cp "$CP" -d "$CHECKOUT/target" "$PROD/scripts/ExtractTitleFont.java"
/usr/lib/jvm/java-25-openjdk/bin/java -cp "$CHECKOUT/target:$CP" ExtractTitleFont "$CHECKOUT/s2.gen" "$PROD/design/rom-title-font"
/usr/lib/jvm/java-25-openjdk/bin/java --enable-native-access=ALL-UNNAMED -cp "$CP" com.openggf.tools.audio.FmSfxRenderTool --game s2 --rom "$CHECKOUT/s2.gen" --sfx cc --rate 48000 --max-seconds 4 --out "$PROD/audio/stingers"
```

CC render completed: **51,200 frames / 1.066667 s, 223 YM writes, complete=true**. It is editorially aligned to the captured spring, not recovered from the silent take. One uninterrupted EHZ 2P bed remains the music owner. `promo_kit.mix()` uses its existing preview processing; no separate master or final listening approval was performed.

`verify_revision.py` uses `ast.parse()` over the edit and all `scripts/*.py`, asserts an empty checker result and 2602-frame duration, then executes the following exact argv forms for the whole cut and every file in `previews/ranges.json`:

```bash
ffprobe -v error -show_streams -show_format -of json <absolute-mp4-path>
ffmpeg -v error -xerror -i <absolute-mp4-path> -f null -
ffmpeg -hide_banner -nostats -i "$PROD/out/emerald-remix-rough.mp4" -af ebur128=peak=true -f null -
```

Four final encoded frames were also extracted with argv `ffmpeg -v error -y -i <absolute-rough-path> -vf "select=eq(n\\,N)" -frames:v 1 <absolute-build/encoded-N.png>`, for N=935,1260,1410,2095, then opened at original resolution.

The last command measures encoded AAC only; it does not modify the rough. Metadata checks require 1920×1080, `60/1`, exact frame counts, stereo 48 kHz and duration within 0.06 s. Preview WAV scratch files are deleted after successful mux.

## Tool, source and documentation issues

- Read the assigned checkout's current `AGENTS.md`, `promo-direction/SKILL.md`, `references/lessons.md` and `references/moves.md` directly. The catalogued older paths were not treated as authority. The documented `shades=` API and bare-stretch checker worked.
- Stock type's black shadow is already in the extracted pixels. Blindly supplying an additional sampled `drop=` would double it. Preserving indices and using `drop=None` is the observed correct treatment for this art.
- First palette comparison demanded transparent M padding be empty, but native neighbouring glyphs overlap five of those pixels. The corrected comparison checks all ink pixels with their own palette colours; it still checks both grey indices through R/A/D.
- First track matte kept only the largest component and lost the single corkscrew. Full-size review caught it; the actual two large components are now retained. A later review caught native HUD fragments in stitched source columns; explicit HUD-column exclusion removed them. Both corrections are in reproducible `prepare_revision.py`, not painted onto a final frame.
- The 400px take shows beyond Clover's native right bound late in the goal run. Final held cropping handles it editorially. No gameplay source is altered and no engine fix is claimed.
- Native Clover custom-name title cards remain the prior presentation limitation. Retained footage uses `mods.skipModZoneTitleCards: true` and no `--title-card`; the overlay is editorial.
- Browser setup first returned `Invalid preview URL (parse: https:; input length 11)` for `about:blank`; corrected to the task-owned localhost HTTP page. A resize attempt returned `Expected "fill" | "freeform" | "preset"`; corrected to `freeform` at 1920×1116 (1080px video plus navigation). The first review-page visit preceded its preview encode and logged one 404; reloading the completed file returned 200. These were setup errors, not export failures.
- The skill's archive/default final-delivery workflow is superseded by the user's explicit **rough only; do not master/archive; do not touch OpenGGF-Media**. No archive path was read or written in this revision. Reference treatments draw on the already recorded research and the local native title-card capture.

Review server command: `python3 -m http.server 8873 --bind 127.0.0.1 --directory "$PROD"`. Browser page: `previews/review.html`, task-owned tab. The owned browser tab was closed and the exact task-owned HTTP server process was stopped after review. All encoding/verification commands completed; no capture, Maven or worker process was launched or left running by this revision.

Earlier capture-stage provenance remains in `STATUS.capture-session.md`, `scripts/commands.jsonl` and each take's `provenance.json`/state CSV. Existing older planning files are historical; this status, revised beat sheet and instantiated edit are current.

Final checkout check: `git status --short` was empty; `git rev-parse HEAD` remained `c6d96fb37ac372663a3a4b284945e064d58e1eea`; branch remained `feature/ai-promo-skill-coaching`. No mastering, archiving or repository delivery is pending within this assignment. Total elapsed task time was not measured; no Maven queue wait occurred.
