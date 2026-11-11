#!/usr/bin/env python3
"""Purpose: archive the 2026-11-11 MICA & TALON production promo into an OpenGGF-Media checkout: copy production
text (edit, tools, hosts, capture recipes/provenance, checkpoints, README), catalogue external assets (videos,
frame sequences, state CSVs, ROM-derived SFX/bed PCM, owner music by name+hash, fonts) with SHA-256, and update
the catalog/README indexes. Never copies the owner's music WAV, ROM-derived audio or frames. No push.
Inputs: --media <checkout of feature/ai-mt-promo-production>. Origin: MT production promo 2026-11-11."""
import argparse, csv, hashlib, json, shutil
from pathlib import Path

T = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument('--media', type=Path, required=True); a = ap.parse_args()
A = a.media.resolve(); proj = 'mica-and-talon'; label = 'production-20261111'
D = A / 'projects' / proj; dest = D / 'sources' / label
roots = json.loads((A / 'catalog/roots.json').read_text())
sources = json.loads((A / 'catalog/sources.json').read_text())
projects = json.loads((A / 'catalog/projects.json').read_text())
rid = f'{proj}/{label}'
assert not any(r['id'] == rid for r in roots), 'already archived on this branch'
roots.append(dict(id=rid, original=str(T), archive=str(dest.relative_to(A))))

TEXT = {'.py', '.java', '.md', '.json', '.csv', '.txt', '.script'}
SKIP_DIRS = {'work', 'music', 'sfx', 'probes', '__pycache__', 'saves'}
copied = []
for f in sorted(T.rglob('*')):
    rel = f.relative_to(T)
    if f.is_symlink() or not f.is_file() or rel.parts[0] in SKIP_DIRS or 'saves' in rel.parts:
        continue
    if 'frames' in rel.parts or f.name in ('state.csv',) or f.suffix not in TEXT:
        continue
    if rel.parts[0] == 'captures' and f.name not in ('provenance.json', 'input.script', 'input.txt', 'slots.json',
                                                      'observations.json'):
        continue
    out = dest / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, out)
    b = out.read_bytes()
    sources.append(dict(path=str(out.relative_to(A)), root=rid, original_path=str(rel), bytes=len(b),
                        sha256=hashlib.sha256(b).hexdigest(), snapshot='byte-copy'))
    copied.append(rel)
# the shared S2 card glyph table was extracted from the ROM: keep it external
for c in list(copied):
    if c.name == 's2-title-font.txt':
        (dest / c).unlink(); copied.remove(c)
        sources[:] = [s for s in sources if s['path'] != str((dest / c).relative_to(A))]

assets, hashes = [], []


