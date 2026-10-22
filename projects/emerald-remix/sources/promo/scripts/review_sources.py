#!/usr/bin/env python3
"""Verify retained rough-cut source windows, state/pose and native cadence, 2026-10-22.
Inputs: actual CSV/PNG/video captures. Bounded promo evidence, no parity claim.
"""
import csv,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
PY='/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/promo-planning-venv/bin/python'
selections={'remix-tumble-hero-final':[(65,335),(103,240)],
 'remix-tumble-wide-final':[(50,321)],'stock-tumble-wide-exit02-final':[(50,321)],
 'clover-shipping-route-final':[(100,1079)]}
for name,picks in selections.items():
 d=P/'captures'/name;r=list(csv.DictReader((d/'state.csv').open()));fs=sorted((d/'frames').glob('*.png'))
 assert [int(p.stem) for p in fs]==list(range(len(r)))
 assert all(0<=a<b<=len(r) for a,b in picks)
 assert all(x['hurt']=='0' and x['dead']=='0' for a,b in picks for x in r[a:b])
 if 'tumble' in name:
  assert all(x['rolling']=='0' for x in r[80:210 if name.startswith('stock') else 273])
  assert any(95<=int(x['mapping_frame'])<=106 for x in r[80:210])
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(d/'capture.mp4')],text=True))['streams']
 assert len(v)==1 and v[0]['r_frame_rate']=='60/1' and int(v[0]['nb_frames'])==len(r)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(d/'capture.mp4'),'-f','null','-'],check=True,stderr=subprocess.PIPE)
 for a,b in picks:subprocess.run([PY,str(P/'scripts/contact_sheet.py'),str(d),str(a),str(b-1)],check=True,stdout=subprocess.DEVNULL)
 result={'status':'retained rough-cut source','windows_end_exclusive':picks,'frames':len(r),'hurt_dead_in_windows':0,'fps':60,'decode':'passed'}
 (d/'source-review.json').write_text(json.dumps(result,indent=2)+'\n');print(name,result)
