#!/usr/bin/env python3
"""Purpose: mine the takes already on disk for fast, eventful windows (no ROM time): per take, mean speed,
interaction list and the best N-frame window by events + speed. Reuses tools/pacing.py's event detector.
Usage: mine.py [window_frames=168] > table. Origin: MICA & TALON promo redo, pacing revision 2026-11-12."""
import json, math, sys
from pathlib import Path
sys.argv = sys.argv[:1] + sys.argv[1:]
T = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(T / 'tools'))
import pacing
W = int(sys.argv[1]) if len(sys.argv) > 1 else 168
out = []
for d in sorted((T / 'captures').iterdir()):
    if not (d / 'state.csv').exists() or not (d / 'frames').exists():
        continue
    try:
        r = pacing.rows(d.name)
    except Exception:
        continue
    lv = [i for i, x in enumerate(r) if x.get('mode') == 'LEVEL']
    if len(lv) < 120:
        continue
    try:
        pv = json.load(open(d / 'provenance.json'))
    except Exception:
        pv = {}
    ev = pacing.events(d.name, 1, len(r) - 1)
    sp = [math.hypot(pacing.num(x, 'xvel'), pacing.num(x, 'yvel')) for x in r]
    hard = [e for e in ev if e[1] in ('kill', 'boss hit', 'spring', 'spindash', 'transform', 'ring loss', 'hurt')]
    best = (-1, 0)
    for a in range(1, max(2, len(r) - W), 6):
        n = sum(1 for e in ev if a <= e[0] < a + W and e[1] in ('kill', 'boss hit', 'spring', 'spindash'))
        n += 0.3 * sum(1 for e in ev if a <= e[0] < a + W and e[1] in ('air burst', 'rings'))
        hurt = any(a <= e[0] < a + W and e[1] in ('hurt', 'ring loss') for e in ev)
        sc = n + sum(sp[a:a + W]) / W / 1024 - (5 if hurt else 0)
        if sc > best[0]:
            best = (sc, a)
    a = best[1]
    out.append(dict(id=d.name, game=pv.get('game'), zone=pv.get('zone'), act=pv.get('act'), main=(pv.get('props') or {}).get('promo.main') or pv.get('main'),
                    sk=(pv.get('props') or {}).get('promo.sidekick') or pv.get('sidekick'), em=(pv.get('props') or {}).get('promo.emeralds') or pv.get('emeralds'),
                    frames=len(r), mean_v=round(sum(sp[i] for i in lv) / len(lv)), best_a=a, best_score=round(best[0], 2),
                    best_v=round(sum(sp[a:a + W]) / W), ev=[f'{k}{dd}@{f}' for f, k, dd in ev if k != 'rings'][:14],
                    note=(pv.get('note') or '')[:110]))
json.dump(out, open(T / 'checkpoint4/mine.json', 'w'), indent=1)
for o in sorted(out, key=lambda o: -o['best_score']):
    print(f"{o['id']:24} {str(o['game']):4} z{str(o['zone']):4} {str(o['main'])[-6:]:6}/{str(o['sk'])[-6:]:6} em {str(o['em']):8} n{o['frames']:5} v{o['mean_v']:5} best@{o['best_a']:4} s{o['best_score']:5} bv{o['best_v']:5} | {' '.join(o['ev'])}")
