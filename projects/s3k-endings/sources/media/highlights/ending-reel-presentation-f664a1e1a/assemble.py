#!/usr/bin/env python3
"""Reproduce the provisional S3K ending reel from indexed engine films.

Inputs: chapters.edl.json and the original videos/CSVs under --root.
Origin: 2026-10-13 S3K playable-completion task, qualified presentation repair f664a1e1a / source 70c09903 plus unaffected historical b2af sources.
No engine state, inputs or playback clocks are edited by this presentation tool.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def run(argv):
    subprocess.run(argv, check=True)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-show_chapters", "-of", "json", str(path)]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    edl_path = Path(__file__).resolve().with_name("chapters.edl.json")
    edl = json.loads(edl_path.read_text())
    assert digest(edl_path.parent / edl["source_index"]) == edl["source_index_sha256"]
    sources = {}
    for row in edl["clips"]:
        source = args.root / row["source"]
        if source not in sources:
            assert digest(source) == row["source_sha256"], source
            assert digest(args.root / row["csv"]) == row["csv_sha256"], row["csv"]
            sources[source] = probe(source)
        info = sources[source]
        stream = next(s for s in info["streams"] if s["codec_type"] == "video")
        assert stream["width"] == row["logical_width"] * row["source_integer_scale"]
        assert stream["height"] == 224 * row["source_integer_scale"]
        assert 0 <= row["source_start_seconds"] < row["source_end_seconds"]
        assert row["source_end_seconds"] <= float(info["format"]["duration"])

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    with tempfile.TemporaryDirectory(prefix="reel-encode-", dir=out) as temp_name:
        temp = Path(temp_name)
        segments = []
        for i, row in enumerate(edl["clips"]):
            title = temp / f"title-{i}.txt"
            subtitle = temp / f"subtitle-{i}.txt"
            title.write_text(row["title"])
            subtitle.write_text(row["label"])
            width = row["logical_width"] * 2
            left = (1600 - width) // 2
            filters = (
                f"scale={width}:448:flags=neighbor,setsar=1,fps=15,"
                f"pad=1600:520:{left}:72:color=black,"
                f"drawtext=fontfile={font}:textfile={title}:fontsize=25:"
                "fontcolor=white:x=16:y=9,"
                f"drawtext=fontfile={font}:textfile={subtitle}:fontsize=18:"
                "fontcolor=0xBFC7D2:x=16:y=43,format=yuv420p"
            )
            segment = temp / f"segment-{i:02}.mkv"
            run(["ffmpeg", "-v", "error", "-threads", "2", "-filter_threads", "2", "-ss",
                 str(row["source_start_seconds"]), "-i", str(args.root / row["source"]),
                 "-t", str(row["source_end_seconds"] - row["source_start_seconds"]),
                 "-vf", filters, "-an", "-c:v", "ffv1", "-level", "3",
                 "-threads", "2", "-y", str(segment)])
            segments.append(segment)
            print(f"Normalized {i + 1}/{len(edl['clips'])}: {row['title']}", flush=True)

        concat = temp / "segments.ffconcat"
        concat.write_text("ffconcat version 1.0\n" + "".join(
            f"file '{s}'\n" for s in segments))
        metadata = temp / "chapters.ffmetadata"
        lines = [";FFMETADATA1", "title=OpenGGF S3K ending presentation repair - provisional",
                 "comment=Declared scene entries and actual final-fight input fixture; focused qualification passed; integration smoke/guards pending"]
        for row in edl["clips"]:
            lines.extend(["[CHAPTER]", "TIMEBASE=1/1000",
                          f"START={round(row['output_start_seconds'] * 1000)}",
                          f"END={round(row['output_end_seconds'] * 1000)}",
                          "title=" + row["title"]])
        metadata.write_text("\n".join(lines) + "\n")
        output = out / edl["output"]
        run(["ffmpeg", "-v", "error", "-threads", "2", "-f", "concat", "-safe", "0",
             "-i", str(concat), "-f", "ffmetadata", "-i", str(metadata), "-map", "0:v:0",
             "-map_metadata", "1", "-map_chapters", "1", "-an", "-c:v", "libx264",
             "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-threads", "2",
             "-movflags", "+faststart", "-y", str(output)])

    info = probe(output)
    stream = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (stream["width"], stream["height"], stream["r_frame_rate"]) == (1600, 520, "15/1")
    assert len(info["chapters"]) == len(edl["clips"])
    assert abs(float(info["format"]["duration"]) - edl["duration_seconds"]) < 1 / 15
    assert all(s["codec_type"] != "audio" for s in info["streams"])
    run(["ffmpeg", "-v", "error", "-xerror", "-threads", "2", "-i", str(output),
         "-f", "null", "-"])
    report = {
        "status": edl["status"], "output": output.name, "output_sha256": digest(output),
        "edl_sha256": digest(edl_path), "assembly_script_sha256": digest(Path(__file__)),
        "duration_seconds": float(info["format"]["duration"]),
        "dimensions": [1600, 520], "fps": stream["r_frame_rate"], "audio": False,
        "chapters": info["chapters"], "full_xerror_decode_exit": 0,
        "limits": "Editorial excerpts do not demonstrate a continuous cold campaign or native pixel parity."
    }
    (out / "media-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Verified " + str(len(info["chapters"])) + " chapters, " + str(report["duration_seconds"]) + "s; SHA256 " + report["output_sha256"], flush=True)


if __name__ == "__main__":
    main()
