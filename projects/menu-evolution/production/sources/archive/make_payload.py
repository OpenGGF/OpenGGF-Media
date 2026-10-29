#!/usr/bin/env python3
"""Menu evolution promo: build the bounded OpenGGF-Media archive payload for project menu-evolution.

Purpose: copy the production's text sources (edit, capture recorders and take recipes, capture
records, provenance, README) byte for byte into archive-payload/projects/menu-evolution/, write the
project index and external-assets.json, and write catalog fragments (projects/roots/sources JSON
and assets.csv rows) for the Media maintainer to merge. Nothing is written to a Media checkout.
Footage, frames, ROM-derived audio, synthesised tones, fonts, builds, logs and review images stay
external and are hashed instead.
Usage: make_payload.py [--verify-against MEDIA_CHECKOUT]  (the verify copies the checkout's
catalog/tools/projects to a scratch directory, merges the fragments there and runs
tools/catalog.py verify; the checkout itself is only read).
Origin: menu-evolution-promo-20261029 (Opus 5.5 producer).
"""
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

PROD = Path(__file__).resolve().parents[2]
OUT = PROD / 'archive-payload'
PID = 'menu-evolution'
PROJ = OUT / 'projects' / PID
ROOT_ID = f'{PID}/production'
FONT_ROOT = f'{PID}/fonts'
FONTS = Path('/usr/share/fonts/TTF')
FONT_FILES = ['FiraSansCompressed-Heavy.ttf', 'FiraSansCompressed-HeavyItalic.ttf', 'FiraSansCondensed-BoldItalic.ttf',
              'FiraSans-Bold.ttf', 'FiraSans-BoldItalic.ttf']
DATE = '2026-10-29'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def source_files():
    """Relative paths (to the production root) of every preserved text source."""
    keep = ['README.md', 'provenance/source-map.json', 'provenance/deliverables.json',
            'final/revisions/r1-README.txt']
    for pattern in ['sources/promo/*.py', 'sources/promo/*.csv', 'sources/promo/*.txt', 'sources/promo/*.json',
                    'sources/promo/revisions/*.py', 'sources/capture/*.py', 'sources/capture/takes/*.take',
                    'sources/capture/java/**/*.java', 'sources/capture/java05/**/*.java', 'sources/archive/*.py']:
        keep += [str(p.relative_to(PROD)) for p in sorted(PROD.glob(pattern)) if p.is_file()]
    for take in sorted((PROD / 'clips').glob('*/*')):
        if take.is_symlink() or not take.is_dir():
            continue
        for name in ['events.csv', 'provenance.json', 'take.txt', 'state.csv']:
            if (take / name).is_file():
                keep.append(str((take / name).relative_to(PROD)))
    return sorted(dict.fromkeys(keep))


def sequence_hash(files):
    lines = []
    for p in sorted(files, key=lambda q: q.name):
        lines.append(f'{p.name}\0{p.stat().st_size}\0{sha(p)}\n')
    return hashlib.sha256(''.join(lines).encode()).hexdigest()


