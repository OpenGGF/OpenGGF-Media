#!/usr/bin/env python3
"""Readable-holds cut: build the additive OpenGGF-Media payload for revision readable-holds of project
menu-evolution (2026-10-29, Opus 5.5 pacing revision; adapted from the hill-climb-story builder).

Purpose: copy this revision's text sources (README, edit, review/identity/old-holds scripts, chapter/EDL/cue/
reading-hold lists, the result row, provenance, this script, and the superseded pre-hub-criteria render's
README, sources and provenance) byte for byte to
archive-payload/projects/menu-evolution/production/revisions/readable-holds/ (the same relative place as on
disk, so the edit's parents[3] still finds the archived production root), write the revision's external-asset
index and the updated project index, and write catalog fragments for the Media maintainer: sources.json and
projects.json rows to upsert (by path / id), assets.csv rows to append (final film, master and review images;
the superseded render's film, master and review images; the Hub and Dialogs follow-up still under the existing
design-review-evidence root) and the README table row. The music bed (super-sonic-cut), the moving takes, SFX and
UI tones (first delivery) and the earlier design-review stills (hill-climb-story) are already catalogued: the
external index names them with their hashes and the catalog that holds them, and no row or root is added for
them. Nothing is written to a Media checkout.
Usage: make_revision_payload.py [--verify-against MEDIA_CHECKOUT]  (copies the checkout's catalog/tools/projects
to a scratch directory under this revision, applies the fragments there, checks that only the project index row
of the existing menu-evolution sources changes and that every earlier menu-evolution source stays byte-identical,
runs tools/catalog.py verify, then deletes the scratch copy; the checkout itself is only read).
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
REL = REV.relative_to(PROD)                       # revisions/readable-holds
OUT = REV / 'archive-payload'
PID = 'menu-evolution'
PROJ = OUT / 'projects' / PID
ROOT_ID = f'{PID}/production'
EVID_ROOT = f'{PID}/design-review-evidence'
EVID_ORIGINAL = PROD.parent                       # the audit's evidence sets (MENU_EVIDENCE)
DATE = '2026-10-29'
ORIGINAL_INDEX = PROD / 'revisions/hill-climb-story/archive-payload/projects/menu-evolution/README.md'
ORIGINAL_INDEX_SHA = '25af35fb193f1df9df2bd754b191a150dbd620254ffd269057610053f3ffa328'   # as published at 6ea11dd97
EXT_INDEX = 'external-assets.readable-holds.json'
FILM = 'final/menu-evolution-readable-holds.mp4'
MASTER = 'final/menu-evolution-readable-holds-master.mkv'
SUP = 'superseded/pre-hub-criteria'
NEW_STILLS = {'hub_fu'}                           # first catalogued by this revision


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def source_files():
    keep = ['README.md', 'provenance/source-map.json', 'provenance/deliverables.json']
    keep += [f'{SUP}/README.md']
    for pattern in ['sources/promo/*.py', 'sources/promo/*.csv', 'sources/promo/*.txt', 'sources/promo/*.json',
                    'sources/archive/*.py', f'{SUP}/sources/promo/*', f'{SUP}/provenance/*.json']:
        keep += [str(p.relative_to(REV)) for p in sorted(REV.glob(pattern)) if p.is_file()]
    return sorted(dict.fromkeys(keep))


def inventory(files):
    lines = ''.join(f'{p.name}\0{p.stat().st_size}\0{sha(p)}\n' for p in sorted(files, key=lambda q: q.name))
    return hashlib.sha256(lines.encode()).hexdigest()


def external_assets():
    """(new rows for catalog/assets.csv, reused entries already catalogued elsewhere)."""
    new, reused = [], []

    def add(rel, kind):
        p = REV / rel
        new.append(dict(root=ROOT_ID, path=f'{REL}/{rel}', kind=kind, bytes=p.stat().st_size, files=1, sha256=sha(p)))

    add(FILM, 'finished film (revision readable-holds, final)')
    add(MASTER, 'lossless master (FFV1 + PCM, revision readable-holds, final)')
    add(f'{SUP}/final/menu-evolution-readable-holds-pre-hub-criteria.mp4',
        'superseded film (readable-holds first render, pre-hub-criteria)')
    add(f'{SUP}/final/menu-evolution-readable-holds-pre-hub-criteria-master.mkv',
        'superseded lossless master (readable-holds first render, pre-hub-criteria)')
    for d, kind in (('review', 'review images (footage-derived)'),
                    (f'{SUP}/review', 'review images of the superseded render (footage-derived)')):
        review = sorted((REV / d).glob('*.png'))
        new.append(dict(root=ROOT_ID, path=f'{REL}/{d}/*.png', kind=kind, bytes=sum(p.stat().st_size for p in review),
                        files=len(review), inventory_sha256=inventory(review)))
    smap = json.loads((REV / 'provenance/source-map.json').read_text())
    music = PROD / smap['reused']['music']['path']
    if sha(music) != smap['reused']['music']['sha256']:
        raise SystemExit('music bed changed')
    reused.append(dict(root=ROOT_ID, path=smap['reused']['music']['path'], kind='music bed (Super Sonic render)',
                       bytes=music.stat().st_size, files=1, sha256=smap['reused']['music']['sha256'],
                       catalogued_in='external-assets.super-sonic-cut.json'))
    for key, e in smap['evidence_stills']['files'].items():
        p = EVID_ORIGINAL / e['path']
        if sha(p) != e['sha256'] or p.stat().st_size != e['bytes']:
            raise SystemExit(f'evidence still changed: {p}')
        if key in NEW_STILLS:
            new.append(dict(root=EVID_ROOT, path=e['path'], kind=f'design-review capture still (Hub and Dialogs follow-up, '
                            f'{e["head"][:9]})', bytes=e['bytes'], files=1, sha256=e['sha256']))
            continue
        reused.append(dict(root=EVID_ROOT, path=e['path'], kind=f'design-review capture still ({key})', bytes=e['bytes'],
                           files=1, sha256=e['sha256'], catalogued_in='external-assets.hill-climb-story.json'))
    reused.append(dict(root=ROOT_ID, path='clips/{pre,new}/{hub,settings,locate,mods,legal,shader}/frames/*.png, '
                       'audio/sfx/*.wav, audio/ui/*.wav', kind='moving takes, SFX renders and UI tones',
                       catalogued_in='external-assets.json'))
    return new, reused


LATEST = """# ROAD TO 9: OpenGGF menu evolution promo

