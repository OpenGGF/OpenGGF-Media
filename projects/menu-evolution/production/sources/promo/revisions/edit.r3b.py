#!/usr/bin/env python3
"""ROAD TO 9: the OpenGGF menu evolution promo (project menu-evolution, 2026-10-29).

Brief (one line each)
  Request.   "Get opus xhigh to do a promo video of the old menu vs the new one. Could even include the
             old 0.5 menu.." then "Maybe film it like a action movie montage, with various numbers
             slowly climbing".
  Audience.  Sonic fans and OpenGGF players who have met the engine's menus in 0.5 or 0.7 builds.
  Form.      A menu showcase cut as a training montage. Every UI frame is a real per-frame render of
             that era's own production menu code, driven by scripted keys (sources/capture). Menus are
             the subject because the user asked for an old-vs-new menu film, so the promo-direction
             default of >=80% gameplay / <=15% menus is superseded here; gameplay appears only under
             the in-game shader picker, where the overlay's relation to play is the point.
  Promise.   Every engine menu, rebuilt round by round: from 0.5's three words to 27 of 27 at 9.
  Numbers.   Only real, dated values. Design-review scores (1-10, the review's own subjective
             judgments, not usability or performance measurements) from
             docs/architecture/audits/2026-10-27-menu-design-review.md at d823ce643 (see SCORES); the
             version 0.5 -> 0.7; the count of menu families at 9 per pass. Each number ticks only to a
             recorded value (no interpolated scores), on a beat, with Sonic 2's results-tally sounds.
  Selling points and proof (matched tasks; old and new run the same key timeline in sync, and a
             before/now divider sweeps across one pane as the score climbs):
             Libraries: enable a code mod (bracket strings -> switches, a structured trust page).
             Settings: turn off a switch, scroll, change a value, see the save prompt (truncated
               labels -> whole labels in groups; change list with old -> new values).
             Pickers: pick the wrong file in Locate ROM (ROM? on every row -> icons, scroll bar,
               a clear error card).
             Hub and dialogs: help, quit and setup (one consistent dialog language).
             Cold open: the in-game display shader picker over Emerald Hill (debug text printed over
               the HUD -> a framed panel).
  Eras.      0.5 = tag v0.5.20260411 (77c6364ce): game select only, silent stubs. "Before" = develop
             2f9ca84b1 (27 Oct 2026), whose menus are those scored in review round 0 (no src/main
             change from the review base 9a796ec60). "Now" = d823ce643 (29 Oct 2026, delivered).
  Hero.      The count of menu families at 9 ticking 0 -> 13 -> 26 -> 27 over a wall of the new
             menus, landing on the Got-an-Emerald jingle; a 1.5 s fragment opens nothing (the cold
             open is the first old/new transformation instead, so the climax keeps its surprise).
  Sound.     Sonic 2 Metropolis Zone (engine music 0x82) from the canonical S2 REV01 ROM through
             OpenGGF's SMPS driver (FmSfxRenderTool --paced): 137.14 BPM, exactly 105 video frames a
             bar, first beat 0.432 s. Form measured: intro build beats 0-16 (cold open), groove A 16-80,
             calmer B 80-112 (holds the dense Settings rep), A' returns at 112 (Pickers), cut at 176
             for the Got-an-Emerald jingle (0xBA), then the Sonic 2 title theme (0x96), which is the
             delivered hub's own music for the Sonic 2 card, under the end card. Stingers: Blip 0xCD
             on each score tick and Tally End 0xC5 on each 9 (the results tally), Spindash charge
             0xE0 and release 0xBC into the title, Swish 0xAB on chapter wipes. Menu navigation
             sounds are the engine's own HostUiSfx tones (identical in "before" and "now"),
             synthesised from that source at the exact cue frames each take logged. 0.5 is silent,
             as it was. Sound was checked by measurement only; nobody listened to this mix.
  Palette.   Sampled from d823ce643 menu frames: navy #051035 / #0a245c, deep #02081c, focus gold
             #ffd64c, pale #e8edff.
  Type.      Fira Sans Compressed Heavy / Condensed (OFL, system package ttf-fira-sans 4.301) with
             stroke and hard shadow: the film's voice must not look like the menus' pixel font.
  Pixels.    Captures are native 320x224 at 60 Hz, shown at integer 4x (grid/wall cells 2x),
             nearest-neighbour, never zoomed fractionally; editorial type sits in the margins, or
             over footage only while that footage is dimmed background. Divider steps are whole
             game pixels.
  End card.  Badge, one line, URL, status, the fan-made disclaimer and the score source line.

Beat sheet (b = bed beat, frame = round(25.92 + 26.25 b); seconds = 0.432 + 0.4375 b)
  b0-16    COLD OPEN   EHZ1 run; picker opens b4 (before), divider sweeps to "now" b8-10; picker closes
                       b12, run resumes; promise line b12. Proves: same game, new menus.
  b16-24   TITLE       "ROAD TO 9" pops word by word (spindash release on b16, tally ka-ching on "9").
  b24-40   PROLOGUE    0.5 game select (b24, version pill 0.5) pushes to the 0.7 pre-redesign hub (b32,
                       pill rolls 0.5 -> 0.7). Proves: three eras, accurately dated.
  b40-56   ROUND 0     2x2 of the old menus with their round-0 scores (5.5 / 4 / 3.5 / 4) popping on
                       beats; the scores are named as the review's judgments.
  b56-80   REP 1       LIBRARIES, Mod manager: 3.5 -> 6.5 -> 7.5 -> 8 -> 8.5 -> 9 (ticks b65-72).
  b80-112  REP 2       SETTINGS: 5.5 -> 7 -> 7.5 -> 8 -> 8.5 -> 9 (ticks b89-96); calm B section.
  b112-136 REP 3       PICKERS, Locate ROM: 4 -> 6.5 -> 7.5 -> 8 -> 8.5 -> 9 (ticks b121-128).
  b136-160 REP 4       HUB & DIALOGS: 6.5 -> 7 -> 7.5 -> 8 -> 8.5 -> 9 (ticks b145-152).
  b160-176 CLIMAX      wall of six new menus pops b160-165; dims b168; families at 9: 0 -> 13 -> 26 -> 27.
  b176     PAYOFF      flash, Got an Emerald, "27 / 27".
  +2.9 s   HERO        the delivered hub, its own Sonic 2 title theme; end card; fade.

Commands (run with a Python that has numpy and Pillow; see README.md):
  edit.py prep             synthesise the HostUiSfx tones into audio/ui/
  edit.py check            edit-list, pacing and stinger-balance warnings
  edit.py sheet [step]     contact sheet into build/
  edit.py frames N...      single frames into build/
  edit.py preview A B      lossless-ish H.264 preview of output frames A..B (moving review)
  edit.py master           FFV1 + PCM master with chapters, chapters.txt, edl.csv
  edit.py remix            audio-only revision: re-mix into the existing master (video copied)
  edit.py mp4              distribution MP4 from the master (true-peak-checked AAC, chapters)
"""
import csv
import json
import math
import os
import subprocess
import sys
import wave
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
KIT = Path(os.environ.get('OPENGGF_WORKTREE', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-3a990895')) / 'tools/media'
sys.path.insert(0, str(KIT))
import promo_kit  # noqa: E402
from promo_kit import (Edit, Custom, Fn, Flash, Fade, paste, text, rounded, clamp, ease_out, smooth, back,  # noqa: E402
                       wipe, push, read_wav, write_wav, SR)

W, H, FPS = 1920, 1080, 60
BPM, FIRST = 3600 / 26.25, 0.432          # 105 frames a bar exactly; measured 137.12 BPM, first beat 0.432 s
CLIPS = ROOT / 'clips'
AUDIO = ROOT / 'audio'
BUILD = ROOT / 'build'
FINAL = ROOT / 'final'
BADGE = KIT.parents[1] / 'src/main/resources/icon/openggf-256.png'

NAVY = (5, 16, 53)
NAVY2 = (10, 36, 92)
DEEP = (2, 8, 28)
GOLD = (255, 214, 76)
PALE = (232, 237, 255)
LIGHT = (184, 196, 229)
WHITE = (255, 255, 255)
INK = (6, 12, 40)
AMBER = (255, 170, 40)

S = 4                                   # pane scale: 320x224 -> 1280x896
PANE_C = (320, 92)                      # centred pane
PANE_L = (56, 92)                       # montage pane, counter column to its right
COL_X = 1392                            # counter column left edge
F = lambda b: int(round(25.92 + 26.25 * b))   # bed beat -> output frame
fr = lambda b: int(round(26.25 * b))          # beats inside a take -> take frame

# --------------------------------------------------------------------------------- the numbers
# Every value and its source in docs/architecture/audits/2026-10-27-menu-design-review.md (d823ce643).
# Rounds 0-4 score classes (A hub, B settings, C pickers/editors, D libraries, E notices); later passes
# score the families shown. Dates are the commits' UTC dates. All are subjective design judgments.
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
    'hub': [('6.5', 'ROUND 0', '27 OCT', 'Round 0 baseline, class A Hub and dialogs'),
            ('7', 'ROUND 1', '27 OCT', 'Round 1 scores, class A'),
            ('7.5', 'ROUND 2', '27 OCT', 'Round 2 scores, class A'),
            ('8', 'TARGET 8', '28 OCT', 'All-menus target 8 final matrix, A1 Hub'),
            ('8.5', 'TOWARD 9', '28 OCT', 'Hill climb toward 9 matrix, A1 Hub (ea7df5c1a)'),
            ('9', 'STRUCTURAL', '28 OCT', 'Structural pass matrix, A1 Hub, A3 Prompts, A5 Help at 9')],
    'round0': [('SETTINGS', '5.5'), ('PICKERS', '4'), ('LIBRARIES', '3.5'), ('NOTICES', '4')],
    'families_at_9': [(0, 'TOWARD 9', '28 OCT', 'Hill climb toward 9: "No family reached 9 overall"'),
                      (13, 'STRUCTURAL', '28 OCT', 'Structural pass: "Thirteen families reach 9 overall"'),
                      (26, 'FINISH', '28 OCT', 'Finish pass: "Twenty-six families reach 9"'),
                      (27, 'LEAD ACCEPTANCE', '29 OCT', 'Lead acceptance: Time Attack accepted at 9 overall '
                       '(d823ce643); individual criteria keep their 8.5 entries')],
}

REPS = [  # key, family, detail, take, first beat, end beat, take beat at shot start, tick beats
    ('libraries', 'LIBRARIES', 'Mod manager', 'mods', 56, 80, 3, [56, 65, 67, 69, 70, 72]),
    ('settings', 'SETTINGS', 'Display tab', 'settings', 80, 112, 4, [80, 89, 91, 93, 94, 96]),
    ('pickers', 'PICKERS', 'Locate ROM', 'locate', 112, 136, 0, [112, 121, 123, 125, 126, 128]),
    ('hub', 'HUB & DIALOGS', 'Help, quit, setup', 'dialogs', 136, 160, 0, [136, 145, 147, 149, 150, 152]),
]

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
        p = self.dir / 'events.csv'
        for row in csv.DictReader(p.open()):
            if row['kind'] == 'cue':
                out.append((int(row['frame']), row['detail']))
        return out


@lru_cache(maxsize=None)
def clip(era, take):
    return Clip(era, take)


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
    """Deep navy with slow diagonal bands leaning like title-card speed lines."""
    base, diag = _stage_base()
    band = ((diag - f * 1.2) // 90) % 2
    c = base.copy()
    c += (band[..., None] * np.array((4, 8, 18), np.float32))
    return c


def pane(c, img, x, y, s=S, border=6, colour=GOLD, alpha=1.0):
    big = up(img, s)
    h, w = big.shape[:2]
    if border:
        c[y - border:y + h + border, x - border:x + w + border] = np.array(colour, np.float32) * alpha + \
            c[y - border:y + h + border, x - border:x + w + border] * (1 - alpha)
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


def over(dst, src, x, y, alpha=1.0):
    """Source-over compositing of a float RGBA array onto a float RGBA array (labels and plates)."""
    x, y = int(round(x)), int(round(y))
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if x0 >= x1 or y0 >= y1 or alpha <= 0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
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


# ---------------------------------------------------------------------------- counter column


def roll(c, s_old, s_new, x, y, t, size=300, colour=GOLD):
    """A slot-machine roll from the old value to the new one over 14 frames (only recorded values)."""
    u = clamp(t / 14)
    img_new = text(s_new, 'title', size, colour, stroke=10, sfill=INK, shadow=12)
    if u >= 1 or s_old is None:
        paste(c, img_new, x, y)
        return img_new.shape
    img_old = text(s_old, 'title', size, colour, stroke=10, sfill=INK, shadow=12)
    h = img_new.shape[0]
    e = ease_out(u)
    slot = np.zeros((h, max(img_new.shape[1], img_old.shape[1]), 4), np.float32)
    # both values fully opaque, clipped by the slot window: the old one leaves upward as the new one
    # arrives from below with a small overshoot (no cross-faded double image)
    over(slot, img_old, 0, -int(e * h))
    over(slot, img_new, 0, int((1 - back(u, 1.3)) * h))
    paste(c, slot, x, y)
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
    """A step chart of the recorded stops reached so far (labelled by the round tag beside it)."""
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


def counter_column(c, f, key, family, detail, ticks, alpha=1.0):
    stops = SCORES[key]
    frames = [F(b) for b in ticks]
    k = max(i for i, t in enumerate(frames) if f >= t) if f >= frames[0] else 0
    t = f - frames[k]
    x = COL_X
    kick = text('DESIGN REVIEW', 'sub', 34, LIGHT, tracking=6)
    paste(c, kick, x, 96, alpha)
    paste(c, text(family, 'title', 92 if len(family) < 10 else 76, WHITE, stroke=5, sfill=INK, shadow=6), x, 136, alpha)
    paste(c, text(detail, 'sub', 44, GOLD, stroke=3, sfill=INK, shadow=4), x, 250, alpha)
    prev = stops[k - 1][0] if k > 0 else None
    shape = roll(c, prev, stops[k][0], x - 6, 318, t)
    ten = text('/10', 'title', 64, LIGHT, stroke=4, sfill=INK, shadow=5)
    paste(c, ten, min(x + shape[1] - 10, W - 24 - ten.shape[1]), 318 + shape[0] - ten.shape[0] - 36, alpha)
    flash = (1 - clamp(t / 18)) if k > 0 else 0.0
    pips(c, x, 712, float(stops[k][0]), flash)
    tag = pill(f'{stops[k][1]} · {stops[k][2]}', 40)
    paste(c, tag, x, 768, clamp(t / 6) if k > 0 else 1.0)
    chart(c, x - 6, 846, [s[0] for s in stops], k, clamp(t / 10))


def divider_at(f, key, ticks):
    """Divider column (native px): 0 before the first tick; each recorded stop moves it to the share
    of the remaining climb it represents, easing over 10 frames from its beat."""
    stops = [float(s[0]) for s in SCORES[key]]
    s0 = stops[0]
    pos = [320 * (s - s0) / (stops[-1] - s0) for s in stops]
    frames = [F(b) for b in ticks]
    if f < frames[1]:
        return 0.0
    k = max(i for i, t in enumerate(frames) if f >= t)
    u = ease_out(clamp((f - frames[k]) / 10))
    return pos[k - 1] + (pos[k] - pos[k - 1]) * u


# --------------------------------------------------------------------------------- shot builders


def rep_shot(key, family, detail, take, b0, b1, in_beat, ticks):
    old, new = clip('pre', take), clip('new', take)
    src0 = fr(in_beat)

    def fn(f, shot, edit):
        c = stage(f)
        i = src0 + (f - F(b0))
        d = divider_at(f, key, ticks)
        img = compare_native(old.native(i), new.native(i), d)
        x, y = PANE_L
        pane(c, img, x, y)
        divider(c, x, y, d)
        era_tabs(c, x, y, d)
        counter_column(c, f, key, family, detail, ticks)
        return c
    return fn


def cold_open(f, shot, edit):
    c = stage(f)
    old, new = clip('pre', 'shader'), clip('new', 'shader')
    d = 320 * ease_out(clamp((f - F(8)) / (F(10) - F(8)))) if f >= F(8) else 0.0
    d = round(d)
    x, y = PANE_C
    pane(c, compare_native(old.native(f), new.native(f), d), x, y)
    divider(c, x, y, d)
    if f < F(16) - 8:
        era_tabs(c, x, y, d)
    return c


def title_bg(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    img = clip('new', 'shader').native(f)
    pane(c, img, x, y)
    u = smooth(clamp((f - F(16)) / 20))
    c *= 1 - 0.62 * u
    return c


def prologue_v05(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('v05', 'v05-title').native(f - F(24)), x, y)
    return c


def prologue_pre(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    pane(c, clip('pre', 'hub').native(f - F(32)), x, y)
    return c


GRID = [  # take, take frame at b40, label index
    ('settings', fr(8)), ('locate', fr(2)), ('mods', fr(3)), ('legal', 200)]
GRID_POS = [(56, 40), (720, 40), (56, 552), (720, 552)]


def round0(f, shot, edit):
    c = stage(f)
    for k, ((take, src), (x, y)) in enumerate(zip(GRID, GRID_POS)):
        t0 = F(40 + k)
        if f < t0:
            continue
        drop = int(round((1 - ease_out(clamp((f - t0) / 14))) * -600))
        img = up(clip('pre', take).native(src + f - F(40)), 2)
        yy = y + drop
        if yy + 448 > 0:
            top = max(0, -yy)
            c[max(0, yy - 4):yy + 452, x - 4:x + 644] = np.array(LIGHT, np.float32)
            c[yy + top:yy + 448, x:x + 640] = img[top:]
        name, score = SCORES['round0'][k]
        plate = rounded(640, 44, 10, DEEP).copy()
        over(plate, text(name, 'title_it', 36, PALE), 14, 2)
        sc = text(score, 'title', 40, GOLD)
        over(plate, sc, 640 - 14 - sc.shape[1], 0)
        paste(c, plate, x, y + 456 + drop, clamp((f - t0 - 6) / 8))
    x = COL_X + 20
    paste(c, text('ROUND 0', 'title', 120, WHITE, stroke=6, sfill=INK, shadow=8), x, 110, clamp((f - F(40)) / 10))
    paste(c, text('27 OCT 2026', 'sub', 48, GOLD, stroke=3, sfill=INK, shadow=4), x, 250, clamp((f - F(40) - 6) / 10))
    a = clamp((f - F(46)) / 12)
    for j, line in enumerate(['Scores out of 10 from', "OpenGGF's own design", 'review. Judgments,', 'not measurements.']):
        paste(c, text(line, 'body', 38, PALE, stroke=2, sfill=INK, shadow=3), x, 360 + j * 52, a)
    return c


WALL = [  # take, take frame at b160 (each runs to the payoff end without passing its last frame)
    ('hub', 160), ('settings', fr(14)), ('mods', fr(5)), ('locate', fr(0)), ('shader', 40), ('dialogs', fr(1))]


def wall(f, shot, edit):
    c = stage(f)
    for k, (take, src) in enumerate(WALL):
        t0 = F(160 + k)
        if f < t0:
            continue
        x, y = (k % 3) * 640, 92 + (k // 3) * 448
        drop = int(round((1 - ease_out(clamp((f - t0) / 12))) * -500))
        img = up(clip('new', take).native(src + f - F(160)), 2)
        yy = y + drop
        top = max(0, 92 - yy) if k < 3 else 0
        c[yy + top:yy + 448, x:x + 640] = img[top:]
        # after the slam every new menu lights up again, one cell every 8 frames
        light = smooth(clamp((f - F(176) - 40 - 8 * k) / 12))
        dim = smooth(clamp((f - F(168)) / 18)) * 0.76 * (1 - light)
        c[max(92, yy):yy + 448, x:x + 640] *= 1 - dim
    return c


def hero(f, shot, edit):
    c = stage(f)
    x, y = PANE_C
    img = clip('new', 'hub').native(f - shot.f0)
    t = f - shot.f0
    pane(c, img, x, y)
    u = smooth(clamp((t - 120) / 30))
    if u > 0:
        blurred = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6 * u)),
                             np.float32)
        c = blurred * (1 - 0.7 * u)
    return c


# ------------------------------------------------------------------------------------- overlays


def families_counter(c, f, o, edit=None):
    """Families at 9 per pass, counted up one family at a time like a results tally."""
    stops = SCORES['families_at_9']
    frames = [F(b) for b in COUNT_BEATS]
    if f < frames[0]:
        return
    k = max(i for i, t in enumerate(frames) if f >= t)
    shown = stops[k][0]
    if k > 0:
        prev = stops[k - 1][0]
        steps = shown - prev
        shown = prev + int(clamp((f - frames[k]) / max(1, min(40, 4 * steps))) * steps)
    a = clamp((f - frames[0]) / 10)
    t = f - F(176)
    payoff = t >= 0
    leave = smooth(clamp((t - 40) / 14)) if payoff else 0.0
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
        s = 1 + 0.5 * (1 - ease_out(clamp(t / 14))) - 0.2 * leave
    img = promo_kit.scaled(block, s) if s != 1.0 else block
    shake = math.sin(t * 2.4) * max(0, 12 - t) * 2.0 if payoff else 0.0
    paste(c, img, W / 2 - img.shape[1] / 2 + shake, 600 - img.shape[0] / 2, a * (1 - leave))
    if payoff and t >= 44:
        banner = text('27 / 27 MENU FAMILIES AT 9', 'title_it', 64, WHITE, stroke=5, sfill=INK, shadow=6, tracking=2)
        u = ease_out(clamp((t - 44) / 14))
        paste(c, banner, W / 2 - banner.shape[1] / 2, 10 - (1 - u) * 90, u * clamp((174 - t) / 8))


COUNT_BEATS = [168, 169.5, 172, 175]


def title_words(c, f, o, edit=None):
    rows = [('ROAD', 16, 170, WHITE), ('TO', 17, 170, WHITE)]
    x0 = 330
    for word, b, size, col in rows:
        t = f - F(b)
        if t < 0:
            continue
        img = text(word, 'title', size, col, stroke=9, sfill=INK, shadow=10)
        s = 0.4 + 0.6 * back(clamp(t / 10), 2.2)
        img = promo_kit.scaled(img, s)
        y = 250 if word == 'ROAD' else 470
        paste(c, img, x0 + 300 - img.shape[1] / 2, y + 100 - img.shape[0] / 2, clamp(t / 3))
    t = f - F(18)
    if t >= 0:
        nine = text('9', 'title', 640, GOLD, stroke=14, sfill=INK, shadow=18)
        s = 1 + 0.35 * (1 - ease_out(clamp(t / 12)))
        nine = promo_kit.scaled(nine, s)
        paste(c, nine, 1300 - nine.shape[1] / 2, 520 - nine.shape[0] / 2, clamp(t / 3))
    t = f - F(20)
    if t >= 0:
        sub = text("OpenGGF's menus, round by round", 'sub', 60, PALE, stroke=4, sfill=INK, shadow=5)
        paste(c, sub, W / 2 - sub.shape[1] / 2, 880 + (1 - ease_out(clamp(t / 14))) * 60, clamp(t / 10))


def era_label(c, f, o, edit=None):
    """Top-margin era tag over the prologue, rolling 0.5 -> 0.6 -> 0.7 at the push."""
    x = PANE_C[0]
    t_push = F(32)
    if f < t_push:
        ver, line = '0.5', 'OPENGGF 0.5 · APRIL 2026 RELEASE'
    else:
        steps = ['0.5', '0.6', '0.7']
        k = int(clamp((f - t_push) / 8, 0, 2))
        ver, line = steps[k], 'OPENGGF 0.7 IN DEVELOPMENT · 27 OCT 2026 · BEFORE THE REDESIGN'
    a = clamp((f - F(24) - 4) / 10) * clamp((F(40) - f) / 6)
    v = pill(ver, 46)
    paste(c, v, x, 24, a)
    paste(c, text(line, 'title_it', 44, PALE, stroke=3, sfill=INK, shadow=4), x + v.shape[1] + 16, 22, a)


def promise(c, f, o, edit=None):
    t = f - o.f0
    line = text('SAME GAME. NEW MENUS.', 'title_it', 64, WHITE, stroke=5, sfill=INK, shadow=6)
    paste(c, line, W / 2 - line.shape[1] / 2, 1000 + (1 - ease_out(clamp(t / 12))) * 40,
          clamp(t / 8) * clamp((o.f1 - f) / 8))


def end_card(c, f, o, edit=None):
    t = f - o.f0
    badge = np.asarray(Image.open(BADGE).convert('RGBA'), np.float32)
    paste(c, badge, W / 2 - badge.shape[1] / 2, 120, clamp(t / 12))
    lines = [
        (text('ROAD TO 9', 'title', 130, GOLD, stroke=8, sfill=INK, shadow=10), 392, 10),
        (text('Every OpenGGF menu, rebuilt round by round.', 'sub', 56, WHITE, stroke=4, sfill=INK, shadow=5), 546, 22),
        (text('github.com/OpenGGF/OpenGGF', 'title_it', 78, WHITE, stroke=5, sfill=INK, shadow=6), 640, 34),
        (text('In development for OpenGGF 0.7', 'body', 42, LIGHT, stroke=3, sfill=INK, shadow=4), 756, 44),
        (text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body', 36, PALE,
              stroke=2, sfill=INK, shadow=3), 900, 56),
        (text("Scores: OpenGGF's own menu design review, 27–29 Oct 2026. Subjective judgments, "
              'not usability measurements.', 'body', 30, LIGHT, stroke=2, sfill=INK, shadow=3), 962, 64),
    ]
    for img, y, d in lines:
        paste(c, img, W / 2 - img.shape[1] / 2, y + (1 - ease_out(clamp((t - d) / 14))) * 30, clamp((t - d) / 10))


# ----------------------------------------------------------------------------------- the edit

CHAPTERS = []   # (start frame, end frame, title, sources)
CUES = []       # (output frame, era, take, take frame, cue)
E = None


def sfx(name):
    return AUDIO / 'sfx' / f's2-sfx-{name}-paced.wav'


def build(e):
    global CHAPTERS, CUES
    CHAPTERS, CUES = [], []
    X = e.X
    # A. cold open: the in-game picker, before then now, on the bed's intro build
    e.S(Custom(0, F(16), cold_open))
    CHAPTERS.append((0, F(16), 'Cold open: the in-game shader picker, before and now',
                     'pre+new/shader 0-446 (EHZ1 real start, RIGHT held; picker open 131-341)'))
    e.O(Fn(F(12), F(16), promise))
    X(F(8), sfx('ab'), 1.4)
    X(F(14), sfx('e0'), 0.9, length=(F(16) - F(14)) / FPS)
    # B. title drop
    e.S(Custom(F(16), F(24), title_bg))
    CHAPTERS.append((F(16), F(24), 'Title: Road to 9', 'new/shader 446-656, dimmed'))
    e.O(Flash(F(16), 16, 0.8))
    e.O(Fn(F(16), F(24), title_words))
    X(F(16), sfx('bc'), 1.0)
    X(F(18), sfx('c5'), 0.9)
    # C. prologue: 0.5, then the pre-redesign 0.7 hub
    e.S(Custom(F(24), F(32), prologue_v05, trans='wipe', tdur=14))
    e.S(Custom(F(32), F(40), prologue_pre, trans='push', tdur=16, tdir='left'))
    e.O(Fn(F(24), F(40), era_label))
    X(F(24) - 4, sfx('ab'), 1.4)
    X(F(32), sfx('ab'), 1.4)
    CHAPTERS.append((F(24), F(40), 'Where it started: OpenGGF 0.5, then the 0.7 hub before the redesign',
                     'v05/v05-title 0-210; pre/hub 0-210'))
    for fo, cue in clip('pre', 'hub').cues():
        if fo < F(40) - F(32):
            CUES.append((F(32) + fo, 'pre', 'hub', fo, cue))
    # D. round 0
    e.S(Custom(F(40), F(56), round0, trans='wipe', tdur=14))
    X(F(40) - 4, sfx('ab'), 1.4)
    for k in range(4):
        X(F(40 + k), sfx('cd'), 1.1)
    CHAPTERS.append((F(40), F(56), 'Round 0, 27 Oct 2026: the old menus and their first scores',
                     'pre/settings-pre, pre/locate, pre/mods, pre/legal (grid, 2x)'))
    # E. the four reps
    for key, family, detail, take, b0, b1, in_beat, ticks in REPS:
        e.S(Custom(F(b0), F(b1), rep_shot(key, family, detail, take, b0, b1, in_beat, ticks), trans='wipe', tdur=14))
        X(F(b0) - 4, sfx('ab'), 1.4)
        for b in ticks[1:-1]:
            X(F(b), sfx('cd'), 1.1)
        X(F(ticks[-1]), sfx('c5'), 0.9)
        src0 = fr(in_beat)
        for era in ('pre', 'new'):
            for fo, cue in clip(era, take).cues():
                out = F(b0) + fo - src0
                if F(b0) <= out < F(b1):
                    d = divider_at(out, key, ticks)
                    visible = 'new' if d >= 160 else 'pre'
                    if era == visible:
                        CUES.append((out, era, take, fo, cue))
        CHAPTERS.append((F(b0), F(b1), f'{family.title()}: {detail}, {SCORES[key][0][0]} to 9',
                         f'pre+new/{take} take frames {src0}-{src0 + F(b1) - F(b0) - 1}'))
    # F. climax: the wall of new menus, the count of families at 9
    payoff = F(176) + 174
    e.S(Custom(F(160), payoff, wall, trans='wipe', tdur=14))
    X(F(160) - 4, sfx('ab'), 1.4)
    for k in range(6):
        X(F(160 + k), sfx('cd'), 1.2)
    e.O(Fn(F(168), payoff, families_counter))
    beats = COUNT_BEATS
    vals = [s[0] for s in SCORES['families_at_9']]
    for k in range(1, len(beats)):
        steps = vals[k] - vals[k - 1]
        dur = max(1, min(40, 4 * steps))
        for j in range(steps):
            X(F(beats[k]) + int(j * dur / steps), sfx('cd'), 1.3)
        if k < len(beats) - 1:
            X(F(beats[k]) + dur, sfx('c5'), 0.8)
    e.O(Flash(F(176), 20, 0.9))
    CHAPTERS.append((F(160), payoff, 'Twenty-seven of twenty-seven menu families at 9',
                     'new/hub, settings-new, mods, locate, shader, dialogs (wall, 2x)'))
    # G. hero and end card
    end = payoff + 420
    e.S(Custom(payoff, end, hero, trans='iris', tdur=24))
    X(payoff - 6, sfx('c3'), 1.0)
    for fo, cue in clip('new', 'hub').cues():
        out = payoff + fo
        if payoff <= out < payoff + 120:
            CUES.append((out, 'new', 'hub', fo, cue))
    e.O(Fn(payoff + 130, end, end_card))
    e.O(Fade(end - 50, end + 1))
    CHAPTERS.append((payoff, end, 'The delivered hub, end card',
                     'new/hub take frames 0-419'))
    # sound: one bed, the jingle on the payoff, the hub's own theme under the end card
    e.bed(AUDIO / 'music/s2-music-82-paced.wav', 0, 0.75, length=F(176) / FPS + 0.02, fade_out=0.03)
    e.bed(AUDIO / 'music/s2-music-ba-paced.wav', F(176), 0.95)
    e.bed(AUDIO / 'music/s2-music-96-paced.wav', payoff, 0.8, length=(end - payoff) / FPS, fade_out=1.6)
    for out, era, take, fo, cue in CUES:
        e.X(out, AUDIO / 'ui' / f'ui-{cue.lower()}.wav', 1.1)
    return end


def edit():
    global E
    if E is None:
        E = Edit(bpm=BPM, first=FIRST, fps=FPS, size=(W, H), out=FINAL / 'menu-evolution-promo.mp4', work=BUILD)
        E.total = build(E)
    return E


# ---------------------------------------------------------------------------------- audio prep


def host_ui_tone(notes, rate=48000):
    """HostUiSfx (com.openggf.audio.presentation, identical at 2f9ca84b1 and d823ce643): sine notes at
    peak 0.18 with raised-cosine 8 ms attack / 18 ms release, mono."""
    out = []
    for hz, ms in notes:
        n = round(rate * ms / 1000)
        k = np.arange(n)
        fade = lambda p: 0.5 - 0.5 * np.cos(np.pi * np.minimum(1.0, p))
        env = np.minimum(fade(k / (rate * 8 // 1000)), fade((n - 1 - k) / (rate * 18 // 1000)))
        out.append(np.sin(2 * np.pi * hz * k / rate) * 0.18 * env)
    return np.round(np.concatenate(out) * 32767) / 32767


def prep():
    d = AUDIO / 'ui'
    d.mkdir(parents=True, exist_ok=True)
    cues = {'navigate': [(760, 45)], 'confirm': [(660, 55), (990, 75)], 'cancel': [(520, 65)],
            'error': [(440, 75), (290, 95)]}
    for name, notes in cues.items():
        a = host_ui_tone(notes)
        write_wav(d / f'ui-{name}.wav', np.stack([a, a], axis=1))
    print('wrote', sorted(p.name for p in d.iterdir()))


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


def write_chapters(e, path):
    lines = [';FFMETADATA1', 'title=ROAD TO 9: OpenGGF menu evolution promo', 'artist=OpenGGF']
    for f0, f1, title, _ in CHAPTERS:
        lines += ['[CHAPTER]', 'TIMEBASE=1/60', f'START={f0}', f'END={f1}', f'title={title}']
    path.write_text('\n'.join(lines) + '\n')
    with (ROOT / 'sources/promo/edl.csv').open('w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['start_s', 'end_s', 'start_frame', 'end_frame', 'chapter', 'sources'])
        for f0, f1, title, src in CHAPTERS:
            w.writerow([f'{f0 / FPS:.3f}', f'{f1 / FPS:.3f}', f0, f1, title, src])
    with (ROOT / 'sources/promo/chapters.txt').open('w') as fh:
        for f0, f1, title, src in CHAPTERS:
            fh.write(f'{f0 / FPS:6.2f}-{f1 / FPS:6.2f}  {title}  [{src}]\n')
    (ROOT / 'sources/promo/cues.json').write_text(json.dumps(
        [dict(frame=o, era=era, take=t, take_frame=fo, cue=c) for o, era, t, fo, c in CUES], indent=0))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'prep':
        prep()
        return
    e = edit()
    if cmd == 'check':
        for w in e.check():
            print('warning:', w)
        print('pacing:', e.pacing()[0])
        print('end', e.end(), f'{e.end() / FPS:.2f}s', 'cues', len(CUES))
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
        write_chapters(e, meta)
        video = BUILD / 'master-video.mkv'
        frames_to(['ffmpeg', '-v', 'error', '-y', *RAW, '-c:v', 'ffv1', '-level', '3', '-g', '1', '-slices', '16',
                   '-slicecrc', '1', '-pix_fmt', 'bgr0', str(video)], 0, e.end())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-i', str(audio), '-i', str(meta),
                        '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2', '-c:v', 'copy',
                        '-c:a', 'pcm_s16le', str(FINAL / 'menu-evolution-master.mkv')], check=True)
        video.unlink()
        print(FINAL / 'menu-evolution-master.mkv')
    elif cmd == 'remix':
        # audio-only revision: new mix into the existing master (video stream copied, chapters kept)
        audio = BUILD / 'mix.wav'
        write_wav(audio, e.mix())
        meta = BUILD / 'chapters.ffmeta'
        write_chapters(e, meta)
        master_file = FINAL / 'menu-evolution-master.mkv'
        tmp = FINAL / 'menu-evolution-master.remix.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(master_file), '-i', str(audio), '-i', str(meta),
                        '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2', '-c:v', 'copy',
                        '-c:a', 'pcm_s16le', str(tmp)], check=True)
        tmp.replace(master_file)
        print(master_file)
    elif cmd == 'mp4':
        finish_mp4()


def true_peak(path):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    peak = float(tail.split('Peak:')[1].split('dBFS')[0].strip())
    integ = float(tail.split('I:')[1].split('LUFS')[0].strip())
    return peak, integ


def finish_mp4():
    master_file = FINAL / 'menu-evolution-master.mkv'
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
    out = FINAL / 'menu-evolution-promo.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(master_file), '-i', str(aac), '-i', str(meta),
                    '-map', '0:v', '-map', '1:a', '-map_metadata', '2', '-map_chapters', '2',
                    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                    '-c:a', 'copy', '-movflags', '+faststart', str(out)], check=True)
    (BUILD / 'audio-gain.json').write_text(json.dumps({'aac_gain_db': gain_db, 'true_peak_dbtp': peak,
                                                        'integrated_lufs': integ}))
    print(out)


if __name__ == '__main__':
    sys.modules.setdefault('promo_kit', promo_kit)
    main()
