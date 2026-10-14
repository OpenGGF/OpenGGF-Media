from pathlib import Path
import subprocess,os,sys
p=Path('target/ownership-probe').resolve();cp=(p/'classpath.txt').read_text()
out,inputfile,prefix,candidates=sys.argv[1:]
cmd=['/usr/lib/jvm/java-21-openjdk/bin/java','-Xmx1g',*(['-Dsoz.knuckles.boss=true'] if os.environ.get('SOZ_AUTHOR_BOSS') else []),'-javaagent:/home/farrell/.m2/repository/org/mockito/mockito-core/5.14.2/mockito-core-5.14.2.jar','-Djava.io.tmpdir='+str(p/'tmp'),'-Ds3k.rom.path=/home/farrell/code/projects/OpenGGF/s3k.gen','-Dsoz.knuckles.author='+out,'-Dsoz.knuckles.input='+inputfile,'-Dsoz.knuckles.prefix='+prefix,'-Dsoz.knuckles.candidates='+candidates,'-jar','/home/farrell/.m2/repository/org/junit/platform/junit-platform-console-standalone/1.10.3/junit-platform-console-standalone-1.10.3.jar','execute','--class-path',str(p/'classes')+':'+cp,'--select-class','com.openggf.tools.TestSozKnucklesAuthor','--disable-ansi-colors']
logfile=p/(Path(out).name+'.log')
with logfile.open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'DISPLAY':':0'})
print('exit',r.returncode)
if r.returncode:print('\n'.join(logfile.read_text().splitlines()[-40:]))
else:
 import csv
 for f in sorted(Path(out).glob('variant-*.csv')):
  if 'contacts' in f.name or 'mechanism' in f.name:continue
  rows=list(csv.DictReader(f.open()))
  if rows:print(f.name,rows[-1])
