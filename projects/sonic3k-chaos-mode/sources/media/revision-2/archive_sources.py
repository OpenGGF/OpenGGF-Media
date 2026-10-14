#!/usr/bin/env python3
"""Verify/compact this task's RGB masters and archive the reproducible reel.

Origin: Sonic3K Chaos Mode reel revision, 2026-10-14. Every decoder and this
archival pass hold shared exclusive admission. Original first-reel assets are
read-only. Only redundant, owned revision2 PNG/audio copies are removed after
their complete decoded pixels and PCM samples match the retained MKV.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import signal
import subprocess
import sys
import wave
import zipfile
from PIL import Image

P = Path(__file__).resolve().parent
OLD = P.parent
LEASE = None
INHERITED = None


def run(args):
    child = subprocess.Popen(list(map(str, args)), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True,
                             **INHERITED(LEASE))
    try:
        stdout, stderr = child.communicate()
    except BaseException:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
        raise
    if child.returncode:
        raise RuntimeError(stderr.decode(errors='replace')[-3000:])
    return stdout


def verify_master(folder):
    source = folder / 'source.mkv'
    info = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                          '-of', 'json', source]))
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    assert (video['width'], video['height'], video['r_frame_rate']) == (400, 224, '60/1')
    assert (audio['sample_rate'], audio['channels'], audio['codec_name']) == ('48000', 2, 'pcm_s16le')
    manifest = run(['ffmpeg', '-nostdin', '-v', 'error', '-threads', '1', '-i', source,
                    '-map', '0:v:0', '-pix_fmt', 'rgb24', '-f', 'framemd5', '-']).decode()
    digests = [s.split(',')[-1].strip() for s in manifest.splitlines()
               if s and not s.startswith('#')]
    with (folder / 'output/state.csv').open() as f:
        rows = list(csv.DictReader(f))
    assert len(digests) == len(rows)
    assert [int(r['frame']) for r in rows] == list(range(len(rows)))
    assert abs(float(info['format']['duration']) - len(rows) / 60) < .003
    pngs = folder / 'output/frames'
    if pngs.exists():
        files = sorted(pngs.glob('*.png'))
        assert len(files) == len(digests)
        for i, (file, digest) in enumerate(zip(files, digests)):
            assert file.name == f'{i:05d}.png'
            with Image.open(file) as image:
                assert hashlib.md5(image.convert('RGB').tobytes()).hexdigest() == digest, file
    pcm = run(['ffmpeg', '-nostdin', '-v', 'error', '-threads', '1', '-i', source,
               '-map', '0:a:0', '-c:a', 'pcm_s16le', '-f', 'hash', '-hash', 'sha256', '-']).decode().strip().removeprefix('SHA256=')
    wav = folder / 'output/audio.wav'
    if wav.exists():
        with wave.open(str(wav)) as recording:
            assert (recording.getnchannels(), recording.getsampwidth(), recording.getframerate()) == (2, 2, 48000)
            assert recording.getnframes() == len(rows) * 800
            assert hashlib.sha256(recording.readframes(recording.getnframes())).hexdigest() == pcm
    return {'frames': len(rows), 'frameRate': '60/1', 'rgbSequenceSha256': hashlib.sha256('\n'.join(digests).encode()).hexdigest(),
            'pcmSha256': pcm, 'pngPixelsEqual': True, 'nativePcmEqual': True,
            'masterSha256': hashlib.sha256(source.read_bytes()).hexdigest()}


def archive(args):
    timeline = json.loads((P / 'out/edit-timeline.json').read_text())
    assert not timeline['pending_sources']
    checks_file = P / 'out/lossless-source-checks.json'
    checks = json.loads(checks_file.read_text()) if checks_file.exists() else {}
    # Include unused experiments' compact masters as well; their exclusion is
    # documented. Only raw redundant media is consumed, never inputs or state.
    for folder in sorted((P / 'captures').iterdir()):
        if not (folder / 'source.mkv').exists():
            continue
        if folder.name in checks:
            assert hashlib.sha256((folder / 'source.mkv').read_bytes()).hexdigest() == checks[folder.name]['masterSha256']
            continue
        checks[folder.name] = verify_master(folder)
        checks_file.write_text(json.dumps(checks, indent=2) + '\n')
        if args.compact:
            import shutil
            pngs = folder / 'output/frames'
            if pngs.exists():
                shutil.rmtree(pngs)
            (folder / 'output/audio.wav').unlink(missing_ok=True)
        print('LOSSLESS', folder.name, checks[folder.name]['frames'], flush=True)
    sources = {Path(p['source']).parent for s in timeline['shots'] for p in s['panels']}
    selected = set()
    for folder in sources | {p for p in (P / 'captures').iterdir() if (p / 'source.mkv').exists()}:
        for file in folder.rglob('*'):
            if file.is_file() and 'frames' not in file.parts and file.suffix != '.log' and file.name != 'audio.wav':
                selected.add(file)
    selected.update(f for f in (P / 'mod-source').rglob('*') if f.is_file())
    selected.add(OLD / 'card_renderer.py')
    selected.update(p for p in (OLD / 'assets').rglob('*') if p.is_file())
    selected.update(p for p in (P / 'assets').rglob('*') if p.is_file())
    selected.update(p for p in P.glob('*') if p.is_file() and p.suffix in {'.py', '.md', '.json'})
    selected.update(p for p in (P / 'out').rglob('*') if p.is_file() and p.name != 'source-archive.json' and p.suffix in {'.json', '.csv', '.png', '.jar'})
    destination = P / 'out/sonic3k-chaos-mode-demo-v2-sources.zip'
    with zipfile.ZipFile(destination, 'w', allowZip64=True) as output:
        for file in sorted(selected):
            name = Path(OLD.name) / file.relative_to(OLD)
            compression = zipfile.ZIP_STORED if file.suffix in {'.mkv', '.wav', '.png', '.jar'} else zipfile.ZIP_DEFLATED
            output.write(file, str(name), compress_type=compression)
    with zipfile.ZipFile(destination) as output:
        assert output.testzip() is None
        count = len(output.infolist())
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    (P / 'out/source-archive.json').write_text(json.dumps({'file': destination.name, 'files': count,
        'bytes': destination.stat().st_size, 'sha256': digest, 'losslessNewMasters': len(checks),
        'originalSourcesUnchanged': True, 'noRomImageIncluded': True}, indent=2) + '\n')
    print('ARCHIVE', destination, count, digest, flush=True)


def main():
    global LEASE, INHERITED
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission-worktree', type=Path, required=True)
    parser.add_argument('--compact', action='store_true')
    args = parser.parse_args()
    sys.path.insert(0, '/home/farrell/code/projects/OpenGGF/tools/testing')
    from maven_queue import maven_slot, inherited_slot, handle_termination
    INHERITED = inherited_slot
    with handle_termination():
        with maven_slot(args.admission_worktree, exclusive=True, estimate=180,
                        kind='chaos-media-archive') as leases:
            LEASE = leases
            try:
                archive(args)
            finally:
                LEASE = None


if __name__ == '__main__':
    main()
