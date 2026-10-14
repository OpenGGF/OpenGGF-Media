#!/usr/bin/env python3
"""Hash manifest of the retained native r5 footage (Opus, 2026-10-06).

The lossless masters are the captures themselves: one 320x224 PNG per 60 Hz row (title-frames/
then frames/) and the row-synchronous 48 kHz 16-bit stereo PCM (title.wav then gameplay.wav).
This writes native-manifest.json: per capture, row counts, the SHA-256 of each WAV and a
SHA-256 over every PNG (sorted name + NUL + bytes + NUL), plus the provenance digests.
Usage: native_manifest.py   (run in the capture revision directory)
"""
import hashlib
import json
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = {}
# Current-source captures only: preserved superseded revisions (_superseded-*) keep their own files.
for cap in sorted(p.parent for p in ROOT.rglob("provenance.json") if not any(part.startswith("_") for part in p.relative_to(ROOT).parts)):
    entry = {"provenance": json.loads((cap / "provenance.json").read_text())}
    for folder in ("title-frames", "frames"):
        d = hashlib.sha256()
        files = sorted((cap / folder).glob("*.png"))
        for f in files:
            d.update(f.name.encode() + b"\0" + f.read_bytes() + b"\0")
        entry[folder] = {"pngs": len(files), "sha256": d.hexdigest()}
    for name in ("title.wav", "gameplay.wav"):
        with wave.open(str(cap / name)) as w:
            entry[name] = {"rows": w.getnframes() // 800, "rate": w.getframerate(), "channels": w.getnchannels(),
                           "sha256": hashlib.sha256((cap / name).read_bytes()).hexdigest()}
    entry["rows_match"] = entry["title-frames"]["pngs"] == entry["title.wav"]["rows"] and \
        entry["frames"]["pngs"] == entry["gameplay.wav"]["rows"]
    out[str(cap.relative_to(ROOT))] = entry
(ROOT / "native-manifest.json").write_text(json.dumps(out, indent=1) + "\n")
print({k: (v["title-frames"]["pngs"], v["frames"]["pngs"], v["rows_match"]) for k, v in out.items()})
