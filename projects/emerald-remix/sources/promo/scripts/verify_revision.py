#!/usr/bin/env python3
"""Verify the Emerald Remix round5 rough exports, 2026-10-22.
Inputs: instantiated edit, preview ranges, encoded MP4s. Probe/decode and syntax checks;
this is bounded media validation, not gameplay parity or a final mastering approval.
"""
import ast,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
e=pk.load_edit(P/'edit.py');assert e.check()==[],e.check()
assert e.end()==2501
for p in [P/'edit.py',*(P/'scripts').glob('*.py')]:ast.parse(p.read_text(),filename=str(p))
print('syntax: edit.py and all scripts/*.py passed')
print('check:',e.check());print('pacing:',e.pacing()[0])
ranges=json.loads((P/'previews/ranges.json').read_text())
exports=[(P/'out/emerald-remix-rough.mp4',2501)]+[(P/f'previews/{name}.mp4',r['out']-r['in']) for name,r in ranges.items()]
for path,n in exports:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
 v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'60/1',n),(path,v)
 assert (int(a['sample_rate']),int(a['channels']))==(48000,2)
 assert abs(float(probe['format']['duration'])-n/60)<.06
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 print(path.relative_to(P),'frames=',n,'duration=',probe['format']['duration'],'1080p60 stereo48k probe/decode PASS',flush=True)
q=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(P/'out/emerald-remix-rough.mp4'),'-af','ebur128=peak=true','-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
print('Encoded AAC measurement (rough mix, no mastering change):\n'+q.stderr[q.stderr.rfind('Summary:'):])
