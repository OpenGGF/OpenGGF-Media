#!/usr/bin/env python3
"""Purpose: one labelled sheet of evenly spaced whole frames from several takes' windows, to pick replacement
windows without ROM time. Usage: peek.py out.jpg cols thumb_w id:first:last[:n] ... Origin: MT promo redo 2026-11-12."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parent.parent
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cells = []
for spec in sys.argv[4:]:
    p = spec.split(':'); name, a, b = p[0], int(p[1]), int(p[2]); n = int(p[3]) if len(p) > 3 else cols
    fr = sorted((T / 'captures' / name / 'frames').glob('*.png'))
    for k in range(n):
        i = min(len(fr) - 1, a + round((b - a) * k / max(1, n - 1)))
        cells.append((f'{name} #{i}', Image.open(fr[i]).convert('RGB')))
th = round(tw * 224 / 320)
S = Image.new('RGB', (cols * tw, ((len(cells) + cols - 1) // cols) * (th + 13)), (10, 10, 30)); D = ImageDraw.Draw(S)
for k, (lab, im) in enumerate(cells):
    x, y = k % cols * tw, k // cols * (th + 13)
    S.paste(im.resize((tw, th), Image.BOX if tw < 320 else Image.NEAREST), (x, y)); D.text((x + 2, y + th + 1), lab, fill='yellow')
S.save(out, quality=84); print(out, S.size)
