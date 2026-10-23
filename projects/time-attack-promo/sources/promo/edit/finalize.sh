#!/bin/sh
# Final master: two-pass EBU R128 loudnorm of the compositor mix (-15 LUFS, -1.5 dBTP), AAC 256k,
# chapters, faststart. Inputs: edit/build/render/promo-{video.mp4,audio.wav} from promo_kit render.
set -eu
P=/home/farrell/Videos/OGGF/ta-promo-a
R=$P/edit/build/render
OUT=$P/out/openggf-multiplayer-time-attack-promo.mp4
J=$(ffmpeg -hide_banner -nostats -i $R/promo-audio.wav -af loudnorm=I=-15:TP=-1.5:LRA=7:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
mi=$(echo "$J" | sed -n 's/.*"input_i" : "\(.*\)",/\1/p'); mtp=$(echo "$J" | sed -n 's/.*"input_tp" : "\(.*\)",/\1/p')
mlra=$(echo "$J" | sed -n 's/.*"input_lra" : "\(.*\)",/\1/p'); mth=$(echo "$J" | sed -n 's/.*"input_thresh" : "\(.*\)",/\1/p')
off=$(echo "$J" | sed -n 's/.*"target_offset" : "\(.*\)"/\1/p')
ffmpeg -v error -y -i $R/promo-audio.wav -af "loudnorm=I=-15:TP=-1.5:LRA=7:measured_I=$mi:measured_TP=$mtp:measured_LRA=$mlra:measured_thresh=$mth:offset=$off:linear=true,aresample=48000" -c:a pcm_s16le $R/promo-audio-norm.wav
cat > $R/chapters.txt <<'CH'
;FFMETADATA1
title=OpenGGF - Multiplayer Time Attack
[CHAPTER]
TIMEBASE=1/1000
START=0
END=7417
title=Cold open: GET READY
[CHAPTER]
TIMEBASE=1/1000
START=7417
END=13817
title=Title
[CHAPTER]
TIMEBASE=1/1000
START=13817
END=26617
title=Your name, any script
[CHAPTER]
TIMEBASE=1/1000
START=26617
END=33817
title=Your colours
[CHAPTER]
TIMEBASE=1/1000
START=33817
END=45817
title=The lobby is a level
[CHAPTER]
TIMEBASE=1/1000
START=45817
END=55417
title=No lives, go again
[CHAPTER]
TIMEBASE=1/1000
START=55417
END=61817
title=Up to 256 per room (capacity test)
[CHAPTER]
TIMEBASE=1/1000
START=61817
END=76217
title=Photo finish, standings, vote
[CHAPTER]
TIMEBASE=1/1000
START=76217
END=81817
title=End card
CH
ffmpeg -v error -y -i $R/promo-video.mp4 -i $R/promo-audio-norm.wav -i $R/chapters.txt -map 0:v -map 1:a -map_metadata 2 -map_chapters 2 \
  -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
echo "$OUT"
