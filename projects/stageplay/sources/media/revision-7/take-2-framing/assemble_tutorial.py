#!/usr/bin/env python3
"""Build a first-creator Stageplay tutorial/promo at native cadence.
Audience: first-time creators. Form: directing notes beside real authored LIVE footage.
Promise: turn a simple relationship into a scene using set, cast and directing tracks.
Story: Sonic races ahead, hears Tails, returns, then counts them into a shared crossing.
Hero: the final crossing together; the complete 26-second short closes the lesson.
Sound: one uninterrupted ROM-rendered DEZ2 bed for instruction; native story soundtrack
for its screening; a deliberate musical reprise for the end card. No voice or second bed.
Palette: deep blue, cream, violet and gold from Death Egg and the dialogue panels.
Type: supplied Fira Sans Compressed Heavy Italic and Fira Sans Medium (SIL OFL 1.1).
Reference: Slay the Robotnik's code/live-view hierarchy, adapted to calm instructional pacing.
End card: sample location, project URL, development status and fan-project/ROM notice.
Origin: OpenGGF Stageplay tutorial, 2026-10-22. Requires FFmpeg, Pillow, source movies/JSONL.
All notes/timeline/target outlines are editorial diagrams, NOT a simulated editor interface.
"""
import argparse,hashlib,io,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1600,1120,60
CREAM='#fff1cf'; GOLD='#ffc65c'; BLUE='#102238'; MUTED='#aac2d6'; AQUA='#73d5df'
# out duration, source start, source kind, chapter title, instructional rows
EDL=[
 (6,5.5,'story','MAKE A SCENE.',[]),
 (11,0,'clean','01  GIVE IT A REASON', [('GOAL','Reach the other lift. Together.'),('PROBLEM','Sonic turns it into a race.'),('CHANGE','He comes back for his friend.')]),
 (12,0,'clean','02  CHOOSE SET + CAST',[('SET','Death Egg · Act 2'),('WORLD: LIVE','The level’s own moving objects.'),('CAST: PUPPET','Sonic + Tails. Native physics.')]),
 (12,2,'clean','03  DIRECT THE MOVEMENT',[('MOVE_TO','Aim Sonic at the other platform.'),('URGENCY: 0.65','Request 65% of native run speed.'),('JUMP','Hold for 20 frames. Physics takes over.')]),
 (12,14,'clean','04  WAIT FOR THE RESULT',[('WAIT: ON_OBJECT','Wait until the actor is on the lift.'),('THEN: STOP','Brake after landing, not mid-jump.'),('CHECK THE PREVIEW','A destination is an attempt, not a teleport.')]),
 (12,4,'clean','05  KEEP BOTH IN FRAME',[('FOLLOW','Choose Sonic AND Tails.'),('SMOOTHING: 0.2','The camera responds to real positions.'),('HOLD ZOOM AT 1','Let framing and movement tell the story.')]),
 (12,8,'story','06  GIVE THEM A VOICE',[('SPEAKER: TAILS','A name and pointer identify the line.'),('REVEAL: GRADUAL','Two frames per character in this scene.'),('LEAVE READING TIME','Let the reply change what happens next.')]),
 (10,8,'clean','07  PREVIEW, THEN SHARE',[('WATCH THE WHOLE SCENE','Check landings, framing and reading time.'),('SAVE: .stageplay','One scene format for both editors.'),('START FROM THE SAMPLE','wait-for-me.stageplay')]),
 (3,0,'clean','WAIT FOR ME',[]),
 (26,0,'story','The finished short',[]),
 (8,18,'clean','YOUR TURN TO DIRECT.',[])
]

def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-5000:])
 return p.stdout

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def font(path,size):return ImageFont.truetype(str(path),size)

def text(d,xy,s,f,fill=CREAM,maxw=None,stroke=0):
 box=d.textbbox(xy,s,font=f,anchor='lt',stroke_width=stroke)
 if maxw is not None and box[2]-xy[0]>maxw:raise ValueError('Text overflows: '+s)
 d.text(xy,s,font=f,anchor='lt',fill=fill,stroke_width=stroke,stroke_fill='#081020')

def wrap(d,s,f,maxw):
 lines=[];line=''
 for word in s.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=f)>maxw and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 return lines

def timeline(d,screenplay):
 text(d,(48,925),'THE SCENE’S TRACKS',font(BODY,22),MUTED)
 text(d,(1300,925),'26 SECONDS',font(BODY,22),GOLD)
 x0,x1=212,1530
 tracks=[('SONIC',980,'#7798ff'),('TAILS',1012,GOLD),('CAMERA',1044,AQUA),('DIALOGUE',1076,'#ddd5ed')]
 for name,y,col in tracks:
  text(d,(48,y-6),name,font(BODY,18),col);d.rounded_rectangle((x0,y,x1,y+12),6,fill='#263d50')
 shot=screenplay['shots'][0]
 for name,y,col in tracks[:2]:
  for a in shot['actions'][name.lower()]:
   if a['kind']=='MOVE_TO':
    x=x0+a['frame']/1560*(x1-x0);d.rounded_rectangle((x,y,x+50,y+12),4,fill=col)
 d.rounded_rectangle((x0,1044,x1,1056),4,fill=AQUA)
 for a in shot['dialogue']:
  d.rounded_rectangle((x0+a['startFrame']/1560*(x1-x0),1076,x0+a['endFrame']/1560*(x1-x0),1088),4,fill='#ddd5ed')

