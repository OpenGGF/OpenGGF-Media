#!/usr/bin/env python3
"""Record the actual instantiated rough-cut edit and source windows, 2026-10-22."""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
e=pk.load_edit(P/'edit.py');b=e.bf
rows=[(0,4,'Cold open','remix-tumble-hero-final',103,'Full bleed; already inside the tumble. No introductory logo.'),
 (4,12,'Two versus three','stock-tumble-wide-exit02-final + remix-tumble-wide-final',50,'800px stacked strips, native ORIGINAL / REMIX labels and count words following observed crests. Stock jumps only after its double; shared input before that, no identical-input claim afterward.'),
 (12,16,'New route','stock-opening-final + remix-opening-final',195,'One short stacked comparison. SAME HILL NEW ROUTE; terrain visibly diverges. These are distinct cold runs, not matched post-divergence inputs.'),
 (16,24,'Title drop','remix-opening-final',0,'Moving opening, ROM EMERALD REMIX, flash, C3 stinger, 26-frame slam-out and glyph-clipped shine.'),
 (24,32,'Complete triple','remix-tumble-hero-final',65,'One unrolled approach through all three and the exit. Clear of captions. CSV rolling=0 and tumble mappings 95–106.'),
 (32,40,'Clover entrance','clover-shipping-route-final',100,'Banded wipe into default mod presentation; editorial CLOVER VALLEY in ROM letterforms. No native mod-zone card.'),
 (40,56,'Clover spring and route','clover-shipping-route-final',370,'Exact continuation; spring f435, upper landing f506, ring line and final step jump f710. No gameplay audio or invented collection effects.'),
 (56,61,'Clover finish','clover-shipping-route-final',910,'Exact continuation through signpost contact/spin and native run-out. Ends before a long results hold.'),
 (61,73,'End card','clover-tail-final',30,'Separate fresh moving run-out, softened; ROM logo, promise, readable example URL/status/disclaimer, final two-second fade.')]
head='''# Emerald Remix — revised rough-cut beat sheet

This supersedes the capture-stage plan. `edit.py build(e)` is instantiated and is the authoritative timeline. 1920×1080 / 60 fps; 106.63416863432099 BPM, first beat 0.04071119047619047 s. Gameplay stays at native speed, with every captured frame used.

The review corrections are structural: the hero runs unrolled, the count uses 800px full-width strips, Clover is announced editorially over its default shipping presentation, and each comparison appears once. Comparison time is now 6.77 s (4.52 s for the stronger count, 2.25 s for the weaker route claim), down from about 21 s. Overall rough cut: 41.117 s. Title remains at musical candidate 16, Clover moves to candidate 32, and the end card takes candidate 61. Section candidates/beat phase were measured; musical bar/downbeat and listening approval remain open.

| Beats | Output seconds / frames [in,out) | Picture / source frames [in,out) | Type, sound and evidence |
|---|---|---|---|
'''
lines=[];chap=[]
for a,z,name,source,src,why in rows:
 f0=0 if a==0 else b(a);f1=b(z);end=src+f1-f0
 lines.append(f'| {a}–{z} | {f0/60:.3f}–{f1/60:.3f} / {f0}–{f1} | **{name}** — `{source}` {src}–{end} | {why} |')
 chap.append(dict(name=name,out_in=f0,out_out=f1,source=source,source_in=src,source_out=end,fps=60))
foot='''

The cold open intentionally quotes the later hero; it is the sole repeated action. The complete triple is protected as one take. Clover source 100–1079 is continuous across its three editorial shot entries. No freeze, looping clip, time warp, invulnerability or state/velocity writes were introduced. Corkscrew and separate end-card footage use disclosed positioned entries; cold EHZ openings and Clover are direct act loads. They do not imply uninterrupted EHZ-to-Clover progression.

Sources are silent. One uninterrupted ROM EHZ 2P bed owns the music; B5 on comparison entry, C3 on the title and BC before Clover are editorial punctuation. `promo_kit.mix()` applies its default preview mix processing; no final mastering or loudness approval is claimed. The end-card source is separate from the continuous Clover route.

Native A–Z extraction succeeded, including X. `scripts/ExtractTitleFont.java` uses the supplied ROM, production Nemesis decompressor, `TitleCardManager` offset/size tables and column-major sprite tile order. E/N/O/Z come from the base title-card art. `design/rom-title-font/s2-title-font.txt` is the extracted local bitmap alphabet. No system font imitates the title face. Practical URL/status/disclaimer use the installed Fira Sans Condensed Bold Italic; font-role checks report no fallbacks.

No Clover card repair is planned. The former corrupt-card take remains historical evidence; none of it is selected. Current Clover capture uses `mods.skipModZoneTitleCards: true`, no `--title-card`, and only native controller inputs. Earlier plans that demanded a native Clover card are superseded.
'''
(P/'BEAT_SHEET_REVISED.md').write_text(head+'\n'.join(lines)+foot)
(P/'chapters.json').write_text(json.dumps(chap,indent=2)+'\n')
print(e.pacing()[0]);print('warnings',e.check())
