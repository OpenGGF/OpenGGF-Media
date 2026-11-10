#!/usr/bin/env python3
"""MICA & TALON, final showcase.
Audience: Sonic fans and would-be modders. Promise: two original heroes across three games.
Form/evidence: GameplayCaptureTool native gameplay; positioned setups disclosed; art morph is editorial.
Seven proofs: redraw morph; three-host split; homing lock/strike; flight/down-lock/dive;
leader/follower; presentation mosaic; real MicaMod registration beside play.
Hero: MGZ2 airborne three-Mantis homing chain, native score transitions 65/82/104.
Sound: paced ROM LBZ1, 163.255 BPM, first .362; sections 12.86/16.17/61.74/65.41/73.13.
Palette: jade00926D/coralFF4949/slate6D6D92/amberFFB624 and native title band.
Title: native S2 title-card glyphs, as S3K has no general alphabet asset.
Treatment: Slay the Robotnik beat grid, slam, native banners, full-bleed action, comparisons.
Rejected: plain labelled clips (no idea); frantic ability montage (consequence unreadable).
End: example framework demo, source URL, fan disclaimer; never a release/download.
Setup: positioned gameplay and seeded presentation components; no cold-route claim.
Archive: local OpenGGF-Media commit, no push until lead publication. Sound checked by measurement only.
"""
import sys,os,csv
from pathlib import Path
from functools import lru_cache
ROOT=Path(os.environ.get('MT_CHECKOUT','/mnt/LinuxData/T3/worktrees/OpenGGF/t3-97452066'))
P=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools/media'))
from promo_kit import *
V=os.environ.get('MT_VERTICAL')=='1'
EDIT=dict(bpm=163.255,first=.362,fps=60,size=(1080,1920) if V else (1920,1080),out=P/'out'/('master-9x16.mp4' if V else 'master-16x9.mp4'),work=P/'edit'/('vertical' if V else 'wide'))
CAP=Path(os.environ.get('MT_CAPTURES',str(P/'captures')))
NATIVE=BitmapFont(P/'edit/assets/s2-title-font.txt',space=8)
@lru_cache(None)
def native(s,scale=4):return NATIVE.render(s,scale=scale,fill=WHITE,shades={'1':(0,0,0),'6':WHITE,'7':(182,182,182),'8':(146,146,146)},outline=None,drop=None)
def clip(n,take='phase1'):return Frames(CAP/os.environ.get('MT_TAKE',take)/n/'frames')
hero=clip('hero-mgz2');team=clip('team');carry=clip('carry');gilded=clip('gilded');solar=clip('solar');finish=clip('ehz-clear','revision2');data=clip('data-select-team')
runs=[clip(n) for n in ['s1-safe','s2-run','s3k-run']]
def frame(c,i,e):return arr(game_view(c.frame(i),ow=e.W,oh=e.H))
@lru_cache(None)
def picture(p):return Image.open(p).convert('RGBA')
def label(c,s,x,y,size=64,col=WHITE):paste(c,text(s,'title_it',size,col,stroke=4,shadow=5),x,y)
def fullsafe(c,i,e):
 im=c.frame(i); bg=arr(game_view(im,ow=e.W,oh=e.H));
 if V:
  bg*=.25; q=arr(im.resize((1080,756),Image.Resampling.NEAREST));bg[560:1316]=q
 return bg

class VerticalGame(Game):
 def image(self,f,e):return fullsafe(self.clip,self.src_frame(f),e)*(1-self.dim)
if V:Game=VerticalGame

def title(f,s,e):
 if s.f0<4000:
  im=clip('title-s2-full').frame(510+f-s.f0)
  # Full native emblem and complete character rise; independently letterboxed vertical.
  if V:
   c=stripes(e,f,c0=(8,16,56),c1=(0,73,73));q=rgba_of(im.resize((1080,756),Image.Resampling.NEAREST));paste(c,q,0,480);return c
  return frame(clip('title-s2-full'),510+f-s.f0,e)
 # Opaque end plate clears every pixel of the HUD and results text.
 c=stripes(e,f,c0=(8,16,56),c1=(0,36,73))
 for k,line in enumerate(['MICA','TALON']):
  a=native(line,6 if V else 8);paste(c,a,(e.W-a.shape[1])/2,e.H*.23+k*200)
 return c

