#!/usr/bin/env python3
"""Reproducible Chaos Mode promo edit, 2026-10-14.
Real production60Hz captures plus editorial ROM-lettered cards and ROM audio
stings. Source frames stay at real speed and4x integer nearest scaling within
a1920x1080 navy/gold canvas, preserving the full native HUD. Each shot is encoded
once; final video is copied, PCM normalized in two passes and encoded AAC.
"""
from pathlib import Path
import csv, json, subprocess, sys, shutil
from PIL import Image,ImageDraw
import card_renderer as cards
P=Path(__file__).resolve().parent; W=P/'work'; O=P/'out'
W.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
V=['-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-r','60','-threads','4']
A=['-c:a','pcm_s16le','-ar','48000','-ac','2']
def run(args, quiet=True):
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1',*map(str,args)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr[-6000:])
    return r.stderr
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
def overlay(i,text):
    im=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rectangle((156,40,1763,943),outline=(255,202,48,255),width=3)
    d.line((160,970,1759,970),fill=(255,202,48,255),width=3)
    header=cards.text_image('SONIC3K CHAOS MODE',small=True,color=cards.GOLD)
    header=header.resize((header.width*2,header.height*2),Image.Resampling.NEAREST)
    im.alpha_composite(header,(160,12))
    title=cards.text_image(text,small=True,color=cards.WHITE)
    scale=min(4,1740/title.width)
    title=title.resize((round(title.width*scale),round(title.height*scale)),Image.Resampling.NEAREST)
    im.alpha_composite(title,((1920-title.width)//2,995))
    path=W/f'overlay-{i:02d}.png';im.save(path);return path
def render(i,s):
    out=W/f'{i:02d}.mov'
    receipt=W/f'{i:02d}-shot.json'
    if '--resume' in sys.argv and out.exists() and receipt.exists() and json.loads(receipt.read_text())==s:return out
    dur=s['dur']
    if 'card' in s:
        inputs=['-framerate','60','-i',P/'cards'/s['card']/'f%04d.png','-ss',(i*1.3)%25,'-i',P/'assets/audio/data-select.wav']
        vid='[0:v]scale=2000:1120:flags=neighbor,crop=1920:1080:40:20,setsar=1[v]'
        aud=f'[1:a]atrim=duration={dur},asetpts=PTS-STARTPTS,volume=0.72,afade=t=in:d=0.01,afade=t=out:st={dur-.06}:d=0.06[bed]'
        if s.get('sfx'):
            inputs+=['-i',P/'assets/audio'/f'{s["sfx"]}.wav']
            aud+=f';[2:a]atrim=duration={dur},asetpts=PTS-STARTPTS,volume=0.8[sting];[bed][sting]amix=inputs=2:normalize=0,apad=whole_dur={dur},atrim=duration={dur}[a]'
        else:aud+=';[bed]anull[a]'
        if s['card']=='end':aud=aud.replace('[a]',f'[mix];[mix]afade=t=out:st={dur-1}:d=1[a]')
        graph=vid+';'+aud
    else:
        src=P/'captures'/s['src']/'source.mkv';info=probe(src)
        if s['start']+dur>float(info['format']['duration'])+.001:raise ValueError(f'Interval past source: {s}')
        inputs=['-ss',s['start'],'-i',src,'-loop','1','-i',overlay(i,s['caption'])]
        vf=f'[0:v]trim=duration={dur},setpts=PTS-STARTPTS,scale=1600:896:flags=neighbor,pad=1920:1080:160:44:color=0x091431,setsar=1[base];[base][1:v]overlay=shortest=1[v]'
        af=f'[0:a]atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.007,afade=t=out:st={dur-.03}:d=0.03[a]'
        graph=vf+';'+af
    run([*inputs,'-filter_complex',graph,'-map','[v]','-map','[a]','-t',dur,*V,*A,out])
    actual=float(probe(out)['format']['duration'])
    if abs(actual-dur)>.04:raise ValueError((out,actual,dur))
    receipt.write_text(json.dumps(s,sort_keys=True)+'\n')
    return out
def metadata(timeline):
    meta=W/'chapters.ffmeta';text=';FFMETADATA1\ntitle=Sonic3K Chaos Mode\ncomment=Curated real gameplay with fictional editorial captions.\n'
    for s in timeline:
        text+=f'[CHAPTER]\nTIMEBASE=1/60000\nSTART={round(s["output_start"]*60000)}\nEND={round(s["output_end"]*60000)}\ntitle={s["title"]}\n'
    meta.write_text(text);return meta
def main():
    shots=json.loads((P/'edit.json').read_text());timeline=[];parts=[];clock=0
    for i,s in enumerate(shots):
        print(i,round(clock,2),s['title'],flush=True)
        source=f'captures/{s["src"]}/source.mkv' if 'src'in s else f'cards/{s["card"]}/f%04d.png'
        parts.append(render(i,s));timeline.append({**s,'source':source,'index':i,'act':'AIZ1' if 'src'in s else 'editorial','route_order':i,'output_start':round(clock,6),'output_end':round(clock+s['dur'],6),'source_start_seconds':s.get('start',0),'source_end_seconds':round(s.get('start',0)+s['dur'],6)})
        clock+=s['dur']
    (O/'edit-timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
    keys=['act','route_order','title','source','src','card','source_start_seconds','source_end_seconds','output_start','output_end','caption']
    with (O/'chapters.csv').open('w') as f:
        wr=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');wr.writeheader();wr.writerows(timeline)
    (O/'chapters.txt').write_text('\n'.join(f'{s["output_start"]:06.2f}–{s["output_end"]:06.2f} {s["title"]}' for s in timeline)+'\n')
    lst=W/'concat.txt';lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    joined=W/'joined.mov';run(['-f','concat','-safe','0','-i',lst,'-c','copy',joined])
    r=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(joined),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr[-3000:])
    stats=json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}')+1])
    (O/'loudness.json').write_text(json.dumps(stats,indent=2)+'\n')
    ln='loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true'.format(**stats)
    final=O/'sonic3k-chaos-mode-demo.mp4'
    run(['-i',joined,'-i',metadata(timeline),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c:v','copy','-af',ln+',aresample=48000','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',final])
    info=probe(final)
    if abs(float(info['format']['duration'])-clock)>.04:raise ValueError(('final duration',info['format']['duration'],clock))
    (O/'media-info.json').write_text(json.dumps(info,indent=2)+'\n')
    run(['-v','error','-xerror','-i',final,'-f','null','-'])
    print('FINAL',final,round(clock,3),flush=True)
if __name__=='__main__':main()
