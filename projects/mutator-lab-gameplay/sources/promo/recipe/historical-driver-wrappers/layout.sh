#!/bin/sh
# Display-free layout dump: layout.sh game zone act
O=/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3
W=/home/farrell/code/projects/OpenGGF/.worktrees/ai-mutators-gameplay-promo
case $1 in s1) R="Sonic The Hedgehog (W) (REV01) [!].gen";; s2) R="Sonic The Hedgehog 2 (W) (REV01) [!].gen";; *) R="Sonic and Knuckles & Sonic 3 (W) [!].gen";; esac
D=$O/layouts/$1-$2$3; mkdir -p $D/user
cd $D/user && env -u DISPLAY -u WAYLAND_DISPLAY -u XDG_SESSION_TYPE -u LD_LIBRARY_PATH -u EGL_PLATFORM ALSOFT_DRIVERS=null \
  timeout 120 /usr/lib/jvm/java-21-openjdk/bin/java -Djava.awt.headless=true -Dopenggf.headless.gl=surfaceless-egl \
  -Dorg.lwjgl.system.SharedLibraryExtractPath=$W/target/test-tmp/promo-lwjgl -Duser.dir=$D/user -Dopenggf.saveRoot=$D/user/saves \
  -cp "$O/tools/driver/classes:$W/target/classes:$(cat $W/target/mutators-classpath.txt | tr -d '\n')" promo.LayoutProbe $1 "/home/farrell/code/projects/OpenGGF/$R" $2 $3 $D > $D/probe.log 2>&1
echo "$1 $2 $3 exit $? rings=$(($(wc -l < $D/rings.csv)-1)) objects=$(($(wc -l < $D/objects.csv)-1))"
