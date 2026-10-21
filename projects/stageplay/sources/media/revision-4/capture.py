#!/usr/bin/env python3
"""Rebuild the revised Stageplay film in a new, self-contained external take directory.
Origin: OpenGGF Stageplay native physics revision, 2026-10-21.
Copies only the screenplay's declared creator assets, never ROMs or existing footage.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def dependencies(script):
    paths={skin['decorationAsset'] for skin in script.get('dialogueSkins',[]) if skin.get('decorationAsset')}
    for shot in script['shots']:
        if shot['set'].get('levelProject'):paths.add(shot['set']['levelProject'])
        paths.update(cue['asset'] for cue in shot.get('audio',[]) if cue.get('asset'))
        paths.update(cue['portraitAsset'] for cue in shot.get('dialogue',[]) if cue.get('portraitAsset'))
    return sorted(paths)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--screenplay',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    for game in ['s1','s2','s3k']:p.add_argument('--'+game+'-rom',type=Path,required=True)
    p.add_argument('--build',action='store_true')
    a=p.parse_args();source=a.screenplay.resolve();source_root=source.parent
    recipe=json.loads(source.read_text());inputs=[]
    for relative in dependencies(recipe):
        name=Path(relative)
        if name.is_absolute() or '..' in name.parts:raise ValueError('Unsafe asset path')
        resolved=(source_root/name).resolve(strict=True)
        if not resolved.is_relative_to(source_root) or not resolved.is_file():raise ValueError('Asset escapes screenplay root')
        inputs.append((name,resolved))
    root=a.out_dir.resolve();root.mkdir(parents=True,exist_ok=False)
    screenplay=root/'location-remote.screenplay.json';shutil.copy2(source,screenplay)
    for name,resolved in inputs:
        target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(resolved,target)
    cli=[sys.executable,str(a.engine.resolve()/'tools/stageplay/stageplay.py')]
    if a.build:subprocess.run(cli+['--build','help'],check=True)
    scene=root/'location-remote.stageplay'
    subprocess.run(cli+['compile','--script',str(screenplay),'--out',str(scene)],check=True)
    subprocess.run(cli+['timeline','--scene',str(scene),'--out',str(root/'authored.jsonl')],check=True)
    subprocess.run(cli+['simulate','--scene',str(scene),'--out',str(root/'state.jsonl'),
        '--s1-rom',str(a.s1_rom.resolve()),'--s2-rom',str(a.s2_rom.resolve()),'--s3k-rom',str(a.s3k_rom.resolve())],check=True)
    subprocess.run(cli+['render','--scene',str(scene),'--out',str(root/'location-remote.mkv'),
        '--s1-rom',str(a.s1_rom.resolve()),'--s2-rom',str(a.s2_rom.resolve()),'--s3k-rom',str(a.s3k_rom.resolve())],check=True)
