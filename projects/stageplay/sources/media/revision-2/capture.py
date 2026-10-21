#!/usr/bin/env python3
"""Rebuild a Stageplay source movie in a new external take directory.
Origin: Location, Location, Location production, 2026-10-21.
"""
import argparse
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--engine',type=Path,required=True)
p.add_argument('--screenplay',type=Path,required=True)
p.add_argument('--out-dir',type=Path,required=True)
for game in ['s1','s2','s3k']:p.add_argument('--'+game+'-rom',type=Path,required=True)
p.add_argument('--build',action='store_true')
a=p.parse_args();root=a.out_dir.resolve();root.mkdir(parents=True,exist_ok=False)
cli=[sys.executable,str(a.engine.resolve()/'tools/stageplay/stageplay.py')]
if a.build:subprocess.run(cli+['--build','help'],check=True)
scene=root/'location-remote.stageplay'
subprocess.run(cli+['compile','--script',str(a.screenplay.resolve()),'--out',str(scene)],check=True)
subprocess.run(cli+['timeline','--scene',str(scene),'--out',str(root/'state.jsonl')],check=True)
subprocess.run(cli+['render','--scene',str(scene),'--out',str(root/'location-remote.mkv'),
    '--s1-rom',str(a.s1_rom.resolve()),'--s2-rom',str(a.s2_rom.resolve()),'--s3k-rom',str(a.s3k_rom.resolve())],check=True)
