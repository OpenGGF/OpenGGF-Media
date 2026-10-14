#!/usr/bin/env python3
"""Compile the SOZ completion campaign's original clips without replacing them.
Input: MP4 captures below this folder. Output: complete chronological archive. Curated reel: curate_highlights.py.
Origin: SOZ methodology-v2 completion, 2026-09-15.
"""
from pathlib import Path
import csv, hashlib, json, math, shutil, subprocess, textwrap

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'SOZ-work-compilation.mp4'
HIGHLIGHTS = ROOT / 'SOZ-work-highlights.mp4'
BUILD = ROOT / '.reel-build'


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', str(path)]))


def label(path):
    name = str(path.relative_to(ROOT).parent)
    if name.endswith('completion-cold-route/native-320-final'): status = 'Cold Act 1 controller route through playable Act 2'
    elif name.endswith('completion-cold-route/act2-native-320-final'): status = 'Cold Act 2 controller route through playable Lava Reef'
    elif '4x-slow' in path.name: status = '4x slow motion - background redraw and art admission'
    elif name.endswith('aligned-complete-route/lower') or name.endswith('complete-solo-route/lower'): status = 'Earlier escape capture - follower alias selected fallback Sonic, not solo'
    elif 'ordinary-sonic-tails' in name: status = 'Sampled cold-route attempt - ends in death, not completion'
    elif 'authored-act1' in name: status = 'Sampled cold Act 1 attempt - see route milestone notes'
    elif 'authored-act2' in name: status = 'Sampled connected Act 2 attempt - see route limits'
    elif 'ordinary-act2' in name: status = 'Sampled cold Act 2 attempt - stalls before capsule'
    elif path.name == 'still-sequence.mp4': status = 'Sampled development stills - not continuous motion'
    elif name.startswith('engine-desert-foreground-haze'): status = 'Foreground heat shimmer'
    elif name.startswith('engine-desert-fixed'): status = 'Background corrections'
    elif name.startswith('engine-desert'): status = 'Earlier background work in progress'
    elif 'layer-fix' in name: status = 'Switch layering correction'
    elif 'capsule-route' in name or name.endswith('capsule-act2'): status = 'Route attempt - stops before capsule'
    elif name.endswith('capsule-positioned-act2'): status = 'Earlier capsule capture - before title startup correction'
    elif 'positioned' in name: status = 'Positioned local scenario'
    elif name.startswith('native-') or name.startswith('pilot-'): status = 'Native reference stills - see probe notes'
    else: status = 'Local development capture'
    return name.replace('/', ' / ') + '\n' + status


def prepare_still_sequences():
    # Preserve sparse captures as explicitly labelled slides, retaining their
    # original chronology. Do not suggest these are continuous gameplay videos.
    frame_dirs = [p for p in ROOT.rglob('frames') if p.is_dir()]
    # Native probes often retain only last.png directly in their task folder.
    # Include those too; direct stills beside a frames/ sequence are duplicates.
    direct_dirs = {p.parent for p in ROOT.rglob('*.png')
                   if p.parent.name != 'frames' and not (p.parent / 'frames').is_dir()}
    for frames in sorted(set(frame_dirs) | direct_dirs):
        if BUILD in frames.parents: continue
        folder = frames.parent if frames.name == 'frames' else frames
        if folder.name == 'act2-native-320-final': continue  # final movie is produced by its capture owner
        if any(p.name != 'still-sequence.mp4' for p in folder.glob('*.mp4')): continue
        images = sorted(frames.glob('*.png'))
        if not images: continue
        # A probe may retain thousands of PNGs without producing a movie.
        # Show every probe as a compact montage; retain every original PNG.
        original_count = len(images)
        if len(images) > 24:
            images = [images[round(i * (len(images) - 1) / 23)] for i in range(24)]
        output = folder / 'still-sequence.mp4'
        if output.exists(): continue
        with (folder / 'still-sequence-frames.csv').open('w') as stream:
            writer = csv.writer(stream)
            writer.writerow(['source_png', 'original_frame_count', 'montage_duration_seconds'])
            writer.writerows([str(p.relative_to(folder)), original_count, 0.25] for p in images)
        manifest = folder / '.still-sequence.txt'
        manifest.write_text(''.join(f"file '{p.resolve()}'\nduration 0.25\n" for p in images)
                            + f"file '{images[-1].resolve()}'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
            '-i', str(manifest), '-r', '60', '-c:v', 'libx264', '-crf', '18',
            '-threads', '8', '-pix_fmt', 'yuv420p', '-bf', '0', '-video_track_timescale', '60000', str(output)], check=True)
        import os
        stamp = max(p.stat().st_mtime_ns for p in images)
        os.utime(output, ns=(stamp, stamp))
        manifest.unlink()