def origin(f,s,e):
 c=stripes(e,f,c0=(8,16,56),c1=(0,73,73));u=s.u(f)
 base=Path.home()/'scratch/agent-tmp/mica-regen-20261108'
 paths=[ROOT/'examples/mica-and-talon/concept/mica.png',base/'attempts/wait-00-2.png',ROOT/'examples/mica-and-talon/art/mica/frames/wait-00.png',ROOT/'examples/mica-and-talon/art/mica/frames/wait-00.png']
 if u>.55:
  # Binding model sheet -> enlarged pose -> strip; editorial source imagery.
  paths=[ROOT/'examples/mica-and-talon/concept/mica.png',ROOT/'examples/mica-and-talon/art/mica/frames/wait-00.png']
  boxes=[(40,260,980,600),(40,900,440,620),(540,1080,480,420)] if V else [(40,180,780,650),(870,180,400,650),(1300,180,580,650)]
  sheet=picture(str(paths[0])).copy();sheet.thumbnail((boxes[0][2],boxes[0][3]),Image.Resampling.LANCZOS)
  pose=picture(str(paths[1]));pose=pose.crop(pose.getbbox());pose=pose.resize((pose.width*12,pose.height*12),Image.Resampling.NEAREST)
  for im,box in zip([sheet,pose],boxes):paste(c,rgba_of(im),box[0]+(box[2]-im.width)/2,box[1]+(box[3]-im.height)/2)
  strip=Image.new('RGBA',(150,50));
  for i,n in enumerate(['wait-00','walk-00','walk-01']):
   q=picture(str(ROOT/f'examples/mica-and-talon/art/mica/frames/{n}.png'));q=q.crop(q.getbbox());strip.paste(q,(i*50,50-q.height),q)
  strip=strip.resize((600,200),Image.Resampling.NEAREST);box=boxes[2];paste(c,rgba_of(strip),box[0]+(box[2]-600)/2,box[1]+200)
  for title,box in zip(['MODEL SHEET','ENLARGED POSE','SPRITE STRIP'],boxes):label(c,title,box[0],box[1]-60,40)
  label(c,'EDITORIAL / FRAME-BY-FRAME ORIGINAL ART',40,e.H-100,36)
  return c
 # A true source-to-redraw dissolve, then native-sized reduction; no fabricated sprite motion.
 phase=min(2,int(u/.55*3));mix=smooth((u/.55*3-phase))
 def tile(path):
  im=picture(str(path));im=im.crop(im.getbbox());limit=600 if V else 650;im.thumbnail((limit,limit),Image.Resampling.NEAREST)
  if im.height<limit: im=im.resize((int(im.width*limit/im.height),limit),Image.Resampling.NEAREST)
  return rgba_of(im)
 a=tile(paths[phase]);b=tile(paths[phase+1]);x=e.W*.5;y=e.H*.46
 paste(c,a,x-a.shape[1]/2,y-a.shape[0]/2,1-mix);paste(c,b,x-b.shape[1]/2,y-b.shape[0]/2,mix)
 label(c,['MODEL SHEET','GPT REDRAW','FINAL SPRITE'][phase],60,e.H*.78,60)
 label(c,'EDITORIAL PROCESS / ORIGINAL SOURCE IMAGES',60,e.H*.87,30)
 return c

def triple(f,s,e):
 names=['s1-safe','s2-run','s3k-run'];labels=['SONIC 1','SONIC 2','SONIC 3 & K']
 if V:
  c=stripes(e,f);h=(e.H-20)//3
  for k,n in enumerate(names):
   if f<s.f0+k*22:continue
   c[k*(h+10):k*(h+10)+h]=tracked(n,45+f-s.f0-k*22,e.W,h)
   q=chip(labels[k]);paste(c,q,40,k*(h+10)+h-q.shape[0]-24)
  return c
 panes=[]
 for k,n in enumerate(names):
  # Narrow slice needs a padded full scene recentered on the live actor.
  def pane(lf,n=n):
   idx=45+lf;r=clip(n);im=r.frame(idx);row=states(n)[min(idx,len(states(n))-1)]
   x=float(row['x'])-float(row['cam_x']);y=float(row['y'])-float(row['cam_y'])
   bg=Image.new('RGB',(640,360),(8,16,56));bg.paste(im,(round(320-x),round(180-y)))
   return arr(game_view(bg,ow=e.W,oh=e.H))
  panes.append((s.f0+k*22,pane,labels[k]))
 return slanted_split(e,f,panes,divider=(255,182,36))

