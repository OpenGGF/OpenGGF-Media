#!/usr/bin/env python3
"""Readable-holds cut: measure the settled holds of the accepted hill-climb-story edit, for the before/after
record (origin menu-evolution-promo-20261029, revisions/readable-holds, 2026-10-29).

Purpose: the user found the hill-climb story's dense screens "flashed up too quickly to ingest" and said some
"transition as soon as they finish animating". This probe renders that edit (../../hill-climb-story/sources/
promo/edit.py, unchanged) with its footage and background held still, and for each dense screen walks back
from the frame where the screen starts to change to the first frame of its settled state: the hold the
viewer actually got. Inputs: the hill-climb-story edit and its production inputs (clips, evidence stills);
OPENGGF_WORKTREE as for edit.py. Usage: old_holds.py  (prints one row per screen; writes nothing).
"""
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

OLD = Path(__file__).resolve().parents[3] / 'hill-climb-story/sources/promo'
os.environ.setdefault('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-e4055369')
sys.path.insert(0, str(OLD))
import edit as old  # noqa: E402

_stage, _native = old.stage, old.Clip.native.__wrapped__
old.stage = lambda f: _stage(0)
old.Clip.native = lambda self, i: _native(self, 100)
F = old.F
# (screen, the frame its settled state starts to change: the next statement's fade or the cut, from the code)
STATES = [
    ('ask', F(4) - 2 - 8), ('step 1 labels', F(8) - 2 - 8), ('rubric matrix', F(16) - 8), ('target + loop', F(24)),
    ('round 4', F(32)), ('27-family board', F(36)), ('Time Attack 5.5 -> 8', F(40)), ('all 27 at 8', F(44) - 8),
    ('raised the bar', F(48) - 8), ('9 = production polish', F(56) - 8), ('pass 1 quote', F(64) - 8),
    ('review drop', F(72) - 8), ('structure, 13', F(80) - 2 - 8), ('sent back', F(82.5) - 2 - 8),
    ('finish, 26', F(86) - 2 - 8), ('last gap', old.SLAM), ('27 / 27 criteria row', old.IRIS),
    ('end card', old.END_HIT)]


def frame(f):
    return old.edit().render_frame(f)


def main():
    old.edit()
    with Pool(8) as pool:
        for name, t in STATES:
            fs = list(range(t - 150, t + 3))
            ims = dict(zip(fs, pool.map(frame, fs)))
            same = lambda a, b: not (ims[a] != ims[b]).any()
            first_change = next(f for f in range(t - 2, t + 3) if not same(f, t - 3))
            ref = first_change - 1
            s = ref
            while s - 1 in ims and same(s - 1, ref):
                s -= 1
            print(f'{name:24s} settled f{s} -> changes f{first_change}: hold {(first_change - s) / 60:.2f} s')


if __name__ == '__main__':
    main()
