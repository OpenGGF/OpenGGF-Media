#!/usr/bin/env python3
"""Purpose: list ROM object spawns of acts (PromoCapture 'scout' mode) to pick honest mid-act positions
(starposts as safe ground, badnik clusters for strikes). One JVM at a time.
Usage: scout.py CHECKOUT game:zoneIdx:actIdx ...   -> work/scout/<game>-<zone>-<act>.txt
Origin: MICA & TALON promo redo 2026-11-11."""
import os, subprocess, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent
R = Path(sys.argv[1]).resolve()
cp = str(T / 'hosts/declared') + os.pathsep + str(R / 'target/classes') + os.pathsep + (R / 'target/mica-classpath.txt').read_text().strip()
env = {k: v for k, v in os.environ.items() if k not in ('DISPLAY', 'WAYLAND_DISPLAY', 'JAVA_TOOL_OPTIONS')}
(T / 'work/scout').mkdir(parents=True, exist_ok=True)
for spec in sys.argv[2:]:
    g, z, a = spec.split(':')
    out = T / f'work/scout/{g}-{z}-{a}.txt'
    if out.exists() and out.stat().st_size > 200:
        print('SKIP', spec); continue
    tmp = T / 'work/scout/tmp'
    r = subprocess.run(['java', '-Xmx1g', '--enable-native-access=ALL-UNNAMED', '-Dmse=off', '-Dopenggf.headless.gl=surfaceless-egl',
                        f'-Dopenggf.saveRoot={T / "work/scout/saves"}', '-cp', cp, 'PromoCapture', 'scout', str(tmp),
                        str(R / 'target/mica-and-talon/mica-and-talon.jar'), str(R / f'{g}.gen'), z, a],
                       cwd=R, env=env, capture_output=True, text=True, timeout=300)
    lines = [l for l in r.stdout.splitlines() if 'ObjectSpawn' in l or l.startswith('ACTIVE')]
    out.write_text('\n'.join(lines) + '\n')
    print(spec, r.returncode, len(lines), 'spawn lines', flush=True)
