#!/usr/bin/env python3
"""ROAD TO 9, hill-climb story cut: the OpenGGF menu promo rebuilt as the account of an AI design
review (project menu-evolution, revision hill-climb-story, 2026-10-29).

Brief (one line each)
  Request.   The user on the 43.2 s Super Sonic cut: "not bad but the direction sucks. It's difficult to
             see what the video is getting at. We need to establish the context ... We asked Opus originally
             to classify the menus based on categories, then asked it to raise that classification in a hill
             climb until 8 overall (and then raised it to 9)". Kept: Sonic 2 Super Sonic music throughout,
             about 43-44 s, montage energy with climbing numbers, readable real moving UI.
  Diagnosis. Both earlier films (87.333 s r3b, 43.2 s super-sonic-cut) showed old -> new menus and rolled
             scores 3.5 -> 9 without ever saying who scored, on what scale, against which target, or why the
             numbers moved; the only context was a footnote and an end-card line. That is a structural
             failure, so this cut is rebuilt around the experiment itself, not re-captioned.
  Story.     We gave an AI (Claude Opus) every OpenGGF menu -> it sorted them into six groups -> scored each
             group on seven criteria, 1-10 -> step 3, climb to 8+, one loop per round (change, recapture,
             rescore, keep or revert) -> rounds 1-4 -> every menu family (27) -> all at 8 -> we raised the
             target to 9 -> a polish pass stalls at 0 -> a fresh AI review marks up the pictures and scores
             go DOWN -> structural pass, 13 -> another review sends one 9 back, finish pass, 26 -> the last
             gap (one keyboard hint) -> 27 / 27 at 9 overall, with the criteria that stay 8.5 on screen.
             Every chapter answers one viewer question: what was asked (ch 1), how it was judged (2), what
             the target was and how a round works (3), what changed (4, 5, 9-11), why the target rose (6-7),
             why the numbers stalled and fell (8-9), what the result is (12).
  Audience.  Sonic fans, OpenGGF players and people curious about AI-assisted design, meeting it cold.
  Form.      Editorial story film over real UI: an evolving score board (matrix -> six rows -> 27 family
             tiles) is the narrator; moving per-frame renders of the production menus (the original
             production's clips/: round-0 menus from 2f9ca84b1, delivered menus from d823ce643) and the
             review's own capture stills (the pictures that were scored, from the audit's evidence sets,
             including the reviewer's annotated picture) are the proof. No chat transcript; quotation marks
             only around verbatim sentences of the design review document.
  Promise.   How an AI hill-climbed every OpenGGF menu from 3.5 to 9, and what it took.
  Numbers.   Only recorded values from docs/architecture/audits/2026-10-27-menu-design-review.md at
             d823ce643 (SCORES below, each with its section). Subjective capture-based design judgments, said
             on screen as "judged from screenshots"; no usability or performance claim. Overall is holistic,
             not an average (said in ch 2 and proven in ch 12). Groups (6 + bundled Time Attack) are not the
             seven criteria; the board keeps them on different axes.
  Proof.     ch1 six round-0 menus moving in a wall, labelled with their groups; ch4 Mod manager and legal
             notice round 0 -> the 8 state (moving; the take frames are pixel-identical to the audit's
             a694db926 / 64ed120d2 captures, see provenance); ch5 Time Attack 5.5 -> 8 (audit stills);
             ch8-10 one crowded hub picture through pass 1, the reviewer's mark-up and the structural fix;
             ch11 Settings structural still -> delivered moving (captions); Time Attack's TAB: DETAILS cap;
             ch12 the six groups again, delivered, moving.
  Hero.      The turn: ALL 27 AT 8 -> "THEN WE RAISED THE BAR" -> TARGET 8 rolls to 9, every tile drops below
             it, ROAD TO 9 on the intro riff; and the payoff 27 / 27 on the cadence downbeat.
  Sound.     Sonic 2 "Super Sonic" (engine music 0x93 = native MusID_SuperSonic $96, ROM $FCBBC, canonical
             S2 REV01) through OpenGGF's SMPS driver, FmSfxRenderTool --paced, 48 kHz: the exact render the
             super-sonic-cut used (same file, same sha256), one bed from its first sample to the G-major stab
             that resolves its third loop (frame 2555), cut in the rest after it (frame 2566). 146.48 BPM,
             24.576 frames a beat, 12-bar loop: INTRO 2 bars (rising chromatic riff), A 4 (melody),
             B 4 (stabs), TURN 2 (C-E-G cadence). Chapters sit on those sections. Stingers (S2 REV01 renders of
             the original production): Swish 0xAB on chapter wipes, Blip 0xCD on board ticks and tallies,
             Beep 0xA8 on the review's score drops, Spindash Release 0xBC on the target turn, Tally End 0xC5
             on the two milestones only (all at 8, 27 / 27), Enter Giant Ring 0xC3 under the iris. Menu sounds
             are the engine's HostUiSfx tones at the cue frames the moving takes logged, only while their era
             is on screen. Checked by measurement only; nobody listened to this mix.
  Palette.   Sampled from d823ce643 menu frames: navy #051035 / #0a245c, deep #02081c, focus gold #ffd64c,
             pale #e8edff; heat cells run review-red -> navy -> gold.
  Type.      Fira Sans Compressed Heavy / Condensed (OFL) with stroke and hard shadow: the film's voice never
             looks like the menus' pixel font. One statement per bar at most, <= 8 words.
  Pixels.    Native 320x224 frames at integer nearest-neighbour 4x (single panes), 3x (evidence panes; the
             reviewer's annotated picture is itself a 3x image and is shown 1:1) or 2x (wall cells).
  End card.  Badge, title, one line, URL, status, who did the work (AI agents named), disclaimer.

Beat sheet (b = bed beat, F(b) = round(24.576 b); bar = 4 beats = 1.638 s; [music section])
  b0-8     1 THE ASK       [INTRO 1]  six round-0 menus drop into a wall on the riff (b0-2.5); "WE GAVE AN AI
                                      EVERY OPENGGF MENU." (kicker: Claude Opus, 27 Oct); b4 "STEP 1: SORT
                                      THEM INTO GROUPS" and the six group labels land, one a half beat.
  b8-16    2 THE RUBRIC    [A 1]      labels fly to matrix rows (the wall fades out under it by b16, before its
                                      shortest take ends); "STEP 2: SCORE EACH GROUP"; seven criteria
                                      columns light a half beat apart with the round-0 values; b12 OVERALL
                                      (one judgment, not an average); b13 the scale 5 / 7 / 9; overlays
                                      "not yet pictured".
  b16-24   3 THE GOAL      [A 1]      "STEP 3: EVERY GROUP TO 8 OR BETTER", TARGET column; b20 the loop
                                      CHANGE -> RECAPTURE -> RESCORE -> KEEP OR REVERT lights one a beat.
  b24-32   4 ROUNDS 1-4    [B 1]      Mod manager round 0 -> 8 state (b24-28), legal notice (b28-32), divider
                                      sweeps; six-row board laps R1 b27, R2 b29, R3 b30, R4 b31 with the
                                      loop strip; b31 "CLOSE. NOT 8 YET."
  b32-40   5 EVERY FAMILY  [B 1]      27 family tiles in the group rows (+ bundled Time Attack) light to 8
                                      except Editor HUD 7.5, Stageplay 7.5, Time Attack 5.5; b36 Time Attack
                                      5.5 -> 8 side by side by divider.
  b40-48   6 ALL AT 8      [TURN 1]   slam "ALL 27 AT 8" + Tally End; b44 "THEN WE RAISED THE BAR."
  b48-56   7 ROAD TO 9     [INTRO 2]  flash + spindash release; TARGET 8 -> 9; tiles drop below the target;
                                      ROAD / TO / 9; b52 "9 = PRODUCTION POLISH" and AT 9: 0 / 27.
  b56-64   8 PLATEAU       [A 2]      pass 1 (polish): crowded hub at 8, then its pass-1 picture; five tiles
                                      to 8.5; quote "No family reached 9 overall in this pass."
  b64-72   9 FRESH REVIEW  [A 2]      the reviewer's annotations draw onto that picture; scores drop (hub,
                                      help, editor HUD, Stageplay 8.5 -> 8; notices 8 -> 8.5; trace plates ?);
                                      "SCORES WENT DOWN, NOT UP."
  b72-80   10 STRUCTURE    [B 2]      quote "The remaining blockers are structural rather than polish";
                                      divider: marked-up -> rebuilt hub; hub 9; tally to 13 on the stabs.
  b80-88   11 FINISH       [B 2]      another review sends Editor projects' 9 back (13 -> 12); Settings
                                      structural still -> delivered moving; tally to 26; b86 Time Attack's
                                      last gap, TAB: DETAILS.
  b88-96   12 27 / 27      [TURN 2]   slam + Tally End on the cadence; the hub's final criteria row (two
                                      8.5s under an overall 9); Giant Ring iris (b91.5) into the six groups,
                                      delivered, moving, labelled as in ch 1.
  b95-104  END CARD        [INTRO 3]  lines on the riff's steps; the G-major stab b104; fade. 2592 frames, 43.20 s.

Commands (Python with numpy + Pillow; OPENGGF_WORKTREE = a tree with tools/media/promo_kit.py):
  edit.py check | sheet [step] | frames N... | preview A B | master | mp4 | loudness | lists
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
REV = HERE.parents[1]                              # revisions/hill-climb-story
ROOT = HERE.parents[3]                             # the original production root (clips, sfx, ui tones)
EVID = Path(os.environ.get('MENU_EVIDENCE', str(ROOT.parent)))   # parent of the audit's evidence sets
KIT = Path(os.environ.get('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-9bc4fdd2')) / 'tools/media'
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
BUILD = REV / 'build'
FINAL = REV / 'final'
FILM = FINAL / 'menu-evolution-hill-climb-story.mp4'
MASTER = FINAL / 'menu-evolution-hill-climb-story-master.mkv'
BADGE = KIT.parents[1] / 'src/main/resources/icon/openggf-256.png'

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

F = lambda b: int(round(BEAT * b))      # bed beat -> output frame
END_HIT = F(104)
TOTAL = END_HIT + 36                    # 2592 frames
BED_CUT = 2566
UI_GAIN = float(os.environ.get('UI_GAIN', '0.7'))

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
    # Hill climb toward 9, "Score matrix (toward 9)": "No family reached 9 overall in this pass."
    'p1': fam_values('8', A1='8.5', A5='8.5', F4='8.5', F5='8.5', SP='8.5'),
    # Fresh critical review: "crowded 320-wide hub, help, editor command sheet and Stageplay remain at 8; the
    # toast remains 8.5. Notices were independently judged 8.5"; trace plates' pictures invalid (G1).
    'rev': fam_values('8', F5='8.5', E1_2='8.5', F6_10='?'),
    # Structural pass matrix: "Thirteen families reach 9 overall; fourteen stay at 8.5."
    'str': {**{f: '8.5' for f in FAM}, **{f: '9' for f in FAM if f.split()[0] in (
        'A1', 'A3', 'A4', 'A5', 'A7', 'B2', 'B4', 'B5', 'D10', 'E1-2', 'F3', 'F4', 'F5')}},
    # Finish pass: "Twenty-six families reach 9; Time Attack stays 8.5"
    'fin': fam_values('9', TA='8.5'),
    # Lead acceptance: Time Attack accepted at 9 overall (d823ce643); criteria keep their 8.5 entries
    'lead': fam_values('9'),
}
assert sum(v == '9' for v in PASSES['str'].values()) == 13
HUB_FINAL = ([9, 9, 8.5, 9, 8.5, 9, 9], '9')       # finish-pass matrix, A1 Hub (weakest state 60-hub-overflow-start)

# ------------------------------------------------------------------------------- evidence stills
T9 = 'menu-target9-20261028'
STILL = {   # the review's own captures (320x224 unless noted); provenance/evidence.json has heads and hashes
    'hub_t8': f'{T9}/baseline/320/hub/38-hub-crowded.png',                    # a694db926, the delivered 8
    'hub_p1': f'{T9}/final/320/hub/38-hub-crowded.png',                       # toward-9 pass-1 tree (ea7df pixels)
    'hub_rev': f'{T9}/review-opus55/hub38-320-annotated.png',                 # 960x672: the reviewer's mark-up
    'hub_str': f'{T9}/structural/final/320/hub/38-hub-crowded.png',           # d8d947336
    'set_str': f'{T9}/structural/final/320/hub/11-settings.png',              # d8d947336
    'ta_pre': 'all-menus-final-families-20261028/before/time-attack/320/ta04-menu-solo.png',   # efae20d69, 5.5
    'ta_8': 'all-menus-final-families-20261028/final/time-attack/320/ta04-menu-solo.png',      # final families, 8
    'ta_tab': f'{T9}/finish/lead-shortcut/final/time-attack/320/lead-chat-ready.png',  # e716cc55b, TAB: DETAILS
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


# take in-points: (era(s), take, output start, output end, take frame at output start)
SRC = {
    'lib':     ('pre+new', 'mods', F(24), F(28), 53),      # the manager list (ENTER at take 52)
    'notice':  ('pre+new', 'legal', F(28), F(32), 0),
    'set_fin': ('new', 'settings', F(81.5), F(86), 86),    # take 86 = a513dd5fd 11-settings (0.01 % differ)
}
WALL_PRE = {'hub': 160, 'settings': 100, 'locate': 40, 'mods': 53, 'legal': 0, 'shader': 145}   # at b0
WALL_NEW = {'hub': 160, 'settings': 86, 'locate': 40, 'mods': 53, 'legal': 0, 'shader': 145}    # at the iris
IRIS = F(91.5)


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
    band = ((diag - f * 1.6) // 90) % 2
    return base + band[..., None] * np.array((4, 8, 18), np.float32)


def box(c, x, y, w, h, colour, alpha=1.0):
    x0, y0, x1, y1 = max(0, int(x)), max(0, int(y)), min(W, int(x + w)), min(H, int(y + h))
    if x0 < x1 and y0 < y1:
        c[y0:y1, x0:x1] = c[y0:y1, x0:x1] * (1 - alpha) + np.array(colour, np.float32) * alpha


def frame_rect(c, x, y, w, h, colour, t=6):
    box(c, x - t, y - t, w + 2 * t, t, colour)
    box(c, x - t, y + h, w + 2 * t, t, colour)
    box(c, x - t, y, t, h, colour)
    box(c, x + w, y, t, h, colour)


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


def fit(s, role, size, maxw, **kw):
    """The text at the largest size <= size whose width fits maxw."""
    while size > 12:
        img = text(s, role, size, **kw)
        if img.shape[1] <= maxw:
            return img
        size -= 2
    return text(s, role, size, **kw)


def appear(t, dur=12):
    return clamp(t / dur)


def say(c, f, t0, t1, s, y, size=96, colour=WHITE, role='title', x=None, kicker=None, kcol=LIGHT):
    """A statement line: enters upward over 12 frames, leaves over 8 (faster than it came)."""
    if not t0 <= f < t1:
        return
    t = f - t0
    a = clamp(t / 10) * clamp((t1 - f) / 8)
    dy = (1 - ease_out(clamp(t / 14))) * 40
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
    a = clamp(t / 10) * clamp((t1 - f) / 8)
    q = text(f'“{s}”', 'body_it', 44, PALE, stroke=3, sfill=INK, shadow=4)
    w_ = text(who, 'sub', 30, GOLD, stroke=2, sfill=INK, shadow=3)
    paste(c, q, W / 2 - q.shape[1] / 2, y + (1 - ease_out(clamp(t / 14))) * 30, a)
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


# ch2/ch3 matrix geometry
MX = 60                                     # left edge of the row labels
MCOL0, MCOLW = 470, 146                     # first criterion column, column pitch
MOVX, MOVW = MCOL0 + 7 * MCOLW + 10, 180    # overall column
MTGX = MOVX + MOVW + 10                     # target column
MROW0, MROWH = 330, 88


def label_anchor_wall(k):
    return (k % 3) * 640 + 16, 92 + (k // 3) * 448 + 448 - 66


def label_anchor_matrix(k):
    return MX, MROW0 + k * MROWH + 14


def matrix(c, f, t0, rubric_fill=True, target=None):
    """The round-0 score matrix: groups down, seven criteria across, a holistic overall."""
    # criteria headers, one column every half beat
    for j, name in enumerate(CRITERIA):
        tj = f - (t0 + F(0.5 * j))
        if tj < 0:
            continue
        a = appear(tj, 8)
        hd = fit(name, 'title_it', 32, MCOLW - 10, fill=PALE, stroke=2, sfill=INK)
        paste(c, hd, MCOL0 + j * MCOLW + MCOLW / 2 - hd.shape[1] / 2, MROW0 - 54 + (1 - a) * 20, a)
        for k, (g, _, _) in enumerate(GROUPS):
            vals = ROUND0[g][0]
            tk = tj - 3 * k
            if tk < 0:
                continue
            x, y = MCOL0 + j * MCOLW + 6, MROW0 + k * MROWH
            if vals is None:
                continue
            u = appear(tk, 8)
            box(c, x, y, MCOLW - 12, MROWH - 10, heat(vals[j]), 0.92 * u)
            n = text(str(vals[j]), 'title', 54, WHITE, stroke=3, sfill=INK, shadow=4)
            paste(c, n, x + (MCOLW - 12) / 2 - n.shape[1] / 2, y + (MROWH - 10) / 2 - n.shape[0] / 2 + 2, u)
    # overlays row: not pictured in round 0
    tj = f - (t0 + F(3.5))
    if tj >= 0:
        k = 5
        nyp = text('NOT YET PICTURED IN ROUND 0', 'title_it', 40, LIGHT, stroke=2, sfill=INK)
        y = MROW0 + k * MROWH
        box(c, MCOL0 + 6, y, 7 * MCOLW - 12, MROWH - 10, NAVY2, 0.8 * appear(tj, 8))
        paste(c, nyp, MCOL0 + 7 * MCOLW / 2 - nyp.shape[1] / 2, y + (MROWH - 10) / 2 - nyp.shape[0] / 2, appear(tj, 8))
    # the overall column: one holistic judgment
    to = f - (t0 + F(4))
    if to >= 0:
        a = appear(to, 8)
        hd = text('OVERALL', 'title_it', 40, GOLD, stroke=3, sfill=INK, shadow=3)
        paste(c, hd, MOVX + MOVW / 2 - hd.shape[1] / 2, MROW0 - 58, a)
        nt = text('one judgment, not an average', 'sub', 26, LIGHT, stroke=2, sfill=INK)
        paste(c, nt, MOVX + MOVW / 2 - nt.shape[1] / 2 - 20, MROW0 + 6 * MROWH - 2, a)
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
    if target is not None and f >= target:
        tt = f - target
        a = appear(tt, 10)
        hd = text('TARGET', 'title_it', 40, WHITE, stroke=3, sfill=INK, shadow=3)
        paste(c, hd, MTGX + 80 - hd.shape[1] / 2, MROW0 - 58, a)
        for k in range(6):
            tk = tt - 3 * k
            if tk < 0:
                continue
            y = MROW0 + k * MROWH
            n = text('8+', 'title', 64, WHITE, stroke=4, sfill=INK, shadow=5)
            paste(c, n, MTGX + 80 - n.shape[1] / 2, y + (MROWH - 6) / 2 - n.shape[0] / 2 + (1 - ease_out(clamp(tk / 10))) * 30,
                  appear(tk, 8))


LOOP = ['CHANGE', 'RECAPTURE', 'RESCORE', 'KEEP OR REVERT']


def loop_strip(c, f, x, y, active, size=40, alpha=1.0, lit=None, centre=False):
    """The hill-climb loop: four steps with arrows; `active` is the lit step (or None)."""
    parts = []
    for k, s in enumerate(LOOP):
        on = (active == k) or (lit is not None and k <= lit)
        parts.append(pill(f'{k + 1}  {s}', size, INK if on else PALE, GOLD if on else NAVY3))
    arrow = text('→', 'title', size + 4, GOLD, stroke=2, sfill=INK)
    total = sum(p.shape[1] for p in parts) + arrow.shape[1] * 3 + 16 * 6
    xx = W / 2 - total / 2 if centre else x
    xs = []
    for k, p in enumerate(parts):
        paste(c, p, xx, y, alpha)
        xs.append((xx, xx + p.shape[1]))
        xx += p.shape[1] + 16
        if k < 3:
            paste(c, arrow, xx, y - 4, alpha)
            xx += arrow.shape[1] + 16
    # the return line back to step 1 (it is a loop)
    ph = parts[0].shape[0]
    ry = int(y + ph + 10)
    if alpha > 0:
        a0, a1 = int((xs[0][0] + xs[0][1]) / 2), int((xs[3][0] + xs[3][1]) / 2)
        box(c, a0, ry, a1 - a0, 4, GOLD, 0.7 * alpha)
        box(c, a0, ry - 10, 4, 10, GOLD, 0.7 * alpha)
        box(c, a1, ry - 10, 4, 14, GOLD, 0.7 * alpha)
    return total


# --------------------------------------------------------------------------- the family board


def tile_board(c, f, values, target, x0, y0, labw, tw, th, gap, rowh, lab_size, num_size,
               lit_until=None, order_t0=None, step=4, highlight=(), flags=None, alpha=1.0, met_colour=GOLD,
               notmet=()):
    """The 27 families in their group rows. A tile is gold when it meets the target. lit_until/order_t0 animate
    tiles turning on in reading order (one every `step` frames from order_t0). flags maps family -> (colour,
    start frame) for a pulse (drops, a send-back)."""
    n = 0
    for r, (label, fams) in enumerate(ROWS):
        y = y0 + r * rowh
        if labw < 400 and label.startswith('TIME ATTACK'):
            label = 'TIME ATTACK'
        lab = fit(label, 'title_it', lab_size, labw - 16, fill=PALE, stroke=2, sfill=INK, shadow=2)
        paste(c, lab, x0, y + th / 2 - lab.shape[0] / 2, alpha)
        for i, fam in enumerate(fams):
            x = x0 + labw + i * (tw + gap)
            v = values[fam]
            shown = True
            if order_t0 is not None:
                shown = f >= order_t0 + step * n
            n += 1
            met = shown and v not in ('?', '—') and float(v) >= target and fam not in notmet
            col = met_colour if met else (NAVY3 if shown else NAVY)
            box(c, x, y, tw, th, col, 0.95 * alpha)
            if fam in highlight:
                frame_rect(c, x, y, tw, th, WHITE, 4)
            if flags and fam in flags:
                fc, t0 = flags[fam]
                k = f - t0
                if 0 <= k < 40:
                    p = 0.5 + 0.5 * math.cos(k * 0.45)
                    box(c, x, y, tw, th, fc, 0.75 * p * alpha)
                    frame_rect(c, x, y, tw, th, fc, 4)
                elif k >= 40:
                    frame_rect(c, x, y, tw, th, fc, 3)
            if shown:
                num = text(v, 'title', num_size, INK if met else (WHITE if v != '?' else LIGHT),
                           stroke=0 if met else 3, sfill=INK)
                paste(c, num, x + tw / 2 - num.shape[1] / 2, y + th / 2 - num.shape[0] / 2 + 2, alpha)


BIG = dict(x0=70, y0=262, labw=520, tw=176, th=86, gap=12, rowh=100, lab_size=42, num_size=56)
SMALL = dict(x0=1052, y0=508, labw=280, tw=70, th=46, gap=7, rowh=56, lab_size=26, num_size=32)


def count9(values, target=9.0):
    return sum(1 for v in values.values() if v not in ('?', '—') and float(v) >= target)


# -------------------------------------------------------------------------------- the chapters
WALL_LABEL_T = [F(4 + 0.5 * k) for k in range(6)]     # group labels land
WALL_OUT = F(16)                                      # the round-0 wall has faded out under the matrix
MATRIX_T = F(8)


def wall_cells(c, f, era, s0s, t_in, dim=0.0, labels=None, drop=True, pills=True):
    for k, (g, label, take) in enumerate(GROUPS):
        t0 = t_in + F(0.5 * k) if drop else t_in
        if f < t0:
            continue
        x, y = (k % 3) * 640, 92 + (k // 3) * 448
        dy = int(round((1 - ease_out(clamp((f - t0) / 12))) * -500)) if drop else 0
        img = up(clip(era, take).native(s0s[take] + f - t_in), 2)
        yy = y + dy
        top = max(0, 92 - yy) if k < 3 else 0
        if yy + 448 > 0:
            c[yy + top:yy + 448, x:x + 640] = img[top:]
            if dim:
                c[max(92, yy):yy + 448, x:x + 640] *= 1 - dim
    # seams between cells, so six menus read as six things
    a = 0.9 * (clamp((f - t_in - F(2.5) - 6) / 8) if drop else 1.0)
    if f >= t_in and a > 0:
        box(c, 638, 92, 4, 896, GOLD, a)
        box(c, 1278, 92, 4, 896, GOLD, a)
        box(c, 0, 538, W, 4, GOLD, a)


def ch_assignment(f, shot, edit):
    """b0-24: the ask, the rubric, the goal (one continuous screen so the labels can travel)."""
    c = stage(f)
    wall_dim = 0.55 if f < F(4) else 0.0
    if f >= F(4):
        wall_dim = 0.55 * (1 - smooth(clamp((f - F(4)) / 8)))
    if f >= MATRIX_T:
        wall_dim = 0.55 + 0.32 * smooth(clamp((f - MATRIX_T) / 10))
        wall_dim += (1 - wall_dim) * smooth(clamp((f - WALL_OUT + 16) / 16))
    if f < WALL_OUT:    # gone before the shortest take (legal, 420 frames) would run out
        wall_cells(c, f, 'pre', WALL_PRE, 0, dim=wall_dim)
    if f < F(4):        # a band behind the opening statement
        a = clamp(f / 8) * clamp((F(4) - f) / 8)
        box(c, 0, 380, W, 230, DEEP, 0.78 * a)
    if f >= MATRIX_T:   # a navy wash under the matrix
        box(c, 0, 0, W, H, DEEP, 0.55 * smooth(clamp((f - MATRIX_T) / 10)))
    # group labels: land on their cells, then fly to the matrix rows
    for k, (g, label, take) in enumerate(GROUPS):
        t0 = WALL_LABEL_T[k]
        if f < t0:
            continue
        p = pill(label, 40)
        ax, ay = label_anchor_wall(k)
        if f >= MATRIX_T:
            u = ease_out(clamp((f - MATRIX_T - 2 * k) / 14))
            bx, by = label_anchor_matrix(k)
            ax, ay = ax + (bx - ax) * u, ay + (by - ay) * u
        s = 1 + 0.4 * (1 - ease_out(clamp((f - t0) / 8)))
        img = promo_kit.scaled(p, s) if s != 1 else p
        paste(c, img, ax, ay, clamp((f - t0) / 3))
    if f >= MATRIX_T:
        matrix(c, f, MATRIX_T + 6, target=F(16.5))
    return c


def ch_assignment_text(c, f, o, edit):
    say(c, f, 0, F(4) - 2, 'WE GAVE AN AI EVERY OPENGGF MENU.', 470, size=110,
        kicker='CLAUDE OPUS  ·  AN AI DESIGN REVIEW  ·  27 OCT 2026')
    say(c, f, F(4), F(8) - 2, 'STEP 1: SORT THEM INTO GROUPS.', 2, size=64)
    say(c, f, F(8) + 4, F(16), 'STEP 2: SCORE EACH GROUP, 1 TO 10.', 92, size=88,
        kicker='JUDGED FROM SCREENSHOTS, ON SEVEN CRITERIA')
    say(c, f, F(16), F(24) + 4, 'STEP 3: EVERY GROUP TO 8 OR BETTER.', 92, size=88,
        kicker='THE TARGET')
    # the scale, then the loop
    t = f - F(13)
    if F(13) <= f < F(20):
        a = clamp(t / 10) * clamp((F(20) - f) / 8)
        items = [('5', 'visibly amateur'), ('7', 'good indie'), ('9', 'production polish')]
        imgs = []
        for n, s in items:
            imgs.append((text(n, 'title', 70, GOLD, stroke=4, sfill=INK, shadow=5),
                         text(s, 'sub', 40, PALE, stroke=3, sfill=INK, shadow=3)))
        total = sum(a_.shape[1] + b_.shape[1] + 90 for a_, b_ in imgs) - 90
        x = W / 2 - total / 2
        for a_, b_ in imgs:
            paste(c, a_, x, 930, a)
            paste(c, b_, x + a_.shape[1] + 8, 952, a)
            x += a_.shape[1] + b_.shape[1] + 90
    if f >= F(20):
        k = int(clamp((f - F(20)) // F(1), 0, 3))
        a = clamp((f - F(20)) / 8)
        lab = text('EVERY ROUND', 'sub', 30, LIGHT, tracking=6)
        paste(c, lab, W / 2 - lab.shape[1] / 2, 892, a)
        loop_strip(c, f, 0, 934, None, 40, a, lit=k, centre=True)


# ch4: rounds 1-4 --------------------------------------------------------------------------------
PANE_L = (56, 92)
COL_X = 1392
LAPS = [  # (change, recapture, rescore, keep) beats per round; laps get faster as the climb gathers pace
    (25, 26.5, 27, 27.5), (28, 28.5, 29, 29.5), (29.75, 30, 30.25, 30.5), (30.75, 31, 31.25, 31.5)]
RESCORE = [F(l[2]) for l in LAPS]


def round_at(f):
    r = 0
    for k, t in enumerate(RESCORE):
        if f >= t:
            r = k + 1
    return r


def lap_step(f):
    for k, lap in enumerate(LAPS):
        if F(lap[0]) <= f < (F(LAPS[k + 1][0]) if k + 1 < len(LAPS) else F(32)):
            return max(i for i, b in enumerate(lap) if f >= F(b))
    return None


def six_rows(c, f, x, y, focus):
    """Overall per group after the current round, rolling at each rescore."""
    r = round_at(f)
    t = f - RESCORE[r - 1] if r else 99
    for k, (g, label, _) in enumerate(GROUPS):
        yy = y + k * 104
        lab = pill(label, 30, INK if g == focus else PALE, GOLD if g == focus else NAVY3)
        paste(c, lab, x, yy + 18)
        old = ROUNDS[r - 1][g] if r else None
        roll(c, old, ROUNDS[r][g], W - 40, yy - 6, t, size=86, colour=WHITE if g != focus else GOLD, dur=10,
             anchor='right')


def climb_column(c, f, focus):
    x = COL_X
    r = round_at(f)
    paste(c, text('STEP 3  ·  THE HILL CLIMB', 'sub', 30, LIGHT, tracking=4), x, 96)
    rt = text(f'ROUND {r}', 'title', 100, WHITE, stroke=5, sfill=INK, shadow=6)
    paste(c, rt, x, 128)
    st = lap_step(f)
    # the loop, compact: four dots, the lit step named
    for k in range(4):
        on = st is not None and k <= st
        box(c, x + k * 122, 262, 110, 14, GOLD if on else NAVY3)
    if st is not None:
        nm = text(LOOP[st], 'title_it', 40, GOLD, stroke=3, sfill=INK, shadow=3)
        paste(c, nm, x, 282)
    six_rows(c, f, x, 350, focus)
    if r == 4 and f >= F(31.5):
        a = clamp((f - F(31.5)) / 6)
        t = text('CLOSE. NOT 8 YET.', 'title_it', 52, AMBER, stroke=4, sfill=INK, shadow=4)
        paste(c, t, x, 984, a)


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
    if f < F(28):
        key, focus, t0, t1 = 'lib', 'D', F(25), F(26.5)
    else:
        key, focus, t0, t1 = 'notice', 'E', F(28.25), F(29.5)
    take = SRC[key][1]
    i = src(key, f)
    d = sweep(f, t0, t1)
    img = compare_native(clip('pre', take).native(i), clip('new', take).native(i), d)
    put(c, up(img, 4), x, y)
    divider(c, x, y, d, 4)
    era_tabs(c, x, y, d, 4, 'ROUND 0 · 27 OCT', 'AT 8 · 28 OCT')
    # recapture: the camera flash on the pane's frame
    for lap in LAPS:
        k = f - F(lap[1])
        if 0 <= k < 8:
            frame_rect(c, x, y, 1280, 896, WHITE, 6 + int(10 * (1 - k / 8)))
    climb_column(c, f, focus)
    return c


# ch5-7: every family, all at 8, the turn ---------------------------------------------------------
TILE_ON = F(32.5)
TA_CMP = (F(36), F(40))
ALL8 = F(40)
TURN = F(48)


def board_values_8(f):
    return PASSES['t8'] if f >= ALL8 else PASSES['t8_pre']


def target_at(f):
    return 9.0 if f >= TURN else 8.0


def ch_families(f, shot, edit):
    c = stage(f)
    if TA_CMP[0] <= f < TA_CMP[1]:
        return ta_compare(c, f)
    vals = board_values_8(f)
    tgt = 8.0
    flags = None
    if f >= TURN:       # every tile falls below the new target, a sweep from the left
        tgt = 9.0
    order = TILE_ON if f < TA_CMP[0] else None
    tile_board(c, f, vals, tgt if f < TURN or f >= TURN + 18 else 8.0, order_t0=order, step=3, flags=flags,
               met_colour=GOLD, **BIG)
    if TURN <= f < TURN + 18:   # the drop sweeps left -> right across the board
        u = smooth((f - TURN) / 18)
        edge = int(W * u)
        cover = stage(f)
        tile_board(cover, f, vals, 9.0, **BIG)
        c[:, :edge] = cover[:, :edge]
    # stragglers: name them while they are below 8
    if TILE_ON + 30 <= f < TA_CMP[0]:
        a = clamp((f - TILE_ON - 30) / 8)
        for fam in ('F4 Editor HUD', 'SP Stageplay', 'TA Time Attack'):
            r = next(i for i, (_, fs) in enumerate(ROWS) if fam in fs)
            i = ROWS[r][1].index(fam)
            bx = BIG['x0'] + BIG['labw'] + i * (BIG['tw'] + BIG['gap'])
            by = BIG['y0'] + r * BIG['rowh']
            frame_rect(c, bx, by, BIG['tw'], BIG['th'], AMBER, 4)
    # target chip
    tc = 'TARGET 9' if f >= TURN else 'TARGET 8'
    chip_ = pill(tc, 44, INK, GOLD if f < TURN else WHITE)
    paste(c, chip_, W - 60 - chip_.shape[1], 200)
    if f >= TURN:
        n = text('AT 9:  0 / 27', 'title_it', 44, PALE, stroke=3, sfill=INK, shadow=3)
        paste(c, n, W - 60 - chip_.shape[1] - 30 - n.shape[1], 200, clamp((f - TURN - 24) / 8))
    return c


def ta_compare(c, f):
    x, y = PANE_L
    d = sweep(f, F(36.75), F(38.25))
    img = compare_native(still('ta_pre'), still('ta_8'), d)
    put(c, up(img, 4), x, y)
    divider(c, x, y, d, 4)
    era_tabs(c, x, y, d, 4, 'BEFORE · 28 OCT', 'AFTER · 28 OCT')
    cx = COL_X
    paste(c, text('FURTHEST BELOW 8', 'sub', 30, LIGHT, tracking=6), cx, 96)
    paste(c, text('TIME ATTACK', 'title', 92, WHITE, stroke=5, sfill=INK, shadow=6), cx, 128)
    paste(c, text('the bundled race mod', 'sub', 40, GOLD, stroke=3, sfill=INK, shadow=3), cx, 238)
    t = f - F(38.5)
    roll(c, '5.5' if t >= 0 else None, '8' if t >= 0 else '5.5', cx - 6, 310, t, size=260, dur=12)
    paste(c, text('also:', 'sub', 36, LIGHT, stroke=2, sfill=INK), cx, 680)
    for k, s in enumerate(('Editor HUD  7.5 → 8', 'Stageplay editor  7.5 → 8')):
        paste(c, text(s, 'title_it', 46, PALE, stroke=3, sfill=INK, shadow=3), cx, 726 + k * 64)
    paste(c, text('screens judged by Claude Opus from captures', 'sub', 28, LIGHT, stroke=2, sfill=INK), cx, 900)
    return c


def ch_families_text(c, f, o, edit):
    say(c, f, F(32), F(36) - 2, 'THEN EVERY MENU, FAMILY BY FAMILY: 27.', 96, size=84,
        kicker='ALL-MENUS PASS  ·  EVERY CRITERION AND OVERALL TO 8')
    if F(40) <= f < F(44):
        t = f - F(40)
        s = 1 + 0.6 * (1 - ease_out(clamp(t / 12)))
        box(c, 0, 0, W, H, DEEP, 0.55 * clamp(t / 6) * clamp((F(44) - f) / 8))
        img = text('ALL 27 AT 8', 'title', 210, WHITE, stroke=12, sfill=INK, shadow=14)
        img = promo_kit.scaled(img, s) if s != 1 else img
        shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0
        paste(c, img, W / 2 - img.shape[1] / 2 + shake, 560 - img.shape[0] / 2, clamp(t / 3) * clamp((F(44) - f) / 8))
        d = pill('28 OCT 2026', 44)
        paste(c, d, W / 2 - d.shape[1] / 2, 700, clamp((t - 8) / 8) * clamp((F(44) - f) / 8))
        say(c, f, F(40), F(44), 'GOAL MET.', 96, size=84, kicker='STEP 3 DONE')
    say(c, f, F(44), F(48), 'THEN WE RAISED THE BAR.', 96, size=96)
    # the turn: ROAD / TO / 9, then the meaning of 9
    if TURN <= f < F(52):
        for word, b, y, xc in (('ROAD', 48, 360, 640), ('TO', 48.5, 590, 640)):
            t = f - F(b)
            if t < 0:
                continue
            img = text(word, 'title', 190, WHITE, stroke=10, sfill=INK, shadow=11)
            img = promo_kit.scaled(img, 0.4 + 0.6 * back(clamp(t / 10), 2.2))
            paste(c, img, xc - img.shape[1] / 2, y - img.shape[0] / 2, clamp(t / 3) * clamp((F(52) - f) / 8))
        t = f - F(49)
        if t >= 0:
            nine = text('9', 'title', 660, GOLD, stroke=14, sfill=INK, shadow=18)
            nine = promo_kit.scaled(nine, 1 + 0.35 * (1 - ease_out(clamp(t / 12))))
            paste(c, nine, 1240 - nine.shape[1] / 2, 560 - nine.shape[0] / 2, clamp(t / 3) * clamp((F(52) - f) / 8))
    if F(48) <= f < F(52):   # dim the board under the title words
        pass
    say(c, f, F(52), F(56), '9 MEANS PRODUCTION POLISH. NONE ARE THERE.', 96, size=80,
        kicker='NEW TARGET  ·  28 OCT')


def turn_dim(c, f, o, edit):
    a = smooth(clamp((f - TURN) / 6)) * (1 - smooth(clamp((f - F(51.5)) / 10)))
    if a > 0:
        c *= 1 - 0.55 * a


# ch8-11: the road to 9 ---------------------------------------------------------------------------
EP = (48, 228)          # evidence pane (3x, 960x672)
P1 = F(58)              # pass 1 rescore
REV_T = F(64)           # the review's mark-up starts
DROP = F(67)            # the review's scores
STR_T = F(72)
STR_SWEEP = (F(73), F(74.5))
HUB9 = F(75)
TALLY13 = F(76)
SENTBACK = F(80)
SET_SWEEP = (F(82), F(83.5))
TALLY26 = F(82.5)
TA_LAST = F(86)
SLAM = F(88)

ORDER = [f for f in FAM]    # reading order for tallies


def road_state(f):
    """(values, flags, families at 9, sent-back families) on the road to 9 at frame f."""
    flags, rejected = {}, set()
    if f < P1:
        return dict(PASSES['t8']), flags, 0, rejected
    if f < DROP:
        for k in ('A1 Hub', 'A5 Help', 'F4 Editor HUD', 'F5 Toast', 'SP Stageplay'):
            flags[k] = (WHITE, P1)
        return dict(PASSES['p1']), flags, 0, rejected
    if f < STR_T:
        for j, k in enumerate(('A1 Hub', 'A5 Help', 'F4 Editor HUD', 'SP Stageplay')):
            flags[k] = (RED, DROP + 6 * j)
        flags['E1-2 Notices'] = (WHITE, DROP + 24)
        flags['F6-10 HUD plates'] = (LIGHT, DROP + 30)
        return dict(PASSES['rev']), flags, 0, rejected
    if f < SENTBACK:
        v = dict(PASSES['rev'])
        goal = PASSES['str']
        nines = ['A1 Hub'] + [k for k in ORDER if goal[k] == '9' and k != 'A1 Hub']   # the pictured fix first
        n_on = (1 if f >= HUB9 else 0) + (max(0, min(12, (f - TALLY13) // 7 + 1)) if f >= TALLY13 else 0)
        if f >= TALLY13:
            for k in ORDER:          # the families that stay 8.5 settle with the tally
                if goal[k] != '9':
                    v[k] = goal[k]
        for k in nines[:n_on]:
            v[k] = '9'
        return v, flags, n_on, rejected
    v = dict(PASSES['str'])
    flags['F3 Editor projects'] = (RED, SENTBACK)
    if f < TALLY26:
        return v, flags, 12, {'F3 Editor projects'}
    goal = PASSES['fin']
    todo = ['F3 Editor projects'] + [k for k in ORDER if goal[k] == '9' and v[k] != '9']
    for k in todo[:max(0, min(len(todo), (f - TALLY26) // 6 + 1))]:
        v[k] = '9'
    if f < TALLY26 + 6 * 0 + 1:
        rejected = {'F3 Editor projects'}
    if f >= TA_LAST:
        flags['TA Time Attack'] = (AMBER, TA_LAST)
    n = count9(v) - (1 if 'F3 Editor projects' in rejected else 0)
    return v, flags, n, rejected


@lru_cache(maxsize=1)
def review_marks():
    base = up(still('hub_p1'), 3)
    mark = still('hub_rev')
    return base, mark, np.abs(mark - base).sum(axis=2) > 0


def evidence(c, f):
    """The left pane: the hub picture through pass 1, review and fix; then Settings; then Time Attack."""
    x, y = EP
    if f < P1:
        img = up(still('hub_t8'), 3)
        lab = 'CROWDED HUB  ·  THE 8 BUILD'
    elif f < REV_T:
        img = up(still('hub_p1'), 3)
        lab = 'PASS 1: A SUMMARY LINE ADDED'
    elif f < STR_T:
        base, mark, diff = review_marks()
        u = smooth(clamp((f - REV_T) / F(2)))
        reveal = diff & (np.arange(960)[None, :] < 960 * u)
        img = base.copy()
        img[reveal] = mark[reveal]
        lab = 'THE REVIEWER’S MARKED-UP CAPTURE'
    elif f < SENTBACK + F(1.5):
        old = still('hub_rev')
        new = up(still('hub_str'), 3)
        d = sweep(f, *STR_SWEEP)
        px = int(round(d)) * 3
        img = old.copy()
        img[:, :px] = new[:, :px]
        put(c, img, x, y)
        divider(c, x, y, d, 3)
        era_tabs(c, x, y, d, 3, 'MARKED UP', 'REBUILT · 28 OCT')
        return 'hub'
    elif f < TA_LAST:
        i = src('set_fin', f)
        d = sweep(f, *SET_SWEEP)
        img = up(compare_native(still('set_str'), clip('new', 'settings').native(i), d), 3)
        put(c, img, x, y)
        divider(c, x, y, d, 3)
        era_tabs(c, x, y, d, 3, 'PASS 2', 'PASS 3 · DELIVERED')
        return 'settings'
    else:
        img = up(still('ta_tab'), 3)
        put(c, img, x, y)
        # the cap that changed: 'TAB: DETAILS' on the chat card (native x 91-166, y 83-95)
        k = f - TA_LAST
        if k >= 6:
            frame_rect(c, x + 3 * 90, y + 3 * 82, 3 * 78, 3 * 14, GOLD, 5)
        pl = pill('TIME ATTACK LOBBY  ·  29 OCT', 36)
        paste(c, pl, x, y - 6 - 10 - pl.shape[0])
        return 'ta'
    put(c, img, x, y)
    pl = pill(lab, 36)
    paste(c, pl, x, y - 6 - 10 - pl.shape[0])
    return 'hub'


SUBJECT = {  # (name, [(frame, value)]) for the big score beside the evidence
    'hub': ('HUB', [(0, '8'), (P1, '8.5'), (DROP, '8'), (HUB9, '9')]),
    'settings': ('SETTINGS', [(0, '8.5'), (SET_SWEEP[1], '9')]),
    'ta': ('TIME ATTACK', [(0, '8.5')]),
}


def subject(c, f, which):
    name, stops = SUBJECT[which]
    k = max(i for i, (t, _) in enumerate(stops) if f >= t or i == 0)
    t = f - stops[k][0]
    x = 1052
    paste(c, text(name, 'title', 70, WHITE, stroke=4, sfill=INK, shadow=5), x, 222)
    prev = stops[k - 1][1] if k > 0 else None
    down = prev is not None and float(stops[k][1]) < float(prev)
    col = RED if down and t < 40 else GOLD
    shape = roll(c, prev, stops[k][1], x - 4, 290, t, size=180, colour=col, dur=12)
    ten = text('/10', 'title', 56, LIGHT, stroke=3, sfill=INK, shadow=4)
    paste(c, ten, x + shape[1] - 26, 290 + shape[0] - ten.shape[0] - 24)


def counter(c, f, n, target=9):
    x = 1420
    paste(c, text(f'FAMILIES AT {target}', 'sub', 30, LIGHT, tracking=4), x, 230)
    big = text(f'{n}', 'title', 150, WHITE if n < 27 else GOLD, stroke=7, sfill=INK, shadow=8)
    paste(c, big, x, 262)
    of = text('/ 27', 'title', 80, LIGHT, stroke=4, sfill=INK, shadow=5)
    paste(c, of, x + big.shape[1] + 10, 330)


def ch_road(f, shot, edit):
    c = stage(f)
    which = evidence(c, f)
    v, flags, n, rejected = road_state(f)
    subject(c, f, which)
    counter(c, f, n)
    focus = {'hub': ('A1 Hub',), 'settings': ('B1 Settings',), 'ta': ('TA Time Attack',)}[which]
    tile_board(c, f, v, 9.0, flags=flags, highlight=focus, notmet=rejected, **SMALL)
    if SENTBACK <= f < TALLY26 + 30:     # name the family that was sent back
        r = 5
        i = ROWS[r][1].index('F3 Editor projects')
        bx = SMALL['x0'] + SMALL['labw'] + i * (SMALL['tw'] + SMALL['gap'])
        by = SMALL['y0'] + r * SMALL['rowh']
        lab = pill('EDITOR PROJECTS: SENT BACK', 26, WHITE, RED)
        paste(c, lab, min(bx, W - 20 - lab.shape[1]), by - lab.shape[0] - 4,
              clamp((f - SENTBACK) / 6) * clamp((TALLY26 + 30 - f) / 8))
    if DROP + 30 <= f < STR_T:
        nt = text('? = its screenshots turned out to be invalid', 'sub', 26, LIGHT, stroke=2, sfill=INK)
        paste(c, nt, SMALL['x0'], SMALL['y0'] + 7 * SMALL['rowh'] + 2, clamp((f - DROP - 30) / 8))
    return c


def ch_road_text(c, f, o, edit):
    say(c, f, F(56), F(60) - 2, 'PASS 1: POLISH. SOME 8.5s, NO 9s.', 40, size=84, kicker='28 OCT')
    quote(c, f, F(60), F(64), 'No family reached 9 overall in this pass.', '— the design review, 28 Oct')
    say(c, f, F(64), F(68) - 2, 'A FRESH AI REVIEW MARKED UP THE PICTURES.', 40, size=80,
        kicker='SECOND OPINION  ·  A NEW CLAUDE OPUS SESSION')
    say(c, f, F(68), F(72), 'SCORES WENT DOWN, NOT UP.', 40, size=92, colour=WHITE, kicker='ITS VERDICT')
    say(c, f, F(72), F(80) - 2, 'PASS 2: FIX THE STRUCTURE, NOT THE POLISH.', 40, size=78, kicker='28 OCT')
    quote(c, f, F(72), F(80), 'The remaining blockers are structural rather than polish.',
          '— the design review, 28 Oct')
    say(c, f, F(80), F(82.5) - 2, 'ANOTHER REVIEW SENT ONE 9 BACK.', 40, size=84, kicker='CHECKED AGAIN')
    say(c, f, F(82.5), F(86) - 2, 'PASS 3: FINISH WHAT THE REVIEW FOUND.', 40, size=84, kicker='28–29 OCT')
    say(c, f, F(86), F(88), 'LAST GAP: ONE KEYBOARD HINT.', 40, size=84, kicker='26 OF 27')


# ch12: 27 / 27 and the six groups, delivered ----------------------------------------------------


def ch_payoff(f, shot, edit):
    """27 / 27 slams over the all-gold board, then the hub's final criteria row shows what 'overall' means."""
    c = stage(f)
    tile_board(c, f, PASSES['lead'], 9.0, **BIG)
    t = f - SLAM
    box(c, 0, 0, W, H, DEEP, 0.35 + 0.45 * smooth(clamp((t - 30) / 12)))
    s_ = 1 + 0.5 * (1 - ease_out(clamp(t / 12)))
    y_big = 330 - 230 * smooth(clamp((t - 30) / 14))
    big = text('27 / 27 AT 9', 'title', 230, WHITE, stroke=12, sfill=INK, shadow=14)
    big = promo_kit.scaled(big, s_) if s_ != 1 else big
    shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0
    paste(c, big, W / 2 - big.shape[1] / 2 + shake, y_big + 200 - big.shape[0] / 2, clamp(t / 3))
    a = smooth(clamp((t - 36) / 10))
    if a > 0:   # the honest row: overall 9 is a judgment; two of the hub's criteria stay 8.5
        y = 640
        kick = text('THE HUB, FINAL SCORES', 'sub', 30, LIGHT, tracking=6)
        paste(c, kick, W / 2 - kick.shape[1] / 2, y - 110, a)
        for j, name in enumerate(CRITERIA):
            x = MCOL0 + j * MCOLW + 6
            hd = fit(name, 'title_it', 32, MCOLW - 10, fill=PALE, stroke=2, sfill=INK)
            paste(c, hd, MCOL0 + j * MCOLW + MCOLW / 2 - hd.shape[1] / 2, y - 54, a)
            v = HUB_FINAL[0][j]
            box(c, x, y, MCOLW - 12, MROWH - 10, heat(v), 0.95 * a)
            n = text(f'{v:g}', 'title', 54, INK if v >= 9 else WHITE, stroke=0 if v >= 9 else 3, sfill=INK)
            paste(c, n, x + (MCOLW - 12) / 2 - n.shape[1] / 2, y + (MROWH - 10) / 2 - n.shape[0] / 2 + 2, a)
            if v < 9:
                frame_rect(c, x, y, MCOLW - 12, MROWH - 10, WHITE, 3)
        lab = pill('HUB & DIALOGS', 40)
        paste(c, lab, MX, y + 14, a)
        hd = text('OVERALL', 'title_it', 40, GOLD, stroke=3, sfill=INK, shadow=3)
        paste(c, hd, MOVX + MOVW / 2 - hd.shape[1] / 2, y - 58, a)
        box(c, MOVX, y - 4, MOVW, MROWH - 2, INK, 0.8 * a)
        frame_rect(c, MOVX, y - 4, MOVW, MROWH - 2, GOLD, 3)
        n = text('9', 'title', 76, GOLD, stroke=4, sfill=INK, shadow=5)
        paste(c, n, MOVX + MOVW / 2 - n.shape[1] / 2, y + (MROWH - 6) / 2 - n.shape[0] / 2, a)
    say(c, f, SLAM + 44, IRIS + 20, 'EVERY FAMILY 9 OVERALL. SOME CRITERIA STILL 8.5.', 800, size=72)
    return c


