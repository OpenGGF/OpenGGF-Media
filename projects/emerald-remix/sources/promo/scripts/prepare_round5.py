#!/usr/bin/env python3
"""Build editorial whole-zone landscape from the actual pixel function. Emerald Remix promo r5, 2026-10-22.
Inputs: generator source only. Outputs: original pixel layers and scenic/whole-map art outside repository.
This is an explanatory drawing, not engine footage or an editor screen.
"""
from pathlib import Path
import importlib.util
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];D=P/'design/round5';D.mkdir(exist_ok=True)
R=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
spec=importlib.util.spec_from_file_location('cv',R/'examples/emerald-remix/tools/generate_clover_valley.py');cv=importlib.util.module_from_spec(spec);spec.loader.exec_module(cv)
cells,surface=cv.build_cells();fg,bg=cv.render(cells,surface)
f=np.array(fg,dtype=np.uint8);pal=np.array([cv.rgb(w) for w in cv.LINE2],dtype=np.uint8)
Image.fromarray(np.dstack((pal[f],(f!=0).astype(np.uint8)*255))).save(D/'whole-foreground.png')
# Scenic diagram: the same world foreground over the same background function, framed to show the route.
b=np.array([[cv.rgb(cv.LINE3[cv.bg_pixel(x,y//2)]) for x in range(512)] for y in range(512)],dtype=np.uint8)
b=np.tile(b,(1,10,1));front=f[256:768];scene=b.copy();mask=front!=0;scene[mask]=pal[front[mask]]
Image.fromarray(scene).save(D/'whole-landscape.png')
Image.fromarray(b[:,1536:2816]).save(D/'scene-background.png')
Image.fromarray(np.dstack((pal[front[:,1536:2816]],(front[:,1536:2816]!=0).astype(np.uint8)*255))).save(D/'scene-foreground.png')
print('actual pixel function -> 5120x512 landscape, 1280x512 scenic layers',D)
