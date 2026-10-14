#!/bin/sh
# DDZ native probes from pass-1 states. Usage: run-probe.sh <name> <state_row_hex> <first_row_hex> <last_row_hex> <every>
R=/home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-visual-fixes
N=/home/farrell/Videos/OGGF/ddz-bring-up/native
B=514214
name=$1; s=$((B+$2)); f=$((B+$3)); l=$((B+$4))
printf 'return {fixture_frame=%d, fixture_zone=0x0C00, boss_code=%s, slots=%s, windows={{label="%s",first=%d,last=%d,every=%d}}}\n' $s ${BOSS_CODE:-nil} ${SLOTS:-nil} $name $f $l $5 > $N/plan-$name.lua
rm -rf $N/probe-$name
python3 $R/tools/bizhawk/capture_native_references.py --bizhawk-home /home/farrell/code/projects/OpenGGF/docs/BizHawk-2.11-linux-x64 \
  --rom $R/s3k.gen --rom-sha1 CFBF98C36C776677290A872547AC47C53D2761D6 \
  --movie $R/src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/s3k-sonic-tails-complete-emeralds.bk2 \
  --exporter $R/tools/bizhawk/capture_ddz_route_reference.lua --plan $N/plan-$name.lua \
  --fixture-state $N/pass1/states/$(printf '%07d' $s).State \
  --output $N/probe-$name --require-output observations.csv --require-output done.txt --timeout 900
echo "$name exit=$?"
