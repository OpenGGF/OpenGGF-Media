#!/usr/bin/env python3
"""Hill-climb story cut: pixel identity of the moving takes against the design review's own captures.

Purpose: the film labels some delivered-tree (d823ce643) take frames as the state the review scored at a
given pass ("AT 8 · 28 OCT", "PASS 3 · DELIVERED"). This probe proves or refutes each label by comparing a
take frame with the audit's capture of the same scene at each recorded head (64ed120d2, a694db926 = the
target-8 delivery, d8d947336 = structural pass, a513dd5fd = finish pass).
Inputs: the original production's clips/ (two levels above this revision) and the audit's evidence sets
(MENU_EVIDENCE, default: the production root's parent). Origin: menu-evolution revision hill-climb-story,
2026-10-29. Usage: identity.py   (prints the share of differing pixels per take frame and capture set)
"""
import glob
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edit as ed  # noqa: E402

SETS = {'64ed120d2': 'all-menus-target8-20261028/baseline/320', 'a694db926': 'menu-target9-20261028/baseline/320',
        'd8d947336': 'menu-target9-20261028/structural/final/320', 'a513dd5fd': 'menu-target9-20261028/finish/final/320'}
CASES = [  # (take, take frame, capture name prefix, what the film claims)
    ('mods', 52, 'menus/m12', 'ch4 "AT 8": the Mod manager list is the 8 build (and unchanged after)'),
    ('legal', 398, 'menus/m20', 'ch4 "AT 8": the legal notice is the 8 build (differences = the blinking prompt)'),
    ('settings', 86, 'hub/11-', 'ch11 "PASS 3 · DELIVERED": Settings Display changed after the structural pass'),
]


def load(p):
    return np.asarray(Image.open(p).convert('RGB'), np.int16)


def main():
    for take, i, prefix, claim in CASES:
        frame = load(ed.CLIPS / 'new' / take / 'frames' / f'{i:05d}.png')
        row = []
        for head, rel in SETS.items():
            g = sorted(glob.glob(str(ed.EVID / rel / f'{prefix}*.png')))
            if not g:
                row.append(f'{head}: none')
                continue
            d = (np.abs(load(g[0]) - frame).sum(axis=2) > 0).mean() * 100
            row.append(f'{head}: {d:.2f}%')
        print(f'new/{take}#{i} vs {os.path.basename(g[0]) if g else prefix}: ' + ', '.join(row) + f'  [{claim}]')


if __name__ == '__main__':
    main()
