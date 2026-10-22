# Engine and production references

Pinned to the engine checkout used for archive discovery: [`485e89fbe`](https://github.com/OpenGGF/OpenGGF/commit/485e89fbea5a2587b763052f0db115986ca681ce). Individual films retain their own capture commits.

- [Highlights production method](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/.agents/skills/gameplay-highlights/SKILL.md)
- [Gameplay capture tool and pitfalls](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/.agents/skills/gameplay-capture/SKILL.md)
- [Controller input authoring](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/.agents/skills/bk2-input-authoring/SKILL.md)
- [Trace replay rendering](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/.agents/skills/trace-capture/SKILL.md)
- [Headless setup](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/guide/contributing/headless-testing.md)
- [Capture/audio observation and isolated window diagnostics](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/tools/media/README.md)
- [Measurement hazards and promo lessons](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/agent-workflow/briefing-trace-rounds.md)
- [Development timeline](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/project/development-timeline.md)
- [Sitar Hero presentation and promo decisions](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/designs/2026-10-08-sitar-hero-presentation-polish.md)
- [Starpost Valley design and promo record](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/designs/2026-10-09-starpost-valley.md)
- [Flappy Tails tutorial and promo record](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/plans/2026-10-08-flappy-tails-tutorial.md)
- [Mutator Lab expansion record](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/plans/2026-10-08-mutator-lab-expansion.md)
- [S3K playable completion and ending reel record](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/plans/2026-10-13-s3k-playable-completion.md)
- [S3K ending lifecycle design](https://github.com/OpenGGF/OpenGGF/blob/485e89fbea5a2587b763052f0db115986ca681ce/docs/architecture/designs/2026-10-13-s3k-ending-lifecycle.md)

Implementation designs stay in the engine repository. Media-specific plans, EDLs and production scripts are preserved in this archive.

The [Second Strike AIZ development edit](../projects/second-strike/sources/aiz-campaign-20261015/README.md)
pins its original development HEAD, staged source tree and separate creator
artifact in local provenance. It is an editable unrendered production, not an
engine integration or whole-campaign qualification.

The [Emerald Remix finished promo](../projects/emerald-remix/README.md) pins its
compositor to OpenGGF `7d7246fbe`, preserves the coaching commit range
`f11ad311f..7d7246fbe`, and keeps the individual capture commits in their original
provenance. Its final edit, three post-round-5 coach fixes and exact loudness
normalisation encode are preserved separately from the superseded rough records.
