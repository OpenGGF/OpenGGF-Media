#!/usr/bin/env python3
"""Process/ownership manifest for task mutator-complete-showcase-20261010 (Opus 5.5 complete Mutator Lab showcase).
Held under an flock; records exact owned PIDs/start ticks/CWD for bounded capture JVMs."""
import json, os, fcntl, datetime
from pathlib import Path
REG = Path("/home/farrell/.local/state/temporary-agents/mutator-complete-showcase-20261010/manifest.json")
LOCK = REG.parent / "registry-write.lock"
AGENT = "opus55_complete_showcase"
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def update(fn):
    with open(LOCK, "a") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        m = json.loads(REG.read_text())
        assert datetime.datetime.fromisoformat(m["expires_at"]) > datetime.datetime.now(datetime.timezone.utc), "registration expired"
        fn(m)
        tmp = REG.with_suffix(".new"); tmp.write_text(json.dumps(m, indent=2) + "\n"); os.chmod(tmp, 0o600)
        os.replace(tmp, REG)
def put_process(rec):
    def f(m):
        procs = m.setdefault("processes", [])
        procs[:] = [p for p in procs if p.get("id") != rec["id"]]; procs.append(rec)
    update(f)
