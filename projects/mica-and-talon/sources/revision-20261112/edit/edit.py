#!/usr/bin/env python3
"""MICA & TALON - public promo, pacing revision (2026-11-12).

Audience: Sonic fans first, would-be modders second.
Form/evidence: gameplay showcase. Every gameplay claim is native OpenGGF footage from GameplayCaptureTool or the
  PromoCapture hosts (positioned mid-act starts with declared rings, time and score, listed in the README).
  Nothing is re-timed.
Promise: "Two original heroes, at home in all three classic Sonic games."
Cleverest true thing: not palette swaps. Every screen of three games is redrawn in that game's own style and
  driven by the game's own logic. Proof 1: lockstep splits, stock Sonic & Tails beside MICA & TALON on the same
  inputs, identical in every state column. Proof 2: "same moment, three games" triptychs.
Owner review of the 124 s cut this replaces: use the game's own sound, not placed stingers; faster pacing, no
  slow scene that touches nothing; (art fixes came from the art lane).
Pacing: two-bar cuts as the base, one-bar cuts in the builds, 48 shots in 124 s. Every window is placed so its
  hit lands on a beat: by choosing the capture window and the cut, never by sliding a sound.
Sound: the owner's "RUN INTO THE SUNSHINE (Chiptune Remix)" from its first sample, uncut, one fade (raised cosine,
  bar 85 to bar 88); cuts sit on TRACKED bar lines (the tempo drifts 172.2 to 170.2 BPM). Game sound is each
  take's own SFX-only stem (music volume 0 at capture), cut to the frames on screen. No stingers are placed.
Introductions: each hero gets a one-bar card at the head of their chapter (edit/cards.py), after the owner's
  1.0 promo cards: the hero drawing nearly the height of the frame, the lettered name from the other side; the
  field leaves first and drawing and name linger over the play. The end card carries the duo drawing.
Palette: S2 title-card blue 2449DB, red FF0000, yellow FFFF00, MICA jade, TALON slate.
Title face: Fira Sans Compressed Heavy on the S2 card's blue band for the title lock-up (white); the lettered
  names on the two cards and the end card; native lettering wherever the game supplies it.
Canvas: full-bleed 320x180 windows of the native frame at exactly 6x; no camera moves in 16:9. Splits only for
  comparisons. 9:16 is recomposed shot by shot (tall frame, stacked bands, whole screens on their own ground).
Rejected: a 400-px widescreen capture; a zoom anywhere in the cold open (owner); a caption per shot; the lettered
  names in the title band (they read poorly on the card blue); a card on the cold open's duo shot (it would cover
  the hook).
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
CAP = T / os.environ.get('MT_CAPTURES', 'captures')
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


import cards as CARDS  # noqa: E402  (edit/cards.py: the introduction cards and the duo end card)

SFXG = float(os.environ.get('MT_SFX_GAIN', '1.5'))   # gain on every captured SFX-only stem: hits sit about 2 dB under the bed
# The game's own sounds are not equally loud: the Death Egg booster and a spindash release are 5-8 dB hotter than a
# badnik pop. These takes are trimmed so nothing leaps out of the mix (measured by tools/mixcheck.py).
TRIM = {'dez-talon': 0.6, 'dez-solar': 0.6, 'cpz-lock-mod': 0.7, 'dez-hyper': 0.8}


def B(n):
    """Output frame of a bar that may be fractional (16.5 = bar 16, beat 3)."""
    return bar(int(n), (n - int(n)) * 4)


GIL_STRIKE = 94      # aiz-gilded: the Gilded strike that kills the Rhinobot


def timing():
    """Source frame shown on each shot's first output frame: every window is placed so that its hit lands on a
    beat (the event frames are checked against the takes by tools/takes_check.py)."""
    b = bar
    k = dict(
        duo0=218 - (b(3, 3) - b(2)),            # spring on bar 3 beat 4
        carry0=128 - (b(4, 2) - b(4)),          # catch on bar 4 beat 3
        tdive0=120 - (b(6, 2) - b(6)),          # TALON's kill on bar 6 beat 3
        norm0=163 - (b(7, 2) - b(7)),           # MICA's kill on bar 7 beat 3
        mhzh0=262,
        s2_0=757 - (b(12) - b(10)),             # the title's own flash on bar 12
        mgz0=65 - (b(15, 1) - b(14)),           # kills on bar 15 beats 2, 3, 4; negative: the take starts under the card's opaque field
        hcz0=408 - (b(20) - b(18, 2)),          # out on the spring (#396)
        cpz0=45 - (b(20, 1) - b(20)),           # spindash release on beat 2
        ghzm0=264 - (b(21, 3) - b(21)),         # Sonic 1: monitor pop on beat 4
        ehzc0=133 - (b(23, 2) - b(22)),         # side spring on bar 23 beat 3
        mhzs0=108 - (b(24, 2) - b(24)),         # mushroom spring on beat 3
        cnz0=152,
        syz0=118 - (b(29, 1) - b(28)),          # kills on bar 29 beats 2 and 4
        htz0=114 - (b(31, 2) - b(31)),          # the dive starts on beat 3 and the shot ends before he outruns the camera
        dezt0=239 - (b(33, 2) - b(32)),         # booster on bar 33 beat 3
        arzt0=191 - (b(35) - b(34)),            # Whisp killed on bar 35
        lockA=80, lockB=289 - (b(37, 1) - b(37)), lockC=182,
        scz0=259 - (b(48, 1) - b(48)),          # kills on bar 48 beat 2, bar 49 beats 1 and 3
        end_side=2760 - (b(51) - b(50)), end_pose=4098 - (b(51, 1) - b(51)),
        mtz0=271, lbzs0=143 - (b(54, 2) - b(54)), cnzr0=68, buz0=281 - (b(58) - b(57)),
        g0=160 - (b(60) - b(58, 2)),            # gold reveal on bar 60
        trn0=55 - (b(62, 2) - b(62)), trg0=GIL_STRIKE - (b(63) - b(62, 2)),
        slz0=112, arzg0=251 - (b(65, 1) - b(65)), cpzg0=238 - (b(66, 1) - b(66)),
        sol0=104 - (b(68) - b(67, 2)),          # flame reveal on bar 68, kill (#188) on bar 69
        dezs0=331 - (b(71, 1) - b(70)), syzs0=405, htzs0=165, fbz0=149,   # Flying Battery: the dive starts on beat 2
        h0=96 - (b(76) - b(75, 1)),             # Hyper reveal on bar 76, kill (#182) on bar 77
        b0=632 - (b(79) - b(78)),               # the one hit on bar 79
        p0=86 - (b(80, 1) - b(80)),             # twin reveal on bar 80 beat 2, catch (#128) on beat 4
    )
    k['beat'] = b(12, 1) - b(12)
    k['pair_end'] = k['p0'] + (b(84) - b(80))
    k['end_f'] = b(88) + 36
    return k


TRI_STRIKE = [('ghz2-buzz', 60, 'SONIC 1'), ('arz-whisp', 138, 'SONIC 2'), ('aiz-hero', 70, 'SONIC 3 & K')]
PART = CARDS.PART0          # frames into a card's bar at which its field starts to part and the play shows


def stem(e, take, src, at, n, gain=1.0):
    """The take's own SFX-only audio for the frames a shot shows (5 ms fades at both ends, kit's stem)."""
    wav = CAP / take / 'audio.wav'
    if not wav.exists():
        return
    if src < 0:
        at, n, src = at - src, n + src, 0
    if n > 0:
        e.stem(wav, int(src), int(at), int(n), SFXG * gain * TRIM.get(take, 1.0))


def sound(e, k):
    """Bed plus the captured game sound of every shot: no placed stingers. A split screen mixes its panes a
    little lower; the lockstep split plays the mod's side only (the stock side makes the same sounds)."""
    e.bed(T / 'work/bed.wav', 0, 0.75, fade_out=0.0)
    bt = k['beat']
    one = [  # take, source frame at f0, f0, f1
        ('title-s3k', 267, bar(0) + 33, B(2)), ('lbz-duo', k['duo0'], B(2), B(4)), ('carry-swoop', k['carry0'], B(4), B(6)),
        ('aiz-talon-dive', k['tdive0'], B(6), B(7)), ('aiz-normal', k['norm0'], B(7), B(8)), ('mhz-hyper', k['mhzh0'], B(8), B(10)),
        ('title-s2', k['s2_0'], B(10), B(14)),
        ('mgz-chain', k['mgz0'] + PART, B(14) + PART, B(16.5)),          # silent while the card's field is whole
        ('hcz-loop', k['hcz0'], B(18.5), B(20)), ('cpz-spindash', k['cpz0'], B(20), B(21)), ('ghz2-buzz', k['ghzm0'], B(21), B(22)),
        ('ehz2-corkscrew', k['ehzc0'], B(22), B(24)), ('mhz-spring', k['mhzs0'], B(24), B(26)), ('cnz-bumpers', k['cnz0'], B(26), B(28)),
        ('syz-talon', k['syz0'] + PART, B(28) + PART, B(31)),
        ('htz-talon-dive', k['htz0'], B(31), B(32)), ('dez-talon', k['dezt0'], B(32), B(34)), ('arz-talon-whisp', k['arzt0'], B(34), B(36)),
        ('cpz-lock-mod', k['lockA'], B(36), B(37)), ('cpz-lock-mod', k['lockB'], B(37), B(38)), ('ehz-lock-mod', k['lockC'], B(38), B(40)),
        ('ehz-clear', 471, B(43), B(44)),
        ('scz-chain', k['scz0'], B(48), B(50)), ('ending', k['end_side'], B(50), B(51)), ('ending', k['end_pose'], B(51), B(52)),
        ('mtz-run', k['mtz0'], B(52), B(54)), ('lbz-slope', k['lbzs0'], B(54), B(56)), ('cnz-bumpers', k['cnzr0'], B(56), B(57)),
        ('ehz2-corkscrew', k['buz0'], B(57), B(58.5)), ('hcz-gilded-runin', k['g0'], B(58.5), B(62)),
        ('slz-gilded', k['slz0'], B(64), B(65)), ('arz-gilded', k['arzg0'], B(65), B(66)), ('cpz-gilded', k['cpzg0'], B(66), B(67.5)),
        ('aiz-solar-reveal', k['sol0'], B(67.5), B(70)), ('dez-solar', k['dezs0'], B(70), B(72)), ('syz-solar', k['syzs0'], B(72), B(73)),
        ('htz-solar', k['htzs0'], B(73), B(74)), ('fbz-solar', k['fbz0'], B(74), B(75.25)), ('dez-hyper', k['h0'], B(75.25), B(78)),
        ('lbz-boss', k['b0'], B(78), B(80)), ('lbz-pair', k['p0'], B(80), B(84)),
    ]
    for take, src, f0, f1 in one:
        stem(e, take, src, f0, f1 - f0)
    for n, (take, hit, _) in enumerate(TRI_STRIKE):                      # each pane from the beat it drops in
        stem(e, take, hit - 2 * bt, B(16.5) + n * bt, B(18.5) - B(16.5) - n * bt, 0.75)
    stem(e, 'ghz-clear', 227, B(42), B(43) - B(42), 0.75)
    stem(e, 'ehz-clear', 387, B(42) + 10, B(43) - B(42) - 10, 0.75)
    for n, (take, src) in enumerate((('ghz-ss', 900), ('halfpipe-run', 740), ('blue-sphere', 430))):
        stem(e, take, src, B(44) + n * bt, B(46) - B(44) - n * bt, 0.6)
    for n, (take, src) in enumerate((('continue', 60), ('data-select', 405), ('halfpipe-run', 1010), ('cpz-talon', 60))):
        stem(e, take, src, B(46) + n * bt, B(48) - B(46) - n * bt, 0.5)
    stem(e, 'aiz-normal', k['trn0'], B(62), B(64) - B(62), 0.8)
    stem(e, 'aiz-gilded', k['trg0'], B(62.5), B(64) - B(62.5), 0.8)
    stem(e, 'lbz-pair', k['pair_end'], B(84), PAIR_LOOP - k['pair_end'], 0.7)   # the carry's flaps run on under the end card until the loop point


