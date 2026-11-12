"""Purpose: one row of evenly spaced frames per capture, to triage a batch at a glance.
Usage: overview.py out.jpg cols capture_id[:first:last] ...  Origin: MICA & TALON promo redo 2026-11-11."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parent.parent
out, cols = sys.argv[1], int(sys.argv[2]); specs = sys.argv[3:]
tw = 1920 // cols
rows = []
for spec in specs:
    p = spec.split(':'); name = p[0]
    fr = sorted((T / 'captures' / name / 'frames').glob('*.png'))
    if not fr:
        continue
    a = int(p[1]) if len(p) > 1 else 0; b = min(int(p[2]) if len(p) > 2 else len(fr) - 1, len(fr) - 1)
    rows.append((name, fr, a, b))
w0, h0 = Image.open(rows[0][1][0]).size
th = max(Image.open(r[1][0]).size[1] * tw // Image.open(r[1][0]).size[0] for r in rows)
S = Image.new('RGB', (tw * cols, len(rows) * (th + 12)), (10, 10, 30)); D = ImageDraw.Draw(S)
for r, (name, fr, a, b) in enumerate(rows):
    for k in range(cols):
        i = a + (b - a) * k // (cols - 1)
        im = Image.open(fr[i]).convert('RGB'); im = im.resize((tw, im.height * tw // im.width), Image.BILINEAR)
        S.paste(im, (k * tw, r * (th + 12)))
        D.text((k * tw + 2, r * (th + 12) + th), f'{name} {i}', fill='white')
S.save(out, quality=82); print(out)
