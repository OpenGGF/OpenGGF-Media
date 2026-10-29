#!/usr/bin/env python3
"""ROAD TO 9, Super Sonic cut: the half-length recut of the OpenGGF menu evolution promo
(project menu-evolution, revision super-sonic-cut, 2026-10-29).

Brief (one line each)
  Request.   The user on the 87.333 s film: "bit slow and repetitive. Do it against the S2 super sonic
             music, half the length". Kept steering: "film it like a action movie montage, with various
             numbers slowly climbing".
  Response.  Cause, not symptom: the old cut spent 25 s before its first comparison and ran the same
             six-stop 3.5 -> 9 climb four times. This cut is rebuilt on the new track's own form; the
             prologue, round-0 grid and the fourth rep (hub & dialogs, the weakest visual change) are cut;
             the three strongest matched comparisons remain, each with a different move and a different
             climb; one build, one payoff, a button ending. 43.2 s, about half of 87.333 s.
  Audience.  Sonic fans and OpenGGF players who have met the engine's menus in 0.5 or 0.7 builds.
  Form.      Menu showcase cut as an action montage. Every UI frame is a real per-frame render of that
             era's production menu code driven by scripted keys (the original production's clips/, reused
             unchanged; sources/capture there). Menus are the subject because the user asked for an
             old-vs-new menu film, so the promo-direction gameplay quota is superseded; gameplay appears
             only under the in-game shader picker.
  Promise.   Every engine menu, rebuilt round by round: from 0.5 to 27 of 27 at 9.
  Numbers.   Only real, dated values: design-review scores (1-10, the review's own subjective judgments,
             not usability or performance measurements) from
             docs/architecture/audits/2026-10-27-menu-design-review.md at d823ce643 (SCORES), the version
             0.5 -> 0.7 and the menu families at 9 per pass. Every number stops only on a recorded value.
             Each climb moves differently: Libraries steps one recorded stop a beat (blips); Pickers climbs
             side by side on the bed's rising chromatic riff (silent ticks, the riff is the sound);
             Settings spins through its stops at two a beat in one sweep; the families tally counts up.
  Proof.     Matched tasks, old and new on one key timeline in sync:
             Cold open: the in-game display shader picker over Emerald Hill (debug text over the HUD ->
               a framed panel), a gold divider sweeping before -> now.
             Libraries (Mod manager): bracket strings -> switches; plain trust text -> a trust card;
               enabling Eggman's Sky, then Details.
             Pickers (Locate ROM): ROM? on every row -> icons and a scroll bar, both eras side by side at
               3x; picking the wrong file -> a clear error card.
             Settings (Display tab): truncated labels -> whole labels in groups; a switch toggles, a value
               changes, the save prompt lists old -> new.
  Eras.      0.5 = tag v0.5.20260411 (77c6364ce, glimpsed for one bar); "before" = develop 2f9ca84b1
             (27 Oct 2026, the round-0 menus); "now" = d823ce643 (29 Oct 2026, delivered).
  Hero.      27 / 27 slams onto the wall of new menus on the cadence of the Super Sonic loop, the menus
             relight one by one under the PSG cascade, a Giant Ring iris opens the delivered hub.
  Sound.     Sonic 2 "Super Sonic" (engine music 0x93 = native MusID_SuperSonic $96, ROM $FCBBC, canonical
             S2 REV01) through OpenGGF's SMPS driver, FmSfxRenderTool --paced, 48 kHz stereo, one bed from
             its first sample to the downbeat of its third loop. Measured: 146.48 BPM (header tempo $FA,
             24 ticks a beat, exactly 24.576 frames a beat at 60 Hz), first beat at sample 306 (frame 0),
             12-bar loop: INTRO 2 bars (kick/snare figure, chromatic riff climbing a semitone every half
             bar), A 4 bars (melody), B 4 bars (stabs, the quietest section), TURN 2 bars (C-E-G cadence
             with descending PSG runs, the loudest). The bed ends on the G-major stab that resolves the
             third loop's riff (frame 2555) and is cut in the eighth-note rest after it (frame 2566).
             Stingers (S2 REV01, the original production's renders): Spindash Release 0xBC on the title
             flash, Tally End 0xC5 on each 9 and on 27, Blip 0xCD on Libraries' and Settings' ticks and on
             the families tally, Swish 0xAB on the five chapter wipes and the cold-open sweep, Enter Giant
             Ring 0xC3 under the iris. Menu sounds are the engine's HostUiSfx tones placed at the cue frames
             each take logged, re-mapped through this cut's source intervals, only from the era on screen
             (side by side: once, the eras' cue frames and tones being identical; none under the end card).
             Fewer and quieter than r3b: 74 placed sounds instead of 117 (no wall-pop blips, no Tally End
             after each tally leg, no spindash charge, no jingle); bed 0.75, Tally End 0.7 (0.9 on 27),
             UI tones 0.7 (r3b 1.1), chosen from per-chapter loudness of the mix (edit.py loudness).
             Sound was checked by measurement only; nobody listened to this mix.
  Palette.   Sampled from d823ce643 menu frames: navy #051035 / #0a245c, deep #02081c, focus gold
             #ffd64c, pale #e8edff (unchanged from the original film).
  Type.      Fira Sans Compressed Heavy / Condensed (OFL, ttf-fira-sans 4.301) with stroke and hard
             shadow, so the film's voice never looks like the menus' pixel font.
  Pixels.    Native 320x224 captures at 60 Hz shown at integer 4x (centred and montage panes), 3x
             (side-by-side) or 2x (wall cells), nearest-neighbour, never fractionally zoomed; divider
             steps are whole game pixels.
  End card.  Badge, title, one line, URL, status, the fan-made disclaimer and the score source line.

Beat sheet (b = bed beat; frame F(b) = round(24.576 b); bar = 4 beats = 1.638 s; music section in [])
  b0-8     COLD OPEN  [INTRO 1]  EHZ1 run; the old picker opens b1; divider sweeps to now b4-6; "SAME GAME.
                      NEW MENUS." b5. Proves: same game, new menus, in 3.3 s.
  b8-16    TITLE      [A 1]      flash + spindash release; ROAD b8, TO b9, 9 b10 (ka-ching), line b12.
  b16-24   GLIMPSE    [A 1]      0.5 game select one bar (silent, as 0.5 was), push to the 0.7 hub before the
                      redesign; version pill rolls 0.5 -> 0.6 -> 0.7.
  b24-40   LIBRARIES  [B 1]      Mod manager opens on b24; old at 3.5; b28-31 one recorded stop a beat (divider
                      steps to each stop's share), 9 on b32 as the cut jumps to enabling Eggman's Sky; Details.
  b40-56   PICKERS    [TURN 1, INTRO 2]  side by side at 3x: both cursors march down the list; jump cut b48 to
                      the wrong file; new score climbs one stop a beat b50-53 on the riff, 9 on b54.
  b56-72   SETTINGS   [A 2]      old b56-60, one sweep b60-62 while the score spins two stops a beat, 9 on b62;
                      cut b64 to a value change; cut b68 to the save prompt with old -> new.
  b72-88   CLIMAX     [B 2]      six new menus drop in one a beat b72-77; dim b80; families at 9: 0 b80,
                      tally to 13 from b81, to 26 from b84.
  b88      PAYOFF     [TURN 2]   27 / 27 slam with flash and Tally End on the cadence's downbeat; banner;
                      menus relight one by one; Giant Ring iris b91 opens the delivered hub on the high G (b92).
  b95-104  END CARD   [INTRO 3]  lines enter on the riff's steps; the G-major stab on b104 is the last sound;
                      fade to black. 2592 frames, 43.20 s.

Commands (Python with numpy + Pillow; OPENGGF_WORKTREE = a tree with tools/media/promo_kit.py):
  edit.py check            edit-list, pacing and stinger-balance warnings
  edit.py sheet [step]     contact sheet into build/
  edit.py frames N...      single frames into build/
  edit.py preview A B      H.264 preview of output frames A..B
  edit.py master           FFV1 + PCM master with chapters; writes chapters.txt, edl.csv, cues.json
  edit.py remix            audio-only revision: re-mix into the existing master (video copied)
  edit.py loudness         per-chapter integrated loudness of the mix (no video)
  edit.py lists            rewrite chapters.txt, edl.csv, cues.json (and build/chapters.ffmeta) only
  edit.py mp4              distribution MP4 from the master (true-peak-checked AAC, chapters)
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
REV = HERE.parents[1]                              # revisions/super-sonic-cut
ROOT = HERE.parents[3]                             # the original production root (clips, sfx, ui tones)
KIT = Path(os.environ.get('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-70d5dcc5')) / 'tools/media'
sys.path.insert(0, str(KIT))
import promo_kit  # noqa: E402
from promo_kit import (Edit, Custom, Fn, Flash, Fade, paste, text, rounded, clamp, ease_out, smooth, back,  # noqa: E402
                       write_wav)

W, H, FPS = 1920, 1080, 60
BEAT = 24.576                                      # frames a beat: 24 SMPS ticks at tempo $FA (250/256 a frame)
BPM = 3600 / BEAT                                  # 146.484
CLIPS = ROOT / 'clips'
SFX = ROOT / 'audio/sfx'
UI = ROOT / 'audio/ui'
MUSIC = REV / 'audio/music/s2-music-93-paced.wav'
BUILD = REV / 'build'
FINAL = REV / 'final'
FILM = FINAL / 'menu-evolution-super-sonic-cut.mp4'
MASTER = FINAL / 'menu-evolution-super-sonic-cut-master.mkv'
BADGE = KIT.parents[1] / 'src/main/resources/icon/openggf-256.png'

NAVY = (5, 16, 53)
NAVY2 = (10, 36, 92)
DEEP = (2, 8, 28)
GOLD = (255, 214, 76)
PALE = (232, 237, 255)
LIGHT = (184, 196, 229)
WHITE = (255, 255, 255)
INK = (6, 12, 40)

S = 4                                   # pane scale: 320x224 -> 1280x896
PANE_C = (320, 92)                      # centred pane
PANE_L = (56, 92)                       # montage pane, counter column to its right
COL_X = 1392                            # counter column left edge
TWO_Y = 316                             # side-by-side panes (3x, 960x672 each) top edge
F = lambda b: int(round(BEAT * b))      # bed beat -> output frame
END_HIT = F(104)                        # the G-major stab that ends the bed
TOTAL = END_HIT + 36                    # 2592 frames
BED_CUT = 2566                          # inside the eighth-note rest after the stab (measured)
UI_GAIN = float(os.environ.get('UI_GAIN', '0.7'))   # HostUiSfx tones; r3b used 1.1 over a denser edit

# --------------------------------------------------------------------------------- the numbers
# Every value and its source in docs/architecture/audits/2026-10-27-menu-design-review.md (d823ce643),
# unchanged from the original film. Dates are the commits' UTC dates. All are subjective judgments.
SCORES = {
    'libraries': [('3.5', 'ROUND 0', '27 OCT', 'Round 0 baseline, class D Libraries'),
                  ('6.5', 'ROUND 1', '27 OCT', 'Round 1 scores, class D (f496d6e36)'),
                  ('7.5', 'ROUND 3', '27 OCT', 'Round 3 scores, class D (de250fca8)'),
                  ('8', 'TARGET 8', '28 OCT', 'All-menus target 8 final matrix, D7-D9 Mod manager'),
                  ('8.5', 'STRUCTURAL', '28 OCT', 'Structural pass matrix, D7-D9 (d8d947336)'),
                  ('9', 'FINISH', '28 OCT', 'Finish pass matrix, D7-D9 (a513dd5fd)')],
    'settings': [('5.5', 'ROUND 0', '27 OCT', 'Round 0 baseline, class B Settings (round 1 unchanged)'),
                 ('7', 'ROUND 2', '27 OCT', 'Round 2 scores, class B (191701bfe)'),
                 ('7.5', 'ROUND 4', '27 OCT', 'Round 4 scores, class B (4bed3bc06)'),
                 ('8', 'TARGET 8', '28 OCT', 'All-menus target 8 final matrix, B1 Settings tabs'),
                 ('8.5', 'STRUCTURAL', '28 OCT', 'Structural pass matrix, B1 Settings tabs'),
                 ('9', 'FINISH', '28 OCT', 'Finish pass matrix, B1 Settings Display')],
    'pickers': [('4', 'ROUND 0', '27 OCT', 'Round 0 baseline, class C Pickers/editors'),
                ('6.5', 'ROUND 1', '27 OCT', 'Round 1 scores, class C'),
                ('7.5', 'ROUND 3', '27 OCT', 'Round 3 scores, class C'),
                ('8', 'TARGET 8', '28 OCT', 'All-menus target 8 final matrix, C1 Path browser'),
                ('8.5', 'STRUCTURAL', '28 OCT', 'Structural pass matrix, C1 Path browser'),
                ('9', 'FINISH', '28 OCT', 'Finish pass matrix, C1 Path browser')],
    'families_at_9': [(0, 'TOWARD 9', '28 OCT', 'Hill climb toward 9: "No family reached 9 overall"'),
                      (13, 'STRUCTURAL', '28 OCT', 'Structural pass: "Thirteen families reach 9 overall"'),
                      (26, 'FINISH', '28 OCT', 'Finish pass: "Twenty-six families reach 9"'),
                      (27, 'LEAD ACCEPTANCE', '29 OCT', 'Lead acceptance: Time Attack accepted at 9 overall '
                       '(d823ce643); individual criteria keep their 8.5 entries')],
}

# score tick frames (one per recorded stop, the first is the starting value)
TICKS = {
    'libraries': [F(24), F(28), F(29), F(30), F(31), F(32)],
    'pickers': [F(40), F(50), F(51), F(52), F(53), F(54)],
    'settings': [F(56), F(60), F(60.5), F(61), F(61.5), F(62)],
}
COUNT = [F(80), F(81), F(84), F(88)]    # families at 9: 0 shown, tally to 13, tally to 26, slam 27
TALLY_STEP = 4                          # frames between counted families (and blips)

# take in-points: (era(s), take, output start, output end, take frame at output start)
SRC = {
    'cold':   ('pre+new', 'shader', 0, F(16), 106),      # picker opens at take 131 = b1; title shows it on
    'v05':    ('v05', 'v05-title', F(16), F(20), 50),
    'prehub': ('pre', 'hub', F(20), F(24), 0),
    'lib1':   ('pre+new', 'mods', F(24), F(32), 52),     # ENTER into the manager on b24
    'lib2':   ('new', 'mods', F(32), F(40), 421),        # confirm trust (take 446) on b33
    'pick1':  ('pre+new', 'locate', F(40), F(48), 20),   # ENTER into the browser, six DOWNs
    'pick2':  ('pre+new', 'locate', F(48), F(56), 320),  # the wrong file (take 341) on b49
    'set1':   ('pre+new', 'settings', F(56), F(64), 120),
    'set2':   ('new', 'settings', F(64), F(68), 690),    # value change (take 709)
    'set3':   ('new', 'settings', F(68), F(72), 795),    # save prompt (take 814)
    'hero':   ('new', 'hub', F(91), TOTAL, 0),
}
WALL = [  # take, take frame at b72 (each runs to the iris without passing its last frame)
    ('hub', 160), ('settings', 367), ('mods', 131), ('locate', 0), ('shader', 40), ('dialogs', 26)]

# ------------------------------------------------------------------------------- clip access


class Clip:
    def __init__(self, era, take):
        self.era, self.take = era, take
        self.dir = CLIPS / era / take
        self.n = len(list((self.dir / 'frames').glob('*.png')))
        if not self.n:
            raise FileNotFoundError(self.dir)

    @lru_cache(maxsize=48)
    def native(self, i):
        i = int(clamp(i, 0, self.n - 1))
        return np.asarray(Image.open(self.dir / 'frames' / f'{i:05d}.png').convert('RGB'), np.float32)

    def cues(self):
        out = []
        for row in csv.DictReader((self.dir / 'events.csv').open()):
            if row['kind'] == 'cue':
                out.append((int(row['frame']), row['detail']))
        return out


@lru_cache(maxsize=None)
def clip(era, take):
    return Clip(era, take)


def src(key, f):
    """Take frame shown at output frame f for a source interval."""
    _, _, f0, _, in_ = SRC[key]
    return in_ + f - f0


def up(a, s):
    return np.repeat(np.repeat(a, s, axis=0), s, axis=1)


# ---------------------------------------------------------------------------------- the stage


@lru_cache(maxsize=None)
def _stage_base():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    g = (ys / H)[..., None]
    base = np.array(DEEP, np.float32) * g + np.array(NAVY, np.float32) * (1 - g)
    return base, xs + 0.42 * ys


def stage(f):
    """Deep navy with diagonal bands leaning like title-card speed lines (a little faster than r3)."""
    base, diag = _stage_base()
    band = ((diag - f * 1.6) // 90) % 2
    c = base.copy()
    c += (band[..., None] * np.array((4, 8, 18), np.float32))
    return c


def pane(c, img, x, y, s=S, border=6, colour=GOLD):
    big = up(img, s)
    h, w = big.shape[:2]
    if border:
        c[y - border:y + h + border, x - border:x + w + border] = np.array(colour, np.float32)
    c[y:y + h, x:x + w] = big


def compare_native(old, new, d):
    """d native columns of the new picture from the left, the rest still the old one."""
    d = int(clamp(round(d), 0, 320))
    out = old.copy()
    out[:, :d] = new[:, :d]
    return out


def divider(c, x, y, d, s=S):
    if 0 < d < 320:
        px = x + int(round(d)) * s
        c[y - 10:y + 224 * s + 10, px - 4:px + 4] = np.array(GOLD, np.float32)
        c[y - 10:y + 224 * s + 10, px - 1:px + 1] = np.array(WHITE, np.float32)


def over(dst, src_, x, y, alpha=1.0):
    """Source-over compositing of a float RGBA array onto a float RGBA array (labels and plates)."""
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
    rgb = (s[..., :3] * sa + d[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6)
    d[..., :3] = rgb
    d[..., 3:4] = oa * 255


@lru_cache(maxsize=None)
def pill(label, size=40, fg=INK, bg=GOLD, role='title_it'):
    t = text(label, role, size, fg)
    p = rounded(t.shape[1] + 36, t.shape[0] + 6, 12, bg).copy()
    over(p, t, 18, 3)
    return p


def era_tabs(c, x, y, d, before='BEFORE · 27 OCT', now='NOW · 29 OCT'):
    """Labels riding the divider in the top margin: NOW behind it (left), BEFORE ahead (right)."""
    pb, pn = pill(before, bg=LIGHT), pill(now)
    top = y - 6 - 12 - pb.shape[0]
    if d <= 0:
        paste(c, pb, x, top)
    elif d >= 320:
        paste(c, pn, x, top)
    else:
        px = x + int(round(d)) * S
        paste(c, pn, px - 14 - pn.shape[1], top)
        paste(c, pb, px + 14, top)


# ---------------------------------------------------------------------------- score graphics


def roll(c, s_old, s_new, x, y, t, size=300, colour=GOLD, dur=14, alpha=1.0):
    """A slot-machine roll from the old value to the new one (only recorded values)."""
    u = clamp(t / dur)
    img_new = text(s_new, 'title', size, colour, stroke=10, sfill=INK, shadow=12)
    if u >= 1 or s_old is None:
        paste(c, img_new, x, y, alpha)
        return img_new.shape
    img_old = text(s_old, 'title', size, colour, stroke=10, sfill=INK, shadow=12)
    h = img_new.shape[0]
    e = ease_out(u)
    slot = np.zeros((h, max(img_new.shape[1], img_old.shape[1]), 4), np.float32)
    # both values fully opaque, clipped by the slot window: the old one leaves upward as the new one
    # arrives from below with a small overshoot (no cross-faded double image)
    over(slot, img_old, 0, -int(e * h))
    over(slot, img_new, 0, int((1 - back(u, 1.3)) * h))
    paste(c, slot, x, y, alpha)
    return img_new.shape


def pips(c, x, y, score, flash=0.0):
    for k in range(10):
        fill = clamp(score - k)
        bx = x + k * 47
        c[y:y + 26, bx:bx + 40] = np.array(NAVY2, np.float32)
        if fill > 0:
            w = int(40 * fill)
            col = np.array(GOLD, np.float32) * (1 - flash) + np.array(WHITE, np.float32) * flash
            c[y:y + 26, bx:bx + w] = col


def chart(c, x, y, values, upto, u):
    """A step chart of the recorded stops reached so far."""
    w, h = 480, 150
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for g in (2, 4, 6, 8, 10):
        gy = h - 6 - (h - 12) * g / 10
        d.line((0, gy, w, gy), fill=(90, 116, 190, 140), width=2)
    pts = [(10 + i * (w - 20) / (len(values) - 1), h - 6 - (h - 12) * float(v) / 10) for i, v in enumerate(values)]
    for i in range(1, upto + 1):
        a, b = pts[i - 1], pts[i]
        k = u if i == upto else 1.0
        mid = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        d.line((a, (mid[0], a[1])), fill=GOLD + (255,), width=7)
        d.line(((mid[0], a[1]), mid), fill=GOLD + (255,), width=7)
    for i in range(0, upto + 1):
        px, py = pts[i]
        r = 11 if i == upto else 8
        d.ellipse((px - r, py - r, px + r, py + r), fill=(WHITE if i == upto else GOLD) + (255,))
    paste(c, np.asarray(im, np.float32), x, y)


def stop_at(key, f):
    """(index of the recorded stop shown at f, frames since it arrived)."""
    frames = TICKS[key]
    k = max(i for i, t in enumerate(frames) if f >= t) if f >= frames[0] else 0
    return k, f - frames[k]


def counter_column(c, f, key, family, detail, roll_dur=14):
    stops = SCORES[key]
    k, t = stop_at(key, f)
    x = COL_X
    paste(c, text('DESIGN REVIEW', 'sub', 34, LIGHT, tracking=6), x, 96)
    paste(c, text(family, 'title', 92, WHITE, stroke=5, sfill=INK, shadow=6), x, 136)
    paste(c, text(detail, 'sub', 44, GOLD, stroke=3, sfill=INK, shadow=4), x, 250)
    prev = stops[k - 1][0] if k > 0 else None
    shape = roll(c, prev, stops[k][0], x - 6, 318, t, dur=roll_dur)
    ten = text('/10', 'title', 64, LIGHT, stroke=4, sfill=INK, shadow=5)
    paste(c, ten, min(x + shape[1] - 10, W - 24 - ten.shape[1]), 318 + shape[0] - ten.shape[0] - 36)
    flash = (1 - clamp(t / 18)) if k > 0 else 0.0
    pips(c, x, 712, float(stops[k][0]), flash)
    tag = pill(f'{stops[k][1]} · {stops[k][2]}', 40)
    paste(c, tag, x, 768, clamp(t / 6) if k > 0 else 1.0)
    chart(c, x - 6, 846, [s[0] for s in stops], k, clamp(t / 10))


def divider_at(f, key, ease=10):
    """Divider column (native px): 0 before the first climb tick; each recorded stop moves it to the
    share of the climb it represents, easing from its tick."""
    stops = [float(s[0]) for s in SCORES[key]]
    pos = [320 * (s - stops[0]) / (stops[-1] - stops[0]) for s in stops]
    frames = TICKS[key]
    if f < frames[1]:
        return 0.0
    k = max(i for i, t in enumerate(frames) if f >= t)
    u = ease_out(clamp((f - frames[k]) / ease))
    return pos[k - 1] + (pos[k] - pos[k - 1]) * u


# --------------------------------------------------------------------------------- shot builders


def cold_open(f, shot, edit):
    c = stage(f)
    i = src('cold', f)
    old, new = clip('pre', 'shader'), clip('new', 'shader')
    d = round(320 * ease_out(clamp((f - F(4)) / (F(6) - F(4))))) if f >= F(4) else 0
    x, y = PANE_C
    pane(c, compare_native(old.native(i), new.native(i), d), x, y)
    divider(c, x, y, d)
    if f < F(8) - 4:
        era_tabs(c, x, y, d)
    return c


def title_bg(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('new', 'shader').native(src('cold', f)), x, y)
    c *= 1 - 0.62 * smooth(clamp((f - F(8)) / 20))
    return c


def glimpse_v05(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('v05', 'v05-title').native(src('v05', f)), x, y)
    return c


def glimpse_pre(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('pre', 'hub').native(src('prehub', f)), x, y)
    return c


def divider_rep(key, family, detail, part, ease=10, roll_dur=14, note=False):
    """Montage pane with the counter column. The part's take frames come from SRC; parts after the climb
    show the new era whole."""
    era, take = SRC[part][0], SRC[part][1]

    def fn(f, shot, edit):
        c = stage(f)
        i = src(part, f)
        x, y = PANE_L
        new = clip('new', take).native(i)
        if era == 'new':
            d = 320
            img = new
        else:
            d = divider_at(f, key, ease)
            img = compare_native(clip('pre', take).native(i), new, d)
        pane(c, img, x, y)
        divider(c, x, y, d)
        era_tabs(c, x, y, d)
        counter_column(c, f, key, family, detail, roll_dur)
        if note:
            line = text("Scores out of 10: OpenGGF's own design review, 27–29 Oct 2026. Judgments, not measurements.",
                        'body', 30, LIGHT, stroke=2, sfill=INK, shadow=3)
            paste(c, line, x, 1012, clamp((f - F(24) - 8) / 10))
        return c
    return fn


def two_up(part):
    """Old and new side by side at 3x, each with its own score; the new one climbs."""
    take = SRC[part][1]
    key = 'pickers'

    def fn(f, shot, edit):
        c = stage(f)
        i = src(part, f)
        old, new = up(clip('pre', take).native(i), 3), up(clip('new', take).native(i), 3)
        c[TWO_Y:TWO_Y + 672, 0:960] = old
        c[TWO_Y:TWO_Y + 672, 960:1920] = new
        c[TWO_Y - 6:TWO_Y, :] = np.array(GOLD, np.float32)
        c[TWO_Y + 672:TWO_Y + 678, :] = np.array(GOLD, np.float32)
        c[TWO_Y - 6:TWO_Y + 678, 957:963] = np.array(GOLD, np.float32)
        # centre heading
        kick = text('DESIGN REVIEW', 'sub', 34, LIGHT, tracking=6)
        paste(c, kick, W / 2 - kick.shape[1] / 2, 40)
        fam = text('PICKERS', 'title', 104, WHITE, stroke=5, sfill=INK, shadow=6)
        paste(c, fam, W / 2 - fam.shape[1] / 2, 74)
        det = text('Locate ROM', 'sub', 46, GOLD, stroke=3, sfill=INK, shadow=4)
        paste(c, det, W / 2 - det.shape[1] / 2, 196)
        # era pills sit on the panes' top edge
        pb, pn = pill('BEFORE · 27 OCT', bg=LIGHT), pill('NOW · 29 OCT')
        paste(c, pb, 24, TWO_Y - 6 - 12 - pb.shape[0])
        paste(c, pn, 1920 - 24 - pn.shape[1], TWO_Y - 6 - 12 - pn.shape[0])
        # old score, fixed at round 0
        ten = text('/10', 'title', 52, LIGHT, stroke=4, sfill=INK, shadow=5)
        o = text(SCORES[key][0][0], 'title', 200, LIGHT, stroke=8, sfill=INK, shadow=10)
        paste(c, o, 40, 34)
        paste(c, ten, 40 + o.shape[1] - 30, 34 + o.shape[0] - ten.shape[0] - 26)
        # new score climbs on its ticks
        k, t = stop_at(key, f)
        stops = SCORES[key]
        prev = stops[k - 1][0] if k > 0 else None
        wk = text(stops[k][0], 'title', 200, GOLD, stroke=10, sfill=INK, shadow=12).shape[1]
        nx = 1896 - ten.shape[1] - wk + 30           # right-aligned so '/10' stays on screen
        shape = roll(c, prev, stops[k][0], nx, 34, t, size=200, dur=12)
        paste(c, ten, nx + shape[1] - 30, 34 + shape[0] - ten.shape[0] - 26)
        if k > 0:
            tag = pill(f'{stops[k][1]} · {stops[k][2]}', 36)
            paste(c, tag, 1920 - 24 - pn.shape[1] - 18 - tag.shape[1], TWO_Y - 6 - 12 - tag.shape[0],
                  clamp(t / 6))
        return c
    return fn


def wall(f, shot, edit):
    c = stage(f)
    for k, (take, s0) in enumerate(WALL):
        t0 = F(72 + k)
        if f < t0:
            continue
        x, y = (k % 3) * 640, 92 + (k // 3) * 448
        drop = int(round((1 - ease_out(clamp((f - t0) / 12))) * -500))
        img = up(clip('new', take).native(s0 + f - F(72)), 2)
        yy = y + drop
        top = max(0, 92 - yy) if k < 3 else 0
        c[yy + top:yy + 448, x:x + 640] = img[top:]
        # after the slam every new menu lights up again, one cell every 6 frames
        light = smooth(clamp((f - F(88) - 12 - 6 * k) / 10))
        dim = smooth(clamp((f - F(80)) / 16)) * 0.76 * (1 - light)
        c[max(92, yy):yy + 448, x:x + 640] *= 1 - dim
    return c


def hero(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('new', 'hub').native(src('hero', f)), x, y)
    u = smooth(clamp((f - F(95)) / 24))
    if u > 0:
        blurred = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6 * u)),
                             np.float32)
        c = blurred * (1 - 0.7 * u)
    return c


# ------------------------------------------------------------------------------------- overlays


def families_counter(c, f, o, edit=None):
    """Families at 9 per pass, counted up one family at a time like a results tally."""
    stops = SCORES['families_at_9']
    if f < COUNT[0]:
        return
    k = max(i for i, t in enumerate(COUNT) if f >= t)
    shown = stops[k][0]
    if 0 < k < 3:
        prev = stops[k - 1][0]
        shown = prev + min(shown - prev, (f - COUNT[k]) // TALLY_STEP + 1)
    a = clamp((f - COUNT[0]) / 10)
    t = f - COUNT[3]
    payoff = t >= 0
    leave = smooth(clamp((t - 20) / 12)) if payoff else 0.0
    big = text(f'{shown}', 'title', 400, WHITE if payoff else GOLD, stroke=12, sfill=INK, shadow=14)
    of = text('/ 27', 'title', 150, LIGHT, stroke=6, sfill=INK, shadow=8)
    lab = text('MENU FAMILIES AT 9', 'title_it', 74, WHITE, stroke=5, sfill=INK, shadow=6, tracking=2)
    tag = pill(f'{stops[k][1]} · {stops[k][2]}', 44)
    block = np.zeros((760, 1000, 4), np.float32)
    bx = 500 - of.shape[1] / 2 - 10
    over(block, big, bx - big.shape[1] / 2, 400 - big.shape[0] + 50)
    over(block, of, bx + big.shape[1] / 2 + 20, 400 - of.shape[0] + 10)
    over(block, lab, 500 - lab.shape[1] / 2, 470)
    over(block, tag, 500 - tag.shape[1] / 2, 590)
    s = 1.0
    if payoff:
        s = 1 + 0.5 * (1 - ease_out(clamp(t / 12))) - 0.2 * leave
    img = promo_kit.scaled(block, s) if s != 1.0 else block
    shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0 if payoff else 0.0
    paste(c, img, W / 2 - img.shape[1] / 2 + shake, 600 - img.shape[0] / 2, a * (1 - leave))


def banner(c, f, o, edit=None):
    t = f - o.f0
    img = text('27 / 27 MENU FAMILIES AT 9', 'title_it', 64, WHITE, stroke=5, sfill=INK, shadow=6, tracking=2)
    u = ease_out(clamp(t / 12))
    # opaque rows 11-87 of the image: y -4 keeps it inside the top margin, clear of the pane border at 86
    paste(c, img, W / 2 - img.shape[1] / 2, -4 - (1 - u) * 90, u * clamp((o.f1 - f) / 8))


def title_words(c, f, o, edit=None):
    for word, b, y in (('ROAD', 8, 250), ('TO', 9, 470)):
        t = f - F(b)
        if t < 0:
            continue
        img = text(word, 'title', 170, WHITE, stroke=9, sfill=INK, shadow=10)
        img = promo_kit.scaled(img, 0.4 + 0.6 * back(clamp(t / 10), 2.2))
        paste(c, img, 630 - img.shape[1] / 2, y + 100 - img.shape[0] / 2, clamp(t / 3))
    t = f - F(10)
    if t >= 0:
        nine = text('9', 'title', 640, GOLD, stroke=14, sfill=INK, shadow=18)
        nine = promo_kit.scaled(nine, 1 + 0.35 * (1 - ease_out(clamp(t / 12))))
        paste(c, nine, 1300 - nine.shape[1] / 2, 520 - nine.shape[0] / 2, clamp(t / 3))
    t = f - F(12)
    if t >= 0:
        sub = text("OpenGGF's menus, round by round", 'sub', 60, PALE, stroke=4, sfill=INK, shadow=5)
        paste(c, sub, W / 2 - sub.shape[1] / 2, 880 + (1 - ease_out(clamp(t / 14))) * 60, clamp(t / 10))


def era_label(c, f, o, edit=None):
    """Top-margin era tag over the glimpse, rolling 0.5 -> 0.6 -> 0.7 at the push."""
    x = PANE_C[0]
    if f < F(20):
        ver, line = '0.5', 'OPENGGF 0.5 · APRIL 2026 RELEASE'
    else:
        ver = ['0.5', '0.6', '0.7'][int(clamp((f - F(20)) / 8, 0, 2))]
        line = 'OPENGGF 0.7 IN DEVELOPMENT · 27 OCT 2026 · BEFORE THE REDESIGN'
    a = clamp((f - F(16) - 4) / 8) * clamp((F(24) - f) / 6)
    v = pill(ver, 46)
    paste(c, v, x, 24, a)
    paste(c, text(line, 'title_it', 44, PALE, stroke=3, sfill=INK, shadow=4), x + v.shape[1] + 16, 22, a)


def promise(c, f, o, edit=None):
    t = f - o.f0
    line = text('SAME GAME. NEW MENUS.', 'title_it', 64, WHITE, stroke=5, sfill=INK, shadow=6)
    paste(c, line, W / 2 - line.shape[1] / 2, 1000 + (1 - ease_out(clamp(t / 12))) * 40,
          clamp(t / 8) * clamp((o.f1 - f) / 6))


def end_card(c, f, o, edit=None):
    badge = np.asarray(Image.open(BADGE).convert('RGBA'), np.float32)
    lines = [  # image, y, entry beat (the riff steps a semitone every half bar)
        (badge, 120, 95),
        (text('ROAD TO 9', 'title', 130, GOLD, stroke=8, sfill=INK, shadow=10), 392, 96),
        (text('Every OpenGGF menu, rebuilt round by round.', 'sub', 56, WHITE, stroke=4, sfill=INK, shadow=5), 546, 97),
        (text('github.com/OpenGGF/OpenGGF', 'title_it', 78, WHITE, stroke=5, sfill=INK, shadow=6), 640, 98),
        (text('In development for OpenGGF 0.7', 'body', 42, LIGHT, stroke=3, sfill=INK, shadow=4), 756, 99),
        (text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body', 36, PALE,
              stroke=2, sfill=INK, shadow=3), 900, 100),
        (text("Scores: OpenGGF's own menu design review, 27–29 Oct 2026. Subjective judgments, "
              'not usability measurements.', 'body', 30, LIGHT, stroke=2, sfill=INK, shadow=3), 962, 100.5),
    ]
    for img, y, b in lines:
        t = f - F(b)
        if t >= 0:
            paste(c, img, W / 2 - img.shape[1] / 2, y + (1 - ease_out(clamp(t / 12))) * 30, clamp(t / 8))


# ----------------------------------------------------------------------------------- the edit

CHAPTERS = []   # (start frame, end frame, title)
EDL = []        # (start frame, end frame, chapter, layout, sources)
CUES = []       # (output frame, era, take, take frame, cue)
E = None


def sfx(name):
    return SFX / f's2-sfx-{name}-paced.wav'


def map_cues(part, visible, until=None):
    """UI cues of a source interval at their output frames, from the era on screen (visible(f) -> era,
    or 'both' for side by side: one tone per cue, the eras' timelines and tones being identical)."""
    era, take, f0, f1, in_ = SRC[part]
    seen = set()
    for e in ('pre', 'new'):
        if e not in era:
            continue
        for fo, cue in clip(e, take).cues():
            out = f0 + fo - in_
            if not f0 <= out < (f1 if until is None else min(f1, until)):
                continue
            v = visible(out)
            if v == 'both':
                if (out, cue) in seen:
                    continue
                seen.add((out, cue))
            elif v != e:
                continue
            CUES.append((out, e, take, fo, cue))


def edl(part, chapter, layout, f0=None, f1=None, era=None):
    era_, take, s0, s1, in_ = SRC[part]
    era = era or era_
    f0 = s0 if f0 is None else f0
    f1 = s1 if f1 is None else f1
    EDL.append((f0, f1, chapter, layout, f'{era}/{take} take frames {in_ + f0 - s0}-{in_ + f1 - s0 - 1}'))


def build(e):
    global CHAPTERS, EDL, CUES
    CHAPTERS, EDL, CUES = [], [], []
    X = e.X
    # A. cold open: the in-game picker, before then now, on the bed's rising intro
    ch = 'Cold open: the in-game shader picker, before and now'
    e.S(Custom(0, F(8), cold_open))
    e.O(Fn(F(5), F(8), promise))
    X(F(4) - 4, sfx('ab'), 1.2)
    CHAPTERS.append((0, F(8), ch))
    edl('cold', ch, 'centred pane 4x, divider sweep b4-6', 0, F(8))
    # B. title drop on the melody's entrance
    ch = 'Title: Road to 9'
    e.S(Custom(F(8), F(16), title_bg))
    e.O(Flash(F(8), 14, 0.8))
    e.O(Fn(F(8), F(16), title_words))
    X(F(8), sfx('bc'), 1.0)
    X(F(10), sfx('c5'), 0.7)
    CHAPTERS.append((F(8), F(16), ch))
    edl('cold', ch, 'centred pane 4x, dimmed under the title', F(8), F(16), era='new')
    # C. glimpse: 0.5, then the pre-redesign 0.7 hub
    ch = 'Where it started: OpenGGF 0.5, then the 0.7 hub before the redesign'
    e.S(Custom(F(16), F(20), glimpse_v05, trans='wipe', tdur=14))
    e.S(Custom(F(20), F(24), glimpse_pre, trans='push', tdur=14, tdir='left'))
    e.O(Fn(F(16), F(24), era_label))
    X(F(16) - 4, sfx('ab'), 1.2)
    map_cues('prehub', lambda f: 'pre')
    CHAPTERS.append((F(16), F(24), ch))
    edl('v05', ch, 'centred pane 4x (0.5 silent)')
    edl('prehub', ch, 'centred pane 4x')
    # D. Libraries: one recorded stop a beat on the stabs
    ch = 'Libraries: Mod manager, 3.5 to 9'
    e.S(Custom(F(24), F(32), divider_rep('libraries', 'LIBRARIES', 'Mod manager', 'lib1', note=True),
               trans='wipe', tdur=14))
    e.S(Custom(F(32), F(40), divider_rep('libraries', 'LIBRARIES', 'Mod manager', 'lib2', note=True)))
    X(F(24) - 4, sfx('ab'), 1.2)
    for t in TICKS['libraries'][1:-1]:
        X(t, sfx('cd'), 1.0)
    X(TICKS['libraries'][-1], sfx('c5'), 0.7)
    map_cues('lib1', lambda f: 'new' if divider_at(f, 'libraries') >= 160 else 'pre')
    map_cues('lib2', lambda f: 'new')
    CHAPTERS.append((F(24), F(40), ch))
    edl('lib1', ch, 'montage pane 4x + counter column; divider steps b28-32')
    edl('lib2', ch, 'montage pane 4x + counter column; now (jump cut)')
    # E. Pickers: side by side, the new score climbing on the riff
    ch = 'Pickers: Locate ROM, 4 to 9, side by side'
    e.S(Custom(F(40), F(48), two_up('pick1'), trans='wipe', tdur=14))
    e.S(Custom(F(48), F(56), two_up('pick2')))
    X(F(40) - 4, sfx('ab'), 1.2)
    X(TICKS['pickers'][-1], sfx('c5'), 0.7)
    map_cues('pick1', lambda f: 'both')
    map_cues('pick2', lambda f: 'both')
    CHAPTERS.append((F(40), F(56), ch))
    edl('pick1', ch, 'side by side 3x (before | now)')
    edl('pick2', ch, 'side by side 3x (before | now), jump cut')
    # F. Settings: one sweep while the score spins, then the new flow
    ch = 'Settings: Display tab, 5.5 to 9'
    e.S(Custom(F(56), F(64), divider_rep('settings', 'SETTINGS', 'Display tab', 'set1', ease=12, roll_dur=10),
               trans='wipe', tdur=14))
    e.S(Custom(F(64), F(68), divider_rep('settings', 'SETTINGS', 'Display tab', 'set2')))
    e.S(Custom(F(68), F(72), divider_rep('settings', 'SETTINGS', 'Display tab', 'set3')))
    X(F(56) - 4, sfx('ab'), 1.2)
    for t in TICKS['settings'][1:-1]:
        X(t, sfx('cd'), 1.0)
    X(TICKS['settings'][-1], sfx('c5'), 0.7)
    map_cues('set1', lambda f: 'new' if divider_at(f, 'settings', 12) >= 160 else 'pre')
    map_cues('set2', lambda f: 'new')
    map_cues('set3', lambda f: 'new')
    CHAPTERS.append((F(56), F(72), ch))
    edl('set1', ch, 'montage pane 4x + counter column; sweep b60-62')
    edl('set2', ch, 'montage pane 4x; now (jump cut)')
    edl('set3', ch, 'montage pane 4x; now (jump cut)')
    # G. climax: the wall of new menus, the count of families at 9, the slam
    ch = 'Twenty-seven of twenty-seven menu families at 9'
    e.S(Custom(F(72), F(91), wall, trans='wipe', tdur=14))
    X(F(72) - 4, sfx('ab'), 1.2)
    e.O(Fn(F(80), F(91), families_counter))
    vals = [s[0] for s in SCORES['families_at_9']]
    for k in (1, 2):
        for j in range(vals[k] - vals[k - 1]):
            X(COUNT[k] + j * TALLY_STEP, sfx('cd'), 0.8)
    X(COUNT[3], sfx('c5'), 0.9)
    e.O(Flash(COUNT[3], 18, 0.9))
    e.O(Fn(COUNT[3] + 12, F(95) + 8, banner))
    CHAPTERS.append((F(72), F(91), ch))
    EDL.append((F(72), F(91) + 24, ch, 'wall of six cells 2x (3x2), seen until the iris completes',
                'new/' + ', new/'.join(f'{t} take frames {s0}-{s0 + F(91) + 24 - F(72) - 1}' for t, s0 in WALL)))
    # H. the delivered hub through a Giant Ring iris; end card; the stab
    ch = 'The delivered hub, end card'
    e.S(Custom(F(91), TOTAL, hero, trans='iris', tdur=24))
    X(F(91) - 6, sfx('c3'), 0.9)
    map_cues('hero', lambda f: 'new', until=F(96))      # silent once the hub is blurred under the card
    e.O(Fn(F(95), TOTAL, end_card))
    e.O(Flash(END_HIT, 10, 0.35))
    e.O(Fade(END_HIT + 12, TOTAL + 1))
    CHAPTERS.append((F(91), TOTAL, ch))
    edl('hero', ch, 'centred pane 4x, iris in; blurred under the end card from b95')
    # sound: one bed from its first sample to the stab that ends its third loop's intro
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
    lines = [';FFMETADATA1', 'title=ROAD TO 9 (Super Sonic cut): OpenGGF menu evolution promo', 'artist=OpenGGF']
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
            srcs = '; '.join(s for a, b, ch, _, s in EDL if ch == title)
            fh.write(f'{f0 / FPS:6.2f}-{f1 / FPS:6.2f}  {title}  [{srcs}]\n')
    (HERE / 'cues.json').write_text(json.dumps(
        [dict(frame=o, era=era, take=t, take_frame=fo, cue=c) for o, era, t, fo, c in sorted(CUES)], indent=0))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    e = edit()
    if cmd == 'check':
        for w in e.check():
            print('warning:', w)
        print('pacing:', e.pacing()[0])
        print('end', e.end(), f'{e.end() / FPS:.3f}s', 'cues', len(CUES), 'sfx', len(e.sfx))
    elif cmd == 'sheet':
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        BUILD.mkdir(exist_ok=True)
        print(e.contact_sheet(BUILD / 'sheet.png', step, 0, None, workers=8))
    elif cmd == 'frames':
        BUILD.mkdir(exist_ok=True)
        for a in sys.argv[2:]:
            p = BUILD / f'frame-{int(a):05d}.png'
            Image.fromarray(e.render_frame(int(a))).save(p)
            print(p)
    elif cmd == 'preview':
        a, b = int(sys.argv[2]), int(sys.argv[3])
        out = BUILD / f'preview-{a:05d}-{b:05d}.mp4'
        BUILD.mkdir(exist_ok=True)
        frames_to(['ffmpeg', '-v', 'error', '-y', *RAW, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12',
                   '-pix_fmt', 'yuv420p', str(out)], a, b)
        print(out)
    elif cmd == 'master':
        FINAL.mkdir(exist_ok=True)
        BUILD.mkdir(exist_ok=True)
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
        # audio-only revision: the new mix into the existing master (video stream copied, chapters kept)
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
        # chapters.txt, edl.csv and cues.json only (the same files master/remix write)
        BUILD.mkdir(exist_ok=True)
        write_chapters(BUILD / 'chapters.ffmeta')
    elif cmd == 'loudness':
        # the mix only (no video): integrated loudness per chapter, for gain decisions before a remix
        audio = BUILD / 'mix-probe.wav'
        write_wav(audio, e.mix())
        for f0, f1, title in [(0, e.end(), 'whole film')] + CHAPTERS:
            print(f'{f0 / FPS:6.2f}-{f1 / FPS:6.2f}s  I {true_peak_range(audio, f0, f1)[1]:6.1f} LUFS  {title}')
        audio.unlink()
    elif cmd == 'mp4':
        finish_mp4()


def true_peak(path):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    peak = float(tail.split('Peak:')[1].split('dBFS')[0].strip())
    integ = float(tail.split('I:')[1].split('LUFS')[0].strip())
    return peak, integ


def true_peak_range(path, f0, f1):
    r = subprocess.run(['ffmpeg', '-nostats', '-ss', f'{f0 / FPS:.3f}', '-t', f'{(f1 - f0) / FPS:.3f}', '-i', str(path),
                        '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    return float(tail.split('Peak:')[1].split('dBFS')[0].strip()), float(tail.split('I:')[1].split('LUFS')[0].strip())


def finish_mp4():
    meta = BUILD / 'chapters.ffmeta'
    mix = BUILD / 'mix.wav'
    gain_db = 0.0
    for attempt in range(4):
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


if __name__ == '__main__':
    sys.modules.setdefault('promo_kit', promo_kit)
    main()
