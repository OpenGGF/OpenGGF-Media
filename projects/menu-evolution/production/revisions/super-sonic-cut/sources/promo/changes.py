#!/usr/bin/env python3
"""Per-take visible-change finder: frames where a native take's picture changes, with changed-pixel
counts, for picking in-points and syncing UI cues (super-sonic-cut, 2026-10-29).
Usage: changes.py <era> <take> [min_pixels]. Reads ../../../../clips (the original production clips)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
CLIPS = Path(__file__).resolve().parents[4] / 'clips'
era, take = sys.argv[1], sys.argv[2]
mn = int(sys.argv[3]) if len(sys.argv) > 3 else 200
d = CLIPS / era / take / 'frames'
n = len(list(d.glob('*.png')))
prev = None
out = []
for i in range(n):
    a = np.asarray(Image.open(d / f'{i:05d}.png').convert('RGB'))
    if prev is not None:
        c = int((a != prev).any(axis=2).sum())
        if c >= mn:
            out.append((i, c))
    prev = a
# collapse consecutive frames into runs
runs, cur = [], None
for i, c in out:
    if cur and i == cur[1] + 1:
        cur = [cur[0], i, max(cur[2], c)]
    else:
        if cur:
            runs.append(cur)
        cur = [i, i, c]
if cur:
    runs.append(cur)
print(f'{era}/{take} {n} frames; change runs (first-last, max px):')
print(' '.join(f'{a}-{b}:{c}' if a != b else f'{a}:{c}' for a, b, c in runs))
