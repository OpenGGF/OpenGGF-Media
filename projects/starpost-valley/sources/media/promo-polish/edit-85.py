#!/usr/bin/env python3
"""Starpost Valley promo polish, 2026-10-10.

Inputs: production GameLoop PNG captures in sv-promo/final and this task directory;
Azure Lake rendered by OpenGGF from the supplied S3K ROM; existing ROM SFX bank.
Output: reproducible 1080p60 trailer, exact edit list, soundtrack and QA frames.
No engine or mod implementation is changed. Gameplay is shown at its captured speed;
the crop-growth passage alone is explicitly presented as a time-lapse.
"""
from pathlib import Path
from functools import lru_cache
from multiprocessing import Pool
import bisect, csv, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/home/farrell/scratch/sv-promo/final')
REFERENCE = Path('/home/farrell/Videos/OGGF/slay-the-robotnik-promo')
W, H, FPS, SR = 1920, 1080, 60, 48000
TEMPO = 0.85
PERIOD, PHASE = 0.8001 / TEMPO, 0.360 / TEMPO
CREAM = (255, 248, 225)
GOLD = (255, 216, 100)
GREEN = (111, 218, 130)
INK = (12, 32, 29)
FONTS = Path('/usr/share/fonts/TTF')
NEW = {'snowboard', 'fair', 'feast', 'maze', 'grow-sfx', 'orchard-sfx', 'farmers-clean',
       'season-spring','season-summer','season-autumn','season-winter'}

def clamp(x): return max(0, min(1, x))
def ease(x): return 1 - (1 - clamp(x)) ** 3
def smooth(x):
    x = clamp(x)
    return x*x*(3-2*x)
def bf(b): return round((PHASE + b * PERIOD) * FPS)

@lru_cache(maxsize=64)
def font(size, style='heavy'):
    name = {'heavy':'FiraSansCompressed-Heavy.ttf', 'italic':'FiraSansCondensed-BoldItalic.ttf',
            'body':'FiraSans-Medium.ttf', 'bold':'FiraSans-Bold.ttf'}[style]
    return ImageFont.truetype(str(FONTS/name), round(size))

@lru_cache(maxsize=256)
def lettering(s, size, style='heavy', colour=CREAM):
    f = font(size, style)
    x0,y0,x1,y1 = f.getbbox(s)
    im = Image.new('RGBA',(x1-x0+24,y1-y0+28))
    d = ImageDraw.Draw(im)
    d.text((12-x0,16-y0),s,font=f,fill=(0,18,20,190),stroke_width=3)
    d.text((9-x0,9-y0),s,font=f,fill=colour)
    return im

def paste(c, im, xy, alpha=1):
    if alpha <= 0: return
    if alpha < .999:
        im = im.copy()
        im.putalpha(im.getchannel('A').point(lambda a:round(a*alpha)))
    c.paste(im,tuple(round(k) for k in xy),im)

def txt(c,s,size,xy,style='heavy',colour=CREAM,alpha=1,centre=False):
    im=lettering(s,size,style,colour)
    x,y=xy
    if centre:x-=im.width/2
    paste(c,im,(x,y),alpha)

@lru_cache(maxsize=32)
def files(name):
    p=(ROOT if name in NEW else SOURCE)/name
    return sorted(p.glob('[0-9][0-9][0-9][0-9].png'))

@lru_cache(maxsize=48)
def frame(name,index):
    fs=files(name)
    if not fs:raise ValueError('Missing source '+name)
    return Image.open(fs[max(0,min(len(fs)-1,round(index)))]).convert('RGB')

