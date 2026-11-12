"""Archive production text and catalog external assets; no upload or push."""
from pathlib import Path
import json,csv,hashlib,shutil,re
P=Path(__file__).resolve().parent;A=P/'media-archive';proj='mica-and-talon';D=A/'projects'/proj;D.mkdir(parents=True,exist_ok=True)
roots=json.loads((A/'catalog/roots.json').read_text());sources=json.loads((A/'catalog/sources.json').read_text());projects=json.loads((A/'catalog/projects.json').read_text())
assert not any(r['id'].startswith(proj+'/')for r in roots),'Run once against fresh archive branch'
assets=[];hashes=[]
def save_root(root,label):
 rid=proj+'/'+label;dest=D/'sources'/label;roots.append(dict(id=rid,original=str(root),archive=str(dest.relative_to(A))))
 wanted=[]
 for f in root.rglob('*'):
  rel=f.relative_to(root)
  if any(x in rel.parts for x in ['media-archive','venv','fonts','music','__pycache__','build-generated','saves','saves-title']):continue
  if f.is_symlink()or not f.is_file():continue
  if f.suffix not in ['.py','.java','.md','.json','.csv','.txt','.script','.ffmetadata']:continue
  if f.name=='state.csv' or 'assets'in rel.parts:continue
  if 'out'in rel.parts and f.suffix!='.json':continue
  if label=='phase2' and 'captures'in rel.parts and f.name not in ['provenance.json','input.script','input.txt','slots.json']:continue
  wanted.append(f)
 for f in wanted:
  rel=f.relative_to(root);out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out);b=out.read_bytes();sources.append(dict(path=str(out.relative_to(A)),root=rid,original_path=str(rel),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),snapshot='byte-copy'))
 # Aggregate each sequence/PCM as external; keep ROM-derived assets outside Git.
 groups=[]
 for d in root.glob('captures/*/*/frames'):
  if d.is_dir():groups.append((d,'native capture frame sequence'))
 for f in root.glob('captures/*/*/state.csv'):groups.append((f,'measured native gameplay CSV; see provenance for detached ending-loop limit'))
 for f in root.glob('out/master-*.mp4'):groups.append((f,'finished promo video'))
 for f in root.glob('out/*.jpg'):groups.append((f,'review contact/still image'))
 for d in root.glob('edit/*/sheet-0.png'):groups.append((d,'composition contact sheet'))
 for d,kind in groups:
  files=sorted(d.rglob('*'))if d.is_dir()else[d];files=[f for f in files if f.is_file()];size=sum(f.stat().st_size for f in files)
  if not files:continue
  path=str(d.relative_to(root));assets.append(dict(project=proj,root=rid,path=path,kind=kind,bytes=size,files=len(files)))
  digest=hashlib.sha256()
  for f in files:digest.update(str(f.relative_to(root)).encode()+b'\0'+hashlib.sha256(f.read_bytes()).digest())
  hashes.append(dict(root=rid,path=path,files=len(files),bytes=size,sha256_manifest=digest.hexdigest(),algorithm='sha256(concat(relative_path UTF8, NUL, sha256(file bytes))) sorted paths'))
 return len(wanted)
count=save_root(P,'final')+save_root(P.parent/'phase2','phase2')
# External music, fonts and art inputs used by both revisions.
for label,root,kind in [('music',(P/'music').resolve(),'ROM-derived paced PCM; external'),('fonts',(P/'fonts').resolve(),'third-party font dependency; external'),('drawing',Path.home()/'scratch/agent-tmp/mica-regen-20261108/attempts','original redraw reference; external')]:
 rid=proj+'/'+label;roots.append(dict(id=rid,original=str(root),archive='projects/mica-and-talon/sources/final'))
 for f in root.iterdir():
  if not f.is_file():continue
  if label=='drawing' and f.name!='wait-00-2.png':continue
  assets.append(dict(project=proj,root=rid,path=f.name,kind=kind,bytes=f.stat().st_size,files=1));hashes.append(dict(root=rid,path=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
(D/'external-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
(D/'README.md').write_text('''# MICA & TALON Mod Showcase

Final pass recorded against engine a64655fe97 on 2026-11-10. Local archive for lead publication after user review; no upload or push. The carry shot uses the carry fix (integration b8c105a986), captured by the lead after the final lane stopped; see the review history. Team footage makes no carry claim.

- [Final brief, review history, qualifications and rebuild instructions](sources/final/README.md)
- [Editable brief/beat sheet/compositor](sources/final/edit/edit.py)
- [Selected source intervals](sources/final/selected-shots.csv), [capture inventory](sources/final/shot-list.csv), [chapter map](sources/final/chapters.json)
- [Viewer pass](sources/final/viewer-pass.md), [encoded verification](sources/final/verification.json)
- [Retained phase-2 handoff](sources/phase2/handoff.md) — superseded picture; retained methods and review context.
- [External hashes](external-hashes.json) and repository catalog locate large recordings, lossless frames, PCM and other dependencies. They remain local external files, not GitHub downloads.

No stock Sonic/Tails art in selected final footage. ROMs, extracted glyphs/audio, videos, frame sequences, bulk state, build jars and installed environments are excluded from this commit. Obtain your own ROMs. OpenGGF-derived source retains GPL-3.0; this archive grants no rights to Sega assets or third-party dependencies. Sound checked by measurement only.
''')
# Review directions copied verbatim as retained production feedback.
for name in ['promo-direction.md','promo-review-phase2.md']:
 src=P.parent.parent/'mt-wave-20261110'/name;shutil.copy2(src,D/name)
projects.append(dict(id=proj,title='MICA & TALON example mod showcase',notes='Final local review cut; sound measured only',source_files=count,catalog_entries=len(assets)))
(A/'catalog/projects.json').write_text(json.dumps(projects,indent=2)+'\n');(A/'catalog/roots.json').write_text(json.dumps(roots,indent=2)+'\n');(A/'catalog/sources.json').write_text(json.dumps(sources,indent=2)+'\n')
with (A/'catalog/assets.csv').open('a',newline='')as f:csv.DictWriter(f,fieldnames=['project','root','path','kind','bytes','files']).writerows(assets)
p=A/'README.md';s=p.read_text();s=s.replace('| Production | Sources | External asset/sequence entries |','| Production | Sources | External asset/sequence entries |').replace('| --- | ---: | ---: |','| --- | ---: | ---: |\n'+f'| [MICA & TALON example mod showcase](projects/mica-and-talon/) | {count} | {len(assets)} |',1);s=s.replace('**33 production groups · 7,815 preserved source files','**34 production groups · '+f'{7815+count:,} preserved source files');p.write_text(s)
print('Archived',count,'source files;',len(assets),'external catalog entries')
