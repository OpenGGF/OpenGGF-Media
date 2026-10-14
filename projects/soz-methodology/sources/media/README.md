# Sandopolis implementation captures

Completed SOZ methodology-v2 media collection, 2026-09-16. All original captures,
controller inputs, state CSVs and PNGs remain in their task subfolders.

## Watch

| Video | Duration | Size | Contents |
| --- | --- | --- | --- |
| [Highlights](SOZ-work-highlights.mp4) | 4:20.700 | 374 MB | 22 moving gameplay excerpts, ordered through Act 1 then Act 2 |
| [Complete compilation](SOZ-work-compilation.mp4) | 5:28:57.783 | 14.48 GB | Initial 311-source campaign archive, including sampled still probes |
| [Cold Act 1 completion](completion-cold-route/native-320-final/capture.mp4) | 7:25.267 | Original capture | Cold SOZ1 through real Egg Golem defeat to playable SOZ2 |
| [Cold Act 2 completion](completion-cold-route/act2-native-320-final/capture.mp4) | 9:00.533 | Original capture | Cold SOZ2 through eight boss hits, capsule/results and playable Lava Reef |

Both videos are silent 1920×1080. The complete compilation preserves source
cadence and all 311 chapters. The curated highlights have 22 chapters at 60 fps;
Act 1 footage was originally captured at 15 fps. Original movies had no audio.

- [Complete chapter index](compilation-chapters.csv)
- [Highlights chapters and exact source time ranges](highlights-chapters.csv)
- [Source inventory, dimensions, duration and SHA-256](capture-index.csv)

## Editorial selection

The highlights were recut after feedback about still images and repeated tests.
They use the two final cold Sonic + Tails runs and the final 800-pixel golem
acceptance capture, following level progression:
Act 1 desert, mechanisms, Egg Golem and pyramid entry; then Act 2 temple,
ghosts, lighting, wires, sand, mechanisms, Eggman and the exit into Lava Reef.
The wide golem excerpt replaces the earlier native-width battle excerpt; it
does not add another test variant or duplicate scene. Every excerpt plays at normal speed. There are no still montages, test variants,
or repeated source intervals. Cuts omit travel and waiting between features.
Use the full cold-route movies for uninterrupted completion evidence.

The complete archive remains unchanged: it retains failed attempts, native
reference probes, corrected scenarios and explicitly labelled sampled stills.
All original PNGs, inputs, movies and state CSVs remain in their task folders.

## Verification and scope

- The original complete compilation decoded without errors; its 311 sections
  match source durations and its source SHA-256 checks passed at delivery.
- The recut highlights were fully decoded, chapter timings checked, and
  representative frames inspected across all 22 scenes.
- Highlights use one consistent final encode for reliable chapter seeking.
- The initial editorial correction changed no engine code. The later acceptance
  follow-up fixes widescreen arena admission and verifies its own route/render path.

