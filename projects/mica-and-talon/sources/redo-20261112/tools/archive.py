#!/usr/bin/env python3
"""Purpose: archive the 2026-11-12 MICA & TALON promo redo into an OpenGGF-Media checkout: copy production text
(edit, tools, hosts, capture batches and per-take provenance, checkpoints' text, beat track, README), catalogue
external assets (videos, review pages, frame sequences, state CSVs, ROM-derived SFX, the bed, the owner's music
by name and hash, fonts) with SHA-256, and update the catalogue and README indexes. Never copies the owner's music,
the bed, ROM-derived audio, glyph tables, frames or video. No push.
Inputs: --media <checkout of a branch made from feature/ai-mt-promo-production>.
Origin: tools/archive.py of the 2026-11-11 production promo, adapted for the redo."""
import argparse, csv, hashlib, json, re, shutil
from pathlib import Path

T = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument('--media', type=Path, required=True); a = ap.parse_args()
A = a.media.resolve(); proj = 'mica-and-talon'; label = 'redo-20261112'
D = A / 'projects' / proj; dest = D / 'sources' / label
roots = json.loads((A / 'catalog/roots.json').read_text())
sources = json.loads((A / 'catalog/sources.json').read_text())
projects = json.loads((A / 'catalog/projects.json').read_text())
rid = f'{proj}/{label}'
assert not any(r['id'] == rid for r in roots), 'already archived on this branch'
roots.append(dict(id=rid, original=str(T), archive=str(dest.relative_to(A))))

TEXT = {'.py', '.java', '.md', '.json', '.csv', '.txt', '.script'}
SKIP_DIRS = {'work', 'sfx', 'logs', 'final', '__pycache__'}
WORK_KEEP = ('beat-track.json', 'music-bars.json', 'music-sections.json', 'chapters.ffmeta')   # the edit reads the beat track
EXTERNAL_TEXT = {'s2-title-font.txt'}        # glyph table extracted from the ROM: by hash only
CAPTURE_KEEP = ('provenance.json', 'input.script', 'input.txt', 'slots.json', 'observations.json')
copied = []


def keep(f, rel):
    out = dest / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, out)
    b = out.read_bytes()
    sources.append(dict(path=str(out.relative_to(A)), root=rid, original_path=str(rel), bytes=len(b),
                        sha256=hashlib.sha256(b).hexdigest(), snapshot='byte-copy'))
    copied.append(rel)


for f in sorted(T.rglob('*')):
    rel = f.relative_to(T)
    if f.is_symlink() or not f.is_file() or rel.parts[0] in SKIP_DIRS or '__pycache__' in rel.parts or 'saves' in rel.parts:
        continue
    if 'frames' in rel.parts or f.name == 'state.csv' or f.suffix not in TEXT or f.name in EXTERNAL_TEXT:
        continue
    if rel.parts[0] == 'captures' and f.name not in CAPTURE_KEEP:
        continue
    keep(f, rel)
for n in WORK_KEEP:
    keep(T / 'work' / n, Path('work') / n)

assets, hashes = [], []


