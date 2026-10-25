#!/usr/bin/env python3
"""Production launcher for the "Day Off" Stageplay promo (sp-promo-a, 2026-10-24).

Runs com.openggf.tools.StageplayTool from a snapshot engine jar with the same JVM
shape as tools/stageplay/stageplay.py (surfaceless EGL, desktop display variables
removed, -Xmx4g, offline audio), supplies the three verified ROM paths, and holds the
shared Maven build-activity lease while the JVM runs. Unlike the repository launcher
it does not take the worktree build lock: the snapshot jar lives outside target/, so
focused Maven checks in the worktree and production renders can overlap.

Usage: sp.py [--jar PATH] COMMAND [ARGS...]   (ROM flags are appended for
simulate/render/route/ground unless already present)
"""
import os
import subprocess
import sys
from pathlib import Path

WORKTREE = Path('/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a')
PROD = Path('/home/farrell/Videos/OGGF/sp-promo-a')
DEFAULT_JAR = PROD / 'engine' / 'openggf-sp-promo-a-r2.jar'  # v2: develop 81f25c89f (v1 used -r1.jar, 0ba60490e)
ROMS = {
    '--s1-rom': WORKTREE / 'Sonic The Hedgehog (W) (REV01) [!].gen',
    '--s2-rom': WORKTREE / 'Sonic The Hedgehog 2 (W) (REV01) [!].gen',
    '--s3k-rom': WORKTREE / 'Sonic and Knuckles & Sonic 3 (W) [!].gen',
}
PATH_FLAGS = {'--scene', '--script', '--out', '--rom', '--s1-rom', '--s2-rom', '--s3k-rom',
              '--staging-dir', '--observations', '--request'}
sys.path.insert(0, str(WORKTREE / 'tools' / 'testing'))
from maven_activity import build_activity_slot  # noqa: E402


def main(argv):
    jar = DEFAULT_JAR
    if argv[:1] == ['--jar']:
        jar, argv = Path(argv[1]), argv[2:]
    if not argv:
        raise SystemExit(__doc__)
    command, args = argv[0], list(argv[1:])
    if command in {'simulate', 'render', 'route', 'ground'}:
        for flag, rom in ROMS.items():
            if flag not in args:
                args += [flag, str(rom)]
    for i, item in enumerate(args[:-1]):
        if item in PATH_FLAGS:
            args[i + 1] = str(Path(args[i + 1]).resolve())
    env = os.environ.copy()
    env.pop('DISPLAY', None)
    env.pop('WAYLAND_DISPLAY', None)
    java = str(Path(env.get('JAVA_HOME', '/usr/lib/jvm/java-25-openjdk')) / 'bin' / 'java')
    cmd = [java, '-Xmx4g', '--enable-native-access=ALL-UNNAMED', '-Djava.awt.headless=true',
           '-Dopenggf.headless.gl=surfaceless-egl', '-cp', str(jar.resolve()),
           'com.openggf.tools.StageplayTool', command, *args]
    with build_activity_slot(WORKTREE) as leases:
        return subprocess.run(cmd, cwd=WORKTREE, env=env, pass_fds=tuple(leases)).returncode


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
