#!/bin/sh
# Purpose: engine footage + engine audio for the S2 Competition highlights reel (one frame per route row).
# Inputs: lead worktree at the PR #273 head; frozen routes. Origin: 2026-11-09 highlights request.
set -e
cd /home/farrell/code/projects/OpenGGF/.worktrees/s2-competition-parity
OUT=${1:-$HOME/Videos/OGGF/s2-competition/highlights/src}
git rev-parse HEAD > $OUT/source-commit.txt
first=clean
for r in ehz-tied-act-wins-special ehz-zone-results cnz1-slot-flip; do
  mkdir -p $OUT/$r
  env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -Dmse=off $first "-Dtest=DebugSonic2CompetitionRouteVideo" \
    -Dopenggf.headless.gl=surfaceless-egl -Ds2video.route=$r -Ds2video.audio=true -Ds2video.out=$OUT/$r test > $OUT/$r/mvn.log 2>&1
  first=
  grep -E "Tests run:.*Fail" $OUT/$r/mvn.log | tail -1
done
