#!/usr/bin/env python3
"""Purpose: repeatable, sequential captures for the MICA & TALON promo redo (2026-11-11).
Inputs: --checkout (built engine + example jar, verified ROM links in its root), --shots JSON list(s).
Origin: mt-promo-final-20261111/tools/capture.py, generalised: shots come only from JSON batches, stock
(no-mod) controls are supported for lockstep comparisons, finished captures are skipped unless --force.
Every shot is silent, 60 Hz, every=1, surfaceless EGL, no trace input. One JVM at a time.
Shot keys: id, kind (tool|host|title), game, zone, act, x, y, rings, timer, emeralds, main, sidekick,
  stock (true = no mod, stock characters), script | input_from, frames, width, flags, props, host, mode, slots.
Stage B (2026-11-12): every take also records audio.wav, SFX only (GameplayCaptureTool --audio --no-music; the
  hosts through hosts/common/PromoAudio). Shot keys audio (false = silent take) and music (true = keep the
  music, for the RMS control run). --dest picks the output folder (captures-b, probes-b).
Usage: capture.py --checkout DIR --shots a.json [b.json ...] [--only id ...] [--force] [--dest DIR] [--silent]
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
    ap.add_argument('--dest', default='captures')
    ap.add_argument('--mod-commit', help='the integration commit the example mod comes from (recorded as mod_commit)')
    ap.add_argument('--develop-commit', help='the develop commit merged into the build (recorded as develop_commit)')
    ap.add_argument('--silent', action='store_true', help='no audio at all (the pre-stage-B behaviour)')
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
    # The build is a local merge, so a take names three commits: the build (HEAD), the integration commit the
    # mod comes from, and the develop commit merged in. Both must be ancestors of the build, and the mod's
    # sources in the build must be byte-identical to the integration commit's.
    ident = {}
    for key, ref in (('mod_commit', a.mod_commit), ('develop_commit', a.develop_commit)):
        if ref:
            full = subprocess.check_output(['git', 'rev-parse', ref + '^{commit}'], cwd=R, text=True).strip()
            if subprocess.run(['git', 'merge-base', '--is-ancestor', full, 'HEAD'], cwd=R).returncode:
                raise SystemExit(f'{key} {ref} is not an ancestor of the build commit')
            ident[key] = full
    if 'mod_commit' in ident:
        same = subprocess.run(['git', 'diff', '--quiet', ident['mod_commit'], 'HEAD', '--', 'examples/mica-and-talon'], cwd=R).returncode == 0
        if not same:
            raise SystemExit('examples/mica-and-talon in the build differs from mod_commit')
        ident['mod_sources_identical_to_mod_commit'] = True
    shots = [s for f in a.shots for s in json.loads(f.read_text())]
    jvm = ['java', '-Xmx1g', '--enable-native-access=ALL-UNNAMED', '-Dmse=off', '-Dopenggf.headless.gl=surfaceless-egl']
    roms = {g: R / f'{g}.gen' for g in ('s1', 's2', 's3k')}
    for s in shots:
        if a.only and s['id'] not in a.only:
            continue
        d = T / a.dest / s['id']
        audio = not a.silent and s.get('audio', True)
        music = bool(s.get('music'))
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
            aud = ([] if audio else ['-Dpromo.audio=false']) + (['-Dpromo.music=true'] if music else [])
            cmd = jvm + [f'-D{k}={v}' for k, v in s.get('props', {}).items()] + aud + [
                f'-Dopenggf.saveRoot={saves}', '-cp', str(host) + os.pathsep + str(T / 'hosts/common') + os.pathsep + cp,
                'PromoCapture'] + args
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
            if audio:
                args += ['--audio'] + ([] if music else ['--no-music'])
            if inp:
                args += ['--input', str(inp)]
            cmd = jvm + [f'-Dopenggf.saveRoot={saves}', '-cp', cp, 'com.openggf.tools.GameplayCaptureTool'] + args
        prov = dict({k: (str(v) if isinstance(v, Path) else v) for k, v in s.items()}, commit=commit, build_commit=commit, **ident, worktree_dirty=dirty,
                    jar_sha256=jar_sha, checkout=str(R), command=cmd[cmd.index('-cp') + 2:],
                    source_kind={'tool': 'positioned native gameplay', 'host': 'debug/positioned presentation host',
                                 'title': 'title-first production presentation'}[kind] + (' (stock control, no mod)' if stock else ''),
                    fps=60, every=1, audio=audio, audio_stem=('music and SFX' if music else 'SFX only, music volume 0') if audio else None)
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
                if audio and (d / 'audio.wav').exists():
                    import wave
                    with wave.open(str(d / 'audio.wav')) as w:
                        summ['audio'] = dict(rate=w.getframerate(), channels=w.getnchannels(), samples=w.getnframes(),
                                             samples_per_video_frame=round(w.getnframes() / max(1, len(rows)), 2))
                elif audio:
                    summ['audio'] = 'MISSING'
                (d / 'observations.json').write_text(json.dumps(summ, indent=2))
        (d / 'DONE').write_text('')
        print('DONE', s['id'], n, 'frames', flush=True)


if __name__ == '__main__':
    main()
