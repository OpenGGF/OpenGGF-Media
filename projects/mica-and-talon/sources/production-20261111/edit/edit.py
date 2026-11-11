#!/usr/bin/env python3
"""MICA & TALON - production promo (2026-11-11).

Audience: Sonic fans first, would-be modders second.
Form/evidence: gameplay showcase; every gameplay claim is native OpenGGF footage from GameplayCaptureTool
  or the retained PromoCapture hosts (positioned starts/declared rings+timer, listed in the README).
Promise: "Two original heroes, at home in all three classic Sonic games."
Cleverest true thing: not palette swaps - every surface redrawn in each game's own style and driven by the
  game's own logic. Proof = "same moment, three games" triptychs and pairs, never a static inventory.
Selling points (each a moving proof): homing chain in S3K + the same move in S1/S2 (native chain score);
  TALON flight, carry and divebomb; titles/signposts/results/special stages side by side; Gilded MICA and
  Solar TALON at 70 rings mid-act.
Hero moment: Gilded MICA's transformation landing on the post-breakdown downbeat, into the Instagib run;
  a fragment of the Instagib flight is in the cold open.
Sound: owner-supplied "RUN INTO THE SUNSHINE (Chiptune Remix)", 172.218 BPM, bar 0 at 0.178 s in the source.
  Bed = source bars 8-35 + bars 76-end (one bar-line splice, 12 ms equal-power, see tools/build_bed.py),
  so output bar n = source bar n+8 (n<28) or n+48 (n>=28). Sparse ROM stingers, rendered --paced, on the
  event frames from state.csv.
Palette: S2 title-card blue 2449DB, red FF0000, yellow FFFF00 (sampled from the native EHZ2 card), MICA jade.
Title face: Sonic 2 title-card glyphs (BitmapFont, native palette indices) on the card's own blue band;
  Fira Sans Compressed Heavy only for lines the game cannot supply ("&", URL, disclaimer).
Treatment: Slay the Robotnik beat grid + Putt-Putt's S2 title-card bands. Signature move: the banded wipe.
End card: logo, one line, URL, disclaimer over a blurred, darkened still. Fade to black on the final hit.
Rejected: a feature grid as the whole of chapter 3 (inventory); a text-led cold open (the S3K roll-in is
  stronger); slowing the native roll-in to fill the build (alters native timing).
"""
import csv
import os
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-3c245e9e'))
T = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools/media'))
from promo_kit import *  # noqa: E402,F401

V = os.environ.get('MT_VERTICAL') == '1'
EDIT = dict(bpm=172.218, first=0.0, fps=60, size=(1080, 1920) if V else (1920, 1080),
            out=T / 'out' / ('master-9x16.mp4' if V else 'master-16x9.mp4'),
            work=T / 'work' / ('build-v' if V else 'build-h'))
CAP = T / 'captures'
SFX = T / 'sfx'

BLUE2 = (36, 73, 219)
RED2 = (255, 0, 0)
YEL2 = (255, 255, 0)
JADE = (0, 146, 109)
NAVYD = (8, 16, 56)

S2FONT = BitmapFont(T / 'edit/s2-title-font.txt', space=8)
S2SHADES = {'1': (0, 0, 0), '6': WHITE, '7': (182, 182, 182), '8': (146, 146, 146)}


@lru_cache(None)
def native(word, scale=6):
    return S2FONT.render(word, scale=scale, fill=WHITE, shades=S2SHADES, outline=None, drop=None)


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
    else:  # window narrower than the view: centre on the window, stay inside the frame
        y0 = clamp((ylo + yhi) / 2 - vh / 2, 0, img.height - vh)
    return arr(resample(img, x0, y0, vw, vh, ow, oh))


# S3K/S2/S1 HUD occupies y < 58; the lives icon y > 194. Action close-ups stay between them.
ACT = (58, 194)


