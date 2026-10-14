#!/bin/sh
# Promo captures for Flappy Tails (task tool). Runtime classes come from a snapshot so a
# concurrent Maven run in the worktree cannot race them.
set -e
W=/home/farrell/code/projects/OpenGGF/.worktrees/ai-flappy-tails
S=/home/farrell/scratch/flappy-tails-20261008/runtime
C=/home/farrell/scratch/flappy-tails-20261008/promo/caps
CP="$S/test-classes:$S/classes:$(cat $S/test-classpath.txt)"
cd "$W"
cap() {
  name=$1; ticks=$2; script=$3
  rm -rf "$C/$name"; mkdir -p "$C/$name"
  echo "== $name $(date +%T)"
  java -cp "$CP" com.openggf.mods.code.ExampleModCapture --rom "$W/s3k.gen" --mod examples/flappy-tails \
    --out "$C/$name" --scale 5 --every 0 --ticks "$ticks" --script "$script" \
    --audio "$C/$name/$name.wav" --video "$C/$name/$name.mp4" 2>&1 | grep -E "Capture|Video|Exception|Error" || true
}
cap title 720 ""
cap tour 6700 "1:jump=seed:0x5eed 2:jump=autopilot:on 3:jump=play:classic"
cap rings 1150 "1:jump=seed:0x5eed 2:jump=autopilot:on 3:jump=play:sonic 700:jump=rings:40 760:jump=autopilot:off 840:jump=autopilot:on"
cap crash 3150 "1:jump=seed:0x5eed 2:jump=autopilot:on 3:jump=play:classic 2520:jump=autopilot:off"
echo "== done $(date +%T)"
