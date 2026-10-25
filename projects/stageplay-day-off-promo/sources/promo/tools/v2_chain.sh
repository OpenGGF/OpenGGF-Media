#!/usr/bin/env bash
# Day Off v2 (sp-promo-a, 2026-10-24): sequential renders and editor captures for take t10.
# One JVM at a time (lead rule: no parallel JVM sweeps). Neutral scene folder: /tmp/stageplay.
set -u
P=/home/farrell/Videos/OGGF/sp-promo-a
cd "$P/scenes"
run() { echo "== $1"; shift; "$@"; echo "   exit $?"; }
run render1 timeout 2400 python3 ../tools/sp.py render --scene t10.stageplay --out ../captures/v2/t10-preview.mkv > ../captures/v2/t10-render.json 2> ../captures/v2/t10-render.err
run simulate timeout 1200 python3 ../tools/sp.py simulate --scene t10.stageplay --out ../captures/v2/t10.sim.jsonl --every 1 > ../captures/v2/t10-sim.json 2>/dev/null
run timeline timeout 900 python3 ../tools/sp.py timeline --scene t10.stageplay --out ../captures/v2/t10.timeline.jsonl --every 1 > /dev/null 2>&1
run sfx timeout 2400 python3 ../tools/sp.py render --scene t10-sfx.stageplay --out ../captures/v2/t10-sfx.mkv > ../captures/v2/t10-sfx.json 2> ../captures/v2/t10-sfx.err
run render4 timeout 3000 python3 ../tools/sp.py render --scene t10.stageplay --out ../captures/v2/day-off-v2-film-1080p.mkv --scale 4 > ../captures/v2/t10-render4.json 2> ../captures/v2/t10-render4.err
cd "$P"
rm -rf /tmp/stageplay/*.json /tmp/stageplay/*.mkv /tmp/stageplay/*-applied.stageplay
cp scenes/t10.stageplay /tmp/stageplay/day-off.stageplay
run tour timeout 2400 python3 tools/capture_editor.py tour /tmp/stageplay/day-off.stageplay captures/v2/editor-tour --tool EditorCapture2.java
cp /tmp/stageplay/day-off.screenplay.json /tmp/stageplay/day-off.mkv captures/v2/editor-tour/ 2>/dev/null
cp scenes/t10-editor.stageplay /tmp/stageplay/day-off.stageplay
run desktop timeout 2400 python3 tools/capture_editor.py desktop-route /tmp/stageplay/day-off.stageplay captures/v2/editor-desktop-route --tool EditorCapture2.java --desktop
cp /tmp/stageplay/desktop-route-applied.stageplay captures/v2/editor-desktop-route/ 2>/dev/null
echo "== done"
