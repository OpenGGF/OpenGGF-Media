#!/usr/bin/env python3
"""Final audio master for the Sonic Echoes promo: two-pass EBU R128 loudnorm of promo_kit's PCM mix
to -16 LUFS plus a -4.4 dBFS limiter (measured <= -1 dBTP after AAC), then re-mux with the rendered video stream copied untouched.

Why: promo_kit's mix peaks at -0.7 dBFS PCM, but the SMPS FM bed's square-edged waveforms overshoot
to +2.7 dBTP after AAC encoding. Run after `promo_kit.py render edit/edit.py`.
Origin: Sonic Echoes promo, 2026-10-24.
"""
import json
import subprocess
import sys
from pathlib import Path

TASK = Path(__file__).resolve().parent.parent
pcm = TASK / "edit/build/render/promo-audio.wav"
video = TASK / "out/sonic-echoes-promo.mp4"
out = TASK / "out/sonic-echoes-promo-master.mp4"
target = "I=-16:TP=-2:LRA=11"
probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(pcm), "-af",
                        f"loudnorm={target}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
af = (f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
      # AAC adds ~2 dB of inter-sample overshoot to this bed, so hold the PCM well under the ceiling.
      "alimiter=limit=0.6:attack=1:release=60:level=disabled,aresample=48000")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(pcm), "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out)],
               check=True)
print(out)
