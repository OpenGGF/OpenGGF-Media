#!/usr/bin/env python3
"""Original synthesized "voice" clips for the Motobug in "Day Off" (sp-promo-a, 2026-10-24).

The Motobug speaks in PSG-style square-wave beeps, one syllable per word, timed to the exact
frame its dialogue reveals each word (read from the authored `timeline` JSONL). Each line is
one 48 kHz mono 16-bit WAV under voice/, imported by the screenplay as a VOICE cue. Nothing
here is taken from a ROM or a voice service; it is procedural audio made for this film.

Usage: make_voice.py TIMELINE.jsonl  -> writes voice/*.wav and voice/cues.json
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "voice"
RATE = 48000
FPS = 60

# Pitch contour (Hz) per line, one value per word; the last value repeats if a line is longer.
CONTOURS = {
    "Patrol... turn. Patrol...": [440, 330, 440],
    "...": [300],
    "Thirty-five years of this.": [440, 415, 392, 370, 330],
    "I need a day off.": [330, 370, 392, 440, 523],
    "Day off.": [440, 392],
    "Long drive.": [392, 349],
    "They do now.": [440, 494, 587],
    "Best. Day. Ever.": [523, 659, 784],
    "Patrol... turn.": [440, 330],
    "...Only 364 days to go.": [392, 370, 349, 330, 311, 294],
}


def syllable(freq, length, glide=1.06, duty=0.35, level=0.32):
    n = int(RATE * length)
    t = np.arange(n) / RATE
    # quick upward chirp into the note, then a little vibrato
    f = freq * (1 + (glide - 1) * np.exp(-t / 0.018)) * (1 + 0.006 * np.sin(2 * np.pi * 9 * t))
    phase = np.cumsum(f) / RATE
    wave_ = np.where((phase % 1.0) < duty, 1.0, -1.0)
    env = np.minimum(1.0, t / 0.004) * (0.72 + 0.28 * np.exp(-t / 0.03))
    env *= np.clip((length - t) / 0.02, 0, 1)
    out = wave_ * env * level
    return np.round(out * 15) / 15          # 4-bit level steps, like a PSG attenuator


def words_and_frames(rows, cue_id):
    """Global frame where each word's first grapheme becomes visible."""
    starts, last = [], ""
    for row in rows:
        for pose in row["sample"].get("dialogue", []):
            if pose["cue"]["id"] != cue_id:
                continue
            text = pose["visibleText"]
            if len(text) > len(last):
                for i in range(len(last), len(text)):
                    if text[i] != " " and (i == 0 or text[i - 1] == " "):
                        starts.append((row["frame"], i))
                last = text
    return starts


def main(timeline):
    rows = [json.loads(line) for line in open(timeline)]
    cues = {}
    for row in rows:
        for pose in row["sample"].get("dialogue", []):
            cue = pose["cue"]
            if cue["speakerName"] == "Motobug" and cue["id"] not in cues:
                cues[cue["id"]] = cue
    OUT.mkdir(exist_ok=True)
    manifest = []
    for cue_id, cue in cues.items():
        text = cue["text"]
        words = text.split()
        contour = CONTOURS.get(text, [440])
        starts = words_and_frames(rows, cue_id)
        if not starts:
            continue
        first = starts[0][0]
        total = (starts[-1][0] - first) / FPS + 0.5
        clip = np.zeros(int(RATE * total))
        for k, (frame, index) in enumerate(starts):
            word = text[index:].split(" ")[0].strip(".?!,")
            length = 0.28 if word == "" else min(0.07 + 0.014 * len(word), 0.2)
            freq = contour[min(k, len(contour) - 1)]
            s = syllable(freq, length, glide=0.92 if word == "" else 1.06)
            at = int((frame - first) / FPS * RATE)
            clip[at:at + len(s)] += s[: max(0, len(clip) - at)]
        name = f"{cue_id.replace('.', '-')}.wav"
        with wave.open(str(OUT / name), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
            w.writeframes((np.clip(clip, -1, 1) * 32767).astype(np.int16).tobytes())
        manifest.append(dict(cue=cue_id, text=text, globalFrame=first, asset=f"voice/{name}",
                             words=[f for f, _ in starts]))
        print(name, first, len(starts), "words")
    (OUT / "cues.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
