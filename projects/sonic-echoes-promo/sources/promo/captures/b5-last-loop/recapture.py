"""Promo worker B final captures: authored controller routes and scheduled player actions."""
import os,subprocess,json,hashlib,csv
from pathlib import Path
base=Path('/home/james/tmp/sonic-echoes-promo/captures')
for shot,room,zone in [('b5-last-loop','3-4','cpz'),('b4-paradox','3-1','cpz'),('b1-double-bounce','2-2','htz'),('b2-counterweight','2-4','htz'),('b3-spring-relay','3-2','cpz'),('b6-clockwork','3-3','cpz')]:
 p=base/shot;action=(p/'actions.txt').exists();jar=base/('b5-last-loop/promo-action-capture.jar' if action else 'a-helper-proof/promo-capture.jar')
 cmd=['python3','tools/testing/maven_queue.py','-q','-Dmse=off','exec:java','-Dexec.mainClass=com.openggf.tools.InputLogAuthorTool',f'-Dexec.args=--script {p}/inputs.script --out {p}/inputs.txt']
 r=subprocess.run(cmd,capture_output=True,text=True);print('AUTHOR',shot,r.returncode,flush=True);assert r.returncode==0
 cmd=['python3','tools/testing/maven_queue.py','-q','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dechoes.capture.room={room}',f'-Dechoes.capture.session={p}/session.csv',f'-Dopenggf.saveRoot={p}/save']
 if action:cmd.append(f'-Dechoes.capture.actions={(p/"actions.txt").read_text()}')
 cmd+=['exec:java','-Dexec.mainClass=com.openggf.tools.GameplayCaptureTool',f"-Dexec.args=--game s2 --rom '/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen' --mod {jar} --zone {zone} --act 1 --width 400 --every 1 --input {p}/inputs.txt --no-video --out-dir {p}"]
 (p/'command.json').write_text(json.dumps({'argv':cmd,'jarSha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'env':{'DISPLAY':None,'WAYLAND_DISPLAY':None,'JAVA_HOME':os.environ['JAVA_HOME']}},indent=2))
 print('START',shot,flush=True);r=subprocess.run(cmd,capture_output=True,text=True);print('DONE',shot,r.returncode,flush=True)
 if r.returncode:print(r.stdout[-2000:],r.stderr[-2000:],flush=True);break
 rows=list(csv.DictReader((p/'session.csv').open()));print('EVENTS',[(x['frame'],x['events']) for x in rows if any(e in x['events'] for e in ['commit','restore','launch','spring','clear','badnik','fracture','star'])],flush=True)
