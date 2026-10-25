# Typing / Stageplay route planning demo — 2026-10-25

Final: `route-demo-current.mp4`, 41.683333 seconds, 1280×720, 60 fps, silent.
The original movies, PNGs and measured telemetry remain external in the catalogued
`typing-of-the-hedgehog/route-demo-20261025` root. This source directory is not a
video download. `route-demo.mp4` / `assemble-v1.py` are rejected preliminary output:
their end card names the earlier delivered commit instead of the actual build.

The demo shows two real Stageplay planner results, their fresh native-world
replays, then actual Typing selected-section gameplay. The route overview and
coordinates come from planner/simulation output; this is an explanatory overlay,
not a recording of the editor UI or search nodes being explored in real time.

| Output seconds | Chapter |
| --- | --- |
| 0–3 | Destination and verified route |
| 3–8.5 | Green Hill: Run + Hard Stop, through the native loop |
| 8.5–13.583333 | Emerald Hill: Walk + Gentle Stop, uphill |
| 13.583333–39.683333 | Typing: Hill Top 2 run → fight → run |
| 39.683333–41.683333 | Shared steering and separate rehearsal systems |

See [PROVENANCE.md](PROVENANCE.md) for source revisions, requests, observed
milestones, setup, verification and limits. [edit-list.json](edit-list.json)
contains exact source/output frame intervals; [chapters.ffmeta](chapters.ffmeta)
contains the corresponding chapter map. Every moving source interval plays at 1×.

## Rebuild

Use a separate OpenGGF checkout at `d3fa3d519f6acb7285d538b5f972807036f1019e`,
Java 25, Python 3 with Pillow, FFmpeg/FFprobe and DejaVu Sans. Supply the existing
original Sonic 1 World REV01 and Sonic 2 World REV01 ROMs. Never copy them into
this archive. Work in a **new empty production directory**; the scene tools and
assembler refuse to overwrite existing films/scenes.

```bash
ENGINE_ROOT=/path/to/OpenGGF
ROM_ROOT=/path/to/original-roms
FILM_ROOT=/path/to/new-empty-production
SOURCE_ROOT=/path/to/this-archived-source-directory
cd "$ENGINE_ROOT"
python3 tools/stageplay/stageplay.py --build help
python3 examples/typing-of-the-hedgehog/build.py \
  --engine target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar \
  --sdk target/OpenGGF-0.7.prerelease-openggf-mod-sdk.jar
python3 "$SOURCE_ROOT/capture_stageplay.py" --engine "$ENGINE_ROOT" --rom-dir "$ROM_ROOT" --out "$FILM_ROOT"
python3 "$SOURCE_ROOT/capture_typing.py" --engine "$ENGINE_ROOT" --rom "$ROM_ROOT/s2.gen" --out "$FILM_ROOT"
python3 "$SOURCE_ROOT/assemble.py" --root "$FILM_ROOT" --revision d3fa3d519
ffprobe -v error -show_streams -show_format -show_chapters "$FILM_ROOT/route-demo-current.mp4"
ffmpeg -v error -xerror -i "$FILM_ROOT/route-demo-current.mp4" -f null -
```

The two authored screenplays, source scenes, routed scenes and planner JSON are
preserved for inspection. Bulk `*-native.jsonl`, actual Typing `state.csv`, full
PNG frames and movies are external, not substitutes for authored timelines.
The capture recipes use isolated preferences and no desktop input or audio.
