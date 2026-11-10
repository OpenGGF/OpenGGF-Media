"""Replay retained phase-2 provenance against final checkout; preserve original setup and controller inputs."""
import os,json,subprocess,hashlib,shutil
from pathlib import Path
P=Path(__file__).resolve().parent; OLD=P.parent/'phase2';R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-bf758747'); OR='/mnt/LinuxData/T3/worktrees/OpenGGF/t3-66af4c18';J=R/'target/mica-and-talon/mica-and-talon.jar'
cp=str(R/'target/classes')+':'+(R/'target/mica-classpath.txt').read_text().strip()
env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
for host in (P/'hosts').iterdir():subprocess.run(['javac','-cp',cp,str(host/'PromoCapture.java')],check=True)
names=['hero-mgz2','hero','s1-run','s2-run','s3k-run','talon-s2','talon-s3k','team','gilded','solar','ehz-clear','gilded-clear-low','halfpipe-cleared-post','blue-play','continue','data-select-team','ending-full']
for name in names:
 src=OLD/'captures/phase2'/name;d=P/'captures/final'/name;d.mkdir(parents=True,exist_ok=True)
 pr=json.loads((src/'provenance.json').read_text());cmd=pr['command']
 if cmd[0]!='java':cmd=['java','-Xmx768m','--enable-native-access=ALL-UNNAMED','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dopenggf.saveRoot={P}/saves','-cp',cp,'com.openggf.tools.GameplayCaptureTool',*cmd]
 mapped=[]
 for x in cmd:
  if x==OR+'/s2.gen' or x==OR+'/s3k.gen':x=str(R/Path(x).name)
  elif x.startswith('-Dopenggf.saveRoot='):x=f'-Dopenggf.saveRoot={P}/saves'
  elif x==str(src):x=str(d)
  elif x.startswith(OR):x=x.replace(OR,str(R))
  elif x.startswith(str(OLD)) and Path(x).is_file():
   dest=d/Path(x).name;shutil.copy2(x,dest);x=str(dest)
  mapped.append(x)
 cmd=mapped
 host=pr.get('capture_host_source','hosts/original/PromoCapture.java');cmd[cmd.index('-cp')+1]=str((P/host).parent)+':'+cp
 if '--save-slots' in cmd:
  ix=cmd.index('--save-slots')+1;dest=d/'slots.json';shutil.copy2(cmd[ix],dest) if Path(cmd[ix])!=dest else None;cmd[ix]=str(dest)
 pr.update(command=cmd,commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),jar=str(J),jar_sha256=hashlib.sha256(J.read_bytes()).hexdigest(),checkout=str(R))
 (d/'provenance.json').write_text(json.dumps(pr,indent=2))
 print('CAPTURE',name,flush=True)
 with (d/'capture.log').open('w')as log:subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=600)
 print('DONE',name,flush=True)
# Native title, neutral controller, no seeded level state.
d=P/'captures/final/title-s2';d.mkdir(parents=True,exist_ok=True)
cmd=['java','-Xmx768m','--enable-native-access=ALL-UNNAMED','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dopenggf.saveRoot={P}/saves-title','-cp',cp,'com.openggf.tools.GameplayCaptureTool','--game','s2','--zone','ehz','--act','1','--title-screen','--mod',str(J),'--main','mica-and-talon:mica','--sidekick','mica-and-talon:talon','--frames','660','--width','320','--scale','1','--no-video','--out-dir',str(d)]
(d/'provenance.json').write_text(json.dumps(dict(command=cmd,commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),source_kind='production S2 title; neutral input through full rise',jar_sha256=hashlib.sha256(J.read_bytes()).hexdigest()),indent=2))
with (d/'capture.log').open('w')as log:subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
print('DONE title-s2',flush=True)
