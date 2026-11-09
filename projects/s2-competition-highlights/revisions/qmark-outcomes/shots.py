"""Edit list for the S2 two-player "?" monitor outcomes reel.

User request (2026-11-09): "I'd like to see each getting activated and held for a few seconds so
I can see the outcome is correct visually." One frozen route per outcome (ehz-qmark-<content>,
ENGINE + BIZHAWK qualified, commit 0b7b4db4f); engine captures in ../engine/<content>/ and native
BizHawk per-frame captures in ../native-<content>/. Native frame = engine row + 69.
Each outcome: (content id, item number, title, Level_frame_counter at icon init, break engine row,
what to look for ('|' = line break), layout: half = the breaker's (Sonic's) half,
engine stacked over native at 2x; full = both halves side by side, for outcomes that involve Tails). Obj2E_Init (s2.asm:25755-25776): item = (Level_frame_counter & 7) + 1.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENGINE = ROOT.parent / "engine"
NATIVE_ROOT = ROOT.parent
NATIVE_OFFSET = 69
LEAD, HOLD = 75, 285   # frames shown before / after the break

OUTCOMES = [
    ("sonic-1up", 1, "SONIC 1-UP", 288, 1547, "Sonic's lives go up|and the 1-up jingle plays", "half"),
    ("tails-1up", 2, "TAILS 1-UP", 329, 1588, "Sonic breaks it, but the extra life goes to Tails", "full"),
    ("robotnik", 3, "ROBOTNIK", 330, 1589, "It hurts the player|who broke it", "half"),
    ("super-ring", 4, "SUPER RING", 331, 1590, "Ten rings for|the breaker", "half"),
    ("speed-shoes", 5, "SPEED SHOES", 340, 1599, "Speed shoes, with|the faster music", "half"),
    ("shield", 6, "SHIELD", 333, 1592, "A shield for|the breaker", "half"),
    ("invincibility", 7, "INVINCIBILITY", 334, 1593, "Invincibility stars|and music", "half"),
    ("teleport", 8, "TELEPORT", 335, 1594, "The two players swap places", "full"),
]
