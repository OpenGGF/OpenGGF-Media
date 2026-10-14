#!/usr/bin/env python3
"""Starpost Valley lane: assemble captured production GameLoop chapters, ROM music and SFX.
Inputs: cuts.txt, segment MP4s in this directory; output: the requested promo plus chapter map.
Every chapter has its own in-game PromoCard; 0.2 seconds of initial still lead extends the
0.333-second recorded card lead beyond 0.5 seconds. Source takes retain at least 0.5 seconds
before/after the chosen actions. Crossfades join clips; no game imagery is altered.
Origin: Starpost Valley Seasons, Promo and Docs lane, 2026-10-10, d3d1afbd6.
"""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent
OUT=Path('/home/farrell/Videos/OGGF/starpost-valley/starpost-valley-promo.mp4')
FADE=.35
cuts=[]
for line in (R/'cuts.txt').read_text().splitlines():
 line=line.split('#',1)[0].strip()
 if not line:continue
 label,start,end=line.split(); chapter,sep,seg=label.partition(':')
 cuts.append((chapter,seg if sep else chapter,float(start),float(end)))
# Record absolute editorial chapter positions, including the crossfade overlap.
parts=[];args=['ffmpeg','-y','-v','error','-filter_complex_threads','2'];chapter_map=[];running=0
for i,(chapter,seg,start,end) in enumerate(cuts):
 first=i==0 or chapter!=cuts[i-1][0];lead=.2 if first else 0
 if first:chapter_map.append({'chapter':chapter,'start':round(max(0,running-FADE if i else 0),3)})
 args+=['-threads','1','-ss',str(start),'-t',str(end-start),'-i',str(R/(seg+'.mp4'))]
 parts.append(f'[{i}:v]fps=60,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS'+(f',tpad=start_mode=clone:start_duration={lead}' if lead else '')+f'[v{i}]')
 parts.append(f'[{i}:a]aresample=48000,asetpts=PTS-STARTPTS'+(f',adelay={int(lead*1000)}|{int(lead*1000)}' if lead else '')+f'[a{i}]')
 running+=end-start+lead-(FADE if i else 0)
vprev,aprev='v0','a0';offset=cuts[0][3]-cuts[0][2]+.2
for i in range(1,len(cuts)):
 offset-=FADE
 parts += [f'[{vprev}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.6f}[vx{i}]',f'[{aprev}][a{i}]acrossfade=d={FADE}[ax{i}]']
 vprev,aprev=f'vx{i}',f'ax{i}'
 offset+=cuts[i][3]-cuts[i][2]+(.2 if cuts[i][0]!=cuts[i-1][0] else 0)
args += ['-filter_complex',';'.join(parts),'-map',f'[{vprev}]','-map',f'[{aprev}]','-threads','2','-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT)]
OUT.parent.mkdir(parents=True,exist_ok=True)
subprocess.run(args,check=True)
for i,c in enumerate(chapter_map):c['end']=chapter_map[i+1]['start'] if i+1<len(chapter_map) else round(running,3)
(R/'chapters.json').write_text(json.dumps(chapter_map,indent=2)+'\n')
print(json.dumps({'duration':running,'chapters':chapter_map},indent=2))
