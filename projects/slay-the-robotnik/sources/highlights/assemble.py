#!/usr/bin/env python3
"""Assembles reel.mp4 from edit.csv: trims each source interval, scales the 800x448 capture
x2 with nearest-neighbour into a 1920x1080 frame, captions it in the lower bar, fades each
cut through black (video and audio), concatenates, and writes chapters.txt."""
import csv, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
FADE = 0.2
seg_dir = ROOT / "segments"
seg_dir.mkdir(exist_ok=True)
rows = list(csv.DictReader(open(ROOT / "edit.csv")))
segments, chapters, t = [], [], 0.0

def esc(text):
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")

for r in rows:
    start, end = float(r["source_start_seconds"]), float(r["source_end_seconds"])
    d = end - start
    out = seg_dir / f"{int(r['order']):02d}.mp4"
    caption = esc(r["title"])
    tag = "positioned start (debug jump)" if r["positioned"] == "yes" else "played from the title screen"
    vf = (f"scale=1600:896:flags=neighbor,pad=1920:1080:160:92:black,"
          f"drawtext=fontfile={FONT}:text='{caption}':x=160:y=1004:fontsize=34:fontcolor=white,"
          f"drawtext=fontfile={FONT}:text='{esc(tag)}':x=1760-tw:y=1014:fontsize=20:fontcolor=0x8090A0,"
          f"drawtext=fontfile={FONT}:text='SLAY THE ROBOTNIK  -  an OpenGGF example mod':x=160:y=34:fontsize=26:fontcolor=0xFFD040,"
          f"fade=t=in:st=0:d={FADE},fade=t=out:st={d - FADE:.3f}:d={FADE}")
    af = f"afade=t=in:st=0:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                    "-i", str(ROOT / r["source"]), "-vf", vf, "-af", af, "-r", "60",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)], check=True)
    real = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(out)]))
    chapters.append((t, t + real, r))
    t += real
    segments.append(out)

(seg_dir / "list.txt").write_text("".join(f"file '{s.name}'\n" for s in segments))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(seg_dir / "list.txt"),
                "-c", "copy", "-movflags", "+faststart", str(ROOT / "reel.mp4")], check=True)
with open(ROOT / "chapters.txt", "w") as f:
    f.write("output_start,output_end,title,source,source_start,source_end,positioned\n")
    for a, b, r in chapters:
        f.write(f"{a:.2f},{b:.2f},{r['title']},{r['source']},{r['source_start_seconds']},"
                f"{r['source_end_seconds']},{r['positioned']}\n")
print(f"reel.mp4: {t:.1f} s, {len(segments)} segments")
