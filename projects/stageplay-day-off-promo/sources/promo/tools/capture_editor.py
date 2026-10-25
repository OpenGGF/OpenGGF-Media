#!/usr/bin/env python3
"""Run EditorCapture.java (in-engine Stageplay editor, display-free) for the sp-promo-a promo.

Usage: capture_editor.py SCRIPT SCENE OUT_DIR [--jar JAR] [--tool EditorCapture2.java] [--desktop]
Writes OUT_DIR/SCRIPT.mkv (FFV1 1920x1080 60 fps), OUT_DIR/SCRIPT.events.json and
OUT_DIR/SCRIPT.log. Surfaceless EGL; DISPLAY/WAYLAND_DISPLAY are removed; offline audio only.
Holds the shared build-activity lease like tools/sp.py. Origin: 2026-10-24 sp-promo-a.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sp  # noqa: E402  (ROM paths, jar and lease helpers)


def main(argv):
    jar = sp.DEFAULT_JAR
    desktop = '--desktop' in argv
    argv = [a for a in argv if a != '--desktop']
    if '--jar' in argv:
        i = argv.index('--jar'); jar = Path(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    tool = 'EditorCapture.java'                      # v1 driver; v2 passes --tool EditorCapture2.java
    if '--tool' in argv:
        i = argv.index('--tool'); tool = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    script, scene, out_dir = argv[0], Path(argv[1]).resolve(), Path(argv[2]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    mkv, events, log = (out_dir / f'{script}.mkv', out_dir / f'{script}.events.json', out_dir / f'{script}.log')
    if mkv.exists():
        raise SystemExit(f'refusing to overwrite {mkv}')
    env = os.environ.copy()
    env.pop('DISPLAY', None)
    env.pop('WAYLAND_DISPLAY', None)
    java = str(Path(env.get('JAVA_HOME', '/usr/lib/jvm/java-25-openjdk')) / 'bin' / 'java')
    classpath = str(jar.resolve())
    extra = []
    if desktop:
        # OpenGGF Editor worktree classes and its private-repository ImGui jars (desktop chrome).
        editor = Path('/home/farrell/code/projects/OpenGGF-Editor/.worktrees/sp-promo-a')
        repo = editor / '.m2' / 'repository' / 'io' / 'github' / 'spair'
        jars = [editor / 'target' / 'classes'] + sorted(repo.glob('imgui-java-*/1.92.7.1/*.jar'))
        classpath = ':'.join([str(p) for p in jars] + [classpath])
        extra = ['-Dcapture.chrome=desktop']
    cmd = [java, '-Xmx4g', '--enable-native-access=ALL-UNNAMED', '-Djava.awt.headless=true',
           '-Dopenggf.headless.gl=surfaceless-egl', *extra, '-cp', classpath, str(HERE / tool),
           script, str(mkv), str(events), str(scene),
           str(sp.ROMS['--s1-rom']), str(sp.ROMS['--s2-rom']), str(sp.ROMS['--s3k-rom'])]
    with open(log, 'w') as handle, sp.build_activity_slot(sp.WORKTREE) as leases:
        return subprocess.run(cmd, cwd=sp.WORKTREE, env=env, stdout=handle, stderr=subprocess.STDOUT,
                              pass_fds=tuple(leases)).returncode


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
