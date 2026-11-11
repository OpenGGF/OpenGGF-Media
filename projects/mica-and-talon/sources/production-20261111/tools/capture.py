#!/usr/bin/env python3
"""Purpose: repeatable captures for the MICA & TALON production promo (2026-11-11).
Inputs: --checkout (built engine + example jar), verified ROM symlinks in the checkout root.
Origin: reuses the 2026-11-10 promo recipes (shots.json / hosts) against the final art build.
Every gameplay shot is silent, 60 Hz, every=1, surfaceless EGL, no trace input.
Declared setup (position, rings, timer, emeralds) is recorded per shot in provenance.json.
Usage: capture.py --checkout DIR [--only id ...] [--list]
"""
import argparse, csv, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

T = Path(__file__).resolve().parent.parent
OLD = Path.home() / 'scratch/agent-tmp/mt-promo-20261110/final/captures/final'
TITLE_FRAMES = 1300

# kind: tool = GameplayCaptureTool, host = hosts/<host>/PromoCapture, title = title-first production path
SHOTS = [
    # Chapter 1: homing chains deep in acts
    dict(id='hero-mgz2', kind='host', host='original', mode='hero', game='s3k', zone=2, act=1, x=7600, y=1136,
         input_from=OLD / 'hero-mgz2/input.txt', note='solo MICA; MGZ2 airborne three-Mantis chain'),
    # Chapter 2: TALON
    dict(id='carry', kind='tool', game='s3k', zone='aiz', x=6040, y=1040, rings=34, timer=5400, sidekick='talon',
         script='30 -; 22 - / R; 1 - / A; 2 -; 1 - / A; repeat 15 { 8 -; 1 - / A }; 120 -'),
    dict(id='talon-s3k', kind='tool', game='s3k', zone='aiz', x=7100, y=900, rings=38, timer=6300, main='talon',
         script='30 -; 1 A; 20 -; repeat 5 { 1 A; 8 - }; 18 D; 1 D+A; 120 R; 60 -'),
    dict(id='talon-s2', kind='tool', game='s2', zone='ehz', x=1800, y=540, rings=32, timer=3900, main='talon',
         script='30 -; 1 R+A; 20 R; repeat 5 { 1 A; 8 R }; 18 D; 1 D+A; 120 R; 60 -'),
    dict(id='team', kind='tool', game='s3k', zone='aiz', x=6040, y=1040, rings=34, timer=5400, sidekick='talon',
         script='30 -; 210 R; 1 R+A; 59 R; 60 -'),
    # Chapter 3: same moment, three games
    dict(id='ehz-clear', kind='tool', game='s2', zone='ehz', x=9900, y=400, rings=48, timer=8700,
         script='30 -; 240 R; 660 -'),
    dict(id='ghz-clear', kind='tool', game='s1', zone='ghz', x=9100, y=940, rings=48, timer=8700,
         script='30 -; 240 R; 660 -'),
    dict(id='blue-play', kind='tool', game='s3k', zone='cnz', x=11616, y=1612, rings=42, timer=9600,
         script='90 -; 90 R; 540 -'),
    dict(id='halfpipe', kind='host', host='starpost', mode='halfpipe', game='s2', zone=0, act=0, x=3568, y=150,
         input_from=OLD / 'halfpipe-cleared-post/input.txt',
         note='debug positioned ROM-starpost component entry; ring collision admits SPECIAL_STAGE'),
    dict(id='continue', kind='host', host='original', mode='continue', game='s2', zone=0, act=0,
         note='debug presentation component entry'),
    dict(id='ending', kind='host', host='original', mode='ending', game='s2', zone=10, act=0,
         note='debug credits entry from DEZ; stock photos excluded in edit'),
    dict(id='data-select', kind='title', game='s3k', zone='aiz', script='360 -; 1 S; 360 -', slots=True),
    # Chapter 4: powered up, 50+ rings deep in an act
    dict(id='gilded', kind='tool', game='s3k', zone='aiz', x=7100, y=900, rings=70, timer=7200, emeralds='1111111',
         script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 8 { 1 R+A; 16 R }; 120 R'),
    dict(id='solar', kind='tool', game='s3k', zone='aiz', x=7100, y=900, rings=70, timer=7200, emeralds='1111111',
         main='talon', script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 5 { 1 A; 8 - }; 18 D; 1 D+A; 180 R'),
    dict(id='gilded-clear', kind='tool', game='s2', zone='ehz', x=9000, y=780, rings=70, timer=8100,
         emeralds='1111111', sidekick='talon',
         script='30 -; 1 A; 20 -; 1 A; 40 -; repeat 16 { 1 R+A; 18 R }; 360 R; 660 -'),
    # Titles (S2 last: TALON gaze redraw b088fae95b)
    dict(id='title-s3k', kind='title', game='s3k', zone='aiz', frames=TITLE_FRAMES),
    dict(id='title-s1', kind='title', game='s1', zone='ghz', frames=TITLE_FRAMES),
    dict(id='title-s2', kind='title', game='s2', zone='ehz', frames=TITLE_FRAMES),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--checkout', type=Path, required=True)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--extra', type=Path, help='JSON file with extra shot dicts')
    a = ap.parse_args()
    R = a.checkout.resolve()
    jar = R / 'target/mica-and-talon/mica-and-talon.jar'
    cp = str(R / 'target/classes') + os.pathsep + (R / 'target/mica-classpath.txt').read_text().strip()
    env = os.environ.copy()
    for k in ('DISPLAY', 'WAYLAND_DISPLAY'):
        env.pop(k, None)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
    jar_sha = hashlib.sha256(jar.read_bytes()).hexdigest()
    shots = SHOTS + (json.loads(a.extra.read_text()) if a.extra else [])
    jvm = ['java', '-Xmx1g', '--enable-native-access=ALL-UNNAMED', '-Dmse=off',
           '-Dopenggf.headless.gl=surfaceless-egl']
    roms = {g: R / f'{g}.gen' for g in ('s1', 's2', 's3k')}
    for s in shots:
        if a.only and s['id'] not in a.only:
            continue
        d = T / 'captures' / s['id']
        if d.exists():
            shutil.rmtree(d)
        (d / 'frames').mkdir(parents=True)
        saves = d / 'saves'
        saves.mkdir()
        inp = None
        if s.get('script'):
            (d / 'input.script').write_text(s['script'] + '\n')
            inp = d / 'input.txt'
            subprocess.run(jvm + ['-cp', cp, 'com.openggf.tools.InputLogAuthorTool', '--script', str(d / 'input.script'),
                                  '--out', str(inp)], cwd=R, env=env, check=True, capture_output=True)
        elif s.get('input_from'):
            inp = d / 'input.txt'
            shutil.copy2(s['input_from'], inp)
        if s['kind'] == 'host':
            host = T / 'hosts' / s['host']
            args = [s['mode'], str(d), str(jar), str(roms[s['game']]), str(s['zone']), str(s['act'])]
            if 'x' in s:
                args += [str(s['x']), str(s['y'])]
            if inp:
                args += [str(inp)]
            cmd = jvm + [f'-D{k}={v}' for k, v in s.get('props', {}).items()] + [f'-Dopenggf.saveRoot={saves}', '-cp', str(host) + os.pathsep + cp, 'PromoCapture'] + args
        else:
            args = ['--game', s['game'], '--zone', str(s['zone']), '--act', str(s.get('act', 1)),
                    '--main', 'mica-and-talon:' + s.get('main', 'mica'), '--mod', str(jar),
                    '--out-dir', str(d), '--width', str(s.get('width', 320)), '--scale', '1', '--no-video']
            if s['kind'] == 'title':
                args += ['--title-screen', '--interactive-pacing', '--sidekick', 'mica-and-talon:talon']
                if s.get('frames'):
                    args += ['--frames', str(s['frames'])]
                if s.get('slots'):
                    slots = d / 'slots.json'
                    slots.write_text(json.dumps({str(i): dict(act=0, zone=0, lives=3, mainCharacter='mica-and-talon:mica',
                                                              sidekicks=['mica-and-talon:talon'], chaosEmeralds=[], clear=False,
                                                              progressCode=1, clearState=0) for i in range(1, 4)}))
                    args += ['--save-slots', str(slots)]
            else:
                for k in ('x', 'y', 'rings', 'timer'):
                    if k in s:
                        args += ['--' + k, str(s[k])]
                if 'emeralds' in s:
                    args += ['--emeralds', s['emeralds']]
                if 'sidekick' in s:
                    args += ['--sidekick', 'mica-and-talon:' + s['sidekick']]
                for flag in s.get('flags', []):
                    args += [flag]
            if inp:
                args += ['--input', str(inp)]
            cmd = jvm + [f'-Dopenggf.saveRoot={saves}', '-cp', cp, 'com.openggf.tools.GameplayCaptureTool'] + args
        prov = dict({k: (str(v) if isinstance(v, Path) else v) for k, v in s.items()}, commit=commit, jar_sha256=jar_sha,
                    checkout=str(R), command=cmd[cmd.index('-cp') + 2:] if s['kind'] != 'host' else cmd[cmd.index('-cp') + 2:],
                    source_kind={'tool': 'positioned native gameplay', 'host': 'debug/positioned presentation host',
                                 'title': 'title-first production presentation'}[s['kind']],
                    fps=60, every=1, audio=False)
        if s['kind'] == 'host':
            prov['capture_host_sha256'] = hashlib.sha256((T / 'hosts' / s['host'] / 'PromoCapture.java').read_bytes()).hexdigest()
        (d / 'provenance.json').write_text(json.dumps(prov, indent=2))
        print('CAPTURE', s['id'], flush=True)
        with (d / 'capture.log').open('w') as log:
            r = subprocess.run(cmd, cwd=R, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=900)
        if r.returncode:
            print('FAILED', s['id'], r.returncode, flush=True)
            continue
        if (d / 'state.csv').exists():
            rows = list(csv.DictReader(open(d / 'state.csv')))
            if rows:
                summ = dict(frames=len(rows), first=rows[0], last=rows[-1],
                            hurt=sum(r.get('hurt') == '1' for r in rows), dead=sum(r.get('dead') == '1' for r in rows))
                (d / 'observations.json').write_text(json.dumps(summ, indent=2))
        print('DONE', s['id'], len(list((d / 'frames').glob('*.png'))), 'frames', flush=True)


if __name__ == '__main__':
    main()
