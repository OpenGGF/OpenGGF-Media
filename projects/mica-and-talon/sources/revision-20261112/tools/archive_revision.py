#!/usr/bin/env python3
"""Purpose: archive the pacing revision of the MICA & TALON promo into the local OpenGGF-Media checkout, on top of
the delivered cut's archive (root mica-and-talon/redo-20261112): copy production text (README, edit, tools,
capture hosts, shot lists, per-take provenance and inputs, checkpoint data, out/ text), catalogue external files
by SHA-256 (masters, contact sheets, review pages, frame sequences, state CSVs, the takes' SFX-only audio, the
bed, the mascot cut-outs, fonts, the owner's music by name and hash), and update the indexes.
Never copies: the owner's music, the bed, any take audio (ROM-derived), frames, video, images. No push.
The delivered cut's takes moved from captures/ to captures-old-art-1e0faac123/ when the final takes were shot;
the note written here says so, and their hashes are unchanged.
Inputs: --media <worktree on feature/ai-mt-promo-redo>, --label (default revision-20261112).
Origin: tools/archive.py of the delivered cut, 2026-11-12."""
import argparse, csv, hashlib, json, re, shutil
from pathlib import Path

T = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument('--media', type=Path, required=True)
ap.add_argument('--label', default='revision-20261112')
a = ap.parse_args()
A = a.media.resolve(); proj = 'mica-and-talon'; label = a.label
D = A / 'projects' / proj; dest = D / 'sources' / label
roots = json.loads((A / 'catalog/roots.json').read_text())
sources = json.loads((A / 'catalog/sources.json').read_text())
projects = json.loads((A / 'catalog/projects.json').read_text())
rid = f'{proj}/{label}'
assert not any(r['id'] == rid for r in roots), 'already archived on this branch'
OLD_TAKES = 'captures-old-art-1e0faac123'
for r in roots:                                # the delivered cut's root: say where its takes are now
    if r['id'] == f'{proj}/redo-20261112' and (T / OLD_TAKES).is_dir():
        r['note'] = (f'captures/ of this root was renamed {OLD_TAKES}/ when the pacing revision was shot; every path under '
                     f'captures/ in assets.csv and external-hashes-redo-20261112.json resolves under {OLD_TAKES}/ (same files, same hashes)')
roots.append(dict(id=rid, original=str(T), archive=str(dest.relative_to(A))))

TEXT = {'.py', '.java', '.md', '.json', '.csv', '.txt', '.script', '.sh'}
KEEP_DIRS = {'edit', 'tools', 'hosts', 'shots-b', 'captures', 'checkpoint4', 'checkpoint5', 'checkpoint6', 'out'}
WORK_KEEP = ('beat-track.json', 'music-bars.json', 'music-sections.json', 'chapters.ffmeta')
EXTERNAL_TEXT = {'s2-title-font.txt'}
CAPTURE_KEEP = ('provenance.json', 'input.script', 'input.txt', 'slots.json', 'observations.json')
copied = []


def keep(f, rel):
    out = dest / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, out)
    b = out.read_bytes()
    sources.append(dict(path=str(out.relative_to(A)), root=rid, original_path=str(rel), bytes=len(b),
                        sha256=hashlib.sha256(b).hexdigest(), snapshot='byte-copy'))
    copied.append(rel)


keep(T / 'README.md', Path('README.md'))
for f in sorted(T.rglob('*')):
    rel = f.relative_to(T)
    if f.is_symlink() or not f.is_file() or rel.parts[0] not in KEEP_DIRS or '__pycache__' in rel.parts or 'saves' in rel.parts:
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


for f in sorted((T / 'out').glob('master-*.mp4')):
    manifest(f, 'finished promo video (H.264 High/AAC 320k)')
for f in sorted((T / 'out').glob('*.jpg')):
    manifest(f, 'contact sheet of the encoded master')
for c in ('checkpoint4', 'checkpoint5', 'checkpoint6'):
    for f in sorted((T / c).iterdir()):
        if f.is_file() and f.suffix in ('.html', '.mp4', '.jpg', '.png'):
            manifest(f, f'review page or preview ({c})')
for d in sorted((T / 'captures').glob('*/frames')):
    manifest(d, 'native capture frame sequence (ROM-derived pixels; external)')
for f in sorted((T / 'captures').glob('*/state.csv')):
    manifest(f, 'measured native gameplay CSV (see provenance for entry kind)')
for f in sorted((T / 'captures').glob('*/audio.wav')):
    manifest(f, 'SFX-only capture audio, music volume 0 (ROM-derived PCM; external)')
manifest(T / 'work/bed.wav', 'music bed PCM (owner-supplied track 0-123.4 s with one fade); external, not redistributable')
for f in sorted((T / 'art').glob('*.png')):
    manifest(f, 'mascot drawing cut-out (Sol, from the owner\'s release-promo project); external')
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
prov = json.loads(next((T / 'captures').glob('*/provenance.json')).read_text())
idx = D / 'README.md'
s = idx.read_text()
S = f'sources/{label}'
head = f'''# MICA & TALON Mod Showcase

**Current: pacing revision, {label[-8:-4]}-{label[-4:-2]}-{label[-2:]}** (mod commit `{prov.get('mod_commit', '')[:10]}`, build `{prov.get('build_commit', '')[:10]}`, develop
`{prov.get('develop_commit', '')[:10]}`; 124.0 s, 16:9 and designed 9:16 cuts; the owner's music from its start with one fade; game sound from
each take's own SFX-only audio). Local archive only; not pushed. Sound checked by measurement only.

- [README: source and commits, owner feedback, sound, cards, what is not filmed as it ships, 1.0 clips, rebuild]({S}/README.md)
- [Edit: brief, tracked bar grid and both cuts]({S}/edit/edit.py), [cards]({S}/edit/cards.py)
- [Shot index]({S}/out/shot-index.csv), [chapters]({S}/out/chapters.txt), [verification]({S}/out/verification.json),
  [game-sound levels]({S}/out/sfx-levels.json), [takes check]({S}/out/takes-check.json)
- Reviews: [pacing storyboard data]({S}/checkpoint4/plan.json), [probe results]({S}/checkpoint5/probes.json)
- [External hashes](external-hashes-{label}.json): masters, review pages, frames, state CSVs, take audio, the bed, mascot
  cut-outs, fonts and the owner's music (name + SHA-256 only; no WAV is in this repository).

## Superseded: promo redo, delivered 2026-11-12

The 124 s cut the owner reviewed (OpenGGF `1e0faac123`, placed ROM stingers). Its takes now live in
`{OLD_TAKES}/` in the task folder: `captures/` there was renamed when the revision was shot, so every `captures/...`
path in [its external hashes](external-hashes-redo-20261112.json) resolves under that folder. Same files, same hashes.
'''
old = s[:s.index('- [README: source, music decision')]
assert old.startswith('# MICA & TALON Mod Showcase') and 'Current: promo redo, 2026-11-12' in old
s = s.replace(old, head + '\n', 1)
idx.write_text(s)
for p in projects:
    if p['id'] == proj:
        p['notes'] = 'Pacing revision (current); superseded: delivered redo 2026-11-12, production promo 2026-11-11, showcase 2026-11-10; local, sound measured only'
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
