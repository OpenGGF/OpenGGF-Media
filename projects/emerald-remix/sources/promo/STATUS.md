# Emerald Remix promo — round 5 rough

2026-10-22. **41.683333 s / 2,501 frames, 1920×1080 at 60 fps.** Current film: `out/emerald-remix-rough.mp4`. Current source: `edit.py`, `chapters-round5.json`, `previews/ranges.json`. Seven changed-section previews are listed below. This is a new rough for human creative review; no master, archive, commit or push was requested or performed. OpenGGF-Media was not accessed.

User feedback driving this revision: **“minimal effort has been put in to achieve the goals”.** Round 4's native Sonic 2 type palette and double + single → triple construction are retained. Its repeated Clover slogans and corner-size generator decoration are removed. An empty checker warning list is a mechanical floor, not the creative objective.

## Treatments considered and selected

| Weak section | Treatment | Decision and reason |
|---|---|---|
| Clover run | A. Trim the original take and retain one chapter caption. | Rejected: shorter but still asks scenery alone to carry the pitch. |
| Clover run | B. Event-led three-passage edit: spring → high platform and pickups; complete last jump → landing; ring run → signpost. Actual pickup counter, pips and quiet ring cues follow CSV gains. | **Built.** The spring has an approach and consequence, the counter makes the high route a payoff, and each later cut reveals another action. Travel between them is cut out. Native speed is preserved. |
| Clover run | C. Ambitious simultaneous three-panel spring / flight / landing choreography, with a moving route map. | Rejected: several times at once would compete for attention, reduce Sonic and make the simple native action harder to read. The new generator panorama already supplies the map-scale view. |
| Drawn by code | A. Enlarge the decoration and cycle three actual generated tiles. | Rejected: still sells a few tiles rather than a whole place. |
| Drawn by code | B. Source-code panel beside a live view, with the real soil equation highlighted. | Rejected: the technical reading load would slow the pitch for Sonic fans. |
| Drawn by code | C. Ambitious landscape build: use the **actual pixel function** to draw sky, peaks, soil, grass, slopes, decorations and floating ledge in a travelling chunk wave; draw the entire 5,120-pixel route below; open a gold-ring iris into native play in that region. | **Built.** The screen becomes a place to play. Large scenic detail and the complete route make the scale visible; a single 16px decoration no longer stands in for the zone. |
| Type over gameplay | A. Stronger gradient / more drop shadow over the footage. | Rejected: grass and clouds would still break the native letter silhouettes. |
| Type over gameplay | B. Sonic 2 blue title-card bands, red serrated tabs and yellow footers; preserve all white/grey/black ROM glyph pixels. Let the band's movement carry the title entrance. | **Built.** The native negative spaces and bevels read against one stable field. Comparison labels and the construction headline use the same blue vocabulary. |
| Type over gameplay | C. Ambitious giant letter-window wipe, with gameplay inside the letters before resolving to native colours. | Rejected: a busy texture inside the letters repeats the exact silhouette problem the user identified. The native card treatment is the stronger readable choice. |

References: the locally recorded Putt-Putt Sonic 2 band treatment, native card frame 62, and the skill's Slay-style comparison/build-to-gameplay grammar. No new reference-video or Media-repository access was made. Current `.agents/skills/promo-direction/SKILL.md`, `references/lessons.md`, `references/moves.md` and gameplay-highlights guidance were read directly in the assigned worktree. The explicit rough-only/no-archive instruction overrides the skill's default final-delivery archive requirement.

## Current edit and source evidence

| Output | Picture / source interval [in,out), at 60Hz |
|---|---|
| 0.000–2.283 | Cold hero, `remix-tumble-hero-final` [103,240). |
| 2.283–6.800 | Counted stock/remix split; wide sources [50,321). |
| 6.800–9.050 | Opening-route split; stock/remix opening sources [195,330). |
| 9.050–13.550 | Native-palette title on blue card band; remix opening [0,270). |
| 13.550–15.800 | Actual ROM foreground double and single assemble into triple; editorial art diagram. |
| 15.800–20.300 | Triple payoff, hero [65,335), with a small schematic counting its native sections. |
| 20.300–24.800 | Actual generated landscape / whole-zone panorama draws in; editorial art diagram, not an editor UI or engine capture. |
| 24.800–29.300 | Clover [410,680): spring approach, launch, high-platform landing, pickups and slope. |
| 29.300–31.550 | Clover [710,845): complete final leap, landing and crest. |
| 31.550–34.933 | Clover [850,1053): ring run and goal spin, held 320px editorial crop. |
| 34.933–41.683 | End-card invitation over fresh moving tail source [30,435), then fade. |

