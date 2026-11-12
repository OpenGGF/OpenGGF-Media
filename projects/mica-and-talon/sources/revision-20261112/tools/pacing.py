#!/usr/bin/env python3
"""Purpose: measure the pace of every shot of the current cut from the per-frame state CSVs, for the pacing
re-storyboard (owner feedback 2026-11-12: "set scenes could do with improvement when gspeed is low and no
badnik/boss interactions").
Method: render every 2nd output frame with promo_kit.Frames.frame instrumented, so each shot (and each pane of a
split shot) gets the exact source frames it shows; then, over those frames of the take's state.csv:
  mean |gspeed| (the CSV's subpixels/frame, 256 = 1 px/frame; it is 0 or stale in the air, so it understates
  flight and jumps), mean speed (the larger of hypot(xvel, yvel) and the frame-to-frame displacement, so a tube
  or a carry that moves her with no velocity still counts), camera travel, and the interactions found in the rows:
  score steps (badnik or boss hits), ring pickups, ring loss, springs (launch with yvel <= -0x900 or a one-frame
  ground xvel step >= 0x800), air bursts (homing strike / divebomb: a one-frame airborne velocity step
  >= 0x600), spindash releases, transformations (powered host columns).
  idle = frames with speed < 1.5 px/frame and no interaction within 30 frames either side.
Subject 'sk_' panes (TALON as sidekick) take speed from his position deltas.
Usage: pacing.py out.json. Origin: MICA & TALON promo redo, stage A of the 2026-11-12 pacing revision."""
import csv, json, math, os, sys
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
        _LOG.append((self.path.parent.name, int(i)))
        return orig(self, i)

    promo_kit.Frames.frame = frame
    _E = promo_kit.load_edit(str(T / 'edit/edit.py'))


def _one(f):
    _LOG.clear()
    _E.render_frame(f)
    return f, sorted(set(_LOG))


_ROWS = {}


def rows(name):
    if name not in _ROWS:
        _ROWS[name] = list(csv.DictReader(open(T / 'captures' / name / 'state.csv')))
    return _ROWS[name]


def num(r, k, d=0.0):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return d


def events(name, a, b):
    """Interactions in rows [a, b] of a take: list of (frame, kind, detail)."""
    r = rows(name)
    ev = []
    for i in range(max(1, a), min(len(r) - 1, b) + 1):
        p, q = r[i - 1], r[i]
        if q.get('mode') != 'LEVEL' or p.get('mode') != 'LEVEL':
            continue
        ds = num(q, 'score') - num(p, 'score')
        if ds > 0:
            ev.append((i, 'boss hit' if ds >= 1000 else 'kill', f'+{int(ds)}'))
        dr = num(q, 'rings') - num(p, 'rings')
        if dr > 0:
            ev.append((i, 'rings', f'+{int(dr)}'))
        elif dr < -1:
            ev.append((i, 'ring loss', f'{int(dr)}'))
        if num(q, 'hurt') and not num(p, 'hurt'):
            ev.append((i, 'hurt', ''))
        dvx, dvy = num(q, 'xvel') - num(p, 'xvel'), num(q, 'yvel') - num(p, 'yvel')
        air0, air1 = num(p, 'air'), num(q, 'air')
        if not air0 and air1 and num(q, 'yvel') <= -0x900:
            ev.append((i, 'spring', 'up'))
        elif not air0 and not air1 and abs(dvx) >= 0x800 and not num(p, 'spindash'):
            ev.append((i, 'spring', 'side'))
        elif air0 and air1 and math.hypot(dvx, dvy) >= 0x600 and ds <= 0:
            ev.append((i, 'air burst', ''))
        if num(p, 'spindash') and not num(q, 'spindash'):
            ev.append((i, 'spindash', ''))
        for k, lab in (('p1_super', 'MICA'), ('sk_super', 'TALON')):
            if k in q and q[k] != p.get(k) and q[k] not in ('', '0', 'false'):
                ev.append((i, 'transform', lab))
    return ev


