#!/usr/bin/env python3
"""Rebuild Stageplay LIVE demonstration movies from preserved directing sources.

Inputs: matching OpenGGF checkout/package, existing S3K ROM, fresh external output.
Origin: OpenGGF Stageplay live-world delivery, 2026-10-21. Uses no desktop input.
This driver does not build silently; supply a matching packaged engine with --jar.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

NAMES=('live-platform-relay','live-air-traffic','live-ring-run','one-more-take')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--s3k-rom',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--sources',type=Path,default=Path(__file__).resolve().parent/'scenes')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy()
    for key in ('DISPLAY','WAYLAND_DISPLAY'):env.pop(key,None)
    launch=[sys.executable,str(args.engine.resolve()/'tools/stageplay/stageplay.py'),'--jar',str(args.jar.resolve())]
    for name in NAMES:
        script=args.out/(name+'.screenplay.json');shutil.copyfile(args.sources/(name+'.screenplay.json'),script)
        scene=args.out/(name+'.stageplay')
        commands=[['compile','--script',str(script),'--out',str(scene)],
                  ['simulate','--scene',str(scene),'--out',str(args.out/(name+'-final.jsonl')),'--s3k-rom',str(args.s3k_rom.resolve())],
                  ['render','--scene',str(scene),'--out',str(args.out/(name+'-review.mkv')),'--s3k-rom',str(args.s3k_rom.resolve()),'--scale','2']]
        subprocess.run(launch+commands[0],env=env,check=True)
        preserved=args.sources/(name+'.stageplay')
        if scene.read_bytes()!=preserved.read_bytes():raise RuntimeError('Compiled scene differs from preserved source: '+name)
        for command in commands[1:]:subprocess.run(launch+command,env=env,check=True)
    print(json.dumps({'ok':True,'out':str(args.out),'scenes':list(NAMES)}))

if __name__=='__main__':main()
