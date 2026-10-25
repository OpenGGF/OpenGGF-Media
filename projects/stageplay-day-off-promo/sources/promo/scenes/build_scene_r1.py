#!/usr/bin/env python3
"""Screenplay generator for "Day Off", the Stageplay introduction film (sp-promo-a).

Story: Green Hill's first Motobug runs its real patrol, stops dead (the director takes it
over: Free -> Puppet), decides it needs a day off and leaves. Sonic runs the loop behind
it, skids and turns back. Tails meets it in Emerald Hill ("aren't you from Sonic 1?").
On Sonic 3's Angel Island, Knuckles glides in to throw it out and lets it stay. Finale:
friends from three games watch the sea with it. Epilogue: back on patrol next morning.

Usage: build_scene.py TAKE  -> writes TAKE.screenplay.json (refuses to overwrite).
Route-helper output (Sonic's loop) is read from routes/loop-route.json when present.
Measured native data (patrol freeze position, floors) is read from measured.json.
Coordinates are native world centres (ROM x_pos/y_pos); frames are shot-local.
Origin: 2026-10-24 sp-promo-a production; engine 0ba60490e (632a5f8c3 + loop-plane fix).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 480, 270
MEASURED = json.loads((HERE / "measured.json").read_text()) if (HERE / "measured.json").exists() else {}

# ---------------------------------------------------------------- styling
def argb(hexrgb, a=0xFF):
    v = (a << 24) | int(hexrgb.lstrip('#'), 16)
    return v - (1 << 32) if v >= (1 << 31) else v

SKINS = [
    dict(id="moto", nameArgb=argb("#FF6A5A"), textArgb=argb("#F4F1E8"), panelArgb=argb("#141A2B", 0xF0),
         borderArgb=argb("#B8C0CC"), decorationAsset="decor/moto.png", decorationBorder=6, padding=8, pointer=True),
    dict(id="sonic", nameArgb=argb("#7FB2FF"), textArgb=argb("#F4F1E8"), panelArgb=argb("#101C3A", 0xF0),
         borderArgb=argb("#3D6CE0"), decorationAsset="decor/sonic.png", decorationBorder=6, padding=8, pointer=True),
    dict(id="knuckles", nameArgb=argb("#FF7A8A"), textArgb=argb("#F4F1E8"), panelArgb=argb("#2A1018", 0xF0),
         borderArgb=argb("#D83050"), decorationAsset="decor/knuckles.png", decorationBorder=6, padding=8, pointer=True),
    dict(id="tails", nameArgb=argb("#FFC35A"), textArgb=argb("#F4F1E8"), panelArgb=argb("#2A1E0C", 0xF0),
         borderArgb=argb("#F0A020"), decorationAsset="decor/tails.png", decorationBorder=6, padding=8, pointer=True),
]
TYPERS = [
    dict(id="moto", framesPerGrapheme=3, punctuationPauseFrames=14, spacePauseFrames=2),
    dict(id="sonic", framesPerGrapheme=1, punctuationPauseFrames=6, spacePauseFrames=0),
    dict(id="knuckles", framesPerGrapheme=2, punctuationPauseFrames=10, spacePauseFrames=0),
    dict(id="tails", framesPerGrapheme=2, punctuationPauseFrames=8, spacePauseFrames=0),
]
PAD = 8

def wrap_rows(text, width):
    """Greedy word wrap mirroring StageplayDialogue: 10 px advance, 9 px glyphs."""
    per_row = (width - 2 * PAD + 1) // 10
    rows, current = [], ""
    for word in text.split(" "):
        candidate = word if not current else current + " " + word
        if len(candidate) <= per_row:
            current = candidate
        else:
            rows.append(current)
            current = word
    rows.append(current)
    return len(rows)

def line(start, end, speaker, text, side="left", y=10, width=None, reveal=None, cue_id=None, x=None):
    if width is None:
        width = next(w for w in (156, 196, 236, 276, 316) if wrap_rows(text, w) <= 2 or w == 316)
    rows = wrap_rows(text, width)
    height = 2 * PAD + 14 + 12 * (rows - 1) + 10
    # Dialogue speakers must be player cast members; object roles speak as named speakers.
    who = dict(speakerActor="", speakerName="Motobug") if speaker == "moto" else dict(speakerActor=speaker)
    if x is None:
        x = 10 if side == "left" else W - width - 10
    cue = dict(startFrame=start, endFrame=end, **who, text=text, skinId=speaker, typerId=speaker,
               x=x, y=y, width=width, height=height)
    if reveal is not None:
        cue["revealFrames"] = reveal
    if cue_id:
        cue["id"] = cue_id
    return cue

def timed_reveal(text, beats, per=2):
    """revealFrames for text split into chunks; beats = elapsed frame where each chunk starts."""
    chunks = text.split("|")
    assert len(chunks) == len(beats), (chunks, beats)
    frames = []
    for chunk, beat in zip(chunks, beats):
        for i, _ in enumerate(chunk):
            frames.append(beat + i * per)
    return "".join(chunks), frames

def music(game, sound_id, frame=0):
    return dict(frame=frame, kind="ROM_MUSIC", gameId=game, soundId=sound_id)

def remove(layout, object_id, subtype, frame=0):
    return dict(frame=frame, kind="REMOVE_OBJECT", target=dict(layoutIndex=layout, objectId=object_id, subtype=subtype))

GHZ = dict(gameId="s1", zone=0, act=0)
EHZ = dict(gameId="s2", zone=0, act=0)
AIZ = dict(gameId="s3k", zone=0, act=0)

# ---------------------------------------------------------------- Motobug drive cycle
# Ani_Moto .drive: delay 7 -> each mapping frame shows for 8 ticks, sequence 0,1,0,2
# (_anim/Moto Bug.asm). .stand holds frame 2. Directed S1 Motobug graphs declare no pure
# animation, so the cycle is authored as explicit Pose mapping frames.
DRIVE = (0, 1, 0, 2)

def piecewise(points):
    pts = sorted(points)
    def f(x):
        if x <= pts[0][0]:
            return pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 != x0 else y1
        return pts[-1][1]
    return f

def drive(keys, start, end, x0, direction, floor, flip, speed=1.0, step=8, phase=0):
    """Append Pose keys driving from x0 at `start` to `end` (exclusive) at speed px/tick."""
    frame = start
    i = phase
    while frame < end:
        x = x0 + direction * speed * (frame - start)
        keys.append(dict(frame=frame, x=round(x, 3), y=round(floor(x), 3), mode="POSE",
                         pose=DRIVE[i % 4], flipX=flip, interpolation="LINEAR"))
        frame += step
        i += 1
    return x0 + direction * speed * (end - start)

def hold(keys, frame, x, floor, flip, pose=2, mode="POSE"):
    keys.append(dict(frame=frame, x=round(x, 3), y=round(floor(x), 3), mode=mode, pose=pose, flipX=flip,
                     interpolation="HOLD"))

# Floors as Motobug anchor heights (feet = y + 14), measured from native Free Motobugs
# (probe/floors) or player spawn snapping (measured.json).
GHZ_LOOP_FLOOR = piecewise([(5256, 689), (5676, 689), (5686, 680), (5706, 675), (5726, 665), (5746, 655),
                            (5766, 645), (5786, 635), (5806, 631), (5826, 625), (5926, 625), (5966, 630),
                            (5996, 632), (6036, 631), (6056, 629)])
EHZ_FLOOR = piecewise([tuple(v) for v in MEASURED.get("ehz_floor", [[0, 656], [600, 656]])])
AIZ_FLOOR = piecewise([tuple(v) for v in MEASURED.get("aiz_floor", [[4800, 1055], [5600, 1055]])])
LEDGE_FLOOR = piecewise([tuple(v) for v in MEASURED.get("ledge_floor", [[6017, 705], [6207, 705]])])

# ---------------------------------------------------------------- shots
# S1 ObjectFall gravity: obVelY += $38 per frame (0.21875 px/tick), as Moto_Main uses.
GRAVITY = 0x38 / 256

def drop(keys, start, x0, y0, direction, speed, floor_y, flip, step=2):
    """Posed fall off a ledge with the ROM's object gravity; returns the landing frame."""
    vy, y, x, frame = 0.0, y0, x0, start
    while y < floor_y:
        keys.append(dict(frame=frame, x=round(x, 3), y=round(y, 3), mode="POSE", pose=0, flipX=flip,
                         interpolation="LINEAR"))
        for _ in range(step):
            vy += GRAVITY
            y += vy
            x += direction * speed
        frame += step
    keys.append(dict(frame=frame, x=round(x, 3), y=floor_y, mode="POSE", pose=2, flipX=flip, interpolation="HOLD"))
    return frame

