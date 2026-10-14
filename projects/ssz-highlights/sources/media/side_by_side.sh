#!/bin/sh
# usage: side_by_side.sh <before-raw> <after-raw> <first> <last> <out.mp4>
# Left: feature disabled; right: feature enabled. 3x nearest-neighbour, labelled.
set -e
font=$(fc-match -f '%{file}' 'DejaVu Sans:bold')
count=$(($4 - $3 + 1))
ffmpeg -loglevel error -y -framerate 60 -start_number "$3" -i "$1/frames/%05d.png" \
  -framerate 60 -start_number "$3" -i "$2/frames/%05d.png" -filter_complex \
  "[0:v]scale=iw*3:ih*3:flags=neighbor,drawtext=fontfile=$font:text='before':x=12:y=h-44:fontsize=32:fontcolor=white:borderw=3,pad=iw+12:ih:0:0:white[l];[1:v]scale=iw*3:ih*3:flags=neighbor,drawtext=fontfile=$font:text='after':x=12:y=h-44:fontsize=32:fontcolor=white:borderw=3[r];[l][r]hstack" \
  -frames:v "$count" -c:v libx264 -pix_fmt yuv420p -crf 16 "$5"
