from pathlib import Path
import os,subprocess,sys
ROOT=Path('/home/james/IdeaProjects/OpenGGF');TASK=Path('/home/james/tmp/sonic-echoes-promo/captures');JAR=TASK/'a-helper-proof/promo-capture.jar';ROM=ROOT/'Sonic The Hedgehog 2 (W) (REV01) [!].gen'
os.environ['JAVA_HOME']='/home/james/.jdks/corretto-25.0.4.1';os.environ['PATH']='/usr/share/idea/plugins/maven-plugin/lib/maven3/bin:'+os.environ['PATH']
os.environ.pop('DISPLAY',None);os.environ.pop('WAYLAND_DISPLAY',None)
def props(room):
 p={}
 for l in (ROOT/f'examples/sonic-echoes/src/main/resources/rooms/{room}.properties').read_text().splitlines():
  if '=' in l and not l.startswith('#'):k,v=l.split('=',1);p[k]=v
 return p
def route(room,kind='solution'):
 p=props(room);loops=[];i=0
 while f'{kind}.{i}' in p:
  loops.append([(int(a.split(':')[0]),'+'.join(a.split(':')[1].replace('J','A'))) for a in p[f'{kind}.{i}'].split(',')]);i+=1
 result=[]
 for i,loop in enumerate(loops):
  result.extend(loop)
  if i<len(loops)-1:result.append((int(p['loopFrames'])-sum(n for n,b in loop)+12,'-'))
 return result

def run(name,room,segments,title=False,save=None,extra=None,actions=None):
 d=TASK/name;d.mkdir(parents=True,exist_ok=True)
 script=d/'inputs.script';script.write_text('\n'.join(f'{n} {b}' for n,b in segments if n>0)+'\n')
 cmd=['python3','tools/testing/maven_queue.py','-q','-Dmse=off','exec:java','-Dexec.mainClass=com.openggf.tools.InputLogAuthorTool',f'-Dexec.args=--script {script} --out {d}/inputs.txt']
 with (d/'author.log').open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
 p=props(room or '1-1');save=save or d/'save'
 cmd=['python3','tools/testing/maven_queue.py','-q','-Dmse=off','-Dopenggf.headless.gl=surfaceless-egl',f'-Dechoes.capture.session={d}/session.csv',f'-Dopenggf.saveRoot={save}']
 if room:cmd.append(f'-Dechoes.capture.room={room}')
 if actions:cmd.append(f'-Dechoes.capture.actions={actions}')
 jar=TASK/'a-helper-proof/promo-actions.jar' if actions else JAR
 cmd+=['exec:java','-Dexec.mainClass=com.openggf.tools.GameplayCaptureTool',f"-Dexec.args=--game s2 --rom '{ROM}' --mod {jar} --zone {p['zone']} --act {int(p['act'])+1} --width 400 --every 1 --input {d}/inputs.txt --no-video --stop-on-death false --out-dir {d}"+(' --title-screen --interactive-pacing' if title else '')+(extra or '')]
 (d/'command.txt').write_text(' '.join(__import__('shlex').quote(x) for x in cmd)+'\n')
 with (d/'capture.log').open('w') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
 print(name,'completed',flush=True)
if __name__=='__main__':
 if sys.argv[1]=='rooms':
  for name,room in [('a2-two-hands','1-2'),('a3-escort','1-4')]:run(name,room,[(180,'-')]+route(room)+[(120,'-')])
 elif sys.argv[1]=='titleprobe':run('a1-chain/probe',None,[(900,'-'),(1,'S'),(60,'-'),(1,'S'),(200,'-'),(40,'R'),(572,'-'),(240,'R'),(120,'-'),(1,'A'),(240,'-')],True)
