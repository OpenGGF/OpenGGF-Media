#!/usr/bin/env python3
"""Purpose: repeatable positioned MICA/TALON promo captures, phase 1.
Inputs: checkout and freshly built example jar, original ROMs resolved by engine.
Origin: 2026-11-10 promo lane; InputLogAuthorTool roundtrips every script.
No gameplay state is read from comparison traces. Declared setup is in shots.json.
"""
import argparse,subprocess,os,json,csv,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--checkout',type=Path,required=True);ap.add_argument('--jar',type=Path,required=True);ap.add_argument('--only',nargs='*');ap.add_argument('--take',default='phase1');a=ap.parse_args()
R=a.checkout.resolve(); J=a.jar.resolve(); O=P/'captures'/a.take; O.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
for k in ('DISPLAY','WAYLAND_DISPLAY'):env.pop(k,None)
cp=str(R/'target/classes')+os.pathsep+(R/'target/mica-classpath.txt').read_text().strip()
def java(tool,args,log):
 with open(log,'w') as f:subprocess.run(['java','-Xmx768m','--enable-native-access=ALL-UNNAMED','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dopenggf.saveRoot={O}/saves','-cp',cp,'com.openggf.tools.'+tool,*map(str,args)],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=300)
SHOTS=[
 dict(id='s1-run',game='s1',zone='ghz',x=3100,y=660,rings=28,timer=4200,script='30 -; 240 R; 30 -'),
 dict(id='s2-run',game='s2',zone='ehz',x=1800,y=540,rings=32,timer=3900,script='30 -; 240 R; 30 -'),
 dict(id='s3k-run',game='s3k',zone='aiz',x=6040,y=1040,rings=34,timer=5400,script='30 -; 240 R; 30 -'),
 dict(id='hero',game='s3k',zone='aiz',x=7100,y=900,rings=38,timer=6300,script='30 -; 20 R; 1 R+A; 12 R; 1 A; 12 -; repeat 10 { 1 R+A; 12 R }; repeat 18 { 12 R; 1 R+A; 15 R }'),
 dict(id='talon-s2',game='s2',zone='ehz',x=1800,y=540,rings=32,timer=3900,main='talon',script='30 -; 1 R+A; 20 R; repeat 5 { 1 A; 8 R }; 18 D; 1 D+A; 120 R; 60 -'),
 dict(id='talon-s3k',game='s3k',zone='aiz',x=7100,y=900,rings=38,timer=6300,main='talon',script='30 -; 1 A; 20 -; repeat 5 { 1 A; 8 - }; 18 D; 1 D+A; 120 R; 60 -'),
 dict(id='team',game='s3k',zone='aiz',x=6040,y=1040,rings=34,timer=5400,sidekick='talon',script='30 -; 210 R; 1 R+A; 59 R; 60 -'),
 dict(id='gilded',game='s3k',zone='aiz',x=7100,y=900,rings=70,timer=7200,emeralds='1111111',script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 8 { 1 R+A; 16 R }; 120 R'),
 dict(id='solar',game='s3k',zone='aiz',x=7100,y=900,rings=70,timer=7200,emeralds='1111111',main='talon',script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 5 { 1 A; 8 - }; 18 D; 1 D+A; 180 R'),
 dict(id='hero-ehz',game='s2',zone='ehz',x=9040,y=520,rings=48,timer=8100,script='10 -; 1 R+A; 10 R; 1 A; 12 R; repeat 9 { 1 R+A; 16 R }; 180 R'),
 dict(id='gilded-clear-low',game='s2',zone='ehz',x=9000,y=780,rings=70,timer=8100,emeralds='1111111',sidekick='talon',script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 16 { 1 R+A; 18 R }; 360 R; 660 -'),
 dict(id='half-pipe-approach',game='s2',zone='ehz',x=3500,y=150,rings=70,timer=6600,sidekick='talon',script='48 R; 32 L; 100 -; 1 A; 45 -; repeat 4 { 1 A; 45 - }; 420 -'),
 dict(id='carry',game='s3k',zone='aiz',x=6040,y=1040,rings=34,timer=5400,sidekick='talon',script='30 -; 22 - / R; 1 - / A; 2 -; 1 - / A; repeat 15 { 8 -; 1 - / A }; 120 -'),
 dict(id='blue-play',game='s3k',zone='cnz',x=11616,y=1612,rings=42,timer=9600,script='90 -; 90 R; 540 -'),
 dict(id='blue-sphere',game='s3k',zone='cnz',x=11616,y=1612,rings=42,timer=9600,complete=True,script='90 -; 90 R; 900 -'),
 dict(id='ehz-clear',game='s2',zone='ehz',x=9900,y=400,rings=48,timer=8700,script='30 -; 240 R; 660 -'),
 dict(id='ghz-clear',game='s1',zone='ghz',x=9100,y=940,rings=48,timer=8700,script='30 -; 240 R; 660 -'),
 dict(id='data-select-team',game='s3k',zone='aiz',title=True,script='360 -; 1 S; 360 -'),
]
(P/'shots.json').write_text(json.dumps(SHOTS,indent=2))
for s in SHOTS:
 if a.only and s['id'] not in a.only:continue
 d=O/s['id'];d.mkdir(exist_ok=True); sc=d/'input.script';sc.write_text(s['script']+'\n')
 java('InputLogAuthorTool',['--script',sc,'--out',d/'input.txt'],d/'author.log')
 args=['--game',s['game'],'--zone',s['zone'],'--act',str(s.get('act',1)),'--main','mica-and-talon:'+s.get('main','mica'),'--mod',J,'--input',d/'input.txt','--out-dir',d,'--width','320','--scale','1','--no-video']
 if s.get('title'):
  slots=d/'slots.json';slots.write_text(json.dumps({str(i):dict(act=0,zone=0,lives=3,mainCharacter='mica-and-talon:mica',sidekicks=['mica-and-talon:talon'],chaosEmeralds=[],clear=False,progressCode=1,clearState=0) for i in range(1,4)})); args+=['--title-screen','--interactive-pacing','--save-slots',slots]
 else:
  for k in ('x','y','rings','timer'):args+=['--'+k,str(s[k])]
 if s.get('starpost'):args+=['--star-post']
 if s.get('complete'):args+=['--complete-special-stage']
 if 'emeralds'in s:args+=['--emeralds',s['emeralds']]
 if 'sidekick'in s:args+=['--sidekick','mica-and-talon:'+s['sidekick']]
 provenance=dict(s,checkout=str(R),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),jar=str(J),jar_sha256=hashlib.sha256(J.read_bytes()).hexdigest(),command=args,source_kind='positioned native gameplay' if not s.get('title') else 'title-first production presentation',fps=60,every=1,audio=False)
 (d/'provenance.json').write_text(json.dumps(provenance,indent=2,default=str))
 print('CAPTURE',s['id'],flush=True)
 try:java('GameplayCaptureTool',args,d/'capture.log')
 except Exception as ex: print('FAILED',s['id'],str(ex),flush=True);continue
 rows=list(csv.DictReader(open(d/'state.csv')))
 summary=dict(frames=len(rows),first=rows[0],last=rows[-1],hurt_frames=sum(r['hurt']=='1' for r in rows),dead_frames=sum(r['dead']=='1' for r in rows),poses=sorted(set(r['mapping_frame']for r in rows)))
 (d/'observations.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
 from PIL import Image,ImageDraw
 frames=sorted((d/'frames').glob('*.png')); sheet=Image.new('RGB',(960,3*248),(8,16,56));draw=ImageDraw.Draw(sheet)
 for i in range(9):
  f=frames[min(len(frames)-1,round(i*(len(frames)-1)/8))]; im=Image.open(f);x=i%3*320;y=i//3*248;sheet.paste(im,(x,y));draw.text((x+6,y+226),f.name,fill='white')
 sheet.save(d/'contact.jpg')
