#!/usr/bin/env python3
"""Screenplay generator for "Day Off", the Stageplay introduction film (sp-promo-a).

Story: Green Hill's first Motobug runs its native patrol, stops (the director takes it
over: Free -> Puppet), decides it needs a day off and leaves. Sonic runs the loop behind
it, skids, turns back. It holidays on Sonic 3's Angel Island, where Knuckles lets it stay
and friends from two games join it. Epilogue: back on patrol next morning.

Output: a version-6 screenplay JSON written beside this script (never overwrites; pass a
new take name). Compile with tools/sp.py compile --script TAKE.screenplay.json --out TAKE.stageplay
from this directory so relative decoration assets keep their root.

Coordinates are native world centres (ROM x_pos/y_pos). Frames are shot-local.
Origin: 2026-10-24 sp-promo-a production; engine 632a5f8c3 + Sonic1LoopManager fix.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 480, 270

# ---------------------------------------------------------------- styling
def argb(hexrgb, a=0xFF):
    v = (a << 24) | int(hexrgb.lstrip('#'), 16)
    return v - (1 << 32) if v >= (1 << 31) else v

SKINS = [
    # name colour, text, panel, border, decoration
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

PANEL_W = 236

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

def line(start, end, speaker, text, side="left", y=10, width=None, reveal=None, cue_id=None):
    if width is None:
        width = next(w for w in (176, 216, 256, 300, 360) if wrap_rows(text, w) <= 2 or w == 360)
    rows = wrap_rows(text, width)
    height = 2 * PAD + 14 + 12 * (rows - 1) + 10
    # Dialogue speakers must be player cast members; object roles speak as named speakers.
    who = dict(speakerActor="", speakerName="Motobug") if speaker == "moto" else dict(speakerActor=speaker)
    cue = dict(startFrame=start, endFrame=end, **who, text=text, skinId=speaker_skin(speaker),
               typerId=speaker_skin(speaker), x=(10 if side == "left" else W - width - 10), y=y,
               width=width, height=height)
    if reveal is not None:
        cue["revealFrames"] = reveal
    if cue_id:
        cue["id"] = cue_id
    return cue

def speaker_skin(actor):
    return {"moto": "moto", "sonic": "sonic", "knuckles": "knuckles", "tails": "tails"}[actor]

def music(game, sound_id, frame=0):
    return dict(frame=frame, kind="ROM_MUSIC", gameId=game, soundId=sound_id)

GHZ = dict(gameId="s1", zone=0, act=0)
AIZ = dict(gameId="s3k", zone=0, act=0)

# ---------------------------------------------------------------- shots
def shot_patrol():
    """Green Hill 1, the first hill. Native patrol, the takeover, a push-in, the decision."""
    freeze = 330
    return dict(
        id="patrol", durationFrames=900, set=GHZ,
        camera=[
            dict(frame=0, x=400, y=715, interpolation="HOLD"),
            dict(frame=freeze + 20, x=400, y=715, interpolation="SMOOTH"),
            dict(frame=freeze + 70, x=520, y=790, zoom=2, interpolation="HOLD"),
        ],
        objects={"moto": [
            dict(frame=0, x=720, y=845, mode="FREE"),
            dict(frame=freeze, x=0, y=0, mode="PUPPET"),   # position patched from simulation
        ]},
        captions=[dict(startFrame=20, endFrame=200, text="GREEN HILL ZONE   9:00 AM", x=14, y=246, argb=argb("#FFFFFF"))],
        dialogue=[
            line(40, freeze - 10, "moto", "Patrol... turn. Patrol... turn.", side="right"),
            line(freeze + 90, freeze + 230, "moto", "...", side="right"),
            line(freeze + 240, freeze + 400, "moto", "Thirty-five years of this.", side="right"),
            line(freeze + 410, 880, "moto", "I need a day off.", side="right"),
        ],
        audio=[music("s1", 129), dict(frame=freeze, kind="MUSIC_STOP")],
        worldCommands=[dict(frame=0, kind="REMOVE_OBJECT", target=dict(layoutIndex=1, objectId=38, subtype=6)),
                       dict(frame=0, kind="REMOVE_OBJECT", target=dict(layoutIndex=4, objectId=64, subtype=0))],
    )

def shot_loop():
    """Green Hill 1 loop. The Motobug on the road; Sonic runs the planned loop route and skids."""
    return dict(
        id="loop", durationFrames=840, set=GHZ,
        transition=dict(kind="WIPE_RIGHT", durationFrames=24),
        camera=[
            dict(frame=0, x=5340, y=480, interpolation="HOLD"),
            dict(frame=200, x=5340, y=480, interpolation="SMOOTH"),
            dict(frame=270, x=5560, y=440, interpolation="HOLD"),
        ],
        actors={"sonic": [dict(frame=0, x=5100, y=686)]},
        actions={"sonic": []},   # route helper fills MOVE_TO/STOP/FACE_LEFT; later intents appended after routing
        objects={"moto": [dict(frame=0, x=5510, y=691, mode="POSE", pose=0, flipX=True)]},
        objectActions={"moto": []},
        dialogue=[
            line(300, 430, "sonic", "Uh... aren't you supposed to be chasing me?", side="right"),
            line(440, 530, "moto", "Day off.", side="left"),
            line(580, 680, "sonic", "...Huh. Fair enough.", side="right"),
        ],
        audio=[music("s1", 129)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_island():
    """Angel Island 1: the holiday. Knuckles glides in to throw it out."""
    return dict(
        id="island", durationFrames=900, set=AIZ,
        transition=dict(kind="WIPE_RIGHT", durationFrames=24),
        camera=[dict(frame=0, x=4872, y=840, interpolation="HOLD")],
        actors={"knuckles": [dict(frame=0, x=5480, y=1051, flipX=True)]},
        actions={"knuckles": [
            dict(frame=200, kind="JUMP", holdFrames=20),
            dict(frame=222, kind="GLIDE_TO", x=5160, y=1051, urgency=0.8),
        ]},
        objects={"moto": [dict(frame=0, x=4840, y=1056, mode="POSE", pose=0, flipX=True)]},
        objectActions={"moto": [dict(frame=0, kind="MOVE_TO", x=5080, y=1056, speed=1),
                                dict(frame=240, kind="STOP")]},
        captions=[dict(startFrame=30, endFrame=210, text="ANGEL ISLAND ZONE   11:00 AM", x=14, y=246, argb=argb("#FFFFFF"))],
        dialogue=[
            line(300, 420, "knuckles", "Hey! No badniks on my island!", side="right"),
            line(430, 520, "moto", "Day off.", side="left"),
            line(540, 650, "knuckles", "...Badniks get days off?", side="right"),
            line(660, 760, "moto", "They do now.", side="left"),
            line(780, 890, "knuckles", "...Huh.", side="right"),
        ],
        audio=[music("s3k", 1)],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_friends():
    """Angel Island 1 by the waterfall: friends from two games join; best day ever."""
    return dict(
        id="friends", durationFrames=720, set=AIZ,
        transition=dict(kind="FADE_BLACK", durationFrames=20),
        camera=[dict(frame=0, x=4872, y=840, interpolation="HOLD")],
        actors={"knuckles": [dict(frame=0, x=5150, y=1051, flipX=True)],
                "sonic": [dict(frame=0, x=4840, y=1051)],
                "tails": [dict(frame=0, x=5300, y=880, flipX=True)]},
        actions={"sonic": [dict(frame=60, kind="MOVE_TO", x=4990, y=1051, urgency=0.6)],
                 "tails": [dict(frame=150, kind="JUMP", holdFrames=10),
                           dict(frame=165, kind="FLY_TO", x=5200, y=1000, urgency=0.5)]},
        objects={"moto": [dict(frame=0, x=5080, y=1056, mode="POSE", pose=2, flipX=True)]},
        dialogue=[
            line(140, 250, "sonic", "Room for one more?", side="left"),
            line(330, 430, "tails", "Make that two!", side="right"),
            line(480, 700, "moto", "Best. Day. Ever.", side="left"),
        ],
        worldCommands=[dict(frame=0, kind="CLEAR_BADNIKS")],
    )

def shot_epilogue():
    """Green Hill 1, next morning: the native patrol resumes."""
    return dict(
        id="morning", durationFrames=480, set=GHZ,
        transition=dict(kind="FADE_BLACK", durationFrames=30),
        camera=[dict(frame=0, x=400, y=715, interpolation="HOLD")],
        objects={"moto": [dict(frame=0, x=720, y=845, mode="FREE")]},
        captions=[dict(startFrame=20, endFrame=200, text="NEXT MORNING", x=14, y=246, argb=argb("#FFFFFF"))],
        dialogue=[
            line(60, 250, "moto", "Patrol... turn.", side="right"),
            line(300, 470, "moto", "Only 364 days to go.", side="right"),
        ],
        audio=[music("s1", 129)],
        worldCommands=[dict(frame=0, kind="REMOVE_OBJECT", target=dict(layoutIndex=1, objectId=38, subtype=6)),
                       dict(frame=0, kind="REMOVE_OBJECT", target=dict(layoutIndex=4, objectId=64, subtype=0))],
    )

def screenplay():
    return dict(
        version=6, name="Day Off", width=W, height=H,
        cast=[
            dict(id="sonic", name="Sonic", gameId="s1", character="sonic"),
            dict(id="knuckles", name="Knuckles", gameId="s3k", character="knuckles"),
            dict(id="tails", name="Tails", gameId="s3k", character="tails"),
        ],
        objectCast=[dict(id="moto", name="Motobug", gameId="s1", zone=0, act=0, objectId=64, subtype=0,
                         layoutIndex=-1, sourceKind="LAYOUT_OBJECT")],
        dialogueTypers=TYPERS, dialogueSkins=SKINS,
        shots=[shot_patrol(), shot_loop(), shot_island(), shot_friends(), shot_epilogue()],
    )

if __name__ == "__main__":
    out = HERE / (sys.argv[1] if len(sys.argv) > 1 else "take.screenplay.json")
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    out.write_text(json.dumps(screenplay(), indent=1))
    print(out)
