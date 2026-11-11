"""Purpose: contact sheet of a capture with frame numbers (and optional state columns).
Usage: sheet.py CAPDIR first last step [out.jpg]. Origin: MT production promo 2026-11-11."""
import sys,csv
from pathlib import Path
from PIL import Image,ImageDraw
d=Path(sys.argv[1]);a,b,st=map(int,sys.argv[2:5]);out=sys.argv[5] if len(sys.argv)>5 else str(d/'sheet.jpg')
fr=sorted((d/'frames').glob('*.png'));rows=list(csv.DictReader(open(d/'state.csv'))) if (d/'state.csv').exists() else []
idx=list(range(a,min(b,len(fr)),st));cols=6;W,H=320,224
S=Image.new('RGB',(cols*W,((len(idx)+cols-1)//cols)*(H+14)),(10,10,30));D=ImageDraw.Draw(S)
for k,i in enumerate(idx):
  x=k%cols*W;y=k//cols*(H+14);S.paste(Image.open(fr[i]).convert('RGB'),(x,y))
  r=rows[i] if i<len(rows) else {}
  D.text((x+2,y+H+1),f"{i} x{r.get('x','')} y{r.get('y','')} a{r.get('air','')} rg{r.get('rings','')} sc{r.get('score','')} {r.get('mode','')}",fill='white')
S.save(out,quality=85);print(out,len(idx))
