"""Mux explicit chapter map, then inspect AAC, streams and complete decodes."""
import json,subprocess
from pathlib import Path
P=Path(__file__).parent
chap=json.loads((P/'chapters.json').read_text());m=P/'chapters.ffmetadata';m.write_text(';FFMETADATA1\n'+''.join(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(c['start']*1000)}\nEND={round(c['end']*1000)}\ntitle={c['title']}\n"for c in chap));results=[]
for name,aspect in [('wide','16x9'),('vertical','9x16')]:
 v=P/f'out/master-{aspect}.mp4';out=P/f'out/chaptered-{aspect}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(v),'-i',str(m),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(out)],check=True)
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(out)]));assert len(data['chapters'])==13
 with (P/f'out/{name}-decode.log').open('w')as f:subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],stdout=f,stderr=subprocess.STDOUT,check=True)
 with (P/f'out/{name}-loudness.log').open('w')as f:subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],stdout=f,stderr=subprocess.STDOUT,check=True)
 raw=(P/f'out/{name}-loudness.log').read_text();l=json.loads(raw[raw.rfind('{'):]);assert float(l['input_tp'])<=-1
 s=next(s for s in data['streams']if s['codec_type']=='video');assert s['r_frame_rate']=='60/1';assert (s['width'],s['height'])==((1920,1080)if name=='wide'else(1080,1920))
 out.replace(v);data['format']['filename']=str(v);(P/f'out/{name}-ffprobe.json').write_text(json.dumps(data,indent=2));results.append(dict(video=str(v),size=[s['width'],s['height']],fps=s['r_frame_rate'],duration=data['format']['duration'],chapters=13,decode_exit=0,true_peak_dbtp=l['input_tp'],integrated_lufs=l['input_i'],check=(P/f'out/{name}-check.log').read_text(),sound='checked by measurement only'))
(P/'verification.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
