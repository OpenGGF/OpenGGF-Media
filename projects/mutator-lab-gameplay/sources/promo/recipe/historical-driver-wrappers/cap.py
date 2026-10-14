#!/usr/bin/env python3
"""Display-free Mutator Lab capture for task e0603654 (opus_gameplay_promo_r1).

Usage: cap.py NAME --game s1|s2|s3k --zone Z [--prefs prefs.json] [--script authored.script]
              [--bk2 movie.bk2 --bk2-from N --bk2-count M] [--] [extra PromoCapture/GameplayCaptureTool flags]

Builds one input log (optional recorded-BK2 prefix, then an authored InputLogAuthorTool script),
seeds an isolated preference root, and runs promo.PromoCapture (GameplayCaptureSession, one native
tick per input frame, PNG every frame, offline PCM) in a fresh JVM with NO display environment:
-Dopenggf.headless.gl=surfaceless-egl (fails closed), java.awt.headless, ALSOFT null driver,
DISPLAY/WAYLAND_DISPLAY removed. Registers the exact PID/start ticks in the run manifest and writes
receipt.json with source head/dirty state, jar hash, argv and exit.
"""
from pathlib import Path
import os, sys, json, subprocess, hashlib, argparse, zipfile, shutil
sys.path.insert(0, str(Path(__file__).parent))
import reg

ROOT = Path("/home/farrell/code/projects/OpenGGF/.worktrees/ai-mutators-gameplay-promo")
OUT = Path("/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3")
JAVA = "/usr/lib/jvm/java-21-openjdk/bin/java"
ROMS = {"s1": "/home/farrell/code/projects/OpenGGF/Sonic The Hedgehog (W) (REV01) [!].gen",
        "s2": "/home/farrell/code/projects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen",
        "s3k": "/home/farrell/code/projects/OpenGGF/Sonic and Knuckles & Sonic 3 (W) [!].gen"}

ap = argparse.ArgumentParser()
ap.add_argument("name"); ap.add_argument("--game", required=True); ap.add_argument("--zone", required=True)
ap.add_argument("--act", default="1"); ap.add_argument("--prefs"); ap.add_argument("--script")
ap.add_argument("--bk2"); ap.add_argument("--bk2-from", type=int, default=0); ap.add_argument("--bk2-count", type=int)
ap.add_argument("--sidekick", default="none"); ap.add_argument("--timeout", type=int, default=1500)
a, extra = ap.parse_known_args()
for k in ("prefs", "script", "bk2"):
    if getattr(a, k): setattr(a, k, str(Path(getattr(a, k)).resolve()))
extra = [x for x in extra if x != "--"]
out = OUT / "captures" / a.name
assert not out.exists(), f"refusing existing output {out}"
out.mkdir(parents=True); (out / "user").mkdir(); (out / "saves" / "mutators").mkdir(parents=True)
if a.prefs:
    prefs = json.loads(Path(a.prefs).read_text())
    shutil.copy(a.prefs, out / "saves" / "mutators" / f"mutator-preferences-{prefs['profile']}.json")
    shutil.copy(a.prefs, out / "prefs-seed.json")
cp = str(ROOT / "target/classes") + os.pathsep + (ROOT / "target/mutators-classpath.txt").read_text().strip()
driver_cp = str(OUT / "tools/driver/classes") + os.pathsep + cp
jar = ROOT / "target/example-mutators/example-mutators.jar"

# Build the input log: recorded BK2 prefix lines (input-only), then the authored script.
lines, header = [], None
if a.bk2:
    with zipfile.ZipFile(a.bk2) as z:
        log = z.read("Input Log.txt").decode().splitlines()
    header = [l for l in log if l.startswith("LogKey:")]
    rows = [l for l in log if l.startswith("|")]
    count = a.bk2_count if a.bk2_count is not None else len(rows) - a.bk2_from
    lines += rows[a.bk2_from:a.bk2_from + count]
    (out / "bk2-prefix.json").write_text(json.dumps({"bk2": a.bk2, "sha256": hashlib.sha256(Path(a.bk2).read_bytes()).hexdigest(),
                                                     "from": a.bk2_from, "count": count}, indent=2))
