#!/usr/bin/env python3
"""Bounded native audio/event checks for Chaos reel revision4, 2026-10-14.

Origin: missing DAC percussion in the earlier direct-read exporter. These checks
distinguish a nonzero whole mix from real DAC streaming, and accepted native SFX
events from an invented editorial sound schedule. No engine state is written.
Standalone invocation holds shared admission even for WAV reads/PCM statistics.
"""
from __future__ import annotations

import argparse
from array import array
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys
import wave

ROOT = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def pcm_stats(path, expected_frames=None):
    with wave.open(str(path), 'rb') as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (2, 2, 48000):
            raise ValueError(f'Expected 48kHz stereo PCM16: {path}')
        frames = wav.getnframes()
        if expected_frames is not None and frames != expected_frames * 800:
            raise ValueError(f'Wrong source-timeline WAV length: {path}: {frames}/{expected_frames * 800}')
        # Exclude initial chip/resampler startup from the silence control variance.
        wav.setpos(min(24000, frames))
        count = total = squares = peak = 0
        while block := wav.readframes(8192):
            samples = array('h', block)
            if sys.byteorder != 'little':
                samples.byteswap()
            for sample in samples:
                count += 1
                total += sample
                squares += sample * sample
                peak = max(peak, abs(sample))
        mean = total / count if count else 0
        variance = max(0, squares / count - mean * mean) if count else 0
    return dict(stereo_frames=frames, sample_rate=48000, channels=2,
                samples_per_presentation=800, ac_variance=variance,
                ac_rms=variance ** .5, mean=mean, peak=peak, sha256=sha256(path))


def dac_proof(full, dac_only, muted, full_observation, dac_observation, frames):
    full_stats = pcm_stats(full, frames)
    dac_stats = pcm_stats(dac_only, 180)
    mute_stats = pcm_stats(muted, 180)
    for label, report in [('full', full_observation), ('dac-only', dac_observation)]:
        if report['dac_enable_2b80_writes'] < 1:
            raise ValueError(f'{label}: no native DAC enable 2Bh=80h observed')
        if report['native_streamed_2a_writes'] < 100:
            raise ValueError(f'{label}: too few native DAC_STREAM sample bytes')
        if report['native_streamed_2a_distinct_values'] < 8:
            raise ValueError(f'{label}: DAC data is absent/constant')
    if dac_stats['ac_variance'] <= max(1, mute_stats['ac_variance'] * 100):
        raise ValueError('DAC-only PCM does not exceed the all-muted resting-level control')
    if full_stats['ac_variance'] <= 1:
        raise ValueError('Full production music render is silent')
    return dict(full=full_stats, dac_only=dac_stats, all_muted=mute_stats,
                dac_enabled=True, nonconstant_native_dac_stream=True,
                proof='Profile-owned native 2Bh enable and DAC_STREAM 2Ah writes; output-stage DAC-only PCM versus all-muted control. Not shipped-ROM parity certification.')


def compare_states(reference, replay):
    with Path(reference).open() as a, Path(replay).open() as b:
        original = list(csv.DictReader(a))
        actual = list(csv.DictReader(b))
    if len(original) != len(actual):
        raise ValueError(f'Original/replayed ghost state counts differ: {len(original)}/{len(actual)}')
    for frame, (left, right) in enumerate(zip(original, actual)):
        if left != right:
            fields = {key: [left.get(key), right.get(key)] for key in left.keys() | right.keys()
                      if left.get(key) != right.get(key)}
            raise ValueError(f'Ghost native replay diverged at source frame {frame}: {fields}')
    return dict(frames=len(original), exact_state_and_input_rows=True,
                original_csv_sha256=sha256(reference), replay_csv_sha256=sha256(replay))