@lru_cache(None)
def states(name):
 return list(csv.DictReader(open(CAP/os.environ.get('MT_TAKE','final')/name/'state.csv')))
def tracked(name,idx,w,h):
 r=clip(name);im=r.frame(idx);rs=states(name);row=rs[min(idx,len(rs)-1)]
 x=float(row['x'])-float(row['cam_x']);y=float(row['y'])-float(row['cam_y'])
 # Recenter the entire native viewport in a padded plane, then choose the pane.
 pad=Image.new('RGB',(960,672),(8,16,56));pad.paste(im,(320,224))
 return arr(game_view(pad,320+x,224+y,3 if V else 7.5, w,h))
def pair(f,s,e,left,right,labels):
 names=[left.path.parent.name,right.path.parent.name] if False else []
 # Frames objects retain the directory under .dir (resolved below).
 names=[Path(left.path).parent.name,Path(right.path).parent.name]
 sh=(e.H-10)//2;c=stripes(e,f)
 for k,name in enumerate(names):
  t=s.f0+k*22
  if f<t:continue
  q=tracked(name,30+f-t,e.W,sh)
  c[k*(sh+10):k*(sh+10)+sh]=q
  pill=chip(labels[k]);paste(c,pill,40,k*(sh+10)+sh-pill.shape[0]-24)
 return c

def mosaic(f,s,e):
 cells=[('HUD',clip('talon-s2'),80,(0,100)),('SIGNPOST',finish,300,(80,60)),('RESULTS',clip('gilded-clear-low'),650,(80,22)),('HALF PIPE',clip('halfpipe-cleared-post'),300,(80,70)),('BLUE SPHERE',clip('blue-play'),200,(80,48)),('CONTINUE',clip('continue'),80,(80,64)),('DATA SELECT',data,480,(100,30)),('ENDING',clip('ending-full'),2700,(80,60))]
 cols,rows=(2,4) if V else (4,2);w=e.W//cols;h=e.H//rows;c=stripes(e,f)
 for i,(name,r,src,(cx,cy))in enumerate(cells):
  if f<s.f0+i*22:continue
  x=i%cols*w;y=i//cols*h;im=r.frame(min(450,src+f-s.f0) if name=='SIGNPOST' else src+f-s.f0)
  # Exactly 3x native; subject crops preserve readable pixels inside eight cells.
  cw=(w-12)//3;ch=(h-70)//3;cx=min(cx,320-cw);cy=min(cy,224-ch)
  im=im.crop((cx,cy,cx+cw,cy+ch)).resize((cw*3,ch*3),Image.Resampling.NEAREST)
  paste(c,rgba_of(im),x+6,y+6)
  label(c,name,x+18,y+h-58,36)
 return c

def code(f,s,e):
 c=fullsafe(hero,30+f-s.f0,e);return c*.5