## Latest delivery: the readable-holds cut ({date})

The pacing revision [`production/revisions/readable-holds/`](production/revisions/readable-holds/README.md)
answers the user's review of the hill-climb story cut: "great work but some of the screens are a bit rushed.
lots of info on the screen that gets flashed up too quickly to ingest" and "some of the screens transition as
soon as they finish animating, too". Its external film
`revisions/readable-holds/final/menu-evolution-readable-holds.mp4` is **{seconds} seconds** ({frames:,} frames),
1920x1080 at 60 fps, H.264 with AAC stereo 48 kHz (integrated {lufs} LUFS, true peak {tp} dBTP) and
{chapters} chapters, with a lossless FFV1 + PCM master. Made by **Claude Opus 5.5 (xhigh)**; delivered for
review, so the user's acceptance is not recorded here.

Same story, bed and look as the hill-climb story cut, re-edited from its sources (no slow motion, no stretched
video): every information-heavy screen now finishes its reveal, then holds still for {hold_min:.1f}-{hold_max:.1f}
seconds before it changes (the accepted cut held its dense screens 0-1.5 s), measured frame by frame on a frozen
render (`reads.json`). Dense boards were simplified to one idea at a time; repeated captions, the scale line,
footnotes, the derived "12" count and the Time Attack still comparison were removed. The Super Sonic bed plays as
one continuous excerpt (bed beats 16 to the stab on 152).

