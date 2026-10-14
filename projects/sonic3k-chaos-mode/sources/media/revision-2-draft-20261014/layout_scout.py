#!/usr/bin/env python3
"""Small PNG/Pillow layout scouts, not final EDL/gameplay qualification.

Uses already captured new PNGs as temporary stand-ins for reused masters whose
PNG sequences were consumed. No engine/encoder/decoder jobs. Writes representative
1920x1080 layout frames and a contact sheet under revision2/previews only.
"""
from pathlib import Path
from copy import deepcopy
import json

from PIL import Image,ImageDraw
import assemble as a

P=Path(__file__).resolve().parent


def replacement(panel,name,start=600):
    out=deepcopy(panel)
    out.update(name=name,source=str(P/"captures"/name/"source.mkv"),source_start_frame=start,
               qualified=False,effect=a.EFFECTS.get(name))
    return out


def main():
    plan=a.normalized_plan();out=P/"previews";out.mkdir(exist_ok=True)
    chosen=[]
    # Every shot is explicitly a layout prototype; these replacements never enter
    # the final EDL or source-selections lock.
    shot=deepcopy(plan[8]);shot["panels"]=[replacement(shot["panels"][0],"blueprint"),replacement(shot["panels"][1],"rainbow")]
    chosen.append(("slice-2",shot,25))
    shot=deepcopy(plan[11]);chosen.append(("pair",shot,64))
    shot=deepcopy(plan[15]);shot["panels"]=[replacement(p,n) for p,n in zip(shot["panels"],["rainbow","giant","hudshuffle"])]
    chosen.append(("triple",shot,70))
    shot=deepcopy(plan[12]);shot["panels"][0]=replacement(shot["panels"][0],"hudorbit",585)
    for tick in [0,84,86,89,110,150]:chosen.append((f"shrink-{tick}",deepcopy(shot),tick))
    shot=deepcopy(plan[22]);shot["panels"][0]=replacement(shot["panels"][0],"blueprint")
    chosen.append(("quad",shot,180))
    shot=deepcopy(plan[42]);shot["panels"]=[replacement(p,n,780) for p,n in zip(shot["panels"],["rainbow","blueprint","tiny","spinning"])]
    chosen.append(("slice-4",shot,155))
    chosen.append(("critics",deepcopy(plan[31]),40))
    chosen.append(("end",deepcopy(plan[43]),90))
    sheet=Image.new("RGB",(1920,((len(chosen)+1)//2)*570),a.NAVY);d=ImageDraw.Draw(sheet)
    metadata=[]
    for i,(name,shot,tick) in enumerate(chosen):
        renderer=a.ShotRenderer(shot,True,prefer_png=True)
        try:image=renderer.frame(tick)
        finally:renderer.close()
        file=out/f"layout-{name}.png";image.save(file)
        x=(i%2)*960;y=(i//2)*570
        sheet.paste(image.resize((960,540),Image.Resampling.BOX),(x,y))
        d.text((x+10,y+550),f"LAYOUT PROTOTYPE — {name.upper()} / source stand-ins, not final shot proof",fill=a.GOLD)
        metadata.append(dict(name=name,tick=tick,file=str(file.relative_to(P)),panels=[p["name"] for p in shot["panels"]],final_selection=False))
    sheet.save(out/"layout-contact-sheet.png")
    (out/"layout-scouts.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(f"{len(chosen)} PNG layout prototypes; no video encoding.")


if __name__=="__main__":main()
