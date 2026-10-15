#!/usr/bin/env python3
"""Assemble the 47-second Second Strike AIZ development excerpt, at native speed.

Inputs: this revision's edit-list.json/provenance.json and the relocated immutable
sonic-solo-r7 cold-campaign.mkv/state.csv. Requires Python 3 and ffmpeg/ffprobe.
No engine, ROM, display, capture, audio device or additional soundtrack is used.
Origin: Second Strike AIZ completion task, 2026-10-15; capture development HEAD
22841e86ae4de2fd4206bef5cab0cad535127728 plus staged tree 6508a7a64826a0ab.

The default only validates the small source files/header and prints the plan.
--render performs one final H.264/AAC encode; launch it through the host's normal
admission and intended-tree lease, as documented in README.md. Rendering is not
visual/audio approval or full-decode verification. Earlier outputs are preserved.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from fractions import Fraction

HERE = Path(__file__).resolve().parent
FPS = 60
SAMPLE_RATE = 48_000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS
EXPECTED_FRAMES = 2_820
CANVAS = (1_600, 900)


def read_json(path: Path):
    return json.loads(path.read_text())


def digest(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def probe(path: Path, executable: str) -> dict:
    command = [executable, "-v", "error", "-show_streams", "-show_format",
               "-show_chapters", "-of", "json", str(path)]
    return json.loads(subprocess.check_output(command, text=True, timeout=30))


def validate(capture_root: Path, ffprobe: str) -> tuple[list[dict], dict]:
    provenance = read_json(HERE / "provenance.json")
    shots = read_json(HERE / "edit-list.json")
    movie = capture_root / provenance["movie"]["file"]
    if movie.stat().st_size != provenance["movie"]["bytes"]:
        raise ValueError("Source movie size differs from the pinned capture")
    for entry in provenance["small_capture_files"]:
        path = capture_root / entry["file"]
        if path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
            raise ValueError(f"Source differs from the pinned capture: {path.name}")
    with (capture_root / "state.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != provenance["movie"]["frames"]:
        raise ValueError("CSV row count differs from the native movie frame count")
    offset = 0
    previous_end = 0
    for shot in shots:
        start, end = shot["source_start_frame"], shot["source_end_frame_exclusive"]
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("Source intervals require integer frame boundaries")
        if not 0 <= start < end <= len(rows) or start < previous_end:
            raise ValueError("Source interval is invalid or reverses native route order")
        if shot["output_start_frame"] != offset:
            raise ValueError("Output frame intervals must be contiguous")
        offset += end - start
        if shot["output_end_frame_exclusive"] != offset:
            raise ValueError("Source and output interval lengths disagree")
        for number in range(start, end):
            row = rows[number]
            if int(row["frame"]) != number or row["dead"] != "0" or row["mode"] != "LEVEL":
                raise ValueError(f"Selected row {number} is not the admitted alive LEVEL frame")
        previous_end = end
    if offset != EXPECTED_FRAMES:
        raise ValueError("This preserved edit must contain exactly 2,820 frames")
    cuts = [shot["output_start_frame"] for shot in shots[1:]]
    if sum(cut > offset - 20 * FPS for cut in cuts) > 1:
        raise ValueError("The final twenty seconds must contain at most one picture cut")
    header = probe(movie, ffprobe)
    video = [stream for stream in header["streams"] if stream["codec_type"] == "video"]
    audio = [stream for stream in header["streams"] if stream["codec_type"] == "audio"]
    if len(video) != 1 or len(audio) != 1:
        raise ValueError("Expected one native video and one synchronized audio stream")
    stream = video[0]
    if ((stream["width"], stream["height"]) != (320, 224)
            or Fraction(stream["avg_frame_rate"]) != FPS
            or stream["codec_name"] != "ffv1"):
        raise ValueError("Source is not the pinned 320x224, 60 fps FFV1 capture")
    if (audio[0]["codec_name"] != "flac" or int(audio[0]["sample_rate"]) != SAMPLE_RATE
            or audio[0]["channels"] != 2):
        raise ValueError("Source is not the pinned stereo 48 kHz FLAC capture")
    if any(float(stream.get("start_time", 0)) != 0 for stream in video + audio):
        raise ValueError("The native frame/sample mapping requires both streams to start at zero")
    return shots, header


def filter_path(path: Path) -> str:
    # FFmpeg option/filter escaping is distinct from shell escaping. All commands
    # below are argv lists, with no shell. Text labels use textfile/expansion=none.
    value = str(path).replace("\\", "\\\\").replace(":", "\\:")
    return "'" + value.replace("'", "'\\''") + "'"


def render(capture_root: Path, output_root: Path, shots: list[dict], font: Path,
           ffmpeg: str, ffprobe: str, timeout: int) -> Path:
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError("Use a new empty output directory; earlier productions are never overwritten")
    output_root.mkdir(parents=True, exist_ok=True)
    labels = output_root / "labels"
    labels.mkdir()
    title = labels / "title.txt"
    title.write_text("Second Strike · development excerpt\n")
    filters = [f"[0:v:0]split={len(shots)}" + "".join(f"[v{i}]" for i in range(len(shots))),
               f"[0:a:0]asplit={len(shots)}" + "".join(f"[a{i}]" for i in range(len(shots)))]
    for i, shot in enumerate(shots):
        start, end = shot["source_start_frame"], shot["source_end_frame_exclusive"]
        headline = labels / f"{i}-title.txt"
        headline.write_text(shot["title"] + "\n")
        draw = lambda text, x, y, size, color="white": (
            f"drawtext=fontfile={filter_path(font)}:textfile={filter_path(text)}:"
            f"x={x}:y={y}:fontsize={size}:fontcolor={color}:expansion=none")
        video = [f"[v{i}]trim=start_frame={start}:end_frame={end}",
                 "setpts=PTS-STARTPTS", "scale=960:672:flags=neighbor",
                 "pad=1600:900:320:114:color=0x101928", "setsar=1",
                 draw(title, 40, 42, 26, "0xb7c7d8"),
                 draw(headline, 40, 822, 28)]
        filters.append(",".join(video) + f"[picture{i}]")
        duration = (end - start) / FPS
        # Nonoverlapping fades, not crossfades: at any time one source interval
        # owns the audio. Fixed -1.5 dB gain preserves dynamics and cue timing.
        filters.append(
            f"[a{i}]atrim=start_sample={start * SAMPLES_PER_FRAME}:"
            f"end_sample={end * SAMPLES_PER_FRAME},asetpts=PTS-STARTPTS,"
            f"volume=-1.5dB,afade=t=in:st=0:d=0.05,"
            f"afade=t=out:st={duration - 0.05:.9f}:d=0.05[sound{i}]")
    filters.append("".join(f"[picture{i}][sound{i}]" for i in range(len(shots)))
                   + f"concat=n={len(shots)}:v=1:a=1[video][audio]")
    graph = output_root / "filters.txt"
    graph.write_text(";\n".join(filters) + "\n")
    metadata = output_root / "chapters.ffmeta"
    metadata.write_text((HERE / "chapters.ffmeta").read_text())
    output = output_root / "second-strike-aiz-development.mp4"
    command = [ffmpeg, "-hide_banner", "-loglevel", "warning", "-nostdin", "-n",
               "-filter_complex_threads", "2", "-threads", "2",
               "-i", str(capture_root / "cold-campaign.mkv"), "-f", "ffmetadata", "-i", str(metadata),
               "-filter_complex", graph.read_text(), "-map", "[video]", "-map", "[audio]",
               "-map_metadata", "1", "-map_chapters", "1", "-t", "47", "-c:v", "libx264",
               "-preset", "medium", "-crf", "18", "-threads", "2", "-pix_fmt", "yuv420p",
               "-r", "60", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
               "-movflags", "+faststart", str(output)]
    (output_root / "assembly-command.json").write_text(json.dumps(command, indent=2) + "\n")
    subprocess.run(command, check=True, timeout=timeout)
    header = probe(output, ffprobe)
    (output_root / "output-probe.json").write_text(json.dumps(header, indent=2) + "\n")
    for filename in ("edit-list.json", "edit-list.csv", "chapters.json", "provenance.json"):
        shutil.copyfile(HERE / filename, output_root / filename)
    # No success/approval record is generated. Root must review actual motion and
    # audio, verify all cuts, full-decode, and finalize the external asset catalog.
    return output


def inside_git_worktree(path: Path) -> bool:
    # Some task hosts create empty .git marker directories outside repositories.
    # A marker alone is not Git identity. Ask Git to validate each candidate;
    # worktree .git files and ordinary repository directories are both supported.
    for parent in (path, *path.parents):
        if not (parent / ".git").exists():
            continue
        result = subprocess.run(
            ["git", "-C", str(parent), "rev-parse", "--show-toplevel"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=10, check=False)
        if result.returncode == 0:
            root = Path(result.stdout.strip()).resolve()
            if path == root or root in path.parents:
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-root", type=Path, required=True,
                        help="Relocated sonic-solo-r7 directory with the pinned movie/CSV/input/receipt")
    parser.add_argument("--output-root", type=Path,
                        help="New empty production directory outside this archive (required for --render)")
    parser.add_argument("--render", action="store_true", help="Encode after normal host admission")
    parser.add_argument("--verify-movie-sha256", action="store_true",
                        help="Read/hash the large movie, only when this I/O is appropriate/admitted")
    parser.add_argument("--font", type=Path,
                        default=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    capture_root = args.capture_root.resolve()
    shots, header = validate(capture_root, args.ffprobe)
    if args.verify_movie_sha256:
        expected = read_json(HERE / "provenance.json")["movie"]["sha256"]
        if digest(capture_root / "cold-campaign.mkv") != expected:
            raise ValueError("Source movie SHA-256 differs from the observed pinned capture")
    summary = dict(status="plan_only", frames=EXPECTED_FRAMES, duration_seconds=47,
                   canvas=list(CANVAS), fps=FPS, picture_cuts=3,
                   cuts_in_last_twenty_seconds=1, source_duration=header["format"]["duration"],
                   source_root=str(capture_root), shots=shots,
                   limits="Not rendered, full-decoded, moving/audio reviewed or publicly archived by this command")
    if args.render:
        if args.output_root is None:
            parser.error("--render requires a new --output-root outside the archive")
        output_root = args.output_root.resolve()
        # The editable source may run from its archived Git path or a relocated
        # standalone working copy. A fixed HERE.parents offset misidentifies a
        # relocated copy's host directory as the archive. Check actual repository
        # markers at the destination, and protect this source directory itself.
        if (output_root == HERE or HERE in output_root.parents
                or inside_git_worktree(output_root)):
            parser.error("Generated media must remain outside source directories and Git working trees")
        if not args.font.is_file() or not 1 <= args.timeout_seconds <= 1800:
            parser.error("Supply a readable font and a 1..1800 second bounded render timeout")
        output = render(capture_root, output_root, shots, args.font.resolve(),
                        args.ffmpeg, args.ffprobe, args.timeout_seconds)
        summary.update(status="encoded_unreviewed", output=str(output),
                       limits="Moving/audio review, full decode and public archive delivery remain required")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
