#!/usr/bin/env python3
"""Assemble the Putt Putt Paradise promo kit (Opus, 2026-10-06, r5).

Writes putt-putt-paradise-promo-kit.zip and SHA256SUMS: the film, its manifests and QA, the
edit/verify/package scripts, the editorial audio render tool, and the capture-side sources and
records (harness source, the SDK-validated mod jar, provenance, inputs, per-row state/events/audio
requests, audio QC). No ROM, no ROM-derived stems, PNG rows or WAVs: those stay in the media
directories, hashed by the capture revision's native-manifest.json.
"""
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHOW = ROOT.parent.parent / "showcase-20261006-opus-final"
FILM = ROOT / "putt-putt-paradise-promo.mp4"

TOP = ["putt-putt-paradise-promo.mp4", "putt-putt-paradise-promo.verify.json", "promo.edl.json", "promo.chapters.csv",
       "promo.audio.json", "promo.cuts.png", "promo.waveform.png", "browser-qa.json", "README.md", "render_promo.py",
       "verify_promo.py", "waveform.py", "package.py", "tools/S2PromoAudioRender.java", "tools/render_stems.sh"]
CAPTURE_TOP = ["README.md", "capture_runs.py", "capture_online.py", "audio_qc.py", "check_jar_source.py", "native_manifest.py", "compare_states.py", "rewind_audio_check.py",
               "source/GolfPromoCapture.java", "source/putt-putt-paradise.jar", "jar-source-check.json",
               "jar-sdk-validate.log", "build-snapshot.json", "state-comparison.json", "state-comparison-vs-f3.json", "state-comparison-vs-82a.json", "native-manifest.json", "capture-runs.log",
               "online/online-timeline.json"]
PER_CAPTURE = ["provenance.json", "events.csv", "title-events.csv", "title-rows.csv", "audio-requests.csv", "input.script",
               "input.bk2", "state.csv", "audio-qc.json", "title.wav.rows.json", "gameplay.wav.rows.json"]


def main():
    files = [(ROOT / name, name) for name in TOP]
    files += [(SHOW / name, "capture/" + name) for name in CAPTURE_TOP]
    for cap in ("ehz1-practice", "ehz2-practice", "local-match", "online/online-host", "online/online-guest"):
        files += [(SHOW / cap / name, f"capture/{cap}/{name}") for name in PER_CAPTURE]
    for cap in ("ehz1-practice", "online/online-host", "online/online-guest"):  # captures with a whole-shot rewind
        files.append((SHOW / cap / "rewind-audio.json", f"capture/{cap}/rewind-audio.json"))
    missing = [str(src) for src, _ in files if not src.exists()]
    if missing:
        raise SystemExit("missing: " + ", ".join(missing))
    sums = [f"{hashlib.sha256(src.read_bytes()).hexdigest()}  {arc}" for src, arc in files]
    (ROOT / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    out = ROOT / "putt-putt-paradise-promo-kit.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in files:
            z.write(src, arc, compress_type=zipfile.ZIP_STORED if arc.endswith((".mp4", ".png", ".jar")) else zipfile.ZIP_DEFLATED)
        z.write(ROOT / "SHA256SUMS", "SHA256SUMS")
    print(out, out.stat().st_size, hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
