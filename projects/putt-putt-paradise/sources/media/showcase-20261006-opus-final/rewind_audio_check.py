#!/usr/bin/env python3
"""Does the captured rewind sound like the shot played backwards? (Opus, 2026-10-06, r5)

For a capture with a whole-shot rewind, take the audio of the rows the rewind presentation covers
(state.csv rewind_intensity > 0) and the audio of the shot it undoes (from the shot's commit to the
rewind request). Reverse the rewind audio, resample it over a range of playback rates (the rewind
may run faster than real time) and slide it along the forward audio; report the best normalised
correlation of the two loudness envelopes (5 ms RMS hops), and the same score for the rewind
audio NOT reversed. Real reverse playback scores high reversed and clearly lower unreversed;
forward-only audio under a rewind picture shows no such asymmetry.

Then, sample-exactly: every rewind row's 800-sample packet is reversed and located in the recorded
forward shot audio by normalised cross-correlation at every offset (integer replay rates 1-4
tried). A true backwards replay matches packet by packet (correlation ~1.0) and the matched
forward rows walk backwards monotonically; "per_packet" lists every row's match.

Usage: rewind_audio_check.py CAPTURE_DIR [shot_event request_event]   (writes rewind-audio.json)
Defaults: practice EHZ1 events "shot-committed" (the one before the request) and "rewind-request".
For the online host the events are "shot-1" and "guest-rewind-request".
"""
import csv
import json
import sys
import wave
from pathlib import Path

import numpy as np

SPF, HOP = 800, 240


def env(x):
    n = len(x) // HOP
    return np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(axis=1) + 1e-12)


def best(fwd, probe):
    out = (-1.0, None, None)
    for rate in np.linspace(0.75, 4.0, 66):
        m = int(round(len(probe) * rate))
        if m < 8 or m > len(fwd):
            continue
        p = np.interp(np.linspace(0, len(probe) - 1, m), np.arange(len(probe)), probe)
        p = (p - p.mean()) / (p.std() + 1e-9)
        for off in range(0, len(fwd) - m + 1, 2):
            f = fwd[off:off + m]
            c = float(np.dot(p, (f - f.mean()) / (f.std() + 1e-9)) / m)
            if c > out[0]:
                out = (c, float(rate), off)
    return out


def packet_matches(x, forward_rows, rewind_rows, rates=(1, 2, 3, 4)):
    """Per-packet proof of reverse playback. Each rewind row's 800-sample packet (left channel) is
    reversed and located in the forward shot audio by normalised cross-correlation (every offset,
    FFT). For an integer replay rate s the packet covers s*800 forward samples, so the forward
    audio is also tried decimated by s. Returns one record per rewind row."""
    a, b = forward_rows
    out = []
    for s_ in rates:
        f = x[a * SPF:b * SPF:s_]
        n = 1 << int(np.ceil(np.log2(len(f) + SPF)))
        Fh = np.fft.rfft(f, n)
        cs = np.concatenate([[0.0], np.cumsum(f * f)])
        e = np.sqrt(np.maximum(cs[SPF:] - cs[:-SPF], 1e-12))
        for i, r in enumerate(range(*rewind_rows)):
            pkt = x[r * SPF:(r + 1) * SPF][::-1]
            if len(out) <= i:
                out.append({"row": r, "corr": -1.0})
            if np.linalg.norm(pkt) < 1e-4:
                out[i]["silent"] = True
                continue
            c = np.fft.irfft(Fh * np.conj(np.fft.rfft(pkt, n)), n)[:len(f) - SPF + 1] / (e[:len(f) - SPF + 1] * np.linalg.norm(pkt))
            k = int(np.argmax(c))
            if c[k] > out[i]["corr"]:
                out[i].update({"corr": round(float(c[k]), 4), "rate": s_, "forward_row": round(a + k * s_ / SPF, 3)})
    return out


def main():
    cap = Path(sys.argv[1])
    shot_ev = sys.argv[2] if len(sys.argv) > 2 else "shot-committed"
    req_ev = sys.argv[3] if len(sys.argv) > 3 else "rewind-request"
    ev = [(int(r), n) for r, n in (l.split(",", 1) for l in (cap / "events.csv").read_text().splitlines()[1:])]
    req = next(r for r, n in ev if n == req_ev)
    shot = max(r for r, n in ev if n == shot_ev and r < req)
    rows = list(csv.reader(open(cap / "state.csv")))
    ri = rows[0].index("rewind_intensity")
    active = [k for k, r in enumerate(rows[1:]) if k >= req and float(r[ri]) > 0]
    a, b = active[0], active[-1] + 1
    with wave.open(str(cap / "gameplay.wav")) as w:
        stereo = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    x, x_left = stereo.mean(axis=1), stereo[:, 0].copy()
    fwd = env(x[shot * SPF:req * SPF])
    rew = env(x[a * SPF:b * SPF])
    rev_score, rev_rate, rev_off = best(fwd, rew[::-1])
    fwd_score, fwd_rate, fwd_off = best(fwd, rew)
    left = x_left
    packets = packet_matches(left, (shot, req), (a, b))
    voiced = [p for p in packets if not p.get("silent")]
    matched = [p for p in voiced if p["corr"] > 0.98]
    steps = [q["forward_row"] - p["forward_row"] for p, q in zip(matched, matched[1:])]
    # Integer proof on both channels: a rate-1 match on a whole forward row must reproduce that
    # row's int16 stereo samples exactly, reversed in time.
    with wave.open(str(cap / "gameplay.wav")) as w:
        raw = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)
    exact = 0
    for q in matched:
        fr = q["forward_row"]
        if q.get("rate") == 1 and abs(fr - round(fr)) < 1e-6:
            fr = int(round(fr))
            if np.array_equal(raw[q["row"] * SPF:(q["row"] + 1) * SPF][::-1], raw[fr * SPF:(fr + 1) * SPF]):
                exact += 1
    level = float(20 * np.log10(max(np.sqrt((x[a * SPF:b * SPF] ** 2).mean()), 1e-9)))
    report = {"capture": cap.name, "shot_row": shot, "request_row": req, "rewind_rows": [a, b - 1],
              "rewind_level_dbfs": round(level, 1),
              "reversed": {"corr": round(rev_score, 3), "rate": rev_rate, "offset_hops": rev_off},
              "unreversed": {"corr": round(fwd_score, 3), "rate": fwd_rate, "offset_hops": fwd_off},
              "packets": {"voiced": len(voiced), "sample_exact_reversed": len(matched),
                          "min_corr": min((p["corr"] for p in voiced), default=None),
                          "rates": sorted({p.get("rate") for p in matched}),
                          "forward_rows_first_last": [matched[0]["forward_row"], matched[-1]["forward_row"]] if matched else None,
                          "steps_per_row": sorted({round(v, 3) for v in steps}),
                          "unmatched_rows": [p["row"] for p in voiced if p["corr"] <= 0.98],
                          "stereo_int16_identical_reversed": exact},
              "per_packet": packets,
              "reverse_evident": rev_score > 0.6 and rev_score - fwd_score > 0.15 and level > -50,
              "waveform_reverse_match": len(voiced) > 0 and len(matched) >= 0.9 * len(voiced) and all(v < 0 for v in steps)}
    (cap / "rewind-audio.json").write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
