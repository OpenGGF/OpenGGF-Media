#!/usr/bin/env python3
"""One row per clip: N frames evenly spaced over [first, last], labelled; for picking in/out points."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
out, n, first, last, names = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:]
W, H = 200, 112
sheet = Image.new("RGB", (W * n + 150, H * len(names)))
d = ImageDraw.Draw(sheet)
for r, name in enumerate(names):
    fs = sorted((ROOT / "build/frames" / name).glob("frame-*.png"))
    hi = min(last, len(fs) - 1)
    d.text((2, r * H + 50), name[:24], fill="white")
    for c in range(n):
        k = first + (hi - first) * c // (n - 1)
        im = Image.open(fs[k]).convert("RGB").resize((W, H), Image.BILINEAR)
        ImageDraw.Draw(im).text((2, 1), str(k), fill="yellow")
        sheet.paste(im, (150 + c * W, r * H))
sheet.save(ROOT / "build" / out)
