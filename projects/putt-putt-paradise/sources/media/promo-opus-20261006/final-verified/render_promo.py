#!/usr/bin/env python3
"""Putt Putt Paradise public promo, final verified revision (Opus, 2026-10-06, r5).

Composites the r5 captures (one lossless PNG and one 800-sample stereo PCM packet per 60 Hz
row, recorded from the production GameLoop with the real headless SMPS backend) and a short
OpenGGF 0.6 Sonic 2 engine opener into a 1920x1080 / 60 fps film.

Rules the edit keeps:
- Gameplay plays at normal speed: one captured row is one output frame, and its sound is that
  row's own packet. Captures are addressed in one "unified" row space per capture: the title
  rows first, then the course rows, exactly as they were recorded back to back, so the menu,
  the engine's exit fade, the Sonic 2 title card and the course play as one take.
- Cuts crossfade the real game audio with equal-power fades. Where both sides carry Emerald Hill
  music at normal tempo, the incoming clip shifts by under half a beat so the bed keeps its pulse.
- Editorial audio (declared in promo.audio.json): the Title Screen theme under the engine opener,
  the Option Screen theme under the end card, and a Spindash Release whoosh on chapter cards.
  All are rendered from the same Sonic 2 ROM by OpenGGF's SMPS driver (tools/).

  render_promo.py edl                write the resolved timeline (promo.edl.json, chapters)
  render_promo.py frames N [N ...]   write single output frames to build/check/
  render_promo.py sheet [step]       contact sheet of output frames (promo.cuts.png)
  render_promo.py clip A B           render output frames A..B-1 to build/check/clip.mp4 with audio
  render_promo.py audio              mix the soundtrack (promo.soundtrack.wav)
  render_promo.py render [--out F]   full render to MP4 (H.264 + AAC) and an FFV1/PCM master MKV

Environment: PROMO_SHOW overrides the capture directory (default showcase-20261006-opus-final);
PROMO_WORKERS sets the frame pool size (default 6).
"""
import json
import math
import os
import subprocess
import sys
import wave
from bisect import bisect_right
from dataclasses import dataclass, field
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
SHOW = Path(os.environ.get("PROMO_SHOW", BASE / "showcase-20261006-opus-final"))
EDITORIAL = ROOT / "audio"
MASTER = Path.home() / "Videos/OGGF/S2-0.6/s2-0.6-V2.mov"
BUILD = ROOT / "build"
REPO = Path("/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise")
BADGE = REPO / "src/main/resources/icon/openggf-256.png"
W, H, FPS, SR = 1920, 1080, 60, 48000
SPF = SR // FPS  # 800 stereo frames per output frame == one captured row
BEAT = 25.93     # Emerald Hill Zone beat in 60 Hz rows (measured from the ROM-rendered stem)
WORKERS = int(os.environ.get("PROMO_WORKERS", "6"))

FONT_DIR = "/usr/share/fonts/TTF/"
F_TITLE = "FiraSansCompressed-Heavy.ttf"
F_TITLE_IT = "FiraSansCompressed-HeavyItalic.ttf"
F_SUB = "FiraSansCondensed-BoldItalic.ttf"
F_BODY = "FiraSans-Bold.ttf"
F_MONO = "Hack-Regular.ttf"

WHITE, CREAM, GOLD = (255, 255, 255), (255, 243, 203), (255, 212, 91)
NIGHT, INK = (11, 34, 48), (8, 20, 34)
SONIC, TAILS, CYAN = (92, 146, 255), (244, 162, 60), (97, 215, 237)
# Sonic 2's title card, sampled from the captured TITLE_CARD rows (RAW_RGB), softened a touch.
CARD_BLUE, CARD_YELLOW, CARD_RED = (48, 87, 206), (255, 226, 30), (232, 22, 30)

CAPTURES = {
    "e1": SHOW / "ehz1-practice", "e2": SHOW / "ehz2-practice", "lm": SHOW / "local-match",
    "oh": SHOW / "online/online-host", "og": SHOW / "online/online-guest",
}
if os.environ.get("PROMO_DEV"):  # Layout work only: r4 stand-ins for captures not yet recorded.
    _r4 = BASE / "showcase-20261006-opus-polish"
    CAPTURES.update({"e2": _r4 / "ehz2-practice", "lm": _r4 / "local-match",
                     "oh": _r4 / "online/online-host", "og": _r4 / "online/online-guest"})


# ------------------------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(u):
    u = clamp(u); return 1 - (1 - u) ** 3


def ease_in(u):
    u = clamp(u); return u ** 3


def smooth(u):
    u = clamp(u); return u * u * (3 - 2 * u)


def back(u, s=1.7):
    u = clamp(u) - 1; return u * u * ((s + 1) * u + s) + 1


