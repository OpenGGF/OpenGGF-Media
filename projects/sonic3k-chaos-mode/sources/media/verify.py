#!/usr/bin/env python3
"""Final media verification for Chaos demo,2026-10-14. Measures actual exported
frames, chapter/cut alignment, decode, audio and representative moving sequences.
Does not assert engine parity or treat editorial cards as gameplay evidence.
"""
from pathlib import Path
import json, subprocess, hashlib, struct
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;O=P/'out';W=P/'work';W.mkdir(exist_ok=True)
FINAL=O/'sonic3k-chaos-mode-demo.mp4'
def ff(args):
    r=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-v','error',*map(str,args)],capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode()[-5000:])
    return r.stdout
def raw(path,at,frames=1):
    return ff(['-ss',f'{at:.9f}','-i',path,'-map','0:v:0','-frames:v',frames,'-pix_fmt','rgb24','-f','rawvideo','-'])
def main():
    shots=json.loads((O/'edit-timeline.json').read_text())
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-show_chapters','-of','json',str(FINAL)],text=True))
    v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert(v['width'],v['height'],v['avg_frame_rate'],v['codec_name'])==(1920,1080,'60/1','h264')
    assert(a['sample_rate'],a['channels'],a['codec_name'])==('48000',2,'aac')
    expected=sum(s['dur'] for s in shots);assert abs(float(info['format']['duration'])-expected)<.001
    assert int(v['nb_read_frames'])==round(expected*60)
    assert len(info['chapters'])==len(shots)
    for chapter,s in zip(info['chapters'],shots):
        assert abs(float(chapter['start_time'])-s['output_start'])<.002
        assert abs(float(chapter['end_time'])-s['output_end'])<.002
    ff(['-xerror','-i',FINAL,'-f','null','-'])
    # Remux copied each encoded shot. Check both boundary frames and midpoint,
    # including the two narrowly re-edited shots, against the per-shot encode.
    cuts=[]
    for s in shots:
        clip=W/f'{s["index"]:02d}.mov';positions=[0,round(s['dur']*60/2)/60,s['dur']-1/60]
        for at in positions:
            assert raw(FINAL,s['output_start']+at)==raw(clip,at),(s['index'],at)
        cuts.append({'shot':s['index'],'title':s['title'],'firstMiddleLastFrameMatches':True})
    # Ten-frame strips at3Hz through key actual motion and consequences. Full
    # frame is retained, including UI; no320px crop of a400px native source.
    names=['A normal day','Bobble Head','Where Did Sonic Go?','DVD HUD','Moon Gravity','Gravity Hiccup','Badnik Overdrive','Flash Flood','Ring Pong','Sandopolis Ghost Party']
    motion=[]
    for name in names:
        s=next(s for s in shots if s['title']==name)
        frames=min(10,int(s['dur']*3));im=Image.new('RGB',(960,frames//2*151+151),(9,20,49));d=ImageDraw.Draw(im);digests=[]
        for i in range(frames):
            at=min(s['dur']-1/60,i*s['dur']/frames);pixels=raw(FINAL,s['output_start']+at)
            digests.append(hashlib.sha256(pixels).hexdigest())
            thumb=Image.frombytes('RGB',(1920,1080),pixels).resize((480,270),Image.Resampling.NEAREST)
            x=i%2*480;y=i//2*151;thumb=thumb.resize((240,135),Image.Resampling.NEAREST)
            im.paste(thumb,(x,y));d.text((x+244,y+12),f'{name}\n{at:.2f}s\nsource {s.get("start",0)+at:.2f}s',fill=(255,202,48))
        unique=len(set(digests));assert unique>1,name
        out=O/'motion-review';out.mkdir(exist_ok=True)
        im.crop((0,0,960,((frames+1)//2)*151)).save(out/(s['src']+'.png'))
        motion.append({'title':name,'sampledFrames':frames,'distinctFrames':unique,'timing':'unchanged60Hz presentation speed'})
    r=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(FINAL),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
    assert r.returncode==0
    loud=json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}')+1])
    assert float(loud['input_tp'])<0 and abs(float(loud['input_i'])+14)<1
    boxes=[]
    with FINAL.open('rb') as f:
        while True:
            start=f.tell();header=f.read(8)
            if len(header)<8:break
            size,kind=struct.unpack('>I4s',header)
            if size==1:size=struct.unpack('>Q',f.read(8))[0]
            if size==0:size=FINAL.stat().st_size-start
            boxes.append((kind.decode(),start));f.seek(start+size)
    assert next(p for k,p in boxes if k=='moov')<next(p for k,p in boxes if k=='mdat')
    report={'video':{'dimensions':[1920,1080],'fps':60,'frames':int(v['nb_read_frames']),'duration':expected,'codec':'H264','audio':'AAC48kHz stereo','chapters':len(shots),'fastStart':True,'fullDecode':'PASS'},'cuts':cuts,'motion':motion,'loudnessLUFS':float(loud['input_i']),'truePeakDBTP':float(loud['input_tp']),'sha256':hashlib.sha256(FINAL.read_bytes()).hexdigest(),'limits':'Actual media checks. Curated AIZ1 footage; no all-effect/all-act certification. Audio level/decode checks are not a listening review.'}
    (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    # Editorial overview, full-frame thumbnails with no uneven resampling.
    im=Image.new('RGB',(1440,((len(shots)+2)//3)*294),(9,20,49));d=ImageDraw.Draw(im)
    for i,s in enumerate(shots):
        pixels=raw(FINAL,(s['output_start']+s['output_end'])/2)
        tile=Image.frombytes('RGB',(1920,1080),pixels).resize((480,270),Image.Resampling.NEAREST)
        x=i%3*480;y=i//3*294;im.paste(tile,(x,y));d.text((x+7,y+277),f'{i:02d} {s["output_start"]:.2f}s {s["title"]}',fill=(255,202,48))
    im.save(O/'reel-contact-sheet.png')
    print(json.dumps(report['video']), 'LUFS',report['loudnessLUFS'],'peak',report['truePeakDBTP'],flush=True)
if __name__=='__main__':main()