def pixel_view(im, size=(W,H), box=None):
    # Integer nearest-neighbour enlargement, area filtering only at the output boundary.
    if box is None:box=(0,0,im.width,im.height)
    x0,y0,x1,y1=box
    k=max(1,math.ceil(size[0]/(x1-x0)))
    ix0,iy0=math.floor(x0),math.floor(y0)
    ix1,iy1=math.ceil(x1),math.ceil(y1)
    crop=im.crop((ix0,iy0,ix1,iy1))
    big=crop.resize((crop.width*k,crop.height*k),Image.Resampling.NEAREST)
    return big.resize(size,Image.Resampling.BOX,box=((x0-ix0)*k,(y0-iy0)*k,(x1-ix0)*k,(y1-iy0)*k))

def view(name,index,size=(W,H),zoom=1,cx=200,cy=112,box=None):
    im=frame(name,index)
    if box is None:
        vh=min(im.height/zoom,im.width/zoom*size[1]/size[0]);vw=vh*size[0]/size[1]
        x=max(0,min(im.width-vw,cx-vw/2));y=max(0,min(im.height-vh,cy-vh/2))
        box=(x,y,x+vw,y+vh)
    return pixel_view(im,size,box)

@lru_cache(maxsize=4)
def shade(which):
    a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=INK
    y=np.arange(H)
    if which=='top':opacity=np.maximum(0,1-y/410)**1.7*.9
    elif which=='bottom':opacity=np.maximum(0,1-(H-y)/400)**1.3*.95
    else:opacity=np.full(H,.59)
    a[:,:,3]=(255*opacity).astype(np.uint8)[:,None]
    return Image.fromarray(a)

def header(c, title, sub, age, hold=2.7):
    a=ease(age/.28)*(1-smooth((age-hold)/.4))
    if a<=0:return
    paste(c,shade('top'),(0,0),a)
    dx=-60*(1-ease(age/.32))
    d=ImageDraw.Draw(c)
    d.rectangle((90+dx,66,98+dx,217),fill=GOLD)
    txt(c,title,96,(116+dx,60),alpha=a)
    if sub:txt(c,sub,35,(120+dx,173),style='body',alpha=a)

def lower(c, title, sub, age, hold=10):
    a=ease(age/.3)*(1-smooth((age-hold)/.35))
    paste(c,shade('bottom'),(0,0),a)
    dy=35*(1-ease(age/.3))
    txt(c,title,83,(95,842+dy),alpha=a)
    if sub:txt(c,sub,34,(100,944+dy),style='body',colour=GOLD,alpha=a)

def label(c,s,xy,age=1):
    im=lettering(s,32,'bold',CREAM)
    x,y=xy;d=ImageDraw.Draw(c)
    d.rounded_rectangle((x,y,x+im.width+30,y+im.height+12),radius=9,fill=INK)
    paste(c,im,(x+15,y+2),ease(age/.22))

@lru_cache(maxsize=8)
def logo(width):
    im=np.array(frame('story',180).crop((142,29,252,83)))
    a=Image.new('RGBA',(110,54));rgba=np.zeros((54,110,4),np.uint8)
    rgba[:,:,:3]=CREAM
    rgba[:,:,3]=(np.min(im,axis=2)>180).astype(np.uint8)*255
    a=Image.fromarray(rgba)
    return a.resize((width,round(width*54/110)),Image.Resampling.NEAREST)

def scenic(f, night=False):
    # Moving water/sky from an uninterrupted intro background; hide only the skip bar.
    im=view('story',565+(f%65),box=(0,28,400,205))
    im=ImageEnhance.Brightness(im).enhance(.58 if night else .68)
    return im