def lerp(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------------------------------ sources
@lru_cache(maxsize=None)
def title_rows(cap):
    """Title rows recorded before the course (the unified offset of course row 0)."""
    with wave.open(str(CAPTURES[cap] / "title.wav")) as w:
        return w.getnframes() // SPF


def G(cap, r):
    """Unified index of course row r."""
    return title_rows(cap) + r


def ev(cap, name, k=0):
    """Course row of the k-th occurrence of a capture event."""
    return events(cap)[name][k]


# The edit was cut against course rows of the r4 captures, whose practice and local runs reached
# "course-ready" at row 120. Later builds open the first lie at the mod's own (later) settle point,
# and every scripted input after it is relative, so a pick is that offset from "course-ready".
R4_COURSE_READY = 120


def at(cap, r4_row):
    """Unified row in this capture for an r4 course row of a practice/local run."""
    return G(cap, ev(cap, "course-ready") + r4_row - R4_COURSE_READY)


@lru_cache(maxsize=192)
def row(cap, u):
    t = title_rows(cap)
    path = CAPTURES[cap] / ("title-frames" if u < t else "frames") / f"{(u if u < t else u - t):06d}.png"
    return Image.open(path).convert("RGB")


@lru_cache(maxsize=None)
def unified_audio(cap):
    out = []
    for name in ("title.wav", "gameplay.wav"):
        with wave.open(str(CAPTURES[cap] / name)) as w:
            assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2
            out.append(np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768)
    return np.concatenate(out)


@lru_cache(maxsize=None)
def requests(cap):
    """Audio requests in unified rows: (u, class, id)."""
    t, out = title_rows(cap), []
    for line in (CAPTURES[cap] / "audio-requests.csv").read_text().splitlines()[1:]:
        phase, r, kind, ident = line.split(",")
        if phase == "title":
            out.append((int(r), kind, ident))
        elif phase == "gameplay":
            out.append((t + int(r), kind, ident))
    return out


@lru_cache(maxsize=None)
def events(cap):
    out = {}
    for line in (CAPTURES[cap] / "events.csv").read_text().splitlines()[1:]:
        r, name = line.split(",", 1)
        out.setdefault(name, []).append(int(r))
    return out


@lru_cache(maxsize=None)
def title_modes(cap):
    rows = []
    for line in (CAPTURES[cap] / "title-rows.csv").read_text().splitlines()[1:]:
        r, mode, fade, exiting = line.split(",")
        rows.append((int(r), mode, fade == "true", exiting == "true"))
    return rows


def start_press(cap):
    """Unified row of the START press: the first title row whose provider reports exiting."""
    return next(r for r, mode, fade, exiting in title_modes(cap) if exiting)


def card_rows(cap):
    """Unified rows of the engine's Sonic 2 TITLE_CARD mode."""
    rows = [r for r, mode, fade, exiting in title_modes(cap) if mode == "TITLE_CARD"]
    return rows[0], rows[-1]


@lru_cache(maxsize=64)
def master(shot, i):
    files = sorted((BUILD / "master" / shot).glob("*.png"))
    return Image.open(files[int(clamp(i, 0, len(files) - 1))]).convert("RGB")


def bed_phase(cap, u):
    """Beat phase (rows) of the Emerald Hill bed at unified row u, or None when unknown, sped up
    or interrupted by a jingle."""
    starts = [r for r, k, i in requests(cap) if k == "MUSIC" and i == "0x81"]
    i = bisect_right(starts, u) - 1
    if i < 0:
        return None
    for r, k, ident in requests(cap):
        if starts[i] < r <= u and (k == "MUSIC" and ident != "0x81" or k == "COMMAND" and ident in ("0xFB", "0xFC")):
            return None
    first_sound = starts[i] + 7  # The SMPS bed's first audible tick trails the request (measured: 421 -> 428).
    return (u - first_sound) % BEAT


# ------------------------------------------------------------------------------------ pixels
def resample(img, x0, y0, vw, vh, ow, oh):
    """Pixel-art scaling: nearest up by an integer factor, then an area filter to the output."""
    k = max(1, math.ceil(ow / vw - 1e-9))
    ix0, iy0 = math.floor(x0), math.floor(y0)
    ix1, iy1 = min(img.width, math.ceil(x0 + vw)), min(img.height, math.ceil(y0 + vh))
    crop = img.crop((ix0, iy0, ix1, iy1)).resize(((ix1 - ix0) * k, (iy1 - iy0) * k), Image.NEAREST)
    box = ((x0 - ix0) * k, (y0 - iy0) * k, (x0 - ix0 + vw) * k, (y0 - iy0 + vh) * k)
    return crop.resize((max(1, round(ow)), max(1, round(oh))), Image.BOX, box=box)


@lru_cache(maxsize=1)
def stripes():
    tile = Image.new("RGB", (W + 400, H), NIGHT)
    d = ImageDraw.Draw(tile)
    top, bottom = np.array((9, 27, 46)), np.array((14, 52, 60))
    for y in range(H):
        d.line((0, y, W + 400, y), fill=tuple(int(v) for v in top + (bottom - top) * (y / H)))
    over = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    for x in range(-H, W + 400, 64):
        od.polygon([(x, H), (x + 28, H), (x + 28 + H, 0), (x + H, 0)], fill=(255, 255, 255, 9))
    return Image.alpha_composite(tile.convert("RGBA"), over).convert("RGB")


def background(f):
    shift = int(f * 0.6) % 64
    return stripes().crop((shift, 0, shift + W, H))


def blurred(img, dim=0.55):
    """A soft, darkened full-bleed copy of a game frame, for backdrops."""
    bg = img.resize((W // 8, round(W // 8 * img.height / img.width)), Image.BILINEAR)
    bg = bg.filter(ImageFilter.GaussianBlur(5)).resize((W, round(W * img.height / img.width)), Image.BILINEAR)
    top = (bg.height - H) // 2
    return Image.blend(bg.crop((0, top, W, top + H)), Image.new("RGB", (W, H), INK), dim)


@lru_cache(maxsize=16)
def shadow_box(w, h, radius=22, alpha=150):
    m = Image.new("L", (w + 40, h + 40), 0)
    ImageDraw.Draw(m).rectangle((20, 20, 20 + w, 20 + h), fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(radius))
    return Image.merge("RGBA", (Image.new("L", m.size, 0),) * 3 + (m,))


def window_at(canvas, img, x, y, w, border=GOLD, edge=5):
    """Game window at an arbitrary rectangle with a drop shadow and a thin gold frame."""
    w = int(round(w)); h = int(round(w * img.height / img.width)); x = int(round(x)); y = int(round(y))
    sh = shadow_box(w, h)
    canvas.paste(sh, (x - 10, y - 6), sh)
    if edge:
        ImageDraw.Draw(canvas).rectangle((x - edge, y - edge, x + w + edge - 1, y + h + edge - 1), fill=border)
    canvas.paste(resample(img, 0, 0, img.width, img.height, w, h), (x, y))
    return h


def blur_fill(img):
    canvas = blurred(img)
    gw = round(H * img.width / img.height)
    sh = shadow_box(gw, H)
    canvas.paste(sh, ((W - gw) // 2 - 20, -20), sh)
    canvas.paste(resample(img, 0, 0, img.width, img.height, gw, H), ((W - gw) // 2, 0))
    return canvas


# ------------------------------------------------------------------------------------ type
@lru_cache(maxsize=None)
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


@lru_cache(maxsize=768)
def text(s, fname, size, fill=WHITE, stroke=0, shadow=0, scol=(0, 0, 0), stroke_fill=(10, 18, 30)):
    f = font(fname, size)
    l, t, r, b = f.getbbox(s, stroke_width=stroke)
    pad = stroke + shadow + 6
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + shadow, pad - t + shadow), s, font=f, fill=scol + (170,),
                                stroke_width=stroke, stroke_fill=scol + (170,))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(max(1, shadow // 2))))
    ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=fill + (255,), stroke_width=stroke,
                            stroke_fill=stroke_fill + (255,))
    return im


def put(canvas, im, x, y, alpha=1.0, anchor="lt"):
    if alpha <= 0.002:
        return
    if anchor == "mt":
        x -= im.width // 2
    elif anchor == "rt":
        x -= im.width
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    canvas.paste(im, (int(round(x)), int(round(y))), im)


def fitted(s, fname, size, max_width, **kw):
    while size > 20 and text(s, fname, size, **kw).width > max_width:
        size -= 4
    return text(s, fname, size, **kw)


# ------------------------------------------------------------------------------------ captions
def zigzag(h, w, teeth=7):
    """The serrated right edge of Sonic 2's red title-card strip, as a polygon."""
    pts = [(0, 0)]
    step = h / teeth
    for i in range(teeth):
        pts += [(w, i * step), (w - w * 0.45, (i + 0.5) * step)]
    pts += [(w, h), (0, h)]
    return pts


def card_caption(canvas, local, start, end, lines, x, y, size=118, sub=None, sub_size=40, max_width=1500,
                 align="left", sub_max=None):
    """A caption in the style of Sonic 2's title card: a red serrated tab drops in, the blue band
    wipes across behind the heavy italic heading, and a yellow strip slides in from the other side
    carrying the subtitle. Everything slides back out over the last 14 frames."""
    if local < start or local >= end:
        return
    age, left = local - start, end - local
    out = ease_in((14 - left) / 14) if left < 14 else 0.0
    heads = [fitted(s, F_TITLE_IT, size, max_width, fill=WHITE, stroke=5, shadow=6) for s in lines]
    hw = max(im.width for im in heads)
    gap = int(size * 0.80)
    band_h = gap * (len(lines) - 1) + heads[-1].height - 6
    subim = fitted(sub, F_SUB, sub_size, sub_max or max(hw + 40, 520), fill=INK, stroke=0) if sub else None
    sub_h = (subim.height + 4) if subim else 0
    band_w = hw + 90
    if align == "right":
        x -= band_w
    exit_dx = -out * (band_w + 300) if align == "left" else out * (band_w + 300)
    layer = Image.new("RGBA", (band_w + 260, band_h + sub_h + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = 40, 10
    # Blue band: wipes across from the tab side.
    reveal = ease_out((age - 2) / 13)
    if reveal > 0:
        bw = int(band_w * reveal)
        d.polygon([(ox, oy), (ox + bw + 34, oy), (ox + bw, oy + band_h), (ox, oy + band_h)], fill=CARD_BLUE + (238,))
    # Yellow strip: slides in from the far side under the band.
    if subim:
        yu = ease_out((age - 8) / 14)
        if yu > 0:
            yw = subim.width + 70
            sx = ox + 18 + int((1 - yu) * 380)
            d.polygon([(sx, oy + band_h), (sx + yw + 26, oy + band_h), (sx + yw, oy + band_h + sub_h), (sx - 26, oy + band_h + sub_h)],
                      fill=CARD_YELLOW + (250,))
            sa = clamp((age - 13) / 8)
            if sa > 0:
                s2 = subim.copy(); s2.putalpha(subim.getchannel("A").point(lambda v: int(v * sa)))
                layer.paste(s2, (sx + 22, oy + band_h + 1), s2)
    # Heading lines: slide in over the band, staggered.
    for i, im in enumerate(heads):
        hu = back((age - 5 - i * 4) / 14)
        a = clamp((age - 5 - i * 4) / 6)
        if a > 0:
            h2 = im if a >= 0.999 else im.copy()
            if a < 0.999:
                h2.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            layer.paste(h2, (ox + 26 - int((1 - hu) * 120), oy - 8 + i * gap), h2)
    # Red serrated tab: drops in first and stays as the caption's spine.
    tu = back(age / 11)
    if tu > 0:
        tab_h = band_h + sub_h + 16
        tab = Image.new("RGBA", (40, tab_h), (0, 0, 0, 0))
        ImageDraw.Draw(tab).polygon(zigzag(tab_h, 40, max(3, tab_h // 26)), fill=CARD_RED + (255,))
        layer.paste(tab, (ox - 34, oy - 8 - int((1 - tu) * 120)), tab)
    put(canvas, layer, x - ox + exit_dx, y - oy, alpha=1 - out * 0.6)


def pill(canvas, local, start, end, label, x, y, colour=GOLD, size=40, ink=INK, right=None):
    if local < start or local >= end:
        return
    im = text(label, F_TITLE, size, ink)
    if right is not None:
        x = right - (im.width + 38)
    age, left = local - start, end - local
    w, h = im.width + 26, im.height - 2
    t = back(age / 12)
    a = clamp(age / 6) * clamp(left / 10)
    plate = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle((6, 6, 6 + w, 6 + h), radius=10, fill=colour + (255,))
    plate.paste(im, (19, 2), im)
    put(canvas, plate, x + (1 - t) * 60, y, alpha=a)


def small(canvas, local, start, s, x, y, size=26, colour=CREAM, anchor="lt", end=10**9):
    if local < start or local >= end:
        return
    put(canvas, text(s, F_BODY, size, colour, stroke=2), x, y, alpha=clamp((local - start) / 12) * clamp((end - local) / 10),
        anchor=anchor)


# ------------------------------------------------------------------------------------ timeline
@dataclass
class Seg:
    name: str
    frames: int
    trans: str = "cut"                # transition into this segment
    tlen: int = 0
    chapter: str = ""
    source: str = ""
    draw_fn: object = None            # non-gameplay: draw(local) -> RGB image
    audio: list = field(default_factory=list)   # extra/editorial: [(wav, src_frame, local_frame, count, gain)]
    cap: str = None                   # gameplay: capture key and first unified row
    u0: int = 0
    layout: object = None
    extra: object = None
    gain: float = 1.0
    shift: int = 0                    # beat-alignment shift applied to u0 (rows)
    start: int = 0
    card: str = None                  # chapter card label shown during a "card" transition into this segment
    card_sub: str = None              # the yellow line under it (default PUTT PUTT PARADISE)
    align: bool = True                # take part in Emerald Hill beat alignment

    def draw(self, local):
        if self.cap is None:
            return self.draw_fn(local)
        u = self.u0 + local
        canvas = self.layout(row(self.cap, u), local)
        if self.extra:
            self.extra(canvas, local, u)
        return canvas

    def game_audio(self):
        return None if self.cap is None else (self.cap, self.u0, self.frames)


def cinema(img, local=0):
    """HUD-free 16:9 action framing: the middle 300x169 game pixels (6.4x)."""
    return resample(img, 10, 30, 300, 169, W, H)


def push_in(t0, dur):
    """Full frame with its HUD first, then an eased push into the HUD-free action crop."""
    def layout(img, local):
        u = smooth((local - t0) / dur)
        if u <= 0:
            return blur_fill(img)
        x0, y0 = 10 * u, 30 * u
        w, h = 320 - 20 * u, 224 - 55 * u
        scale = min(W / w, H / h)
        ow, oh = round(w * scale), round(h * scale)
        canvas = blurred(img) if ow < W - 2 else Image.new("RGB", (W, H))
        canvas.paste(resample(img, x0, y0, w, h, ow, oh), ((W - ow) // 2, (H - oh) // 2))
        return canvas
    return layout


def framed(x=60, y=118, w=1280, seed=0):
    def layout(img, local):
        canvas = background(local + seed)
        window_at(canvas, img, x, y, w)
        return canvas
    return layout


# Panel geometry for framed chapters: game window on the left, a 470 px information column.
PX = 1392


def steps_panel(canvas, local, u, steps, cap, x=PX, y=372):
    for i, (name, desc, a, b) in enumerate(steps):
        a, b = at(cap, a), at(cap, b) if b < 10**8 else 10**9
        on, done = a <= u < b, u >= b
        col = GOLD if on else (CREAM if done else (110, 140, 150))
        plate = Image.new("RGBA", (470, 100), (0, 0, 0, 0))
        pd = ImageDraw.Draw(plate)
        pd.rounded_rectangle((0, 0, 469, 99), radius=14, fill=(20, 58, 72, 240) if on else (12, 30, 42, 205),
                             outline=GOLD if on else (40, 80, 92), width=3)
        num = text(str(i + 1), F_TITLE_IT, 52, INK if on else col)
        if on:
            pd.ellipse((14, 18, 74, 78), fill=GOLD)
        plate.paste(num, (44 - num.width // 2, 48 - num.height // 2), num)
        t = text(name, F_TITLE, 44, col)
        plate.paste(t, (88, 4), t)
        sub = text(desc, F_BODY, 23, CREAM if on or done else (120, 150, 160))
        plate.paste(sub, (92, 60), sub)
        pop = back((u - a) / 10) if on else 1
        put(canvas, plate, x + (1 - pop) * 36, y + i * 112, alpha=clamp((local - 6 - i * 5) / 10))


def build():
    segs = []
    e1t, e2t = title_rows("e1"), title_rows("e2")

    # ---- A. Cold open: OpenGGF plays Sonic 2 (engine 0.6 footage, muted; ROM Title Screen theme).
    shots = [("ehz", 12, 84), ("cnz", 1218, 78), ("special", 1440, 78), ("sky", 3360, 100)]
    def opener(local):
        acc = 0
        for name, first, count in shots:
            if local < acc + count:
                img = master(name, local - acc); break
            acc += count
        canvas = Image.blend(img, Image.new("RGB", (W, H), INK), 0.40)
        size = 360
        t = back((local - 8) / 18)
        if t > 0:
            b = badge_img(size).resize((max(1, int(size * t)),) * 2, Image.BICUBIC)
            put(canvas, b, W // 2 - b.width // 2, 104 + (size - b.width) // 2)
        put(canvas, text("THE OPEN-SOURCE ENGINE FOR CLASSIC SONIC", F_TITLE, 96, WHITE, stroke=6, shadow=9), W // 2, 510,
            alpha=clamp((local - 28) / 10), anchor="mt")
        put(canvas, text("Sonic 2, rebuilt in Java · running from your own ROM", F_SUB, 54, GOLD, stroke=4, shadow=6),
            W // 2, 660, alpha=clamp((local - 92) / 14), anchor="mt")
        put(canvas, text("Now it runs mods. Here's one.", F_SUB, 60, WHITE, stroke=4, shadow=6),
            W // 2, 790, alpha=clamp((local - 220) / 14), anchor="mt")
        return canvas
    segs.append(Seg("cold-open", sum(c for _, _, c in shots), "fade", 20,
                    "OpenGGF: the open-source engine for classic Sonic", "OpenGGF 0.6 Sonic 2 promo master (muted)",
                    draw_fn=opener, audio=[(EDITORIAL / "s2-music-96.wav", 0, 0, 340, "editorial")]))

    # ---- B. Hook: Sonic is the ball, then Tails (HUD-free action crops, real game audio).
    def hook_sonic(canvas, local, u):
        card_caption(canvas, local, 22, 182, ["WHAT IF SONIC", "WAS THE GOLF BALL?"], 96, 70, size=150)
    segs.append(Seg("hook-sonic", 196, "flash", 16, "What if Sonic was the golf ball?", "ehz1-practice",
                    cap="e1", u0=at("e1", 96), layout=cinema, extra=hook_sonic))
    def hook_tails(canvas, local, u):
        card_caption(canvas, local, 6, 166, ["...OR TAILS?"], 1830, 70, size=150, align="right")
    segs.append(Seg("hook-tails", 176, "whip", 12, "", "ehz2-practice",
                    cap="e2", u0=at("e2", 300), layout=cinema, extra=hook_tails))

    # ---- C. Title drop: the creator menu with its ROM menu music (the four modes browsed), then
    # one take from Practice through START, the engine's own fade, Sonic 2's title card with the
    # Emerald Hill music starting under it, and the first tee.
    press = start_press("e1")
    expand0, expand1 = press + 6, press + 30
    browse_from, browse_to, setup_from = 58, 152, 262  # Mode list browsed; Practice re-selected.
    dissolve = 12
    def title_layout(base):
        def layout(img, local):
            u = base + local
            e = smooth((u - expand0) / (expand1 - expand0))
            big_w = round(H * 320 / 224)
            w = lerp(1280, big_w, e)
            x = lerp(60, (W - big_w) / 2, e); y = lerp(92, 0, e)
            canvas = background(local + 4000 + base)
            if e > 0:
                canvas = Image.blend(canvas, blurred(img), e)
            window_at(canvas, img, x, y, w, edge=int(round(5 * (1 - e))))
            return canvas
        return layout
    def title_text(offset):
        def draw(canvas, local, u):
            t = local + offset  # title-chapter time, continuous across the dissolve
            x = 1396
            fade_out = 1 - smooth((u - expand0) / 14) if u >= expand0 - 1 and u > browse_to else 1
            if fade_out <= 0:
                return
            put(canvas, text("PUTT PUTT", F_TITLE_IT, 116, GOLD, stroke=5, shadow=8), x, 130, alpha=clamp((t - 14) / 10) * fade_out)
            put(canvas, text("PARADISE", F_TITLE_IT, 116, WHITE, stroke=5, shadow=8), x, 228, alpha=clamp((t - 20) / 10) * fade_out)
            put(canvas, text("Sonic 2 Mini Golf", F_SUB, 56, CREAM, stroke=3, shadow=5), x + 4, 356, alpha=clamp((t - 34) / 12) * fade_out)
            put(canvas, text("An example mod for", F_BODY, 34, CREAM, stroke=2, shadow=4), x + 4, 440, alpha=clamp((t - 48) / 12) * fade_out)
            put(canvas, text("the OpenGGF engine", F_BODY, 34, CREAM, stroke=2, shadow=4), x + 4, 484, alpha=clamp((t - 48) / 12) * fade_out)
            for i, (at, label, colour) in enumerate([(62, "PRACTICE", GOLD), (76, "LOCAL 2 PLAYERS", TAILS),
                                                      (90, "ONLINE MATCHES", CYAN)]):
                if fade_out > 0.98:
                    pill(canvas, t, at, 10**9, label, x, 590 + i * 84, colour)
        return draw
    browse = Seg("title", browse_to - browse_from, "card", 36, "Putt Putt Paradise: Sonic 2 Mini Golf",
                 "ehz1-practice title rows: the four modes", cap="e1", u0=browse_from, layout=title_layout(browse_from),
                 extra=title_text(0), card="PUTT PUTT PARADISE", card_sub="SONIC 2 MINI GOLF", align=False)
    segs.append(browse)
    segs.append(Seg("title-start", G("e1", min(112, ev("e1", "course-ready") - 8)) - setup_from, "fade", dissolve, "",
                    "ehz1-practice: Practice setup, START, fade, title card, course (title rows then course rows, one take)",
                    cap="e1", u0=setup_from, layout=title_layout(setup_from), extra=title_text(browse.frames - dissolve),
                    align=False))

    # ---- D. How to play: one continuous chip, the panel follows the real shot stages.
    steps = [("AIM", "Up/Down loft · Left/Right direction", 760, 810),
             ("HIT POINT", "Topspin or backspin", 810, 866),
             ("POWER", "One sweep, one press", 866, 930), ("SPIN DASH!", "The ROM's own rev and release", 930, 962),
             ("ROLL", "Native Sonic 2 physics take over", 962, 10**9)]
    def howto(canvas, local, u):
        card_caption(canvas, local, 0, 10**9, ["ONE BUTTON."], PX + 12, 96, size=100,
                     sub="Kirby's Dream Course-style shots", sub_size=36, max_width=420, sub_max=410)
        steps_panel(canvas, local, u, steps, "e1")
    segs.append(Seg("how-to", 470, "whip", 12, "One button: aim, hit point, power", "ehz1-practice",
                    cap="e1", u0=at("e1", 744), layout=framed(), extra=howto))

    # ---- E. Real physics, a trio of action crops.
    segs.append(Seg("loops", 220, "iris", 24, "Real Sonic 2 physics: loops, springs, badniks", "ehz1-practice",
                    cap="e1", u0=at("e1", 2688), layout=cinema, extra=lambda c, l, u: card_caption(
                        c, l, 4, 10**9, ["EVERY LOOP."], 80, 64, size=140, sub="Two loops, one putt")))
    segs.append(Seg("springs", 330, "whip", 12, "", "ehz2-practice",
                    cap="e2", u0=at("e2", 318), layout=cinema, extra=lambda c, l, u: card_caption(
                        c, l, 4, 10**9, ["EVERY SPRING."], 80, 64, size=140, sub="Rings, springs, monitors and badniks")))
    segs.append(Seg("arch", 170, "whip", 12, "", "ehz1-practice",
                    cap="e1", u0=at("e1", 2062), layout=cinema, extra=lambda c, l, u: card_caption(
                        c, l, 4, 10**9, ["EVERY SOUND."], 80, 64, size=140,
                        sub="Every sound here is the game's own, recorded live")))

    # ---- F. Rewind.
    def rewind_text(canvas, local, u):
        card_caption(canvas, local, 10, 10**9, ["BAD SHOT?", "REWIND IT."], PX + 12, 110, size=100,
                     sub="The whole course rolls back", sub_size=36, max_width=420, sub_max=410)
        pill(canvas, local, 150, 10**9, "STROKE REFUNDED", PX + 4, 640, CYAN, size=44)
        pill(canvas, local, 176, 10**9, "3 PER HOLE · CONFIGURABLE", PX + 4, 724, GOLD, size=38)
    segs.append(Seg("rewind", 340, "card", 36, "Rewind a whole shot", "ehz1-practice",
                    cap="e1", u0=at("e1", 222), layout=framed(seed=2000), extra=rewind_text, card="REWIND", card_sub="WHOLE-SHOT UNDO"))

    # ---- G. The numbers, over the local match.
    def stats_layout(img, local):
        canvas = cinema(img).filter(ImageFilter.GaussianBlur(4))
        canvas = Image.blend(canvas, Image.new("RGB", (W, H), INK), 0.45)
        d = ImageDraw.Draw(canvas, "RGBA")
        bw = int((W + 120) * ease_out((local - 2) / 14) * (1 - ease_in((local - 136) / 14)))
        if bw > 0:
            d.polygon([(-60, 268), (bw, 268), (bw - 60, 760), (-60, 760)], fill=CARD_BLUE + (228,))
        yw = int((W + 120) * ease_out((local - 8) / 14) * (1 - ease_in((local - 132) / 14)))
        if yw > 0:
            d.polygon([(W + 60 - yw, 760), (W + 60, 760), (W + 60, 830), (W + 120 - yw, 830)], fill=CARD_YELLOW + (240,))
        th = int(562 * ease_out(local / 10) * (1 - ease_in((local - 140) / 10)))
        if th > 4:
            d.polygon([(px, py + 268) for px, py in zigzag(th, 46, 9)], fill=CARD_RED + (255,))
        return canvas
    def stats_extra(canvas, local, u):
        items = [("1", "BUTTON"), ("2", "HOLES"), ("2", "GOLFERS"), ("3", "WAYS TO PLAY")]
        for i, (num, label) in enumerate(items):
            cx = 300 + i * 440
            t = back((local - 10 - i * 9) / 14)
            if t <= 0:
                continue
            n = text(num, F_TITLE_IT, 300, GOLD, stroke=8, shadow=10)
            n = n.resize((max(1, int(n.width * t)), max(1, int(n.height * t))), Image.BICUBIC)
            out = 1 - ease_in((local - 130) / 12)
            put(canvas, n, cx, 290 + (1 - t) * 60 + (n.height * (1 - t)) / 2, anchor="mt", alpha=out)
            put(canvas, text(label, F_TITLE, 64, WHITE, stroke=4, shadow=6), cx, 650, alpha=clamp((local - 18 - i * 9) / 8) * out,
                anchor="mt")
        put(canvas, text("Emerald Hill Acts 1 and 2 · Sonic or Tails · practice, local and online", F_SUB, 40, INK),
            W // 2, 768, alpha=clamp((local - 40) / 10) * (1 - ease_in((local - 128) / 10)), anchor="mt")
    segs.append(Seg("numbers", 150, "card", 36, "Two holes, two golfers, three ways to play", "local-match (blurred backdrop)",
                    cap="lm", u0=at("lm", 380), layout=stats_layout, extra=stats_extra, card="AT A GLANCE"))

    # ---- H. Local two-player.
    def local_text(offset):
        def draw(canvas, local, u):
            l = local + offset
            card_caption(canvas, l, 6, 10**9, ["PASS THE PAD."], PX + 12, 110, size=96,
                         sub="Local two-player, turn by turn", sub_size=36, max_width=420, sub_max=410)
            pill(canvas, l, 60, 10**9, "YOUR OWN BUTTON PROMPT", PX + 4, 500, GOLD, size=38)
            pill(canvas, l, 90, 10**9, "HELD UNTIL YOU'RE READY", PX + 4, 584, CYAN, size=38)
            pill(canvas, l, 120, 10**9, "SONIC, TAILS — OR BOTH", PX + 4, 668, TAILS, size=38)
        return draw
    segs.append(Seg("local", 420, "whip", 12, "Local two-player", "local-match",
                    cap="lm", u0=at("lm", 560), layout=framed(seed=5000), extra=local_text(0)))
    segs.append(Seg("local-2", 170, "cut", 0, "", "local-match",
                    cap="lm", u0=at("lm", 1060), layout=framed(seed=5000), extra=local_text(420)))

    # ---- I. Online: host and guest side by side (two real JVMs over TCP), host audio.
    def online_layout(img, local):
        return background(local + 9000)
    def online_extra(offset):
        def draw(canvas, local, u):
            for i, cap in enumerate(("oh", "og")):
                # Host and guest course rows are lockstepped by the orchestrator; their title rows differ.
                window_at(canvas, row(cap, G(cap, u - title_rows("oh"))), 26 + i * 948, 300, 920)
            l = local + offset
            # The link between the two processes: a dashed line with packets running both ways.
            d = ImageDraw.Draw(canvas)
            y = 268
            d.line((486, y, 1434, y), fill=(60, 110, 130), width=4)
            for k in range(6):
                p = ((l * 7 + k * 160) % 948) / 948
                q = 1 - ((l * 5 + k * 160 + 80) % 948) / 948
                d.ellipse((486 + p * 948 - 7, y - 7, 486 + p * 948 + 7, y + 7), fill=SONIC)
                d.ellipse((486 + q * 948 - 7, y - 7, 486 + q * 948 + 7, y + 7), fill=TAILS)
            plate = text("DIRECT TCP · 127.0.0.1:20502", F_TITLE, 34, INK)
            bg = Image.new("RGBA", (plate.width + 30, plate.height + 6), (0, 0, 0, 0))
            ImageDraw.Draw(bg).rounded_rectangle((0, 0, bg.width - 1, bg.height - 1), radius=10, fill=CYAN + (255,))
            bg.paste(plate, (15, 0), plate)
            put(canvas, bg, W // 2, y - bg.height // 2, anchor="mt")
            card_caption(canvas, l, 0, 10**9, ["OR PLAY ONLINE."], 40, 40, size=100,
                         sub="The host runs the course; the guest sees and hears it live", sub_size=36)
            # The guest's whole-shot rewind: requested on the guest, restored by the host on both screens.
            rq = G("oh", ev("oh", "guest-rewind-request"))
            if u >= rq:
                pill(canvas, u - rq, 0, G("oh", ev("oh", "guest-rewind-restored")) - rq + 70, "GUEST REWINDS \u00b7 HOST RESTORES BOTH",
                     None, 948, CYAN, size=40, right=W // 2 + 340)
            put(canvas, text("HOST · P1 SONIC", F_TITLE, 44, SONIC, stroke=3), 30, 960)
            put(canvas, text("GUEST · P2 TAILS", F_TITLE, 44, TAILS, stroke=3), 1894, 960, anchor="rt")
            put(canvas, text("two separate engine processes · recorded live · host audio", F_BODY, 26, CREAM, stroke=2),
                W // 2, 1010, anchor="mt")
        return draw
    segs.append(Seg("online", 300, "card", 36, "Online play over direct IP", "online-host + online-guest (host audio)",
                    cap="oh", u0=G("oh", ev("oh", "handoff-0") + 7), layout=online_layout, extra=online_extra(0), card="ONLINE", card_sub="DIRECT IP MULTIPLAYER"))
    # The guest's turn from its ready press through its shot, its whole-shot rewind (heard reversed
    # on both peers) and the restore, ending 40 rows after the restore plus the outgoing card.
    o2_from = ev("oh", "ready-1", 1) - 10
    o2_frames = ev("oh", "guest-rewind-restored") + 40 + 36 - o2_from
    segs.append(Seg("online-2", o2_frames, "whip", 12, "", "online-host + online-guest (host audio)",
                    cap="oh", u0=G("oh", o2_from), layout=online_layout, extra=online_extra(300)))

    # ---- J. Make your own: the actual registration source beside the running mod.
    source = REPO / "examples/putt-putt-paradise/src/main/java/paradise"
    code = (source / "PuttPuttParadiseMod.java").read_text().splitlines()
    begin = next(i for i, line in enumerate(code) if "public void register" in line)
    snippet = [line[4:] for line in code[begin:begin + 5]]
    snippet = [line if len(line) <= 66 else line[:65] + "…" for line in snippet]
    files = sorted(source.rglob("*.java"))
    lines_of_java = sum(len(f.read_text().splitlines()) for f in files)
    def mod_layout(img, local):
        canvas = background(local + 12000)
        window_at(canvas, img, 1090, 330, 770)
        return canvas
    def mod_extra(canvas, local, u):
        card_caption(canvas, local, 0, 10**9, ["MAKE YOUR OWN."], 80, 56, size=110,
                     sub="Putt Putt Paradise is an example mod for the OpenGGF Mod API")
        panel = Image.new("RGBA", (960, 450), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        pd.rounded_rectangle((0, 0, 959, 449), radius=16, fill=(10, 18, 30, 245), outline=(60, 90, 110), width=2)
        for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            pd.ellipse((22 + i * 30, 20, 40 + i * 30, 38), fill=c)
        pd.text((130, 16), "PuttPuttParadiseMod.java (excerpt)", font=font(F_MONO, 22), fill=(150, 160, 190))
        budget = int(clamp((local - 10) / 70) * sum(len(x) for x in snippet))
        y = 72
        for line in snippet:
            pd.text((24, y), line[:max(0, budget)], font=font(F_MONO, 22), fill=GOLD if "register" in line else (220, 230, 240))
            budget -= len(line); y += 36
        pd.line((24, 270, 935, 270), fill=(50, 80, 96), width=2)
        pd.text((24, 290), f"{len(files)} Java files · {lines_of_java:,} lines · one SDK-validated jar",
                font=font(F_BODY, 28), fill=GOLD)
        pd.text((24, 340), "Rules, menus, HUD, sounds, rewind and netplay live in the mod.", font=font(F_BODY, 25), fill=CREAM)
        pd.text((24, 384), "Art, music and physics come from your ROM.", font=font(F_BODY, 25), fill=CREAM)
        put(canvas, panel, 80, 330, alpha=clamp((local - 4) / 10))
    segs.append(Seg("mod-api", 330, "card", 36, "Make your own with the OpenGGF Mod API", "local-match + PuttPuttParadiseMod.java",
                    cap="lm", u0=at("lm", 3470), layout=mod_layout, extra=mod_extra, gain=0.85, card="MAKE YOUR OWN", card_sub="THE OPENGGF MOD API"))

    # ---- K. Finale: Tails' last putt, the signpost, Stage Clear, the scorecard.
    def finale(canvas, local, u):
        card_caption(canvas, local, 4, 84, ["THE FINAL PUTT."], 80, 64, size=110, sub="Full power. One shot.")
    segs.append(Seg("finale", 690, "iris", 24, "The final putt: Hole Complete", "ehz2-practice",
                    cap="e2", u0=G("e2", [r for r in events("e2")["shot-committed"]][-1] - 56), layout=push_in(84, 40), extra=finale))

    # ---- L. End card.
    def end_card(local):
        title = row("e1", 200)
        backdrop = resample(title, 0, 40, 320, 180, W, H).filter(ImageFilter.GaussianBlur(14))
        canvas = Image.blend(backdrop, Image.new("RGB", (W, H), INK), 0.6)
        banner = title.crop((42, 2, 278, 24)); plate = title.crop((104, 24, 216, 34))
        logo = Image.new("RGB", (236, 32), (0, 0, 0)); mask = Image.new("L", (236, 32), 0)
        logo.paste(banner, (0, 0)); mask.paste(255, (0, 0, 236, 22))
        logo.paste(plate, (62, 22)); mask.paste(255, (62, 22, 174, 32))
        k = 6
        big, bigmask = logo.resize((236 * k, 32 * k), Image.NEAREST), mask.resize((236 * k, 32 * k), Image.NEAREST)
        t = back((local - 6) / 20)
        if t > 0:
            sw, sh = max(1, int(big.width * t)), max(1, int(big.height * t))
            canvas.paste(big.resize((sw, sh), Image.NEAREST), (W // 2 - sw // 2, 120 + (big.height - sh) // 2),
                         bigmask.resize((sw, sh), Image.NEAREST))
        put(canvas, text("Practice · Local two-player · Online", F_SUB, 56, GOLD, stroke=3, shadow=5), W // 2, 362,
            alpha=clamp((local - 30) / 12), anchor="mt")
        put(canvas, badge_img(190), 450, 500, alpha=clamp((local - 46) / 12))
        put(canvas, text("An example mod for the OpenGGF Mod API", F_BODY, 46, WHITE, stroke=3, shadow=5), 680, 510,
            alpha=clamp((local - 52) / 12))
        put(canvas, text("github.com/OpenGGF/OpenGGF", F_TITLE_IT, 86, WHITE, stroke=5, shadow=7), 680, 572,
            alpha=clamp((local - 60) / 12))
        put(canvas, text("Mod API in development for OpenGGF 0.7", F_BODY, 30, CREAM, stroke=2), 684, 690,
            alpha=clamp((local - 70) / 12))
        put(canvas, text("Fan-made and free. Not affiliated with SEGA. Requires your own Sonic 2 ROM.",
                         F_BODY, 26, (195, 205, 215), stroke=2), W // 2, 980, alpha=clamp((local - 80) / 14), anchor="mt")
        put(canvas, text("Gameplay is real engine footage at normal speed with its own game audio. Opener and end-card "
                         "music and chapter-card whooshes: Sonic 2 ROM audio added in editing.",
                         F_BODY, 22, (165, 180, 190), stroke=2), W // 2, 1022, alpha=clamp((local - 90) / 14), anchor="mt")
        return canvas
    segs.append(Seg("end", 540, "fade", 30, "Learn more", "end card; editorial Option Screen theme",
                    draw_fn=end_card, audio=[(EDITORIAL / "s2-music-89.wav", 0, 24, 516, "editorial")]))
    return segs


@lru_cache(maxsize=4)
def badge_img(size):
    return Image.open(BADGE).convert("RGBA").resize((size, size), Image.LANCZOS)


def align_beats(segs):
    """Shift an incoming gameplay clip by at most half a beat so Emerald Hill keeps its pulse
    across the cut. Only clips whose music is the zone bed at normal tempo on both sides move."""
    report = []
    for prev, seg in zip(segs, segs[1:]):
        if prev.cap is None or seg.cap is None or not seg.align:
            continue
        cut = seg.start + seg.tlen // 2
        out_u = prev.u0 + (cut - prev.start)
        in_u = seg.u0 + seg.tlen // 2
        a, b = bed_phase(prev.cap, out_u), bed_phase(seg.cap, in_u)
        if a is None or b is None:
            report.append({"cut_into": seg.name, "aligned": False, "reason": "no normal-tempo zone bed on both sides"})
            continue
        d = ((a - b + BEAT / 2) % BEAT) - BEAT / 2
        seg.shift = int(round(d)); seg.u0 += seg.shift
        report.append({"cut_into": seg.name, "aligned": True, "shift_rows": seg.shift, "beat_phase_out": round(a, 2),
                       "beat_phase_in": round(bed_phase(seg.cap, seg.u0 + seg.tlen // 2), 2)})
    return report


def layout_times(segs):
    t = 0
    for i, s in enumerate(segs):
        if i:
            t -= s.tlen
        s.start = t
        t += s.frames
    return t


# ------------------------------------------------------------------------------------ transitions
@lru_cache(maxsize=16)
def card_label(label):
    return text(label, F_TITLE_IT, 150, WHITE, stroke=6, shadow=10)


def chapter_card(u, label, a, b, card_sub=None):
    """A Sonic 2 title-card wipe: the blue field drops from the top, the yellow field rises from
    the bottom and the red serrated strip slides in from the left; the chapter name sits on the
    blue field; then the three parts leave the way they came, revealing the next shot."""
    cover_in, cover_out = ease_out(u / 0.4), ease_in((u - 0.6) / 0.4)
    cover = cover_in if u < 0.6 else 1 - cover_out
    out = (a if u < 0.5 else b).copy()
    d = ImageDraw.Draw(out)
    split = int(H * 0.66)
    blue_h = int(split * cover)
    d.rectangle((0, 0, W, blue_h), fill=CARD_BLUE)
    yel_h = int((H - split) * clamp(cover * 1.15))
    d.rectangle((0, H - yel_h, W, H), fill=CARD_YELLOW)
    red_w = int(330 * clamp(cover * 1.2))
    if red_w > 0:
        strip = Image.new("RGBA", (red_w + 40, H), (0, 0, 0, 0))
        ImageDraw.Draw(strip).polygon([(x + (red_w - 40), y) for x, y in zigzag(H, 80, 14)] +
                                      [(0, H), (0, 0)], fill=CARD_RED + (255,))
        out.paste(strip, (0, 0), strip)
    if label and 0.25 < u < 0.78:
        im = card_label(label)
        la = clamp((u - 0.25) / 0.12) * clamp((0.78 - u) / 0.1)
        slide = (1 - ease_out((u - 0.25) / 0.2)) * 500 - ease_in((u - 0.62) / 0.16) * 900
        put(out, im, W - 140 - im.width + slide, split - im.height - 40, alpha=la)
        sub = text(card_sub or "PUTT PUTT PARADISE", F_TITLE, 46, INK)
        put(out, sub, W - 160 - sub.width - slide * 0.5, split + 40, alpha=la)
    return out


def blend_transition(seg, a, b, u):
    kind = seg.trans
    if kind == "fade":
        return Image.blend(a, b, smooth(u))
    if kind == "flash":
        if u < 0.5:
            return Image.blend(a, Image.new("RGB", (W, H), WHITE), smooth(u * 2))
        return Image.blend(Image.new("RGB", (W, H), WHITE), b, smooth((u - 0.5) * 2))
    if kind == "whip":
        e = smooth(u)
        out = Image.new("RGB", (W, H))
        shift = int(e * W)
        blur = 0.15 < u < 0.85
        out.paste(a.filter(ImageFilter.BoxBlur(18)) if blur else a, (-shift, 0))
        out.paste(b.filter(ImageFilter.BoxBlur(18)) if blur else b, (W - shift, 0))
        return out
    if kind == "iris":
        r_max = math.hypot(W, H) / 2
        if u < 0.5:
            r, src = r_max * (1 - smooth(u * 2)), a
        else:
            r, src = r_max * smooth((u - 0.5) * 2), b
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=255)
        out = Image.new("RGB", (W, H), (4, 10, 16))
        out.paste(src, (0, 0), mask)
        d = ImageDraw.Draw(out)
        if r > 2:
            d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=GOLD, width=8)
        if r < 26:
            d.ellipse((W / 2 - 26, H / 2 - 26, W / 2 + 26, H / 2 + 26), fill=(4, 10, 16), outline=GOLD, width=6)
        return out
    if kind == "card":
        return chapter_card(u, seg.card, a, b, seg.card_sub)
    return b


# ------------------------------------------------------------------------------------ rendering
SEGS = None
ALIGN = []


def segments():
    global SEGS, ALIGN
    if SEGS is None:
        SEGS = build()
        layout_times(SEGS)
        ALIGN = align_beats(SEGS)
    return SEGS


def total_frames():
    s = segments()[-1]
    return s.start + s.frames


def render_frame(f):
    segs = segments()
    active = [s for s in segs if s.start <= f < s.start + s.frames]
    if len(active) == 1:
        img = active[0].draw(f - active[0].start)
    else:
        a, b = active[0], active[1]
        u = (f - b.start + 0.5) / max(1, b.tlen)
        img = blend_transition(b, a.draw(f - a.start), b.draw(f - b.start), u)
    if f < 12:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, f / 12)
    end = total_frames()
    if f > end - 20:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, max(0, end - 1 - f) / 20)
    return img.convert("RGB").tobytes()


def load_wav(p, cache={}):
    if p not in cache:
        with wave.open(str(p)) as w:
            assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2, p
            cache[p] = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    return cache[p]


def ac_rms(x):
    if len(x) == 0:
        return 0.0
    m = x.mean(axis=1)
    return float(np.sqrt(np.mean((m - m.mean()) ** 2)))


def mix_audio(path):
    """Place every segment's real game audio (and the declared editorial pieces), each with
    equal-power fades over its transitions, then normalise the whole mix (two-pass EBU R128)."""
    segs = segments()
    n = total_frames() * SPF
    out = np.zeros((n, 2), np.float32)
    placements = []
    # Reference level: the median AC RMS of the gameplay segments, so no clip jumps out.
    levels = {s.name: ac_rms(unified_audio(s.cap)[s.u0 * SPF:(s.u0 + s.frames) * SPF]) for s in segs if s.cap}
    ref = float(np.median([v for v in levels.values() if v > 0]))
    for i, s in enumerate(segs):
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        pieces = []
        if s.cap:
            data = unified_audio(s.cap)
            # Level-match each clip to the reference, within +/-4 dB, then the segment's own trim.
            g = clamp(ref / max(levels[s.name], 1e-6), 10 ** (-4 / 20), 10 ** (4 / 20)) * s.gain
            pieces.append(("game", data, s.u0, 0, s.frames, g, str(CAPTURES[s.cap])))
        for wav, src0, local0, count, kind in s.audio:
            data = load_wav(wav)
            seg_ref = ac_rms(data[src0 * SPF:(src0 + count) * SPF])
            pieces.append((kind, data, src0, local0, count, ref / max(seg_ref, 1e-6), str(wav)))
        for kind, data, src0, local0, count, gain, label in pieces:
            a = src0 * SPF
            o = (s.start + local0) * SPF
            length = max(0, min(count * SPF, len(data) - a))
            piece = data[a:a + length].copy() * gain
            fin = max(6, s.tlen) * SPF if i else 20 * SPF
            fout = max(6, nxt.tlen) * SPF if nxt else 30 * SPF
            k = np.arange(length, dtype=np.float32)
            env = np.minimum(np.sin(np.clip(k / fin, 0, 1) * np.pi / 2), np.sin(np.clip((length - k) / fout, 0, 1) * np.pi / 2))
            piece *= env[:, None]
            end = min(n, o + length)
            out[o:end] += piece[:end - o]
            placements.append({"segment": s.name, "kind": kind, "source": label, "source_frame": src0,
                               "out_frame": s.start + local0, "frames": length // SPF, "gain": round(gain, 4)})
        if s.trans == "card":
            # Editorial whoosh on chapter cards: the ROM's Spindash Release, quiet, under the wipe.
            sfx = load_wav(EDITORIAL / "s2-sfx-bc.wav")
            o = (s.start + 2) * SPF
            g = 0.45 * ref / max(ac_rms(sfx), 1e-6)
            end = min(n, o + len(sfx))
            out[o:end] += sfx[:end - o] * g
            placements.append({"segment": s.name, "kind": "editorial-transition", "source": str(EDITORIAL / "s2-sfx-bc.wav"),
                               "source_frame": 0, "out_frame": s.start + 2, "frames": len(sfx) // SPF, "gain": round(g, 4)})
    raw = BUILD / "soundtrack-raw.wav"
    write_wav(raw, out)
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(raw), "-af",
                            "loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-y", "-i", str(raw), "-af",
                    f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
                    f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(path)], check=True)
    return placements, m, {k: round(20 * math.log10(max(v, 1e-9)), 2) for k, v in levels.items()}


def write_wav(path, data):
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def chapters():
    return [(s.start, s.chapter) for s in segments() if s.chapter]


def write_edl():
    segs = segments()
    BUILD.mkdir(exist_ok=True)
    edl = {"fps": FPS, "frames": total_frames(), "seconds": total_frames() / FPS, "show": str(SHOW), "segments": [
        {"name": s.name, "start_frame": s.start, "frames": s.frames, "start_s": round(s.start / FPS, 3),
         "end_s": round((s.start + s.frames) / FPS, 3), "transition_in": s.trans, "transition_frames": s.tlen,
         "chapter": s.chapter, "card": s.card, "source": s.source, "capture": s.cap,
         "title_rows": title_rows(s.cap) if s.cap else None,
         "first_unified_row": s.u0 if s.cap else None, "last_unified_row": s.u0 + s.frames - 1 if s.cap else None,
         "beat_shift_rows": s.shift,
         "editorial_audio": [{"wav": str(a[0]), "source_frame": a[1], "local_frame": a[2], "frames": a[3]} for a in s.audio]}
        for s in segs], "beat_alignment": ALIGN}
    (ROOT / "promo.edl.json").write_text(json.dumps(edl, indent=1) + "\n")
    lines = ["start_s,end_s,chapter"]
    ch = chapters()
    for i, (start, name) in enumerate(ch):
        end = ch[i + 1][0] if i + 1 < len(ch) else total_frames()
        lines.append(f"{start / FPS:.3f},{end / FPS:.3f},\"{name}\"")
    (ROOT / "promo.chapters.csv").write_text("\n".join(lines) + "\n")
    meta = [";FFMETADATA1", "title=Putt Putt Paradise - Sonic 2 Mini Golf (OpenGGF example mod)",
            "comment=Gameplay is real OpenGGF engine footage at normal speed with its own captured game audio. "
            "Opener uses OpenGGF 0.6 Sonic 2 footage; Title/Option themes and chapter-card whooshes are Sonic 2 ROM "
            "sounds rendered by OpenGGF and added in editing."]
    for i, (start, name) in enumerate(ch):
        end = ch[i + 1][0] if i + 1 < len(ch) else total_frames()
        meta += ["[CHAPTER]", "TIMEBASE=1/60", f"START={start}", f"END={end}", f"title={name}"]
    (BUILD / "chapters.ffmeta").write_text("\n".join(meta) + "\n")
    return edl


def extract_master():
    for name, first, count in [("ehz", 12, 84), ("cnz", 1218, 78), ("special", 1440, 78), ("sky", 3360, 100)]:
        out = BUILD / "master" / name
        if out.exists() and len(list(out.glob("*.png"))) == count:
            continue
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("*.png"):
            old.unlink()
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-threads", "2", "-i", str(MASTER), "-vf",
                        f"select='between(n\\,{first}\\,{first + count - 1})',crop=1920:1080:0:132", "-fps_mode", "passthrough",
                        "-frames:v", str(count), str(out / "%05d.png")], check=True)


def encode(frames, out, audio, extra_outputs=()):
    """Pipe RGB frames to ffmpeg: H.264/AAC MP4 and, optionally, an FFV1/PCM master."""
    cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-y", "-threads", "2",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(audio), "-i", str(BUILD / "chapters.ffmeta"),
           "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-x264-params", "threads=4",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", str(out)]
    for master_out in extra_outputs:
        cmd += ["-map", "0:v", "-map", "1:a", "-map_chapters", "2", "-c:v", "ffv1", "-level", "3", "-pix_fmt", "rgb24",
                "-c:a", "pcm_s16le", "-shortest", str(master_out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(WORKERS) as pool:
        for k, b in enumerate(pool.imap(render_frame, frames, chunksize=6)):
            enc.stdin.write(b)
            if k % 600 == 0:
                print(f"frame {k}/{len(frames)}", flush=True)
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("encoder failed")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    BUILD.mkdir(exist_ok=True)
    extract_master()
    if cmd == "edl":
        e = write_edl(); print(json.dumps({"frames": e["frames"], "seconds": e["seconds"], "align": ALIGN})); return
    if cmd == "frames":
        out = BUILD / "check"; out.mkdir(exist_ok=True)
        for a in sys.argv[2:]:
            Image.frombytes("RGB", (W, H), render_frame(int(a))).save(out / f"frame-{int(a):05d}.png")
        return
    if cmd == "sheet":
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        idx = list(range(0, total_frames(), step))
        with Pool(WORKERS) as pool:
            imgs = pool.map(render_frame, idx)
        cols, tw, th = 6, 384, 216
        sheet = Image.new("RGB", (cols * tw, ((len(idx) + cols - 1) // cols) * th))
        for k, b in enumerate(imgs):
            im = Image.frombytes("RGB", (W, H), b).resize((tw, th), Image.BILINEAR)
            ImageDraw.Draw(im).text((4, 4), f"{idx[k]} ({idx[k] / FPS:.1f}s)", fill=(255, 255, 0))
            sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
        sheet.save(ROOT / "promo.cuts.png"); return
    if cmd == "audio":
        write_edl()
        placements, m, levels = mix_audio(ROOT / "promo.soundtrack.wav")
        (ROOT / "promo.audio.json").write_text(json.dumps({"placements": placements, "segment_ac_dbfs": levels,
                                                           "loudnorm_first_pass": m}, indent=1) + "\n")
        return
    if cmd == "clip":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        write_edl()
        if not (ROOT / "promo.soundtrack.wav").exists():
            mix_audio(ROOT / "promo.soundtrack.wav")
        out = BUILD / "check"; out.mkdir(exist_ok=True)
        clip_audio = BUILD / "clip.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "promo.soundtrack.wav"), "-ss", f"{a / FPS}",
                        "-t", f"{(b - a) / FPS}", str(clip_audio)], check=True)
        meta = BUILD / "chapters.ffmeta"
        encode(list(range(a, b)), out / f"clip-{a}-{b}.mp4", clip_audio)
        print("wrote", out / f"clip-{a}-{b}.mp4"); return
    if cmd == "render":
        out = ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "putt-putt-paradise-promo.mp4")
        write_edl()
        placements, m, levels = mix_audio(ROOT / "promo.soundtrack.wav")
        (ROOT / "promo.audio.json").write_text(json.dumps({"placements": placements, "segment_ac_dbfs": levels,
                                                           "loudnorm_first_pass": m}, indent=1) + "\n")
        masters = [BUILD / "putt-putt-paradise-promo.master.mkv"] if "--master" in sys.argv else []
        encode(list(range(total_frames())), out, ROOT / "promo.soundtrack.wav", masters)
        print("wrote", out)


if __name__ == "__main__":
    main()
