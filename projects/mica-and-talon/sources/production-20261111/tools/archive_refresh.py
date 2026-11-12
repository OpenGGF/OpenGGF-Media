"""Purpose: refresh an existing production-20261111 archive snapshot after a revision: re-copy changed/new
production text, refresh sources.json hashes, append new external assets. No push.
Inputs: --media <OpenGGF-Media checkout>. Origin: MT production promo 2026-11-11 (9:16 band fix)."""
import argparse, csv, hashlib, json, shutil
from pathlib import Path
T = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument('--media', type=Path, required=True); a = ap.parse_args()
A = a.media.resolve(); proj = 'mica-and-talon'; rid = f'{proj}/production-20261111'
D = A / 'projects' / proj; dest = D / 'sources/production-20261111'
sources = json.loads((A / 'catalog/sources.json').read_text())
byp = {s['path']: s for s in sources}
TEXT = {'.py', '.java', '.md', '.json', '.csv', '.txt', '.script'}
SKIP = {'work', 'music', 'sfx', 'probes', '__pycache__', 'saves'}
changed = added = 0
for f in sorted(T.rglob('*')):
    rel = f.relative_to(T)
    if f.is_symlink() or not f.is_file() or rel.parts[0] in SKIP or 'saves' in rel.parts or '__pycache__' in rel.parts:
        continue
    if 'frames' in rel.parts or f.name == 'state.csv' or f.suffix not in TEXT or f.name == 's2-title-font.txt':
        continue
    if rel.parts[0] == 'captures' and f.name not in ('provenance.json', 'input.script', 'input.txt', 'slots.json', 'observations.json'):
        continue
    out = dest / rel; key = str(out.relative_to(A)); b = f.read_bytes()
    if out.exists() and out.read_bytes() == b:
        continue
    out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, out)
    e = dict(path=key, root=rid, original_path=str(rel), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), snapshot='byte-copy')
    if key in byp: byp[key].update(e); changed += 1
    else: sources.append(e); added += 1
(A / 'catalog/sources.json').write_text(json.dumps(sources, indent=2) + '\n')
hp = D / 'external-hashes-production-20261111.json'; hashes = json.loads(hp.read_text())
assets = []
for f in [T / 'out/master-9x16.mp4', T / 'out/master-16x9-s1fix.mp4', T / 'out/contact-9x16-2fps.jpg', T / 'out/contact-16x9-s1fix-2fps.jpg']:
    rel = str(f.relative_to(T)); h = hashlib.sha256(f.read_bytes()).hexdigest()
    kind = 'finished promo video (H.264 High/AAC 320k)' if f.suffix == '.mp4' else 'review contact sheet / key frame'
    old = [x for x in hashes if x['path'] == rel]
    if old:
        old[0].update(bytes=f.stat().st_size, sha256=h, sha256_manifest=None, revision='2026-11-11 9:16 band fix')
    else:
        hashes.append(dict(root=rid, path=rel, files=1, bytes=f.stat().st_size, sha256=h))
        assets.append(dict(project=proj, root=rid, path=rel, kind=kind, bytes=f.stat().st_size, files=1))
hp.write_text(json.dumps(hashes, indent=2) + '\n')
if assets:
    with (A / 'catalog/assets.csv').open('a', newline='') as fh:
        csv.DictWriter(fh, fieldnames=['project', 'root', 'path', 'kind', 'bytes', 'files']).writerows(assets)
# keep catalog byte counts for re-rendered assets current
rows = list(csv.DictReader((A / 'catalog/assets.csv').open()))
for r in rows:
    if r['root'] == rid and r['path'] in ('out/master-9x16.mp4', 'out/contact-9x16-2fps.jpg'):
        r['bytes'] = str((T / r['path']).stat().st_size)
with (A / 'catalog/assets.csv').open('w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['project', 'root', 'path', 'kind', 'bytes', 'files']); w.writeheader(); w.writerows(rows)
projects = json.loads((A / 'catalog/projects.json').read_text())
for p in projects:
    if p['id'] == proj:
        p['source_files'] += added; p['catalog_entries'] += len(assets)
(A / 'catalog/projects.json').write_text(json.dumps(projects, indent=2) + '\n')
r = A / 'README.md'; t = r.read_text()
row = next(l for l in t.splitlines() if l.startswith('| [MICA & TALON'))
n_src, n_ast = [int(x.strip().replace(',', '')) for x in row.split('|')[2:4]]
t = t.replace(row, f'| [MICA & TALON example mod showcase](projects/mica-and-talon/) | {n_src + added:,} | {n_ast + len(assets):,} |')
import re
m = re.search(r'(\d[\d,]*) preserved source files', t)
t = t.replace(m.group(0), f'{int(m.group(1).replace(",", "")) + added:,} preserved source files', 1); r.write_text(t)
print('changed', changed, 'added', added, 'new assets', len(assets))
