#!/usr/bin/env python3
"""Purpose: stage B probes for the pacing revision: the six re-stages, the four timing tunes and the window
searches of checkpoint 4. Each probe is a short state-only run (no PNGs, no audio) through the positioned or
powered host; `report` prints, per probe, the events the re-stage is judged on (kills, boss hit, springs,
transformation reveal, carry start, speed). Probes are written to shots-b/probes-<batch>.json and captured into
probes-b/ by tools/capture.py, one JVM at a time.
Usage: probes_b.py gen <batch> | report <prefix> [...]. Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import csv, json, math, sys
from pathlib import Path

T = Path(__file__).resolve().parent.parent
FAST = {'promo.png.every': 0}


def shot(id_, game, zone, act, x, y, script, host='positioned', **props):
    p = dict(FAST); p.update({k.replace('_', '.'): v for k, v in props.items()})
    return dict(id=id_, kind='host', host=host, mode='run', game=game, zone=zone, act=act, x=x, y=y, script=script, props=p, audio=False)


def batch1():
    S = []
    # R1 Launch Base duo from a run-up: where is the floor left of the bridge, and how long is the top-speed run?
    for x in (13700, 13900, 14100, 14300):
        S.append(shot(f'r1-lbz-{x}', 's3k', 6, 0, x, 1470, '20 -; 420 R', promo_sidekick='talon', promo_rings=30, promo_timer=9600, promo_score=283000))
    # R2 carry swoop, Angel Island 1: TALON takes off at 20 and flies right; MICA starts running d frames later and jumps at j
    for d in (0, 8, 16):
        for j in (24, 32, 40):
            pre = f'20 -; 1 - / R+A; 2 - / R; 1 - / R+A; '
            # frames 24.. : TALON flaps every 8 with R; MICA idle until 20+d, runs, jumps at 20+j
            seq = []
            for f in range(24, 20 + 240):
                p1 = ('R+A' if f == 20 + j else 'R') if f >= 20 + d else '-'
                p2 = 'R+A' if (f - 24) % 8 == 7 else 'R'
                seq.append(f'1 {p1} / {p2}')
            S.append(shot(f'r2-carry-d{d}-j{j}', 's3k', 0, 0, 6040, 1040, pre + '; '.join(seq), promo_sidekick='talon', promo_rings=34, promo_timer=5400, promo_score=3700))
    # R3 TALON divebomb on the Aquatic Ruin Whisps: n flaps before the dive
    for n in (8, 10, 12, 14):
        S.append(shot(f'r3-arz-n{n}', 's2', 2, 0, 8300, 860, f'20 -; 1 R+A; 20 R; repeat {n} {{ 1 A; 8 R }}; 18 D+R; 1 D+A; 200 R', promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300))
    # R4 Solar reveal straight into the dive kill (Angel Island Rhinobot): start x, wait after the transform press, flaps
    for x, w, fl in ((6990, 27, 5), (7060, 52, 2), (7030, 40, 4), (6990, 52, 5)):
        S.append(shot(f'r4-solar-x{x}-w{w}-f{fl}', 's3k', 0, 0, x, 900, f'30 -; 1 A; 20 -; 1 A; {w} -; 1 R+A; 20 R; repeat {fl} {{ 1 R+A; 8 R }}; 6 D+R; 1 D+A; 150 R; 40 -',
                      host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=9400))
    # R5 boss run-in: back off left nl frames from t1, stand, run right for r frames into the hop at 626
    for nl, r in ((30, 36), (40, 50), (24, 30), (0, 0)):
        if r:
            t1 = 626 - r - 24 - nl
            mid = f'{t1 - 222} -; {nl} L; 24 -; {r} R; 1 R+A; 15 R; 1 R+A; 300 -'
        else:
            mid = '404 -; 1 A; 15 -; 1 A; 300 -'
        S.append(shot(f'r5-boss-l{nl}-r{r}', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; ' + mid, host='powered',
                      promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900))
    # R6 pair: is there upper-level floor left of the starpost to transform on and fly right from?
    for x in (14900, 15100, 15300):
        S.append(shot(f'r6-map-{x}', 's3k', 6, 0, x, 440, '90 -; 90 R', host='powered', promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200))
    # T1 Marble Garden chain: second and third strike presses moved so the kills are 21 frames apart
    for b, c in ((80, 103), (84, 106), (84, 105), (83, 105), (85, 107)):
        S.append(shot(f't1-mgz-{b}-{c}', 's3k', 2, 1, 7600, 1136, f'21 -; 1 R+A; 12 R; 1 R+A; 22 R; 1 R+A; {b - 58} R; 1 R+A; {c - b - 1} R; 1 R+A; 70 R', promo_rings=36, promo_timer=8100, promo_score=87300))
    # T2 Sky Chase: the two later strikes moved 3 and 6 frames later
    def scz(presses):
        out, f = [], 0
        for p in presses:
            out.append(f'{p - f} -; 1 A'); f = p + 1
        return '; '.join(out) + '; 120 -'
    base = [236] + list(range(257, 420, 10))
    S.append(shot('t2-scz-base', 's2', 8, 0, 288, 112, scz(base), promo_rings=0, promo_timer=0))
    for k2, k3 in ((320, 363), (320, 362), (321, 364), (319, 362)):
        pr = [236, 257, 267, 277, 287, 297, 307, k2] + [k2 + 10, k2 + 20, k2 + 30] + [k3] + list(range(k3 + 10, 430, 10))
        S.append(shot(f't2-scz-{k2}-{k3}', 's2', 8, 0, 288, 112, scz(pr), promo_rings=0, promo_timer=0))
    # T3 Casino Night bumpers: the leap a few frames either side
    for j in (268, 269, 270, 271, 272, 274):
        S.append(shot(f't3-cnz-j{j}', 's2', 3, 0, 5944, 276, f'30 -; {j - 30} R; 1 R+A; {329 - j} R; 60 -', promo_sidekick='talon', promo_rings=45, promo_timer=5400, promo_score=31700))
    # T4 Hyper reveal to kill in 85 frames (Death Egg): the wait after the transform press
    for w in (50, 47, 46, 45):
        S.append(shot(f't4-dez-w{w}', 's3k', 11, 0, 5096, 1300, f'24 -; 26 R; 1 R+A; 20 R; 1 A; {w} -; repeat 10 {{ 1 R+A; 16 R }}; 160 R', host='powered',
                      promo_emeralds='3333333', promo_rings=75, promo_timer=6000, promo_score=512600))
    return S


def batch2():
    S = []
    # R2 step A: TALON's trajectory when he runs ahead, hops, starts flight low and hovers (MICA idle)
    for run, fl in ((50, 8), (70, 8), (50, 12), (70, 12)):
        S.append(shot(f'r2a-hover-run{run}-fl{fl}', 's3k', 0, 0, 6040, 1040, f'20 -; {run} - / R; 1 - / R+A; {fl} - / -; 1 - / A; 200 - / -',
                      promo_sidekick='talon', promo_rings=34, promo_timer=5400, promo_score=3700))
    # R3 TALON on the ground toward the Whisps, jump at t, dive (Down+A) dd frames later
    for t in (90, 100, 110, 120):
        for dd in (8, 14):
            S.append(shot(f'r3b-arz-t{t}-d{dd}', 's2', 2, 0, 8300, 860, f'20 -; {t - 20} R; 1 R+A; {dd - 1} R; 1 D+A; 60 R; 1 D+A; 100 R',
                          promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300))
    # R4 Solar: transform in the air at 79 (reveal 104), then F flaps before the dive; start further left
    for x in (6900, 6920, 6940):
        for fl in (8, 9):
            S.append(shot(f'r4b-solar-x{x}-f{fl}', 's3k', 0, 0, x, 900, f'30 -; 1 A; 20 -; 1 A; 27 -; 1 R+A; 20 R; repeat {fl} {{ 1 R+A; 8 R }}; 6 D+R; 1 D+A; 150 R; 40 -',
                          host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=9400))
    # R5 boss: back off left from tl for nl frames, run right from rs, hop at 626, strike at 642
    for tl, nl, rs in ((560, 30, 594), (560, 30, 598), (556, 30, 592), (566, 24, 594), (512, 40, 588), (512, 40, 594)):
        mid = f'{tl - 222} -; {nl} L; {rs - tl - nl} -; {626 - rs} R; 1 R+A; 15 R; 1 R+A; 300 -'
        S.append(shot(f'r5b-boss-t{tl}-l{nl}-r{rs}', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; ' + mid, host='powered',
                      promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900))
    # pictures: the Launch Base lower bridge run and the upper level left of the starpost (PNG every 6th frame)
    look = {'promo.png.every': 6}
    s_ = shot('r1-look-14300', 's3k', 6, 0, 14300, 1470, '20 -; 300 R', promo_sidekick='talon', promo_rings=30, promo_timer=9600, promo_score=283000); s_['props'].update(look); S.append(s_)
    for x, y in ((14900, 440), (15100, 440), (15300, 440), (15450, 440), (14640, 1480)):
        s_ = shot(f'r6-look-{x}', 's3k', 6, 0, x, y, '60 -; 120 R', host='powered', promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200)
        s_['props'].update(look); S.append(s_)
    # T4 one more wait value
    for w in (48, 49):
        S.append(shot(f't4-dez-w{w}', 's3k', 11, 0, 5096, 1300, f'24 -; 26 R; 1 R+A; 20 R; 1 A; {w} -; repeat 10 {{ 1 R+A; 16 R }}; 160 R', host='powered',
                      promo_emeralds='3333333', promo_rings=75, promo_timer=6000, promo_score=512600))
    return S


def batch3():
    S = []
    # R2 grid B: TALON runs ahead, hops at 70, starts flight at 78 and hovers; MICA starts running at s and jumps at s + j (0 = no jump)
    for st in (60, 75, 90, 105):
        for j in (0, 25, 40):
            seq = []
            for f in range(20, 330):
                p2 = 'R' if f < 70 else 'R+A' if f == 70 else 'A' if f == 78 else ('R+A' if f >= 150 and (f - 150) % 8 == 0 else 'R' if f >= 150 else '-')
                p1 = '-' if f < st else ('R+A' if j and st + j <= f < st + j + 12 else 'R')
                seq.append(f'1 {p1} / {p2}')
            S.append(shot(f'r2b-carry-s{st}-j{j}', 's3k', 0, 0, 6040, 1040, '20 -; ' + '; '.join(seq), promo_sidekick='talon', promo_rings=34, promo_timer=5400, promo_score=3700))
    # R3: TALON runs, jumps at t and divebombs dd frames later (one press, or three presses for a chain)
    for t in (140, 146, 150):
        for dd in (6, 10, 14):
            S.append(shot(f'r3c-arz-t{t}-d{dd}', 's2', 2, 0, 8300, 860, f'20 -; {t - 20} R; 1 R+A; {dd - 1} R; 1 D+A; 120 R',
                          promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300))
            S.append(shot(f'r3c-arz-t{t}-d{dd}-x3', 's2', 2, 0, 8300, 860, f'20 -; {t - 20} R; 1 R+A; {dd - 1} R; 1 D+A; 11 R; 1 D+A; 9 R; 1 D+A; 100 R',
                          promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300))
    # R4: Solar, 8 flaps, the Down hold before the dive stretched so the kill lands 84-85 frames after the reveal
    for x in (6900, 6920):
        for dh in (10, 11, 12):
            S.append(shot(f'r4c-solar-x{x}-dh{dh}', 's3k', 0, 0, x, 900, f'30 -; 1 A; 20 -; 1 A; 27 -; 1 R+A; 20 R; repeat 8 {{ 1 R+A; 8 R }}; {dh} D+R; 1 D+A; 150 R; 40 -',
                          host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=9400))
    # R5 picture of the run-in that hits
    s_ = shot('r5-look-t512-l40-r588', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; 290 -; 40 L; 36 -; 38 R; 1 R+A; 15 R; 1 R+A; 120 -', host='powered',
               promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900)
    s_['props']['promo.png.every'] = 3; S.append(s_)
    # R6 pair on the lower bridge: both jump at 40, transform at 61; TALON starts flight sd frames after the reveal and holds R
    for sd in (0, 12, 24, 34, 40):
        seq = []
        for f in range(62, 520):
            p2 = '-'
            if f >= 86 + sd:
                k = f - (86 + sd)
                p2 = 'R+A' if k == 0 or k == 4 or (k > 40 and k % 9 == 0) else 'R'
            seq.append(f'1 - / {p2}')
        S.append(shot(f'r6b-pair-sd{sd}', 's3k', 6, 0, 14350, 1470, '40 - / -; 1 A / A; 20 - / -; 1 A / A; ' + '; '.join(seq), host='powered',
                      promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200))
    return S


def batch4():
    S = []
    look = {'promo.png.every': 3}
    def carry(st, j, id_):
        seq = []
        for f in range(20, 330):
            p2 = 'R' if f < 70 else 'R+A' if f == 70 else 'A' if f == 78 else ('R+A' if f >= 150 and (f - 150) % 8 == 0 else 'R' if f >= 150 else '-')
            p1 = '-' if f < st else ('R+A' if j and st + j <= f < st + j + 12 else 'R')
            seq.append(f'1 {p1} / {p2}')
        s_ = shot(id_, 's3k', 0, 0, 6040, 1040, '20 -; ' + '; '.join(seq), promo_sidekick='talon', promo_rings=34, promo_timer=5400, promo_score=3700)
        s_['props'].update(look); return s_
    S.append(carry(75, 40, 'r2-look-s75-j40')); S.append(carry(90, 40, 'r2-look-s90-j40'))
    def pair(sd, id_, pat=9, png=True):
        seq = []
        for f in range(62, 560):
            p2 = '-'
            if f >= 86 + sd:
                k = f - (86 + sd)
                p2 = 'R+A' if k == 0 or k == 4 or (k > 40 and k % pat == 0) else 'R'
            seq.append(f'1 - / {p2}')
        s_ = shot(id_, 's3k', 6, 0, 14350, 1470, '40 - / -; 1 A / A; 20 - / -; 1 A / A; ' + '; '.join(seq), host='powered',
                  promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200)
        if png: s_['props'].update(look)
        return s_
    S.append(pair(27, 'r6-look-sd27')); S.append(pair(48, 'r6-look-sd48'))
    for sd in (26, 28, 47, 49):
        S.append(pair(sd, f'r6c-pair-sd{sd}', png=False))
    s_ = shot('r4-look-x6900-dh12', 's3k', 0, 0, 6900, 900, '30 -; 1 A; 20 -; 1 A; 27 -; 1 R+A; 20 R; repeat 8 { 1 R+A; 8 R }; 12 D+R; 1 D+A; 150 R; 40 -',
               host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=9400)
    s_['props'].update(look); S.append(s_)
    s_ = shot('r3-look-t150-d14-x3', 's2', 2, 0, 8300, 860, '20 -; 130 R; 1 R+A; 13 R; 1 D+A; 11 R; 1 D+A; 9 R; 1 D+A; 100 R', promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300)
    s_['props'].update(look); S.append(s_)
    for k in (4, 8, 12, 16, 22):          # a fourth dive press after the kill at 191
        S.append(shot(f'r3d-arz-k{k}', 's2', 2, 0, 8300, 860, f'20 -; 130 R; 1 R+A; 13 R; 1 D+A; 11 R; 1 D+A; 9 R; 1 D+A; {5 + k - 1} R; 1 D+A; 100 R',
                      promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300))
    s_ = shot('r1-final-look', 's3k', 6, 0, 14300, 1470, '20 -; 250 R', promo_sidekick='talon', promo_rings=30, promo_timer=9600, promo_score=283000)
    s_['props'].update(look); S.append(s_)
    return S


def batch5():
    S = []
    # R5: keep the camera at the arena lock: back off on screen, run in, hop at h, strike st frames later
    for tl, nl, rs in ((512, 40, 576), (560, 30, 590), (540, 30, 584)):
        for h in (618, 622, 626):
            for st in (8, 12, 16):
                mid = f'{tl - 222} -; {nl} L; {rs - tl - nl} -; {h - rs} R; 1 R+A; {st - 1} R; 1 R+A; 300 -'
                S.append(shot(f'r5c-boss-t{tl}-r{rs}-h{h}-s{st}', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; ' + mid, host='powered',
                              promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900))
    # R6: the carry holds Right for n frames after the catch, then only flaps, so it stops short of the wall
    for n in (70, 100, 130):
        seq = []
        for f in range(62, 800):
            p2 = '-'
            if f >= 113:
                k = f - 113
                d = 'R' if f < 128 + n else ''
                flap = k == 0 or k == 4 or (k > 40 and k % 9 == 0)
                p2 = (d + '+A' if d and flap else 'A' if flap else d or '-')
            seq.append(f'1 - / {p2}')
        S.append(shot(f'r6d-pair-n{n}', 's3k', 6, 0, 14350, 1470, '40 - / -; 1 A / A; 20 - / -; 1 A / A; ' + '; '.join(seq), host='powered',
                      promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200))
    return S


def pair_script(n, flap=9, total=800):
    """Lower-bridge pair: jump 40, transform 61 (reveal 86), TALON hops at 113 and catches at 128, holds Right n frames."""
    seq = []
    for f in range(62, total):
        p2 = '-'
        if f >= 113:
            k = f - 113
            d = 'R' if f < 128 + n else ''
            fl = k == 0 or k == 4 or (k > 40 and k % flap == 0)
            p2 = (d + '+A' if d and fl else 'A' if fl else d or '-')
        seq.append(f'1 - / {p2}')
    return '40 - / -; 1 A / A; 20 - / -; 1 A / A; ' + '; '.join(seq)


def batch6():
    S = []
    look = {'promo.png.every': 3}
    s_ = shot('r5-look2-t560-r590-h618-s8', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; 338 -; 30 L; 28 R; 1 R+A; 7 R; 1 R+A; 200 -', host='powered',
               promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900)
    s_['props'].update(look); S.append(s_)
    for n in (20, 30, 40, 50):
        S.append(shot(f'r6e-pair-n{n}', 's3k', 6, 0, 14350, 1470, pair_script(n), host='powered',
                      promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200))
    for n, fl in ((30, 12), (40, 12)):
        S.append(shot(f'r6e-pair-n{n}-fl{fl}', 's3k', 6, 0, 14350, 1470, pair_script(n, fl), host='powered',
                      promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200))
    return S


def rows(d):
    return list(csv.DictReader(open(d / 'state.csv')))


def num(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return 0.0


def report(d):
    r = rows(d)
    ev = []
    carry = None; run = 0
    for i in range(1, len(r)):
        p, q = r[i - 1], r[i]
        ds = num(q, 'score') - num(p, 'score')
        if ds > 0:
            ev.append(f"{'BOSS' if ds >= 1000 else 'kill'}+{int(ds)}@{i}")
        if num(q, 'hurt') and not num(p, 'hurt'):
            ev.append(f'HURT@{i}')
        if not num(p, 'air') and num(q, 'air') and num(q, 'yvel') <= -0x900:
            ev.append(f'spring@{i}')
        for k, lab in (('p1_state', 'p1'), ('sk_state', 'sk')):
            if k in q and q[k] != p.get(k):
                ev.append(f'{lab}:{q[k]}@{i}')
        if q.get('sk_x'):
            dx, dy = num(q, 'x') - num(q, 'sk_x'), num(q, 'y') - num(q, 'sk_y')
            run = run + 1 if abs(dx) <= 1 and 27 <= dy <= 29 else 0
            if run == 8 and carry is None:
                carry = i - 7
    sp = [math.hypot(num(x, 'xvel'), num(x, 'yvel')) / 256 for x in r]
    g = [abs(num(x, 'gspeed')) for x in r]
    top = [i for i, v in enumerate(g) if v >= 1500 and not num(r[i], 'air')]
    last = r[-1]
    print(f"{d.name:26} n{len(r):4} end x{last['x']:>6} y{last['y']:>5} rings {last['rings']:>3} | " + ' '.join(ev[:14])
          + (f' | carry@{carry}' if carry else '') + (f' | top speed frames {top[0]}-{top[-1]} ({len(top)})' if top else ''))


if __name__ == '__main__':
    if sys.argv[1] == 'gen':
        S = globals()['batch' + sys.argv[2]]()
        (T / 'shots-b').mkdir(exist_ok=True)
        (T / f'shots-b/probes-{sys.argv[2]}.json').write_text(json.dumps(S, indent=1))
        print(len(S), 'probes')
    else:
        for pre in sys.argv[2:]:
            for d in sorted((T / 'probes-b').glob(pre + '*')):
                if (d / 'state.csv').exists():
                    report(d)
                else:
                    print(d.name, 'NO STATE', (d / 'capture.log').read_text()[-300:] if (d / 'capture.log').exists() else '')
