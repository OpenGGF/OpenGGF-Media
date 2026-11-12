"""Purpose: render ROM SFX stingers through OpenGGF's SMPS driver, paced (FmSfxRenderTool --paced), one JVM at a time.
Inputs: checkout with built classes + verified ROMs. Origin: MT production promo 2026-11-11; redo list 2026-11-12."""
import subprocess,sys
from pathlib import Path
R=Path(sys.argv[1]).resolve();out=Path(__file__).resolve().parent.parent/'sfx';out.mkdir(exist_ok=True)
cp=str(R/'target/classes')+':'+(R/'target/mica-classpath.txt').read_text().strip()
for game,sid in [('s3k','B3'),('s3k','B4'),('s3k','9F'),('s3k','6E'),('s3k','B8'),('s3k','4A'),('s2','CF'),('s2','C1'),('s2','DF'),('s1','C1'),('s1','CF')]:
  with open(out/f'{game}-{sid}.log','w') as log:
    r=subprocess.run(['java','-Xmx512m','-cp',cp,'com.openggf.tools.audio.FmSfxRenderTool','--game',game,'--rom',str(R/f'{game}.gen'),'--sfx',sid,'--rate','48000','--max-seconds','3','--out',str(out),'--paced'],cwd=R,stdout=log,stderr=subprocess.STDOUT)
    print(game,sid,r.returncode,flush=True)
print(sorted(p.name for p in out.glob('*.wav')))
