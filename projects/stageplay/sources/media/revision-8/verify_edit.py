#!/usr/bin/env python3
"""Verify revision-eight edit cadence, full decode, chapters and sectional AAC levels.
Inputs: candidate directory containing plan.json, chapters.json and tutorial.mp4.
Origin: Stageplay revision eight, 2026-10-22. Does not claim hearing or creative approval.
"""
import argparse,hashlib,json,re,subprocess
from pathlib import Path

def call(args):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-3000:])
    return p

def levels(path,start=None,end=None):
    cmd=['ffmpeg','-hide_banner','-nostdin','-i',path]
    filt=(f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,' if start is not None else '')+'ebur128=peak=true'
    p=call(cmd+['-vn','-af',filt,'-f','null','-'])
    tail=p.stderr.rsplit('Summary:',1)[-1]
    return {'integratedLufs':float(re.search(r'I:\s+(-?[\d.]+) LUFS',tail)[1]),'truePeakDbfs':float(re.search(r'Peak:\s+(-?[\d.]+) dBFS',tail)[1])}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);a=ap.parse_args();r=a.candidate
    plan=json.loads((r/'plan.json').read_text());edl=json.loads((r/'chapters.json').read_text());v=r/'tutorial.mp4'
    p=json.loads(call(['ffprobe','-v','error','-count_frames','-show_streams','-show_chapters','-show_format','-of','json',v]).stdout)
    vid=next(s for s in p['streams'] if s['codec_type']=='video');aud=next(s for s in p['streams'] if s['codec_type']=='audio')
    assert int(vid['nb_read_frames'])==plan['frames'];assert (vid['width'],vid['height'],vid['avg_frame_rate'])==(1920,1080,'60/1')
    assert len(p['chapters'])==len(edl);assert aud['channels']==2 and aud['sample_rate']=='48000'
    for c,s in zip(p['chapters'],edl):
        assert abs(float(c['start_time'])-s['startFrame']/60)<.002
        assert abs(float(c['end_time'])-s['endFrame']/60)<.002
        assert s['playbackRate']==(0 if s['instructionalFreeze'] else 1)
    call(['ffmpeg','-v','error','-nostdin','-xerror','-i',v,'-f','null','-'])
    sections=[]
    for s in edl:
        sections.append({'title':s['title'],'startSeconds':s['startFrame']/60,'endSeconds':s['endFrame']/60,**levels(v,s['startFrame']/60,s['endFrame']/60)})
    result={'file':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'frames':int(vid['nb_read_frames']),'dimensions':[vid['width'],vid['height']],'fps':vid['avg_frame_rate'],'seconds':plan['seconds'],'chapters':len(edl),'audioChannels':aud['channels'],'fullDecode':'passed','encodedAudio':levels(v),'sections':sections,'limits':'Encoded measurements only. Full-rate motion review and visual inspection recorded separately; no physical listening claim.'}
    (r/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
