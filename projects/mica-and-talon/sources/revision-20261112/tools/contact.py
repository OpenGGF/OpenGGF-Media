#!/usr/bin/env python3
"""Purpose: contact sheet of an ENCODED master: one frame every N seconds, time-labelled.
Usage: contact.py video out.jpg step_s cols thumb_w [t0]. Origin: MICA & TALON promo redo 2026-11-12."""
import io, subprocess, sys
from PIL import Image, ImageDraw
v, out, step, cols, tw = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
t0 = float(sys.argv[6]) if len(sys.argv) > 6 else step / 2
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
ts = []
while t0 < dur - 0.05:
    ts.append(t0); t0 += step
ims = []
for t in ts:
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', v, '-frames:v', '1', '-vf', f'scale={tw}:-2:flags=lanczos', '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True)
    ims.append(Image.open(io.BytesIO(r.stdout)).convert('RGB'))
th = ims[0].height
S = Image.new('RGB', (cols * tw, ((len(ims) + cols - 1) // cols) * (th + 16)), (10, 10, 30)); d = ImageDraw.Draw(S)
for k, (t, im) in enumerate(zip(ts, ims)):
    x, y = (k % cols) * tw, (k // cols) * (th + 16)
    S.paste(im, (x, y)); d.text((x + 3, y + th + 2), f'{t:.1f} s', fill='yellow')
S.save(out, quality=86); print(out, S.size, len(ims))
