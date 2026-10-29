#!/usr/bin/env python3
"""Hill-climb story cut: build the additive OpenGGF-Media payload for revision hill-climb-story of
project menu-evolution (2026-10-29, Opus 5.5 narrative rebuild; adapted from the super-sonic-cut builder).

Purpose: copy this revision's text sources (README, edit, review and identity scripts, chapter/EDL/cue
lists, provenance, this script) byte for byte to
archive-payload/projects/menu-evolution/production/revisions/hill-climb-story/ (the same relative place
as on disk, so the edit's parents[3] still finds the archived production root), write the revision's
external-asset index and the updated project index, and write catalog fragments for the Media
maintainer: sources.json and projects.json rows to upsert (by path / id), assets.csv rows and one
roots.json row (the design-review evidence stills) to append, and the README table row. Film, master,
evidence stills and review images stay external and are hashed; the music bed is the Super Sonic cut's
render, already catalogued. Nothing is written to a Media checkout.
Usage: make_revision_payload.py [--verify-against MEDIA_CHECKOUT]  (copies the checkout's
catalog/tools/projects to a scratch directory under this revision, applies the fragments there, checks
that only the project index row of the existing menu-evolution sources changes, runs
tools/catalog.py verify, then deletes the scratch copy; the checkout itself is only read).
"""
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[2]
PROD = REV.parents[1]
REL = REV.relative_to(PROD)                       # revisions/hill-climb-story
OUT = REV / 'archive-payload'
PID = 'menu-evolution'
PROJ = OUT / 'projects' / PID
ROOT_ID = f'{PID}/production'
DATE = '2026-10-29'
ORIGINAL_INDEX = PROD / 'revisions/super-sonic-cut/archive-payload/projects/menu-evolution/README.md'
ORIGINAL_INDEX_SHA = '9c30dfdb4b38582a2faa4c53eb054780f20d48234454cf885ba059d221d7d23d'   # as published at c99d61a42
EXT_INDEX = 'external-assets.hill-climb-story.json'
EVID_ROOT = f'{PID}/design-review-evidence'
EVID_ORIGINAL = PROD.parent                       # the audit's evidence sets (MENU_EVIDENCE)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def source_files():
    keep = ['README.md', 'provenance/source-map.json', 'provenance/deliverables.json']
    for pattern in ['sources/promo/*.py', 'sources/promo/*.csv', 'sources/promo/*.txt', 'sources/promo/*.json',
                    'sources/archive/*.py']:
        keep += [str(p.relative_to(REV)) for p in sorted(REV.glob(pattern)) if p.is_file()]
    return sorted(dict.fromkeys(keep))


def inventory(files):
    lines = ''.join(f'{p.name}\0{p.stat().st_size}\0{sha(p)}\n' for p in sorted(files, key=lambda q: q.name))
    return hashlib.sha256(lines.encode()).hexdigest()


def external_assets():
    rows = []

    def add(rel, kind):
        p = REV / rel
        rows.append(dict(root=ROOT_ID, path=f'{REL}/{rel}', kind=kind, bytes=p.stat().st_size, files=1, sha256=sha(p)))

    add('final/menu-evolution-hill-climb-story.mp4', 'finished film (revision hill-climb-story)')
    add('final/menu-evolution-hill-climb-story-master.mkv', 'lossless master (FFV1 + PCM, revision hill-climb-story)')
    evidence = json.loads((REV / 'provenance/source-map.json').read_text())['evidence_stills']['files']
    for key, e in evidence.items():
        p = EVID_ORIGINAL / e['path']
        if sha(p) != e['sha256'] or p.stat().st_size != e['bytes']:
            raise SystemExit(f'evidence still changed: {p}')
        rows.append(dict(root=EVID_ROOT, path=e['path'], kind=f'design-review capture still (UI evidence, {e["head"][:9]})',
                         bytes=e['bytes'], files=1, sha256=e['sha256']))
    review = sorted((REV / 'review').glob('*.png'))
    rows.append(dict(root=ROOT_ID, path=f'{REL}/review/*.png', kind='review images (footage-derived)',
                     bytes=sum(p.stat().st_size for p in review), files=len(review), inventory_sha256=inventory(review)))
    return rows


