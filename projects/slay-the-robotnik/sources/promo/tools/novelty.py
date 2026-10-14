#!/usr/bin/env python3
"""Checkerboard novelty on beat-synchronous spectra: peaks mark section changes (in beats)."""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from beats import load, tempo
bpm, first, x, sr = tempo(sys.argv[1])
p = 60 / bpm
beats = np.arange(first, len(x) / sr - p, p)
F = []
for a in beats:
    seg = x[int(a * sr):int((a + p) * sr)]
    s = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 8192))[:2000]
    s = np.log1p(s.reshape(100, 20).sum(axis=1))
    F.append(s / (np.linalg.norm(s) + 1e-9))
F = np.array(F)
S = F @ F.T
K = int(sys.argv[2]) if len(sys.argv) > 2 else 8
g = np.outer(np.r_[-np.ones(K), np.ones(K)], np.r_[-np.ones(K), np.ones(K)])
nov = np.zeros(len(F))
for i in range(K, len(F) - K):
    nov[i] = (S[i - K:i + K, i - K:i + K] * g).sum()
top = np.argsort(nov)[::-1]
picked = []
for i in top:
    if all(abs(i - j) > K for j in picked):
        picked.append(i)
    if len(picked) >= 14:
        break
for i in sorted(picked):
    print(f"beat {i:4d}  t={beats[i]:6.2f}s  novelty={nov[i]:.2f}")