PAIR_LOOP = 570      # the pair's flight tires at #593: the end card's backdrop plays back and forth from here


def intro(e, who, f0, f1, plate_until, left):
    """A character's introduction card (edit/cards.py) over the shot that starts on f0."""
    card = CARDS.Intro(who, e.W, e.H, hero_left=left)

    def draw(c, f, o, ed):
        c[:] = card.draw(np.clip(c, 0, 255).astype(np.uint8), f - f0, plate_until=plate_until)

    e.O(Fn(f0, f1, draw))


K = {}       # the timing table, kept for the tools


def build(e):
    k = timing()
    K.clear()
    K.update(k)
    sound(e, k)
    (build_v if V else build_h)(e, k)
    e.total = k['end_f']
    return e.total


def build_h(e, k):
    W, H = e.W, e.H
    bt = k['beat']
    half = lambda n: B(n - 0.5)

    def play(take, key, b0, b1, y0=0, **kw):
        """A full-frame shot: the 320x180 window at 6x, from the take's timed in-point."""
        return e.S(Custom(B(b0), B(b1), lambda f, s, ed: full(take, k[key] + f - s.f0, y0), **kw))

    # ================= COLD OPEN, bars 0-10 ========================================================
    # S3K title roll-in as it ships, without the SEGA logo: black for the 33 frames the logo is on screen
    # (src 234-266), then the smear (267), the native flash (296), logo drop, wink (~404). Ends at src 411, one
    # frame before the title's stock Tornado fly-by.
    def rollin(f, s, ed):
        i = 234 + f - s.f0
        if i < 267:
            return np.zeros((H, W, 3), np.float32)
        return full('title-s3k', i, 8)            # rows 8-188: '& KNUCKLES' whole, menu rows out

    e.S(Custom(0, B(2), rollin))

    # Partners: the two cross the Launch Base bridge together, name tags a beat apart, out on the spring.
    play('lbz-duo', 'duo0', 2, 4)
    e.O(Tag(B(2) + 14, B(4) - 4, 'MICA', JADE, 'lbz-duo', k['duo0']))
    e.O(Tag(B(2) + bt + 14, B(4) - 4, 'TALON', SLATE, 'lbz-duo', k['duo0'], key='sk_', other=''))

    # The carry swoop: she jumps from a run, he catches her in the air on beat 3; the promise line follows.
    play('carry-swoop', 'carry0', 4, 6, 8)         # rows 8-188: her run-up is along the level's lowest ground
    e.O(Shade(B(4) + 2 * bt, B(6) - 4, 'bottom'))
    e.O(Txt(B(4) + 2 * bt + 6, B(6) - 4, line('TWO ORIGINAL HEROES. THREE CLASSIC GAMES.', 72), W / 2, H - 150, enter='up',
            leave='fade', centre=True, dur=10))

    play('aiz-talon-dive', 'tdive0', 6, 7)        # his first hit, on beat 3
    play('aiz-normal', 'norm0', 7, 8)             # hers, on beat 3 of the next bar
    play('mhz-hyper', 'mhzh0', 8, 10)             # the riser: Hyper MICA through two loops, after-images banding

    # ================= TITLE DROP, bars 10-14 ======================================================
    # S2 title as it ships: the emblem on black while MICA then TALON rise; the title's own white flash (src 757)
    # is the drop on bar 12. Rows 26-206: the emblem whole, '2 PLAYER VS' and the copyright line out whole. The
    # lock-up band is part of the picture, so the cut carries it away.
    def s2_title(f, s, ed):
        c = view(clip('title-s2').frame(k['s2_0'] + f - s.f0), 160, 116, 1.0, W, H, 26, 206)
        t = f - (B(12) + 10)
        if t >= 0:
            h, size = 150, 116
            y = H - h
            x = (1 - ease_out(clamp(t / 14))) * (W + 60)
            paste(c, card_band(W, h), x, y)
            g = f - B(13)                     # a gold glint sweeps the names on bar 13
            draw_lockup(c, x + (W - lockup_width(h, size)) / 2, y, h, t, size, beat=bt,
                        glint=W * 0.22 + W * 0.60 * g / 34 if 0 <= g < 34 else None)
        return c

    e.S(Custom(B(10), B(14), s2_title))
    e.O(Flash(B(12), 16, 0.9))

    # ================= MICA, bars 14-28 ============================================================
    # Her card lands on bar 14 over the Marble Garden take's lead-in; the three kills land on beats 2, 3 and 4 of
    # bar 15, just after the drawing has gone. The take ends before she is hurt.
    mgz_hits = [65, 85, 107]
    # the take's first frame is held for the frames before it starts: the card's field is whole until PART
    e.S(Custom(B(14), B(16.5), lambda f, s, ed: full('mgz-chain', max(0, k['mgz0'] + f - s.f0))))
    intro(e, 'mica', B(14), B(16.5), B(16.5) - B(14), True)
    chain_imgs = [text(s_, 'title', 150, YELLOW, stroke=9, sfill=NAVY, shadow=10) for s_ in ('1', '2', '3')]
    for n, h in enumerate(mgz_hits):
        at = B(14) + h - k['mgz0']
        end = B(14) + mgz_hits[n + 1] - k['mgz0'] if n < 2 else B(16.5) - 6
        e.O(Txt(at, end, chain_imgs[n], W * 0.87, H * 0.24, enter='pop', leave='pop', centre=True, dur=8))
    e.O(Txt(B(14) + mgz_hits[2] - k['mgz0'] + 4, B(16.5) - 6, pill('CHAIN', JADE, 56), W * 0.87, H * 0.24 + 130, enter='up', centre=True))

    # One move, three games: a slice drops on each beat and lands its strike two beats later, a 1-2-3.
    SLICE = (0, 194)   # slice panes may use the rows above 58 as headroom; slice_guard keeps the HUD out of the slice

    def pane(name, src0, pad=120, zoom=1.65):
        return lambda lf: tracked(name, src0 + lf, W, H, zoom, pad=pad, window=SLICE, slice_guard=True)

    def three(f, s, ed):
        return slanted_split(ed, f, [(B(16.5) + n * bt, pane(nm, hit - 2 * bt), lab) for n, (nm, hit, lab) in enumerate(TRI_STRIKE)], divider=YEL2)

    e.S(Custom(B(16.5), B(18.5), three, trans='push', tdur=12, tdir='left'))

    play('hcz-loop', 'hcz0', 18.5, 20)            # the Hydrocity channel at speed, out on the spring
    play('cpz-spindash', 'cpz0', 20, 21)          # spindash release on beat 2
    play('ghz2-buzz', 'ghzm0', 21, 22)            # Sonic 1: two dashes and a monitor pop on beat 4
    play('ehz2-corkscrew', 'ehzc0', 22, 24)       # corkscrew, side spring on bar 23 beat 3
    play('mhz-spring', 'mhzs0', 24, 26)           # mushroom spring on beat 3, ring arc
    play('cnz-bumpers', 'cnz0', 26, 28)           # the two bounce through the bumpers

    # ================= TALON, bars 28-36 ===========================================================
    # His card lands on bar 28 over his flight in; both kills (beats 2 and 4 of bar 29) are clear of it. From
    # beat 3 of bar 29 the lives inset takes the corner the name plate held.
    syz, syz0 = 'syz-talon', k['syz0']
    inset0 = B(29.5)
    play(syz, 'syz0', 28, 31)
    intro(e, 'talon', B(28), B(31), inset0 - B(28), False)
    e.O(Txt(inset0, B(31) - 6, pill('IN SONIC 1, TOO', SLATE, 54), W * 0.80, H * 0.86, enter='up', leave='fade', centre=True))

    def lives(c, f, o, ed):   # the lives display the 16:9 window drops: shown whole, at its own scale, as an inset
        im = clip(syz).frame(syz0 + f - B(28)).crop((8, 196, 80, 222)).resize((432, 156), Image.NEAREST)
        pop_panel(c, im, 60, H - 156 - 80, f, o.f0, None, 6, YEL2)

    e.O(Fn(inset0, B(31) - 6, lives))

    play('htz-talon-dive', 'htz0', 31, 32)        # Hill Top: flight over the lake, the dive on beat 3
    play('dez-talon', 'dezt0', 32, 34)            # dive, land, run into the booster on bar 33 beat 3
    play('arz-talon-whisp', 'arzt0', 34, 36)      # his Sonic 2 hit: a Whisp on bar 35

    # ================= EVERY SCREEN, bars 36-52 ====================================================
    LOCK = [(B(36), 'cpz-lock-stock', 'cpz-lock-mod', k['lockA']), (B(37), 'cpz-lock-stock', 'cpz-lock-mod', k['lockB']),
            (B(38), 'ehz-lock-stock', 'ehz-lock-mod', k['lockC'])]

    def lockstep(f, s, ed):
        t0, st, md, s0 = [x for x in LOCK if x[0] <= f][-1]
        i = s0 + f - t0
        mx, my = subject(md, i)
        sx, sy = subject(md, i, 'sk_')
        cx = (mx + sx) / 2 if abs(mx - sx) < 110 else mx

        def side(name):
            return lambda lf: view(clip(name).frame(i), cx, my, 1.1, W, H, 58, 224)   # rows 58+: the HUD is out whole
        return slanted_split(ed, f, [(s.f0 - 100, side(st), None), (s.f0 - 100, side(md), None)], divider=YEL2, drop_frames=1)

    e.S(Custom(B(36), B(40), lockstep, trans='wipe', tdur=16))
    e.O(CardHeader(B(36) + 4, B(37) + 30, 'EVERY SCREEN', sub='REDRAWN'))
    e.O(Txt(B(36) + 20, B(40) - 6, chip('ORIGINAL', size=50), W * 0.25, 60, enter='down', leave='fade', centre=True))
    e.O(Txt(B(36) + 26, B(40) - 6, pill('MICA & TALON', JADE, 50), W * 0.75, 60, enter='down', leave='fade', centre=True))
    e.O(Txt(B(38), B(40) - 6, line('SAME INPUTS. SAME PHYSICS. EVERY FRAME.', 66), W / 2, H - 130, enter='up', leave='fade',
            centre=True, dur=12))

    def titles3(f, s, ed):
        def tp(name, src, cx, cy):
            return lambda lf: view(clip(name).frame(src + lf), cx, cy, 1.25, W, H, 0, 224)
        starts = [B(40) + n * bt for n in range(3)]
        panes = [(starts[0], lambda lf: view(clip('title-s1').frame(392 + lf), 160, 72, 224 / 147, W, H, 0, 147), None),   # rows 0-147: the emblem's SEGA plate stays out
                 (starts[1], tp('title-s2', 840, 172, 96), None), (starts[2], tp('title-s3k', 320, 150, 96), None)]
        c = slanted_split(ed, f, panes, divider=YEL2)
        for n, lab in enumerate(('SONIC 1', 'SONIC 2', 'SONIC 3 & K')):
            if f >= starts[n] + 8:
                p = chip(lab)
                cx = (n + 0.5) * W / 3 + 0.22 * (54 - H / 2)
                paste(c, p, cx - p.shape[1] / 2, 26, clamp((f - starts[n] - 8) / 8))
        return c

    e.S(Custom(B(40), B(42), titles3, trans='push', tdur=12, tdir='left'))

    # Signposts from mid-spin; both land on her face on beat 4. S1's results card is excluded (engine fault).
    e.S(Custom(B(42), B(43), lambda f, s, ed: pair_3x(ed, f, [(s.f0, 'ghz-clear', 227, 'SONIC 1'), (s.f0 + 10, 'ehz-clear', 387, 'SONIC 2')])))
    e.S(Custom(B(43), B(44), lambda f, s, ed: full('ehz-clear', 471 + f - s.f0)))       # MICA GOT THROUGH flies in

    def stages(f, s, ed):
        panes = [(B(44), lambda lf: view(clip('ghz-ss').frame(900 + lf), 160, 112, 1.0, W, H, 0, 224), 'SONIC 1'),
                 (B(44) + bt, lambda lf: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.0, W, H, 44, 224), 'SONIC 2'),
                 (B(44) + 2 * bt, lambda lf: view(clip('blue-sphere').frame(430 + lf), 160, 140, 1.2, W, H, 34, 224), 'SONIC 3 & K')]
        return slanted_split(ed, f, panes, divider=YEL2)

    e.S(Custom(B(44), B(46), stages, trans='push', tdur=12, tdir='left'))

    def screens(f, s, ed):
        t0 = s.f0
        cells = [(t0, clip('continue'), 60, 'CONTINUE', (160, 100, 1.7)),
                 (t0 + bt, clip('data-select'), 405, 'DATA SELECT', (232, 110, 1.75)),
                 (t0 + 2 * bt, clip('halfpipe-run'), 1010, 'SPECIAL STAGE HUD', (160, 72, 1.25)),
                 (t0 + 3 * bt, clip('cpz-talon'), 60, 'LIVES', (46, 207, 4.6))]
        return grid(ed, f, cells, 2, 2, colour=YEL2)

    e.S(Custom(B(46), B(48), screens, trans='push', tdur=12, tdir='left'))

    # TALON's Tornado as one beat: the Sky Chase chain from the wing, then the ending.
    play('scz-chain', 'scz0', 48, 50)
    e.O(Txt(B(49) + 2 * bt, B(50) - 6, pill('TALON FLIES THE TORNADO', SLATE, 50), W * 0.30, H * 0.86, enter='up', leave='fade', centre=True))
    play('ending', 'end_side', 50, 51, 22)
    play('ending', 'end_pose', 51, 52, 22)
    e.O(Txt(B(51) + bt + 4, B(52) - 4, pill('ENDINGS, TOO', JADE, 60), W * 0.74, H * 0.50, enter='pop', leave='fade', centre=True, dur=8))

    # ================= BUILD, bars 52-58.5 =========================================================
    play('mtz-run', 'mtz0', 52, 54)               # the fastest normal-form run
    play('lbz-slope', 'lbzs0', 54, 56)            # spring on beat 3
    play('cnz-bumpers', 'cnzr0', 56, 57)          # the two run the neon ledge and leap
    play('ehz2-corkscrew', 'buz0', 57, 58.5)      # a Buzzer struck on bar 58

    # ================= POWERED UP, bars 58.5-75.5 ==================================================
    play('hcz-gilded-runin', 'g0', 58.5, 62)      # normal MICA runs, jumps, winds up; gold on the chorus
    e.O(Flash(B(60), 10, 0.45))
    e.O(CardHeader(B(60) + 12, B(61) + 10, 'POWERED UP', sub='50 RINGS  MID-ACT'))
    e.O(Txt(B(61) + 14, B(62) - 6, pill('GILDED MICA', GOLD2, 56, fg=NAVY), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))

    def trails(f, s, ed):                         # the same Rhinobot twice: strikes two beats apart
        strips = [(B(62), 'aiz-normal', k['trn0']), (B(62.5), 'aiz-gilded', k['trg0'])]
        return stacked_tracked(ed, f, strips, [('NORMAL: JADE TRAIL', JADE, WHITE), ('GILDED: GOLD TRAIL', GOLD2, NAVY)], zoom=1.35)

    e.S(Custom(B(62), B(64), trails, trans='push', tdur=12, tdir='left'))

    play('slz-gilded', 'slz0', 64, 65)            # Gilded in Sonic 1
    play('arz-gilded', 'arzg0', 65, 66)           # Gilded in Sonic 2, spring on beat 2
    play('cpz-gilded', 'cpzg0', 66, 67.5)         # gold through the tubes, spring on beat 2

    play('aiz-solar-reveal', 'sol0', 67.5, 70)    # wind-up, flame reveal on bar 68, divebomb kill on bar 69
    e.O(Flash(B(68), 10, 0.45))
    e.O(Txt(B(68) + 30, B(70) - 6, pill('SOLAR TALON', (255, 146, 36), 56, fg=NAVY), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))
    play('dez-solar', 'dezs0', 70, 72)            # ember flight into the booster on bar 71 beat 2
    play('syz-solar', 'syzs0', 72, 73)            # Solar in Sonic 1
    play('htz-solar', 'htzs0', 73, 74)            # Solar in Sonic 2
    play('fbz-solar', 'fbz0', 74, 75.25)          # Solar streak through Flying Battery's ring line

    # ================= HERO, bars 75.5-84 ==========================================================
    play('dez-hyper', 'h0', 75.25, 78)            # Hyper reveal on the lift, kill on bar 77
    e.O(Flash(B(76), 10, 0.5))
    e.O(Txt(B(76) + 30, B(78) - 6, pill('HYPER MICA', ROSE, 56), W * 0.82, H * 0.86, enter='up', leave='fade', centre=True))

    # The boss: Launch Base 1's mini-boss. She backs off, runs in, hops and strikes once. The game ends her Hyper
    # form ON the kill frame (the ROM rule: a Super form ends when the HUD timer stops) and draws her in normal
    # colours about 15 frames later; she travels right after the hit, under the ONE HIT. card, so no frame shows
    # her after the form has ended. The machine breaks apart beside the card.
    boss = 'lbz-boss'
    play(boss, 'b0', 78, 80)
    e.O(Flash(B(79), 10, 0.55))
    one_im = text('ONE', 'title', 250, WHITE, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
    hit_im = text('HIT.', 'title', 250, YELLOW, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
    CARD_X = BOSS_CARD_X * 6                  # the card's edge at mid-height, in native x

    def hit_card(c, f, o, ed):
        t = f - o.f0
        xs, ys, _ = ed.grids()
        edge = CARD_X + 0.22 * (ys - H / 2) + (1 - ease_out(clamp(t / 7))) * (W - CARD_X + 200)
        c[xs >= edge] = np.array(BLUE2, np.float32)
        zig = ((ys // 18) % 2) * 9
        c[(xs >= edge) & (xs < edge + 46 + zig)] = np.array(RED2, np.float32)
        c[(xs >= edge - 14) & (xs < edge)] = np.array(YEL2, np.float32)
        cx = (CARD_X + W) / 2 + 40 + (1 - ease_out(clamp(t / 7))) * (W - CARD_X + 200)
        for n, (im, yy) in enumerate(((one_im, H * 0.33), (hit_im, H * 0.63))):
            u = (t - 5 - n * bt / 2) / 7
            if u <= 0:
                continue
            sc = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, cx - im2.shape[1] / 2, yy - im2.shape[0] / 2, clamp(u * 2))

    e.O(Fn(B(79), B(80), hit_card))

    # The pair: MICA on pad 1, TALON on pad 2, on the bridge the film opened on. The cut is white for the nine
    # frames in which the two are still in normal colours; both snap open on beat 2; he catches her on beat 4 and
    # they drift up and across the domes.
    pair, p0 = 'lbz-pair', k['p0']
    play(pair, 'p0', 80, 84)
    white_n = 74 - p0                         # press #61: normal colours to #73, silhouettes #74-85, reveal #86

    def white_in(c, f, o, ed):
        t = f - o.f0
        a = 1.0 if t < white_n else 1.0 - (t - white_n) / 9
        c *= (1 - a)
        c += 255 * a

    e.O(Fn(B(80), B(80) + white_n + 9, white_in))
    tag_m, tag_t = pill('HYPER MICA', ROSE, 56), pill('SOLAR TALON', (255, 146, 36), 56, fg=NAVY)

    def pair_tags(c, f, o, ed):
        i = p0 + f - B(80)
        t, out = f - o.f0, o.f1 - f
        for n, (im, key) in enumerate(((tag_m, ''), (tag_t, 'sk_'))):
            u = (t - n * bt) / 9
            if u <= 0:
                continue
            x, y = subject(pair, i, key, 6)
            sc = 0.7 + 0.3 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, (x + 24) * 6 + (im.shape[1] - im2.shape[1]) / 2, (y - 2) * 6 - im2.shape[0] / 2, clamp(u * 2) * clamp(out / 8))

    e.O(Fn(B(81), B(83), pair_tags))

    # ================= END CARD, bars 84-88, fades with the music ==================================
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = (1.0 - 0.45 * np.clip(np.hypot((xs - W / 2) / (W * 0.70), (ys - H * 0.45) / (H * 0.60)), 0, 1) ** 1.4)[..., None]
    endc = CARDS.EndCard(W, H)

    def endcard(f, s, ed):
        kf = pair_frame(k['pair_end'] + (f - s.f0))
        c = blurred(clip(pair).frame(kf).crop((114, 4, 320, 120)), ed, radius=1.8, dim=0.66, zoom=1.0) * vig   # right of the HUD: sky, domes, the pair
        return endc.draw(np.clip(c, 0, 255).astype(np.uint8), f - s.f0).astype(np.float32)

    e.S(Custom(B(84), k['end_f'], endcard, trans='iris', tdur=24))
    e.O(Fade(B(87), B(88) + 6))
    e.O(Fn(B(88) + 6, 10 ** 6, lambda c, f, o, ed: c.__imul__(0)))


BOSS_CARD_X = 194    # native x of the ONE HIT. card's edge: she is right of it from 13 frames after the hit


def pair_frame(kf):
    """The pair take under the end card: it plays on, then back and forth before the flight tires."""
    if kf > PAIR_LOOP:
        j = (kf - PAIR_LOOP) % 120
        kf = PAIR_LOOP - (j if j < 60 else 120 - j)
    return kf



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


def build_v(e, k):
    W, H = e.W, e.H
    bt = k['beat']

    def ground(f):
        return stripes(e, f, c0=NAVYD, c1=(14, 30, 92))

    def whole(c, im, rows_, y, rules=False):
        """Paste native rows [a, b) of a frame at full canvas width (3.375x), top at y; returns its height."""
        a, b = rows_
        ph = round((b - a) * W / 320)
        c[y:y + ph] = arr(resample(im, 0, a, 320, b - a, W, ph))
        if rules:
            c[y - 14:y] = np.array(YEL2, np.float32)
            c[y + ph:y + ph + 14] = np.array(YEL2, np.float32)
        return ph

    def on_own_ground(im, rows_, y):
        fill = np.array(im.getpixel((2, rows_[0] + 2)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        whole(c, im, rows_, y)
        return c

    def window_on_ground(im, box, y):       # a native window at full canvas width, on the picture's own flat ground
        x0, y0, x1, y1 = box
        fill = np.array(im.getpixel((x1 - 3, y1 - 3)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        ph = round((y1 - y0) * W / (x1 - x0))
        c[y:y + ph] = arr(resample(im, x0, y0, x1 - x0, y1 - y0, W, ph))
        return c

    def tall(take, key, b0, b1, **kw):
        """The tall frame: every native row, 126 px wide, never left of x 116 (the HUD is out whole); it follows
        the hero only as far as the game's own camera lets her leave the centre. x0 fixes the window instead."""
        pk = {a: kw.pop(a) for a in ('x0', 'lead', 'sm', 'key_') if a in kw}
        if 'key_' in pk:
            pk['key'] = pk.pop('key_')
        return e.S(Custom(B(b0), B(b1), lambda f, s, ed: pv(take, k[key] + f - s.f0, **pk), **kw))

    # ================= COLD OPEN ===================================================================
    def rollin(f, s, ed):
        i = 234 + f - s.f0
        if i < 267:
            return np.zeros((H, W, 3), np.float32)
        im = clip('title-s3k').frame(i)
        if i < 296:                           # the smear frames fill the frame: full-height centre window
            return arr(resample(im, 160 - PW / 2, 0, PW, 224, W, H))
        # the title whole (columns 28-292, rows 0-188) at 4.09x on its own sky; the clouds beside the logo ease out
        fill = np.array(im.getpixel((2, 2)), np.float32)
        c = np.empty((H, W, 3), np.float32)
        c[:] = fill
        ph = round(188 * W / 264)
        pic = arr(resample(im, 28, 0, 264, 188, W, ph))
        a = np.clip((ph - np.arange(ph)) / 28.0, 0, 1)[:, None, None] * np.ones((1, W, 1), np.float32)
        a[:, 131:965] = 1.0
        c[540:540 + ph] = pic * a + fill * (1 - a)
        return c

    e.S(Custom(0, B(2), rollin))

    # The duo: one band each, the same size, until the spring; then the tall frame for the launch.
    duo0 = k['duo0']
    DUO_CUT = B(2) + 216 - duo0               # two frames before the spring fires

    def duo(f, s, ed):
        i = duo0 + f - s.f0
        if f >= DUO_CUT:
            return pv('lbz-duo', i, x0=116.0)
        return bands_v(ed, f, [(s.f0 - 100, lambda lf, ow, oh: band('lbz-duo', i, ow, oh), None),
                               (s.f0 - 100, lambda lf, ow, oh: band('lbz-duo', i, ow, oh, key='sk_'), None)])

    e.S(Custom(B(2), B(4), duo))
    sh2 = (H - 14) // 2
    e.O(Txt(B(2) + 14, DUO_CUT, pill('MICA', JADE, 64), W / 2, sh2 / 2 - 250, enter='pop', leave='fade', centre=True, dur=9, out_dur=6))
    e.O(Txt(B(2) + bt + 14, DUO_CUT, pill('TALON', SLATE, 64), W / 2, sh2 + 14 + sh2 / 2 - 250, enter='pop', leave='fade', centre=True, dur=9, out_dur=6))

    # The carry swoop: one fixed window (native x 134-260) holds her run-up, him hovering ahead, and the catch.
    tall('carry-swoop', 'carry0', 4, 6, x0=134.0)
    e.O(Shade(B(4) + 2 * bt, B(6) - 4, 'bottom'))
    for n, s_ in enumerate(('TWO ORIGINAL HEROES.', 'THREE CLASSIC GAMES.')):
        e.O(Txt(B(4) + 2 * bt + 6 * (n + 1), B(6) - 4, line(s_, 82), W / 2, H - 380 + 110 * n, enter='up', leave='fade', centre=True, dur=10))

    tall('aiz-talon-dive', 'tdive0', 6, 7)
    tall('aiz-normal', 'norm0', 7, 8)
    tall('mhz-hyper', 'mhzh0', 8, 10)

    # ================= TITLE DROP ==================================================================
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
        im = clip('title-s2').frame(k['s2_0'] + f - s.f0)
        c = on_own_ground(im, (26, 206), S2Y)         # black before the flash, the title's sky after it
        t = f - B(12)
        if t >= 0:                                    # the card rides in under the title's own flash
            x = (1 - ease_out(clamp(t / 14))) * (W + 60)
            paste(c, card_block(W, H - CARD_Y), x, CARD_Y)
            lock_h = int(lockup_words(LS)[0].shape[0] * 1.80)
            stacked_lockup(c, x + 130, CARD_Y + (H - CARD_Y - 28 - lock_h) / 2, t - 6, LS, bt)
        return c

    e.S(Custom(B(10), B(14), s2_title))
    e.O(Flash(B(12), 16, 0.9))

    # ================= MICA ========================================================================
    mgz_hits = [65, 85, 107]
    e.S(Custom(B(14), B(16.5), lambda f, s, ed: pv('mgz-chain', max(0, k['mgz0'] + f - s.f0))))
    intro(e, 'mica', B(14), B(16.5), B(16.5) - B(14), True)
    chain_imgs = [text(s_, 'title', 190, YELLOW, stroke=10, sfill=NAVY, shadow=11) for s_ in ('1', '2', '3')]
    for n, h in enumerate(mgz_hits):
        at = B(14) + h - k['mgz0']
        end = B(14) + mgz_hits[n + 1] - k['mgz0'] if n < 2 else B(16.5) - 6
        e.O(Txt(at, end, chain_imgs[n], W * 0.80, H * 0.14, enter='pop', leave='pop', centre=True, dur=8))
    e.O(Txt(B(14) + mgz_hits[2] - k['mgz0'] + 4, B(16.5) - 6, pill('CHAIN', JADE, 64), W * 0.80, H * 0.14 + 170, enter='up', centre=True))

    def three(f, s, ed):
        return bands_v(ed, f, [(B(16.5) + n * bt, (lambda nm, s0: lambda lf, ow, oh: band_right(nm, s0 + lf, ow, oh))(nm, hit - 2 * bt), lab)
                               for n, (nm, hit, lab) in enumerate(TRI_STRIKE)])

    e.S(Custom(B(16.5), B(18.5), three, trans='push', tdur=12, tdir='left'))

    tall('hcz-loop', 'hcz0', 18.5, 20)
    tall('cpz-spindash', 'cpz0', 20, 21)
    tall('ghz2-buzz', 'ghzm0', 21, 22)
    tall('ehz2-corkscrew', 'ehzc0', 22, 24)
    tall('mhz-spring', 'mhzs0', 24, 26)
    tall('cnz-bumpers', 'cnz0', 26, 28, x0=116.0)

    # ================= TALON =======================================================================
    syz, syz0 = 'syz-talon', k['syz0']
    inset0 = B(29.5)
    tall(syz, 'syz0', 28, 31)
    intro(e, 'talon', B(28), B(31), inset0 - B(28), False)
    e.O(Txt(inset0, B(31) - 6, pill('IN SONIC 1, TOO', SLATE, 60), W * 0.5, H - 250, enter='up', leave='fade', centre=True))

    def lives(c, f, o, ed):                   # the lives display, which the tall frame drops: whole, as an inset
        im = clip(syz).frame(syz0 + f - B(28)).crop((8, 196, 80, 222)).resize((504, 182), Image.NEAREST)
        pop_panel(c, im, (W - 514) / 2, H - 530, f, o.f0, None, 6, YEL2)

    e.O(Fn(inset0, B(31) - 6, lives))

    tall('htz-talon-dive', 'htz0', 31, 32)
    tall('dez-talon', 'dezt0', 32, 34)
    tall('arz-talon-whisp', 'arzt0', 34, 36)

    # ================= EVERY SCREEN ================================================================
    LOCK = [(B(36), 'cpz-lock-stock', 'cpz-lock-mod', k['lockA']), (B(37), 'cpz-lock-stock', 'cpz-lock-mod', k['lockB']),
            (B(38), 'ehz-lock-stock', 'ehz-lock-mod', k['lockC'])]

    def lockstep(f, s, ed):
        t0, st, md, s0 = [x for x in LOCK if x[0] <= f][-1]
        i = s0 + f - t0
        mx, my = subject(md, i)
        sx, sy = subject(md, i, 'sk_')
        cx = (mx + sx) / 2 if abs(mx - sx) < 110 else mx

        def side(name):
            # rows 52-224: under the HUD; never left of x 64: the lives display is out
            return lambda lf, ow, oh: arr(resample(clip(name).frame(i), clamp(cx - 86 * ow / oh, 64, 320 - 172 * ow / oh), 52, 172 * ow / oh, 172, ow, oh))
        return bands_v(ed, f, [(s.f0 - 100, side(st), 'ORIGINAL'), (s.f0 - 100, side(md), ('MICA & TALON', JADE, WHITE))], top=True)

    e.S(Custom(B(36), B(40), lockstep, trans='wipe', tdur=16))
    e.O(CardHeaderV(B(36) + 4, B(37) + 30, 'EVERY SCREEN', sub='REDRAWN'))
    e.O(Shade(B(38), B(40) - 6, 'bottom'))
    for n, s_ in enumerate(('SAME INPUTS. SAME PHYSICS.', 'EVERY FRAME.')):
        e.O(Txt(B(38) + 6 * n, B(40) - 6, line(s_, 72), W / 2, H - 330 + 100 * n, enter='up', leave='fade', centre=True, dur=12))

    def titles3(f, s, ed):                    # three whole title screens, one per band, a beat apart
        return bands_v(ed, f, [
            (B(40), lambda lf, ow, oh: view(clip('title-s1').frame(392 + lf), 160, 72, 224 / 147, ow, oh, 0, 147), 'SONIC 1'),
            (B(40) + bt, lambda lf, ow, oh: view(clip('title-s2').frame(840 + lf), 160, 116, 224 / 180, ow, oh, 26, 206), 'SONIC 2'),
            # The whole S3K title needs the full width, where its stock Tornado fly-by is in view (src 412-505 on
            # the left, 696-775 on the right): this band plays from src 506, while the plane is behind the emblem.
            (B(40) + 2 * bt, lambda lf, ow, oh: view(clip('title-s3k').frame(506 + lf), 160, 93, 224 / 186, ow, oh, 0, 186), 'SONIC 3 & K')], top=True)

    e.S(Custom(B(40), B(42), titles3, trans='push', tdur=12, tdir='left'))

    def signs(f, s, ed):                      # two whole screens, stacked, from mid-spin
        c = ground(f)
        for n, (t0, name, src, label) in enumerate(((s.f0, 'ghz-clear', 227, 'SONIC 1'), (s.f0 + 10, 'ehz-clear', 387, 'SONIC 2'))):
            if f < t0:
                continue
            im = clip(name).frame(src + f - t0)
            ph = round(179 * W / 320)
            y = 190 + n * (ph + 190)
            x = int(round(-(1 - ease_out(clamp((f - t0) / 10))) * W))
            pic = arr(resample(im, 0, 0, 320, 179, W, ph))
            vis = W + x
            if vis > 0:
                c[y - 14:y, :vis] = np.array(YEL2, np.float32)
                c[y:y + ph, :vis] = pic[:, -x:] if x < 0 else pic
                c[y + ph:y + ph + 14, :vis] = np.array(YEL2, np.float32)
            p = chip(label)
            paste(c, p, (W - p.shape[1]) / 2 + x, y + ph + 40, clamp((f - t0 - 8) / 8))
        return c

    e.S(Custom(B(42), B(43), signs))

    def tally(f, s, ed):                      # the whole native screen: nothing of the results lettering is cropped
        c = ground(f)
        ph = whole(c, clip('ehz-clear').frame(471 + f - s.f0), (0, 224), 520, rules=True)
        p = chip('SONIC 2')
        paste(c, p, (W - p.shape[1]) / 2, 520 + ph + 54)
        return c

    e.S(Custom(B(43), B(44), tally))

    def stages(f, s, ed):
        return bands_v(ed, f, [
            (B(44), lambda lf, ow, oh: view(clip('ghz-ss').frame(900 + lf), 160, 112, 224 / 187, ow, oh, 0, 224), 'SONIC 1'),
            (B(44) + bt, lambda lf, ow, oh: view(clip('halfpipe-run').frame(740 + lf), 160, 134, 1.5, ow, oh, 44, 224), 'SONIC 2'),   # its 256-px picture, side borders out
            (B(44) + 2 * bt, lambda lf, ow, oh: view(clip('blue-sphere').frame(430 + lf), 160, 140, 1.2, ow, oh, 34, 224), 'SONIC 3 & K')])

    e.S(Custom(B(44), B(46), stages, trans='push', tdur=12, tdir='left'))

    def screens(f, s, ed):                    # four wide strips, a beat apart
        c = ground(f)
        t0 = s.f0
        cells = [(clip('continue'), 60, 'CONTINUE', (160, 104, 1.0)), (clip('data-select'), 405, 'DATA SELECT', (201, 116, 2.75)),
                 (clip('halfpipe-run'), 1010, 'SPECIAL STAGE HUD', (160, 56, 1.25)), (clip('cpz-talon'), 60, 'LIVES', (62, 200, 4.6))]
        pw_, ph_ = 956, 370
        for n, (cl, src, label, (cx, cy, z)) in enumerate(cells):
            tn = t0 + n * bt
            if f < tn:
                continue
            img = game_view(cl.frame(src + f - tn), cx, cy, z, pw_, ph_)
            pop_panel(c, img, (W - pw_) / 2 - 5, 52 + n * (ph_ + 96), f, tn, label, 5, YEL2)
        return c

    e.S(Custom(B(46), B(48), screens, trans='push', tdur=12, tdir='left'))

    tall('scz-chain', 'scz0', 48, 50, lead=0, sm=16)
    e.O(Txt(B(49) + 2 * bt, B(50) - 6, pill('TALON FLIES THE TORNADO', SLATE, 52), W / 2, H * 0.90, enter='up', leave='fade', centre=True))
    e.S(Custom(B(50), B(51), lambda f, s, ed: window_on_ground(clip('ending').frame(k['end_side'] + f - s.f0), (0, 60, 200, 200), 560)))
    e.S(Custom(B(51), B(52), lambda f, s, ed: window_on_ground(clip('ending').frame(k['end_pose'] + f - s.f0), (60, 12, 280, 196), 380)))
    e.O(Txt(B(51) + bt + 4, B(52) - 4, pill('ENDINGS, TOO', JADE, 68), W / 2, 1480, enter='pop', leave='fade', centre=True, dur=8))

    # ================= BUILD =======================================================================
    tall('mtz-run', 'mtz0', 52, 54)
    tall('lbz-slope', 'lbzs0', 54, 56)
    tall('cnz-bumpers', 'cnzr0', 56, 57, x0=116.0)
    tall('ehz2-corkscrew', 'buz0', 57, 58.5)

    # ================= POWERED UP ==================================================================
    tall('hcz-gilded-runin', 'g0', 58.5, 62)
    e.O(Flash(B(60), 10, 0.45))
    e.O(CardHeaderV(B(60) + 12, B(61) + 10, 'POWERED UP', sub='50 RINGS  MID-ACT'))
    e.O(Txt(B(61) + 14, B(62) - 6, pill('GILDED MICA', GOLD2, 64, fg=NAVY), W / 2, H * 0.88, enter='up', leave='fade', centre=True))

    def trails(f, s, ed):
        return bands_v(ed, f, [(B(62), lambda lf, ow, oh: band_right('aiz-normal', k['trn0'] + lf, ow, oh, vw=170), ('NORMAL: JADE TRAIL', JADE, WHITE)),
                               (B(62.5), lambda lf, ow, oh: band_right('aiz-gilded', k['trg0'] + lf, ow, oh, vw=170), ('GILDED: GOLD TRAIL', GOLD2, NAVY))])

    e.S(Custom(B(62), B(64), trails, trans='push', tdur=12, tdir='left'))

    tall('slz-gilded', 'slz0', 64, 65)
    tall('arz-gilded', 'arzg0', 65, 66)
    tall('cpz-gilded', 'cpzg0', 66, 67.5)

    tall('aiz-solar-reveal', 'sol0', 67.5, 70)
    e.O(Flash(B(68), 10, 0.45))
    e.O(Txt(B(68) + 30, B(70) - 6, pill('SOLAR TALON', (255, 146, 36), 64, fg=NAVY), W / 2, H * 0.88, enter='up', leave='fade', centre=True))
    tall('dez-solar', 'dezs0', 70, 72)
    tall('syz-solar', 'syzs0', 72, 73)
    tall('htz-solar', 'htzs0', 73, 74)
    tall('fbz-solar', 'fbz0', 74, 75.25)

    # ================= HERO ========================================================================
    tall('dez-hyper', 'h0', 75.25, 78)
    e.O(Flash(B(76), 10, 0.5))
    e.O(Txt(B(76) + 30, B(78) - 6, pill('HYPER MICA', ROSE, 64), W / 2, H * 0.88, enter='up', leave='fade', centre=True))

    # The boss: the window follows her run-in between native x 112 and 140, then holds from the hit. From the hit
    # the ONE HIT. card covers native x >= BOSS_CARD_X (she travels right under it); its edge is upright here.
    boss, b0 = 'lbz-boss', k['b0']
    HIT = b0 + (B(79) - B(78))

    HOP = HIT - 14

    def boss_x0(i):
        x, _ = subject(boss, min(i, HOP), '', 10)
        x0 = clamp(x - 100, 112.0, 140.0)
        return x0 + (130.0 - x0) * smooth(clamp((i - HOP) / 14))    # settles on x 130-256 by the hit: boss and hero whole, room for the card

    e.S(Custom(B(78), B(80), lambda f, s, ed: arr(resample(clip(boss).frame(b0 + f - s.f0), boss_x0(b0 + f - s.f0), 0, PW, 224, W, H))))
    e.O(Flash(B(79), 10, 0.55))
    CX = int(round((BOSS_CARD_X - boss_x0(HIT)) * SV))
    for OS in range(300, 100, -10):
        one_im = text('ONE', 'title', OS, WHITE, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
        hit_im = text('HIT.', 'title', OS, YELLOW, stroke=11, sfill=NAVY, shadow=12, scol=(0, 0, 30, 230), tracking=6)
        if max(one_im.shape[1], hit_im.shape[1]) <= W - CX - 46 - 40:
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
            u = (t - 5 - n * bt / 2) / 7
            if u <= 0:
                continue
            sc = 0.8 + 0.2 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            paste(c, im2, cx - im2.shape[1] / 2, yy - im2.shape[0] / 2, clamp(u * 2))

    e.O(Fn(B(79), B(80), hit_card))

    # The pair: a closer two-shot for the twin transformation (native x 111-217, rows 0-188: the HUD is out
    # whole), then the tall frame from the catch.
    pair, p0 = 'lbz-pair', k['p0']
    white_n = 74 - p0
    CUTV = 131                                # three frames after the catch (#128)

    def pair_v(f, s, ed):
        i = p0 + f - s.f0
        if i < CUTV:
            return close_v(pair, i, 111 + 188 * 1080 / 1920 / 2, y0=0, vh=188)
        return pv(pair, i, x0=116.0)

    e.S(Custom(B(80), B(84), pair_v))

    def white_in(c, f, o, ed):
        t = f - o.f0
        a = 1.0 if t < white_n else 1.0 - (t - white_n) / 9
        c *= (1 - a)
        c += 255 * a

    e.O(Fn(B(80), B(80) + white_n + 9, white_in))
    tag_m, tag_t = pill('HYPER MICA', ROSE, 60), pill('SOLAR TALON', (255, 146, 36), 60, fg=NAVY)

    def pair_tags(c, f, o, ed):
        i = p0 + f - B(80)
        t, out = f - o.f0, o.f1 - f
        for n, (im, key) in enumerate(((tag_m, ''), (tag_t, 'sk_'))):
            u = (t - n * bt) / 9
            if u <= 0:
                continue
            x, y = subject(pair, i, key, 6)
            sc = 0.7 + 0.3 * back(u, 2.0) if u < 1 else 1.0
            im2 = scaled(im, sc) if sc != 1.0 else im
            px = clamp((x + 22 - 116) * SV, 20, W - im.shape[1] - 20)
            paste(c, im2, px + (im.shape[1] - im2.shape[1]) / 2, (y - 2) * SV - im2.shape[0] / 2, clamp(u * 2) * clamp(out / 8))

    e.O(Fn(B(81), B(83), pair_tags))

    # ================= END CARD ====================================================================
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = (1.0 - 0.45 * np.clip(np.hypot((xs - W / 2) / (W * 0.85), (ys - H * 0.40) / (H * 0.60)), 0, 1) ** 1.4)[..., None]
    endc = CARDS.EndCard(W, H)

    def endcard(f, s, ed):
        kf = pair_frame(k['pair_end'] + (f - s.f0))
        c = blurred(clip(pair).frame(kf), ed, radius=1.8, dim=0.66, cx=116 + PW / 2, cy=112, zoom=1.0) * vig
        return endc.draw(np.clip(c, 0, 255).astype(np.uint8), f - s.f0).astype(np.float32)

    e.S(Custom(B(84), k['end_f'], endcard, trans='iris', tdur=24))
    e.O(Fade(B(87), B(88) + 6))
    e.O(Fn(B(88) + 6, 10 ** 6, lambda c, f, o, ed: c.__imul__(0)))
