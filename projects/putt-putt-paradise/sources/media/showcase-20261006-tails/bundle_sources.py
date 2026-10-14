"""Bundle the verified 2026-10-06 golf showcase; no ROMs or Maven diagnostics."""
from pathlib import Path
import hashlib, zipfile
root = Path(__file__).resolve().parent
files = [root / name for name in (
    'README.md', 'build-reference.json', 'assemble.py', 'capture_runs.py',
    'encode_sources.py', 'bundle_sources.py', 'edit-list.json', 'chapters.csv',
    'reel-probe.json', 'cadence.json', 'capture-checks.json', 'state-comparison.json', 'cut-contact-sheet.png',
    'verify_sources.py', 'verify_reel.py', 'effect-checks.json', 'browser-qa.json',
    'tails-visibility-checks.json', 'source/GolfShowcaseCapture.java', 'source/putt-putt-paradise.jar')]
for capture in sorted(root.glob('*-final-v5')):
    files.extend(capture / name for name in (
        'gameplay.mkv', 'title.mkv', 'input.script', 'input.bk2',
        'state.csv', 'events.csv', 'provenance.json'))
files.extend(root / 'ehz1-sonic-rewind-final-v5' / name for name in ('rewind-raw.png', 'rewind-vhs.png'))
assert len(files)==len(set(files)) and all(f.is_file() for f in files)
checksums = ''.join(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' +
                    str(f.relative_to(root)) + '\n' for f in files)
(root / 'SHA256SUMS').write_text(checksums)
archive = root / 'putt-putt-paradise-source.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as z:
    for f in files + [root / 'SHA256SUMS']:
        z.write(f, str(f.relative_to(root)))
with zipfile.ZipFile(archive) as z:
    assert len(z.infolist()) == len(files)+1 and z.testzip() is None
    assert not any(n.lower().endswith(('.gen', '.bin', '.rom')) for n in z.namelist())
print(str(archive) + ': ' + str(archive.stat().st_size) + ' bytes; '+str(len(files)+1)+' verified entries')
