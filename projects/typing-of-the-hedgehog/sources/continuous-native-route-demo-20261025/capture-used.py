#!/usr/bin/env python3
"""Plan/capture the spaced Typing route demo using real GameplayCaptureTool.

Origin: 2026-10-25 replacement route demo. No compile/package/test is performed.
Default is a read-only plan; --execute launches a single queued EGL capture.
--record-build records inputs/artifacts AFTER the parent builds a stable candidate.
"""
import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from demo_common import (BASE_HEAD, FPS, external_new_dir, file_tree, frames_summary,
                         json_new, read_state, sha256)

SCOPES = ['pom.xml', '.mvn', 'src', 'examples/typing-of-the-hedgehog',
          'examples/build_example.py', 'tools/modding', 'tools/testing',
          'mod-api-release-policy.properties']
ROM_SHA1 = {
    's1': '69e102855d4389c3fd1a8f3dc7d193f8eee5fe5b',
    's2': '8bca5dcef1af3e00098666fd892dc1c2a76333f9',
    's3k': 'cfbf98c36c776677290a872547ac47c53d2761d6',
}
ZONE_SOURCES = {
    's1': 'src/main/java/com/openggf/game/sonic1/constants/Sonic1Constants.java',
    's2': 'src/main/java/com/openggf/game/sonic2/Sonic2LevelEventManager.java',
    's3k': 'src/main/java/com/openggf/game/sonic3k/constants/Sonic3kZoneIds.java',
}


def git(checkout, *args):
    return subprocess.check_output(['git', '-C', str(checkout), *args])


def artifact_identity(engine, sdk, head):
    identities = []
    for path, member in ((engine, 'version.properties'), (sdk, 'META-INF/openggf-build.properties')):
        with zipfile.ZipFile(path) as archive:
            text = archive.read(member).decode()
        identities.append(dict(line.split('=', 1) for line in text.splitlines()
                               if '=' in line and not line.startswith('#')))
    if identities[0] != identities[1]:
        raise ValueError('Engine and SDK have different recorded candidate identities')
    commit = identities[0].get('app.commit', '')
    if not commit or not head.startswith(commit):
        raise ValueError('Packaged candidate identity differs from the checkout HEAD')
    return identities[0]


