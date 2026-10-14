# Sonic3K Chaos Mode — card gallery revision 3

This revision replaces the rapid montage with one stationary page. A large,
labelled gameplay card plays at native presentation speed; completed cards
remain frozen around it. There are 48 distinct effects across 12 actual S3K
zones. Each card has 4–6 seconds, with a restrained 18-frame dissolve. The verified
edit has 14,460 frames / 241 seconds at 1920×1080 / 60 Hz.

The earlier first reel and rapid revision 2 remain intact. This folder holds the
new reproducible edit and separate source captures. Final actual qualification
is recorded in `out/media-review/summary.json` and `SHOT_REVIEW.md`; this README
alone is not evidence of a successful render.

## Sources and scope

- Engine/capture source: `1a038f53cbdfc59184a32042a4f44f62d3664ee3`.
- Matching unchanged example mod is SDK-validated with 0 findings, treating warnings as errors;
  its JAR hash and source snapshot are retained in `out/mod-package.json` and
  `mod-source/`. It contains no ROM asset bytes.
- Supplied S3&K locked-on ROM SHA1: `CFBF98C36C776677290A872547AC47C53D2761D6`.
  ROM bytes are neither archived nor distributed.
- Thirty-seven new 400×224 / 60 Hz presentation captures cover 11 non-AIZ zones.
  Thirty-five are selected, with 13 earlier actual demonstrations. The rejected
  MHZ bunny and SOZ2 pulley/sidegame takes remain available and are identified
  in the review.
- Native load identities, exact inputs/settings, selected singleton pools and
  seed 22 are retained beside each source. All motion is real production gameplay;
  no session or trace-state hydration was used.
- This is an editorial collection of separately captured effects, not an
  uninterrupted completion, whole-zone certification or native parity proof.
  Positioned MGZ / deep FBZ scenes and the SSZ checkpoint entry are declared.
  Leaky Pockets starts with 32 carried rings, not rings earned in that take.

## Sound

The coherent background is one continuous 270-second ROM-native HCZ2 SMPS render;
there is no arbitrary repeated-file splice. During the final ghost card the
bed is smoothly ducked and the recording's genuine mixed PCM is retained, with
gain/fades only. The native ghost appearance sound 0x92 already existed in the
engine. The old montage muted it; no engine sound change was necessary.

Ghost charge has no additional native cue. The new DEZ1 source has no observed
death, so no death or charge sound is invented. Standalone ROM 0x92/0x8A renders are
review references, not automatic dubbed cues. The remaining cards use the same
music bed and no noisy card-slam stings. `audio.json` and the actual mix/loudness
summary describe the final levels.

## Rebuild

Requirements: matching Java 25 OpenGGF checkout, supplied ROM, FFmpeg/ffprobe,
Python 3 and Pillow. Build classes/dependencies and the matching example mod in
an isolated checkout. Preserve the relative media tree for reused earlier
masters/assets. The original ROM-glyph/plate font dependencies remain under
`../assets`, and `../card_renderer.py` is preserved in the public source archive.
Linux captures use surfaceless EGL with `DISPLAY` and `WAYLAND_DISPLAY` unset.

```sh
OPENGGF_WORKTREE=/your/isolated/checkout python3 ../revision-2/build_package.py
python3 capture.py --admission-worktree /your/isolated/checkout --rom /your/locked-on.gen
python3 render_audio.py --admission-worktree /your/isolated/checkout --rom /your/locked-on.gen
python3 review_sources.py --admission-worktree /your/isolated/checkout --compact
python3 assemble.py preview --admission-worktree /your/isolated/checkout
python3 assemble.py render --admission-worktree /your/isolated/checkout
python3 verify.py --admission-worktree /your/isolated/checkout
```

Set `OPENGGF_QUEUE_ROOT` to the host repository carrying the current testing
scheduler. All Java/compiler/capture/decoder/encoder work acquires shared
scheduler OS leases and propagates them to child processes. No desktop input,
manual queue-lock cleanup, admission bypass or foreign process manipulation is
part of this production.

`cards.json` is the sole source-to-output edit list. Its labels/zone names are
checked against capture provenance, every interval is checked against actual
CSV/EOF/death state, and `thumb_frame` is a representative source frame inside
that same interval. The compositor produces chapters and a frame-level edit map.
Audio-only changes can reuse the picture only when plan/source/renderer/video
hashes still match. Raw redundant new PNG/WAV copies are consumed only after
their complete decoded pixels/PCM match the retained lossless MKV.

## Preservation

Production source, plans, input recipes, settings, chapters, provenance and
bounded verification conclusions are published under the existing Chaos
project in OpenGGF-Media. Videos, native audio/art, packaged JARs, bulk CSVs and
review image sets remain external and are catalogued by location; a catalogue
entry does not upload or make those media downloadable. GPL-3.0 engine/example
terms and original asset notices remain applicable. This independent fan
project is not affiliated with Sega.

## Final verification

The actual final file has 14,460 frames / 241 seconds (4:01), at 1920×1080 / 60 Hz, with 50 ordered chapters. Full video/audio decode, every-frame cadence, selected-source EOF/death checks and fast-start pass. All 48 active-region sample groups change; actual moving/cut strips are retained for visual review. AAC measured −14.23 LUFS and −2.48 dBTP.

Final MP4 SHA256: `5844f2ca440bda71b3a1772915720cfeb5bb144ac7fbe3d31a9986ee7c0be1a8`, 219,027,107 bytes. All 37 new 1,200-presentation masters (44,400 frames) matched every captured RGB frame and native PCM sample before redundant raw media compaction. SDK package unchanged; engine source was not edited.

The first final-review invocation failed while FFmpeg parsed a flat 300-term sample-selection expression, before decoding. The helper now uses balanced parentheses; the subsequent complete scan passed without changing or re-encoding the movie. This was a media-review helper correction, not a footage defect. No listening-review or continuous-route/parity claim is made.
