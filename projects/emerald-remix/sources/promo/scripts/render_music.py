#!/usr/bin/env python3
"""Planning audio only: render S2 EHZ 2P (0x91) through OpenGGF, no graphics or gameplay.
Inputs: this checkout compiled with Java 25, its dependency classpath, S2 REV01 ROM.
Origin: Emerald Remix promo planning, 2026-10-22; source 8aa692b045c195ef8a42896b6bbc9549158470c0.
"""
import argparse, os, subprocess
from pathlib import Path
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--checkout', type=Path, default=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach'))
p.add_argument('--java-home', type=Path, default=Path('/usr/lib/jvm/java-25-openjdk'))
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
cp = os.pathsep.join([str(a.checkout / 'target/classes'), (a.checkout / 'target/examples-classpath.txt').read_text().strip()])
subprocess.run([str(a.java_home / 'bin/java'), '--enable-native-access=ALL-UNNAMED', '-Xmx2g', '-cp', cp,
 'com.openggf.tools.audio.FmSfxRenderTool', '--game', 's2', '--rom', str(a.checkout / 's2.gen'),
 '--music', '91', '--rate', '48000', '--max-seconds', '76', '--out', str(root / 'audio/raw')], cwd=a.checkout, check=True)
# Keep only the full mix; FM-only and register writes are tool diagnostics, not production stems.
raw = root / 'audio/raw'
(raw / 's2-music-91-fm.wav').unlink()
(raw / 's2-music-91-ym-writes.txt').unlink()
