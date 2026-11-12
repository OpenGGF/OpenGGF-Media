#!/usr/bin/env python3
"""Purpose: the final capture list for the pacing revision (stage B): every take the film uses, with the windows
approved at checkpoints 4-6, plus the clips the owner's 1.0 release promo reuses under their 2026-11-11 ids.
Writes shots-b/final.json (film) and shots-b/promo10.json (1.0 clips). Every take records the SFX-only stem.
Scripts for the re-stages and tunes are the ones probed at checkpoint 5 (tools/probes_b.py, checkpoint5/probes.json).
Takes that were shot without a declared score now go through the positioned host with a plausible one; takes at
an act's own start keep the true score.
Usage: final_shots.py. Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import glob, json
from pathlib import Path

T = Path(__file__).resolve().parent.parent
OLD = {}
for f in sorted(glob.glob(str(T / 'shots/*.json')), key=lambda p: int(''.join(c for c in Path(p).stem if c.isdigit()) or 0)):
    for s in json.load(open(f)):
        OLD[s['id']] = s


def pos(id_, game, zone, act, x, y, script, host='positioned', note='', **props):
    return dict(id=id_, kind='host', host=host, mode='run', game=game, zone=zone, act=act, x=x, y=y, script=script,
                props={k.replace('_', '.'): v for k, v in props.items()}, note=note)


def old(new_id, old_id, **over):
    s = dict(OLD[old_id], id=new_id)
    s.update(over)
    return s


def carry_script(st=75, j=40):
    seq = []
    for f in range(20, 330):
        p2 = 'R' if f < 70 else 'R+A' if f == 70 else 'A' if f == 78 else ('R+A' if f >= 150 and (f - 150) % 8 == 0 else 'R' if f >= 150 else '-')
        p1 = '-' if f < st else ('R+A' if j and st + j <= f < st + j + 12 else 'R')
        seq.append(f'1 {p1} / {p2}')
    return '20 -; ' + '; '.join(seq)


def pair_script(total=660):
    seq = []
    for f in range(62, total):
        p2 = '-'
        if f >= 113:
            k = f - 113
            d = 'R' if (f < 148 or f % 10 == 0) else ''
            fl = k == 0 or k == 4 or (k > 40 and k % 9 == 0)
            p2 = (d + '+A' if d and fl else 'A' if fl else d or '-')
        seq.append(f'1 - / {p2}')
    return '40 - / -; 1 A / A; 20 - / -; 1 A / A; ' + '; '.join(seq)


def scz_script(k2=320, k3=363):
    pr = [236, 257, 267, 277, 287, 297, 307, k2, k2 + 10, k2 + 20, k2 + 30, k3] + list(range(k3 + 10, 430, 10))
    out, f = [], 0
    for p in pr:
        out.append(f'{p - f} -; 1 A'); f = p + 1
    return '; '.join(out) + '; 120 -'


FILM = [
    # ---- screens
    old('title-s3k', 'title-s3k'), old('title-s2', 'title-s2'), old('title-s1', 'title-s1'), old('data-select', 'data-select'),
    old('continue', 'continue'), old('ending', 'ending'), old('halfpipe-run', 'halfpipe-run'),
    old('ghz-ss', 'f-ghz-ss'), old('blue-sphere', 'q-blue-c'),
    # ---- cold open
    pos('lbz-duo', 's3k', 6, 0, 14300, 1470, '20 -; 250 R', promo_sidekick='talon', promo_rings=30, promo_timer=9600, promo_score=283000,
        note='R1. Launch Base 1 lower bridge from a run-up: top speed #139, spring #218.'),
    pos('carry-swoop', 's3k', 0, 0, 6040, 1040, carry_script(), promo_sidekick='talon', promo_rings=34, promo_timer=5400, promo_score=3700,
        note='R2. TALON (pad 2) runs ahead, hops (#70), hovers; MICA runs (#75), jumps (#115) and is caught in the air (#128).'),
    old('aiz-talon-dive', 'd-aiz-talon-dive'), old('aiz-normal', 'd-aiz-normal'),
    pos('mhz-hyper', 's3k', 7, 0, 10176, 1428, OLD['p-mhz1-hyper']['script'], host='powered', promo_emeralds='3333333', promo_rings=77, promo_timer=8100, promo_score=61800,
        note='Hyper MICA through the Mushroom Hill 1 loops (was p-mhz1-hyper, shot 400 wide without a score).'),
    # ---- MICA
    pos('mgz-chain', 's3k', 2, 1, 7600, 1136, '21 -; 1 R+A; 12 R; 1 R+A; 22 R; 1 R+A; 26 R; 1 R+A; 20 R; 1 R+A; 78 R', promo_rings=36, promo_timer=8100, promo_score=87300,
        note='T1. Marble Garden 2 chain, strike presses tuned so the kills (#65, #85, #107) are 20 and 22 frames apart. Its lead-in cannot be lengthened: the Mantises are on a timer, and 40 more idle frames change which ones are struck.'),
    old('ghz2-buzz', 'd-ghz2-buzz'), old('arz-whisp', 'd-arz1-whisp'),
    pos('aiz-hero', 's3k', 0, 0, 7100, 900, OLD['aiz-hero']['script'], promo_rings=38, promo_timer=6300, promo_score=4800),
    pos('hcz-loop', 's3k', 1, 0, 6848, 856, OLD['h-hcz1']['script'], promo_rings=35, promo_timer=6000, promo_score=38200),
    old('cpz-spindash', 'd-cpz1-run'),
    pos('ehz2-corkscrew', 's2', 0, 1, 8960, 560, OLD['ehz2-chain-b']['script'], promo_rings=44, promo_timer=8400, promo_score=27400),
    pos('mhz-spring', 's3k', 7, 0, 7520, 404, OLD['f-mhz1-team']['script'], promo_sidekick='talon', promo_rings=29, promo_timer=6300, promo_score=52300),
    old('cnz-bumpers', 'd-cnz2-team'),
    # ---- TALON
    old('syz-talon', 'd-syz1-talon'),
    pos('htz-talon-dive', 's2', 4, 0, 4160, 184, OLD['f-htz1-talon']['script'], promo_main='talon', promo_rings=25, promo_timer=4800, promo_score=35600),
    pos('dez-talon', 's3k', 11, 0, 5096, 1300, OLD['g-dez1-talon-a']['script'], promo_main='talon', promo_rings=33, promo_timer=6000, promo_score=498700),
    pos('arz-talon-whisp', 's2', 2, 0, 8300, 860, '20 -; 130 R; 1 R+A; 13 R; 1 D+A; 11 R; 1 D+A; 9 R; 1 D+A; 112 R', promo_main='talon', promo_rings=31, promo_timer=7200, promo_score=46300,
        note='R3. TALON solo divebombs a Whisp in Aquatic Ruin 1 (#191).'),
    old('cpz-talon', 'd-cpz-talon'),
    # ---- every screen
    old('cpz-lock-mod', 'f-cpz-medley'), old('cpz-lock-stock', 'f-stock-cpz-medley'),
    pos('ehz-lock-mod', 's2', 0, 0, 1884, 560, '20 -; 345 R', promo_sidekick='talon', promo_rings=28, promo_timer=2700, promo_score=3100),
    pos('ehz-lock-stock', 's2', 0, 0, 1884, 560, '20 -; 345 R', promo_stock='true', promo_main='sonic', promo_sidekick='tails', promo_rings=28, promo_timer=2700, promo_score=3100),
    old('ghz-clear', 'd-ghz-clear'), old('ehz-clear', 'd-ehz-clear'),
    pos('scz-chain', 's2', 8, 0, 288, 112, scz_script(), promo_rings=0, promo_timer=0,
        note='T2. Sky Chase from the act start; strike presses tuned (kills #259, #321, #364). The game puts TALON in the cockpit.'),
    # ---- build
    pos('mtz-run', 's2', 7, 0, 6330, 330, OLD['h-mtz1-asteron']['script'], promo_rings=34, promo_timer=6000, promo_score=187300),
    pos('lbz-slope', 's3k', 6, 0, 7296, 788, OLD['h-lbz1']['script'], promo_rings=31, promo_timer=5700, promo_score=244100),
    # ---- powered up
    old('hcz-gilded-runin', 'd-hcz1-gilded-runin'),
    pos('aiz-gilded', 's3k', 0, 0, 7100, 900, OLD['gilded-aiz']['script'], host='powered', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=6100),
    pos('slz-gilded', 's1', 4, 0, 3000, 400, OLD['f-slz1-gilded']['script'], host='powered', promo_emeralds='111111', promo_rings=70, promo_timer=4800, promo_score=143200),
    pos('arz-gilded', 's2', 2, 0, 5200, 700, OLD['s2-gilded-arz']['script'], host='powered', promo_emeralds='1111111', promo_rings=70, promo_timer=4800, promo_score=51200),
    pos('cpz-gilded', 's2', 1, 0, 7936, 724, OLD['f-cpz1-gilded']['script'], host='powered', promo_emeralds='1111111', promo_rings=72, promo_timer=6900, promo_score=24800),
    pos('aiz-solar-reveal', 's3k', 0, 0, 6900, 900, '30 -; 1 A; 20 -; 1 A; 27 -; 1 R+A; 20 R; repeat 8 { 1 R+A; 8 R }; 12 D+R; 1 D+A; 150 R; 40 -', host='powered',
        promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=7200, promo_score=9400,
        note='R4. Solar TALON: transform in the air (#79), reveal #104, eight flaps, dive, Rhinobot killed #188.'),
    pos('dez-solar', 's3k', 11, 0, 5096, 1300, OLD['g-dez1-solar']['script'], host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=70, promo_timer=6000, promo_score=503900),
    pos('syz-solar', 's1', 2, 0, 5112, 425, OLD['g-syz1-solar']['script'], host='powered', promo_main='talon', promo_emeralds='111111', promo_rings=70, promo_timer=6300, promo_score=61400),
    pos('htz-solar', 's2', 4, 0, 4160, 184, OLD['f-htz1-solar']['script'], host='powered', promo_main='talon', promo_emeralds='1111111', promo_rings=66, promo_timer=4800, promo_score=36900),
    pos('fbz-solar', 's3k', 4, 0, OLD['f-fbz1-solar']['x'], OLD['f-fbz1-solar']['y'], OLD['f-fbz1-solar']['script'], host='powered', promo_main='talon',
        promo_emeralds='1111111', promo_rings=OLD['f-fbz1-solar']['rings'], promo_timer=OLD['f-fbz1-solar']['timer'], promo_score=176300,
        note='Solar TALON in Flying Battery 1 (replaces the second Angel Island Rhinobot dive, whose last 0.7 s is TALON against a wall).'),
    # ---- hero
    pos('dez-hyper', 's3k', 11, 0, 5096, 1300, '24 -; 26 R; 1 R+A; 20 R; 1 A; 47 -; repeat 10 { 1 R+A; 16 R }; 160 R', host='powered',
        promo_emeralds='3333333', promo_rings=75, promo_timer=6000, promo_score=512600, note='T4. Hyper reveal #96, kill #182.'),
    pos('lbz-boss', 's3k', 6, 0, 15552, 468, '30 -; 1 A; 20 -; 1 A; 60 -; 94 R; 14 L; 1 R; 338 -; 30 L; 28 R; 1 R+A; 7 R; 1 R+A; 200 -', host='powered',
        promo_emeralds='3333333', promo_rings=92, promo_timer=10800, promo_score=283900,
        note='R5. Hyper MICA at the Launch Base 1 mini-boss: backs off (#560), runs in (#590), hops (#618), strikes once (#626), boss hit #632.'),
    pos('lbz-pair', 's3k', 6, 0, 14350, 1470, pair_script(), host='powered', promo_sidekick='talon', promo_emeralds='3333333', promo_rings=97, promo_timer=11520, promo_score=283200,
        note='R6. Lower bridge, MICA on pad 1 and TALON on pad 2: both jump (#40) and transform (#61, reveal #86); TALON hops (#113), catches her (#128) and carries her up and right.'),
]

# The clips the 1.0 release promo reuses, under their 2026-11-11 ids and recipes (title-s2 and halfpipe-run are in FILM).
P10 = ['s1-ghz2-buzz', 'mgz2-chain', 'carry-fly', 'gilded-clear', 'solar-fly',
       'w-title-s2', 'w-s1-ghz2-buzz', 'w-mgz2-chain', 'w-carry-fly', 'w-gilded-clear', 'w-solar-fly']
PROMO10 = [dict(OLD[i], note=(OLD[i].get('note') or '') + ' [1.0 release-promo clip, 2026-11-11 recipe]') for i in P10]

if __name__ == '__main__':
    ids = [s['id'] for s in FILM + PROMO10]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    (T / 'shots-b').mkdir(exist_ok=True)
    (T / 'shots-b/final.json').write_text(json.dumps(FILM, indent=1))
    (T / 'shots-b/promo10.json').write_text(json.dumps(PROMO10, indent=1))
    print(len(FILM), 'film takes;', len(PROMO10), '1.0 clips (plus title-s2 and halfpipe-run from the film list)')
