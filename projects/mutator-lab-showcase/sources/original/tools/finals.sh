#!/bin/sh
# Final new source takes for the complete Mutator Lab showcase (task mutator-complete-showcase-20261010).
# Source: .worktrees/ai-mutators-complete-showcase @ 379b6641323853f61851943fb7aadd5e7a389e01 (clean), display-free.
set -e
cd /home/farrell/scratch/agent-tmp/claude/mutator-complete-showcase-20261010
C="python3 -I tools/cap.py"
$C final-stealth --game s2 --zone ehz --prefs inputs/s2-bighead200.json --script inputs/final/stealth.script --timeout 900 &
$C final-np --game s1 --zone ghz --prefs inputs/s1-np-none.json --script inputs/final/np.script --timeout 900 &
$C final-nc --game s3k --zone aiz --prefs inputs/s3k-stock.json --script inputs/final/nc.script --timeout 900 -- --x 0x2740 --y 0x250 &
wait
$C final-ss-stock --game s1 --zone ghz --prefs inputs/s1-stock.json --script inputs/final/ghz-ss-stock.script --timeout 900 -- --x 0x2100 --y 0x370 --rings 50 &
$C final-ss-deny --game s1 --zone ghz --prefs inputs/s1-stock.json --script inputs/final/ghz-ss-deny.script --timeout 900 -- --x 0x2100 --y 0x370 --rings 50 &
$C final-bonus-stock --game s3k --zone aiz --prefs inputs/s3k-stock.json --script inputs/final/bonus-stock.script --timeout 900 -- --x 0x2740 --y 0x250 --rings 25 &
wait
$C final-bonus-deny --game s3k --zone aiz --prefs inputs/s3k-stock.json --script inputs/final/bonus-deny.script --timeout 900 -- --x 0x2740 --y 0x250 --rings 25 &
$C final-speed-live --game s3k --zone aiz --prefs inputs/s3k-stock.json --script inputs/final/speed-live.script --paced --timeout 900 &
$C final-speed50 --game s3k --zone aiz --prefs inputs/s3k-speed50.json --script inputs/final/speed-same.script --paced --timeout 900 &
wait
$C final-speed100 --game s3k --zone aiz --prefs inputs/s3k-speed100on.json --script inputs/final/speed-same.script --paced --timeout 900 &
$C final-speed200 --game s3k --zone aiz --prefs inputs/s3k-speed200.json --script inputs/final/speed-same.script --paced --timeout 900 &
wait