The original cold-route implementation was pushed to `develop` at `1e3626aca7f18f3bfee77e9194c9d52724237393`.
[CI passed](https://github.com/OpenGGF/OpenGGF/actions/runs/35043945260).
Integrated ordinary validation ran 21,161 tests with zero failures/errors and
27 skips. The three guard failures exactly match the unchanged baseline.
Both cold capture regressions passed explicitly, including actual Sonic + Tails,
no death, real boss/transition events, visible destinations and released controls.

Cold-route completion is verified for native Sonic + Tails at width 320. The lower
Act 2 subtype-$87 rock puzzle, strict native trace/pixel parity and the broader
character/donor/viewport route product remain separately documented coverage gaps.

Regenerate the curated reel with `python3 curate_highlights.py`; regenerate only
the complete archive with `python3 assemble_highlights.py`. Both require Python
3.11+ and FFmpeg/ffprobe and preserve the originals.


## Non-trace acceptance follow-up

The additional capture and native probes live under `acceptance-followup/`.
[800-pixel golem victory](acceptance-followup/act1-victory-wide800/capture.mp4)
is 88.800 seconds at normal cadence (15 rendered frames/s, one every four gameplay
frames). Its 5,325-row CSV ends in visible, unlocked Act 2 after natural golem
sinking. The full capture test passed with no skips; battle, sinking and destination
frames were inspected. The revised reel remains 22 moving scenes and 4:20.700,
with Act 1 first, and passed a full decoder check. The original 311-source archive
is retained unchanged; it predates this acceptance follow-up.


Acceptance code is integrated and pushed on `develop`: source/test commit
`31686bac5`, verification record `d2b84abb5`. Local focused validation completed
1,139 tests (eight opt-in capture skips), 13 lifecycle guards, two explicit cold
controls and 90 post-integration arena/victory cases without failures or errors.
These are focused checks, not a full-suite claim. The authored 40 final-boss cases
also release playable LRZ controls through the real title/fade. Full acceptance
and the documented remaining routes/native comparisons are still open.
[Acceptance CI smoke suite passed](https://github.com/OpenGGF/OpenGGF/actions/runs/35079558658)
on 2026-09-16 at 09:34 UTC; the trace job was skipped.


## Priority and playtest follow-up

Current moving captures are under `priority-pass/` and `playtest-followup/`.
The highlights now use the corrected 800px pyramid-rumble/golem capture,
400px lower-sand priority scene, 400px checkpoint-to-boss approach, and 320px
final boss/victory capture. The reel remains 22 chapters, Act 1 then Act 2,
260.700 seconds. It was fully decoded after the refresh.

The checkpoint approach invokes the real last-checkpoint debug shortcut from
early SOZ2. After the corrected production reload, ordinary switch-push and jump
input reaches the boss-room lighting/art trigger at frame 689 and the visible
shell at frame 760. The final `checkpoint-shortcut-shell/` capture supplies 99
rings after reload to retain the view through contact; it does not change events,
position or geometry. Earlier shortcut attempts are retained as input-authoring
attempts and are excluded from the highlights. The original complete compilation
and its 311-row inventory are unchanged and predate this follow-up.

The source fix `116d542a9` was integrated as `7bdb0fc41`; `develop` was pushed at
`4ad126bd8` with the verification record. Both candidate and integrated ordinary
runs passed 21,573 tests with 27 skips and no failures/errors. The same three
structural guard failures were confirmed on the unchanged baseline. The task
worktree and local branch were removed after push; original assets and captures
remain intact. The repository SOZ plan owns the detailed verification record.


[CI smoke passed for the priority/playtest delivery](https://github.com/OpenGGF/OpenGGF/actions/runs/35098235031)
at `4ad126bd8`. Trace replay was skipped, consistent with the deferred trace scope.


## Latest pyramid presentation refresh (2026-09-16)

The four Act 1 arena excerpts now use `pyramid-presentation/final/capture.mp4`:
800px Sonic+Tails, 5,373 frames / 89.55 seconds, with controller-only victory and
playable Act 2 entry. `state.csv` records inputs, event phases and both sprite
priority flags. This starts above the native priority switch; the earlier
positioned start skipped it and misleadingly showed Sonic behind the pyramid.
The runtime repeats plain ROM masonry beyond the right edge and caps the wider
view before the foreground wall without shortening player movement bounds.

The reel remains 22 chapters and 260.700 seconds, Act 1 before Act 2, and passed
full decode verification. `highlights-chapters.csv` lists the exact source ranges.
All older captures remain available, including diagnostic attempts under
`pyramid-presentation/`; only `final/` supplies the refreshed highlights.

Source `5162c693b`, integration `8d1ca597d`, pushed develop `b6624468d`.
The integrated focused selection passed 177 tests without failures or skips.
The repository SOZ methodology plan records scope, rejected attempts and limits.

[Push CI smoke passed](https://github.com/OpenGGF/OpenGGF/actions/runs/35113926848) for `b6624468d`; task worktree and local branch were removed.
