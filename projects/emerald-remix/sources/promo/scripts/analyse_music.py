#!/usr/bin/env python3
"""Analyse the planning bed and export its reproducible editorial grid. No capture.
Inputs: checkout promo_kit.py and rendered full-mix WAV. Origin: Emerald Remix promo, 2026-10-22.
"""
import argparse, csv, hashlib, importlib.util, json, subprocess, sys, wave
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--checkout',type=Path,default=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach'))
a=p.parse_args(); root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('promo_kit',a.checkout/'tools/media/promo_kit.py');kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)
raw=root/'audio/raw/s2-music-91-mix.wav'; x=kit.read_wav(raw);mono=x.mean(axis=1)
bpm,first=kit.tempo(mono);period=60/bpm
nov=[dict(beat=b,seconds=t,novelty=n) for b,t,n in kit.sections(mono,bpm,first)]
# Frame-exact review endpoint at the strong late novelty candidate; no internal song edits.
end_frame=round((first+125*period)*60);end=end_frame/60
bed=root/'audio/emerald-remix-review-bed.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-t',str(end),'-af',f'highpass=f=20,volume=6dB,afade=t=out:st={end-2}:d=2','-ar','48000','-c:a','pcm_s16le',str(bed)],check=True)
with (root/'audio/beats.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['beat_zero_based','seconds','video_frame_60fps','editorial_bar_zero_based','beat_in_bar_zero_based'])
 for b in range(126):w.writerow([b,f'{first+b*period:.6f}',round((first+b*period)*60),b//4,b%4])
with (root/'audio/section-candidates.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['beat','seconds','novelty']);w.writeheader();w.writerows(nov)
# Independent first attack, after removing the initial constant chip/DC baseline.
# A first-nonzero check would incorrectly report t=0 because the renderer begins with DC.
with wave.open(str(raw)) as w:
 raw_pcm=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(float)/32768
baseline=np.median(raw_pcm[:480],axis=0)
first_material=int(np.flatnonzero(np.max(np.abs(raw_pcm-baseline),axis=1)>0.01)[0])/48000
windows=[]
for start in (0,18,36):
 b,ph=kit.tempo(mono,start=start,length=24);windows.append(dict(start_seconds=start,bpm=b,first_beat_seconds=ph))
report=dict(source_commit='8aa692b045c195ef8a42896b6bbc9549158470c0',track='Sonic 2 Emerald Hill Zone (2P)',music_id_hex='91',render='accurate FM core; NTSC; full SMPS mix; not gameplay audio',sample_rate=48000,channels=2,raw_duration_seconds=len(x)/48000,bpm=bpm,first_beat_seconds=first,period_seconds=period,first_attack_over_initial_baseline_seconds=first_material,initial_dc_baseline=baseline.tolist(),onset_threshold_above_baseline=0.01,phase_distance_from_first_material_ms=(first-first_material)*1000,independent_24_second_windows=windows,sections_are='spectral novelty candidates, not certified musical downbeats',review_frames=end_frame,review_duration_seconds=end,review_highpass_hz=20,review_gain_db=6,review_fade_out_seconds=2,sha256={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (raw,bed)},phase_review='PCM onset comparison performed; no physical listening or bar/downbeat confirmation performed. Audition before footage lock.')
(root/'audio/analysis.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
