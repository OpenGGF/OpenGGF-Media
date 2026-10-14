#!/usr/bin/env python3
"""Tempo and beat-phase estimate for a rendered track: spectral-flux onsets, autocorrelation for
the period, then the phase whose comb best matches the onsets. Prints BPM, the first beat and
loudness per 4 s."""
import sys, wave
import numpy as np

def load(path):
    w = wave.open(path)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768
    return a.mean(axis=1), w.getframerate()

def onsets(x, sr, hop=480):
    n = 2048
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
    mag = np.log1p(np.abs(np.fft.rfft(frames, axis=1)) * 10)
    flux = np.maximum(mag[1:] - mag[:-1], 0).sum(axis=1)
    flux -= np.convolve(flux, np.ones(16) / 16, mode="same")
    return np.maximum(flux, 0), sr / hop

def tempo(path, start=0.0, length=40.0):
    x, sr = load(path)
    seg = x[int(start * sr):int((start + length) * sr)]
    env, fps = onsets(seg, sr)
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    lags = np.arange(len(ac)) / fps
    ok = (lags > 60 / 200) & (lags < 60 / 70)
    lag = np.argmax(np.where(ok, ac, 0))
    # refine the period across the whole segment with a fine search around the peak
    best = None
    for period in np.linspace(lag / fps * 0.97, lag / fps * 1.03, 400):
        for ph in np.linspace(0, period, 60, endpoint=False):
            idx = ((np.arange(ph, len(env) / fps, period)) * fps).astype(int)
            idx = idx[idx < len(env)]
            s = env[idx].mean()
            if best is None or s > best[0]:
                best = (s, period, ph)
    _, period, ph = best
    return 60 / period, start + ph, x, sr

if __name__ == "__main__":
    for p in sys.argv[1:]:
        bpm, first, x, sr = tempo(p)
        rms = [20 * np.log10(np.sqrt((x[int(s * sr):int((s + 4) * sr)] ** 2).mean()) + 1e-9) for s in range(0, 100, 4)]
        nz = np.nonzero(np.abs(x) > 0.003)[0]
        print(f"{p}: {bpm:.2f} BPM, beat at {first:.3f}s, sound {nz[0]/sr:.2f}-{nz[-1]/sr:.2f}s")
        print("   dB/4s:", " ".join(f"{r:.0f}" for r in rms))