def shot_patrol():
    """Green Hill 1, the first hill: native patrol, the takeover at the edge, the decision."""
    m = MEASURED.get("patrol", {})
    turn1 = m.get("turn_frame", 105)          # native: leaves the left edge
    edge2 = m.get("edge2_frame", 297)         # native: reaches the right edge and waits
    turn2 = m.get("turn2_frame", 357)         # native: would turn here; the director holds it instead
    fx, fy = m.get("edge2_x", 736.0), m.get("freeze_y", 849.0)
    freeze = edge2 + 28                       # exhaust smoke has expired; the graph is clean
    keys = [dict(frame=0, x=m.get("spawn_x", 580), y=845, mode="FREE")]
    keys.append(dict(frame=freeze, x=fx, y=fy, mode="PUPPET", pose=2, flipX=False, interpolation="HOLD"))
    leave = 790
    edge_x = drive(keys, leave, leave + 8, fx, +1, lambda x: fy, flip=False)
    last = drop(keys, leave + 8, edge_x, fy, +1, 1.0, fy + 110, flip=False)
    text, reveal = timed_reveal("Patrol...| turn.| Patrol...", [0, turn1 - 15, turn1 + 15])
    cx, cy = fx - 30, fy - 12                 # close-up centre: the Motobug right of centre, facing out
    return dict(
        id="patrol", durationFrames=leave + 50, set=GHZ,
        camera=[
            dict(frame=0, x=400, y=715, interpolation="HOLD"),
            dict(frame=turn2 + 20, x=400, y=715, interpolation="SMOOTH"),
            dict(frame=turn2 + 80, x=round(cx - 120, 3), y=round(cy - 67.5, 3), zoom=2, interpolation="HOLD"),
        ],
        objects={"moto": keys},
        captions=[dict(startFrame=20, endFrame=200, text="GREEN HILL ZONE   9:00 AM", x=14, y=248,
                       argb=argb("#FFFFFF"))],
        dialogue=[
            line(15, turn2, "moto", text, side="right", reveal=reveal),
            line(turn2 + 100, turn2 + 160, "moto", "...", side="left"),
            line(turn2 + 170, turn2 + 300, "moto", "Thirty-five years of this.", side="left"),
            line(turn2 + 310, leave - 5, "moto", "I need a day off.", side="left"),
        ],
        audio=[music("s1", 129), dict(frame=turn2, kind="MUSIC_STOP")],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS"), remove(1, 38, 6)],
    )

