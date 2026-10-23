#!/usr/bin/env python3
"""<Production> promo edit. Rebuild: python3 tools/media/promo_kit.py render THIS_FILE.
Creative brief (keep it here, one line each):
  audience / promise / hero moment / music + BPM / palette / title face / end card.
"""
import sys
sys.path.insert(0, "/ABSOLUTE/PATH/TO/OpenGGF/tools/media")
from promo_kit import *

# bpm/first come from `promo_kit.py beats music.wav`; place every cut in beats.
EDIT = dict(bpm=171.107, first=0.316, fps=60, size=(1920, 1080), out="out/promo.mp4", work="build")

CAP = "/ABSOLUTE/task/captures"
title = Frames(f"{CAP}/title/frames")
run = Frames(f"{CAP}/run/frames")


def build(e):
    b = e.bf
    # A. cold open: strongest motion first, a promise in one line
    e.S(Game(0, b(8), run, src=120, cam=cam_move((200, 112, 1.25), (230, 112, 1.0)), dim=0.35))
    for k, word in enumerate(["FASTER.", "LOUDER.", "YOURS."]):
        e.O(Txt(b(1 + k * 1.5), b(8), text(word, "title", 190, WHITE, stroke=9, shadow=10),
                e.W / 2, 300 + k * 210, enter="pop", centre=True))
    # B. title drop on the downbeat of a new section
    e.S(Game(b(8), b(24), title, src=0, cam=cam_slam(1.3, 26, b(24) - b(8)), trans="wipe", tdur=14))
    e.O(Flash(b(8), 18))
    # C. chapters: Header + one take each; splits/grids for short pieces
    # D. end card: logo, one line, URL, disclaimer; hold 5-7 s, fade out
    # e.bed("audio/music.wav", 0, 1.0, fade_out=2.0)   # one bed, chapter changes on its sections
    # e.X(b(8), "audio/sfx-spindash.wav", 0.8)          # ROM stingers on transitions only
    return b(24)
