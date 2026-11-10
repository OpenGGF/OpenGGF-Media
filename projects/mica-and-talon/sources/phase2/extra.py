import subprocess,os,json,hashlib,csv
from pathlib import Path
P=Path(__file__).resolve().parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-66af4c18');J=R/'target/mica-and-talon/mica-and-talon.jar'
cp=str(P)+':'+str(R/'target/classes')+':'+(R/'target/mica-classpath.txt').read_text().strip()
env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
def java(mode,name,game,zone,act,x=None,y=None,log=None):
 d=P/'captures/phase2'/name;d.mkdir(parents=True,exist_ok=True)
 rom=R/('s3k.gen'if game=='s3k'else's2.gen')
 cmd=['java','-Xmx768m','--enable-native-access=ALL-UNNAMED','-Dopenggf.headless.gl=surfaceless-egl','-Dmse=off','-Dopenggf.saveRoot='+str(P/'saves'),'-cp',cp,'PromoCapture',mode,str(d),str(J),str(rom),str(zone),str(act)]
 if x is not None:cmd += [str(x),str(y)]
 if log:cmd += [str(log)]
 (d/'provenance.json').write_text(json.dumps(dict(id=name,source_kind='debug presentation component entry'if mode in ['ending','continue']else 'positioned native gameplay',game=game,zone=zone,act=act,x=x,y=y,rings=70,main='mica',sidekick='talon',commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),jar_sha256=hashlib.sha256(J.read_bytes()).hexdigest(),command=cmd),indent=2))
 with open(d/'capture.log','w')as f:subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=300)
 return d
if __name__=='__main__':
 import sys
 if sys.argv[1]=='screens':
  for mode,zone in [('continue',0),('ending',10)]:
   try:print(java(mode,mode,'s2',zone,0),flush=True)
   except Exception as e:print(e,flush=True)
 else:
  for g,z,act in [('s2',0,1),('s2',2,0),('s2',13,0),('s2',1,0),('s2',4,0),('s3k',0,1),('s3k',1,0),('s3k',2,0),('s3k',2,1),('s3k',6,0)]:
   try:print(java('scout',f'scout-{g}-{z}-{act}',g,z,act),flush=True)
   except Exception as e:print(e,flush=True)
