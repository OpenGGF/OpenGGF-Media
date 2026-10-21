# OpenGGF Stageplay

## One More Take — camera correction, 2026-10-22

Revision six corrects the vertical foreground mismatch the user found in the
ring-spill fall. Directed sprites, foreground scroll and the priority mask now
share the same view. The final landing meets the visible floor; all 4,860 native
state observations match revision five. No movement, physics or screenplay timing
was changed to hide the rendering error.

- [Production notes and rebuild](sources/media/revision-6/README.md)
- [Reusable scenes](sources/media/revision-6/scenes/) and
  [capture driver](sources/media/revision-6/capture.py)
- [Promo compositor](sources/media/revision-6/assemble_promo.py) and
  [five-shot chapter map](sources/media/revision-6/chapters.json)
- [Source and review evidence](sources/media/revision-6/provenance.json),
  [decoded media checks](sources/media/revision-6/decoded-media-checks.json),
  [assembly identity](sources/media/revision-6/stageplay-live-promo.assembly.json)
  and [external asset hashes](sources/media/revision-6/external-assets.json)

The replacement retains the 60-second film and 8/9/4-second companions. All nine
MKV/MP4 files decoded completely at 60 fps; the promo measures −18.0 LUFS and
−4.8 dB true peak. Normal-speed browser playback and bounded visual review included
contact, shot boundaries and the closing group run. The browser reported two
presentation-frame drops in the promo and none in the companions; source decoding
contained every expected frame. Physical listening and creative acceptance are not
claimed. The corrected runtime passed 124 focused checks; the external Editor
passed 22 checks with no skips against it.

Background deformation and effects retain the native gameplay camera phase;
arbitrary-view parallax is not recomputed. Death Egg's stationary background is
intentional. At ring frame 120, Tails' native collision surface has transparent
floor art; the correction preserves this distinction.

External movies, state, review images and the exact engine package are retained
under `stageplay/media` at `revision-6/`. The promo is
`stageplay-live-promo.mp4`; catalog entries identify files, not downloads.
Revision five remains below as the known flawed predecessor.

## One More Take — LIVE world revision, 2026-10-21

**Known visual defect, identified by the user on 2026-10-22:** the ring-spill fall
uses inconsistent vertical camera origins for scenery and native sprites. Grounded
characters can appear to stand in empty space. Revision five is preserved as the
reviewed-but-flawed take; its recorded codec and physics checks did not detect this
rendering defect. Revision six above supplies the corrected take. The original provenance below
records the earlier review and must be read with this correction.

Revision five directs real level objects and native character abilities. Sonic and
Tails board and trade moving platforms, a ring-run mishap produces native hurt and
scattered rings, Tails and Knuckles regroup by flight/glide, and the three-character
closing run uses a following camera. Puppet and Poser remain distinct authoring modes.

- [Production notes and rebuild](sources/media/revision-5/README.md)
- [Reusable scene sources](sources/media/revision-5/scenes/)
- [Agent-friendly capture driver](sources/media/revision-5/capture.py)
- [Continuous promo compositor](sources/media/revision-5/assemble_promo.py)
  and [five-shot chapter map](sources/media/revision-5/chapters.json)
- [Native evidence and review](sources/media/revision-5/provenance.json),
  [decoded media checks](sources/media/revision-5/decoded-media-checks.json),
  [assembly identity](sources/media/revision-5/stageplay-live-promo.assembly.json)
  and [external asset hashes](sources/media/revision-5/external-assets.json)

The retained short is 60 seconds at 60 fps. The promo preserves all 3,600 source
frames, with fixed integer enlargement, brief opening/closing titles and one
captured soundtrack. Companion demonstrations isolate platform transfers (8 s),
flight/glide (9 s) and ring pickup/hurt/recovery (4 s). Source recipes include explicit
native movement, waits, abilities and actual placement targets. The recorded ring
count is the shared native total, not separate collection credit for each actor.

LIVE is an isolated production world per shot, with positioned starts and authored
routes. It does not prove uninterrupted level completion, general pathfinding or
ROM parity. Its native state JSONL is distinct from both pure authored timeline
samples and normal gameplay capture CSV. Limits and exact review scope are retained
in the provenance; physical audio listening and user creative approval are not claimed.

External outputs live under `stageplay/media` at `revision-5/`:
`one-more-take-review.mkv`, its MP4 viewing copy and `stageplay-live-promo.mp4`.
The three companion movies, state observations, editor images, packaged engine and
superseded first rendering remain external too. Catalog entries are not downloads.
Earlier revisions below preserve the development history.

## Location, Location, Location — terrain Puppet revision, 2026-10-21

Revision four uses native player physics for all three roles: floor support,
destination/urgency commands, acceleration, jump holds, collision and landing.
The 51-second story keeps its named dialogue, three typing styles and decorated
speaker panels, with fixed zoom and camera pans, shake, wipes and fades. Both
editors also retain **Poser** mode for manual position, animation and frame selection.

- [Production notes and rebuild](sources/media/revision-4/README.md)
- [Screenplay](sources/media/revision-4/take-3/location-remote.screenplay.json)
  and [compiled scene](sources/media/revision-4/take-3/location-remote.stageplay)
- [Screenplay/panel generator](sources/media/revision-4/direct_remote.py)
  and [compile, simulate and capture driver](sources/media/revision-4/capture.py)
- [Promo compositor](sources/media/revision-4/assemble_promo.py),
  [edit list](sources/media/revision-4/edl.json) and
  [chapters](sources/media/revision-4/chapters.json)
- [Native simulation observations and review](sources/media/revision-4/provenance.json),
  [decoded media checks](sources/media/revision-4/decoded-media-checks.json) and
  [external asset hashes](sources/media/revision-4/external-assets.json)

All 3,060 native simulation frames resolve without blocked goals. Four jumps land
through the native controller; the two final chase goals intentionally leave the
frame before arrival. Agent review covered half-second motion samples, all six
transitions, named dialogue, tails and title entrances/exits. Both MP4s decoded in
full and browser playback reached 51 seconds at rate one with zero reported dropped
frames. Audio was decoded and metered; physical listening and user creative approval
are not claimed.

This is authored performance against detached terrain. It does not run live objects,
moving platforms, water/zone events, automatic navigation or native cross-game loads.
Authored timeline JSONL and actual Puppet simulation JSONL remain distinct; neither
certifies full-world gameplay or ROM parity. The first two revision-four input takes
are retained with their outcomes in provenance; take three is the final render.

External outputs: `revision-4/location-remote.mp4` (1200×672) and
`revision-4/stageplay-promo.mp4` (1600×900) under `stageplay/media` below.
The lossless 400×224 source and all production dependencies remain external.

## Superseded dialogue revision, 2026-10-21

The user rejected revision three's hand-keyed jump. Its retained review establishes
decoding and presentation checks, not acceptance of that motion.

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
materials outside the retained numbered revisions were not imported by this production snapshot.
