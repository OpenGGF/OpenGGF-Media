#!/usr/bin/env python3
"""Purpose: labelled sheet of frames from stage B probes or takes (any folder under the task root).
Usage: plook.py out.jpg cols thumb_w dir/id:first:last:n ... Origin: MT promo redo stage B 2026-11-12."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parent.parent
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cells = []
for spec in sys.argv[4:]:
    name, a, b, n = spec.split(':'); a, b, n = int(a), int(b), int(n)
    fr = sorted((T / name / 'frames').glob('*.png')); idx = [int(f.stem) for f in fr]
    for k in range(n):
        w = a + round((b - a) * k / max(1, n - 1))
        j = min(range(len(idx)), key=lambda i: abs(idx[i] - w))
        cells.append((f'{Path(name).name} #{idx[j]}', Image.open(fr[j]).convert('RGB')))
th = round(tw * 224 / 320)
S = Image.new('RGB', (cols * tw, ((len(cells) + cols - 1) // cols) * (th + 13)), (10, 10, 30)); D = ImageDraw.Draw(S)
for k, (lab, im) in enumerate(cells):
    x, y = k % cols * tw, k // cols * (th + 13)
    S.paste(im.resize((tw, th), Image.BOX if tw < 320 else Image.NEAREST), (x, y)); D.text((x + 2, y + th + 1), lab, fill='yellow')
S.save(out, quality=85); print(out, S.size)
