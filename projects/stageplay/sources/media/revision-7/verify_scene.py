#!/usr/bin/env python3
"""Check the tutorial's actual native outcome and reproducible authored inputs.
Origin: Stageplay first-creator tutorial, 2026-10-22. Inputs: generated scene JSONL,
clean-view JSONL and the scene generator. No ROM parity or editor interaction claim.
"""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args();r=a.root
rows=[json.loads(l) for l in (r/'wait-for-me.jsonl').open()];clean=[json.loads(l) for l in (r/'directing-view.jsonl').open()]
assert len(rows)==len(clean)==1560
changes=[];last={};timeouts=[];outside=[]
for j,c in zip(rows,clean):
 f=j['frame'];s=j['sample'];cs=c['sample']
 assert (s['world'],s['actors'],s['camera'])==(cs['world'],cs['actors'],cs['camera'])
 for v in s['world']['actors']:
  assert not v['dead'] and not v['hurt']
  if last.get(v['actorId'])!=v['ridingLayoutIndex']:
   changes.append([f,v['actorId'],v['ridingLayoutIndex']]);last[v['actorId']]=v['ridingLayoutIndex']
 for v in s['actors']:
  x=v['x']-s['camera']['x'];y=v['y']-s['camera']['y']
  if not (16<=x<=304 and 16<=y<=(150 if s['dialogue'] else 208)):outside.append([f,v['actorId'],x,y])
 for e in s['world']['events']:
  if 'WAIT_TIMED_OUT' in str(e):timeouts.append([f,e])
assert not timeouts and not outside,(timeouts,outside[:5])
expected=[[0,'sonic',-1],[0,'tails',-1],[15,'sonic',179],[16,'tails',179],[241,'sonic',-1],[293,'sonic',166],[661,'sonic',-1],[728,'sonic',179],[1141,'sonic',-1],[1146,'tails',-1],[1199,'sonic',166],[1204,'tails',166]]
assert changes==expected,changes
with tempfile.TemporaryDirectory() as td:
 out=Path(td)/'wait-for-me.screenplay.json'
 subprocess.run([sys.executable,str(r/'direct_scene.py'),'--out',str(out),'--variants'],check=True)
 for name in ['wait-for-me','directing-view','music-bed']:
  file=name+'.screenplay.json';assert (Path(td)/file).read_bytes()==(r/file).read_bytes(),file
report=dict(frames=1560,worldPolicy='LIVE',platformChanges=changes,deaths=0,hurt=0,waitTimeouts=0,actorCentresOutsideSafeArea=0,cleanViewMatchesNativeStateEveryFrame=True,generatorMatchesAllThreeSources=True,limits='Authored starting positions and inputs. Native route observation, not general pathfinding, a cold level completion or ROM parity.')
(r/'scene-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
