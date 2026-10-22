#!/usr/bin/env python3
"""Emerald Remix coached revision, 2026-10-22; rough cut only.
Audience: Sonic fans who recognise Emerald Hill and want a quick new run.
Form/evidence: Native-speed gameplay, honest stock/remix comparison; editorial strip assembly and actual generator-pixel graphic are explicitly art diagrams.
Promise: Your ROM, rearranged. Then somewhere entirely new.
Selling points: A double plus a single makes a triple; Clover is an original zone drawn by a pixel function.
Proof: Counted stock/remix splits; actual ROM foreground pieces join at their real 768px seam; real generator decoration draws itself over native Clover play; complete spring/landing/finish.
Hero: Full unrolled triple, with a short invitation outside Sonic's path, then room to read the animation.
Sound: One ROM EHZ 2P bed, measured 106.634169 BPM/0.040711s; sparse ROM punctuation and spring cue aligned to actual launch.
Palette/type: Stock card frame 62: white index6, black1, greys7/8 (182/146). Its black shadow is embedded at +2,+2; no invented outline, extra drop, yellow recolour or white-mask shine.
Treatment: Preserve cold open, count and flash/stinger/slam; beat-led strip assembly, generated clover scan, spring callout, ring trail and last jump; no bare filler.
End: Game-native logo; one promise; source URL/status/disclaimer over fresh moving runout.
Scope: Production-directory assets, changed-section previews and rough cut. No commits, pushes, mastering or archive.
"""
import sys
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
from promo_kit import *
ROOT=Path(__file__).resolve().parent
EDIT=dict(bpm=106.63416863432099,first=0.04071119047619047,fps=60,size=(1920,1080),out=ROOT/'out/emerald-remix-rough.mp4',work=ROOT/'build')
CAP=ROOT/'captures';NATIVE=BitmapFont(ROOT/'design/rom-title-font/s2-title-font.txt',space=8)
BLUE=(48,87,206);WHITE=(255,255,255);YELLOW=(255,255,0);RED=(255,0,0)
SHADES={'1':(0,0,0),'6':WHITE,'7':(182,182,182),'8':(146,146,146)}
def clip(name):return Frames(CAP/name/'frames')
@lru_cache(maxsize=96)
def native(s,scale=4,yellow=False):
    # The native bevel AND black +2,+2 shadow live in the ROM glyph itself.
    return NATIVE.render(s,scale=scale,fill=WHITE,shades=SHADES,outline=None,drop=None)
@lru_cache(maxsize=8)
def art(name):return Image.open(ROOT/'design/revision'/name).convert('RGBA')
def rect(c,x,y,w,h,col,a=255):
    q=np.zeros((int(h),int(w),4),np.float32);q[...,:3]=col;q[...,3]=a;paste(c,q,x,y)
def logo(c,f,t0,cx=960,cy=430,scale=9,shine=False):
    t=f-t0
    for i,word in enumerate(['EMERALD','REMIX']):
        img=native(word,scale);u=clamp((t-i*6)/14)
        if not u:continue
        # Integer-sized glyphs translate into place; camera supplies the title slam.
        x=round(cx-img.shape[1]/2+(1-ease_out(u))*700)
        y=round(cy+i*(16*scale+28)-img.shape[0]/2)
        paste(c,img,x,y,clamp(u*3))
def caption(e,b,a,z,line,y=870,scale=4):
    e.O(Shade(b(a),b(z),'bottom'))
    e.O(Txt(b(a),b(z),native(line,scale),960,y,enter='up',leave='right',centre=True,dur=12))

