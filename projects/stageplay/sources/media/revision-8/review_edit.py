#!/usr/bin/env python3
"""Render bounded cut and action review sheets for Stageplay revision eight.
Input: candidate directory with tutorial.mp4 and chapters.json. Stills supplement motion review.
"""
import argparse,json,subprocess,io
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('candidate',type=Path);a=p.parse_args();r=a.candidate
edl=json.loads((r/'chapters.json').read_text());v=r/'tutorial.mp4'
def frame(n):
 data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(n/60),'-i',str(v),'-frames:v','1','-f','image2pipe','-vcodec','png','-threads','1','-'])
 return Image.open(io.BytesIO(data)).convert('RGB')
frames=[0]
for s in edl[1:]:frames.extend([s['startFrame']-1,s['startFrame']])
frames.append(edl[-1]['endFrame']-1)
im=Image.new('RGB',(1920,((len(frames)+3)//4)*292),'#102238');d=ImageDraw.Draw(im)
for i,n in enumerate(frames):
 x=(i%4)*480;y=(i//4)*292;im.paste(frame(n).resize((480,270)),(x,y+22));d.text((x+4,y+4),f'frame {n} / {n/60:.3f}s',fill='white')
im.save(r/'review-cuts.png')
for name,n in [('story',980),('count',1140),('count-lesson',3060),('lesson',2350),('comparison',3820),('endcard',4200)]:frame(n).save(r/('review-'+name+'.png'))
print('Cut boundaries and five full-size action/layout frames written.')
