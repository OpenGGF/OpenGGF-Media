#!/bin/sh
# Purpose: focused route checks on the PR head, then reel v2 captures (engine video + audio) of the
# simultaneous tie route and the CNZ slot route. Origin: 2026-11-09 reel v2 for James.
set -e
cd /home/farrell/code/projects/OpenGGF/.worktrees/s2-competition-parity
OUT=$HOME/Videos/OGGF/s2-competition/highlights/cap2
git rev-parse HEAD > $OUT/source-commit.txt
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -Dmse=off clean \
  "-Dtest=TestCommittedRoutesQualifiedGuard,TestStageplayCompetitionSpiralJump,TestStageplayCompetitionEhzFrozenRoutes,TestCompetitionRouteConversion" \
  -Dopenggf.headless.gl=surfaceless-egl test > $OUT/focused.log 2>&1 || true
grep -E "Tests run:|FAIL" $OUT/focused.log | tail -6
for r in ehz-simultaneous-tie-special cnz1-slot-flip; do
  mkdir -p $OUT/$r
  env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -Dmse=off "-Dtest=DebugSonic2CompetitionRouteVideo" \
    -Dopenggf.headless.gl=surfaceless-egl -Ds2video.route=$r -Ds2video.audio=true -Ds2video.out=$OUT/$r test > $OUT/$r/mvn.log 2>&1 || true
  grep -E "Tests run:.*Fail" $OUT/$r/mvn.log | tail -1
done
