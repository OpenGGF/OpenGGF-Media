#!/usr/bin/env python3
"""Masters and muxes the sp-promo-a promo (2026-10-24).

Inputs: edit/build/promo-video.mp4 and edit/build/promo-audio.wav from tools/run_edit.py render.
Applies one gain so the mix's true peak is at most -1.5 dBTP (the promo_kit master limits
sample peaks only), encodes AAC 256 kb/s, writes chapters at the edit's chapter cuts (each is
checked against the loaded edit's shot boundaries), and muxes out/day-off-stageplay.mp4.
Usage: mux_final.py EDIT.py [--chapters v2]
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/tools/media")
os.environ.setdefault("PROMO_FONT_DIRS", "/home/farrell/Videos/OGGF/sp-promo-a/fonts")
import promo_kit  # noqa: E402

# (shot index in the edit, chapter title)
CHAPTERS = [(0, "Day Off (the film)"), (1, "Stageplay"), (3, "Rewind"), (4, "Sets and cast"),
            (6, "Free and Puppet"), (8, "World and camera"), (11, "The route"), (17, "Dialogue"),
            (18, "Screenplay"), (19, "Export"), (20, "Epilogue"), (21, "End card")]
# v2 (edit_v2.py) shot indices: route picker / voices chapters (pass --chapters v2).
CHAPTERS_V2 = [(0, "Day Off (the film)"), (1, "Stageplay"), (3, "Rewind"), (4, "Sets and cast"),
               (6, "Free and Puppet"), (8, "World and camera"), (11, "The route"), (18, "Lines and voices"),
               (22, "Screenplay"), (23, "Export"), (24, "Epilogue"), (25, "End card")]
TARGET_TP = -1.5


def true_peak(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = err[err.rfind("Summary"):]
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", summary, re.S).group(1))
    loud = float(re.search(r"I:\s+(-?[\d.]+)", summary).group(1))
    return tp, loud


def main(argv):
    chapters = CHAPTERS_V2 if "--chapters" in argv and argv[argv.index("--chapters") + 1] == "v2" else CHAPTERS
    e = promo_kit.load_edit(argv[1])
    work, out = e.work, Path(e.out)
    video, audio = work / "promo-video.mp4", work / "promo-audio.wav"
    for k, (i, _) in enumerate(chapters):
        assert i < len(e.shots), (i, len(e.shots))
    tp, loud = true_peak(audio)
    gain_db = min(0.0, TARGET_TP - tp)
    a = promo_kit.read_wav(audio) * (10 ** (gain_db / 20))
    final = work / "promo-audio-final.wav"
    promo_kit.write_wav(final, a.astype(np.float32))
    tp2, loud2 = true_peak(final)
    print(f"mix: I {loud:.1f} LUFS, true peak {tp:.1f} dBTP -> gain {gain_db:+.2f} dB -> I {loud2:.1f} LUFS, "
          f"true peak {tp2:.1f} dBTP")
    meta = work / "chapters.txt"
    starts = [e.shots[i].f0 for i, _ in chapters] + [e.end()]
    lines = [";FFMETADATA1", "title=Day Off - a Stageplay film (OpenGGF)",
             "comment=Stageplay promo; staged story exported by Stageplay, editors captured offscreen."]
    for (i, title), f0, f1 in zip(chapters, starts, starts[1:]):
        ms0, ms1 = round(f0 * 1000 / e.fps), round(f1 * 1000 / e.fps)
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={ms0}", f"END={ms1}", f"title={title}"]
        print(f"chapter {ms0 / 1000:7.2f}s  {title}")
    meta.write_text("\n".join(lines) + "\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(final), "-i", str(meta),
                    "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                    "-movflags", "+faststart", "-shortest", str(out)], check=True)
    tp3, loud3 = true_peak(out)
    print(f"encoded AAC: I {loud3:.1f} LUFS, true peak {tp3:.1f} dBTP -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
