#!/usr/bin/env python3
"""filmsheet.py OUTPREFIX seg_id... : for each segment, first/middle/last output frames of the final film (480x270) in rows."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parents[1]
ch = json.load(open(T / "out/chapters.json"))
film = T / "out/mutator-lab-complete-showcase.mp4"
pre, ids = sys.argv[1], sys.argv[2:]
idx, starts = 0, {}
for s in ch["segments"]:
    starts[s["id"]] = (idx, s["frames"]); idx += s["frames"]
def grab(n):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(film), "-vf", f"select=eq(n\\,{n}),scale=480:270", "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (480, 270), b[:480 * 270 * 3])
rows = []
for sid in ids:
    a, n = starts[sid]
    ims = []
    for f in (a + 1, a + n // 2, a + n - 2):
        im = grab(f); ImageDraw.Draw(im).text((4, 4), f"{sid} {f}", fill=(255, 0, 255)); ims.append(im)
    rows.append(ims)
sheet = Image.new("RGB", (480 * 3, 270 * len(rows)))
for r, ims in enumerate(rows):
    for c, im in enumerate(ims): sheet.paste(im, (c * 480, r * 270))
sheet.save(T / "work" / f"{pre}.png"); print(T / "work" / f"{pre}.png")