def ch_delivered(f, shot, edit):
    c = stage(f)
    wall_cells(c, f, 'new', WALL_NEW, IRIS, drop=False)
    for k, (g, label, take) in enumerate(GROUPS):
        ax, ay = label_anchor_wall(k)
        paste(c, pill(label, 40), ax, ay)
    pn = pill('THE SAME SIX GROUPS, DELIVERED  ·  29 OCT', 44)
    paste(c, pn, W / 2 - pn.shape[1] / 2, 20)
    u = smooth(clamp((f - F(95)) / 24))
    if u > 0:
        blurred = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(6 * u)), np.float32)
        c = blurred * (1 - 0.72 * u)
    return c


def end_card(c, f, o, edit):
    badge = np.asarray(Image.open(BADGE).convert('RGBA'), np.float32)
    lines = [
        (badge, 96, 95),
        (text('ROAD TO 9', 'title', 130, GOLD, stroke=8, sfill=INK, shadow=10), 368, 96),
        (text('An AI design review of every OpenGGF menu, round by round.', 'sub', 52, WHITE, stroke=4, sfill=INK,
              shadow=5), 520, 97),
        (text('github.com/OpenGGF/OpenGGF', 'title_it', 78, WHITE, stroke=5, sfill=INK, shadow=6), 610, 98),
        (text('In development for OpenGGF 0.7', 'body', 42, LIGHT, stroke=3, sfill=INK, shadow=4), 726, 99),
        (text('Scored and rebuilt by AI agents: Claude Opus 5.5, with OpenAI Codex GPT-6.1 on later passes.',
              'body', 32, PALE, stroke=2, sfill=INK, shadow=3), 830, 99.5),
        (text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body', 36, PALE,
              stroke=2, sfill=INK, shadow=3), 900, 100),
    ]
    for img, y, b in lines:
        t = f - F(b)
        if t >= 0:
            paste(c, img, W / 2 - img.shape[1] / 2, y + (1 - ease_out(clamp(t / 12))) * 30, clamp(t / 8))


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
    # 1-3 the assignment: ask, rubric, goal and loop
    e.S(Custom(0, F(24), ch_assignment))
    e.O(Fn(0, F(24) + 8, ch_assignment_text))
    for k in range(6):
        X(WALL_LABEL_T[k], sfx('cd'), 1.0)
    X(MATRIX_T - 3, sfx('ab'), 1.3)
    for k in range(6):
        X(MATRIX_T + 6 + F(4) + 4 * k, sfx('cd'), 1.0)          # the overall column, one judgment per group
    for k in range(4):
        X(F(20 + k), sfx('cd'), 1.0)                            # the loop's steps
    CHAPTERS += [(0, F(8), 'The ask: an AI gets every OpenGGF menu and sorts them into six groups'),
                 (F(8), F(16), 'The rubric: seven criteria, 1 to 10, one overall judgment'),
                 (F(16), F(24), 'The goal: every group to 8 or better, one loop per round')]
    wall = ', '.join(f'pre/{t} take frames {s}-{s + WALL_OUT - 1}' for t, s in WALL_PRE.items())
    EDL.append((0, WALL_OUT, CHAPTERS[0][2] + ' / rubric', 'wall of six cells 2x (3x2), dimmed under the matrix '
                'from b8, faded out by b16', wall))
    EDL.append((WALL_OUT, F(24), CHAPTERS[2][2], 'matrix, target column and loop', 'editorial board'))
    # 4 rounds 1-4
    ch = 'Rounds 1-4: Mod manager and legal notice, round 0 to the 8 build; six groups 7 to 7.5'
    e.S(Custom(F(24), F(32), ch_rounds, trans='wipe', tdur=14))
    X(F(24) - 4, sfx('ab'), 1.3)
    for t in RESCORE:
        X(t, sfx('cd'), 1.0)
    map_cues('lib', lambda f: 'new' if sweep(f, F(25), F(26.5)) >= 160 else 'pre')
    map_cues('notice', lambda f: 'new' if sweep(f, F(28.25), F(29.5)) >= 160 else 'pre')
    CHAPTERS.append((F(24), F(32), ch))
    EDL.append((F(24), F(28), ch, 'pane 4x + six-row board; divider b25-26.5',
                f'pre+new/mods take frames {SRC["lib"][4]}-{src("lib", F(28) - 1)}'))
    EDL.append((F(28), F(32), ch, 'pane 4x + six-row board; divider b28.25-29.5',
                f'pre+new/legal take frames {SRC["notice"][4]}-{src("notice", F(32) - 1)}'))
    # 5-7 every family, all at 8, the turn
    ch = 'Every menu family: 27 tiles; Time Attack 5.5 to 8'
    e.S(Custom(F(32), F(56), ch_families, trans='wipe', tdur=14))
    e.O(Fn(TURN, F(52) + 10, turn_dim))
    e.O(Fn(F(32), F(56), ch_families_text))
    X(F(32) - 4, sfx('ab'), 1.3)
    for k in range(0, 24, 3):
        X(TILE_ON + 3 * k, sfx('cd'), 0.9)
    X(F(38.5), sfx('cd'), 1.0)
    X(ALL8, sfx('c5'), 0.5)
    e.O(Flash(ALL8, 14, 0.7))
    X(TURN, sfx('bc'), 1.0)
    e.O(Flash(TURN, 14, 0.8))
    CHAPTERS += [(F(32), F(40), ch), (F(40), F(48), 'All 27 at 8; then we raised the bar'),
                 (F(48), F(56), 'Road to 9: the new target, 9 = production polish')]
    EDL.append((F(32), F(36), ch, 'full family board (tiles light on the stabs)', 'editorial board'))
    EDL.append((F(36), F(40), ch, 'pane 4x stills + column; divider b36.75-38.25',
                f'{STILL["ta_pre"]} | {STILL["ta_8"]}'))
    EDL.append((F(40), F(56), 'All 27 at 8 / road to 9', 'full family board, slam, target 8 -> 9', 'editorial board'))
    # 8-11 the road: pass 1, the fresh review, structure, finish
    e.S(Custom(F(56), SLAM, ch_road, trans='wipe', tdur=14))
    e.O(Fn(F(56), SLAM, ch_road_text))
    X(F(56) - 4, sfx('ab'), 1.3)
    X(P1, sfx('cd'), 1.0)
    for k in range(4):
        X(DROP + 6 * k, sfx('a8'), 2.0)
    X(DROP + 24, sfx('cd'), 1.0)
    X(STR_T - 4, sfx('ab'), 1.3)
    X(HUB9, sfx('cd'), 1.0)
    for k in range(12):
        X(TALLY13 + 7 * k, sfx('cd'), 0.9)
    X(SENTBACK, sfx('a8'), 2.0)
    for k in range(14):
        X(TALLY26 + 6 * k, sfx('cd'), 0.9)
    map_cues('set_fin', lambda f: 'new' if sweep(f, *SET_SWEEP) >= 160 else 'none')
    CHAPTERS += [(F(56), F(64), 'Pass 1: polish; no family reaches 9'),
                 (F(64), F(72), 'A fresh AI review marks up the pictures; scores go down'),
                 (F(72), F(80), 'Pass 2: structure; 13 families at 9'),
                 (F(80), SLAM, 'Another review sends one 9 back; pass 3 finishes 26; the last gap')]
    EDL.append((F(56), REV_T, 'Pass 1', 'evidence pane 3x + subject score + family board',
                f'{STILL["hub_t8"]} then {STILL["hub_p1"]}'))
    EDL.append((REV_T, STR_T, 'Fresh review', 'evidence pane: mark-up drawn onto the same capture',
                f'{STILL["hub_p1"]} + {STILL["hub_rev"]} (1:1)'))
    EDL.append((STR_T, F(81.5), 'Structure', 'divider b73-74.5', f'{STILL["hub_rev"]} | {STILL["hub_str"]}'))
    EDL.append((F(81.5), TA_LAST, 'Finish', 'divider b82-83.5, still | moving',
                f'{STILL["set_str"]} | new/settings take frames {SRC["set_fin"][4]}-{src("set_fin", TA_LAST - 1)}'))
    EDL.append((TA_LAST, SLAM, 'Last gap', 'evidence pane 3x', STILL['ta_tab']))
    # 12 payoff
    ch = '27 / 27 at 9 overall; the six groups, delivered'
    e.S(Custom(SLAM, IRIS, ch_payoff))
    e.S(Custom(IRIS, TOTAL, ch_delivered, trans='iris', tdur=24))
    X(SLAM, sfx('c5'), 0.6)
    e.O(Flash(SLAM, 18, 0.9))
    X(IRIS - 6, sfx('c3'), 0.7)
    CHAPTERS.append((SLAM, F(95), ch))
    EDL.append((SLAM, IRIS, ch, 'full family board, slam, the hub final criteria row', 'editorial board'))
    wall = ', '.join(f'new/{t} take frames {s}-{s + TOTAL - IRIS - 1}' for t, s in WALL_NEW.items())
    EDL.append((IRIS, TOTAL, ch, 'iris into the wall of six cells 2x; blurred under the end card from b95', wall))
    e.O(Fn(F(95), TOTAL, end_card))
    e.O(Flash(END_HIT, 10, 0.35))
    e.O(Fade(END_HIT + 12, TOTAL + 1))
    CHAPTERS.append((F(95), TOTAL, 'End card'))
    e.bed(MUSIC, 0, 0.75, length=BED_CUT / FPS, fade_out=0.01)
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
    lines = [';FFMETADATA1', 'title=ROAD TO 9 (hill-climb story): an AI design review of every OpenGGF menu',
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


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    e = edit()
    BUILD.mkdir(exist_ok=True)
    if cmd == 'check':
        for w in e.check():
            print('warning:', w)
        print('pacing:', e.pacing()[0])
        print('end', e.end(), f'{e.end() / FPS:.3f}s', 'cues', len(CUES), 'sfx', len(e.sfx))
    elif cmd == 'sheet':
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(e.contact_sheet(BUILD / 'sheet.png', step, 0, None, workers=8))
    elif cmd == 'keys':
        # review sheet of frames at the given bed beats (3 columns, 640x360 each)
        from PIL import ImageDraw
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
