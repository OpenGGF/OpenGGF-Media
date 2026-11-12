"""Contact sheets sampled from actual final encoded files at 4-second intervals."""
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).parent
for aspect in ['16x9','9x16']:
 folder=P/'out'/f'encoded-{aspect}';folder.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/f'out/master-{aspect}.mp4'),'-vf','fps=1/4','-frames:v','22',str(folder/'%02d.png')],check=True)
 w,h=(384,216)if aspect=='16x9'else(216,384);files=sorted(folder.glob('*.png'));o=Image.new('RGB',(w*5,(h+26)*5),(8,16,56));d=ImageDraw.Draw(o)
 for k,f in enumerate(files):
  im=Image.open(f);im.thumbnail((w,h));x=k%5*w;y=k//5*(h+26);o.paste(im,(x,y));d.text((x+8,y+h+4),f'{k*4:02d}s',fill='white')
 o.save(P/f'out/contact-{aspect}.jpg',quality=94)
