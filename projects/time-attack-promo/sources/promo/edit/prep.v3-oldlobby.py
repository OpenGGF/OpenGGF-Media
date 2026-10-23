#!/usr/bin/env python3
"""Extract the edit's source frame ranges from the lossless FFV1 captures into native 320x224 PNGs.
Usage: prep.py [name ...]   (no names: every clip in CLIPS that is missing or has a changed range)
Each clip directory records its source capture and range in source.txt (provenance for the edit)."""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "captures"
BUILD = ROOT / "edit/build/clips"

# name: (capture, first source frame, frame count) -- source frames are capture presentation frames (60 fps)
CLIPS = {
    "open":     ("race-clean3", 1220, 1100),
    "names":    ("race-clean3", 3040, 700),
    "lineup":   ("names-relay", 1150, 560),
    "finish":   ("race-clean3", 4150, 620),
    "after":    ("race-clean3", 5590, 2460),
    "prompt":   ("lobby-s3k-profile", 590, 160),
    "profile":  ("lobby-s3k-profile", 1300, 260),
    "hpz":      ("lobby-s3k-profile", 1670, 520),
    "aizhero":  ("lobby-s3k-profile", 2400, 159),
    "ghzlobby": ("lobby-s1", 1190, 800),
    "ehzlobby": ("lobby-s2", 1130, 800),
    "death":    ("race-death", 1350, 600),
    "cap":      ("race-256", 690, 820),
}


def extract(name):
    cap, first, count = CLIPS[name]
    out = BUILD / name
    stamp = f"{cap} {first} {count}\n"
    if (out / "source.txt").exists() and (out / "source.txt").read_text() == stamp:
        return
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(CAP / cap / "video.mkv"),
                    "-vf", f"select='between(n\\,{first}\\,{first + count - 1})'", "-fps_mode", "passthrough",
                    "-start_number", "0", str(out / "%05d.png")], check=True)
    (out / "source.txt").write_text(stamp)
    print(name, stamp.strip(), len(list(out.glob("*.png"))))


if __name__ == "__main__":
    for name in (sys.argv[1:] or CLIPS):
        if (CAP / CLIPS[name][0] / "video.mkv").exists():
            extract(name)
        else:
            print("missing capture", name)
