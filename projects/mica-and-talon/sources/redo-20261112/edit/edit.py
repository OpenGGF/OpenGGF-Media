#!/usr/bin/env python3
"""MICA & TALON - public promo, owner-review redo (2026-11-12).

Audience: Sonic fans first, would-be modders second.
Form/evidence: gameplay showcase. Every gameplay claim is native OpenGGF footage from GameplayCaptureTool or
  the retained PromoCapture hosts at integration tip 1e0faac123 (positioned mid-act starts with declared
  rings/timer, listed in the README). Nothing is re-timed.
Promise: "Two original heroes, at home in all three classic Sonic games."
Cleverest true thing: not palette swaps. Every screen of three games is redrawn in that game's own style and
  driven by the game's own logic. Proof 1: a lockstep split, stock Sonic & Tails beside MICA & TALON on the same
  inputs; every position matches on every frame (measured in state.csv). Proof 2: "same moment, three games"
  triptychs (strike, titles, special stages, powered forms).
Selling points (each a moving proof): MICA's homing chain with its jade trail; TALON's flight, carry and
  divebomb, in Sonic 1 too; TALON flying the Tornado (Sky Chase, ending); titles, signposts, special stages,
  continue, data select, lives names; Gilded MICA, Solar TALON, Hyper MICA.
Hero moment: the powered climax over the chorus and lift (bars 60-84): Gilded MICA's burst and glinting run,
  Solar TALON's flare, then Hyper MICA's after-images and ONE Instagib hit on the Launch Base mini-boss on bar 79,
  then both together on bar 80: Hyper MICA and Solar TALON in one frame, TALON carrying her up past the towers. A fragment of
  Hyper MICA is in the cold open.
Sound: owner-supplied "RUN INTO THE SUNSHINE (Chiptune Remix)", played from its first sample, uncut. The track's
  tempo is not constant (172.2 BPM to bar 43, 170.2 by bar 80), so every cut sits on TRACKED bar lines
  (tools/beat_track.py), not a fixed BPM grid. One fade: raised cosine from bar 85 to bar 88 (119.14-123.41 s);
  from bar 89 the track's pulse falls apart (README "Music"). Sparse ROM stingers, rendered --paced, on the
  event frames from state.csv.
Palette: S2 title-card blue 2449DB, red FF0000, yellow FFFF00 (sampled from the native EHZ2 card), MICA jade,
  TALON slate.
Title face: Fira Sans Compressed Heavy on the S2 card's own blue band (the S2 card glyphs split "M" into
  "/\\/\\" at display scale); native lettering wherever the game supplies it (results, HUD, titles).
Canvas: full-bleed 320x180 windows of the native frame at exactly 6x; no camera moves. Splits only for
  comparisons. No slam-out on the title drop: the owner asked for no zooms; the native flash carries the hit.
Treatment: Slay the Robotnik beat grid + Putt-Putt's S2 title-card bands. Signature move: the banded wipe at
  chapter changes.
End card: lock-up, one line, URL, disclaimer over the pair shot playing on in soft focus; fades with the music.
Rejected: a 400-px widescreen capture for everything (camera-locked arenas leave an unrendered band, and the art
  is 17 % smaller); a zoom/push anywhere in the cold open (owner); a caption per shot; a feature grid as a chapter.
"""
import csv
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
T = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools/media'))
from promo_kit import *  # noqa: E402,F401

V = os.environ.get('MT_VERTICAL') == '1'
EDIT = dict(bpm=172.218, first=0.178, fps=60, size=(1080, 1920) if V else (1920, 1080),
            out=T / 'out' / ('kit-9x16.mp4' if V else 'kit-16x9.mp4'),
            work=T / 'work' / ('build-v' if V else 'build-h'))
CAP = T / 'captures'
SFX = T / 'sfx'
BAR_T = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]

BLUE2 = (36, 73, 219)
RED2 = (255, 0, 0)
YEL2 = (255, 255, 0)
JADE = (0, 146, 109)
SLATE = (84, 100, 150)
NAVYD = (8, 16, 56)
GOLD2 = (255, 200, 40)
ROSE = (219, 109, 146)

NOTES = []   # beat sheet rows for the storyboard: filled by build()


def bar(n, beat=0.0):
    """Output frame of tracked bar n (+ beats 0..4), measured on the uncut track."""
    k = int(n)
    t0, t1 = BAR_T[k], BAR_T[k + 1]
    return int(round((t0 + (t1 - t0) * ((n - k) * 4 + beat) / 4) * 60))


@lru_cache(None)
def clip(name):
    return Frames(CAP / name / 'frames')


@lru_cache(None)
def rows(name):
    return list(csv.DictReader(open(CAP / name / 'state.csv')))


def subject(name, i, key='', smooth_n=10):
    """Screen position of the player (or sidekick with key='sk_') in a capture, smoothed over +-n frames."""
    r = rows(name)
    xs, ys = [], []
    for k in range(i - smooth_n, i + smooth_n + 1):
        row = r[max(1, min(len(r) - 1, k))]
        if not row.get(key + 'x'):
            continue
        xs.append(float(row[key + 'x']) - float(row['cam_x']))
        ys.append(float(row[key + 'y']) - float(row['cam_y']))
    return (sum(xs) / len(xs), sum(ys) / len(ys)) if xs else (160, 112)


def view(img, cx, cy, zoom, ow, oh, ylo=0, yhi=224):
    """Camera onto a native frame that keeps its vertical window inside [ylo, yhi] (crop the HUD whole)."""
    vh = img.height / zoom
    vw = vh * ow / oh
    if vw > img.width:
        vw = img.width / zoom
        vh = vw * oh / ow
    x0 = clamp(cx - vw / 2, 0, img.width - vw)
    if vh <= yhi - ylo:
        y0 = clamp(cy - vh / 2, ylo, yhi - vh)
    else:
        y0 = clamp((ylo + yhi) / 2 - vh / 2, 0, img.height - vh)
    return arr(resample(img, x0, y0, vw, vh, ow, oh))


def full(name, i, y0=0, ow=None, oh=None):
    """The film's default canvas: a fixed 320x180 window of the native frame at exactly 6x (16:9). y0 picks the
    rows: 0 keeps the HUD whole and drops the lives icon whole; 44 does the reverse."""
    im = clip(name).frame(i)
    ow, oh = ow or EDIT['size'][0], oh or EDIT['size'][1]
    return arr(im.crop((0, y0, 320, y0 + 180)).resize((ow, oh), Image.NEAREST))


ACT = (58, 194)  # rows between the HUD and the lives icon


def tracked(name, i, ow, oh, zoom=1.4, key='', dy=0, window=ACT, pad=None, sm=10, slice_guard=False):
    """A view that follows the player. slice_guard is for slanted-split panes whose window reaches the HUD rows: a
    slice shows only the columns around the view centre, so while HUD rows (y < 58) are in view the centre eases
    right until the slice's left edge clears the HUD's last column (x 116). The HUD is then out of the slice
    whole, and a subject high on screen is not cut by the top edge."""
    im = clip(name).frame(i)
    x, y = subject(name, i, key, sm)
    if slice_guard:
        vh = im.height / zoom
        vw = vh * ow / oh
        y0 = clamp(y + dy - vh / 2, window[0], max(window[0], window[1] - vh))
        half = (ow / 6 + 0.22 * oh / 2) / ow * vw          # slice half-width plus its lean, in native px
        x += clamp((58 - y0) / 16) * max(0.0, 116 + half - x)
    if pad:
        canvas = Image.new('RGB', (im.width + 2 * pad, im.height), NAVYD)
        canvas.paste(im, (pad, 0))
        im, x = canvas, x + pad
    return view(im, x, y + dy, zoom, ow, oh, *window)


# ------------------------------------------------------------------------------- graphics