LATEST = """# ROAD TO 9: OpenGGF menu evolution promo

## Latest delivery: the hill-climb story cut ({date})

The narrative rebuild [`production/revisions/hill-climb-story/`](production/revisions/hill-climb-story/README.md)
answers the user's review of the Super Sonic cut: "not bad but the direction sucks. It's difficult to
see what the video is getting at. We need to establish the context". Its external film
`revisions/hill-climb-story/final/menu-evolution-hill-climb-story.mp4` is **43.200 seconds** (2,592 frames),
1920x1080 at 60 fps, H.264 with AAC stereo 48 kHz (integrated -14.6 LUFS, true peak -1.5 dBTP) and
13 chapters, with a lossless FFV1 + PCM master. Made by **Claude Opus 5.5 (xhigh)**; delivered for
review, so the user's acceptance is not recorded here.

It tells the experiment instead of only showing old and new menus: we gave an AI (Claude Opus) every
OpenGGF menu; it sorted them into six groups, scored each on seven criteria from screenshots, and hill
climbed round by round (change, recapture, rescore, keep or revert) until all 27 menu families reached 8;
then we raised the target to 9. A polish pass stalled at 0, a fresh AI review marked up the pictures and
lowered scores, a structural pass reached 13, another review sent one 9 back, the finish pass reached 26
and the last gap made 27 / 27 at 9 overall, with the criteria still at 8.5 shown. One evolving score
board narrates; the round-0 and delivered menus (moving) and the review's own captures prove it. Same
Super Sonic bed as the second delivery. Sound was checked by measurement only, motion through strips.

- [Revision README](production/revisions/hill-climb-story/README.md): the rejection, chapter questions,
  decisions, viewer pass, checks and limits.
- [Edit](production/revisions/hill-climb-story/sources/promo/edit.py): brief and beat sheet in its docstring;
  every score with its audit section; chapters, source intervals and cues beside it.
- [External assets of this cut](external-assets.hill-climb-story.json): film, master, the design-review
  capture stills and review images, hashed and not uploaded.

"""


def index_text():
    original = ORIGINAL_INDEX.read_bytes()
    if hashlib.sha256(original).hexdigest() != ORIGINAL_INDEX_SHA:
        raise SystemExit('original project index differs from the published one')
    body = original.decode()
    head = '# ROAD TO 9: OpenGGF menu evolution promo\n\n'
    old = '## Latest delivery: the Super Sonic cut (2026-10-29)\n'
    if not body.startswith(head + old):
        raise SystemExit('unexpected original index heading')
    second = ('## Second delivery: the Super Sonic cut (43.2 s, retained)\n\n'
              'The user found this cut "not bad but the direction sucks. It\'s difficult to see what the video '
              'is getting at". It stays byte-identical with its sources; the hill-climb story cut reads its bed '
              'in place.\n')
    return LATEST.format(date=DATE) + second + body[len(head) + len(old):]


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    sources = []
    for rel in source_files():
        dst = PROJ / 'production' / REL / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REV / rel, dst)
        sources.append(dict(path=f'projects/{PID}/production/{REL}/{rel}', root=ROOT_ID, original_path=f'{REL}/{rel}',
                            bytes=dst.stat().st_size, sha256=sha(dst), snapshot='byte-copy'))
    (PROJ / 'README.md').write_text(index_text())
    assets = external_assets()
    (PROJ / EXT_INDEX).write_text(json.dumps(dict(
        project=PID, revision='hill-climb-story', snapshot_date=DATE,
        notes='External bytes of the hill-climb story cut, hashed at archive time, not uploaded. Its native frame '
              'sequences, SFX renders, UI tones and fonts are the first delivery\'s (external-assets.json); its music '
              'bed is the Super Sonic cut\'s render (external-assets.super-sonic-cut.json). The design-review stills '
              'are original captures of the menu audit (root menu-evolution/design-review-evidence). Render work '
              '(build/), the Python venv, logs and ROMs are excluded.',
        sequence_hash='inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append UTF-8 basename + NUL '
                      '+ decimal byte length + NUL + lowercase SHA-256 + LF.',
        assets=assets), indent=1) + '\n')
    for name in ['README.md', EXT_INDEX]:
        p = PROJ / name
        sources.append(dict(path=f'projects/{PID}/{name}', root=ROOT_ID,
                            original_path=f'{REL}/archive-payload/projects/{PID}/{name}',
                            bytes=p.stat().st_size, sha256=sha(p), snapshot='generated index'))
    frag = OUT / 'catalog-fragments'
    frag.mkdir(parents=True)
    (frag / 'sources.json').write_text(json.dumps(sources, indent=1) + '\n')
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    for a in assets:
        w.writerow([PID, a['root'], a['path'], a['kind'], a['bytes'], a['files']])
    (frag / 'assets.csv').write_text(buf.getvalue())
    (frag / 'roots.json').write_text(json.dumps([dict(
        id=EVID_ROOT, original=str(EVID_ORIGINAL), archive='',
        notes='Menu design-review evidence sets (2026-10-28/29 captures of the audit, outside every repository): the '
              'capture stills and the reviewer\'s annotated picture used by the hill-climb story cut; hashed, not '
              'uploaded.')], indent=1) + '\n')
    print(f'{len(sources)} payload source rows (1 replaces the project index), {len(assets)} external rows -> {OUT}')
    return sources, assets


def merged_counts(existing_sources, existing_assets_rows, sources, assets):
    paths = {s['path'] for s in existing_sources if s['path'].startswith(f'projects/{PID}/')}
    new = [s for s in sources if s['path'] not in paths]
    return len(paths) + len(new), existing_assets_rows + len(assets)


