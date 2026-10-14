#!/usr/bin/env python3
"""Assemble the Flappy Tails promo from ExampleModCapture recordings and ROM-drawn card sequences.

Inputs (task directory, never the repository):
  cards/<name>/f%04d.png   400x224 card frames from PromoCards (ROM lettering, sprites, backdrops)
  caps/<name>/<name>.mp4   2000x1120 60 fps captures with game audio (ExampleModCapture --scale 5)
  sfx/<name>.wav           stingers cut from the captures' own audio
Output: out/flappy-tails-promo.mp4, 1920x1080 60 fps H.264 + AAC 48 kHz, loudness-normalised.

Task tool for the 2026-10-08 Flappy Tails promo; see the tutorial's part 9.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
OUT = ROOT / "out"
FPS = 60
VIDEO = ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AUDIO = ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]
# 400x224 at 5x is 2000x1120; crop 40 px each side and 20 top and bottom for exact 1080p.
CROP = "crop=1920:1080:40:20"


def run(cmd):
    print(" ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def card(name, frames, sfx=None, sfx_at=0.0, sfx_gain=1.0, music=None, music_from=0.0, music_gain=0.6):
    """A card's PNG sequence scaled 5x nearest, with an optional stinger and music bed."""
    out = WORK / f"card-{name}.mov"
    dur = frames / FPS
    inputs = ["-framerate", FPS, "-i", ROOT / "cards" / name / "f%04d.png"]
    mix = []
    idx = 1
    if sfx:
        inputs += ["-i", ROOT / "sfx" / f"{sfx}.wav"]
        mix.append(f"[{idx}:a]adelay={int(sfx_at * 1000)}|{int(sfx_at * 1000)},volume={sfx_gain}[s{idx}]")
        idx += 1
    if music:
        inputs += ["-ss", music_from, "-i", music]
        mix.append(f"[{idx}:a]volume={music_gain}[s{idx}]")
        idx += 1
    if idx == 1:
        inputs += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        audio = "[1:a]atrim=0:%f[a]" % dur
    else:
        labels = "".join(f"[s{i}]" for i in range(1, idx))
        audio = ";".join(mix) + f";{labels}amix=inputs={idx - 1}:normalize=0,atrim=0:{dur},apad=whole_dur={dur}[a]"
    graph = f"[0:v]scale=2000:1120:flags=neighbor,{CROP},setsar=1[v];{audio}"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-t", dur, *VIDEO, *AUDIO, out])
    return out


def clip(name, src, start, dur, speed=1.0, punches=(), flash_at=(), label=None):
    """A cut from a capture: trimmed, cropped, optionally slowed (pitch falls with it), with zoom
    punches (times in seconds of the output) and white flashes."""
    out = WORK / f"clip-{name}.mov"
    v = [f"trim=start={start}:duration={dur}", "setpts=PTS-STARTPTS", CROP]
    if speed != 1.0:
        v.append(f"setpts=PTS/{speed}")
        v.append(f"minterpolate=fps={FPS}:mi_mode=dup")
    for t in punches:
        # A quick 12% zoom that decays over a quarter second.
        z = f"(1+0.12*max(0,1-abs(t-{t})/0.25))"
        v.append(f"scale=w='iw*{z}':h='ih*{z}':eval=frame:flags=neighbor,crop=1920:1080")
    for t in flash_at:
        v.append(f"eq=brightness='0.6*max(0,1-abs(t-{t})/0.12)':eval=frame")
    v.append("setsar=1")
    a = [f"atrim=start={start}:duration={dur}", "asetpts=PTS-STARTPTS"]
    if speed != 1.0:
        a.append(f"asetrate=48000*{speed},aresample=48000")
    graph = f"[0:v]{','.join(v)}[v];[0:a]{','.join(a)}[a]"
    run(["ffmpeg", "-y", "-i", src, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", *VIDEO, *AUDIO, out])
    return out


def join(parts, out):
    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = WORK / "joined.mov"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", joined])
    # Two-pass loudness to -14 LUFS, -1 dBTP.
    probe = subprocess.run(["ffmpeg", "-i", str(joined), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
    stats = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    ln = ("loudnorm=I=-14:TP=-1:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:linear=true").format(**stats)
    run(["ffmpeg", "-y", "-i", joined, "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
         "-af", ln + ",aresample=48000,alimiter=limit=0.79:level=false", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])


if __name__ == "__main__":
    WORK.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    plan = __import__("promo_plan").PLAN
    parts = [step() for step in plan(card, clip, ROOT)]
    join(parts, OUT / "flappy-tails-promo.mp4")
    print("done", OUT / "flappy-tails-promo.mp4")
