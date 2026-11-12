#!/usr/bin/env python3
"""Purpose: the promo's music bed = the owner-supplied track from its first sample, uncut, with one fade-out.
No splices: samples [0, fade_end) are the source's own, multiplied only by the fade curve after fade_start.
The fade is a raised cosine from the bar-85 line to the bar-88 line (tracked bar lines, tools/beat_track.py):
see README "Music" for why the track cannot be used past bar 88.
Inputs: source WAV, beat-track.json, out WAV [fade_start_bar fade_end_bar]. Output stays in the task dir only.
Origin: MICA & TALON promo redo 2026-11-11."""
import json, sys, wave
import numpy as np
src, bt, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
b0, b1 = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (85, 88)
T = [b['t'] for b in bt['bars']]
w = wave.open(src); sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
assert (sr, ch, sw) == (48000, 2, 2), (sr, ch, sw)
x = np.frombuffer(w.readframes(n), np.int16).reshape(-1, 2).astype(np.float64)
s0, s1 = int(round(T[b0] * sr)), int(round(T[b1] * sr))
y = x[:s1 + sr].copy()            # one second of digital silence after the fade for the picture's tail
u = np.clip((np.arange(len(y)) - s0) / (s1 - s0), 0, 1)
y *= (0.5 * (1 + np.cos(np.pi * u)))[:, None]
o = wave.open(out, 'wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr)
o.writeframes(np.round(y).clip(-32768, 32767).astype(np.int16).tobytes()); o.close()
print(f'bed: source 0.000-{s1 / sr:.3f} s uncut; fade bar {b0} ({s0 / sr:.3f} s) -> bar {b1} ({s1 / sr:.3f} s), '
      f'{(s1 - s0) / sr:.3f} s raised cosine; -6 dB at {(s0 + s1) / 2 / sr:.3f} s; file {len(y) / sr:.3f} s')