The user then asked for the hub's spacing and icon criteria to be earned rather than rounded; an engine follow-up
did that (`ca3d04a1d`, `55d9fec81`, audit at `56c9aed13`). The final row shows the follow-up's exact A1 Hub row
(9 on each criterion, spacing and icons marked "was 8.5") from `result-row.json`, and the delivered wall's hub
cell is the follow-up's own still, labelled as one; only the hub is claimed 9 on each criterion. The first
render, with the finish-pass row, is kept as `superseded/pre-hub-criteria/`. Sound was checked by measurement
only, motion through frames and strips.

- [Revision README](production/revisions/readable-holds/README.md): reading holds before and after, what was
  removed, checks and limits.
- [Edit](production/revisions/readable-holds/sources/promo/edit.py): brief, beat sheet and reading-hold table in
  its docstring; chapters, source intervals, cues and holds beside it.
- [External assets of this cut](external-assets.readable-holds.json): film, master, review images, the superseded
  render and the follow-up still, hashed and not uploaded, plus the already-catalogued bed, takes and capture
  stills it reuses.

"""


def index_text(film):
    original = ORIGINAL_INDEX.read_bytes()
    if hashlib.sha256(original).hexdigest() != ORIGINAL_INDEX_SHA:
        raise SystemExit('original project index differs from the published one')
    body = original.decode()
    head = '# ROAD TO 9: OpenGGF menu evolution promo\n\n'
    old = '## Latest delivery: the hill-climb story cut (2026-10-29)\n'
    if not body.startswith(head + old):
        raise SystemExit('unexpected original index heading')
    third = ('## Third delivery: the hill-climb story cut (43.2 s, retained)\n\n'
             'The user found this cut "great work but some of the screens are a bit rushed. lots of info on the '
             'screen that gets flashed up too quickly to ingest". It stays byte-identical with its sources; the '
             'readable-holds cut is re-edited from them.\n')
    reads = json.loads((REV / 'sources/promo/reads.json').read_text())['reads']
    holds = [r['hold_s'] for r in reads if r['id'] != 'delivered']
    return LATEST.format(date=DATE, hold_min=min(holds), hold_max=max(holds), **film) + third + body[len(head) + len(old):]


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    deliv = json.loads((REV / 'provenance/deliverables.json').read_text())['film']
    film = dict(seconds=deliv['seconds'], frames=deliv['frames'], lufs=deliv['aac_integrated_lufs'],
                tp=deliv['aac_true_peak_dbtp'], chapters=deliv['chapters'])
    sources = []
    for rel in source_files():
        dst = PROJ / 'production' / REL / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REV / rel, dst)
        sources.append(dict(path=f'projects/{PID}/production/{REL}/{rel}', root=ROOT_ID, original_path=f'{REL}/{rel}',
                            bytes=dst.stat().st_size, sha256=sha(dst), snapshot='byte-copy'))
    (PROJ / 'README.md').write_text(index_text(film))
    new, reused = external_assets()
    (PROJ / EXT_INDEX).write_text(json.dumps(dict(
        project=PID, revision='readable-holds', snapshot_date=DATE,
        notes='External bytes of the readable-holds cut, hashed at archive time, not uploaded. `assets` are new '
              'catalog rows (final film, master and review images; the superseded pre-hub-criteria render; the Hub and '
              'Dialogs follow-up still); `reused` are inputs already catalogued by an earlier '
              'revision (named in catalogued_in), listed here with their hashes so this cut can be rebuilt. Render '
              'work (build/), the Python venv, logs, fonts and ROMs are excluded.',
        sequence_hash='inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append UTF-8 basename + NUL '
                      '+ decimal byte length + NUL + lowercase SHA-256 + LF.',
        assets=new, reused=reused), indent=1) + '\n')
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
    for a in new:
        w.writerow([PID, a['root'], a['path'], a['kind'], a['bytes'], a['files']])
    (frag / 'assets.csv').write_text(buf.getvalue())
    print(f'{len(sources)} payload source rows (1 replaces the project index), {len(new)} new external rows, '
          f'{len(reused)} reused entries -> {OUT}')
    return sources, new


def write_project_fragments(media, sources, assets):
    frag = OUT / 'catalog-fragments'
    existing = json.loads((media / 'catalog/sources.json').read_text())
    with (media / 'catalog/assets.csv').open(newline='') as fh:
        ext_rows = sum(1 for a in csv.DictReader(fh) if a['project'] == PID)
    paths = {s['path'] for s in existing if s['path'].startswith(f'projects/{PID}/')}
    n_src = len(paths) + sum(1 for s in sources if s['path'] not in paths)
    n_ext = ext_rows + len(assets)
    (frag / 'projects.json').write_text(json.dumps([dict(
        id=PID, title='ROAD TO 9: menu evolution promo, Super Sonic, hill-climb story and readable-holds cuts',
        notes='Promo of the engine menus across OpenGGF 0.5, the pre-redesign 0.7 menus and the delivered redesign '
              'with dated design-review scores (first film, 87.333 s); its half-length recut on Sonic 2\'s Super '
              'Sonic music (43.2 s); the hill-climb story cut (43.2 s), which tells the AI design review itself; and '
              'the readable-holds cut (latest delivery), the same story re-edited so every dense screen settles and '
              'holds before it changes, ending on the hub\'s exact criteria after its spacing and icon follow-up (9 on each) and that '
              'follow-up\'s still; its pre-follow-up first render is kept as superseded. Edits, recorders, take recipes, capture '
              'records, reading-hold measurements and provenance. Films, masters, frames, ROM-derived audio, review '
              'captures and fonts remain external. Listening and real-time viewing not claimed.',
        source_files=n_src, catalog_entries=n_ext)], indent=1) + '\n')
    (frag / 'README-row.md').write_text(
        f'Replace the menu-evolution row of the README project table with:\n\n'
        f'| [ROAD TO 9: menu evolution promo, Super Sonic, hill-climb story and readable-holds cuts](projects/{PID}/) '
        f'| {n_src} | {n_ext:,} |\n\n'
        'Suggested ending for the README paragraph on retained material: "The Road to 9 menu-evolution promo retains '
        'authentic moving 0.5, pre-redesign and delivered-menu captures, its edit and subjective design-review score '
        'sources, its half-length Super Sonic recut, the hill-climb story cut that tells the AI design review and its '
        'readable-holds pacing revision."\n\n'
        'Merge: upsert catalog-fragments/sources.json rows by path (only projects/menu-evolution/README.md already '
        'exists) and projects.json by id; append assets.csv. No new root: the revision lives under the '
        f'{ROOT_ID} root; its stills, including the new Hub and Dialogs follow-up still '
        '(hub-criteria-nine-20261029/...), under the existing {EVID_ROOT} root.\n'.replace('{EVID_ROOT}', EVID_ROOT))
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
    unchanged = sum(1 for p, s in old_proj.items()
                    if p != f'projects/{PID}/README.md' and sha(scratch / p) == s['sha256'])
    print(f'{unchanged}/{len(old_proj) - 1} earlier menu-evolution sources byte-identical; project index row replaced')
    mine = [p for p in merged if p.startswith(f'projects/{PID}/')]
    with (scratch / 'catalog/assets.csv').open(newline='') as fh:
        ext = sum(1 for a in csv.DictReader(fh) if a['project'] == PID)
    print(f'merged menu-evolution sources {len(mine)} (projects.json says {new_proj["source_files"]}), '
          f'external rows {ext} (projects.json says {new_proj["catalog_entries"]})')
    r = subprocess.run([sys.executable, 'tools/catalog.py', 'verify'], cwd=scratch, capture_output=True, text=True)
    print(r.stdout + r.stderr)
    shutil.rmtree(scratch)
    if not any((REV / 'build').iterdir()):
        (REV / 'build').rmdir()
    return (r.returncode or (unchanged != len(old_proj) - 1) or len(mine) != new_proj['source_files']
            or ext != new_proj['catalog_entries'])


if __name__ == '__main__':
    src, ext = build()
    if '--verify-against' in sys.argv:
        media = Path(sys.argv[sys.argv.index('--verify-against') + 1])
        print('project row: sources %d, external entries %d' % write_project_fragments(media, src, ext))
        sys.exit(1 if verify(media) else 0)