def brand(c, age, end=False):
    paste(c,shade('full'),(0,0),.25)
    a=ease(age/.6)
    im=logo(1000 if end else 1120)
    x=(W-im.width)/2;y=170 if end else 185
    paste(c,im,(x,y+40*(1-a)),a)
    txt(c,'THE VALLEY AFTER THE CREDITS',48,(W/2,y+im.height+50),'bold',GOLD,a,True)
    if end:
        txt(c,'A farming story in Green Hill',44,(W/2,800),'body',CREAM,ease((age-.5)/.5),True)
        txt(c,'An OpenGGF mod',34,(W/2,874),'bold',GOLD,ease((age-1)/.5),True)
        txt(c,'Bring your Sonic 1 + Sonic 3 & Knuckles ROMs',29,(W/2,935),'body',CREAM,ease((age-1.4)/.5),True)
        txt(c,'github.com/OpenGGF/OpenGGF',28,(W/2,992),'body',CREAM,ease((age-1.8)/.5),True)
    else:
        txt(c,'A farming story in Green Hill',49,(W/2,855),'italic',CREAM,ease((age-.6)/.4),True)
        txt(c,'An OpenGGF mod',31,(W/2,945),'bold',GOLD,ease((age-1)/.4),True)

SHOTS=[]
def add(a,b,kind,name=None,src=0,title='',sub='',trans=False,**kw):
    SHOTS.append(dict(f0=0 if a==0 else bf(a),f1=bf(b),kind=kind,name=name,src=src,
                      title=title,sub=sub,trans=trans,**kw))

# The measured 75 BPM grid is slowed to 63.75 BPM, retaining the original pitch.
add(0,4,'hook','story',485)
add(4,10,'brand',trans=True)
add(10,16,'game','farmers-clean',260,title='CHOOSE YOUR FARMER',sub='Sonic, Tails or Knuckles',
    lower=True,trans=True)
add(16,20,'game','grow',145,title='SPIN DASH. PLANT. HARVEST.',sub='A familiar move. A new way to use it.',trans=True)
add(20,22,'game','grow',328,tag='PLANT',zoom=(1.12,1.15),cx=200,cy=118)
add(22,24,'game','grow',528,tag='WATER',zoom=(1.12,1.15),cx=200,cy=118)
add(24,28,'game','grow',650,tag='WATCH IT GROW',src_end=870,rate=1.3)
add(28,32,'game','grow',890,tag='HARVEST',zoom=(1.04,1.07))
add(32,36,'game','grow',1265,tag='SHIP IT',src_end=1450)
add(36,43,'seasons',title='FOUR SEASONS. ONE HOME.',sub='Spring rain. Summer sun. Autumn gold. Winter snow.',trans=True)
add(43,48,'game','seasons',840,title='STAY FOR THE AURORA',sub='',hold_header=2.7)
add(48,54,'game','neighbours',190,title='MAKE A FEW NEW FRIENDS',sub='The animals you saved have a place to call home.',lower=True,src_end=310,trans=True)
add(54,58,'game','neighbours',360,src_end=500)
add(58,64,'game','neighbours',674,src_end=910)
add(64,68,'game','lake',350,title='TAKE THE SCENIC ROUTE',sub='Cast a line at Waterfall Lake.',trans=True)
add(68,72,'game','lake',670,src_end=887)
add(72,74,'game','orchard-museum',62,title='GROW YOUR OWN LITTLE PARADISE',hold_header=1.3)
add(74,78,'collection')
add(78,84,'ruins',title='A LITTLE ADVENTURE',sub='Marble. Labyrinth. Scrap Brain.',trans=True)
add(84,88,'game','labyrinth',240,tag='DEEP IN THE RUINS')
add(88,92,'game','hunt',615,title='A WHOLE VALLEY OF CELEBRATIONS',sub='Eight festivals through the year.',trans=True)
add(92,96,'game','race',610,tag='THE GREAT VALLEY RACE',zoom=(1.03,1.03))
add(96,100,'game','snowboard',575,tag='ICE CAP SNOWBOARD RUN',trans=True)
add(100,102,'game','fair',340,tag='THE VALLEY FAIR')
add(102,104,'game','maze',445,tag='SCRAP BRAIN NIGHT')
add(104,108,'celebrations')
add(108,116,'game','finale',153,title='A VALLEY TO COME HOME TO',sub='',src_end=500,trans=True)
add(116,124,'end',trans=True)
ENDS=[s['f1'] for s in SHOTS]
TOTAL=SHOTS[-1]['f1']

