#!/usr/bin/env python3
"""Purpose: do the hits read under the music? The film's game sound is each take's own SFX-only stem; this
measures, for every event the picture shows (kill, boss hit, spring, spindash release, carry grab,
transformation), the loudest 100 ms of the SFX bus in the 250 ms from the event against the music bed over the
same samples, at the gains the edit uses. Also the whole SFX bus against the bed, and each event's distance from
the nearest tracked beat. Nothing here listens: it is a measurement.
Usage: MT_CAPTURES=<folder> mixcheck.py [out.json]. Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import csv, json, math, os, sys
from pathlib import Path
import numpy as np

T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
sys.path.insert(0, str(T / 'tools'))
import promo_kit
from promo_kit import SR, read_wav

e = promo_kit.load_edit(str(T / 'edit/edit.py'))
spf = SR // e.fps
total = e.end()
BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
BEATS = [int(round((BT[n] + (BT[n + 1] - BT[n]) * k / 4) * 60)) for n in range(88) for k in range(4)]


def bus(items):
    out = np.zeros((total * spf + SR, 2), np.float32)
    for a, at, gain in items:
        at = int(at)
        a = a[:max(0, len(out) - at)]
        out[at:at + len(a)] += a * gain
    return out[:total * spf]


bed = bus([(read_wav(w)[int(src * SR):], at * spf, g) for w, at, g, src, length, fin, fout in e.beds])
sfx = bus([(read_wav(w)[src * spf:(src + n) * spf], at * spf, g) for w, src, at, n, g in e.stems])


def db(a):
    return 20 * math.log10(max(float(np.sqrt((a ** 2).mean())) if len(a) else 0.0, 1e-9))


def num(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return 0.0


rows, seen = [], set()
for w, src, at, n, g in sorted(e.stems, key=lambda s: s[2]):
    take = Path(w).parent.name
    r = list(csv.DictReader(open(Path(w).parent / 'state.csv')))
    run = 0
    for i in range(max(1, src), min(len(r), src + n)):
        p, q = r[i - 1], r[i]
        if q.get('mode') != 'LEVEL':
            continue
        kind = None
        ds = num(q, 'score') - num(p, 'score')
        if ds >= 1000:
            kind = 'boss hit'
        elif ds >= 100:
            kind = 'kill'
        elif ds == 10:
            kind = 'bumper'
        elif not num(p, 'air') and num(q, 'air') and num(q, 'yvel') <= -0x900:
            kind = 'spring'
        elif not num(p, 'air') and not num(q, 'air') and abs(num(q, 'xvel') - num(p, 'xvel')) >= 0x800 and not num(p, 'spindash'):
            kind = 'spring'
        elif num(p, 'spindash') and not num(q, 'spindash'):
            kind = 'spindash'
        elif q.get('p1_state') == 'TRANSFORMING' and p.get('p1_state') != 'TRANSFORMING':
            kind = 'transform'
        if q.get('sk_x'):
            dx, dy = num(q, 'x') - num(q, 'sk_x'), num(q, 'y') - num(q, 'sk_y')
            run = run + 1 if abs(dx) <= 1 and 27 <= dy <= 29 else 0
            if run == 1 and kind is None and num(p, 'y') - num(p, 'sk_y') != dy and 20 <= i - src:
                pass
        if kind is None:
            continue
        f = at + i - src
        if (f, kind) in seen:
            continue
        seen.add((f, kind))
        a0 = f * spf
        seg = sfx[a0:a0 + SR // 4]
        power = (seg ** 2).mean(axis=1)
        win = SR // 10
        j = int(np.argmax(np.convolve(power, np.ones(win) / win, mode='valid'))) if len(power) > win else 0
        s_db, b_db = db(seg[j:j + win]), db(bed[a0 + j:a0 + j + win])
        k = min(range(len(BEATS)), key=lambda x: abs(BEATS[x] - f))
        rows.append(dict(t=round(f / 60, 2), take=take, src=i, event=kind, sfx_db=round(s_db, 1), bed_db=round(b_db, 1), under_bed_db=round(b_db - s_db, 1),
                         bar=k // 4, beat=k % 4 + 1, frames_from_beat=f - BEATS[k]))
hits = [r for r in rows if r['event'] in ('kill', 'boss hit')]
ub = sorted(r['under_bed_db'] for r in hits)
loud = np.abs(sfx).max(axis=1) > 1e-4
summary = dict(sfx_gain=getattr(next(m for n, m in sys.modules.items() if n.startswith('promo_edit_')), 'SFXG', None) if any(n.startswith('promo_edit_') for n in sys.modules) else None,
               events=len(rows), kills_and_boss_hits=len(hits),
               hits_under_bed_db=dict(min=ub[0], median=ub[len(ub) // 2], max=ub[-1]) if ub else None,
               hits_more_than_6_db_under=[(r['t'], r['take'], r['under_bed_db']) for r in hits if r['under_bed_db'] > 6],
               hits_within_1_frame_of_a_beat=sum(abs(r['frames_from_beat']) <= 1 for r in hits),
               worst_hit_offset_frames=max((abs(r['frames_from_beat']) for r in hits), default=None),
               sfx_bus_db_where_sounding=round(db(sfx[loud]), 1), bed_db=round(db(bed[: int(119 * SR)]), 1),
               sfx_peak=round(float(np.abs(sfx).max()), 3), sounding_share=round(float(loud.mean()), 2))
if len(sys.argv) > 1:
    json.dump(dict(summary=summary, events=rows), open(sys.argv[1], 'w'), indent=1)
print(json.dumps(summary))
for r in rows:
    print(f"{r['t']:7.2f} {r['take']:18} {r['event']:9} sfx {r['sfx_db']:6.1f} bed {r['bed_db']:6.1f} under {r['under_bed_db']:5.1f}  bar {r['bar']:2} beat {r['beat']} {r['frames_from_beat']:+d}")
