"""Purpose: zoomed strip of a capture around the player (or whole frame) to judge sprite art and effects.
Usage: zstrip.py CAPDIR first last step out.png [scale=3] [crop_w=128] [crop_h=96] [key=''|sk_] [cols=8]
Origin: MICA & TALON promo redo 2026-11-11."""
import sys, csv
from pathlib import Path
from PIL import Image, ImageDraw
d = Path(sys.argv[1]); a, b, st = map(int, sys.argv[2:5]); out = sys.argv[5]
sc = int(sys.argv[6]) if len(sys.argv) > 6 else 3
cw = int(sys.argv[7]) if len(sys.argv) > 7 else 128
ch = int(sys.argv[8]) if len(sys.argv) > 8 else 96
key = sys.argv[9] if len(sys.argv) > 9 else ''
cols = int(sys.argv[10]) if len(sys.argv) > 10 else 8
fr = sorted((d / 'frames').glob('*.png')); rows = list(csv.DictReader(open(d / 'state.csv'))) if (d / 'state.csv').exists() else []
idx = list(range(a, min(b, len(fr)), st))
S = Image.new('RGB', (cols * cw * sc, ((len(idx) + cols - 1) // cols) * (ch * sc + 12)), (10, 10, 30)); D = ImageDraw.Draw(S)
for k, i in enumerate(idx):
    im = Image.open(fr[i]).convert('RGB')
    if cw >= im.width and ch >= im.height:
        cx, cy = im.width // 2, im.height // 2
    else:
        r = rows[min(i, len(rows) - 1)] if rows else {}
        try:
            cx = int(float(r[key + 'x']) - float(r['cam_x'])); cy = int(float(r[key + 'y']) - float(r['cam_y']))
        except Exception:
            cx, cy = im.width // 2, im.height // 2
    x0 = max(0, min(im.width - cw, cx - cw // 2)); y0 = max(0, min(im.height - ch, cy - ch // 2))
    c = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((cw * sc, ch * sc), Image.NEAREST)
    x = k % cols * cw * sc; y = k // cols * (ch * sc + 12); S.paste(c, (x, y)); D.text((x + 2, y + ch * sc), str(i), fill='white')
S.save(out); print(out, len(idx))
