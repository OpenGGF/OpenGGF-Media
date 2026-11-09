#!/bin/sh
# Purpose: final mux of the outcomes reel: -1.8 dB (AAC true-peak headroom) and chapters.
# Inputs: build/promo-video.mp4, build/promo-audio.wav, build/chapters.txt. Origin: 2026-11-09.
set -e
cd "$(dirname "$0")"
ffmpeg -v error -y -i build/promo-video.mp4 -i build/promo-audio.wav -i build/chapters.txt -map 0:v -map 1:a \
  -map_metadata 2 -map_chapters 2 -af volume=-1.8dB -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest \
  out/s2-qmark-outcomes.mp4
