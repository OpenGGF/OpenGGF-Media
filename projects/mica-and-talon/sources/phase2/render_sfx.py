from pathlib import Path
import subprocess,os,argparse
p=argparse.ArgumentParser();p.add_argument('--checkout',type=Path,required=True);a=p.parse_args();r=a.checkout.resolve();out=Path(__file__).parent/'music';cp=str(r/'target/classes')+':'+(r/'target/mica-classpath.txt').read_text().strip()
for sid in ['B3','33','34','B6']:
 with open(out/f'sfx-{sid}.log','w') as log:subprocess.run(['java','-Xmx512m','-cp',cp,'com.openggf.tools.audio.FmSfxRenderTool','--game','s3k','--rom',str(r/'s3k.gen'),'--sfx',sid,'--rate','48000','--max-seconds','3','--out',str(out),'--paced'],cwd=r,stdout=log,stderr=subprocess.STDOUT,check=True)
