#!/usr/bin/env python3
"""Dense transition review frames for Emerald Remix r5. Not a substitute for moving previews.
Actual edit frames every 4 ticks across each cut +/-28, at final cadence and unaltered sources.
"""
from pathlib import Path
import json,sys
from multiprocessing import Pool
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
if __name__=='__main__':
 e=pk.load_edit(P/'edit.py');dest=P/'previews/transition-frames';dest.mkdir(exist_ok=True)
 fs=[max(0,min(e.end()-1,s.f0+j)) for s in e.shots[1:] for j in range(-28,32,4)]
 with Pool(4,initializer=pk._init_worker,initargs=(str(P/'edit.py'),)) as pool:
  ims=list(pool.imap(pk._frame_array,fs,chunksize=4))
 for i,s in enumerate(e.shots[1:]):
  sheet=Image.new('RGB',(5*480,3*270))
  for j in range(15):
   im=Image.fromarray(ims[i*15+j]).resize((480,270),Image.Resampling.BOX)
   ImageDraw.Draw(im).text((6,4),str(fs[i*15+j]),fill='yellow',stroke_width=1,stroke_fill='black')
   sheet.paste(im,((j%5)*480,(j//5)*270))
  sheet.save(dest/f'cut-{s.f0:05d}.png')
 (dest/'ranges.json').write_text(json.dumps([{'cut':s.f0,'frames':fs[i*15:(i+1)*15]} for i,s in enumerate(e.shots[1:])],indent=2)+'\n')
 print('reviewed ranges',[(s.f0,s.f0/60) for s in e.shots[1:]],flush=True)