def tracked(name, i, ow, oh, zoom=1.4, key='', dy=0, window=ACT, punch=1.0, pad=None, xlo=0):
    if V and window is ACT and not xlo and not pad:
        # Portrait views are 126/zoom game px wide: keep the HUD and lives (x<116) out horizontally instead.
        window, xlo = (0, 224), 116
    im = clip(name).frame(i)
    x, y = subject(name, i, key)
    if pad:
        canvas = Image.new('RGB', (im.width + 2 * pad, im.height), (8, 16, 56))
        canvas.paste(im, (pad, 0))
        im, x = canvas, x + pad
    if xlo:  # needs vw <= width - xlo, i.e. zoom >= ~2 at 16:9, or view() clamps it back
        vw = min(im.width, im.height / (zoom * punch) * ow / oh)
        assert vw <= im.width - xlo, 'xlo infeasible at this zoom'
        x = max(x, xlo + vw / 2)
    return view(im, x, y + dy, zoom * punch, ow, oh, *window)


def portrait_fit(img, fill, zoom=1.0, ow=None, oh=None):
    """9:16 view of a whole 320-wide native screen: fit its width and extend top/bottom with the screen's own
    flat edge colour (S2 title sky/menu blue, ending black), so nothing is cropped and nothing is letterboxed."""
    ow, oh = ow or 1080, oh or 1920
    ch = round(img.width * oh / ow)
    canvas = Image.new('RGB', (img.width, ch), fill)
    canvas.paste(img, (0, (ch - img.height) // 2))
    return arr(game_view(canvas, None, None, zoom, ow, oh))


# ------------------------------------------------------------------------------- graphics

def card_band(w, h, word_img=None, tab=True, strip=True, sub=None):
    """The S2 title card in miniature: solid card blue, serrated red tab, yellow strip; native letters."""
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
    if sub is not None:
        paste(a[..., :3], sub, a.shape[1] - sub.shape[1] - 40, h - max(10, h // 9) - sub.shape[0] - 10)
    return a


class CardHeader(Overlay):
    """Chapter header, S2 title-card grammar: the red tab drops from the top-left, the blue band and its
    letters slide in from the right, the yellow strip follows; everything leaves left at double speed."""

    def __init__(self, f0, f1, word, sub=None, y=None, h=None):
        super().__init__(f0, f1)
        self.word, self.sub, self.y, self.h = word, sub, y, h

    def draw(self, c, f, e):
        h = self.h or (150 if not V else 170)
        y = self.y if self.y is not None else e.H - h - (40 if not V else 300)
        # Same face as the lock-up: the S2 card glyphs split M and A at display scale (lead review).
        word = text(self.word, 'title', 104 if not V else 96, WHITE, stroke=7, sfill=NAVY, shadow=8,
                    scol=(0, 0, 30, 230), tracking=3)
        sub = text(self.sub, 'title_it', 46, YELLOW, stroke=5, shadow=5) if self.sub else None
        w = min(e.W - 60, word.shape[1] + 260 + (sub.shape[1] + 60 if sub is not None and not V else 0))
        band = card_band(w, h, word, sub=None if V else sub)
        t, out = f - self.f0, self.f1 - f
        u_in, u_out = clamp(t / 14), clamp(out / 8)
        x = 30 + (1 - ease_out(u_in)) * (e.W + 40) - (1 - u_out) * (w + 80)
        paste(c, band, x, y)
        # tab drops first, independent of the band
        tab = np.zeros((h + 40, max(40, h // 3), 4), np.float32)
        tab[..., :3] = RED2
        tab[..., 3] = 255
        ty = y - 20 - (1 - ease_out(clamp(t / 10))) * (y + h + 60) - (1 - u_out) * (h + 200)
        paste(c, tab, 30 - (1 - u_out) * (w + 80), ty)
        if V and sub is not None:
            paste(c, sub, 60 + (1 - ease_out(clamp((t - 4) / 14))) * e.W - (1 - u_out) * e.W, y + h + 16)


@lru_cache(None)
def lockup_words(size):
    """MICA & TALON in the heavy condensed face: white caps, thick dark-navy outline, hard shadow, slight
    tracking, the '&' in yellow. The game's card letters split 'M' into '/\\/\\' at this size (lead review)."""
    st, sh, tr = max(6, size // 14), max(7, size // 12), max(3, size // 40)
    mica = text('MICA', 'title', size, WHITE, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230), tracking=tr)
    amp = text('&', 'title', size, YELLOW, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230))
    talon = text('TALON', 'title', size, WHITE, stroke=st, sfill=NAVY, shadow=sh, scol=(0, 0, 30, 230), tracking=tr)
    return mica, amp, talon


def draw_lockup(c, band_x, band_y, h, t, size):
    """Words staggered onto an S2-card band whose left edge is band_x; returns nothing."""
    mica, amp, talon = lockup_words(size)
    gap = size // 6
    lx = band_x + max(40, h // 3) + 60
    ly = band_y + (h - max(10, h // 9) - mica.shape[0]) / 2 + 2
    paste(c, mica, lx, ly, clamp((t - 6) / 6))
    paste(c, amp, lx + mica.shape[1] + gap, ly, clamp((t - 9) / 6))
    paste(c, talon, lx + mica.shape[1] + gap + amp.shape[1] + gap, ly, clamp((t - 12) / 6))


def lockup_width(h, size):
    mica, amp, talon = lockup_words(size)
    return max(40, h // 3) + 60 + mica.shape[1] + amp.shape[1] + talon.shape[1] + 2 * (size // 6) + 70


def jade_pill(label, size=50):
    return chip(label, size=size, fg=WHITE, bg=JADE)


def strike_marks(e, frames, amp=0.12):
    for f in frames:
        e.punches.append((f, amp))


# ----------------------------------------------------------------------------------- shots

def B(e, n):
    """Output frame of bar n."""
    return e.bf(4 * n)


def build(e):
    b = e.bf
    bar = lambda n: B(e, n)
    W, H = e.W, e.H
    e.bed(T / 'work/bed.wav', 0, 0.75, fade_out=0.0)

    # ---- COLD OPEN, bars 0-3: the S3K roll-in, hard on the first strong downbeat ----------------
    s3k_title_src = 258

    def s3k_title(f, s, ed):
        i = s3k_title_src + f - s.f0
        im = clip('title-s3k').frame(i)
        if i < 268:   # chase the ball out of the logo, pushing out as it grows
            u = clamp((i - s3k_title_src) / (268 - s3k_title_src))
            z = 2.8 + (1.0 - 2.8) * smooth(u)  # SEGA logo (y>=88) stays out of frame
            cx, cy = 200 + (160 - 200) * smooth(u), 30 + (112 - 30) * smooth(u)
        elif i < 300:
            z, cx, cy = 1.0, 160, 112
        else:         # slow push toward MICA through the logo drop and the wink
            # The small stock-art Tornado is on screen at x<~80 for src 412-510 (sprite diff + frame check):
            # by src 408 the view's left edge is x>=96 and stays there (push into MICA's face for the wink).
            u = clamp((i - 300) / 108)
            z, cx, cy = 1.0 + 0.6 * smooth(u), 160 + 36 * smooth(u), 120 - 64 * smooth(u)
            if V:  # portrait: 126 px wide on MICA, left edge >= x112 so the Tornado never enters
                return view(im, 175, 112, 1.0 + 0.15 * smooth(u), W, H)
            return view(im, cx, cy, z, W, H, 0, 188)
        if V:
            return view(im, 175 if i >= 268 else cx + 10, cy if i < 268 else 112, max(z, 1.0), W, H)
        return view(im, cx, cy, z, W, H)

    e.S(Custom(0, bar(3), s3k_title))
    # Instagib fragment on the riser (hero preview)
    e.S(Custom(bar(3), bar(4), lambda f, s, ed: view(clip('gilded').frame(236 + f - s.f0), 160, 90, 1.0, W, H, 0, 180) if not V else tracked('gilded', 236 + f - s.f0, W, H, 1.0)))
    e.O(Flash(bar(4), 18))
    e.X(bar(4), SFX / 's3k-sfx-b3-paced.wav', 1.6)

    # ---- TITLE DROP, bars 4-7: S2 title as it ships, native flash on bar 6 ---------------------
    s2_src = 760 - (bar(6) - bar(4))

    def s2_title(f, s, ed):
        i = s2_src + f - s.f0
        im = clip('title-s2').frame(i)
        z = 1 + 0.3 * (1 - ease_out(clamp((f - s.f0) / 26)))
        if V:  # whole title, width-fit, extended with its own flat sky/menu blue
            return portrait_fit(im, im.getpixel((2, 2)), z)  # own corner colour: black before the fade-in
        return view(im, 160, 124, z, W, H, 34, 214)

    e.S(Custom(bar(4), bar(8), s2_title))

    def lockup(c, f, o, ed):
        t, out = f - o.f0, o.f1 - f
        h = 168 if not V else 200
        size = 128 if not V else 112
        w = W  # full width: the native menu rows (y186-214, x56-312) are covered whole, never in fragments
        y = H - h if not V else H - h - 330
        x = (1 - ease_out(clamp(t / 14))) * (w + 60) - (1 - clamp(out / 8)) * (W + 100)
        paste(c, card_band(w, h), x, y)
        draw_lockup(c, x + (w - lockup_width(h, size)) / 2, y, h, t, size)  # words centred on the band

    e.O(Fn(bar(6) + 24, bar(8) - 4, lockup))

    # ---- CH1 HOMING, bars 8-19 --------------------------------------------------------------
    e.S(Custom(bar(8), bar(12), lambda f, s, ed: tracked('hero-mgz2', f - s.f0, W, H, 1.65 if not V else 1.0,
                                                         punch=ed.punch(f)), trans='wipe', tdur=16))
    e.O(CardHeader(bar(8) + 4, bar(9) + 30, 'HOMING ATTACK'))
    mgz_hits = [65, 82, 104, 273]
    for k, h in enumerate(mgz_hits):
        e.punches.append((bar(8) + h, 0.14))
        e.X(bar(8) + h, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    chain_imgs = [text(s, 'title', 120, YELLOW, stroke=8, shadow=9) for s in ('1', '2', '3')]
    for k, h in enumerate(mgz_hits[:3]):
        end = bar(8) + mgz_hits[k + 1] if k < 2 else bar(8) + 200
        e.O(Txt(bar(8) + h, end, chain_imgs[k], W * (0.86 if not V else 0.8), H * (0.2 if not V else 0.14),
                enter='pop', leave='pop', centre=True, dur=8))
    e.O(Txt(bar(8) + mgz_hits[2] + 4, bar(8) + 200, jade_pill('CHAIN'), W * (0.86 if not V else 0.8),
            H * (0.2 if not V else 0.14) + 110, enter='up', centre=True))

    # One move, three games: each slice drops on its bar, its strike lands inside the slice
    s1n, s2n, s3n = 's1-ghz2-buzz', 'ehz2-chain-b', 'aiz-hero'
    s1hit, s2hit, s3hit = 60, 281, 70  # S1 chain 60/70 (score 100->300), S2 Buzzer, S3K Rhinobot
    s1_src0 = s1hit - 40
    s2_src0 = s2hit - 40
    s3_src0 = s3hit - 40

    def pane(name, src0, pad=120):
        if V:  # stacked bands: band-sized tracked view, HUD and lives out vertically
            return lambda lf, ow, oh: tracked(name, src0 + lf, ow, oh, 1.65, window=(58, 194), pad=pad)
        return lambda lf: tracked(name, src0 + lf, W, H, 1.65, pad=pad)

    def three(f, s, ed):
        t0 = s.f0
        panes = [(t0, pane(s1n, s1_src0), 'SONIC 1'), (t0 + b(4), pane(s2n, s2_src0), 'SONIC 2'),
                 (t0 + b(8), pane(s3n, s3_src0), 'SONIC 3 & K')]
        if V:
            return stacked_v(ed, f, panes)
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(12), bar(16), three, trans='push', tdur=14, tdir='left'))
    e.X(bar(12) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    e.X(bar(12) + 50, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    e.X(bar(12) + b(4) + 40, SFX / 's2-sfx-c1-paced.wav', 2.0)
    e.X(bar(12) + b(8) + 40, SFX / 's3k-sfx-b4-paced.wav', 1.8)

    # S2 Aquatic Ruin: lock-on reticle -> Whisp strike (score 0->100 at #138), off the green hills
    e.S(Custom(bar(16), bar(20), lambda f, s, ed: tracked('arz1-whisp-a', 57 + f - s.f0, W, H, 1.65 if not V else 1.0,
                                                          punch=ed.punch(f))))
    e.punches.append((bar(16) + 81, 0.14))
    e.X(bar(16) + 81, SFX / 's2-sfx-c1-paced.wav', 2.0)

    # ---- CH2 TALON, bars 20-27 (breakdown) ------------------------------------------------------
    e.S(Custom(bar(20), bar(24), lambda f, s, ed: tracked('carry-fly', 40 + f - s.f0, W, H, 2.0 if not V else 1.0,
                                                          window=(0, 224) if V else (0, 194), xlo=116 if V else 120), trans='wipe', tdur=16))
    e.O(CardHeader(bar(20) + 4, bar(21) + 30, 'TALON', sub='FLIGHT  CARRY  DIVEBOMB'))

    def dives(f, s, ed):
        t0 = s.f0
        strips = [(t0, 'talon-cpz', 40), (t0 + b(2), 'talon-s3k', 40)]
        return stacked_tracked(ed, f, strips, ['SONIC 2', 'SONIC 3 & K'])

    e.S(Custom(bar(24), bar(28), dives, trans='push', tdur=14, tdir='left'))

    # ---- CH3 SAME MOMENT, THREE GAMES, bars 28-46 ----------------------------------------------
    def titles3(f, s, ed):
        t0 = s.f0
        def tp(name, src, cx, cy, vcy):
            if V:  # each title whole-width in its own band
                return lambda lf, ow, oh: view(clip(name).frame(src + lf), 160, vcy, 1.0, ow, oh, 0, 224)
            return lambda lf: view(clip(name).frame(src + lf), cx, cy, 1.25, W, H, 0, 224)
        panes = [(t0, tp('title-s1', 420, 160, 96, 112), 'SONIC 1'),
                 (t0 + b(2), tp('title-s2', 840, 172, 96, 124), 'SONIC 2'),
                 (t0 + b(4), tp('title-s3k', 420, 150, 80, 96), 'SONIC 3 & K')]
        if V:
            return stacked_v(ed, f, panes)
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(28), bar(32), titles3, trans='wipe', tdur=16))
    e.O(CardHeader(bar(28) + 4, bar(29) + 30, 'THREE GAMES', sub='EVERY SCREEN REDRAWN'))

    def signs(f, s, ed):
        t0 = s.f0
        return pair_3x(ed, f, [(t0, 'ghz-clear2', 160, 'SONIC 1'), (t0 + b(2), 'ehz-clear', 262, 'SONIC 2')])

    # S1's results card is excluded: its act oval renders over the text with MICA (see README).
    e.S(Custom(bar(32), bar(34), signs))

    def stages(f, s, ed):
        t0 = s.f0
        if V:  # stacked halves: stage HUDs cropped out whole (y>=44 / y>=34)
            panes = [(t0, lambda lf, ow, oh: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.25, ow, oh, 44, 224), 'SONIC 2'),
                     (t0 + b(2), lambda lf, ow, oh: view(clip('blue-turn').frame(250 + lf), 160, 140, 1.3, ow, oh, 34, 224), 'SONIC 3 & K')]
        else:
            panes = [(t0, lambda lf: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.0, W, H, 44, 224), 'SONIC 2'),
                     (t0 + b(2), lambda lf: view(clip('blue-turn').frame(250 + lf), 160, 140, 1.2, W, H, 34, 224), 'SONIC 3 & K')]
        if V:
            return stacked_v(ed, f, panes)
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(bar(34), bar(38), stages, trans='push', tdur=14, tdir='left'))

    def screens(f, s, ed):
        t0 = s.f0
        cells = [(t0, clip('continue'), 60, 'CONTINUE', (160, 100, 1.7)),
                 (t0 + b(1), clip('data-select'), 560, 'DATA SELECT', (232, 110, 1.75)),
                 (t0 + b(2), clip('halfpipe-run'), 1010, 'SPECIAL STAGE HUD', (160, 72, 1.25)),
                 (t0 + b(3), clip('s1-ghz2-buzz'), 160, 'LIVES', (80, 170, 1.9))]
        if V:
            vcells = [(t0, clip('continue'), 60, 'CONTINUE', (160, 104, 1.0)),
                      (t0 + b(1), clip('data-select'), 560, 'DATA SELECT', (245, 112, 1.0)),
                      (t0 + b(2), clip('halfpipe-run'), 1010, 'STAGE HUD', (81, 47, 2.36)),
                      (t0 + b(3), clip('s1-ghz2-buzz'), 160, 'LIVES', (42, 196, 2.6))]
            return grid_v(ed, f, vcells)
        return grid(ed, f, cells, 2, 2, colour=YEL2)

    e.S(Custom(bar(38), bar(42), screens, trans='push', tdur=14, tdir='left'))
    # The S2 ending pose: start on the plane's front view (the side-view flight shows the stock "SONIC"
    # decal, so it is excluded); MICA lands on the wing at src 4098 -> punch + ENDINGS callout.
    end_src, end_land = 4080, 4098
    def ending(f, s, ed):
        im = clip('ending').frame(end_src + f - s.f0)
        z = (1.0 + 0.10 * smooth(s.u(f))) * ed.punch(f)
        if V:  # whole pose, width-fit, on the ending's own black
            return portrait_fit(im, (0, 0, 0), z)
        return view(im, 200, 112, z, W, H)

    e.S(Custom(bar(42), bar(45), ending))
    e.punches.append((bar(42) + end_land - end_src, 0.15))
    e.O(Txt(bar(42) + end_land - end_src, bar(45) - 6, jade_pill('ENDINGS TOO', 60),
            W * (0.80 if not V else 0.5), H * (0.80 if not V else 0.82), enter='pop', leave='fade', centre=True, dur=10))

    # ---- CH4 POWERED UP, bars 45-63 ------------------------------------------------------------
    # Solar TALON: punch in ~1.8x on him from the jump (src 30) through the grey->gold change (~56-72),
    # release to full frame (HUD whole: RINGS 70, 2:00) before the divebomb kill at src 101.
    solar_src = 10

    def solar(f, s, ed):
        i = solar_src + f - s.f0
        im = clip('solar-fly').frame(i)
        if V:
            return tracked('solar-fly', i, W, H, 1.6 - 0.6 * smooth(clamp((i - 84) / 14)))
        k = smooth(clamp((i - 84) / 14))           # 0 = punched in, 1 = full frame
        sx, sy = subject('solar-fly', i)
        z = 1.8 + (1.0 - 1.8) * k
        cx, cy = sx + (160 - sx) * k, sy + (90 - sy) * k
        # punched in: HUD (y<58) and lives (y>194) stay out; released: the whole HUD slides in with the camera
        return view(im, cx, cy, z, W, H, 58 * (1 - k), 194 - 14 * k)

    e.S(Custom(bar(45), bar(50), solar, trans='wipe', tdur=16))
    e.O(CardHeader(bar(45) + 4, bar(46) + 20, 'POWERED UP', sub='70 RINGS, MID-ACT'))
    e.O(Flash(bar(45) + 101 - solar_src, 8, 0.45))   # divebomb kill: solar-fly #101 (yvel -1605 rebound)
    e.X(bar(45) + 101 - solar_src, SFX / 's3k-sfx-b4-paced.wav', 1.8)
    gild_src = 51

    def gilded(f, s, ed):
        i = gild_src + f - s.f0
        return view(clip('gilded').frame(i), 160, 90, 1.0, W, H, 0, 180) if not V else tracked('gilded', i, W, H, 1.0)

    e.S(Custom(bar(50), bar(54), gilded))
    e.O(Flash(bar(50), 20))
    e.X(bar(50), SFX / 's3k-sfx-9f-paced.wav', 3.0)
    e.O(Flash(bar(50) + 43, 8, 0.45))  # Instagib impact: gilded #94 (yvel flips to -1280)
    e.X(bar(50) + 43, SFX / 's3k-sfx-b4-paced.wav', 1.8)

    def pair(f, s, ed):
        t0 = s.f0
        strips = [(t0, 'gilded', 240), (t0 + b(2), 'solar-fly', 300)]
        return stacked_tracked(ed, f, strips, ['GILDED MICA', 'SOLAR TALON'], zoom=1.2)

    e.S(Custom(bar(54), bar(57), pair, trans='push', tdur=12, tdir='left'))
    clear_src = 180

    def climax(f, s, ed):
        i = clear_src + f - s.f0
        if not V:
            return view(clip('gilded-clear').frame(i), 160, 90, ed.punch(f), W, H, 0, 180)
        if i < 355:
            return tracked('gilded-clear', i, W, H, 1.0, punch=ed.punch(f))
        # Portrait from the signpost on (src 355+): the whole native screen width-fit on top (HUD, tally
        # whole), and a close-up of the spinning signpost (Obj0D spawn 10816,739) beneath it.
        im = clip('gilded-clear').frame(i)
        row = rows('gilded-clear')[min(i, len(rows('gilded-clear')) - 1)]
        if i >= 544:  # the native tally enters at src ~546: show the whole screen, never fragments of its text
            c = blurred(im, ed, radius=10, dim=0.35, zoom=1.0)
            c[582:1338] = arr(im.resize((W, 756), Image.NEAREST))
            return c
        c = np.zeros((H, W, 3), np.float32)
        c[:756] = arr(im.resize((W, 756), Image.NEAREST))
        c[756:770] = np.array(YEL2, np.float32)
        sx = max(10816 - float(row['cam_x']), 116 + 66)  # left edge >= x116: no HUD digits in the close-up
        c[770:] = view(im, sx, 739 - float(row['cam_y']) - 10, 1.6, W, H - 770, 60, 224)
        return c

    e.S(Custom(bar(57), bar(64), climax))
    e.O(Flash(bar(57), 14, 0.8))
    for pop in (197, 207):  # EHZ pops: HUD score changes 0->100->300 on these source frames
        e.punches.append((bar(57) + pop - clear_src, 0.08))
        e.X(bar(57) + pop - clear_src, SFX / 's2-sfx-c1-paced.wav', 2.0)
    # Signpost: MICA's x crosses the Obj0D spawn (10816) at src 360, where the ROM plays its signpost sound
    e.X(bar(57) + 360 - clear_src, SFX / 's2-sfx-cf-paced.wav', 1.6)

    # ---- END CARD, bars 64-67, black on the final hit --------------------------------------------
    bg = clip('title-s2').frame(900)

    def endcard(f, s, ed):
        c = blurred(bg, ed, radius=8, dim=0.30, zoom=1.25)
        t = f - s.f0
        h = 230 if not V else 200
        size = 170 if not V else 112
        w = lockup_width(h, size)
        y = H * (0.28 if not V else 0.32)
        x = (W - w) / 2 + (1 - ease_out(clamp(t / 16))) * W
        paste(c, card_band(w, h), x, y)
        draw_lockup(c, x, y, h, t, size)
        lines = [('An example character mod for OpenGGF', 'sub', 60 if not V else 52, WHITE),
                 ('github.com/OpenGGF/OpenGGF', 'title_it', 64 if not V else 58, YELLOW)]
        yy = y + h + 70
        for k, (s_, role, size, col) in enumerate(lines):
            im = text(s_, role, size, col, stroke=4, shadow=5)
            paste(c, im, (W - im.shape[1]) / 2, yy, clamp((t - 20 - 8 * k) / 10))
            yy += im.shape[0] + 26
        disc = text('Fan-made and free. Not affiliated with SEGA. Requires your own ROM.', 'body',
                    30 if not V else 26, (220, 225, 240))
        paste(c, disc, (W - disc.shape[1]) / 2, H - (110 if not V else 260), clamp((t - 40) / 10))
        return c

    e.S(Custom(bar(64), bar(67) + 90, endcard, trans='iris', tdur=24))
    e.X(bar(64), SFX / 's3k-sfx-b3-paced.wav', 1.6)
    e.O(Fade(bar(67) - 12, bar(67)))
    e.O(Fn(bar(67), 10 ** 6, lambda c, f, o, ed: c.__imul__(0)))  # black through the ring-out
    e.total = bar(67) + 120
    return e.total


# ---------------------------------------------------------------------- layouts we needed

def stacked_tracked(e, f, strips, labels, zoom=1.35, window=ACT, divider=YEL2):
    """Two full-width strips (or two stacked panes in 9:16), each tracking its player, sliding in from the
    left on its own start frame; label pills sit away from any HUD."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    if V:
        zoom = max(zoom, 1.35)
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
        pill = chip(labels[k])
        paste(c, pill, e.W - pill.shape[1] - 40 + x, y + sh - pill.shape[0] - 24, clamp((f - t0 - 8) / 8))
    return c


def stacked_v(e, f, panes, divider=YEL2):
    """9:16 comparison: slanted-split panes become stacked bands, each band centred on its pane's subject."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    n = len(panes)
    gap = 14
    sh = (e.H - (n - 1) * gap) // n
    for k, (t0, fn, label) in enumerate(panes):
        if f < t0:
            continue
        img = fn(f - t0, e.W, sh)
        x = int(round(-(1 - ease_out((f - t0) / 16)) * e.W))
        y = k * (sh + gap)
        vis = e.W + x
        if vis > 0:
            c[y:y + sh, :vis] = img[:, -x:] if x < 0 else img
            if k:
                c[y - gap:y, :vis] = np.array(divider, np.float32)
        if label:
            pill = chip(label)
            paste(c, pill, 40 + x, y + sh - pill.shape[0] - 24, clamp((f - t0 - 8) / 8))
    return c


def pair_3x(e, f, panes):
    """Two whole native screens side by side at exactly 3x (16:9) or stacked at 3.375x (9:16), popping in on
    their beats over the stripes: the "same moment" pair where a slice would crop the native text."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    for k, (t0, name, src, label) in enumerate(panes):
        if f < t0:
            continue
        if not V:  # 310x174 at exactly 3x: HUD whole, lives icon out
            im = clip(name).frame(src + f - t0).crop((5, 0, 315, 174))
            pw, ph = 930, 522
            x, y = 15 + k * 960, (e.H - ph) / 2 - 40
        else:      # 320x180 at exactly 3x, stacked
            im = clip(name).frame(src + f - t0).crop((0, 0, 320, 180))
            pw, ph = 960, 540
            x, y = 60, 230 + k * (ph + 190)
        u = clamp((f - t0) / 12)
        img = im.resize((pw, ph), Image.NEAREST)
        pop_panel(c, img, x, y, f, t0, None, 5, YEL2)
        pill = chip(label)
        paste(c, pill, x + pw / 2 - pill.shape[1] / 2, y + ph + 30, clamp((f - t0 - 8) / 8))
    return c


def grid_v(e, f, cells, gap=24, label_h=74):
    """9:16 2x2 grid of portrait cells (each a native crop at >= 2.3x), popping in a beat apart."""
    c = stripes(e, f, c0=NAVYD, c1=(14, 30, 92))
    cw = (e.W - 3 * gap) // 2 - 10
    ch = (e.H - 3 * gap - 2 * label_h) // 2 - 10
    for i, (t0, cl, src, label, (cx, cy, z)) in enumerate(cells):
        if f < t0:
            continue
        img = game_view(cl.frame(src + f - t0), cx, cy, z, cw, ch)
        x = gap + (i % 2) * (cw + 10 + gap)
        y = gap + (i // 2) * (ch + 10 + label_h + gap)
        pop_panel(c, img, x, y, f, t0, label, 5, YEL2)
    return c
