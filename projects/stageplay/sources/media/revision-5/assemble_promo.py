#!/usr/bin/env python3
"""One More Take: continuous Stageplay LIVE story with restrained promotional titles.

Audience: Sonic fans and directors using OpenGGF.
Form: authored performance in the production world; native motion is measured in JSONL.
Promise: direct characters, moving scenery and a following camera with reusable scripts.
Beats: platform relay, ring mishap, flight/glide, clean retry, three-character run.
Hero moment: the cast runs together after the clean platform transfer.
Sound: captured native world music/SFX, one owner, constant +6 dB; no second music bed.
Palette: cream, gold and deep blue, sampled from dialogue and the DEZ background.
Title face: Fira Sans Compressed Heavy Italic, externally supplied under SIL OFL 1.1.
End card: title, development status, project URL and fan-project/ROM notice.
Origin: OpenGGF Stageplay live-world delivery, 2026-10-21.
Inputs: one-more-take-review.mkv (640x448, 60fps, 60s), FFmpeg, Pillow, Fira fonts.
The complete source remains in order at exact integer scale; no gameplay retiming.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

FPS, FRAMES, WIDTH, HEIGHT = 60, 3600, 1280, 896
CHAPTERS = [(0,960,'Platform relay'),(960,1260,'The wrong floor'),(1260,2220,'Air traffic'),
            (2220,3060,'One clean take'),(3060,3600,'One more run')]
CARDS = [(12,210,16,12,'opening'),(3240,3600,20,0,'closing')]


def run(args):
    result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode: raise RuntimeError(result.stderr[-4000:])
    return result.stdout


def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def cards(directory,title_font,body_font):
    result=[]
    for _,_,_,_,name in CARDS:
        image=Image.new('RGBA',(WIDTH,264)); draw=ImageDraw.Draw(image)
        for y in range(264):
            draw.line((0,y,WIDTH,y),fill=(8,16,32,round(195*(1-y/264)**.7)))
        title=ImageFont.truetype(str(title_font),104 if name=='opening' else 106)
        body=ImageFont.truetype(str(body_font),26)
        label='OPENGGF STAGEPLAY' if name=='opening' else 'DIRECT THE ACTION.'
        draw.polygon([(28,29),(38,29),(28,116),(18,116)],fill='#FFC65C')
        draw.text((55,31),label,font=title,anchor='lt',fill='#FFF1CF',stroke_width=4,stroke_fill='#081020')
        if draw.textbbox((55,31),label,font=title,anchor='lt',stroke_width=4)[2]>WIDTH-40:
            raise ValueError('Title exceeds safe width')
        if name=='opening':
            draw.text((60,148),'ONE MORE TAKE  /  A NATIVE PHYSICS SHORT',font=body,anchor='lt',fill='#FFC65C',stroke_width=1,stroke_fill='#081020')
        else:
            lines=['OpenGGF Stageplay  /  Development preview','github.com/OpenGGF/OpenGGF',
                   'Fan-made and free. Not affiliated with SEGA. Requires your own ROM.']
            for i,line in enumerate(lines):
                font=ImageFont.truetype(str(body_font),23 if i==2 else 26)
                draw.text((60,147+i*34),line,font=font,anchor='lt',fill='#FFC65C' if i==0 else '#FFF1CF',stroke_width=1,stroke_fill='#081020')
        path=directory/(name+'.png'); image.save(path);result.append(path)
    return result


def graph():
    parts=['[0:v]scale=1280:896:flags=neighbor,setsar=1[base]'];last='base'
    for i,(start,end,enter,leave,name) in enumerate(CARDS,1):
        duration=(end-start)/FPS
        fade=f'fade=t=in:st=0:d={enter/FPS}:alpha=1'
        if leave:fade+=f',fade=t=out:st={duration-leave/FPS}:d={leave/FPS}:alpha=1'
        parts.append(f'[{i}:v]format=rgba,trim=end_frame={end-start},setpts=PTS-STARTPTS,{fade},setpts=PTS+{start/FPS}/TB[card{i}]')
        x=f'-24*pow(max(0,1-(t-{start/FPS})/{enter/FPS}),3)'
        parts.append(f'[{last}][card{i}]overlay=x=\'{x}\':y=0:eof_action=pass:repeatlast=0:enable=\'between(t,{start/FPS},{(end-1)/FPS})\'[v{i}]');last=f'v{i}'
    parts.append(f'[{last}]format=yuv420p[v]');return ';'.join(parts)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--out',default='stageplay-live-promo.mp4')
    ap.add_argument('--title-font',type=Path,default=Path('/usr/share/fonts/TTF/FiraSansCompressed-HeavyItalic.ttf'))
    ap.add_argument('--body-font',type=Path,default=Path('/usr/share/fonts/TTF/FiraSans-Medium.ttf'))
    args=ap.parse_args();root=args.root.resolve();source=root/'one-more-take-review.mkv';out=root/args.out
    if out.exists():raise ValueError('Refusing to replace '+str(out))
    source_hash=digest(source)
    info=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(source)]))
    video=next(x for x in info['streams'] if x['codec_type']=='video')
    assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_read_frames']))==(640,448,'60/1',FRAMES)
    with tempfile.TemporaryDirectory(prefix='stageplay-promo-',dir=root) as tmp:
        temp=Path(tmp);images=cards(temp,args.title_font,args.body_font)
        metadata=temp/'chapters.ffmeta'
        metadata.write_text(';FFMETADATA1\ntitle=One More Take — OpenGGF Stageplay\n'+''.join(
            f'[CHAPTER]\nTIMEBASE=1/60\nSTART={start}\nEND={end}\ntitle={title}\n' for start,end,title in CHAPTERS))
        staged=temp/'promo.mp4'
        command=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-i',str(source)]
        for image in images:command+=['-loop','1','-framerate','60','-i',str(image)]
        command+=['-f','ffmetadata','-i',str(metadata),'-filter_complex_threads','1','-filter_complex',graph(),
                  '-map','[v]','-map','0:a:0','-map_metadata','3','-map_chapters','3',
                  '-c:v','libx264','-preset','slow','-crf','18','-threads','4','-pix_fmt','yuv420p',
                  '-frames:v',str(FRAMES),'-c:a','aac','-b:a','192k','-af','volume=6dB','-movflags','+faststart',str(staged)]
        run(command);run(['ffmpeg','-v','error','-xerror','-i',str(staged),'-f','null','-'])
        if digest(source)!=source_hash:raise RuntimeError('Source changed during assembly')
        staged.rename(out)
    report={'source':source.name,'sourceSha256':source_hash,'output':out.name,'outputSha256':digest(out),
            'frames':FRAMES,'fps':FPS,'dimensions':[WIDTH,HEIGHT],'gainDb':6,
            'sourceOrder':'All 3600 frames, no cuts, repeats, retiming or camera effects added',
            'chapters':[{'startFrame':a,'endFrame':b,'title':t} for a,b,t in CHAPTERS],
            'cards':[{'startFrame':a,'endFrame':b,'enterFrames':c,'leaveFrames':d,'name':e} for a,b,c,d,e in CARDS],
            'fonts':{args.title_font.name:digest(args.title_font),args.body_font.name:digest(args.body_font)},
            'assemblyScriptSha256':digest(Path(__file__))}
    out.with_suffix('.assembly.json').write_text(json.dumps(report,indent=2)+'\n')
    (root/'chapters.json').write_text(json.dumps(report['chapters'],indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
