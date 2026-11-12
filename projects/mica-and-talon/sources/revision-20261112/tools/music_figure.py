#!/usr/bin/env python3
"""Purpose: one picture of why the bed fades at bars 85-88: tracked tempo, pulse lock (comb contrast), beat jitter
and loudness per bar over the whole owner-supplied track, with the film's sections and the fade marked.
Inputs: work/beat-track.json, work/music-sections.json, out PNG. Origin: MICA & TALON promo redo 2026-11-11."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
T = Path(__file__).resolve().parent.parent
bt = json.load(open(T / 'work/beat-track.json'))['bars']; sec = json.load(open(T / 'work/music-sections.json'))
out = sys.argv[1] if len(sys.argv) > 1 else str(T / 'work/music-figure.png')
W, H, L, R = 1800, 790, 90, 30
im = Image.new('RGB', (W, H), (14, 18, 34)); d = ImageDraw.Draw(im)
try:
    f = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 17); fs = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 14)
except OSError:
    f = fs = ImageFont.load_default()
tmax = 162.8
X = lambda t: L + (W - L - R) * t / tmax
tb = lambda b: bt[b]['t']
FADE0, FADE1, OFF = tb(85), tb(88), tb(89)
rows = [('local tempo (BPM)', [b['bpm'] for b in bt], 154, 174, (120, 220, 170)),
        ('pulse lock: on-beat onset / mean (comb contrast)', [b['contrast'] for b in bt], 0, 5, (255, 214, 80)),
        ('beat jitter (ms)', [b['jitter_ms'] for b in bt], 0, 24, (255, 120, 120)),
        ('level per bar (dB RMS)', [s['rms'] for s in sec][:len(bt)], -23, -15, (130, 170, 255))]
top, rh, gap = 76, 135, 30
d.text((L, 14), 'RUN INTO THE SUNSHINE (Chiptune Remix): tracked pulse, bar by bar. Film uses 0.00-123.41 s, uncut.', font=f, fill=(255, 255, 255))
for k, (name, vals, lo, hi, col) in enumerate(rows):
    y0 = top + k * (rh + gap); y1 = y0 + rh
    d.rectangle((X(0), y0, X(tmax), y1), fill=(20, 26, 48))
    d.rectangle((X(OFF), y0, X(tmax), y1), fill=(58, 22, 30))
    d.rectangle((X(FADE0), y0, X(FADE1), y1), fill=(30, 70, 60))
    Y = lambda v: y1 - (max(lo, min(hi, v)) - lo) / (hi - lo) * rh
    for b in range(0, len(bt), 8):
        d.line((X(tb(b)), y0, X(tb(b)), y1), fill=(40, 50, 84))
    pts = [(X(bt[i]['t']), Y(v)) for i, v in enumerate(vals)]
    d.line(pts, fill=col, width=3)
    d.text((L + 6, y0 + 4), name, font=fs, fill=col)
    d.text((8, y0 - 2), str(hi), font=fs, fill=(170, 180, 200)); d.text((8, y1 - 16), str(lo), font=fs, fill=(170, 180, 200))
yb = top + 4 * (rh + gap) - 10
for b in range(0, len(bt), 8):
    d.text((X(tb(b)) - 8, yb), str(b), font=fs, fill=(200, 205, 220))
d.text((8, yb), 'bar', font=fs, fill=(200, 205, 220))
for t in range(0, 161, 20):
    d.text((X(t) - 10, yb + 20), f'{t}s', font=fs, fill=(140, 150, 175))
SECT = [(0, 'intro'), (8, 'riser'), (12, 'A'), (28, 'break'), (36, 'B'), (44, 'stabs'), (52, 'pre-chorus'), (60, 'chorus'), (76, 'lift'), (89, 'pulse falls apart'), (94, 'dropout'), (97, 'reprise, unstable')]
for k, (b, name) in enumerate(SECT):
    yy = 40 if k % 2 == 0 else 54
    d.line((X(tb(b)), yy + 2, X(tb(b)), 68), fill=(255, 255, 255)); d.text((X(tb(b)) + 4, yy - 4), name, font=fs, fill=(255, 255, 255))
d.text((L, H - 24), 'green band: the fade, bar 85 (119.14 s) to bar 88 (123.41 s)', font=fs, fill=(120, 230, 180))
d.text((L + 520, H - 24), 'red: not used (from bar 89, 124.84 s, the pulse stops tracking)', font=fs, fill=(255, 140, 150))
im.save(out); print(out)
