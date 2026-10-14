#!/usr/bin/env python3
"""Inspect the OpenGGF media source archive and external footage inventory.

Inputs: catalog/{projects,roots,sources}.json and assets.csv, relative to this file.
Origin: OpenGGF-Media initial archive, 2026-10-14. No media is read or modified.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_json(name):
    return json.loads((ROOT / 'catalog' / name).read_text())


def verify():
    errors = []
    seen = set()
    roots = {r['id']: r for r in read_json('roots.json')}
    sources = read_json('sources.json')
    for source in sources:
        relative = Path(source['path'])
        path = ROOT / relative
        if relative.is_absolute() or '..' in relative.parts or path.is_symlink():
            errors.append(f'Invalid source path: {relative}')
            continue
        if source['path'] in seen:
            errors.append(f'Duplicate source: {relative}')
        seen.add(source['path'])
        if source['root'] not in roots:
            errors.append(f'Unknown root: {relative}')
        try:
            data = path.read_bytes()
            if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
                errors.append(f'Source differs from import: {relative}')
            if path.name == 'Project.db':
                with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as db:
                    if db.execute('pragma integrity_check').fetchone() != ('ok',):
                        errors.append(f'Invalid Resolve database: {relative}')
        except (OSError, sqlite3.Error) as exc:
            errors.append(f'{relative}: {exc}')
    count = 0
    with (ROOT / 'catalog/assets.csv').open(newline='') as handle:
        for asset in csv.DictReader(handle):
            count += 1
            path = Path(asset['path'])
            if asset['root'] not in roots or path.is_absolute() or '..' in path.parts:
                errors.append(f"Invalid asset reference: {asset['root']}:{path}")
            minimum = 0 if asset['kind'] == 'empty-frame-directory' else 1
            if int(asset['bytes']) < 0 or int(asset['files']) < minimum:
                errors.append(f'Invalid asset measurements: {path}')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'{len(sources)} source hashes/sizes verified; Resolve databases intact; {count} external catalog entries valid.')
    print('External footage availability, contents and historical render claims were not verified.')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify')
    sub.add_parser('projects')
    assets = sub.add_parser('assets')
    assets.add_argument('project')
    assets.add_argument('--limit', type=int, default=30)
    args = parser.parse_args()
    if args.command == 'verify':
        return verify()
    projects = read_json('projects.json')
    if args.command == 'projects':
        for project in projects:
            print(f"{project['id']}: {project['title']} ({project['source_files']} sources)")
        return 0
    if args.project not in {p['id'] for p in projects}:
        parser.error('Unknown project; run the projects command to list IDs.')
    if args.limit < 1:
        parser.error('--limit must be positive.')
    with (ROOT / 'catalog/assets.csv').open(newline='') as handle:
        matched = [r for r in csv.DictReader(handle) if r['project'] == args.project]
    roots = {r['id']: r['original'] for r in read_json('roots.json')}
    for asset in matched[:args.limit]:
        print(f"{roots[asset['root']]}/{asset['path']} [{asset['kind']}; {asset['files']} file(s), {asset['bytes']} bytes]")
    print(f'Showing {min(args.limit, len(matched))} of {len(matched)} entries; these are external paths, not downloads.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
