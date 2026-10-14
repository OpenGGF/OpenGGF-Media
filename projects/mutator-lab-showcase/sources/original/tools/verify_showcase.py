#!/usr/bin/env python3
"""verify_showcase.py — whole-film verification for task mutator-complete-showcase-20261010.
1. Full -xerror decode; ffprobe stream facts (CFR 60/1, frame count, AAC 48 kHz stereo, chapters).
2. Video cadence: for every segment and panel, three output frames are cropped, nearest-downscaled to native
   320x224 and matched against source frames j-2..j+2 (mean abs RGB). A correct edit matches offset 0.
3. Native PCM: the pre-loudnorm edit track work/edit/audio.wav must equal, sample for sample, each segment's
   source audio.wav range [a*800,b*800) outside the 10 ms (480-sample) boundary fades.
4. A/V: cross-correlate the final AAC against the pre-loudnorm track at 12 windows (lag in ms).
Writes out/verify.json."""
import json, subprocess, struct, wave
from pathlib import Path
T = Path(__file__).resolve().parents[1]
FILM = T / "out/mutator-lab-complete-showcase.mp4"
ch = json.load(open(T / "out/chapters.json"))
R = {}
d = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(FILM), "-f", "null", "-"], capture_output=True, text=True)
R["decode"] = {"exit": d.returncode, "stderr": d.stderr[-500:]}
p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_chapters", "-show_format",
                               "-of", "json", str(FILM)], capture_output=True, text=True, check=True).stdout)
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]; a = [s for s in p["streams"] if s["codec_type"] == "audio"][0]
R["probe"] = {"video": {k: v.get(k) for k in ("codec_name", "profile", "width", "height", "pix_fmt", "r_frame_rate", "avg_frame_rate", "nb_read_frames", "duration")},
              "audio": {k: a.get(k) for k in ("codec_name", "sample_rate", "channels", "channel_layout", "duration")},
              "chapters": [c["tags"]["title"] for c in p["chapters"]], "format_duration": p["format"]["duration"],
              "size": p["format"]["size"], "expected_frames": ch["frames"]}
# PTS cadence: every frame delta exactly 1/60.
pts = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pts", "-of", "csv=p=0", str(FILM)],
                     capture_output=True, text=True, check=True).stdout.replace(",", " ").split()
deltas = {int(pts[i + 1]) - int(pts[i]) for i in range(len(pts) - 1)}
R["pts"] = {"frames": len(pts), "distinct_deltas": sorted(deltas), "time_base": v.get("time_base")}

def raw(args, w, h):
    return subprocess.run(["ffmpeg", "-v", "error"] + args + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout[: w * h * 3]
def mad(x, y):
    return sum(abs(p - q) for p, q in zip(x[::5], y[::5])) / (len(x) / 5)
checks, idx = [], 0
for s in ch["segments"]:
    n = s["frames"]
    if s["id"] not in ("title", "outro"):
        for j in (n // 4, n // 2, (3 * n) // 4):
            for src in s["sources"]:
                x, y, w, h = src["crop"]; f = w // 320
                fc = raw(["-i", str(FILM), "-vf", f"select=eq(n\\,{idx + j}),crop={w}:{h}:{x}:{y},scale=320:224:flags=neighbor", "-frames:v", "1"], 320, 224)
                base = src["frames"][0] + j
                sc = {}
                for dd in (-2, -1, 0, 1, 2):
                    fp = Path(src["take"]) / "capture/frames" / f"{base + dd:05d}.png"
                    if fp.exists(): sc[dd] = round(mad(fc, raw(["-i", str(fp)], 320, 224)), 2)
                best = min(sc, key=sc.get)
                checks.append({"segment": s["id"], "out": idx + j, "take": Path(src["take"]).name, "src": base, "best": best, "mad": sc})
    idx += n
bad = [c for c in checks if c["best"] != 0 and c["mad"][c["best"]] < c["mad"][0] - 0.5]
R["video"] = {"checks": len(checks), "mismatches": bad, "max_mad_at_0": max(c["mad"][0] for c in checks), "detail": checks}
# Native PCM exactness.
def wav(path):
    w = wave.open(str(path)); assert w.getframerate() == 48000 and w.getnchannels() == 2 and w.getsampwidth() == 2
    return w.readframes(w.getnframes())
ed = wav(T / "work/edit/audio.wav"); cache = {}
pos, pcm_bad, total_cmp = 0, [], 0
for s in ch["segments"]:
    src = [x for x in s["sources"] if x["audio"]][0]
    if src["take"] not in cache: cache[src["take"]] = wav(Path(src["take"]) / "capture/audio.wav")
    a0, a1 = src["audio_samples"]; n = a1 - a0
    seg_src = cache[src["take"]][a0 * 4:a1 * 4]; seg_ed = ed[pos * 4:(pos + n) * 4]
    inner_s, inner_e = 481 * 4, (n - 481) * 4  # afade boundary sample itself is already attenuated
    ok = len(seg_src) == n * 4 and seg_ed[inner_s:inner_e] == seg_src[inner_s:inner_e]
    total_cmp += max(0, n - 962)
    if not ok: pcm_bad.append(s["id"])
    pos += n
R["pcm"] = {"edit_track_frames": len(ed) // 4, "expected": ch["frames"] * 800, "segments_mismatched": pcm_bad, "samples_compared": total_cmp}
def mono(path):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return struct.unpack(f"<{len(b)//2}h", b)
fin, ref = mono(FILM), mono(T / "work/edit/audio.wav")
dur = ch["duration_s"]; out = []
for k in range(12):
    t = 2 + k * (dur - 6) / 11; s0, n = int(t * 8000), 4000
    r = ref[s0:s0 + n]; rn = sum(q * q for q in r) ** 0.5 or 1; best = None
    for lag in range(-240, 241, 2):
        f = fin[s0 + lag:s0 + lag + n]
        if len(f) < n: continue
        c = sum(p1 * q for p1, q in zip(r, f)) / (rn * (sum(q * q for q in f) ** 0.5 or 1))
        if best is None or c > best[1]: best = (lag, c)
    out.append({"t": round(t, 2), "lag_ms": best[0] / 8.0, "corr": round(best[1], 3)})
R["av"] = out
json.dump(R, open(T / "out/verify.json", "w"), indent=1)
print(json.dumps({k: R[k] for k in ("decode", "probe", "pts", "pcm")}, indent=1))
print("video checks", len(checks), "mismatches", len(bad), "max mad@0", R["video"]["max_mad_at_0"])
for b in bad: print(" ", b)
print("av", [(o["t"], o["lag_ms"], o["corr"]) for o in out])
