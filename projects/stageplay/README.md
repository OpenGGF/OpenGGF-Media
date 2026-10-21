# OpenGGF Stageplay

## Location, Location, Location — dialogue revision, 2026-10-21

Revision three is a 51-second original Stageplay short: Tails' location remote
interrupts Sonic's shortcut and Knuckles' quiet afternoon. Seven continuous shots
use entrances, landings, turns and a closing chase, with fourteen named dialogue
lines, three reusable typing rhythms and original decorated speaker panels.
Camera zoom stays at 1x; pans, shake and scene transitions provide movement.

- [Production notes and rebuild](sources/media/revision-3/README.md)
- [Screenplay](sources/media/revision-3/take-1/location-remote.screenplay.json)
  and [compiled scene](sources/media/revision-3/take-1/location-remote.stageplay)
- [Story and original panel generator](sources/media/revision-3/direct_remote.py)
  and [offline capture driver](sources/media/revision-3/capture.py)
- [Promo compositor](sources/media/revision-3/assemble_promo.py),
  [edit list](sources/media/revision-3/edl.json) and
  [chapter map](sources/media/revision-3/chapters.json)
- [Source provenance](sources/media/revision-3/provenance.json),
  [decoded media checks](sources/media/revision-3/decoded-media-checks.json) and
  [external asset hashes](sources/media/revision-3/external-assets.json)

The 1200×672 short and 1600×900 promo use integer enlargement of 400×224 source
frames. The promo keeps the complete story and adds sparse opening/closing titles
and a constant +10 dB audio gain. All 3,060 frames and stereo audio decoded;
browser playback reported zero dropped frames. Half-second motion samples and
every transition were inspected. The final audio master preserves the reviewed
video stream exactly and has no clipped decoded samples. This is bounded agent
review, not user creative approval or physical audio listening. It demonstrates
authored scene presentation, not native gameplay completion or dynamic world events.
The quieter first audio edit is retained under `edit-1-unmastered`.

External outputs are `revision-3/stageplay-promo.mp4` and
`revision-3/location-remote.mp4` under the `stageplay/media` root below.
`stageplay/fira-fonts` identifies the two external Fira editorial fonts.

## Superseded directing preview

Revision two (superseded preview): a 46-second original staged short follows Tails and Sonic through a malfunctioning
location remote, with an interrupted Knuckles cameo. The 29.45-second, seven-chapter
promo uses moving excerpts from its second take at 60 fps, with the source ROM music
and sound effects. It demonstrates Tails accessories, camera pan/zoom/shake and
in-level, cross-act and cross-game transitions.

User review rejected fractional nearest-neighbour zoom, idle performances and
unclear speakers. The retained verification describes decoding and frame/audio
accounting, not creative approval. Revision three above addresses that feedback.

- [Production notes and rebuild](sources/media/revision-2/README.md)
- [Superseded shot-local screenplay](sources/media/revision-2/take-2/location-remote.screenplay.json)
  and [compiled Stageplay scene](sources/media/revision-2/take-2/location-remote.stageplay)
- [Agent capture driver](sources/media/revision-2/capture.py) and
  [original screenplay generator](sources/media/revision-2/direct_remote.py)
- [Promo assembly](sources/media/revision-2/assemble_promo.py),
  [edit list](sources/media/revision-2/edl.json) and
  [chapter map](sources/media/revision-2/chapters.json)
- [Source provenance and bounded review](sources/media/revision-2/provenance.json),
  [decoded media checks](sources/media/revision-2/decoded-media-checks.json) and
  [external asset hashes](sources/media/revision-2/external-assets.json)

Both revision-two MP4s and the lossless source passed full decode. Browser playback reached
the end with zero reported dropped frames; representative motion and every promo
cut were reviewed. The 1280×720 promo uses integer scaling with padding; the full
short is 1200×672. This is detached Stageplay animation, not a native completion run
or a demonstration of dynamic gameplay events. Audio was decoded and inspected
numerically; physical listening is not claimed. Earlier rejected framing take 1
is retained separately and is not used in the final edit.

`stageplay/media` maps `~/scratch/agent-tmp/codex/stageplay-delivery` to the
[preserved source layout](sources/media/). Superseded external outputs are
`revision-2/stageplay-promo.mp4` and `revision-2/location-remote.mp4`. Videos,
ROM-derived pixels/audio, frame reviews, sampled state, fonts and packaged builds
remain external; catalog entries are not downloads. `stageplay/font` identifies
the external DejaVu Sans label font. Use a fresh writable copy when rebuilding.

See the [archive policy](../../docs/archive-policy.md) and
[rebuilding guidance](../../docs/rebuilding.md). Earlier exploratory Stageplay
materials outside revisions two and three were not imported by this production snapshot.
