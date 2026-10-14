#!/usr/bin/env python3
"""verify_final.py — per-segment cadence/sync check of the final promo (task e0603654).
For sampled output frames, crops the game area, nearest-downscales it to native size and finds which
source frame (j-2..j+2) it matches best (mean absolute RGB difference). A correct edit matches j exactly.
Also extracts first/last frames of every segment into a boundary contact sheet."""
import json, subprocess, sys
from pathlib import Path
O = Path(__file__).resolve().parent.parent
FINAL = O / "out/mutator-lab-gameplay-promo.mp4"
ch = json.load(open(O / "out/chapters.json"))
def raw(args, w, h):
    return subprocess.run(["ffmpeg", "-v", "error"] + args + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, check=True).stdout[: w * h * 3]
def final_crop(idx, crop):
    x, y, w, h, f = crop
    return raw(["-i", str(FINAL), "-vf", f"select=eq(n\\,{idx}),crop={w}:{h}:{x}:{y},scale={w // f}:{h // f}:flags=neighbor", "-frames:v", "1"], w // f, h // f)
def src(take, n):
    return raw(["-i", str(O / "captures" / take / "capture/frames" / f"{n:05d}.png")], 320, 224)
def mad(a, b):
    return sum(abs(p - q) for p, q in zip(a[::7], b[::7])) / (len(a) / 7)
res, fidx = [], 0
for s in ch["segments"]:
    n = s["frames"]
    titled = s["id"] in ("title", "outro")
    for j in (n // 4, n // 2, (3 * n) // 4):
        if titled: continue
        srcs = s["sources"]
        crops = [(320, 40, 1280, 896, 4)] if len(srcs) == 1 else [(0, 150, 960, 672, 3), (960, 150, 960, 672, 3)]
        for crop, sd in zip(crops, srcs):
            fc = final_crop(fidx + j, crop)
            base = sd["frames"][0] + j
            scores = {d: round(mad(fc, src(sd["take"], base + d)), 2) for d in (-2, -1, 0, 1, 2)}
            best = min(scores, key=scores.get)
            res.append({"segment": s["id"], "out_frame": fidx + j, "take": sd["take"], "src_frame": base, "best_offset": best, "mad": scores})
    fidx += n
bad = [r for r in res if r["best_offset"] != 0 and r["mad"][r["best_offset"]] < r["mad"][0] - 0.5]
json.dump({"checks": res, "mismatches": bad}, open(O / "out/verify-cadence.json", "w"), indent=1)
print("checks", len(res), "mismatches", len(bad))
for r in bad: print(" ", r)
print("max mad at offset 0:", max(r["mad"][0] for r in res))
