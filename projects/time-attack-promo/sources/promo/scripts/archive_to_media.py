#!/usr/bin/env python3
"""Archive Film A (multiplayer Time Attack promo) into an OpenGGF-Media checkout.

Inputs: this production root (/home/farrell/Videos/OGGF/ta-promo-a) and the path of an
OpenGGF-Media worktree. Copies bounded production text into projects/time-attack-promo/sources,
hashes every other production file as an external asset (PNG directories as sequences), and
extends catalog/{roots,sources,projects}.json and assets.csv. Re-running replaces this project's
rows. Origin: Film A delivery, 2026-10-23.
"""
import csv, hashlib, io, json, os, shutil, sys
from pathlib import Path

P = Path('/home/farrell/Videos/OGGF/ta-promo-a')
PROJECT = 'time-attack-promo'
ROOT_ID = PROJECT + '/promo'
FONT_ROOT = PROJECT + '/fonts'
ARCHIVE = f'projects/{PROJECT}/sources/promo'
SKIP_DIRS = {'archive-staging', 'cwd', '__pycache__', 'build', 'classes', 'classes-audio', 'classes-tools', 'bots'}
# Consumed logs, machine-local config/identities and compiled classes are neither sources nor catalogued.
SKIP_SUFFIXES = {'.log', '.class', '.key', '.pub', '.example'}
TEXT = {'.py', '.sh', '.md', '.java', '.txt', '.csv', '.tsv', '.route', '.json'}
BULK_TEXT = ('ym-writes.txt',)
SOURCE_MAX = 1_000_000


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def is_source(rel):
    parts = rel.parts
    if rel.suffix not in TEXT or rel.name.endswith(BULK_TEXT):
        return False
    if (P / rel).stat().st_size > SOURCE_MAX:
        return False
    if parts[0] in ('music', 'review', 'probes', 'out'):
        return rel.suffix in ('.md', '.tsv')
    if 'profile' in parts and rel.name not in ('settings.txt',):
        return False
    if 'superseded' in parts and rel.name == 'state.csv':
        return False
    return True


def kind(rel):
    n = rel.name
    if rel.parts[0] == 'out':
        return 'delivered final film' if n == 'openggf-multiplayer-time-attack-promo.mp4' else 'final picture / pre-normalisation master'
    if n == 'compositor-premaster.mp4':
        return 'final picture / pre-normalisation master'
    if n == 'video.mkv':
        return 'superseded capture' if 'superseded' in rel.parts else 'lossless capture'
    if n == 'audio.pcm':
        return 'capture audio (ROM-derived)'
    if rel.parts[0] == 'music':
        return 'ROM-derived audio'
    if rel.parts[0] == 'fonts':
        return 'external editorial font'
    if n.endswith('.csv') or n.endswith('.txt') or n.endswith('.log'):
        return 'generated state/diagnostic data'
    return 'media dependency'


def walk():
    sources, files, pngdirs = [], [], {}
    for dirpath, dirnames, filenames in os.walk(P, followlinks=False):
        d = Path(dirpath)
        dirnames[:] = sorted(x for x in dirnames if x not in SKIP_DIRS and not (d / x).is_symlink()
                             and not (x == 'server' and d.parent.name in ('captures', 'captures-v3', 'superseded')))
        for name in sorted(filenames):
            full = d / name
            if full.is_symlink():
                continue
            rel = full.relative_to(P)
            if rel.suffix in SKIP_SUFFIXES or ('profile' in rel.parts and rel.name != 'settings.txt'):
                continue
            if rel == Path('scripts/archive_to_media.py') or is_source(rel):
                sources.append(rel)
            elif rel.suffix == '.png':
                pngdirs.setdefault(rel.parent, []).append(full)
            else:
                files.append(rel)
    return sources, files, pngdirs


