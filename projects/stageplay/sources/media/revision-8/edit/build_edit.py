#!/usr/bin/env python3
"""First-time creators; authored LIVE story → one continuous rehearsal → real A/B.
Promise: direct a relationship through timing, native movement and a visible result.
Hero: a shared crossing. Sound: one continuous ROM bed plus separate native SFX.
Palette: navy/cream/gold. Type: heavy condensed Fira. No simulated editor interface.
Origin: Stageplay revision eight, 2026-10-22. Requires Python/Pillow and FFmpeg.
"""
import argparse,json,subprocess,tempfile,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1920,1080,60
TITLE=Path('/usr/share/fonts/TTF/FiraSansCompressed-HeavyItalic.ttf')
BODY=Path('/usr/share/fonts/TTF/FiraSans-Medium.ttf')
GOLD='#ffc65c'; CREAM='#fff1cf'; MUTED='#aac2d6'
def run(cmd):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
 return p.stdout

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))
def put(d,xy,s,size=40,color=CREAM,title=False,width=510,bottom=H):
 f=ImageFont.truetype(str(TITLE if title else BODY),size); lines=[]; line=''
 for word in s.replace('/', '/ ').split():
  t=(line+' '+word).strip()
  if d.textlength(t,font=f)>width and line: lines.append(line);line=word
  else:line=t
 if line:lines.append(line)
 for i,l in enumerate(lines):
  if d.textlength(l,font=f)>width:raise ValueError('Unbreakable text exceeds column: '+l)
  pos=(xy[0],xy[1]+i*(size+12))
  if d.textbbox(pos,l,font=f,anchor='lt')[3]>bottom:
   raise ValueError(f'Text exceeds bottom bound {bottom}: {s}')
  d.text(pos,l,font=f,fill=color,anchor='lt')
 return xy[1]+len(lines)*(size+12)
def card(path,mode,title,body='',command='',end=None):
 im=Image.new('RGBA',(W,H),'#102238');d=ImageDraw.Draw(im)
 # Architectural margin with restrained diagonal beams, never overlays actors.
 for x in range(-1080,1920,240):d.polygon([(x,0),(x+12,0),(x+1092,H),(x+1080,H)],fill='#183249')
 x=320 if mode=='story' else 40
 d.rectangle((x-4,88,x+1283,991),fill=GOLD);d.rectangle((x,92,x+1279,987),fill=(0,0,0,0))
 if mode=='story':
  put(d,(320,24),'WAIT FOR ME',46,GOLD,True,1280)
  put(d,(320,1010),'OpenGGF Stageplay · An authored native performance',28,MUTED,width=1280)
 else:
  put(d,(40,30),'YOUR FIRST SCENE  /  OPENGGF STAGEPLAY',34,GOLD,True,1280)
  limit=900 if end is not None else 988
  y=put(d,(1360,126),title,64,GOLD,True,bottom=limit)
  y=put(d,(1360,y+42),body,42,width=510,bottom=limit)
  if command:
   d.rectangle((1360,y+44,1870,y+48),fill=GOLD)
   put(d,(1360,y+78),command,34,MUTED,width=510,bottom=limit)
  if end is None:put(d,(40,1016),'DIRECTING NOTES · editorial annotations',27,MUTED,width=1280)
 if end is not None:
  # Endcard uses side column plus the generous lower editorial margin.
  put(d,(40,1008),end.get('url','github.com/OpenGGF/OpenGGF'),28,GOLD,width=1260,bottom=1044)
 im.save(path)

