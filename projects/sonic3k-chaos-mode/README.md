# Sonic 3&K Chaos Mode demo and card-gallery revisions

## Latest: focused revision-4 gallery

The latest edit shows 20 representative effects across 12 actual S3K zones in
106 seconds: 6,360 frames at 1920×1080 / 60 Hz, with 22 chapters. One large
labelled picture plays at a time while completed cards stay frozen on a stationary
page. The film omits minigames, related challenges and chat; the example mod's
105-effect pool stays unchanged. A fresh native `ring-repulsion` demonstration
is labelled Ring Repellent editorially. Earlier reels and source identities
remain preserved.

Music and SFX reuse Slay the Robotnik and Flappy Tails' production scene-audio
method through the normal AudioManager, S3K profile and driver session. Actual
DAC proof combines 526 native enable writes, 980,211 nonconstant sample writes
and DAC-only output against an all-muted control. A fresh ghost replay reproduces
all 1,200 state/input rows and 342 selected picture frames; a music-stopped
soundboard then reproduces all 61 accepted native SFX admissions from their raw
requests. HCZ continues throughout the ghost card at the same gain. The film
uses neither DEZ music nor the older mixed PCM, guessed cues or external drums.

The clear Ring Repellent take has full RGB/PCM equality and keeps rings at zero
without hurt/death. The earlier unclear late-brake take remains rejected, with
its raw PNG/WAV retained because its interrupted comparison did not run. Native
roster and resolved-ID replay mistakes are documented without treating them as
passing evidence. This revision changes media workflows; the general direct-read
audio exporter and production engine remain unchanged.

Final checks cover complete audio/video decode, every PTS, all source intervals,
EOF/death, chapters and fast-start. Root and independent review cover seven
actual moving/cut/bookend pages (125 output samples) plus the six-frame native Ring
flight page. AAC measures −15.48 LUFS / −2.28 dBTP; three cue-free windows before,
during and after the ghosts retain HCZ at zero-lag correlations above 0.9998.
These are bounded media checks, without listening, continuous-route or native
parity claims.

- [Revision-4 production and rebuild](sources/media/revision-4/README.md), [plan](sources/media/revision-4/PLAN.md) and [20-card edit list](sources/media/revision-4/cards.json)
- [Final source and visual review](sources/media/revision-4/SHOT_REVIEW.md), [actual timeline](sources/media/revision-4/out/edit-timeline.json), [card/source map](sources/media/revision-4/out/chapters.csv) and [export qualification](sources/media/revision-4/out/media-review/summary.json)
- [Borrowed native-audio method and rejected approaches](sources/media/revision-4/audio-source/README.md), [production wrapper](sources/media/revision-4/audio-source/NativeAudioCapture.java), [renderer](sources/media/revision-4/render_audio.py) and [audio proof checks](sources/media/revision-4/verify_audio.py)
- [Music/DAC proof](sources/media/revision-4/assets/hcz2/render-provenance.json), [accepted ghost events](sources/media/revision-4/assets/ghosts/accepted-events.json), [SFX replay proof](sources/media/revision-4/assets/ghosts/render-provenance.json), [actual mix](sources/media/revision-4/out/audio-mix.json) and [source levels](sources/media/revision-4/out/audio-source-levels.json)

The packaged JAR remains byte-identical to revision 3. Its existing text-only
mod snapshot stays in [revision 3](sources/media/revision-3/mod-source/README.md)
and is not duplicated. New capture/audio source is engine commit
`88fc03dacd9835437070d40109d62b97a665f944`; retained earlier picture sources keep
their original identities and positioned/checkpoint qualifications.

## Published revision-3 gallery

The preceding edit is a stationary card gallery: one large labelled effect plays at a time, while completed cards stay frozen around it. Revision 3 shows 48 effects across 12 actual S3K zones in 241 seconds (14,460 frames at 60 Hz), with an HCZ2 music bed and genuine recorded mixed PCM during the final ghost card. The later DAC/workflow correction is recorded above; this section preserves revision 3's historical evidence.

Footage, ROM-derived artwork/audio, lossless source masters, state CSV, packaged mods and source ZIPs remain external. Their location and measurements belong to the [asset catalog](../../catalog/assets.csv), not downloadable GitHub attachments. This repository preserves the production sources and recorded evidence; it does not certify all effects, acts or ROM parity. See [rebuilding](../../docs/rebuilding.md).

## Revisions

- [Completed revision 4](sources/media/revision-4/README.md): the focused gallery, clear ring repulsion and qualified native DAC/SFX correction.
- [Completed revision 3](sources/media/revision-3/README.md): the calmer gallery, varied-zone captures, native ghost sound, exact source intervals and completed media review.
- [First reel production](sources/media/README.md): the original 89.4-second, 30-chapter demo and its original verification.
- [Completed revision 2](sources/media/revision-2/README.md): revised native footage, beat-based edit, exact source approvals, rebuild commands and documented limits.
- [Initial revision-2 blueprint](sources/media/revision-2-draft-20261014/PLAN.md): the earlier source snapshot retained before this refresh. These draft plans and partial implementation claims describe their historical state; use the completed directory to rebuild the delivered edit.

