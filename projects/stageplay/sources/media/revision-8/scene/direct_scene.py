#!/usr/bin/env python3
"""Generate revision-eight Wait for me takes. Origin: approved Stageplay aesthetic revision.
Inputs: no assets; placements 179/166 are the verified supplied-ROM DEZ2 route.
Only initial placements are authored; subsequent motion belongs to native Puppet inputs.
Outputs are exclusive-create. Keep rejected takes instead of overwriting them.
"""
import argparse, copy, json
from pathlib import Path
STORY_FRAMES=1560
TOTAL_FRAMES=STORY_FRAMES+480

def target(index,offset=0):
 return dict(layoutIndex=index,objectId=74,subtype=1 if index==179 else 4,offsetX=offset,offsetY=-35)
def transfer(frame,index,offset=0):
 return [dict(frame=frame,kind='MOVE_TO',x=0,y=0,urgency=.65,target=target(index,offset)),dict(frame=frame+1,kind='JUMP',holdFrames=20),dict(frame=frame+2,kind='WAIT',condition='ON_OBJECT',timeoutFrames=180,target=target(index,offset)),dict(frame=frame+3,kind='STOP')]
def line(a,b,actor,text,**kwargs):
 return dict(startFrame=a,endFrame=b,speakerActor=actor,text=text,x=8,y=0,width=304,height=48,typerId='speech',skinId=actor,**kwargs)
def screenplay():
 count='One. Two. Three!'
 # Three begins at 1135 and completes at 1140, immediately before native takeoff.
 reveal=[0,1,2,3,4,33,34,35,36,37,70,71,72,73,74,75]
 assert len(count)==len(reveal), (len(count),len(reveal))
 return dict(version=3,name='Wait for me',width=320,height=224,
 cast=[dict(id=c,name=c.title(),gameId='s3k',character=c,snapToFloor=False) for c in ['sonic','tails']],
 dialogueTypers=[dict(id='speech',framesPerGrapheme=2,punctuationPauseFrames=4,spacePauseFrames=0)],
 dialogueSkins=[dict(id='sonic',nameArgb=-7495937,borderArgb=-7495937),dict(id='tails',nameArgb=-11172,borderArgb=-11172)],
 shots=[dict(id='together',durationFrames=TOTAL_FRAMES,set=dict(gameId='s3k',zone=11,act=1,worldPolicy='LIVE'),
 camera=[dict(frame=0,x=5268,y=1824,interpolation='HOLD',zoom=1,follow=dict(actors=['sonic','tails'],deadZoneX=12,deadZoneY=12,lookAhead=0,smoothing=.2,offsetX=0,offsetY=0))],
 actors={'sonic':[dict(frame=0,x=5428,y=1936)],'tails':[dict(frame=0,x=5472,y=1936)]},
 actions={
 'sonic':[dict(frame=0,kind='WAIT',condition='ON_OBJECT',timeoutFrames=90,target=target(179)),dict(frame=1,kind='STOP')]+transfer(240,166,-16)+[dict(frame=535,kind='CROUCH',holdFrames=45),dict(frame=580,kind='STOP')]+transfer(660,179,-16)+transfer(1140,166,-16),
 'tails':[dict(frame=0,kind='WAIT',condition='ON_OBJECT',timeoutFrames=90,target=target(179)),dict(frame=1,kind='STOP'),dict(frame=50,kind='MOVE_TO',x=0,y=0,urgency=.2,target=target(179,12)),dict(frame=51,kind='WAIT',condition='ARRIVED',timeoutFrames=90),dict(frame=52,kind='STOP'),dict(frame=390,kind='LOOK_UP',holdFrames=90)]+transfer(1145,166,16)},
 dialogue=[line(25,150,'tails','Other lift. Together, okay?'),line(160,235,'sonic','Race you there!'),line(340,520,'tails','You forgot the "together" bit.'),line(550,645,'sonic','Oh. Coming back!'),line(780,945,'tails','I could just fly over.'),line(950,1060,'sonic','This time, together.'),line(1065,1170,'sonic',count,revealFrames=reveal),line(1240,1385,'tails','See? Teamwork.'),line(1395,1550,'sonic','My slowest personal best.')],
 audio=[dict(frame=0,kind='ROM_MUSIC',gameId='s3k',soundId=23)])])

def takes():
 story=screenplay();clean=copy.deepcopy(story);clean['shots'][0]['dialogue']=[]
 sfx=copy.deepcopy(story);sfx['shots'][0]['audio']=[dict(frame=0,kind='MUSIC_STOP')]
 clean_sfx=copy.deepcopy(sfx);clean_sfx['shots'][0]['dialogue']=[]
 comparison=copy.deepcopy(clean_sfx)
 next(v for v in comparison['shots'][0]['actions']['sonic'] if v['frame']==241)['holdFrames']=8
 bed=dict(version=3,name='Continuous DEZ2 music bed',width=320,height=224,cast=[],shots=[dict(id='bed',durationFrames=5760,set=dict(gameId='s3k',zone=11,act=1),camera=[dict(frame=0,x=5268,y=1824)],actors={},audio=[dict(frame=0,kind='ROM_MUSIC',gameId='s3k',soundId=23)])])
 return {'story':story,'clean':clean,'story-sfx':sfx,'clean-sfx':clean_sfx,'comparison-hold8':comparison,'music-bed':bed}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out-dir',type=Path,required=True);a=p.parse_args();a.out_dir.mkdir(parents=True,exist_ok=True)
 for name,data in takes().items():
  with (a.out_dir/(name+'.screenplay.json')).open('x') as f:json.dump(data,f,indent=2);f.write('\n')
