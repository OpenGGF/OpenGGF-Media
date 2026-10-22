#!/usr/bin/env python3
"""Frame-numbered source contact sheet, not an editorial promo render; Emerald Remix 2026-10-22.
Reads each clip's measured CSV before selecting available PNGs. Optional frame range focuses action.
"""
import csv, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
clip=Path(sys.argv[1]); rows=list(csv.DictReader((clip/'state.csv').open()))
by_frame={int(r['frame']):r for r in rows}
files=sorted((clip/'frames').glob('*.png')); frames=[int(p.stem) for p in files]
lo=int(sys.argv[2]) if len(sys.argv)>2 else frames[0]
hi=int(sys.argv[3]) if len(sys.argv)>3 else frames[-1]
avail=[f for f in frames if lo<=f<=hi]
if not avail: raise SystemExit('No source frames in requested range')
n=min(32,len(avail)); picks=[avail[round(i*(len(avail)-1)/max(n-1,1))] for i in range(n)]
native_size=Image.open(files[0]).size
w,h=400,round(400*native_size[1]/native_size[0]); cellh=h+42
out=Image.new('RGB',(4*w,58+((n+3)//4)*cellh),(20,24,32)); d=ImageDraw.Draw(out)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
d.text((12,8),f'{clip.name} | native {native_size[0]}x{native_size[1]} | frames {lo}–{hi} | source contact sheet',font=font,fill='white')
d.text((12,31),'Labels are diagnostic metadata; numbered frames preserve source cadence and provenance.',font=font,fill=(180,190,200))
for i,f in enumerate(picks):
    r=by_frame[f]; x=(i%4)*w; y=58+(i//4)*cellh
    out.paste(Image.open(clip/'frames'/f'{f:05d}.png').convert('RGB').resize((w,h),Image.Resampling.BOX),(x,y))
    d.text((x+5,y+h+2),f'f{f:05d} x={r["x"]} y={r["y"]} v={r["gspeed"]} {r["mode"]}',font=font,fill='white')
    d.text((x+5,y+h+21),f'air={r["air"]} roll={r["rolling"]} rings={r["rings"]} hurt={r["hurt"]}',font=font,fill=(190,200,210))
name='contact-sheet.png' if len(sys.argv)==2 else f'contact-{lo:05d}-{hi:05d}.png'
out.save(clip/name)
print(clip/name)
print(json.dumps({'rows':len(rows),'pngs':len(frames),'picks':picks,'first':rows[0],'last':rows[-1],'hurt_frames':sum(r['hurt']=='1' for r in rows),'dead_frames':sum(r['dead']=='1' for r in rows)}))
