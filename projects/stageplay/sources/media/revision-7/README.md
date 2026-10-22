# Your first scene — OpenGGF Stageplay

A 124-second conceptual tutorial/promo for first-time creators, followed by the
complete 26-second **Wait for me** short at 01:30. A standalone short is included.
This is a new small story: Sonic races to the other lift, leaves Tails behind,
hears the objection, returns, and counts them into a crossing together. The last
line, “My slowest personal best,” pays off the change from racing to cooperation.

The user liked the working features in One More Take but found the story confusing
and wanted more than characters jumping around. This revision teaches a few
choices through one relationship rather than assembling unrelated ability checks.
The user chose first-time creators as the audience. Technical verification and
bounded agent review do not imply their creative acceptance.

## Watch and try

- `stageplay-first-scene-tutorial.mp4`: 2:04, 1600×1120, 60 fps, stereo.
- `wait-for-me.mp4`: the uninterrupted 26-second short at the same resolution.
- `wait-for-me.screenplay.json`: editable shot-local source.
- `wait-for-me.stageplay`: compiled document for both Stageplay editors.
- `chapters.json`: exact output/source intervals and source kind.

In OpenGGF's in-engine level editor, press F4, choose Open scene and select the
portable file. It also opens in OpenGGF Editor's Stageplay workspace. Supply your
S3&K ROM. Start by changing a line or Sonic's return timing, preview the result,
and watch the whole scene before exporting. The engine's
`examples/stageplay-demo/README.md` walks through the settings and native outcomes.
Scripted changes should edit the screenplay; editor saves update the portable
scene and do not round-trip back to the screenplay.

The seven lessons are story purpose, set/cast, movement, waits, group camera,
dialogue, and preview/share. The cards and simplified track diagram are editorial
explanations using real values, not a simulated editor interface. The destination
outline tracks the measured native placement in the directed camera. The track
playhead shows source-scene time; excerpts restart deliberately for each lesson.
The clean instructional view omits dialogue but matches every native actor, world
and camera sample in the finished story.

## Rebuild

Requires Python 3 with Pillow, FFmpeg/FFprobe, Java 25, the named Fira fonts below,
a matching OpenGGF engine checkout/package, and your existing S3&K locked-on ROM.
The captured runtime is `efa7875f8c60885dad0458a2cfbe77c0cd49a4de`, integrated into
engine develop at `38c2736ccf1a0372cf3df3edbd7ba1d6393e5340`. This production changes
scene data and guidance, not the Java runtime. The exact external jar remains in
`../revision-6/engine/OpenGGF-stageplay-live-efa7875f.jar`; hash in provenance.
Linux commands below use the CLI's surfaceless EGL/no-device audio owner. Other
platforms need their supported headless GL prerequisites. Keep desktop display
variables absent; the renderer must not fall back to the user's desktop.

Copy the production Python programs to a fresh external directory, and set paths
to your existing checkout, packaged engine and ROM:

```bash
export JAVA_HOME=/path/to/jdk-25
export STAGEPLAY_ENGINE=/path/to/OpenGGF
export STAGEPLAY_JAR=/path/to/matching-engine.jar
export STAGEPLAY_ROM=/path/to/your-existing-s3k.gen
python3 direct_scene.py --out wait-for-me.screenplay.json --variants
python3 capture.py --engine "$STAGEPLAY_ENGINE" --jar "$STAGEPLAY_JAR" --rom "$STAGEPLAY_ROM" --script wait-for-me.screenplay.json
python3 capture.py --engine "$STAGEPLAY_ENGINE" --jar "$STAGEPLAY_JAR" --rom "$STAGEPLAY_ROM" --script directing-view.screenplay.json
python3 capture.py --engine "$STAGEPLAY_ENGINE" --jar "$STAGEPLAY_JAR" --rom "$STAGEPLAY_ROM" --script music-bed.screenplay.json
python3 verify_scene.py
python3 assemble_tutorial.py --title-font /path/to/FiraSansCompressed-HeavyItalic.ttf --body-font /path/to/FiraSans-Medium.ttf
ffmpeg -v error -nostdin -n -i wait-for-me.mkv -vf scale=1600:1120:flags=neighbor -c:v libx264 -preset medium -crf 18 -threads 4 -pix_fmt yuv420p -c:a aac -b:a 192k -af volume=6dB -movflags +faststart wait-for-me.mp4
python3 verify_media.py
```

The generator/compiler/capture refuse to overwrite takes. Pillow cards are
regenerable editorial intermediates. Assembly makes temporary lossless normalized
segments and performs one final H.264 encode with chapters; those segments are
removed on exit. Video preserves each excerpt's native speed and every 60 Hz
frame. Full views enlarge native pixels five times, instructional views three
times; there is no fractional animated zoom or aspect-ratio distortion.

One uninterrupted ROM-rendered DEZ2 track (ID 23) owns the first 90 seconds. It
fades into the short's original captured music and native effects, then a deliberate
bed reprise supports the end card. There is no voiceover or external music. The
instructional bed is +3 dB; the story soundtrack is +6 dB. `verify_media.py` meters
the encoded result, not only the source PCM.

Fira Sans Compressed Heavy Italic and Fira Sans Medium are supplied externally
under SIL OFL 1.1; the original notice is `/usr/share/licenses/ttf-fira-sans/OFL.txt`
on the production host. Their hashes are in `assembly.json`. No ROM, decoded art,
recording, font or packaged engine is uploaded by the source archive.

## Review and limits

`scene-checks.json` records native contact changes, absence of hurt/death/timeouts,
framing checks and generator/clean-view equivalence. `decoded-media-checks.json`
records full decodes, cadence, dimensions, channels, chapters and encoded audio
measurements. `provenance.json` records the exact runtime and bounded moving review.
These are production evidence, not engine-suite or native-ROM-parity results.

All movement is native input under an authored starting position. The two actual
DEZ2 platforms are placements 179 and 166. Initial floor snapping is deliberately
disabled for the short drop onto the moving start platform. The explicit route is
not a pathfinder; `WAIT` has a finite timeout and success is checked. The group stays
inside the native activation window. LIVE background phase remains native; the
film does not claim arbitrary-camera background deformation or cross-game loads.

`wait-for-me-take1.*` preserves initial blocking. `take-2-framing/` preserves the
first complete tutorial cut: Sonic clipped the top edge at his return-jump apex.
The final version raises group framing by 15 pixels and ends his return line before
takeoff. Earlier revision-six captures remain technically useful, but the user's
story criticism supersedes their creative direction. No physical audio listening
or user creative approval is claimed.
