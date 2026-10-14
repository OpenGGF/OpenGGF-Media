#!/usr/bin/env python3
"""Render native AIZ music under official admission; no desktop connection.
Origin: delivered Second Strike reel, 2026-10-14. Inputs match capture_shots.py.
"""
from pathlib import Path
import sys,os,subprocess,json,hashlib
ROOT=Path(os.environ.get('OPENGGF_ROOT','/home/farrell/code/projects/OpenGGF')).resolve()
MEDIA=Path(os.environ.get('SECOND_STRIKE_MEDIA_ROOT',Path(__file__).resolve().parent)).resolve()
sys.path.insert(0,str(ROOT/'tools/testing'))
from maven_queue import maven_slot,inherited_slot,handle_termination

def main():
 out=MEDIA/'music';out.mkdir(exist_ok=True);runtime=out/'runtime';runtime.mkdir(exist_ok=True);runtime.chmod(0o700)
 env=os.environ.copy()
 for k in ['DISPLAY','WAYLAND_DISPLAY','JDK_JAVA_OPTIONS','JAVA_TOOL_OPTIONS','MAVEN_OPTS']:env.pop(k,None)
 env.update(ALSOFT_DRIVERS='null',XDG_RUNTIME_DIR=str(runtime))
 engine=ROOT/'target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar'
 cmd=['java','--enable-native-access=ALL-UNNAMED','-Dopenggf.headless.gl=surfaceless-egl','-cp',str(engine),str(MEDIA/'ReelMusic.java'),str(out),str(ROOT/'Sonic and Knuckles & Sonic 3 (W) [!].gen')]
 with maven_slot(ROOT,kind='second-strike-reel-music',estimate=30) as fd:
  assert hashlib.sha256(engine.read_bytes()).hexdigest()=='fad75320bf72a6de6fb84c7a8443afc08838d4bef54972103414d8e746271267'
  with (out/'capture.log').open('w')as log:p=subprocess.run(cmd,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120,**inherited_slot(fd))
  if p.returncode:print((out/'capture.log').read_text()[-3000:]);raise SystemExit(p.returncode)
  (out/'capture-result.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode,'gameplay_steps':1,'audio_presentations':900,'sample_rate':48000,'audio_policy':'ROM-native music-only; stopAllSfx before advancing presentation owner'},indent=2)+'\n')
  (out/'capture.log').unlink()
 print('Native music stem captured',flush=True)
if __name__=='__main__':
 with handle_termination():main()