def main():
    prepare_still_sequences()
    clips = sorted((p for p in ROOT.rglob('*.mp4') if p.parent != ROOT and not any(part.startswith('.') for part in p.relative_to(ROOT).parts)),
                   key=lambda p: (p.stat().st_mtime_ns, str(p)))
    if not clips: raise SystemExit('No source clips')
    BUILD.mkdir(exist_ok=True)
    rows, chapters, elapsed = [], [], 0
    for index, clip in enumerate(clips, 1):
        info = probe(clip)
        video = next(s for s in info['streams'] if s.get('codec_type') == 'video')
        # Recover native dimensions from the usual 3x captures, then use the
        # largest integer scale that fits below the caption (up to 4x).
        native_scale = 3 if video['height'] == 672 else 1
        nw, nh = video['width'] // native_scale, video['height'] // native_scale
        scale = max(1, min(4, 1920 // nw, 900 // nh))
        width, height = nw * scale, nh * scale
        if width > 1920 or height > 900:
            fit = min(1920 / width, 900 / height)
            width = max(2, int(width * fit) // 2 * 2)
            height = max(2, int(height * fit) // 2 * 2)
        caption = BUILD / f'{index:03d}.txt'
        title = f'{index:02d} / {len(clips):02d}   ' + label(clip)
        caption_text = '\n'.join(textwrap.fill(line, width=95) for line in title.splitlines())
        caption.write_text(caption_text)
        out = BUILD / f'{index:03d}.mp4'
        vf = (f'scale={width}:{height}:flags=neighbor,pad=1920:1080:(ow-iw)/2:180+(900-ih)/2:black,'
              f'drawtext=textfile={caption}:fontcolor=white:fontsize=30:x=50:y=35:line_spacing=12')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(clip), '-vf', vf,
            '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-threads', '8', '-pix_fmt', 'yuv420p', '-bf', '0', '-video_track_timescale', '60000', str(out)], check=True)
        duration = float(probe(out)['format']['duration'])
        chapters.append((elapsed, elapsed + duration, str(clip.relative_to(ROOT).parent)))
        elapsed += duration
        with clip.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        rows.append([index, str(clip.relative_to(ROOT)), info['format']['duration'],
                     video['width'], video['height'], digest])
        print(f'{index}/{len(clips)} {clip.relative_to(ROOT)}', flush=True)
    with (ROOT / 'capture-index.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['sequence', 'relative_path', 'duration_seconds', 'width', 'height', 'sha256'])
        writer.writerows(rows)
    concat = BUILD / 'concat.txt'
    concat.write_text(''.join(f"file '{index:03d}.mp4'\n" for index in range(1, len(clips)+1)))
    metadata = BUILD / 'chapters.txt'
    metadata.write_text(';FFMETADATA1\ntitle=Sandopolis Zone - complete development compilation\n' + ''.join(
        f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(a*1000)}\nEND={round(b*1000)}\ntitle={name}\n'
        for a,b,name in chapters))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
        '-i', str(metadata), '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy',
        '-movflags', '+faststart', str(OUTPUT)], check=True)
    actual = float(probe(OUTPUT)['format']['duration'])
    if abs(actual - elapsed) > 0.1: raise RuntimeError(f'Duration mismatch {actual} vs {elapsed}')
    with (ROOT / 'compilation-chapters.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['start_seconds', 'end_seconds', 'source'])
        writer.writerows((f'{a:.3f}', f'{b:.3f}', name) for a,b,name in chapters)
    shutil.rmtree(BUILD)
    print(f'Completed {OUTPUT}: {len(clips)} clips, {actual:.3f}s')

if __name__ == '__main__': main()
