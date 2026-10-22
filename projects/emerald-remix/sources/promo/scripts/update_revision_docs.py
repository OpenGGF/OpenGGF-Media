#!/usr/bin/env python3
"""Write frame-accurate revision metadata from the instantiated local promo, 2026-10-22.
Inputs: edit.py; outputs: production beat sheet and chapters. No repository writes.
"""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
e=pk.load_edit(P/'edit.py');b=e.bf
rows=[('Cold open',0,4,'remix-tumble-hero-final',103,'Best tumble poses, unchanged native motion.'),
 ('Two versus three',4,12,'stock-tumble-wide-exit02-final + remix-tumble-wide-final',50,'ONE / TWO / THREE follows measured crests; native palette restored.'),
 ('New route',12,16,'stock-opening-final + remix-opening-final',195,'One brief comparison; labels moved clear of the native HUD.'),
 ('Title slam',16,24,'remix-opening-final',0,'Preserved flash, C3 stinger and 26-frame camera slam; native white/grey/black type.'),
 ('ROM strip assembly',24,28,'editorial ROM-art diagram',None,'Actual foreground pieces from remixed world x4096–5248, split at x4864: double + single. They arrive separately and join; this is a diagram, not gameplay.'),
 ('Run the triple',28,36,'remix-tumble-hero-final',65,'NOW RUN IT clears quickly; complete unrolled triple stays uninterrupted.'),
 ('Clover route',36,60,'clover-shipping-route-final',100,'Continuous native spring, upper landing, ring line and step jump.'),
 ('Clover finish',60,65,'clover-shipping-route-final',100+b(60)-b(36),'Exact source continuation; held 1.25x crop at (160,89.6) keeps the 400px capture from revealing beyond the native right bound, while preserving top HUD rows. Sonic exits the cropped view.'),
 ('End card',65,77,'clover-tail-final',30,'Fresh moving run-out; native logo and practical source URL/status/disclaimer.')]
chap=[]
for name,a,z,src,si,note in rows:
 f0=0 if a==0 else b(a);f1=b(z)
 chap.append(dict(name=name,out_in=f0,out_out=f1,source=src,source_in=si,source_out=None if si is None else si+f1-f0,fps=60,note=note))
(P/'chapters.json').write_text(json.dumps(chap,indent=2)+'\n')
s='''# Emerald Remix — coached revision beat sheet

2026-10-22. This supersedes the 41-second rejected rough cut. `edit.py build(e)` is authoritative.
1920×1080, 60 Hz, 106.63416863432099 BPM, first beat 0.04071119047619047 s.
**2602 frames / 43.366667 s.** Native gameplay remains unretimed.

The pitch is now **your ROM, rearranged — then somewhere entirely new**. The counted comparison,
cold open and title impact remain. Four added beats show the actual double + single construction.
Clover's continuous run has a new editorial development every bar, instead of 14 seconds of bare footage.

| Beats | Output frames [in,out) / seconds | Source | What the beat gives the viewer |
|---|---|---|---|
'''
for r,c in zip(rows,chap):
 name,a,z,src,si,note=r
 source=src if si is None else f'{src} {si}–{c["source_out"]}'
 s+=f'| {a}–{z} | {c["out_in"]}–{c["out_out"]} / {c["out_in"]/60:.3f}–{c["out_out"]/60:.3f} | {source} | {note} |\n'
s+='''
Clover accompaniment (all over the same continuous native-speed take):

| Beats | Editorial change / evidence |
|---|---|
| 36–40 | CLOVER VALLEY / SOMEWHERE NEW enters in stock-card colours; all native HUD digits remain clear. |
| 40–44 | A ZONE DRAWN BY CODE. The actual `decor_pixel("clover",x,y)` output scans in row by row at a fixed 18× scale; PIXEL RULE identifies it as an art diagram. The generator reads no ROM. |
| 44–48.1 | TAKE THE HIGH ROAD. Subtle 4.5% compositor punch and ROM CC spring cue at the observed launch (source 435 / output 1553), not a guessed beat. Native landing is source 506. |
| 48.2–52 | FOLLOW THE GOLD points the eye down the native ring trail. No fake score or invented collection sounds. |
| 52.2–56 | ONE MORE LEAP accompanies the actual step-up jump at source 710. |
| 56.2–60 | HOW FAST CAN YOU GO turns the last crest/run into a player invitation. |
| 60.2–64.8 | YOUR TURN over signpost contact/spin and run-out, before the source end card. |

Palette evidence: stock title-card reference frame 62. ROM glyph indices 6/1/7/8 are white,
black, #B6B6B6 and #929292. The black +2,+2 shadow and grey bevels are already in the art.
There is no extra outline/drop, red shadow, yellow recolouring or mask-wide white shine.
Eight reference letters have palette-exact ink matches against the native screenshot.

The strip image is a world-aligned editorial mosaic, with moving background/HUD detached;
only the two large orange/brown track components are retained. Source frames are unmodified.
The exact 768px double/384px single division comes from `ehz1.remix`, not a fitted route.
It is a conceptual assembly, not a filmed editor feature or continuous gameplay.

Corkscrew shots and the end-card run retain disclosed positioned entries. EHZ openings and
Clover are direct act loads; the film does not claim a continuous EHZ-to-Clover run. Clover
keeps the prior shipping-presentation limitation (`mods.skipModZoneTitleCards: true`, no
native mod card). No new gameplay capture, engine repair, asset export, immunity or state write.

One uninterrupted ROM EHZ 2P bed owns the music. C3 title, BC chapter and B5 split/assembly
cues remain editorial; CC is separately rendered from the ROM and aligned to the observed
spring. This is a rough mix, not a mastering or physical listening approval.
'''
(P/'BEAT_SHEET_REVISED.md').write_text(s)
print('updated chapters / beat sheet',e.end(),e.check(),e.pacing()[0])
