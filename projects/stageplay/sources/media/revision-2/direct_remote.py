#!/usr/bin/env python3
"""Author 'Location, Location, Location' with Stageplay's shot-local screenplay format.
Origin: OpenGGF Stageplay directing extension, 2026-10-21. No ROM data is embedded.
"""
import json
from pathlib import Path
import argparse

def key(f,x,y,a=5,**kw): return dict(frame=f,x=x,y=y,animation=a,**kw)
def cam(f,x,y,z=1,**kw): return dict(frame=f,x=x,y=y,zoom=z,**kw)
def caption(start,end,text,y=18,color=-1): return dict(startFrame=start,endFrame=end,text=text,x=14,y=y,argb=color)
def sound(frame,id,game='s2',kind='ROM_SFX'): return dict(frame=frame,kind=kind,gameId=game,soundId=id)
def shake(start,end,ax=3,ay=2,seed=17): return dict(startFrame=start,endFrame=end,amplitudeX=ax,amplitudeY=ay,frequency=9,seed=seed)
def shot(id,frames,game,zone,act,camera,actors,captions,*,transition=None,audio=None,effects=None):
    result=dict(id=id,durationFrames=frames,set=dict(gameId=game,zone=zone,act=act),camera=camera,actors=actors,captions=captions,audio=audio or [],cameraEffects=effects or [])
    if transition: result['transition']=dict(kind=transition,durationFrames=36)
    return result

def screenplay():
    return dict(version=1,name='Location, Location, Location',width=400,height=224,cast=[
        dict(id='sonic',name='Sonic',gameId='s2',character='sonic'),
        dict(id='tails',name='Tails',gameId='s2',character='tails'),
        dict(id='knuckles',name='Knuckles',gameId='s3k',character='knuckles')],shots=[
        shot('remote',420,'s2',0,0,[cam(0,0,500),cam(300,35,515,1.15,interpolation='SMOOTH')],{
            'sonic':[key(0,-20,655,0),key(100,156,648),key(300,156,648,7)],
            'tails':[key(0,240,648,flipX=True),key(260,240,648,7,flipX=True)]},[
                caption(12,140,'LOCATION, LOCATION, LOCATION',20,-256),
                caption(150,290,'Tails: One remote. Every location.'),
                caption(300,402,'Sonic: Can it skip the walking?')],audio=[sound(0,129,kind='ROM_MUSIC'),sound(390,160)]),
        shot('closer',300,'s2',0,0,[cam(0,380,470,1.15),cam(299,420,495,1.35)],{
            'sonic':[key(0,520,622,7),key(170,520,622,5,flipX=True)],
            'tails':[key(0,600,624,5,flipX=True),key(210,600,624,7,flipX=True)]},[
                caption(30,160,'Sonic: That was only three steps.'),
                caption(170,275,'Tails: I was being careful.')],transition='WIPE_LEFT',audio=[sound(265,160)],effects=[shake(240,280,2,2)]),
        shot('acttwo',420,'s2',0,1,[cam(0,0,535),cam(220,20,547,1.2)],{
            'sonic':[key(0,150,687,7),key(175,150,687,5,flipX=True)],
            'tails':[key(0,235,687,5,flipX=True),key(280,235,687,7,flipX=True)]},[
                caption(35,180,'Sonic: This looks familiar...'),
                caption(195,390,'Tails: Same hill. Different act.')],transition='FADE_BLACK',audio=[sound(0,129,kind='ROM_MUSIC'),sound(390,160)],effects=[shake(350,402,4,2,5)]),
        shot('greenhill',420,'s1',0,0,[cam(0,0,800),cam(300,45,820,1.25)],{
            'sonic':[key(0,130,944,7),key(150,160,944,0),key(205,160,944,5,flipX=True)],
            'tails':[key(0,240,944,5,flipX=True),key(300,240,944,7,flipX=True)]},[
                caption(30,175,'Sonic: Now this is REALLY familiar.'),
                caption(190,390,'Tails: The settings are... nostalgic.')],transition='FADE_WHITE',audio=[sound(0,129,'s1','ROM_MUSIC'),sound(390,160)],effects=[shake(350,402,3,4,31)]),
        shot('island',540,'s3k',0,0,[cam(0,4900,900),cam(180,5000,906,1.1),cam(440,5010,920,1.25)],{
            'sonic':[key(0,5035,1000,2),key(45,5035,1050,5),key(350,5035,1050,7)],
            'tails':[key(0,5110,990,2),key(45,5110,1052,5,flipX=True),key(380,5110,1052,7,flipX=True)],
            'knuckles':[key(0,5280,1046,0,flipX=True),key(180,5180,1046,5,flipX=True)]},[
                caption(45,210,'Knuckles: I ordered a quiet\n          afternoon.'),
                caption(230,365,'Sonic: We can return this one.'),
                caption(390,510,'Tails: Found the HOME button!')],transition='WIPE_RIGHT',audio=[sound(0,1,'s3k','ROM_MUSIC'),sound(25,0xb1,'s2'),sound(510,160)],effects=[shake(20,65,5,3,11),shake(490,525,2,2,3)]),
        shot('home',420,'s2',0,0,[cam(0,25,515,1.15),cam(240,0,500),cam(419,0,500)],{
            'sonic':[key(0,156,648,5),key(180,156,648,7),key(320,156,648,5,flipX=True)],
            'tails':[key(0,240,648,5,flipX=True),key(270,240,648,7,flipX=True)]},[
                caption(35,180,'Tails: See? Perfectly reliable.'),
                caption(200,350,'Sonic: Great. Now put it down.')],transition='FADE_BLACK',audio=[sound(0,129,kind='ROM_MUSIC'),sound(390,160)]),
        shot('mostly',240,'s1',0,0,[cam(0,20,810,1.2),cam(210,30,815,1.25)],{
            'sonic':[key(0,130,944,7,flipX=True)],
            'tails':[key(0,240,944,5,flipX=True)]},[
                caption(30,125,'Tails: ...Mostly reliable.'),
                caption(145,230,'Made with OpenGGF Stageplay',18,-256)],transition='FADE_WHITE',audio=[sound(0,129,'s1','ROM_MUSIC')])])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);args=parser.parse_args()
    with args.output.open('x') as f:json.dump(screenplay(),f,indent=2);f.write('\n')