def card(k,path,screenplay):
 duration,source,kind,title,rows=EDL[k]
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 if rows:
  for y in range(H):d.line((0,y,W,y),fill=(11+int(y/H*5),24+int(y/H*12),42+int(y/H*16),255))
  for x in range(-H,W,150):d.polygon([(x,0),(x+10,0),(x+H+10,H),(x+H,H)],fill=(23,46,65,255))
  d.rectangle((0,0,W,156),fill='#0b182a');d.rectangle((48,150,1552,155),fill=GOLD)
  text(d,(48,26),'OPENGGF STAGEPLAY  /  A FIRST SCENE',font(BODY,24),GOLD)
  text(d,(48,65),title,font(TITLE,74),maxw=1504,stroke=2)
  text(d,(600,179),'LIVE SCENE  /  AUTHORED PERFORMANCE',font(BODY,23),MUTED)
  d.rectangle((594,214,1566,898),fill=GOLD);d.rectangle((600,220,1559,891),fill=(0,0,0,0))
  # Notes are stable while the native performance advances.
  for i,(label,body) in enumerate(rows):
   yy=240+i*204
   text(d,(48,yy),label,font(TITLE,34),GOLD,maxw=510)
   for j,line in enumerate(wrap(d,body,font(BODY,31),500)):
    text(d,(48,yy+53+j*42),line,font(BODY,31),maxw=500)
  footer={1:'A goal → a mistake → a changed choice.',2:'Poser mode keeps manual poses and frames.',3:'Explicit routes and jumps; no automatic pathfinder.',4:'This wait has a finite 180-frame timeout.',5:'Fixed pixel scale. No animated zoom.',6:'Dialogue belongs on the dialogue track.',7:'In-engine workspace + OpenGGF Editor.'}[k]
  for j,line in enumerate(wrap(d,footer,font(BODY,22),510)):text(d,(48,853+j*29),line,font(BODY,22),MUTED)
  timeline(d,screenplay)
 elif k==9:
  return None
 else:
  # Full moving footage remains visible below a compact top shade.
  bottom=440 if k==10 else 285
  for y in range(bottom):d.line((0,y,W,y),fill=(7,18,34,int(230*(1-y/bottom)**.6)))
  d.polygon([(38,47),(48,47),(35,162),(25,162)],fill=GOLD)
  text(d,(65,48),title,font(TITLE,116),stroke=4,maxw=1480)
  if k==0:
   text(d,(70,187),'A small story. The tools to direct it.',font(BODY,35),stroke=1)
  elif k==8:
   text(d,(70,187),'THE FINISHED SCENE  /  WATCH IT ALL COME TOGETHER',font(BODY,29),GOLD,stroke=1)
  else:
   for y,s,size,col in [(190,'Start with wait-for-me.stageplay in examples/stageplay-demo.',30,CREAM),(238,'In-engine workspace · OpenGGF Editor · Script authoring',29,GOLD),(288,'github.com/OpenGGF/OpenGGF   /   Development preview',29,CREAM),(342,'Fan-made and free. Not affiliated with SEGA. Requires your own ROM.',25,CREAM)]:
    text(d,(70,y),s,font(BODY,size),col,maxw=1460,stroke=1)
 im.save(path);return path

def ass_time(frame):
 cs=round(frame*100/60);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def target_outline(path,rows,start,frames):
 header='[Script Info]\nScriptType: v4.00+\nPlayResX: 1600\nPlayResY: 1120\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Fira Sans,24,&H005CC6FF,&H005CC6FF,&H00201008,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,0,0,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
 out=[]
 for f in range(frames):
  s=rows[start+f]['sample'];o=next(o for o in s['world']['objects'] if o['layoutIndex']==166)
  x=600+3*(o['x']-s['camera']['x']-32);y=220+3*(o['y']-s['camera']['y']-16)
  out.append(f'Dialogue: 0,{ass_time(f)},{ass_time(f+1)},Default,,0,0,0,,{{\\an7\\pos({round(x)},{round(y)})\\p1\\bord0}}m 0 0 l 38 0 38 4 4 4 4 25 0 25 m 192 0 l 154 0 154 4 188 4 188 25 192 25 m 0 96 l 0 71 4 71 4 92 38 92 38 96 m 192 96 l 154 96 154 92 188 92 188 71 192 71\n')
 path.write_text(header+''.join(out))

