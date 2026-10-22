#!/usr/bin/env python3
"""Build bounded review grids at lesson cuts and the corrected return-jump apex.
Origin: Stageplay tutorial, 2026-10-22. Inputs: final movie and chapters.json.
Stills supplement full-rate playback; they cannot certify motion or audio quality.
"""
import argparse,io,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args();r=a.root
movie=r/'stageplay-first-scene-tutorial.mp4'
def frame(t):
 return Image.open(io.BytesIO(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(movie),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])))
def sheet(name,times,w=640):
 h=w*1120//1600;out=Image.new('RGB',(w*2,(h+24)*((len(times)+1)//2)), '#091521');d=ImageDraw.Draw(out)
 for i,t in enumerate(times):
  x=i%2*w;y=i//2*(h+24);out.paste(frame(t).resize((w,h)),(x,y+24));d.text((x+8,y+6),f'{t:.3f}s',fill='yellow')
 out.save(r/name)
chapters=json.loads((r/'chapters.json').read_text());cuts=[c['startFrame']/60 for c in chapters[1:]]
sheet('review-cuts.png',[t+delta for t in cuts for delta in [-1/60,1/60]])
sheet('review-apex.png',[90+f/60 for f in [655,661,676,687,700,712,728,744]],800)
sheet('tutorial-review.png',[2,10,22,34,46,57,70,81],800)
