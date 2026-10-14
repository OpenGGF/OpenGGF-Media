#!/usr/bin/env python3
"""Assembles the Starpost Valley promo from recorded segment videos.

Usage: assemble.py OUT.mp4 CUTS.txt
CUTS.txt: one cut per line, "file.mp4 start end" in seconds ('#' comments). Cuts are joined with a
short crossfade (video xfade, audio acrossfade). Each segment video comes from ExampleModCapture
--video with --audio (800x448, 60 fps, AAC). Origin: Starpost Valley promo, 2026-10-09.
"""
import subprocess
import sys

FADE = 0.35


def main():
    out, cuts_file = sys.argv[1], sys.argv[2]
    cuts = []
    for line in open(cuts_file):
        line = line.split('#', 1)[0].strip()
        if line:
            f, s, e = line.split()
            cuts.append((f, float(s), float(e)))
    args = ['ffmpeg', '-y', '-v', 'error']
    for f, s, e in cuts:
        args += ['-ss', str(s), '-to', str(e), '-i', f]
    parts = []
    for i in range(len(cuts)):
        parts.append(f'[{i}:v]fps=60,format=yuv420p,setpts=PTS-STARTPTS[v{i}]')
        parts.append(f'[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{i}]')
    vprev, aprev = 'v0', 'a0'
    offset = cuts[0][2] - cuts[0][1]
    for i in range(1, len(cuts)):
        offset -= FADE
        parts.append(f'[{vprev}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.3f}[vx{i}]')
        parts.append(f'[{aprev}][a{i}]acrossfade=d={FADE}[ax{i}]')
        vprev, aprev = f'vx{i}', f'ax{i}'
        offset += cuts[i][2] - cuts[i][1]
    args += ['-filter_complex', ';'.join(parts), '-map', f'[{vprev}]', '-map', f'[{aprev}]',
             '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)


if __name__ == '__main__':
    main()
