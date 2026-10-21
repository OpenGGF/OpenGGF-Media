#!/usr/bin/env python3
"""Decode and measure retained Stageplay films; this does not replace moving review.

Inputs: final MKVs/MP4 in this production directory; FFmpeg and FFprobe.
Origin: OpenGGF Stageplay live-world delivery, 2026-10-21.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def run(command):
    r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
    return r.stdout,r.stderr


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);args=p.parse_args()
    root=args.root.resolve();expected={'live-platform-relay-review':480,'live-air-traffic-review':540,'live-ring-run-review':240,
                                      'one-more-take-review':3600,'stageplay-live-promo':3600}
    records=[]
    for file in sorted([*root.glob('*.mkv'),*root.glob('*.mp4')]):
        if file.stem not in expected:continue
        stdout,_=run(['ffprobe','-v','error','-count_frames','-show_streams','-show_chapters','-show_format','-of','json',str(file)])
        probe=json.loads(stdout);v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
        assert v['r_frame_rate']=='60/1' and int(v['nb_read_frames'])==expected[file.stem]
        assert a['channels']==2 and int(a['sample_rate'])==48000
        run(['ffmpeg','-v','error','-xerror','-i',str(file),'-f','null','-'])
        _,meter=run(['ffmpeg','-hide_banner','-nostats','-i',str(file),'-af','ebur128=peak=true','-vn','-f','null','-'])
        summary=meter[meter.rfind('Summary:'):];lufs=float(re.search(r'I:\s*([-\d.]+) LUFS',summary).group(1));peak=float(re.search(r'Peak:\s*([-\d.]+) dBFS',summary).group(1))
        assert peak < -1, (file,peak)
        if file.stem=='stageplay-live-promo':assert len(probe['chapters'])==5 and (v['width'],v['height'])==(1280,896)
        with file.open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
        records.append(dict(file=file.name,sha256=sha,frames=int(v['nb_read_frames']),dimensions=[v['width'],v['height']],
                            duration=float(probe['format']['duration']),fps=v['r_frame_rate'],audioChannels=2,audioRate=48000,
                            lufs=lufs,truePeakDbfs=peak,fullDecode=True,chapters=probe['chapters']))
    assert any(r['file']=='stageplay-live-promo.mp4' for r in records)
    out=root/'decoded-media-checks.json';out.write_text(json.dumps({'measurements':records,'limits':'Decode/cadence/audio metering; no claim of physical listening or user creative approval.'},indent=2)+'\n')
    print(json.dumps({'files':len(records),'allDecoded':True,'report':str(out)}))

if __name__=='__main__':main()
