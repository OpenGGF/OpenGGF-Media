"""Edit list for the S2 Competition highlights reel (shared by prep.py and edit.py).

Each shot: (name, clip, first route row, frames, layout). Rows are engine route rows of the
captures in cap/<route>/ (one frame per row, 60 fps). Layouts: full (whole 2P screen with player labels), single (one shared screen, no labels), top or
bottom (one player's half), parity (engine beside native BizHawk), white (plain white card).
Origin: 2026-11-09 highlights request for James.
"""
CLIPS = {
    "T": "ehz-tied-act-wins-special",
    "Z": "ehz-zone-results",
    "C": "cnz1-slot-flip",
}

# Native BizHawk frame for an act-1 engine row (engine row 1260 and native frame 1329 both have Level_frame_counter 0).
NATIVE_OFFSET = 69

SHOTS = [
    # cold open: player 1 through the act-1 loop
    ("open-loop", "T", 2620, 300, "top"),
    # title drop over the real title screen, then one take: menu -> fade -> title card -> go
    ("title", "T", 720, 252, "full"),
    ("flow", "T", 1000, 330, "full"),
    # player 1's act-1 run, then the finish and the two-player signpost
    ("p1-run", "T", 1800, 270, "full"),
    ("p1-finish", "T", 3640, 300, "full"),
    # parity: engine and native BizHawk, same route rows
    ("parity", "T", 2300, 480, "parity"),
    # player 2's run and finish, results
    ("p2-loop", "T", 5040, 270, "bottom"),
    ("p2-finish", "T", 6200, 210, "full"),
    ("results1", "T", 6489, 270, "full"),
    # Casino Night: its own title card, then player 1 rides the slot machine to a jackpot
    ("cnz-card", "C", 1180, 100, "full"),
    ("cnz", "C", 1890, 450, "full"),
    # act 2 results and the tie into the special stage
    ("results2", "T", 14700, 240, "full"),
    ("ss-entry", "T", 18365, 90, "single"),
    ("ss-start", "T", 18490, 476, "single"),
]