def card_band(w, h, word_img=None, tab=True, strip=True):
    """The S2 title card in miniature: solid card blue, serrated red tab, yellow strip."""
    a = np.zeros((h, w, 4), np.float32)
    a[..., :3] = BLUE2
    a[..., 3] = 255
    if strip:
        a[h - max(10, h // 9):, :, :3] = YEL2
    if tab:
        tw = max(40, h // 3)
        a[:, :tw, :3] = RED2
        zig = max(8, h // 14)
        for yy in range(h):
            k = (yy // zig) % 2
            edge = tw + (zig // 2 if k else 0)
            a[yy, tw:edge, :3] = RED2
    if word_img is not None:
        x = (max(40, h // 3) + 50) if tab else 50
        paste(a[..., :3], word_img, x, (h - max(10, h // 9) - word_img.shape[0]) / 2)
    return a


class CardHeader(Overlay):
    """Chapter header, S2 title-card grammar: the red tab drops from the top-left, the blue band and its
    letters slide in from the right, the yellow sub-line follows; everything leaves left at double speed."""

    def __init__(self, f0, f1, word, sub=None, y=None, h=150):
        super().__init__(f0, f1)
        self.word, self.sub, self.y, self.h = word, sub, y, h

    def draw(self, c, f, e):
        h = self.h
        y = self.y if self.y is not None else e.H - h - 40
        word = text(self.word, 'title', 104, WHITE, stroke=7, sfill=NAVY, shadow=8, scol=(0, 0, 30, 230), tracking=3)
        sub = text(self.sub, 'title_it', 46, YELLOW, stroke=5, shadow=5) if self.sub else None
        w = min(e.W - 60, word.shape[1] + 260 + (sub.shape[1] + 60 if sub is not None else 0))
        band = card_band(w, h, word)
        if sub is not None:
            paste(band[..., :3], sub, w - sub.shape[1] - 40, h - max(10, h // 9) - sub.shape[0] - 10)
        t, out = f - self.f0, self.f1 - f
        u_in, u_out = clamp(t / 14), clamp(out / 8)
        x = 30 + (1 - ease_out(u_in)) * (e.W + 40) - (1 - u_out) * (w + 80)
        paste(c, band, x, y)
        tab = np.zeros((h + 40, max(40, h // 3), 4), np.float32)
        tab[..., :3] = RED2
        tab[..., 3] = 255
        ty = y - 20 - (1 - ease_out(clamp(t / 10))) * (y + h + 60) - (1 - u_out) * (h + 200)
        paste(c, tab, 30 - (1 - u_out) * (w + 80), ty)


@lru_cache(None)
def lockup_words(size):
    """MICA & TALON in the heavy condensed face: both names the same size and colour (partners), the '&' yellow."""
    st, sh, tr = max(6, size // 14), max(7, size // 12), max(3, size // 40)
    mica = text('MICA', 'title', size, WHITE, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230), tracking=tr)
    amp = text('&', 'title', size, YELLOW, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230))
    talon = text('TALON', 'title', size, WHITE, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230), tracking=tr)
    return mica, amp, talon


def draw_lockup(c, band_x, band_y, h, t, size, beat=12, glint=None):
    """Words popping one beat apart onto an S2-card band whose left edge is band_x. glint is the canvas x of a
    slanted gold sweep across the white letters (None = no sweep)."""
    mica, amp, talon = lockup_words(size)
    gap = size // 6
    lx = band_x + max(40, h // 3) + 60
    ly = band_y + (h - max(10, h // 9) - mica.shape[0]) / 2 + 2
    for k, (im, x) in enumerate(((mica, lx), (amp, lx + mica.shape[1] + gap),
                                 (talon, lx + mica.shape[1] + gap + amp.shape[1] + gap))):
        u = (t - 6 - k * beat) / 7
        if u <= 0:
            continue
        s = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
        im2 = scaled(im, s) if s != 1.0 else im
        if glint is not None and s == 1.0:
            yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]].astype(np.float32)
            d = np.abs((x + xx) - 0.45 * (yy - im.shape[0] / 2) - glint)
            k_ = np.clip(1 - d / 70, 0, 1)[..., None] * (im[..., :3].min(axis=2, keepdims=True) > 200)   # white faces only
            im2 = im.copy()
            im2[..., :3] = im[..., :3] * (1 - k_) + np.array(GOLD2, np.float32) * k_
        paste(c, im2, x + (im.shape[1] - im2.shape[1]) / 2, ly + (im.shape[0] - im2.shape[0]) / 2, clamp(u * 2))


def lockup_width(h, size):
    mica, amp, talon = lockup_words(size)
    return max(40, h // 3) + 60 + mica.shape[1] + amp.shape[1] + talon.shape[1] + 2 * (size // 6) + 70


def pill(label, bg=JADE, size=50, fg=WHITE):
    return chip(label, size=size, fg=fg, bg=bg)


def line(s, size=74, fill=WHITE):
    return text(s, 'title_it', size, fill, stroke=7, sfill=NAVY, shadow=7, scol=(0, 0, 30, 230), tracking=2)


class Tag(Overlay):
    """A name pill riding above a character (screen position from the capture's state.csv): the two heroes get
    the same size tag, each in their own colour. A tag never sits on the native HUD (it rides under the character
    instead) and never touches the other hero's tag (it stacks above it)."""

    def __init__(self, f0, f1, label, bg, name, src0, key='', y0=0, dy=-34, other=None):
        super().__init__(f0, f1)
        self.img, self.name, self.src0, self.key, self.y0, self.dy = pill(label, bg, 54), name, src0, key, y0, dy
        self.other = other

    def place(self, f, e, key, im):
        x, y = subject(self.name, self.src0 + f - e.shot_at(f).f0, key, 6)
        px, py = x * 6 - im.shape[1] / 2, (y - self.y0 + self.dy) * 6 - im.shape[0]
        if py < 372 and px < 720:      # would sit on the native HUD (SCORE/TIME/RINGS): ride under the character instead
            py = (y - self.y0 + 30) * 6
        return clamp(px, 20, e.W - im.shape[1] - 20), max(20, py)

    def draw(self, c, f, e):
        t, out = f - self.f0, self.f1 - f
        s = 0.7 + 0.3 * back(t / 9, 2.0) if t < 9 else 1.0
        im = scaled(self.img, s) if s != 1.0 else self.img
        px, py = self.place(f, e, self.key, self.img)
        if self.other is not None:     # keep clear of the other hero's tag
            ox, oy = self.place(f, e, self.other, self.img)
            if abs(px - ox) < self.img.shape[1] + 16 and abs(py - oy) < self.img.shape[0] + 10:
                py = oy - self.img.shape[0] - 12 if oy > self.img.shape[0] + 40 else oy + self.img.shape[0] + 12
        paste(c, im, px + (self.img.shape[1] - im.shape[1]) / 2, py + (self.img.shape[0] - im.shape[0]) / 2, clamp(t / 4) * clamp(out / 6))


# ----------------------------------------------------------------------------------- shots

def note(b0, b1, section, shot, proves, accompaniment, src):
    NOTES.append(dict(b0=b0, b1=b1, t0=bar(b0) / 60, t1=bar(b1) / 60, section=section, shot=shot, proves=proves,
                      accompaniment=accompaniment, src=src))


K = {}       # build_h's scalar locals (source offsets, cut frames, capture ids), reused by the vertical cut


def build(e):
    total = build_h(e)
    if V:                                     # same sound and timing; every picture recomposed for 9:16
        e.shots.clear()
        e.overlays.clear()
        e.punches.clear()
        build_v(e)
    return total


def build_h(e):
    W, H = e.W, e.H
    NOTES.clear()
    e.bed(T / 'work/bed.wav', 0, 0.75, fade_out=0.0)

    # ================= COLD OPEN, bars 0-12 (intro + riser) =======================================
    # S3K title roll-in, as it ships, from its first frame without the SEGA logo: the smear (src 267), the native
    # flash (296), logo drop, wink (~404). The film opens on black for the 33 frames the logo is on screen
    # (src 234-266); the in-point is unchanged, so nothing inside the roll-in is cut. Last frame shown is src 411:
    # the title's small Tornado fly-by (stock art) puts its first pixel on screen at 412.
    def rollin(f, s, ed):
        i = 234 + f - s.f0
        if i < 267:
            return np.zeros((H, W, 3), np.float32)
        return full('title-s3k', i, 8)            # rows 8-188: '& KNUCKLES' whole, menu rows out

    e.S(Custom(0, bar(2), rollin))
    note(0, 2, 'Cold open', 'Black for 0.55 s, then the Sonic 3 & Knuckles title roll-in from its first frame without the SEGA logo; whole width, no camera move',
         'The S3K intro is MICA: the smear frames, the flash, the wink', 'cut from black to the smear on beat 2; native white flash at 1.03 s; logo drop; wink at 2.8 s',
         [('title-s3k', 268), ('title-s3k', 300), ('title-s3k', 405)])

    # Partners: MICA and TALON run Launch Base side by side; each gets a name tag of the same size.
    lbz0 = 62
    e.S(Custom(bar(2), bar(4), lambda f, s, ed: full('d-lbz1-team', lbz0 + f - s.f0)))
    e.O(Tag(bar(2) + 14, bar(4) - 4, 'MICA', JADE, 'd-lbz1-team', lbz0))
    e.O(Tag(bar(2, 1) + 14, bar(4) - 4, 'TALON', SLATE, 'd-lbz1-team', lbz0, key='sk_', other=''))
    note(2, 4, 'Cold open', 'S3K Launch Base 1: MICA and TALON run together', 'Two heroes, equal billing, in play',
         'name tags pop a beat apart (MICA jade, TALON slate, same size)', [('d-lbz1-team', lbz0 + 40), ('d-lbz1-team', lbz0 + 120)])

    # The carry: TALON catches MICA and climbs out of the canopy to the open sky.
    e.S(Custom(bar(4), bar(8), lambda f, s, ed: full('d-carry-fly', 30 + f - s.f0)))
    e.O(Shade(bar(5), bar(8) - 6, 'bottom'))
    e.O(Txt(bar(5), bar(8) - 6, line('TWO ORIGINAL HEROES. THREE CLASSIC GAMES.', 72), W / 2, H - 150, enter='up',
            leave='fade', centre=True, dur=12))
    e.X(bar(4) + 58 - 30, SFX / 's3k-sfx-4a-paced.wav', 1.4)   # ROM Grab on the catch frame (carry-fly #58)
    note(4, 8, 'Cold open', 'S3K Angel Island 1: TALON catches MICA and carries her above the canopy',
         'Carry: his flight and carry art are one character', 'ROM grab sound on the catch; climb reveals the sea; the promise line rises on bar 5',
         [('d-carry-fly', 62), ('d-carry-fly', 200), ('d-carry-fly', 330)])

    # Hero fragment on the riser: Hyper MICA's after-images and an Instagib kill in Death Egg.
    hyp = 'd-dez1-hyper'
    frag0 = 185 - (bar(9) - bar(8))        # the kill (#185) lands on bar 9
    e.S(Custom(bar(8), bar(10), lambda f, s, ed: full(hyp, frag0 + f - s.f0)))
    e.O(Flash(bar(9), 8, 0.5))
    e.X(bar(9), SFX / 's3k-sfx-b4-paced.wav', 1.8)
    note(8, 10, 'Cold open (riser)', 'S3K Death Egg 1: Hyper MICA, after-images, one strike (hero fragment)',
         'A taste of the climax in the first 12 s', 'kill + ROM explosion on bar 9', [(hyp, frag0 + 20), (hyp, 185)])

    # ================= TITLE DROP, bars 10-16 ====================================================
    # S2 title as it ships: on the riser the emblem holds on black while MICA then TALON rise; the title's own
    # white flash (src 757) is the drop on bar 12.
    s2_0 = 757 - (bar(12) - bar(10))
    # rows 26-206: the emblem whole; the bottom row ('2 PLAYER VS' and the copyright line, rows 208-215) is out whole.
    # The lock-up band is part of this shot's picture (not an overlay), so the chapter wipe carries it away and the
    # native '1 PLAYER' row under it is never uncovered.
    def s2_title(f, s, ed):
        c = view(clip('title-s2').frame(s2_0 + f - s.f0), 160, 116, 1.0, W, H, 26, 206)
        t = f - (bar(12) + 10)
        if t >= 0:
            h, size = 150, 116
            y = H - h
            x = (1 - ease_out(clamp(t / 14))) * (W + 60)
            paste(c, card_band(W, h), x, y)   # full width, rows 181-206
            g = f - bar(14)                   # a gold glint sweeps the names on bar 14
            draw_lockup(c, x + (W - lockup_width(h, size)) / 2, y, h, t, size, beat=bar(12, 1) - bar(12),
                        glint=W * 0.22 + W * 0.60 * g / 34 if 0 <= g < 34 else None)
        return c

    e.S(Custom(bar(10), bar(16), s2_title))
    e.O(Flash(bar(12), 16, 0.9))
    e.X(bar(12), SFX / 's3k-sfx-b3-paced.wav', 1.6)
    note(10, 16, 'TITLE DROP', 'Sonic 2 title as it ships: MICA then TALON rise over the emblem; native flash on the drop; lock-up band',
         'The game\'s own title screen is the title; the pop-out no longer clips',
         'both rises on the riser; native flash + Big Ring on bar 12; "MICA" "&" "TALON" pop a beat apart; a gold glint sweeps the names on bar 14',
         [('title-s2', s2_0 + 60), ('title-s2', s2_0 + 150), ('title-s2', 800)])

    # ================= CH1 MICA, bars 16-28 =======================================================
    # The Marble Garden take ends at src 167: she is hit at #183 and the film does not show the hero losing rings.
    mgz = 'd-mgz2-chain'
    e.S(Custom(bar(16), bar(18), lambda f, s, ed: full(mgz, f - s.f0), trans='wipe', tdur=16))
    e.O(CardHeader(bar(16) + 4, bar(17) - 22, 'MICA', sub='HOMING STRIKE'))
    mgz_hits = [65, 82, 104]              # score 87300 -> 87400 -> 87600 -> 88100: native 100, 200, 500
    for h in mgz_hits:
        e.X(bar(16) + h, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    chain_imgs = [text(s, 'title', 150, YELLOW, stroke=9, sfill=NAVY, shadow=10) for s in ('1', '2', '3')]
    for k, h in enumerate(mgz_hits):
        end = bar(16) + mgz_hits[k + 1] if k < 2 else bar(18) - 6
        e.O(Txt(bar(16) + h, end, chain_imgs[k], W * 0.87, H * 0.24, enter='pop', leave='pop', centre=True, dur=8))
    e.O(Txt(bar(16) + mgz_hits[2] + 4, bar(18) - 6, pill('CHAIN', JADE, 56), W * 0.87, H * 0.24 + 130, enter='up', centre=True))
    note(16, 18, 'MICA', 'S3K Marble Garden 2, 36 rings at 2:15: lock-on, three Mantises struck in one flight (native score 100, 200, 500)',
         'The homing chain, with the jade trail', 'banded wipe + header; 1-2-3 counter and ROM explosion on each hit',
         [(mgz, 60), (mgz, 84), (mgz, 106)])

    # One move, three games: each slice drops on its bar and lands its own strike 40 frames later.
    SLICE = (0, 194)   # slice panes may use the rows above 58 as headroom; tracked(slice_guard=True) keeps the HUD out of the slice

    def pane(name, src0, pad=120, zoom=1.65):
        return lambda lf: tracked(name, src0 + lf, W, H, zoom, pad=pad, window=SLICE, slice_guard=True)

    tri = [('d-ghz2-buzz', 60, 'SONIC 1', 's1-sfx-c1-paced.wav'), ('d-arz1-whisp', 138, 'SONIC 2', 's2-sfx-c1-paced.wav'),
           ('aiz-hero', 70, 'SONIC 3 & K', 's3k-sfx-b4-paced.wav')]

    def three(f, s, ed):
        panes = [(bar(18 + k / 2), pane(n, hit - 40), lab) for k, (n, hit, lab, _) in enumerate(tri)]
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(18), bar(22), three, trans='push', tdur=14, tdir='left'))
    for k, (n, hit, lab, wav) in enumerate(tri):
        e.X(bar(18 + k / 2) + 40, SFX / wav, 1.9)
    e.X(bar(18) + 50, SFX / 's1-sfx-c1-paced.wav', 1.9)   # S1 pane's second chained hit (d-ghz2-buzz #70)
    note(18, 22, 'MICA', 'Slanted triptych: the same strike in Sonic 1 (Green Hill 2), Sonic 2 (Aquatic Ruin 1), Sonic 3 & K (Angel Island 1)',
         'One move, three games, each in its own art style', 'a slice drops every two beats from bar 18; each lands its strike 40 frames later with that game\'s own pop; Sonic 1 chains a second pair',
         [('d-ghz2-buzz', 60), ('d-arz1-whisp', 138), ('aiz-hero', 70)])

    # Sky Chase: MICA strikes from the wing while TALON flies the Tornado; a real S2 chain (100, then 200).
    scz0 = 324 - (bar(23) - bar(22))      # score steps: #255 +100, #324 +100 (on bar 23), #358 +200 (chained)
    e.S(Custom(bar(22), bar(26), lambda f, s, ed: full('h-scz-a', scz0 + f - s.f0)))
    for h in (255, 324, 358):
        e.X(bar(22) + h - scz0, SFX / 's2-sfx-c1-paced.wav', 1.9)
    e.O(Txt(bar(22) + 358 - scz0 + 2, bar(25), pill('CHAIN  x2', JADE, 56), W * 0.84, H * 0.30, enter='pop', leave='fade', centre=True, dur=8))
    e.O(Txt(bar(24, 2), bar(26) - 6, pill('TALON FLIES THE TORNADO', SLATE, 50), W * 0.30, H * 0.86, enter='up', leave='fade', centre=True))
    note(22, 26, 'MICA', 'S2 Sky Chase from the act start: MICA strikes Balkiry and Nebula from the wing; TALON pilots',
         'A Sonic 2 homing chain (native 100 then 200) and TALON at the stick, in play',
         'three strikes with S2 pops; strike 2 on bar 23; CHAIN x2 on the chained hit; pilot callout',
         [('h-scz-a', 256), ('h-scz-a', 326), ('h-scz-a', 360)])

    # Partners again, into TALON's chapter: the two run Casino Night and leap into its skyline.
    cnz0 = 40
    e.S(Custom(bar(26), bar(28), lambda f, s, ed: full('d-cnz2-team', cnz0 + f - s.f0)))
    note(26, 28, 'MICA', 'S2 Casino Night 1, 45 rings at 1:30: MICA and TALON run past the neon and leap into the skyline together',
         'Partners in Sonic 2 as well; a third palette after jungle and sky', 'new zone on the cut; the leap off the ledge; TALON follows her down',
         [('d-cnz2-team', 60), ('d-cnz2-team', 120), ('d-cnz2-team', 180)])

    # ================= CH2 TALON, bars 28-36 (breakdown, build) ===================================
    syz = 'd-syz1-talon'
    syz0 = 118 - (bar(29, 1) - bar(28))   # kills (#118 +100, #160 +200) land on beats 2 and 4 of bar 29
    e.S(Custom(bar(28), bar(32), lambda f, s, ed: full(syz, syz0 + f - s.f0), trans='wipe', tdur=16))
    e.O(CardHeader(bar(28) + 4, bar(29) - 6, 'TALON', sub='FLIGHT  CARRY  DIVEBOMB'))
    for h in (118, 160):
        e.X(bar(28) + h - syz0, SFX / 's1-sfx-c1-paced.wav', 1.9)
    e.O(Txt(bar(30), bar(32) - 6, pill('IN SONIC 1, TOO', SLATE, 54), W * 0.80, H * 0.86, enter='up', leave='fade', centre=True))

    def lives(c, f, o, ed):   # the lives display the 16:9 window drops: shown whole, at its own scale, as an inset
        im = clip(syz).frame(syz0 + f - bar(28)).crop((8, 196, 80, 222)).resize((432, 156), Image.NEAREST)
        pop_panel(c, im, 60, H - 156 - 80, f, o.f0, None, 6, YEL2)

    e.O(Fn(bar(30), bar(32) - 6, lives))
    note(28, 32, 'TALON', 'S1 Spring Yard 1, 28 rings at 1:45: TALON takes off, flies between the columns, locks on and divebombs two Crabmeats (native 100, then 200)',
         'Flight and divebomb with the slate trail, in a game that never had a flyer; lives read TALON',
         'banded wipe + header; kills with S1 pops on beats 2 and 4 of bar 29; "IN SONIC 1, TOO" and the lives inset on bar 30; second take-off',
         [(syz, 70), (syz, 112), (syz, 120), (syz, 162)])

    verbs = [('d-cpz-talon', 22, '', 0, 'FLIGHT', SLICE), ('d-carry-fly', 60, 'sk_', 14, 'CARRY', SLICE), ('d-aiz-talon-dive', 80, '', 0, 'DIVEBOMB', SLICE)]

    def talon3(f, s, ed):
        panes = [(bar(32 + k / 2), (lambda n, s0, key, dy, win: lambda lf: tracked(n, s0 + lf, W, H, 1.65, key=key, dy=dy, pad=120, window=win, slice_guard=True))(n, s0, key, dy, win), lab)
                 for k, (n, s0, key, dy, lab, win) in enumerate(verbs)]
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(32), bar(36), talon3, trans='push', tdur=14, tdir='left'))
    e.X(bar(33) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)   # divebomb kill: d-aiz-talon-dive #120 (score +100)
    note(32, 36, 'TALON', 'Slanted triptych: flight (S2 Chemical Plant), carry (S3K), divebomb kill (S3K)',
         'Three verbs, one consistent character', 'a slice every two beats from bar 32; the divebomb lands 40 frames after its slice',
         [('d-cpz-talon', 120), ('d-carry-fly', 200), ('d-aiz-talon-dive', 120)])

    # ================= CH3 EVERY SCREEN, bars 36-60 ===============================================
    med0 = 40

    def lockstep(f, s, ed):
        i = med0 + f - s.f0
        mx, my = subject('f-cpz-medley', i)
        sx, sy = subject('f-cpz-medley', i, 'sk_')
        cx = (mx + sx) / 2 if abs(mx - sx) < 110 else mx

        def side(name):
            return lambda lf: view(clip(name).frame(i), cx, my, 1.1, W, H, 58, 224)   # rows 58+: the HUD is out whole
        return slanted_split(ed, f, [(s.f0 - 100, side('f-stock-cpz-medley'), None), (s.f0 - 100, side('f-cpz-medley'), None)],
                             divider=YEL2, drop_frames=1)

    e.S(Custom(bar(36), bar(40), lockstep, trans='wipe', tdur=16))
    e.O(CardHeader(bar(36) + 4, bar(37) + 30, 'EVERY SCREEN', sub='REDRAWN'))
    e.O(Txt(bar(36) + 20, bar(40) - 6, chip('ORIGINAL', size=50), W * 0.25, 60, enter='down', leave='fade', centre=True))
    e.O(Txt(bar(36) + 26, bar(40) - 6, pill('MICA & TALON', JADE, 50), W * 0.75, 60, enter='down', leave='fade', centre=True))
    e.O(Txt(bar(38), bar(40) - 6, line('SAME INPUTS. SAME PHYSICS. EVERY FRAME.', 66), W / 2, H - 130, enter='up', leave='fade',
            centre=True, dur=12))
    note(36, 40, 'EVERY SCREEN', 'Lockstep split, S2 Chemical Plant 1: stock Sonic & Tails | MICA & TALON on one input script',
         'Not a palette swap: run, jump, roll, skid, look up, duck, spindash all redrawn, and all 461 frames match position for position',
         'wipe + header on the drop; the two halves move as one; the line lands on bar 38',
         [('f-stock-cpz-medley', 125), ('f-cpz-medley', 125), ('f-cpz-medley', 285)])

    def titles3(f, s, ed):
        def tp(name, src, cx, cy):
            return lambda lf: view(clip(name).frame(src + lf), cx, cy, 1.25, W, H, 0, 224)
        starts = [bar(40), bar(40, 2), bar(41)]
        panes = [(starts[0], lambda lf: view(clip('title-s1').frame(392 + lf), 160, 72, 224 / 147, W, H, 0, 147), None),   # rows 0-147: the emblem's SEGA plate (148-164) stays out
                 (starts[1], tp('title-s2', 840, 172, 96), None), (starts[2], tp('title-s3k', 320, 150, 96), None)]
        c = slanted_split(ed, f, panes, divider=YEL2)
        for k, lab in enumerate(('SONIC 1', 'SONIC 2', 'SONIC 3 & K')):   # labels at the top: the bottom of each pane is the title's own lettering
            if f >= starts[k] + 8:
                p = chip(lab)
                cx = (k + 0.5) * W / 3 + 0.22 * (54 - H / 2)
                paste(c, p, cx - p.shape[1] / 2, 26, clamp((f - starts[k] - 8) / 8))
        return c

    e.S(Custom(bar(40), bar(44), titles3, trans='push', tdur=14, tdir='left'))
    note(40, 44, 'EVERY SCREEN', 'Slanted triptych: the three title screens',
         'Same moment, three games, three art styles', 'slices drop two beats apart; S1 pops up as its slice lands',
         [('title-s1', 440), ('title-s2', 860), ('title-s3k', 380)])

    def signs(f, s, ed):
        return pair_3x(ed, f, [(s.f0, 'd-ghz-clear', 135, 'SONIC 1'), (bar(44, 1), 'd-ehz-clear', 262, 'SONIC 2')])

    # S1's results card is excluded (its act oval draws over the text for stock Sonic too): S1 ends at src 316.
    e.S(Custom(bar(44), bar(46), signs))
    e.X(bar(44) + 150 - 135, SFX / 's1-sfx-cf-paced.wav', 1.5)
    e.S(Custom(bar(46), bar(48), lambda f, s, ed: full('d-ehz-clear', 470 + f - s.f0)))
    note(44, 48, 'EVERY SCREEN', 'Signposts spin to MICA in S1 Green Hill 1 and S2 Emerald Hill 1, then S2\'s own "MICA GOT THROUGH" tally',
         'Signposts and results lettering are hers', 'pair pops in a beat apart on the stabs; S1 signpost sound as she passes it; tally counts',
         [('d-ghz-clear', 200), ('d-ehz-clear', 330), ('d-ehz-clear', 520)])

    def stages(f, s, ed):
        panes = [(bar(48), lambda lf: view(clip('f-ghz-ss').frame(900 + lf), 160, 112, 1.0, W, H, 0, 224), 'SONIC 1'),
                 (bar(48, 2), lambda lf: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.0, W, H, 44, 224), 'SONIC 2'),
                 (bar(49), lambda lf: view(clip('q-blue-c').frame(430 + lf), 160, 140, 1.2, W, H, 34, 224), 'SONIC 3 & K')]   # after the banner (220-420), before the exit (940)
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(48), bar(52), stages, trans='push', tdur=14, tdir='left'))
    note(48, 52, 'EVERY SCREEN', 'Slanted triptych: the three special stages (S1 maze, S2 half-pipe with TALON, S3K Blue Sphere)',
         'Special stages posed per game', 'a slice every two beats on the stabs; the maze turns, the pipe bends, the sphere grid scrolls', [('f-ghz-ss', 1000), ('halfpipe-run', 800), ('q-blue-c', 500)])

    def screens(f, s, ed):
        t0 = s.f0
        bt = bar(52, 1) - bar(52)
        cells = [(t0, clip('continue'), 60, 'CONTINUE', (160, 100, 1.7)),
                 (t0 + bt, clip('data-select'), 405, 'DATA SELECT', (232, 110, 1.75)),
                 (t0 + 2 * bt, clip('halfpipe-run'), 1010, 'SPECIAL STAGE HUD', (160, 72, 1.25)),
                 (t0 + 3 * bt, clip('d-cpz-talon'), 60, 'LIVES', (46, 207, 4.6))]
        return grid(ed, f, cells, 2, 2, colour=YEL2)

    e.S(Custom(bar(52), bar(55), screens, trans='push', tdur=14, tdir='left'))
    note(52, 55, 'EVERY SCREEN', '2x2 grid: Continue (S2), Data Select (S3K), special-stage HUD names (S2), lives name TALON (S2)',
         'Breadth: every cell is moving native UI', 'cells pop a beat apart',
         [('continue', 100), ('data-select', 450), ('halfpipe-run', 1040), ('d-cpz-talon', 100)])

    # S2 ending: MICA flies beside the Tornado with TALON at the stick, then the final front-view pose.
    side0, side1 = bar(55), bar(56, 2)       # side view for 1.5 bars: the plane is in frame from its first beat
    e.S(Custom(side0, side1, lambda f, s, ed: full('ending', 2760 - (side1 - side0) + f - s.f0, 22)))
    end_src, end_land = 4086, 4098
    pose1 = bar(58, 2)
    e.S(Custom(side1, pose1, lambda f, s, ed: full('ending', end_src + f - s.f0, 22)))
    e.O(Txt(side1 + end_land - end_src + 4, pose1 - 4, pill('ENDINGS, TOO', JADE, 60), W * 0.74, H * 0.50,
            enter='pop', leave='fade', centre=True, dur=10))
    note(55, 58.5, 'EVERY SCREEN', 'S2 ending: MICA flies beside the Tornado, TALON piloting; then the front-view pose, MICA on the wing',
         'TALON pilots the Tornado, including the final pose', 'the plane rises into frame; MICA lands on the wing; ENDINGS, TOO',
         [('ending', 2700), ('ending', 4100), ('ending', 4140)])

    # ================= CH4 POWERED UP, bars 58.5-84 (chorus + lift) ===============================
    REV = 96                                   # S3K: gold/flame reveal frame; wind-up from #71, silhouette #84-95
    half = lambda n: bar(n) - (bar(n) - bar(n - 1)) // 2

    # Gilded: a bar and a half of normal MICA running Hydrocity first, so the form is seen to arrive mid-act.
    gil = 'd-hcz1-gilded-runin'             # runs from #24, jumps #114, ability press #135, gold reveal #160
    GREV, gstart = 160, bar(58, 2)
    g0 = GREV - (bar(60) - gstart)
    e.S(Custom(gstart, bar(64), lambda f, s, ed: full(gil, g0 + f - s.f0)))
    e.X(gstart + 135 - g0, SFX / 's3k-sfx-9f-paced.wav', 2.6)
    e.O(Flash(bar(60), 10, 0.45))
    e.O(CardHeader(bar(60) + 30, bar(61) + 50, 'POWERED UP', sub='50 RINGS  MID-ACT'))
    e.O(Txt(bar(62), bar(64) - 6, pill('GILDED MICA', GOLD2, 56, fg=NAVY), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))
    note(58.5, 64, 'POWERED UP (chorus)', 'S3K Hydrocity 1, 66 rings at 1:40: normal MICA runs the ledge, jumps, winds up and snaps open gold; glinting dashes over the bridge and down the curve',
         'Gilded transformation is animated, bright gold, Open Cone plates, coral boots, ring of glints',
         'ROM transform sound on the wind-up; the gold reveal lands ON bar 60; header; glints shed all run',
         [(gil, 60), (gil, 152), (gil, 162), (gil, 290)])

    def trails(f, s, ed):
        strips = [(bar(64), 'd-aiz-normal', 55 - 40), (bar(65), 'gilded-aiz', 94 - 40)]
        return stacked_tracked(ed, f, strips, [('NORMAL: JADE TRAIL', JADE, WHITE), ('GILDED: GOLD TRAIL', GOLD2, NAVY)], zoom=1.35)

    e.S(Custom(bar(64), bar(68) - (bar(68) - bar(67)) // 2, trails, trans='push', tdur=12, tdir='left'))
    e.X(bar(64) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    e.X(bar(65) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    note(64, 67.5, 'POWERED UP', 'Stacked pair, same Rhinobot in S3K Angel Island 1: normal MICA\'s strike above, Gilded MICA\'s below',
         'Normal trail is jade; Gilded trail is gold', 'strips slide in a bar apart; each strike lands 40 frames after its strip',
         [('d-aiz-normal', 55), ('gilded-aiz', 94)])

    sol = 'd-cnz1-solar'
    SREV = 76                                 # d-cnz1-solar: press #51, silhouette #64-75, flame-lit reveal #76 (measured)
    s0 = SREV - (bar(68) - half(68))
    e.S(Custom(half(68), bar(72), lambda f, s, ed: full(sol, s0 + f - s.f0)))
    e.X(half(68) + 51 - s0, SFX / 's3k-sfx-9f-paced.wav', 2.6)
    e.O(Flash(bar(68), 10, 0.45))
    e.O(Txt(bar(69), bar(72) - 6, pill('SOLAR TALON', (255, 146, 36), 56, fg=NAVY), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))
    note(67.5, 72, 'POWERED UP', 'S3K Carnival Night 1, 68 rings at 1:35: TALON\'s crest ignites, goggles drop, flare ring; ember flight across the night',
         'Solar transformation is animated; Corona Crest; embers in flight', 'ROM transform sound; the flame-lit reveal lands ON bar 68; flaps shed embers',
         [(sol, 66), (sol, 78), (sol, 230)])

    pw = [('f-slz1-gilded', 74, '', 'SONIC 1', None), ('g-mcz1-solar', 94, '', 'SONIC 2', None), ('d-aiz-solar-dive', 186, '', 'SONIC 3 & K', 's3k-sfx-b4-paced.wav')]

    def powered3(f, s, ed):
        panes = [(bar(72 + k / 2), pane(n, ev - 40), lab) for k, (n, ev, _, lab, _) in enumerate(pw)]
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(72), half(76), powered3, trans='push', tdur=14, tdir='left'))
    e.X(bar(73) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)   # d-aiz-solar-dive: dive pressed #176, Rhinobot struck #186
    note(72, 75.5, 'POWERED UP', 'Slanted triptych: Gilded MICA transforms in Sonic 1 (Star Light), Solar TALON transforms in Sonic 2 (Mystic Cave), Solar TALON divebombs a Rhinobot in S3K (Angel Island)',
         'Powered forms in all three games, a Super form in Sonic 1 included', 'a slice every two beats from bar 72; each transformation or kill lands 40 frames after its slice',
         [('f-slz1-gilded', 76), ('g-mcz1-solar', 96), ('d-aiz-solar-dive', 180), ('d-aiz-solar-dive', 187)])

    h0 = REV - (bar(76) - half(76))
    e.S(Custom(half(76), bar(78), lambda f, s, ed: full(hyp, h0 + f - s.f0)))
    e.X(half(76) + 71 - h0, SFX / 's3k-sfx-9f-paced.wav', 2.6)
    e.O(Flash(bar(76), 10, 0.5))
    e.X(half(76) + 185 - h0, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    e.O(Txt(bar(76) + 30, bar(78) - 6, pill('HYPER MICA', ROSE, 56), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))
    note(75.5, 78, 'HERO (lift)', 'S3K Death Egg 1, 75 rings, Super Emeralds: Hyper MICA, Prism Gilt flashing, banded after-images, a jade Instagib strike',
         'Hyper has Hyper-Sonic-style after-images in gold, white, jade and rose', 'reveal ON bar 76 (the lift); kill a bar later',
         [(hyp, 98), (hyp, 170), (hyp, 187)])

    # The boss: Launch Base 1's mini-boss, a real fight that ends the act. (The Angel Island machine used at the
    # storyboard is a scripted fire-bombing set piece; edit-aiz-boss-version.py keeps that cut.)
    # The game ends her Hyper form ON the kill frame: state.csv of e-lbz-boss-state has p1_super 1 -> 0 and
    # timer_paused 0 -> 1 at #648 (the ROM rule: a Super form ends when the HUD timer stops). She stays gold for
    # frames 651-660 and is jade from #663. From the hit, the part of the frame she is in sits under the ONE HIT.
    # card, so no frame shows her after the form has ended; the boss breaks apart beside it.
    boss = 'd-lbz-boss'
    HIT = 648                                 # score 283900 -> 284900; tap-jump #626, strike pressed #642
    b0 = HIT - (bar(79) - bar(78))
    e.S(Custom(bar(78), bar(80), lambda f, s, ed: full(boss, b0 + f - s.f0)))
    e.O(Flash(bar(79), 10, 0.55))
    e.X(bar(79), SFX / 's3k-sfx-6e-paced.wav', 2.2)
    e.X(bar(79) + 6, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    one_im = text('ONE', 'title', 250, WHITE, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
    hit_im = text('HIT.', 'title', 250, YELLOW, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
    CARD_X = 208 * 6                          # card edge at mid-height: native x 208; at her rows (69-96) it is x 203-209

    def hit_card(c, f, o, ed):
        t = f - o.f0
        xs, ys, _ = ed.grids()
        edge = CARD_X + 0.22 * (ys - H / 2) + (1 - ease_out(clamp(t / 7))) * (W - CARD_X + 200)
        c[xs >= edge] = np.array(BLUE2, np.float32)
        zig = ((ys // 18) % 2) * 9                      # the card's serrated red tab, as on the lock-up band
        c[(xs >= edge) & (xs < edge + 46 + zig)] = np.array(RED2, np.float32)
        c[(xs >= edge - 14) & (xs < edge)] = np.array(YEL2, np.float32)
        cx = (CARD_X + W) / 2 + 40 + (1 - ease_out(clamp(t / 7))) * (W - CARD_X + 200)
        for k, (im, yy) in enumerate(((one_im, H * 0.33), (hit_im, H * 0.63))):
            u = (t - 5 - k * (bar(79, 1) - bar(79)) / 2) / 7
            if u <= 0:
                continue
            sc = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, cx - im2.shape[1] / 2, yy - im2.shape[0] / 2, clamp(u * 2))

    e.O(Fn(bar(79), bar(80), hit_card))
    note(78, 80, 'HERO', 'S3K Launch Base 1 mini-boss, 83 rings at 3:10, score 283,900: it swings in overhead; Hyper MICA hops and strikes ONCE from its side; score +1000; it breaks apart beside the ONE HIT. card',
         'Hyper kills a boss with one Instagib hit; jade strike, banded after-images',
         'the hop over bar 78; the hit ON bar 79 with flash, ROM boss-hit + explosion; the card slams in from the right and ONE / HIT. pop half a beat apart; the machine flies to pieces',
         [(boss, 620), (boss, 645), (boss, 650), (boss, 690)])

    # The pair payoff: Hyper MICA and Solar TALON together, both powered, in one frame. TALON is on pad 2. Both
    # press at #45; twin silhouettes #58-69; both snap open at #70, which lands ON beat 2 of bar 80. TALON then
    # catches her (#125) and carries her up. The cut is white for the nine frames in which the two are still in
    # normal colours (#49-57). Her Prism Gilt cycle shows jade at #139-159 and #265-285; the shot ends
    # at #388, three frames before the next jade phase, so the last image is gold and flame.
    pair = 'd-lbz-pair-312'                   # d-lbz-pair with the declared time moved to 3:12: the HUD clock follows the boss take's 3:10
    p0 = 70 - (bar(80, 1) - bar(80))
    e.S(Custom(bar(80), bar(84), lambda f, s, ed: full(pair, p0 + f - s.f0)))
    white_n = 58 - p0                         # the take's first 9 frames (#49-57) are the two still in normal colours

    def white_in(c, f, o, ed):                # full white over those frames, then it clears onto the twin silhouettes
        t = f - o.f0
        k = 1.0 if t < white_n else 1.0 - (t - white_n) / 9
        c *= (1 - k)
        c += 255 * k

    e.O(Fn(bar(80), bar(80) + white_n + 9, white_in))
    e.X(bar(80) + 45 - p0, SFX / 's3k-sfx-9f-paced.wav', 2.6)   # both ability presses, 4 frames before the cut
    CATCHF = bar(80) + 125 - p0
    e.X(CATCHF, SFX / 's3k-sfx-4a-paced.wav', 2.1)       # ROM Grab on the catch frame; louder than the cold open's: the music is louder here
    tag_m, tag_t = pill('HYPER MICA', ROSE, 56), pill('SOLAR TALON', (255, 146, 36), 56, fg=NAVY)

    def pair_tags(c, f, o, ed):
        i = p0 + f - bar(80)
        t, out = f - o.f0, o.f1 - f
        for k, (im, key) in enumerate(((tag_m, ''), (tag_t, 'sk_'))):
            u = (t - k * (bar(81, 1) - bar(81))) / 9
            if u <= 0:
                continue
            x, y = subject(pair, i, key, 6)
            sc = 0.7 + 0.3 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, (x + 24) * 6 + (im.shape[1] - im2.shape[1]) / 2, (y - 2) * 6 - im2.shape[0] / 2, clamp(u * 2) * clamp(out / 8))

    e.O(Fn(bar(81), bar(83), pair_tags))
    note(80, 84, 'HERO: THE PAIR', 'S3K Launch Base 1, both pads: MICA and TALON transform side by side and snap open together as Hyper MICA and Solar TALON; TALON hops, catches her and carries her up past the towers',
         'Two heroes, both powered, in one frame: Prism Gilt colours below, flame wings and embers above',
         'the cut is a white flash that clears onto the twin silhouettes; both snap open ON beat 2 of bar 80; ROM grab on the catch (beat 4.6); name tags pop a beat apart on bar 81; the towers fall away under them',
         [(pair, 62), (pair, 72), (pair, 127), (pair, 220), (pair, 330), (pair, 388)])

    # ================= END CARD, bars 84-88, fades with the music =================================
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    # gentle vignette: bright behind the lock-up, easing darker toward the corners and the small type below
    vig = (1.0 - 0.60 * np.clip(np.hypot((xs - W / 2) / (W * 0.62), (ys - H * 0.33) / (H * 0.42)), 0, 1) ** 1.4)[..., None]
    PAIR_END = p0 + (bar(84) - bar(80))       # the pair take simply plays on behind the card

    def endcard(f, s, ed):
        k = PAIR_END + (f - s.f0)
        if k > 620:                           # they reach the top of the level near #580: ping-pong the hover
            j = (k - 620) % 120
            k = 620 - (j if j < 60 else 120 - j)
        bg = clip(pair).frame(k)
        c = blurred(bg.crop((114, 4, 320, 120)), ed, radius=1.8, dim=0.80, zoom=1.0) * vig   # columns right of the HUD: sky, towers, the pair
        t = f - s.f0
        h, size = 230, 170
        w = lockup_width(h, size)
        y = H * 0.25
        x = (W - w) / 2 + (1 - ease_out(clamp(t / 16))) * W
        paste(c, card_band(w, h), x, y)
        draw_lockup(c, x, y, h, t, size, beat=10)
        lines = [('An example character mod for OpenGGF', 'sub', 62, WHITE), ('github.com/OpenGGF/OpenGGF', 'title_it', 66, YELLOW)]
        yy = y + h + 64
        for k, (s_, role, sz, col) in enumerate(lines):
            im = text(s_, role, sz, col, stroke=6, sfill=NAVY, shadow=6, scol=(0, 0, 30, 235))
            paste(c, im, (W - im.shape[1]) / 2, yy, clamp((t - 44 - 14 * k) / 10))
            yy += im.shape[0] + 26
        disc = text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body', 34, WHITE, stroke=4, sfill=NAVY, shadow=3, scol=(0, 0, 30, 235))
        paste(c, disc, (W - disc.shape[1]) / 2, H - 112, clamp((t - 80) / 10))
        return c

    end_f = bar(88) + 36
    e.S(Custom(bar(84), end_f, endcard, trans='iris', tdur=24))
    e.X(bar(84), SFX / 's3k-sfx-b3-paced.wav', 1.6)
    e.O(Fade(bar(87), bar(88) + 6))
    e.O(Fn(bar(88) + 6, 10 ** 6, lambda c, f, o, ed: c.__imul__(0)))
    note(84, 88, 'END CARD', 'Lock-up, "An example character mod for OpenGGF", github.com/OpenGGF/OpenGGF, disclaimer, over the pair shot playing on in soft focus (sky and towers; HUD cropped out)',
         '', 'gold iris + Big Ring on bar 84; music fades bars 85-88; picture fades to black over bar 87', [(pair, 430)])
    e.total = end_f
    K.update({k: v for k, v in locals().items() if isinstance(v, (int, float, str))})
    return e.total


# ---------------------------------------------------------------------- layouts we needed

def stacked_tracked(e, f, strips, labels, zoom=1.35, window=ACT, divider=YEL2):
    """Two full-width strips, each tracking its player, sliding in from the left on its own start frame; label
    pills (text, bg, fg) sit bottom-right, away from any HUD."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    n = len(strips)
    gap = 12
    sh = (e.H - (n - 1) * gap) // n
    for k, (t0, name, src) in enumerate(strips):
        if f < t0:
            continue
        img = tracked(name, src + f - t0, e.W, sh, zoom, window=window)
        x = int(round(-(1 - ease_out((f - t0) / 16)) * e.W))
        y = k * (sh + gap)
        vis = e.W + x
        if vis > 0:
            c[y:y + sh, :vis] = img[:, -x:] if x < 0 else img
            if k:
                c[y - gap:y, :vis] = np.array(divider, np.float32)
        lab, bg, fg = labels[k]
        p = chip(lab, size=50, fg=fg, bg=bg)
        paste(c, p, e.W - p.shape[1] - 40 + x, y + sh - p.shape[0] - 24, clamp((f - t0 - 8) / 8))
    return c


def pair_3x(e, f, panes):
    """Two whole native screens side by side at exactly 3x, popping in on their beats over the stripes: the
    "same moment" pair where a slice would crop the native text. 310x174: HUD whole, lives icon out."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    for k, (t0, name, src, label) in enumerate(panes):
        if f < t0:
            continue
        im = clip(name).frame(src + f - t0).crop((5, 0, 315, 174))
        pw, ph = 930, 522
        x, y = 15 + k * 960, (e.H - ph) / 2 - 40
        pop_panel(c, im.resize((pw, ph), Image.NEAREST), x, y, f, t0, None, 5, YEL2)
        p = chip(label)
        paste(c, p, x + pw / 2 - p.shape[1] / 2, y + ph + 30, clamp((f - t0 - 8) / 8))
    return c


# ============================================================================ the vertical cut (9:16)
# Same sound, same cut points, same captures as the 16:9 film; every picture is recomposed for 1080x1920:
#   - action:       a portrait window, the full native height (8.571x), 126 px wide, never left of x 116, so the
#                   HUD and the lives icon are out whole; it follows the hero only when the game's camera does not
#   - comparisons:  stacked bands (rows 58-194 of each source: no HUD, no lives icon)
#   - whole screens (titles, results, ending): the whole native width on the picture's own flat ground
SV = 1920 / 224
PW = 1080 / SV


def pv(name, i, key='', lead=18, lo=116.0, sm=10, x0=None):
    im = clip(name).frame(i)
    if x0 is None:
        x, _ = subject(name, i, key, sm)
        x0 = clamp(x - PW / 2 + lead, lo, im.width - PW)
        xn, _ = subject(name, i, key, 0)       # where she is on this frame: never closer than 22 px to either edge
        x0 = clamp(clamp(x0, xn - (PW - 22), xn - 22), lo, im.width - PW)
    return arr(resample(im, x0, 0, PW, 224, 1080, 1920))


def close_v(name, i, cx, y0=58, vh=None):
    """A closer portrait window that starts below the HUD rows: native rows y0-224 (93 px wide at y0 = 58)."""
    vh = vh or 224 - y0
    vw = vh * 1080 / 1920
    im = clip(name).frame(i)
    return arr(resample(im, clamp(cx - vw / 2, 0, im.width - vw), y0, vw, vh, 1080, 1920))


def band(name, i, ow, oh, key='', zoom=1.65, dy=0, sm=10):
    return tracked(name, i, ow, oh, zoom, key=key, dy=dy, window=ACT, sm=sm)


def band_right(name, i, ow, oh, key='', dy=0, vw=150.0):
    """A band that may use every row (a hero near the top of the screen): it never starts left of x 111, so the
    HUD (x 16-110) and the lives display (x 17-62) are out whole. The hero sits a third of the way across, with
    the room ahead; the window follows her vertically."""
    vh = vw * oh / ow
    x, y = subject(name, i, key)
    im = clip(name).frame(i)
    return arr(resample(im, clamp(x - 0.36 * vw, 111, im.width - vw), clamp(y + dy - vh / 2, 0, 224 - vh), vw, vh, ow, oh))


def bands_v(e, f, panes, divider=YEL2, gap=14, top=False):
    """Stacked full-width bands, each sliding in from the left on its own start frame.
    panes = (t0, fn(local_frame, ow, oh), label | (label, bg, fg) | None)."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    n = len(panes)
    sh = (e.H - (n - 1) * gap) // n
    for k, (t0, fn, label) in enumerate(panes):
        if f < t0:
            continue
        img = fn(f - t0, e.W, sh)
        x = int(round(-(1 - ease_out(clamp((f - t0) / 16))) * e.W))
        y = k * (sh + gap)
        vis = e.W + x
        if vis > 0:
            c[y:y + sh, :vis] = img[:, -x:] if x < 0 else img
            if k:
                c[y - gap:y, :vis] = np.array(divider, np.float32)
        if label:
            p = chip(label) if isinstance(label, str) else chip(label[0], size=50, fg=label[2], bg=label[1])
            paste(c, p, 40 + x, y + 24 if top else y + sh - p.shape[0] - 24, clamp((f - t0 - 8) / 8))
    return c


def card_block(w, h, tab=70, strip=28):
    """The S2 card as a tall block: card blue, serrated red tab down the left edge, yellow strip along the bottom."""
    a = np.zeros((h, w, 4), np.float32)
    a[..., :3] = BLUE2
    a[..., 3] = 255
    for yy in range(h):
        a[yy, :tab + (9 if (yy // 18) % 2 else 0), :3] = RED2
    a[h - strip:, :, :3] = YEL2
    return a


class CardHeaderV(Overlay):
    """The chapter header for 9:16: the band holds the word; the sub-line follows underneath."""

    def __init__(self, f0, f1, word, sub=None, y=None, h=150):
        super().__init__(f0, f1)
        self.word, self.sub, self.y, self.h = word, sub, y, h

    def draw(self, c, f, e):
        h = self.h
        y = self.y if self.y is not None else e.H - h - 330
        word = text(self.word, 'title', 104, WHITE, stroke=7, sfill=NAVY, shadow=8, scol=(0, 0, 30, 230), tracking=3)
        sub = text(self.sub, 'title_it', 50, YELLOW, stroke=5, sfill=NAVY, shadow=5) if self.sub else None
        w = min(e.W - 60, word.shape[1] + 240)
        band_ = card_band(w, h, word)
        t, out = f - self.f0, self.f1 - f
        u_in, u_out = clamp(t / 14), clamp(out / 8)
        x = 30 + (1 - ease_out(u_in)) * (e.W + 40) - (1 - u_out) * (e.W + 80)
        paste(c, band_, x, y)
        tab = np.zeros((h + 40, max(40, h // 3), 4), np.float32)
        tab[..., :3] = RED2
        tab[..., 3] = 255
        ty = y - 20 - (1 - ease_out(clamp(t / 10))) * (y + h + 60) - (1 - u_out) * (h + 200)
        paste(c, tab, 30 - (1 - u_out) * (e.W + 80), ty)
        if sub is not None:
            paste(c, sub, 60 + (1 - ease_out(clamp((t - 4) / 14))) * e.W - (1 - u_out) * e.W, y + h + 18)


def build_v(e):
    W, H = e.W, e.H
    k = K
    hyp, mgz, syz, gil, sol, boss, pair = k['hyp'], k['mgz'], k['syz'], k['gil'], k['sol'], k['boss'], k['pair']
    half = lambda n: bar(n) - (bar(n) - bar(n - 1)) // 2
    beat = bar(12, 1) - bar(12)

    def ground(f):
        return stripes(e, f, c0=NAVYD, c1=(14, 30, 92))

    def whole(c, im, rows, y, rules=False):
        """Paste native rows [a, b) of a frame at full canvas width (3.375x), top at y; returns its height."""
        a, b = rows
        ph = round((b - a) * W / 320)
        c[y:y + ph] = arr(resample(im, 0, a, 320, b - a, W, ph))
        if rules:
            c[y - 14:y] = np.array(YEL2, np.float32)
            c[y + ph:y + ph + 14] = np.array(YEL2, np.float32)
        return ph

    def on_own_ground(im, rows, y, fade=0):
        fill = np.array(im.getpixel((2, rows[0] + 2)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        ph = whole(c, im, rows, y)
        if fade:                              # the picture's last rows ease into its own ground
            a = np.clip((ph - np.arange(ph)) / fade, 0, 1)[:, None, None]
            c[y:y + ph] = c[y:y + ph] * a + fill * (1 - a)
        return c

    # ================= COLD OPEN ===================================================================
    def rollin(f, s, ed):
        i = 234 + f - s.f0
        if i < 267:
            return np.zeros((H, W, 3), np.float32)
        im = clip('title-s3k').frame(i)
        if i < 296:                           # the smear frames fill the frame: full-height centre window
            return arr(resample(im, 160 - PW / 2, 0, PW, 224, W, H))
        # the title whole (columns 28-292 hold the ring, the logo and its ribbon; menu and copyright rows out),
        # at 4.09x on its own sky; the clouds beside the logo ease into that sky over their last seven rows
        fill = np.array(im.getpixel((2, 2)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        ph = round(188 * W / 264)
        pic = arr(resample(im, 28, 0, 264, 188, W, ph))
        a = np.clip((ph - np.arange(ph)) / 28.0, 0, 1)[:, None, None] * np.ones((1, W, 1), np.float32)
        a[:, 131:965] = 1.0                   # the logo's own columns stay whole; only the clouds beside it ease out
        c[540:540 + ph] = pic * a + fill * (1 - a)
        return c

    e.S(Custom(0, bar(2), rollin))

    lbz0 = k['lbz0']

    DUO_CUT = bar(3, 2)

    def duo(f, s, ed):                        # one band each, the same size: partners
        # TALON takes off 1.5 s into this run (src 142) and climbs past the HUD rows, out of any band that keeps
        # the HUD out. So the bands play the run up to his take-off, and on beat 3 of bar 3 the picture cuts to
        # the tall frame (native x 112-238, every row, the HUD's last column is x 110) for his flight over MICA.
        n, na = f - s.f0, DUO_CUT - s.f0
        i = 152 + n - na
        if n >= na:
            return pv('d-lbz1-team', i, x0=112.0)
        return bands_v(ed, f, [(s.f0 - 100, lambda lf, ow, oh: band('d-lbz1-team', i, ow, oh), None),
                               (s.f0 - 100, lambda lf, ow, oh: band('d-lbz1-team', i, ow, oh, key='sk_'), None)])

    e.S(Custom(bar(2), bar(4), duo))
    sh2 = (H - 14) // 2
    e.O(Txt(bar(2) + 14, DUO_CUT, pill('MICA', JADE, 64), W / 2, sh2 / 2 - 250, enter='pop', leave='fade', centre=True, dur=9, out_dur=6))
    e.O(Txt(bar(2, 1) + 14, DUO_CUT - 8, pill('TALON', SLATE, 64), W / 2, sh2 + 14 + sh2 / 2 - 250, enter='pop', leave='fade', centre=True, dur=9, out_dur=6))

    def carry(f, s, ed):
        i = 30 + f - s.f0
        if i < 58:                            # TALON walks in: a closer two-shot below the HUD rows
            return close_v('d-carry-fly', i, 146)
        return pv('d-carry-fly', i, x0=116.0)  # the catch: cut to the tall frame for the climb

    e.S(Custom(bar(4), bar(8), carry))
    e.O(Shade(bar(5), bar(8) - 6, 'bottom'))
    for n, s_ in enumerate(('TWO ORIGINAL HEROES.', 'THREE CLASSIC GAMES.')):
        e.O(Txt(bar(5) + 6 * n, bar(8) - 6, line(s_, 82), W / 2, H - 380 + 110 * n, enter='up', leave='fade', centre=True, dur=12))

    frag0 = k['frag0']
    e.S(Custom(bar(8), bar(10), lambda f, s, ed: pv(hyp, frag0 + f - s.f0)))
    e.O(Flash(bar(9), 8, 0.5))

    # ================= TITLE DROP ==================================================================
    s2_0 = k['s2_0']
    S2Y = 500
    CARD_Y = S2Y + round((181 - 26) * W / 320)        # the card starts on the native '1 PLAYER' row
    for LS in range(340, 150, -10):
        m_, a_, t_ = lockup_words(LS)
        if max(m_.shape[1], a_.shape[1] + LS // 5 + t_.shape[1]) <= 900:
            break

    def stacked_lockup(c, x, y, t, size, bt_):
        mica, amp, talon = lockup_words(size)
        lh = int(mica.shape[0] * 0.80)
        for n, (im, px, py) in enumerate(((mica, x, y), (amp, x, y + lh), (talon, x + amp.shape[1] + size // 5, y + lh))):
            u = (t - 6 - n * bt_) / 7
            if u <= 0:
                continue
            sc = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, px + (im.shape[1] - im2.shape[1]) / 2, py + (im.shape[0] - im2.shape[0]) / 2, clamp(u * 2))

    def s2_title(f, s, ed):
        im = clip('title-s2').frame(s2_0 + f - s.f0)
        c = on_own_ground(im, (26, 206), S2Y)         # black before the flash, the title's sky after it
        t = f - bar(12)
        if t >= 0:                                    # the card rides in under the title's own flash
            x = (1 - ease_out(clamp(t / 14))) * (W + 60)
            paste(c, card_block(W, H - CARD_Y), x, CARD_Y)
            lock_h = int(lockup_words(LS)[0].shape[0] * 1.80)
            stacked_lockup(c, x + 130, CARD_Y + (H - CARD_Y - 28 - lock_h) / 2, t - 6, LS, beat)
        return c

    e.S(Custom(bar(10), bar(16), s2_title))
    e.O(Flash(bar(12), 16, 0.9))

    # ================= MICA ========================================================================
    e.S(Custom(bar(16), bar(18), lambda f, s, ed: pv(mgz, f - s.f0), trans='wipe', tdur=16))
    e.O(CardHeaderV(bar(16) + 4, bar(17) - 22, 'MICA', sub='HOMING STRIKE'))
    mgz_hits = [65, 82, 104]
    chain_imgs = [text(s_, 'title', 190, YELLOW, stroke=10, sfill=NAVY, shadow=11) for s_ in ('1', '2', '3')]
    for n, h in enumerate(mgz_hits):
        end = bar(16) + mgz_hits[n + 1] if n < 2 else bar(18) - 6
        e.O(Txt(bar(16) + h, end, chain_imgs[n], W * 0.80, H * 0.14, enter='pop', leave='pop', centre=True, dur=8))
    e.O(Txt(bar(16) + mgz_hits[2] + 4, bar(18) - 6, pill('CHAIN', JADE, 64), W * 0.80, H * 0.14 + 170, enter='up', centre=True))

    tri = [('d-ghz2-buzz', 60, 'SONIC 1'), ('d-arz1-whisp', 138, 'SONIC 2'), ('aiz-hero', 70, 'SONIC 3 & K')]

    def three(f, s, ed):
        return bands_v(ed, f, [(bar(18 + n / 2), (lambda nm, s0: lambda lf, ow, oh: band_right(nm, s0 + lf, ow, oh))(nm, hit - 40), lab)
                               for n, (nm, hit, lab) in enumerate(tri)])

    e.S(Custom(bar(18), bar(22), three, trans='push', tdur=14, tdir='left'))

    scz0 = k['scz0']
    e.S(Custom(bar(22), bar(26), lambda f, s, ed: pv('h-scz-a', scz0 + f - s.f0, lead=0, sm=16)))
    e.O(Txt(bar(22) + 358 - scz0 + 2, bar(25), pill('CHAIN  x2', JADE, 64), W * 0.5, H * 0.12, enter='pop', leave='fade', centre=True, dur=8))
    e.O(Txt(bar(24, 2), bar(26) - 6, pill('TALON FLIES THE TORNADO', SLATE, 52), W / 2, H * 0.90, enter='up', leave='fade', centre=True))

    cnz0 = k['cnz0']
    e.S(Custom(bar(26), bar(28), lambda f, s, ed: pv('d-cnz2-team', cnz0 + f - s.f0, x0=116.0)))

    # ================= TALON =======================================================================
    syz0 = k['syz0']
    e.S(Custom(bar(28), bar(32), lambda f, s, ed: pv(syz, syz0 + f - s.f0), trans='wipe', tdur=16))
    e.O(CardHeaderV(bar(28) + 4, bar(29) - 6, 'TALON', sub='FLIGHT  CARRY  DIVEBOMB'))
    e.O(Txt(bar(30), bar(32) - 6, pill('IN SONIC 1, TOO', SLATE, 60), W * 0.5, H - 250, enter='up', leave='fade', centre=True))

    def lives(c, f, o, ed):                   # the lives display, which the portrait window drops: whole, as an inset
        im = clip(syz).frame(syz0 + f - bar(28)).crop((8, 196, 80, 222)).resize((504, 182), Image.NEAREST)
        pop_panel(c, im, (W - 514) / 2, H - 530, f, o.f0, None, 6, YEL2)

    e.O(Fn(bar(30), bar(32) - 6, lives))

    def talon3(f, s, ed):
        return bands_v(ed, f, [
            (bar(32), lambda lf, ow, oh: band_right('d-cpz-talon', 22 + lf, ow, oh), 'FLIGHT'),
            (bar(32, 2), lambda lf, ow, oh: band_right('d-carry-fly', 60 + lf, ow, oh, key='sk_', dy=14), 'CARRY'),
            (bar(33), lambda lf, ow, oh: band_right('d-aiz-talon-dive', 80 + lf, ow, oh), 'DIVEBOMB')])

    e.S(Custom(bar(32), bar(36), talon3, trans='push', tdur=14, tdir='left'))

    # ================= EVERY SCREEN ================================================================
    med0 = k['med0']

    def lockstep(f, s, ed):
        i = med0 + f - s.f0
        mx, my = subject('f-cpz-medley', i)
        sx, sy = subject('f-cpz-medley', i, 'sk_')
        cx = (mx + sx) / 2 if abs(mx - sx) < 110 else mx

        def side(name):
            # rows 52-224: under the HUD; never left of x 64: the lives display is out
            return lambda lf, ow, oh: arr(resample(clip(name).frame(i), clamp(cx - 86 * ow / oh, 64, 320 - 172 * ow / oh), 52, 172 * ow / oh, 172, ow, oh))
        return bands_v(ed, f, [(s.f0 - 100, side('f-stock-cpz-medley'), 'ORIGINAL'),
                               (s.f0 - 100, side('f-cpz-medley'), ('MICA & TALON', JADE, WHITE))], top=True)

    e.S(Custom(bar(36), bar(40), lockstep, trans='wipe', tdur=16))
    e.O(CardHeaderV(bar(36) + 4, bar(37) + 30, 'EVERY SCREEN', sub='REDRAWN'))
    e.O(Shade(bar(38), bar(40) - 6, 'bottom'))
    for n, s_ in enumerate(('SAME INPUTS. SAME PHYSICS.', 'EVERY FRAME.')):
        e.O(Txt(bar(38) + 6 * n, bar(40) - 6, line(s_, 72), W / 2, H - 330 + 100 * n, enter='up', leave='fade', centre=True, dur=12))

    def titles3(f, s, ed):                    # three whole title screens, one per band
        return bands_v(ed, f, [
            (bar(40), lambda lf, ow, oh: view(clip('title-s1').frame(392 + lf), 160, 72, 224 / 147, ow, oh, 0, 147), 'SONIC 1'),
            (bar(40, 3.5), lambda lf, ow, oh: view(clip('title-s2').frame(840 + lf), 160, 116, 224 / 180, ow, oh, 26, 206), 'SONIC 2'),
            # The whole S3K title needs the full width, where its stock Tornado fly-by is in view (src 412-505 on the
            # left, 696-775 on the right). This band therefore plays src 506-695, while the plane is behind the emblem.
            (bar(41, 3) + 2, lambda lf, ow, oh: view(clip('title-s3k').frame(506 + lf), 160, 93, 224 / 186, ow, oh, 0, 186), 'SONIC 3 & K')], top=True)

    e.S(Custom(bar(40), bar(44), titles3, trans='push', tdur=14, tdir='left'))

    def signs(f, s, ed):                      # two whole screens, stacked
        c = ground(f)
        for n, (t0, name, src, label) in enumerate(((s.f0, 'd-ghz-clear', 135, 'SONIC 1'), (bar(44, 1), 'd-ehz-clear', 262, 'SONIC 2'))):
            if f < t0:
                continue
            im = clip(name).frame(src + f - t0)
            ph = round(179 * W / 320)
            y = 190 + n * (ph + 190)
            x = int(round(-(1 - ease_out(clamp((f - t0) / 12))) * W))
            pic = arr(resample(im, 0, 0, 320, 179, W, ph))
            vis = W + x
            if vis > 0:
                c[y - 14:y, :vis] = np.array(YEL2, np.float32)
                c[y:y + ph, :vis] = pic[:, -x:] if x < 0 else pic
                c[y + ph:y + ph + 14, :vis] = np.array(YEL2, np.float32)
            p = chip(label)
            paste(c, p, (W - p.shape[1]) / 2 + x, y + ph + 40, clamp((f - t0 - 8) / 8))
        return c

    e.S(Custom(bar(44), bar(46), signs))

    def tally(f, s, ed):                      # the whole native screen: nothing of the results lettering is cropped
        c = ground(f)
        ph = whole(c, clip('d-ehz-clear').frame(470 + f - s.f0), (0, 224), 520, rules=True)
        p = chip('SONIC 2')
        paste(c, p, (W - p.shape[1]) / 2, 520 + ph + 54)
        return c

    e.S(Custom(bar(46), bar(48), tally))

    def stages(f, s, ed):
        return bands_v(ed, f, [
            (bar(48), lambda lf, ow, oh: view(clip('f-ghz-ss').frame(900 + lf), 160, 112, 224 / 187, ow, oh, 0, 224), 'SONIC 1'),
            (bar(48, 2), lambda lf, ow, oh: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.5, ow, oh, 44, 224), 'SONIC 2'),   # its 256-px picture, side borders out
            (bar(49), lambda lf, ow, oh: view(clip('q-blue-c').frame(430 + lf), 160, 140, 1.2, ow, oh, 34, 224), 'SONIC 3 & K')])

    e.S(Custom(bar(48), bar(52), stages, trans='push', tdur=14, tdir='left'))

    def screens(f, s, ed):                    # four wide strips, a beat apart
        c = ground(f)
        t0 = s.f0
        cells = [(clip('continue'), 60, 'CONTINUE', (160, 104, 1.0)), (clip('data-select'), 405, 'DATA SELECT', (201, 116, 2.75)),
                 (clip('halfpipe-run'), 1010, 'SPECIAL STAGE HUD', (160, 56, 1.25)), (clip('d-cpz-talon'), 60, 'LIVES', (62, 200, 4.6))]
        pw_, ph_ = 956, 370
        for n, (cl, src, label, (cx, cy, z)) in enumerate(cells):
            tn = t0 + n * beat
            if f < tn:
                continue
            img = game_view(cl.frame(src + f - tn), cx, cy, z, pw_, ph_)
            pop_panel(c, img, (W - pw_) / 2 - 5, 52 + n * (ph_ + 96), f, tn, label, 5, YEL2)
        return c

    e.S(Custom(bar(52), bar(55), screens, trans='push', tdur=14, tdir='left'))

    side0, side1, pose1, end_src, end_land = k['side0'], k['side1'], k['pose1'], k['end_src'], k['end_land']
    def window_on_ground(im, box, y):       # a native window at full canvas width, on the picture's own flat ground
        x0, y0, x1, y1 = box
        fill = np.array(im.getpixel((x1 - 3, y1 - 3)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        ph = round((y1 - y0) * W / (x1 - x0))
        c[y:y + ph] = arr(resample(im, x0, y0, x1 - x0, y1 - y0, W, ph))
        return c

    e.S(Custom(side0, side1, lambda f, s, ed: window_on_ground(clip('ending').frame(2760 - (side1 - side0) + f - s.f0), (0, 60, 200, 200), 560)))
    e.S(Custom(side1, pose1, lambda f, s, ed: window_on_ground(clip('ending').frame(end_src + f - s.f0), (60, 12, 280, 196), 380)))
    e.O(Txt(side1 + end_land - end_src + 4, pose1 - 4, pill('ENDINGS, TOO', JADE, 68), W / 2, 1480, enter='pop', leave='fade', centre=True, dur=10))

    # ================= POWERED UP ==================================================================
    g0, gstart = k['g0'], k['gstart']
    e.S(Custom(gstart, bar(64), lambda f, s, ed: pv(gil, g0 + f - s.f0)))
    e.O(Flash(bar(60), 10, 0.45))
    e.O(CardHeaderV(bar(60) + 30, bar(61) + 50, 'POWERED UP', sub='50 RINGS  MID-ACT'))
    e.O(Txt(bar(62), bar(64) - 6, pill('GILDED MICA', GOLD2, 64, fg=NAVY), W / 2, H * 0.88, enter='up', leave='fade', centre=True))

    def trails(f, s, ed):
        return bands_v(ed, f, [(bar(64), lambda lf, ow, oh: band_right('d-aiz-normal', 15 + lf, ow, oh, vw=170), ('NORMAL: JADE TRAIL', JADE, WHITE)),
                               (bar(65), lambda lf, ow, oh: band_right('gilded-aiz', 54 + lf, ow, oh, vw=170), ('GILDED: GOLD TRAIL', GOLD2, NAVY))])

    e.S(Custom(bar(64), bar(68) - (bar(68) - bar(67)) // 2, trails, trans='push', tdur=12, tdir='left'))

    s0 = k['s0']
    e.S(Custom(half(68), bar(72), lambda f, s, ed: pv(sol, s0 + f - s.f0, x0=116.0)))
    e.O(Flash(bar(68), 10, 0.45))
    e.O(Txt(bar(69), bar(72) - 6, pill('SOLAR TALON', (255, 146, 36), 64, fg=NAVY), W / 2, H * 0.88, enter='up', leave='fade', centre=True))

    pw3 = [('f-slz1-gilded', 74, 'SONIC 1'), ('g-mcz1-solar', 94, 'SONIC 2'), ('d-aiz-solar-dive', 186, 'SONIC 3 & K')]

    def powered3(f, s, ed):
        return bands_v(ed, f, [(bar(72 + n / 2), (lambda nm, s0_: lambda lf, ow, oh: band_right(nm, s0_ + lf, ow, oh))(nm, ev - 40), lab)
                               for n, (nm, ev, lab) in enumerate(pw3)])

    e.S(Custom(bar(72), half(76), powered3, trans='push', tdur=14, tdir='left'))

    h0 = k['h0']
    e.S(Custom(half(76), bar(78), lambda f, s, ed: pv(hyp, h0 + f - s.f0)))
    e.O(Flash(bar(76), 10, 0.5))
    e.O(Txt(bar(76) + 30, bar(78) - 6, pill('HYPER MICA', ROSE, 64), W / 2, H * 0.88, enter='up', leave='fade', centre=True))

    # ---- the boss: a fixed window, x 140-266. From the hit the ONE HIT. card covers native x >= 199 (she is at
    # x >= 202 once the form has ended); its edge is upright here so that it clears the machine (x <= 197).
    b0 = k['b0']
    BX0, CX = 140.0, 524
    e.S(Custom(bar(78), bar(80), lambda f, s, ed: arr(resample(clip(boss).frame(b0 + f - s.f0), BX0, 0, PW, 224, W, H))))
    e.O(Flash(bar(79), 10, 0.55))
    for OS in range(300, 120, -10):
        one_im = text('ONE', 'title', OS, WHITE, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
        hit_im = text('HIT.', 'title', OS, YELLOW, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
        if max(one_im.shape[1], hit_im.shape[1]) <= W - CX - 46 - 70:
            break

    def hit_card(c, f, o, ed):
        t = f - o.f0
        off = (1 - ease_out(clamp(t / 7))) * (W - CX + 200)
        x0_ = int(round(CX + off))
        if x0_ < W:
            c[:, x0_:] = np.array(BLUE2, np.float32)
            for yy in range(0, H, 18):
                c[yy:yy + 18, x0_:min(W, x0_ + 46 + (9 if (yy // 18) % 2 else 0))] = np.array(RED2, np.float32)
            c[:, max(0, x0_ - 14):x0_] = np.array(YEL2, np.float32)
        cx = CX + 46 + (W - CX - 46) / 2 + off
        for n, (im, yy) in enumerate(((one_im, H * 0.42), (hit_im, H * 0.42 + one_im.shape[0] * 0.86))):
            u = (t - 5 - n * beat / 2) / 7
            if u <= 0:
                continue
            sc = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, cx - im2.shape[1] / 2, yy - im2.shape[0] / 2, clamp(u * 2))

    e.O(Fn(bar(79), bar(80), hit_card))

    # ---- the pair: a closer two-shot for the twin transformation, then the tall frame from the catch
    p0, white_n = k['p0'], k['white_n']
    CUTV = 128                                # three frames after the catch (#125)

    def pair_v(f, s, ed):
        i = p0 + f - s.f0
        if i < CUTV:
            # They transform in the air, level with the HUD rows, so this window starts at x 111 (the HUD ends at
            # x 110, so it is out whole) and takes rows 0-188: native x 111-217, the pair a third of the way down
            # with the sky above them, both whole apart from 3 px of TALON's wingtip.
            return close_v(pair, i, 111 + 188 * 1080 / 1920 / 2, y0=0, vh=188)
        return pv(pair, i, x0=116.0)

    e.S(Custom(bar(80), bar(84), pair_v))

    def white_in(c, f, o, ed):
        t = f - o.f0
        a = 1.0 if t < white_n else 1.0 - (t - white_n) / 9
        c *= (1 - a)
        c += 255 * a

    e.O(Fn(bar(80), bar(80) + white_n + 9, white_in))
    tag_m, tag_t = pill('HYPER MICA', ROSE, 60), pill('SOLAR TALON', (255, 146, 36), 60, fg=NAVY)

    def pair_tags(c, f, o, ed):
        i = p0 + f - bar(80)
        t, out = f - o.f0, o.f1 - f
        for n, (im, key) in enumerate(((tag_m, ''), (tag_t, 'sk_'))):
            u = (t - n * beat) / 9
            if u <= 0:
                continue
            x, y = subject(pair, i, key, 6)
            sc = 0.7 + 0.3 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, (x + 22 - 116) * SV + (im.shape[1] - im2.shape[1]) / 2, (y - 2) * SV - im2.shape[0] / 2, clamp(u * 2) * clamp(out / 8))

    e.O(Fn(bar(81), bar(83), pair_tags))

    # ================= END CARD ====================================================================
    PAIR_END = k['PAIR_END']
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = (1.0 - 0.55 * np.clip(np.hypot((xs - W / 2) / (W * 0.80), (ys - H * 0.36) / (H * 0.52)), 0, 1) ** 1.4)[..., None]

    def endcard(f, s, ed):
        kf = PAIR_END + (f - s.f0)
        if kf > 620:
            j = (kf - 620) % 120
            kf = 620 - (j if j < 60 else 120 - j)
        c = blurred(clip(pair).frame(kf), ed, radius=1.8, dim=0.80, cx=116 + PW / 2, cy=112, zoom=1.0) * vig
        t = f - s.f0
        x = (1 - ease_out(clamp(t / 16))) * W
        bh = int(lockup_words(LS)[0].shape[0] * 1.80) + 150
        y = int(H * 0.20)
        paste(c, card_block(W, bh), x, y)
        stacked_lockup(c, x + 130, y + 70, t, LS, 10)
        yy = y + bh + 90
        for n, (s_, role, sz, col) in enumerate((('An example character mod', 'sub', 66, WHITE), ('for OpenGGF', 'sub', 66, WHITE),
                                                 ('github.com/OpenGGF/OpenGGF', 'title_it', 68, YELLOW))):
            im = text(s_, role, sz, col, stroke=6, sfill=NAVY, shadow=6, scol=(0, 0, 30, 235))
            paste(c, im, (W - im.shape[1]) / 2, yy, clamp((t - 44 - 10 * n) / 10))
            yy += im.shape[0] + (18 if n == 0 else 44)
        for n, s_ in enumerate(('Fan-made and free. Not affiliated with SEGA.', 'Requires your own ROM.')):
            im = text(s_, 'body', 38, WHITE, stroke=4, sfill=NAVY, shadow=3, scol=(0, 0, 30, 235))
            paste(c, im, (W - im.shape[1]) / 2, H - 260 + 56 * n, clamp((t - 80) / 10))
        return c

    e.S(Custom(bar(84), k['end_f'], endcard, trans='iris', tdur=24))
    e.O(Fade(bar(87), bar(88) + 6))
    e.O(Fn(bar(88) + 6, 10 ** 6, lambda c, f, o, ed: c.__imul__(0)))
