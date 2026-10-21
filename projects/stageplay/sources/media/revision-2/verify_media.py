#!/usr/bin/env python3
"""Inspect the exact Stageplay edit's continuous decoded motion, audio and every cut.
Inputs: source/reel and chapters under a relocated production root, FFmpeg, Pillow.
Origin: Stageplay production, 2026-10-21. Numerical checks supplement visual review.
"""
import array,json,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageStat

root=Path(__file__).resolve().parent
chapters=json.loads((root/'chapters.json').read_text()); review=root/'review';review.mkdir(exist_ok=True)
reel=root/'stageplay-promo.mp4'
times=[c['output_start_seconds'] for c in chapters[1:]]
canvas=Image.new('RGB',(1920,len(times)*160),'#101827');draw=ImageDraw.Draw(canvas)
for row,t in enumerate(times):
 for col,delta in enumerate([-.3,-.15,-1/60,1/60,.15,.3,.5,.8]):
  png=review/f'cut{row}-{col}.png'
  subprocess.run(['ffmpeg','-v','error','-ss',str(t+delta),'-i',str(reel),'-frames:v','1','-y',str(png)],check=True)
  im=Image.open(png).resize((240,135),Image.Resampling.NEAREST)
  canvas.paste(im,(col*240,row*160+22));draw.text((col*240+4,row*160+5),f'{t+delta:.3f}s',fill='white')
canvas.save(review/'cuts-complete.png')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(reel),'-vf','scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-'])
size=160*90*3;count=len(raw)//size
assert count==1767 and len(raw)%size==0
motion=[]
for c in chapters:
 a,b=c['output_start_frame'],c['output_end_frame'];deltas=[]
 prior=Image.frombytes('RGB',(160,90),raw[a*size:(a+1)*size])
 for i in range(a+1,b):
  current=Image.frombytes('RGB',(160,90),raw[i*size:(i+1)*size])
  deltas.append(sum(ImageStat.Stat(ImageChops.difference(current,prior)).mean)/3);prior=current
 motion.append(dict(title=c['title'],frames=b-a,changedFrames=sum(d>.05 for d in deltas),maxMeanDelta=max(deltas)))
 assert any(d>.05 for d in deltas)
audio=array.array('f',subprocess.check_output(['ffmpeg','-v','error','-i',str(reel),'-map','0:a:0','-f','f32le','-']))
result=dict(frames=count,motion=motion,audioPeak=max(abs(x) for x in audio),audioRms=(sum(x*x for x in audio)/len(audio))**.5,audioSamplesPerChannel=len(audio)//2)
source=root/'take-2/location-remote.mkv'
source_audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-map','0:a:0','-f','s16le','-'])
assert len(source_audio)//4==2760*800
result['losslessSourceAudioSamplesPerChannel']=len(source_audio)//4
for file in [source,root/'location-remote.mp4',reel]:
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(file),'-f','null','-'],check=True)
result['fullDecodes']=['take-2/location-remote.mkv','location-remote.mp4','stageplay-promo.mp4']
(root/'decoded-media-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
