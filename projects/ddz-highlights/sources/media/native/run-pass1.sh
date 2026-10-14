#!/bin/sh
python3 /home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-bring-up/tools/bizhawk/capture_native_references.py --bizhawk-home /home/farrell/code/projects/OpenGGF/docs/BizHawk-2.11-linux-x64 \
  --rom /home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-bring-up/s3k.gen --rom-sha1 CFBF98C36C776677290A872547AC47C53D2761D6 \
  --movie /home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-bring-up/src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/s3k-sonic-tails-complete-emeralds.bk2 \
  --exporter /home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-bring-up/tools/bizhawk/capture_ddz_route_reference.lua --plan /home/farrell/Videos/OGGF/ddz-bring-up/native/plan-pass1.lua \
  --output /home/farrell/Videos/OGGF/ddz-bring-up/native/pass1 --require-output observations.csv --require-output done.txt --timeout 1800
echo "pass1 exit=$?"
