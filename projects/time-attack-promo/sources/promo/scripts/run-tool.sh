#!/bin/sh
# Usage: run-tool.sh <capture-name> <racing-server tool> [tool args after OUTPUT ROOT...]
# Runs a racing-server capture tool display-free (surfaceless EGL, no X11/Wayland) in an
# isolated working directory under captures/<name>, against the ta-promo-a worktree.
set -eu
name="$1"; tool="$2"; shift 2
ROOT=/home/farrell/code/projects/OpenGGF/.worktrees/ta-promo-a
OUT=/home/farrell/Videos/OGGF/ta-promo-a/captures/$name
mkdir -p "$OUT/cwd"
cd "$OUT/cwd"
unset DISPLAY WAYLAND_DISPLAY LD_LIBRARY_PATH
export JAVA_TOOL_OPTIONS="-Dopenggf.headless.gl=surfaceless-egl -Xmx3g"
git -C "$ROOT" rev-parse HEAD > "$OUT/source-commit.txt"
git -C "$ROOT" diff > "$OUT/fixture.patch"
exec "$ROOT/target/racing-server/racing-server" "$tool" "$OUT" "$ROOT" "$@" > "$OUT/run.log" 2>&1
