"""First Typing of the Hedgehog promo EDL, 2026-10-10, Flappy-style premiere trailer.
Source in/out are actual 60 Hz capture seconds. Only the explicitly labelled keyboard
shot runs at half speed; video and actual captured PCM slow together. No fixture footage.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
def plan():
    dez_end=json.loads((P/'caps/dez/clock.json').read_text())['ticks']/60
    return [
      dict(card='one',dur=1.2),dict(card='keyboard',dur=1.2),dict(card='survive',dur=2.0),
      dict(src='hub',start=0,dur=3.0,name='Title logo and announcer'),
      dict(src='ehz',start=.65,dur=3.7,caption='ready',name='Sonic 2 spindash: 3-2-1 START'),
      dict(src='ghz',start=.8,dur=3.6,caption='ready',name='Sonic 1 run and roll launch'),
      dict(src='ehz',start=4.35,dur=2.2,caption='ready',name='GET READY while travelling'),
      dict(src='ghz',start=7.5,dur=4.0,caption='combat',punches=[1.5,3.5],name='Closing badniks and typed homing strikes'),
      dict(src='ehz',start=13.0,dur=3.2,caption='combat',punches=[1.0],name='Keyboard lights and chained bounces'),
      dict(src='ehz',start=12.0,dur=1.4,speed=.5,zoom=1.6,caption='slow',name='Keyboard impact: labelled half speed'),
      dict(card='letters',dur=1.3),
      dict(src='ehz',start=49.7,dur=3.2,caption='rings',name='Letter rings to recover'),
      dict(src='ghz',start=38.5,dur=3.0,caption='rescue',name='Monitors and animal rescue'),
      dict(src='ehz',start=146.9,dur=2.0,caption='combat',name='WAVE CLEAR'),
      dict(card='school',dur=1.0),
      dict(src='hub',start=5.3,dur=1.2,name='Sonic 1 Story chapter map'),
      dict(src='hub',start=8.3,dur=1.2,name='Sonic 2 Story chapter map'),
      dict(src='hub',start=11.3,dur=1.2,name='Sonic 3 and Knuckles Story map'),
      dict(src='hub',start=14.0,dur=3.0,name='Tails welcomes you to Typing School'),
      dict(src='hub',start=23.35,dur=3.3,name='Boss Training drill'),
      dict(src='hub',start=27.8,dur=2.0,name='Records: per-key heat map'),
      dict(src='hub',start=31.5,dur=1.6,name='Boss Rush selection'),
      dict(card='reviews',dur=3.0),dict(card='back',dur=1.1),
      dict(src='ehz',start=159.0,dur=4.5,caption='taunt',name='Robotnik voiced taunt typed back'),
      dict(src='ghz',start=130.8,dur=4.1,caption='quiz',name='Robotnik trivia window'),
      dict(card='boss',dur=1.2),
      dict(src='ghz',start=137.9,dur=3.8,caption='ghz',punches=[1.4],name='Green Hill wrecking-ball dodge'),
      dict(src='ehz',start=171.3,dur=3.3,caption='ehz',punches=[1.5],name='Emerald Hill drill car charge'),
      dict(src='fz',start=53.9,dur=3.5,caption='fz',name='HIT ROBOTNIK S PILLAR: four words'),
      dict(src='fz',start=56.7,dur=2.4,caption='fz',punches=[1.3],name='Final Zone crushers and plasma'),
      dict(card='climax',dur=1.0),
      dict(src='dez',start=13.7,dur=2.7,caption='dez',name='Death Egg rocket fist'),
      dict(src='dez',start=15.6,dur=3.0,caption='dez',punches=[1.2],name='Death Egg targeting-sensor slam'),
      dict(src='dez',start=19.3,dur=2.5,caption='dez',punches=[1.5],name='Death Egg bombs'),
      dict(src='dez',start=dez_end-8.5,dur=3.0,caption='tally',punches=[1.0],name='Twelfth hit and BOSS DEFEATED'),
      dict(src='dez',start=dez_end-3.8,dur=3.2,caption='tally',name='Rank tally'),
      dict(src='hub',start=39.6,dur=1.7,name='Rank A and record reward'),
      dict(card='end',dur=5.0),
    ]