def main():
 global TITLE,BODY
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--cards-only',action='store_true')
 p.add_argument('--title-font',type=Path,default=Path('/usr/share/fonts/TTF/FiraSansCompressed-HeavyItalic.ttf'));p.add_argument('--body-font',type=Path,default=Path('/usr/share/fonts/TTF/FiraSans-Medium.ttf'))
 a=p.parse_args();root=a.root.resolve();TITLE=a.title_font;BODY=a.body_font
 screenplay=json.loads((root/'wait-for-me.screenplay.json').read_text());rows=[json.loads(l) for l in (root/'wait-for-me.jsonl').open()]
 output=root/'stageplay-first-scene-tutorial.mp4'
 if output.exists() and not a.cards_only:raise ValueError('Refusing to replace '+str(output))
 cards=root/'cards';cards.mkdir(exist_ok=True)
 for k in range(len(EDL)):card(k,cards/f'{k:02}.png',screenplay)
 if a.cards_only:return
 chapters=[];at=0
 with tempfile.TemporaryDirectory(prefix='tutorial-encode-',dir=root) as temp:
  tmp=Path(temp);parts=[]
  for k,(duration,source,kind,title,note) in enumerate(EDL):
   print(f'Rendering {k+1}/{len(EDL)}: {title}',flush=True)
   movie=root/('wait-for-me.mkv' if kind=='story' else 'directing-view.mkv');part=tmp/f'{k:02}.mkv';parts.append(part)
   cmd=['ffmpeg','-v','error','-nostdin','-n','-ss',str(source),'-i',str(movie)]
   overlay=cards/f'{k:02}.png';has=overlay.exists()
   if has:cmd+=['-loop','1','-framerate','60','-i',str(overlay)]
   filters=[]
   if note:
    filters+=['[0:v]scale=960:672:flags=neighbor,setsar=1,pad=1600:1120:600:220:color=0x0b182a[base]','[base][1:v]overlay=0:0:shortest=1[card]']
    # Actual scene time, not output-film time; no gameplay retiming.
    filters+=['color=c=white:s=4x118:r=60[marker]',f"[card][marker]overlay=x='212+({source}+t)/26*1318':y=976:shortest=1[marked]"]
    last='marked'
    if k==3:
     outline=tmp/'destination.ass';target_outline(outline,rows,round(source*60),duration*60)
     filters+=[f'[{last}]ass={outline}[outlined]'];last='outlined'
   else:
    filters+=['[0:v]scale=1600:1120:flags=neighbor,setsar=1[base]'];last='base'
    if has:
     filters+=['[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[title]',"[base][title]overlay=x='-32*pow(max(0,1-t/0.25),3)':y=0:shortest=1[titled]"];last='titled'
   filters+=[f'[{last}]format=yuv420p[v]']
   cmd+=['-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[v]','-an','-t',str(duration),'-r','60','-c:v','ffv1','-level','3','-threads','4',str(part)]
   run(cmd)
   chapters.append(dict(startFrame=at,endFrame=at+duration*60,title=title,source=movie.name,sourceStartFrame=round(source*60),sourceEndFrame=round((source+duration)*60),sourceKind='authored Stageplay LIVE',layout='directing notes' if note else 'full scene'))
   at+=duration*60
  concat=tmp/'parts.txt';concat.write_text(''.join("file '"+str(x)+"'\n" for x in parts))
  metadata=tmp/'chapters.ffmeta';metadata.write_text(';FFMETADATA1\ntitle=Your first scene — OpenGGF Stageplay\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/60\nSTART={c["startFrame"]}\nEND={c["endFrame"]}\ntitle={c["title"]}\n' for c in chapters))
  # Tutorial 0..90, uninterrupted final story 90..116, eight-second end card.
  audio='[1:a]atrim=0:90,asetpts=PTS-STARTPTS,volume=3dB,afade=t=out:st=89.5:d=0.5[a];[2:a]atrim=0:26,asetpts=PTS-STARTPTS,volume=6dB,afade=t=in:st=0:d=0.15,afade=t=out:st=25.7:d=0.3[b];[1:a]atrim=90:98,asetpts=PTS-STARTPTS,volume=3dB,afade=t=in:st=0:d=0.3,afade=t=out:st=6.5:d=1.5[c];[a][b][c]concat=n=3:v=0:a=1[audio]'
  run(['ffmpeg','-v','error','-nostdin','-n','-f','concat','-safe','0','-i',str(concat),'-i',str(root/'music-bed.mkv'),'-i',str(root/'wait-for-me.mkv'),'-f','ffmetadata','-i',str(metadata),'-filter_complex_threads','1','-filter_complex',audio,'-map','0:v:0','-map','[audio]','-map_metadata','3','-map_chapters','3','-c:v','libx264','-preset','medium','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(at/60),'-movflags','+faststart',str(output)])
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2)+'\n')
 (root/'assembly.json').write_text(json.dumps(dict(frames=at,fps=60,width=W,height=H,chapters=chapters,sourceHashes={p.name:sha(p) for p in [root/'wait-for-me.mkv',root/'directing-view.mkv',root/'music-bed.mkv',TITLE,BODY]},outputSha256=sha(output),overlayMeaning='Editorial directing notes, actual scene-time track diagram and measured moving target outline; not editor UI.',sound='One 90-second ROM bed, then 26-second native story soundtrack, then 8-second bed reprise. No voiceover.'),indent=2)+'\n')
 print(json.dumps({'output':str(output),'duration':at/60,'frames':at}),flush=True)
if __name__=='__main__':main()