def accepted_schedule(observed, source_frames):
    events = observed['driver_admitted_sfx']
    requests = defaultdict(list)
    admissions = defaultdict(list)
    for event in observed['events']:
        if event['kind'] == 'request' and event.get('request_class') in ('SFX', 'SPECIAL_SFX'):
            requests[event['source_frame']].append(event)
    for event in events:
        admissions[event['source_frame']].append(event)
    if set(requests) != set(admissions):
        raise ValueError('Raw SFX request frames do not match driver admission frames')
    request_by_order = {}
    for frame, admitted in admissions.items():
        if len(requests[frame]) != len(admitted):
            raise ValueError(f'Cannot associate raw requests with accepted admissions at frame {frame}')
        for request, admission in zip(requests[frame], admitted):
            raw, resolved = request['requested_id'], admission['resolved_id']
            # S3K zPlaySound_CheckRing alternates raw 33h into 33h/34h.
            # Replay the actual raw request, never the post-toggle result.
            if raw != resolved and not (raw == 0x33 and resolved == 0x34):
                raise ValueError(f'Unsupported raw/admitted SFX translation: {request}/{admission}')
            request_by_order[admission['order']] = request
    schedule = []
    previous = (-1, -1)
    for event in events:
        position = (event['source_frame'], event['order'])
        if position <= previous or not 0 <= position[0] < source_frames:
            raise ValueError(f'Invalid admission ordering/frame: {event}')
        cue = event['resolved_id']
        if event.get('accepted') is not True or event.get('special_sfx') is True or not 0x33 <= cue <= 0xDB:
            raise ValueError(f'Unsupported native accepted SFX admission: {event}')
        request = request_by_order[event['order']]
        schedule.append(dict(source_frame=position[0], order=position[1], resolved_id=cue,
                             requested_id=request['requested_id'], request_order=request['order'],
                             request_class=request['request_class'],
                             admission_ordinal=event['admission_ordinal'], accepted=True))
        previous = position
    if not any(event['resolved_id'] == 0x92 for event in schedule):
        raise ValueError('The replay has no accepted native ghost apparition request')
    return schedule


def verify_sfx_replay(schedule, observed, wav, source_frames):
    original = [(event['source_frame'], event['resolved_id']) for event in schedule]
    actual = [(event['source_frame'], event['resolved_id'])
              for event in observed['driver_admitted_sfx']]
    if actual != original:
        raise ValueError(f'Soundboard admissions differ from captured native schedule: {original}/{actual}')
    if observed['music_present_service_snapshots']:
        raise ValueError('The isolated soundboard rendered an active music sequencer')
    if any(event.get('request_class') == 'MUSIC' for event in observed['events']):
        raise ValueError('The isolated soundboard submitted music')
    stats = pcm_stats(wav, source_frames)
    if stats['ac_variance'] <= 1:
        raise ValueError('Native SFX soundboard PCM is silent')
    return dict(exact_accepted_event_frames_and_order=True, active_music_services=0,
                music_requests=0, native_cue_ids=sorted(set(event['resolved_id'] for event in schedule)),
                pcm=stats, limitation='ROM-native SFX rendered from captured accepted admissions in an isolated soundboard. This is not a stem extracted from the old mixed PCM.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission-worktree', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, '/home/farrell/code/projects/OpenGGF/tools/testing')
    from maven_queue import handle_termination, maven_slot
    with handle_termination(), maven_slot(args.admission_worktree, exclusive=True,
                                         estimate=10, kind='chaos-native-audio-check'):
        full = ROOT / 'assets/hcz2/native-hcz2.wav'
        dac = ROOT / 'assets/hcz2/dac-only.wav'
        muted = ROOT / 'assets/hcz2/all-muted.wav'
        obs = json.loads((ROOT / 'assets/hcz2/music-observed.json').read_text())
        dac_obs = json.loads((ROOT / 'assets/hcz2/dac-observed.json').read_text())
        proof = dac_proof(full, dac, muted, obs, dac_obs, 7200)
        ghost = ROOT / 'assets/ghosts'
        schedule = json.loads((ghost / 'accepted-events.json').read_text())['events']
        ghost_obs = json.loads((ghost / 'sfx-observed.json').read_text())
        sfx = verify_sfx_replay(schedule, ghost_obs, ghost / 'native-sfx.wav', ghost_obs['source_frames'])
        print(json.dumps(dict(dac=proof, sfx=sfx), indent=2))


if __name__ == '__main__':
    main()
