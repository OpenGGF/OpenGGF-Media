#!/usr/bin/env python3
"""Purpose: prove a take's audio.wav is the SFX-only stem and is in step with the picture.
Per video frame (rate/60 samples) it takes the RMS in dBFS, then reports: the audio length against the frame
count, how many frames are digital silence, the first loud frame, the RMS over a named quiet range and a named
event range, and the frames on which sound starts (onsets) beside the jump presses in state.csv.
Usage: rms_check.py CAPDIR [quiet_a quiet_b event_a event_b]. Output: one JSON line.
Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import csv, json, math, sys, wave
from pathlib import Path
import numpy as np

d = Path(sys.argv[1])
with wave.open(str(d / 'audio.wav')) as w:
    rate, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
    x = np.frombuffer(w.readframes(n), dtype='<i2').astype(np.float64).reshape(-1, ch) / 32768.0
spf = rate / 60.0
frames = int(n / spf + 0.5)
rows = list(csv.DictReader(open(d / 'state.csv'))) if (d / 'state.csv').exists() else []
db = []
for i in range(frames):
    seg = x[int(i * spf):int((i + 1) * spf)]
    r = math.sqrt(float((seg ** 2).mean())) if len(seg) else 0.0
    db.append(20 * math.log10(r) if r > 0 else -120.0)
rng = lambda a, b: round(float(np.mean(db[a:b])), 1) if b > a else None
onsets = [i for i in range(1, frames) if db[i] > -60 and db[i - 1] <= -60]
presses = [i for i in range(1, len(rows)) if 'A' in rows[i].get('input', '').split('|')[1] and 'A' not in rows[i - 1].get('input', '').split('|')[1]] if rows and '|' in rows[0].get('input', '') else []
out = dict(take=d.name, rate=rate, video_frames=len(rows), audio_frames=frames, silent_frames=sum(v <= -100 for v in db),
           loud_frames=sum(v > -60 for v in db), peak_dbfs=round(20 * math.log10(max(1e-9, float(np.abs(x).max()))), 1),
           first_loud=next((i for i, v in enumerate(db) if v > -60), None), onsets=onsets[:14], jump_presses=presses[:14])
if len(sys.argv) > 5:
    qa, qb, ea, eb = map(int, sys.argv[2:6])
    out.update(quiet=[qa, qb], quiet_rms_db=rng(qa, qb), event=[ea, eb], event_rms_db=rng(ea, eb))
print(json.dumps(out))
