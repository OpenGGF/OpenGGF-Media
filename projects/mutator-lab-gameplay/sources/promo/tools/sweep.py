#!/usr/bin/env python3
"""sweep.py PREFIX GAME ZONE ACT PREFS FROMFRAME -- 'script1' 'script2' ... [-- extra capture flags]
Runs each authored script (\\n escapes allowed) as captures PREFIX-i (3 in parallel) and prints
kills (score changes with pre/post y velocity), hurts, deaths and ring/head summary."""
import sys, subprocess, csv, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
O = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
prefix, game, zone, act, prefs, frm = args[:6]
rest = args[7:]
if "--" in rest:
    i = rest.index("--"); scripts, extra = rest[:i], rest[i + 1:]
else:
    scripts, extra = rest, []
def run(i_s):
    i, s = i_s
    name = f"{prefix}-{i}"
    sp = O / "inputs" / "sweep" / f"{name}.script"; sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(s.replace("\\n", "\n") + "\n")
    out = O / "captures" / name
    if out.exists(): subprocess.run(["rm", "-rf", str(out)])
    subprocess.run([sys.executable, "-I", str(O / "tools/cap.py"), name, "--game", game, "--zone", zone, "--act", act,
                    "--prefs", prefs, "--script", str(sp), "--timeout", "300", "--"] + extra,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ob = list(csv.DictReader(open(out / "capture/observe.csv")))
    ev = []
    for k in range(int(frm), len(ob)):
        a, b = ob[k - 1], ob[k]
        if a['score'] != b['score']: ev.append(f"K@{b['frame']}:{a['yvel']}->{b['yvel']}@x{b['x']}")
        if a['hurt'] == '0' and b['hurt'] == '1': ev.append(f"HURT@{b['frame']}")
        if a['dead'] == '0' and b['dead'] == '1': ev.append(f"DEAD@{b['frame']}")
    miny = min(int(r['y']) for r in ob[int(frm):])
    return f"{name}: {s!r}\n   events {ev} min_y {miny} final score {ob[-1]['score']} rings {ob[-1]['rings']}"
with ThreadPoolExecutor(3) as ex:
    for line in ex.map(run, enumerate(scripts)): print(line)