def src_frame(s,f):
    i=s['src']+(f-s['f0'])*s.get('rate',1)
    return min(i,s.get('src_end',len(files(s['name']))-1))

def tile(c,name,src,local,rect,text=None,crop=None,age=1):
    x,y,w,h=rect
    im=view(name,src+local,size=(w,h),box=crop)
    c.paste(im,(x,y))
    d=ImageDraw.Draw(c);d.rectangle((x,y,x+w,y+h),outline=(229,218,164),width=4)
    if text:label(c,text,(x+18,y+15),age)

@lru_cache(maxsize=8)
def screen_positions(name):
    # Driver CSV data is editorial camera evidence only; gameplay is never changed.
    p=(ROOT if name in NEW else SOURCE)/name/'state.csv'
    with p.open() as f:
        rows=list(csv.reader(f))[1:]
    return [(float(r[2])-float(r[8]),float(r[3])-float(r[9])) for r in rows]

def image_for(s,f):
    age=(f-s['f0'])/FPS;local=f-s['f0'];u=local/max(1,s['f1']-s['f0'])
    k=s['kind']
    if k=='game':
        z0,z1=s.get('zoom',(1,1));c=view(s['name'],src_frame(s,f),zoom=z0+(z1-z0)*smooth(u),cx=s.get('cx',200),cy=s.get('cy',112))
        if s['title']:
            if s.get('lower'):lower(c,s['title'],s['sub'],age,hold=10)
            else:header(c,s['title'],s['sub'],age,s.get('hold_header',2.65))
        if s.get('tag'):
            label(c,s['tag'],(86,70),age)
            if s.get('rate',1)!=1:label(c,'TIME-LAPSE',(W-310,70),age)
        return c
    if k in ['brand','end']:
        c=scenic(local);brand(c,age,k=='end');return c
    if k=='hook':
        c=view('story',s['src']+local,box=(0,28,400,205))
        paste(c,shade('full'),(0,0),.5)
        txt(c,'You saved Green Hill.',106,(W/2,345),'italic',CREAM,ease(age/.4),True)
        txt(c,'Now make it a home.',116,(W/2,493),'heavy',GOLD,ease((age-.65)/.4),True)
        return c
    c=Image.new('RGB',(W,H),INK)
    if k=='seasons':
        rects=[(66,235,884,354),(970,235,884,354),(66,627,884,354),(970,627,884,354)]
        entries=[('SPRING','season-spring'),('SUMMER','season-summer'),('AUTUMN','season-autumn'),('WINTER','season-winter')]
        for i,((name,clip),rect) in enumerate(zip(entries,rects)):
            dly=i*7
            if local>=dly:
                tile(c,clip,245,local-dly,rect,name,crop=(0,35,400,195),age=age-dly/FPS)
        header(c,s['title'],s['sub'],age,20)
    elif k=='collection':
        tile(c,'orchard-museum',245,min(local,110),(75,95,1150,644),crop=(0,0,400,224))
        tile(c,'orchard-museum',460,min(local,90),(935,485,910,510),crop=(0,0,400,224))
        txt(c,'COLLECT. DONATE. DISCOVER.',77,(95,844),colour=GOLD,alpha=ease(age/.4))
        txt(c,"Build the Workshop Museum's collection.",33,(101,945),'body')
    elif k=='ruins':
        entries=[('MARBLE','marble',240),('LABYRINTH','labyrinth',145),('SCRAP BRAIN','scrap',155)]
        for i,(name,clip,start) in enumerate(entries):
            rect=(70+i*606,247,568,688)
            sf=start+local
            cx,cy=screen_positions(clip)[sf]
            vw=206*568/688;x=max(0,min(400-vw,cx-vw/2))
            tile(c,clip,sf,0,rect,name,crop=(x,12,x+vw,218),age=age-i*.12)
        header(c,s['title'],s['sub'],age,20)
        txt(c,'Explore the Ruins. Bring something back.',37,(W/2,981),'italic',GOLD,1,True)
    elif k=='celebrations':
        c=view('feast',880+min(local,199))
        tile(c,'parade',350+min(local,169),0,(76,74,844,473),text='SUNFLOWER PARADE',age=age)
        tile(c,'flickies',290+min(local,229),0,(1000,74,844,473),text='NIGHT OF THE FLICKIES',age=age)
        label(c,'STAR LIGHT FEAST',(86,602),age)
    return c

