#!/bin/sh
# Final promo takes from the clean committed head (task e0603654). Run from the output root.
set -e
cd /home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3
C="python3 -I tools/cap.py"
$C final-ghz-hero --game s1 --zone ghz --prefs inputs/s1-hero-seed.json --script inputs/ghz/hero-menu.script --timeout 300 -- --x 0x1180 --y 0x300 --rings 140 &
$C final-ghz-native --game s1 --zone ghz --prefs inputs/s1-hero-seed.json --script inputs/ghz/hero-40.script --timeout 300 -- --x 0x1180 --y 0x300 --rings 140 &
$C final-syz-chain --game s1 --zone mz --prefs inputs/s1-syz-seed.json --script inputs/syz/chain-menu.script --timeout 300 &
wait
$C final-syz-native --game s1 --zone mz --prefs inputs/s1-syz-native.json --script inputs/sweep/syzH-4.script --timeout 300 &
$C final-s2-live --game s2 --zone ehz --prefs inputs/s2-live.json --script inputs/live/gravity.script --timeout 300 &
$C final-aiz-norings --game s3k --zone aiz --prefs inputs/s3k-base.json --script inputs/aiz/norings-a.script --timeout 400 &
wait
$C final-aiz-allon --game s3k --zone aiz --prefs inputs/s3k-allon.json --script inputs/aiz/allon-menu.script --timeout 400 -- --rings 200
