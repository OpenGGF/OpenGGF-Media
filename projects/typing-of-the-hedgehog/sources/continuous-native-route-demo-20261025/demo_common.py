"""Shared file-only helpers for the spaced Typing route demo (2026-10-25).

Inputs are an existing checkout/capture; outputs stay in caller-owned external dirs.
No engine, JVM, Maven, media decoder or desktop is launched by these helpers.
"""
import csv
import hashlib
import json
import struct
from pathlib import Path

FPS = 60
BASE_HEAD = '96aaffb697aefed688b3281389444e3842dd1e76'
STATE_COLUMNS = 'frame,x,y,xvel,yvel,gspeed,air,rolling,spindash,hurt,dead,rings,mapping_frame,cam_x,cam_y,sk_present,sk_x,sk_y,high_priority,mode,input'.split(',')


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def json_new(path, data):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def file_tree(root, paths=None):
    root = Path(root)
    files = sorted(paths if paths is not None else (p for p in root.rglob('*') if p.is_file()))
    listing = {p.relative_to(root).as_posix(): sha256(p) for p in files}
    digest = hashlib.sha256(json.dumps(listing, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'sha256': digest, 'count': len(listing), 'files': listing}


def read_state(path, expected=None):
    with Path(path).open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        header = reader.fieldnames
        # Direct-level capture is deliberately pinned; fail on silent schema drift.
        if header != STATE_COLUMNS:
            raise ValueError(f'Unexpected direct-level CSV schema: {header!r}')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty state CSV')
    for expected_frame, row in enumerate(rows):
        if int(row['frame']) != expected_frame or None in row or any(v is None for v in row.values()):
            raise ValueError(f'Nonconsecutive/malformed row at frame {expected_frame}')
    if expected is not None and len(rows) != expected:
        raise ValueError(f'Incomplete capture: expected {expected} rows, found {len(rows)}')
    return rows


def png_size(path):
    with Path(path).open('rb') as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
        raise ValueError(f'Not a PNG: {path}')
    return struct.unpack('>II', header[16:24])


def frames_summary(root, expected, width):
    folder = Path(root) / 'frames'
    files = sorted(folder.glob('*.png'), key=lambda p: int(p.stem))
    wanted = [folder / f'{i:05d}.png' for i in range(expected)]
    if files != wanted:
        raise ValueError('Frames must be exactly 00000.png through the last CSV row, without gaps/extras')
    if any(png_size(p) != (width, 224) for p in files):
        raise ValueError('Unexpected source PNG dimensions')
    result = file_tree(folder, files)
    # Retain a compact aggregate rather than 3,600 per-frame hash records.
    result.pop('files')
    result['width'], result['height'] = width, 224
    return result


def external_new_dir(path, checkout=None):
    path = Path(path).expanduser().resolve()
    if checkout is not None and path.is_relative_to(Path(checkout).resolve()):
        raise ValueError('Durable output must be outside the checkout')
    path.mkdir(parents=True, exist_ok=False)
    return path
