#!/usr/bin/env python3
"""Assemble the uninterrupted Location, Location, Location Stageplay promo.

Inputs: edl.json, 400x224/60Hz FFV1+FLAC source, FFmpeg/FFprobe, Pillow and Fira fonts.
Origin: OpenGGF Stageplay directing task, 2026-10-21; supersedes the rejected padded edit.
The source remains frame-for-frame intact at 4x integer scale. Two original type
accents occupy only the bottom safe band; no extra camera moves, cuts or audio fades.
Use --preview-dir for clearly labelled synthetic typography/motion checks without ROMs.
"""
import argparse
import array
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import PIL
from PIL import Image, ImageDraw, ImageFont

FPS, RATE, FRAMES = 60, 48000, 3060
MASTER_GAIN_DB = 10.0
WIDTH, HEIGHT = 1600, 900
TITLE_FONT = Path('/usr/share/fonts/TTF/FiraSansCompressed-HeavyItalic.ttf')
KICKER_FONT = Path('/usr/share/fonts/TTF/FiraSans-Medium.ttf')
INK, CREAM, GOLD = '#081020', '#FFF1CF', '#FFC65C'
# Half-open authored output intervals. First dialogue begins at100; last ends at2915.
CARDS = (
    dict(id='opening', start=8, end=88, enter=14, leave=8, y=710, text='ONE BUTTON.'),
    dict(id='closing', start=2916, end=3060, enter=16, leave=0, y=710, text='MAKE A SCENE.'),
)


def run(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[0]} exited {result.returncode}: {result.stderr[-5000:]}')
    return result.stdout


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def probe(path, count=False):
    return json.loads(run(['ffprobe', '-v', 'error', *(['-count_frames'] if count else []),
                          '-show_streams', '-show_format', '-show_chapters', '-of', 'json', str(path)]))


def meter_audio(path):
    """Measure the decoded AAC, not just pre-encode PCM; these are sample/RMS metrics, not LUFS."""
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                             '-f', 'f32le', '-acodec', 'pcm_f32le', '-'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[-5000:])
    samples = array.array('f', result.stdout)
    if sys.byteorder != 'little':
        samples.byteswap()
    if not samples or any(not math.isfinite(value) for value in samples):
        raise ValueError('Decoded promo audio is missing or non-finite')
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(math.fsum(value * value for value in samples) / len(samples))
    clipped = sum(abs(value) >= 1 for value in samples)
    if peak >= .95 or clipped:
        raise ValueError(f'Decoded audio exceeds the mastering ceiling: peak={peak}, clipped={clipped}')
    return dict(peak=peak, rms=rms, rmsDbfs=20 * math.log10(rms) if rms else None,
                clippedSamples=clipped, decodedSamplesPerChannel=len(samples) // 2,
                measurement='AAC decoded to float32; sample peak and RMS, not LUFS or oversampled true peak')


def outlined(draw, position, text, font, color):
    x, y = position
    draw.text((x + 7, y + 8), text, font=font, anchor='lt', fill=INK, stroke_width=5, stroke_fill=INK)
    draw.text((x, y), text, font=font, anchor='lt', fill=color, stroke_width=3, stroke_fill=INK)


