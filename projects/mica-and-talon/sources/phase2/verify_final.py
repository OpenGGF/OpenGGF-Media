from pathlib import Path
import subprocess,json,os
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-66af4c18');env=os.environ.copy();env.update(MT_CHECKOUT=str(R),MT_TAKE='phase2',PROMO_FONT_DIRS=str(P/'fonts'))
summary=[]
for name,aspect in [('wide','16x9'),('vertical','9x16')]:
 v=P/f'out/master-{aspect}.mp4';env['MT_VERTICAL']='1'if name=='vertical'else'0'
 with (P/f'out/{name}-check.log').open('w')as f:subprocess.run([str(P/'venv/bin/python'),str(R/'tools/media/promo_kit.py'),'check',str(P/'edit/edit.py')],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 for label,args in [('loudness',['-hide_banner','-i',str(v),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']),('decode',['-v','error','-xerror','-i',str(v),'-f','null','-'])]:
  if (P/f'out/{name}-{label}.log').exists() and (P/f'out/{name}-{label}.log').stat().st_mtime > v.stat().st_mtime:continue
  with (P/f'out/{name}-{label}.log').open('w')as f:subprocess.run(['ffmpeg',*args],stdout=f,stderr=subprocess.STDOUT,check=True)
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));(P/f'out/{name}-ffprobe.json').write_text(json.dumps(data,indent=2))
 loud=(P/f'out/{name}-loudness.log').read_text();l=json.JSONDecoder().raw_decode(loud[loud.rfind('{'):])[0];assert float(l['input_tp']) < -1, l
 s=next(s for s in data['streams']if s['codec_type']=='video');assert s['r_frame_rate']=='60/1';assert s['width']==(1920 if name=='wide' else 1080)
 summary.append(dict(video=str(v),size=[s['width'],s['height']],fps=s['r_frame_rate'],duration=data['format']['duration'],input_i=l['input_i'],true_peak_dbtp=l['input_tp'],decode_exit=0,check=(P/f'out/{name}-check.log').read_text()))
(P/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