def write_project_fragments(media, sources, assets):
    frag = OUT / 'catalog-fragments'
    existing = json.loads((media / 'catalog/sources.json').read_text())
    with (media / 'catalog/assets.csv').open(newline='') as fh:
        ext_rows = sum(1 for a in csv.DictReader(fh) if a['project'] == PID)
    n_src, n_ext = merged_counts(existing, ext_rows, sources, assets)
    (frag / 'projects.json').write_text(json.dumps([dict(
        id=PID, title='ROAD TO 9: menu evolution promo, Super Sonic cut and hill-climb story cut',
        notes='Promo of the engine menus across OpenGGF 0.5, the pre-redesign 0.7 menus and the delivered redesign '
              'with dated design-review scores (first film, 87.333 s); its half-length recut on Sonic 2\'s Super '
              'Sonic music (43.2 s); and the hill-climb story cut (43.2 s, latest delivery), which tells the AI '
              'design review itself: classification, rubric, the climb to 8, the raised target and the reviews on '
              'the road to 9. Edits, recorders, take recipes, capture records and provenance. Films, masters, frames, '
              'ROM-derived audio, review captures and fonts remain external. Listening and real-time viewing not '
              'claimed.',
        source_files=n_src, catalog_entries=n_ext)], indent=1) + '\n')
    (frag / 'README-row.md').write_text(
        f'Replace the menu-evolution row of the README project table with:\n\n'
        f'| [ROAD TO 9: menu evolution promo, Super Sonic cut and hill-climb story cut](projects/{PID}/) | {n_src} | {n_ext:,} |\n\n'
        'Suggested ending for the README paragraph on retained material: "The Road to 9 menu-evolution promo retains '
        'authentic moving 0.5, pre-redesign and delivered-menu captures, its edit and subjective design-review score '
        'sources, its half-length Super Sonic recut and the hill-climb story cut that tells the AI design review."\n\n'
        'Merge: upsert catalog-fragments/sources.json rows by path (only projects/menu-evolution/README.md already '
        'exists) and projects.json by id; append assets.csv and roots.json (one new root, '
        f'{EVID_ROOT}, for the design-review capture stills; the revision itself lives under the menu-evolution/production '
        'root).\n')
    return n_src, n_ext


def verify(media):
    media = Path(media)
    scratch = REV / 'build' / 'media-verify'
    if scratch.exists():
        shutil.rmtree(scratch)
    for part in ['catalog', 'tools', 'projects']:
        shutil.copytree(media / part, scratch / part, symlinks=True)
    frag = OUT / 'catalog-fragments'
    before = {s['path']: s for s in json.loads((scratch / 'catalog/sources.json').read_text())}
    old_proj = {p: s for p, s in before.items() if p.startswith(f'projects/{PID}/')}
    shutil.copytree(PROJ, scratch / 'projects' / PID, dirs_exist_ok=True)
    rows = json.loads((frag / 'sources.json').read_text())
    replaced = [r['path'] for r in rows if r['path'] in before]
    if replaced != [f'projects/{PID}/README.md']:
        raise SystemExit(f'unexpected replacements: {replaced}')
    merged = dict(before)
    for r in rows:
        merged[r['path']] = r
    (scratch / 'catalog/sources.json').write_text(json.dumps(list(merged.values()), indent=1) + '\n')
    projects = json.loads((scratch / 'catalog/projects.json').read_text())
    new_proj = json.loads((frag / 'projects.json').read_text())[0]
    projects = [new_proj if p['id'] == PID else p for p in projects]
    (scratch / 'catalog/projects.json').write_text(json.dumps(projects, indent=1) + '\n')
    with (scratch / 'catalog/assets.csv').open('a') as fh:
        fh.write((frag / 'assets.csv').read_text())
    roots = json.loads((scratch / 'catalog/roots.json').read_text())
    if any(r['id'] == EVID_ROOT for r in roots):
        raise SystemExit('evidence root already present')
    roots += json.loads((frag / 'roots.json').read_text())
    (scratch / 'catalog/roots.json').write_text(json.dumps(roots, indent=1) + '\n')
    # the first delivery's archived files: every one but the regenerated index is byte-identical
    unchanged = sum(1 for p, s in old_proj.items()
                    if p != f'projects/{PID}/README.md' and sha(scratch / p) == s['sha256'])
    print(f'{unchanged}/{len(old_proj) - 1} earlier menu-evolution sources byte-identical; project index row replaced')
    mine = [p for p in merged if p.startswith(f'projects/{PID}/')]
    print(f'merged menu-evolution sources {len(mine)} (projects.json says {new_proj["source_files"]})')
    r = subprocess.run([sys.executable, 'tools/catalog.py', 'verify'], cwd=scratch, capture_output=True, text=True)
    print(r.stdout + r.stderr)
    shutil.rmtree(scratch)
    if not any((REV / 'build').iterdir()):
        (REV / 'build').rmdir()
    return r.returncode or (unchanged != len(old_proj) - 1) or len(mine) != new_proj['source_files']


if __name__ == '__main__':
    src, ext = build()
    if '--verify-against' in sys.argv:
        media = Path(sys.argv[sys.argv.index('--verify-against') + 1])
        print('project row: sources %d, external entries %d' % write_project_fragments(media, src, ext))
        sys.exit(1 if verify(media) else 0)
