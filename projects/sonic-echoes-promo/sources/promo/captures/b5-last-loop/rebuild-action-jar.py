"""Build only Worker B action wrapper around existing Worker A observer jar."""
from pathlib import Path
import os,subprocess,zipfile
root=Path('/home/james/IdeaProjects/OpenGGF');out=Path(__file__).parent;classes=out/'action-classes';classes.mkdir(exist_ok=True)
with zipfile.ZipFile(out.parent/'a-helper-proof/promo-capture.jar') as z:z.extractall(classes)
cp=os.pathsep.join([str(root/'target/classes'),str(classes),(root/'target/examples-classpath.txt').read_text().strip()])
subprocess.run([os.environ['JAVA_HOME']+'/bin/javac','--release','25','-cp',cp,'-d',str(classes),str(root/'examples/sonic-echoes/src/test/java/echoes/PromoActionCaptureMod.java')],check=True)
f=classes/'META-INF/openggf-mod.yaml';f.write_text(f.read_text().replace('entrypoint: echoes.PromoCaptureMod','entrypoint: echoes.PromoActionCaptureMod'))
with zipfile.ZipFile(out/'promo-action-capture.jar','w',zipfile.ZIP_DEFLATED) as z:
 for f in classes.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(classes))
