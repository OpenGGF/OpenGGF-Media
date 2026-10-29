#!/usr/bin/env python3
"""Compact old|new pair grid of a take at given take frames (1x native, 3 pairs per row), for
choosing in-points (super-sonic-cut, 2026-10-29). Usage: pairgrid.py <take> <out.png> <frame>..."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
CLIPS = Path(__file__).resolve().parents[4] / 'clips'
take, out, frames = sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]]
per = 3
rows = (len(frames) + per - 1) // per
sheet = Image.new('RGB', (per * 660, rows * 240), (60, 60, 60))
for k, f in enumerate(frames):
    x0, y0 = (k % per) * 660, (k // per) * 240
    for c, era in enumerate(('pre', 'new')):
        p = CLIPS / era / take / 'frames' / f'{f:05d}.png'
        if p.exists():
            sheet.paste(Image.open(p).convert('RGB'), (x0 + c * 324, y0 + 14))
    ImageDraw.Draw(sheet).text((x0 + 2, y0 + 1), f'{take} f{f}  (pre | new)', fill='yellow')
sheet.save(out)
print(out)
