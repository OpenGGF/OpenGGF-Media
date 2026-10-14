#!/bin/sh
# DDZ bring-up demo clips. Source: raw-17-seeded-route-320-visual-fixes (GameplayCaptureTool, commit 92c1abba0;
# seeded native route, exact to native through frame 10058).
# Native footage: native/probe-vid-* (BizHawk, capture_ddz_route_reference.lua, every frame).
# Engine frame f == native movie frame 514214 + f.
set -e
cd "$(dirname "$0")"
R=raw-17-seeded-route-320-visual-fixes
clip() { sh make_clip.sh "$R" "$1" "$2" "$3"; echo "$3"; }
clip 0 150 01-ddz-fall-in-transform-hyper.mp4
clip 440 560 02-ddz-asteroid-shatters.mp4
clip 1000 1560 03-ddz-missiles-ride-and-home.mp4
clip 3560 3780 04-ddz-boss-arrival-camera-lock.mp4
clip 3860 3990 05-ddz-missile-redirected-into-body.mp4
clip 5120 5520 06-ddz-phase1-defeat-ship-breaks-up.mp4
clip 5760 6080 07-ddz-phase2-chase-master-emerald.mp4
clip 6200 6420 08-ddz-phase2-bombs.mp4
clip 7360 7540 09-ddz-rockets-and-level-wrap.mp4
clip 9820 9990 10-ddz-defeat-explosions.mp4
clip 9960 10100 11-ddz-exit-white-fade-to-ending.mp4
cp "$R/capture.mp4" 20-ddz-seeded-route-full-uncut.mp4
# Native (left) vs engine (right), same frames.
font=$(fc-match -f '%{file}' 'DejaVu Sans:bold')
nat() { # name first_movie last_movie out
  f=$(($2 - 514214)); count=$(($3 - $2 + 1))
  ffmpeg -loglevel error -y -framerate 60 -start_number "$2" -i "native/probe-$1/$1/%07d.png" \
    -framerate 60 -start_number "$f" -i "$R/frames/%05d.png" -filter_complex \
    "[0:v]scale=960:672:flags=neighbor,drawtext=fontfile=$font:text='native':x=12:y=h-44:fontsize=32:fontcolor=white:borderw=3,pad=iw+12:ih:0:0:white[l];[1:v]scale=960:672:flags=neighbor,drawtext=fontfile=$font:text='engine':x=12:y=h-44:fontsize=32:fontcolor=white:borderw=3[r];[l][r]hstack" \
    -frames:v "$count" -c:v libx264 -pix_fmt yuv420p -crf 16 "$4"
  echo "$4"
}
nat vid-entry 514214 514443 30-ddz-native-vs-engine-entry.mp4
nat vid-arrival 517798 518117 31-ddz-native-vs-engine-boss-arrival.mp4
nat vid-wrap 521622 521760 32-ddz-native-vs-engine-first-wrap.mp4
nat vid-exit 524086 524278 33-ddz-native-vs-engine-exit.mp4
# Before (baseline load, no Doomsday code) vs after.
sh side_by_side.sh raw-00-baseline-before-work "$R" 0 256 00-ddz-before-after-entry.mp4 && echo 00-ddz-before-after-entry.mp4
# Widescreen 800 (raw-18, commit 92c1abba0; native-input route diverges from native at this width).
sh make_clip.sh raw-18-seeded-route-800-visual-fixes 3560 3900 40-ddz-widescreen-800-boss-arrival.mp4 && echo 40-ddz-widescreen-800-boss-arrival.mp4
