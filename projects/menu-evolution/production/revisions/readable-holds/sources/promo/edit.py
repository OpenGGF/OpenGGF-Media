#!/usr/bin/env python3
"""ROAD TO 9, readable-holds cut: the accepted hill-climb story re-timed and simplified so that every
information-heavy screen finishes animating, then holds still long enough to read before it changes
(project menu-evolution, revision readable-holds, 2026-10-29; re-edited from the hill-climb-story sources).

Brief (one line each)
  Request.   The user on the 43.2 s hill-climb story: "great work but some of the screens are a bit rushed.
             lots of info on the screen that gets flashed up too quickly to ingest" and "some of the screens
             transition as soon as they finish animating, too". Then: "Hubs & Dialogs showing 9 everywhere, but
             the final scores have 8.5. None of this rounding crap; I want those spacing and icon scores at 9!"
             The engine follow-up did that by design (ca3d04a1d, 55d9fec81; audit section "Hub and Dialogs
             spacing and icons to 9", 56c9aed13), so the final row now shows that row, exactly, as a follow-up.
  Diagnosis. Animation time was being counted as reading time: rows, columns and counters kept revealing
             until the cut, so the settled state of most dense screens lasted 0-0.8 s. Several screens also
             carried two or three ideas at once (6x7 values, a scale, a footnote, a loop, a quote that
             repeated the caption).
  Fix.       Orient -> reveal -> settled read -> transition, per screen. Reveals got faster (cascades of 2-4
             frames instead of half beats); every dense state then holds 2.0-3.3 s with nothing editorial
             moving (proved by `edit.py reads`); one focal idea per screen; repeated copy and footnotes
             removed. Action beats (the wall drop, the slams, the rounds montage) stay quick.
  Story.     Unchanged from the accepted cut: we gave an AI every OpenGGF menu -> six groups -> seven
             criteria and one overall judgment -> every group to 8 -> rounds -> 27 families -> all at 8 ->
             we raised the bar to 9 -> pass 1 stalls -> a fresh AI review lowers scores -> structure, 13 ->
             another review sends one 9 back -> finish, 26, one key hint left -> 27 / 27 at 9 overall, with
             the hub shown criterion by criterion after its spacing and icon follow-up (9 on each; spacing and
             icons marked "was 8.5"), and the delivered six groups with the hub cell replaced by the follow-up's
             still.
  Removed.   The 5 / 7 / 9 scale line (9 is defined where it matters, at the turn), "one judgment, not an
             average" under the column (it is now the headline), the loop's separate chapter (it is a static
             strip under the rounds pane), "STEP 3 · THE HILL CLIMB" and the loop dots, the Time Attack
             5.5 -> 8 still comparison and its "also:" footnotes, "GOAL MET" / "STEP 3 DONE" and the date
             pill on the slam, "THEN WE RAISED THE BAR" as its own screen (now the turn's top line), "AT 9:
             0 / 27" on the turn, the caption that repeated each audit quote, the 27-tile board's numbers
             and row labels on the road (colour and the counter carry it), the "?" trace-plate tile and its
             footnote, the notices' 8 -> 8.5 tile, the derived "12" count (the counter is hidden while the
             sent-back tile is shown), the Time Attack lobby still (the last gap is a pill on its tile).
  Kept.      Sonic 2 Super Sonic bed, the aesthetic, the evolving board as narrator, the moving round-0 and
             delivered menus (wall, Mod manager, legal notice, Settings), the reviewer's marked-up capture,
             both verbatim audit quotes, the honest criteria row.
  Proof.     The moving takes are the d823ce643 renders. The follow-up changed the hub's pictures and none of
             the other five wall groups' (its before/final captures: Settings 0.00 %, Locate 0.17 % of pixels),
             so only the delivered wall's hub cell is replaced, by the follow-up's own static capture
             (hub-criteria-nine-20261029/final/320/hub/01-hub.png, d6771c478), labelled FOLLOW-UP STILL.
  Numbers.   Recorded values of docs/architecture/audits/2026-10-27-menu-design-review.md: the climb at
             d823ce643 (ROUND0, ROUNDS, PASSES below, each with its section); the final criteria row from the
             Hub and Dialogs follow-up matrix at 56c9aed13 (result-row.json, the one place to replace it; the
             earlier finish-pass row with spacing and icons 8.5 is kept in superseded/pre-hub-criteria/). Only
             the hub is claimed 9 on each criterion; other families keep their own entries (A5 colour 8.5, and
             the finish-pass 8.5s outside A1-A7). Subjective design judgments from captures, not usability
             measurements. Overall is holistic, not an average.
  Pixels.    Native 320x224 frames at integer nearest-neighbour 4x (rounds pane), 3x (evidence pane; the
             reviewer's 960x672 mark-up 1:1) or 2x (wall cells).
  Sound.     The super-sonic-cut's Super Sonic render (same file and sha256), played as one continuous
             excerpt: from bed beat 16 (the A section's second phrase, a downbeat hit) to 10.1 frames after
             the G-major stab on bed beat 152 (the rest after it, the same musical cut point as the accepted
             cut's beat 104, one loop later). 136 film beats = 55.87 s of bed, film 56.30 s. 146.48 BPM,
             24.576 frames a beat. Film beat b = bed beat b + 16: A1b 0-8, B 8-24, TURN 24-32, INTRO 32-40,
             A 40-56, B 56-72, TURN 72-80, INTRO 80-88, A 88-104, B 104-120, TURN 120-128, INTRO 128-136,
             stab 136. ALL 27 AT 8 lands on the B downbeat (56), the end card rides the last intro riff into
             the stab. Stingers and UI tones as before. Checked by measurement only; nobody listened.

Beat sheet (b = film beat, frame = round(24.576 b)). Each dense screen: reveal ends -> settled hold ->
transition (first frame that changes). `edit.py reads` renders the edit with footage and background
frozen and proves the settled frames identical; the table it prints is copied below.
  b0-12.5     1 THE ASK      wall of six round-0 menus drops (4 f apart); "WE GAVE AN AI EVERY OPENGGF
                             MENU." (Claude Opus, 27 Oct); b6 "STEP 1: SORT THEM INTO SIX GROUPS." and the six
                             labels land on their menus (4 f apart).
  b12.5-28    2 THE RUBRIC   labels fly to rows; "STEP 2: SCORE EACH GROUP ON SEVEN CRITERIA." (1 to 10,
                             judged from screenshots); seven named columns of round-0 cells cascade in 1.6 b;
                             overlays "NOT YET PICTURED". b20.5 cells dim, "OVERALL: ONE JUDGMENT, NOT AN
                             AVERAGE." and the six overall scores.
  b28-34.5    3 THE GOAL     "STEP 3: EVERY GROUP TO 8 OR BETTER." and the TARGET column.
  b34.5-47.5  4 ROUNDS 1-4   wipe; static loop strip under the pane; Mod manager round 0 -> at 8 (lap 1, one
                             step per half beat), legal notice (lap 2), laps 3-4 quick; ROUND 4; "CLOSE. NOT 8
                             YET." held.
  b47.5-56    5 EVERY FAMILY wipe; "THEN EVERY MENU: 27 FAMILIES."; tiles cascade (2 f), three below 8 framed.
  b56-62      6 ALL AT 8     slam "ALL 27 AT 8" + Tally End on the B downbeat, held.
  b62-71      7 ROAD TO 9    flash + Spindash Release; TARGET 9; tiles drop below; "THEN WE RAISED THE BAR.",
                             ROAD / TO / 9, "9 MEANS PRODUCTION POLISH.", held 2.9 s.
  b71-78.75   8 PASS 1       hub at 8 -> pass-1 picture, HUB 8 -> 8.5, five tiles flash; quote "No family
                             reached 9 overall in this pass."
  b78.75-87   9 REVIEW       "A FRESH AI REVIEW LOWERED THE SCORES."; mark-up draws; HUB 8.5 -> 8, four tiles red.
  b87-96      10 STRUCTURE   quote "The remaining blockers are structural rather than polish."; marked-up ->
                             rebuilt hub; HUB 9; 13 tiles gold in one wave, counter 13.
  b96-102     11 SENT BACK   "ANOTHER REVIEW SENT ONE 9 BACK."; Editor projects tile red, its pill; no count.
  b102-112    12 FINISH      "PASS 3: FINISH WHAT THE REVIEWS FOUND."; Settings still -> delivered moving,
                             SETTINGS 9; 26 gold, counter 26; Time Attack: one key hint left.
  b112-127.5  13 27 / 27     slam "27 / 27 AT 9 OVERALL"; b115 "THE HUB AFTER A SPACING AND ICON FOLLOW-UP",
                             the hub's row from result-row.json (9 on each, "was 8.5" under spacing and icons),
                             "THE HUB: 9 ON EACH CRITERION."; b123 Giant Ring iris into the six groups, delivered:
                             five moving takes and the hub's follow-up still.
  b127.5-136  END CARD       lines in 24 f, held 3.1 s; the stab; fade. 3378 frames, 56.30 s.

Reading holds (frames; settle = first fully settled frame, measured; transition = first changed frame):
  id          settle         transition     hold   reading payload
  ask         f26     0.43s  f147    2.45s  2.02s  WE GAVE AN AI EVERY OPENGGF MENU. / CLAUDE OPUS · 27 OCT 2026 (6 words + kicker; the text itself settles at f14)
  step1       f178    2.97s  f300    5.00s  2.03s  STEP 1: SORT THEM INTO SIX GROUPS. + 6 two- or three-word labels
  criteria    f359    5.98s  f497    8.28s  2.30s  STEP 2 headline + kicker; 7 criterion names; 5 rows of heat cells (values optional reading); NOT YET PICTURED
  overall     f538    8.97s  f681   11.35s  2.38s  OVERALL: ONE JUDGMENT, NOT AN AVERAGE. + 6 numbers (6.5 5.5 4 3.5 4 —)
  target      f719   11.98s  f841   14.02s  2.03s  STEP 3: EVERY GROUP TO 8 OR BETTER. + a column of 8+
  round4      f1031  17.18s  f1171  19.52s  2.33s  ROUND 4, six overall scores (7.5 x4, 7, 7), CLOSE. NOT 8 YET.; static loop strip
  families    f1241  20.68s  f1369  22.82s  2.13s  THEN EVERY MENU: 27 FAMILIES. + board overview (gold 8s; 7.5, 7.5, 5.5 framed); tile = overall
  all8        f1390  23.17s  f1517  25.28s  2.12s  ALL 27 AT 8 (4 words)
  turn        f1559  25.98s  f1738  28.97s  2.98s  THEN WE RAISED THE BAR. / ROAD TO 9 / 9 MEANS PRODUCTION POLISH. (12 words) + TARGET 9 chip
  pass1       f1793  29.88s  f1928  32.13s  2.25s  PASS 1: POLISH. + quote (8 words) + HUB 8.5, FAMILIES AT 9: 0 / 27
  review      f2001  33.35s  f2131  35.52s  2.17s  A FRESH AI REVIEW LOWERED THE SCORES. + kicker; HUB 8 (red); four red tiles; the marked-up picture
  structure   f2218  36.97s  f2352  39.20s  2.23s  PASS 2: STRUCTURE. + quote (8 words) + HUB 9 + 13 / 27, 13 gold tiles
  sentback    f2375  39.58s  f2500  41.67s  2.08s  ANOTHER REVIEW SENT ONE 9 BACK. + EDITOR PROJECTS: SENT BACK (no count shown)
  finish      f2586  43.10s  f2746  45.77s  2.67s  PASS 3 headline + SETTINGS 9 + 26 / 27 + TIME ATTACK: ONE KEY HINT LEFT
  result      f2851  47.52s  f3024  50.40s  2.88s  27 / 27 AT 9 OVERALL; follow-up kicker; A1 HUB 9 on each criterion, OVERALL 9, "was 8.5" under spacing and icons; THE HUB: 9 ON EACH CRITERION. (6 words)
  delivered   f3043  50.72s  f3134  52.23s  1.52s  THE SAME SIX GROUPS, DELIVERED · 29 OCT + the six labels from chapter 1; the hub cell is the follow-up still, labelled FOLLOW-UP STILL
  endcard     f3166  52.77s  f3342  55.70s  2.93s  title, line, URL, status, credit, disclaimer (about 40 words)
  (Measured by `edit.py reads`; the accepted hill-climb story held the same states 0.02-1.48 s, seven of them
  under 0.2 s: `old_holds.py`.)

Commands (Python with numpy + Pillow; OPENGGF_WORKTREE = a tree with tools/media/promo_kit.py):
  edit.py check | reads | readsheet MASTER | sheet [step] | frames N... | keys B... | preview A B | master |
  mp4 | remix | loudness | lists
"""
import csv
import json
import math
import os
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
REV = HERE.parents[1]                              # revisions/readable-holds
ROOT = HERE.parents[3]                             # the original production root (clips, sfx, ui tones)
EVID = Path(os.environ.get('MENU_EVIDENCE', str(ROOT.parent)))   # parent of the audit's evidence sets
KIT = Path(os.environ.get('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-e4055369')) / 'tools/media'
sys.path.insert(0, str(KIT))
import promo_kit  # noqa: E402
from promo_kit import (Edit, Custom, Fn, Flash, Fade, paste, text, rounded, clamp, ease_out, smooth, back,  # noqa: E402
                       write_wav)