def external_assets():
    rows = []

    def add(rel, kind):
        p = PROD / rel
        rows.append(dict(root=ROOT_ID, path=rel, kind=kind, bytes=p.stat().st_size, files=1, sha256=sha(p)))

    add('final/menu-evolution-promo.mp4', 'finished film')
    add('final/menu-evolution-master.mkv', 'lossless master (FFV1 + PCM)')
    for p in sorted((PROD / 'final/revisions').glob('*.mp4')):
        add(str(p.relative_to(PROD)), 'superseded revision')
    for take in sorted((PROD / 'clips').glob('*/*')):
        if take.is_symlink() or not take.is_dir():
            continue
        frames = sorted((take / 'frames').glob('*.png'))
        rows.append(dict(root=ROOT_ID, path=str((take / 'frames').relative_to(PROD)) + '/*.png',
                         kind='frame-sequence (native 320x224 engine capture, ROM-derived art)',
                         bytes=sum(f.stat().st_size for f in frames), files=len(frames),
                         inventory_sha256=sequence_hash(frames)))
    for sub, kind in [('music', 'audio render (ROM-derived music)'), ('sfx', 'audio render (ROM-derived SFX)'),
                      ('candidates', 'audio render (ROM-derived, unused candidate)'),
                      ('ui', 'synthesised engine UI tone (HostUiSfx formula)')]:
        for p in sorted((PROD / 'audio' / sub).glob('*.wav')):
            add(str(p.relative_to(PROD)), kind)
    review = sorted(p for p in (PROD / 'review').rglob('*.png'))
    rows.append(dict(root=ROOT_ID, path='review/**/*.png', kind='review images (footage-derived)',
                     bytes=sum(p.stat().st_size for p in review), files=len(review),
                     inventory_sha256=sequence_hash(review) if len({p.name for p in review}) == len(review) else
                     hashlib.sha256(''.join(f'{p.relative_to(PROD)}\0{p.stat().st_size}\0{sha(p)}\n'
                                            for p in review).encode()).hexdigest()))
    for name in FONT_FILES:
        p = FONTS / name
        rows.append(dict(root=FONT_ROOT, path=name, kind='font (SIL OFL, system package ttf-fira-sans 4.301)',
                         bytes=p.stat().st_size, files=1, sha256=sha(p)))
    return rows


INDEX = """# ROAD TO 9: OpenGGF menu evolution promo

Finished production, {date}. The external film `final/menu-evolution-promo.mp4` is **87.333 seconds**,
1920x1080 at 60 fps, H.264 with AAC stereo 48 kHz (integrated -14.2 LUFS, true peak -1.4 dBTP) and
10 chapters; a lossless FFV1 + PCM master sits beside it. Made by **Claude Opus 5.5 (xhigh)** for the
request "a promo video of the old menu vs the new one. Could even include the old 0.5 menu", steered
to "an action movie montage, with various numbers slowly climbing".

A training montage for the engine's menus: the OpenGGF 0.5 game select (`77c6364ce`), the 0.7 menus
before the redesign (`2f9ca84b1`) and the delivered menus (`d823ce643`), each recorded frame by frame
from its own production code with scripted keys. Old and new run the same task in sync while a
before/now divider sweeps across one pane and the design review's dated scores climb to 9; the
climax counts menu families at 9 (0 -> 13 -> 26 -> 27). The scores are the review's subjective
judgments (docs/architecture/audits/2026-10-27-menu-design-review.md), not usability measurements;
the end card says so. Sound was checked by measurement only; real-time viewing was replaced by
consecutive-frame strips and per-frame measurements.

## Sources

- [Production README](production/README.md): eras, rebuild steps, capture notes and limits, revisions
  and the viewer pass.
- [Edit](production/sources/promo/edit.py) (promo_kit compositor): brief and beat sheet in its docstring,
  every score with its round, date and audit section, audio prep and the master/MP4 commands.
  Superseded edit snapshots: `production/sources/promo/revisions/edit.r2.py`, `edit.r3.py`; `edit.r3b.py` = final.
- Chapters, edit list and UI cue map: `production/sources/promo/{{chapters.txt,edl.csv,cues.json}}`.
- Capture: `production/sources/capture/capture.py`, the recorders (`java/` for 2f9ca84b1 and d823ce643; `java05/`
  for 0.5 with its EGL compatibility shim) and the beat-grid take recipes `takes/*.take`.
- Capture records: `production/clips/<era>/<take>/{{events.csv,provenance.json,take.txt,state.csv}}`.
- Provenance: `production/provenance/source-map.json` (commits, build commands, ROM identities, fonts, tools),
  `production/provenance/deliverables.json` (film/master hashes).

## External, not uploaded

[external-assets.json](external-assets.json) hashes the film, master and superseded revisions, every
native frame sequence, the ROM-derived music/SFX renders, the synthesised UI tones, review images and
the Fira faces. ROMs, compiled trees, the Python environment and logs are excluded.
"""


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    files = source_files()
    sources = []
    for rel in files:
        dst = PROJ / 'production' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROD / rel, dst)
        sources.append(dict(path=f'projects/{PID}/production/{rel}', root=ROOT_ID, original_path=rel,
                            bytes=dst.stat().st_size, sha256=sha(dst), snapshot='byte-copy'))
    (PROJ / 'README.md').write_text(INDEX.format(date=DATE))
    assets = external_assets()
    (PROJ / 'external-assets.json').write_text(json.dumps(dict(
        project=PID, snapshot_date=DATE,
        notes='External bytes hashed at archive time, not uploaded. build/ render work, compiled engine trees '
              '(target/eras, target/promo-helpers), the Python venv, logs and ROMs are excluded.',
        sequence_hash='inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append UTF-8 basename + '
                      'NUL + decimal byte length + NUL + lowercase SHA-256 + LF (review/**: relative path instead '
                      'of basename when basenames repeat).',
        assets=assets), indent=1) + '\n')
    for name in ['README.md', 'external-assets.json']:
        p = PROJ / name
        sources.append(dict(path=f'projects/{PID}/{name}', root=ROOT_ID, original_path=f'archive-payload/projects/{PID}/{name}',
                            bytes=p.stat().st_size, sha256=sha(p), snapshot='generated index'))
    frag = OUT / 'catalog-fragments'
    frag.mkdir(parents=True)
    (frag / 'projects.json').write_text(json.dumps([dict(
        id=PID, title='ROAD TO 9: menu evolution promo',
        notes='Training-montage promo of the engine menus across OpenGGF 0.5, the pre-redesign 0.7 menus and the '
              'delivered redesign, with dated design-review scores; edit, recorders, take recipes, capture records '
              'and provenance. Film, master, frames, ROM-derived audio and fonts remain external. Listening and '
              'real-time viewing not claimed.',
        source_files=len(sources), catalog_entries=len(assets))], indent=1) + '\n')
    (frag / 'roots.json').write_text(json.dumps([
        dict(id=ROOT_ID, original=str(PROD), archive=f'projects/{PID}/production',
             notes='Menu evolution promo production root: byte-preserved edit, recorders, takes, capture records and '
                   'provenance. Film, master, native frame sequences, ROM-derived audio, synthesised UI tones and '
                   'review images remain external.'),
        dict(id=FONT_ROOT, original=str(FONTS), archive='',
             notes='External Fira editorial faces (system package ttf-fira-sans 4.301, OFL); hashed, not redistributed.')],
        indent=1) + '\n')
    (frag / 'sources.json').write_text(json.dumps(sources, indent=1) + '\n')
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    for a in assets:
        w.writerow([PID, a['root'], a['path'], a['kind'], a['bytes'], a['files']])
    (frag / 'assets.csv').write_text(buf.getvalue())
    (frag / 'README-row.md').write_text(f'| [ROAD TO 9: menu evolution promo](projects/{PID}/) | {len(sources)} | {len(assets)} |\n')
    print(f'{len(sources)} sources, {len(assets)} external entries -> {OUT}')


