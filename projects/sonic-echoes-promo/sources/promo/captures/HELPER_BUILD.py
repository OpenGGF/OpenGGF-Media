#!/usr/bin/env python3
"""Build test-only promo jar; reuse current engine classes, never alter distributed jar."""
from pathlib import Path
import os,subprocess,shutil,zipfile,sys
root=Path.cwd(); out=Path(__file__).parent/'a-helper-proof'; classes=out/'classes'
classes.mkdir(parents=True,exist_ok=True)
cp=str(root/'target/classes')+os.pathsep+(root/'target/examples-classpath.txt').read_text().strip()
java=Path(os.environ['JAVA_HOME'])/'bin'
sources=list((root/'examples/sonic-echoes/src/main/java').rglob('*.java'))+[root/'examples/sonic-echoes/src/test/java/echoes/PromoCaptureMod.java']
actions='--actions' in sys.argv
if actions:sources.append(root/'examples/sonic-echoes/src/test/java/echoes/PromoActionCaptureMod.java')
subprocess.run([str(java/'javac'),'--release','25','-cp',cp,'-d',str(classes),*map(str,sources)],check=True)
shutil.copytree(root/'examples/sonic-echoes/src/main/resources',classes,dirs_exist_ok=True)
p=classes/'META-INF/openggf-mod.yaml';p.write_text(p.read_text().replace('entrypoint: echoes.EchoesMod','entrypoint: echoes.PromoActionCaptureMod' if actions else 'entrypoint: echoes.PromoCaptureMod'))
jar=out/('promo-actions.jar' if actions else 'promo-capture.jar')
with zipfile.ZipFile(jar,'w',zipfile.ZIP_DEFLATED) as z:
 for p in classes.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(classes))
print(jar)
