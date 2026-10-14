#!/usr/bin/env python3
"""Records promo clips with ExampleModCapture: every tick as a lossless 400x224 PNG (scale 1)
plus the scene's audio. Slay the Robotnik runs with its own "no music" setting seeded (see
prepare_mods), so clip audio is sound effects only and the soundtrack is laid separately.

Script headers: '# jump: cmd', '# ticks: n', '# mod: <examples dir name>' (default slay-the-robotnik).
Usage: record.py [scripts/pNN-*.txt ...]   (default: every script; 3 at a time)
"""
import re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WT = Path("/home/farrell/code/projects/OpenGGF/.worktrees/ai-slay-the-robotnik")
CP = f"{WT}/target/test-classes:{WT}/target/classes:" + (WT / "target/slay-test-classpath.txt").read_text().strip()

def prepare_mods():
    """Copies of the example mods for recording stems: Slay the Robotnik's "no music" setting
    also stops whatever is already playing (the harness boots a level whose music would otherwise
    continue underneath), and hello-scene stops music instead of starting it. Nothing visual
    changes; the soundtrack is laid separately by promo.py."""
    dst = ROOT / "build/mods"
    shutil.rmtree(dst, ignore_errors=True)
    for name in ("slay-the-robotnik", "hello-scene"):
        shutil.copytree(WT / "examples" / name / "src", dst / name / "src")
    shell = dst / "slay-the-robotnik/src/main/java/slaytherobotnik/scene/Shell.java"
    old = "            currentMusic = id;\n            return;"
    text = shell.read_text()
    assert old in text
    shell.write_text(text.replace(old, "            currentMusic = id;\n            ctx.audio().stopMusic();\n            return;", 1))
    # The debug jump always starts a room at floor 0 of the earliest act it can appear in, so
    # every event would stand at the start of Angel Island. "...@act:actFloor:nodeX" places the
    # room that far into an act instead (only acts the room may really appear in are used).
    scene = dst / "slay-the-robotnik/src/main/java/slaytherobotnik/scene/SlayScene.java"
    text = scene.read_text()
    head = "    public boolean debugJump(String command) {\n"
    assert head in text and "        shell.goNow(new RunScreen());\n        return true;\n" in text
    text = text.replace(head, head + """        int[] promoAt = null;
        int promoSplit = command.indexOf('@');
        if (promoSplit > 0) {
            String[] at = command.substring(promoSplit + 1).split(":");
            promoAt = new int[] {Integer.parseInt(at[0]), Integer.parseInt(at[1]), Integer.parseInt(at[2])};
            command = command.substring(0, promoSplit);
        }
""", 1)
    text = text.replace("        shell.goNow(new RunScreen());\n        return true;\n", """        if (promoAt != null) {
            run.state().setPosition(promoAt[0], (promoAt[0] - 1) * 16 + promoAt[1], promoAt[1], promoAt[2]);
        }
        shell.goNow(new RunScreen());
        return true;
""", 1)
    scene.write_text(text)
    hello = dst / "hello-scene/src/main/java/hello/HelloScene.java"
    text = hello.read_text()
    assert "ctx.audio().playMusic(MUSIC_AIZ1);" in text
    hello.write_text(text.replace("ctx.audio().playMusic(MUSIC_AIZ1);", "ctx.audio().stopMusic();"))


def header(text, key):
    m = re.search(rf"^# {key}: *(.*)$", text, re.M)
    return m.group(1).strip() if m else ""

def record(script):
    name = script.stem
    text = script.read_text()
    mod = header(text, "mod") or "slay-the-robotnik"
    out = ROOT / "build/frames" / name
    shutil.rmtree(out, ignore_errors=True)
    prof = out / "saves/mods/slay-the-robotnik"
    prof.mkdir(parents=True)
    (prof / "profile.properties").write_text("setting.nomusic=1\n")
    args = ["java", "-cp", CP, "com.openggf.mods.code.ExampleModCapture", "--rom", str(WT / "s3k.gen"),
            "--mod", str(ROOT / "build/mods" / mod), "--out", str(out), "--script-file", str(script),
            "--every", "1", "--scale", "1", "--audio", str(ROOT / "clips" / f"{name}.wav")]
    if header(text, "jump"):
        args += ["--jump", header(text, "jump")]
    if header(text, "ticks"):
        args += ["--ticks", header(text, "ticks")]
    log = ROOT / "build" / f"{name}.log"
    with open(log, "w") as f:
        r = subprocess.run(args, cwd=WT, stdout=f, stderr=subprocess.STDOUT)
    frames = len(list(out.glob("frame-*.png")))
    errors = [l for l in log.read_text().splitlines() if "Exception" in l or "SEVERE" in l][:2]
    return f"{name}: exit {r.returncode}, {frames} frames {' | '.join(errors)}"

if __name__ == "__main__":
    scripts = [Path(a).resolve() for a in sys.argv[1:]] or sorted((ROOT / "scripts").glob("p*.txt"))
    (ROOT / "build/frames").mkdir(parents=True, exist_ok=True)
    (ROOT / "clips").mkdir(exist_ok=True)
    prepare_mods()
    with ThreadPoolExecutor(3) as pool:
        for line in pool.map(record, scripts):
            print(line, flush=True)
