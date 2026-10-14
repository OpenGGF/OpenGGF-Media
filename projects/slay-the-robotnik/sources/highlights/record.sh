#!/bin/bash
# Records every reel clip from scripts/*.txt with ExampleModCapture: 800x448 at 60 fps,
# with the scene's audio from the engine's SMPS driver. Usage: record.sh [clip.txt ...]
# Classpath: the str-slots integration build (same tree as feature/ai-slay-the-robotnik 8521b9d65).
R=~/Videos/OGGF/slay-the-robotnik-reel
W=/home/farrell/code/projects/OpenGGF/.worktrees/str-slots
cd $W || exit 1
CP="/tmp/str-ov/test:/tmp/str-ov/main:$W/target/classes:$(cat $W/target/test-classpath.txt)"
cd $R/scripts
files=("$@"); [ ${#files[@]} -eq 0 ] && files=(*.txt)
for f in "${files[@]}"; do
  n=$(basename $f .txt)
  jump=$(grep -m1 "^# jump:" $f | sed 's/^# jump: *//')
  ticks=$(grep -m1 "^# ticks:" $f | sed 's/^# ticks: *//')
  args=(--rom "$W/s3k.gen" --mod "$W/examples/slay-the-robotnik" --out /tmp/str-rec-$n --script-file "$R/scripts/$f" --every 0
        --video "$R/clips/$n.mp4" --audio "$R/clips/$n.wav")
  [ -n "$jump" ] && args+=(--jump "$jump")
  [ -n "$ticks" ] && args+=(--ticks "$ticks")
  rm -rf /tmp/str-rec-$n
  (cd $W && java -cp "$CP" com.openggf.mods.code.ExampleModCapture "${args[@]}") > /tmp/str-rec-$n.log 2>&1
  echo "$n: $(grep -E 'Audio:|Video:|Exception' /tmp/str-rec-$n.log | tr '\n' ' ')"
done
