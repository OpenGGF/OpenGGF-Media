#!/usr/bin/env python3
"""Soundtrack QA picture for the r5 promo (Opus, 2026-10-06): per-frame level of the final mix
(decoded from the MP4) with segment boundaries, editorial pieces shaded, and each segment's
source capture labelled. Writes promo.waveform.png. Usage: waveform.py putt-putt-paradise-promo.mp4"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_promo as rp  # noqa: E402

mp4 = Path(sys.argv[1])
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vn", "-f", "s16le", "-ac", "2", "-ar", "48000", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).reshape(-1, 2).astype(np.float32) / 32768
frames = len(x) // rp.SPF
level = 20 * np.log10(np.maximum(x[:frames * rp.SPF].reshape(frames, rp.SPF, 2).std(axis=1).max(axis=1), 1e-5))
Wd, Hd = 2400, 520
im = Image.new("RGB", (Wd, Hd), (12, 20, 30))
d = ImageDraw.Draw(im)
font = ImageFont.truetype(rp.FONT_DIR + rp.F_BODY, 16)
sx = Wd / frames
for s in rp.segments():
    x0 = s.start * sx
    if s.cap is None:
        d.rectangle((x0, 40, (s.start + s.frames) * sx, Hd - 60), fill=(40, 30, 60))
    d.line((x0, 30, x0, Hd - 40), fill=(80, 110, 130))
    d.text((x0 + 3, Hd - 56 + (rp.segments().index(s) % 2) * 18), f"{s.name} [{s.cap or 'editorial'}]", font=font, fill=(200, 210, 220))
for db in (-60, -40, -20, 0):
    y = 40 + (0 - db) / 70 * (Hd - 100)
    d.line((0, y, Wd, y), fill=(40, 55, 70)); d.text((4, y - 18), f"{db} dBFS", font=font, fill=(120, 140, 150))
pts = [(i * sx, 40 + (0 - max(-70, v)) / 70 * (Hd - 100)) for i, v in enumerate(level)]
d.line(pts, fill=(255, 212, 91), width=1)
d.text((8, 6), f"{mp4.name}: per-frame level of the final mix ({frames} frames at 60 fps); shaded = editorial music", font=font, fill=(255, 255, 255))
im.save(mp4.parent / "promo.waveform.png")
print("wrote promo.waveform.png")
