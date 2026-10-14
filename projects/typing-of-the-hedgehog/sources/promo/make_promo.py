#!/usr/bin/env python3
"""Assemble the first Typing of the Hedgehog promo from synchronous production recordings.

Inputs (task directory, never repository media): caps/<name>/capture.mp4 + audio.wav,
cards/<name>/f%04d.png, captions/*.png and promo_plan.py. Card glyphs are ROM decoded.
Output: out/typing-of-the-hedgehog-promo.mp4, 1920x1080 60 fps H.264 + AAC 48 kHz
stereo; two-pass -14 LUFS / -1 dBTP loudness normalization. Also exports timestamped
shot list and stills. Task tool, 2026-10-10; follows the Flappy Tails edit language.
"""
import subprocess,json,os,sys
from pathlib import Path
from PIL import Image,ImageDraw
from promo_plan import plan
P=Path(__file__).resolve().parent;W=P/'work';O=P/'out'
V=['-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p','-r','60','-threads','4']
A=['-c:a','pcm_s16le','-ar','48000','-ac','2']
CROP='crop=1920:1080:40:20'

def run(args):
    r=subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-filter_complex_threads','1',*map(str,args)],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr[-6000:])

def render(i,s):
    out=W/f'{i:02d}.mov';dur=s['dur']/s.get('speed',1)
    if '--resume' in sys.argv and out.exists():return out
    if 'card' in s:
        n=s['card'];inp=['-framerate','60','-i',P/'cards'/n/'f%04d.png']
        # Real recorded ROM music/SFX under the trailer slams; no manufactured game audio.
        bed=P/'caps/hub/audio.wav';bedstart=3.5
        if n=='end':bedstart=0.0
        if n in ('boss','climax'):bed=P/'caps/dez/audio.wav';bedstart=14
        inp+=['-ss',bedstart,'-i',bed]
        aud=f'[1:a]atrim=duration={dur},asetpts=PTS-STARTPTS,volume=0.85,afade=t=in:d=0.012,afade=t=out:st={dur-.06}:d=0.06[a]'
        if n=='survive':
            # Shipped creator voice asset, explicitly editorial narration over a ROM-font card.
            voice=P/'assets/announcer_type_to_survive.ogg'
            inp+=['-i',voice]
            aud=f'[1:a]atrim=duration={dur},asetpts=PTS-STARTPTS,volume=0.5[bed];[2:a]atrim=duration={dur},asetpts=PTS-STARTPTS[voc];[bed][voc]amix=inputs=2:normalize=0,apad=whole_dur={dur}[a]'
        vid=f'[0:v]scale=2000:1120:flags=neighbor,{CROP},setsar=1[v]'
        if n=='end':aud=f'[1:a]atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=out:st={dur-1.5}:d=1.5[a]'
        run([*inp,'-filter_complex',vid+';'+aud,'-map','[v]','-map','[a]','-t',dur,*V,*A,out])
    else:
        n=s['src'];start=s['start'];speed=s.get('speed',1)
        inp=['-ss',start,'-i',P/'caps'/n/'capture.mp4','-ss',start,'-i',P/'caps'/n/'audio.wav']
        vf=f'trim=duration={s["dur"]},setpts=(PTS-STARTPTS)/{speed},{CROP}'
        if s.get('zoom'):vf+=f',scale=iw*{s["zoom"]}:ih*{s["zoom"]}:flags=neighbor,crop=1920:1080'
        for t in s.get('punches',[]):
            z=f'(1+0.10*max(0,1-abs(t-{t})/0.20))'
            vf+=f",scale=w='iw*{z}':h='ih*{z}':eval=frame:flags=neighbor,crop=1920:1080:x='(iw-1920)/2+min((iw-1920)/2,10)*sin(n*2.7)':y='(ih-1080)/2'"
        # Two-frame white cut flashes, a deliberate trailer transition.
        if i>3:vf+=",eq=brightness='0.22*max(0,1-t/0.045)':eval=frame"
        vf+=',fps=60,setsar=1'
        af=f'atrim=duration={s["dur"]},asetpts=PTS-STARTPTS'
        if speed!=1:af+=f',asetrate=48000*{speed},aresample=48000,apad=whole_dur={dur},atrim=duration={dur}'
        af+=f',afade=t=in:d=0.007,afade=t=out:st={dur-.03}:d=0.03'
        if s.get('caption'):
            inp+=['-loop','1','-i',P/'captions'/f'{s["caption"]}.png']
            graph=f'[0:v]{vf}[base];[2:v]scale=2000:1120:flags=neighbor,{CROP}[cap];[base][cap]overlay=shortest=1[v];[1:a]{af}[a]'
        else:graph=f'[0:v]{vf}[v];[1:a]{af}[a]'
        run([*inp,'-filter_complex',graph,'-map','[v]','-map','[a]','-t',dur,*V,*A,out])
    return out

def finish(parts):
    lst=W/'concat.txt';lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    joined=W/'joined.mov';run(['-f','concat','-safe','0','-i',lst,'-c','copy',joined])
    probe=subprocess.run(['ffmpeg','-nostdin','-i',str(joined),'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    stats=json.loads(probe[probe.rindex('{'):probe.rindex('}')+1]);(O/'loudness-first-pass.json').write_text(json.dumps(stats,indent=2)+'\n')
    ln=('loudnorm=I=-14:TP=-1:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true').format(**stats)
    final=O/'typing-of-the-hedgehog-promo.mp4'
    run(['-i',joined,'-c:v','copy','-af',ln+',aresample=48000','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',final])
    return final

def sheet(final,shots):
    chosen=[0,3,4,7,9,11,12,15,18,20,24,25,27,29,33,38]
    # Representative action instants, rather than inactive intervals inside a boss cycle.
    offsets={25:1.7,27:1.4,29:.35}
    picks=[(shots[i]['start']+offsets.get(i,(shots[i]['end']-shots[i]['start'])/2),shots[i].get('name',shots[i].get('card')).upper()) for i in chosen]
    im=Image.new('RGB',(1920,1184),(11,18,38));d=ImageDraw.Draw(im)
    for j,(t,label) in enumerate(picks):
        f=W/f'still-{j}.png';run(['-ss',t,'-i',final,'-vf','scale=480:270:flags=neighbor','-frames:v','1',f])
        x=(j%4)*480;y=(j//4)*296;im.paste(Image.open(f),(x,y));d.text((x+9,y+277),f'{t:05.1f}s  {label[:48]}',fill=(245,202,69));f.unlink()
    im.save(O/'typing-of-the-hedgehog-promo-stills.png')

if __name__=='__main__':
    W.mkdir(exist_ok=True);O.mkdir(exist_ok=True);shots=plan();clock=0;parts=[];timeline=[]
    for i,s in enumerate(shots):
        dur=s['dur']/s.get('speed',1);name=s.get('name',s.get('card'));print(f'{i:02d} {clock:06.2f} +{dur:.2f} {name}',flush=True)
        timeline.append({**s,'source_start':s.get('start'),'index':i,'start':round(clock,3),'end':round(clock+dur,3)});parts.append(render(i,s));clock+=dur
    (O/'shot-list.json').write_text(json.dumps(timeline,indent=2)+'\n')
    (O/'shot-list.txt').write_text('\n'.join(f'{s["start"]:06.2f}-{s["end"]:06.2f} {s.get("name",s.get("card"))}' for s in timeline)+'\n')
    final=finish(parts);sheet(final,timeline);print('done',final,clock,flush=True)
