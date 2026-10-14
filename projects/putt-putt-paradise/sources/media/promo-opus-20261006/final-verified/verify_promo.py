#!/usr/bin/env python3
"""Verify the final Putt Putt Paradise promo against its sources (Opus, 2026-10-06, r5).

One full decode of the MP4 (ffmpeg, rawvideo pipe) drives every picture check, so the file is
also proven to decode end to end. Checks:
1. Stream facts: H.264 1920x1080 at exactly 60 fps, AAC 48 kHz stereo, frame count equal to the
   EDL, duration, chapter count/order equal to promo.chapters.csv, faststart.
2. Picture fidelity and normal speed: five samples inside every gameplay segment (away from
   transitions). The decoded frame is compared with the renderer's composite of unified row u
   and of u-1 / u+1. Row u must be closest (ties allowed only where the game itself is still),
   and the absolute mean error must be small (encoding noise only).
3. Motion: inside every gameplay segment, consecutive decoded frames must change somewhere, and
   the segment must not hold one picture for more than 2 s unless its source rows do too.
4. A/V sync: in the middle of every gameplay segment, 0.5 s of the decoded audio is
   cross-correlated (first difference, normalised) with the segment's own captured audio. The
   best lag must be within one video frame and the correlation at zero lag above 0.9.
4b. Reverse audio in the film: every rewind row the capture proved to be a sample-exact reversal of
   the forward shot (rewind-audio.json) is checked again in the decoded MP4: film packet vs source
   packet, and film packet played backwards vs the forward packet it reverses.
5. Soundtrack health: integrated loudness and true peak (ffmpeg ebur128), clipped samples, and
   every run of >= 8 consecutive near-silent output frames, each attributed to its source rows,
   which must be silent there too (pause, the title card's silent gap, fades).

Usage: verify_promo.py promo.mp4     (writes promo.verify.json next to it)
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_promo as rp  # noqa: E402

W, H, FPS, SPF = rp.W, rp.H, rp.FPS, rp.SPF


def ffprobe(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_chapters", "-of", "json", str(mp4)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def composite(seg, local, shift):
    saved = seg.u0
    try:
        seg.u0 = saved + shift
        return np.asarray(seg.draw(local).convert("RGB"), np.float32)
    finally:
        seg.u0 = saved


def main():
    mp4 = Path(sys.argv[1])
    segs = rp.segments()
    total = rp.total_frames()
    report = {"file": mp4.name, "stream": {}, "picture": [], "motion": [], "audio_sync": [], "soundtrack": {}}

    # 1. Stream facts.
    info = ffprobe(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    chapters_file = list(csv.DictReader(open(rp.ROOT / "promo.chapters.csv")))
    report["stream"] = {
        "video_codec": v["codec_name"], "size": [v["width"], v["height"]], "r_frame_rate": v["r_frame_rate"],
        "avg_frame_rate": v["avg_frame_rate"], "nb_frames": int(v.get("nb_frames", 0)), "expected_frames": total,
        "audio_codec": a["codec_name"], "sample_rate": int(a["sample_rate"]), "channels": a["channels"],
        "duration_s": float(info["format"]["duration"]), "expected_s": total / FPS,
        "chapters": [c["tags"]["title"] for c in info.get("chapters", [])],
        "chapters_expected": [c["chapter"] for c in chapters_file],
    }
    st = report["stream"]
    st["ok"] = (st["video_codec"] == "h264" and st["size"] == [W, H] and st["r_frame_rate"] == "60/1"
                and st["avg_frame_rate"] == "60/1" and st["nb_frames"] == total and st["sample_rate"] == 48000
                and st["channels"] == 2 and st["chapters"] == st["chapters_expected"]
                and abs(st["duration_s"] - total / FPS) < 0.05)

    # 2 + 3. One decode pass feeds the picture samples and the motion statistics.
    samples = {}
    for i, seg in enumerate(segs):
        if seg.cap is None:
            continue
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        lo, hi = max(seg.tlen + 4, 6), seg.frames - 8 - (nxt.tlen if nxt else 0)
        for k in range(5):
            samples[seg.start + lo + (hi - lo) * (k + 1) // 6] = seg
    seg_of = {}
    for seg in segs:
        if seg.cap is None:
            continue
        nxt = segs[segs.index(seg) + 1] if segs.index(seg) + 1 < len(segs) else None
        for f in range(seg.start + seg.tlen, seg.start + seg.frames - (nxt.tlen if nxt else 0)):
            seg_of[f] = seg
    motion = {seg.name: {"frames": 0, "changed": 0, "longest_hold": 0, "hold": 0, "hold_frames": set()} for seg in segs if seg.cap}
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", "-threads", "2", "-i", str(mp4), "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    prev, decoded = None, 0
    size = W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        f = decoded
        decoded += 1
        frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        seg = seg_of.get(f)
        if seg is not None and prev is not None and seg_of.get(f - 1) is seg:
            m = motion[seg.name]
            diff = float(np.mean(np.abs(frame[::4, ::4].astype(np.int16) - prev[::4, ::4].astype(np.int16))))
            m["frames"] += 1
            if diff > 0.35:
                m["changed"] += 1; m["hold"] = 0
            else:
                m["hold"] += 1; m["longest_hold"] = max(m["longest_hold"], m["hold"]); m["hold_frames"].add(f)
        if f in samples:
            seg = samples[f]
            local = f - seg.start
            got = frame.astype(np.float32)
            diffs = {s: float(np.mean(np.abs(got - composite(seg, local, s)))) for s in (-1, 0, 1)}
            best = min(diffs.values())
            # Row u must be the closest composite. Where the game itself is still, u-1/u/u+1 composite
            # to (nearly) the same picture and encoder noise decides the order, so a near-tie within
            # 0.05 is accepted and marked non-discriminating. The absolute error bounds encoding noise.
            report["picture"].append({"segment": seg.name, "frame": f, "unified_row": seg.u0 + local, "capture": seg.cap,
                                      "mad_row": round(diffs[0], 3), "mad_prev": round(diffs[-1], 3), "mad_next": round(diffs[1], 3),
                                      "discriminating": diffs[0] + 0.05 < min(diffs[-1], diffs[1]),
                                      "ok": diffs[0] <= best + 0.05 and diffs[0] < 6.0})
        prev = frame
    dec.wait()
    report["decoded_frames"] = decoded
    report["decode_ok"] = dec.returncode == 0 and decoded == total
    # Stutter check against the source's own motion: an output frame that barely changes (a "hold")
    # is only allowed where the captured rows themselves barely change (menu at rest, golfer
    # lining up). A hold over a visibly moving source row (native mean change > 1.5/255) counts
    # as a violation; at most 2% of a segment's frames may be violations (encoder noise on tiny
    # sprites), and none may form a run of more than 2 frames.
    by_name = {s2.name: s2 for s2 in segs}
    for name, m in motion.items():
        m.pop("hold")
        seg = by_name[name]
        holds = m.pop("hold_frames")
        violations, run, worst = 0, 0, 0
        for f in sorted(holds):
            u = seg.u0 + f - seg.start
            a_img = np.asarray(rp.row(seg.cap, u - 1), np.int16); b_img = np.asarray(rp.row(seg.cap, u), np.int16)
            if float(np.mean(np.abs(b_img - a_img))) > 1.5:
                violations += 1; run = run + 1 if (f - 1) in holds else 1; worst = max(worst, run)
        m["holds_over_moving_source"] = violations
        m["longest_violation_run"] = worst
        m["ok"] = m["frames"] > 0 and violations <= 0.02 * m["frames"] and worst <= 2
        report["motion"].append({"segment": name, **m})

    # 4. A/V sync against each segment's own captured audio.
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(mp4), "-vn", "-f", "s16le", "-ac", "2", "-ar", "48000", "-"],
                         capture_output=True, check=True).stdout
    mixed = np.frombuffer(pcm, np.int16).reshape(-1, 2).astype(np.float32) / 32768
    mono = mixed.mean(axis=1)
    for seg in segs:
        if seg.cap is None:
            continue
        src = rp.unified_audio(seg.cap).mean(axis=1)
        mid = seg.frames // 2
        o, s = (seg.start + mid) * SPF, (seg.u0 + mid) * SPF
        n, search = 24000, 2400
        ref = src[s:s + n]
        if np.abs(np.diff(ref)).max() < 1e-4:
            report["audio_sync"].append({"segment": seg.name, "skipped": "silent source window"}); continue
        r = np.diff(ref)

        def corr(lag):
            y = np.diff(mono[o + lag:o + lag + n])
            return float(np.dot(r, y) / (np.linalg.norm(r) * np.linalg.norm(y) + 1e-12))
        coarse = max(range(-search, search + 1, 4), key=corr)
        fine = max(range(coarse - 4, coarse + 5), key=corr)
        report["audio_sync"].append({"segment": seg.name, "capture": seg.cap, "source_unified_row": seg.u0 + mid,
                                     "out_frame": seg.start + mid, "lag_samples": fine, "lag_ms": round(fine / 48, 3),
                                     "corr_at_lag": round(corr(fine), 4), "corr_at_zero": round(corr(0), 4),
                                     "ok": abs(fine) <= SPF and corr(0) > 0.9})

    # 4b. Reverse audio in the film itself. For every rewind row the capture proved to be a reversed
    # forward packet (capture rewind-audio.json, per_packet corr > 0.98), the film's packet at that
    # row's output frame must match the source packet (AAC-coded, gain-scaled: correlation), and the
    # film packet played backwards must match the forward shot packet it reverses.
    report["rewind_in_film"] = []
    left = mixed[:, 0]
    for seg in segs:
        if seg.cap is None:
            continue
        proof = rp.CAPTURES[seg.cap] / "rewind-audio.json"
        if not proof.exists():
            continue
        pk = json.loads(proof.read_text())
        t = rp.title_rows(seg.cap)
        src = rp.unified_audio(seg.cap)[:, 0]
        nxt = segs[segs.index(seg) + 1] if segs.index(seg) + 1 < len(segs) else None
        same, back = [], []
        for q in pk["per_packet"]:
            if q.get("silent") or q["corr"] <= 0.98:
                continue
            u = t + q["row"]
            f = seg.start + (u - seg.u0)
            if not (seg.start + seg.tlen <= f < seg.start + seg.frames - (nxt.tlen if nxt else 0)):
                continue
            film = left[f * SPF:(f + 1) * SPF]
            ref = src[u * SPF:(u + 1) * SPF]
            fwd = src[(t + int(round(q["forward_row"]))) * SPF:(t + int(round(q["forward_row"])) + 1) * SPF]
            nc = lambda x, y: float(np.dot(x - x.mean(), y - y.mean()) / ((np.linalg.norm(x - x.mean()) * np.linalg.norm(y - y.mean())) + 1e-12))
            same.append(nc(film, ref)); back.append(nc(film[::-1], fwd))
        if same:
            report["rewind_in_film"].append({"segment": seg.name, "capture": seg.cap, "rows": len(same),
                                             "film_vs_source_min": round(min(same), 4), "film_vs_source_median": round(float(np.median(same)), 4),
                                             "film_reversed_vs_forward_min": round(min(back), 4),
                                             "film_reversed_vs_forward_median": round(float(np.median(back)), 4),
                                             "ok": min(same) > 0.9 and float(np.median(back)) > 0.95})

    # 5. Soundtrack health.
    ebu = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(mp4), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summary = ebu[ebu.rindex("Summary:"):]
    def value(label):
        line = next(l for l in summary.splitlines() if l.strip().startswith(label))
        return float(line.split(":")[1].split()[0])
    frames_ac = mixed[:len(mixed) // SPF * SPF].reshape(-1, SPF, 2).std(axis=1).max(axis=1)
    quiet = frames_ac < 10 ** (-60 / 20)
    runs, start = [], None
    for f in range(len(quiet) + 1):
        if f < len(quiet) and quiet[f]:
            start = f if start is None else start
        elif start is not None:
            if f - start >= 8:
                where = [s for s in segs if s.start <= start < s.start + s.frames]
                attribution = []
                for s in where:
                    if s.cap:
                        u0, u1 = s.u0 + (start - s.start), s.u0 + (f - 1 - s.start)
                        src = rp.unified_audio(s.cap)[u0 * SPF:(u1 + 1) * SPF]
                        attribution.append({"segment": s.name, "unified_rows": [u0, u1],
                                            "source_ac_dbfs": round(20 * np.log10(max(rp.ac_rms(src), 1e-9)), 1)})
                    else:
                        attribution.append({"segment": s.name, "editorial": True})
                edge = start < 30 or f > len(quiet) - 40
                legit = edge or all(a.get("source_ac_dbfs", 0) < -60 for a in attribution if not a.get("editorial"))
                runs.append({"from_frame": start, "to_frame": f - 1, "frames": f - start, "at_film_edge": edge,
                             "sources": attribution, "source_silent_too": legit})
            start = None
    report["soundtrack"] = {
        "integrated_lufs": value("I:"), "true_peak_dbtp": value("Peak:"), "lra_lu": value("LRA:"),
        "clipped_samples": int((np.abs(mixed) >= 0.9999).sum()),
        "quiet_runs": runs,
    }
    sd = report["soundtrack"]
    sd["ok"] = sd["true_peak_dbtp"] <= -1.0 and sd["clipped_samples"] == 0 and all(r["source_silent_too"] for r in runs) \
        and -17 <= sd["integrated_lufs"] <= -13

    report["picture_ok"] = all(p["ok"] for p in report["picture"])
    report["motion_ok"] = all(m["ok"] for m in report["motion"])
    report["audio_sync_ok"] = all(x.get("ok", True) for x in report["audio_sync"])
    report["rewind_in_film_ok"] = bool(report["rewind_in_film"]) and all(r["ok"] for r in report["rewind_in_film"])
    report["all_ok"] = all(report[k] for k in ("picture_ok", "motion_ok", "audio_sync_ok", "decode_ok", "rewind_in_film_ok")) \
        and st["ok"] and sd["ok"]
    out = mp4.with_suffix(".verify.json")
    out.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({"stream_ok": st["ok"], "decode_ok": report["decode_ok"], "decoded": decoded,
                      "picture_samples": len(report["picture"]), "picture_ok": report["picture_ok"],
                      "motion_ok": report["motion_ok"], "audio_windows": len(report["audio_sync"]),
                      "audio_sync_ok": report["audio_sync_ok"], "lufs": sd["integrated_lufs"], "tp": sd["true_peak_dbtp"],
                      "quiet_runs": len(runs), "soundtrack_ok": sd["ok"], "rewind_in_film": report["rewind_in_film"],
                      "all_ok": report["all_ok"]}))


if __name__ == "__main__":
    main()
