#!/bin/sh
# Usage: run-promo.sh <capture-name> <mode> [mode args after OUT ROOT...]
# Runs the promo capture driver (scripts/driver, compiled into scripts/driver/classes) display-free:
# surfaceless EGL, DISPLAY/WAYLAND_DISPLAY unset, isolated cwd under captures/<name>/cwd.
set -eu
name="$1"; mode="$2"; shift 2
ROOT=/home/farrell/code/projects/OpenGGF/.worktrees/ta-promo-a
P=/home/farrell/Videos/OGGF/ta-promo-a
OUT=$P/captures/$name
rm -rf "$OUT"; mkdir -p "$OUT/cwd"
cd "$OUT/cwd"
unset DISPLAY WAYLAND_DISPLAY LD_LIBRARY_PATH
CP=$(sed -n 's/^-cp "\(.*\)"$/\1/p' "$ROOT/target/racing-server/java-args.txt")
git -C "$ROOT" rev-parse HEAD > "$OUT/source-commit.txt"
git -C "$ROOT" status --short > "$OUT/source-status.txt"
echo "$mode $* classes=${CLASSES:-classes}" > "$OUT/args.txt"
exec java --enable-native-access=ALL-UNNAMED -Xmx3g -Dopenggf.headless.gl=surfaceless-egl \
  -cp "$P/scripts/driver/${CLASSES:-classes}:$CP" openggf.racing.server.tools.PromoCapture "$mode" "$OUT" "$ROOT" "$@" > "$OUT/run.log" 2>&1
