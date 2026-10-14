#!/usr/bin/env python3
"""Prove the capture jar was compiled from the committed golf sources (r5, 2026-10-06).

Recompiles examples/putt-putt-paradise/src/main/java with javac --release 21 against the engine
class snapshot (no Maven, no writes into the worktree) and compares every .class entry of
source/putt-putt-paradise.jar byte for byte, plus the packaged manifest. Writes jar-source-check.json.
"""
import hashlib, json, os, subprocess, tempfile, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = Path("/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise")
project = REPO / "examples/putt-putt-paradise"
cp = str(ROOT / "engine-classes") + os.pathsep + (ROOT / "engine-classpath.snapshot.txt").read_text().strip()
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["javac", "--release", "21", "-nowarn", "-cp", cp, "-d", tmp,
                    *map(str, sorted((project / "src/main/java").rglob("*.java")))], check=True, capture_output=True)
    built = {str(p.relative_to(tmp)): p.read_bytes() for p in Path(tmp).rglob("*.class")}
with zipfile.ZipFile(ROOT / "source/putt-putt-paradise.jar") as jar:
    packed = {n: jar.read(n) for n in jar.namelist() if n.endswith(".class")}
    manifest_ok = jar.read("META-INF/openggf-mod.yaml") == (project / "src/main/resources/META-INF/openggf-mod.yaml").read_bytes()
mismatch = sorted(n for n in set(built) | set(packed) if built.get(n) != packed.get(n))
result = {"classes_compared": len(built), "jar_classes": len(packed), "mismatched": mismatch, "manifest_identical": manifest_ok,
          "jar_sha256": hashlib.sha256((ROOT / "source/putt-putt-paradise.jar").read_bytes()).hexdigest(),
          "ok": not mismatch and manifest_ok}
(ROOT / "jar-source-check.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "mismatched"}), "mismatched:", len(mismatch))
