#!/usr/bin/env python3
"""Local Emerald Remix promo revision assets, 2026-10-22.
Inputs: native card frame, palette-index alphabet, captured world strip, actual Clover pixel function.
Editorial assembly/scan graphics only; never gameplay or editor UI. No repository writes.
"""
import csv,json,importlib.util
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];R=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
D=P/'design/revision';D.mkdir(exist_ok=True)
palette={'1':(0,0,0),'6':(255,255,255),'7':(182,182,182),'8':(146,146,146)}
# Palette values measured in the stock card; confirm each index against a full native E/M glyph.
font={};name=None
for line in (P/'design/rom-title-font/s2-title-font.txt').read_text().splitlines():
 if line.startswith('= '):name=line[2];font[name]=[]
 elif line:font[name].append(line)
ref=np.array(Image.open(P/'captures/stock-titlecard-reference/frames/00062.png').convert('RGB'))
for ch,g in font.items():
 rgba=np.array([[(*palette[v],255) if v!='.' else (0,0,0,0) for v in row] for row in g],dtype=np.uint8)
 Image.fromarray(rgba).save(P/f'design/rom-title-font/{ch}.png')
for ch in ['E','M','R','A','L','D','H','I']:
 g=font[ch];a=np.array([[palette.get(v,(48,87,206)) for v in row] for row in g],dtype=np.uint8)
 matches=[]
 for y in range(54,59):
  for x in range(110,315-a.shape[1]+1):
   mask=np.array([[v!='.' for v in row] for row in g])
   if np.array_equal(ref[y:y+16,x:x+a.shape[1]][mask],a[mask]):matches.append([x,y])
 assert matches,(ch,'no palette-exact native match')
 print('native palette-exact match',ch,matches[0])
(D/'type-sampling.json').write_text(json.dumps({'reference':'captures/stock-titlecard-reference/frames/00062.png','palette_indices':palette,'native_black_shadow_offset':[2,2],'additional_outline':False,'additional_drop':False},indent=2)+'\n')
# World-aligned extraction avoids the centred actor/HUD, using far-right columns of real frames.
rows=list(csv.DictReader((P/'captures/remix-tumble-wide-final/state.csv').open()))
imgs={};out=Image.new('RGB',(1152,192))
for xx in range(1152):
 wx=4096+xx
 row=min((r for r in rows if 0<=wx-int(r['cam_x'])<800 and not 240<=wx-int(r['cam_x'])<=365 and 480<=int(r['cam_y'])<=512 and abs(wx-int(r['x']))>45),key=lambda r:abs(wx-int(r['cam_x'])-680))
 f=int(row['frame']);cx=int(row['cam_x']);cy=int(row['cam_y'])
 if f not in imgs:imgs[f]=Image.open(P/f'captures/remix-tumble-wide-final/frames/{f:05d}.png').convert('RGB')
 out.paste(imgs[f].crop((wx-cx,512-cy,wx-cx+1,704-cy)),(xx,0))
out.save(D/'rom-triple-strip.png')
# Keep the two large connected track components in the native orange/brown art palette.
# This removes the moving background and detached HUD/ring fragments from the editorial strip assembly.
a=np.array(out);soil=[(36,0,0),(109,36,0),(146,73,0),(219,109,0),(255,146,0),(255,182,0)]
mask=np.zeros(a.shape[:2],bool)
for colour in soil:mask|=np.all(a==colour,axis=2)
seen=np.zeros_like(mask);best=[];components=[]
for y,x in zip(*np.where(mask)):
 if seen[y,x]:continue
 stack=[(y,x)];seen[y,x]=True;component=[]
 while stack:
  yy,xx=stack.pop();component.append((yy,xx))
  for ny,nx in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
   if 0<=ny<192 and 0<=nx<1152 and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;stack.append((ny,nx))
 components.append(component)
 if len(component)>len(best):best=component
alpha=np.zeros(mask.shape,np.uint8)
print("ROM art component sizes",sorted([len(q) for q in components],reverse=True)[:12])
for comp in components:
 if len(comp)>5000:
  for y,x in comp:alpha[y,x]=255
Image.fromarray(np.dstack([a,alpha])).save(D/'rom-triple-art.png')
# Exact generator decoration, not a redrawn approximation.
spec=importlib.util.spec_from_file_location('cv',R/'examples/emerald-remix/tools/generate_clover_valley.py');cv=importlib.util.module_from_spec(spec);spec.loader.exec_module(cv)
def rgb(word):return tuple(round(((word>>shift)&14)/14*255) for shift in (0,4,8))
for kind in ['clover','flower']:
 im=Image.new('RGBA',(16,16))
 for y in range(16):
  for x in range(16):
   i=cv.decor_pixel(kind,x,y)
   if i:im.putpixel((x,y),(*rgb(cv.LINE2[i]),255))
 im.save(D/(kind+'-pixel-function.png'))
print('prepared native type, actual ROM strip and generator art',D)
