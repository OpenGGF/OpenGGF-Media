#!/usr/bin/env python3
"""ROM-lettered 400x224 trailer cards for the first Typing of the Hedgehog promo.
Inputs: glyphs/ from PromoGlyphs (own S3K ROM), backgrounds/ from actual captures.
Outputs: cards/<name>/f%04d.png, plus transparent caption assets. Scale 5x nearest
and crop to 1080p only at assembly. Task tool, 2026-10-10; Flappy promo style.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json
P=Path(__file__).resolve().parent
FONT={f.stem:Image.open(f).convert('RGBA') for f in (P/'glyphs').glob('?.png')}
SMALL={}
lines=(P/'assets/plate-font.txt').read_text().splitlines()
for i,line in enumerate(lines):
    if line.startswith('= '):
        g=Image.new('RGBA',(5,9),(0,0,0,0));d=ImageDraw.Draw(g)
        for y,row in enumerate(lines[i+1:i+10]):
            for x,c in enumerate(row):
                if c=='#':d.point((x,y),fill='white')
        SMALL[line[2]]=g

def text(im,txt,x,y,scale=1,color=None,band=True,reveal=999):
    font=FONT if band else SMALL
    if not band:scale*=2
    widths=[10 if band else 6 if c==' ' else 6 for c in txt] if not band else [10 if c==' ' else FONT[c].width+2 for c in txt]
    w=sum(widths)-2
    if band: ImageDraw.Draw(im).rectangle((x-4*scale,y+8*scale,x+(w+4)*scale,y+24*scale),fill=(22,25,37,255))
    for i,c in enumerate(txt):
        if c!=' ' and i<reveal:
            g=font[c].copy()
            if color:
                a=g.getchannel('A');g=Image.new('RGBA',g.size,color);g.putalpha(a)
            g=g.resize((max(1,round(g.width*scale)),max(1,round(g.height*scale))),Image.Resampling.NEAREST)
            im.alpha_composite(g,(round(x),round(y)))
        x+=widths[i]*scale
    return w*scale

def width(txt):return sum(10 if c==' ' else FONT[c].width+2 for c in txt)-2
def center(im,txt,y,scale=1,color=None,band=True,reveal=999,dx=0):text(im,txt,200-(width(txt) if band else (len(txt)*6-2)*2)*scale/2+dx,y,scale,color,band,reveal)
def bg(name,t):
    im=Image.open(P/'backgrounds'/f'{name}.png').convert('RGBA')
    im.alpha_composite(Image.new('RGBA',im.size,(5,9,27,195)))
    d=ImageDraw.Draw(im)
    for i in range(20):
        x=(i*71+t*1.4)%420-10;y=(i*29+t*.35)%230
        d.rectangle((x,y,x+1,y+1),fill=(95,174,226,65))
    d.rectangle((0,201,399,223),fill=(11,26,63,255))
    d.rectangle((0,0,399,3),fill=(255,194,44));d.rectangle((0,220,399,223),fill=(255,194,44))
    return im

# Main words use only authentic ROM title-card glyphs. The typography's dark band is retained.
CARDS={
 'one':(72,['ONE','HEDGEHOG'],'ghz',''),
 'keyboard':(72,['ONE','KEYBOARD'],'ehz',''),
 'survive':(120,['TYPE TO','SURVIVE'],'ghz',''),
 'letters':(78,['EVERY LETTER','COUNTS'],'ehz',''),
 'school':(60,['CLASS IS','IN SESSION'],'ehz',''),
 'back':(66,['TALK BACK'],'ghz',''),
 'boss':(72,['FACE','ROBOTNIK'],'probe',''),
 'reviews':(180,[],'ghz',''),
 'climax':(60,['TYPE','OR DIE'],'probe',''),
 'end':(360,['TYPING OF','THE HEDGEHOG'],'ghz',''),
}
def card(name,t):
    frames,lines,b,_=CARDS[name];im=bg(b,t);d=ImageDraw.Draw(im)
    if name=='reviews':
        q=min(2,t//60);age=t%60
        quotes=[(['MY TOASTER','TYPES FASTER'],'ROBOTNIK'),(['TAILS','APPROVES'],'TAILS'),(['FIVE RINGS','OUT OF FIVE'],'SONIC')]
        lines,author=quotes[q]
        ring=Image.open(P/'glyphs'/f'ring-{(t//6)%4}.png').convert('RGBA').resize((28,28),Image.Resampling.NEAREST)
        for i in range(5):
            g=ring.copy()
            if age<i*6:g.putalpha(g.getchannel('A').point(lambda a:a//4))
            im.alpha_composite(g,(106+36*i,24))
        for j,line in enumerate(lines):center(im,line,76+j*29,min(1.2,350/width(line)))
        center(im,author,152,.7,(255,209,76,255),False)
        center(im,'FICTIONAL CRITICS',192,.65,(185,207,237,255),False)
    elif name=='end':
        for j,line in enumerate(lines):center(im,line,42+j*41,min(1.65,352/width(line)),reveal=max(0,(t-j*12)//2))
        if t>35:
            center(im,'AN OPENGGF EXAMPLE MOD',142,.55,(255,212,68,255),False)
            center(im,'REQUIRES YOUR OWN ROMS',165,.52,None,False)
            center(im,'SONIC 1  SONIC 2  SONIC 3 AND KNUCKLES',184,.38,None,False)
            center(im,'INDEPENDENT FAN PROJECT',204,.38,(175,195,225,255),False)
    else:
        fit=min(2.0,min(352/width(line) for line in lines))
        s=fit+max(0,8-t)*.22
        shake=math.sin(t*2.5)*max(0,12-t)*.35
        for j,line in enumerate(lines):center(im,line,72+j*42-(s-fit)*7,s,dx=shake)
        if name=='keyboard':
            for row in range(3):
                for col in range(10):
                    x=140+col*12;y=166+row*10
                    d.rectangle((x,y,x+9,y+7),fill=(255,203,49) if col==(t//3+row)%10 else (87,111,145))
        if t<4:im.alpha_composite(Image.new('RGBA',im.size,(255,255,255,max(0,180-t*45))))
    return im.convert('RGB')

def caption(txt,file):
    im=Image.new('RGBA',(400,224),(0,0,0,0));d=ImageDraw.Draw(im)
    # The full-width blue caption panel covers the attract-demo label, not gameplay targets.
    d.rectangle((0,201,399,223),fill=(11,26,63,255));d.rectangle((0,201,399,202),fill=(255,195,43,255))
    center(im,txt,207,min(.65,367/(len(txt)*12)),None,False)
    im.save(file)

if __name__=='__main__':
    for n,(f,*_) in CARDS.items():
        path=P/'cards'/n;path.mkdir(parents=True,exist_ok=True)
        for t in range(f):card(n,t).save(path/f'f{t:04d}.png')
        print(n,f,flush=True)
    capdir=P/'captions';capdir.mkdir(exist_ok=True)
    for n,txt in {
      'ready':'GET READY  GET TYPING','combat':'TYPE THE WORD  STRIKE THE BADNIK',
      'rings':'TYPE THE LETTERS  WIN YOUR RINGS BACK','rescue':'BREAK MONITORS  RESCUE ANIMALS',
      'ghz':'GREEN HILL  TYPE TO DODGE THE BALL','ehz':'EMERALD HILL  STOP THE DRILL CAR',
      'fz':'FINAL ZONE  HIT ROBOTNIK S PILLAR','dez':'DEATH EGG  TWELVE HITS TO VICTORY',
      'taunt':'HE TALKS  YOU TYPE BACK','quiz':'OUTSMART ROBOTNIK','tally':'BOSS DEFEATED  EARN YOUR RANK',
      'slow':'EVERY KEY LIGHTS UP  SLOW MOTION',
      }.items():caption(txt,capdir/f'{n}.png')
