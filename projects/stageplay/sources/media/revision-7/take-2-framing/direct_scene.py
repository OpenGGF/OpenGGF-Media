#!/usr/bin/env python3
"""Author 'Wait for me', a first-creator directing example. Origin: Stageplay tutorial, 2026-10-22.
Inputs: none; native placements derive from the supplied-ROM DEZ2 level catalog.
"""
import argparse,json
from pathlib import Path

def target(index,offset=0):
 return dict(layoutIndex=index,objectId=74,subtype=1 if index==179 else 4,offsetX=offset,offsetY=-35)
def transfer(frame,index,offset=0):
 return [dict(frame=frame,kind='MOVE_TO',x=0,y=0,urgency=.65,target=target(index,offset)),dict(frame=frame+1,kind='JUMP',holdFrames=20),dict(frame=frame+2,kind='WAIT',condition='ON_OBJECT',timeoutFrames=180,target=target(index,offset)),dict(frame=frame+3,kind='STOP')]
def line(a,b,actor,text):
 return dict(startFrame=a,endFrame=b,speakerActor=actor,text=text,x=8,y=170,width=304,height=48,typerId='speech',skinId=actor)
def screenplay():
 return dict(version=3,name='Wait for me',width=320,height=224,
 cast=[dict(id=c,name=c.title(),gameId='s3k',character=c,snapToFloor=False) for c in ['sonic','tails']],
 dialogueTypers=[dict(id='speech',framesPerGrapheme=2,punctuationPauseFrames=4,spacePauseFrames=0)],
 dialogueSkins=[dict(id='sonic',nameArgb=-7495937,borderArgb=-7495937),dict(id='tails',nameArgb=-11172,borderArgb=-11172)],
 shots=[dict(id='together',durationFrames=1560,set=dict(gameId='s3k',zone=11,act=1,worldPolicy='LIVE'),
 camera=[dict(frame=0,x=5268,y=1824,interpolation='HOLD',follow=dict(actors=['sonic','tails'],deadZoneX=12,deadZoneY=12,lookAhead=0,smoothing=.2,offsetX=0,offsetY=15))],
 actors={'sonic':[dict(frame=0,x=5428,y=1936)],'tails':[dict(frame=0,x=5472,y=1936)]},
 actions={
 'sonic':[dict(frame=0,kind='WAIT',condition='ON_OBJECT',timeoutFrames=90,target=target(179)),dict(frame=1,kind='STOP')]+transfer(240,166,-16)+transfer(660,179,-16)+transfer(1140,166,-16),
 'tails':[dict(frame=0,kind='WAIT',condition='ON_OBJECT',timeoutFrames=90,target=target(179)),dict(frame=1,kind='STOP'),dict(frame=50,kind='MOVE_TO',x=0,y=0,urgency=.2,target=target(179,12)),dict(frame=51,kind='WAIT',condition='ARRIVED',timeoutFrames=90),dict(frame=52,kind='STOP'),dict(frame=390,kind='LOOK_UP',holdFrames=90)]+transfer(1145,166,16)},
 dialogue=[line(25,150,'tails','Other lift. Together, okay?'),line(160,300,'sonic','Race you there!'),line(340,520,'tails','You forgot the "together" bit.'),line(550,720,'sonic','Oh. Coming back!'),line(800,1000,'tails','Try counting us in this time.'),line(1010,1150,'sonic','One. Two. Three!'),line(1240,1385,'tails','See? Teamwork.'),line(1395,1550,'sonic','My slowest personal best.')],
 audio=[dict(frame=0,kind='ROM_MUSIC',gameId='s3k',soundId=23)])])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--variants',action='store_true');a=p.parse_args()
 with a.out.open('x') as f:json.dump(screenplay(),f,indent=2);f.write('\n')

 if a.variants:
  root=a.out.parent
  clean=screenplay();clean['shots'][0]['dialogue']=[];clean['name']='Wait for me / clean directing view'
  bed={'version':3,'name':'Stageplay tutorial music bed','width':320,'height':224,'cast':[], 'shots':[{'id':'bed','durationFrames':5880,'set':{'gameId':'s3k','zone':11,'act':1},'camera':[{'frame':0,'x':5268,'y':1824}],'actors':{},'audio':[{'frame':0,'kind':'ROM_MUSIC','gameId':'s3k','soundId':23}]}]}
  for name,value in [('directing-view',clean),('music-bed',bed)]:
   with (root/(name+'.screenplay.json')).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
