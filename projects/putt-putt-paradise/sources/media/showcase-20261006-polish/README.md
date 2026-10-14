# Putt Putt Paradise — Sonic 2 Mini Golf showcase

The highlight reel is 80.5 seconds, 1280×720, 30 fps and silent. Gameplay runs
at normal speed; there are cuts between chapters, not sped-up gameplay.
The native 320×224 image is scaled exactly 3× with nearest-neighbour sampling
and framed with a caption. `chapters.csv` and `edit-list.json` identify every
source interval. Sources retain each complete capture, including portions that
do not appear in the edit.

## What was recorded

- Emerald Hill 1, Sonic practice: a moving-shot rewind, then the full act in
  10 counted strokes (the rewound stroke is refunded).
- Emerald Hill 1, local two-player: Sonic and Tails alternate two actual shots.
- Emerald Hill 2, Tails practice: the full act in 25 strokes.

All three captures execute the final mod through the engine's `GameLoop` with
logical Genesis movie input at 60 Hz. Images are captured every two executed
rows. `state.csv` records native centre position, velocity, camera, shot phase,
owner and score. `events.csv` marks commit, rewind, turn and finish boundaries;
`input.script` and `input.bk2` retain the inputs. The recipes are cold-start
routes; the driver never writes player/world positions or hydrates gameplay
from a trace. These captures show local/practice gameplay, not online playback.

The ordinary gameplay capture launcher deliberately disables creator code.
`source/GolfShowcaseCapture.java` therefore uses an explicit SDK-validated
ModContext wrapper for this one mod, passed to `HeadlessGameBoot`. This is a
capture entry point, not a claim that the ordinary capture launcher supports
code mods. Title selection uses the real creator menu, and the normal
level reload restores course palettes. Reflection reads shot diagnostics only.

Runtime art comes from the user's Sonic 2 World REV01 ROM, SHA-1
`8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9`; no ROM is included. Per-capture
`provenance.json` records the jar digest, Java source digest, baseline commit and
working-diff digest at capture time. The capture baseline plus working changes
is deliberate: the final polish was verified before committing it.

## Files and reproduction

The source archive contains lossless FFV1/BGR0 native gameplay and title videos,
input scripts/movies, state/event CSVs, provenance, the driver, the validated
code-only mod jar, and the exact edit/encoding scripts. It excludes ROMs,
Maven logs and regenerable intermediate clips. `SHA256SUMS` covers its contents.

Use the corresponding repository revision, Java 21, Python 3, Maven, FFmpeg
with FFV1/libx264, and DejaVu Sans. Supply your own matching ROM and a working
OpenGL display/context (the recorded run used this host's graphics service).
Build the example with:

```sh
python3 examples/putt-putt-paradise/build.py
```

Compile `source/GolfShowcaseCapture.java` with `javac --release 21` against
`target/classes` and the dependency list emitted as
`target/putt-putt-paradise/engine-classpath.txt`. Launch
`com.openggf.mods.code.GolfShowcaseCapture` with these six arguments:

```text
<absolute-ROM> <validated-jar> <fresh-output-directory> <act-index> <character> <mode>
```

Use `(0, sonic, practice)`, `(0, sonic, local)`, and `(1, tails, practice)`.
The driver writes PNGs plus input/state/event files. `capture_runs.py` records
the exact commands and local paths used here; adjust paths and choose fresh
output directories before repeating. `encode_sources.py` converts retained
native PNG sequences to the full lossless videos. From the archive root,
`python3 assemble.py` reproduces the edit directly from those videos.

The finished MP4 was fully decoded, probed for 2,415 frames and 12 chapters,
and checked for a continuous 1/30-second presentation cadence. Every cut was
visually inspected. The corrected local capture keeps Tails visible through
aiming, crouching and release feedback. Complete native sources provide the
route evidence behind the excerpts.

`build-reference.json` binds the captures to the final source commit and matching
Java-source and validated mod-jar digests. These follow-up captures replace the
previous reel's footage. All preexisting state columns match the preceding
captures exactly, preserving routes, scores and turn boundaries; presentation
pixels intentionally change for the HUD polish and rewind effect. The previous
published reel and source archive remain in their own directory.

The corrected capture uses the engine's production `RewindVhsEffectPass` with
`REWIND_VHS_EFFECT` and `REWIND_VHS_TEAR_BANDS` enabled. Developer live rewind
is disabled; the mod's presentation-only request supplies intensity and speed.
`state.csv` records both alongside gameplay state. `effect-checks.json` identifies
native frames 290–359, checks that the effect clears after restore, and compares
same-frame `rewind-raw.png` / `rewind-vhs.png` evidence. This changes rendering,
not replay speed or restored state. The filter also follows the normal host
configuration during live play.

`verify_sources.py` checks the cold routes, full lossless decoding and effect
pair. `verify_reel.py` checks output cadence and generates the contact sheet;
those scripts require Pillow. `browser-qa.json` records moving 1× playback in
the collaborative browser. `state-comparison.json` records the exact comparison
with the previous version; those earlier sources are retained separately and
are not duplicated in this archive.
