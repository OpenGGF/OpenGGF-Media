# Emerald Remix — “Know the way?”

Planning review • 22 October 2026 • design only • source `8aa692b045c195ef8a42896b6bbc9549158470c0`

Audience: Sonic fans who know Emerald Hill by feel and want a fresh reason to run it.

Form and evidence: a music-led gameplay trailer. All playable action comes from ordinary OpenGGF gameplay under controller inputs. The title and chapter treatments are editorial. No Stageplay, fake physics, editor tour or developer monologue is needed.

Promise: rediscover Emerald Hill Act 1, then explore the original Clover Valley zone.

The emotional route is recognition → surprise → discovery → “I want a turn.” Lead with familiar grass, loops and momentum. Let the new arrangement challenge the viewer’s memory. Show the triple corkscrew as a complete action. Open the picture into Clover Valley and let its new landscape carry the second half. Finish with the native signpost and a practical invitation.

Hero moments: Emerald Hill’s joined triple corkscrew is the memorable remix proof. Clover Valley’s proposed spring → ring line → landing is the new-zone payoff. Its trajectory remains an unverified capture target; do not advertise it as achieved. The fallback is a sustained hill descent with a clear landing and parallax.

Sound: one coherent Emerald Hill 2P bed (S2 `0x91`), already used by Clover Valley. It keeps the Sonic 2 identity while feeling like a side of Emerald Hill some fans hear less often. No mid-cut clip music. At most two quiet editorial ROM stingers: swish on title/reveal and ring on the invitation, separately rendered if useful after review. No voice-over. The planning bed has no SFX yet.

Delivery target: approximately 70.37 seconds, 1920×1080 at 60 fps, landscape. The edit has eleven proposed source blocks, including one moving end card. Most action takes last 4.5–9.5 seconds. More than 90% of the proposed timeline retains moving gameplay as its background; there are no menus. Reallocate bars if a complete action needs room. Never speed up gameplay to fit music.

## Why these choices

This mod changes two places rather than adding a large feature system. The best invitation is to show how those places feel to run. A tutorial or code panel would spend its strongest seconds addressing mod authors. A rapid feature montage would repeat the same few routes. The selected treatment gives fans time to recognize a piece, notice the surprise and follow the consequence.

The triple corkscrew is stronger evidence than “remixed” written over an ordinary hill. Clover Valley earns an uninterrupted full-width reveal; its original tiles, flowers and layered horizon deserve equal attention. The late spring/landing shot gives the original zone a climax of its own. Stock Act 2 stays outside the showcase, with a short explicit progression caption so the edit cannot imply that Clover directly follows Act 1.

A 45–50 second version was considered: it would compress two route identities, two hero actions and practical copy into short fragments. A 90-second developer tour would overstate the scale of this small example. The current 70-second proposal is a reviewable middle; S05 is the first cut if the pacing needs tightening, and the repeated single in S06 is expendable if it repeats the hero. The information-rich end card gets nine seconds so the invitation can actually be read.

## Visual direction

Use broad, stable gameplay views and crisp Sonic 2-inspired diagonal type. Travel and transitions run left → right. Only the title and Clover reveal get a short banded wipe; ordinary changes are clean musical cuts. One restrained dissolve leads into the end card. Avoid zoom punches during the corkscrew or spring arc: they could hide the action this film is selling.

Capture the hero passes at 400×224. Preserve the whole frame with a static 4× nearest-neighbour enlargement (1600×896), positioned at (160,92) on the 1080p canvas. Use an edge-to-edge moving extension of the same scenery, softened and dimmed, behind it; no solid letterbox field. Keep the foreground view large and visually unboxed. If that treatment feels inset at review, use a static aspect-preserving 1920×1075.2 fit with BOX filtering after integer upscale, and inspect motion for softness. Never stretch 400×224 directly into 16:9. Native 320×224 is a fallback if 400-wide behavior proves unstable; widen the background treatment rather than crop a landing.

Primary colors come from Clover Valley’s committed Genesis palette, decoded with the generator’s RGB conversion: grass `#6DDA6D` (line 2 index 10), sky `#6DB6FF` (shared sky), flower-center gold `#FFDA00` (line 2 index 14), and deep green `#004800` (line 2 index 7). White is a text neutral. These are original-zone colors, not invented samples from uncaptured gameplay. Recheck the rendered display profile next session.

Use installed Fira Sans Compressed Heavy / Heavy Italic for the editorial title: a deliberate heavy condensed fallback because Emerald Remix keeps Sonic 2’s stock title and ships no mod logo/font. Title 150–180 px at 1080p; chapter 100–130 px; promise 64–76 px; practical copy 30–40 px. White/gold fill, dark green 6–8 px outline and firm shadow. A short diagonal grass/sky band is original editorial decoration, not claimed to be ROM title-card art. Type enters in 12–16 frames, exits in 8; hold informational lines still. Leave Sonic’s path, jump apex, landing and HUD readable. Use no more than one sales idea at once and keep most of the new-zone action text-free.

## Copy and invitation

Opening: “KNOW THE WAY?” → “EMERALD HILL. REMIXED.” The promise must read by six seconds, even though the full identity arrives at the first strong section candidate around nine seconds.

Title: “EMERALD REMIX” / “A fresh run through Sonic 2.”

Remix hero: “THREE CORKSCREWS. ONE RUN.” Remove before the rotations.

Bridge: “AFTER EMERALD HILL ACT 2…” → “CLOVER VALLEY”. Avoid a false direct Act 1 → Clover handoff.

End card, stable for roughly 9 seconds:

- EMERALD REMIX
- Take the remix for a spin.
- `github.com/OpenGGF/OpenGGF` • `examples/emerald-remix`
- Development example • Mod API 0.7 candidate
- Java 25 + matching development JVM build
- Fan-made and free. Not affiliated with SEGA. Requires your own ROM.
- Sonic 2 World REV01

Use the repository URL plus visible folder path as the call to action; there is no verified standalone download page. Native game title, other zones and EHZ Act 2 remain stock. Do not imply a full new campaign, new bosses, stock-ROM compatibility or inclusion in the public 0.6 release. The example manifest’s `1.0.0` is its own package version, not engine-release status.

## Session boundary

This package is ready for a creative review. No gameplay or reference footage has been captured. The generated map is an authoring reference, not an engine screenshot. Capture begins only in a later session after the user reviews this plan. No repository edits, commits, pushes or OpenGGF-Media changes are authorized in this session. The skills’ eventual archive requirement is deferred by that explicit boundary.
