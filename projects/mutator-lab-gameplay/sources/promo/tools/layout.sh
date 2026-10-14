#!/bin/sh
# Display-free maintained layout dump: layout.sh game zone act
set -eu
[ "$#" -eq 3 ] || { echo 'Usage: layout.sh game zone act' >&2; exit 2; }
O=/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3
W=${OPENGGF_PROMO_ENGINE_ROOT:-/home/farrell/code/projects/OpenGGF/.worktrees/ai-mutators-prototype}
case $1 in s1) R="Sonic The Hedgehog (W) (REV01) [!].gen";; s2) R="Sonic The Hedgehog 2 (W) (REV01) [!].gen";; s3k) R="Sonic and Knuckles & Sonic 3 (W) [!].gen";; *) echo 'Unknown game' >&2; exit 2;; esac
D=$O/layouts/$1-$2$3-maintained
[ ! -e "$D" ] || { echo 'Refusing existing output' >&2; exit 2; }
mkdir -p "$D/user"
cd "$D/user"
env -u DISPLAY -u WAYLAND_DISPLAY -u XDG_SESSION_TYPE -u LD_LIBRARY_PATH -u EGL_PLATFORM ALSOFT_DRIVERS=null \
  timeout 120 /usr/lib/jvm/java-21-openjdk/bin/java -Djava.awt.headless=true -Dopenggf.headless.gl=surfaceless-egl \
  "-Dorg.lwjgl.system.SharedLibraryExtractPath=$W/target/test-tmp/promo-lwjgl" "-Duser.dir=$D/user" "-Dopenggf.saveRoot=$D/user/saves" \
  -cp "$W/target/classes:$(cat "$W/target/mutators-classpath.txt")" com.openggf.tools.LevelLayoutDumpTool "$1" "/home/farrell/code/projects/OpenGGF/$R" "$2" "$3" "$D/data" > "$D/probe.log" 2>&1
wc -l "$D/data/rings.csv" "$D/data/objects.csv"
