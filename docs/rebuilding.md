# Rebuilding an edit

Start with a project's index, then its original plan, edit list and assembly script.
The source files are historical snapshots, preserved byte for byte. They have not
all been ported to a common CLI or rerun against today's engine. A historical
verification result describes that edit at the time it was made.

## Find and relink dependencies

`catalog/roots.json` maps each logical source root to its original location and
the corresponding archived source directory. `catalog/assets.csv` records the
external video, audio, image sets and bulk observation data found under those
roots. `bytes` and `files` are inventory measurements, not content verification.
Wildcards identify image sets; a `frame-sequence` row represents a whole directory.

For example, `sonic3k-chaos-mode/media` was `~/scratch/sonic3k-chaos-demo-20261014`.
The archived `revision-2/edl.json`, its selections and its assembly script preserve
their relative layout under that root. Source MKVs, PCM, artwork and generated
frames remain in the original external root. Place archived sources in a **new
working copy** of that media root, supply its external dependencies, and adjust
machine-specific paths or the script's existing environment overrides. Keep the
preserved archive and earlier deliverables intact.

```sh
python3 tools/catalog.py projects
python3 tools/catalog.py assets sonic3k-chaos-mode --limit 30
python3 tools/catalog.py verify
```

The catalog is not a download service. It does not make footage available on
GitHub. Some sources already have content hashes in their original provenance;
the inventory does not invent hashes for the 100+ GB of external material.

## Recapture when source footage is unavailable

Use the source commit and commands recorded by the particular project. Build a
separate checkout of OpenGGF and its matching example mod, then use that revision's
maintained capture tools and supplied ROMs. Historical scratch drivers are kept
where found; maintained replacements are often identified in the original README.
Some older instructions name Java 21; the current engine requires Java 25. Use the
requirements of the actual engine revision being built.

On Linux, ordinary gameplay capture should use the engine's surfaceless EGL path
with `DISPLAY` and `WAYLAND_DISPLAY` unset. Follow the engine's current capture and
Maven queue guidance. Historical window scripts are source records; do not run
them against a shared desktop. Genuine window/focus diagnostics require an owned
isolated display. Do not copy or redistribute ROMs to reconstruct a shot.

Capture inputs, preference seeds, entry coordinates, audio policy and viewport are
part of the edit's provenance. Positioned demonstrations, debug/autoplay footage,
cuts and slow motion retain their original qualifications. They do not certify
uninterrupted completion or ROM parity.

## Original Resolve editing projects

`projects/release-reels/sources/resolve/*/Project.db` are consistent SQLite backup
snapshots of the seven original Resolve projects. They are **not `.drp` exports**.
Their database integrity was checked, but opening/rendering them in Resolve was
not tested in this import. Do not overwrite an active project library with these
files. Restore a copy using a compatible Resolve project-library workflow and
relink the media. `catalog/resolve-references.json` exposes the text path references
found in the databases, including historical Windows paths which may be unavailable.
Private account settings and the rest of the Resolve user library were not copied.

## Verify a recreated reel

Check edit intervals against actual source durations and review every moving cut.
Confirm dimensions, frame rate, audio policy and chapters with `ffprobe`, then
decode the complete output with `ffmpeg -v error -xerror -i REEL -f null -`.
Keep both the exact edit commands and the source-to-output chapter map. Original
verification JSON is evidence of its historical run, not proof of a new render.
