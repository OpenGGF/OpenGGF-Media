#!/usr/bin/env python3
"""Run the Opus polish-round captures with synchronized game audio (2026-10-06).

Purpose: reproducible capture of the final Putt Putt Paradise build: EHZ1 Sonic practice
(with a whole-shot rewind), EHZ2 Tails practice, a full local two-player match, and a real
two-JVM online session. Inputs: the worktree (compiled target/classes, validated jar), the
user's Sonic 2 REV01 ROM (absolute path, never copied). Writes provenance.json beside each
capture with ROM/jar/engine-source digests, the baseline commit and the working-diff digest.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise")
ROM = Path("/home/farrell/code/projects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen")
JAR = ROOT / "source" / "putt-putt-paradise.jar"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def engine_source_sha():
    digest = hashlib.sha256()
    for source in sorted((REPO / "src/main/java").rglob("*.java")):
        digest.update(str(source.relative_to(REPO)).encode() + b"\0" + source.read_bytes() + b"\0")
    return digest.hexdigest()


def mod_source_sha():
    digest = hashlib.sha256()
    project = REPO / "examples/putt-putt-paradise"
    for source in sorted(list(project.rglob("*.java")) + [project / "src/main/resources/META-INF/openggf-mod.yaml"]):
        digest.update(str(source.relative_to(REPO)).encode() + b"\0" + source.read_bytes() + b"\0")
    return digest.hexdigest()


def main():
    classpath = str(REPO / "target/classes") + os.pathsep + (REPO / "target/putt-putt-paradise/engine-classpath.txt").read_text().strip()
    (ROOT / "engine-classpath.txt").write_text(classpath)
    classes = ROOT / "classes"
    subprocess.run(["javac", "--release", "21", "-nowarn", "-cp", classpath, "-d", str(classes),
                    str(ROOT / "source/GolfPromoCapture.java")], check=True)
    git = lambda *args: subprocess.check_output(["git", *args], cwd=REPO)
    meta = {
        "rom_sha1": hashlib.sha1(ROM.read_bytes()).hexdigest(), "mod_jar_sha256": sha256(JAR),
        "mod_source_sha256": mod_source_sha(), "engine_java_sha256": engine_source_sha(),
        "baseline": git("rev-parse", "HEAD").decode().strip(),
        "working_diff_sha256": hashlib.sha256(git("diff", "HEAD")).hexdigest(),
        "native_hz": 60, "png_fps": 60, "dimensions": [320, 224], "viewport": "NATIVE_4_3",
        "audio": "real HeadlessSmpsAudioBackend; one Engine.presentOuterAudioFrame + one LiveCaptureAudioHandle drain per row",
        "audio_format": "48 kHz 16-bit stereo PCM, 800 frames per 60 Hz row",
        "rewind_vhs_effect": True, "rewind_vhs_tear_bands": True,
        "entry": "explicit SDK-validated ModContext capture wrapper (source/GolfPromoCapture.java)",
    }
    wanted = sys.argv[1:] or ["ehz1-practice", "ehz2-practice", "local-match", "online"]
    for scenario in wanted:
        out = ROOT / scenario
        if scenario == "online":
            subprocess.run([sys.executable, str(ROOT / "capture_online.py"), "--rom", str(ROM), "--jar", str(JAR),
                            "--classes", str(classes), "--classpath", classpath, "--out", str(out), "--repo", str(REPO)], check=True)
            for role in ("online-host", "online-guest"):
                (out / role / "provenance.json").write_text(json.dumps({**meta, "scenario": role,
                        "transport": "real direct TCP room on 127.0.0.1:20502 between two JVMs"}, indent=2) + "\n")
            continue
        out.mkdir()
        (out / "provenance.json").write_text(json.dumps({**meta, "scenario": scenario}, indent=2) + "\n")
        with (out / "capture.log").open("w") as log:
            subprocess.run(["java", "-cp", str(classes) + os.pathsep + classpath, "com.openggf.mods.code.GolfPromoCapture",
                            str(ROM), str(JAR), str(out), scenario, "1"], stdout=log, stderr=subprocess.STDOUT, check=True, cwd=REPO)
        print("Captured", scenario, flush=True)


if __name__ == "__main__":
    main()
