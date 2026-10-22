#!/usr/bin/env python3
"""Verify the bounded native scene and publish measured evidence, not parity claims.
Origin: approved Stageplay revision eight. Inputs: take-3 sources/simulations,
direct_scene.py. No engine logs or pass caches are retained.
"""
import importlib.util,json
from pathlib import Path
root=Path(__file__).resolve().parent;take=root/'take-3'
def rows(name):return [json.loads(x) for x in (take/f'{name}.jsonl').open()]
def write(name,value): (root/name).write_text(json.dumps(value,indent=2)+'\n')
a=rows('story');assert len(a)==2040
for name in ['clean','story-sfx','clean-sfx']:
 b=rows(name);assert len(b)==len(a)
 for x,y in zip(a,b):
  for key in ['world','actors','camera','puppets']:
   assert x['sample'][key]==y['sample'][key],(name,x['frame'],key)
changes=[];last={};mins={'bodyToPanel':999,'bodyToViewport':999,'supportToPanel':999};dialogue={}
for row in a:
 f=row['frame'];s=row['sample'];cam=s['camera'];assert cam['zoom']==1
 for w in s['world']['actors']:
  assert not(w['hurt'] or w['dead']),(f,w)
  if last.get(w['actorId'])!=w['ridingLayoutIndex']:
   changes.append([f,w['actorId'],w['ridingLayoutIndex']]);last[w['actorId']]=w['ridingLayoutIndex']
 assert not any('TIMED_OUT' in str(e) for e in s['world']['events']),f
 for actor in s['actors']:
  x=actor['x']-cam['x'];y=actor['y']-cam['y'];radius=20 if actor['actorId']=='sonic' else 24
  clearance=min(x-radius,320-x-radius,y-radius,224-y-radius)
  mins['bodyToViewport']=min(mins['bodyToViewport'],clearance);assert clearance>=0,(f,actor)
  for d in s['dialogue']:
   cue=d['cue'];gap=y-radius-(cue['y']+cue['height']);mins['bodyToPanel']=min(mins['bodyToPanel'],gap);assert gap>0,(f,actor,d)
 for d in s['dialogue']:
  cue=d['cue'];record=dialogue.setdefault(cue['id'],dict(startFrame=cue['startFrame'],endFrame=cue['endFrame'],speaker=d['speakerName'],text=cue['text'],panel=dict(x=cue['x'],y=cue['y'],width=cue['width'],height=cue['height'])))
  if d['visibleText']==cue['text']:record.setdefault('fullyRevealedFrame',f)
  for obj in s['world']['objects']:
   if obj['layoutIndex'] in [166,179]:
    gap=obj['y']-cam['y']-16-(cue['y']+cue['height']);mins['supportToPanel']=min(mins['supportToPanel'],gap);assert gap>0,(f,obj)
expected=[[0,'sonic',-1],[0,'tails',-1],[15,'sonic',179],[16,'tails',179],[241,'sonic',-1],[293,'sonic',166],[661,'sonic',-1],[728,'sonic',179],[1141,'sonic',-1],[1146,'tails',-1],[1199,'sonic',166],[1204,'tails',166]]
assert changes==expected,changes
assert dialogue['together.dialogue6']['fullyRevealedFrame']==1140
for f in range(535,580):assert a[f]['sample']['world']['actors'][0]['animation']==8
for f in range(390,480):assert a[f]['sample']['world']['actors'][1]['animation']==7
b=rows('comparison-hold8');assert len(b)==2040

def diff(x,y,path=''):
 if isinstance(x,dict):return sum([diff(x[k],y[k],path+'/'+str(k)) for k in x],[])
 if isinstance(x,list):return sum([diff(v,w,path+'/'+str(i)) for i,(v,w) in enumerate(zip(x,y))],[])
 return [] if x==y else [dict(path=path,before=x,after=y)]
source=json.loads((take/'clean-sfx.screenplay.json').read_text());other=json.loads((take/'comparison-hold8.screenplay.json').read_text());difference=diff(source,other)
assert len(difference)==1 and difference[0]['before']==20 and difference[0]['after']==8,difference
metrics={}
for name,r in [('hold20',a),('hold8',b)]:
 for row in r:
  for actor in row['sample']['world']['actors']:assert not(actor['hurt'] or actor['dead'])
  assert not any('TIMED_OUT' in str(e) for e in row['sample']['world']['events'])
 apex=min((row['sample']['actors'][0]['y'],row['frame']) for row in r[241:294])
 landing=next(row['frame'] for row in r[242:] if row['sample']['world']['actors'][0]['ridingLayoutIndex']==166)
 metrics[name]=dict(apexY=apex[0],apexFrame=apex[1],landingFrame=landing)
assert metrics['hold8']['landingFrame']==285
comparison=dict(change=difference[0],sourceInterval=dict(startFrame=180,endFrame=450,endExclusive=True),outcome=metrics,apexHeightDifferencePixels=metrics['hold8']['apexY']-metrics['hold20']['apexY'],landingEarlierFrames=8,interpretation='Both land on placement 166 safely. Shorter hold makes a lower arc and lands eight frames earlier. Same native approach/camera rules; no pathfinding claim.')
platformY=[]
for row in a[1560:]:
 s=row['sample'];assert all(v['ridingLayoutIndex']==166 for v in s['world']['actors'])
 platformY.append(next(o['y'] for o in s['world']['objects'] if o['layoutIndex']==166))
assert max(platformY)>min(platformY)
spec=importlib.util.spec_from_file_location('director',root/'direct_scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for name,value in m.takes().items():assert json.loads((take/f'{name}.screenplay.json').read_text())==value
report=dict(storyFrames=1560,totalFrames=2040,worldPolicy='LIVE',platformChanges=changes,dialogue=list(dialogue.values()),countThreeBeginsFrame=1135,reactions=dict(sonicCrouch=[535,580],tailsLookUp=[390,480],intervalsEndExclusive=True),tail=dict(startFrame=1560,endFrame=2040,platform=166,platformYRange=[min(platformY),max(platformY)]),deaths=0,hurt=0,waitTimeouts=0,allFrameWorldActorPuppetCameraEquivalentVariants=['story','clean','story-sfx','clean-sfx'],geometryClearancesPixels=mins,geometryMethod='Every-frame actor centre envelopes: Sonic +/-20, Tails +/-24; support +/-16 vertically; panel rectangles. Positive gaps establish conservative body/panel separation, not exact accessory/pointer pixel masks. Selected rendered contact/apex reviews supplement this check.',comparison=comparison,generatorMatchesAllSixSources=True,limits='Authored initial placements and native inputs. Bounded LIVE route observation; not general pathfinding, cold level completion, ROM parity, engine-suite coverage, full-motion human review or physical audio listening.')
write('scene-checks.json',report);print(json.dumps(report))
