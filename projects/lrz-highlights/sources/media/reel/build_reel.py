#!/usr/bin/env python3
"""Build an OpenGGF highlights reel with the animated title cards used by DDZ/HPZ."""

from __future__ import annotations

import csv
import json
import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent
WORK = ROOT / "work"
OUT = ROOT / f"{SRC.name}-highlights.mp4"
W, H, FPS = 1920, 1080, 60
CARD_FRAMES = 132

HEAVY = "/usr/share/fonts/TTF/FiraSansCompressed-Heavy.ttf"
XBOLD = "/usr/share/fonts/TTF/FiraSansCompressed-ExtraBold.ttf"
BODY = "/usr/share/fonts/TTF/FiraSans-Medium.ttf"
BOLD = "/usr/share/fonts/TTF/FiraSans-Bold.ttf"

THEMES = {
    "space": ((70, 120, 255), (255, 214, 64), (8, 14, 60)),
    "sky": ((70, 210, 255), (255, 255, 255), (8, 34, 72)),
    "gravity": ((190, 88, 255), (88, 240, 255), (30, 12, 70)),
    "boss": ((60, 110, 230), (255, 255, 255), (10, 22, 60)),
    "chase": ((235, 48, 60), (70, 230, 150), (70, 10, 18)),
    "lava": ((245, 72, 32), (255, 214, 64), (72, 12, 8)),
    "finale": ((255, 214, 64), (70, 120, 255), (40, 24, 8)),
}


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def probe(path: Path) -> dict:
    result = run(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration", "-of", "json", str(path), capture=True
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "rate": stream["r_frame_rate"],
        "duration": float(data["format"]["duration"]),
    }


def font(path: str, size: int):
    return ImageFont.truetype(path, size)


