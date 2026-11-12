#!/usr/bin/env python3
"""Purpose: for every full-frame gameplay shot of the edit, count the output frames on which the hero is not
whole on screen (16:9: the 320x180 window; 9:16: the tall frame's 126 px), from the take's state.csv. A fast
dive can outrun the game's camera; a shot must not sit on an empty frame.
Usage: MT_CAPTURES=<folder> onscreen.py. Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import csv, os, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit
e = promo_kit.load_edit(str(T / 'edit/edit.py'))
CAP = T / os.environ.get('MT_CAPTURES', 'captures')
for st in sorted(e.stems, key=lambda s: s[2]):
    wav, src, at, n, gain = st
    take = Path(wav).parent.name
    r = list(csv.DictReader(open(CAP / take / 'state.csv')))
    if r[min(len(r) - 1, src)].get('mode') != 'LEVEL':
        continue
    key = 'sk_' if take in () else ''
    out_h, out_v, worst = 0, 0, []
    run = best = 0
    for j in range(n):
        q = r[min(len(r) - 1, src + j)]
        x, y = float(q['x']) - float(q['cam_x']), float(q['y']) - float(q['cam_y'])
        off = not (14 <= x <= 306 and 14 <= y <= 166)
        out_h += off
        run = run + 1 if off else 0
        best = max(best, run)
        out_v += not (116 + 14 <= x <= 242 - 14 and 14 <= y <= 210)
    flag = 'CHECK' if best >= 12 else ''
    print(f'{at / 60:6.2f}s {take:18} src {src:5}-{src + n:5}  off 16:9 {out_h:3}/{n} (longest run {best:3})  outside tall-frame centre {out_v:3}  {flag}')
