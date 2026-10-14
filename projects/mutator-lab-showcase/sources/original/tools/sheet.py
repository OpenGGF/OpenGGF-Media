#!/usr/bin/env python3
"""Contact sheet: sheet.py CAPTURE OUT.png frame frame ... (4 columns, labelled)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parents[1]
cap, out, *fs = sys.argv[1:]
d = T / "captures" / cap / "capture" / "frames"
ims = []
for f in fs:
    im = Image.open(d / f"{int(f):05d}.png").convert("RGB"); ImageDraw.Draw(im).text((250, 2), f, fill=(255, 0, 255)); ims.append(im)
W, H = ims[0].size; cols = 4; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, H * rows))
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * W, (i // cols) * H))
sheet.save(T / "work" / out)
