#!/usr/bin/env python3
"""Purpose: master the promo_kit render to -14 LUFS / TP <= -1.0 dBTP and deliver H.264 high/yuv420p + AAC 320k,
then measure the ENCODED file (ebur128 peak=true), ffprobe it and fully decode it.
Inputs: kit render (video stream + promo-audio.wav in the edit's work dir), output path, optional chapters file.
Origin: MICA & TALON production promo 2026-11-11. promo_kit's own ceiling is sample-peak only."""
import json, re, subprocess, sys
from pathlib import Path

work, out = Path(sys.argv[1]), Path(sys.argv[2])
chapters = Path(sys.argv[3]) if len(sys.argv) > 3 else None
video, audio = work / 'promo-video.mp4', work / 'promo-audio.wav'
TARGET_I, TARGET_TP = -14.0, -1.5   # aim under -1.0 so AAC overshoot still lands <= -1.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


# pass 1: measure
m = run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(audio), '-af',
         f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=11:print_format=json', '-f', 'null', '-']).stderr
j = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
mastered = work / 'promo-audio-mastered.wav'
af = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
      f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
      "aresample=48000")
run(['ffmpeg', '-hide_banner', '-y', '-i', str(audio), '-af', af, '-ar', '48000', '-c:a', 'pcm_s16le', str(mastered)])

meta = []
if chapters and chapters.exists():
    meta = ['-i', str(chapters), '-map_metadata', '2', '-map_chapters', '2']


def encode(gain_db):
    cmd = ['ffmpeg', '-hide_banner', '-y', '-i', str(video), '-i', str(mastered)] + meta + [
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
        '-preset', 'slow', '-crf', '16', '-tune', 'animation', '-r', '60',
        '-af', f'volume={gain_db}dB', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000',
        '-movflags', '+faststart', '-shortest', str(out)]
    run(cmd)


def measure():
    e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(out), '-map', '0:a:0', '-af',
                        'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = e[e.rindex('Summary:'):]
    i = float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1))
    lra = float(re.search(r'LRA:\s+(-?[\d.]+) LU', s).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))
    return i, tp, lra, s


gain = 0.0
for attempt in range(3):
    encode(gain)
    i, tp, lra, summary = measure()
    if tp <= -1.0:
        break
    gain -= (tp + 1.05)
probe = run(['ffprobe', '-v', 'error', '-show_entries',
             'stream=codec_name,profile,pix_fmt,width,height,avg_frame_rate,bit_rate,sample_rate,channels:format=duration',
             '-of', 'json', str(out)]).stdout
dec = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'], capture_output=True, text=True)
report = dict(out=str(out), integrated_lufs=i, true_peak_dbtp=tp, lra_lu=lra, extra_gain_db=gain,
              pass1=j, ffprobe=json.loads(probe), full_decode_exit=dec.returncode, decode_errors=dec.stderr[-2000:])
(out.with_suffix('.loudness.json')).write_text(json.dumps(report, indent=2))
print(json.dumps({k: report[k] for k in ('out', 'integrated_lufs', 'true_peak_dbtp', 'lra_lu', 'extra_gain_db',
                                         'full_decode_exit')}))
print(summary)