def measure(name, src, key=''):
    r = rows(name)
    src = [min(len(r) - 1, max(1, i)) for i in src]
    a, b = min(src), max(src)
    level = [i for i in src if r[i].get('mode') == 'LEVEL']
    out = dict(capture=name, src=[a, b], frames=len(src) * 2)
    if len(level) < len(src) * 0.6:
        out['kind'] = sorted({r[i].get('mode') for i in src})[0].lower()
        return out
    out['kind'] = 'level'
    if key:
        sp = []
        for i in level:
            j = max(1, i - 1)
            sp.append(256 * math.hypot((num(r[i], key + 'x') - num(r[j], key + 'x')), (num(r[i], key + 'y') - num(r[j], key + 'y'))))
        out['subject'] = 'TALON (sidekick; speed from position)'
    else:
        # the larger of the velocity and the real displacement: a tube or a carry moves her with near-zero velocity
        sp = [max(math.hypot(num(r[i], 'xvel'), num(r[i], 'yvel')),
                  min(6400.0, 256 * math.hypot(num(r[i], 'x') - num(r[i - 1], 'x'), num(r[i], 'y') - num(r[i - 1], 'y'))))
              for i in level]
    gs = [abs(num(r[i], 'gspeed')) for i in level]
    ev = events(name, a, b)
    evf = [e[0] for e in ev]
    idle = [i for i, s in zip(level, sp) if s < 384 and not any(abs(i - f) <= 30 for f in evf)]
    run = best = 0
    prev = None
    for i in idle:
        run = run + 1 if prev is not None and i - prev <= 2 else 1
        best = max(best, run); prev = i
    cam = abs(num(r[b], 'cam_x') - num(r[a], 'cam_x')) + abs(num(r[b], 'cam_y') - num(r[a], 'cam_y'))
    out.update(mean_gspeed=round(sum(gs) / len(gs)), mean_speed=round(sum(sp) / len(sp)),
               air_share=round(sum(num(r[i], 'air') for i in level) / len(level), 2),
               cam_px_per_s=round(cam / max(1, b - a) * 60), idle_s=round(len(idle) * 2 / 60, 2),
               longest_idle_s=round(best * 2 / 60, 2), events=[dict(src=f, kind=k, detail=d) for f, k, d in ev])
    return out


if __name__ == '__main__':
    out = sys.argv[1]
    e = promo_kit.load_edit(str(T / 'edit/edit.py'))
    mod = next(m for k, m in sys.modules.items() if k.startswith('promo_edit_')) if any(k.startswith('promo_edit_') for k in sys.modules) else None
    shots = sorted(e.shots, key=lambda s: s.f0)
    fs = list(range(0, e.end(), 2))
    with Pool(6, initializer=_init) as pool:
        res = dict(pool.map(_one, fs, chunksize=24))
    table = []
    for n, s in enumerate(shots):
        guard = (getattr(s, 'tdur', 0) or 0) + 2 if getattr(s, 'trans', None) else 0
        use = {}
        for f in range(s.f0 + guard + (s.f0 + guard) % 2, s.f1, 2):
            for name, i in res.get(f, []):
                use.setdefault(name, []).append((f, i))
        panes = []
        for name, fi in use.items():
            if len(fi) < 8 or not (T / 'captures' / name / 'state.csv').exists():
                continue
            m = measure(name, [i for _, i in fi])
            m['on_screen_s'] = [round(fi[0][0] / 60, 2), round(fi[-1][0] / 60, 2)]
            m['out0'], m['src0'] = fi[0]
            panes.append(m)
        table.append(dict(shot=n, f0=s.f0, f1=s.f1, t0=round(s.f0 / 60, 2), t1=round(s.f1 / 60, 2), panes=panes))
    json.dump(table, open(out, 'w'), indent=1)
    for row in table:
        print(f"#{row['shot']:>2} {row['t0']:6.2f}-{row['t1']:6.2f}")
        for p in row['panes']:
            if p['kind'] != 'level':
                print(f"      {p['capture']:22} {p['src']} {p['kind']}")
                continue
            evs = ', '.join(f"{x['kind']}{x['detail']}@{x['src']}" for x in p['events'][:9])
            print(f"      {p['capture']:22} {str(p['src']):11} g {p['mean_gspeed']:5} v {p['mean_speed']:5} air {p['air_share']:.2f} "
                  f"cam {p['cam_px_per_s']:4} idle {p['idle_s']:4} (run {p['longest_idle_s']}) | {evs}")