def verify(media):
    media = Path(media)
    scratch = PROD / 'build' / 'media-verify'
    if scratch.exists():
        shutil.rmtree(scratch)
    for part in ['catalog', 'tools', 'projects']:
        shutil.copytree(media / part, scratch / part, symlinks=True)
    shutil.copytree(PROJ, scratch / 'projects' / PID)
    frag = OUT / 'catalog-fragments'
    for name in ['projects.json', 'roots.json', 'sources.json']:
        merged = json.loads((scratch / 'catalog' / name).read_text())
        ids = {x.get('id') or x.get('path') for x in merged}
        new = json.loads((frag / name).read_text())
        if any((x.get('id') or x.get('path')) in ids for x in new):
            raise SystemExit(f'{name}: id collision with the existing catalog')
        (scratch / 'catalog' / name).write_text(json.dumps(merged + new, indent=1) + '\n')
    with (scratch / 'catalog' / 'assets.csv').open('a') as fh:
        fh.write((frag / 'assets.csv').read_text())
    r = subprocess.run([sys.executable, 'tools/catalog.py', 'verify'], cwd=scratch, capture_output=True, text=True)
    print(r.stdout + r.stderr)
    shutil.rmtree(scratch)
    return r.returncode


if __name__ == '__main__':
    build()
    if '--verify-against' in sys.argv:
        sys.exit(verify(sys.argv[sys.argv.index('--verify-against') + 1]))
