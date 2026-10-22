#!/usr/bin/env python3
"""Emerald Remix rough-cut editorial punctuation; 2026-10-22.
Inputs: supplied S2 ROM and this checkout's production SMPS driver. Offline PCM only.
C3=Enter Giant Ring (title), BC=Spindash Release (chapter), B5=Ring Right (split).
These cues are editorial, not recordings of an event in the silent gameplay sources.
"""
import subprocess
from pathlib import Path
R=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
P=Path(__file__).resolve().parents[1]
cp=str(R/'target/classes')+':'+(R/'target/examples-classpath.txt').read_text().strip()
for s in ['c3','bc','b5']:
 subprocess.run(['/usr/lib/jvm/java-25-openjdk/bin/java','--enable-native-access=ALL-UNNAMED','-cp',cp,
  'com.openggf.tools.audio.FmSfxRenderTool','--game','s2','--rom',str(R/'s2.gen'),
  '--sfx',s,'--rate','48000','--max-seconds','4','--out',str(P/'audio/stingers')],check=True)
 for tail in ['fm.wav','ym-writes.txt']:(P/f'audio/stingers/s2-sfx-{s}-{tail}').unlink(missing_ok=True)
