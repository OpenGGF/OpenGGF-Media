#!/usr/bin/env python3
"""Summarise a capture's native events (observe.csv + observe2.csv). Usage: events.py CAPTURE_NAME..."""
import sys, csv
from pathlib import Path
T = Path(__file__).resolve().parents[1]
for n in sys.argv[1:]:
    d = T / "captures" / n / "capture"
    o = list(csv.DictReader(open(d / "observe.csv"))); o2 = list(csv.DictReader(open(d / "observe2.csv")))
    ev, prev = [], None
    for a, b in zip(o, o2):
        k = (a["score"], a["rings"], a["hurt"], a["dead"], b["lives"], b["checkpoint_idx"], b["mode"], b["paused"], b["stealth_body"],
             b["no_rings"], b["no_checkpoints"], b["no_special"], b["no_bonus"], b["removed_monitors"], b["speed_pct"], b["audio_follows"], b["bonus_type"], b["special_provider"])
        if k != prev:
            ev.append(f'{a["frame"]}:s{a["score"]} r{a["rings"]} h{a["hurt"]} d{a["dead"]} L{b["lives"]} cp{b["checkpoint_idx"]} {b["mode"][:6]} P{b["paused"][0]} '
                      f'st{b["stealth_body"][:1]} nr{b["no_rings"][:1]}nc{b["no_checkpoints"][:1]}ns{b["no_special"][:1]}nb{b["no_bonus"][:1]} rm[{b["removed_monitors"]}] '
                      f'sp{b["speed_pct"]}{b["audio_follows"][:1]} {b["bonus_type"]}{b["special_provider"]} @{int(a["x"] or 0):x},{int(a["y"] or 0):x}')
            prev = k
    print(f"== {n} frames={len(o)}"); print("\n".join("  " + e for e in ev))
