#!/usr/bin/env python3
"""Per-bar features for a track (beat grid from beats.py): loudness, low-band energy and the
novelty against the previous bar and the bar four before, to locate phrase boundaries."""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from beats import load, tempo
path = sys.argv[1]
bpm, first, x, sr = tempo(path)
period = 60 / bpm
beats = np.arange(first, len(x) / sr - period, period)
def feat(a, b):
    seg = x[int(a * sr):int(b * sr)]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    bands = [spec[(f >= lo) & (f < hi)].sum() for lo, hi in [(30, 150), (150, 400), (400, 1000), (1000, 2500), (2500, 6000), (6000, 16000)]]
    v = np.log1p(np.array(bands))
    return v
off = int(sys.argv[2]) if len(sys.argv) > 2 else 0
bars = [feat(beats[i], beats[i + 4]) for i in range(off, len(beats) - 4, 4)]
print(f"{bpm:.3f} BPM, period {period:.5f}s, first beat {first:.3f}s, bar offset {off}")
for i, v in enumerate(bars):
    t = beats[off + i * 4]
    n1 = np.linalg.norm(v - bars[i - 1]) if i else 0
    n4 = np.linalg.norm(v - bars[i - 4]) if i >= 4 else 0
    print(f"bar {i:3d} t={t:6.2f}  low={v[0]:.1f} mid={v[2]:.1f} hi={v[4]:.1f}  d1={n1:.2f} d4={n4:.2f}")
