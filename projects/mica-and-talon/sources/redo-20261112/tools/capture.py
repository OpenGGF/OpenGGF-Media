#!/usr/bin/env python3
"""Purpose: repeatable, sequential captures for the MICA & TALON promo redo (2026-11-11).
Inputs: --checkout (built engine + example jar, verified ROM links in its root), --shots JSON list(s).
Origin: mt-promo-final-20261111/tools/capture.py, generalised: shots come only from JSON batches, stock
(no-mod) controls are supported for lockstep comparisons, finished captures are skipped unless --force.
Every shot is silent, 60 Hz, every=1, surfaceless EGL, no trace input. One JVM at a time.
Shot keys: id, kind (tool|host|title), game, zone, act, x, y, rings, timer, emeralds, main, sidekick,
  stock (true = no mod, stock characters), script | input_from, frames, width, flags, props, host, mode, slots.
Usage: capture.py --checkout DIR --shots a.json [b.json ...] [--only id ...] [--force]
"""
import argparse, csv, hashlib, json, os, shutil, subprocess
from pathlib import Path

T = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--checkout', type=Path, required=True)
    ap.add_argument('--shots', type=Path, nargs='+', required=True)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    R = a.checkout.resolve()
    jar = R / 'target/mica-and-talon/mica-and-talon.jar'
    cp = str(R / 'target/classes') + os.pathsep + (R / 'target/mica-classpath.txt').read_text().strip()
    env = os.environ.copy()
    for k in ('DISPLAY', 'WAYLAND_DISPLAY', 'JAVA_TOOL_OPTIONS'):
        env.pop(k, None)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--', 'src', 'examples'], cwd=R, text=True).strip() != ''
    jar_sha = hashlib.sha256(jar.read_bytes()).hexdigest()
    shots = [s for f in a.shots for s in json.loads(f.read_text())]
    jvm = ['java', '-Xmx1g', '--enable-native-access=ALL-UNNAMED', '-Dmse=off', '-Dopenggf.headless.gl=surfaceless-egl']
    roms = {g: R / f'{g}.gen' for g in ('s1', 's2', 's3k')}
    for s in shots:
        if a.only and s['id'] not in a.only:
            continue
        d = T / 'captures' / s['id']
        if d.exists() and (d / 'DONE').exists() and not a.force:
            print('SKIP', s['id'], flush=True)
            continue
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
        stock = bool(s.get('stock'))
        kind = s.get('kind', 'tool')
        if kind == 'host':
            host = T / 'hosts' / s['host']
            args = [s['mode'], str(d), str(jar), str(roms[s['game']]), str(s['zone']), str(s['act'])]
            if 'x' in s:
                args += [str(s['x']), str(s['y'])]
            if inp:
                args += [str(inp)]
            cmd = jvm + [f'-D{k}={v}' for k, v in s.get('props', {}).items()] + [
                f'-Dopenggf.saveRoot={saves}', '-cp', str(host) + os.pathsep + cp, 'PromoCapture'] + args
        else:
            main_key = s.get('main', 'sonic') if stock else 'mica-and-talon:' + s.get('main', 'mica')
            args = ['--game', s['game'], '--zone', str(s['zone']), '--act', str(s.get('act', 1)), '--main', main_key]
            if not stock:
                args += ['--mod', str(jar)]
            args += ['--out-dir', str(d), '--width', str(s.get('width', 320)), '--scale', '1', '--no-video']
            if kind == 'title':
                args += ['--title-screen', '--interactive-pacing', '--sidekick', 'tails' if stock else 'mica-and-talon:talon']
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
                    args += ['--sidekick', s['sidekick'] if stock else 'mica-and-talon:' + s['sidekick']]
            if s.get('frames'):
                args += ['--frames', str(s['frames'])]
            for flag in s.get('flags', []):
                args += [flag]
            if inp:
                args += ['--input', str(inp)]
            cmd = jvm + [f'-Dopenggf.saveRoot={saves}', '-cp', cp, 'com.openggf.tools.GameplayCaptureTool'] + args
        prov = dict({k: (str(v) if isinstance(v, Path) else v) for k, v in s.items()}, commit=commit, worktree_dirty=dirty,
                    jar_sha256=jar_sha, checkout=str(R), command=cmd[cmd.index('-cp') + 2:],
                    source_kind={'tool': 'positioned native gameplay', 'host': 'debug/positioned presentation host',
                                 'title': 'title-first production presentation'}[kind] + (' (stock control, no mod)' if stock else ''),
                    fps=60, every=1, audio=False)
        if kind == 'host':
            prov['capture_host_sha256'] = hashlib.sha256((T / 'hosts' / s['host'] / 'PromoCapture.java').read_bytes()).hexdigest()
        (d / 'provenance.json').write_text(json.dumps(prov, indent=2))
        print('CAPTURE', s['id'], flush=True)
        with (d / 'capture.log').open('w') as log:
            try:
                r = subprocess.run(cmd, cwd=R, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)
                rc = r.returncode
            except subprocess.TimeoutExpired:
                rc = -9
        n = len(list((d / 'frames').glob('*.png')))
        if rc:
            print('FAILED', s['id'], rc, n, 'frames', flush=True)
            continue
        if (d / 'state.csv').exists():
            rows = list(csv.DictReader(open(d / 'state.csv')))
            if rows:
                summ = dict(frames=len(rows), first=rows[0], last=rows[-1],
                            hurt=sum(r.get('hurt') == '1' for r in rows), dead=sum(r.get('dead') == '1' for r in rows))
                (d / 'observations.json').write_text(json.dumps(summ, indent=2))
        (d / 'DONE').write_text('')
        print('DONE', s['id'], n, 'frames', flush=True)


if __name__ == '__main__':
    main()
