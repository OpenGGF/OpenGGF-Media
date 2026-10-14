#!/bin/sh
# usage: make_clip.sh <raw-dir> <first-frame> <last-frame> <output.mp4>
# Encodes captured PNG frames [first,last] at 60 fps, 3x nearest-neighbour.
set -e
raw="$1"; first="$2"; last="$3"; out="$4"
count=$((last - first + 1))
ffmpeg -loglevel error -y -framerate 60 -start_number "$first" -i "$raw/frames/%05d.png" \
  -frames:v "$count" -vf "scale=iw*3:ih*3:flags=neighbor" -c:v libx264 -pix_fmt yuv420p -crf 16 "$out"
