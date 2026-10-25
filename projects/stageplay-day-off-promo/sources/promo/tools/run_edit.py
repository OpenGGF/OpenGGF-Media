#!/usr/bin/env python3
"""Runs a promo_kit edit with a capped worker count (shared machine): sheet/frames/audio/render.
Usage: run_edit.py CMD EDIT.py [args]   (sp-promo-a, 2026-10-24)"""
import os
import sys
from pathlib import Path

sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/tools/media")
os.environ.setdefault("PROMO_FONT_DIRS", "/home/farrell/Videos/OGGF/sp-promo-a/fonts")
import promo_kit  # noqa: E402
sys.modules.setdefault("promo_kit", promo_kit)
WORKERS = int(os.environ.get("EDIT_WORKERS", "4"))


def render_video(e, workers, crf=14):
    import subprocess
    from multiprocessing import Pool
    total = e.end()
    video = e.work / "promo-video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{e.W}x{e.H}", "-r", str(e.fps), "-i", "-", "-c:v", "libx264", "-threads", "6",
                            "-preset", "slow", "-crf", str(crf), "-tune", "animation", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            str(video)], stdin=subprocess.PIPE)
    with Pool(workers, initializer=promo_kit._init_worker, initargs=(promo_kit._EDIT_SPEC,)) as pool:
        for k, b in enumerate(pool.imap(promo_kit._frame_bytes, range(total), chunksize=12)):
            enc.stdin.write(b)
            if k % 600 == 0:
                print(f"frame {k}/{total}", flush=True)
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg video encode failed")
    promo_kit.write_wav(e.work / "promo-audio.wav", e.mix())
    return video


def main(argv):
    cmd, path = argv[1], argv[2]
    e = promo_kit.load_edit(path)
    for w in e.check():
        print("warning:", w)
    print("pacing:", e.pacing()[0])
    e.work.mkdir(parents=True, exist_ok=True)
    if cmd == "sheet":
        step = int(argv[3]) if len(argv) > 3 else 60
        first = int(argv[4]) if len(argv) > 4 else 0
        last = int(argv[5]) if len(argv) > 5 else None
        print(e.contact_sheet(e.work / f"sheet-{first}.png", step, first, last, workers=WORKERS))
    elif cmd == "frames":
        for a in argv[3:]:
            p = e.work / f"frame-{int(a):05d}.png"
            promo_kit.Image.fromarray(e.render_frame(int(a))).save(p)
            print(p)
    elif cmd == "audio":
        a = e.mix()
        promo_kit.write_wav(e.work / "promo-audio.wav", a)
        print(f"audio {len(a) / promo_kit.SR:.2f}s peak {abs(a).max():.3f}")
    elif cmd == "render":
        # Video only, niced, with x264 capped at 6 threads (shared machine); audio is mastered and
        # muxed separately by tools/mux_final.py (true-peak gain, chapters).
        os.nice(10)
        print(render_video(e, WORKERS), f"{e.end() / e.fps:.2f}s")
    elif cmd == "check":
        print("frames", e.end(), f"{e.end() / e.fps:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
