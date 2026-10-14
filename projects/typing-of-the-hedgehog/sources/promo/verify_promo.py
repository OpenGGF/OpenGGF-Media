#!/usr/bin/env python3
"""Verify the first Typing of the Hedgehog promo, 2026-10-10. Task tool.
Inputs: final MP4, EDL, original synchronous captures/PCM. Checks frame/tick/PCM
clocks, ffprobe format, full decode, loudness, and waveform A/V offsets on real-speed
gameplay. Human visual playback remains required; these are measurements, not taste.
"""
from pathlib import Path
import subprocess,json,wave
import numpy as np
from scipy.signal import correlate
from promo_plan import plan
P=Path(__file__).resolve().parent;O=P/'out';F=O/'typing-of-the-hedgehog-promo.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def pcm(p,start,dur):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-ac','1','-ar','48000','-f','f32le','pipe:1']),dtype='<f4')

if __name__=='__main__':
    sources=[]
    for n in ['ghz','ehz','fz','dez','hub']:
        d=P/'caps'/n;p=probe(d/'capture.mp4');v=next(s for s in p['streams'] if s['codec_type']=='video')
        with wave.open(str(d/'audio.wav')) as w:
            row=dict(source=n,video_frames=int(v['nb_frames']),pcm_stereo_frames=w.getnframes(),sample_rate=w.getframerate(),channels=w.getnchannels(),pcm_bytes_per_tick=800*4)
        assert row['sample_rate']==48000 and row['channels']==2
        assert row['pcm_stereo_frames']==row['video_frames']*800,row
        assert v['avg_frame_rate']=='60/1' and (v['width'],v['height'])==(2000,1120)
        sources.append(row)
    p=probe(F);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
    total=sum(s['dur']/s.get('speed',1) for s in plan())
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
    assert (v['width'],v['height'])==(1920,1080) and v['avg_frame_rate']=='60/1'
    assert a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2
    assert int(v['nb_frames'])==round(total*60),(v['nb_frames'],total)
    assert abs(float(v['duration'])-float(a['duration']))<1/60,(v['duration'],a['duration'])
    decode=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(F),'-f','null','-'],capture_output=True,text=True)
    assert decode.returncode==0 and not decode.stderr,decode.stderr
    offsets=[];timeline=json.loads((O/'shot-list.json').read_text())
    for i in [4,8,11,24,27,29,33,36]:
        s=timeline[i];duration=min(1.1,s['dur']-.4)
        actual=pcm(F,s['start']+.2,duration)
        reference=pcm(P/'caps'/s['src']/'audio.wav',s['source_start']+.2,duration)
        n=min(len(actual),len(reference));actual=actual[:n];reference=reference[:n]
        c=correlate(actual,reference,mode='full',method='fft');mid=n-1
        limit=2400;local=c[mid-limit:mid+limit+1];lag=int(np.argmax(local))-limit
        coeff=float(local.max()/np.sqrt(np.dot(actual,actual)*np.dot(reference,reference)))
        offsets.append(dict(shot=i,label=s.get('name'),lag_samples=lag,lag_ms=round(lag/48,3),correlation=round(coeff,5)))
        assert abs(lag)<=800 and coeff>.75,offsets[-1]
    stderr=subprocess.run(['ffmpeg','-nostdin','-i',str(F),'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    loud=json.loads(stderr[stderr.rindex('{'):stderr.rindex('}')+1]);assert abs(float(loud['input_i'])+14)<.5,loud
    assert float(loud['input_tp'])<=-.8,loud
    report=dict(duration=total,video={k:v[k] for k in ['codec_name','width','height','pix_fmt','avg_frame_rate','nb_frames','duration']},audio={k:a[k] for k in ['codec_name','sample_rate','channels','channel_layout','duration']},loudness=loud,sources=sources,av_waveform_checks=offsets,full_decode='passed')
    (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
