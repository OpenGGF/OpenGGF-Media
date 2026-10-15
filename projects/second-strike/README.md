# Second Strike gameplay reels

## AIZ campaign development excerpt, 2026-10-15

The [new four-shot project](sources/aiz-campaign-20261015/README.md) preserves a
47-second native-speed excerpt from one native-entry Sonic solo development run:
forest approach, fire continuation, warned first-boss follow-up and playable Act 2
arrival. Three cuts leave the final twenty seconds with only one scene change.
Its own synchronized mixed native audio supplies each shot; no additional score
or loop is layered over it. The47-second/2820-frame edit passed full decode and bounded moving/cut/decoded-audio review; it does not certify complete AIZ or campaign traversal. The external movie is catalogued with its SHA-256 in provenance.

- [Editable frame-exact EDL](sources/aiz-campaign-20261015/edit-list.json)
- [Chapter map](sources/aiz-campaign-20261015/chapters.json)
- [Capture/source/creator-artifact provenance](sources/aiz-campaign-20261015/provenance.json)
- [Relocatable assembly source](sources/aiz-campaign-20261015/assemble.py)

This revision retains its original development HEAD/staged-tree and immutable
creator artifact separately; it does not reuse the old reel's delivered-package
claim. Footage and bulk state remain external. Earlier sources below are intact.

## Enemy expansion, 2026-10-14

This 14.5-second reel shows three changes to the Second Strike example mod: the
Guard's armored flame charge, the plant's wider barrage and the longer
Caterkiller Jr. Three native-speed gameplay shots are followed by a brief end
card, with two scene cuts and one continuous ROM-backed Angel Island music stem.
Scene SFX are omitted. The output is 1600×900 at 60 fps: 870 frames and four
chapters.

The new pictures come from the delivered engine package built at
`a8221fb7d5eb48f5bb199602227ec6ab4bbbf945`; its published evidence-only successor is
`7277cef4040af3ae95d86a794bce7f75a16cc483`.

- [Production notes and rebuild](sources/enemy-expansion-20261014/README.md)
- [Capture and package provenance](sources/enemy-expansion-20261014/provenance.json)
- [Edit list](sources/enemy-expansion-20261014/edit-list.json) and
  [chapter map](sources/enemy-expansion-20261014/chapters.json)
- [Capture controller](sources/enemy-expansion-20261014/ReelCapture.java),
  [native music controller](sources/enemy-expansion-20261014/ReelMusic.java) and
  [assembly script](sources/enemy-expansion-20261014/assemble.py)
- [Codec verification](sources/enemy-expansion-20261014/encode-verification.json)
  and [delivery review](sources/enemy-expansion-20261014/delivery-review.json)

The complete output decoded successfully. Recorded review covers every cut,
selected feature/caption frames, all selected source-frame identities and alive
state rows. Decoded audio contains 696,000 stereo frames at 48 kHz with no clipped
samples. These are bounded media checks, without a physical listening claim.

The scenes use positioned setups and declared incoming rings. The Caterkiller
take additionally selects the inherited fire-continuation event state on the
physical second act. These demonstrations do not certify cold-route completion,
native parity or physical audio latency.

Footage, recorded audio, PNG sequences, state CSVs and packaged builds remain
external. This repository preserves the production sources and location catalog;
catalog entries do not make the media downloadable. See
[rebuilding](../../docs/rebuilding.md) and [archive policy](../../docs/archive-policy.md).

## Source root

`second-strike/media` maps
`~/scratch/agent-tmp/codex/second-strike-enemy-expansion-20261014/short-reel-20261014`
to [the preserved sources](sources/enemy-expansion-20261014/). The final external
film is `second-strike-changes.mp4`. Place sources in a fresh writable copy of
that production layout and supply the catalogued dependencies before rebuilding.
Earlier `31b9503d3` proof captures are not used in this reel.
