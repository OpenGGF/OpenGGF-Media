#!/usr/bin/env python3
"""audit.py CAPTURE... — CSV-first event audit of final takes (provenance, policy, kills, hurts, spills, rings)."""
import csv, json, sys
from pathlib import Path
O = Path(__file__).resolve().parent.parent
out = {}
for name in sys.argv[1:]:
    d = O / "captures" / name
    rc = json.loads((d / "receipt.json").read_text())
    ob = list(csv.DictReader(open(d / "capture/observe.csv")))
    ev = []
    for i in range(1, len(ob)):
        p, r = ob[i - 1], ob[i]
        f = int(r['frame'])
        if r['score'] != p['score']: ev.append([f, "kill", int(p['yvel']), int(r['yvel']), int(r['x']), int(r['score'])])
        if r['hurt'] != p['hurt'] and r['hurt'] == '1': ev.append([f, "hurt", int(p['rings']), int(r['lost_rings']), int(r['lost_rings_slotless'])])
        if r['dead'] != p['dead'] and r['dead'] == '1': ev.append([f, "dead"])
        pol = ('gravity_pct', 'ringfall_full', 'rebound_pct', 'rebound_cap')
        if any(r[k] != p[k] for k in pol): ev.append([f, "policy", {k: r[k] for k in pol}])
        if r['mode'] != p['mode']: ev.append([f, "mode", r['mode']])
        if int(r['x']) - int(p['x']) < -2000: ev.append([f, "restart", int(r['x'])])
    out[name] = {"head": rc["source_head"], "dirty": rc["source_dirty"], "jar": rc["jar_sha256"][:16], "exit": rc["exit_code"],
                 "frames": len(ob), "events": ev, "max_rings": max(int(r['rings']) for r in ob),
                 "head_scale_range": [min(int(r['head_scale']) for r in ob), max(int(r['head_scale']) for r in ob)],
                 "final_rings": int(ob[-1]['rings'])}
json.dump(out, open(O / "captures" / "final-audit.json", "w"), indent=1)
for k, v in out.items():
    print(k, v["head"][:9], "dirty" if v["dirty"] else "clean", "jar", v["jar"], "frames", v["frames"], "maxrings", v["max_rings"], "head", v["head_scale_range"], "final", v["final_rings"])
    for e in v["events"]: print("   ", e)
