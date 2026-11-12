#!/usr/bin/env python3
"""Purpose: cut the Sol mascot drawings out of their flat magenta ground, for the character introduction cards.
The drawings are read in place from the owner's release-promo project and the cut-outs are written to this task's
scratch folder (art/), never to a repository.
Method: the same as art() in that project's tools/animatic.py (line 185): a region is background if it is near
the corner colour and mostly the exact colour, which keeps pinks inside the drawing; alpha ramps over the rim and
the rim pixels are repainted in ink so no magenta fringe survives. The white sticker edge is added later, at the
size the card needs (edit/cards.py).
Run with that project's Python (it has scipy): <release-promo>/.venv/bin/python tools/sol_art.py
Origin: MICA & TALON promo redo, character introductions, 2026-11-12."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = Path('/home/farrell/.t3/projects/openggf-release-promo/out/art/sol')
OUT = Path(__file__).resolve().parent.parent / 'art'
OUT.mkdir(exist_ok=True)
for name in sys.argv[1:] or ['mica-hero', 'talon-hero', 'name-mica', 'name-talon', 'duo-sunrise', 'duo-sunrise-b']:
    rgb = np.asarray(Image.open(SRC / f'{name}.png').convert('RGB')).astype(np.int16)
    far = np.abs(rgb - rgb[4, 4]).sum(2)
    regions, count = ndimage.label(far < 220)
    exact = ndimage.mean(far < 40, regions, np.arange(1, count + 1))
    back = np.isin(regions, np.flatnonzero(exact > 0.2) + 1)
    alpha = np.where(back, np.clip((far - 60) / 160, 0, 1), 1.0)
    rgb[alpha < 1] = (36, 36, 36)
    im = Image.fromarray(np.dstack([rgb.astype(np.uint8), (alpha * 255).astype(np.uint8)]), 'RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
    im.save(OUT / f'{name}.png')
    print(name, im.size)
