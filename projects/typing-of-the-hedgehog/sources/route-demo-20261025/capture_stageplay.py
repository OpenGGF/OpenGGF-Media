#!/usr/bin/env python3
"""Produce real verified Stageplay route rehearsals for the 2026-10-25 Typing route demo.
Inputs: current OpenGGF checkout, original S1/S2 ROMs, Java 25 and FFmpeg.
Outputs: authored scenes, actual planner results, native simulation telemetry and lossless films.
No desktop input/audio; terrain rehearsals clear placed objects and begin at authored anchors.
"""
import argparse,json,subprocess
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--engine',type=Path,required=True)
p.add_argument('--rom-dir',type=Path,required=True)
p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)

def cli(label,*args):
    r=subprocess.run(['python3',str(a.engine/'tools/stageplay/stageplay.py'),*map(str,args)],cwd=a.engine,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode:
        print(r.stderr[-5000:]);print(r.stdout);r.check_returncode()
    value=json.loads(r.stdout)
    assert value['ok'],value
    print(label,json.dumps({k:v for k,v in value['result'].items() if k not in ('candidate','path','commands','objectCommands')})[:1000],flush=True)
    return value

cases=[
 dict(id='ghz-loop',game='s1',start=[5100,686],goal=[5860,621],travel='RUN',ending='HARD_STOP',frames=420,camera=[dict(frame=0,x=5000,y=450,interpolation='LINEAR'),dict(frame=210,x=5420,y=450,interpolation='HOLD')]),
 dict(id='ehz-gentle',game='s2',start=[100,656],goal=[400,624],travel='WALK',ending='GENTLE_STOP',frames=420,camera=[dict(frame=0,x=0,y=480,interpolation='HOLD')]),
]
for c in cases:
    name=c['id'];src=a.out/(name+'.screenplay.json');scene=a.out/(name+'.stageplay');routed=a.out/(name+'-routed.stageplay')
    source=dict(version=7,name='Route demo: '+name,width=640,height=280,cast=[dict(id='sonic',name='Sonic',gameId=c['game'],character='sonic')],shots=[dict(id='rehearsal',durationFrames=c['frames'],set=dict(gameId=c['game'],zone=0,act=0),camera=c['camera'],actors=dict(sonic=[dict(frame=0,x=c['start'][0],y=c['start'][1],facing='RIGHT')]),worldCommands=[dict(frame=0,kind='CLEAR_OBJECTS')])])
    src.write_text(json.dumps(source,indent=2)+'\n')
    cli('compiled '+name,'compile','--script',src,'--out',scene)
    result=cli('planned '+name,'route','--scene',scene,'--actor','sonic','--frame',0,'--x',c['goal'][0],'--y',c['goal'][1],'--travel',c['travel'],'--ending',c['ending'],'--facing','LEFT','--frames',c['frames']-1,'--nodes',1024,'--ticks',120000,'--millis',60000,'--out',routed,'--'+c['game']+'-rom',a.rom_dir/(c['game']+'.gen'))
    assert result['result']['status']=='VERIFIED' and result['result']['nativeVerified']
    (a.out/(name+'-plan.json')).write_text(json.dumps(result,indent=2)+'\n')
    cli('simulated '+name,'simulate','--scene',routed,'--out',a.out/(name+'-native.jsonl'),'--'+c['game']+'-rom',a.rom_dir/(c['game']+'.gen'))
    cli('rendered '+name,'render','--scene',routed,'--out',a.out/(name+'.mkv'),'--'+c['game']+'-rom',a.rom_dir/(c['game']+'.gen'),'--scale',1)
