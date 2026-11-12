#!/usr/bin/env bash
# Purpose: the whole final run of the pacing revision, once the last art commit exists: capture every take once
#   (film takes and the 1.0 release-promo clips, SFX-only audio), check them, render and master both cuts, and
#   write the usage, shot index, verification and contact sheets. The archive is a separate step (tools/archive.py).
# Before this: merge the integration commit into the local build branch, clean-build, rebuild the mod jar and
#   recompile hosts/ (README "Rebuild"). JVM captures run one at a time.
# Usage: tools/final_run.sh <integration sha> [develop sha] [stage]   (stage: capture | render | reports | all)
# Origin: MICA & TALON promo redo, stage B, 2026-11-12.
set -euo pipefail
T="$(cd "$(dirname "$0")/.." && pwd)"
R="${MT_CHECKOUT:-/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f}"
MOD="$1"; DEV="${2:-4f885afbd6}"; STAGE="${3:-all}"
PY="$HOME/scratch/agent-tmp/mt-promo-20261110/venv/bin/python"
KIT="$R/tools/media/promo_kit.py"
export PROMO_FONT_DIRS="$HOME/scratch/agent-tmp/mt-promo-20261110/final/fonts" MT_CAPTURES=captures
cd "$T"
if [[ "$STAGE" == capture || "$STAGE" == all ]]; then
  # the delivered cut's takes (old art, silent) keep their files under another name; nothing is deleted
  if [[ -d captures && ! -d captures-old-art-1e0faac123 ]]; then mv captures captures-old-art-1e0faac123; fi
  python3 tools/final_shots.py
  python3 tools/capture.py --checkout "$R" --shots shots-b/final.json shots-b/promo10.json --dest captures \
      --mod-commit "$MOD" --develop-commit "$DEV" > logs/final-capture.log 2>&1
  grep -c '^DONE' logs/final-capture.log; grep FAILED logs/final-capture.log && exit 1
  python3 tools/takes_check.py captures --json out/takes-check.json | tail -4
  python3 tools/takes_check.py captures | grep -q 'problems 0'
fi
if [[ "$STAGE" == render || "$STAGE" == all ]]; then
  "$PY" tools/chapters.py > /dev/null
  "$PY" "$KIT" render edit/edit.py > logs/final-render-h.log 2>&1
  "$PY" tools/finish.py work/build-h out/master-16x9.mp4 work/chapters.ffmeta | head -1
  MT_VERTICAL=1 "$PY" "$KIT" render edit/edit.py > logs/final-render-v.log 2>&1
  "$PY" tools/finish.py work/build-v out/master-9x16.mp4 work/chapters.ffmeta | head -1
  rm -f out/kit-16x9.mp4 out/kit-9x16.mp4
fi
if [[ "$STAGE" == reports || "$STAGE" == all ]]; then
  "$PY" tools/usage.py out/usage-16x9.json | tail -1
  MT_VERTICAL=1 "$PY" tools/usage.py out/usage-9x16.json | tail -1
  "$PY" tools/shot_index.py
  "$PY" tools/verify.py | tail -8
  "$PY" tools/onscreen.py > out/onscreen.txt
  "$PY" tools/contact.py out/master-16x9.mp4 out/contact-16x9-2s.jpg 2 8 400
  "$PY" tools/contact.py out/master-9x16.mp4 out/contact-9x16-2s.jpg 2 16 200
fi