def main():
 global TITLE,BODY
 p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--font-dir',type=Path,help='Directory containing FiraSansCompressed-HeavyItalic.ttf and FiraSans-Medium.ttf');p.add_argument('--music',type=Path,required=True);p.add_argument('--previews-only',action='store_true');p.add_argument('--standalone',action='store_true');p.add_argument('--pause-frames',type=int,default=360);p.add_argument('--music-gain-db',type=float,default=0);p.add_argument('--sfx-gain-db',type=float,default=0);a=p.parse_args()
 if a.font_dir:
  TITLE=a.font_dir/'FiraSansCompressed-HeavyItalic.ttf';BODY=a.font_dir/'FiraSans-Medium.ttf'
 root=a.manifest.resolve().parent;m=json.loads(a.manifest.read_text());out=a.out.resolve()
 if out.exists():raise ValueError('Use a new take directory; refusing overwrite')
 out.mkdir(parents=True)
 if m.get('fps',m.get('FPS',60))!=60:raise ValueError('Expected every-frame 60Hz source')
 paths=m['paths'];src={k:(root/v).resolve() for k,v in paths.items() if isinstance(v,str)}
 story=int(m['storyFrames']);total=int(m['totalFrames']);notes=m['tutorialNotes'];c=m['comparison'];end=m.get('endcard',{})
 if not notes or notes[0]['startFrame']!=0 or notes[-1]['endFrame']!=story:raise ValueError('Notes must partition entire clean pass')
 for i,n in enumerate(notes):
  if n['endFrame']<=n['startFrame'] or (i and notes[i-1]['endFrame']!=n['startFrame']):raise ValueError('Gap/overlap in tutorialNotes')
 tail=int(end.get('frames',480))
 if total-story<tail:raise ValueError('Missing NEW moving tail for endcard')
 segments=[]
 def add(key,start,frames,title,body='',command='',mode='notes',freeze=False,sfx=True):
  segments.append(dict(key=key,source=str(src[key]),sourceStartFrame=start,sourceEndFrame=start+(1 if freeze else frames),frames=frames,title=title,body=body,command=command,mode=mode,instructionalFreeze=freeze,sfx=sfx))
 add('story',0,story,'The finished short',mode='story')
 if a.pause_frames:
  add('clean',0,a.pause_frames,'DIRECT A CHOICE','Watch how a reply changes Sonic’s next move. Then change one setting.','PAUSED REHEARSAL · scene frame 0',freeze=True,sfx=False)
 for n in notes:
  key=n.get('source','clean')
  if key not in ('clean','story'):raise ValueError('Tutorial note source must be clean or matched story')
  add(key,n['startFrame'],n['endFrame']-n['startFrame'],n['title'],n['body'],n.get('command',''))
 count=c['endFrame']-c['startFrame']
 add('clean',c['startFrame'],count,c.get('labelA','A · ORIGINAL'),c['change'],c.get('commandA',''))
 add('comparison',c.get('variantStartFrame',c['startFrame']),count,c.get('labelB','B · ONE CHANGE'),c['outcome'],c.get('commandB',''))
 add('clean',story,tail,'YOUR TURN.','Open the sample. Change one timing. Preview the whole scene.',end.get('samplePath','examples/stageplay-demo/wait-for-me.stageplay'))
 # Long legal/status content gets a separate readable end overlay beside NEW tail.
 at=0;edl=[]
 for i,s in enumerate(segments):
  s['startFrame']=at;at+=s['frames'];s['endFrame']=at;s['sourceKind']='authored Stageplay LIVE';s['playbackRate']=0 if s['instructionalFreeze'] else 1
  overlay=out/f'layout-{i:02}.png';card(overlay,s['mode'],s['title'],s['body'],s['command'],end if i==len(segments)-1 else None);s['overlay']=str(overlay);edl.append(s)
 # Legal line lives outside viewport, and is available the entire eight-second ending.
 im=Image.open(edl[-1]['overlay']);d=ImageDraw.Draw(im)
 put(d,(1360,922),end.get('status','Development preview'),30,GOLD,bottom=988)
 put(d,(40,1048),'Fan-made and free. Not affiliated with SEGA. Requires your own ROM.',23,width=1840);im.save(edl[-1]['overlay'])
 (out/'chapters.json').write_text(json.dumps(edl,indent=2)+'\n')
 (out/'plan.json').write_text(json.dumps(dict(fps=FPS,width=W,height=H,frames=at,seconds=at/FPS,manifest=str(a.manifest.resolve()),provisional=m.get('provisional',False),audio='One continuous ROM bed. Only explicit SFX paths; never combined capture audio.',music=str(a.music.resolve()),musicGainDb=a.music_gain_db,sfxGainDb=a.sfx_gain_db),indent=2)+'\n')
 if a.previews_only:return
 if at/FPS>float(probe(a.music)['format']['duration']):raise ValueError('Music too short; looping/restart forbidden')
 for key in {s['key'] for s in segments}:
  v=next(x for x in probe(src[key])['streams'] if x['codec_type']=='video')
  if int(v['width'])*224!=int(v['height'])*320:raise ValueError('Native aspect mismatch '+key)
  if v['avg_frame_rate'] not in ('60/1','60000/1000'):raise ValueError('Source cadence must be 60Hz '+key)
  needed=max(s['sourceEndFrame'] for s in segments if s['key']==key)
  if float(probe(src[key])['format']['duration'])+1/FPS<needed/FPS:raise ValueError('Source interval beyond EOF '+key)
 with tempfile.TemporaryDirectory(prefix='encode-',dir=out) as td:
  tmp=Path(td);parts=[];audios=[]
  for i,s in enumerate(segments):
   print(f"Normalize {i+1}/{len(segments)}: {s['title']}",flush=True)
   part=tmp/f'{i:02}.mkv';parts.append(part)
   # Frame trim is exact; freeze is a documented single frame held by tpad.
   trim=f"trim=start_frame={s['sourceStartFrame']}:end_frame={s['sourceEndFrame']},settb=1/60,setpts=N"
   if s['instructionalFreeze']:trim+=f",tpad=stop_mode=clone:stop_duration={s['frames']/FPS}"
   x=320 if s['mode']=='story' else 40
   vf=f'[0:v]{trim},scale=1280:896:flags=neighbor,setsar=1[game];[1:v]settb=1/60,setpts=N[plate];[plate][game]overlay={x}:92:shortest=1,format=yuv420p[v]'
   run(['ffmpeg','-v','error','-nostdin','-n','-i',s['source'],'-loop','1','-framerate','60','-i',s['overlay'],'-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-an','-frames:v',s['frames'],'-c:v','ffv1','-level','3','-threads','4',part])
   stem=src.get('comparisonSfx') if s['key']=='comparison' else src.get('sfx')
   audio=tmp/f'a{i:02}.wav';audios.append(audio)
   if stem and s['sfx']:
    run(['ffmpeg','-v','error','-nostdin','-n','-i',stem,'-af',f"atrim=start={s['sourceStartFrame']/FPS}:end={s['sourceEndFrame']/FPS},asetpts=PTS-STARTPTS,apad",'-t',s['frames']/FPS,'-ar','48000','-ac','2','-c:a','pcm_s16le',audio])
   else:run(['ffmpeg','-v','error','-nostdin','-n','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',s['frames']/FPS,'-c:a','pcm_s16le',audio])
  def listing(name,items):
   f=tmp/name;f.write_text(''.join("file '"+str(v).replace("'","'\\''")+"'\n" for v in items));return f
  video=listing('video.txt',parts);audio=listing('audio.txt',audios)
  meta=tmp/'chapters.ffmeta';meta.write_text(';FFMETADATA1\ntitle=Your first scene — OpenGGF Stageplay\n'+''.join(f"[CHAPTER]\nTIMEBASE=1/60\nSTART={s['startFrame']}\nEND={s['endFrame']}\ntitle={s['title']}\n" for s in segments))
  # Fixed shared gains, no per-section normalization or bed resets. Limiter supplies headroom.
  af=f'[1:a]atrim=duration={at/FPS},asetpts=PTS-STARTPTS,volume={a.music_gain_db}dB,afade=t=out:st={at/FPS-1.5}:d=1.5[bed];[2:a]volume={a.sfx_gain_db}dB[sfx];[bed][sfx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=false[a]'
  run(['ffmpeg','-v','error','-nostdin','-n','-f','concat','-safe','0','-i',video,'-i',a.music,'-f','concat','-safe','0','-i',audio,'-f','ffmetadata','-i',meta,'-filter_complex_threads','1','-filter_complex',af,'-map','0:v','-map','[a]','-map_metadata','3','-map_chapters','3','-c:v','libx264','-preset','medium','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-r','60','-frames:v',at,'-t',at/FPS,'-movflags','+faststart',out/'tutorial.mp4'])
 if a.standalone:
  run(['ffmpeg','-v','error','-nostdin','-n','-i',src['story'],'-i',out/'layout-00.png','-filter_complex_threads','1','-filter_complex','[0:v]settb=1/60,setpts=N,scale=1280:896:flags=neighbor[g];[1:v]settb=1/60,setpts=N[plate];[plate][g]overlay=320:92[v]','-map','[v]','-map','0:a?','-t',story/FPS,'-c:v','libx264','-preset','medium','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',out/'finished-short.mp4'])
 print(json.dumps({'output':str(out/'tutorial.mp4'),'frames':at,'seconds':at/FPS}))
if __name__=='__main__':main()
