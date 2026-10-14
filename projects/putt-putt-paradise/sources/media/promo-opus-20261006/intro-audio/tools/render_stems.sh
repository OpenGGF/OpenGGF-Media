#!/bin/sh
# Render the Sonic 2 soundtrack stems for the Putt Putt Paradise intro-audio promo.
# Purpose: compile tools/S2PromoAudioRender.java OUTSIDE the repository against an OpenGGF build's
# target/classes and render music/SFX from a user-supplied Sonic 2 REV01 ROM through OpenGGF's SMPS
# driver. Inputs: OPENGGF (worktree with target/classes, default below), S2ROM (ROM path).
# Output: ../audio/s2-*.wav (48 kHz 16-bit stereo). Originating task: 2026-10-06 promo intro-audio lane,
# OpenGGF b2faa748f + working follow-up (feature/ai-putt-putt-paradise).
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
OPENGGF=${OPENGGF:-/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise}
S2ROM=${S2ROM:-"/home/farrell/code/projects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen"}
echo "8bca5dcef1af3e00098666fd892dc1c2a76333f9  $S2ROM" | sha1sum -c -
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT
javac -cp "$OPENGGF/target/classes" -d "$BUILD" "$HERE/S2PromoAudioRender.java"
# 0x96 Title Screen, 0x81 Emerald Hill, 0x97 Stage Clear, 0x89 Option Screen; SFX 0xBC Spindash Release, 0xB5 Ring
java -cp "$OPENGGF/target/classes:$BUILD" S2PromoAudioRender --rom "$S2ROM" --out "$HERE/../audio" --rate 48000 \
    music:96:20 music:81:120 music:97:15 music:89:60 sfx:BC sfx:B5 2>&1 | grep -v -e '^INFO' -e '^[A-Z][a-z][a-z] [0-9]'
