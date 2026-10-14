#!/bin/sh
# Rebuild the first Typing of the Hedgehog promo (2026-10-10) from its task-owned sources.
# --capture: build in the assigned promo worktree, re-record production gameplay and hub.
# --from-captures (default): retain recordings and ROM glyphs; regenerate cards and final edit.
# Inputs: own ROMs at the existing root paths; no ROM copying/linking/build recipe.
# Outputs: promo/caps, glyphs, cards, work, and out. Nothing is written to repository media.
set -eu
P=/home/farrell/scratch/typing-hedgehog/promo
W=/home/farrell/code/projects/OpenGGF/.worktrees/ai-typing-hedgehog-promo
PYTHON=${PROMO_PYTHON:-$P/.venv/bin/python}
if [ ! -x "$PYTHON" ]; then
 python3 -m venv --system-site-packages "$P/.venv"
 "$P/.venv/bin/pip" install -r "$P/requirements.txt"
fi
case ${1:---from-captures} in
 --capture)
   cd "$W"
   mvn -Dmse=off compile test-compile
   python3 examples/build_example.py typing-of-the-hedgehog --skip-engine
   "$P/capture.sh" all
   CP="$W/target/test-classes:$W/target/classes:$(cat "$W/target/examples-classpath.txt")"
   mkdir -p "$P/classes" "$P/glyphs" "$P/assets"
   javac --release 21 -cp "$CP" -d "$P/classes" "$P"/fontsrc/flappytails/*.java
   java -cp "$P/classes:$CP" flappytails.PromoGlyphs /home/farrell/code/projects/OpenGGF/s3k.gen "$P/glyphs"
   cp "$W/examples/typing-of-the-hedgehog/src/main/resources/art/plate-font.txt" "$P/assets/plate-font.txt"
   cp "$W/examples/typing-of-the-hedgehog/src/main/resources/audio/voice/announcer_type_to_survive.ogg" "$P/assets/announcer_type_to_survive.ogg"
   ;;
 --from-captures) ;;
 *) echo 'use --capture or --from-captures' >&2; exit 2 ;;
esac
mkdir -p "$P/backgrounds"
ffmpeg -nostdin -loglevel error -y -ss 10 -i "$P/caps/ghz/capture.mp4" -vf scale=400:224:flags=neighbor -frames:v 1 "$P/backgrounds/ghz.png"
ffmpeg -nostdin -loglevel error -y -ss 24 -i "$P/caps/ehz/capture.mp4" -vf scale=400:224:flags=neighbor -frames:v 1 "$P/backgrounds/ehz.png"
ffmpeg -nostdin -loglevel error -y -ss 2 -i "$P/caps/ehz/capture.mp4" -vf scale=400:224:flags=neighbor -frames:v 1 "$P/backgrounds/probe.png"
"$PYTHON" "$P/make_cards.py"
"$PYTHON" "$P/make_promo.py"
"$PYTHON" "$P/verify_promo.py"
