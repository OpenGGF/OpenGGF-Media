#!/usr/bin/env python3
"""SOZ v2 curated moving-gameplay reel, 2026-09-16 user editorial correction.
Inputs: cold-route captures and corrected priority-pass boss captures. Output: chronological Act 1 then Act 2 excerpts.
No stills, repeated test variants, speed changes, or source modifications.
"""
from pathlib import Path
import csv,json,subprocess,shutil
R=Path(__file__).resolve().parent
B=R/'.curated-build'; B.mkdir(exist_ok=True)
SCENES=[
(1,20,14,'Desert parallax and heat shimmer'),
(1,84,10,'Desert enemies and ruins'),
(1,115,10,'Sandfalls and spikes'),
(1,172,12,'Moving platforms'),
(1,266,12,'Crossing the ruins'),
(1,294,14,'Swinging across the desert'),
(1,326,12,'The final ascent'),
(1,382,13,'Egg Golem'),
(1,413,13,'Egg Golem defeat'),
(1,437,8.2,'Entering the pyramid'),
(2,24,12,'Inside the temple'),
(2,52,12,'Releasing the ghosts'),
(2,84,14,'Darkness and pursuit'),
(2,142,14,'Wire traversal'),
(2,174,12,'Light switches'),
(2,204,12,'Rising sand'),
(2,324,14,'Temple mechanisms'),
(2,356,12,'Rock platforms'),
(2,465,12,'The final approach'),
(2,502,20,'Eggman and the final hits'),
(2,522,4,'Victory and rescue'),
(2,536,4.5,'Into Lava Reef'),
]
rows=[];elapsed=0
for n,(act,start,duration,title) in enumerate(SCENES):
 folder='native-320-final' if act==1 else 'act2-native-320-final'
 source=R/'completion-cold-route'/folder/'capture.mp4'
 wide=n in (6,7,8,9)
 if wide:
  source=R/'pyramid-presentation/final/capture.mp4'
  start={6:1,7:24,8:50,9:80}[n]
  if n==6: title="The pyramid rises"
  if n==7: title='Egg Golem — widescreen arena'
 if n in (19,20,21):
  source=R/'playtest-followup/act2-boss/capture.mp4'
  start={19:2,20:22,21:46.3}[n]
 if n==18:
  source=R/'playtest-followup/checkpoint-shortcut-shell/capture.mp4'
  start=8
  title='Checkpoint approach and boss-room entry'
 if n==15:
  source=R/'priority-pass/complete/act2-mechanisms/lower/capture.mp4'
  start=16
 label=B/f'{n:02}.txt';label.write_text(f'ACT {act}  /  {title}')
 segment=B/f'scene-{n:02}.mp4'
 vf=f"scale=1280:896:flags=neighbor,pad=1920:1080:320:160:black,setsar=1,drawtext=textfile={label}:fontcolor=white:fontsize=38:x=320:y=60,fps=60"
 if wide:
  vf=f"scale=1600:448:flags=neighbor,pad=1920:1080:160:320:black,setsar=1,drawtext=textfile={label}:fontcolor=white:fontsize=38:x=160:y=200,fps=60"
 if n in (15,18):
  vf=f"scale=1600:896:flags=neighbor,pad=1920:1080:160:160:black,setsar=1,drawtext=textfile={label}:fontcolor=white:fontsize=38:x=160:y=60,fps=60"
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(source),'-t',str(duration),'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','8','-bf','0','-refs','3','-pix_fmt','yuv420p','-video_track_timescale','60000',str(segment)],check=True)
 rows.append((elapsed,elapsed+duration,str(source.relative_to(R)),start,start+duration,f'Act {act} - {title}'))
 elapsed+=duration
 print(f'{n+1}/{len(SCENES)}: Act {act} - {title}',flush=True)
manifest=B/'concat.txt';manifest.write_text(''.join(f"file '{B/f'scene-{n:02}.mp4'}'\n" for n in range(len(SCENES))))
meta=B/'chapters.txt';meta.write_text(';FFMETADATA1\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(a*1000)}\nEND={round(b*1000)}\ntitle={title}\n' for a,b,_,_,_,title in rows))
output=R/'SOZ-work-highlights.new.mp4'
# One encode ensures a single H.264 configuration for reliable chapter seeking.
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-i',str(meta),'-map','0:v','-map_metadata','1','-map_chapters','1','-an','-c:v','libx264','-preset','veryfast','-crf','16','-threads','8','-bf','0','-refs','3','-r','60','-fps_mode','cfr','-pix_fmt','yuv420p','-video_track_timescale','60000','-movflags','+faststart',str(output)],check=True)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
with (R/'highlights-chapters.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['start_seconds','end_seconds','source','source_start_seconds','source_end_seconds','title']);w.writerows(rows)
print(json.dumps({'duration':elapsed,'chapters':len(rows),'output':str(output)}),flush=True)

output.replace(R/'SOZ-work-highlights.mp4')
shutil.rmtree(B)
