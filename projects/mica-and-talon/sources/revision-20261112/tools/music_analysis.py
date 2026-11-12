#!/usr/bin/env python3
"""Purpose: decide where the owner-supplied bed can end on a clean phrase boundary before its ending degrades.
Per-bar loudness, band energy, onset-grid alignment, local tempo, chroma key stability, bar-to-bar and
phrase-to-phrase similarity, and a section-novelty curve. Prints a table and writes JSON for the storyboard.
Inputs: WAV, bpm, bar-0 seconds, [json out]. Origin: MICA & TALON promo redo 2026-11-11.
"""
import json, sys, wave
import numpy as np

p, bpm, first = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
w = wave.open(p)
sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
x = np.frombuffer(w.readframes(n), {2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(np.float32) / 2 ** (8 * sw - 1)
m = x.mean(1)
side = (x[:, 0] - x[:, 1]) / 2 if ch == 2 else m * 0
hop, win = 240, 2048  # 5 ms hop
fr = np.lib.stride_tricks.sliding_window_view(np.pad(m, (win // 2, win)), win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1)).astype(np.float32)
f = np.fft.rfftfreq(win, 1 / sr)
fps = sr / hop
logS = np.log1p(50 * S)
flux = np.r_[0, np.maximum(0, np.diff(logS, axis=0)).sum(1)]


def band(lo, hi):
    e = np.log1p(100 * S[:, (f >= lo) & (f < hi)].sum(1))
    return np.maximum(0, np.diff(e, prepend=e[0]))


kick, snare = band(30, 130), band(1500, 6000)


def pk(v, t):
    i = int(t * fps)
    seg = v[max(0, i - 4):i + 5]
    return float(seg.max()) if len(seg) else 0.0

# chroma
A4 = 440.0
valid = (f > 55) & (f < 4000)
pc = (np.round(12 * np.log2(f[valid] / A4)) % 12).astype(int)
chroma = np.zeros((len(S), 12), np.float32)
for k in range(12):
    chroma[:, k] = (S[:, valid][:, pc == k] ** 2).sum(1)
bp = 60 / bpm
bar = 4 * bp
nb = int((n / sr - first) / bar) + 1
KRUM_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KRUM_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
NOTES = 'C C# D D# E F F# G G# A A# B'.split()


def key_of(c):
    best = (-9, '')
    for k in range(12):
        for nm, prof in (('', KRUM_MAJ), ('m', KRUM_MIN)):
            r = np.corrcoef(np.roll(prof, k), c)[0, 1]
            if r > best[0]:
                best = (r, NOTES[k] + nm)
    return best


rows = []
barchroma, barspec, barons = [], [], []
for b in range(nb):
    t0, t1 = first + b * bar, first + (b + 1) * bar
    a, z = int(t0 * sr), int(min(n, t1 * sr))
    if z - a < sr * 0.2:
        break
    fa, fz = int(t0 * fps), int(min(len(S), t1 * fps))
    seg = m[a:z]
    rms = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    srms = 20 * np.log10(np.sqrt((side[a:z] ** 2).mean()) + 1e-9)
    sp = S[fa:fz].mean(0)
    lo, mid, hi = sp[f < 150].sum(), sp[(f >= 150) & (f < 4000)].sum(), sp[f >= 4000].sum()
    cen = (sp * f).sum() / (sp.sum() + 1e-9)
    # grid alignment: share of onset flux within +-25 ms of the 16th grid in this bar
    o = flux[fa:fz]
    tt = (np.arange(fa, fz) / fps - first) / (bp / 4)
    d = np.abs(tt - np.round(tt)) * (bp / 4)
    align = o[d < 0.025].sum() / (o.sum() + 1e-9)
    # kick on beats / snare on backbeats strength
    kb = sum(pk(kick, t0 + k * bp) for k in range(4)) / 4
    sb = sum(pk(snare, t0 + k * bp) for k in (1, 3)) / 2
    c = chroma[fa:fz].sum(0)
    c = c / (c.sum() + 1e-9)
    kr, kn = key_of(c)
    # 16-step onset pattern for rhythm similarity
    pat = np.array([pk(flux, t0 + s * bp / 4) for s in range(16)])
    barchroma.append(c); barspec.append(np.log1p(sp[:400])); barons.append(pat)
    rows.append(dict(bar=b, t=round(t0, 3), rms=round(float(rms), 1), side=round(float(srms), 1), lo=float(lo), mid=float(mid), hi=float(hi),
                     cen=round(float(cen)), align=round(float(align), 3), kick=round(float(kb), 2), snare=round(float(sb), 2),
                     key=kn, keyr=round(float(kr), 2), flux=round(float(o.mean()), 1)))


def cos(a, b):
    return float((a * b).sum() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


N = len(rows)
feat = [np.r_[barchroma[i] * 8, barspec[i] / np.linalg.norm(barspec[i]), barons[i] / (np.linalg.norm(barons[i]) + 1e-9)] for i in range(N)]
SS = np.array([[cos(feat[i], feat[j]) for j in range(N)] for i in range(N)])
K = 4
for i in range(N):
    r = rows[i]
    r['sim1'] = round(cos(barchroma[i], barchroma[i - 1]), 3) if i else 1
    r['sim4'] = round(float(SS[i, i - 4]), 3) if i >= 4 else None
    r['sim8'] = round(float(SS[i, i - 8]), 3) if i >= 8 else None
    r['rhy1'] = round(cos(barons[i], barons[i - 1]), 3) if i else 1
    if K <= i <= N - K:
        A, Bq = SS[i - K:i, i - K:i].mean(), SS[i:i + K, i:i + K].mean()
        C = SS[i - K:i, i:i + K].mean()
        r['nov'] = round(float((A + Bq) / 2 - C), 3)
    else:
        r['nov'] = None
# local tempo: best lag of the flux autocorrelation in a +-4 bar window
for i in range(N):
    a, z = int((first + max(0, i - 2) * bar) * fps), int((first + min(N, i + 2) * bar) * fps)
    o = flux[a:z] - flux[a:z].mean()
    best = (-9, 0)
    for cand in np.arange(bpm - 6, bpm + 6.01, 0.25):
        lag = 60 / cand * fps * 4  # bar lag
        l0 = int(np.floor(lag)); fr_ = lag - l0
        if l0 + 1 >= len(o):
            continue
        v = (1 - fr_) * (o[:-l0] * o[l0:]).sum() + fr_ * (o[:-l0 - 1] * o[l0 + 1:]).sum()
        v /= (o * o).sum() + 1e-9
        if v > best[0]:
            best = (v, cand)
    rows[i]['tempo'] = best[1]; rows[i]['tempo_r'] = round(float(best[0]), 3)
print('sr', sr, 'dur %.3f' % (n / sr), 'bars', N, 'bar %.4f s' % bar)
print('bar     t    rms  side   cen  align kick snare key   kr  sim1 sim4 sim8 rhy1  nov  tempo  tr')
for r in rows:
    print('%3d %7.2f %5.1f %5.1f %5d %5.2f %5.2f %5.2f %-3s %4.2f %5.2f %4s %4s %5.2f %5s %6.2f %4.2f' % (
        r['bar'], r['t'], r['rms'], r['side'], r['cen'], r['align'], r['kick'], r['snare'], r['key'], r['keyr'], r['sim1'],
        '' if r['sim4'] is None else '%.2f' % r['sim4'], '' if r['sim8'] is None else '%.2f' % r['sim8'], r['rhy1'],
        '' if r['nov'] is None else '%.2f' % r['nov'], r['tempo'], r['tempo_r']))
if out:
    json.dump(dict(sr=sr, dur=n / sr, bpm=bpm, first=first, bar=bar, rows=rows), open(out, 'w'), indent=1)
