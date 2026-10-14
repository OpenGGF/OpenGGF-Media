#!/usr/bin/env python3
"""Check that gameplay in a rendered promo is unaltered real footage at normal speed.

For sampled clean (non-transition) frames of every gameplay range, the output window
is sampled at the centre of each integer-scaled pixel block and compared with the
source frame the edit list says should be there, and with its neighbours (+-1, +-2).
Passes when the expected frame is the best match (ties allowed only where the
neighbouring source frames are identical, marked OK*) and its mean absolute error is
small (only H.264/yuv420 loss). Proves integer nearest scaling, placement and that
output frame n+1 shows source frame k+1 (normal speed, no holds/skips).

Paced-cut copy: additionally checks the real title-menu clips (title.mkv) in the title and
online segments; title-menu frames are mostly static, so ties there are reported as OK*.

Intro-audio copy: also checks the cold-open intro segment (after its fade from black).

Usage: verify_fidelity.py <promo.mp4> <promo.edl.json>   (originating task: 2026-10-06 promo)
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

NW, NH = 320, 224
mp4, edl = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
W, H = edl["canvas"]

checks = []  # (out_frame, src_dir, mkv_frame, scale, (x, y))
for s in edl["segments"]:
    a, b = s["out_frames"]
    T = (s["transition_in"] or {}).get("frames", 0)
    clean = [a + T + 2, (a + T + b) // 2, b - 14]
    places = []
    if s["kind"] == "game":
        places.append((s["source"], 4, (320, 64)))
    elif s["kind"] == "intro":   # intro-audio cut: cold open (first clean frame after the fade from black)
        clean = [a + s.get("fade_in_frames", 0) + 2, (a + b) // 2, b - 14]
        places.append((s["source"], 4, (320, 64)))
    elif s["kind"] == "split":
        places.append((s["source_left"], 3, (0, 72)))
        places.append((s["source_right"], 3, (960, 64 + 896 - 672)))
    elif s["kind"] == "engine":
        places.append((s["source_mini"], 2, (1180, 250)))
    if s["kind"] in ("title", "online"):   # paced cut: also check the real title-menu clips
        src = s["source"]
        lead = src.get("lead_graphic_frames", 0)
        sc, xy = (4, (320, 64)) if s["kind"] == "title" else (3, (90, 170))
        fa = a + max(T, lead + 10)
        for f in (fa + 2, (fa + b) // 2, b - 14):
            checks.append((f, src["dir"], src["frames"][0] + (f - a - lead), sc, xy, s["id"], "title.mkv"))
    for src, sc, xy in places:
        for f in clean:
            checks.append((f, src["dir"], src["mkv_frames"][0] + (f - a), sc, xy, s["id"], "gameplay.mkv"))


def grab_out(frames):
    expr = "+".join(f"eq(n\\,{f})" for f in sorted(set(frames)))
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"select={expr}", "-fps_mode", "passthrough",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], check=True, capture_output=True).stdout
    n = W * H * 3
    return {f: Image.frombytes("RGB", (W, H), data[i * n:(i + 1) * n]) for i, f in enumerate(sorted(set(frames)))}


def grab_src(d, k, name="gameplay.mkv"):
    if k < 0:
        return None
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", str(Path(d) / name), "-vf",
                           f"select=eq(n\\,{k})", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          check=True, capture_output=True).stdout
    return Image.frombytes("RGB", (NW, NH), data[:NW * NH * 3]) if data else None


def mad(a, b):
    pa, pb = a.tobytes(), b.tobytes()
    return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)


outs = grab_out([c[0] for c in checks])
results, ok = [], True
for f, d, k, sc, (x, y), sid, name in checks:
    crop = outs[f].crop((x, y, x + NW * sc, y + NH * sc))
    px_ = crop.load()
    sampled = Image.frombytes("RGB", (NW, NH), b"".join(bytes(px_[px * sc + sc // 2, py * sc + sc // 2])
                                                        for py in range(NH) for px in range(NW)))
    scores = {}
    for dk in (-2, -1, 0, 1, 2):
        s = grab_src(d, k + dk, name)
        if s is not None:
            scores[dk] = mad(sampled, s)
    others = min(v for a, v in scores.items() if a)
    static = abs(others - scores[0]) < 1e-6   # neighbouring source frames identical (scene at rest)
    good = scores[0] <= others + 1e-6 and scores[0] < 6.0
    ok &= good
    results.append({"segment": sid, "out_frame": f, "src": Path(d).name, "file": name, "mkv_frame": k, "scale": sc,
                    "mad_expected": round(scores[0], 3), "mad_neighbours": {str(a): round(b, 3) for a, b in scores.items() if a},
                    "static_tie": static, "ok": good})
    print(f"{('OK*' if static else 'OK ') if good else 'BAD'} {sid:12s} out {f:4d} -> {Path(d).name} mkv {k:4d} x{sc}  mad {scores[0]:.2f}  next-best {min(v for a, v in scores.items() if a):.2f}")
Path(mp4.with_suffix(".fidelity.json")).write_text(json.dumps({"ok": ok, "checks": results}, indent=2) + "\n")
print("fidelity:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