The two wide comparison sources are `stock-tumble-wide-exit02-final` and `remix-tumble-wide-final`. All CSVs and original capture provenance remain untouched. Their own recorded capture SHAs, entries, input and ROM hashes remain authoritative; the editing checkout is now **7d7246fbe0913683b88d114b4081d73fc039b80a**, branch `feature/ai-promo-skill-coaching`. `git diff 2f18020dae5ad9b1c59918cc5d15c474a9bb10ba HEAD -- examples/emerald-remix` was empty, so the current generator/example matches that retained shipping capture source. No new gameplay recording or engine build was necessary.

Measured Clover events from `clover-shipping-route-final/state.csv`:

- **435:** spring impulse yvel −2560, x1820/y548; editorial punch and ROM CC spring cue align here (output frame 1513 / 25.2167 s).
- **455:** first post-launch ring, 21→22; the counter opens at +1.
- **506:** high-platform landing, air 1→0, y380, yvel0 (output frame1584 / 26.400s).
- **507–539:** high ledge's ring line, total23→30. **597–650:** hill and downhill line, total30→43. Counter shows the actual gain from21, ending at **22**, with one pip per gain; no invented score.
- **710–794:** last takeoff to grounded landing; yvel−2565 at710, air0/yvel0 at794. Landing accent at output1842 / 30.700s.
- **858–902:** six final rings, total43→49. Signpost at world x5016; CSV x5015 at976 and x5022 at977. Source frame980 onward was visually checked for the spinning goal; the invitation starts there, after the crossing. Signpost state is visual evidence, not an unrecorded field invented in the CSV.

The strip assembly and landscape build are explanatory animation. Generator art uses the source foreground function at its real world coordinates, the same background pixel function and palette; the diagram's scenic background framing is editorial and does not claim native parallax. Its large window is world x1536..2816, y256..768, with the entire route below. The imagery is generated directly without running the generator's file-writing CLI. Gameplay itself is never retimed, resimulated or repainted.

Corkscrew hero and comparison captures have positioned entries, as disclosed in their provenance. Clover shipping route is the retained cold direct-act load with scripted inputs and no position/velocity/ring/clock seeds; this **edited** selection does not advertise an uninterrupted completion. Clover tail is a separate positioned source. Clover's unsupported native custom-name card remains the inherited presentation gap; retained shipping footage skips that card, and the new blue name band is editorial.

## Viewer pass — one row per four seconds

| Output seconds | What is new on screen | Why keep watching? |
|---|---|---|
| 0–4 | Native corkscrew tumble immediately; the full-screen view opens into matched original/remix strips. | Recognisable Sonic 2 motion becomes a visual spot-the-difference question. |
| 4–8 | Original stops at TWO; remix reaches THREE. A second split reveals the changed opening route. | The viewer sees and counts the remix, then discovers it affects more than one feature. |
| 8–12 | Route comparison resolves into a flash/stinger/slam and a large readable native title on its blue band. | The demonstrated difference gets a name worth remembering. |
| 12–16 | The native foreground double and single arrive separately and join at the real seam, then the cut returns to Sonic. | A simple construction trick becomes a playable challenge, rather than a claim on a caption. |
| 16–20 | Sonic traverses all three sections; the schematic fills ONE, TWO, THREE in sequence. | The construction pays off in native movement. The viewer can count along. |
| 20–24 | A gridded field becomes sky and peaks, then original terrain, ledge, grass and decorations; the full-zone strip draws below. | The remembered idea is a whole world drawing itself into existence. |
| 24–28 | Gold-ring iris opens into the spring; launch and high-platform landing get exact accents; pickups begin filling the counter. | The newly drawn world is immediately playable, and the spring earns a visible route and ring payoff. |
| 28–32 | The counter reaches22 on the downhill sweep, then a new complete leap lands and carries over the crest into the goal run. | Collection resolves into a new physical action; uneventful intervening travel has been removed. |
| 32–36 | Last rings, signpost crossing and native spin, followed by the closing blue-band identity and source invitation. | The run has a payoff and a clear next step. The invitation follows the actual goal. |
| 36–40 | Full end-card layout: name, two-part promise, source path, example status and disclaimer over a separate moving run-out. | Intentional reading time to identify and find the example. This is the closing invitation, not a caption used to sustain an otherwise empty gameplay take. |
| 40–41.683 | Music and complete card fade together to black. | A clean, deliberate finish after the link's reading hold; no extra traversal appended. |