def card_images(directory, title_font, kicker_font):
    """Original sparse bottom-band artwork; source dialogue at output y50..306 stays untouched."""
    result = []
    for card in CARDS:
        image = Image.new('RGBA', (WIDTH, 190))
        draw = ImageDraw.Draw(image)
        # A soft local shade keeps the title readable over grass; it is not a permanent frame.
        for y in range(190):
            draw.line((0, y, WIDTH, y), fill=(8, 16, 32, round(132 * (y / 189) ** 1.6)))
        if card['id'] == 'opening':
            draw.text((87, 15), 'AN OPENGGF STAGEPLAY SHORT', font=ImageFont.truetype(str(kicker_font), 24),
                      anchor='lt', fill=CREAM, stroke_width=1, stroke_fill=INK)
            font = ImageFont.truetype(str(title_font), 120)
            outlined(draw, (80, 52), 'ONE', font, CREAM)
            x = 80 + round(draw.textlength('ONE ', font=font))
            outlined(draw, (x, 52), 'BUTTON.', font, GOLD)
        else:
            font = ImageFont.truetype(str(title_font), 128)
            outlined(draw, (80, 43), 'MAKE A', font, CREAM)
            x = 80 + round(draw.textlength('MAKE A ', font=font))
            outlined(draw, (x, 43), 'SCENE.', font, GOLD)
        # One small directional accent echoes the characters' forward movement.
        draw.polygon([(47, 60), (59, 60), (43, 151), (31, 151)], fill=GOLD)
        if draw.textbbox((80, 52), card['text'], font=font, anchor='lt', stroke_width=5)[2] > WIDTH - 60:
            raise ValueError('Title font is too wide for the approved lower-band composition')
        path = directory / (card['id'] + '.png')
        image.save(path)
        result.append(path)
    return result


def filter_graph(start=0, frames=FRAMES):
    """Use global source time for the two title accents, even in a synthetic excerpt."""
    graph = [f'[0:v]trim=end_frame={frames},setpts=PTS-STARTPTS+{start}/{FPS}/TB,'
             'scale=1600:896:flags=neighbor,pad=1600:900:0:2:color=0x080C14,setsar=1[base]']
    previous = 'base'
    for index, card in enumerate(CARDS, 1):
        duration = card['end'] - card['start']
        animation = f'fade=t=in:st=0:d={card["enter"] / FPS:.9f}:alpha=1'
        if card['leave']:
            animation += f',fade=t=out:st={(duration-card["leave"])/FPS:.9f}:d={card["leave"]/FPS:.9f}:alpha=1'
        graph.append(f'[{index}:v]format=rgba,trim=end_frame={duration},setpts=PTS-STARTPTS,{animation},'
                     f'setpts=PTS+{card["start"]}/{FPS}/TB[card{index}]')
        y = f'{card["y"]}+28*pow(max(0,1-(t-{card["start"]}/{FPS})/({card["enter"]}/{FPS})),3)'
        graph.append(f'[{previous}][card{index}]overlay=x=0:y=\'{y}\':eof_action=pass:repeatlast=0:'
                     f'enable=\'gte(t,{card["start"]}/{FPS})*lt(t,{card["end"]}/{FPS})\'[layer{index}]')
        previous = f'layer{index}'
    graph.append(f'[{previous}]setpts=PTS-STARTPTS,format=yuv420p[v]')
    return ';\n'.join(graph)


def metadata_escape(value):
    return str(value).replace('\\', '\\\\').replace('\n', ' ').replace('\r', ' ').replace('=', '\\=').replace(';', '\\;').replace('#', '\\#')


def read_edit(root):
    edits = json.loads((root / 'edl.json').read_text())
    if not isinstance(edits, list) or len(edits) != 7:
        raise ValueError('This story has exactly seven retained chapter intervals')
    sources = {row['source'] for row in edits}
    if len(sources) != 1:
        raise ValueError('This continuous edit uses one retained lossless source')
    source = (root / next(iter(sources))).resolve()
    if not source.is_relative_to(root):
        raise ValueError('Source must remain inside the relocated production root')
    prior, chapters = 0, []
    for number, row in enumerate(edits, 1):
        start, end = row['source_start_frame'], row['source_end_frame']
        if type(start) is not int or type(end) is not int or start != prior or not start < end <= FRAMES:
            raise ValueError('Chapter intervals must cover the source continuously, without gaps or repeats')
        if row['sequence'] != number or row['source_start_seconds'] != start / FPS or row['source_end_seconds'] != end / FPS:
            raise ValueError('Chapter sequence/frame/second fields disagree')
        chapters.append(dict(row, output_start_frame=start, output_end_frame=end,
                             output_start_seconds=start / FPS, output_end_seconds=end / FPS))
        prior = end
    if prior != FRAMES:
        raise ValueError('The edit must retain all 3060 source frames')
    return source, chapters


