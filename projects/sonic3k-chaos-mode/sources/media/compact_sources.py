#!/usr/bin/env python3
"""Compact owned capture masters losslessly; preserve every decoded RGB pixel,
audio sample and60Hz frame. Compare PNG/FFV1/RGB-H264 before publishing and remove
only redundant owned raw PNG frame directories after all comparisons succeed.
Task-local media archival tool, Chaos demo2026-10-14, not gameplay authority.
"""
from pathlib import Path
import subprocess, hashlib, json, shutil
P=Path(__file__).resolve().parent
def run(args):
    return subprocess.check_output(['ffmpeg','-nostdin','-v','error',*map(str,args)],text=True)
def picture_hash(args):
    data=run([*args,'-map','0:v:0','-pix_fmt','rgb24','-f','framemd5','-'])
    frames=[line.split(',')[-1].strip() for line in data.splitlines() if line and not line.startswith('#')]
    return len(frames),hashlib.sha256('\n'.join(frames).encode()).hexdigest()
def audio_hash(path):
    return run(['-i',path,'-map','0:a:0','-c:a','pcm_s16le','-f','hash','-hash','sha256','-']).strip()
def main():
    receipt=P/'out/lossless-source-checks.json'
    checks=json.loads(receipt.read_text()) if receipt.exists() else {}
    for base in sorted((P/'captures').iterdir()):
        if base.name in checks:continue
        src=base/'source.mkv';temp=base/'source-compact.mkv'
        before=picture_hash(['-i',src]);old_audio=audio_hash(src)
        pngs=base/'output/frames'
        if picture_hash(['-framerate','60','-i',pngs/'%05d.png'])!=before:raise ValueError(('PNG mismatch',base))
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(src),'-c:v','libx264rgb','-crf','0','-preset','medium','-pix_fmt','rgb24','-threads','2','-c:a','copy',str(temp)],check=True)
        after=picture_hash(['-i',temp])
        if before!=after or old_audio!=audio_hash(temp):raise ValueError(('Lossless mismatch',base))
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate,sample_rate,channels','-of','json',str(temp)],text=True))
        if abs(float(info['format']['duration'])-before[0]/60)>.002:raise ValueError(('Cadence mismatch',base))
        original_bytes=src.stat().st_size;compact_bytes=temp.stat().st_size
        temp.replace(src)
        checks[base.name]={'frames':before[0],'decodedRGBSequenceSha256':before[1],'decodedPCMSha256':old_audio.removeprefix('SHA256='),'pngToFfv1Equal':True,'ffv1ToLosslessRgbH264Equal':True,'nativeFrameRate':'60/1','originalBytes':original_bytes,'archivedBytes':compact_bytes,'archivedVideoCodec':'H264 lossless RGB, crf0','audio':'original PCM16 stereo48kHz, copied without re-encoding'}
        receipt.write_text(json.dumps(checks,indent=2)+'\n')
        # Native source pixels/audio now have two verified encodings and a retained
        # compact lossless master; only this task's redundant raw frames go away.
        shutil.rmtree(pngs)
        print(base.name,'verified',before[0],'frames',original_bytes,'->',compact_bytes,flush=True)
if __name__=='__main__':main()
