# Sonic 3&K Chaos Mode demo and rapid-fire revision

The first reel is preserved alongside the completed rapid-fire second edit. Revision 2 has 45 shots and 46 qualified effect identities over 81.067 seconds (4,864 frames at 60 Hz), with a continuous HCZ2 music bed, sliced panels and a post-credit consequence. Different panels use independent captures. The original first-reel export and inputs remain unchanged.

Footage, ROM-derived artwork/audio, lossless source masters, state CSV, packaged mods and source ZIPs remain external. Their location and measurements belong to the [asset catalog](../../catalog/assets.csv), not downloadable GitHub attachments. This repository preserves the production sources and recorded evidence; it does not certify all effects, acts or ROM parity. See [rebuilding](../../docs/rebuilding.md).

## Revisions

- [First reel production](sources/media/README.md): the original 89.4-second, 30-chapter demo and its original verification.
- [Completed revision 2](sources/media/revision-2/README.md): revised native footage, beat-based edit, exact source approvals, rebuild commands and documented limits.
- [Initial revision-2 blueprint](sources/media/revision-2-draft-20261014/PLAN.md): the earlier source snapshot retained before this refresh. These draft plans and partial implementation claims describe their historical state; use the completed directory to rebuild the delivered edit.

## Source root

`sonic3k-chaos-mode/media` maps `~/scratch/sonic3k-chaos-demo-20261014` to [sources/media/](sources/media/). Restore archived files into a new working copy of that layout and supply the external dependencies. The dated draft directory is a preserved copy of the former `revision-2` contents, not an additional capture root.

## Rebuild and review

- [Revision-2 edit plan](sources/media/revision-2/PLAN.md) and [assembly guidance](sources/media/revision-2/ASSEMBLY.md)
- [Capture and interaction review](sources/media/revision-2/SHOT_REVIEW.md)
- [Source approval lock](sources/media/revision-2/source-selections.json)
- [Actual edit timeline](sources/media/revision-2/out/edit-timeline.json) and [chapter/source map](sources/media/revision-2/out/chapters.csv)
- [Export and cut review](sources/media/revision-2/out/media-review/summary.json)
- [Lossless master checks](sources/media/revision-2/out/lossless-source-checks.json), [source ZIP record](sources/media/revision-2/out/source-archive.json) and [mod package record](sources/media/revision-2/out/mod-package.json)
- [Text-only mod sources](sources/media/revision-2/mod-source/README.md); the GPL-3.0 engine-derived source snapshot is included, while its JAR remains external
- [Rejected takes](sources/media/revision-2/rejected-takes/README.md)

Claude Opus 5.5 supplied the initial edit plan; OpenAI Codex GPT-6.1-Sol reviewed interactions, adapted the edit, captured the revised footage and assembled the final export. Source commit and package hashes belong to each original capture's provenance. Corrected native footage records `543c076fd`; allocator follow-up `45fff2130` preserves ordinary palette allocation without changing those small-roster scenes.

All source gameplay PCM is muted in the edit because native music and SFX were captured together. The continuous ROM-backed HCZ2 render and explicit editorial stings are documented in the audio plan; native PCM is retained in external lossless masters. Leaky Pockets begins with a declared 32-ring inventory, and badnik transform takes use a positioned setup. Defence shows its board, inputs and score without claiming travelling shots or a victory; Snake shows movement without a food/win claim. The missed Vine grab and label-only Landmark are excluded.

The final mod package was built against composed host `97880ca2f662f4cd0ef24150755ad472d00f3d7a`, with SDK validation reporting zero findings and 74 focused tests passing across 14 classes without skips. These recorded package checks are separate from delivery-wide engine smoke qualification. The retained export review records −14.28 LUFS / −1.45 dBTP and unchanged H.264 packets/timestamps after audio remux. All 36 new masters passed complete RGB/native-PCM equality checks before redundant raw PNG/WAV copies were removed. This archive refresh reads those completed records and verifies preserved source hashes; it does not rerun the engine or decode footage.