def encode_command(source_args, images, graph, staged, frames, metadata=None):
    command = ['ffmpeg', '-v', 'error', '-n', *source_args]
    for image in images:
        command += ['-loop', '1', '-framerate', str(FPS), '-i', str(image)]
    if metadata:
        command += ['-f', 'ffmetadata', '-i', str(metadata)]
    command += ['-filter_complex_threads', '1', '-filter_complex', graph, '-map', '[v]']
    if metadata:
        command += ['-map', '0:a:0', '-map_metadata', '3', '-map_chapters', '3',
                    '-c:a', 'aac', '-b:a', '192k', '-af',
                    f'atrim=end_sample={frames * RATE // FPS},asetpts=PTS-STARTPTS,volume={MASTER_GAIN_DB:g}dB']
    command += ['-frames:v', str(frames), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                '-threads', '4', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(staged)]
    return command


def assemble(root, out, title_font, kicker_font):
    chapter_path = out.parent / 'chapters.json'
    provenance_path = out.with_suffix('.assembly.json')
    for path in (out, chapter_path, provenance_path):
        if path.exists():
            raise ValueError(f'Choose a fresh output location; refusing to replace {path}')
    source, chapters = read_edit(root)
    info = probe(source, count=True)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (video['width'], video['height'], video['r_frame_rate'], int(video['nb_read_frames'])) != (400, 224, '60/1', FRAMES):
        raise ValueError('Expected exactly 3060 400x224 frames at 60Hz; finish and verify source capture first')
    if audio['sample_rate'] != str(RATE) or audio['channels'] != 2 or video['codec_name'] != 'ffv1' or audio['codec_name'] != 'flac':
        raise ValueError('Expected the retained FFV1/FLAC stereo 48kHz source')
    if any(abs(float(s.get('start_time', 0))) > 1 / RATE for s in (video, audio)):
        raise ValueError('Source streams must start together at zero')
    original_hash = sha256(source)
    with tempfile.TemporaryDirectory(prefix='.stageplay-edit-', dir=out.parent) as temporary:
        staging = Path(temporary)
        images = card_images(staging, title_font, kicker_font)
        metadata = staging / 'chapters.ffmeta'
        metadata.write_text(';FFMETADATA1\ntitle=OpenGGF Stageplay - Location, Location, Location\n' + ''.join(
            f'[CHAPTER]\nTIMEBASE=1/60\nSTART={row["output_start_frame"]}\nEND={row["output_end_frame"]}\ntitle={metadata_escape(row["title"])}\n'
            for row in chapters))
        staged = staging / 'promo.mp4'
        command = encode_command(['-i', str(source)], images, filter_graph(), staged, FRAMES, metadata)
        run(command)
        run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(staged), '-f', 'null', '-'])
        audio_measurements = meter_audio(staged)
        final = probe(staged)
        stream = next(s for s in final['streams'] if s['codec_type'] == 'video')
        if (int(stream['nb_frames']), stream['r_frame_rate'], stream['width'], stream['height']) != (FRAMES, '60/1', WIDTH, HEIGHT):
            raise ValueError('Output frame count/cadence/dimensions mismatch')
        if len(final.get('chapters', [])) != len(chapters):
            raise ValueError('Encoded chapter count mismatch')
        if sha256(source) != original_hash:
            raise ValueError('Source changed during assembly; nothing published')
        staged_chapters = staging / 'chapters.json'
        staged_chapters.write_text(json.dumps(chapters, indent=2) + '\n')
        report = dict(output=out.name, frames=FRAMES, seconds=FRAMES / FPS, width=WIDTH, height=HEIGHT,
            chapters=len(chapters), fullDecode='passed', visualReview='pending; codec checks do not establish dramatic quality',
            source=dict(path=str(source.relative_to(root)), sha256=original_hash, kind='Stageplay authored performance'),
            presentation=dict(integerScale=4, sourceOffset=[0, 2], sourceFrames='all, unchanged order and speed',
                              audio='continuous authored ROM score/effects; constant +10 dB gain before AAC encode, no added bed or chapter fades', cards=CARDS),
            mastering=dict(gainDb=MASTER_GAIN_DB, method='constant amplitude gain; no loudness normalization or limiter',
                           decodedAudio=audio_measurements),
            fonts=[dict(path=str(font), sha256=sha256(font)) for font in (title_font, kicker_font)],
            sourceFiles={str(path.relative_to(root)): sha256(path) for path in
                         (root / 'edl.json', root / 'assemble_promo.py', source.with_suffix('.screenplay.json'), source.with_suffix('.stageplay'))
                         if path.exists()},
            outputSha256=sha256(staged), pillowVersion=PIL.__version__, ffmpegVersion=run(['ffmpeg', '-version']).splitlines()[0],
            encodeCommand=command, rebuildCommand=['python3', 'assemble_promo.py', '--root', str(root), '--out', str(out),
                                                  '--font', str(title_font), '--kicker-font', str(kicker_font)])
        staged_report = staging / 'assembly.json'
        staged_report.write_text(json.dumps(report, indent=2) + '\n')
        published = []
        try:
            # Link publication fails if another process created a destination meanwhile.
            for staged_path, destination in ((staged_chapters, chapter_path), (staged_report, provenance_path), (staged, out)):
                os.link(staged_path, destination)
                published.append(destination)
        except BaseException:
            for destination in reversed(published):
                destination.unlink()
            raise
    return report


