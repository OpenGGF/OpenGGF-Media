#!/usr/bin/env python3
"""Import the completed Chaos Mode revision-3 production sources and asset inventory.

Inputs: a frozen revision-3 directory under the original Chaos media root.
Origin: Chaos gallery follow-up, 2026-10-14. Copies bounded production text only;
media bytes remain external. Earlier production revisions and catalog rows stay
unchanged. Run only after capture, edit and qualification files are frozen.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'sonic3k-chaos-mode'
ROOT_ID = PROJECT + '/media'
PREFIX = 'projects/' + PROJECT + '/sources/media/revision-3/'
MAX_SOURCE_BYTES = 1024 * 1024
MEDIA_SUFFIXES = {'.mp4', '.mkv', '.mov', '.webm', '.avi', '.wav', '.pcm',
                  '.flac', '.mp3', '.ogg', '.aac', '.png', '.jpg', '.jpeg',
                  '.webp', '.ttf', '.otf', '.jar', '.zip', '.bk2', '.csv'}
EXCLUDED_PARTS = {'__pycache__', '.venv', 'target', 'work', '.git'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def production_text(relative):
    """Keep plans/recipes/provenance, excluding bulk state and temporary work."""
    if relative.parts[0] == 'mod-source' and relative.suffix in {'.java', '.yaml'}:
        return True
    if relative.suffix in {'.py', '.md'}:
        return True
    if relative.suffix == '.json':
        return True
    if relative.name in {'input.script', 'input.txt', 'settings.txt', 'config.yaml'}:
        return True
    if relative.parts[0] == 'out' and relative.name in {'chapters.csv', 'chapters.txt'}:
        return True
    return relative.parts[0] == 'assets' and relative.suffix == '.txt'


def collect(directory):
    sources, assets, image_sets, omitted = [], [], {}, []
    for path in sorted(directory.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(directory)
        if path.is_symlink():
            raise ValueError(f'Symlink needs explicit review: {relative}')
        if any(part in EXCLUDED_PARTS for part in relative.parts) or path.suffix == '.log':
            continue
        size = path.stat().st_size
        if production_text(relative) and size <= MAX_SOURCE_BYTES:
            sources.append((relative, path.read_bytes()))
        elif path.suffix.lower() in MEDIA_SUFFIXES:
            if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}:
                key = (relative.parent, path.suffix.lower())
                measured = image_sets.setdefault(key, [0, 0])
                measured[0] += size
                measured[1] += 1
            else:
                assets.append(dict(project=PROJECT, root=ROOT_ID,
                    path='revision-3/' + relative.as_posix(),
                    kind='generated state/diagnostic data' if path.suffix == '.csv' else 'media dependency',
                    bytes=str(size), files='1'))
        else:
            omitted.append(relative.as_posix())
    for (directory_path, suffix), (size, count) in sorted(image_sets.items()):
        assets.append(dict(project=PROJECT, root=ROOT_ID,
            path='revision-3/' + (directory_path / ('*' + suffix)).as_posix(),
            kind='frame-sequence' if directory_path.name == 'frames' else 'image-sequence-or-review-set',
            bytes=str(size), files=str(count)))
    return sources, assets, omitted


def load_catalog(name):
    return json.loads((ROOT / 'catalog' / name).read_text())


def save_catalog(name, value):
    (ROOT / 'catalog' / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--write', action='store_true', help='Copy the frozen sources and update catalogs')
    args = parser.parse_args()
    directory = args.directory.resolve()
    if directory.name != 'revision-3' or not directory.is_dir():
        parser.error('Expected the completed revision-3 production directory')
    preserved = load_catalog('sources.json')
    earlier = [row for row in preserved if row['root'] == ROOT_ID and not row['path'].startswith(PREFIX)]
    for row in earlier:
        data = (ROOT / row['path']).read_bytes()
        if len(data) != row['bytes'] or digest(data) != row['sha256']:
            raise ValueError('Earlier production source changed: ' + row['path'])
    sources, new_assets, omitted = collect(directory)
    if omitted:
        raise ValueError('Unclassified files need explicit review: ' + ', '.join(omitted))
    print(f'{len(sources)} production text sources; {len(new_assets)} external asset/sequence rows; '
          f'{len(earlier)} earlier Chaos sources unchanged.')
    if not args.write:
        print('Read-only inventory; source copy and catalogs unchanged.')
        return 0
    required = {'PLAN.md', 'README.md', 'capture.py', 'assemble.py', 'cards.json', 'captures.json', 'audio.json'}
    missing = required - {relative.as_posix() for relative, _ in sources}
    if missing:
        raise ValueError('Incomplete production: ' + ', '.join(sorted(missing)))
    expected_paths = {PREFIX + relative.as_posix() for relative, _ in sources}
    target = ROOT / PREFIX
    if target.exists():
        unexpected = [str(path.relative_to(ROOT)) for path in target.rglob('*')
                      if path.is_file() and str(path.relative_to(ROOT)) not in expected_paths]
        if unexpected:
            raise ValueError('Existing revision-3 files need accounting: ' + ', '.join(unexpected))
    updated = [row for row in preserved if not row['path'].startswith(PREFIX)]
    for relative, data in sources:
        # Detect source edits during inventory instead of archiving a mixed state.
        if (directory / relative).read_bytes() != data:
            raise ValueError('Production changed during import: ' + str(relative))
        archived = ROOT / PREFIX / relative
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_bytes(data)
        updated.append(dict(path=PREFIX + relative.as_posix(), root=ROOT_ID,
            original_path='revision-3/' + relative.as_posix(), bytes=len(data),
            sha256=digest(data), snapshot='byte-copy'))
    save_catalog('sources.json', updated)
    asset_file = ROOT / 'catalog/assets.csv'
    original_csv = asset_file.read_bytes()
    line_ending = '\r\n' if b'\r\n' in original_csv else '\n'
    with asset_file.open(newline='') as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        assets = [row for row in reader if not (row['root'] == ROOT_ID and row['path'].startswith('revision-3/'))]
    assets.extend(new_assets)
    with asset_file.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        writer.writerows(assets)
    project_rows = load_catalog('projects.json')
    project = next(row for row in project_rows if row['id'] == PROJECT)
    project['title'] = 'Sonic 3&K Chaos Mode demo and card-gallery revisions'
    project['notes'] = ('First reel, rapid-fire revision 2 and its earlier blueprint preserved. '
                        'Revision 3 retains the calmer labelled gallery, varied-zone captures, '
                        'native ghost-finale audio and exact source/render qualification. '
                        'Footage and extracted assets remain external.')
    project['source_files'] = sum(row['root'] == ROOT_ID for row in updated)
    project['catalog_entries'] = sum(row['project'] == PROJECT for row in assets)
    save_catalog('projects.json', project_rows)
    roots = load_catalog('roots.json')
    next(row for row in roots if row['id'] == ROOT_ID)['notes'] = (
        'First reel preserved. revision-2 contains the rapid-fire edit; revision-2-draft-20261014 '
        'is its pre-refresh snapshot. revision-3 contains the completed labelled gallery and '
        'varied-zone capture sources under the same original media root.')
    save_catalog('roots.json', roots)
    readme = ROOT / 'README.md'
    text = readme.read_text()
    text = re.sub(r'([\d,]+) preserved source files', f'{len(updated):,} preserved source files', text)
    text = re.sub(r'\| \[Sonic 3&K Chaos Mode[^\n]+',
        f"| [{project['title']}](projects/{PROJECT}/) | {project['source_files']} | {project['catalog_entries']} |", text)
    readme.write_text(text)
    print('Frozen sources copied; source, project, root and external-asset catalogs refreshed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
