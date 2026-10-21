# One More Take — camera-alignment correction

A 60-second rehearsal turns a moving-platform relay into a ring-spill mishap,
an airborne regrouping, a clean retry and one final run with Sonic, Tails and
Knuckles. The companion demos isolate platform transfers (8 s), flight and glide
(9 s), and ring collection, hurt and recovery (4 s).

These are authored performances in the production gameplay world. Scripts publish
native character inputs; the engine owns acceleration, jumps, flight/glide, solid
contact, rings, hazards, animation, objects and sound effects. The scripts do not
tween platforms, assign pickup counters or force velocities. The source positions
are deliberately staged entries, not uninterrupted play from the act start.
Native state observations are retained beside every movie as `*-final.jsonl`.
They demonstrate the recorded interactions, not whole-game completion or ROM parity.

User feedback on revision five: “something's wrong with vertical camera movement relative the level,” specifically the “Ring-spill fall.” The native state showed grounded/skidding actors while the rendered floor was elsewhere. Revision six aligns the directed foreground and its priority mask with the native sprites. All four movies were recaptured from engine `efa7875f8`; all 4,860 parsed native state records match revision five. The reviewed frame-239 landing now meets the visible floor. Earlier footage remains preserved.

## Source and rebuild

`provenance.json` identifies the exact engine, editor and packaged artifacts.
`scenes/` preserves four screenplay-v3 recipes and their compiled scene-v5 files.
The engine's matching `examples/stageplay-demo` has the same reusable demonstrations.
Build the identified engine revision with Java 25, using its current build/queue
instructions, and supply your existing S3K locked-on ROM. ROM bytes are never
included in the source archive. Lua 5.4 is needed for engine validation, FFmpeg for
capture, Python 3 with Pillow for the promo compositor, and surfaceless EGL for
display-free Linux rendering.

```sh
python3 capture.py --engine /your/OpenGGF \
  --jar /your/OpenGGF/target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar \
  --s3k-rom /your/existing-s3k.gen --out /external/new-take
```

The driver refuses an existing output directory. It compiles each screenplay,
compares the canonical scene, simulates native world state and renders FFV1/FLAC
at 640×448, 60 Hz. It never navigates engine menus or uses the shared desktop.
For authoring, use the engine's `tools/stageplay/stageplay.py level`, `catalog`,
`compile`, `inspect`, `simulate` and `render` commands. Its stageplay-authoring skill
explains discovery, native route evidence and bounded wait/ability semantics.

The development bounds are native height 224, width 320–1920, fixed zoom one,
same-game native Puppets and the engine's native roster/activation window. Destinations
are attempts; there is no general pathfinder. Specify jumps and waypoints. Camera
following uses actual actor positions with dead zones, smoothing and look-ahead.
The directed foreground, sprites and priority mask share one view. Background
registers, deformation and effects retain the native gameplay camera’s phase;
arbitrary-view parallax recomputation is outside this correction. Death Egg’s
intentionally stationary background remains stationary. Poser mode and terrain-only
scenes remain available for manual choreography.

## Promo edit

The promo retains the complete 60-second story without additional cuts, repeats,
retiming or camera zoom. It doubles the lossless source to 1280×896 with integer
nearest-neighbour scaling (four times the native pixels). Cream/gold Fira title
accents enter briefly at the opening and occupy the top safe area for the final
six seconds. Named dialogue remains unobstructed. The close identifies the project,
development status, URL and fan-project/ROM requirement. The edit follows the
restrained narrative treatment of the earlier Stageplay film; it does not turn the
story into a rapidly cut feature inventory.

The captured soundtrack is the sole music/effects source. A constant +6 dB gain
raises its level; no second bed or fabricated voice track is added. Measure the
encoded AAC using the verifier, including oversampled true peak.

```sh
python3 assemble_promo.py --root /external/new-take
python3 verify_media.py --root /external/new-take
```

The compositor uses external `FiraSansCompressed-HeavyItalic.ttf` and
`FiraSans-Medium.ttf`, normally in `/usr/share/fonts/TTF`, configurable through
`--title-font` and `--body-font`. The installed notice is
`/usr/share/licenses/ttf-fira-sans/OFL.txt` (SIL Open Font License 1.1).
Exact font and media hashes are recorded by the assembly and asset manifests.
`chapters.json` describes the five continuous shots; intervals are half-open.

## Evidence and review limits

The short native routes establish placement 179 → 166 → 179 transfers in DEZ2;
S3K Tails flight/hover/release/landing and Knuckles glide/release/landing; and three
once-only ring pickups followed by native hazard hurt, scattered rings and recovery.
Ring counts are the team's shared native total, never additive per-character credit.
The combined film ends with all three independently controlled and group-followed.

`provenance.json` records the exact retained take, review findings and corrections.
`decoded-media-checks.json` records full decode, dimensions, cadence, chapters and
encoded audio measurements. Moving review checks framing, native contact, tails,
abilities, reading time and transitions. These are bounded agent observations;
physical audio listening and user creative acceptance are not claimed.

Production text is archived in OpenGGF-Media. Movies, ROM-derived art/audio,
review images, bulk native state, fonts and packaged builds remain external.
`external-assets.json` records their hashes; catalog entries are not downloads.
Earlier revision-four Puppet/Poser terrain footage remains preserved separately.
