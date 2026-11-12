from pathlib import Path
import subprocess,json
P=Path(__file__).parent
for name,aspect in [('wide','16x9'),('vertical','9x16')]:
 video=P/'out'/f'rough-{aspect}.mp4';raw=P/'edit'/name/'unmastered.mp4'
 if not raw.exists():video.replace(raw)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-c:v','copy','-af','volume=-4dB','-c:a','aac','-b:a','192k','-movflags','+faststart',str(video)],check=True)
 for label,args in [('loudness',['-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']),('decode',['-v','error','-xerror','-i',str(video),'-f','null','-'])]:
  with open(P/'out'/f'{name}-{label}.log','w')as f:subprocess.run(['ffmpeg',*args],stdout=f,stderr=subprocess.STDOUT,check=True)
 with open(P/'out'/f'{name}-ffprobe.json','w')as f:subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],stdout=f,check=True)