def shot_loop():
    """Green Hill 1 loop: the Motobug on the road; Sonic runs the planned loop route."""
    keys = []
    stop_x = drive(keys, 0, 300, 5490, +1, GHZ_LOOP_FLOOR, flip=False)
    hold(keys, 300, stop_x, GHZ_LOOP_FLOOR, flip=False)
    drive(keys, 720, 800, stop_x, +1, GHZ_LOOP_FLOOR, flip=False)
    route_file = HERE / "routes" / "loop-route.json"
    # --no-route builds the editor's "before" scene: Sonic waits at his spawn until the
    # route is planned and applied in the editor capture.
    route = json.loads(route_file.read_text()) if route_file.exists() and "--no-route" not in sys.argv else []
    actions = list(route) + [
        dict(frame=545, kind="LOOK_UP", holdFrames=40),
        dict(frame=680, kind="MOVE_TO", x=6400, y=621, urgency=1.0),
    ]
    if "--no-route" in sys.argv:
        # The editor's "before" scene: Sonic has no direction in this shot yet. (A later MOVE_TO
        # would also prefill the route form's destination and motion settings.)
        actions = []
    two_cx, two_cy = (stop_x + 5856) / 2, 606
    return dict(
        id="loop", durationFrames=800, set=GHZ,
        # A hard cut on the drop. It also keeps the shot-entry frame (where player routes are
        # planned) visible in the editor; a wipe's opaque midpoint would sit on that frame.
        camera=[
            dict(frame=0, x=5260, y=470, interpolation="HOLD"),
            dict(frame=200, x=5260, y=470, interpolation="SMOOTH"),
            dict(frame=275, x=5583, y=440, interpolation="HOLD"),
            dict(frame=292, x=round(two_cx - 120, 3), y=round(two_cy - 67.5, 3), zoom=2, interpolation="HOLD"),
        ],
        actors={"sonic": [dict(frame=0, x=5100, y=686)]},
        actions={"sonic": actions},
        objects={"moto": keys},
        dialogue=[
            line(305, 440, "sonic", "Uh... aren't you supposed to be chasing me?", side="right"),
            line(450, 535, "moto", "Day off.", side="left"),
            line(590, 690, "sonic", "...Huh. Fair enough.", side="right"),
        ],
        audio=[music("s1", 129)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_ehz():
    """Emerald Hill 1: Tails meets a badnik from another game."""
    keys = []
    stop_x = drive(keys, 0, 190, 0, +1, EHZ_FLOOR, flip=False)
    hold(keys, 190, stop_x, EHZ_FLOOR, flip=False)
    drive(keys, 470, 700, stop_x, +1, EHZ_FLOOR, flip=False)
    tails_x = MEASURED.get("ehz_tails_x", 290)
    cx, cy = (stop_x + tails_x) / 2, 618
    return dict(
        id="ehz", durationFrames=700, set=EHZ,
        transition=dict(kind="WIPE_RIGHT", durationFrames=24),
        camera=[dict(frame=0, x=40, y=455, interpolation="HOLD"),
                dict(frame=196, x=round(cx - 120, 3), y=round(cy - 67.5, 3), zoom=2, interpolation="HOLD")],
        actors={"tails": [dict(frame=0, x=tails_x, y=MEASURED.get("ehz_tails_y", 650), flipX=True)]},
        actions={"tails": [dict(frame=548, kind="JUMP", holdFrames=14),
                           dict(frame=549, kind="WAIT", condition="GROUNDED", timeoutFrames=90),
                           dict(frame=550, kind="FACE_RIGHT")]},
        objects={"moto": keys},
        captions=[dict(startFrame=30, endFrame=190, text="EMERALD HILL ZONE   10:00 AM", x=14, y=248,
                       argb=argb("#FFFFFF"))],
        dialogue=[
            line(215, 345, "tails", "Wait... aren't you from Sonic 1?", side="right"),
            line(355, 460, "moto", "Long drive.", side="left"),
        ],
        audio=[music("s2", 129)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_island():
    """Angel Island 1 under the great tree: Knuckles glides in to throw it out."""
    k = MEASURED.get("knuckles", {})
    keys = []
    stop_x = drive(keys, 0, k.get("moto_stop_frame", 170), 4840, +1, AIZ_FLOOR, flip=False)
    hold(keys, k.get("moto_stop_frame", 170), stop_x, AIZ_FLOOR, flip=False)
    hold(keys, 230, stop_x, AIZ_FLOOR, flip=True)      # looks back the way it came
    hold(keys, 275, stop_x, AIZ_FLOOR, flip=False)     # and forward again
    jump = k.get("jump_frame", 300)
    land = k.get("land_frame", jump + 112)
    knux_x = k.get("land_x", stop_x + 85)
    cx, cy = (stop_x + knux_x) / 2, 1030
    l0 = land + 40
    return dict(
        id="island", durationFrames=l0 + 470, set=AIZ,
        transition=dict(kind="WIPE_RIGHT", durationFrames=24),
        camera=[dict(frame=0, x=4872, y=860, interpolation="HOLD"),
                dict(frame=land + 18, x=round(cx - 120, 3), y=round(cy - 67.5, 3), zoom=2, interpolation="HOLD")],
        actors={"knuckles": [dict(frame=0, x=k.get("spawn_x", 5460), y=k.get("spawn_y", 1051), flipX=True)]},
        actions={"knuckles": [
            dict(frame=jump, kind="JUMP", holdFrames=k.get("hold", 16)),
            dict(frame=jump + k.get("hold", 16) + 2, kind="GLIDE_TO", x=k.get("glide_x", 4950), y=1051, urgency=1.0),
            dict(frame=jump + k.get("release_after", 95), kind="RELEASE"),
            dict(frame=jump + k.get("release_after", 95) + 1, kind="WAIT", condition="GROUNDED", timeoutFrames=200),
            dict(frame=jump + k.get("release_after", 95) + 2, kind="STOP"),
        ]},
        objects={"moto": keys},
        captions=[dict(startFrame=30, endFrame=210, text="ANGEL ISLAND ZONE   11:00 AM", x=14, y=248,
                       argb=argb("#FFFFFF"))],
        dialogue=[
            line(l0, l0 + 125, "knuckles", "Hey! No badniks on my island!", side="right"),
            line(l0 + 135, l0 + 215, "moto", "Day off.", side="left"),
            line(l0 + 235, l0 + 345, "knuckles", "...Badniks get days off?", side="right"),
            line(l0 + 355, l0 + 440, "moto", "They do now.", side="left"),
        ],
        audio=[music("s3k", 1), music("s3k", 0x1F, frame=jump - 20)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_ledge():
    """Angel Island 1 cliff ledge over the sea: friends from three games; best day ever."""
    keys = []
    hold(keys, 0, 6176, LEDGE_FLOOR, flip=True)
    text, reveal = timed_reveal("Best.| Day.| Ever.", [0, 50, 100], per=3)
    cx, cy = 6108, 672
    return dict(
        id="ledge", durationFrames=760, set=AIZ,
        transition=dict(kind="FADE_BLACK", durationFrames=40),
        camera=[dict(frame=0, x=cx - 120, y=cy - 67.5, zoom=2, interpolation="HOLD"),
                dict(frame=560, x=cx - 120, y=cy - 67.5, zoom=2, interpolation="SMOOTH"),
                dict(frame=740, x=cx - 120, y=cy - 67.5 - 110, zoom=2, interpolation="HOLD")],
        actors={"knuckles": [dict(frame=0, x=6128, y=703)],
                "sonic": [dict(frame=0, x=6082, y=703)],
                "tails": [dict(frame=0, x=6040, y=707)]},
        actions={"knuckles": [dict(frame=90, kind="CROUCH", holdFrames=420)],
                 "sonic": [dict(frame=230, kind="LOOK_UP", holdFrames=180)]},
        objects={"moto": keys},
        captions=[dict(startFrame=40, endFrame=200, text="LATER", x=14, y=248, argb=argb("#FFFFFF"))],
        dialogue=[line(300, 580, "moto", text, side="left", reveal=reveal)],
        audio=[music("s3k", 0x2F), music("s3k", 0x29, frame=300 + 100)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS"), remove(4, 1, 4), remove(5, 1, 3)],
    )

def shot_morning():
    """Green Hill 1, next morning: the native patrol resumes."""
    m = MEASURED.get("patrol", {})
    turn = m.get("turn_frame", 105)
    text, reveal = timed_reveal("Patrol...| turn.", [0, turn - 45])
    return dict(
        id="morning", durationFrames=480, set=GHZ,
        transition=dict(kind="FADE_BLACK", durationFrames=40),
        camera=[dict(frame=0, x=400, y=715, interpolation="HOLD")],
        objects={"moto": [dict(frame=0, x=m.get("spawn_x", 580), y=845, mode="FREE")]},
        captions=[dict(startFrame=30, endFrame=210, text="NEXT MORNING", x=14, y=248, argb=argb("#FFFFFF"))],
        dialogue=[
            line(45, turn + 40, "moto", text, side="right", reveal=reveal),
            line(turn + 80, 476, "moto", "...Only 364 days to go.", side="right"),
        ],
        audio=[music("s1", 129)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS"), remove(1, 38, 6)],
    )

def add_voice(shots):
    """Motobug beeps (make_voice.py) as VOICE cues at each line's first revealed word."""
    manifest = HERE / "voice" / "cues.json"
    if not manifest.exists() or "--no-voice" in sys.argv:
        return shots
    starts, at = {}, 0
    for shot in shots:
        starts[shot["id"]] = at
        at += shot["durationFrames"]
    by_id = {shot["id"]: shot for shot in shots}
    for entry in json.loads(manifest.read_text()):
        shot = by_id[entry["cue"].split(".")[0]]
        local = entry["globalFrame"] - starts[shot["id"]]
        shot.setdefault("audio", []).append(dict(frame=local, kind="VOICE", asset=entry["asset"], gain=0.3))
        shot["audio"].sort(key=lambda cue: cue["frame"])
    return shots

def strip_music(shots):
    """--no-music: an SFX stem take. Native SFX and voices stay; authored ROM music is removed."""
    if "--no-music" in sys.argv:
        # Exports play each level's native music unless a MUSIC_STOP is cued at frame zero.
        for shot in shots:
            kept = [c for c in shot.get("audio", []) if c["kind"] not in ("ROM_MUSIC", "MUSIC_STOP")]
            shot["audio"] = [dict(frame=0, kind="MUSIC_STOP")] + kept
    return shots

def screenplay():
    return dict(
        version=6, name="Day Off", width=W, height=H,
        cast=[
            dict(id="sonic", name="Sonic", gameId="s1", character="sonic"),
            dict(id="tails", name="Tails", gameId="s2", character="tails"),
            dict(id="knuckles", name="Knuckles", gameId="s3k", character="knuckles"),
        ],
        objectCast=[dict(id="moto", name="Motobug", gameId="s1", zone=0, act=0, objectId=64, subtype=0,
                         layoutIndex=-1, sourceKind="LAYOUT_OBJECT")],
        dialogueTypers=TYPERS, dialogueSkins=SKINS,
        shots=strip_music(add_voice([shot_patrol(), shot_loop(), shot_ehz(), shot_island(), shot_ledge(), shot_morning()])),
    )

if __name__ == "__main__":
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = HERE / ((names[0] if names else "take") + ".screenplay.json")
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    out.write_text(json.dumps(screenplay(), indent=1))
    print(out)
