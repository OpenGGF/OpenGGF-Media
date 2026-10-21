#!/usr/bin/env python3
"""Rebuild the Stageplay promo from a lossless cutscene and explicit frame-accurate EDL.
Inputs: production root, FFmpeg/FFprobe and DejaVu Sans. Origin: Stageplay, 2026-10-21.
No ROM data is embedded. Run in a relocated working copy, not the preserved archive.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

FPS=60
RATE=48000

def run(command):
    result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode: raise RuntimeError(result.stderr[-5000:])
    return result.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def assemble(root,out,font):
    edits=json.loads((root/'edl.json').read_text())
    if out.exists(): raise ValueError('Choose a new output filename')
    sources={row['source'] for row in edits}
    if len(sources)!=1: raise ValueError('This edit uses one retained lossless source')
    source=root/next(iter(sources)); info=probe(source)
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (video['width'],video['height'],video['r_frame_rate'],audio['sample_rate'])!=(400,224,'60/1','48000'):
        raise ValueError('Expected 400x224,60Hz,48kHz source')
    duration=float(info['format']['duration']); prior=0; chapters=[]; filters=[]
    with tempfile.TemporaryDirectory(prefix='.stageplay-edit-',dir=out.parent) as staging:
        staging=Path(staging)
        n=len(edits)
        filters += ['[0:v]split='+str(n)+''.join(f'[v{i}]' for i in range(n)),
                    '[0:a]asplit='+str(n)+''.join(f'[a{i}]' for i in range(n))]
        for i,row in enumerate(edits):
            start=round(row['source_start_seconds']*FPS);end=round(row['source_end_seconds']*FPS)
            if start<0 or end<=start or end/FPS>duration or abs(start/FPS-row['source_start_seconds'])>1e-6 or abs(end/FPS-row['source_end_seconds'])>1e-6:
                raise ValueError('Invalid or non-frame-aligned source interval')
            if i and row['source_start_seconds']<edits[i-1]['source_end_seconds']:
                raise ValueError('Accidental overlapping/reversed intervals')
            label=staging/f'label-{i}.txt';label.write_text(row['title'])
            footer=staging/f'footer-{i}.txt';footer.write_text(row['subtitle'])
            # Paths below are tool-owned POSIX paths. Refuse FFmpeg filter metacharacters.
            for path in [font,label,footer]:
                if any(c in str(path) for c in "':,;[]\\"): raise ValueError('Relocate font/output to a plain path')
            filters.append(f'[v{i}]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,'
                'scale=1200:672:flags=neighbor,pad=1280:720:40:24:color=0x101827,'
                f'drawtext=fontfile={font}:textfile={label}:fontsize=18:fontcolor=0xFFE184:x=40:y=2,'
                f'drawtext=fontfile={font}:textfile={footer}:fontsize=15:fontcolor=0xD6E4FF:x=40:y=698,'
                f'setsar=1,format=yuv420p[vx{i}]')
            length=(end-start)/FPS
            filters.append(f'[a{i}]atrim=start_sample={start*RATE//FPS}:end_sample={end*RATE//FPS},asetpts=PTS-STARTPTS,'
                f'afade=t=in:st=0:d=0.02,afade=t=out:st={length-.03:.8f}:d=0.03[ax{i}]')
            chapters.append(dict(row,output_start_frame=prior,output_end_frame=prior+end-start,
                                 output_start_seconds=prior/FPS,output_end_seconds=(prior+end-start)/FPS))
            prior+=end-start
        filters.append(''.join(f'[vx{i}][ax{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[v][a]')
        graph=staging/'filter.txt';graph.write_text(';\n'.join(filters))
        metadata=staging/'chapters.ffmeta'
        metadata.write_text(';FFMETADATA1\ntitle=OpenGGF Stageplay — Location, Location, Location\n'+''.join(
            f"[CHAPTER]\nTIMEBASE=1/60\nSTART={c['output_start_frame']}\nEND={c['output_end_frame']}\ntitle={c['title']}\n" for c in chapters))
        staged=staging/'promo.mp4'
        run(['ffmpeg','-v','error','-i',str(source),'-f','ffmetadata','-i',str(metadata),'-filter_complex',graph.read_text(),
             '-map','[v]','-map','[a]','-map_metadata','1','-map_chapters','1','-c:v','libx264','-preset','slow','-crf','18',
             '-threads','4','-c:a','aac','-b:a','192k','-movflags','+faststart',str(staged)])
        run(['ffmpeg','-v','error','-xerror','-i',str(staged),'-f','null','-'])
        final=probe(staged);stream=next(s for s in final['streams'] if s['codec_type']=='video')
        if int(stream['nb_frames'])!=prior or stream['r_frame_rate']!='60/1':raise ValueError('Output cadence/frame count mismatch')
        os.link(staged,out)
    (root/'chapters.json').write_text(json.dumps(chapters,indent=2)+'\n')
    return dict(output=out.name,frames=prior,seconds=prior/FPS,width=1280,height=720,chapters=len(chapters),fullDecode='passed')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--font',type=Path,required=True);a=p.parse_args()
    print(json.dumps(assemble(a.root.resolve(),a.out.resolve(),a.font.resolve()),indent=2))