def main(media):
    media = Path(media)
    sources, files, pngdirs = walk()
    dest = media / ARCHIVE
    if dest.exists():
        shutil.rmtree(dest)
    src_rows = []
    for rel in sources:
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(P / rel, out)
        data = out.read_bytes()
        src_rows.append({'path': f'{ARCHIVE}/{rel.as_posix()}', 'root': ROOT_ID,
                         'original_path': rel.as_posix(), 'bytes': len(data),
                         'sha256': hashlib.sha256(data).hexdigest(), 'snapshot': 'byte-copy'})
    assets = []
    for rel in files:
        root = FONT_ROOT if rel.parts[0] == 'fonts' else ROOT_ID
        assets.append({'root': root, 'path': rel.as_posix(), 'kind': kind(rel),
                       'bytes': (P / rel).stat().st_size, 'files': 1, 'sha256': sha(P / rel)})
    for d, pngs in sorted(pngdirs.items()):
        inv = hashlib.sha256()
        total = 0
        for f in sorted(pngs, key=lambda x: x.name):
            size = f.stat().st_size
            total += size
            inv.update(f'{f.name}\0{size}\0{sha(f)}\n'.encode())
        assets.append({'root': ROOT_ID, 'path': d.as_posix() + '/*.png', 'kind': 'frame-sequence'
                       if d.parts[0] not in ('design',) else 'external artwork / editorial plates',
                       'bytes': total, 'files': len(pngs), 'inventory_sha256': inv.hexdigest()})
    proj = media / 'projects' / PROJECT
    (proj / 'external-assets.json').write_text(json.dumps({
        'project': PROJECT, 'snapshot_date': '2026-10-23',
        'notes': 'External bytes hashed at archive time, not uploaded. edit/build render work, capture '
                 'cwd/profile trees, compiled driver classes and Python caches are excluded.',
        'sequence_hash': 'inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append '
                         'UTF-8 basename + NUL + decimal byte length + NUL + lowercase SHA-256 + LF.',
        'assets': assets}, indent=1) + '\n')

    cat = media / 'catalog'
    def load(n):
        return json.loads((cat / n).read_text())
    def save(n, v):
        (cat / n).write_text(json.dumps(v, indent=2) + '\n')
    roots = [r for r in load('roots.json') if not r['id'].startswith(PROJECT + '/')]
    roots += [{'id': ROOT_ID, 'original': str(P), 'archive': ARCHIVE,
               'notes': 'Film A, the multiplayer Time Attack promo: byte-preserved edit, capture driver, '
                        'records and revision history. Footage, ROM-derived audio and plates remain external.'},
              {'id': FONT_ROOT, 'original': str(P / 'fonts'), 'archive': '',
               'notes': 'External Fira/Anton editorial faces; hashed, not redistributed.'}]
    save('roots.json', roots)
    srcs = [s for s in load('sources.json') if not s['path'].startswith(f'projects/{PROJECT}/')]
    extra = []
    for f in sorted(proj.rglob('*')):
        if f.is_file() and not str(f).startswith(str(dest)):
            data = f.read_bytes()
            extra.append({'path': f.relative_to(media).as_posix(), 'root': ROOT_ID,
                          'original_path': '', 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest(), 'snapshot': 'archive-authored'})
    save('sources.json', srcs + src_rows + extra)
    projects = [p for p in load('projects.json') if p['id'] != PROJECT]
    projects.append({'id': PROJECT, 'title': 'Multiplayer Time Attack promo',
                     'notes': 'Film A, the delivered multiplayer Time Attack promo, with its edit, capture driver, '
                              'capture records and every superseded edit revision; film/footage/audio remain external.',
                     'source_files': len(src_rows) + len(extra), 'catalog_entries': len(assets)})
    save('projects.json', projects)
    # Append, leaving other projects' rows byte-identical (the file mixes CRLF and LF endings).
    raw = (cat / 'assets.csv').read_bytes().decode('utf-8')
    kept = ''.join(l for l in raw.splitlines(keepends=True) if not l.startswith(PROJECT + ','))
    if not kept.endswith('\n'):
        kept += '\r\n'
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\r\n')
    for a in assets:
        w.writerow([PROJECT, a['root'], a['path'], a['kind'], a['bytes'], a['files']])
    (cat / 'assets.csv').write_bytes((kept + buf.getvalue()).encode('utf-8'))
    print(f'{len(src_rows)} sources, {len(extra)} archive files, {len(assets)} external entries')


if __name__ == '__main__':
    main(sys.argv[1])
