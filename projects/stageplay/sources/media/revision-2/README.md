# Location, Location, Location — Stageplay production

**Superseded preview.** User review rejected the fractional nearest-neighbour zoom,
idle performances and insufficient speaker identification. Revision three replaces
this presentation. The codec/frame/audio checks below remain historical observations,
not approval of its creative quality. Earlier take names and files are preserved.

An original 46-second short: Tails demonstrates a location remote, overcorrects
through another act and another game, disturbs Knuckles, and almost gets home.
This is staged animation using supplied ROM art, not a native gameplay route or
simulation-parity demonstration. The final 29.45-second promo selects seven moving
excerpts at their original speed and retains their music and sound effects.

The production demonstrates movement, pose changes, visible Tails accessories,
camera pan/zoom/shake and in-level, cross-act and cross-game transitions. Its sets
are Emerald Hill 1 and 2, Green Hill 1 and Angel Island 1; scene changes can also
select another level in the same game. Captions carry the original dialogue.

## Preserved sources and external dependencies

`direct_remote.py` authors the final version-one shot-local screenplay. The
engine's maintained `tools/stageplay/stageplay.py` compiles it to a version-two
scene, validates, samples and renders without interactive editor navigation.
`take-2/` contains the final screenplay and compiled scene. The root screenplay
and `take-1/` compiled scene retain the rejected framing draft: some standing
poses floated and Knuckles' caption was too wide. Take 2 adjusts those poses,
wraps the line and gives the island arrival a short falling action. Native physics
and collision are not implied.

Supply Java 25, Python 3, FFmpeg/FFprobe (observed: n9.0.2), your own verified ROMs,
and Linux EGL/Mesa or the engine's documented hidden-context prerequisites on
another platform. `verify_media.py` also needs Pillow. Promo labels use the external
DejaVu Sans font identified in `provenance.json`; no font or ROM assets are bundled.

Videos, decoded images/audio, sampled state and the exact packaged engine remain
external. `external-assets.json` records their sizes and SHA-256 digests. This
repository is a source archive, not a movie download. Relocate the preserved
sources into a fresh writable production root and supply or regenerate external
assets. Do not overwrite historical takes or run assembly in the archive checkout.

## Rebuild

Check out the delivered engine revision recorded in `provenance.json`, follow its
build prerequisites, then use a new writable production directory. `ENGINE`,
`PRODUCTION`, `S1_ROM`, `S2_ROM`, `S3K_ROM` and `FONT` below are paths you supply.
The archived canonical scene can be used directly; compiling the screenplay is
shown to exercise the agent authoring workflow.

```sh
export JAVA_HOME=/path/to/jdk-25
python3 capture.py --engine "$ENGINE" \
  --screenplay "$PRODUCTION/take-2/location-remote.screenplay.json" \
  --out-dir "$PRODUCTION/recapture" --build \
  --s1-rom "$S1_ROM" --s2-rom "$S2_ROM" --s3k-rom "$S3K_ROM"
```

In the new working copy, place the regenerated source at
`take-2/location-remote.mkv` (or edit the EDL source path and verification script to
match). The movie is 400×224 at 60 fps, 2,760 frames, FFV1/FLAC, with 2,208,000 stereo
sample frames at 48 kHz. `state.jsonl` is authored evaluator state, not measured
native gameplay; the final take has exactly one row per film frame.

```sh
python3 assemble_promo.py --root "$PRODUCTION" \
  --out "$PRODUCTION/stageplay-promo.mp4" --font "$FONT"
ffmpeg -v error -i "$PRODUCTION/take-2/location-remote.mkv" \
  -vf scale=1200:672:flags=neighbor -c:v libx264 -preset slow -crf 18 \
  -threads 4 -c:a aac -b:a 192k -movflags +faststart \
  "$PRODUCTION/location-remote.mp4"
python3 "$PRODUCTION/verify_media.py"
```

The promo assembly validates source intervals, performs one final encode, writes
chapters and rejects an existing output. It scales pixels by three and pads to
1280×720, preserves 60 fps and uses only the source audio with short cut-edge fades.
`edl.json` and `chapters.json` map every output chapter to source frames/times.
The full short remains a separate 1200×672 MP4. Existing outputs must be moved aside
in the fresh working copy before rebuilding. Assembly paths/font paths must avoid
FFmpeg filter metacharacters, as checked by the script.

## Observed review and limits

Both final MP4s and the lossless final take passed full FFmpeg decode. Frame counts,
durations, sample accounting, chapters, fast-start layout and continuous decoded
motion were checked. Both MP4s played to completion in a muted collaborative
browser, reporting zero dropped frames. Representative moving states, all seven
shot frames and eight samples around every promo cut were inspected, including
transition cover and reveal. This is bounded visual review, not a claim that every
frame was individually inspected or that physical audio listening was performed.
The editor images were rendered offscreen at 1280×720 and 1024×576; they do not
certify native window focus, HiDPI or platform window-manager behavior.

The first promo command used the removed FFmpeg `-filter_complex_script` option
and failed before producing a movie. The retained script passes its graph through
`-filter_complex` instead; the corrected output passed the checks above. Numerical
motion/audio inspection uses Pillow and Python's standard library, without NumPy.
See `decoded-media-checks.json`, `promo-render.json` and `provenance.json` for exact
historical observations. A new render requires new verification.
