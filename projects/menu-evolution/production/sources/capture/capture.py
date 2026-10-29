#!/usr/bin/env python3
"""Menu evolution promo: record moving menu takes from three source eras.

Purpose: compile the production-root recorders against each era's own compiled tree and run the
named takes, writing native 60 Hz PNG frames, events.csv and provenance under clips/<era>/<take>/.
Origin: menu-evolution-promo-20261029 (Opus 5.5 producer, base d823ce643).

Eras (each built from its own tree; historical trees are `git archive` exports under the
producer worktree's target/eras, compiled with `mvn -Dmse=off -q -DskipTests compile
dependency:build-classpath -Dmdep.outputFile=target/cp.txt`):
  v05  77c6364ce (tag v0.5.20260411)      V05TitleRecorder (0.5 had only the game-select title)
  pre  2f9ca84b1 (pre-redesign develop)    MenuFilmRecorder, ShaderFilmRecorder
  new  d823ce643 (delivered menus)         MenuFilmRecorder, ShaderFilmRecorder

Usage: capture.py <era> <take> [<take>...]   (take names are files in takes/<name>.take)
       capture.py --list
Environment: OPENGGF_WORKTREE (default: the producer worktree), JAVA_HOME (JDK 25).
Runs display-free: DISPLAY/WAYLAND_DISPLAY/LD_LIBRARY_PATH removed, surfaceless EGL selected.
ROMs are read in place from the original root by absolute path; nothing is copied or linked.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # production root
WT = Path(os.environ.get('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-3a990895'))
JAVA_HOME = Path(os.environ.get('JAVA_HOME', '/usr/lib/jvm/java-25-openjdk'))
ROMS = Path('/home/farrell/code/projects/OpenGGF')
S1 = ROMS / 'Sonic The Hedgehog (W) (REV01) [!].gen'
S2 = ROMS / 'Sonic The Hedgehog 2 (W) (REV01) [!].gen'
S3K = ROMS / 'Sonic and Knuckles & Sonic 3 (W) [!].gen'
MODS = ROMS / 'mods'
ERAS = {
    'v05': ('77c6364cee5ceb7c16ade97c3117b864044a3cb2', WT / 'target/eras/v05', 'java05'),
    'pre': ('2f9ca84b18c8bae45a298348676e28d0a91a0798', WT / 'target/eras/pre', 'java'),
    'new': ('d823ce643d2acd23e9024aafa55b4f90211421ff', WT, 'java'),
}


def classpath(era):
    tree = ERAS[era][1]
    return f"{tree / 'target/classes'}:{(tree / 'target/cp.txt').read_text().strip()}"


def compile_helpers(era):
    src = HERE / ERAS[era][2]
    out = WT / 'target/promo-helpers' / era
    out.mkdir(parents=True, exist_ok=True)
    files = [str(p) for p in src.rglob('*.java')]
    subprocess.run([str(JAVA_HOME / 'bin/javac'), '-nowarn', '-d', str(out), '-cp', classpath(era), *files],
                   check=True)
    return out


def run(era, take):
    sha, tree, _ = ERAS[era]
    takefile = HERE / 'takes' / f'{take}.take'
    head = dict(l.split('=', 1) for l in takefile.read_text().splitlines() if '=' in l and not l.startswith('#'))
    tool = head.get('tool', 'MenuFilmRecorder').strip()
    out = ROOT / 'clips' / era / take
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    helpers = compile_helpers(era)
    env = {k: v for k, v in os.environ.items() if k not in ('DISPLAY', 'WAYLAND_DISPLAY', 'LD_LIBRARY_PATH')}
    run_dir = WT / 'target/promo-run' / era
    run_dir.mkdir(parents=True, exist_ok=True)
    args = [str(JAVA_HOME / 'bin/java'), '-Xmx2g', '-Dopenggf.headless.gl=surfaceless-egl',
            '-cp', f'{helpers}:{classpath(era)}', f'com.openggf.tools.{tool}', str(takefile), str(out),
            str(S1), str(S2), str(S3K), str(MODS)]
    log = WT / 'target/promo-logs' / f'take-{era}-{take}.log'
    with log.open('w') as stream:
        r = subprocess.run(args, cwd=run_dir, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
    frames = len(list((out / 'frames').glob('*.png')))
    (out / 'provenance.json').write_text(json.dumps({
        'era': era, 'source_commit': sha, 'tree': str(tree), 'tool': tool, 'take': f'takes/{take}.take',
        'frames': frames, 'rate': 60, 'scale': 1, 'exit': r.returncode,
        'roms': [str(S1), str(S2), str(S3K)], 'mods_dir': str(MODS),
        'backend': 'surfaceless EGL, DISPLAY/WAYLAND_DISPLAY/LD_LIBRARY_PATH unset, no audio device opened',
        'command': ' '.join(args[:4] + ['<helpers:classpath>'] + args[5:]),
    }, indent=1))
    print(f'{era} {take}: exit {r.returncode}, {frames} frames (log {log})', flush=True)
    if r.returncode:
        print(log.read_text()[-3000:])
    return r.returncode


def main():
    if sys.argv[1:] == ['--list']:
        print('\n'.join(sorted(p.stem for p in (HERE / 'takes').glob('*.take'))))
        return
    era, takes = sys.argv[1], sys.argv[2:]
    codes = [run(era, t) for t in takes]
    sys.exit(max(codes) if codes else 0)


if __name__ == '__main__':
    main()