def snapshot(checkout, mod, engine=None, sdk=None):
    raw = git(checkout, 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', *SCOPES)
    files = []
    for name in sorted(set(raw.decode().split('\0')) - {''}):
        path = checkout / name
        # Ignored build outputs must not enter source identity even if beneath a scope.
        if 'target' not in Path(name).parts and path.is_file():
            files.append(path)
    source = file_tree(checkout, files)
    source['head'] = git(checkout, 'rev-parse', 'HEAD').decode().strip()
    source['branch'] = git(checkout, 'branch', '--show-current').decode().strip()
    source['scoped_status'] = git(checkout, 'status', '--porcelain=v1', '--untracked-files=all', '--', *SCOPES).decode()
    classes = checkout / 'target/classes'
    if not (classes / 'com/openggf/tools/GameplayCaptureTool.class').is_file():
        raise ValueError('Parent must compile/package this checkout before recording a build')
    classes_id = file_tree(classes)
    classes_id.pop('files')
    artifacts = {}
    for key, path in [('mod', mod), ('engine', engine), ('sdk', sdk)]:
        if path is not None:
            path = Path(path).resolve(strict=True)
            artifacts[key] = {'path': str(path), 'sha256': sha256(path), 'bytes': path.stat().st_size}
    identity = artifact_identity(engine, sdk, source['head']) if engine and sdk else None
    return {'source': source, 'compiled_classes': classes_id, 'artifacts': artifacts,
            'packaged_candidate_identity': identity}


def comparable(value):
    # Relocation is allowed; byte identity is authoritative.
    return {'source': value['source'], 'compiled_classes': value['compiled_classes'],
            'packaged_candidate_identity': value['packaged_candidate_identity'],
            'artifacts': {k: {'sha256': v['sha256'], 'bytes': v['bytes']} for k, v in value['artifacts'].items()}}


def resolve_zone(checkout, game, value):
    if re.fullmatch(r'\d+|0[xX][0-9a-fA-F]+', value):
        return int(value, 16 if value.lower().startswith('0x') else 10)
    source = (checkout / ZONE_SOURCES[game]).read_text()
    match = re.search(r'\bZONE_' + re.escape(value.upper()) + r'\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*;', source)
    if not match:
        raise ValueError(f'Cannot resolve {game} zone {value!r}; use its zero-based numeric zone ID')
    return int(match.group(1), 16 if match.group(1).startswith('0x') else 10)


def resolve_rom(root, explicit, game):
    root = root.expanduser().resolve(strict=True)
    candidates = [explicit.expanduser().resolve(strict=True)] if explicit else sorted(
        p for p in root.iterdir() if p.is_file() and p.suffix.lower() in {'.gen', '.bin', '.md'})
    for path in candidates:
        if not path.is_relative_to(root):
            raise ValueError('--rom must identify an original file within --rom-root')
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        if digest == ROM_SHA1[game]:
            return path, digest
    raise ValueError(f'No matching original {game} ROM under {root}; expected SHA-1 {ROM_SHA1[game]}')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout', type=Path, required=True)
    p.add_argument('--mod-jar', type=Path, required=True)
    p.add_argument('--engine-jar', type=Path, help='Matching packaged engine, recorded as a build dependency')
    p.add_argument('--sdk-jar', type=Path, help='Matching packaged SDK used to compile the mod')
    action = p.add_mutually_exclusive_group()
    action.add_argument('--record-build', type=Path, help='Write a NEW build record and scoped dirty patch; never launches Java')
    action.add_argument('--execute', action='store_true', help='Run queued Java25 probe and capture; otherwise print a plan')
    p.add_argument('--build-record', type=Path, help='Record made immediately after the parent built this exact source/artifact set')
    p.add_argument('--rom-root', type=Path)
    p.add_argument('--rom', type=Path, help='Optional exact original ROM; otherwise identify immediate children by SHA-1')
    p.add_argument('--out-dir', type=Path)
    p.add_argument('--game', choices=ROM_SHA1, default='s2')
    p.add_argument('--zone', default='htz', help='Zero-based ID or native short constant name; default Hill Top')
    p.add_argument('--act', type=int, default=2, choices=(1, 2, 3), help='One-based; intent uses act-1')
    p.add_argument('--frames', type=int, default=3600, help='Outer input rows; every row is drawn/captured at 60 Hz')
    p.add_argument('--width', type=int, choices=(320, 352, 400, 528, 800), default=400)
    p.add_argument('--seed', type=int, default=5)
    p.add_argument('--java-home', type=Path, default=os.environ.get('JAVA_HOME'))
    a = p.parse_args()
    checkout = a.checkout.expanduser().resolve(strict=True)
    mod = a.mod_jar.expanduser().resolve(strict=True)
    if a.record_build:
        if not a.engine_jar or not a.sdk_jar:
            p.error('--record-build requires the matching --engine-jar and --sdk-jar')
        record = a.record_build.expanduser().resolve()
        if record.is_relative_to(checkout):
            p.error('Build record belongs in an external task directory')
        record.parent.mkdir(parents=True, exist_ok=True)
        patch = record.with_suffix('.patch')
        if record.exists() or patch.exists():
            p.error('Build record or patch exists; choose a new name')
        state = snapshot(checkout, mod, a.engine_jar, a.sdk_jar)
        with patch.open('xb') as stream:
            stream.write(git(checkout, 'diff', '--binary', 'HEAD', '--', *SCOPES))
        json_new(record, {'kind': 'parent_build_input_and_artifact_record', 'created_utc': datetime.now(timezone.utc).isoformat(),
                          'intended_base': BASE_HEAD, 'checkout_at_record': str(checkout), 'snapshot': state,
                          'dirty_patch': patch.name,
                          'limit': 'Attests byte identities after parent build; does not prove build causality. Preserve untracked source bytes separately or commit them.'})
        print(f'Build identity recorded: {record}\nNo JVM/build/capture was launched.')
        return
    if not a.rom_root or not a.out_dir or not a.build_record:
        p.error('Capture/plan requires --rom-root, --out-dir and --build-record')
    if a.frames < 1:
        p.error('--frames must be positive')
    if sys.platform != 'linux':
        p.error('This display-free EGL recipe requires Linux; no ambient-display fallback exists')
    build_path = a.build_record.expanduser().resolve(strict=True)
    build = json.loads(build_path.read_text())
    expected = build['snapshot']
    engine = Path(expected['artifacts']['engine']['path'])
    sdk = Path(expected['artifacts']['sdk']['path'])
    # Optional new paths support relocating artifacts from the recorded build.
    engine = a.engine_jar or engine
    sdk = a.sdk_jar or sdk
    before = snapshot(checkout, mod, engine, sdk)
    if comparable(before) != comparable(expected):
        raise ValueError('Sources/classes/artifacts differ from the recorded build; finish edits, rebuild, record a new identity')
    rom, rom_sha1 = resolve_rom(a.rom_root, a.rom, a.game)
    zone = resolve_zone(checkout, a.game, a.zone)
    out = a.out_dir.expanduser().resolve()
    if out.exists() or out.is_relative_to(checkout):
        raise ValueError('Use a NEW external capture output directory')
    prefs = out / 'preferences'
    intent = dict(mode='ARCADE', game=a.game, zone=zone, act=a.act-1, difficulty='NORMAL',
                  capitals='false', punctuation='false', dictionaries='standard', seed=a.seed,
                  bossStars=1, noFail='true', slowMotion='false', voice='OFF', demo='true', demoRows=0)
    tool_args = ['--game', a.game, '--rom', str(rom), '--mod', str(mod), '--zone', str(zone), '--act', str(a.act),
                 '--width', str(a.width), '--main', 'sonic', '--sidekick', 'none', '--donor', 'off',
                 '--frames', str(a.frames), '--capture-from', '0', '--every', '1', '--fps', str(FPS),
                 '--stop-on-death', 'true', '--death-grace', '60', '--no-video', '--out-dir', str(out)]
    # exec:java uses Plexus quote parsing, not a shell. Reject ambiguous quote characters.
    if any(any(c in v for c in ('\n', '\r', "'", '"')) for v in tool_args):
        raise ValueError('Tool argument paths cannot contain quotes or newlines; spaces are supported')
    exec_args = ' '.join('"' + v + '"' for v in tool_args)
    queue = [sys.executable, str(checkout / 'tools/testing/maven_queue.py')]
    command = [*queue, '-Dmse=off', '-Djava.awt.headless=true', '-Dopenggf.headless.gl=surfaceless-egl',
               '-Dopenggf.saveRoot=' + str(prefs), 'exec:java',
               '-Dexec.mainClass=com.openggf.tools.GameplayCaptureTool', '-Dexec.args=' + exec_args]
    print('cwd:', checkout)
    print('env: DISPLAY/WAYLAND_DISPLAY removed; JAVA_HOME:', a.java_home or '(inherited Java via PATH; checked through queue)')
    print('intent:', json.dumps(intent))
    print('queued version probe:', shlex.join([*queue, '-v']))
    print('capture:', shlex.join(command))
    print('Audio: GameplayCaptureSession disables synthesis; HeadlessGameBoot installs NullAudioBackend before playback. No --audio.')
    if not a.execute:
        print('PLAN ONLY: no outputs, JVM, queue request or capture created.')
        return
    env = os.environ.copy()
    env.pop('DISPLAY', None)
    env.pop('WAYLAND_DISPLAY', None)
    env.pop('WAYLAND', None)
    if a.java_home:
        env['JAVA_HOME'] = str(Path(a.java_home).expanduser().resolve(strict=True))
        env['PATH'] = str(Path(env['JAVA_HOME']) / 'bin') + os.pathsep + env.get('PATH', '')
    probe = subprocess.run([*queue, '-v'], cwd=checkout, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
    print(probe.stdout)
    if not re.search(r'Java version:\s*25(?:\D|$)', probe.stdout):
        raise ValueError('Queued Maven probe did not report Java 25')
    out = external_new_dir(out, checkout)
    provenance = out / 'provenance'
    provenance.mkdir()
    storage = prefs / 'mods/typing-of-the-hedgehog'
    storage.mkdir(parents=True)
    intent_text = ''.join(f'{k}={v}\n' for k, v in intent.items())
    (storage / 'intent.txt').write_text(intent_text)
    (provenance / 'intent.txt').write_text(intent_text)  # Course consumes its storage copy.
    json_new(provenance / 'build-record.json', build)
    patch_path = build_path.parent / build['dirty_patch']
    (provenance / 'source.patch').write_bytes(patch_path.read_bytes())
    manifest = {'status': 'capture_pending', 'route_qualified': None, 'fps': FPS, 'every': 1, 'capture_from': 0,
                'frames_requested': a.frames, 'game': a.game, 'zone': zone, 'act_one_based': a.act,
                'width': a.width, 'height': 224, 'main': 'sonic', 'sidekick': 'none', 'donor': 'off',
                'entry': 'direct native level boot; mod selects its course section; no positioned CLI seed',
                'source_kind': 'GameplayCaptureTool actual selected-section attract gameplay',
                'audio': 'silent; synthesis disabled; NullAudioBackend through HeadlessGameBoot',
                'rom': {'original_path': str(rom), 'sha1': rom_sha1, 'sha256': sha256(rom)},
                'intent': intent, 'snapshot_before': before,
                'driver_sources': {name: sha256(Path(__file__).parent / name) for name in ('capture.py', 'demo_common.py')}, 'command_argv': command, 'tool_args': tool_args,
                'environment': {'DISPLAY': None, 'WAYLAND_DISPLAY': None, 'JAVA_HOME': env.get('JAVA_HOME')},
                'started_utc': datetime.now(timezone.utc).isoformat()}
    # Persist a useful pending record even if capture fails; never overwrite final identity.
    json_new(provenance / 'capture.pending.json', manifest)
    capture_log = checkout / 'target' / ('typing-demo-' + out.name + '.log')
    with capture_log.open('x') as log:
        result = subprocess.run(command, cwd=checkout, env=env, stdout=log, stderr=subprocess.STDOUT)
    manifest['returncode'] = result.returncode
    manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
    manifest['status'] = 'capture_failed_or_incomplete'
    manifest['fingerprint_unchanged'] = False
    try:
        after = snapshot(checkout, mod, engine, sdk)
        manifest['snapshot_after'] = after
        manifest['fingerprint_unchanged'] = comparable(before) == comparable(after)
        if result.returncode != 0:
            raise ValueError(f'Capture process exited {result.returncode}; inspect {capture_log}')
        if not manifest['fingerprint_unchanged']:
            raise ValueError('Source/classes/artifacts changed during queue wait/capture; outputs cannot be attributed to the build record')
        rows = read_state(out / 'state.csv', a.frames)
        manifest['outputs'] = {'state_sha256': sha256(out / 'state.csv'), 'rows': len(rows),
                               'frames': frames_summary(out, len(rows), a.width)}
        manifest['status'] = 'capture_complete_route_review_pending'
    except Exception as exc:
        manifest['error'] = str(exc)
        raise
    finally:
        json_new(provenance / 'capture.json', manifest)
    print(f'Captured {a.frames} rows. Route qualification/phase boundaries/visual correctness remain PENDING: {out}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        sys.exit(str(exc))
