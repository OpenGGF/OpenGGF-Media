#!/usr/bin/env python3
"""Build one OpenGGF highlights reel from the edit_list.csv beside this file."""

from __future__ import annotations

import csv
import json
import os
import subprocess
from pathlib import Path


REQUIRED_COLUMNS = {
    "act",
    "route_order",
    "title",
    "source",
    "source_start_seconds",
    "source_end_seconds",
}


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=capture,
    )


def probe(path: Path) -> dict:
    result = run(
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
        capture=True,
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "rate": stream["r_frame_rate"],
        "duration": float(data["format"]["duration"]),
    }


def metadata_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("=", r"\=")
        .replace(";", r"\;")
        .replace("#", r"\#")
        .replace("\n", r"\n")
    )


def main() -> None:
    reel_dir = Path(__file__).resolve().parent
    zone_root = reel_dir.parent
    edit_path = reel_dir / "edit_list.csv"
    output = reel_dir / f"{zone_root.name}-highlights.mp4"
    temporary = reel_dir / f".{output.name}.tmp.mp4"
    concat_path = reel_dir / "assembly_concat.txt"
    metadata_path = reel_dir / "chapters.ffmeta"
    chapters_path = reel_dir / "chapters.csv"

    with edit_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("edit list is empty")
    if not REQUIRED_COLUMNS <= set(rows[0]):
        missing = sorted(REQUIRED_COLUMNS - set(rows[0]))
        raise SystemExit(f"edit list is missing columns: {', '.join(missing)}")

    checked = []
    dimensions = None
    total = 0.0
    for row in rows:
        source = zone_root / row["source"]
        if not source.is_file():
            raise SystemExit(f"missing source: {source}")
        start = float(row["source_start_seconds"])
        end = float(row["source_end_seconds"])
        info = probe(source)
        if start < 0 or end <= start or end > info["duration"] + 0.08:
            raise SystemExit(
                f"invalid interval {row['source']}: {start}..{end} / {info['duration']:.6f}"
            )
        if abs(start) > 0.001 or abs(end - info["duration"]) > 0.08:
            raise SystemExit(
                f"edit interval is not the complete retained clip: {row['source']}"
            )
        current_dimensions = (info["width"], info["height"], info["rate"])
        if dimensions is None:
            dimensions = current_dimensions
        elif current_dimensions != dimensions:
            raise SystemExit(
                f"incompatible source format: {row['source']} has {current_dimensions}, "
                f"expected {dimensions}"
            )
        checked.append((row, source, info, total, total + end - start))
        total += end - start

    with concat_path.open("w", encoding="utf-8") as handle:
        for _, source, _, _, _ in checked:
            escaped = str(source).replace("'", "'\\''")
            handle.write(f"file '{escaped}'\n")

    with metadata_path.open("w", encoding="utf-8") as handle:
        handle.write(";FFMETADATA1\n")
        handle.write(f"title={metadata_escape(zone_root.name + ' highlights')}\n")
        for row, _, _, output_start, output_end in checked:
            handle.write("[CHAPTER]\n")
            handle.write("TIMEBASE=1/1000\n")
            handle.write(f"START={round(output_start * 1000)}\n")
            handle.write(f"END={round(output_end * 1000)}\n")
            handle.write(f"title={metadata_escape(row['title'])}\n")

    run(
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-i",
        str(metadata_path),
        "-map",
        "0:v:0",
        "-map_metadata",
        "1",
        "-vf",
        "fps=60,format=yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-an",
        "-movflags",
        "+faststart",
        str(temporary),
    )
    final_info = probe(temporary)
    if (final_info["width"], final_info["height"], final_info["rate"]) != dimensions:
        raise SystemExit(f"unexpected final format: {final_info}")
    if abs(final_info["duration"] - total) > 0.12:
        raise SystemExit(
            f"final duration {final_info['duration']:.6f} differs from edit list {total:.6f}"
        )
    run("ffmpeg", "-v", "error", "-xerror", "-i", str(temporary), "-f", "null", "-")
    os.replace(temporary, output)

    with chapters_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "act",
                "route_order",
                "title",
                "source",
                "source_start_seconds",
                "source_end_seconds",
                "output_start_seconds",
                "output_end_seconds",
            ],
        )
        writer.writeheader()
        for row, _, _, output_start, output_end in checked:
            writer.writerow(
                {
                    **row,
                    "output_start_seconds": f"{output_start:.6f}",
                    "output_end_seconds": f"{output_end:.6f}",
                }
            )

    print(f"built {output} ({final_info['duration']:.3f}s, {len(rows)} chapters)")


if __name__ == "__main__":
    main()
