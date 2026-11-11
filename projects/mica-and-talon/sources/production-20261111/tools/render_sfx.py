"""Purpose: render ROM SFX stingers through OpenGGF's SMPS driver, paced (FmSfxRenderTool --paced).
Inputs: checkout with built classes + verified ROMs. Origin: MT production promo 2026-11-11."""
import subprocess,sys
from pathlib import Path
R=Path(sys.argv[1]).resolve();out=Path(__file__).resolve().parent.parent/'sfx';out.mkdir(exist_ok=True)
cp=str(R/'target/classes')+':'+(R/'target/mica-classpath.txt').read_text().strip()
for game,sid in [('s3k','B3'),('s3k','B4'),('s3k','9F'),('s3k','B8'),('s2','CF'),('s2','C1'),('s2','DF'),('s2','CA')]:
  with open(out/f'{game}-{sid}.log','w') as log:
    subprocess.run(['java','-Xmx512m','-cp',cp,'com.openggf.tools.audio.FmSfxRenderTool','--game',game,'--rom',str(R/f'{game}.gen'),'--sfx',sid,'--rate','48000','--max-seconds','3','--out',str(out),'--paced'],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
print(sorted(p.name for p in out.glob('*.wav')))
