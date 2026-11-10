from pathlib import Path
P=Path(__file__).parent;p=P/'edit/edit.py';s=p.read_text()
s=s.replace('phase-one local rough cut','phase-two showcase').replace("hero=clip('hero','revision2')","hero=clip('hero-mgz2')").replace("data=clip('data-select','revision2')","data=clip('data-select-team')").replace("'rough-9x16.mp4' if V else 'rough-16x9.mp4'","'master-9x16.mp4' if V else 'master-16x9.mp4'")
s=s.replace(" # A true source-to-redraw", """ if u>.55:
  # Binding model sheet -> enlarged pose -> strip; editorial source imagery.
  paths=[ROOT/'examples/mica-and-talon/concept/mica.png',ROOT/'examples/mica-and-talon/art/mica/frames/wait-00.png']
  boxes=[(40,260,980,600),(40,900,440,620),(540,1080,480,420)] if V else [(40,180,780,650),(870,180,400,650),(1300,180,580,650)]
  sheet=picture(str(paths[0])).copy();sheet.thumbnail((boxes[0][2],boxes[0][3]),Image.Resampling.LANCZOS)
  pose=picture(str(paths[1]));pose=pose.crop(pose.getbbox());pose=pose.resize((pose.width*12,pose.height*12),Image.Resampling.NEAREST)
  for im,box in zip([sheet,pose],boxes):paste(c,arr(im),box[0]+(box[2]-im.width)/2,box[1]+(box[3]-im.height)/2)
  strip=Image.new('RGBA',(150,50));
  for i,n in enumerate(['wait-00','walk-00','walk-01']):
   q=picture(str(ROOT/f'examples/mica-and-talon/art/mica/frames/{n}.png'));q=q.crop(q.getbbox());strip.paste(q,(i*50,50-q.height),q)
  strip=strip.resize((600,200),Image.Resampling.NEAREST);box=boxes[2];paste(c,arr(strip),box[0]+(box[2]-600)/2,box[1]+200)
  for title,box in zip(['MODEL SHEET','ENLARGED POSE','SPRITE STRIP'],boxes):label(c,title,box[0],box[1]-60,40)
  label(c,'EDITORIAL / FRAME-BY-FRAME ORIGINAL ART',40,e.H-100,36)
  return c
 # A true source-to-redraw""")
a=s.index('def mosaic(');z=s.index('\ndef code(',a)
s=s[:a]+'''def mosaic(f,s,e):
 cells=[('HUD',clip('talon-s2'),80,(0,74)),('SIGNPOST',finish,350,(80,60)),('RESULTS',clip('gilded-clear-low'),650,(80,22)),('HALF PIPE',clip('halfpipe-component'),300,(80,70)),('BLUE SPHERE',clip('blue-play'),200,(80,48)),('CONTINUE',clip('continue'),80,(80,64)),('DATA SELECT',data,480,(100,30)),('ENDING',clip('ending-full'),2700,(80,60))]
 cols,rows=(2,4) if V else (4,2);w=e.W//cols;h=e.H//rows;c=stripes(e,f)
 for i,(name,r,src,(cx,cy))in enumerate(cells):
  if f<s.f0+i*22:continue
  x=i%cols*w;y=i//cols*h;im=r.frame(src+f-s.f0)
  # Exactly 3x native; subject crops preserve readable pixels inside eight cells.
  cw=(w-12)//3;ch=(h-70)//3;cx=min(cx,320-cw);cy=min(cy,224-ch)
  im=im.crop((cx,cy,cx+cw,cy+ch)).resize((cw*3,ch*3),Image.Resampling.NEAREST)
  paste(c,arr(im),x+6,y+6)
  label(c,name,x+18,y+h-58,36)
 return c
''' + s[z:]
# Continuous cold-open chain exits before damage, then an explicit title drop.
s=s.replace('Game(0,b(16),hero,src=30','Game(0,b(8),hero,src=15').replace('Custom(b(16),sec(12.86),title','Custom(b(8),sec(12.86),title').replace('Flash(b(16),16)','Flash(b(8),16)').replace("e.X(b(16),P/", "e.X(b(8),P/").replace('Txt(b(6),b(14)','Txt(b(4),b(8)')
# Homing full screen uses approach then the triple pops, no tail after damage.
s=s.replace('Game(b(71),b(83),hero,src=35','Game(b(71),b(83),hero,src=0')
s=s.replace("pair(f,s,e,hero,gilded", "pair(f,s,e,clip('hero'),gilded")
a=s.index(" lines=(ROOT/");z=s.index(" e.S(Game(sec(61.74)",a)
s=s[:a]+''' # Exact MicaMod.java call, whitespace wrapped and enlarged for the final panel.
 lines=[('n','context.registerCharacter('),('n','    "mica",'),('n','    MicaCharacter.definition('),('n','        context.modId(),'),('n','        materialized, presentation,'),('n','        micaGilded));')]
 e.O(Typed(b(147)+18,sec(61.74),lines,50,150 if V else 530,w=980,h=390,cps=55,title='MicaMod.java / actual registration'))
''' +s[z:]
a=s.index(' e.S(Game(sec(61.74)');z=s.index(' e.S(Custom(sec(73.13)',a)
s=s[:a]+''' e.S(Game(sec(61.74),sec(76.74),clip('gilded-clear-low'),src=70,cam=cam_move((160,112,1),(160,112,1.04)),trans='wipe',tdur=16))
''' +s[z:]
s=s.replace('sec(73.13)','sec(76.74)').replace('b(220)','sec(84.8)').replace('b(218)','sec(83.8)')
s=s.replace('PHASE 1 ROUGH / POSITIONED GAMEPLAY','POSITIONED GAMEPLAY / EDITORIAL SHOWCASE')
s=s.replace("text('PHASE", "text('PHASE")
p.write_text(s)
# Keep original outputs; give phase 2 its own render destinations.
p=P/'render_all.py';s=p.read_text().replace('rough-9x16.mp4','master-9x16.mp4').replace('rough-16x9.mp4','master-16x9.mp4').replace('volume=-4dB','volume=-5dB');p.write_text(s)
