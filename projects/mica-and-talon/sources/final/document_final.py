import os,sys,json,csv
from pathlib import Path
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-bf758747');os.environ.update(MT_CHECKOUT=str(R),MT_TAKE='final',PROMO_FONT_DIRS=str(P/'fonts'));sys.path.insert(0,str(R/'tools/media'))
from promo_kit import load_edit
E=load_edit(P/'edit/edit.py');titles=['Cold open','Native title rise','Original art','Three games','Homing chain','Jade and Gilded','Talon flies','Together','Team and Solar','Every screen','Mod API','Continuous climax and results','End plate'];chap=[]
for s,t in zip(E.shots,titles):chap.append(dict(title=t,start=s.f0/60,end=s.f1/60,source=str(s.clip.path.relative_to(P))if hasattr(s,'clip')else 'edit.py custom composition'))
(P/'chapters.json').write_text(json.dumps(chap,indent=2));(P/'chapters.txt').write_text('\n'.join(f"{v['start']:06.2f}–{v['end']:06.2f} {v['title']}"for v in chap)+'\n')
rows=[]
for d in sorted((P/'captures/final').iterdir()):
 if not (d/'state.csv').exists():continue
 pr=json.loads((d/'provenance.json').read_text());rs=list(csv.DictReader((d/'state.csv').open()));rows.append(dict(take=d.name,frames=len(rs),source_kind=pr.get('source_kind',''),commit=pr['commit'],provenance=str((d/'provenance.json').relative_to(P))))
with (P/'shot-list.csv').open('w')as f:w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
p=P/'selected-shots.csv';s=p.read_text().replace('captures/phase2/','captures/final/').replace('three-games-s1,s1-run','three-games-s1,s1-safe').replace('final/s1-run/','final/s1-safe/').replace('title-background,ehz-clear,60,650,captures/final/ehz-clear/provenance.json','title-rise,title-s2-full,510,1128,captures/final/title-s2-full/provenance.json');p.write_text(s)
text=['MGZ2 reticle and airborne chain; flash into native title.','Emblem forms and MICA rises from behind it.','TALON rises beside MICA; complete native title resolves.','ORIGINAL full band; model drawing transforms into final sprite.','Drawn pose resolves into model/pose/strip process comparison.','Three process views give way to three game hosts.','MICA stays centred in three hosts; MGZ2 homing goes full screen.','Three airborne Mantis defeats; Jade/Gilded comparison opens.','Both MICA strikes centred; TALON two-host flight opens.','Wingbeats, down-lock and dive shown in two hosts.','MICA leads TALON; team footage occupies carry slot.','Team/Solar comparison; first presentation cells arrive on beats.','HUD name, spinning signpost, named results and half-pipe characters.','Blue Sphere, continue, custom save portraits and TALON pilot complete mosaic.','Actual registration types beside gameplay.','Code hands into one continuous Gilded/team EHZ take.','Badnik defeats and downhill run retain one native clock.','Native signpost resolves to MICA, then named Act 1 clear.','Results tally payoff remains in the same take.','Opaque end plate clears HUD and gives framework invitation.','Source URL, fan disclaimer and names remain readable.','Final picture and bed fade.']
(P/'viewer-pass.md').write_text('# Final viewer pass\n\nOne row per 4 seconds, both compositions. Sampled composition and source motion-frame review; no physical listening. Sound was checked by measurement only. This does not certify ROM parity or continuous cold-route completion.\n\n| Seconds | New information / reason to watch |\n|---|---|\n'+''.join(f'| {i*4}–{min(84.8,i*4+4)} | {t} |\n'for i,t in enumerate(text)))
(P/'README.md').write_text('''# MICA & TALON — final promo pass

Mod Showcase: an example built with OpenGGF's mod framework. Not a release or download announcement. Engine source a64655fe97; all selected captures rebuilt and recorded against final art. No engine commits, stash, hook bypass, ROM modifications or pushes.

## Review history and fixes

User: final art everywhere, no stock Sonic/Tails art, both aspect ratios, measurement-based sound qualification, local archive only. The earlier native-pose reference is replaced with model sheet → GPT drawing → final sprite; the boot-logo Sonic animation and stock ending photos are excluded.

Lead phase-2 review:
1. Persistent positioned/editorial strip removed; setup remains in provenance here.
2. Results-backed editorial title replaced with real S2 title, neutral capture through full MICA/TALON rise. Source frames 510 onward exclude the boot sequence. End names sit on opaque designed plate.
3. Stray tabs removed. Complete blue bands with red tab and yellow baseline enter and leave together below the HUD.
4. Jade/Gilded and flight panes follow native CSV player position within padded source viewports. Both subjects remain in their panes, including strikes.
5. End plate is fully opaque: no HUD/results show through.
6. Carry branch remained 3aac15eb45 at final selection. Team footage retained; no carry claim. This is the one open item.
7. Both splits and grids inspected; S1 switched to a cold-start shot with visible MICA, HUD cell reframed to retain full TALON name, signpost interval limited to its spin and final branded face before results cover it. Grid cells use exactly 3× native pixels; they are subject crops, not full viewports.

## Evidence and limits

Positioned starts and declared rings/emeralds are demonstrations, not legitimate continuous acquisitions. Gilded climax is one uninterrupted positioned EHZ take through combat, signpost and results. MGZ2 chain source score changes at 65,82,104 show airborne three-Mantis defeats. Half-pipe is debug positioned ROM-starpost component entry after checkpoint reset; actual native collision admits SPECIAL_STAGE. Continue and ending use debug production-provider entry; ending selects TALON piloting the plane and excludes stock photos. Ending state.csv observes the detached capture loop, not the separately bound Engine ending loop. Data Select uses declared team save slots; stock No Save tile is excluded. These shots certify selected surfaces only.

Sound was checked by measurement only. One paced DAC-enabled S3K LBZ1 bed; Giant Ring is an editorial title-slam cue at the exact picture transition. Ambiguous ring accents removed; no fabricated jump or pickup sounds. See check and AAC loudness results in verification.json. Every source is silent; no unsynced native track is mixed under the bed.

## Rebuild and relocate

Java 25, Python with numpy/Pillow, ffmpeg/ffprobe, provided fonts, user's verified ROMs, final example jar. Build `python3 examples/mica-and-talon/build.py`. `recapture.py` replays phase-2 per-shot provenance against final engine/classes and recompiles retained Java presentation hosts; keep original phase2 root available. `safe_run.py` supplies cold GHZ; `title_full.py` supplies complete title. Scripts record exact commands and jar hashes beside each capture. Relocate checkout constants, retained source root, font/music symlinks and historical GPT drawing path. No ROM/art/audio/build/environment bytes are in this archive.

Run `venv/bin/python render_all.py --checkout <engine> --take final`; it checks/sheets/renders both layouts, masters AAC, ffprobes, measures encoded true peak and fully decodes. `chapters.json`, `selected-shots.csv`, and `edit/edit.py` supply chapter map, source intervals, brief and beat sheet. Source frame sequences, artwork, fonts, PCM, packaged jar and finished reels stay external at the catalogued production root; cataloguing is not uploading. Media branch is local only for lead publication after user review.
''')
