#!/usr/bin/env python3
"""Write a schema-1 Mutator Lab preference seed. Usage: prefs.py OUT.json PROFILE key=json ...
Each key is a mutator id (e.g. big-head) whose value is a JSON object of options; presence enables it."""
import json, sys
DEFAULTS = {"no-checkpoints": {}, "no-rings": {}, "game-speed": {"percent": 100, "audio": False},
    "no-special-stages": {}, "stealth": {"target": "leader", "effects": False},
    "violent-explosions": {"percent": 150, "cap": 12}, "no-bonus-stages": {}, "gravity": {"percent": 100},
    "ringfall": {"capped": False, "cap": 32, "percent": 100, "full": False},
    "no-powerups": {k: True for k in ("super", "life", "bubble_shield", "lightning_shield", "rings", "random",
        "invincibility", "teleport", "static", "s_monitor", "speed_shoes", "fire_shield", "goggles", "eggman", "basic_shield")} | {"broken_shell": False},
    "big-head": {"rings": False, "target": "leader", "percent": 150}}
out, profile, *specs = sys.argv[1:]
enabled = {}
for s in specs:
    k, v = s.split("=", 1); enabled[k] = json.loads(v)
entries = {}
for k, d in DEFAULTS.items():
    entries["example-mutators:" + k] = {"schemaVersion": 1, "enabled": k in enabled, "options": d | enabled.get(k, {})}
json.dump({"formatVersion": 1, "profile": profile, "entries": entries}, open(out, "w"))
print(out)
