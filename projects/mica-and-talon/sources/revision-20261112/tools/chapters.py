"""Purpose: write chapters.txt (human) and chapters.ffmeta (ffmpeg) from the edit's tracked bar layout.
Origin: MICA & TALON promo redo 2026-11-12."""
import json
from pathlib import Path
T=Path(__file__).resolve().parent.parent
BT=[b['t'] for b in json.load(open(T/'work/beat-track.json'))['bars']]
bf=lambda n:int(round((BT[int(n)]+(BT[int(n)+1]-BT[int(n)])*(n-int(n)))*60))
END=bf(88)+36
CH=[('Cold open: roll-in, partners, the carry',0,10),('Title drop: Sonic 2 title',10,14),('MICA: homing strike',14,28),
    ('TALON: flight and divebomb',28,36),('Every screen, redrawn',36,52),('At speed',52,58.5),('Powered up: Gilded and Solar',58.5,75.25),
    ('Hyper MICA: one hit',75.25,80),('Together, powered',80,84),('End card',84,None)]
txt=[];meta=[';FFMETADATA1','title=MICA & TALON - an example character mod for OpenGGF']
for name,a,b in CH:
  f0=0 if a==0 else bf(a);f1=END if b is None else bf(b)
  txt.append(f'{f0/60:6.2f}-{f1/60:6.2f}  {name}')
  meta+=['[CHAPTER]','TIMEBASE=1/60',f'START={f0}',f'END={f1}',f'title={name}']
(T/'out').mkdir(exist_ok=True)
(T/'out/chapters.txt').write_text('\n'.join(txt)+'\n');(T/'work/chapters.ffmeta').write_text('\n'.join(meta)+'\n')
print('\n'.join(txt))
