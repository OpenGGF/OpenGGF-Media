#!/usr/bin/env python3
"""Emerald Remix round 5, 2026-10-22; rough cut only.
Audience: Sonic fans who recognise Emerald Hill and want a quick new run.
Form/evidence: Native-speed gameplay, honest stock/remix comparison; editorial strip assembly and actual generator-pixel graphic are explicitly art diagrams.
Promise: Your ROM, rearranged. Then somewhere entirely new.
Selling points: A double plus a single makes a triple; Clover is an original zone drawn by a pixel function.
Proof: Counted stock/remix splits; actual ROM foreground pieces join at their real 768px seam; actual whole-zone landscape builds from the generator, then opens into native Clover play; complete spring/landing/finish.
Hero: Full unrolled triple, with a schematic that counts the native sections outside Sonic's path.
Sound: One ROM EHZ 2P bed, measured 106.634169 BPM/0.040711s; sparse ROM punctuation and spring cue aligned to actual launch.
Palette/type: Stock card frame 62: white index6, black1, greys7/8 (182/146). Its black shadow is embedded at +2,+2; no invented outline, extra drop, yellow recolour or white-mask shine.
Treatment: Blue native-card bands; full-screen landscape tile build plus whole-zone panorama; three event-led Clover excerpts, native ring counter and spring/landing accents.
End: Game-native logo; one promise; source URL/status/disclaimer over fresh moving runout.
Scope: Production-directory assets, changed-section previews and rough cut. No commits, pushes, mastering or archive.
"""
import sys
from pathlib import Path
from functools import lru_cache
import csv
from PIL import ImageDraw
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
from promo_kit import *
ROOT=Path(__file__).resolve().parent
EDIT=dict(bpm=106.63416863432099,first=0.04071119047619047,fps=60,size=(1920,1080),out=ROOT/'out/emerald-remix-master.mp4',work=ROOT/'build')
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
def band(c,x,y,w,h,accent=True):
    rect(c,x,y,w,h,BLUE)
    if accent:
        # Sonic 2 red serrated tab and opposing yellow footer.
        rect(c,x-40,y,40,h,RED)
        for yy in range(int(y),int(y+h),24):
            pts=[(x,yy),(x+12,yy+12),(x,yy+24)]
            im=Image.new('RGBA',(16,24));ImageDraw.Draw(im).polygon([(0,0),(12,12),(0,24)],fill=RED)
            paste(c,rgba_of(im),x,yy)
        rect(c,x,y+h-8,w,8,YELLOW)
def label(c,line,x,y,scale=3):
    im=native(line,scale);band(c,x-12,y-10,im.shape[1]+24,im.shape[0]+20,False);paste(c,im,x,y)
def caption(e,b,a,z,line,y=870,scale=4):
    def draw(c,f,o,ed):
        im=native(line,scale);u=ease_out((f-o.f0)/12);x=960-im.shape[1]/2+(1-u)*1500
        band(c,x-28,y-18,im.shape[1]+56,im.shape[0]+40);paste(c,im,x,y)
    e.O(Fn(b(a),b(z),draw))
@lru_cache(maxsize=16)
def r5art(name):return Image.open(ROOT/'design/round5'/name).convert('RGBA')
@lru_cache(maxsize=1)
def cvrows():return list(csv.DictReader((CAP/'clover-shipping-route-final/state.csv').open()))
def ring_icon(c,x,y,size=52):
    im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im)
    d.ellipse((3,3,size-3,size-3),outline=(146,73,0),width=8)
    d.ellipse((1,1,size-7,size-7),outline=YELLOW,width=5)
    paste(c,rgba_of(im),x,y)

