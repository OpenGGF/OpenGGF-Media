#!/usr/bin/env python3
"""Run the final Opus promo captures with synchronized game audio (2026-10-06, revision r5).

Purpose: reproducible capture of the final Putt Putt Paradise build: EHZ1 Sonic practice
(with a whole-shot rewind), EHZ2 Tails practice, a full local two-player match, and a real
two-JVM online session. Inputs: the worktree (compiled target/classes, validated jar), the
user's Sonic 2 REV01 ROM (absolute path, never copied). Writes provenance.json beside each
capture with ROM/jar/engine-source digests, the baseline commit and the working-diff digest.
r5 (showcase-20261006-opus-final) recaptures every scenario after the course-entry music fix
(CourseControl.restore / ControlledFrameRuntime held-row Level_PlayBgm service). It refuses to run
if the jar differs from the freshly built one, or if any engine source is newer than its class,
and re-checks the source digests after the last capture so footage cannot outlive its code.
Title rows run the production TITLE_SCREEN mode through GameLoop.step, and START takes the
engine's own route (fade, Sonic 2 title card, fresh course load); the boot level's armed
Level_PlayBgm countdown is drained before recording (see GolfPromoCapture.main).
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


def golf_main_java_sha():
    """The parent's recorded recipe: examples/putt-putt-paradise/src/main/java only."""
    digest = hashlib.sha256()
    for source in sorted((REPO / "examples/putt-putt-paradise/src/main/java").rglob("*.java")):
        digest.update(str(source.relative_to(REPO)).encode() + b"\0" + source.read_bytes() + b"\0")
    return digest.hexdigest()


def tree_sha(root):
    digest = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(f.relative_to(root)).encode() + b"\0" + f.read_bytes() + b"\0")
    return digest.hexdigest()


def mod_source_sha():
    digest = hashlib.sha256()
    project = REPO / "examples/putt-putt-paradise"
    for source in sorted(list(project.rglob("*.java")) + [project / "src/main/resources/META-INF/openggf-mod.yaml"]):
        digest.update(str(source.relative_to(REPO)).encode() + b"\0" + source.read_bytes() + b"\0")
    return digest.hexdigest()


def assert_fresh():
    """The build is bound by build-snapshot.json (written when target/classes was copied, with zero
    stale classes): the current sources, the class snapshot and the jar must still match it, and
    jar-source-check.json must prove the jar is a fresh javac of these golf sources."""
    snap = json.loads((ROOT / "build-snapshot.json").read_text())
    checks = {"engine_java_sha256": engine_source_sha(), "golf_main_java_sha256": golf_main_java_sha(),
              "engine_classes_tree_sha256": tree_sha(ROOT / "engine-classes"), "jar_sha256": sha256(JAR),
              "engine_classpath_sha256": sha256(ROOT / "engine-classpath.snapshot.txt")}
    bad = {k: v for k, v in checks.items() if snap[k] != v}
    if bad:
        raise SystemExit(f"Build snapshot no longer matches: {bad}")
    if not json.loads((ROOT / "jar-source-check.json").read_text())["ok"]:
        raise SystemExit("jar-source-check.json does not prove the jar")


def main():
    assert_fresh()
    # A snapshot of target/classes (copied once, after the build) so a concurrent Maven run in the
    # worktree cannot rewrite classes under a capture JVM; its digest is recorded below.
    snapshot = ROOT / "engine-classes"
    classpath = str(snapshot) + os.pathsep + (ROOT / "engine-classpath.snapshot.txt").read_text().strip()
    (ROOT / "engine-classpath.txt").write_text(classpath)
    classes = ROOT / "classes"
    subprocess.run(["javac", "--release", "21", "-nowarn", "-cp", classpath, "-d", str(classes),
                    str(ROOT / "source/GolfPromoCapture.java")], check=True)
    git = lambda *args: subprocess.check_output(["git", *args], cwd=REPO)
    meta = {
        "rom_sha1": hashlib.sha1(ROM.read_bytes()).hexdigest(), "mod_jar_sha256": sha256(JAR),
        "mod_source_sha256": mod_source_sha(), "engine_java_sha256": engine_source_sha(),
        "golf_main_java_sha256": golf_main_java_sha(), "engine_classes_snapshot_sha256": tree_sha(snapshot),
        "jar_source_check": json.loads((ROOT / "jar-source-check.json").read_text()),
        "title_path": "production GameLoop TITLE_SCREEN -> fade -> TITLE_CARD -> LEVEL (capture.title=loop)",
        "baseline": git("rev-parse", "HEAD").decode().strip(),
        "integration_base": "f4b40f5026988c5152eb2ae1fadaaf7c648f5618",  # develop (with Slay PR211) merged into the PR branch
        "build_snapshot": json.loads((ROOT / "build-snapshot.json").read_text()),
        "working_diff_sha256": hashlib.sha256(git("diff", "HEAD")).hexdigest(),
        "untracked": git("ls-files", "--others", "--exclude-standard").decode().split(),
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
    after = {"mod_source_sha256": mod_source_sha(), "engine_java_sha256": engine_source_sha(), "mod_jar_sha256": sha256(JAR),
             "golf_main_java_sha256": golf_main_java_sha(),
             "engine_classes_snapshot_sha256": tree_sha(ROOT / "engine-classes")}
    if any(after[k] != meta[k] for k in after):
        raise SystemExit(f"Sources changed during capture: {after} vs {meta}")
    print("Source digests unchanged across the captures", flush=True)


if __name__ == "__main__":
    main()
