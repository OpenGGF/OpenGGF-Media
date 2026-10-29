#!/usr/bin/env python3
"""Menu evolution promo: review and verification helpers for a rendered master or MP4.

Purpose: the measurable half of the moving review (the eye half is watching it).
  review.py motion VIDEO              per-frame change; reports frozen runs (>= 20 identical frames)
  review.py strips VIDEO OUT FRAME... consecutive-frame strips (every 2nd frame, -6..+22) per frame
  review.py pixels MASTER             exact-integer-scale check: pane pixels vs. 4x/2x nearest copies
                                      of the source PNGs at sampled frames (FFV1 master only)
  review.py audio VIDEO               loudness per chapter (ebur128) and true peak
Inputs: the edit (edit.py) for its chapter/source map. Origin: menu-evolution-promo-20261029.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edit as ed  # noqa: E402

W, H = 1920, 1080


def decode(video, w=W, h=H, start=None, frames=None, scale=None):
    vf = []
    if start is not None:
        vf.append(f'select=between(n\\,{start}\\,{start + frames - 1})')
    if scale:
        vf.append(f'scale={scale[0]}:{scale[1]}:flags=area')
        w, h = scale
    cmd = ['ffmpeg', '-v', 'error', '-i', str(video)]
    if vf:
        cmd += ['-vf', ','.join(vf), '-fps_mode', 'passthrough']
    cmd += ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def motion(video):
    prev, same, runs, diffs = None, 0, [], []
    for i, fr in enumerate(decode(video, scale=(480, 270))):
        if prev is not None:
            d = float(np.abs(fr.astype(np.int16) - prev).mean())
            diffs.append(d)
            if d == 0:
                same += 1
            else:
                if same >= 20:
                    runs.append((i - same, i))
                same = 0
        prev = fr
    if same >= 20:
        runs.append((len(diffs) + 1 - same, len(diffs) + 1))
    print(f'{len(diffs) + 1} frames; frozen runs (>=20 identical frames): '
          + (', '.join(f'{a}-{b} ({a / 60:.2f}-{b / 60:.2f}s)' for a, b in runs) or 'none'))
    return runs, diffs


def strips(video, out, frames):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for t in frames:
        picks = list(range(t - 6, t + 24, 2))
        ims = list(decode(video, start=picks[0], frames=picks[-1] - picks[0] + 1))
        ims = ims[::2]
        tw, th = 480, 270
        sheet = Image.new('RGB', (tw * 5, th * ((len(ims) + 4) // 5)))
        for k, im in enumerate(ims):
            sheet.paste(Image.fromarray(im).resize((tw, th), Image.BILINEAR), ((k % 5) * tw, (k // 5) * th))
        p = out / f'strip-{t:05d}.png'
        sheet.save(p)
        print(p)


def pixels(master):
    e = ed.edit()
    checks = []
    # (output frame, era, take, take frame, pane x, pane y, scale): the pane must equal the source exactly
    for key, family, detail, take, b0, b1, in_beat, ticks in ed.REPS:
        for f in (ed.F(b0) + 10, ed.F(b1) - 10):
            d = ed.divider_at(f, key, ticks)
            era = 'new' if d >= 320 else 'pre' if d <= 0 else None
            if era:
                checks.append((f, era, take, ed.fr(in_beat) + f - ed.F(b0), *ed.PANE_L, 4))
    checks.append((ed.F(4) + 10, 'pre', 'shader', ed.F(4) + 10, *ed.PANE_C, 4))
    checks.append((ed.F(28), 'v05', 'v05-title', ed.F(28) - ed.F(24), *ed.PANE_C, 4))
    checks.append((ed.F(36), 'pre', 'hub', ed.F(36) - ed.F(32), *ed.PANE_C, 4))
    checks.append((ed.F(50), 'pre', 'mods', ed.GRID[2][1] + ed.F(50) - ed.F(40), *ed.GRID_POS[2], 2))
    checks.append((ed.F(166), 'new', 'locate', ed.WALL[3][1] + ed.F(166) - ed.F(160), 0, 540, 2))
    ok = 0
    for f, era, take, i, x, y, s in checks:
        got = next(decode(master, start=f, frames=1))
        src = ed.clip(era, take).native(i).astype(np.uint8)
        want = np.repeat(np.repeat(src, s, 0), s, 1)
        region = got[y:y + want.shape[0], x:x + want.shape[1]]
        bad = int((region != want).any(axis=2).sum())
        ok += bad == 0
        print(f'frame {f}: {era}/{take}#{i} at {s}x -> {"exact" if bad == 0 else f"{bad} pixels differ"}')
    print(f'{ok}/{len(checks)} panes exact integer nearest-neighbour copies of their source frames')


def audio(video):
    e = ed.edit()
    rows = []
    for f0, f1, title, _ in ed.CHAPTERS:
        r = subprocess.run(['ffmpeg', '-nostats', '-ss', f'{f0 / 60:.3f}', '-t', f'{(f1 - f0) / 60:.3f}', '-i', str(video),
                            '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
        tail = r.stderr[r.stderr.rfind('Summary:'):]
        integ = float(tail.split('I:')[1].split('LUFS')[0])
        peak = float(tail.split('Peak:')[1].split('dBFS')[0])
        rows.append((f0 / 60, f1 / 60, integ, peak, title))
        print(f'{f0 / 60:6.2f}-{f1 / 60:6.2f}s  I {integ:6.1f} LUFS  TP {peak:+5.1f} dBTP  {title}')
    return rows


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'motion':
        motion(sys.argv[2])
    elif cmd == 'strips':
        strips(sys.argv[2], sys.argv[3], [int(a) for a in sys.argv[4:]])
    elif cmd == 'pixels':
        pixels(sys.argv[2])
    elif cmd == 'audio':
        audio(sys.argv[2])
