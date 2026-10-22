# Study notes and borrowing

All engine/mod observations below refer to checkout `8aa692b045c195ef8a42896b6bbc9549158470c0`, branch `feature/ai-promo-skill-coaching`. This was source study and a generated static-layout inspection, not a playthrough. No claim about the quality of unrecorded motion is implied.

## The actual example

Read `examples/emerald-remix/README.md`, `EmeraldRemixMod.java`, `RemixedLevel.java`/recipe interfaces as needed, the exact `ehz1.remix` strip recipe, Clover Valley’s `level.json`, terrain generator and parallax implementation. Read the package/progression and route-test portions of `TestEmeraldRemix`.

The borrowed EHZ2 passage occupies remixed map columns 7–13 (x=896–1791). EHZ1 columns 18–35 follow. The triple uses remixed columns 32–40 (x=4096–5247): the original double, then the original single. The single reappears at remixed columns 74–76 (x=9472–9855). Those are layout anchors, not invented captured frame numbers.

Clover is one original act, with gentle hills, step-ups, floating ledges, small flowers and clover decorations, a long ring line, monitors, a yellow upright spring, checkpoint and signpost. The generated static map in `design/clover-layout-reference.png` was made with `--check --preview`: it verified all twelve committed exports and wrote no source assets. It omits player/object gameplay and is not evidence that any planned jump succeeds. Its extended background tiling is a layout view, not a production camera preview.

Clover’s scroll owner uses 1/8 camera movement for sky/clouds, 1/4 for mountains/hills and 1/16 vertical rise. Borrow that sense of depth in a long travelling take, rather than covering the horizon with a caption.

Important capture finding: runtime registry appends Clover after Sonic 2’s eleven stock zone entries, so the sole-mod CLI zone is **11**, act **1**. JSON `zoneIndex:64` and `levelIndex:1024` are different internal identities. Confirm resolved identity at capture time; more enabled mods could change the index. The route test uses damage immunity every frame, so it proves a narrower terrain/progression claim and is not a capture recipe for a normal player run.

## Slay the Robotnik — musical organization

Read the complete `build()` edit, music mixer, `render_audio.py`, production README and chapter list at OpenGGF-Media commit `c2f0c0218a2fa97a204ed527a36810babadb4b41` (read-only HTTP; no media checkout touched).

- [Edit source](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/tools/promo.py)
- [Audio renderer](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/tools/render_audio.py)
- [Production notes](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/README.md)

Borrow the beat clock, chapters at musical changes, short title treatment over motion, one coherent bed and an uninterrupted action into its consequence. Its sixteen-beat title interval and longer journey/final-blow intervals demonstrate that a title or payoff need not be a rapid montage. Its debugging setup is explicitly documented; borrow that honesty, not the debug kills. Do not copy its three-game engine pitch, card statistics or crowded event grid: Emerald Remix has a simpler audience promise.

The old renderer depends on another worktree’s test helper and an S3K startup-scene mod. Adapted the *principle* to the current production `FmSfxRenderTool`, which renders S2 music directly through SMPS without graphics or a temporary mod.

## Putt-Putt Paradise — Sonic 2 editorial type

Read `card_caption()`, `chapter_card()`, transition code and relevant `build()` sections in [render_promo.py](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/putt-putt-paradise/sources/media/promo-opus-20261006/final-verified/render_promo.py).

Borrow its staggered heading arrival, strong italic letters, outline/shadow and a decisive departure. Its red serrated spine, blue band and yellow subtitle motivate a coherent Sonic 2 visual language. For this production, use a lighter original grass/sky/gold treatment so it supports the landscape instead of advertising mini golf. Do not copy the cup iris or tutorial panels.

## Local craft and workflow references

Read `.agents/skills/promo-direction/SKILL.md`, `references/lessons.md`, relevant `references/moves.md`, `gameplay-highlights`, `gameplay-capture`, `bk2-input-authoring` and `headless-rendering`.

The archived complaints “very rushed” and “cluttered audio and rapid cuts” are the reason for fewer complete actions and one soundtrack owner. The documented fractional-zoom and vertical-ground-alignment failures motivate stable source framing and a motion review of feet, terrain and jump landings. No screenshot or codec check will substitute for watching those sequences.

Limits: the referenced finished videos were not available in this checkout and were not watched. Reference claims here concern inspected source, chapter timing and recorded feedback, not motion or listening judgments. No footage or visual asset from those productions is reused. No external commercial soundtrack is introduced; the planning WAV is a local ROM-derived render, not represented as royalty-free or independently licensed music.
