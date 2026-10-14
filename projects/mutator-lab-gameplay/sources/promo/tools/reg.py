#!/usr/bin/env python3
"""Atomic manifest updates for run e0603654 (opus_gameplay_promo_r1).
Usage as module: reg.update(fn) where fn mutates the manifest dict; held under registry-write.lock."""
import json, os, fcntl, datetime
from pathlib import Path
REG = Path("/home/farrell/.local/state/temporary-agents/e0603654-55a0-4717-897c-3d93d1137ff3/manifest.json")
LOCK = REG.parent / "registry-write.lock"
AGENT = "opus_gameplay_promo_r1"
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def update(fn):
    with open(LOCK, "a") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        m = json.loads(REG.read_text())
        exp = datetime.datetime.fromisoformat(m["agents"][AGENT]["expires_at"])
        assert exp > datetime.datetime.now(datetime.timezone.utc), "agent registration expired"
        fn(m)
        tmp = REG.with_suffix(".opus-r1.new"); tmp.write_text(json.dumps(m, indent=2) + "\n"); os.chmod(tmp, 0o600)
        os.replace(tmp, REG)
def put_process(rec):
    def f(m):
        procs = m.setdefault("processes", [])
        procs[:] = [p for p in procs if p.get("id") != rec["id"]]; procs.append(rec)
    update(f)
if __name__ == "__main__":
    import sys
    state = sys.argv[1]
    def f(m):
        m["agents"][AGENT]["state"] = state; m["agents"][AGENT]["updated_at"] = now()
    update(f); print("agent state ->", state)
