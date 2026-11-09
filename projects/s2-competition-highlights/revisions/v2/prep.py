#!/usr/bin/env python3
"""Purpose: cut the reel's source frames and engine audio out of the full route captures.
Inputs: cap/<route>/engine.mkv (320x448 FFV1, one frame per route row) and audio.pcm (48 kHz s16le
stereo, 800 frames per row); native BizHawk frames for the parity shot. Writes frames/<shot>/ as
640x448 PNGs (nearest-neighbour, square-pixel 2P picture) and audio/<route>.wav.
Origin: 2026-11-09 S2 Competition highlights for James.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from shots import CAP, CLIPS, NATIVE, NATIVE_OFFSET, SHOTS  # noqa: E402

FRAMES = ROOT / "frames"
AUDIO = ROOT / "audio"


def native_frame(row):
    im = Image.open(NATIVE / f"{row + NATIVE_OFFSET:05d}.png").convert("RGB")
    w, h = im.size
    lines = 448 if h >= 480 else 224  # interlaced 2P frames carry both fields
    left, top = (w - 320) // 2, (h - lines) // 2
    return im.crop((left, top, left + 320, top + lines)).resize((640, 448), Image.NEAREST)


def main():
    AUDIO.mkdir(parents=True, exist_ok=True)
    for key, route in CLIPS.items():
        wanted = {}
        for name, clip, row, n, layout in SHOTS:
            if clip == key:
                for r in range(row, row + n):
                    wanted.setdefault(r, []).append((name, r - row))
        pcm = CAP / route / "audio.pcm"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "2", "-i", str(pcm),
                        str(AUDIO / f"{route}.wav")], check=True)
        if not wanted:
            continue
        last = max(wanted)
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(CAP / route / "engine.mkv"), "-frames:v",
                                str(last + 1), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        size = 320 * 448 * 3
        for r in range(last + 1):
            buf = dec.stdout.read(size)
            if len(buf) != size:
                raise SystemExit(f"{route}: video ended at row {r}")
            for name, i in wanted.get(r, []):
                out = FRAMES / name
                out.mkdir(parents=True, exist_ok=True)
                Image.frombytes("RGB", (320, 448), buf).resize((640, 448), Image.NEAREST).save(out / f"{i:05d}.png")
        dec.stdout.close()
        dec.wait()
        print(route, "frames through row", last)
    for name, clip, row, n, layout in SHOTS:
        if layout == "parity":
            out = FRAMES / f"{name}-native"
            out.mkdir(parents=True, exist_ok=True)
            for i in range(n):
                native_frame(row + i).save(out / f"{i:05d}.png")
    print("ok")


if __name__ == "__main__":
    main()
