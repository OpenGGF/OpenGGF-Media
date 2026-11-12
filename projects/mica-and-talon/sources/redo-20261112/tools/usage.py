#!/usr/bin/env python3
"""Purpose: which captures does the final edit actually put on screen, and does any shot outlive its source?
Renders every Nth output frame of the edit (16:9, or 9:16 with MT_VERTICAL=1) with promo_kit.Frames.frame
instrumented, and writes per capture: source frames used (min, max), output seconds first/last seen, and any
request past the end of the capture (the kit clamps those silently and only warns for Game shots).
Usage: [MT_VERTICAL=1] usage.py out.json [step=3]. Origin: MICA & TALON promo redo 2026-11-12."""
import json, os, sys
from multiprocessing import Pool
from pathlib import Path

T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit  # noqa: E402

_E = None
_LOG = []


def _init():
    global _E
    orig = promo_kit.Frames.frame.__wrapped__

    def frame(self, i):
        _LOG.append((self.path.parent.name, int(i), len(self)))
        return orig(self, i)

    promo_kit.Frames.frame = frame
    _E = promo_kit.load_edit(str(T / 'edit/edit.py'))


def _one(f):
    _LOG.clear()
    _E.render_frame(f)
    return [(f,) + b for b in set(_LOG)]


if __name__ == '__main__':
    out = sys.argv[1]
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    e = promo_kit.load_edit(str(T / 'edit/edit.py'))
    fs = list(range(0, e.end(), step))
    with Pool(6, initializer=_init) as pool:
        res = pool.map(_one, fs, chunksize=24)
    use, over = {}, {}
    for rows in res:
        for f, name, i, n in rows:
            u = use.setdefault(name, dict(capture_frames=n, src_min=i, src_max=i, first_s=f / e.fps, last_s=f / e.fps))
            u['src_min'] = min(u['src_min'], max(0, i)); u['src_max'] = max(u['src_max'], min(n - 1, i)); u['last_s'] = f / e.fps
            if i > n - 1 or i < 0:
                o = over.setdefault(name, dict(capture_frames=n, first_output_frame=f, max_requested=i))
                o['max_requested'] = max(o['max_requested'], i)
    for u in use.values():
        u['first_s'] = round(u['first_s'], 2); u['last_s'] = round(u['last_s'], 2)
    json.dump(dict(vertical=os.environ.get('MT_VERTICAL') == '1', sampled_frames=len(fs), step=step, seconds=e.end() / e.fps,
                   captures=dict(sorted(use.items())), overruns=over), open(out, 'w'), indent=1)
    print(out, len(use), 'captures used;', len(over), 'overruns', over)
