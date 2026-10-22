#!/usr/bin/env python3
"""Review native contact/arc frames. Origin: Stageplay revision eight.
Inputs: take-3 movies. Stills do not replace the parent's full-motion review.
"""
import io,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent

def frame(name,f):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(root/'take-3'/f'{name}.mkv'),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-f','image2pipe','-vcodec','png','-threads','1','-'])
 return Image.open(io.BytesIO(data)).convert('RGB')
items=[('story',f) for f in [15,160,271,293,400,550,688,728,1140,1165,1204,1362,1560,1800,2039]]
canvas=Image.new('RGB',(640*3,480*5),'#142333');d=ImageDraw.Draw(canvas)
for i,(name,f) in enumerate(items):
 x=(i%3)*640;y=(i//3)*480;canvas.paste(frame(name,f),(x,y+25));d.text((x+8,y+6),f'{name} | native frame {f}',fill='#fff4d3')
canvas.save(root/'review-contact-arcs.png')
canvas=Image.new('RGB',(1280,480*3),'#142333');d=ImageDraw.Draw(canvas)
for row,f in enumerate([267,271,285]):
 for col,name in enumerate(['clean-sfx','comparison-hold8']):
  x=640*col;y=480*row;canvas.paste(frame(name,f),(x,y+25));d.text((x+8,y+6),f'{name} | same source frame {f}',fill='#fff4d3')
canvas.save(root/'review-comparison.png')
