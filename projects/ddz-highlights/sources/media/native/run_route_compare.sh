#!/bin/sh
# Engine cold DDZ route (zone0c movie input) vs the native trace positions. Usage: run_route_compare.sh <outdir> [every]
R=/home/farrell/code/projects/OpenGGF/.worktrees/ai-ddz-bring-up
BK=$R/src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/s3k-sonic-tails-complete-emeralds.bk2
OUT=$1; EVERY=${2:-50}
rm -rf $OUT
cd $R && python3 tools/testing/maven_queue.py -Dmse=off -q compile exec:java "-Dexec.mainClass=com.openggf.tools.GameplayCaptureTool" "-Dexec.args=--game s3k --rom $R/s3k.gen --zone ddz --act 1 --sidekick tails --emeralds 3333333 --input $BK --input-start 514213 --frames 10100 --every $EVERY --no-video --out-dir $OUT" 2>&1 | grep -E '^Captured|^Stop|Exception'
python3 /home/farrell/Videos/OGGF/ddz-bring-up/native/compare_trace.py $OUT/state.csv $R/src/test/resources/traces/s3k/runs/s3k-sonic-tails-complete-emeralds/zone0c/physics.csv.gz 8