def build(e):
    b=e.bf
    hero=clip('remix-tumble-hero-final');wide=clip('remix-tumble-wide-final');stock=clip('stock-tumble-wide-exit02-final')
    ro=clip('remix-opening-final');so=clip('stock-opening-final');cv=clip('clover-shipping-route-final');tail=clip('clover-tail-final')
    e.S(Game(0,b(4),hero,src=103))
    def comparison(f,s,ed):
        local=50+f-s.f0
        c=stacked_split(ed,f,[(s.f0,stock,50,None,None),(s.f0,wide,50,None,None)],slide_frames=12)
        for y,label in [(0,'ORIGINAL'),(545,'REMIX')]:
            # Left/right edges avoid the wide capture's central native HUD.
            paste(c,native(label,3),34,y+22)
            count=sum(local>=x for x in ([115,180] if y==0 else [115,180,245]))
            if count:paste(c,native(['ONE','TWO','THREE'][count-1],4),1540,y+27)
        return c
    e.S(Custom(b(4),b(12),comparison))
    def routes(f,s,ed):
        c=stacked_split(ed,f,[(s.f0,so,195,None,None),(s.f0,ro,195,None,None)],slide_frames=10)
        # Stock 400px footage has a left HUD; label the opposite side.
        paste(c,native('ORIGINAL',3),1440,24);paste(c,native('REMIX',3),1560,569)
        return c
    e.S(Custom(b(12),b(16),routes));caption(e,b,12.25,15.9,'SAME HILL NEW ROUTE',1000,3)
    e.S(Game(b(16),b(24),ro,src=0,dim=.22,cam=cam_slam(1.22,26,b(24)-b(16))))
    e.O(Flash(b(16),12,peak=.9));e.O(Fn(b(16),b(24)-12,lambda c,f,o,ed:logo(c,f,b(16))))
    e.O(Txt(b(17),b(23),native('REDISCOVER THE HILL',3),960,750,enter='up',leave='right',centre=True))
    # Editorial diagram uses actual foreground art, cut at the recipe's double/single seam.
    def assemble(f,s,ed):
        t=f-s.f0;c=stripes(ed,f);c*=.6
        paste(c,native('CUT FROM YOUR ROM',5),960-native('CUT FROM YOUR ROM',5).shape[1]/2,120)
        terrain=art('rom-triple-art.png').resize((1728,288),Image.Resampling.NEAREST)
        double=rgba_of(terrain.crop((0,0,1152,288)));single=rgba_of(terrain.crop((1152,0,1728,288)))
        # Two source pieces arrive separately, then join into their true 1152px route.
        join=ease_out((t-60)/24);y=380
        dx=-(1-ease_out(t/18))*1400
        sx=(1-ease_out((t-22)/18))*1000
        paste(c,double,96+dx-45*(1-join),y)
        paste(c,single,1248+sx+45*(1-join),y)
        paste(c,native('DOUBLE',3),500,740,clamp(t/12))
        paste(c,native('SINGLE',3),1370,740,clamp((t-22)/12))
        if t<82:
            rect(c,1243,y-28,6,345,YELLOW,round(255*(1-join)))
        if t>=84:
            im=native('ONE TRIPLE',3);paste(c,im,960-im.shape[1]/2,860,clamp((t-84)/12))
        return c
    e.S(Custom(b(24),b(28),assemble,trans='push',tdur=12,tdir='left'))
    e.S(Game(b(28),b(36),hero,src=65))
    caption(e,b,28,30,'NOW RUN IT',870,4)
    # The full triple is still one continuous, unrolled native-speed take.
    # Clover retains its exact source continuation; only the accompaniment changes.
    e.S(Game(b(36),b(60),cv,src=100,trans='wipe',tdur=18))
    # The 400px take reveals beyond the act's native right bound. A held 320px
    # editorial crop keeps the real exit offscreen and all top HUD rows intact.
    e.S(Game(b(60),b(65),cv,src=100+b(60)-b(36),cam=cam_static(160,89.6,1.25)))
    def cv_header(c,f,o,ed):
        t=f-b(36);u=ease_out(t/14);leave=ease_in((t-122)/8) if t>122 else 0
        x=round(800+(1-u)*1500+leave*2100)
        rect(c,x,90,1120,190,BLUE)
        # Native card red tab, kept right of all native HUD digits.
        rect(c,x-48,70,40,230,RED)
        paste(c,native('CLOVER VALLEY',5),x+35,118)
        paste(c,native('SOMEWHERE NEW',3),x+38,220)
    e.O(Fn(b(36),b(40),cv_header))
    # This is the ACTUAL generator's 16x16 decoration, not invented editor UI.
    def pixel_art(c,f,o,ed):
        t=f-o.f0;u=ease_out(t/12);out=clamp((o.f1-f)/8)
        x=round(1470+(1-u)*600);y=100
        rect(c,x-20,y-20,350,410,BLUE,round(245*out))
        base=np.array(art('clover-pixel-function.png')).copy()
        # Scan in glyph-sized rows, then show the intact native pixel grid.
        n=min(16,max(0,(t-10)//4));base[n:,:,3]=0
        paste(c,rgba_of(Image.fromarray(base).resize((288,288),Image.Resampling.NEAREST)),x+10,y+8,out)
        im=native('PIXEL RULE',2);paste(c,im,x+12,y+326,out)
        if 0<n<16:rect(c,x+10,y+8+n*18,288,3,YELLOW,round(255*out))
    e.O(Fn(b(40),b(44),pixel_art));caption(e,b,40,44,'A ZONE DRAWN BY CODE',870,3)
    caption(e,b,44,48.1,'TAKE THE HIGH ROAD',870,4)
    launch=b(36)+435-100;e.punches.append((launch,.045))
    e.X(launch,ROOT/'audio/stingers/s2-sfx-cc-mix.wav',.32,length=1.3)
    # A ring trail encourages the eye along the actual high route, without a fake score.
    caption(e,b,48.2,52,'FOLLOW THE GOLD',870,4)
    caption(e,b,52.2,56,'ONE MORE LEAP',870,4)
    # Give the final crest its own invitation, then let the signpost answer it.
    caption(e,b,56.2,60,'HOW FAST CAN YOU GO',870,3)
    caption(e,b,60.2,64.8,'YOUR TURN',870,5)
    def endcard(f,s,ed):
        c=blurred(tail.frame(30+f-s.f0),ed,radius=3,dim=.52,zoom=1.0)
        logo(c,f,s.f0,cx=960,cy=240,scale=8);return c
    e.S(Custom(b(65),b(77),endcard,trans='xfade',tdur=18))
    for beat,line,y in [(66,'REDISCOVER THE HILL',570),(66.5,'FIND A NEW VALLEY',635)]:
        e.O(Txt(b(beat),b(77),native(line,3),960,y,enter='up',centre=True))
    for line,y,size in [('github.com/OpenGGF/OpenGGF',745,48),('/tree/develop/examples/emerald-remix',800,44),('Development example · free',880,36),('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.',960,32)]:
        e.O(Txt(b(66),b(77),text(line,'sub',size,WHITE,stroke=2,shadow=3),960,y,enter='up',centre=True))
    e.O(Fade(b(77)-120,b(77)))
    e.bed(ROOT/'audio/emerald-remix-review-bed.wav',gain=.85,length=b(77)/60,fade_out=2)
    for beat,sfx,gain,length in [(4,'b5',.3,.7),(16,'c3',.55,2),(24,'b5',.22,.7),(36-5/34,'bc',.36,.8)]:
        e.X(b(beat),ROOT/f'audio/stingers/s2-sfx-{sfx}-mix.wav',gain,length=length)
    return b(77)
