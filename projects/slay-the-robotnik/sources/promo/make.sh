#!/bin/bash
# Rebuilds promo.mp4 from scratch (about 5 minutes): Python tools, the soundtrack and sound
# effects rendered by OpenGGF's SMPS driver, the mod clips, the OpenGGF 0.6 engine shots, then
# the composite. Needs the feature/ai-slay-the-robotnik worktree compiled (target/classes and
# target/test-classes) with s3k.gen linked in it, and the 0.6 promo masters in ~/Videos/OGGF.
set -e
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q numpy pillow; }
P=.venv/bin/python
rm -rf build/engine && mkdir -p audio build/engine
for m in 0x04:hcz2 0x29:actclear 0x2F:dataselect; do
  python3 tools/render_audio.py music ${m%%:*} 100 audio/m-${m##*:}.wav
done
python3 tools/render_audio.py sfx 0x33,0xAB,0xB6,0xB3,0xAF,0xB4,0xB8,0x63,0x6E,0x9F,0x3C,0x42,0xB1,0x6A,0xAC,0x9C,0x62,0x4E audio/sfx-bank.wav
$P tools/record.py
V=~/Videos/OGGF
while IFS='|' read id f t n y; do
  rm -rf build/engine/$id && mkdir -p build/engine/$id
  ffmpeg -nostdin -v error -y -ss $t -i "$V/$f" -frames:v $n -vf "crop=1920:1080:0:$y" build/engine/$id/%04d.png
done <<'SHOTS'
e1|S1-0.6/s1-promo-0.6.mov|0.2|110|132
e8|S3-0.6/Timeline 1.mkv|40.0|110|264
s1|S1-0.6/s1-promo-0.6.mov|19.0|270|132
s2|S2-0.6/s2-0.6-V2.mov|0.2|190|132
s3|S3-0.6/Timeline 1.mkv|2.0|110|132
SHOTS
$P tools/promo.py prep
$P tools/promo.py render
