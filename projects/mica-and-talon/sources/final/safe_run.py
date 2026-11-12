import json,subprocess,os
from pathlib import Path
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-bf758747');d=P/'captures/final/s1-safe';d.mkdir(parents=True,exist_ok=True)
p=json.loads((P/'captures/final/s1-run/provenance.json').read_text());c=p['command'];c[c.index('--out-dir')+1]=str(d)
for k in ['--x','--y','--rings','--timer']:
 i=c.index(k);del c[i:i+2]
p.update(command=c,source_kind='cold GHZ1 start, authored right input',id='s1-safe');(d/'provenance.json').write_text(json.dumps(p,indent=2));env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
with (d/'capture.log').open('w')as f:subprocess.run(c,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
