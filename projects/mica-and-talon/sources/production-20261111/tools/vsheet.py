"""Purpose: aspect-correct contact sheet of a promo_kit edit (works for 9:16), frames rendered in a pool.
Usage: MT_VERTICAL=1 vsheet.py EDIT step out.jpg [first last]. Origin: MT production promo 2026-11-11."""
import sys,os
sys.path.insert(0,'/mnt/LinuxData/T3/worktrees/OpenGGF/t3-3c245e9e/tools/media')
import promo_kit as pk
sys.modules['promo_kit']=pk
from PIL import Image,ImageDraw
import multiprocessing as mp
E=sys.argv[1];step=int(sys.argv[2]);out=sys.argv[3]
e=pk.load_edit(E);first=int(sys.argv[4]) if len(sys.argv)>4 else 0;last=int(sys.argv[5]) if len(sys.argv)>5 else e.end()
fs=list(range(first,last,step))
def r(f):
  im=Image.fromarray(e.render_frame(f));im.thumbnail((270,270) if e.H>e.W else (384,216));return im
with mp.get_context('fork').Pool(8) as p:ims=p.map(r,fs)
w,h=ims[0].size;cols=10 if e.H>e.W else 6
S=Image.new('RGB',(cols*w,((len(ims)+cols-1)//cols)*h))
for k,(f,im) in enumerate(zip(fs,ims)):
  ImageDraw.Draw(im).text((3,2),f'{f/60:.1f}',fill='yellow');S.paste(im,(k%cols*w,k//cols*h))
S.save(out,quality=82);print(out,len(fs))
