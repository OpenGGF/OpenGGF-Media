# Location, Location, Location — Puppet revision

A 51-second, seven-shot Stageplay comedy: Tails' location remote interrupts Sonic's
shortcut and Knuckles' afternoon, then starts a chase. This revision replaces the
manual movement in revision three, whose jump the user rejected. Revisions two and
three remain historical sources, not accepted motion references.

All three roles use **Puppet** mode: destination and urgency commands, native jump
button holds, and default floor snapping near each shot's spawn. Native player
acceleration, gravity, collision, animation and landing determine their motion.
**Poser** remains available in the engine and both editors for manual position,
animation and mapping frames; this film uses Puppet for its movement.

The scenery is detached ROM terrain. World objects, moving platforms, water events,
zone scripts, automatic obstacle navigation and native cross-game loads do not run.
This is an authored performance using native player physics, not a gameplay route or
ROM-parity certification. Film zoom holds at one; pans, shake, cuts and transitions
change the framing. Fourteen named dialogue lines use reusable typers, speaker
pointers and original PNG panel skins. Native puppet SFX are silent during simulation;
the screenplay deliberately schedules its soundtrack through audio cues.

## Rebuild

Requirements: current OpenGGF with Stageplay v4, Java 25, your existing S1/S2/S3&K
ROMs, Python 3, FFmpeg/FFprobe, and Pillow for the promo. The original panel generator
contains no ROM bytes. Capture requires surfaceless EGL on Linux; it never opens the
interactive engine or plays audio through a live device.

```sh
python3 direct_remote.py /your/production/recipe
python3 capture.py --engine /your/OpenGGF --build \
  --screenplay /your/production/recipe/location-remote.screenplay.json \
  --out-dir /your/production/new-take \
  --s1-rom /your/existing-s1.gen --s2-rom /your/existing-s2.gen \
  --s3k-rom /your/existing-s3k.gen
```

The capture driver compiles screenplay version 2 to Stageplay version 4, exports
`authored.jsonl`, runs the graphics-free native simulator into `state.jsonl`, then
renders lossless FFV1/FLAC. Authored samples contain unresolved puppet placements;
simulated samples contain actual native positions, velocities and arrival/blocked
status. Neither is a full-world gameplay trace. Inspect simulated outcomes before
using the take, and keep its relative `decor/` assets beside the scene.

The retained final take is identified in `edl.json` and `provenance.json`. To make a
new edit, update the edit list to the new retained source; keep its exact 60 Hz frame
intervals. The continuous promo preserves all 3,060 source frames. It adds sparse
cream/gold Fira titles in the bottom safe band before the first line and after the
last, plus a constant audio gain. It adds no camera zoom or replacement music bed.

```sh
ffmpeg -v error -n -i take-3/location-remote.mkv \
  -vf scale=1200:672:flags=neighbor -c:v libx264 -preset slow -crf 18 \
  -threads 4 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
  location-remote.mp4
python3 assemble_promo.py --root . --out stageplay-promo.mp4
python3 verify_media.py
```

The compositor uses Fira Sans Compressed Heavy Italic and Fira Sans Medium from
`/usr/share/fonts/TTF/`, configurable with `--font` and `--kicker-font`. Their installed
notice is `/usr/share/licenses/ttf-fira-sans/OFL.txt` (SIL Open Font License 1.1).
Exact font, source, script and edit-list hashes belong in the assembly sidecar.
No font download or fallback is performed. Use fresh output names: the compiler,
renderer and compositor refuse to replace existing deliverables.

## Review and provenance

`provenance.json` records source revision, artifact identity, native simulation
observations, visual review and remaining limits. `decoded-media-checks.json` records
full decoding and frame/audio accounting. These checks supplement motion review;
codec success does not establish creative acceptance or physical audio listening.
The earlier failed command-line trial is retained separately from the final take.

Production source text is archived in OpenGGF-Media. Movies, ROM-derived imagery and
audio, original panel PNGs, review images, bulk timelines, fonts and the packaged
engine remain external and are catalogued with hashes. Catalog entries do not upload
those assets or make them downloadable. No voice synthesis is part of this production.
