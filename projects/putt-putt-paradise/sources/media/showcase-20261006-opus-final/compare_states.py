#!/usr/bin/env python3
"""Compare the r5 real-menu-route captures with the r4 direct-entry captures (Opus, 2026-10-06).

r4 (showcase-20261006-opus-polish) entered each course with a direct level load; r5 enters through
the production title route, so its course rows start at a different point. Every scripted input
after the first lie is relative, so the two runs are aligned at an anchor event ("course-ready"
for practice/local, the first "handoff-0" for online) and compared row by row over the physics
columns (player position/velocity/state, camera, shot stage, owner/turn/score/status), plus the
event lists after the anchor. Writes state-comparison.json.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
import sys
OLD = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "showcase-20261006-opus-polish"
OUT = sys.argv[2] if len(sys.argv) > 2 else "state-comparison.json"
COLS = ["character", "act", "x", "y", "xvel", "yvel", "gspeed", "air", "rolling", "dead", "cam_x", "cam_y", "stage",
        "owner", "turn", "score", "status"]
PAIRS = {"ehz1-practice": "course-ready", "ehz2-practice": "course-ready", "local-match": "course-ready",
         "online/online-host": "handoff-0", "online/online-guest": "handoff-0"}


def table(path):
    rows = list(csv.reader(open(path)))
    return rows[0], rows[1:]


def events(path):
    return [(int(r), n) for r, n in (l.split(",", 1) for l in path.read_text().splitlines()[1:])]


def main():
    report = {"note": __doc__.strip().splitlines()[0]}
    for cap, anchor in PAIRS.items():
        new, old = ROOT / cap, OLD / cap
        if not (new / "state.csv").exists() or not (old / "state.csv").exists():
            report[cap] = {"skipped": "missing capture"}; continue
        hn, rn = table(new / "state.csv"); ho, ro = table(old / "state.csv")
        en, eo = events(new / "events.csv"), events(old / "events.csv")
        an = next(r for r, n in en if n == anchor); ao = next(r for r, n in eo if n == anchor)
        cols = [c for c in COLS if c in hn and c in ho]
        inew, iold = [hn.index(c) for c in cols], [ho.index(c) for c in cols]
        compared = mismatched = 0
        first = None
        for k in range(min(len(rn) - an, len(ro) - ao)):
            a, b = [rn[an + k][i] for i in inew], [ro[ao + k][i] for i in iold]
            compared += 1
            if a != b:
                mismatched += 1
                if first is None:
                    first = {"offset": k, "new_row": an + k, "old_row": ao + k,
                             "fields": {c: [x, y] for c, x, y in zip(cols, a, b) if x != y}}
        after_n = [(r - an, n) for r, n in en if r >= an and n not in ("lie-open",)]
        after_o = [(r - ao, n) for r, n in eo if r >= ao]
        report[cap] = {"anchor": anchor, "anchor_row_new": an, "anchor_row_old": ao, "shift_rows": an - ao,
                       "rows_new": len(rn), "rows_old": len(ro), "compared_rows": compared, "mismatched_rows": mismatched,
                       "first_mismatch": first, "events_after_anchor_identical": after_n == after_o,
                       "acts_new": sorted({r[hn.index("act")] for r in rn})}
    report["reference"] = str(OLD)
    (ROOT / OUT).write_text(json.dumps(report, indent=1) + "\n")
    for k, v in report.items():
        if isinstance(v, dict) and "anchor" in v:
            print(k, {x: v.get(x) for x in ("shift_rows", "compared_rows", "mismatched_rows", "events_after_anchor_identical", "acts_new")})


if __name__ == "__main__":
    main()
