#!/usr/bin/env python3
"""Contact sheet of a recorded clip: every Nth frame, labelled with its frame number."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
name, step = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 30
first = int(sys.argv[3]) if len(sys.argv) > 3 else 0
last = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
fs = sorted((ROOT / "build/frames" / name).glob("frame-*.png"))
fs = [f for f in fs if first <= int(f.stem[6:]) <= last][::step][:40]
cols = 5
rows = (len(fs) + cols - 1) // cols
sheet = Image.new("RGB", (400 * cols, 224 * rows))
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 34, 10], fill="black")
    d.text((1, 0), f.stem[6:], fill="yellow")
    sheet.paste(im, ((i % cols) * 400, (i // cols) * 224))
out = ROOT / "build" / f"sheet-{name}.png"
sheet.save(out)
print(out)
