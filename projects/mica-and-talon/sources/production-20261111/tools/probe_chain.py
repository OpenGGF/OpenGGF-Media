"""Purpose: fast no-render probes (host 'probe' mode) searching start/inputs for an airborne homing chain.
Inputs: checkout, list of (zone act x y script). Prints score transitions. Origin: MT production promo 2026-11-11."""
import subprocess,os,sys,csv,json,itertools
from pathlib import Path
R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-3c245e9e');T=Path(__file__).resolve().parent.parent
cp=str(T/'hosts/declared')+':'+str(R/'target/classes')+':'+(R/'target/mica-classpath.txt').read_text().strip()
env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
cases=json.loads(Path(sys.argv[1]).read_text())
for c in cases:
  d=T/'probes'/c['id'];d.mkdir(parents=True,exist_ok=True);(d/'frames').mkdir(exist_ok=True);(d/'in.script').write_text(c['script'])
  subprocess.run(['java','-Xmx1g','--enable-native-access=ALL-UNNAMED','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl','-cp',cp,'com.openggf.tools.InputLogAuthorTool','--script',str(d/'in.script'),'--out',str(d/'in.txt')],env=env,check=True,capture_output=True,cwd=R)
  r=subprocess.run(['java','-Xmx1g','--enable-native-access=ALL-UNNAMED','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dopenggf.saveRoot={d}','-cp',cp,'PromoCapture','probe',str(d),str(R/'target/mica-and-talon/mica-and-talon.jar'),str(R/(c['game']+'.gen')),str(c['zone']),str(c['act']),str(c['x']),str(c['y']),str(d/'in.txt')],env=env,capture_output=True,text=True,cwd=R)
  rows=list(csv.DictReader(open(d/'state.csv'))) if (d/'state.csv').exists() else []
  ch=[];p='0'
  for i,x in enumerate(rows):
    if x['score']!=p:ch.append((i,x['score'],x['air']));p=x['score']
  print(c['id'],'rc',r.returncode,'frames',len(rows),'dead',any(x['dead']=='1' for x in rows),'score',ch,flush=True)
