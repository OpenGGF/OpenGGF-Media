#!/usr/bin/env python3
"""One-command local rough production; rerun after capture_all.py, no server/upload."""
import argparse,subprocess,os
from pathlib import Path
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--checkout',type=Path,required=True);ap.add_argument('--take');a=ap.parse_args();env=os.environ.copy();env['PROMO_FONT_DIRS']=str(P/'fonts');env['MT_CHECKOUT']=str(a.checkout.resolve())
if a.take:env['MT_TAKE']=a.take
kit=a.checkout.resolve()/'tools/media/promo_kit.py';py=P/'venv/bin/python'
for vertical in [False,True]:
 env['MT_VERTICAL']='1'if vertical else'0';name='vertical'if vertical else'wide'
 for command in ['check','sheet','render']:
  with open(P/'out'/f'{name}-{command}.log','w')as log:
   subprocess.run([str(py),str(kit),command,str(P/'edit/edit.py')]+(['240']if command=='sheet'else[]),env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 video=P/'out'/('master-9x16.mp4'if vertical else'master-16x9.mp4')
 raw=P/'edit'/name/'unmastered.mp4';video.replace(raw)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-c:v','copy','-af','volume=-5dB','-c:a','aac','-b:a','192k','-movflags','+faststart',str(video)],check=True)
 with open(P/'out'/f'{name}-loudness.log','w')as log:subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],stdout=log,stderr=subprocess.STDOUT,check=True)
 with open(P/'out'/f'{name}-decode.log','w')as log:subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],stdout=log,stderr=subprocess.STDOUT,check=True)
 with open(P/'out'/f'{name}-ffprobe.json','w')as log:subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],stdout=log,check=True)
