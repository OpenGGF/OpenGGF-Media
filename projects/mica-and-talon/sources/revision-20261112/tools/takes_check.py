#!/usr/bin/env python3
"""Purpose: check a capture set before it is cut: every take is complete (frames, state rows and audio agree),
names the three commits, and has the events the edit's windows rely on at the expected frames (kills, boss hit,
springs, spindash release, transformation reveal, carry start). Also proves the two lockstep pairs are still in
step, column for column. A failed line means the edit's source offsets must not be trusted for that take.
Usage: takes_check.py FOLDER [--json out.json]. Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import csv, json, math, sys, wave
from pathlib import Path

T = Path(__file__).resolve().parent.parent
D = T / sys.argv[1]
# take -> [(kind, frame)]; kinds: kill, boss, spring, spindash, super (p1 reveal), sk_super, carry, rings10
EXPECT = {
    'lbz-duo': [('spring', 218)], 'carry-swoop': [('carry', 128)], 'aiz-talon-dive': [('kill', 120)], 'aiz-normal': [('kill', 55), ('kill', 163)],
    'mgz-chain': [('kill', 65), ('kill', 85), ('kill', 107)], 'ghz2-buzz': [('kill', 60), ('kill', 70), ('rings10', 264)], 'arz-whisp': [('kill', 138)],
    'cpz-spindash': [('spindash', 45)], 'ehz2-corkscrew': [('spring', 133), ('kill', 281)], 'mhz-spring': [('spring', 108)],
    'cnz-bumpers': [('kill', 196), ('kill', 211), ('kill', 261), ('kill', 276)], 'syz-talon': [('kill', 118), ('kill', 160)],
    'dez-talon': [('spring', 239)], 'arz-talon-whisp': [('kill', 191)], 'scz-chain': [('kill', 259), ('kill', 321), ('kill', 364)],
    'lbz-slope': [('spring', 143)], 'hcz-loop': [('spring', 396)], 'hcz-gilded-runin': [('super', 160)], 'arz-gilded': [('spring', 251)],
    'cpz-gilded': [('spring', 238)], 'aiz-solar-reveal': [('super', 104), ('kill', 188)], 'dez-solar': [('spring', 331)],
    'dez-hyper': [('super', 96), ('kill', 182)], 'lbz-boss': [('boss', 632)],
    'lbz-pair': [('super', 86), ('sk_super', 86), ('carry', 128)],
}
NO_HURT = {'mgz-chain': 182, 'lbz-duo': 240, 'syz-talon': 230, 'cnz-bumpers': 325, 'scz-chain': 410, 'ehz2-corkscrew': 325}   # no hurt before this frame
LOCK = [('cpz-lock-mod', 'cpz-lock-stock'), ('ehz-lock-mod', 'ehz-lock-stock')]


def num(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return 0.0


def events(r):
    ev = []
    run = 0
    for i in range(1, len(r)):
        p, q = r[i - 1], r[i]
        if q.get('mode') != 'LEVEL' or p.get('mode') != 'LEVEL':
            continue
        ds = num(q, 'score') - num(p, 'score')
        if ds >= 1000:
            ev.append(('boss', i))
        elif ds > 0:
            ev.append(('kill', i))
        if num(q, 'rings') - num(p, 'rings') == 10:
            ev.append(('rings10', i))
        if num(q, 'hurt') and not num(p, 'hurt'):
            ev.append(('hurt', i))
        dvx = num(q, 'xvel') - num(p, 'xvel')
        if not num(p, 'air') and num(q, 'air') and num(q, 'yvel') <= -0x900:
            ev.append(('spring', i))
        elif not num(p, 'air') and not num(q, 'air') and abs(dvx) >= 0x800 and not num(p, 'spindash'):
            ev.append(('spring', i))
        if num(p, 'spindash') and not num(q, 'spindash'):
            ev.append(('spindash', i))
        for k, lab in (('p1_state', 'super'), ('sk_state', 'sk_super')):
            if q.get(k) == 'SUPER' and p.get(k) != 'SUPER':
                ev.append((lab, i))
        if q.get('sk_x'):
            dx, dy = num(q, 'x') - num(q, 'sk_x'), num(q, 'y') - num(q, 'sk_y')
            run = run + 1 if abs(dx) <= 1 and 27 <= dy <= 29 else 0
            if run == 8:
                ev.append(('carry', i - 7))
    return ev


out, bad = {}, 0
for d in sorted(p for p in D.iterdir() if (p / 'provenance.json').exists()):
    name = d.name
    prov = json.load(open(d / 'provenance.json'))
    frames = len(list((d / 'frames').glob('*.png')))
    rows = list(csv.DictReader(open(d / 'state.csv'))) if (d / 'state.csv').exists() else []
    aud = None
    if (d / 'audio.wav').exists():
        with wave.open(str(d / 'audio.wav')) as w:
            aud = w.getnframes() / (w.getframerate() / 60)
    notes = []
    if not (d / 'DONE').exists():
        notes.append('NOT DONE')
    if rows and frames != len(rows):
        notes.append(f'frames {frames} != rows {len(rows)}')
    if aud is None:
        notes.append('NO AUDIO')
    elif rows and abs(aud - len(rows)) > 0.01:
        notes.append(f'audio {aud:.2f} frames != rows {len(rows)}')
    for key in ('build_commit', 'mod_commit', 'develop_commit'):
        if not prov.get(key):
            notes.append(f'no {key}')
    ev = events(rows) if rows else []
    for kind, f in EXPECT.get(name, []):
        if (kind, f) not in ev:
            near = [x for x in ev if x[0] == kind]
            notes.append(f'expected {kind}@{f}, found {near[:6]}')
    if name in NO_HURT and any(k == 'hurt' and f < NO_HURT[name] for k, f in ev):
        notes.append(f'hurt before {NO_HURT[name]}: {[f for k, f in ev if k == "hurt"]}')
    out[name] = dict(frames=frames, rows=len(rows), audio_frames=aud, events=[f'{k}@{f}' for k, f in ev if k != 'rings10'][:16], problems=notes)
    bad += bool(notes)
    print(f"{'FAIL' if notes else 'ok  '} {name:18} {frames:5} frames | " + ('; '.join(notes) if notes else ' '.join(out[name]['events'][:9])))
COLS = ['x', 'y', 'xvel', 'yvel', 'gspeed', 'air', 'rolling', 'spindash', 'cam_x', 'cam_y', 'sk_x', 'sk_y', 'rings']
for a, b in LOCK:
    if (D / a / 'state.csv').exists() and (D / b / 'state.csv').exists():
        ra, rb = list(csv.DictReader(open(D / a / 'state.csv'))), list(csv.DictReader(open(D / b / 'state.csv')))
        diff = sum(1 for i in range(min(len(ra), len(rb))) for c in COLS if ra[i][c] != rb[i][c])
        out[f'lockstep {a}'] = dict(frames=min(len(ra), len(rb)), columns=COLS, differences=diff)
        bad += bool(diff or len(ra) != len(rb))
        print(f"{'FAIL' if diff else 'ok  '} lockstep {a} vs {b}: {min(len(ra), len(rb))} frames, {len(COLS)} columns, {diff} differences")
print('takes', len(out), 'problems', bad)
if '--json' in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
