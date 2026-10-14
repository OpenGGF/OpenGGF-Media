#!/usr/bin/env python3
"""Capture three staged Second Strike scenes from exact delivered build.
Origin: Second Strike short reel, 2026-10-14. The official scheduler owns both
admission and main build lock; no shared desktop or target writes are used.
Inputs: OPENGGF_ROOT, SECOND_STRIKE_MEDIA_ROOT (defaults are this checkout/task).
"""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time

ROOT=Path(os.environ.get('OPENGGF_ROOT','/home/farrell/code/projects/OpenGGF')).resolve()
MEDIA=Path(os.environ.get('SECOND_STRIKE_MEDIA_ROOT',Path(__file__).resolve().parent)).resolve()
sys.path.insert(0,str(ROOT/'tools/testing'))
from maven_queue import maven_slot,inherited_slot,handle_termination

def main():
    engine=ROOT/'target/OpenGGF-0.7.prerelease-jar-with-dependencies.jar'
    mod=ROOT/'target/bundled/second-strike-0.1.0.jar'
    expected={engine:'fad75320bf72a6de6fb84c7a8443afc08838d4bef54972103414d8e746271267',mod:'ed7e49565aeba7e860cd514098e1ac9a2e3d868571c209e5e8b0b9efb2c66077'}
    for name in ['caterkiller','guard','plant']:
        out=MEDIA/'captures'/name
        runtime=out/'runtime';runtime.mkdir(parents=True,exist_ok=True);runtime.chmod(0o700)
        env=os.environ.copy()
        for key in ['DISPLAY','WAYLAND_DISPLAY','JDK_JAVA_OPTIONS','JAVA_TOOL_OPTIONS','MAVEN_OPTS']:
            env.pop(key,None)
        env.update(ALSOFT_DRIVERS='null',XDG_RUNTIME_DIR=str(runtime))
        command=['java','--enable-native-access=ALL-UNNAMED','-Dopenggf.headless.gl=surfaceless-egl','-cp',str(engine),str(MEDIA/'ReelCapture.java'),name,str(out),str(ROOT/'Sonic and Knuckles & Sonic 3 (W) [!].gen'),str(mod)]
        with maven_slot(ROOT,kind='second-strike-reel-capture',estimate=60) as fd:
            for path,sha in expected.items():
                if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise RuntimeError('Artifact changed; preserve take and resolve provenance')
            with (out/'capture.log').open('w') as log:
                p=subprocess.run(command,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180,**inherited_slot(fd))
            result={'name':name,'exit_code':p.returncode,'command':command,'desktop_unset':True,'artifact_sha256':{str(p):h for p,h in expected.items()}}
            (out/'capture-result.json').write_text(json.dumps(result,indent=2)+'\n')
            if p.returncode:print((out/'capture.log').read_text()[-5000:],flush=True);raise SystemExit(p.returncode)
            (out/'capture.log').unlink()
        print(json.dumps(result),flush=True)

if __name__=='__main__':
    with handle_termination():main()