if a.script:
    shutil.copy(a.script, out / "authored.script")
    tmp = out / "authored-log.txt"
    subprocess.run([JAVA, "-cp", cp, "com.openggf.tools.InputLogAuthorTool", "--script", a.script, "--out", str(tmp)],
                   check=True, cwd=out / "user", stdout=open(out / "author.log", "w"), stderr=subprocess.STDOUT)
    auth = tmp.read_text().splitlines()
    akey = [l for l in auth if l.startswith("LogKey:")]
    if header is None: header = akey
    assert header == akey, f"authored LogKey {akey} differs from recorded {header}"
    lines += [l for l in auth if l.startswith("|")]
log_path = out / "input.txt"
log_path.write_text("\n".join(["[Input]"] + header + lines + ["[/Input]"]) + "\n")

env = {k: v for k, v in os.environ.items() if k not in ("DISPLAY", "WAYLAND_DISPLAY", "XDG_SESSION_TYPE",
       "LD_LIBRARY_PATH", "EGL_PLATFORM", "XAUTHORITY", "GDK_BACKEND", "QT_QPA_PLATFORM")}
env.update(JAVA_HOME="/usr/lib/jvm/java-21-openjdk", ALSOFT_DRIVERS="null")
args = [JAVA, "-Xmx3g", "-Djava.awt.headless=true", "-Dopenggf.headless.gl=surfaceless-egl",
        "-Dorg.lwjgl.system.SharedLibraryExtractPath=" + str(ROOT / "target/test-tmp/promo-lwjgl"),
        "-Duser.dir=" + str(out / "user"), "-Dopenggf.saveRoot=" + str(out / "saves"), "-cp", driver_cp,
        "promo.PromoCapture", "--game", a.game, "--rom", ROMS[a.game], "--zone", a.zone, "--act", a.act,
        "--main", "sonic", "--sidekick", a.sidekick, "--mod", str(jar), "--audio", "--input", str(log_path),
        "--stop-on-death", "false", "--out-dir", str(out / "capture"), "--no-video"] + extra
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
info = {"id": reg.AGENT + "-cap-" + a.name, "owner": reg.AGENT, "workspace": str(ROOT), "source_head": head,
        "source_dirty": dirty, "jar_sha256": hashlib.sha256(jar.read_bytes()).hexdigest(), "argv": args,
        "env_removed": ["DISPLAY", "WAYLAND_DISPLAY", "XDG_SESSION_TYPE", "LD_LIBRARY_PATH", "EGL_PLATFORM", "XAUTHORITY"],
        "out": str(out), "created_utc": reg.now(), "teardown": "bounded wait then SIGTERM/SIGKILL of this exact PID",
        "limit": "surfaceless-EGL GameplayCaptureSession, one native tick per input frame, offline PCM; no display"}
with (out / "capture.log").open("wb") as logf:
    p = subprocess.Popen(args, cwd=out / "user", env=env, stdout=logf, stderr=subprocess.STDOUT)
    st = Path(f"/proc/{p.pid}/stat").read_text()
    info.update(pid=p.pid, start_ticks=st[st.rindex(")") + 2:].split()[19], cwd=str(out / "user"), state="running")
    reg.put_process(info)
    try:
        rc = p.wait(timeout=a.timeout)
    except subprocess.TimeoutExpired:
        info["timeout"] = True; p.terminate()
        try: rc = p.wait(timeout=10)
        except subprocess.TimeoutExpired: p.kill(); rc = p.wait(timeout=10)
    info.update(exit_code=rc, completed_utc=reg.now(), state="terminal_absent")
    reg.put_process(info)
(out / "receipt.json").write_text(json.dumps(info, indent=2) + "\n")
print(json.dumps({k: info.get(k) for k in ("id", "pid", "exit_code", "out")}))
sys.exit(0 if rc == 0 else 1)
