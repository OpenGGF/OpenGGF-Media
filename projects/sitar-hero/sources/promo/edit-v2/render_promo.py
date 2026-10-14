#!/usr/bin/env python3
"""Assemble the Sitar Hero promo from ExampleModCapture recordings.

Purpose: cut real-speed scene captures (video + their own ROM audio) into one 1080p promo
with pixel-font captions, dissolves, equal-power audio crossfades, loudness normalisation
and chapters.
Inputs: an edit list JSON (see edit-list.json beside this script's output), the mod's
SitarUi.java for the caption font, and the capture folders it names.
Outputs: <out>.mp4, <out>.chapters.csv, <out>.edl.json (resolved intervals).
Origin: Sitar Hero presentation polish task, 2026-10-08 (feature/ai-sitar-hero-polish).
"""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import pixelfont

W, H = 1920, 1080
GAME_W, GAME_H = 1600, 896          # 400x224 at 4x, nearest neighbour
GAME_X, GAME_Y = (W - GAME_W) // 2, 28
FPS = 60
RATE = 48000
GOLD, CREAM, CYAN = (255, 212, 91, 255), (255, 243, 203, 255), (105, 223, 255, 255)


def run(command):
    subprocess.run(command, check=True)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "default=nw=1:nk=1", str(path)], check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def frame(font, caption, sub, path):
    """The 1080p frame around the game: dark stage gradient, caption band underneath."""
    image = Image.new("RGBA", (W, H), (6, 12, 34, 255))
    draw = ImageDraw.Draw(image)
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(6 + 10 * t), int(12 + 14 * t), int(34 + 30 * t), 255))
    draw.rectangle([GAME_X - 4, GAME_Y - 4, GAME_X + GAME_W + 3, GAME_Y + GAME_H + 3], fill=(54, 94, 149, 255))
    draw.rectangle([GAME_X - 2, GAME_Y - 2, GAME_X + GAME_W + 1, GAME_Y + GAME_H + 1], fill=(8, 19, 45, 255))
    band = GAME_Y + GAME_H + 14
    if caption:
        text = pixelfont.render(font, caption, 6, GOLD)
        image.alpha_composite(text, ((W - text.width) // 2, band))
    if sub:
        text = pixelfont.render(font, sub, 3, CREAM)
        image.alpha_composite(text, ((W - text.width) // 2, band + 64 if caption else band + 20))
    image.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edit_list", type=Path)
    parser.add_argument("--sitar-ui", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    edl = json.loads(args.edit_list.read_text())
    font = pixelfont.load_font(args.sitar_ui)
    args.work.mkdir(parents=True, exist_ok=True)
    base = args.edit_list.parent
    segments = []
    for index, seg in enumerate(edl["segments"]):
        source = (base / seg["source"]).resolve()
        duration = probe_duration(source)
        start, end = seg["start"], seg["end"]
        if not (0 <= start < end <= duration + 1e-6):
            raise SystemExit(f"segment {index} interval {start}-{end} outside {source} ({duration:.3f}s)")
        overlay = args.work / f"frame-{index:02d}.png"
        frame(font, seg.get("caption", ""), seg.get("sub", ""), overlay)
        clip = args.work / f"seg-{index:02d}.mkv"
        audio = source.with_suffix(".wav")
        # Video from the capture's MP4, audio from its lossless WAV of the same ticks.
        run(["ffmpeg", "-y", "-v", "error",
             "-ss", f"{start:.4f}", "-t", f"{end - start:.4f}", "-i", str(source),
             "-ss", f"{start:.4f}", "-t", f"{end - start:.4f}", "-i", str(audio),
             "-loop", "1", "-framerate", str(FPS), "-i", str(overlay),
             "-filter_complex",
             f"[0:v]fps={FPS},scale={GAME_W}:{GAME_H}:flags=neighbor,setsar=1[g];"
             f"[2:v]format=rgba[bg];[bg][g]overlay={GAME_X}:{GAME_Y}:shortest=1,format=yuv420p[v];"
             f"[1:a]aresample={RATE},aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{end - start:.4f}",
             "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-r", str(FPS),
             "-c:a", "pcm_s16le", str(clip)])
        segments.append({**seg, "clip": clip, "length": end - start, "resolved": str(source)})
    # Chain dissolves; each joins with the next segment's own fade length.
    inputs, filters = [], []
    for seg in segments:
        inputs += ["-i", str(seg["clip"])]
    offset = segments[0]["length"]
    v, a = "[0:v]", "[0:a]"
    chapters = [(0.0, segments[0])]
    for i in range(1, len(segments)):
        fade = segments[i].get("fade", 0.5)
        offset -= fade
        chapters.append((offset, segments[i]))
        filters.append(f"{v}[{i}:v]xfade=transition={segments[i].get('transition', 'fade')}:duration={fade}:offset={offset:.4f}[v{i}]")
        filters.append(f"{a}[{i}:a]acrossfade=d={fade}:c1=qsin:c2=qsin[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
        offset += segments[i]["length"]
    total = offset
    filters.append(f"{v}fade=t=in:st=0:d=0.5,fade=t=out:st={total - 0.8:.4f}:d=0.8[vout]")
    filters.append(f"{a}afade=t=in:st=0:d=0.3,afade=t=out:st={total - 0.8:.4f}:d=0.8[aout]")
    graph = ";".join(filters)
    joined = args.work / "joined.mkv"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-c:a", "pcm_s16le", str(joined)])
    # Two-pass EBU R128 loudness, then the delivery encode with chapters.
    measure = subprocess.run(["ffmpeg", "-v", "info", "-i", str(joined), "-af",
                              "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                             check=True, capture_output=True, text=True).stderr
    stats = json.loads(measure[measure.rindex("{"):measure.rindex("}") + 1])
    meta = args.work / "chapters.ffmeta"
    lines = [";FFMETADATA1", "title=Sitar Hero: an OpenGGF example mod",
             "comment=Real engine captures at normal speed with their own ROM audio; autoplay shots are labelled DEMO."]
    rows = ["output_start,output_end,title,source,source_start,source_end"]
    for k, (start, seg) in enumerate(chapters):
        end = chapters[k + 1][0] if k + 1 < len(chapters) else total
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}",
                  f"title={seg['chapter']}"]
        rows.append(f"{start:.3f},{end:.3f},\"{seg['chapter']}\",{seg['source']},{seg['start']},{seg['end']}")
    meta.write_text("\n".join(lines) + "\n")
    loud = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
            f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:"
            f"measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-i", str(meta), "-map_metadata", "1", "-map_chapters", "1",
         "-map", "0:v", "-map", "0:a", "-af", f"{loud},aresample={RATE}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(args.out)])
    args.out.with_suffix(".chapters.csv").write_text("\n".join(rows) + "\n")
    resolved = {"segments": [{k: (str(v) if isinstance(v, Path) else v) for k, v in s.items()} for s in segments],
                "loudness_first_pass": stats, "output_duration_expected": total}
    args.out.with_suffix(".edl.json").write_text(json.dumps(resolved, indent=2) + "\n")
    print(f"wrote {args.out} ({total:.2f}s expected)")


if __name__ == "__main__":
    main()