def manifest(path, kind, root_id=rid, base=T):
    files = sorted(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else [path]
    if not files:
        return
    dig = hashlib.sha256()
    for f in files:
        dig.update(str(f.relative_to(base)).encode() + b'\0' + hashlib.sha256(f.read_bytes()).digest())
    size = sum(f.stat().st_size for f in files)
    rel = str(path.relative_to(base))
    assets.append(dict(project=proj, root=root_id, path=rel, kind=kind, bytes=size, files=len(files)))
    hashes.append(dict(root=root_id, path=rel, files=len(files), bytes=size,
                       sha256=hashlib.sha256(files[0].read_bytes()).hexdigest() if len(files) == 1 else None,
                       sha256_manifest=dig.hexdigest()))


for f in sorted((T / 'out').glob('*.mp4')):
    manifest(f, 'finished promo video (H.264 High/AAC 320k)')
for f in sorted((T / 'out').glob('*.jpg')) + sorted((T / 'checkpoint1').glob('*.png')) + \
        sorted((T / 'checkpoint2').glob('*.jpg')):
    manifest(f, 'review contact sheet / key frame')
for f in sorted((T / 'checkpoint2').glob('*.mp4')):
    manifest(f, 'superseded draft render (checkpoint 2)')
for d in sorted((T / 'captures').glob('*/frames')):
    manifest(d, 'native capture frame sequence (ROM-derived pixels; external)')
for f in sorted((T / 'captures').glob('*/state.csv')):
    manifest(f, 'measured native gameplay CSV (see provenance for entry kind)')
for f in sorted((T / 'sfx').glob('*.wav')):
    manifest(f, 'ROM-derived paced SFX PCM (FmSfxRenderTool --paced); external')
manifest(T / 'work/bed.wav', 'edited music bed PCM (owner-supplied track, spliced); external, not redistributable')
manifest(T / 'edit/s2-title-font.txt', 'S2 title-card glyph table extracted from the ROM (unused in final); external')
mroot = f'{proj}/owner-music'
roots.append(dict(id=mroot, original=str(T / 'music'), archive=str(dest.relative_to(A))))
manifest(T / 'music/run-into-the-sunshine-chiptune.wav',
         'owner-supplied music "RUN INTO THE SUNSHINE (Chiptune Remix)"; reference by name+hash only, never committed',
         mroot, T / 'music')
froot = f'{proj}/fonts-20261110'
fdir = Path.home() / 'scratch/agent-tmp/mt-promo-20261110/final/fonts'
for f in sorted(fdir.iterdir()):
    if f.is_file():
        manifest(f, 'third-party font dependency (PROMO_FONT_DIRS); external', froot, fdir)

(D / 'external-hashes-production-20261111.json').write_text(json.dumps(hashes, indent=2) + '\n')
idx = D / 'README.md'
s = idx.read_text()
head = '''# MICA & TALON Mod Showcase

**Current: production promo, 2026-11-11** (OpenGGF `b088fae95b`, 95.4 s, 16:9 and designed 9:16 cuts, owner-supplied
music). Local archive only; not pushed. Sound checked by measurement only.

- [Production README: sources, music edit, disclosures, known limits, rebuild, review history](sources/production-20261111/README.md)
- [Edit: brief, beat sheet and compositor](sources/production-20261111/edit/edit.py)
- [Shot index (every capture: entry kind, declared setup, command)](sources/production-20261111/out/shot-index.csv),
  [chapters](sources/production-20261111/out/chapters.txt), [viewer pass](sources/production-20261111/out/viewer-pass.md),
  [verification](sources/production-20261111/out/verification.json), [check](sources/production-20261111/out/promo_kit-check.txt),
  [stinger levels](sources/production-20261111/out/stinger-levels.txt)
- Checkpoints with lead reviews: [storyboard](sources/production-20261111/checkpoint1/STORYBOARD.md),
  [draft](sources/production-20261111/checkpoint2/CHECKPOINT2.md)
- [External hashes](external-hashes-production-20261111.json): videos, frames, state CSVs, PCM, fonts and the owner's
  music (name + SHA-256 only; the WAV is not in this repository).

## Superseded: 2026-11-10 showcase ("a very rough cut" per the owner)

'''
s = s.replace('# MICA & TALON Mod Showcase\n\n', head, 1)
idx.write_text(s)
for p in projects:
    if p['id'] == proj:
        p['notes'] = 'Production promo 2026-11-11 (current) and superseded 2026-11-10 showcase; local, sound measured only'
        p['source_files'] = p.get('source_files', 0) + len(copied)
        p['catalog_entries'] = p.get('catalog_entries', 0) + len(assets)
(A / 'catalog/projects.json').write_text(json.dumps(projects, indent=2) + '\n')
(A / 'catalog/roots.json').write_text(json.dumps(roots, indent=2) + '\n')
(A / 'catalog/sources.json').write_text(json.dumps(sources, indent=2) + '\n')
with (A / 'catalog/assets.csv').open('a', newline='') as f:
    csv.DictWriter(f, fieldnames=['project', 'root', 'path', 'kind', 'bytes', 'files']).writerows(assets)
r = A / 'README.md'; t = r.read_text()
old_row = next(l for l in t.splitlines() if l.startswith('| [MICA & TALON'))
n_src, n_ast = [int(x.strip().replace(',', '')) for x in old_row.split('|')[2:4]]
t = t.replace(old_row, f'| [MICA & TALON example mod showcase](projects/mica-and-talon/) | {n_src + len(copied):,} | {n_ast + len(assets):,} |')
import re
m = re.search(r'(\d[\d,]*) preserved source files', t)
t = t.replace(m.group(0), f'{int(m.group(1).replace(",", "")) + len(copied):,} preserved source files', 1)
r.write_text(t)
print('archived', len(copied), 'source files;', len(assets), 'external entries')
