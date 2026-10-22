#!/usr/bin/env python3
"""Compile, measure and capture the tutorial's authored LIVE scene without desktop input.
Origin: Stageplay revision-eight aesthetic revision, 2026-10-22. Requires Java25, matching
OpenGGF jar/checkout, FFmpeg and the user's existing S3K ROM. Never overwrites takes.
"""
import argparse,json,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--engine',type=Path,required=True);p.add_argument('--jar',type=Path,required=True)
p.add_argument('--rom',type=Path,required=True);p.add_argument('--script',type=Path,required=True)
p.add_argument('--render-only',action='store_true');p.add_argument('--simulate-only',action='store_true')
a=p.parse_args();stem=str(a.script.resolve()).removesuffix('.screenplay.json');scene=stem+'.stageplay'
env=os.environ.copy()
if 'JAVA_HOME' not in env and Path('/usr/lib/jvm/java-25-openjdk').is_dir():env['JAVA_HOME']='/usr/lib/jvm/java-25-openjdk'
for key in ('DISPLAY','WAYLAND_DISPLAY','JAVA_TOOL_OPTIONS','JDK_JAVA_OPTIONS','MAVEN_ARGS'):env.pop(key,None)
launch=[sys.executable,str(a.engine.resolve()/'tools/stageplay/stageplay.py'),'--jar',str(a.jar.resolve())]
commands=[]
if not a.render_only:
 commands += [['compile','--script',str(a.script.resolve()),'--out',scene],['simulate','--scene',scene,'--out',stem+'.jsonl','--s3k-rom',str(a.rom.resolve())]]
if not a.simulate_only:commands += [['render','--scene',scene,'--out',stem+'.mkv','--s3k-rom',str(a.rom.resolve()),'--scale','2']]
for command in commands:
 print('Stageplay '+command[0],flush=True)
 r=subprocess.run(launch+command,env=env,capture_output=True,text=True)
 if r.returncode:print(r.stderr[-6000:]);print(r.stdout);raise SystemExit(r.returncode)
 result=json.loads(r.stdout); print(json.dumps({'command':command[0],'ok':result.get('ok')}),flush=True)