W, H, FPS = 1920, 1080, 60
BEAT = 24.576
BPM = 3600 / BEAT
CLIPS = ROOT / 'clips'
SFX = ROOT / 'audio/sfx'
UI = ROOT / 'audio/ui'
MUSIC = ROOT / 'revisions/super-sonic-cut/audio/music/s2-music-93-paced.wav'   # the exact bed, reused in place
MUSIC_SHA256 = '2fa5b72f9ddfbd816de78849e06a11a4a851e81e136aad4d59b68d2c426c3830'
BED_FROM = 16                                       # bed beat at film frame 0 (A section, second phrase)
BED_STAB = 152                                      # the G-major stab after the fourth intro riff
BED_SRC_S = BED_FROM * BEAT / FPS
BED_LEN_S = ((BED_STAB - BED_FROM) * BEAT + (2566 - 104 * BEAT)) / FPS   # into the rest after the stab
BUILD = REV / 'build'
FINAL = REV / 'final'
FILM = FINAL / 'menu-evolution-readable-holds.mp4'
MASTER = FINAL / 'menu-evolution-readable-holds-master.mkv'
BADGE = KIT.parents[1] / 'src/main/resources/icon/openggf-256.png'
RESULT_ROW = HERE / 'result-row.json'
FREEZE = os.environ.get('READ_CHECK') == '1'        # reads check: footage and background held still

NAVY = (5, 16, 53)
NAVY2 = (10, 36, 92)
NAVY3 = (22, 52, 120)
DEEP = (2, 8, 28)
GOLD = (255, 214, 76)
PALE = (232, 237, 255)
LIGHT = (184, 196, 229)
WHITE = (255, 255, 255)
INK = (6, 12, 40)
RED = (226, 64, 76)
AMBER = (255, 160, 64)

F = lambda b: int(round(BEAT * b))      # film beat -> output frame
END_HIT = F(136)                        # the stab (bed beat 152)
TOTAL = END_HIT + 36                    # 3378 frames
BED_CUT = int(BED_LEN_S * FPS)          # 3352: bed ends (10 ms fade) in the rest after the stab
UI_GAIN = float(os.environ.get('UI_GAIN', '0.7'))
SAY_IN, SAY_OUT = 14, 8                 # statement entrance / exit frames

# ------------------------------------------------------------------------------------ the record
# docs/architecture/audits/2026-10-27-menu-design-review.md at d823ce643. Subjective judgments from captures.
GROUPS = [  # key, label, take (the group's representative take in clips/<era>/)
    ('A', 'HUB & DIALOGS', 'hub'), ('B', 'SETTINGS', 'settings'), ('C', 'PICKERS & EDITORS', 'locate'),
    ('D', 'LIBRARIES', 'mods'), ('E', 'STARTUP NOTICES', 'legal'), ('F', 'IN-GAME OVERLAYS', 'shader')]
CRITERIA = ['TYPOGRAPHY', 'HIERARCHY', 'SPACING', 'COLOUR', 'ICONS', 'CONSISTENCY', 'CLARITY']
ROUND0 = {  # "Round 0 baseline" table: seven criteria, then overall
    'A': ([6, 7, 7, 7, 5, 6, 7], '6.5'), 'B': ([5, 6, 6, 6, 5, 6, 5], '5.5'), 'C': ([4, 4, 5, 5, 3, 3, 4], '4'),
    'D': ([3, 3, 4, 4, 2, 3, 4], '3.5'), 'E': ([5, 3, 4, 5, 2, 3, 5], '4'), 'F': (None, None)}   # F: "not yet captured"
ROUNDS = [  # overall per class after each round ("Round 1..4 scores" tables); F first scored in round 3
    {'A': '6.5', 'B': '5.5', 'C': '4', 'D': '3.5', 'E': '4', 'F': '—'},
    {'A': '7', 'B': '5.5', 'C': '6.5', 'D': '6.5', 'E': '7', 'F': '—'},
    {'A': '7.5', 'B': '7', 'C': '6.5', 'D': '6.5', 'E': '7', 'F': '—'},
    {'A': '7.5', 'B': '7', 'C': '7.5', 'D': '7.5', 'E': '7', 'F': '6'},
    {'A': '7.5', 'B': '7.5', 'C': '7.5', 'D': '7.5', 'E': '7', 'F': '7'}]
# The 27 families of the toward-9 matrices, in their groups (Stageplay chrome sits with the editor overlays,
# as class F listed Stageplay and editor menus; Time Attack is the bundled mod, class H, added in the 8 pass).
ROWS = [('HUB & DIALOGS', ['A1 Hub', 'A2 Paused card', 'A3 Prompts', 'A4 Missing ROM', 'A5 Help', 'A6 Add games',
                           'A7 Tools']),
        ('SETTINGS', ['B1 Settings', 'B2 Controls', 'B3 Advanced', 'B4 Game Setup', 'B5 Save prompts']),
        ('PICKERS & EDITORS', ['C1 File browser', 'C2 Keypads', 'C3 Details']),
        ('LIBRARIES', ['D1-6 Playback', 'D7-9 Mod manager', 'D10 Import']),
        ('STARTUP NOTICES', ['E1-2 Notices']),
        ('IN-GAME OVERLAYS', ['F1 Shader picker', 'F2 Mutator Lab', 'F3 Editor projects', 'F4 Editor HUD',
                              'F5 Toast', 'F6-10 HUD plates', 'SP Stageplay']),
        ('TIME ATTACK (BUNDLED MOD)', ['TA Time Attack'])]
FAM = [f for _, fs in ROWS for f in fs]
assert len(FAM) == 27


def fam_values(base, **over):
    v = {f: base for f in FAM}
    for k, x in over.items():
        v[next(f for f in FAM if f.split()[0].replace('-', '_') == k)] = x
    return v


PASSES = {
    # All-menus target 8 (final matrix + completion + final families): every family 8. Stragglers on the way:
    # F4 Editor HUD 7.5 (final matrix), Stageplay chrome 7.5 and Time Attack 5.5 (completion round matrix).
    't8_pre': fam_values('8', F4='7.5', SP='7.5', TA='5.5'),
    't8': fam_values('8'),
    # Lead acceptance: every family 9 overall (d823ce643); the criteria keep their 8.5 entries
    'lead': fam_values('9'),
}
# Hill climb toward 9, "Score matrix (toward 9)": these five rose to 8.5; "No family reached 9 overall in this pass."
P1_UP = ('A1 Hub', 'A5 Help', 'F4 Editor HUD', 'F5 Toast', 'SP Stageplay')
# Fresh critical review: "crowded 320-wide hub, help, editor command sheet and Stageplay remain at 8"
REV_DOWN = ('A1 Hub', 'A5 Help', 'F4 Editor HUD', 'SP Stageplay')
# Structural pass matrix: "Thirteen families reach 9 overall; fourteen stay at 8.5."
STR9 = [f for f in FAM if f.split()[0] in ('A1', 'A3', 'A4', 'A5', 'A7', 'B2', 'B4', 'B5', 'D10', 'E1-2', 'F3', 'F4',
                                          'F5')]
assert len(STR9) == 13
# Independent structural review: "It rejected the open-project page's claimed 9" (F3 Editor projects).
SENT = 'F3 Editor projects'
# Finish pass: "Twenty-six families reach 9; Time Attack stays 8.5" (the keyboard cap A: OPEN)
FIN9 = [f for f in FAM if f != 'TA Time Attack']
assert len(FIN9) == 26


def result_row():
    """The final criteria row (result-row.json): the one block to replace from a newer verified source."""
    r = json.loads(RESULT_ROW.read_text())
    assert list(r['criteria']) == CRITERIA, 'result-row.json must list the seven criteria in order'
    return r


def caveat_line(r):
    vals = [float(v) for v in r['criteria'].values()]
    low = [n for n, v in zip(CRITERIA, vals) if v < 9]
    if not low:     # scoped to the row's family: other families keep their own criterion entries
        return f'{r["subject"]}: 9 ON EACH CRITERION.'
    names = ' AND '.join(low) if len(low) <= 2 else ', '.join(low[:-1]) + ' AND ' + low[-1]
    lv = sorted({r['criteria'][n] for n in low})
    return f'{r["overall"]} OVERALL. {names} STILL {lv[0] if len(lv) == 1 else "BELOW 9"}.'


# ------------------------------------------------------------------------------- evidence stills
T9 = 'menu-target9-20261028'
STILL = {   # the review's own captures (320x224 unless noted); provenance/source-map.json has heads and hashes
    'hub_t8': f'{T9}/baseline/320/hub/38-hub-crowded.png',                    # a694db926, the delivered 8
    'hub_p1': f'{T9}/final/320/hub/38-hub-crowded.png',                       # toward-9 pass-1 tree (ea7df pixels)
    'hub_rev': f'{T9}/review-opus55/hub38-320-annotated.png',                 # 960x672: the reviewer's mark-up
    'hub_str': f'{T9}/structural/final/320/hub/38-hub-crowded.png',           # d8d947336
    'set_str': f'{T9}/structural/final/320/hub/11-settings.png',              # d8d947336
    'hub_fu': 'hub-criteria-nine-20261029/final/320/hub/01-hub.png',          # d6771c478: the hub after its follow-up
}


@lru_cache(maxsize=None)
def still(key):
    return np.asarray(Image.open(EVID / STILL[key]).convert('RGB'), np.float32)


# ------------------------------------------------------------------------------- clip access


