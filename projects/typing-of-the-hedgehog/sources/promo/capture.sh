#!/bin/sh
# First Typing of the Hedgehog promo, 2026-10-10. Task media stays outside the repo.
# Inputs: promo worktree at 9fee32aad, own s1/s2/s3k ROMs, packaged example mod.
# Output: every-tick 400x224 gameplay scaled 5x, synchronous 48 kHz engine audio,
# state.csv and clock.json. Hub scenes use ExampleModCapture --scale 5 --every 0.
set -eu
P=/home/farrell/scratch/typing-hedgehog/promo
W=/home/farrell/code/projects/OpenGGF/.worktrees/ai-typing-hedgehog-promo
R=/home/farrell/code/projects/OpenGGF
cd "$W"
CP="$W/target/test-classes:$W/target/classes:$(cat "$W/target/examples-classpath.txt")"
mkdir -p "$P/classes" "$P/caps"
if [ "${PROMO_PREPARED:-0}" != 1 ]; then
 javac --release 21 -cp "$CP" -d "$P/classes" "$P/PromoCourseCapture.java"
fi
course() {
 name=$1 game=$2 zi=$3 ai=$4 mode=$5 ticks=$6
 O="$P/caps/$name"
 mkdir -p "$O/saves/mods/typing-of-the-hedgehog"
 printf 'mode=%s\ngame=%s\nzone=%s\nact=%s\ndifficulty=NORMAL\ncapitals=false\npunctuation=false\ndictionaries=standard\nseed=7\nbossStars=1\nnoFail=true\nslowMotion=false\nvoice=CLEAN\ndemo=true\ndemoRows=0\n' "$mode" "$game" "$zi" "$ai" > "$O/saves/mods/typing-of-the-hedgehog/intent.txt"
 java -Xmx2g -Dopenggf.saveRoot="$O/saves" -cp "$P/classes:$CP" PromoCourseCapture "$R/$game.gen" "$W/target/examples/typing-of-the-hedgehog/typing-of-the-hedgehog.jar" "$zi" "$ai" "$ticks" "$O" > "$O/capture.log" 2>&1
}
hub() {
 name=$1 game=$2 ticks=$3 script=$4
 O="$P/caps/$name"; mkdir -p "$O"
 java -Xmx2g -cp "$CP" com.openggf.mods.code.ExampleModCapture --rom "$R/$game.gen" --mod examples/typing-of-the-hedgehog --out "$O" --width 400 --height 224 --scale 5 --every 0 --ticks "$ticks" --script-file "$script" --audio "$O/audio.wav" --video "$O/capture.mp4" > "$O/capture.log" 2>&1
}
case ${1:-all} in
 probe) course probe s2 0 1 ARCADE 360 ;;
 ghz) course ghz s1 0 2 ARCADE 16000 ;;
 ehz) course ehz s2 0 1 ARCADE 16000 ;;
 fz) course fz s1 6 0 ARCADE 4800 ;;
 dez) course dez s2 10 0 ARCADE 7200 ;;
 hub) hub hub s3k 2700 "$P/hub-script.txt" ;;
 all) export PROMO_PREPARED=1; "$0" ghz & a=$!; "$0" ehz & b=$!; wait "$a"; wait "$b"; "$0" fz & a=$!; "$0" dez & b=$!; wait "$a"; wait "$b"; "$0" hub ;;
 *) echo "unknown capture $1" >&2; exit 2 ;;
esac
