#!/usr/bin/env python3
"""Import a completed Chaos Mode gallery revision's sources and asset inventory.

Inputs: an explicit frozen revision-3 or revision-4 production directory.
Origin: Chaos gallery follow-ups, 2026-10-14. Copies bounded production text only;
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
ARCHIVE_ROOT = 'projects/' + PROJECT + '/sources/media/'
SUPPORTED_REVISIONS = {'revision-3', 'revision-4'}
MAX_SOURCE_BYTES = 1024 * 1024
MEDIA_SUFFIXES = {'.mp4', '.mkv', '.mov', '.webm', '.avi', '.wav', '.pcm',
                  '.flac', '.mp3', '.ogg', '.aac', '.png', '.jpg', '.jpeg',
                  '.webp', '.ttf', '.otf', '.jar', '.zip', '.bk2', '.csv'}
EXCLUDED_PARTS = {'__pycache__', '.venv', 'target', 'work', '.git', 'build',
                  'classes', 'test-classes', 'node_modules', 'temporary-agents'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive_data(directory, relative, data):
    """Relocate only revision-4 JSON paths; preserve proof values and original hash."""
    if directory.name != 'revision-4' or relative.suffix != '.json':
        return data, {}
    home = Path.home()
    engine = home / 'code/projects/OpenGGF'
    mappings = [
        (str(directory.parent), '${CHAOS_MEDIA_ROOT}'),
        (str(engine / '.worktrees/ai-chaos-reel-v4'), '${CHAOS_WORKTREE}'),
        (str(engine / 'Sonic and Knuckles & Sonic 3 (W) [!].gen'), '${S3K_ROM}'),
        (str(home / '.m2/repository'), '${MAVEN_REPOSITORY}'),
        (str(engine), '${OPENGGF_QUEUE_ROOT}'),
        (str(home), '${ORIGINAL_HOME}'),
    ]
    text = data.decode('utf-8')
    applied = {}
    for original, alias in mappings:
        if original in text:
            if alias in text:
                raise ValueError(f'Ambiguous path alias in {relative}: {alias}')
            text = text.replace(original, alias)
            applied[alias] = original
    normalized = text.encode('utf-8')
    if applied:
        json.loads(normalized)
        restored = text
        for alias, original in reversed(list(applied.items())):
            restored = restored.replace(alias, original)
        if restored.encode('utf-8') != data:
            raise ValueError('Path normalization is not reversible: ' + str(relative))
    return normalized, applied


def production_text(relative):
    """Keep plans/recipes/provenance, excluding bulk state and temporary work."""
    if relative.parts[0] == 'mod-source' and relative.suffix in {'.java', '.yaml'}:
        return True
    if relative.parts[0] == 'audio-source' and (
            relative.suffix in {'.java', '.yaml'} or relative.name.endswith('.java.in')):
        return True
    if relative.suffix in {'.py', '.md'}:
        return True
    if relative.suffix == '.json':
        return True
    if relative.parts[0] == 'captures' and relative.name in {
            'input.script', 'input.txt', 'settings.txt', 'config.yaml'}:
        return True
    if relative.parts[0] == 'out' and relative.name in {'chapters.csv', 'chapters.txt'}:
        return True
    return relative.parts[0] == 'assets' and relative.suffix == '.txt'


def collect(directory):
    sources, assets, image_sets, omitted = [], [], {}, []
    revision = directory.name
    for path in sorted(directory.rglob('*')):
        relative = path.relative_to(directory)
        if path.is_symlink():
            raise ValueError(f'Symlink needs explicit review: {relative}')
        if not path.is_file():
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts) or path.suffix == '.log':
            continue
        if any(part.startswith('.') for part in relative.parts):
            raise ValueError(f'Hidden file needs explicit review: {relative}')
        # Retain only the actual Chaos preference recipe; native creator scene
        # saves and general host configuration are regenerable/private state.
        chaos_settings = (relative.parts[0] == 'captures'
                          and relative.parts[2:] == ('saves', 'mods', PROJECT, 'settings.txt'))
        if 'saves' in relative.parts and not chaos_settings:
            continue
        if relative.parts[0] != 'captures' and path.name in {'config.yaml', 'config.yml'}:
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
                    path=revision + '/' + relative.as_posix(),
                    kind='generated state/diagnostic data' if path.suffix == '.csv' else 'media dependency',
                    bytes=str(size), files='1'))
        else:
            omitted.append(relative.as_posix())
    for (directory_path, suffix), (size, count) in sorted(image_sets.items()):
        assets.append(dict(project=PROJECT, root=ROOT_ID,
            path=revision + '/' + (directory_path / ('*' + suffix)).as_posix(),
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
    revision = directory.name
    if revision not in SUPPORTED_REVISIONS or not directory.is_dir():
        parser.error('Expected an explicit completed revision-3 or revision-4 production directory')
    prefix = ARCHIVE_ROOT + revision + '/'
    preserved = load_catalog('sources.json')
    earlier = [row for row in preserved if row['root'] == ROOT_ID and not row['path'].startswith(prefix)]
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
    expected_paths = {prefix + relative.as_posix() for relative, _ in sources}
    target = ROOT / prefix
    if target.exists():
        unexpected = [str(path.relative_to(ROOT)) for path in target.rglob('*')
                      if path.is_file() and str(path.relative_to(ROOT)) not in expected_paths]
        if unexpected:
            raise ValueError('Existing ' + revision + ' files need accounting: ' + ', '.join(unexpected))
    updated = [row for row in preserved if not row['path'].startswith(prefix)]
    for relative, data in sources:
        # Detect source edits during inventory instead of archiving a mixed state.
        if (directory / relative).read_bytes() != data:
            raise ValueError('Production changed during import: ' + str(relative))
        archived_data, normalization = archive_data(directory, relative, data)
        archived = ROOT / prefix / relative
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_bytes(archived_data)
        row = dict(path=prefix + relative.as_posix(), root=ROOT_ID,
            original_path=revision + '/' + relative.as_posix(), bytes=len(archived_data),
            sha256=digest(archived_data), snapshot='byte-copy')
        if normalization:
            row.update(snapshot='path-normalized-json', original_sha256=digest(data),
                       normalization=normalization)
        updated.append(row)
    save_catalog('sources.json', updated)
    asset_file = ROOT / 'catalog/assets.csv'
    original_csv = asset_file.read_bytes()
    line_ending = '\r\n' if b'\r\n' in original_csv else '\n'
    with asset_file.open(newline='') as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        assets = [row for row in reader if not (row['root'] == ROOT_ID and row['path'].startswith(revision + '/'))]
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
    has_revision4 = any(row['path'].startswith(ARCHIVE_ROOT + 'revision-4/') for row in updated)
    if has_revision4:
        project['notes'] = ('Earlier Chaos reels and source identities preserved. Revision 4 retains '
                            'the focused representative gallery, native ring-repulsion demonstration '
                            'and production music/DAC/SFX capture recipes and qualification. '
                            'The example mod pool is unchanged; footage and extracted assets remain external.')
    project['source_files'] = sum(row['root'] == ROOT_ID for row in updated)
    project['catalog_entries'] = sum(row['project'] == PROJECT for row in assets)
    save_catalog('projects.json', project_rows)
    roots = load_catalog('roots.json')
    next(row for row in roots if row['id'] == ROOT_ID)['notes'] = (
        'First reel preserved. revision-2 contains the rapid-fire edit; revision-2-draft-20261014 '
        'is its pre-refresh snapshot. revision-3 contains the completed labelled gallery and '
        'varied-zone capture sources under the same original media root.')
    if has_revision4:
        next(row for row in roots if row['id'] == ROOT_ID)['notes'] += (
            ' revision-4 retains the focused gallery and production audio correction; '
            'all earlier revision directories remain intact.')
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