class Clip:
    def __init__(self, era, take):
        self.era, self.take = era, take
        self.dir = CLIPS / era / take
        self.n = len(list((self.dir / 'frames').glob('*.png')))
        if not self.n:
            raise FileNotFoundError(self.dir)

    @lru_cache(maxsize=64)
    def native(self, i):
        if FREEZE:      # the reads check holds every take on one frame so only editorial motion remains
            i = 100
        i = int(clamp(i, 0, self.n - 1))
        return np.asarray(Image.open(self.dir / 'frames' / f'{i:05d}.png').convert('RGB'), np.float32)

    def cues(self):
        return [(int(r['frame']), r['detail']) for r in csv.DictReader((self.dir / 'events.csv').open())
                if r['kind'] == 'cue']


@lru_cache(maxsize=None)
def clip(era, take):
    return Clip(era, take)


def up(a, s):
    return np.repeat(np.repeat(a, s, axis=0), s, axis=1)


# ------------------------------------------------------------------------------------ schedule
# ch1 the ask
ASK_IN = 0
WALL_DROP = 2                                   # frames between cell drops
WALL_FALL = 10                                  # frames a cell takes to land
STEP1_T = F(6.25)
LABEL_T = [STEP1_T + 4 + 3 * k for k in range(6)]   # group labels land on their cells
LABEL_POP = 6
# ch2 the rubric
MATRIX_T = F(12.5)                              # labels fly to the matrix rows
STEP2_T = F(12.75)
CELLS_T = F(13)
NYP_T = F(14)
WALL_OUT = F(14.5)                              # the round-0 wall has faded out (shortest take, legal, 420 frames)
OVERALL_T = F(20.5)
# ch3 the goal
TARGET_T = F(28)
# ch4 rounds 1-4
ROUNDS_T = F(34.5)
LAPS = [  # (change, recapture, rescore, keep) beats per round: lap 1 slow enough to name each step
    (35.25, 36.75, 37.25, 37.75), (38.25, 39.25, 39.5, 39.75), (40.0, 40.25, 40.5, 40.75), (40.875, 41.0, 41.125, 41.25)]
RESCORE = [F(lap[2]) for lap in LAPS]
LIB_SWEEP = (F(35.25), F(36.5))
LEGAL_T = F(38.25)
LEGAL_SWEEP = (F(38.25), F(39.25))
NOT8_T = F(41.5)
# ch5-7 every family, all at 8, the turn
FAMILIES_T = F(47.5)
FAMILIES_HEAD = F(47.75)
TILE_ON = F(48)
STRAG_T = F(50.25)
ALL8 = F(56)
TURN = F(62)
# ch8-12 the road to 9
PASS1_T = F(71)
P1 = F(72.25)
P1_QUOTE = F(72.5)
REV_T = F(78.75)
DROP = F(80.75)
STR_T = F(87)
STR_SWEEP = (F(87.75), F(89))
HUB9 = F(89.25)
WAVE13 = F(89.5)
SENTBACK = F(96)
PASS3_T = F(102)
SET_SWEEP = (F(102.75), F(104))
WAVE26 = F(104.25)
TA_T = F(105)
# ch13 the result, delivered, end card
SLAM = F(112)
CRIT_T = F(115)
IRIS = F(123)
END_T = F(127.5)
WAVE = 18                                       # frames for a left-to-right tile wave

# take in-points: (era(s), take, output start, output end, take frame at output start)
SRC = {
    'lib':     ('pre+new', 'mods', ROUNDS_T, LEGAL_T, 53),        # the manager list (ENTER at 52, next ENTER at 158)
    'notice':  ('pre+new', 'legal', LEGAL_T, FAMILIES_T + 14, 0),
    'set_fin': ('new', 'settings', PASS3_T, SLAM + 14, 86),       # take 86 = a513dd5fd 11-settings (0.01 % differ)
}
WALL_PRE = {'hub': 160, 'settings': 100, 'locate': 40, 'mods': 53, 'legal': 0, 'shader': 145}   # at frame 0
WALL_NEW = {'hub': 160, 'settings': 86, 'locate': 40, 'mods': 53, 'legal': 0, 'shader': 145}    # at the iris


def src(key, f):
    return SRC[key][4] + f - SRC[key][2]


# ---------------------------------------------------------------------------------- the stage


@lru_cache(maxsize=None)
def _stage_base():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    g = (ys / H)[..., None]
    base = np.array(DEEP, np.float32) * g + np.array(NAVY, np.float32) * (1 - g)
    return base, xs + 0.42 * ys


