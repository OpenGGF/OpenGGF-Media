#!/usr/bin/env python3
"""Capture current Typing selected-section travel/fight continuation, task 2026-10-25.
Uses the production headless capture tool at full 60-Hz draw cadence. The built-in
attract typist supplies words; No-Fail is declared, and desktop audio stays disabled.
"""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args()
saves=a.out/'typing-hilltop-saves';storage=saves/'mods/typing-of-the-hedgehog';storage.mkdir(parents=True,exist_ok=True)
intent=dict(mode='ARCADE',game='s2',zone=4,act=1,difficulty='NORMAL',capitals='false',punctuation='false',seed=5,dictionaries='standard',bossStars=1,noFail='true',slowMotion='false',voice='OFF',demo='true',demoRows=0)
(storage/'intent.txt').write_text(''.join(f'{k}={v}\n' for k,v in intent.items()))
mod=a.engine/'examples/typing-of-the-hedgehog/target/typing-of-the-hedgehog-mod.jar'
assert mod.is_file(), 'Build the matching artifact-only mod first'
args=f'--game s2 --rom {a.rom.resolve()} --mod {mod.resolve()} --zone 4 --act 2 --width 400 --main sonic --sidekick none --frames 1800 --every 1 --fps 60 --no-video --out-dir {a.out.resolve()}/typing-hilltop-current'
env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
with (a.engine/'target/typing-route-demo-capture.log').open('w') as log:
 subprocess.run(['python3','tools/testing/maven_queue.py','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl','-Dopenggf.saveRoot='+str(saves.resolve()),'exec:java','-Dexec.mainClass=com.openggf.tools.GameplayCaptureTool','-Dexec.args='+args],cwd=a.engine,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
print('Captured 1800 full-draw frames to',a.out/'typing-hilltop-current')
