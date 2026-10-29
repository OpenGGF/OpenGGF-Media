#!/usr/bin/env python3
"""Contact sheet of a take in two eras side by side, sampled at given frames (2x, nearest).
Usage: pairsheet.py <take> <out.png> <frame>... [--eras pre,new]. Origin: menu-evolution-promo-20261029."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
eras = next((a.split('=')[1] for a in sys.argv if a.startswith('--eras=')), 'pre,new').split(',')
take, out, frames = args[0], args[1], [int(a) for a in args[2:]]
cols = len(eras)
sheet = Image.new('RGB', (cols * 640 + (cols - 1) * 8, len(frames) * 456), (40, 40, 40))
for r, f in enumerate(frames):
    for c, era in enumerate(eras):
        p = ROOT / 'clips' / era / take / 'frames' / f'{f:05d}.png'
        if p.exists():
            im = Image.open(p).convert('RGB').resize((640, 448), Image.NEAREST)
            sheet.paste(im, (c * 648, r * 456))
        ImageDraw.Draw(sheet).text((c * 648 + 4, r * 456 + 2), f'{era} f{f}', fill='yellow')
sheet.save(out)
print(out)
