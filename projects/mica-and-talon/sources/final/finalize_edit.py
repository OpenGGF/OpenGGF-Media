from pathlib import Path
P=Path(__file__).parent;p=P/'edit/edit.py';s=p.read_text();s=s.replace('MICA & TALON, phase-two showcase.','MICA & TALON, final showcase.').replace('Hero: AIZ reticle/strike sequence. Gap: only two verified kills, three-enemy chain pending.','Hero: MGZ2 airborne three-Mantis homing chain, native score transitions 65/82/104.').replace('Deviation: missing shots are explicit rough placeholders; final-art and chain/carry/routes remain pending.','Setup: positioned gameplay and seeded presentation components; no cold-route claim.').replace('No upload/archive in phase 1, per user.','Archive: local OpenGGF-Media commit, no push until lead publication.')
a=s.index('def title(');z=s.index('\ndef origin(',a)
s=s[:a]+'''def title(f,s,e):
 if s.f0<4000:
  im=clip('title-s2').frame(f-s.f0)
  # Full native emblem and complete character rise; independently letterboxed vertical.
  if V:
   c=stripes(e,f,c0=(8,16,56),c1=(0,73,73));q=rgba_of(im.resize((1080,756),Image.Resampling.NEAREST));paste(c,q,0,480);return c
  return frame(clip('title-s2'),f-s.f0,e)
 # Opaque end plate clears every pixel of the HUD and results text.
 c=stripes(e,f,c0=(8,16,56),c1=(0,36,73))
 for k,line in enumerate(['MICA','TALON']):
  a=native(line,6 if V else 8);paste(c,a,(e.W-a.shape[1])/2,e.H*.23+k*200)
 return c
''' + s[z:]
# No stock sprite reference remains: show original drawing -> final sprite.
s=s.replace("base/'native/wait-00.png',base/'native/wait-00-8x.png',base/'attempts/wait-00-2.png'","ROOT/'examples/mica-and-talon/concept/mica.png',base/'attempts/wait-00-2.png',ROOT/'examples/mica-and-talon/art/mica/frames/wait-00.png'")
s=s.replace("['NATIVE POSE','8X REFERENCE','GPT REDRAW']","['MODEL SHEET','GPT REDRAW','FINAL SPRITE']")
a=s.index('def pair(');z=s.index('\ndef mosaic(',a)
s=s[:a]+'''@lru_cache(None)
def states(name):
 return list(csv.DictReader(open(CAP/os.environ.get('MT_TAKE','final')/name/'state.csv')))
def tracked(name,idx,w,h):
 r=clip(name);im=r.frame(idx);rs=states(name);row=rs[min(idx,len(rs)-1)]
 x=float(row['x'])-float(row['cam_x']);y=float(row['y'])-float(row['cam_y'])
 # Recenter the entire native viewport in a padded plane, then choose the pane.
 pad=Image.new('RGB',(960,672),(8,16,56));pad.paste(im,(320,224))
 return arr(game_view(pad,320+x,224+y,1, w,h))
def pair(f,s,e,left,right,labels):
 names=[left.path.parent.name,right.path.parent.name] if False else []
 # Frames objects retain the directory under .dir (resolved below).
 names=[Path(left.folder).parent.name,Path(right.folder).parent.name]
 sh=(e.H-10)//2;c=stripes(e,f)
 for k,name in enumerate(names):
  t=s.f0+k*22
  if f<t:continue
  q=tracked(name,30+f-t,e.W,sh)
  c[k*(sh+10):k*(sh+10)+sh]=q
  pill=chip(labels[k]);paste(c,pill,40,k*(sh+10)+sh-pill.shape[0]-24)
 return c
''' +s[z:]
# Replace red-tab header by complete native-colour lower band, clear of upper HUD.
a=s.index('  h=Header(');z=s.index(' e.O(Fade(',a)
s=s[:a]+'''  class Band(Overlay):
   def draw(self,c,f,e):
    h=160 if not V else 140;y=e.H-h-24
    u=min(1,(f-self.f0)/12,(self.f1-f)/12);x=int(-e.W*(1-ease_out(u)))
    plate=Image.new('RGBA',(e.W,h),(8,36,146,255));d=ImageDraw.Draw(plate)
    d.rectangle((0,0,48,h),fill=(255,36,36,255));d.rectangle((48,h-12,e.W,h),fill=(255,219,36,255))
    paste(c,rgba_of(plate),x,y);q=native(self.words,3 if V else 4);paste(c,q,x+80,y+(h-q.shape[0])/2-6)
  h=Band(sec(a),sec(z));h.words=words;e.O(h)
''' + s[z:]
# Ring accents are editorial title/layout stingers, not implied pickups; remove ambiguous ones.
s=s.replace(" e.X(b(56),P/'music/s3k-sfx-33-paced.wav',2.2)"," # No fabricated pickup or jump sounds.").replace(" e.X(b(57),P/'music/s3k-sfx-34-paced.wav',2.2)","")
p.write_text(s)
