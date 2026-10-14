#!/usr/bin/env python3
"""check_av.py — audio/video alignment of the final promo against the exact pre-loudnorm PCM (task e0603654).
Cross-correlates 8 kHz mono windows of the final AAC track and work/audio.wav; reports the best lag per window."""
import subprocess, struct, sys
from pathlib import Path
O = Path(__file__).resolve().parent.parent
def pcm(path):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                       capture_output=True, check=True).stdout
    return struct.unpack(f"<{len(b)//2}h", b)
fin, ref = pcm(O / "out/mutator-lab-gameplay-promo.mp4"), pcm(O / "work/audio.wav")
out = []
for t in (2, 8, 12, 20, 27, 33, 40, 46, 50):
    s, n = int(t * 8000), 4000
    r = ref[s:s + n]
    rn = sum(x * x for x in r) ** 0.5 or 1
    best = None
    for lag in range(-240, 241, 2):
        f = fin[s + lag:s + lag + n]
        if len(f) < n: continue
        c = sum(a * b for a, b in zip(r, f)) / (rn * (sum(x * x for x in f) ** 0.5 or 1))
        if best is None or c > best[1]: best = (lag, c)
    out.append((t, best[0] / 8.0, round(best[1], 3)))
    print(f"t={t:4.1f}s  lag={best[0]/8.0:+.2f} ms  corr={best[1]:.3f}", flush=True)
