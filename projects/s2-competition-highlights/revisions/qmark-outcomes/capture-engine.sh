#!/bin/sh
# Purpose: engine video + audio of the eight 2P "?" monitor outcome routes for the outcomes reel.
# Inputs: lead worktree at the PR #273 head. Origin: 2026-11-09 user request (see each outcome held).
set -e
cd /home/farrell/code/projects/OpenGGF/.worktrees/s2-competition-parity
OUT=$HOME/Videos/OGGF/s2-competition/qmark/engine
mkdir -p $OUT; git rev-parse HEAD > $OUT/source-commit.txt
for c in sonic-1up tails-1up robotnik super-ring speed-shoes shield invincibility teleport; do
  mkdir -p $OUT/$c
  env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -Dmse=off "-Dtest=DebugSonic2CompetitionRouteVideo" \
    -Dopenggf.headless.gl=surfaceless-egl -Ds2video.route=ehz-qmark-$c -Ds2video.audio=true -Ds2video.out=$OUT/$c test > $OUT/$c/mvn.log 2>&1 || true
  echo "$c $(grep -E 'Tests run:.*Fail' $OUT/$c/mvn.log | tail -1)"
done
