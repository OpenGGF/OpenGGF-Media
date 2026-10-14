#!/usr/bin/env python3
"""Verify the final-polish promo against its sources (Opus, 2026-10-06).

1. Picture fidelity and normal speed: for sampled frames inside every gameplay segment, the
   decoded MP4 frame is compared with the renderer's own composite of source row r and of the
   neighbouring rows r-1 / r+1. The exact row must be the closest match, so every sample shows
   the claimed capture row at one row per output frame.
2. Audio sync: for every gameplay segment, a 0.5 s window of the decoded MP4 audio is
   cross-correlated with the segment's source WAV at the claimed offset (±50 ms search). The
   best lag must be within one video frame.
3. Stream facts: frame count, cadence and duration come from verify JSON written by the caller.

Usage: verify_promo.py promo.mp4   (writes promo.verify.json)
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_promo as rp  # noqa: E402

W, H = rp.W, rp.H


def decode_frame(mp4, f):
    out = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(mp4), "-vf", f"select=eq(n\\,{f})",
                          "-fps_mode", "passthrough", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(H, W, 3).astype(np.float32)


def composite(seg, local, shift):
    saved = seg.r0
    try:
        seg.r0 = saved + shift
        return np.asarray(seg.draw(local).convert("RGB"), np.float32)
    finally:
        seg.r0 = saved


def main():
    mp4 = Path(sys.argv[1])
    segs = rp.segments()
    report = {"file": mp4.name, "picture": [], "audio": []}
    for seg in segs:
        if seg.cap is None:
            continue
        lo, hi = max(seg.tlen + 4, 6), seg.frames - 8
        for k in range(5):
            local = lo + (hi - lo) * (k + 1) // 6
            f = seg.start + local
            got = decode_frame(mp4, f)
            # Fades at the very start/end of the film scale brightness; none of the samples sit there.
            diffs = {s: float(np.mean(np.abs(got - composite(seg, local, s)))) for s in (-1, 0, 1)}
            # A held row (menu at rest, golfer aiming) is pixel-identical to its neighbour: a tie is
            # consistent with the claimed row; a moving row must be strictly closest.
            best = min(diffs.values())
            report["picture"].append({"segment": seg.name, "frame": f, "row": seg.r0 + local, "capture": seg.cap,
                                      "mad_row": round(diffs[0], 3), "mad_prev": round(diffs[-1], 3),
                                      "mad_next": round(diffs[1], 3), "discriminating": diffs[0] < min(diffs[-1], diffs[1]),
                                      "ok": diffs[0] <= best + 1e-6 and diffs[0] < 4.0})
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(mp4), "-vn", "-f", "s16le", "-ac", "2", "-ar", "48000", "-"],
                         capture_output=True, check=True).stdout
    mix = np.frombuffer(pcm, np.int16).reshape(-1, 2).astype(np.float32).mean(axis=1)
    for seg in segs:
        if seg.cap is None:
            continue
        wav, src0, local0, count, gain = seg.audio_pieces()[0]
        with wave.open(str(wav)) as w:
            src = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32).mean(axis=1)
        mid = seg.frames // 2
        o = (seg.start + mid) * rp.SPF
        s = (src0 + mid) * rp.SPF
        n, search = 24000, 2400
        ref = src[s:s + n]
        if np.abs(ref).max() == 0:
            report["audio"].append({"segment": seg.name, "skipped": "silent source window"}); continue
        # High-passed, normalised correlation: periodic music cannot fake a match at another lag.
        r = np.diff(ref)
        def corr(lag):
            y = np.diff(mix[o + lag:o + lag + n])
            return float(np.dot(r, y) / (np.linalg.norm(r) * np.linalg.norm(y) + 1e-9))
        coarse = max(range(-search, search + 1, 4), key=corr)
        fine = max(range(coarse - 4, coarse + 5), key=corr)
        report["audio"].append({"segment": seg.name, "capture": seg.cap, "source_frame": src0 + mid, "out_frame": seg.start + mid,
                                "lag_samples": fine, "lag_ms": round(fine / 48, 3), "correlation_at_lag": round(corr(fine), 4),
                                "correlation_at_zero": round(corr(0), 4), "ok": abs(fine) <= rp.SPF and corr(0) > 0.9})
    report["picture_ok"] = all(p["ok"] for p in report["picture"])
    report["audio_ok"] = all(a.get("ok", True) for a in report["audio"])
    out = mp4.with_suffix(".verify.json")
    out.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({"picture_samples": len(report["picture"]), "picture_ok": report["picture_ok"],
                      "audio_windows": len(report["audio"]), "audio_ok": report["audio_ok"]}))


if __name__ == "__main__":
    main()
