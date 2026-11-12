#!/usr/bin/env python3
"""Purpose: contact sheet of the vertical cut straight from the edit (no encode): frames at the given output
times or every N seconds, laid out in portrait thumbnails with time labels.
Usage: MT_VERTICAL=1 vsheet.py out.jpg cols thumb_w t0 t1 step | vsheet.py out.jpg cols thumb_w @t,t,t...
Origin: MICA & TALON promo redo 2026-11-12."""
import os, sys
from multiprocessing import Pool
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit
_E = None


def _init():
    global _E
    _E = promo_kit.load_edit(str(T / 'edit/edit.py'))


def _one(args):
    f, tw = args
    im = Image.fromarray(_E.render_frame(f))
    return f, im.resize((tw, im.height * tw // im.width), Image.LANCZOS)


if __name__ == '__main__':
    out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if sys.argv[4].startswith('@'):
        ts = [float(x) for x in sys.argv[4][1:].split(',')]
    else:
        t0, t1, st = map(float, sys.argv[4:7])
        ts = []
        while t0 < t1:
            ts.append(t0); t0 += st
    with Pool(8, initializer=_init) as pool:
        res = pool.map(_one, [(int(round(t * 60)), tw) for t in ts])
    th = res[0][1].height
    S = Image.new('RGB', (cols * tw, ((len(res) + cols - 1) // cols) * (th + 16)), (10, 10, 30))
    d = ImageDraw.Draw(S)
    for k, (f, im) in enumerate(res):
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        S.paste(im, (x, y)); d.text((x + 3, y + th + 2), f'{f / 60:.1f} s', fill='yellow')
    S.save(out, quality=86); print(out, S.size, len(res))
