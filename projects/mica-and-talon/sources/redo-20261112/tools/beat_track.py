#!/usr/bin/env python3
"""Purpose: track the real bar lines of the owner-supplied bed (its tempo is not constant), so cuts sit on the
uncut track's own beat grid, and measure where the pulse stops being trackable.
Method: PLL-style comb tracker on a 2.5 ms spectral-flux envelope. For each bar, search local beat period and
phase over a +-2-bar window (beats weighted 1, off-beat eighths 0.5), with a small penalty on leaving the
predicted phase; step one bar and repeat. Reports per bar: tracked downbeat time, drift against the fixed
172.218 BPM grid, local BPM, comb contrast (on-grid flux / mean flux), and beat-interval jitter.
Inputs: WAV, bar-0 seconds, initial bpm, [json out]. Origin: MICA & TALON promo redo 2026-11-11.
"""
import json, sys, wave
import numpy as np

p, first, bpm0 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
w = wave.open(p)
sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
m = np.frombuffer(w.readframes(n), np.int16).reshape(-1, ch).astype(np.float32).mean(1) / 32768
hop, win = 120, 1024
fr = np.lib.stride_tricks.sliding_window_view(np.pad(m, (win // 2, win)), win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1)).astype(np.float32)
f = np.fft.rfftfreq(win, 1 / sr)
fps = sr / hop
flux = np.r_[0, np.maximum(0, np.diff(np.log1p(50 * S), axis=0)).sum(1)]
# smooth 3 taps so a +-2.5 ms miss still scores
flux = np.convolve(flux, [0.25, 0.5, 0.25], 'same')
lowS = np.log1p(100 * S[:, (f >= 30) & (f < 130)].sum(1)); kick = np.maximum(0, np.diff(lowS, prepend=lowS[0]))
snS = np.log1p(100 * S[:, (f >= 1500) & (f < 6000)].sum(1)); snare = np.maximum(0, np.diff(snS, prepend=snS[0]))
dur = n / sr


def at(v, t):
    i = np.round(np.asarray(t) * fps).astype(int)
    ok = (i >= 0) & (i < len(v))
    r = np.zeros(len(i)); r[ok] = v[i[ok]]
    return r


def comb(c, P, span=2):
    j = np.arange(-4 * span, 4 * span + 1)
    return at(flux, c + j * P).sum() + 0.5 * at(flux, c + (j[:-1] + 0.5) * P).sum()


P = 60 / bpm0
t = first
bars = []
while t + 4 * P < dur - 0.5:
    best = (-1e9, 0, P)
    for dP in np.arange(-0.012, 0.0121, 0.0005):          # +-3.5 % around the running period
        for dphi in np.arange(-0.040, 0.0401, 0.0025):
            sc = comb(t + dphi, P + dP) - 60 * abs(dphi) - 400 * abs(dP)
            if sc > best[0]:
                best = (sc, dphi, P + dP)
    _, dphi, Pn = best
    t += dphi
    P = 0.7 * P + 0.3 * Pn                                 # low-pass the period
    j = np.arange(0, 4)
    on = at(flux, t + j * P).mean()
    a, z = int(t * fps), int((t + 4 * P) * fps)
    contrast = on / (flux[a:z].mean() + 1e-9)
    # jitter: strongest onset within +-40 ms of each beat, deviation from the beat
    dev = []
    for k in range(4):
        c = int(round((t + k * P) * fps)); wdw = flux[max(0, c - 16):c + 17]
        dev.append((np.argmax(wdw) - min(16, c)) / fps * 1000)
    kd = at(kick, t + np.array([0, 2]) * P).mean(); kb = at(kick, t + np.array([1, 3]) * P).mean()
    sd = at(snare, t + np.array([0, 2]) * P).mean(); sb = at(snare, t + np.array([1, 3]) * P).mean()
    bars.append(dict(bar=len(bars), t=round(float(t), 4), bpm=round(60 / P, 2), contrast=round(float(contrast), 2),
                     jitter_ms=round(float(np.std(dev)), 1), kick13=round(float(kd), 2), kick24=round(float(kb), 2),
                     snare13=round(float(sd), 2), snare24=round(float(sb), 2)))
    t += 4 * P
fixed = lambda b: first + b * 240 / bpm0
print('bar   tracked   fixed   drift_ms   bpm  contrast jitter  k13  k24  s13  s24  barlen')
for i, b in enumerate(bars):
    bl = bars[i + 1]['t'] - b['t'] if i + 1 < len(bars) else 0
    b['drift_ms'] = round((b['t'] - fixed(b['bar'])) * 1000, 1); b['barlen'] = round(bl, 4)
    print('%3d %8.3f %8.3f %8.1f %7.2f %6.2f %6.1f %5.2f %4.2f %4.2f %4.2f %7.4f' % (
        b['bar'], b['t'], fixed(b['bar']), b['drift_ms'], b['bpm'], b['contrast'], b['jitter_ms'], b['kick13'], b['kick24'],
        b['snare13'], b['snare24'], bl))
if out:
    json.dump(dict(first=first, bpm0=bpm0, bars=bars), open(out, 'w'), indent=1)