Changes made after this pass/layout review: removed the repeated Clover slogans; cut the travel between complete actions; replaced the corner decoration with the landscape build; added the factual pickup counter; gave native type a solid backing; enlarged the pickup panel so its label clears the yellow footer. Dense transition inspection then caught title letters arriving ahead of their band for a few frames: their movement is now coupled, and the affected previews and whole cut were re-rendered.

## Previews and verification

| Current preview | Frames | Seconds |
|---|---:|---:|
| `previews/comparison.mp4` | 430 | 7.166667 |
| `previews/type-and-strip.mp4` | 441 | 7.350000 |
| `previews/triple-payoff.mp4` | 306 | 5.100000 |
| `previews/drawn-by-code.mp4` | 334 | 5.566667 |
| `previews/clover-spring-rings.mp4` | 324 | 5.400000 |
| `previews/clover-jump-goal.mp4` | 392 | 6.533333 |
| `previews/end-card.mp4` | 429 | 7.150000 |

Final `promo_kit.py check edit.py` output:

```text
pacing: {'shots': 11, 'mean_shot_s': 3.79, 'busiest_window_cuts': 6, 'cuts_in_last_window': 4, 'seconds': 41.68, 'longest_bare_s': 0, 'busiest_window_captions': 1}
```

`e.check()` returns `[]`. This does not establish creative acceptance; custom compositions/counters are graphics and cannot be judged for value by the bare-stretch detector. The viewer pass above is the separate editorial assessment.

`scripts/verify_revision.py` exited0: syntax for edit/all scripts, exact output frame counts, 1920×1080 / 60/1, stereo48kHz, durations, and complete ffmpeg decode passed for the whole film and all seven current previews. Final encoded rough AAC: **−13.2 LUFS integrated, 1.6LU range, −1.6dBFS true peak**. This measures the existing rough-mix processing; no separate mastering pass was made. Every font role reports `ok`.

Visual review includes the half-second contact sheet, original-size 1920×1080 title/diagram/build/counter/goal/end frames, and **150 dense transition frames** (every4 output frames across all ten cuts, 56-frame windows). The final title entrance was reviewed again after coupling it to its band. `previews/transition-frames/` retains these review strips and their exact frame ranges. These strips supplement the moving previews; they do not prove perfect playback cadence or audio quality.

Browser playback review and final ownership/cleanup results are appended below after completion.

## Exact commands

Paths below match the actual invocations; `cd` selects each command's recorded working directory. No repository source or Media checkout was modified. Existing venv / compiled capture sources were reused.

```bash
CHECKOUT=/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach
PROD=/home/farrell/Videos/OGGF/emerald-remix-promo
PY="$CHECKOUT/target/promo-planning-venv/bin/python"
KIT="$CHECKOUT/tools/media/promo_kit.py"
cd "$PROD"
"$PY" scripts/prepare_round5.py
"$PY" "$KIT" check edit.py
"$PY" "$KIT" frames edit.py 620 850 1300 1400 1450 1510 1650 1780 2010 2240
"$PY" "$KIT" frames edit.py 1140 1390 1450 1650 1780 2010 2240
"$PY" "$KIT" sheet edit.py 30
"$PY" scripts/render_round5.py
"$PY" scripts/review_round5.py
"$PY" "$KIT" frames edit.py 547 551 555 620 1650 2040 2240
"$PY" scripts/render_round5.py rough
"$PY" scripts/render_round5.py comparison type-and-strip
"$PY" scripts/manifest_round5.py
"$PY" scripts/verify_revision.py
"$PY" scripts/review_round5.py
cd "$CHECKOUT"
"$PY" tools/media/promo_kit.py fonts
 git diff 2f18020dae5ad9b1c59918cc5d15c474a9bb10ba HEAD -- examples/emerald-remix
 git status --short
 git rev-parse HEAD
```

Frame/render commands were iterated after actual changes: the first frame pass exposed missing title-font numerals; the first preview pass exposed a Python label-variable collision; later visual review changed the counter panel, goal invitation timing, ring cues and title entrance. All final exports are from the final visual/audio edit. Whole-film re-renders were for those new edits, not repeated unchanged checks. The last edit after verification only corrected the edit docstring's description of the new landscape treatment.

The render driver uses `Pool(4)` and exact ffmpeg argv:

```text
ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 60 -i - -i <range.wav> -c:v libx264 -threads 4 -preset fast -crf 16 -tune animation -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart -shortest <output.mp4>
```

The verifier runs, for each current export:

```text
ffprobe -v error -show_streams -show_format -of json <output.mp4>
ffmpeg -v error -xerror -i <output.mp4> -f null -
ffmpeg -hide_banner -nostats -i <rough.mp4> -af ebur128=peak=true -f null -
```

