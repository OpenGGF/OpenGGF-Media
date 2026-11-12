import subprocess,json,os
from pathlib import Path
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-bf758747');d=P/'captures/final/title-s2-full';d.mkdir(parents=True,exist_ok=True);p=json.loads((P/'captures/final/title-s2/provenance.json').read_text());c=p['command'];c[c.index('--frames')+1]='1200';c[c.index('--out-dir')+1]=str(d);p['command']=c;(d/'provenance.json').write_text(json.dumps(p,indent=2));env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
with (d/'capture.log').open('w')as f:subprocess.run(c,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
