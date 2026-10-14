#!/usr/bin/env python3
"""Locked atomic update of the promo agent's registry entry. Usage: registry_update.py '<json patch>'"""
import fcntl, json, os, sys, tempfile, datetime
D = "/home/farrell/.local/state/temporary-agents/5c24f4a5-76e8-47c7-bc47-4173173d5caa"
M = os.path.join(D, "manifest.json")
patch = json.loads(sys.argv[1])
with open(os.path.join(D, "registry-write.lock"), "a") as lk:
    fcntl.flock(lk, fcntl.LOCK_EX)
    m = json.load(open(M))
    a = m["agents"]["opus_expansion_promo_r1"]
    procs = patch.pop("_process", None)
    a.update(patch)
    a["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if procs:
        m.setdefault("processes", []).append(procs)
    fd, tmp = tempfile.mkstemp(dir=D, prefix=".manifest.")
    with os.fdopen(fd, "w") as f:
        json.dump(m, f, indent=2)
    os.replace(tmp, M)
print("ok")