def build(e):
    b=e.bf
    hero=clip('remix-tumble-hero-final');wide=clip('remix-tumble-wide-final');stock=clip('stock-tumble-wide-exit02-final')
    ro=clip('remix-opening-final');so=clip('stock-opening-final');cv=clip('clover-shipping-route-final');tail=clip('clover-tail-final')
    e.S(Game(0,b(4),hero,src=103))
    def comparison(f,s,ed):
        local=50+f-s.f0
        c=stacked_split(ed,f,[(s.f0,stock,50,None,None),(s.f0,wide,50,None,None)],slide_frames=12)
        for y,name in [(0,'ORIGINAL'),(545,'REMIX')]:
            # Left/right edges avoid the wide capture's central native HUD.
            label_img=native(name,3);band(c,22,y+10,label_img.shape[1]+28,76,False);paste(c,label_img,34,y+22)
            count=sum(local>=x for x in ([115,180] if y==0 else [115,180,245]))
            if count:label(c,['ONE','TWO','THREE'][count-1],1540,y+27,4)
        return c
    e.S(Custom(b(4),b(12),comparison))
    def routes(f,s,ed):
        c=stacked_split(ed,f,[(s.f0,so,195,None,None),(s.f0,ro,195,None,None)],slide_frames=10)
        # Stock 400px footage has a left HUD; label the opposite side.
        label(c,'ORIGINAL',1440,24);label(c,'REMIX',1560,569)
        return c
    e.S(Custom(b(12),b(16),routes));caption(e,b,12.25,15.9,'SAME HILL NEW ROUTE',1000,3)
    e.S(Game(b(16),b(24),ro,src=0,dim=.22,cam=cam_slam(1.22,26,b(24)-b(16))))
    e.O(Flash(b(16),12,peak=.9))
    def title(c,f,o,ed):
        u=ease_out((f-o.f0)/14);x=round(350+(1-u)*1800)
        band(c,x,270,1580,520)
        logo(c,f,b(16),cx=1050+(1-u)*1800,cy=385,scale=9)
    e.O(Fn(b(16),b(24),title))
    e.O(Txt(b(17),b(23),native('REDISCOVER THE HILL',3),1050,705,enter='up',leave='right',centre=True))
    # Editorial diagram uses actual foreground art, cut at the recipe's double/single seam.
    def assemble(f,s,ed):
        t=f-s.f0;c=stripes(ed,f);c*=.6
        band(c,150,80,1770,170);paste(c,native('CUT FROM YOUR ROM',5),960-native('CUT FROM YOUR ROM',5).shape[1]/2,120)
        terrain=art('rom-triple-art.png').resize((1728,288),Image.Resampling.NEAREST)
        double=rgba_of(terrain.crop((0,0,1152,288)));single=rgba_of(terrain.crop((1152,0,1728,288)))
        # Two source pieces arrive separately, then join into their true 1152px route.
        join=ease_out((t-60)/24);y=380
        dx=-(1-ease_out(t/18))*1400
        sx=(1-ease_out((t-22)/18))*1000
        paste(c,double,96+dx-45*(1-join),y)
        paste(c,single,1248+sx+45*(1-join),y)
        label(c,'DOUBLE',500,740)
        if t>=22:label(c,'SINGLE',1370,740)
        if t<82:
            rect(c,1243,y-28,6,345,YELLOW,round(255*(1-join)))
        if t>=84:
            im=native('ONE TRIPLE',3);label(c,'ONE TRIPLE',960-im.shape[1]/2,860)
        return c
    e.S(Custom(b(24),b(28),assemble,trans='push',tdur=12,tdir='left'))
    e.S(Game(b(28),b(36),hero,src=65))
    def count_triple(c,f,o,ed):
        src=65+f-b(28)
        # These are the observed crest-crossing frames in the retained unrolled take.
        n=sum(src>=v for v in (115,180,245))
        if n==0:return
        small=art('rom-triple-art.png').resize((660,110),Image.Resampling.NEAREST)
        band(c,1200,810,720,200,False);paste(c,rgba_of(small),1230,870)
        for i in range(n):
            im=native(['ONE','TWO','THREE'][i],2);paste(c,im,1260+i*215,830)
    e.O(Fn(b(28),b(36),count_triple))
    # The full triple is still one continuous, unrolled native-speed take.
    # Large original landscape drawing. Same real generator; no fake editor UI.
    def draw_zone(f,s,ed):
        t=f-s.f0;c=np.zeros((1080,1920,3),np.float32);c[:]=BLUE
        # A world-space 1280x512 scenic window fills the stage, not one decorative tile.
        # Tile reveal order is diagonal, repeating the actual 16x16 chunk unit.
        bg=r5art('scene-background.png').resize((1920,768),Image.Resampling.NEAREST)
        fg=r5art('scene-foreground.png').resize((1920,768),Image.Resampling.NEAREST)
        back=np.array(bg).copy();front=np.array(fg).copy()
        yy,xx=np.mgrid[0:768,0:1920]
        # Sky/peaks sweep in first; terrain follows as a travelling tile wave.
        prog=clamp((t-12)/85)
        rank=(xx//24)*.72+(yy//24)*.55
        bm=rank<prog*82
        back[...,3]=np.where(bm,255,0)
        fm=rank<clamp((t-45)/137)*82
        front[...,3]=np.where(fm,front[...,3],0)
        paste(c,back,0,190);paste(c,front,0,190)
        # Fine construction grid is eaten by the incoming drawn pixels.
        grid=Image.new('RGBA',(1920,768));d=ImageDraw.Draw(grid)
        if t<190:
            alpha=round(90*(1-clamp((t-150)/40)))
            for x in range(0,1920,24):d.line((x,0,x,768),fill=(255,255,255,alpha),width=1)
            for y in range(0,768,24):d.line((0,y,1920,y),fill=(255,255,255,alpha),width=1)
        paste(c,rgba_of(grid),0,190)
        # Coach fix: the construction header exits right at double speed as the zone name
        # arrives, so the two blue bands never stack.
        hx=round(ease_in(clamp((t-180)/8))*2000)
        band(c,64+hx,20,1856,160)
        im=native('A ZONE DRAWN BY CODE',4);paste(c,im,960-im.shape[1]/2+hx,62)
        # Whole 5120px route: all of it draws, beneath the large scenic detail.
        pano=r5art('whole-landscape.png').resize((1720,172),Image.Resampling.NEAREST)
        p=np.array(pano).copy();p[:,int(1720*clamp((t-40)/145)): ,3]=0
        rect(c,0,886,1920,194,BLUE);paste(c,p,100,896)
        if t>185:
            # Big chapter identity arrives after the construction, not another slogan.
            im=native('CLOVER VALLEY',5);w=im.shape[1]
            x=round(960-w/2+(1-ease_out((t-185)/16))*1500)
            band(c,x-30,230,w+60,120);paste(c,im,x,252)
        return c
    e.S(Custom(b(36),b(44),draw_zone,trans='wipe',tdur=18))
    # Source 410..679: complete spring launch, high-platform landing and 22-ring sweep.
    e.S(Game(b(44),b(52),cv,src=410,trans='iris',tdur=20))
    launch=b(44)+435-410;land=b(44)+506-410
    e.punches.extend([(launch,.065),(land,.025)])
    e.X(launch,ROOT/'audio/stingers/s2-sfx-cc-mix.wav',.36,length=1.1)
    def ring_sweep(c,f,o,ed):
        src=410+f-b(44);rows=cvrows();n=int(rows[src]['rings'])-21
        # A factual pickup counter, activated by the visible first ring after takeoff.
        u=ease_out((f-o.f0)/12);x=round(1475+(1-u)*520)
        band(c,x,832,445,176)
        ring_icon(c,x+24,858)
        im=text(str(max(0,n)),'title',86,WHITE,stroke=2,shadow=3);paste(c,im,x+104,841)
        tag=native('PICKED UP',2);paste(c,tag,x+92,924)
        # Native pickup ticks drive pips; no invented score or frame-fitted motion.
        for i in range(22):rect(c,x+24+i*17,970,11,12,YELLOW if i<n else (20,42,110))
    # Coach fix: no pickup panel; the native RINGS HUD already counts. Ring blips stay.
    rows=cvrows()
    for src in range(455,651):
        if int(rows[src]['rings'])>int(rows[src-1]['rings']):
            e.X(b(44)+src-410,ROOT/'audio/stingers/s2-sfx-b5-mix.wav',.085,length=.16)
    # A second real action: takeoff, complete arc, landing, then the crest.
    e.S(Game(b(52),b(56),cv,src=710))
    e.punches.append((b(52)+794-710,.035))
    # Skip the uneventful traversals. Preserve native speed and the signpost spin.
    e.S(Game(b(56),b(62),cv,src=850,cam=cam_static(160,89.6,1.25)))
    def finish(c,f,o,ed):
        src=850+f-b(56)
        if src<980:return
        # Gold ring punctuation follows the actual goal, clear of Sonic/signpost.
        u=clamp((src-980)/12);im=native('NEXT RUN YOURS',3)
        x=round(960-im.shape[1]/2+(1-ease_out(u))*1600)
        band(c,x-24,840,im.shape[1]+48,110);paste(c,im,x,863)
    e.O(Fn(b(56),b(62),finish))
    def endcard(f,s,ed):
        c=blurred(tail.frame(30+f-s.f0),ed,radius=3,dim=.52,zoom=1.0)
        band(c,350,130,1570,560);logo(c,f,s.f0,cx=1050,cy=240,scale=8);return c
    e.S(Custom(b(62),b(74),endcard,trans='xfade',tdur=18))
    for beat,line,y in [(63,'REDISCOVER THE HILL',570),(63.5,'FIND A NEW VALLEY',635)]:
        e.O(Txt(b(beat),b(74),native(line,3),1050,y,enter='up',centre=True))
    for line,y,size in [('github.com/OpenGGF/OpenGGF',745,48),('/tree/develop/examples/emerald-remix',800,44),('Development example',880,36),('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.',960,32)]:
        e.O(Txt(b(63),b(74),text(line,'sub',size,WHITE,stroke=2,shadow=3),960,y,enter='up',centre=True))
    e.O(Fade(b(74)-120,b(74)))
    e.bed(ROOT/'audio/emerald-remix-review-bed.wav',gain=.85,length=b(74)/60,fade_out=2)
    for beat,sfx,gain,length in [(4,'b5',.3,.7),(16,'c3',.55,2),(24,'b5',.22,.7),(36-5/34,'bc',.36,.8)]:
        e.X(b(beat),ROOT/f'audio/stingers/s2-sfx-{sfx}-mix.wav',gain,length=length)
    return b(74)
