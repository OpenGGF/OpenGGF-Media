# Location, Location, Location — dialogue revision

This 51-second, seven-shot Stageplay screenplay revises the superseded preview in
`../revision-2`. Tails' location button sends Sonic through increasingly unsuitable
locations, interrupts Knuckles, and finally starts a chase. It is an authored
performance using detached ROM scenery, not a native gameplay route.

The revision removes animated fractional zoom. All shots hold zoom one; pans and
cuts change composition. Actors enter, land, turn, back away and leave. Dialogue
uses explicit speakers, pointers, original PNG panel skins and separate typing
profiles for Sonic, Tails and Knuckles. The generated panel art contains no ROM
bytes; the character and world pixels are supplied by the engine's ROM pipeline.

## Sources and rebuilding

- `direct_remote.py` creates a new take directory containing the shot-local
  screenplay and three original nine-slice PNGs under `decor/`.
- `capture.py` copies the screenplay and only its declared creator dependencies
  into another new take directory, then compiles, exports every-frame authored
  timeline JSONL and renders a lossless FFV1/FLAC MKV through the Stageplay tool.
- `edl.json` retains the complete short, with seven narrative chapters and their
  demonstrated features recorded as metadata. No chapter labels cover the picture.
- `assemble_promo.py` presents the source at integer 4×: 1600×896, with only two
  pixels above and below for a 1600×900 canvas. It makes one H.264/AAC encode,
  preserves the continuous authored score/effects without per-chapter fades,
  and writes `chapters.json` plus a `.assembly.json` provenance sidecar.
  The final promo applies a constant **+10 dB amplitude gain** before AAC encoding;
  this is not a LUFS normalization target. Decoded sample peak must remain below
  0.95 with no clipped samples. The earlier, quieter edit and its exact assembly
  sources/checks remain under `edit-1-unmastered/`; the lossless source and full-short
  MP4 are unchanged.
- `verify_media.py` checks cadence, full decoding, frame/audio counts and moving
  chapter samples. These checks supplement playback-speed visual review.

Use Java 25 for capture, FFmpeg/FFprobe, Python 3 and Pillow for assembly/review.
The sparse title treatment uses the installed Fira Sans Compressed Heavy Italic
and Fira Sans Medium faces, with no fallback or font download. Their local defaults
are `/usr/share/fonts/TTF/FiraSansCompressed-HeavyItalic.ttf` and
`/usr/share/fonts/TTF/FiraSans-Medium.ttf`; relocate them with `--font` and
`--kicker-font`. The installed package's notice is
`/usr/share/licenses/ttf-fira-sans/OFL.txt` (SIL Open Font License 1.1; copyright
2012–2018 Mozilla Foundation, Telefonica, Carrois Corporate and bBox Type).
Exact font SHA-256 identities used for the prepared treatment:

- Heavy Italic: `d90978e735829bcb5218e221f4371c54ba3192b166c872a1f1e213fc74916fb1`
- Medium: `7e7acee3fda79ae2cc3ec899f14f7a5b9e988b27a88f31a81a8ad4cb870b8987`

The archive contains source text, not installed tools,
packaged builds, PNGs, music, footage, ROMs or bulk timeline data. External assets
and exact hashes belong in the accompanying catalogue; those entries do not upload
them or make them downloadable.

Run in a writable relocated copy, using new output names. `direct_remote.py` can
regenerate the original PNG decorations from committed source:

```sh
python3 direct_remote.py /your/production/recipe
python3 capture.py --engine /your/OpenGGF --build \
  --screenplay /your/production/recipe/location-remote.screenplay.json \
  --out-dir /your/production/new-take \
  --s1-rom /your/existing-s1.gen --s2-rom /your/existing-s2.gen \
  --s3k-rom /your/existing-s3k.gen
```

The screenplay has format version 1; the canonical film has Stageplay schema 3.
Retain its sibling PNGs when moving it. Both Stageplay editors can open the film;
the compiled scene and decorations can also be packaged under a mod's asset root.
The tool requires compiling beside the screenplay when it references assets.

For the full short, encode the lossless source at integer 4× scale:

```sh
ffmpeg -v error -n -i take-1/location-remote.mkv \
  -vf scale=1600:896:flags=neighbor -c:v libx264 -preset slow -crf 18 \
  -threads 4 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
  location-remote.mp4
python3 assemble_promo.py --root . --out stageplay-promo.mp4
python3 verify_media.py
```

The assembly retains all 3060 frames at 60Hz. Its original lower-band type says
“ONE BUTTON.” at frames `[8,88)`, leaving before the first speaking turn, and
“MAKE A SCENE.” at `[2916,3060)`, after the last line. Cream/gold heavy italic
lettering enters upward with an outline, shadow and small directional accent.
The top dialogue area and source closing caption remain unobstructed; no grid,
extra cut, zoom, constant label or replacement music bed is added. The brief close
does not carry a crowded route list or URL; production/tool details live here.
The two pixels at each outer edge are the only permanent padding.

Synthetic typography previews can be regenerated without footage or ROMs:

```sh
python3 assemble_promo.py --preview-dir /your/production/new-typography-preview
```

The 90-frame opening and 150-frame closing previews are explicitly marked
synthetic. They check composition and overlay plumbing only, not the eventual
character performance. Real assembly requires the completed 400×224 FFV1/FLAC
source; it checks source frames, cadence, streams, encoded frames/chapters and a
full decode before publishing. The sidecar records source/script/EDL/font hashes,
Pillow/FFmpeg versions and the exact command. Moving-footage review remains a
separate requirement. For another assembly use a fresh output directory: the
movie, chapter map and sidecar all refuse replacement.

If a new take is used, change `edl.json` to its retained source path before assembly.
Its intervals are seconds aligned to exact 60Hz source frames. Do not replace a
source with a later render while retaining old interval assumptions. The timeline
JSONL records authored evaluator state, not measured native physics or collision.

## Review and provenance

The source and final outputs contain 3,060 frames at 60 Hz and 51 seconds. All source
and final files decoded completely. The lossless source contains 2,448,000 stereo
sample frames. Browser playback of the full short and initial visual promo reached
the end at rate one with 3,060 presented frames and zero reported dropped frames.
The final audio-mastered promo has an identical compressed video stream; its fresh
decode and audio metrics are in `decoded-media-checks.json`.

Continuous half-second source sequences and all six transition windows were inspected
for character feet, accessories, turns, reactions, speaker identity and text. The
opening/closing editorial type was inspected through its entrance and exit frames.
These are bounded production checks, not user creative acceptance or physical audio
listening. `provenance.json` records the exact source checkpoint, retained artifact,
ROM identities, commands and limits. Earlier rejected media remains labelled as such.
The quieter first edit is retained under `edit-1-unmastered/`, with its exact source
script, edit list, assembly provenance and checks; its visuals are unchanged.

No native objects, collision, evolving zone events or native cross-game loads run
inside these detached sets. Native window focus/HiDPI behavior is separate from
the Linux surfaceless EGL capture and editor-picture checks. Typing is silent;
the soundtrack uses the authored ROM music/SFX cues, with no generated voice.