def build(e):
 b=e.bf; sec=lambda t:round(t*60)
 # Beat sheet: 0-16 cold proof;16-34 title;34-43 origin;43-59 three hosts;
 #59-79 homing;79-99 Talon;99-115 team;115-139 screens;139-167 API;
 #167-198 climax, section changes 61.74/65.41/73.13; end to beat220.
 e.bed(P/'music/s3k-music-0d-paced.wav',gain=.65,fade_out=2)
 e.S(Game(0,b(6),hero,src=15,cam=cam_move((160,112,1.04),(160,112,1.12))))
 e.O(Txt(b(3),b(6),text('TWO NEW HEROES.','title_it',110 if not V else 80,WHITE,stroke=6,shadow=6),e.W/2,e.H*.77,centre=True,enter='up'))
 e.S(Custom(b(6),sec(12.86),title,trans='wipe',tdur=18));e.O(Flash(b(6),16));e.X(b(6),P/'music/s3k-sfx-b3-paced.wav',2.2)
 e.S(Custom(sec(12.86),b(55),origin,trans='wipe',tdur=16))
 e.S(Custom(b(55),b(71),triple,trans='wipe',tdur=16))
 e.S(Game(b(71),b(79),hero,src=0,cam=cam_move((160,112,1),(170,112,1.1)),trans='wipe',tdur=16))
 e.S(Custom(b(79),b(91),lambda f,s,e:pair(f,s,e,clip('hero'),gilded,['JADE / HOMING','GILDED / INSTAGIB']),trans='push',tdur=16))
 e.S(Custom(b(91),b(111),lambda f,s,e:pair(f,s,e,clip('talon-s2'),clip('talon-s3k'),['TALON / SONIC 2','TALON / SONIC 3 & K']),trans='wipe',tdur=16))
 e.S(Game(b(111),b(123),carry,src=40,cam=cam_move((160,112,1),(175,112,1.06)),trans='wipe',tdur=16))
 e.S(Custom(b(123),b(127),lambda f,s,e:pair(f,s,e,team,solar,['TOGETHER','SOLAR FLIGHT']),trans='push',tdur=12))
 e.S(Custom(b(127),b(147),mosaic,trans='wipe',tdur=16))
 e.S(Custom(b(147),sec(61.74),code,trans='wipe',tdur=16))
 # Exact MicaMod.java call, whitespace wrapped and enlarged for the final panel.
 lines=[('n','context.registerCharacter('),('n','    "mica",'),('n','    MicaCharacter.definition('),('n','        context.ownerModId(), materialized,'),('n','        MicaPresentation.load('),('n','            context.modAssets()),'),('n','        MicaGilded.profile('),('n','            context.modAssets())));')]
 e.O(Typed(b(147)+18,sec(61.74),lines,50,150 if V else 530,w=980,h=510,cps=55,title='MicaMod.java / actual registration'))
 e.S(Game(sec(61.74),sec(76.74),clip('gilded-clear-low'),src=70,cam=cam_move((160,112,1),(160,112,1.04)),trans='wipe',tdur=16))
 e.S(Custom(sec(76.74),sec(84.8),title,trans='iris',tdur=24))
 for k,line in enumerate(['An example built with','OpenGGF\'s mod framework','github.com/OpenGGF/OpenGGF']):
  e.O(Txt(sec(76.74)+20,sec(84.8),text(line,'sub',48 if not V else 44,WHITE,stroke=3,shadow=3),e.W/2,e.H*.67+k*65,centre=True,enter='up'))
 e.O(Txt(sec(76.74),sec(84.8),text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.','body',30 if not V else 20,WHITE),e.W/2,e.H*.94,centre=True))
 # No fabricated pickup or jump sounds.

 # Native chapter cards slide in once; distinct from captured HUD.
 for a,z,words in [(12.86,15.5,'ORIGINAL'),(20.58,22.5,'THREE GAMES'),(26.45,28.6,'HOMING'),(33.81,36,'TALON'),(41.16,43.3,'TOGETHER'),(47.04,49.4,'EVERY SCREEN'),(54.39,56.5,'MOD API')]:
  class Band(Overlay):
   def draw(self,c,f,e):
    h=160 if not V else 140;y=e.H-h-24
    u=min(1,(f-self.f0)/12,(self.f1-f)/12);x=int(-e.W*(1-ease_out(u)))
    plate=Image.new('RGBA',(e.W,h),(8,36,146,255));d=ImageDraw.Draw(plate)
    d.rectangle((0,0,48,h),fill=(255,36,36,255));d.rectangle((48,h-12,e.W,h),fill=(255,219,36,255))
    paste(c,rgba_of(plate),x,y);q=native(self.words,3 if V else 4);paste(c,q,x+80,y+(h-q.shape[0])/2-6)
  h=Band(sec(a),sec(z));h.words=words;e.O(h)
 e.O(Fade(sec(83.8),sec(84.8)))
 return sec(84.8)
