# OpenGGF-Media

Production sources for OpenGGF promotional reels, development highlights and mod
showcases: plans, blueprints, capture/input scripts, edit lists, chapters,
provenance and original DaVinci Resolve editing projects.

**31 production groups · 7,631 preserved source files · approximately 179 GiB of
external material catalogued.** The videos and raw captures remain external;
this repository contains their production sources and location catalog.

## Browse the productions

| Production | Sources | External asset/sequence entries |
| --- | ---: | ---: |
| [Hidden Palace highlights and capture sources](projects/hpz-highlights/) | 55 | 236 |
| [Doomsday highlights and capture sources](projects/ddz-highlights/) | 86 | 228 |
| [Lava Reef highlights and capture sources](projects/lrz-highlights/) | 1,772 | 5,106 |
| [Sky Sanctuary highlights and capture sources](projects/ssz-highlights/) | 515 | 1,646 |
| [Death Egg highlights and capture sources](projects/s3k-dez-highlights/) | 796 | 2,092 |
| [Mushroom Hill highlights and capture sources](projects/mhz-highlights/) | 158 | 408 |
| [Sandopolis highlights and capture sources](projects/soz-highlights/) | 62 | 138 |
| [Death Egg campaign follow-ups highlights and capture sources](projects/dez-highlights/) | 39 | 142 |
| [Flying Battery highlights and capture sources](projects/fbz-highlights/) | 4 | 21 |
| [Original Sonic 1 / Sonic 2 / Sonic 3&K release reels](projects/release-reels/) | 11 | 75 |
| [Seamless act presentation](projects/seamless-presentation/) | 5 | 15 |
| [Sky Sanctuary arena demo revisions](projects/ssz-arena-demos/) | 8 | 24 |
| [Slay the Robotnik highlights and promo](projects/slay-the-robotnik/) | 263 | 109 |
| [Starpost Valley promo and follow-ups](projects/starpost-valley/) | 92 | 206 |
| [Sonic 3&K ending reel revisions](projects/s3k-endings/) | 16 | 155 |
| [Putt-Putt Paradise highlights and promo revisions](projects/putt-putt-paradise/) | 350 | 357 |
| [Flappy Tails promo](projects/flappy-tails/) | 7 | 56 |
| [Typing of the Hedgehog promo and route demo](projects/typing-of-the-hedgehog/) | 51 | 59 |
| [Sitar Hero promo](projects/sitar-hero/) | 25 | 15 |
| [Mutator Lab expansion promo](projects/mutator-lab-expansion/) | 5 | 2 |
| [Mutator Lab gameplay promo](projects/mutator-lab-gameplay/) | 678 | 335 |
| [Mutator Lab complete showcase and audio revision](projects/mutator-lab-showcase/) | 480 | 403 |
| [Sandopolis earlier work highlights](projects/soz-methodology/) | 609 | 2,120 |
| [Sonic 3&K Chaos Mode demo and card-gallery revisions](projects/sonic3k-chaos-mode/) | 706 | 293 |
| [Second Strike gameplay reels and AIZ development edit](projects/second-strike/) | 39 | 18 |
| [OpenGGF Stageplay original short and directing promo](projects/stageplay/) | 170 | 205 |
| [Emerald Remix coached promo](projects/emerald-remix/) | 216 | 204 |
| [Multiplayer Time Attack promo](projects/time-attack-promo/) | 231 | 205 |
| [Sonic Echoes promo](projects/sonic-echoes-promo/) | 61 | 66 |
| [Day Off: Stageplay introduction promo](projects/stageplay-day-off-promo/) | 116 | 71 |
| [Shared production workflows and generic reel builder](projects/shared-production/) | 5 | 0 |

The original release-reel projects cover Sonic 1, Sonic 2 and Sonic 3&K. Later
collections cover zone bring-ups, ending sequences, Slay the Robotnik, Putt-Putt
Paradise, Flappy Tails, Typing of the Hedgehog, Sitar Hero, Starpost Valley,
Mutator Lab, Chaos Mode, Second Strike, Stageplay, Emerald Remix, multiplayer Time Attack, Sonic Echoes and the Day Off Stageplay introduction. Retained drafts and revisions remain identifiable;
Chaos Mode retains its earlier reels alongside the focused revision-4 gallery:
twenty representative effects, twelve zones and qualified native DAC/SFX capture.
Second Strike also retains a separately identified47-second AIZ development
excerpt with bounded render review beside its earlier delivered film. Emerald Remix
retains its finished 41.683-second edit, rejected revisions and coached production history.
The multiplayer Time Attack promo retains its finished 81.817-second edit, every
superseded edit revision and the capture records behind each review round.
Day Off retains the approved v2 film's edit, editor capture drivers and scenes beside
its preserved first version.

## Use the archive

- [Rebuild and relink an edit](docs/rebuilding.md)
- [Production/engine references](docs/source-references.md)
- [Scope, maintenance and rights](docs/archive-policy.md)
- [External footage and asset catalog](catalog/assets.csv)
- [Original root locations](catalog/roots.json)
- [Preserved source hashes and provenance](catalog/sources.json)
- [Resolve media references](catalog/resolve-references.json)
- [Initial import scope and measurements](catalog/import.json)

```sh
python3 tools/catalog.py projects
python3 tools/catalog.py assets slay-the-robotnik --limit 20
python3 tools/catalog.py verify
```

Original scripts preserve their historical paths and dependencies. Consult each
production's plan before rebuilding; the archive is not a promise that every
historical edit runs unchanged on the current engine. The source catalog verifies
included file hashes, not external footage availability or a fresh render.

[OpenGGF](https://github.com/OpenGGF/OpenGGF) is an independent fan project, with no
Sega affiliation. ROMs and extracted game assets are not included. Engine-derived
code retains its GPL-3.0 terms; see [rights](docs/archive-policy.md#rights).