def stage(f):
    base, diag = _stage_base()
    band = ((diag - (0 if FREEZE else f) * 1.6) // 90) % 2
    return base + band[..., None] * np.array((4, 8, 18), np.float32)


def box(c, x, y, w, h, colour, alpha=1.0):
    x0, y0, x1, y1 = max(0, int(x)), max(0, int(y)), min(W, int(x + w)), min(H, int(y + h))
    if x0 < x1 and y0 < y1 and alpha > 0:
        c[y0:y1, x0:x1] = c[y0:y1, x0:x1] * (1 - alpha) + np.array(colour, np.float32) * alpha


def frame_rect(c, x, y, w, h, colour, t=6, alpha=1.0):
    box(c, x - t, y - t, w + 2 * t, t, colour, alpha)
    box(c, x - t, y + h, w + 2 * t, t, colour, alpha)
    box(c, x - t, y, t, h, colour, alpha)
    box(c, x + w, y, t, h, colour, alpha)


def put(c, img, x, y, border=6, colour=GOLD):
    """An exact integer image (already scaled) with a gold frame."""
    h, w = img.shape[:2]
    if border:
        frame_rect(c, x, y, w, h, colour, border)
    c[y:y + h, x:x + w] = img


def compare_native(old, new, d):
    d = int(clamp(round(d), 0, old.shape[1]))
    out = old.copy()
    out[:, :d] = new[:, :d]
    return out


def divider(c, x, y, d, s, h=224):
    if 0 < d < 320:
        px = x + int(round(d)) * s
        box(c, px - 4, y - 10, 8, h * s + 20, GOLD)
        box(c, px - 1, y - 10, 2, h * s + 20, WHITE)


def over(dst, src_, x, y, alpha=1.0):
    x, y = int(round(x)), int(round(y))
    h, w = src_.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if x0 >= x1 or y0 >= y1 or alpha <= 0:
        return
    s = src_[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    sa = s[..., 3:4] / 255 * alpha
    da = d[..., 3:4] / 255
    oa = sa + da * (1 - sa)
    d[..., :3] = (s[..., :3] * sa + d[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6)
    d[..., 3:4] = oa * 255


@lru_cache(maxsize=None)
def pill(label, size=40, fg=INK, bg=GOLD, role='title_it'):
    t = text(label, role, size, fg)
    p = rounded(t.shape[1] + 36, t.shape[0] + 6, 12, bg).copy()
    over(p, t, 18, 3)
    return p


def appear(t, dur=12):
    return clamp(t / dur)


def say(c, f, t0, t1, s, y, size=96, colour=WHITE, role='title', x=None, kicker=None, kcol=LIGHT):
    """A statement line: enters upward over SAY_IN frames, leaves over SAY_OUT (faster than it came)."""
    if not t0 <= f < t1:
        return
    t = f - t0
    a = clamp(t / 10) * clamp((t1 - f) / SAY_OUT)
    dy = (1 - ease_out(clamp(t / SAY_IN))) * 40
    img = text(s, role, size, colour, stroke=max(3, size // 18), sfill=INK, shadow=max(4, size // 14))
    px = W / 2 - img.shape[1] / 2 if x is None else x
    if kicker:
        k = text(kicker, 'sub', 30, kcol, tracking=6)
        paste(c, k, W / 2 - k.shape[1] / 2 if x is None else x, y - 40 + dy, a)
    paste(c, img, px, y + dy, a)


def quote(c, f, t0, t1, s, who, y=948):
    """A verbatim sentence of the design review, in quotation marks with its source."""
    if not t0 <= f < t1:
        return
    t = f - t0
    a = clamp(t / 10) * clamp((t1 - f) / SAY_OUT)
    q = text(f'“{s}”', 'body_it', 46, PALE, stroke=3, sfill=INK, shadow=4)
    w_ = text(who, 'sub', 30, GOLD, stroke=2, sfill=INK, shadow=3)
    paste(c, q, W / 2 - q.shape[1] / 2, y + (1 - ease_out(clamp(t / SAY_IN))) * 30, a)
    paste(c, w_, W / 2 - w_.shape[1] / 2, y + q.shape[0] - 4, a)


# ---------------------------------------------------------------------------- score graphics


def heat(v):
    """Cell colour for a score: review red at the bottom, navy through the middle, gold at the top."""
    stops = [(2, (150, 34, 62)), (4, (168, 70, 58)), (5.5, (40, 62, 140)), (7, (44, 86, 170)),
             (8, (196, 160, 70)), (9, GOLD)]
    v = float(v)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if v <= b:
            u = clamp((v - a) / (b - a))
            return tuple(ca[k] + (cb[k] - ca[k]) * u for k in range(3))
    return GOLD


def roll(c, s_old, s_new, x, y, t, size=200, colour=GOLD, dur=12, alpha=1.0, anchor='left'):
    """Slot-machine roll between two recorded values (never an invented one in between)."""
    u = clamp(t / dur)
    img_new = text(s_new, 'title', size, colour, stroke=max(4, size // 22), sfill=INK, shadow=max(5, size // 18))
    if anchor == 'right':
        x = x - img_new.shape[1]
    if u >= 1 or s_old is None or s_old == s_new:
        paste(c, img_new, x, y, alpha)
        return img_new.shape
    img_old = text(s_old, 'title', size, colour, stroke=max(4, size // 22), sfill=INK, shadow=max(5, size // 18))
    h = img_new.shape[0]
    e = ease_out(u)
    slot = np.zeros((h, max(img_new.shape[1], img_old.shape[1]), 4), np.float32)
    down = float(s_new) < float(s_old) if s_old not in ('—', '?') and s_new not in ('—', '?') else False
    if down:   # a score going down leaves downward
        over(slot, img_old, 0, int(e * h))
        over(slot, img_new, 0, -int((1 - back(u, 1.3)) * h))
    else:
        over(slot, img_old, 0, -int(e * h))
        over(slot, img_new, 0, int((1 - back(u, 1.3)) * h))
    paste(c, slot, x, y, alpha)
    return img_new.shape


# matrix geometry (ch2/ch3 and the final criteria row): groups down, seven criteria across
MX = 50                                     # left edge of the row labels
MCOL0, MCOLW = 400, 156                     # first criterion column, column pitch
MOVX, MOVW = MCOL0 + 7 * MCOLW + 12, 170    # overall column
MTGX, MTGW = MOVX + MOVW + 14, 180          # target column
MROW0, MROWH = 392, 86
HEAD_SIZE = 38


def criteria_headers(c, y_row, alpha_of, names=CRITERIA, colour=PALE):
    """The seven criterion names, staggered on two tiers so every word is whole at a readable size."""
    for j, name in enumerate(names):
        a = alpha_of(j)
        if a <= 0:
            continue
        hd = text(name, 'title_it', HEAD_SIZE, colour, stroke=2, sfill=INK, shadow=2)
        cx = MCOL0 + j * MCOLW + MCOLW / 2
        top = y_row - (108 if j % 2 == 0 else 62)
        paste(c, hd, cx - hd.shape[1] / 2, top, a)
        if j % 2 == 0:   # a tick from the upper tier down to its column
            box(c, cx - 1, top + hd.shape[0] + 2, 3, 108 - hd.shape[0] - 14, LIGHT, 0.6 * a)


def cell(c, x, y, v, a, size=46, dark=False):
    box(c, x, y, MCOLW - 12, MROWH - 10, heat(v), 0.94 * a)
    n = text(f'{float(v):g}', 'title', size, INK if dark else WHITE, stroke=0 if dark else 3, sfill=INK)
    paste(c, n, x + (MCOLW - 12) / 2 - n.shape[1] / 2, y + (MROWH - 10) / 2 - n.shape[0] / 2 + 2, a)


def label_anchor_wall(k):
    return (k % 3) * 640 + 16, 92 + (k // 3) * 448 + 448 - 66


def label_anchor_matrix(k):
    p = pill(GROUPS[k][1], 36)
    return MX, MROW0 + k * MROWH + (MROWH - 10) / 2 - p.shape[0] / 2


def matrix(c, f):
    """The round-0 score matrix, then the overall column, then the target."""
    dim = 1 - 0.62 * smooth(clamp((f - OVERALL_T) / 8)) if f >= OVERALL_T else 1.0
    criteria_headers(c, MROW0, lambda j: appear(f - (CELLS_T + 4 * j), 8) * (0.55 + 0.45 * dim))
    for j in range(7):
        for k, (g, _, _) in enumerate(GROUPS):
            vals = ROUND0[g][0]
            tk = f - (CELLS_T + 4 * j + 2 * k)
            if vals is None or tk < 0:
                continue
            cell(c, MCOL0 + j * MCOLW + 6, MROW0 + k * MROWH, vals[j], appear(tk, 8) * dim)
    tj = f - NYP_T
    if tj >= 0:   # overlays row: not pictured in round 0
        y = MROW0 + 5 * MROWH
        a = appear(tj, 8) * (0.4 + 0.6 * dim)
        box(c, MCOL0 + 6, y, 7 * MCOLW - 12, MROWH - 10, NAVY2, 0.8 * a)
        nyp = text('NOT YET PICTURED IN ROUND 0', 'title_it', 40, LIGHT, stroke=2, sfill=INK)
        paste(c, nyp, MCOL0 + 7 * MCOLW / 2 - nyp.shape[1] / 2, y + (MROWH - 10) / 2 - nyp.shape[0] / 2, a)
    to = f - (OVERALL_T + 6)
    if to >= 0:   # the overall column: one holistic judgment per group
        hd = text('OVERALL', 'title_it', 40, GOLD, stroke=3, sfill=INK, shadow=3)
        paste(c, hd, MOVX + MOVW / 2 - hd.shape[1] / 2, MROW0 - 62, appear(to, 8))
        for k, (g, _, _) in enumerate(GROUPS):
            tk = to - 4 * k
            if tk < 0:
                continue
            v = ROUND0[g][1] or '—'
            y = MROW0 + k * MROWH
            box(c, MOVX, y - 4, MOVW, MROWH - 2, INK, 0.75)
            frame_rect(c, MOVX, y - 4, MOVW, MROWH - 2, GOLD, 3)
            s = 1 + 0.5 * (1 - ease_out(clamp(tk / 10)))
            n = text(v, 'title', 76, GOLD if v != '—' else LIGHT, stroke=4, sfill=INK, shadow=5)
            n = promo_kit.scaled(n, s) if s != 1 else n
            paste(c, n, MOVX + MOVW / 2 - n.shape[1] / 2, y + (MROWH - 6) / 2 - n.shape[0] / 2, clamp(tk / 3))
    tt = f - (TARGET_T + 6)
    if tt >= 0:
        hd = text('TARGET', 'title_it', 40, WHITE, stroke=3, sfill=INK, shadow=3)
        paste(c, hd, MTGX + MTGW / 2 - hd.shape[1] / 2, MROW0 - 62, appear(tt, 8))
        for k in range(6):
            tk = tt - 3 * k
            if tk < 0:
                continue
            y = MROW0 + k * MROWH
            n = text('8+', 'title', 64, WHITE, stroke=4, sfill=INK, shadow=5)
            paste(c, n, MTGX + MTGW / 2 - n.shape[1] / 2,
                  y + (MROWH - 6) / 2 - n.shape[0] / 2 + (1 - ease_out(clamp(tk / 10))) * 30, appear(tk, 8))


LOOP = ['CHANGE', 'RECAPTURE', 'RESCORE', 'KEEP OR REVERT']


def loop_strip(c, cx, y, active, size=34):
    """The hill-climb loop as a static strip; only the lit step moves."""
    parts = [pill(f'{k + 1}  {s}', size, INK if active == k else PALE, GOLD if active == k else NAVY3)
             for k, s in enumerate(LOOP)]
    arrow = text('→', 'title', size + 4, GOLD, stroke=2, sfill=INK)
    lab = text('EVERY ROUND', 'sub', 28, LIGHT, tracking=5)
    total = lab.shape[1] + 24 + sum(p.shape[1] for p in parts) + 3 * (arrow.shape[1] + 24)
    xx = cx - total / 2
    paste(c, lab, xx, y + parts[0].shape[0] / 2 - lab.shape[0] / 2)
    xx += lab.shape[1] + 24
    for k, p in enumerate(parts):
        paste(c, p, xx, y)
        xx += p.shape[1] + 12
        if k < 3:
            paste(c, arrow, xx, y - 3)
            xx += arrow.shape[1] + 12


# --------------------------------------------------------------------------- the family boards


def tile_board(c, f, values, target, x0, y0, labw, tw, th, gap, rowh, lab_size, num_size, order_t0=None, step=2,
               numbers=True, alpha=1.0):
    """The 27 families in their group rows, each tile one family's OVERALL score; gold = meets the target.
    order_t0 animates tiles turning on in reading order, one every `step` frames."""
    n = 0
    for r, (label, fams) in enumerate(ROWS):
        y = y0 + r * rowh
        if labw:
            lab = text(label, 'title_it', lab_size, PALE, stroke=2, sfill=INK, shadow=2)
            paste(c, lab, x0, y + th / 2 - lab.shape[0] / 2, alpha)
        for i, fam in enumerate(fams):
            x = x0 + labw + i * (tw + gap)
            v = values[fam]
            shown = order_t0 is None or f >= order_t0 + step * n
            n += 1
            met = shown and float(v) >= target
            box(c, x, y, tw, th, GOLD if met else (NAVY3 if shown else NAVY), 0.95 * alpha)
            if shown and numbers:
                num = text(v, 'title', num_size, INK if met else WHITE, stroke=0 if met else 3, sfill=INK)
                paste(c, num, x + tw / 2 - num.shape[1] / 2, y + th / 2 - num.shape[0] / 2 + 2, alpha)


BIG = dict(x0=70, y0=262, labw=520, tw=176, th=86, gap=12, rowh=100, lab_size=42, num_size=56)
SMALL = dict(x0=1052, y0=520, tw=80, th=44, gap=8, rowh=54)


def tile_xy(fam, g=BIG):
    r = next(i for i, (_, fs) in enumerate(ROWS) if fam in fs)
    i = ROWS[r][1].index(fam)
    return g['x0'] + g.get('labw', 0) + i * (g['tw'] + g['gap']), g['y0'] + r * g['rowh'], i


def board_head(c, target):
    """The board's two fixed labels: what a tile is, and the target."""
    hp = pill('EACH TILE: ONE FAMILY’S OVERALL SCORE', 34, PALE, NAVY3)
    paste(c, hp, BIG['x0'], 200)
    chip_ = pill(f'TARGET {target}', 44, INK, GOLD if target == 8 else WHITE)
    paste(c, chip_, W - 60 - chip_.shape[1], 196)


# -------------------------------------------------------------------------------- the chapters


def wall_cells(c, f, era, s0s, t_in, dim=0.0, drop=True):
    for k, (g, label, take) in enumerate(GROUPS):
        t0 = t_in + WALL_DROP * k if drop else t_in
        if f < t0:
            continue
        x, y = (k % 3) * 640, 92 + (k // 3) * 448
        dy = int(round((1 - ease_out(clamp((f - t0) / WALL_FALL))) * -500)) if drop else 0
        img = up(clip(era, take).native(s0s[take] + f - t_in), 2)
        yy = y + dy
        top = max(0, 92 - yy) if k < 3 else 0
        if yy + 448 > 0:
            c[yy + top:yy + 448, x:x + 640] = img[top:]
            if dim:
                c[max(92, yy):yy + 448, x:x + 640] *= 1 - dim
    # seams between cells, so six menus read as six things
    a = 0.9 * (clamp((f - t_in - WALL_DROP * 5 - WALL_FALL) / 6) if drop else 1.0)
    if f >= t_in and a > 0:
        box(c, 638, 92, 4, 896, GOLD, a)
        box(c, 1278, 92, 4, 896, GOLD, a)
        box(c, 0, 538, W, 4, GOLD, a)


def ch_assignment(f, shot, edit):
    """b0-34.5: the ask, the rubric, the goal (one continuous screen so the labels can travel)."""
    c = stage(f)
    wall_dim = 0.55 * (1 - smooth(clamp((f - STEP1_T) / 8)))
    if f >= MATRIX_T:
        wall_dim = 0.55 + 0.32 * smooth(clamp((f - MATRIX_T) / 10))
        wall_dim += (1 - wall_dim) * smooth(clamp((f - WALL_OUT + 16) / 16))
    if f < WALL_OUT:
        wall_cells(c, f, 'pre', WALL_PRE, 0, dim=wall_dim)
    if f < STEP1_T:     # a band behind the opening statement
        box(c, 0, 380, W, 230, DEEP, 0.78 * clamp((f + 1) / 8) * clamp((STEP1_T - f) / 8))
    if f >= MATRIX_T:   # a navy wash under the matrix
        box(c, 0, 0, W, H, DEEP, 0.55 * smooth(clamp((f - MATRIX_T) / 10)))
    for k, (g, label, take) in enumerate(GROUPS):   # labels land on their cells, then fly to the rows
        t0 = LABEL_T[k]
        if f < t0:
            continue
        p = pill(label, 36)
        ax, ay = label_anchor_wall(k)
        if f >= MATRIX_T:
            u = ease_out(clamp((f - MATRIX_T - 2 * k) / 14))
            bx, by = label_anchor_matrix(k)
            ax, ay = ax + (bx - ax) * u, ay + (by - ay) * u
        s = 1 + 0.4 * (1 - ease_out(clamp((f - t0) / LABEL_POP)))
        paste(c, promo_kit.scaled(p, s) if s != 1 else p, ax, ay, clamp((f - t0) / 3))
    if f >= MATRIX_T:
        matrix(c, f)
    return c


def ch_assignment_text(c, f, o, edit):
    say(c, f, ASK_IN, STEP1_T, 'WE GAVE AN AI EVERY OPENGGF MENU.', 470, size=110, kicker='CLAUDE OPUS  ·  27 OCT 2026')
    say(c, f, STEP1_T, MATRIX_T, 'STEP 1: SORT THEM INTO SIX GROUPS.', 14, size=66)
    say(c, f, STEP2_T, OVERALL_T, 'STEP 2: SCORE EACH GROUP ON SEVEN CRITERIA.', 120, size=84,
        kicker='1 TO 10  ·  JUDGED FROM SCREENSHOTS')
    say(c, f, OVERALL_T, TARGET_T, 'OVERALL: ONE JUDGMENT, NOT AN AVERAGE.', 120, size=84,
        kicker='PLUS ONE OVERALL SCORE PER GROUP')
    say(c, f, TARGET_T, ROUNDS_T, 'STEP 3: EVERY GROUP TO 8 OR BETTER.', 120, size=84, kicker='THE TARGET')


# ch4: rounds 1-4 --------------------------------------------------------------------------------
PANE_L = (56, 92)
COL_X = 1392


def round_at(f):
    return sum(1 for t in RESCORE if f >= t)


def lap_step(f):
    st = None
    for lap in LAPS:
        for i, b in enumerate(lap):
            if f >= F(b):
                st = i
    return st


def six_rows(c, f, x, y):
    """Overall per group after the current round, rolling at each rescore."""
    r = round_at(f)
    t = f - RESCORE[r - 1] if r else 99
    for k, (g, label, _) in enumerate(GROUPS):
        yy = y + k * 104
        paste(c, pill(label, 30, PALE, NAVY3), x, yy + 18)
        roll(c, ROUNDS[r - 1][g] if r else None, ROUNDS[r][g], W - 40, yy - 6, t, size=86, colour=WHITE, dur=10,
             anchor='right')


def era_tabs(c, x, y, d, s, before, now):
    pb, pn = pill(before, 36, bg=LIGHT), pill(now, 36)
    top = y - 6 - 10 - pb.shape[0]
    if d <= 0:
        paste(c, pb, x, top)
    elif d >= 320:
        paste(c, pn, x, top)
    else:
        px = x + int(round(d)) * s
        paste(c, pn, px - 14 - pn.shape[1], top)
        paste(c, pb, px + 14, top)


def sweep(f, t0, t1):
    return 320 * smooth(clamp((f - t0) / max(1, t1 - t0)))


def ch_rounds(f, shot, edit):
    c = stage(f)
    x, y = PANE_L
    if f < LEGAL_T:
        key, (t0, t1) = 'lib', LIB_SWEEP
    else:
        key, (t0, t1) = 'notice', LEGAL_SWEEP
    take = SRC[key][1]
    i = src(key, f)
    d = sweep(f, t0, t1)
    put(c, up(compare_native(clip('pre', take).native(i), clip('new', take).native(i), d), 4), x, y)
    divider(c, x, y, d, 4)
    era_tabs(c, x, y, d, 4, 'ROUND 0 · 27 OCT', 'AT 8 · 28 OCT')
    for lap in LAPS:   # recapture: the camera flash on the pane's frame
        k = f - F(lap[1])
        if 0 <= k < 8:
            frame_rect(c, x, y, 1280, 896, WHITE, 6 + int(10 * (1 - k / 8)))
    loop_strip(c, x + 640, 1006, lap_step(f))
    r = round_at(f)
    paste(c, text(f'ROUND {r}', 'title', 100, WHITE, stroke=5, sfill=INK, shadow=6), COL_X, 104)
    six_rows(c, f, COL_X, 262)
    t = f - NOT8_T
    if t >= 0:
        img = text('CLOSE. NOT 8 YET.', 'title_it', 56, AMBER, stroke=4, sfill=INK, shadow=4)
        paste(c, img, COL_X, 900 + (1 - ease_out(clamp(t / SAY_IN))) * 30, clamp(t / 10))
    return c


# ch5-7: every family, all at 8, the turn ---------------------------------------------------------


def ch_families(f, shot, edit):
    c = stage(f)
    vals = PASSES['t8'] if f >= ALL8 else PASSES['t8_pre']
    tile_board(c, f, vals, 8.0, order_t0=TILE_ON if f < ALL8 else None, **BIG)
    if f >= TURN:       # every tile falls below the new target, a sweep from the left
        cover = stage(f)
        tile_board(cover, f, vals, 9.0, **BIG)
        edge = int(W * smooth(clamp((f - TURN) / WAVE)))
        c[:, :edge] = cover[:, :edge]
    if STRAG_T <= f < ALL8:   # the three below 8
        for fam in ('F4 Editor HUD', 'SP Stageplay', 'TA Time Attack'):
            bx, by, _ = tile_xy(fam)
            frame_rect(c, bx, by, BIG['tw'], BIG['th'], AMBER, 5, clamp((f - STRAG_T) / 6))
    board_head(c, 9 if f >= TURN else 8)
    return c


def ch_families_text(c, f, o, edit):
    say(c, f, FAMILIES_HEAD, ALL8, 'THEN EVERY MENU: 27 FAMILIES.', 96, size=84, kicker='THE ALL-MENUS PASS')
    if ALL8 <= f < TURN:
        t = f - ALL8
        fade = clamp((TURN - f) / SAY_OUT)
        box(c, 0, 0, W, H, DEEP, 0.55 * clamp(t / 6) * fade)
        img = text('ALL 27 AT 8', 'title', 210, WHITE, stroke=12, sfill=INK, shadow=14)
        s = 1 + 0.6 * (1 - ease_out(clamp(t / 12)))
        img = promo_kit.scaled(img, s) if s != 1 else img
        shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0
        paste(c, img, W / 2 - img.shape[1] / 2 + shake, 560 - img.shape[0] / 2, clamp(t / 3) * fade)


def turn_text(c, f, o, edit):
    """The turn: the bar raised, ROAD / TO / 9, and what 9 means, held together as one settled screen."""
    a = smooth(clamp((f - TURN) / 6))
    c *= 1 - 0.55 * a
    fade = clamp((PASS1_T - f) / SAY_OUT)
    for word, dt, y, xc in (('ROAD', 0, 380, 640), ('TO', 6, 600, 640)):
        t = f - (TURN + dt)
        if t < 0:
            continue
        img = text(word, 'title', 190, WHITE, stroke=10, sfill=INK, shadow=11)
        img = promo_kit.scaled(img, 0.4 + 0.6 * back(clamp(t / 10), 2.2))
        paste(c, img, xc - img.shape[1] / 2, y - img.shape[0] / 2, clamp(t / 3) * fade)
    t = f - (TURN + 12)
    if t >= 0:
        nine = text('9', 'title', 600, GOLD, stroke=14, sfill=INK, shadow=18)
        nine = promo_kit.scaled(nine, 1 + 0.35 * (1 - ease_out(clamp(t / 12))))
        paste(c, nine, 1240 - nine.shape[1] / 2, 540 - nine.shape[0] / 2, clamp(t / 3) * fade)
    t = f - (TURN + 24)
    if t >= 0:      # a band under the bottom line, so the dimmed board does not read through it
        box(c, 0, 830, W, 190, DEEP, 0.75 * clamp(t / 10) * fade)
    say(c, f, TURN + 4, PASS1_T, 'THEN WE RAISED THE BAR.', 66, size=76)
    say(c, f, TURN + 24, PASS1_T, '9 MEANS PRODUCTION POLISH.', 888, size=88, kicker='THE NEW TARGET  ·  28 OCT')


# ch8-12: the road to 9 ---------------------------------------------------------------------------
EP = (48, 228)          # evidence pane (3x, 960x672)


def wave_on(f, t0, i):
    return f >= t0 + int(round(WAVE * i / 6))


def road_state(f):
    """(gold families, red families, white-flash families with start, counter value or None, counter alpha)."""
    gold, red, flash = set(), set(), {}
    n, ca = 0, 1.0
    if P1 <= f < REV_T:
        flash = {k: (WHITE, P1) for k in P1_UP}
    elif REV_T <= f < STR_T and f >= DROP:
        red = set(REV_DOWN)
        flash = {k: (RED, DROP) for k in REV_DOWN}
    elif STR_T <= f < SENTBACK:
        gold = {k for k in STR9 if wave_on(f, WAVE13, tile_xy(k, SMALL)[2])}
        n = 13 if f >= WAVE13 else 0
    elif SENTBACK <= f < PASS3_T:
        gold = set(STR9) - {SENT}
        red = {SENT}
        flash = {SENT: (RED, SENTBACK)}
        n, ca = 13, 1 - clamp((f - SENTBACK) / 8)
    elif PASS3_T <= f:
        late = [k for k in FIN9 if k not in STR9 or k == SENT]      # the finish pass's 13, and the repaired F3
        gold = (set(STR9) - {SENT}) | {k for k in late if wave_on(f, WAVE26, tile_xy(k, SMALL)[2])}
        red = {SENT} if f < WAVE26 else set()
        n, ca = 26, clamp((f - WAVE26) / 8)
    return gold, red, flash, n, ca


def small_board(c, f):
    gold, red, flash, _, _ = road_state(f)
    for r, (_, fams) in enumerate(ROWS):
        for i, fam in enumerate(fams):
            x, y, _ = tile_xy(fam, SMALL)
            col = GOLD if fam in gold else (RED if fam in red and fam == SENT else NAVY3)
            box(c, x, y, SMALL['tw'], SMALL['th'], col, 0.95)
            if fam in red and fam != SENT:
                frame_rect(c, x, y, SMALL['tw'], SMALL['th'], RED, 3)
            if fam in flash:
                fc, t0 = flash[fam]
                k = f - t0
                if 0 <= k < 16:
                    p = 0.5 + 0.5 * math.cos(k * math.pi / 8)
                    box(c, x, y, SMALL['tw'], SMALL['th'], fc, 0.75 * p)


@lru_cache(maxsize=1)
def review_marks():
    base = up(still('hub_p1'), 3)
    mark = still('hub_rev')
    return base, mark, np.abs(mark - base).sum(axis=2) > 0


def pane_label(c, lab):
    pl = pill(lab, 36)
    paste(c, pl, EP[0], EP[1] - 6 - 10 - pl.shape[0])


def evidence(c, f):
    """The left pane: the hub picture through pass 1, review and fix; then Settings."""
    x, y = EP
    if f < P1:
        put(c, up(still('hub_t8'), 3), x, y)
        pane_label(c, 'THE CROWDED HUB  ·  AT 8')
    elif f < REV_T:
        put(c, up(still('hub_p1'), 3), x, y)
        pane_label(c, 'PASS 1: A SUMMARY LINE ADDED')
    elif f < STR_T:
        base, mark, diff = review_marks()
        u = smooth(clamp((f - REV_T - 4) / 37))
        reveal = diff & (np.arange(960)[None, :] < 960 * u)
        img = base.copy()
        img[reveal] = mark[reveal]
        put(c, img, x, y)
        pane_label(c, 'THE REVIEWER’S MARKED-UP CAPTURE')
    elif f < PASS3_T:
        old, new = still('hub_rev'), up(still('hub_str'), 3)
        d = sweep(f, *STR_SWEEP)
        img = old.copy()
        img[:, :int(round(d)) * 3] = new[:, :int(round(d)) * 3]
        put(c, img, x, y)
        divider(c, x, y, d, 3)
        era_tabs(c, x, y, d, 3, 'MARKED UP', 'REBUILT · 28 OCT')
        return 'hub'
    else:
        d = sweep(f, *SET_SWEEP)
        put(c, up(compare_native(still('set_str'), clip('new', 'settings').native(src('set_fin', f)), d), 3), x, y)
        divider(c, x, y, d, 3)
        era_tabs(c, x, y, d, 3, 'PASS 2', 'PASS 3 · DELIVERED')
        return 'settings'
    return 'hub'


SUBJECT = {  # (name, [(frame, value)]) for the big score beside the evidence
    'hub': ('HUB', [(0, '8'), (P1, '8.5'), (DROP, '8'), (HUB9, '9')]),
    'settings': ('SETTINGS', [(0, '8.5'), (SET_SWEEP[1], '9')]),
}


def subject(c, f, which):
    name, stops = SUBJECT[which]
    k = max(i for i, (t, _) in enumerate(stops) if f >= t or i == 0)
    x = 1052
    paste(c, text(name, 'title', 70, WHITE, stroke=4, sfill=INK, shadow=5), x, 222)
    prev = stops[k - 1][1] if k > 0 else None
    down = prev is not None and float(stops[k][1]) < float(prev)
    shape = roll(c, prev, stops[k][1], x - 4, 290, f - stops[k][0], size=180, colour=RED if down else GOLD, dur=12)
    ten = text('/10', 'title', 56, LIGHT, stroke=3, sfill=INK, shadow=4)
    paste(c, ten, x + shape[1] - 26, 290 + shape[0] - ten.shape[0] - 24)


def counter(c, f, n, alpha):
    if alpha <= 0:
        return
    x = 1420
    paste(c, text('FAMILIES AT 9', 'sub', 30, LIGHT, tracking=4), x, 230, alpha)
    if STR_T <= f < SENTBACK and f >= WAVE13:
        shape = roll(c, '0', '13', x, 262, f - WAVE13, size=150, colour=WHITE, dur=12, alpha=alpha)
    else:
        big = text(f'{n}', 'title', 150, WHITE, stroke=7, sfill=INK, shadow=8)
        paste(c, big, x, 262, alpha)
        shape = big.shape
    paste(c, text('/ 27', 'title', 80, LIGHT, stroke=4, sfill=INK, shadow=5), x + shape[1] + 10, 330, alpha)


def board_pill(c, f, fam, label, colour, fg, t0, t1, below=False):
    if not t0 <= f < t1:
        return
    bx, by, _ = tile_xy(fam, SMALL)
    p = pill(label, 34, fg, colour)
    a = clamp((f - t0) / 6) * clamp((t1 - f) / SAY_OUT)
    if below:
        paste(c, p, bx + SMALL['tw'] + 14, by + SMALL['th'] / 2 - p.shape[0] / 2, a)
    else:
        paste(c, p, min(bx, W - 20 - p.shape[1]), by - p.shape[0] - 6, a)


def ch_road(f, shot, edit):
    c = stage(f)
    which = evidence(c, f)
    _, _, _, n, ca = road_state(f)
    subject(c, f, which)
    counter(c, f, n, ca)
    small_board(c, f)
    frame_rect(c, *tile_xy('A1 Hub' if which == 'hub' else 'B1 Settings', SMALL)[:2], SMALL['tw'], SMALL['th'], WHITE, 4)
    board_pill(c, f, SENT, 'EDITOR PROJECTS: SENT BACK', RED, WHITE, SENTBACK + 4, PASS3_T)
    if f >= TA_T:
        frame_rect(c, *tile_xy('TA Time Attack', SMALL)[:2], SMALL['tw'], SMALL['th'], AMBER, 4,
                   clamp((f - TA_T) / 6))
    board_pill(c, f, 'TA Time Attack', 'TIME ATTACK: ONE KEY HINT LEFT', AMBER, INK, TA_T, SLAM, below=True)
    return c


def ch_road_text(c, f, o, edit):
    who = '— the design review, 28 Oct'
    say(c, f, PASS1_T + 4, REV_T, 'PASS 1: POLISH.', 40, size=84, kicker='28 OCT')
    quote(c, f, P1_QUOTE, REV_T, 'No family reached 9 overall in this pass.', who)
    say(c, f, REV_T, STR_T, 'A FRESH AI REVIEW LOWERED THE SCORES.', 40, size=84, kicker='A NEW CLAUDE OPUS SESSION')
    say(c, f, STR_T, SENTBACK, 'PASS 2: STRUCTURE.', 40, size=84, kicker='28 OCT')
    quote(c, f, STR_T, SENTBACK, 'The remaining blockers are structural rather than polish.', who)
    say(c, f, SENTBACK, PASS3_T, 'ANOTHER REVIEW SENT ONE 9 BACK.', 40, size=84, kicker='CHECKED AGAIN')
    say(c, f, PASS3_T, SLAM, 'PASS 3: FINISH WHAT THE REVIEWS FOUND.', 40, size=84, kicker='28–29 OCT')


# ch13: 27 / 27, the criteria row, the six groups delivered ----------------------------------------


def criteria_row(c, y, a, r):
    """The final criteria row from result-row.json: seven exact criterion scores and the overall judgment."""
    kick = text(r['kicker'], 'sub', 30, LIGHT, tracking=6)
    paste(c, kick, W / 2 - kick.shape[1] / 2, y - 168, a)
    criteria_headers(c, y, lambda j: a)
    for j, name in enumerate(CRITERIA):
        v = float(r['criteria'][name])
        x = MCOL0 + j * MCOLW + 6
        cell(c, x, y, v, a, size=54, dark=v >= 9)
        if v < 9:
            frame_rect(c, x, y, MCOLW - 12, MROWH - 10, WHITE, 4, a)
        if name in r.get('was', {}):    # the follow-up's own record: '**9** (was 8.5)'
            frame_rect(c, x, y, MCOLW - 12, MROWH - 10, WHITE, 4, a)
            w = text(f'was {r["was"][name]}', 'sub', 30, PALE, stroke=2, sfill=INK, shadow=2)
            paste(c, w, x + (MCOLW - 12) / 2 - w.shape[1] / 2, y + MROWH - 4, a)
    paste(c, pill(r['row_label'], 36), MX, y + (MROWH - 10) / 2 - pill(r['row_label'], 36).shape[0] / 2, a)
    hd = text('OVERALL', 'title_it', 40, GOLD, stroke=3, sfill=INK, shadow=3)
    paste(c, hd, MOVX + MOVW / 2 - hd.shape[1] / 2, y - 62, a)
    box(c, MOVX, y - 4, MOVW, MROWH - 2, INK, 0.8 * a)
    frame_rect(c, MOVX, y - 4, MOVW, MROWH - 2, GOLD, 3, a)
    n = text(r['overall'], 'title', 76, GOLD, stroke=4, sfill=INK, shadow=5)
    paste(c, n, MOVX + MOVW / 2 - n.shape[1] / 2, y + (MROWH - 6) / 2 - n.shape[0] / 2, a)


def ch_payoff(f, shot, edit):
    """27 / 27 at 9 overall slams over the all-gold board, then one family's exact criteria show what
    'overall' does and does not mean."""
    c = stage(f)
    tile_board(c, f, PASSES['lead'], 9.0, **BIG)
    board_head(c, 9)
    t = f - SLAM
    m = smooth(clamp((f - CRIT_T) / 14))
    box(c, 0, 0, W, H, DEEP, 0.35 + 0.57 * m)
    s_ = (1 + 0.5 * (1 - ease_out(clamp(t / 12)))) * (1 - 0.42 * m)
    if m >= 1:      # settled: drawn at its final size rather than resampled
        big = text('27 / 27 AT 9 OVERALL', 'title', 116, WHITE, stroke=7, sfill=INK, shadow=8)
    else:
        big = text('27 / 27 AT 9 OVERALL', 'title', 200, WHITE, stroke=12, sfill=INK, shadow=14)
        big = promo_kit.scaled(big, s_) if s_ != 1 else big
    shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0
    yc = 540 + (110 - 540) * m
    paste(c, big, W / 2 - big.shape[1] / 2 + shake, yc - big.shape[0] / 2, clamp(t / 3))
    a = smooth(clamp((f - CRIT_T) / 10))
    if a > 0:
        r = result_row()
        criteria_row(c, 470, a, r)
        say(c, f, CRIT_T + 14, IRIS + 20, caveat_line(r), 640, size=76)
    return c


HUB_STILL_LABEL = 'HUB & DIALOGS  ·  FOLLOW-UP STILL'


def ch_delivered(f, shot, edit):
    c = stage(f)
    wall_cells(c, f, 'new', WALL_NEW, IRIS, drop=False)
    c[92:92 + 448, 0:640] = up(still('hub_fu'), 2)    # the hub after its follow-up: a still, labelled as one
    for k, (g, label, take) in enumerate(GROUPS):
        paste(c, pill(HUB_STILL_LABEL if k == 0 else label, 36), *label_anchor_wall(k))
    pn = pill('THE SAME SIX GROUPS, DELIVERED  ·  29 OCT', 44)
    paste(c, pn, W / 2 - pn.shape[1] / 2, 20)
    u = smooth(clamp((f - END_T) / 24))
    if u > 0:
        blurred = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(6 * u)), np.float32)
        c = blurred * (1 - 0.72 * u)
    return c


def end_card(c, f, o, edit):
    badge = np.asarray(Image.open(BADGE).convert('RGBA'), np.float32)
    lines = [
        (badge, 96),
        (text('ROAD TO 9', 'title', 130, GOLD, stroke=8, sfill=INK, shadow=10), 368),
        (text('An AI design review of every OpenGGF menu, round by round.', 'sub', 52, WHITE, stroke=4, sfill=INK,
              shadow=5), 520),
        (text('github.com/OpenGGF/OpenGGF', 'title_it', 78, WHITE, stroke=5, sfill=INK, shadow=6), 610),
        (text('In development for OpenGGF 0.7', 'body', 42, LIGHT, stroke=3, sfill=INK, shadow=4), 726),
        (text('Scored and rebuilt by AI agents: Claude Opus 5.5, with OpenAI Codex GPT-6.1 on later passes.',
              'body', 32, PALE, stroke=2, sfill=INK, shadow=3), 830),
        (text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body', 36, PALE,
              stroke=2, sfill=INK, shadow=3), 900),
    ]
    for k, (img, y) in enumerate(lines):
        t = f - (END_T + 4 * k)
        if t >= 0:
            paste(c, img, W / 2 - img.shape[1] / 2, y + (1 - ease_out(clamp(t / 12))) * 30, clamp(t / 8))


# ------------------------------------------------------------------------------- reading holds
# Each information-heavy state: the planned first fully settled frame (the last meaningful reveal has
# ended), the planned first changed frame (the transition starts), and what the viewer reads. `reads`
# measures both on a frozen render; `readsheet` pictures them from the master.
READS = [
    ('ask', 'opening statement + kicker over the six round-0 menus (moving)', WALL_DROP * 5 + WALL_FALL + 6,
     STEP1_T - SAY_OUT + 1,
     'WE GAVE AN AI EVERY OPENGGF MENU. / CLAUDE OPUS · 27 OCT 2026 (6 words + kicker; the text itself settles at f14)'),
    ('step1', 'six group labels on their menus', LABEL_T[5] + LABEL_POP, MATRIX_T - SAY_OUT + 1,
     'STEP 1: SORT THEM INTO SIX GROUPS. + 6 two- or three-word labels'),
    ('criteria', 'the round-0 matrix: seven named criteria', CELLS_T + 4 * 6 + 2 * 4 + 8, OVERALL_T - SAY_OUT + 1,
     'STEP 2 headline + kicker; 7 criterion names; 5 rows of heat cells (values optional reading); NOT YET PICTURED'),
    ('overall', 'six overall scores, cells dimmed', OVERALL_T + 6 + 4 * 5 + 10, TARGET_T - SAY_OUT + 1,
     'OVERALL: ONE JUDGMENT, NOT AN AVERAGE. + 6 numbers (6.5 5.5 4 3.5 4 —)'),
    ('target', 'the target column', TARGET_T + 6 + 3 * 5 + 10, ROUNDS_T - SAY_OUT + 1,
     'STEP 3: EVERY GROUP TO 8 OR BETTER. + a column of 8+'),
    ('round4', 'round 4 result beside the legal notice at 8', NOT8_T + SAY_IN, FAMILIES_T,
     'ROUND 4, six overall scores (7.5 x4, 7, 7), CLOSE. NOT 8 YET.; static loop strip'),
    ('families', 'the 27-family board at 8, three below framed', STRAG_T + 6, ALL8 - SAY_OUT + 1,
     'THEN EVERY MENU: 27 FAMILIES. + board overview (gold 8s; 7.5, 7.5, 5.5 framed); tile = overall'),
    ('all8', 'the slam', ALL8 + 14, TURN - SAY_OUT + 1, 'ALL 27 AT 8 (4 words)'),
    ('turn', 'the raised target', TURN + 24 + SAY_IN, PASS1_T - SAY_OUT + 1,
     'THEN WE RAISED THE BAR. / ROAD TO 9 / 9 MEANS PRODUCTION POLISH. (12 words) + TARGET 9 chip'),
    ('pass1', 'pass 1 on the hub picture', P1_QUOTE + SAY_IN, REV_T - SAY_OUT + 1,
     'PASS 1: POLISH. + quote (8 words) + HUB 8.5, FAMILIES AT 9: 0 / 27'),
    ('review', 'the reviewer’s mark-up and the drop', DROP + 16, STR_T - SAY_OUT + 1,
     'A FRESH AI REVIEW LOWERED THE SCORES. + kicker; HUB 8 (red); four red tiles; the marked-up picture'),
    ('structure', 'the rebuilt hub, 13 at 9', WAVE13 + WAVE, SENTBACK - SAY_OUT + 1,
     'PASS 2: STRUCTURE. + quote (8 words) + HUB 9 + 13 / 27, 13 gold tiles'),
    ('sentback', 'one 9 sent back', SENTBACK + 16, PASS3_T - SAY_OUT + 1,
     'ANOTHER REVIEW SENT ONE 9 BACK. + EDITOR PROJECTS: SENT BACK (no count shown)'),
    ('finish', 'pass 3 result beside delivered Settings (moving)', TA_T + 6, SLAM - SAY_OUT + 1,
     'PASS 3 headline + SETTINGS 9 + 26 / 27 + TIME ATTACK: ONE KEY HINT LEFT'),
    ('result', 'the hub’s exact criteria under 27 / 27 at 9 overall', CRIT_T + 14 + SAY_IN, IRIS,
     '27 / 27 AT 9 OVERALL; follow-up kicker; A1 HUB 9 on each criterion, OVERALL 9, "was 8.5" under spacing and '
     'icons; THE HUB: 9 ON EACH CRITERION. (6 words)'),
    ('delivered', 'the six groups, delivered (moving)', IRIS + 24, END_T + 1,
     'THE SAME SIX GROUPS, DELIVERED · 29 OCT + the six labels from chapter 1; the hub cell is the follow-up still, '
     'labelled FOLLOW-UP STILL'),
    ('endcard', 'end card', END_T + 4 * 6 + 12, END_HIT,
     'title, line, URL, status, credit, disclaimer (about 40 words)'),
]
MIN_HOLD = {'all8': 1.8, 'delivered': 1.3}     # a 4-word slam; the moving wall whose labels were read in ch1


def reads_rows(measured=None):
    rows = []
    for k, (key, what, s, t, payload) in enumerate(READS):
        ms, mt = measured[k] if measured else (s, t)
        rows.append(dict(id=key, what=what, payload=payload, settle=ms, transition=mt, planned_settle=s,
                         planned_transition=t, hold_s=round((mt - ms) / FPS, 2),
                         settle_s=round(ms / FPS, 3), transition_s=round(mt / FPS, 3)))
    return rows


# ----------------------------------------------------------------------------------- the edit

CHAPTERS = []
EDL = []
CUES = []
E = None


def sfx(name):
    return SFX / f's2-sfx-{name}-paced.wav'


def map_cues(part, visible, f0=None, f1=None):
    era, take, s0, s1, in_ = SRC[part]
    f0 = s0 if f0 is None else f0
    f1 = s1 if f1 is None else f1
    for e in ('pre', 'new'):
        if e not in era:
            continue
        for fo, cue in clip(e, take).cues():
            out = s0 + fo - in_
            if f0 <= out < f1 and visible(out) == e:
                CUES.append((out, e, take, fo, cue))


def build(e):
    global CHAPTERS, EDL, CUES
    CHAPTERS, EDL, CUES = [], [], []
    X = e.X
    # 1-3 the assignment: ask, rubric, goal
    e.S(Custom(0, ROUNDS_T, ch_assignment))
    e.O(Fn(0, ROUNDS_T, ch_assignment_text))
    for t in LABEL_T:
        X(t, sfx('cd'), 0.9)
    X(MATRIX_T - 3, sfx('ab'), 1.3)
    for k in range(6):
        X(OVERALL_T + 6 + 4 * k, sfx('cd'), 1.0)                # the overall column, one judgment per group
    X(TARGET_T + 6, sfx('cd'), 1.0)
    CHAPTERS += [(0, MATRIX_T, 'The ask: an AI gets every OpenGGF menu and sorts them into six groups'),
                 (MATRIX_T, TARGET_T, 'The rubric: seven criteria, 1 to 10, one overall judgment'),
                 (TARGET_T, ROUNDS_T, 'The goal: every group to 8 or better')]
    wall = ', '.join(f'pre/{t} take frames {s}-{s + WALL_OUT - 1}' for t, s in WALL_PRE.items())
    EDL.append((0, WALL_OUT, CHAPTERS[0][2] + ' / rubric', 'wall of six cells 2x (3x2), dimmed under the matrix '
                'from b12.5, faded out by b14.5', wall))
    EDL.append((WALL_OUT, ROUNDS_T, 'The rubric / the goal', 'matrix, overall and target columns', 'editorial board'))
    # 4 rounds 1-4
    ch = 'Rounds 1-4: the loop; Mod manager and legal notice, round 0 to the 8 build; six groups 7 to 7.5'
    e.S(Custom(ROUNDS_T, FAMILIES_T, ch_rounds, trans='wipe', tdur=14))
    X(ROUNDS_T - 4, sfx('ab'), 1.3)
    for t in RESCORE:
        X(t, sfx('cd'), 1.0)
    map_cues('lib', lambda f: 'new' if sweep(f, *LIB_SWEEP) >= 160 else 'pre')
    CHAPTERS.append((ROUNDS_T, FAMILIES_T, ch))
    EDL.append((ROUNDS_T, LEGAL_T, ch, 'pane 4x + loop strip + six-row board; divider b35.25-36.5',
                f'pre+new/mods take frames {SRC["lib"][4]}-{src("lib", LEGAL_T - 1)}'))
    EDL.append((LEGAL_T, FAMILIES_T + 14, ch, 'pane 4x + loop strip + six-row board; divider b38.25-39.25',
                f'pre+new/legal take frames {SRC["notice"][4]}-{src("notice", FAMILIES_T + 13)}'))
    # 5-7 every family, all at 8, the turn
    e.S(Custom(FAMILIES_T, PASS1_T, ch_families, trans='wipe', tdur=14))
    e.O(Fn(FAMILIES_T, TURN, ch_families_text))
    e.O(Fn(TURN, PASS1_T, turn_text))
    X(FAMILIES_T - 4, sfx('ab'), 1.3)
    for k in range(0, 27, 6):
        X(TILE_ON + 2 * k, sfx('cd'), 0.9)
    X(ALL8, sfx('c5'), 0.5)
    e.O(Flash(ALL8, 14, 0.7))
    X(TURN, sfx('bc'), 1.0)
    e.O(Flash(TURN, 14, 0.8))
    CHAPTERS += [(FAMILIES_T, ALL8, 'Every menu family: 27 tiles, three below 8'),
                 (ALL8, TURN, 'All 27 at 8'),
                 (TURN, PASS1_T, 'Road to 9: we raised the bar; 9 = production polish')]
    EDL.append((FAMILIES_T, PASS1_T, 'Every family / all 27 at 8 / road to 9',
                'full family board (tiles cascade), slam, target 8 -> 9', 'editorial board'))
    # 8-12 the road: pass 1, the fresh review, structure, sent back, finish
    e.S(Custom(PASS1_T, SLAM, ch_road, trans='wipe', tdur=14))
    e.O(Fn(PASS1_T, SLAM, ch_road_text))
    X(PASS1_T - 4, sfx('ab'), 1.3)
    X(P1, sfx('cd'), 1.0)
    for k in range(4):
        X(DROP + 4 * k, sfx('a8'), 2.0)
    X(STR_SWEEP[0], sfx('ab'), 1.3)
    X(HUB9, sfx('cd'), 1.0)
    for k in range(3):
        X(WAVE13 + 6 * k, sfx('cd'), 0.9)
    X(SENTBACK, sfx('a8'), 2.0)
    for k in range(3):
        X(WAVE26 + 6 * k, sfx('cd'), 0.9)
    map_cues('set_fin', lambda f: 'new' if sweep(f, *SET_SWEEP) >= 160 else 'none', f1=SLAM)
    CHAPTERS += [(PASS1_T, REV_T, 'Pass 1: polish; no family reaches 9'),
                 (REV_T, STR_T, 'A fresh AI review marks up the pictures; scores go down'),
                 (STR_T, SENTBACK, 'Pass 2: structure; 13 families at 9'),
                 (SENTBACK, PASS3_T, 'Another review sends one 9 back'),
                 (PASS3_T, SLAM, 'Pass 3: 26 at 9; one key hint left')]
    EDL.append((PASS1_T, REV_T, 'Pass 1', 'evidence pane 3x + subject score + family board',
                f'{STILL["hub_t8"]} then {STILL["hub_p1"]}'))
    EDL.append((REV_T, STR_T, 'Fresh review', 'evidence pane: mark-up drawn onto the same capture',
                f'{STILL["hub_p1"]} + {STILL["hub_rev"]} (1:1)'))
    EDL.append((STR_T, PASS3_T, 'Structure / sent back', 'divider b87.75-89',
                f'{STILL["hub_rev"]} | {STILL["hub_str"]}'))
    EDL.append((PASS3_T, SLAM, 'Finish', 'divider b102.75-104, still | moving',
                f'{STILL["set_str"]} | new/settings take frames {SRC["set_fin"][4]}-{src("set_fin", SLAM - 1)}'))
    # 13 payoff, delivered, end card
    e.S(Custom(SLAM, IRIS, ch_payoff))
    e.S(Custom(IRIS, TOTAL, ch_delivered, trans='iris', tdur=24))
    X(SLAM, sfx('c5'), 0.6)
    e.O(Flash(SLAM, 18, 0.9))
    X(IRIS - 6, sfx('c3'), 0.7)
    CHAPTERS.append((SLAM, END_T, '27 / 27 at 9 overall; the hub after its follow-up, 9 on each criterion; the six '
                     'groups, delivered'))
    EDL.append((SLAM, IRIS, CHAPTERS[-1][2], 'full family board, slam, the final criteria row (result-row.json)',
                'editorial board'))
    wall = ', '.join(f'new/{t} take frames {s}-{s + TOTAL - IRIS - 1}' for t, s in WALL_NEW.items() if t != 'hub')
    EDL.append((IRIS, TOTAL, CHAPTERS[-1][2], 'iris into the wall of six cells 2x (hub cell: the follow-up still); '
                'blurred under the end card from b127.5', f'{STILL["hub_fu"]} (still) | {wall}'))
    e.O(Fn(END_T, TOTAL, end_card))
    e.O(Flash(END_HIT, 10, 0.35))
    e.O(Fade(END_HIT + 12, TOTAL + 1))
    CHAPTERS.append((END_T, TOTAL, 'End card'))
    e.bed(MUSIC, 0, 0.75, src_seconds=BED_SRC_S, length=BED_LEN_S, fade_in=0.002, fade_out=0.01)
    for out, era, take, fo, cue in CUES:
        X(out, UI / f'ui-{cue.lower()}.wav', UI_GAIN)
    return TOTAL


def edit():
    global E
    if E is None:
        E = Edit(bpm=BPM, first=0.0, fps=FPS, size=(W, H), out=FILM, work=BUILD)
        E.total = build(E)
    return E


# --------------------------------------------------------------------------------- rendering


def _frame(f):
    return edit().render_frame(f).tobytes()


def frames_to(cmd, first, last, workers=8):
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(workers) as pool:
        for k, b in enumerate(pool.imap(_frame, range(first, last), chunksize=8)):
            enc.stdin.write(b)
            if k % 600 == 0:
                print(f'frame {first + k}/{last}', flush=True)
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError('encoder failed')


RAW = ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']


def write_chapters(path):
    lines = [';FFMETADATA1', 'title=ROAD TO 9 (readable holds): an AI design review of every OpenGGF menu',
             'artist=OpenGGF']
    for f0, f1, title in CHAPTERS:
        lines += ['[CHAPTER]', 'TIMEBASE=1/60', f'START={f0}', f'END={f1}', f'title={title}']
    path.write_text('\n'.join(lines) + '\n')
    with (HERE / 'edl.csv').open('w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['start_s', 'end_s', 'start_frame', 'end_frame', 'chapter', 'layout', 'sources'])
        for f0, f1, ch, layout, srcs in EDL:
            w.writerow([f'{f0 / FPS:.3f}', f'{f1 / FPS:.3f}', f0, f1, ch, layout, srcs])
    with (HERE / 'chapters.txt').open('w') as fh:
        for f0, f1, title in CHAPTERS:
            fh.write(f'{f0 / FPS:6.2f}-{f1 / FPS:6.2f}  {title}\n')
    (HERE / 'cues.json').write_text(json.dumps(
        [dict(frame=o, era=era, take=t, take_frame=fo, cue=c) for o, era, t, fo, c in sorted(CUES)], indent=0))


def true_peak(path, f0=None, f1=None):
    cmd = ['ffmpeg', '-nostats']
    if f0 is not None:
        cmd += ['-ss', f'{f0 / FPS:.3f}', '-t', f'{(f1 - f0) / FPS:.3f}']
    r = subprocess.run(cmd + ['-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    return (float(tail.split('Peak:')[1].split('dBFS')[0].strip()),
            float(tail.split('I:')[1].split('LUFS')[0].strip()))


def finish_mp4():
    meta = BUILD / 'chapters.ffmeta'
    mix = BUILD / 'mix.wav'
    gain_db = 0.0
    for _ in range(4):
        aac = BUILD / 'audio.m4a'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(mix), '-af', f'volume={gain_db}dB', '-c:a', 'aac',
                        '-b:a', '256k', str(aac)], check=True)
        peak, integ = true_peak(aac)
        print(f'AAC true peak {peak:+.2f} dBTP, integrated {integ:.1f} LUFS (gain {gain_db:+.2f} dB)')
        if peak <= -1.0:
            break
        gain_db -= peak + 1.5
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(MASTER), '-i', str(aac), '-i', str(meta),
                    '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2',
                    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                    '-c:a', 'copy', '-movflags', '+faststart', str(FILM)], check=True)
    (BUILD / 'audio-gain.json').write_text(json.dumps({'aac_gain_db': gain_db, 'true_peak_dbtp': peak,
                                                        'integrated_lufs': integ}))
    print(FILM)


def _diff(a, b):
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2)
    return int((d > 0).sum())


def _frozen(f):
    return edit().render_frame(f)


def reads():
    """Reading holds on a frozen render (READ_CHECK=1: every take held on one frame, background still), so
    any difference is editorial animation. For each state: walk back from the planned settle to the
    first frame of the settled run and forward from the planned transition to the first changed frame;
    require every sampled frame in between identical to the settle frame."""
    if not FREEZE:
        raise SystemExit('run as READ_CHECK=1 edit.py reads')
    edit()
    measured, report, ok = [], [], True
    with Pool(8) as pool:
        for key, what, s, t, payload in READS:
            probe = sorted(set(list(range(s - 30, s + 2)) + list(range(s, t, 10)) + list(range(t - 2, t + 16))))
            probe = [p for p in probe if 0 <= p < TOTAL]
            ims = dict(zip(probe, pool.map(_frozen, probe)))
            ref = ims[s]
            ms = s
            while ms - 1 in ims and _diff(ims[ms - 1], ref) == 0:
                ms -= 1
            inside = [p for p in probe if s <= p < t]
            bad = [p for p in inside if _diff(ims[p], ref)]
            mt = next((p for p in probe if p >= t - 2 and _diff(ims[p], ref)), None)
            good = not bad and mt is not None and ms < s + 1
            ok &= good
            measured.append((ms, mt if mt is not None else t))
            report.append(f'{key:10s} settle f{ms} ({ms / FPS:6.3f}s, planned f{s})  transition f{mt} '
                          f'({(mt or t) / FPS:6.3f}s, planned f{t})  hold {((mt or t) - ms) / FPS:4.2f}s  '
                          f'{"settled" if not bad else "MOVES at " + str(bad[:4])}')
    for line in report:
        print(line)
    rows = reads_rows(measured)
    short = [r['id'] for r in rows if r['hold_s'] < MIN_HOLD.get(r['id'], 2.0)]
    (HERE / 'reads.json').write_text(json.dumps(dict(
        note='Reading holds measured on a frozen render (edit.py reads, READ_CHECK=1): settle = first frame of the '
             'run of frames identical to the settled state, transition = first frame that differs. Footage and '
             'background were held still for the measurement only; in the film the moving menus keep moving.',
        min_hold_s=dict(default=2.0, **MIN_HOLD), reads=rows), indent=1) + '\n')
    print('all settled' if ok else 'FAILED', '| below minimum:', short or 'none')
    return 0 if ok and not short else 1


def readsheet(master):
    """Frames of the master at each state's settle, +1 s, +2 s, last settled frame and first changed frame."""
    rows = json.loads((HERE / 'reads.json').read_text())['reads']
    out = BUILD / 'readsheets'
    out.mkdir(parents=True, exist_ok=True)
    tw, th = 640, 360
    for r in rows:
        s, t = r['settle'], r['transition']
        picks = [('settle', s), ('+1 s', min(s + 60, t - 1)), ('+2 s', min(s + 120, t - 1)), ('last held', t - 1),
                 ('changed', t)]
        sheet = Image.new('RGB', (tw * len(picks), th + 28), (0, 0, 0))
        d = ImageDraw.Draw(sheet)
        for k, (lab, f) in enumerate(picks):
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{(f - 0.5) / FPS:.6f}', '-i', str(master),
                                  '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                 capture_output=True).stdout
            im = Image.frombytes('RGB', (W, H), raw).resize((tw, th), Image.BILINEAR)
            sheet.paste(im, (k * tw, 28))
            d.text((k * tw + 6, 6), f'{r["id"]}  {lab}: f{f} ({f / FPS:.2f} s)', fill=(255, 220, 80))
        p = out / f'read-{r["id"]}.png'
        sheet.save(p)
        print(p)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    e = edit()
    BUILD.mkdir(exist_ok=True)
    if cmd == 'check':
        for w in e.check():
            print('warning:', w)
        print('pacing:', e.pacing()[0])
        print('end', e.end(), f'{e.end() / FPS:.3f}s', 'cues', len(CUES), 'sfx', len(e.sfx),
              f'bed {BED_SRC_S:.4f}s + {BED_LEN_S:.4f}s (cut at film frame {BED_LEN_S * FPS:.1f})')
        print('result row:', caveat_line(result_row()))
        for r in reads_rows():
            print(f'  planned {r["id"]:10s} settle f{r["settle"]} transition f{r["transition"]} hold {r["hold_s"]:.2f}s')
    elif cmd == 'reads':
        sys.exit(reads())
    elif cmd == 'readsheet':
        readsheet(Path(sys.argv[2]))
    elif cmd == 'sheet':
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(e.contact_sheet(BUILD / 'sheet.png', step, 0, None, workers=8))
    elif cmd == 'keys':
        beats = [float(a) for a in sys.argv[2:]]
        with Pool(8) as pool:
            out = pool.map(_frame, [F(b) for b in beats])
        cols, tw, th = 3, 640, 360
        sheet = Image.new('RGB', (tw * cols, th * ((len(out) + cols - 1) // cols)))
        d = ImageDraw.Draw(sheet)
        for k, b in enumerate(out):
            im = Image.frombytes('RGB', (W, H), b).resize((tw, th), Image.BILINEAR)
            sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
            d.text(((k % cols) * tw + 4, (k // cols) * th + 2), f'{F(beats[k])} b{beats[k]:g}', fill=(255, 0, 255))
        path = BUILD / 'keys.png'
        sheet.save(path)
        print(path)
    elif cmd == 'frames':
        for a in sys.argv[2:]:
            p = BUILD / f'frame-{int(a):05d}.png'
            Image.fromarray(e.render_frame(int(a))).save(p)
            print(p)
    elif cmd == 'preview':
        a, b = int(sys.argv[2]), int(sys.argv[3])
        out = BUILD / f'preview-{a:05d}-{b:05d}.mp4'
        frames_to(['ffmpeg', '-v', 'error', '-y', *RAW, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12',
                   '-pix_fmt', 'yuv420p', str(out)], a, b)
        print(out)
    elif cmd == 'master':
        FINAL.mkdir(exist_ok=True)
        import hashlib
        if hashlib.sha256(MUSIC.read_bytes()).hexdigest() != MUSIC_SHA256:
            raise SystemExit(f'music bed hash mismatch: {MUSIC}')
        cap = result_row()['capture']
        if cap['path'] != STILL['hub_fu'] or hashlib.sha256((EVID / cap['path']).read_bytes()).hexdigest() != cap['sha256']:
            raise SystemExit('the hub follow-up still differs from result-row.json')
        audio = BUILD / 'mix.wav'
        write_wav(audio, e.mix())
        meta = BUILD / 'chapters.ffmeta'
        write_chapters(meta)
        video = BUILD / 'master-video.mkv'
        frames_to(['ffmpeg', '-v', 'error', '-y', *RAW, '-c:v', 'ffv1', '-level', '3', '-g', '1', '-slices', '16',
                   '-slicecrc', '1', '-pix_fmt', 'bgr0', str(video)], 0, e.end())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-i', str(audio), '-i', str(meta),
                        '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2', '-c:v', 'copy',
                        '-c:a', 'pcm_s16le', str(MASTER)], check=True)
        video.unlink()
        print(MASTER)
    elif cmd == 'remix':
        audio = BUILD / 'mix.wav'
        write_wav(audio, e.mix())
        meta = BUILD / 'chapters.ffmeta'
        write_chapters(meta)
        tmp = MASTER.with_suffix('.remix.mkv')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(MASTER), '-i', str(audio), '-i', str(meta),
                        '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2', '-c:v', 'copy',
                        '-c:a', 'pcm_s16le', str(tmp)], check=True)
        tmp.replace(MASTER)
        print(MASTER)
    elif cmd == 'lists':
        write_chapters(BUILD / 'chapters.ffmeta')
    elif cmd == 'loudness':
        audio = BUILD / 'mix-probe.wav'
        write_wav(audio, e.mix())
        for f0, f1, title in [(0, e.end(), 'whole film')] + CHAPTERS:
            print(f'{f0 / FPS:6.2f}-{f1 / FPS:6.2f}s  I {true_peak(audio, f0, f1)[1]:6.1f} LUFS  {title}')
        audio.unlink()
    elif cmd == 'mp4':
        finish_mp4()


if __name__ == '__main__':
    sys.modules.setdefault('promo_kit', promo_kit)
    main()
