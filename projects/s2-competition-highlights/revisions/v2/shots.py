"""Edit list for the S2 Competition highlights reel v2 (shared by prep.py and edit.py).

v2 (user feedback 2026-11-09): "can we please have both players playing at once rather than
alternating?" Sources are the planner-authored simultaneous route ehz-simultaneous-tie-special
(both players race each act together; P1 wins act 1, P2 wins act 2, 1-1 tie into the special
stage) and the CNZ slot route after its object-rendering fix, captured in ../cap2 at the PR head.
Each shot: (name, clip, first route row, frames, layout). Layouts: full (whole 2P screen with
player labels), single (one shared screen, no labels), top/bottom (one player's half), parity
(engine beside native BizHawk).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAP = ROOT.parent / "cap2"
NATIVE = ROOT.parent.parent / "native-sim2" / "frames"

CLIPS = {
    "T": "ehz-simultaneous-tie-special",
    "C": "cnz1-slot-flip",
}

# Native frame for an act-1 engine row: engine row 1260 and native frame 1329 both have
# Level_frame_counter 0. Native and engine positions match through engine row 2410; native
# frame 2480 is the first native level lag frame (not modelled by the engine), so the parity
# shot ends before it.
NATIVE_OFFSET = 69

SHOTS = [
    # cold open: both players through the act-1 loops at once
    ("open-loops", "T", 2800, 300, "full"),
    # title drop over the real title screen, then one take: menu -> fade -> title card -> go
    ("title", "T", 720, 252, "full"),
    ("flow", "T", 1000, 330, "full"),
    # the start: both take off together
    ("race-start", "T", 1290, 300, "full"),
    # parity: engine and native BizHawk, same route rows (both players moving, through the spiral)
    ("parity", "T", 1940, 450, "parity"),
    # act-1 finish: Sonic first (row 3868), Tails (4076), then the results board
    ("finish1", "T", 3800, 300, "full"),
    ("results1", "T", 4259, 240, "full"),
    # Casino Night: its own title card, then player 1 rides the slot machine while Tails runs
    ("cnz-card", "C", 1180, 100, "full"),
    ("cnz", "C", 1890, 450, "full"),
    # act 2: both racing, then Tails wins (6767) ahead of Sonic (6990), results
    ("act2-race", "T", 5340, 300, "full"),
    ("finish2", "T", 6700, 300, "full"),
    ("results2", "T", 7173, 260, "full"),
    # the 1-1 tie fades to white into the competitive special stage
    ("ss-entry", "T", 7462, 90, "single"),
    ("ss-start", "T", 7587, 476, "single"),
]
