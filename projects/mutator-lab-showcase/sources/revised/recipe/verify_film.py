#!/usr/bin/env python3
"""Files-only verification of the root-owned pacing/audio revision, 2026-10-10.

Inputs: chapters.json, source PNGs, mixed WAV and final MP4. No devices or engine.
Check selected native frame provenance, CFR/full decode, encoded sound alignment
and loudness. Technical checks do not claim subjective listening or hardware output.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
FILM=ROOT/'out/mutator-lab-complete-showcase-revised.mp4'
P=json.loads((ROOT/'out/chapters.json').read_text())


def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True,timeout=180)


def mono(path):
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-threads','2','-i',str(path),
        '-map','0:a','-ac','1','-ar','8000','-f','f32le','-'],timeout=120)
    return np.frombuffer(raw,dtype='<f4').astype(np.float64)


def combined(terms):
    if len(terms)==1:return terms[0]
    h=len(terms)//2
    return '('+combined(terms[:h])+')+('+combined(terms[h:])+')'


def main():
    # Single complete selected-frame decode, rather than one full decode per sample.
    checks={}
    for s in P['segments']:
        if s['id'] in ['title','outro']:continue
        for o in [s['frames']//4,s['frames']//2,3*s['frames']//4]:
            checks.setdefault(s['output_frames'][0]+o,[]).extend((s['id'],src,o) for src in s['sources'])
    expr=combined(['eq(n\\,%d)'%f for f in sorted(checks)])
    proc=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-xerror','-threads','4','-filter_threads','2',
        '-i',str(FILM),'-vf','select='+expr,'-fps_mode','vfr','-threads','2',
        '-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    results=[]; thumbs=[]
    try:
        for f in sorted(checks):
            data=bytearray()
            while len(data)<1920*1080*3:
                chunk=proc.stdout.read(1920*1080*3-len(data))
                if not chunk:raise RuntimeError('Missing decoded source sample')
                data.extend(chunk)
            image=Image.frombytes('RGB',(1920,1080),bytes(data))
            if any(s[0] in ['nc-hit','nc-result','ss-touch','ss-outcome','bon-compare','finale-run','speed-on','hero-run'] for s in checks[f]):
                path=ROOT/'review'/f'frame-{f:05d}.png';image.save(path)
            thumb=image.resize((480,270));thumbs.append((f,thumb))
            for sid,source,o in checks[f]:
                x,y,w,h=source['crop']
                sample=np.asarray(image.crop((x,y,x+w,y+h)).resize((320,224),Image.Resampling.NEAREST)).reshape(-1)[::5].astype(np.int16)
                native_f=source['frames'][0]+o; distances={}
                for delta in [-2,-1,0,1,2]:
                    path=Path(source['take'])/'capture/frames'/f'{native_f+delta:05d}.png'
                    if path.exists():
                        with Image.open(path) as im:native=np.asarray(im.convert('RGB')).reshape(-1)[::5].astype(np.int16)
                        distances[delta]=round(float(np.abs(sample-native).mean()),3)
                best=min(distances,key=distances.get)
                results.append({'shot':sid,'output_frame':f,'source_frame':native_f,'distances':distances,
                    'mismatch':best!=0 and distances[best]<distances[0]-.5})
        assert not proc.stdout.read()
        stderr=proc.stderr.read().decode(errors='replace');code=proc.wait(timeout=120)
        assert code==0,stderr
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=10)
    mismatches=[r for r in results if r['mismatch']];assert not mismatches,mismatches
    for page in range(0,len(thumbs),15):
        chunk=thumbs[page:page+15];sheet=Image.new('RGB',(1440,300*((len(chunk)+2)//3)),'#0b1426');draw=ImageDraw.Draw(sheet)
        for i,(f,img) in enumerate(chunk):
            x,y=(i%3)*480,(i//3)*300;sheet.paste(img,(x,y));draw.text((x+8,y+275),f'{f/60:.2f}s / {f}',fill='white')
        sheet.save(ROOT/'review'/f'sheet-{page//15+1}.jpg',quality=90)
    probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(FILM)]).stdout)
    pts=run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts','-of','csv=p=0',str(FILM)]).stdout
    pts=[int(v) for v in pts.replace(',',' ').split()]
    assert len(pts)==P['frames'];assert sorted(set(b-a for a,b in zip(pts,pts[1:])))==[256]
    assert len(probe['chapters'])==14
    run(['ffmpeg','-nostdin','-v','error','-xerror','-threads','4','-i',str(FILM),'-threads','2','-f','null','-'])
    final,reference=mono(FILM),mono(ROOT/'out/soundtrack.wav');alignment=[]
    for s in P['segments']:
        if s['id'] in ['title','outro']:continue
        t=(s['start_s']+s['end_s'])/2;start=int(t*8000);n=4000
        ref=reference[start:start+n];norm=np.linalg.norm(ref)
        if not norm:continue
        scored=[]
        for lag in range(-240,241,2):
            actual=final[start+lag:start+lag+n];den=np.linalg.norm(actual)*norm
            scored.append((float(np.dot(actual,ref)/den) if den else 0,lag))
        corr,lag=max(scored);alignment.append({'shot':s['id'],'time_s':round(t,3),'lag_ms':lag/8,'correlation':round(corr,6)})
    assert max(abs(a['lag_ms']) for a in alignment)==0,alignment
    measurement=run(['ffmpeg','-nostdin','-hide_banner','-v','info','-threads','2','-i',str(FILM),'-vn',
        '-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr
    loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',measurement,re.S)[0])
    assert float(loud['input_tp'])<=-1.0,loud
    assert -18<=float(loud['input_i'])<=-15,loud
    # Critical native 200% sound is unfiltered, sole-owner and sample-synchronous.
    score=np.frombuffer(wave.open(str(ROOT/'out/soundtrack.wav')).readframes(P['frames']*800),dtype='<i2').reshape(-1,2)
    audio=json.loads((ROOT/'out/audio-manifest.json').read_text())
    speed=next(s for s in P['segments'] if s['id']=='speed-on')
    piece=next(s for s in audio['pieces'] if s['segment']=='speed-on')
    path=Path(piece['take'])/'capture/audio.wav'
    with wave.open(str(path)) as f:
        f.setpos(616*800);native=np.frombuffer(f.readframes(144*800),dtype='<i2').reshape(-1,2).astype(np.float64)
    gain=10**((piece['trim_db']+audio['static_gain_db'])/20)*32767/32768
    predicted=np.rint(native*gain).astype('<i2')
    offset=(speed['output_frames'][0]+616-352)*800
    delta=np.abs(score[offset:offset+len(native)].astype(np.int32)-predicted.astype(np.int32))
    assert np.max(delta)<=1,(np.max(delta),'Native audio-follow proof altered')
    report={'film':str(FILM),'sha256':hashlib.sha256(FILM.read_bytes()).hexdigest(),
        'frames':len(pts),'duration_s':P['duration_s'],'shots':P['shots'],
        'cuts_last20':sum(s['start_s']>=P['duration_s']-20 for s in P['segments'][1:]),
        'decode_exit':0,'cfr_pts_deltas':[256],'source_frame_checks':len(results),
        'source_mismatches':mismatches,'source_details':results,'aac_alignment':alignment,
        'final_aac_loudness':loud,'speed_200_pcm_max_sample_error':int(np.max(delta)),
        'speed_200_pcm_stereo_frames_checked':len(native),'probe':probe,
        'limits':'Selected native source ranges and technical sound alignment; no subjective listening or hardware/output claims.'}
    (ROOT/'out/verify.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['source_details','probe','aac_alignment']},indent=2))


if __name__=='__main__':main()
