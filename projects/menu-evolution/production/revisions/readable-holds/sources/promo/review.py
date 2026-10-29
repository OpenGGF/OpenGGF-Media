#!/usr/bin/env python3
"""Readable-holds cut: review and verification helpers for a rendered master or MP4 (the hill-climb-story
review.py re-pointed at this cut's timeline; origin menu-evolution-promo-20261029, revisions/readable-holds).
pixels() samples this cut's panes; motion() marks the edit's intentional reading holds (sources/promo/reads.json).

  review.py motion VIDEO              per-frame change; frozen runs (>= 20 identical frames), each marked
                                      inside or outside an intentional reading hold; a change profile per
                                      2 s window; mean change inside the holds vs their reveals
  review.py strips VIDEO OUT FRAME... consecutive-frame strips (every 2nd frame, -6..+22) per frame
  review.py pixels MASTER             exact-integer-scale check: pane pixels vs. 4x/3x/2x nearest copies of
                                      the source PNGs at sampled frames (FFV1 master only)
  review.py audio VIDEO               loudness per chapter (ebur128) and true peak
  review.py stereo VIDEO              L/R RMS balance per chapter
  review.py stingers                  each stinger's level against the bed under it, from the edit (PCM)
  review.py edl                       edit-list intervals inside their takes; evidence stills present
Inputs: edit.py (same directory) for its chapter and source map.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edit as ed  # noqa: E402

W, H = 1920, 1080


def decode(video, w=W, h=H, start=None, frames=None, scale=None):
    vf = []
    if start is not None:
        vf.append(f'select=between(n\\,{start}\\,{start + frames - 1})')
    if scale:
        vf.append(f'scale={scale[0]}:{scale[1]}:flags=area')
        w, h = scale
    cmd = ['ffmpeg', '-v', 'error', '-i', str(video)]
    if vf:
        cmd += ['-vf', ','.join(vf), '-fps_mode', 'passthrough']
    cmd += ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def motion(video):
    prev, same, runs, diffs = None, 0, [], []
    for i, fr in enumerate(decode(video, scale=(480, 270))):
        if prev is not None:
            d = float(np.abs(fr.astype(np.int16) - prev).mean())
            diffs.append(d)
            if d == 0:
                same += 1
            else:
                if same >= 20:
                    runs.append((i - same, i))
                same = 0
        prev = fr
    if same >= 20:
        runs.append((len(diffs) + 1 - same, len(diffs) + 1))
    import json
    holds = [(r['settle'], r['transition'], r['id']) for r in
             json.loads((Path(__file__).resolve().parent / 'reads.json').read_text())['reads']]
    tag = lambda a, b: next((f'intentional reading hold "{k}"' for s0, t0, k in holds if s0 <= a and b <= t0 + 1),
                            'outside any reading hold')
    print(f'{len(diffs) + 1} frames; frozen runs (>=20 identical frames): '
          + (', '.join(f'{a}-{b} ({a / 60:.2f}-{b / 60:.2f}s, {tag(a, b)})' for a, b in runs) or 'none'))
    d = np.array(diffs)
    inside = np.zeros(len(d), bool)
    for s0, t0, _ in holds:
        inside[max(0, s0):max(0, t0 - 1)] = True
    print(f'  mean change per frame inside the reading holds {d[inside].mean():.2f}, elsewhere {d[~inside].mean():.2f} '
          f'(480x270; inside the holds only the background drift and the moving menus change)')
    for s in range(0, len(d), 120):
        w_ = d[s:s + 120]
        print(f'  {s / 60:5.1f}-{min(len(d), s + 120) / 60:5.1f}s  changed frames {int((w_ > 0).sum()):3d}/120  '
              f'mean {w_.mean():5.2f}  max {w_.max():6.2f}  still runs >=30: {longest_still(w_)}')
    return runs, diffs


def longest_still(w_):
    best = cur = 0
    for v in w_:
        cur = cur + 1 if v == 0 else 0
        best = max(best, cur)
    return best


def strips(video, out, frames):
    from PIL import Image
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for t in frames:
        picks = list(range(t - 6, t + 24, 2))
        ims = list(decode(video, start=picks[0], frames=picks[-1] - picks[0] + 1))[::2]
        tw, th = 480, 270
        sheet = Image.new('RGB', (tw * 5, th * ((len(ims) + 4) // 5)))
        for k, im in enumerate(ims):
            sheet.paste(Image.fromarray(im).resize((tw, th), Image.BILINEAR), ((k % 5) * tw, (k // 5) * th))
        p = out / f'strip-{t:05d}.png'
        sheet.save(p)
        print(p)


def pixels(master):
    """Sampled panes against nearest-neighbour integer copies of their sources (clip frames or the
    audit's capture stills). Regions avoid only the cut's own overlays (wall seams and group labels)."""
    ed.edit()
    F = ed.F
    clip = lambda era, take, i: ed.clip(era, take).native(i).astype(np.uint8)
    still = lambda k: ed.still(k).astype(np.uint8)
    checks = []   # (label, output frame, native source array, x, y, scale, rows, cols)
    full = (0, 224), (0, 320)
    for f, era, s0s, t_in in ((F(8), 'pre', ed.WALL_PRE, 0), (F(125), 'new', ed.WALL_NEW, ed.IRIS)):
        for k in (0, 2, 3, 5):
            g, label, take = ed.GROUPS[k]
            i = s0s[take] + f - t_in
            if era == 'new' and k == 0:     # the delivered wall's hub cell is the follow-up still
                checks.append(('wall hub cell: still hub_fu (follow-up, d6771c478)', f, still('hub_fu'), 0, 92, 2,
                               (0, 180), (0, 320)))
                continue
            checks.append((f'wall {era}/{take}#{i}', f, clip(era, take, i), (k % 3) * 640, 92 + (k // 3) * 448, 2,
                           (4, 180), (2, 318)))
    for f, era, part in ((F(35.1), 'pre', 'lib'), (F(37.5), 'new', 'lib'), (ed.LEGAL_T, 'pre', 'notice'),
                         (F(44), 'new', 'notice')):
        take = ed.SRC[part][1]
        i = ed.src(part, f)
        checks.append((f'{era}/{take}#{i}', f, clip(era, take, i), *ed.PANE_L, 4, *full))
    for f, key in ((F(71.75), 'hub_t8'), (F(75), 'hub_p1'), (F(92), 'hub_str'), (F(102.5), 'set_str')):
        checks.append((f'still {key}', f, still(key), *ed.EP, 3, *full))
    checks.append(('still hub_rev (1:1 of its 3x image)', F(85), still('hub_rev'), *ed.EP, 1, (0, 672), (0, 960)))
    f = F(108)
    i = ed.src('set_fin', f)
    checks.append((f'new/settings#{i}', f, clip('new', 'settings', i), *ed.EP, 3, *full))
    ok = 0
    for label, f, src, x, y, s, (r0, r1), (c0, c1) in checks:
        got = next(decode(master, start=f, frames=1))
        want = np.repeat(np.repeat(src[r0:r1, c0:c1], s, 0), s, 1)
        region = got[y + r0 * s:y + r0 * s + want.shape[0], x + c0 * s:x + c0 * s + want.shape[1]]
        bad = int((region != want).any(axis=2).sum())
        ok += bad == 0
        print(f'frame {f}: {label} at {s}x rows {r0}-{r1 - 1} cols {c0}-{c1 - 1} -> '
              f'{"exact" if bad == 0 else f"{bad} pixels differ"}')
    print(f'{ok}/{len(checks)} panes exact integer nearest-neighbour copies of their sources')


def _ebur(video, f0, f1):
    r = subprocess.run(['ffmpeg', '-nostats', '-ss', f'{f0 / 60:.3f}', '-t', f'{(f1 - f0) / 60:.3f}', '-i', str(video),
                        '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    return float(tail.split('I:')[1].split('LUFS')[0]), float(tail.split('Peak:')[1].split('dBFS')[0])


def audio(video):
    ed.edit()
    integ, peak = _ebur(video, 0, ed.TOTAL)
    print(f'whole film: I {integ:6.1f} LUFS  TP {peak:+5.1f} dBTP')
    for f0, f1, title in ed.CHAPTERS:
        integ, peak = _ebur(video, f0, f1)
        print(f'{f0 / 60:6.2f}-{f1 / 60:6.2f}s  I {integ:6.1f} LUFS  TP {peak:+5.1f} dBTP  {title}')


def stereo(video):
    ed.edit()
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 's16le', '-ac', '2', '-ar', '48000', '-'],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for f0, f1, title in ed.CHAPTERS:
        seg = a[f0 * 800:f1 * 800]
        l, rr = np.sqrt((seg[:, 0] ** 2).mean()), np.sqrt((seg[:, 1] ** 2).mean())
        print(f'{f0 / 60:6.2f}-{f1 / 60:6.2f}s  L {20 * np.log10(l):6.1f} dB  R {20 * np.log10(rr):6.1f} dB  '
              f'L-R {20 * np.log10(l / rr):+5.2f} dB  {title}')
    tail = a[ed.BED_CUT * 800 + 800:]
    print(f'after the bed cut (frame {ed.BED_CUT + 1}-): peak {np.abs(tail).max():.5f}')


def stingers():
    """Every stinger's loudest 100 ms (with its gain) against the bed under it, grouped by sound, and
    its L/R difference; then promo_kit's own sound_balance warnings."""
    from promo_kit import read_wav, SR
    e = ed.edit()
    bed = read_wav(e.beds[0][0])
    gain_bed = e.beds[0][2]
    rows = {}
    win = SR // 10
    cache = {}
    for f, wav, gain, length in e.sfx:
        a = cache.setdefault(wav, read_wav(wav))
        p_ = (a ** 2).mean(axis=1)
        n = min(win, len(a))
        i = int(np.argmax(np.convolve(p_, np.ones(n) / n, mode='valid')))
        loud = a[i:i + n] * gain
        at = f * 800 + i
        under = bed[at:at + n] * gain_bed
        lv = lambda x: 20 * np.log10(max(float(np.sqrt((x ** 2).mean())), 1e-9))
        rows.setdefault(Path(wav).name, []).append((lv(loud) - lv(under), lv(loud[:, 0]) - lv(loud[:, 1])))
    for name, v in sorted(rows.items()):
        d = np.array(v)
        print(f'{name:24s} x{len(v):2d}  stinger - bed {d[:, 0].min():+5.1f} .. {d[:, 0].max():+5.1f} dB  '
              f'L-R {d[:, 1].min():+5.1f} .. {d[:, 1].max():+5.1f} dB')
    for w in e.sound_balance():
        print('warning:', w)
    print('sound_balance warnings: listed above (none if no lines)')


def edl():
    """Every 'era/take take frames a-b' interval in edl.csv lies inside its take; every still exists."""
    import csv
    import re
    ed.edit()
    n_ok = n = 0
    for row in csv.DictReader((Path(__file__).resolve().parent / 'edl.csv').open()):
        for era, take, a, b in re.findall(r'([a-z+]+)/([a-z0-9-]+) take frames (\d+)-(\d+)', row['sources']):
            for e in era.split('+'):
                n += 1
                total = ed.clip(e, take).n
                good = 0 <= int(a) <= int(b) < total
                n_ok += good
                if not good:
                    print(f'BAD {e}/{take} {a}-{b} (take has {total} frames) in {row["chapter"]}')
        for rel in re.findall(r'([\w./-]+\.png)', row['sources']):
            n += 1
            n_ok += (ed.EVID / rel).is_file()
    print(f'{n_ok}/{n} source intervals and stills valid')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'edl':
        edl()
    if cmd == 'motion':
        motion(sys.argv[2])
    elif cmd == 'strips':
        strips(sys.argv[2], sys.argv[3], [int(a) for a in sys.argv[4:]])
    elif cmd == 'pixels':
        pixels(sys.argv[2])
    elif cmd == 'audio':
        audio(sys.argv[2])
    elif cmd == 'stereo':
        stereo(sys.argv[2])
    elif cmd == 'stingers':
        stingers()
