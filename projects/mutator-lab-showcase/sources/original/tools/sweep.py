#!/usr/bin/env python3
"""Run capture variants 3 at a time and summarise native events from observe.csv/observe2.csv.
Usage: sweep.py PREFIX GAME ZONE PREFS [--paced] [--x X --y Y --rings N ...] -- name='script text' ...
Script text uses " / " as newline. Outputs captures/PREFIX-name; prints events (score/rings/hurt/dead/lives/cp/mode)."""
import sys, subprocess, os, csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
T = Path(__file__).resolve().parents[1]
args = sys.argv[1:]; i = args.index("--")
prefix, game, zone, prefs, *extra = args[:i]; variants = args[i+1:]
paced = "--paced" in extra; extra = [e for e in extra if e != "--paced"]
def run(v):
    name, text = v.split("=", 1)
    sp = T / "inputs" / "sweep" / f"{prefix}-{name}.script"; sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(text.replace(" / ", "\n") + "\n")
    cmd = ["python3", "-I", str(T / "tools/cap.py"), f"{prefix}-{name}", "--game", game, "--zone", zone, "--prefs", prefs,
           "--script", str(sp), "--timeout", "600"] + (["--paced"] if paced else []) + (["--"] + extra if extra else [])
    r = subprocess.run(cmd, cwd=T, capture_output=True, text=True)
    return name, r.returncode
with ThreadPoolExecutor(3) as ex:
    res = list(ex.map(run, variants))
for name, rc in res:
    d = T / "captures" / f"{prefix}-{name}" / "capture"
    o = list(csv.DictReader(open(d / "observe.csv"))); o2 = list(csv.DictReader(open(d / "observe2.csv")))
    ev, prev = [], None
    for a, b in zip(o, o2):
        k = (a["score"], a["rings"], a["hurt"], a["dead"], b["lives"], b["checkpoint_idx"], b["mode"], b["monitors"])
        if k != prev:
            ev.append(f'{a["frame"]}:s{a["score"]} r{a["rings"]} h{a["hurt"]} d{a["dead"]} L{b["lives"]} cp{b["checkpoint_idx"]} {b["mode"][:5]} m{b["monitors"]} @{int(a["x"] or 0):x},{int(a["y"] or 0):x}')
            prev = k
    print(f"== {name} rc={rc} frames={len(o)}\n  " + " | ".join(ev))
