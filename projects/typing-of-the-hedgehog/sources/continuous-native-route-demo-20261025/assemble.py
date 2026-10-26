#!/usr/bin/env python3
"""Assemble ONE reviewed continuous Typing journey at native 60-Hz speed.

Origin: spaced route demo, 2026-10-25. Inputs: new full-cadence capture and a filled
edit-list template. Output: silent 1280x720/60 MP4, chapters, resolved edit/provenance.
Default is plan-only. --execute runs FFmpeg/FFprobe, never an engine or build.
Stageplay is omitted from this replacement so the main journey stands on gameplay.
"""
import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from demo_common import (FPS, external_new_dir, frames_summary, json_new,
                         read_state, sha256)

EVENTS = ('first_fight_visible', 'first_fight_cleared', 'travel_start', 'travel_end', 'next_fight_visible')


def validate_edit(edit, rows):
    if edit.get('fps') != FPS or edit.get('playback_speed') != 1:
        raise ValueError('Edit must explicitly use fps=60 and playback_speed=1')
    review = edit['review']
    for key in ('route_candidate_qualified', 'substantial_native_travel_observed', 'continuous_sequence_inspected_at_1x'):
        if review.get(key) is not True:
            raise ValueError(f'PENDING route review: {key}; inspect new footage before assembly')
    if not review.get('reviewer') or not review.get('notes'):
        raise ValueError('Record reviewer and observed evidence/limitations')
    segment = edit['gameplay']
    if segment.get('source_kind') != 'actual_selected_section_gameplay':
        raise ValueError('This assembler accepts actual selected-section gameplay only')
    start, end = segment['start_frame'], segment['end_frame_exclusive']
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(rows):
        raise ValueError('Fill a valid [start_frame,end_frame_exclusive) from the NEW capture')
    event = segment['observed_events']
    if any(type(event.get(k)) is not int for k in EVENTS):
        raise ValueError('All new observed event frames remain mandatory and cannot be guessed')
    a, b, c, d, e = [event[k] for k in EVENTS]
    if not start <= a < b <= c < d <= e < end:
        raise ValueError('Required sequence: first fight -> clear -> continuous travel -> next fight, within the selected interval')
    if any(rows[i]['dead'] == '1' for i in range(start, end)):
        raise ValueError('Selected journey contains a dead player; resolve/describe the failed candidate before using it')
    return start, end


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams',
                                             '-show_format', '-show_chapters', '-of', 'json', str(path)]))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture-dir', type=Path, required=True)
    p.add_argument('--edit-list', type=Path, required=True)
    p.add_argument('--out-dir', type=Path, required=True, help='NEW directory; sources and earlier reels are preserved')
    p.add_argument('--font', type=Path, help='Readable TTF for disclosure; default resolves DejaVu Sans Bold through Pillow')
    p.add_argument('--crf', type=int, default=18)
    p.add_argument('--execute', action='store_true', help='Encode/verify; without this, only inspect inputs and print the plan')
    a = p.parse_args()
    root = a.capture_dir.expanduser().resolve(strict=True)
    out = a.out_dir.expanduser().resolve()
    if out.exists() or out.is_relative_to(root):
        raise ValueError('Use a NEW output directory outside the capture root')
    if not 0 <= a.crf <= 51:
        p.error('--crf must be 0..51')
    manifest = json.loads((root / 'provenance/capture.json').read_text())
    if manifest['status'] != 'capture_complete_route_review_pending' or manifest['fingerprint_unchanged'] is not True:
        raise ValueError('Capture is incomplete or its source/build changed')
    if (manifest['fps'], manifest['every'], manifest['capture_from']) != (60, 1, 0):
        raise ValueError('Require every-row capture from 0 at 60 Hz; sparse footage cannot establish native cadence')
    if manifest['intent']['demo'] != 'true' or manifest['intent']['noFail'] != 'true' or manifest['intent']['slowMotion'] != 'false':
        raise ValueError('This recipe requires disclosed attract typing, No-Fail and no slow motion')
    if sha256(root / 'state.csv') != manifest['outputs']['state_sha256']:
        raise ValueError('state.csv changed since capture')
    rows = read_state(root / 'state.csv', manifest['frames_requested'])
    frames = frames_summary(root, len(rows), manifest['width'])
    if frames != manifest['outputs']['frames']:
        raise ValueError('Source PNGs changed since capture')
    edit = json.loads(a.edit_list.read_text())
    start, end = validate_edit(edit, rows)
    count = end-start
    scale = min(1280 // manifest['width'], (720-48) // manifest['height'])
    if scale < 1:
        raise ValueError('Source cannot fit without downsampling')
    width, height = manifest['width']*scale, manifest['height']*scale
    top = 48 + (672-height)//2
    title = 'Typing: continuous first fight to next fight'
    meta = ';FFMETADATA1\ntitle=Typing route spacing demo\n[CHAPTER]\nTIMEBASE=1/60\nSTART=0\nEND=' + str(count) + '\ntitle=' + title + '\n'
    filters = f'[0:v]scale={width}:{height}:flags=neighbor,pad=1280:720:(ow-iw)/2:{top}:color=0x101820[game];[game][1:v]overlay=0:0:shortest=1[v]'
    movie = out / 'typing-spaced-route-demo.mp4'
    command = ['ffmpeg', '-v', 'error', '-nostdin', '-n', '-framerate', '60', '-start_number', str(start),
               '-i', str(root / 'frames/%05d.png'), '-loop', '1', '-framerate', '60', '-i', str(out / 'disclosure.png'),
               '-f', 'ffmetadata', '-i', str(out / 'chapters.ffmeta'), '-filter_complex', filters,
               '-map', '[v]', '-map_metadata', '2', '-map_chapters', '2', '-frames:v', str(count),
               '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(a.crf), '-threads', '2',
               '-pix_fmt', 'yuv420p', '-r', '60', '-fps_mode', 'cfr', '-movflags', '+faststart', str(movie)]
    resolved = dict(edit)
    resolved.update(capture_root=str(root), capture_manifest_sha256=sha256(root / 'provenance/capture.json'),
                    source_interval_seconds=[start/FPS, end/FPS],
                    assembly_sources={name: sha256(Path(__file__).parent / name) for name in ('assemble.py', 'demo_common.py')}, output_start_frame=0, output_end_frame_exclusive=count,
                    output_seconds=count/FPS, width=1280, height=720, integer_scale=scale, audio='silent',
                    continuity='one unbroken source interval; no temporal resampling or internal cuts',
                    assembly_argv=command, status='planned; visual review of final film pending')
    print(json.dumps({'source_frames_half_open': [start, end], 'output_frames': count,
                      'seconds': count/FPS, 'fps': FPS, 'canvas': [1280,720], 'integer_scale': scale,
                      'audio': 'silent', 'command_argv': command}, indent=2))
    if not a.execute:
        print('PLAN ONLY: no files written and no media/engine processes launched.')
        return
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise ValueError('FFmpeg with libx264 and FFprobe are required')
    import PIL
    from PIL import Image, ImageDraw, ImageFont
    font = str(a.font.expanduser().resolve(strict=True)) if a.font else 'DejaVuSans-Bold.ttf'
    large, small = ImageFont.truetype(font, 22), ImageFont.truetype(font, 16)
    out = external_new_dir(out)
    header = Image.new('RGB', (1280,48), '#101820')
    draw = ImageDraw.Draw(header)
    draw.text((24,1), 'SHARED NATIVE ROUTES  |  2,168px BETWEEN FIGHTS', font=large, fill='#f1f5fa')
    draw.text((24,28), 'MARBLE 3  /  ATTRACT TYPIST  /  NO-FAIL  /  NATIVE 60 Hz', font=small, fill='#ffd45a')
    header.save(out / 'disclosure.png')
    (out / 'chapters.ffmeta').write_text(meta)
    json_new(out / 'edit-list.resolved.json', resolved)
    json_new(out / 'source-provenance.json', manifest)
    subprocess.run(command, check=True)
    actual = probe(movie)
    video = [s for s in actual['streams'] if s['codec_type'] == 'video']
    audio = [s for s in actual['streams'] if s['codec_type'] == 'audio']
    if len(video) != 1 or audio:
        raise ValueError('Unexpected video/audio stream layout')
    stream = video[0]
    if (stream['width'], stream['height']) != (1280,720) or Fraction(stream['avg_frame_rate']) != FPS or Fraction(stream['r_frame_rate']) != FPS:
        raise ValueError('Wrong final dimensions or frame rate')
    if int(stream['nb_read_frames']) != count or abs(float(stream['duration']) - count/FPS) > 1/FPS:
        raise ValueError('Final duration/frame count does not match the unbroken source interval')
    chapters = actual['chapters']
    if len(chapters) != 1 or abs(float(chapters[0]['start_time'])) > 1/FPS or abs(float(chapters[0]['end_time'])-count/FPS) > 1/FPS:
        raise ValueError('Final chapter map disagrees with the edit')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-nostdin', '-i', str(movie), '-f', 'null', '-'], check=True)
    json_new(out / 'verification.json', {'software': {'python': sys.version, 'pillow': PIL.__version__,
                                       'ffmpeg': subprocess.check_output(['ffmpeg', '-version'], text=True).splitlines()[0],
                                       'ffprobe': subprocess.check_output(['ffprobe', '-version'], text=True).splitlines()[0],
                                       'font_requested': font, 'font_sha256': sha256(large.path)}, 'ffprobe': actual, 'full_decode': 'passed', 'sha256': sha256(movie),
                                       'visual_review_at_1x': 'PENDING; inspect whole journey, HUD, fight outcomes and spacing',
                                       'claim_limit': 'Encoding checks plus supplied review annotations; no parity or full-level completion claim.'})
    print(f'Encoded and fully decoded: {movie}\nFinal whole-film 1x visual review remains PENDING.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError, ImportError) as exc:
        sys.exit(str(exc))
