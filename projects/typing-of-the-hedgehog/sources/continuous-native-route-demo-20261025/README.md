# Continuous Typing route demo — Marble 3

Replacement for the earlier 27-pixel selected-section demo. Source engine checkpoint:
`96aaffb697aefed688b3281389444e3842dd1e76`. The accepted source capture and 17-second continuous excerpt were reviewed at native speed; final encoding/publication are recorded in provenance.

This production demonstrates offline-authored controller inputs replayed through
OpenGGF's native world. The shared `NativeRouteSearch` kernel also serves Stageplay;
Typing does not invoke Stageplay's scene planner during gameplay.

Marble's programme uses one selected entry and five continuous native journeys.
Its compiler independently replayed all six arena boundaries at clock phases
0, 1, 63, 127 and 255. The packaged Course completed four fights and its typed boss,
including pause, retry and checkpoint continuation. That bounded verification is
not certification of the remaining stages or full ROM parity.

The source kit defaults to planning only. `capture.py --execute` runs the checkout's
queued GameplayCaptureTool, with Java 25, display-free EGL and no audio device.
The intended capture is Sonic 1, zone `mz`, act `3`, 400×224, every frame at 60 Hz,
4,800 outer rows. Attract typing and No-Fail are enabled; voice is off. There are
no positioned CLI seeds: the packaged course applies its declared initial entry.
The build record records the exact matching engine/SDK/mod artifacts and sources.
Maven diagnostics remain disposable under the engine checkout's `target/`.

## Rebuild after relocating

Set `CHECKOUT` to that exact engine source checkout, `ROM_ROOT` to the directory
containing the user's original S1/S2/S3&K ROMs, and `SOURCE_ROOT` to these scripts.
Use Java 25 (`JAVA_HOME`), Lua 5.4 (`LUA_BIN`), Python 3.10+, Mesa surfaceless EGL,
FFmpeg/FFprobe 5.1+ and Pillow 9.1+. No display connection or speaker device is used.

```sh
cd "$CHECKOUT"
python3 tools/testing/maven_queue.py -Dmse=off -DskipTests package
python3 examples/typing-of-the-hedgehog/build.py \
  --engine "$CHECKOUT/target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar" \
  --sdk "$CHECKOUT/target/OpenGGF-0.7.prerelease-openggf-mod-sdk.jar"
python3 "$SOURCE_ROOT/capture.py" --checkout "$CHECKOUT" \
  --mod-jar "$CHECKOUT/examples/typing-of-the-hedgehog/target/typing-of-the-hedgehog-mod.jar" \
  --engine-jar "$CHECKOUT/target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar" \
  --sdk-jar "$CHECKOUT/target/OpenGGF-0.7.prerelease-openggf-mod-sdk.jar" \
  --record-build "$SOURCE_ROOT/build.json"
python3 "$SOURCE_ROOT/capture.py" --checkout "$CHECKOUT" --rom-root "$ROM_ROOT" \
  --mod-jar "$CHECKOUT/examples/typing-of-the-hedgehog/target/typing-of-the-hedgehog-mod.jar" \
  --build-record "$SOURCE_ROOT/build.json" --game s1 --zone 1 --act 3 --frames 4800 \
  --out-dir "$SOURCE_ROOT/capture-new" --execute
```

Use a new output path for each take. Read the state CSV, inspect real fight and
travel boundaries and review the continuous interval before filling an edit list.
Assembly keeps one uninterrupted interval at native speed, silent, with integer
nearest-neighbour scaling. Disclosure remains outside the complete game picture.
The resolved edit/provenance records are authoritative for actual selected frames
and completed review. A source path or successful encode alone is not review.

Original generic kit and historical rejected footage are retained separately.
Only source scripts, edits and provenance are committed to OpenGGF-Media; recordings,
frames, bulk state and packaged builds remain external catalogue entries.

The exact capture driver is preserved as `capture-used.py`. The maintained `capture.py` additionally fixes S1 named-zone resolution (ROM order differs from logical tool order); the accepted take used explicit numeric zone1 and was unaffected by that later correction. The rejected take selected zone2 and returned to title; none of its frames enter this edit.
