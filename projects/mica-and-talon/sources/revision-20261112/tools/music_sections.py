#!/usr/bin/env python3
"""Purpose: per-bar features on the TRACKED bar lines (tools/beat_track.py), to place chapters on real section
changes and find the last clean phrase boundary. Prints loudness, band balance, chord guess, bass pitch class,
similarity to the bar 1/4/8 back, and 2-bar energy steps.
Inputs: WAV, beat-track.json, [json out]. Origin: MICA & TALON promo redo 2026-11-11."""
import json, sys, wave
import numpy as np
p, bt = sys.argv[1], json.load(open(sys.argv[2]))
w = wave.open(p); sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
x = np.frombuffer(w.readframes(n), np.int16).reshape(-1, ch).astype(np.float32) / 32768
m = x.mean(1)
T = [b['t'] for b in bt['bars']]
T.append(T[-1] + (T[-1] - T[-2]))
hop, win = 480, 4096
fr = np.lib.stride_tricks.sliding_window_view(np.pad(m, (win // 2, win)), win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1)).astype(np.float32); f = np.fft.rfftfreq(win, 1 / sr); fps = sr / hop
valid = (f > 60) & (f < 2000); pc = (np.round(12 * np.log2(f[valid] / 440.0)) % 12).astype(int)
bassv = (f > 40) & (f < 180); bpc = (np.round(12 * np.log2(f[bassv] / 440.0)) % 12).astype(int)
NOTES = 'A A# B C C# D D# E F F# G G#'.split()
TRI = {}
for r in range(12):
    for nm, iv in (('', (0, 4, 7)), ('m', (0, 3, 7))):
        v = np.zeros(12); v[[(r + i) % 12 for i in iv]] = 1; TRI[NOTES[r] + nm] = v
rows, feats = [], []
for b in range(len(T) - 1):
    a, z = int(T[b] * sr), int(min(n, T[b + 1] * sr)); fa, fz = int(T[b] * fps), int(min(len(S), T[b + 1] * fps))
    seg = m[a:z]; sp = (S[fa:fz] ** 2).mean(0)
    rms = 10 * np.log10((seg ** 2).mean() + 1e-12)
    lo = 10 * np.log10(sp[f < 150].sum() + 1e-9); hi = 10 * np.log10(sp[f >= 4000].sum() + 1e-9); mid = 10 * np.log10(sp[(f >= 150) & (f < 4000)].sum() + 1e-9)
    c = np.array([sp[valid][pc == k].sum() for k in range(12)]); c /= c.sum() + 1e-9
    bc = np.array([sp[bassv][bpc == k].sum() for k in range(12)])
    chord = max(TRI, key=lambda k: float((TRI[k] * c).sum()))
    # two half-bar chords
    hm = (fa + fz) // 2
    halves = []
    for (u, v) in ((fa, hm), (hm, fz)):
        s2 = (S[u:v] ** 2).mean(0); c2 = np.array([s2[valid][pc == k].sum() for k in range(12)])
        halves.append(max(TRI, key=lambda k: float((TRI[k] * c2).sum())))
    feats.append(np.r_[c / (np.linalg.norm(c) + 1e-9), np.log1p(sp[:600]) / (np.linalg.norm(np.log1p(sp[:600])) + 1e-9)])
    rows.append(dict(bar=b, t=float(T[b]), rms=float(rms), lo=float(lo), mid=float(mid), hi=float(hi), chord=chord, halves='/'.join(halves), bass=NOTES[int(bc.argmax())]))
cs = lambda a, b: float((a * b).sum() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
print('bar      t    rms    lo   mid    hi  chord halves    bass  s1   s4   s8   step2')
for i, r in enumerate(rows):
    s1 = cs(feats[i], feats[i - 1]) if i else 1; s4 = cs(feats[i], feats[i - 4]) if i >= 4 else 0; s8 = cs(feats[i], feats[i - 8]) if i >= 8 else 0
    step = (np.mean([q['rms'] for q in rows[i:i + 2]]) - np.mean([q['rms'] for q in rows[max(0, i - 2):i]])) if i else 0
    r.update(s1=s1, s4=s4, s8=s8, step2=step)
    print('%3d %7.2f %5.1f %5.1f %5.1f %5.1f  %-4s %-9s %-3s %.2f %.2f %.2f %+5.1f' % (i, r['t'], r['rms'], r['lo'], r['mid'], r['hi'], r['chord'], r['halves'], r['bass'], s1, s4, s8, step))
if len(sys.argv) > 3:
    json.dump(rows, open(sys.argv[3], 'w'), indent=1)