Review server: `python3 -m http.server 8875 --bind 127.0.0.1 --directory "$PROD"`; page `previews/review-round5.html`, browser1920×1116 containing a1920×1080 video at1×. Whole final file requested with `?r5final` to avoid stale browser media.

## Tool / documentation problems and limits

- The extracted Sonic2 title alphabet has A–Z, no numerals. First attempted pickup digit failed with `KeyError: '9'`. Resolved using the existing heavy condensed title face for numerical counters; native title letters remain untouched. No invented ROM digit art.
- The comparison loop initially shadowed helper `label` with a string, causing `TypeError: 'str' object is not callable`. Renamed that loop variable; final rendered/decoded comparison passed.
- The generator's `--preview` CLI also rewrites source assets unless paired with `--check`. Avoided it: the local preparation script imports the pure generation functions and writes only production-directory art. No unnecessary repository generation or engine fix.
- `scripts/render_previews.py` now forwards to the current round5 driver. Its round4 implementation and prior edit/status are preserved under `revisions/round4/`; `out/emerald-remix-round4.mp4` preserves the previous rough. Older planning/capture statuses, beat sheets, `chapters.json`, obsolete preview filenames and doc-regeneration scripts are historical, not current edit authority. Do not run `update_revision_docs.py` or `write_plan.py` over this status. `chapters-round5.json`, instantiated edit and current ranges are authoritative.
- The custom-name native Clover card and the wide take's beyond-right-bound view remain inherited source limitations. Editorial blue name presentation and the held goal crop handle the promo without engine changes or claiming a native card repair.
- First browser visit preceded `type-and-strip.mp4` creation and recorded404; the completed exports subsequently returned200. Snapshot screenshots are tool-scaled; original1920px export frames were separately inspected. Browser playback can drop frames, so its observation is bounded; complete encoded decode is checked separately. No physical hearing or human aesthetic approval is claimed.
- No Maven job, trace sweep, engine test, new capture, repository integration or archive was needed for this production-only edit. No master was made. This is media verification, not a fresh gameplay/parity certification.

## Completed playback review and final state

The final whole file played from start to `ended=true` at **1×**, media time41.683333, with no media error or midstream waiting event. Video element bounds were measured as **1920×1080** in a1920×1116 browser viewport. Browser quality reported **2,501 total / 3 dropped frames**. `requestVideoFrameCallback` recorded2,210 callbacks, from media frame0 through41.666667; callback count is not an independent all-frame vision claim. The complete ffmpeg decode above covers encoded integrity. Visual review combines browser snapshots during playback, full-size export frames and dense transition strips; physical hearing is not claimed.

Changed-section previews were also played from their beginnings through the title, build, spring/rings, jump/goal and end-card sequences. Snapshots during the final build show successive sky/grid → foreground/whole route → gold iris/native play; final spring snapshots show the released spring → high ledge pickup → completed22-ring sweep. The title entrance and static card were inspected again after its motion correction. Earlier preview browser quality samples, while rendering ran, reported26/334 dropped for the build,23/324 for spring/rings,14/392 for jump/goal and16/429 for the end-card; these are browser-review limits, not errors found in the exports.

Two attempts to seek the whole file to8.8s instead restarted near0s, even after awaiting `seeked`. They were **not** counted as successful targeted title review. The correction was to play the short `type-and-strip.mp4?r5final` preview from its beginning; its0.93s/2.23s snapshots show the corrected title on its backing. No browser/engine source repair was attempted.

Separately extracted and inspected final encoded **1920×1080** frames551/620/1310/1410/1565/1700/2040/2240 under `previews/encoded-round5/` using exact argv:

```text
ffmpeg -v error -y -i <rough.mp4> -vf select=eq(n\,N) -frames:v 1 <encoded-round5/NNNNN.png>
```

After the docstring-only correction, Python AST checks over `edit.py` and all current `scripts/*.py` passed again. JSON/source checks verified contiguous eleven-shot output through2501 frames and every declared source interval against the actual PNG count. No encoded media or executable edit behavior changed after the successful final decode.

The task-owned review tab `tab_15_b777ebc1-a1e1-4d5b-beda-3870ab614700` was closed, and its exact HTTP-server command session was stopped with Ctrl-C. All this revision's render/verification commands completed. No worker, capture or Maven process was launched or left running. Final assigned-checkout `git status --short` was empty; HEAD remained **7d7246fbe0913683b88d114b4081d73fc039b80a**. No commits, push, mastering or Media archive occurred. The production files are ready for the next human rough-cut review.