def manifest(path, kind, root_id=rid, base=T, catalogue=True):
    files = sorted(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else [path]
    if not files:
        return
    dig = hashlib.sha256()
    for f in files:
        dig.update(str(f.relative_to(base)).encode() + b'\0' + hashlib.sha256(f.read_bytes()).digest())
    size = sum(f.stat().st_size for f in files)
    rel = str(path.relative_to(base))
    if catalogue:
        assets.append(dict(project=proj, root=root_id, path=rel, kind=kind, bytes=size, files=len(files)))
    hashes.append(dict(root=root_id, path=rel, kind=kind, files=len(files), bytes=size,
                       sha256=hashlib.sha256(files[0].read_bytes()).hexdigest() if len(files) == 1 else None,
                       sha256_manifest=dig.hexdigest()))


for f in sorted((T / 'out').glob('*.mp4')):
    manifest(f, 'finished promo video (H.264 High/AAC 320k)')
for f in sorted((T / 'out').glob('*.jpg')):
    manifest(f, 'contact sheet of the encoded master')
for f in sorted((T / 'final').glob('*')):
    manifest(f, 'final vertical review (self-contained HTML, or its 540 px video)')
for c in ('checkpoint1', 'checkpoint2', 'checkpoint3'):
    for f in sorted((T / c).iterdir()):
        if f.is_file() and f.suffix in ('.html', '.mp4', '.jpg', '.png'):
            manifest(f, f'superseded review package or render ({c})')
for d in sorted((T / 'captures').glob('*/frames')):
    manifest(d, 'native capture frame sequence (ROM-derived pixels; external)')
for f in sorted((T / 'captures').glob('*/state.csv')):
    manifest(f, 'measured native gameplay CSV (see provenance for entry kind)')
for f in sorted((T / 'sfx').glob('*.wav')):
    manifest(f, 'ROM-derived paced SFX PCM (FmSfxRenderTool --paced); external')
manifest(T / 'work/bed.wav', 'music bed PCM (owner-supplied track 0-123.4 s with one fade); external, not redistributable')
manifest(T / 'edit/s2-title-font.txt', 'S2 title-card glyph table extracted from the ROM (unused); external')
# the owner's music and the fonts are the same files the 2026-11-11 archive catalogued: reference, do not re-add
music = Path.home() / 'scratch/agent-tmp/mt-promo-final-20261111/music'
manifest(music / 'run-into-the-sunshine-chiptune.wav',
         'owner-supplied music "RUN INTO THE SUNSHINE (Chiptune Remix)"; name + hash only, never committed',
         f'{proj}/owner-music', music, catalogue=False)
fdir = Path.home() / 'scratch/agent-tmp/mt-promo-20261110/final/fonts'
for f in sorted(fdir.iterdir()):
    if f.is_file():
        manifest(f, 'third-party font dependency (PROMO_FONT_DIRS); external', f'{proj}/fonts-20261110', fdir, catalogue=False)
assert all(r in {x['id'] for x in roots} for r in {h['root'] for h in hashes})

(D / f'external-hashes-{label}.json').write_text(json.dumps(hashes, indent=2) + '\n')
idx = D / 'README.md'
s = idx.read_text()
S = f'sources/{label}'
head = f'''# MICA & TALON Mod Showcase

**Current: promo redo, 2026-11-12** (OpenGGF `1e0faac123`, 124.0 s, 16:9 and designed 9:16 cuts, the owner's music
from its start with one fade). Local archive only; not pushed. Sound checked by measurement only.

- [README: source, music decision, what is not filmed as it ships, the 9:16 cut, review history, rebuild]({S}/README.md)
- [Edit: brief, tracked bar grid and both cuts]({S}/edit/edit.py)
- [Shot index (every capture on screen: entry kind, declared setup, frames used, command)]({S}/out/shot-index.csv),
  [chapters]({S}/out/chapters.txt), [viewer pass]({S}/out/viewer-pass.md),
  [verification]({S}/out/verification.json), [check]({S}/out/promo_kit-check.txt),
  [stinger levels]({S}/out/stinger-levels.json)
- Edit as it stood at each review: [storyboard]({S}/checkpoint1/edit-at-storyboard.py),
  [draft]({S}/checkpoint2/edit-at-draft.py), [climax check]({S}/checkpoint3/edit-at-climax-check.py)
- [External hashes](external-hashes-{label}.json): videos, review pages, frames, state CSVs, PCM, fonts and the
  owner's music (name + SHA-256 only; the WAV is not in this repository).

## Superseded: production promo, 2026-11-11

Superseded by the redo after the owner's feedback (zoom at the start, spliced music, features not shown).
OpenGGF `b088fae95b`, 95.4 s, 16:9 and designed 9:16 cuts.
'''
old = s[:s.index('- [Production README')]
assert old.startswith('# MICA & TALON Mod Showcase') and 'Current: production promo, 2026-11-11' in old
s = s.replace(old, head + '\n', 1)
idx.write_text(s)
for p in projects:
    if p['id'] == proj:
        p['notes'] = 'Promo redo 2026-11-12 (current); superseded 2026-11-11 production promo and 2026-11-10 showcase; local, sound measured only'
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
m = re.search(r'(\d[\d,]*) preserved source files', t)
t = t.replace(m.group(0), f'{int(m.group(1).replace(",", "")) + len(copied):,} preserved source files', 1)
r.write_text(t)
print('archived', len(copied), 'source files;', len(assets), 'catalogue entries;', len(hashes), 'hashed externals')