## Source root

`sonic3k-chaos-mode/media` maps `~/scratch/sonic3k-chaos-demo-20261014` to [sources/media/](sources/media/). Restore archived files into a new working copy of that layout and supply the external dependencies. The dated draft directory is a preserved copy of the former `revision-2` contents, not an additional capture root.

## Rebuild and review

- [Revision-3 plan](sources/media/revision-3/PLAN.md), [capture recipes](sources/media/revision-3/captures.json) and [48-card edit list](sources/media/revision-3/cards.json)
- [Source interaction and final visual review](sources/media/revision-3/SHOT_REVIEW.md)
- [Gallery compositor](sources/media/revision-3/assemble.py), [source qualification helper](sources/media/revision-3/review_sources.py) and [final export verifier](sources/media/revision-3/verify.py)
- [Actual revision-3 timeline](sources/media/revision-3/out/edit-timeline.json), [48-card source map](sources/media/revision-3/out/chapters.csv) and [completed export checks](sources/media/revision-3/out/media-review/summary.json); the movie has 50 chapters including its intro and end card
- [Native audio policy](sources/media/revision-3/audio.json), [actual mix](sources/media/revision-3/out/audio-mix.json), [37 lossless-master checks](sources/media/revision-3/lossless-source-checks.json) and [unchanged mod package record](sources/media/revision-3/out/mod-package.json)
- [Revision-2 edit plan](sources/media/revision-2/PLAN.md) and [assembly guidance](sources/media/revision-2/ASSEMBLY.md)
- [Capture and interaction review](sources/media/revision-2/SHOT_REVIEW.md)
- [Source approval lock](sources/media/revision-2/source-selections.json)
- [Actual edit timeline](sources/media/revision-2/out/edit-timeline.json) and [chapter/source map](sources/media/revision-2/out/chapters.csv)
- [Export and cut review](sources/media/revision-2/out/media-review/summary.json)
- [Lossless master checks](sources/media/revision-2/out/lossless-source-checks.json), [source ZIP record](sources/media/revision-2/out/source-archive.json) and [mod package record](sources/media/revision-2/out/mod-package.json)
- [Text-only mod sources](sources/media/revision-2/mod-source/README.md); the GPL-3.0 engine-derived source snapshot is included, while its JAR remains external
- [Rejected takes](sources/media/revision-2/rejected-takes/README.md)

Claude Opus 5.5 supplied the edit plans; OpenAI Codex GPT-6.1-Sol reviewed interactions, adapted the edits, captured the revised footage and assembled the exports. Revision 3 uses engine source `1a038f53cbdfc59184a32042a4f44f62d3664ee3` and the unchanged, SDK-validated example JAR. Thirty-five new sources and thirteen earlier demonstrations supply the selected cards; all 37 new lossless masters retain their exact captured RGB pixels and native PCM. Positioned MGZ/deep FBZ scenes, the SSZ checkpoint entry and Leaky Pockets' declared 32 carried rings remain explicit. Rejected MHZ bunny and SOZ2 sidegame attempts are retained and excluded from demonstrated effects.

The ghost finale uses DEZ1 source frames 552–894 and its genuine mixed PCM, with gain and fades only while the music bed ducks. The engine already produced apparition sound `0x92`; revision 2 had muted recorded gameplay audio. There is no observed death in this new source, no invented charge/death cue and no engine sound change. Final revision-3 qualification checks complete video/audio decode, every-frame cadence, source intervals/EOF/death, fast-start and 50 chapters. All 48 sampled moving regions change, and independent visual review covers all 12 moving/cut pages (288 sampled frames). The exported AAC measures −14.23 LUFS / −2.48 dBTP. This is media qualification; listening review, native parity and continuous route completion are not claimed.

## Preserved revision-2 evidence

Revision 2 has 45 shots and 46 qualified effect identities over 81.067 seconds (4,864 frames at 60 Hz), with a continuous HCZ2 bed, sliced panels and a post-credit consequence. Different panels use independent captures. Corrected native footage records `543c076fd`; allocator follow-up `45fff2130` preserves ordinary palette allocation without changing those small-roster scenes.

All revision-2 source gameplay PCM is muted in that edit because native music and SFX were captured together. The continuous ROM-backed HCZ2 render and explicit editorial stings are documented in its audio plan; native PCM is retained in external lossless masters. Leaky Pockets begins with a declared 32-ring inventory, and badnik transform takes use a positioned setup. Defence shows its board, inputs and score without claiming travelling shots or a victory; Snake shows movement without a food/win claim. The missed Vine grab and label-only Landmark are excluded.

The final mod package was built against composed host `97880ca2f662f4cd0ef24150755ad472d00f3d7a`, with SDK validation reporting zero findings and 74 focused tests passing across 14 classes without skips. These recorded package checks are separate from delivery-wide engine smoke qualification. The retained export review records −14.28 LUFS / −1.45 dBTP and unchanged H.264 packets/timestamps after audio remux. All 36 new masters passed complete RGB/native-PCM equality checks before redundant raw PNG/WAV copies were removed. This archive refresh reads those completed records and verifies preserved source hashes; it does not rerun the engine or decode footage.
