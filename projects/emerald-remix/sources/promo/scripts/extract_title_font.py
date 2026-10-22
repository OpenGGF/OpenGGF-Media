#!/usr/bin/env python3
"""Rebuild local ROM-derived title alphabet with the production decoder, 2026-10-22.
Inputs: checkout compiled tools, supplied REV01 ROM. No engine or repository source edit.
"""
import subprocess
from pathlib import Path
R=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
P=Path(__file__).resolve().parents[1]
cp=str(R/'target/classes')+':'+(R/'target/examples-classpath.txt').read_text().strip()
subprocess.run(['/usr/lib/jvm/java-25-openjdk/bin/javac','-cp',cp,'-d',str(R/'target'),str(P/'scripts/ExtractTitleFont.java')],check=True)
subprocess.run(['/usr/lib/jvm/java-25-openjdk/bin/java','-cp',str(R/'target')+':'+cp,'ExtractTitleFont',str(R/'s2.gen'),str(P/'design/rom-title-font')],check=True)
