import os,sys
from pathlib import Path
from PIL import Image
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-bf758747');sys.path.insert(0,str(R/'tools/media'));os.environ.update(MT_CHECKOUT=str(R),MT_TAKE='final',PROMO_FONT_DIRS=str(P/'fonts'))
from promo_kit import load_edit
for v in ['0','1']:
 os.environ['MT_VERTICAL']=v;e=load_edit(P/'edit/edit.py')
 for t in [24,32,36,40,52]:Image.fromarray(e.render_frame(t*60)).save(P/f'out/review-{v}-{t}.jpg')