def wipe(old,new,local,duration=22):
    # A restrained checkerboard curtain, echoing the Green Hill ground.
    u=ease(local/duration);c=old.copy();d=ImageDraw.Draw(c)
    rows=12;rh=H//rows
    for y in range(rows):
        lead=(.07 if y%2 else 0);x=round(W*clamp((u-lead)/(1-lead)))
        if x>0:
            c.paste(new.crop((0,y*rh,x,(y+1)*rh)),(0,y*rh))
            if x<W:d.rectangle((x,y*rh,min(W,x+10),(y+1)*rh),fill=GOLD)
    return c

def render_frame(f):
    index=bisect.bisect_right(ENDS,f);s=SHOTS[min(index,len(SHOTS)-1)]
    c=image_for(s,f)
    local=f-s['f0']
    if s['trans'] and index>0 and local<22:
        old=image_for(SHOTS[index-1],SHOTS[index-1]['f1']-1)
        c=wipe(old,c,local)
    if f<18:c=ImageEnhance.Brightness(c).enhance(smooth(f/18))
    if f>TOTAL-35:c=ImageEnhance.Brightness(c).enhance(smooth((TOTAL-f)/35))
    return c

def read_wav(path):
    with wave.open(str(path)) as w:
        assert w.getframerate()==SR and w.getnchannels()==2
        return np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(np.float32)/32768

def write_wav(path,a):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())

