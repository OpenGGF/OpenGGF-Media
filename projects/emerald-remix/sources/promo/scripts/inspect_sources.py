#!/usr/bin/env python3
"""Read measured source states, create source sheets, verify raw clip cadence/decode.
Emerald Remix promo, 2026-10-22. This does not compose, render or approve a promo.
"""
import csv, json, subprocess, sys
from pathlib import Path
PROD=Path('/home/farrell/Videos/OGGF/emerald-remix-promo')
PYTHON=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/promo-planning-venv/bin/python')
selections={
 'remix-triple-final':[(48,588),(94,231),(48,453)],
 'stock-double-final':[(48,318)],
 'remix-opening-final':[(0,270),(160,869)],
 'stock-opening-final':[(160,869)],
 'clover-route-final':[(0,270),(270,810),(810,1215)],
 'clover-tail-final':[(30,435)]}
summary={}
for name,picks in selections.items():
 clip=PROD/'captures'/name
 rows=list(csv.DictReader((clip/'state.csv').open()))
 frames=sorted((clip/'frames').glob('*.png'))
 assert [int(f.stem) for f in frames]==list(range(len(rows))),name+' missing frame'
 assert not any(r['hurt']=='1' or r['dead']=='1' for r in rows),name+' damaged/dead'
 assert all(0<=a<b<=len(rows) for a,b in picks)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip/'capture.mp4')],text=True))
 v=probe['streams'][0]
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1200,672,'60/1',len(rows)),(name,v)
 assert len(probe['streams'])==1,name+' unexpected audio'
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(clip/'capture.mp4'),'-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 subprocess.run([str(PYTHON),str(PROD/'scripts/contact_sheet.py'),str(clip)],check=True,stdout=subprocess.DEVNULL)
 for a,b in picks:
  subprocess.run([str(PYTHON),str(PROD/'scripts/contact_sheet.py'),str(clip),str(a),str(b-1)],check=True,stdout=subprocess.DEVNULL)
 summary[name]={'frames':len(rows),'seconds':len(rows)/60,'source_png_size':[400,224],'review_mp4_size':[v['width'],v['height']],'fps':v['r_frame_rate'],'audio':'none','hurt_frames':0,'dead_frames':0,'source_picks_end_exclusive':picks,'first':rows[0],'last':rows[-1],'decode':'passed'}
 # Event measurements are descriptive: they are not assertions of ROM parity.
 if name=='clover-route-final':
  impulses=[int(r['frame']) for r in rows if 1780<int(r['x'])<1860 and int(r['yvel'])<=-2500]
  landings=[int(rows[i]['frame']) for i in range(1,len(rows)) if rows[i-1]['air']=='1' and rows[i]['air']=='0' and 2000<int(rows[i]['x'])<2300]
  summary[name]['spring_launch_candidates']=impulses
  summary[name]['upper_ledge_landings']=landings
  summary[name]['card_status']='REJECTED: native mod name glyph mapping corrupt; gameplay after f145 is clear'
 (clip/'source-review.json').write_text(json.dumps(summary[name],indent=2)+'\n')
print(json.dumps({k:{f:v[f] for f in ['frames','seconds','decode','source_picks_end_exclusive']} for k,v in summary.items()},indent=2))
