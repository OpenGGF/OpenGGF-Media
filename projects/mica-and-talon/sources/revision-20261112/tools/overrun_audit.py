#!/usr/bin/env python3
"""Purpose: find shots that outlive their source. promo_kit's Frames clamps an index past the end of a capture and
holds the last frame, and its check() only warns for Game shots, so a Custom shot or a split pane can freeze
silently (one draft froze three panes for a second that way). This renders every Nth output frame with
Frames.frame patched to record requests past the end (or before frame 0) and lists them per capture.
Inputs: edit/edit.py [step=2]. Output: JSON on stdout. Origin: MICA & TALON promo redo 2026-11-12."""
import json, os, sys
from multiprocessing import Pool
from pathlib import Path

T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit  # noqa: E402

_E = None
_BAD = []


def _init():
    global _E
    orig = promo_kit.Frames.frame.__wrapped__

    def frame(self, i):
        n = len(self)
        if i > n - 1 or i < 0:
            _BAD.append((self.path.parent.name, int(i), n))
        return orig(self, i)

    promo_kit.Frames.frame = frame
    _E = promo_kit.load_edit(str(T / 'edit/edit.py'))


def _one(f):
    _BAD.clear()
    _E.render_frame(f)
    return [(f,) + b for b in _BAD]


if __name__ == '__main__':
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    e = promo_kit.load_edit(str(T / 'edit/edit.py'))
    fs = list(range(0, e.end(), step))
    with Pool(8, initializer=_init) as pool:
        res = pool.map(_one, fs, chunksize=24)
    by = {}
    for rows in res:
        for f, name, i, n in rows:
            d = by.setdefault(name, dict(capture_frames=n, first_output_frame=f, last_output_frame=f, max_requested=i, min_requested=i))
            d['last_output_frame'] = f
            d['max_requested'] = max(d['max_requested'], i)
            d['min_requested'] = min(d['min_requested'], i)
    json.dump(dict(sampled_frames=len(fs), step=step, overruns=by), sys.stdout, indent=1)
