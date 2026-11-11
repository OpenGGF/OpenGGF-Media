"""Purpose: write chapters.txt (human) and chapters.ffmeta (ffmpeg) from the edit's bar layout.
Origin: MICA & TALON production promo 2026-11-11."""
from pathlib import Path
T=Path(__file__).resolve().parent.parent
bf=lambda n:round(4*n*60/172.218*60)  # output frame of bar n (edit beat clock)
END=bf(67)+120
CH=[('Cold open: S3K title roll-in',0,4),('Title drop: Sonic 2 title',4,8),('Homing attack',8,20),
    ('TALON: flight, carry, divebomb',20,28),('Three games, every screen',28,45),('Powered up: Gilded and Solar',45,64),('End card',64,None)]
txt=[];meta=[';FFMETADATA1','title=MICA & TALON - an example character mod for OpenGGF']
for name,a,b in CH:
  f0=bf(a);f1=END if b is None else bf(b)
  txt.append(f'{f0/60:6.2f}-{f1/60:6.2f}  {name}')
  meta+=['[CHAPTER]','TIMEBASE=1/60',f'START={f0}',f'END={f1}',f'title={name}']
(T/'out').mkdir(exist_ok=True)
(T/'out/chapters.txt').write_text('\n'.join(txt)+'\n');(T/'work/chapters.ffmeta').write_text('\n'.join(meta)+'\n')
print('\n'.join(txt))
