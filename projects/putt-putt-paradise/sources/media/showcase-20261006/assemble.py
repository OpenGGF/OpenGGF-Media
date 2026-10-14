"""Reproduce the 2026-10-06 golf highlight edit from retained ROM-backed captures."""
from pathlib import Path
import subprocess,json,csv
root=Path(__file__).resolve().parent
edit=json.loads((root/'edit-list.json').read_text())
work=root/'encoding';work.mkdir(exist_ok=True)
parts=[]
chapters=[';FFMETADATA1','title=Putt Putt Paradise — Sonic 2 Mini Golf','comment=Authentic ROM-backed gameplay, normal speed, silent; see source archive and edit list.']
for c in edit['clips']:
 source=root/c['source']
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)],text=True))
 stream=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert stream['width']==320 and stream['height']==224 and stream['r_frame_rate']=='30/1'
 assert c['source_frame_start']>=0 and c['source_frame_end_exclusive']<=round(float(probe['format']['duration'])*30)
 label=work/('%02d.txt'%c['order']);label.write_text(c['title'])
 out=work/('%02d.mkv'%c['order'])
 out.unlink(missing_ok=True)
 vf=(f"trim=start_frame={c['source_frame_start']}:end_frame={c['source_frame_end_exclusive']},setpts=PTS-STARTPTS,"
     f"scale=960:672:flags=neighbor,pad=1280:720:160:48:color=0x071425,"
     f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:textfile={label}:fontcolor=0xf5e9bb:fontsize=25:x=(w-text_w)/2:y=11")
 subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(source),'-vf',vf,'-an','-c:v','ffv1','-level','3','-pix_fmt','bgr0','-threads','2',str(out)],check=True)
 parts.append(out)
 chapters.extend(['[CHAPTER]','TIMEBASE=1/30',f"START={c['reel_frame_start']}",f"END={c['reel_frame_end_exclusive']}",'title='+c['title']])
 print('Normalized '+c['title'],flush=True)
manifest=work/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in parts))
meta=work/'chapters.ffmeta';meta.write_text('\n'.join(chapters)+'\n')
reel=root/'putt-putt-paradise-highlights-new.mp4'
subprocess.run(['ffmpeg','-v','error','-nostdin','-f','concat','-safe','0','-i',str(manifest),'-i',str(meta),'-map','0:v:0','-map_metadata','1','-map_chapters','1','-an','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(reel)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(reel)],text=True))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert video['width']==1280 and video['height']==720 and video['avg_frame_rate']=='30/1'
assert int(video['nb_frames'])==edit['total_frames'] and len(probe['chapters'])==len(edit['clips'])
assert abs(float(probe['format']['duration'])-edit['total_frames']/30)<0.04
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(reel),'-f','null','-'],check=True)
(root/'reel-probe.json').write_text(json.dumps(probe,indent=2)+'\n')
with (root/'chapters.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['order','act','reel_start','reel_end','source','source_start','source_end','title'])
 for c in edit['clips']:w.writerow([c['order'],c['act'],c['reel_frame_start']/30,c['reel_frame_end_exclusive']/30,c['source'],c['start_seconds'],c['end_seconds'],c['title']])
reel.replace(root/'putt-putt-paradise-highlights.mp4')
print('Verified '+str(root/'putt-putt-paradise-highlights.mp4')+'; '+str(edit['total_frames']/30)+' seconds',flush=True)
