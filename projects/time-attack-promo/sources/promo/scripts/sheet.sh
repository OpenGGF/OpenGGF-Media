#!/bin/sh
# Usage: sheet.sh <video> <out.png> <first-frame> <step> [count=30] — contact sheet of native frames, 6 columns, frame numbers stamped.
set -eu
v=$1; o=$2; f=$3; s=$4; n=${5:-30}
ffmpeg -v error -y -i "$v" -vf "select='gte(n\,$f)*not(mod(n-$f\,$s))',drawtext=fontfile=/home/farrell/Videos/OGGF/ta-promo-a/fonts/Hack-Bold.ttf:text='%{frame_num}':start_number=0:x=4:y=4:fontsize=12:fontcolor=yellow:box=1:boxcolor=black,tile=6x$(( (n+5)/6 ))" -frames:v 1 -fps_mode passthrough "$o"
