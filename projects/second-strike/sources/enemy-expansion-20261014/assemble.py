#!/usr/bin/env python3
"""Build the 14.5-second Second Strike enemy-change reel at recorded speed.
Inputs: local captures/{guard,plant,caterkiller}/frames, music/music.wav, ffmpeg,
DejaVu Sans fonts. Output: second-strike-changes.mp4. Origin: a8221fb7d/2026-10-14.
All video normalizes losslessly before one final H.264 encode. No ambient display.
"""
from pathlib import Path
import csv,json,subprocess,os,sys,hashlib

HERE=Path(os.environ.get('SECOND_STRIKE_MEDIA_ROOT',Path(__file__).resolve().parent)).resolve()
ENGINE=Path(os.environ.get('OPENGGF_ROOT',Path.home()/'code/projects/OpenGGF')).resolve()
FONT=Path(os.environ.get('SECOND_STRIKE_FONT','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
BOLD=FONT.with_name('DejaVuSans-Bold.ttf')
FPS=60
SHOTS=[
 dict(act=1,route_order=1,name='guard',title='FASTER. LONGER. ARMORED.',detail='225px charge. Invulnerable during the dash.',start_frame=15,end_frame=285,crop=None),
 dict(act=1,route_order=2,name='plant',title='WIDER SPRAY. LESS ROOM.',detail='20 seeds in two releases.',start_frame=15,end_frame=225,crop=None),
 dict(act=1,route_order=3,name='caterkiller',title='DOUBLE-LENGTH CATERKILLERS',detail='12 body segments. Native movement.',start_frame=60,end_frame=360,crop='crop=528:224:0:0'),
]

def ffmpeg(*args):
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True,timeout=240)

def textfile(name,text):
 p=HERE/'labels'/name;p.parent.mkdir(exist_ok=True);p.write_text(text+'\n');return p

def label(path,x,y,size=32,bold=False,color='white'):
 return f"drawtext=fontfile='{BOLD if bold else FONT}':textfile='{path}':x={x}:y={y}:fontsize={size}:fontcolor={color}:expansion=none"

def build():
 segments=HERE/'encoding';segments.mkdir(exist_ok=True)
 title=textfile('title.txt','SECOND STRIKE')
 feature=textfile('edition.txt','ENEMY EXPANSION')
 rows=[];chapters=[];offset=0;paths=[]
 for index,shot in enumerate(SHOTS):
  src=HERE/'captures'/shot['name'];states=list(csv.DictReader((src/'state.csv').open()))
  start,end=shot['start_frame'],shot['end_frame']
  assert 0<=start<end<=len(states)
  assert all(row['dead']=='0' for row in states[start:end]),'No fatal take in final selections'
  assert all((src/'frames'/f'{f:05d}.png').exists() for f in range(start,end))
  head=textfile(f'{index}-headline.txt',shot['title']);detail=textfile(f'{index}-detail.txt',shot['detail'])
  number=textfile(f'{index}-number.txt',f'{index+1:02d} / 03')
  setup=textfile(f'{index}-setup.txt','POSITIONED GAMEPLAY' if shot['name']!='caterkiller' else 'POSITIONED FIRE-CONTINUATION DEMO')
  filters=[shot['crop']] if shot['crop'] else []
  filters += ['scale=iw*3:ih*3:flags=neighbor','pad=1600:900:(ow-iw)/2:114:color=0x101928',
    'drawbox=x=40:y=83:w=96:h=4:color=0xff963f:t=fill',
    label(title,40,23,36,True),label(feature,1100,30,22,False,'0xb7c7d8'),label(number,1450,63,18,True,'0xffb566'),
    label(head,40,805,34,True),label(detail,40,853,22),label(setup,1030,861,15,False,'0x9cadc1')]
  dest=segments/f'{index:02d}.mkv'
  ffmpeg('-framerate',FPS,'-start_number',start,'-i',src/'frames/%05d.png','-frames:v',end-start,
    '-vf',','.join(filters),'-an','-c:v','ffv1','-level','3','-pix_fmt','yuv420p','-threads','2',dest)
  duration=(end-start)/FPS
  rows.append(dict(act=shot['act'],route_order=shot['route_order'],title=shot['title'],source=f"captures/{shot['name']}/frames/%05d.png",source_start_seconds=start/FPS,source_end_seconds=end/FPS,output_start_seconds=offset,output_end_seconds=offset+duration,source_start_frame=start,source_end_frame_exclusive=end))
  chapters.append(dict(start=offset,end=offset+duration,title=shot['title']));offset+=duration;paths.append(dest)
 final_title=textfile('end-title.txt','SECOND STRIKE')
 final_sub=textfile('end-subtitle.txt','S3&K, TURNED UP.')
 end=segments/'03.mkv'
 ffmpeg('-f','lavfi','-i','color=c=0x101928:s=1600x900:r=60','-t','1.5','-vf',','.join([
  label(final_title,'(w-text_w)/2',355,72,True),
  'drawbox=x=680:y=465:w=240:h=5:color=0xff963f:t=fill',
  label(final_sub,'(w-text_w)/2',505,26,False,'0xb7c7d8')]),'-an','-c:v','ffv1','-level','3','-pix_fmt','yuv420p','-threads','2',end)
 paths.append(end);chapters.append(dict(start=offset,end=offset+1.5,title='Second Strike'));offset+=1.5
 concat=segments/'concat.txt';concat.write_text(''.join("file '"+str(x).replace("'","'\\''")+"'\n" for x in paths))
 meta=HERE/'chapters.ffmeta';meta.write_text(';FFMETADATA1\ntitle=Second Strike — Enemy Expansion\n'+''.join(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(c['start']*1000)}\nEND={round(c['end']*1000)}\ntitle={c['title']}\n" for c in chapters))
 (HERE/'edit-list.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'chapters.json').write_text(json.dumps(chapters,indent=2)+'\n')
 with (HERE/'edit-list.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 output=HERE/'second-strike-changes.mp4'
 ffmpeg('-f','concat','-safe','0','-i',concat,'-i',HERE/'music/music.wav','-f','ffmetadata','-i',meta,
  '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-t',offset,
  '-c:v','libx264','-preset','medium','-crf','18','-threads','2','-pix_fmt','yuv420p','-r','60',
  '-af',f'volume=3,afade=t=in:st=0:d=0.12,afade=t=out:st={offset-0.65}:d=0.65,alimiter=limit=0.85:level=false',
  '-c:a','aac','-b:a','192k','-movflags','+faststart',output)
 ffmpeg('-xerror','-i',output,'-f','null','-')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(output)],text=True))
 (HERE/'probe.json').write_text(json.dumps(probe,indent=2)+'\n')
 assert abs(float(probe['format']['duration'])-offset)<.05
 result=dict(output=output.name,duration_seconds=offset,frames=round(offset*FPS),width=1600,height=900,fps=60,chapters=len(chapters),full_decode_exit=0,audio_policy='Single continuous native AIZ music stem; scene SFX omitted, no layered audio',sha256=hashlib.sha256(output.read_bytes()).hexdigest())
 (HERE/'encode-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':
 sys.path.insert(0,str(ENGINE/'tools/testing'))
 from maven_queue import maven_slot,handle_termination
 with handle_termination():
  with maven_slot(ENGINE,kind='second-strike-reel-encode',estimate=60):build()
