#!/usr/bin/env python3
"""Super Sonic cut: review and verification helpers for a rendered master or MP4 (revision of the
original production's review.py; origin menu-evolution-promo-20261029, revisions/super-sonic-cut).

  review.py motion VIDEO              per-frame change; frozen runs (>= 20 identical frames); a change
                                      profile per 2 s window (the measurable half of the viewer pass)
  review.py strips VIDEO OUT FRAME... consecutive-frame strips (every 2nd frame, -6..+22) per frame
  review.py pixels MASTER             exact-integer-scale check: pane pixels vs. 4x/3x/2x nearest copies of
                                      the source PNGs at sampled frames (FFV1 master only)
  review.py audio VIDEO               loudness per chapter (ebur128) and true peak
  review.py stereo VIDEO              L/R RMS balance per chapter
  review.py stingers                  each stinger's level against the bed under it, from the edit (PCM)
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
    print(f'{len(diffs) + 1} frames; frozen runs (>=20 identical frames): '
          + (', '.join(f'{a}-{b} ({a / 60:.2f}-{b / 60:.2f}s)' for a, b in runs) or 'none'))
    d = np.array(diffs)
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
    ed.edit()
    checks = []  # (output frame, era, take, take frame, x, y, scale, (col0, col1) native columns compared)
    full = (0, 320)
    for part in ('lib1', 'lib2', 'set1', 'set2', 'set3'):
        era, take, f0, f1, _ = ed.SRC[part]
        for f in (f0 + 10, f1 - 10):
            key = 'libraries' if part.startswith('lib') else 'settings'
            d = 320 if era == 'new' else ed.divider_at(f, key, 12 if part == 'set1' else 10)
            e = 'new' if d >= 320 else 'pre' if d <= 0 else None
            if e:
                checks.append((f, e, take, ed.src(part, f), *ed.PANE_L, 4, full))
    for f in (ed.F(2), ed.F(7)):
        e = 'pre' if f < ed.F(4) else 'new'
        checks.append((f, e, 'shader', ed.src('cold', f), *ed.PANE_C, 4, full))
    checks.append((ed.F(18), 'v05', 'v05-title', ed.src('v05', ed.F(18)), *ed.PANE_C, 4, full))
    checks.append((ed.F(22), 'pre', 'hub', ed.src('prehub', ed.F(22)), *ed.PANE_C, 4, full))
    for part in ('pick1', 'pick2'):
        f = ed.SRC[part][2] + 60
        # side by side: native column 319 (old) and 0 (new) sit under the 6 px centre rule
        checks.append((f, 'pre', 'locate', ed.src(part, f), 0, ed.TWO_Y, 3, (0, 319)))
        checks.append((f, 'new', 'locate', ed.src(part, f), 960, ed.TWO_Y, 3, (1, 320)))
    f = ed.F(79)
    for k in (0, 4):
        take, s0 = ed.WALL[k]
        checks.append((f, 'new', take, s0 + f - ed.F(72), (k % 3) * 640, 92 + (k // 3) * 448, 2, full))
    f = ed.F(93)
    checks.append((f, 'new', 'hub', ed.src('hero', f), *ed.PANE_C, 4, full))
    ok = 0
    for f, era, take, i, x, y, s, (c0, c1) in checks:
        got = next(decode(master, start=f, frames=1))
        src = ed.clip(era, take).native(i).astype(np.uint8)[:, c0:c1]
        want = np.repeat(np.repeat(src, s, 0), s, 1)
        region = got[y:y + want.shape[0], x + c0 * s:x + c0 * s + want.shape[1]]
        bad = int((region != want).any(axis=2).sum())
        ok += bad == 0
        print(f'frame {f}: {era}/{take}#{i} at {s}x cols {c0}-{c1 - 1} -> '
              f'{"exact" if bad == 0 else f"{bad} pixels differ"}')
    print(f'{ok}/{len(checks)} panes exact integer nearest-neighbour copies of their source frames')


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


if __name__ == '__main__':
    cmd = sys.argv[1]
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