def ease_out_back(t: float) -> float:
    c1, c3 = 1.70158, 2.70158
    t = max(0.0, min(1.0, t))
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_in(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * t


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def metadata_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("=", r"\=").replace(";", r"\;").replace("#", r"\#").replace("\n", r"\n")


def wrap(draw, text: str, fnt, width: int):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] > width and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def load_entries():
    with (ROOT / "title_cards.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    entries = []
    for row in rows:
        row["tags"] = [tag for tag in row["tags"].split("|") if tag]
        entries.append(row)
    return entries


def draw_card(entry: dict, number: int, output: Path) -> None:
    primary, accent, deep = THEMES[entry["theme"]]
    output.mkdir(parents=True, exist_ok=True)
    f_chapter = font(XBOLD, 40)
    f_title = font(HEAVY, 150 if len(entry["title"]) < 22 else 116)
    f_sub = font(BODY, 38)
    f_tag = font(BOLD, 34)
    for frame in range(CARD_FRAMES):
        exit_t = ease_in((frame - (CARD_FRAMES - 16)) / 16)
        image = Image.new("RGB", (W, H), (13, 11, 26))
        draw = ImageDraw.Draw(image, "RGBA")
        for y in range(0, H, 6):
            draw.rectangle([0, y, W, y + 6], fill=lerp(deep, (13, 11, 26), y / H))
        for colour, delay, thickness in ((primary, 0, 210), (accent, 5, 90), ((255, 255, 255), 9, 34)):
            position = ease_out_back((frame - delay) / 26)
            offset = int((1 - position) * -1400 - exit_t * 2600)
            top = 150 + delay * 14
            polygon = [(offset - 300, top), (offset + 1500, top),
                       (offset + 1410, top + thickness), (offset - 390, top + thickness)]
            draw.polygon(polygon, fill=colour + (235,))
        for index in range(26):
            sx = (index * 173 + frame * (3 + index % 4)) % W
            sy = 480 + (index * 97) % 560
            radius = 2 + index % 3
            alpha = int(120 + 120 * math.sin(frame / 7 + index))
            draw.ellipse([sx - radius, sy - radius, sx + radius, sy + radius], fill=accent + (max(0, alpha),))

        chapter_alpha = int(255 * max(0, min(1, (frame - 6) / 14)) * (1 - exit_t))
        draw.text((150, 88), entry["chapter"], font=f_chapter, fill=(255, 255, 255, chapter_alpha))
        title_position = ease_out_back((frame - 10) / 30)
        tx = int(150 + (1 - title_position) * 1500 + exit_t * 2200)
        ty = 420
        draw.text((tx + 8, ty + 8), entry["title"], font=f_title, fill=(0, 0, 0, 170))
        draw.text((tx, ty), entry["title"], font=f_title, fill=(255, 255, 255))
        bbox = draw.textbbox((tx, ty), entry["title"], font=f_title)
        underline = max(0, min(1, (frame - 26) / 20))
        draw.rectangle([150, bbox[3] + 22, 150 + int((bbox[2] - 150) * underline), bbox[3] + 34], fill=accent)

        chars = int(len(entry["sub"]) * max(0, min(1, (frame - 34) / 40)))
        for line_number, line in enumerate(wrap(draw, entry["sub"][:chars], f_sub, W - 300)):
            draw.text((152, bbox[3] + 70 + line_number * 52), line, font=f_sub,
                      fill=(230, 230, 245, int(255 * (1 - exit_t))))

        x = 150
        y = 900
        for tag_index, tag in enumerate(entry["tags"]):
            pop = ease_out_back((frame - 50 - tag_index * 8) / 16)
            if pop <= 0:
                continue
            tag_width = draw.textbbox((0, 0), tag, font=f_tag)[2]
            chip_width = int((tag_width + 56) * pop)
            draw.rounded_rectangle([x, y, x + chip_width, y + 64], radius=32, fill=accent + (235,))
            if pop > 0.7:
                draw.text((x + 28, y + 13), tag, font=f_tag, fill=(10, 10, 20))
            x += tag_width + 78
        draw.text((W - 230, H - 90), f"{number:02d}", font=font(HEAVY, 70), fill=(255, 255, 255, 60))
        image.save(output / f"{frame:04d}.png")


def draw_overlay(entry: dict, layout: tuple[int, int, int, int], output: Path) -> None:
    primary, accent, _ = THEMES[entry["theme"]]
    ox, oy, dw, dh = layout
    image = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, H - 96, W, H], fill=(8, 7, 18, 235))
    draw.rectangle([0, H - 96, 14, H], fill=primary + (255,))
    draw.text((46, H - 76), entry["caption"], font=font(BOLD, 40), fill=(255, 255, 255, 255))
    draw.text((W - 520, H - 70), f"OpenGGF · {SRC.name.upper()}", font=font(BODY, 30), fill=(200, 200, 220, 200))
    text = "NEW"
    tw = draw.textbbox((0, 0), text, font=font(BOLD, 36))[2]
    cx = ox + dw // 2
    y = max(12, oy - 70) if oy > 80 else oy + 16
    draw.rounded_rectangle([cx - tw // 2 - 28, y, cx + tw // 2 + 28, y + 60], radius=30, fill=accent + (240,))
    draw.text((cx - tw // 2, y + 10), text, font=font(BOLD, 36), fill=(10, 10, 20))
    image.save(output)


def encode_card(frames: Path, output: Path) -> None:
    run("ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-video_track_timescale", "60000", str(output))


def encode_clip(entry: dict, output: Path, overlay: Path) -> float:
    source = SRC / entry["source"]
    info = probe(source)
    start = float(entry["source_start_seconds"])
    end = float(entry["source_end_seconds"])
    if start < 0 or end <= start or end > info["duration"] + 0.08:
        raise SystemExit(f"invalid interval for {source}: {start}..{end} / {info['duration']:.6f}")
    if abs(start) > 0.001 or abs(end - info["duration"]) > 0.08:
        raise SystemExit(f"edit interval is not the complete retained clip: {source}")
    if (info["width"], info["height"], info["rate"]) != (960, 672, "60/1"):
        raise SystemExit(f"unexpected source format for {source}: {info}")
    max_width, max_height = W - 40, H - 96 - 110
    scale = min(max_width / info["width"], max_height / info["height"])
    width = int(info["width"] * scale) // 2 * 2
    height = int(info["height"] * scale) // 2 * 2
    left = (W - width) // 2
    top = 90 + (max_height - height) // 2
    draw_overlay(entry, (left, top, width, height), overlay)
    graph = (f"[0:v]scale={width}:{height}:flags=neighbor,pad={W}:{H}:{left}:{top}:color=0x0d0b1a[v];"
             "[v][1:v]overlay=0:0,format=yuv420p[out]")
    run("ffmpeg", "-loglevel", "error", "-y", "-i", str(source), "-loop", "1", "-i", str(overlay),
        "-filter_complex", graph, "-map", "[out]", "-t", f"{end - start:.6f}", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-r", str(FPS), "-video_track_timescale", "60000", "-an", str(output))
    return end - start


def main() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    entries = load_entries()
    segments = []
    edit_rows = []
    chapters = []
    chapter_start = 0.0
    elapsed = 0.0
    card_number = 0

    for index, entry in enumerate(entries):
        if entry["kind"] in {"intro", "card", "clip", "outro"}:
            card_number += 1
            card_path = WORK / f"card{index:03d}"
            draw_card(entry, card_number, card_path)
            card_segment = WORK / f"seg{index:03d}-card.mp4"
            encode_card(card_path, card_segment)
            shutil.rmtree(card_path)
            card_duration = probe(card_segment)["duration"]
            if chapters:
                chapters[-1]["end"] = elapsed
            chapters.append({"title": entry["title"], "start": elapsed, "end": None})
            segments.append((card_segment, True))
            edit_rows.append([entry["chapter"], index, entry["title"], "(title card)", "", ""])
            elapsed += card_duration
        if entry["kind"] == "clip":
            clip_segment = WORK / f"seg{index:03d}-clip.mp4"
            duration = encode_clip(entry, clip_segment, WORK / f"overlay{index:03d}.png")
            segments.append((clip_segment, False))
            edit_rows.append([entry["chapter"], index, entry["caption"], entry["source"], entry["source_start_seconds"], f"{duration:.6f}"])
            elapsed += duration

    if chapters:
        chapters[-1]["end"] = elapsed
    manifest = ROOT / "assembly_concat.txt"
    manifest.write_text("".join(f"file '{path.relative_to(ROOT).as_posix()}'\n" for path, _ in segments), encoding="utf-8")
    metadata = [";FFMETADATA1"]
    for chapter in chapters:
        metadata += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(chapter['start'] * 1000)}",
                     f"END={round(chapter['end'] * 1000)}", f"title={metadata_escape(chapter['title'])}"]
    metadata_path = ROOT / "chapters.ffmeta"
    metadata_path.write_text("\n".join(metadata) + "\n", encoding="utf-8")
    temporary = ROOT / f".{OUT.name}.new.mp4"
    run("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(manifest),
        "-i", str(metadata_path), "-map", "0:v:0", "-map_metadata", "1", "-map_chapters", "1",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-movflags", "+faststart", "-an", str(temporary))
    final = probe(temporary)
    if (final["width"], final["height"], final["rate"]) != (W, H, "60/1"):
        raise SystemExit(f"unexpected final format: {final}")
    run("ffmpeg", "-v", "error", "-xerror", "-i", str(temporary), "-f", "null", "-")
    temporary.replace(OUT)
    with (ROOT / "edit_list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["chapter", "order", "title", "source", "source_start_seconds", "source_end_seconds"])
        writer.writerows(edit_rows)
    with (ROOT / "chapters.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["title", "output_start_seconds", "output_end_seconds"])
        for chapter in chapters:
            writer.writerow([chapter["title"], f"{chapter['start']:.3f}", f"{chapter['end']:.3f}"])
    print(f"built {OUT} ({final['duration']:.3f}s, {len(chapters)} title-card chapters)")


if __name__ == "__main__":
    main()
