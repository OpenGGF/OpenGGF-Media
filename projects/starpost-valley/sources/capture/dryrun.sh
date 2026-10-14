#!/bin/sh
# Promo dry runs: stills every 30 ticks per segment (purpose: timing the promo's cuts).
W=/home/farrell/code/projects/OpenGGF/.worktrees/ai-starpost-valley
cd "$W" || exit 1
CP="target/test-classes:target/classes:$(cat target/test-classpath.txt)"
for seg in "$@"; do
  end=$(tail -1 /home/farrell/scratch/sv-promo/$seg.txt | cut -d: -f1)
  rm -rf /home/farrell/scratch/sv-promo/dry/$seg
  timeout 1800 java -cp "$CP" com.openggf.mods.code.ExampleModCapture --rom "$W/Sonic and Knuckles & Sonic 3 (W) [!].gen" \
    --mod examples/starpost-valley --out /home/farrell/scratch/sv-promo/dry/$seg --script-file /home/farrell/scratch/sv-promo/$seg.txt \
    --every 30 --ticks $((end + 600)) 2>&1 | grep -E "Validation|Exception" | sed "s/^/$seg: /"
done
