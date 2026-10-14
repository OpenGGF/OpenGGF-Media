#!/usr/bin/env python3
"""Native music/DAC and accepted ghost SFX for Chaos reel revision4, 2026-10-14.

Reuses Slay/Flappy's ModScene -> ctx.audio() -> ExampleModHarness/capture path,
not the legacy FmSfxRenderTool direct-read exporter. Engine/runtime/mod pool stay
unchanged. A fresh ghost capture observes its own native accepted admissions;
the borrowed music-stopped soundboard renders that exact event schedule. It is
not a recovered PCM stem or a guessed editorial cue schedule.

All javac, Java, capture, probe, decoder and encoder children hold/inherit the
same normal exclusive scheduler lease for the provided owned worktree. Output
logs and compiled classes belong only in that worktree's target/. Durable inputs,
captured sources, WAVs and production provenance stay under this revision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
QUEUE = Path(os.environ.get('OPENGGF_QUEUE_ROOT', '/home/farrell/code/projects/OpenGGF'))
sys.path.insert(0, str(QUEUE / 'tools/testing'))
from maven_queue import handle_termination, inherited_slot, maven_slot
from verify_audio import accepted_schedule, compare_states, dac_proof, sha256, verify_sfx_replay


def run(command, cwd, log, lease, env):
    started = datetime.now(timezone.utc).isoformat()
    with log.open('w') as output:
        child = subprocess.Popen(list(map(str, command)), cwd=cwd, env=env,
                                 stdout=output, stderr=subprocess.STDOUT,
                                 start_new_session=True, **inherited_slot(lease))
        try:
            code = child.wait()
        except BaseException:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                child.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            raise
    result = dict(pid=child.pid, cwd=str(cwd), startedUtc=started,
                  finishedUtc=datetime.now(timezone.utc).isoformat(), exitCode=code,
                  command=list(map(str, command)))
    with (log.parent / 'execution-intervals.jsonl').open('a') as intervals:
        intervals.write(json.dumps(result) + '\n')
    if code:
        raise RuntimeError(log.read_text()[-5000:])
    return result


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def create_soundboard(name, music, events):
    project = ROOT / 'audio-source/generated' / name
    sources = project / 'src/main/java/promoaudio'
    resources = project / 'src/main/resources/META-INF'
    sources.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)
    templates = ROOT / 'audio-source/templates'
    shutil.copyfile(templates / 'AudioMod.java', sources / 'AudioMod.java')
    shutil.copyfile(templates / 'openggf-mod.yaml', resources / 'openggf-mod.yaml')
    scene = (templates / 'SoundboardScene.java.in').read_text()
    scene = scene.replace('%MUSIC%', str(music)).replace('%FRAMES%', ','.join(
        str(event['source_frame']) for event in events)).replace('%IDS%', ','.join(
        str(event['requested_id']) for event in events))
    (sources / 'SoundboardScene.java').write_text(scene)
    return project


def decode_compare(reference, actual, start, count, lease, cwd, env):
    children = []
    intervals = []
    try:
        for path in [reference, actual]:
            cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '1', '-i', path,
                   '-map', '0:v:0', '-vf', f'trim=start_frame={start}:end_frame={start + count},setpts=PTS-STARTPTS',
                   '-frames:v', count, '-an', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1']
            started = datetime.now(timezone.utc).isoformat()
            child = subprocess.Popen(list(map(str, cmd)), stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, cwd=cwd, env=env, start_new_session=True,
                            **inherited_slot(lease))
            children.append(child)
            intervals.append(dict(pid=child.pid, cwd=str(cwd), startedUtc=started,
                                  command=list(map(str, cmd))))
        digest = hashlib.sha256()
        for offset in range(count):
            pictures = []
            for child in children:
                pieces, remaining = [], 400 * 224 * 3
                while remaining:
                    block = child.stdout.read(remaining)
                    if not block:
                        raise ValueError(f'Ghost picture comparison reached unexpected EOF at {start + offset}')
                    pieces.append(block)
                    remaining -= len(block)
                pictures.append(b''.join(pieces))
            if pictures[0] != pictures[1]:
                raise ValueError(f'Original/fresh ghost pixels differ at source frame {start + offset}')
            digest.update(pictures[0])
        for child, interval in zip(children, intervals):
            code = child.wait()
            interval.update(finishedUtc=datetime.now(timezone.utc).isoformat(), exitCode=code)
            if code != 0:
                raise ValueError('Ghost decoder comparison failed')
        return dict(in_frame=start, clip_frames=count, exact_selected_rgb_frames=True,
                    concatenated_rgb_sha256=digest.hexdigest(), admittedDecoderIntervals=intervals)
    finally:
        for child in children:
            if child.poll() is None:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            if child.stdout:
                child.stdout.close()


def execute(args, lease):
    wt = args.admission_worktree.resolve()
    logs = wt / 'target/chaos-native-audio'
    logs.mkdir(parents=True, exist_ok=True)
    classes = wt / 'target/chaos-native-audio-classes'
    classes.mkdir(exist_ok=True)
    cp = str(wt / 'target/test-classes') + os.pathsep + str(wt / 'target/classes') + os.pathsep + (
        wt / 'target/chaos-classpath.txt').read_text().strip()
    env = os.environ.copy()
    env.pop('DISPLAY', None)
    env.pop('WAYLAND_DISPLAY', None)
    runs = []
    compiled = run(['javac', '--release', '25', '-cp', cp, '-d', classes,
                    ROOT / 'audio-source/NativeAudioCapture.java'], wt, logs / 'helper-compile.log', lease, env)
    runs.append(compiled)
    java = ['java', '--enable-native-access=ALL-UNNAMED', '-Xmx2g', '-XX:ActiveProcessorCount=4',
            '-Dopenggf.headless.gl=surfaceless-egl', '-cp', str(classes) + os.pathsep + cp,
            'com.openggf.tools.NativeAudioCapture']
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=wt, text=True).strip()
    rom_sha = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    if rom_sha.lower() != 'cfbf98c36c776677290a872547ac47c53d2761d6':
        raise ValueError('Requires the verified existing locked-on S3K ROM')

    def scene(name, project, frames, projection='full', sfx_only=False):
        folder = ROOT / 'audio-source/rendered' / name
        folder.mkdir(parents=True, exist_ok=True)
        # The maintained SDK refuses existing package outputs. Each admitted
        # render builds into a fresh owned target directory, preserving inputs
        # and earlier failed package evidence rather than overwriting a JAR.
        build_root = wt / 'target/chaos-native-audio-scenes'
        build_root.mkdir(parents=True, exist_ok=True)
        build = Path(tempfile.mkdtemp(prefix=name + '-', dir=build_root))
        command = java + ['scene', '--rom', args.rom, '--mod', project, '--out', folder,
                          '--build', build,
                          '--frames', frames, '--projection', projection,
                          '--sfx-only', str(sfx_only).lower()]
        print('Native scene render', name, frames, 'presentations', flush=True)
        runs.append(run(command, wt, logs / (name + '.log'), lease, env))
        return folder, json.loads((folder / 'observed.json').read_text())

    if args.mode in ('all', 'music'):
        music = create_soundboard('hcz2', 0x04, [])
        full, full_obs = scene('hcz2', music, 7200)
        dac, dac_obs = scene('dac-only', music, 180, 'dac-only')
        muted, muted_obs = scene('all-muted', music, 180, 'all-muted')
        bed = ROOT / 'assets/hcz2'
        bed.mkdir(parents=True, exist_ok=True)
        for source, output in [(full / 'audio.wav', 'native-hcz2.wav'),
                               (dac / 'audio.wav', 'dac-only.wav'), (muted / 'audio.wav', 'all-muted.wav')]:
            shutil.copyfile(source, bed / output)
        proof = dac_proof(bed / 'native-hcz2.wav', bed / 'dac-only.wav', bed / 'all-muted.wav',
                          full_obs, dac_obs, 7200)
        write_json(bed / 'music-observed.json', full_obs)
        write_json(bed / 'dac-observed.json', dac_obs)
        write_json(bed / 'muted-observed.json', muted_obs)
        shutil.copyfile(ROOT / 'audio-source/NativeAudioCapture.java', full / 'NativeAudioCapture.java')
        write_json(bed / 'render-provenance.json', dict(sourceCommit=revision, romSha1=rom_sha,
            source='Borrowed Slay/Flappy ModScene ctx.audio().playMusic(0x04), normal ExampleModHarness presentation/capture.',
            engineRuntimeChanged=False, musicId=4, sourceFrames=7200, sampleRate=48000,
            natural_driver_loops=True, arbitrary_file_loop=False, dacProof=proof,
            helperSourceSha256=sha256(ROOT / 'audio-source/NativeAudioCapture.java'),
            helperSourceSnapshot='audio-source/rendered/hcz2/NativeAudioCapture.java', admittedRuns=runs.copy()))
        print('HCZ2 DAC proof passed:', proof['dac_only']['ac_rms'], 'DAC-only AC RMS', flush=True)

    if args.mode in ('all', 'ghost', 'sfx'):
        original = TASK / 'revision-3/captures/ghosts-dez1'
        original_meta = json.loads((original / 'provenance.json').read_text())
        if sha256(args.mod) != original_meta['modSha256']:
            raise ValueError('Ghost replay must use the exact retained v3 Chaos JAR')
        folder = ROOT / 'captures/ghost-audio-observed'
        output = folder / 'output'
        frames = original_meta['frames']
        if args.mode == 'sfx':
            capture_proof = json.loads((folder / 'provenance.json').read_text())
            if capture_proof['sourceCommit'] != revision or capture_proof['modSha256'] != sha256(args.mod):
                raise ValueError('Saved replay does not match the current unchanged engine/JAR')
            for path, expected in [(folder / 'source.mkv', capture_proof['replaySourceSha256']),
                                   (output / 'observed.json', capture_proof['observedSha256']),
                                   (output / 'state.csv', capture_proof['stateComparison']['replay_csv_sha256'])]:
                if sha256(path) != expected:
                    raise ValueError(f'Qualified ghost replay input changed: {path}')
            if not capture_proof['stateComparison']['exact_state_and_input_rows'] or not capture_proof['selectedPixelComparison']['exact_selected_rgb_frames']:
                raise ValueError('Saved ghost replay has not passed exact CSV/RGB comparisons')
            state_comparison = capture_proof['stateComparison']
            pixel_comparison = capture_proof['selectedPixelComparison']
            ghost_card = next(card for card in json.loads((ROOT / 'cards.json').read_text())
                              if card['effect'] == 'soz-ghost-party')
            if (ghost_card['in_frame'], ghost_card['clip_frames']) != (pixel_comparison['in_frame'], pixel_comparison['clip_frames']):
                raise ValueError('Current ghost picture interval differs from the qualified RGB interval')
            print('Reusing qualified exact native ghost replay; rendering only SFX', flush=True)
        else:
            output.mkdir(parents=True, exist_ok=True)
            settings = folder / 'saves/mods/sonic3k-chaos-mode/settings.txt'
            settings.parent.mkdir(parents=True, exist_ok=True)
            settings.write_text('formatVersion=1\ninterval=5\ndurationQuarters=4\nselected=soz-ghost-party\nenabled=true\nseed=22\n')
            for file in ['input.script', 'input.txt']:
                shutil.copyfile(original / file, folder / file)
            command = java + ['ghost', '--rom', args.rom, '--mod', args.mod,
                              '--input', folder / 'input.txt', '--out', output,
                              '--saves', folder / 'saves', '--frames', frames]
            print('Exact native ghost replay', frames, 'presentations', flush=True)
            runs.append(run(command, wt, logs / 'ghost-native-replay.log', lease, env))
            state_comparison = compare_states(original / 'output/state.csv', output / 'state.csv')
            encode = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-framerate', '60', '-i', output / 'frames/%05d.png',
                      '-i', output / 'audio.wav', '-c:v', 'libx264rgb', '-crf', '0', '-preset', 'fast',
                      '-pix_fmt', 'rgb24', '-threads', '2', '-c:a', 'pcm_s16le', folder / 'source.mkv']
            runs.append(run(encode, wt, logs / 'ghost-native-encode.log', lease, env))
            cards = json.loads((ROOT / 'cards.json').read_text())
            ghost_card = next(card for card in cards if card['effect'] == 'soz-ghost-party')
            pixel_comparison = decode_compare(original / 'source.mkv', folder / 'source.mkv',
                            ghost_card['in_frame'], ghost_card['clip_frames'], lease, wt, env)
            write_json(folder / 'provenance.json', dict(sourceCommit=revision, effect='soz-ghost-party',
                zone='dez', act=1, nativeAct=0, frames=frames, width=400, character='sonic', sidekick='none',
                setup='Exact original native DEZ1 entry/input; no gameplay state writes.', selectedPool='singleton', seed=22,
                romSha1=rom_sha, modSha256=sha256(args.mod), nativeInputSha256=sha256(folder / 'input.txt'),
                replaySourceSha256=sha256(folder / 'source.mkv'), observedSha256=sha256(output / 'observed.json'),
                originalSource='../revision-3/captures/ghosts-dez1/source.mkv',
                stateComparison=state_comparison, selectedPixelComparison=pixel_comparison, admittedRuns=runs.copy()))
        observed = json.loads((output / 'observed.json').read_text())
        schedule = accepted_schedule(observed, frames)
        assets = ROOT / 'assets/ghosts'
        assets.mkdir(parents=True, exist_ok=True)
        write_json(assets / 'accepted-events.json', dict(source_frames=frames, events=schedule,
            replay_source='captures/ghost-audio-observed/source.mkv', observed_file='captures/ghost-audio-observed/output/observed.json'))
        soundboard = create_soundboard('ghost-sfx', -1, schedule)
        sfx, sfx_obs = scene('ghost-sfx', soundboard, frames, sfx_only=True)
        shutil.copyfile(sfx / 'audio.wav', assets / 'native-sfx.wav')
        write_json(assets / 'sfx-observed.json', sfx_obs)
        proof = verify_sfx_replay(schedule, sfx_obs, assets / 'native-sfx.wav', frames)
        write_json(assets / 'render-provenance.json', dict(sourceCommit=revision, romSha1=rom_sha,
            replay_source='captures/ghost-audio-observed/source.mkv',
            replay_source_sha256=sha256(folder / 'source.mkv'),
            accepted_event_log='assets/ghosts/accepted-events.json',
            accepted_event_log_sha256=sha256(assets / 'accepted-events.json'),
            source_frames=frames, source_start_frame=0, source_end_frame=frames,
            sample_rate=48000, samples_per_presentation=800, render_origin_frame=0, render_offset_frames=0,
            mapping='Actual raw request paired one-to-one with accepted driver SFX at source frame N -> ctx.audio().playSfx(raw requested ID) at soundboard update N -> identical resolved admission and PCM presentation N.',
            cue_ids=proof['native_cue_ids'], only_accepted_cues=True, invented_cues=False,
            pcm_extracted_from_old_mix=False, mixed_dez_music_used=False,
            helperSourcePath='audio-source/NativeAudioCapture.java',
            helperSourceSha256=sha256(ROOT / 'audio-source/NativeAudioCapture.java'),
            raw_request_mapping='Captured raw SFX and SPECIAL_SFX requests pair one-to-one with same-frame ordered accepted driver admissions; native ring33h toggles to33h/34h. Resolved IDs are observations, never replay commands.',
            stateComparison=state_comparison, selectedPixelComparison=pixel_comparison,
            nativeSfxProof=proof, admittedRuns=runs.copy()))
        print('Accepted native ghost SFX:', [(e['source_frame'], hex(e['resolved_id'])) for e in schedule], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission-worktree', type=Path, required=True)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--mod', type=Path, default=TASK / 'revision-3/out/sonic3k-chaos-mode.jar')
    parser.add_argument('--mode', choices=['all', 'music', 'ghost', 'sfx'], default='all')
    args = parser.parse_args()
    with handle_termination(), maven_slot(args.admission_worktree, exclusive=True,
                                         estimate=180, kind='chaos-reel-native-audio') as lease:
        execute(args, lease)


if __name__ == '__main__':
    main()