def preview(directory, title_font, kicker_font):
    """Two brief synthetic clips exercise the same overlay graph; neither is gameplay evidence."""
    directory.mkdir(parents=True, exist_ok=False)
    images = card_images(directory, title_font, kicker_font)
    canvas = Image.new('RGB', (400, 224), '#246174')
    draw = ImageDraw.Draw(canvas)
    for y in range(88, 224, 16):
        for x in range(0, 400, 16):
            draw.rectangle((x, y, x + 15, y + 15), fill=('#245446' if (x // 16 + y // 16) % 2 else '#39664C'))
    draw.rectangle((12, 12, 388, 76), fill='#101827', outline='#FFC65C', width=2)
    draw.text((20, 20), 'SYNTHETIC LAYOUT - NOT GAMEPLAY', fill='#FFC65C')
    draw.text((20, 42), 'The reserved dialogue panel stays clear.', fill='white')
    draw.rectangle((135, 125, 157, 165), fill='#75BFFF')
    draw.rectangle((265, 125, 287, 165), fill='#FFC65C')
    source = directory / 'synthetic.png'
    canvas.save(source)
    outputs = []
    for name, start, frames in [('opening', 0, 90), ('closing', 2910, 150)]:
        path = directory / (name + '-synthetic.mp4')
        run(encode_command(['-loop', '1', '-framerate', str(FPS), '-i', str(source)], images,
                           filter_graph(start, frames), path, frames))
        run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'])
        frame = directory / (name + '-full.png')
        run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', 'select=eq(n\\,45)', '-frames:v', '1', str(frame)])
        outputs.append(dict(path=str(path), frames=frames, synthetic=True))
    return dict(previews=outputs, note='Typography/overlay plumbing only; actual source and moving performance review remain pending')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--font', type=Path, default=TITLE_FONT, help='Fira Sans Compressed Heavy Italic title face')
    parser.add_argument('--kicker-font', type=Path, default=KICKER_FONT, help='Fira Sans Medium opening kicker')
    parser.add_argument('--preview-dir', type=Path, help='New directory for two synthetic layout/motion previews')
    args = parser.parse_args()
    if bool(args.out) == bool(args.preview_dir):
        parser.error('Choose either --out for the real source or --preview-dir for synthetic previews')
    try:
        if args.preview_dir:
            result = preview(args.preview_dir.resolve(), args.font.resolve(), args.kicker_font.resolve())
        else:
            root = args.root.resolve()
            out = args.out.resolve() if args.out.is_absolute() else (root / args.out).resolve()
            result = assemble(root, out, args.font.resolve(), args.kicker_font.resolve())
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, RuntimeError, KeyError, StopIteration) as error:
        print(json.dumps(dict(error=str(error))), file=sys.stderr)
        sys.exit(1)
