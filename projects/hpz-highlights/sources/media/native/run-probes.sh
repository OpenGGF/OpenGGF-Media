#!/bin/sh
# HPZ native probes from saved complete-run states (see bring-up plan, 2026-09-17).
R=/home/farrell/code/projects/OpenGGF/.worktrees/ai-hpz-bring-up
N=/home/farrell/Videos/OGGF/hpz-bring-up/native
B=434069
probe() { # name state_row first_row last_row every
  s=$((B+$2)); f=$((B+$3)); l=$((B+$4))
  printf 'return {fixture_frame=%d, fixture_zone=0x1601, windows={{label="%s",first=%d,last=%d,every=%d}}}\n' $s $1 $f $l $5 > $N/plan-$1.lua
  rm -rf $N/probe-$1
  python3 $R/tools/bizhawk/capture_native_references.py --bizhawk-home /home/farrell/code/projects/OpenGGF/docs/BizHawk-2.11-linux-x64 \
    --rom $R/s3k.gen --rom-sha1 CFBF98C36C776677290A872547AC47C53D2761D6 \
    --movie $R/src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/s3k-sonic-tails-complete-emeralds.bk2 \
    --exporter $R/tools/bizhawk/capture_hpz_route_reference.lua --plan $N/plan-$1.lua \
    --fixture-state $N/sonic-tails-states/states/$(printf '%07d' $s).State \
    --output $N/probe-$1 --require-output observations.csv --require-output done.txt --timeout 900
  echo "$1 exit=$?"
}
# probe palette 0x1E00 0x1E09 0x2000 1
# probe teleporter 0x22C0 0x2300 0x2540 1
# probe seam 0x2740 0x2760 0x2880 1
# probe fight 0x2840 0x2880 0x2E00 2
# probe altar 0x2DC0 0x2DC0 0x3400 2
# probe ending 0x3400 0x3400 0x39A0 2
probe route 0x1E00 0x1E09 0x2880 1
