# Second Strike — enemy expansion short reel

A 14.5-second, 1600×900, 60 fps gameplay reel with two scene changes and one brief end card. Actual animation plays at recorded speed. Captures use the exact delivered engine package from `a8221fb7d5eb48f5bb199602227ec6ab4bbbf945`; published `7277cef4040af3ae95d86a794bce7f75a16cc483` changes only evidence prose.

| Output | Demonstration | Native source interval |
| --- | --- | --- |
| 0.0–4.5 s | Faster Guard with 225px armored flame charge | guard frames 15–284 |
| 4.5–8.0 s | Artillery's wide two-release, 20-seed barrage | plant frames 15–224 |
| 8.0–13.0 s | Double-length Caterkiller, 12 body segments | caterkiller frames 60–359 |
| 13.0–14.5 s | End card | Generated typography |

These are declared positioned demonstrations of native gameplay, with 20 incoming rings so hurt/recollection can occur. They do not demonstrate the five-original-ring economy or uninterrupted campaign completion. The Caterkiller shot explicitly seeds physical act 1 / apparent act 0 as inherited Angel Island fire continuation, then uses ordinary events, terrain, camera, enemies and player input. Sonic remains on the actual ledge throughout. The plant take dies after frame 231; the selected interval ends at frame 224 while alive.

## Audio and picture

One uninterrupted ROM-backed Angel Island music stem under the whole reel; scene SFX are omitted. `ReelMusic.java` advances the existing production audio presentation owner after one ordinary gameplay step and `stopAllSfx()`. The final edit applies fixed gain, short opening/closing fades and a 0.85-full-scale safety limiter. No menu blips, stacked tracks, ambient audio, unrelated music or speaker claim. Original take PCM remains available externally.

The picture uses nearest-neighbour integer 3× scaling. Guard is centred with padding; plant fills 1584×672; Caterkiller is cropped from an 800×224 viewport to the left 528×224 so the extended body and Sonic stay legible. Captions occupy the surrounding canvas rather than covering play. The end card is code-native text, not ROM-derived artwork.

## Rebuild

Supply Java 25, Python 3, ffmpeg/ffprobe, Mesa surfaceless EGL, DejaVu Sans and your own original S3&K ROM. Retain the matching delivered engine fatjar and ROM-free `second-strike-0.1.0.jar`; their exact SHA-256 hashes are in `provenance.json`. The archive does not distribute them or any ROM-derived pixels/audio.

Place the archived sources in a fresh writable production root; relink external `captures/` and `music/` if reusing footage. Set `OPENGGF_ROOT` to the appropriate engine checkout and optionally `SECOND_STRIKE_MEDIA_ROOT` to that root. Exact stage coordinates, inputs and source identity are retained beside each take. Captures fail closed if package hashes change. Use new take directories for a correction; existing `state.csv` is not overwritten.

```sh
python3 capture_shots.py
python3 capture_music.py
python3 assemble.py
```

The launchers use official admission and the intended engine worktree lease, including source-file compilation and encoding. Display variables are unset; graphics are surfaceless EGL; OpenAL uses the null device. No shared desktop focus or keyboard input. Captures are outside the engine repository and do not modify its source/configuration.

`assemble.py` writes `edit-list.csv`, `edit-list.json`, `chapters.json`, `chapters.ffmeta`, `probe.json`, the reel and codec verification. It normalizes source frames to lossless intermediate segments, then performs one final H.264/AAC encode with fast-start metadata and chapters. Complete decode is required. `review/review.json` and `delivery-review.json` record bounded visual/motion/audio checks; these are media checks, not engine parity or release-suite results.

The earlier `31b9503d3` captures are not used. Their Caterkiller setup let the enemy leave the vertical viewport after Sonic fell, so that take was rejected for presentation. The replacement starts Sonic on the upper ledge; all 12 body objects are observed and the complete chain is visibly animated.
