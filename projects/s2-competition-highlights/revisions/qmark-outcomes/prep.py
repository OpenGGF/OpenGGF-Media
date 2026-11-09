#!/usr/bin/env python3
"""Purpose: cut the outcomes reel's engine and native frames and engine audio.
Inputs: ../engine/<content>/engine.mkv + audio.pcm (DebugSonic2CompetitionRouteVideo, 320x448, one
frame per route row) and ../native-<content>/frames/*.png (BizHawk 348x480 interlaced). Writes
frames/<content>/ and frames/<content>-native/ as 640x448 PNGs and audio/<content>.wav.
Origin: 2026-11-09 "?" monitor outcomes request.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from shots import ENGINE, LEAD, HOLD, NATIVE_OFFSET, NATIVE_ROOT, OUTCOMES  # noqa: E402

def native(content, row):
    im = Image.open(NATIVE_ROOT / f"native-{content}" / "frames" / f"{row + NATIVE_OFFSET:05d}.png").convert("RGB")
    w, h = im.size
    lines = 448 if h >= 480 else 224
    left, top = (w - 320) // 2, (h - lines) // 2
    return im.crop((left, top, left + 320, top + lines)).resize((640, 448), Image.NEAREST)

def main():
    (ROOT / "audio").mkdir(exist_ok=True)
    for content, n, title, lfc, brk, note, layout in OUTCOMES:
        first, count = brk - LEAD, LEAD + HOLD
        src = ENGINE / content
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "2", "-i",
                        str(src / "audio.pcm"), str(ROOT / "audio" / f"{content}.wav")], check=True)
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src / "engine.mkv"), "-frames:v",
                                str(first + count), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        out, nout = ROOT / "frames" / content, ROOT / "frames" / f"{content}-native"
        out.mkdir(parents=True, exist_ok=True); nout.mkdir(parents=True, exist_ok=True)
        size = 320 * 448 * 3
        for r in range(first + count):
            buf = dec.stdout.read(size)
            assert len(buf) == size, f"{content}: video ended at {r}"
            if r >= first:
                i = r - first
                Image.frombytes("RGB", (320, 448), buf).resize((640, 448), Image.NEAREST).save(out / f"{i:05d}.png")
                native(content, r).save(nout / f"{i:05d}.png")
        dec.stdout.close(); dec.wait()
        print(content, "ok")

if __name__ == "__main__":
    main()
