#!/bin/bash
set -euo pipefail
cd /home/farrell/code/projects/OpenGGF/.worktrees/ai-starpost-promo
ROOT=/home/farrell/scratch/sv-promo/final
CP="target/test-classes:target/classes:$(cat target/test-classpath.txt)"
java -cp "$ROOT/capture-classes:$CP" com.openggf.StarpostPromoCapture "$PWD/Sonic and Knuckles & Sonic 3 (W) [!].gen" "$PWD/Sonic The Hedgehog (W) (REV01) [!].gen" "$ROOT/mods" "$ROOT/$1" "$ROOT/$1.txt" "$2" > "$ROOT/$1.log" 2>&1
ffmpeg -y -v error -framerate 60 -i "$ROOT/$1/%04d.png" -f s16le -ar 48000 -ac 2 -i "$ROOT/$1/audio.raw" -vf 'scale=800:448:flags=neighbor' -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "$ROOT/$1.mp4"
