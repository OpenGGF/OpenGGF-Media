#!/bin/sh
# Purpose: final mux of the rendered reel: -1.8 dB so the AAC true peak sits under -1 dBFS, plus chapters.
# Inputs: build/promo-video.mp4 and build/promo-audio.wav from `promo_kit.py render edit.py`; build/chapters.txt.
# Origin: 2026-11-09 S2 Competition highlights (render measured +0.4 dBFS true peak before this step).
set -e
cd "$(dirname "$0")"
ffmpeg -v error -y -i build/promo-video.mp4 -i build/promo-audio.wav -i build/chapters.txt -map 0:v -map 1:a \
  -map_metadata 2 -map_chapters 2 -af volume=-1.8dB -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest \
  out/s2-competition-highlights-v2.mp4
