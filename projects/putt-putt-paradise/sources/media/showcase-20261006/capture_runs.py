from pathlib import Path
import subprocess, os, hashlib, json
root=Path(__file__).resolve().parent
repo=Path('/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise')
jar=repo/'target/putt-putt-paradise/putt-putt-paradise.jar'
rom=Path('/home/farrell/code/projects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen')
cp=str(repo/'target/classes')+os.pathsep+(repo/'target/putt-putt-paradise/engine-classpath.txt').read_text().strip()
(root/'engine-classpath.txt').write_text(cp)
subprocess.run(['javac','--release','21','-cp',cp,'-d',str(root/'classes'),str(root/'source/GolfShowcaseCapture.java')],check=True)
engine_source=hashlib.sha256()
for source in sorted((repo/'src/main/java').rglob('*.java')):
 engine_source.update(str(source.relative_to(repo)).encode()+b'\0'+source.read_bytes()+b'\0')
for name,act,character,mode in [('ehz1-sonic-rewind',0,'sonic','practice'),('local-two-player',0,'sonic','local'),('ehz2-tails',1,'tails','practice')]:
 out=root/(name+'-final-v3');out.mkdir()
 meta={'rom_sha1':hashlib.sha1(rom.read_bytes()).hexdigest(),'mod_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'act':act,'character':character,'mode':mode,'native_hz':60,'capture_fps':30,'dimensions':[320,224],'audio':'silent','entry':'explicit SDK-validated ModContext capture wrapper','baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'engine_java_sha256':engine_source.hexdigest(),'working_diff_sha256':hashlib.sha256(subprocess.check_output(['git','diff','HEAD'],cwd=repo)).hexdigest()}
 (out/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
 with (out/'capture.log').open('w') as log:
  subprocess.run(['java','-cp',str(root/'classes')+os.pathsep+cp,'com.openggf.mods.code.GolfShowcaseCapture',str(rom),str(jar),str(out),str(act),character,mode],stdout=log,stderr=subprocess.STDOUT,check=True,cwd=repo)
 print('Captured '+name,flush=True)