def mix():
    n=TOTAL*(SR//FPS);out=np.zeros((n,2),np.float32)
    def add(a,at,gain=1,fin=240,fout=480):
        at=round(at*SR);a=a[:n-at].copy()
        if not len(a):return
        fin=min(fin,len(a));fout=min(fout,len(a))
        a[:fin]*=np.linspace(0,1,fin)[:,None]
        a[-fout:]*=np.linspace(1,0,fout)[:,None]
        out[at:at+len(a)]+=a*gain
    end=SHOTS[-1]['f0']/FPS
    music=read_wav(ROOT/'azure-lake-gentle.wav')
    music*=.15/max(.001,np.sqrt((music**2).mean()))
    add(music[:round(end*SR)],0,.9,fin=SR//3,fout=round(.25*SR))
    data=read_wav(ROOT/'data-select-gentle.wav')
    data*=.12/max(.001,np.sqrt((data**2).mean()))
    add(data,end,.9,fin=round(.35*SR),fout=round(1.15*SR))
    # True SFX-only recording copies use the public music-off debug command.
    stems={}
    for name in ['grow-sfx','orchard-sfx','fair','maze','feast']:
        raw=(ROOT/name/'audio.raw')
        if raw.exists():stems[name]=np.fromfile(raw,'<i2').reshape(-1,2).astype(np.float32)/32768
    for s in SHOTS:
        name=s['name'];stem_name={'grow':'grow-sfx','orchard-museum':'orchard-sfx'}.get(name,name)
        if s['kind']=='game' and stem_name in stems and s.get('rate',1)==1:
            a0=round(s['src']*800);count=(s['f1']-s['f0'])*800
            if s.get('src_end') is not None:count=min(count,round((s['src_end']-s['src'])*800))
            add(stems[stem_name][a0:a0+count],s['f0']/FPS,.8)
    bank=read_wav(REFERENCE/'audio/sfx-bank.wav')
    ids='33 AB B6 B3 AF B4 B8 63 6E 9F 3C 42 B1 6A AC 9C 62 4E'.split()
    def sfx(sid,at,gain=.4,length=.7):
        k=ids.index(sid);a=bank[k*3*SR:k*3*SR+round(length*SR)]
        add(a,at,gain,fout=800)
    for b in [4,16,36,48,64,78,88,96,108,116]:sfx('63',bf(b)/FPS,.26,.52)
    for b in [54,58,72,74,92,100,102,104]:sfx('33',bf(b)/FPS,.24,.46)
    sfx('B8',bf(108)/FPS+.65,.4,1.3)
    # No pitch/rate changes. Headroom leaves the music and transients intact.
    peak=float(np.abs(out).max())
    if peak>.89:out*=.89/peak
    write_wav(ROOT/'soundtrack.wav',out)
    print(json.dumps({'duration':TOTAL/FPS,'rate':SR,'peak_dbfs':20*math.log10(max(1e-10,float(np.abs(out).max()))),
                      'rms_dbfs':20*math.log10(float(np.sqrt((out**2).mean())))},indent=2))

def worker_bytes(f):return render_frame(f).tobytes()

def inspect_sources():
    for s in SHOTS:
        if s['name']:
            final=src_frame(s,s['f1']-1)
            assert 0<=s['src']<len(files(s['name'])) and final<len(files(s['name']))
    for name in NEW:
        raw=ROOT/name/'audio.raw'
        if raw.exists():assert raw.stat().st_size==len(files(name))*800*4,(name,'PCM/frame mismatch')
    (ROOT/'edit.json').write_text(json.dumps({'fps':FPS,'rate':SR,'duration':TOTAL/FPS,'beat_period':PERIOD,
                                           'beat_phase':PHASE,'music_tempo':TEMPO,'shots':SHOTS},indent=2)+'\n')

def sheet():
    fs=sorted(set([min(TOTAL-1,s['f0']+max(35,(s['f1']-s['f0'])//2)) for s in SHOTS]))
    out=Image.new('RGB',(480*4,290*math.ceil(len(fs)/4)),INK);d=ImageDraw.Draw(out)
    for i,f in enumerate(fs):
        x=i%4*480;y=i//4*290
        out.paste(render_frame(f).resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
        d.text((x+6,y+3),f'{f/FPS:.2f}s / frame {f}',fill=CREAM)
    out.save(ROOT/'review-sheet.jpg',quality=94)
    print(ROOT/'review-sheet.jpg')

def render():
    mix();out=ROOT/'polished-video.mp4'
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),
         '-i','pipe:0','-an','-c:v','libx264','-threads','4','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        with Pool(4) as pool:
            for f,b in enumerate(pool.imap(worker_bytes,range(TOTAL),chunksize=6)):
                p.stdin.write(b)
                if f%600==0:print(f'{f}/{TOTAL} frames',flush=True)
    finally:p.stdin.close()
    if p.wait():raise RuntimeError('Video encoder failed')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-i',str(ROOT/'soundtrack.wav'),
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',str(SR),
                    '-t',str(TOTAL/FPS),'-movflags','+faststart',str(ROOT/'starpost-valley-promo.mp4')],check=True)
    print('Rendered',TOTAL/FPS,'seconds',flush=True)

if __name__=='__main__':
    inspect_sources()
    mode=sys.argv[1] if len(sys.argv)>1 else 'sheet'
    if mode=='sheet':sheet()
    elif mode=='frames':
        for t in sys.argv[2:]:
            f=round(float(t)*FPS);render_frame(f).save(ROOT/f'review-{f:05d}.png')
    elif mode=='audio':mix()
    elif mode=='render':render()
    else:raise SystemExit('sheet | frames <seconds...> | audio | render')
