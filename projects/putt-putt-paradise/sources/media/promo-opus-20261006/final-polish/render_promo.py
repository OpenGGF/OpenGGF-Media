#!/usr/bin/env python3
"""Putt Putt Paradise public promo, final-polish revision (Opus, 2026-10-06).

Composites the polish-round captures (60 fps PNG rows with row-synchronous game audio) and a
short OpenGGF 0.6 Sonic 2 engine opener into a 1920x1080 / 60 fps film with kinetic type,
transitions and a soundtrack built from the captured game audio.

Every gameplay segment plays its source rows at normal speed: one captured 60 Hz row is one
output frame, and its audio is that row's own 800-sample packet. Cuts between gameplay clips
crossfade the real game audio; where both sides carry Emerald Hill music at normal tempo, the
incoming clip is shifted by under half a bar so the music keeps its bar phase. Only the
engine opener (Title Screen theme) and the end card (Option Screen theme) use editorial music,
rendered from the same Sonic 2 ROM by OpenGGF's SMPS driver.

  render_promo.py edl                write the resolved timeline (edl.json, chapters.csv)
  render_promo.py frames N [N ...]   write single output frames to build/check/
  render_promo.py sheet [step]       contact sheet of output frames
  render_promo.py audio              mix the soundtrack (soundtrack.wav, normalised)
  render_promo.py render [--out F]   full render (frames + soundtrack + chapters) to MP4
"""
import json
import math
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
SHOW = ROOT.parent.parent / "showcase-20261006-opus-polish"
EDITORIAL = ROOT.parent / "intro-audio" / "audio"
MASTER = Path.home() / "Videos/OGGF/S2-0.6/s2-0.6-V2.mov"
BUILD = ROOT / "build"
REPO = Path("/home/farrell/code/projects/OpenGGF/.worktrees/putt-putt-paradise")
BADGE = REPO / "src/main/resources/icon/openggf-256.png"
W, H, FPS, SR = 1920, 1080, 60, 48000
SPF = SR // FPS  # 800 stereo frames per output frame == one captured row
BEAT = 25.93     # Emerald Hill Zone beat in 60 Hz rows (measured from the ROM-rendered stem)
BAR = 4 * BEAT

FONT_DIR = "/usr/share/fonts/TTF/"
F_TITLE = "FiraSansCompressed-Heavy.ttf"
F_TITLE_IT = "FiraSansCompressed-HeavyItalic.ttf"
F_SUB = "FiraSansCondensed-BoldItalic.ttf"
F_BODY = "FiraSans-Bold.ttf"
F_MONO = "Hack-Regular.ttf"
F_MONO_B = "Hack-Bold.ttf"

WHITE, CREAM, GOLD, RED = (255, 255, 255), (255, 243, 203), (255, 212, 91), (172, 38, 56)
NIGHT, INK, TEAL, SKY = (11, 34, 48), (8, 20, 34), (22, 70, 84), (60, 120, 230)
SONIC, TAILS = (60, 120, 230), (244, 162, 60)

CAPTURES = {
    "e1": SHOW / "ehz1-practice", "e2": SHOW / "ehz2-practice", "lm": SHOW / "local-match",
    "oh": SHOW / "online/online-host", "og": SHOW / "online/online-guest",
}


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


# ------------------------------------------------------------------------------------ sources
@lru_cache(maxsize=256)
def row(cap, r, title=False):
    folder = CAPTURES[cap] / ("title-frames" if title else "frames")
    return Image.open(folder / f"{r:06d}.png").convert("RGB")


@lru_cache(maxsize=64)
def master(shot, i):
    files = sorted((BUILD / "master" / shot).glob("*.png"))
    return Image.open(files[int(clamp(i, 0, len(files) - 1))]).convert("RGB")


def music_starts(cap):
    """Rows where the zone music (re)starts, and speed-shoe tempo windows, from the request log."""
    starts, fast, open_fast = [], [], None
    for line in (CAPTURES[cap] / "audio-requests.csv").read_text().splitlines()[1:]:
        phase, r, kind, ident = line.split(",")
        if phase != "gameplay":
            continue
        r = int(r)
        if kind == "MUSIC" and ident == "0x81":
            if not starts or starts[-1] != r:
                starts.append(r)
        elif kind == "COMMAND" and ident == "0xFB":
            open_fast = r
        elif kind == "COMMAND" and ident == "0xFC" and open_fast is not None:
            fast.append((open_fast, r)); open_fast = None
    return starts, fast


def bar_phase(cap, r):
    """Bar phase (rows) of Emerald Hill music at a gameplay row, or None if unknown or sped up."""
    starts, fast = music_starts(cap)
    i = bisect_right(starts, r) - 1
    if i < 0:
        return None
    if any(a <= r < b for a, b in fast) or any(starts[i] < a <= r for a, b in fast):
        return None
    for line in (CAPTURES[cap] / "audio-requests.csv").read_text().splitlines()[1:]:
        phase, rr, kind, ident = line.split(",")
        if phase == "gameplay" and kind == "MUSIC" and ident != "0x81" and starts[i] < int(rr) <= r:
            return None  # A jingle (1-Up, Stage Clear) interrupted the bed.
    return (r - starts[i]) % BAR


# ------------------------------------------------------------------------------------ pixels
def resample(img, x0, y0, vw, vh, ow, oh):
    """Pixel-art scaling: nearest up by an integer factor, then an area filter to the output."""
    k = max(1, math.ceil(ow / vw - 1e-9))
    ix0, iy0 = math.floor(x0), math.floor(y0)
    ix1, iy1 = min(img.width, math.ceil(x0 + vw)), min(img.height, math.ceil(y0 + vh))
    crop = img.crop((ix0, iy0, ix1, iy1)).resize(((ix1 - ix0) * k, (iy1 - iy0) * k), Image.NEAREST)
    box = ((x0 - ix0) * k, (y0 - iy0) * k, (x0 - ix0 + vw) * k, (y0 - iy0 + vh) * k)
    return crop.resize((round(ow), round(oh)), Image.BOX, box=box)


@lru_cache(maxsize=1)
def stripes():
    tile = Image.new("RGB", (W + 400, H), NIGHT)
    d = ImageDraw.Draw(tile)
    top, bottom = np.array((9, 27, 46)), np.array((14, 52, 60))
    for y in range(H):
        c = tuple(int(v) for v in top + (bottom - top) * (y / H))
        d.line((0, y, W + 400, y), fill=c)
    over = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    for x in range(-H, W + 400, 64):
        od.polygon([(x, H), (x + 28, H), (x + 28 + H, 0), (x + H, 0)], fill=(255, 255, 255, 9))
    return Image.alpha_composite(tile.convert("RGBA"), over).convert("RGB")


def background(f):
    shift = int(f * 0.6) % 64
    return stripes().crop((shift, 0, shift + W, H))


def blur_fill(img, f=0):
    """Full-height game frame over a blurred, darkened copy of itself."""
    bg = img.resize((W // 8, round(W // 8 * img.height / img.width)), Image.BILINEAR)
    bg = bg.filter(ImageFilter.GaussianBlur(5)).resize((W, round(W * img.height / img.width)), Image.BILINEAR)
    top = (bg.height - H) // 2
    bg = bg.crop((0, top, W, top + H))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.55)
    gw = round(H * img.width / img.height)
    game = resample(img, 0, 0, img.width, img.height, gw, H)
    bg.paste(shadow_box(gw, H), ((W - gw) // 2 - 20, -20), shadow_box(gw, H))
    bg.paste(game, ((W - gw) // 2, 0))
    return bg


@lru_cache(maxsize=16)
def shadow_box(w, h, radius=22, alpha=150):
    m = Image.new("L", (w + 40, h + 40), 0)
    ImageDraw.Draw(m).rectangle((20, 20, 20 + w, 20 + h), fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(radius))
    return Image.merge("RGBA", (Image.new("L", m.size, 0),) * 3 + (m,))


def window(canvas, img, x, y, scale, border=GOLD):
    w, h = img.width * scale, img.height * scale
    sh = shadow_box(w, h)
    canvas.paste(sh, (x - 20 + 10, y - 20 + 14), sh)
    d = ImageDraw.Draw(canvas)
    d.rectangle((x - 5, y - 5, x + w + 4, y + h + 4), fill=border)
    d.rectangle((x - 2, y - 2, x + w + 1, y + h + 1), fill=INK)
    canvas.paste(img.resize((w, h), Image.NEAREST), (x, y))


# ------------------------------------------------------------------------------------ type
@lru_cache(maxsize=None)
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


@lru_cache(maxsize=512)
def text(s, fname, size, fill=WHITE, stroke=0, shadow=0, scol=(0, 0, 0)):
    f = font(fname, size)
    l, t, r, b = f.getbbox(s, stroke_width=stroke)
    pad = stroke + shadow + 6
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + shadow, pad - t + shadow), s, font=f, fill=scol + (170,),
                                stroke_width=stroke, stroke_fill=scol + (170,))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(max(1, shadow // 2))))
        d = ImageDraw.Draw(im)
    d.text((pad - l, pad - t), s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(10, 18, 30, 255))
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


def heading(canvas, local, start, end, lines, x, y, size=118, sub=None, sub_size=46, align="lt", accent=GOLD,
            max_width=1760):
    """Chapter heading: heavy italic lines slide in staggered, a gold rule draws, the sub fades in."""
    if local < start or local >= end:
        return
    age, left = local - start, end - local
    out = clamp(left / 14)
    yy = y
    for i, s in enumerate(lines):
        im = fitted(s, F_TITLE_IT, size, max_width, fill=WHITE, stroke=5, shadow=8)
        t = back((age - i * 5) / 16)
        dx = (1 - t) * (-220 if align == "lt" else 0)
        put(canvas, im, x + dx, yy + (1 - ease_out((age - i * 5) / 14)) * (30 if align == "mt" else 0),
            alpha=clamp((age - i * 5) / 8) * out, anchor=align)
        yy += im.height - 26
    rule = int(ease_out((age - 8) / 18) * 220)
    if rule > 0:
        d = ImageDraw.Draw(canvas)
        rx = x if align == "lt" else x - 110
        d.rectangle((rx + 8, yy + 6, rx + 8 + rule, yy + 13), fill=accent)
    if sub:
        im = fitted(sub, F_SUB, sub_size, max_width, fill=GOLD, stroke=3, shadow=5)
        put(canvas, im, x + 4, yy + 24, alpha=clamp((age - 14) / 12) * out, anchor=align)


def pill(canvas, local, start, end, label, x, y, colour=GOLD, size=40, ink=INK, right=None):
    if local < start or local >= end:
        return
    if right is not None:
        x = right - (text(label, F_TITLE, size, ink).width + 38)
    age, left = local - start, end - local
    im = text(label, F_TITLE, size, ink)
    w, h = im.width + 26, im.height - 2
    t = back(age / 12)
    a = clamp(age / 6) * clamp(left / 10)
    plate = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle((6, 6, 6 + w, 6 + h), radius=10, fill=colour + (255,))
    plate.paste(im, (19, 2), im)
    put(canvas, plate, x + (1 - t) * 60, y, alpha=a)


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
    audio: list = field(default_factory=list)   # non-gameplay: [(wav, src_frame, local_frame, count, gain)]
    cap: str = None                   # gameplay: capture key, first row, layout(img, local), extra(canvas, local, row)
    r0: int = 0
    layout: object = None
    extra: object = None
    title: bool = False
    gain: float = 1.0
    shift: int = 0                    # beat-alignment shift applied to r0 (rows)
    start: int = 0

    def draw(self, local):
        if self.cap is None:
            return self.draw_fn(local)
        r = self.r0 + local
        canvas = self.layout(row(self.cap, r, self.title), local)
        if self.extra:
            self.extra(canvas, local, r)
        return canvas

    def audio_pieces(self):
        if self.cap is None:
            return self.audio
        return [(wav_of(self.cap, self.title), self.r0, 0, self.frames, self.gain)]


def cinema(img, local=0):
    """HUD-free 16:9 action framing: the middle 300x169 game pixels (6.4x), chips and pills excluded."""
    return resample(img, 10, 30, 300, 169, W, H)


def push_in(t0, dur):
    """Full frame with its HUD (power sweep) first, then an eased push into the HUD-free action crop."""
    def layout(img, local):
        u = smooth((local - t0) / dur)
        if u <= 0:
            return blur_fill(img)
        x0, y0 = 10 * u, 30 * u
        w, h = 320 - 20 * u, 224 - 55 * u
        scale = min(W / w, H / h)
        ow, oh = round(w * scale), round(h * scale)
        canvas = blur_fill(img) if ow < W - 2 else Image.new("RGB", (W, H))
        canvas.paste(resample(img, x0, y0, w, h, ow, oh), ((W - ow) // 2, (H - oh) // 2))
        return canvas
    return layout


def framed(x=60, y=118, scale=4):
    def layout(img, local):
        canvas = background(local)
        window(canvas, img, x, y, scale)
        return canvas
    return layout


def window_f(canvas, img, x, y, w):
    """Window at an arbitrary width, pixel-art resampled."""
    h = round(w * img.height / img.width)
    sh = shadow_box(w, h)
    canvas.paste(sh, (x - 20 + 10, y - 20 + 14), sh)
    d = ImageDraw.Draw(canvas)
    d.rectangle((x - 5, y - 5, x + w + 4, y + h + 4), fill=GOLD)
    canvas.paste(resample(img, 0, 0, img.width, img.height, w, h), (x, y))
    return h


def wav_of(cap, title=False):
    return CAPTURES[cap] / ("title.wav" if title else "gameplay.wav")


def both(*fns):
    def draw(canvas, local, r):
        for fn in fns:
            fn(canvas, local, r)
    return draw


def corner_label(label, at=6, until=10**9, colour=GOLD):
    def draw(canvas, local, r):
        pill(canvas, local, at, until, label, None, 960, colour, size=46, right=1850)
    return draw


def build():
    segs = []

    # ---- A. Cold open: OpenGGF plays Sonic 2 (engine 0.6 footage, muted; Title Screen theme).
    shots = [("ehz", 12, 84), ("cnz", 1218, 78), ("special", 1440, 78), ("sky", 3360, 96)]
    def opener(local):
        acc = 0
        for name, first, count in shots:
            if local < acc + count:
                img = master(name, local - acc)
                break
            acc += count
        canvas = Image.blend(img, Image.new("RGB", (W, H), INK), 0.42)
        size = 380
        t = back((local - 8) / 18)
        if t > 0:
            b = badge_img(size).resize((max(1, int(size * t)),) * 2, Image.BICUBIC)
            put(canvas, b, W // 2 - b.width // 2, 110 + (size - b.width) // 2)
        put(canvas, text("THE OPEN-SOURCE ENGINE FOR CLASSIC SONIC", F_TITLE, 96, WHITE, stroke=6, shadow=9), W // 2, 530,
            alpha=clamp((local - 30) / 10), anchor="mt")
        put(canvas, text("Sonic 2, rebuilt in Java \u00b7 running from your own ROM", F_SUB, 54, GOLD, stroke=4, shadow=6),
            W // 2, 680, alpha=clamp((local - 96) / 14), anchor="mt")
        return canvas
    segs.append(Seg("cold-open", sum(c for _, _, c in shots), "fade", 20,
                    "OpenGGF: the open-source engine for classic Sonic", "OpenGGF 0.6 Sonic 2 promo master, muted",
                    draw_fn=opener, audio=[(EDITORIAL / "s2-music-96.wav", 0, 0, 346, 1.7)]))

    # ---- B. Hook: Sonic is the ball, then Tails (cinematic crops, kinetic type).
    def hook_sonic(canvas, local, r):
        heading(canvas, r, 118, 400, ["WHAT IF SONIC"], 90, 60, size=160)
        heading(canvas, r, 206, 400, ["WAS THE GOLF BALL?"], 90, 220, size=160)
    segs.append(Seg("hook-sonic", 196, "flash", 16, "What if Sonic was the golf ball?", "ehz1-practice",
                    cap="e1", r0=96, layout=cinema, extra=hook_sonic))
    def hook_tails(canvas, local, r):
        heading(canvas, local, 8, 400, ["...OR TAILS?"], 1830, 60, size=160, align="rt")
    segs.append(Seg("hook-tails", 176, "whip", 12, "", "ehz2-practice",
                    cap="e2", r0=300, layout=cinema, extra=hook_tails))

    # ---- C. Title drop: the creator title screen with its ROM menu music and blips.
    def title_layout(img, local):
        canvas = background(local + 4000)
        window(canvas, img, 60, 92, 4)
        return canvas
    def title_text(canvas, local, r):
        x = 1396
        put(canvas, text("PUTT PUTT", F_TITLE_IT, 116, GOLD, stroke=5, shadow=8), x, 130, alpha=clamp((local - 24) / 10))
        put(canvas, text("PARADISE", F_TITLE_IT, 116, WHITE, stroke=5, shadow=8), x, 228, alpha=clamp((local - 30) / 10))
        put(canvas, text("Sonic 2 Mini Golf", F_SUB, 56, CREAM, stroke=3, shadow=5), x + 4, 356, alpha=clamp((local - 44) / 12))
        put(canvas, text("An example mod for", F_BODY, 34, CREAM, stroke=2, shadow=4), x + 4, 440, alpha=clamp((local - 60) / 12))
        put(canvas, text("the OpenGGF engine", F_BODY, 34, CREAM, stroke=2, shadow=4), x + 4, 484, alpha=clamp((local - 60) / 12))
        for i, (at, label, colour) in enumerate([(100, "PRACTICE", GOLD), (117, "LOCAL 2 PLAYERS", TAILS),
                                                  (134, "ONLINE MATCHES", (97, 215, 237))]):
            pill(canvas, local, at, 10**9, label, x, 590 + i * 84, colour)
    segs.append(Seg("title", 390, "bands", 30, "Putt Putt Paradise: Sonic 2 Mini Golf", "ehz1-practice title rows",
                    cap="e1", r0=0, title=True, layout=title_layout, extra=title_text, gain=0.95))

    # ---- D. How to play: one continuous chip, captions follow the real shot stages.
    steps = [("AIM", "Up/Down loft \u00b7 Left/Right direction", 760, 810),
             ("HIT POINT", "Top or backspin, Dream Course-style", 810, 866),
             ("POWER", "One sweep, one press", 866, 930), ("SPIN DASH!", "The ROM's own charge and release", 930, 962),
             ("ROLL", "Native Sonic 2 physics take over", 962, 10**9)]
    def howto(canvas, local, r):
        heading(canvas, local, 0, 10**9, ["ONE BUTTON."], 1388, 92, size=100, sub="Kirby's Dream Course-style shots",
                sub_size=40, max_width=500)
        for i, (name, desc, a, b) in enumerate(steps):
            y = 372 + i * 118
            on, done = a <= r < b, r >= b
            col = GOLD if on else (CREAM if done else (110, 140, 150))
            plate = Image.new("RGBA", (480, 102), (0, 0, 0, 0))
            pd = ImageDraw.Draw(plate)
            pd.rounded_rectangle((0, 0, 479, 101), radius=14, fill=(20, 58, 72, 240) if on else (12, 30, 42, 205),
                                 outline=GOLD if on else (40, 80, 92), width=3)
            t = text(f"{i + 1}  {name}", F_TITLE, 46, col)
            plate.paste(t, (12, 4), t)
            sub = text(desc, F_BODY, 24, CREAM if on or done else (120, 150, 160))
            plate.paste(sub, (18, 60), sub)
            pop = back((r - a) / 10) if on else 1
            put(canvas, plate, 1388 + (1 - pop) * 36, y, alpha=clamp((local - i * 6) / 10))
    segs.append(Seg("how-to", 470, "whip", 12, "One button: aim, hit point, power", "ehz1-practice",
                    cap="e1", r0=744, layout=framed(), extra=howto))

    # ---- E. Real physics: loops, springs/rings/badniks, the arch (cinematic crops).
    segs.append(Seg("loops", 220, "iris", 24, "Real Sonic 2 physics: loops, springs, badniks", "ehz1-practice",
                    cap="e1", r0=2688, layout=cinema, extra=both(
                        lambda c, l, r: heading(c, l, 0, 10**9, ["EVERY LOOP."], 80, 60, size=140),
                        corner_label("TWO LOOPS, ONE PUTT", 30))))
    segs.append(Seg("springs", 330, "whip", 12, "", "ehz2-practice",
                    cap="e2", r0=318, layout=cinema, extra=both(
                        lambda c, l, r: heading(c, l, 0, 10**9, ["EVERY SPRING."], 80, 60, size=140),
                        corner_label("RINGS \u00b7 SPRINGS \u00b7 MONITORS \u00b7 BADNIKS", 20))))
    segs.append(Seg("arch", 170, "whip", 12, "", "ehz1-practice",
                    cap="e1", r0=2062, layout=cinema, extra=both(
                        lambda c, l, r: heading(c, l, 0, 10**9, ["FROM YOUR ROM."], 80, 60, size=140,
                                                sub="Every object and every sound comes from your own Sonic 2"),
                        corner_label("BRIDGES \u00b7 ARCHES \u00b7 BADNIKS", 30))))

    # ---- F. Rewind.
    def rewind_text(canvas, local, r):
        heading(canvas, local, 10, 10**9, ["BAD SHOT?", "REWIND IT."], 1388, 110, size=100,
                sub="The whole course rolls back", sub_size=40, max_width=500)
        pill(canvas, local, 150, 10**9, "STROKE REFUNDED", 1392, 640, (97, 215, 237), size=44)
        pill(canvas, local, 176, 10**9, "3 PER HOLE \u00b7 CONFIGURABLE", 1392, 724, GOLD, size=40)
    segs.append(Seg("rewind", 340, "bands", 30, "Rewind a whole shot", "ehz1-practice",
                    cap="e1", r0=222, layout=framed(), extra=rewind_text))

    # ---- G. Local two-player.
    def local_text(offset):
        def draw(canvas, local, r):
            l = local + offset
            heading(canvas, l, 6, 10**9, ["PASS THE PAD."], 1388, 110, size=92, sub="Local two-player, turn by turn",
                    sub_size=40, max_width=500)
            pill(canvas, l, 60, 10**9, "YOUR OWN BUTTON PROMPT", 1392, 520, GOLD, size=40)
            pill(canvas, l, 90, 10**9, "HELD UNTIL YOU'RE READY", 1392, 604, (97, 215, 237), size=40)
            pill(canvas, l, 120, 10**9, "SONIC, TAILS \u2014 OR BOTH", 1392, 688, TAILS, size=40)
        return draw
    segs.append(Seg("local", 420, "whip", 12, "Local two-player", "local-match",
                    cap="lm", r0=560, layout=framed(), extra=local_text(0)))
    segs.append(Seg("local-2", 170, "cut", 0, "", "local-match",
                    cap="lm", r0=1060, layout=framed(), extra=local_text(420)))

    # ---- H. Online: host and guest side by side (two real JVMs over TCP).
    def online_layout(img, local):
        return background(local + 9000)
    def online_extra(offset):
        def draw(canvas, local, r):
            for i, cap in enumerate(("oh", "og")):
                window_f(canvas, row(cap, r), 26 + i * 948, 300, 920)
            heading(canvas, local + offset, 0, 10**9, ["OR PLAY ONLINE."], 40, 40, size=104,
                    sub="Direct IP: the host runs the course, the guest sees it live", sub_size=40)
            put(canvas, text("HOST \u00b7 P1 SONIC", F_TITLE, 44, (140, 180, 255), stroke=3), 30, 960)
            put(canvas, text("GUEST \u00b7 P2 TAILS", F_TITLE, 44, TAILS, stroke=3), 1894, 960, anchor="rt")
            put(canvas, text("two separate engine processes \u00b7 real TCP \u00b7 captured live", F_BODY, 26, CREAM, stroke=2),
                W // 2, 1000, anchor="mt")
        return draw
    segs.append(Seg("online", 300, "iris", 24, "Online play over direct IP", "online-host + online-guest (host audio)",
                    cap="oh", r0=10, layout=online_layout, extra=online_extra(0)))
    segs.append(Seg("online-2", 420, "whip", 12, "", "online-host + online-guest (host audio)",
                    cap="oh", r0=1568, layout=online_layout, extra=online_extra(300)))

    # ---- I. Make your own: the actual registration source beside the running mod.
    source = REPO / "examples/putt-putt-paradise/src/main/java/paradise"
    code = (source / "PuttPuttParadiseMod.java").read_text().splitlines()
    begin = next(i for i, line in enumerate(code) if "public void register" in line)
    snippet = [line[4:] for line in code[begin:begin + 5]]
    snippet = [line if len(line) <= 66 else line[:65] + "\u2026" for line in snippet]
    files = sorted(source.rglob("*.java"))
    lines_of_java = sum(len(f.read_text().splitlines()) for f in files)
    def mod_layout(img, local):
        canvas = background(local + 12000)
        window_f(canvas, img, 1090, 330, 770)
        return canvas
    def mod_extra(canvas, local, r):
        heading(canvas, local, 0, 10**9, ["MAKE YOUR OWN."], 80, 50, size=110,
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
            colour = GOLD if "register" in line else (220, 230, 240)
            pd.text((24, y), line[:max(0, budget)], font=font(F_MONO, 22), fill=colour)
            budget -= len(line); y += 36
        pd.line((24, 270, 935, 270), fill=(50, 80, 96), width=2)
        stats = f"{len(files)} Java files \u00b7 {lines_of_java:,} lines \u00b7 one SDK-validated jar"
        pd.text((24, 290), stats, font=font(F_BODY, 28), fill=GOLD)
        pd.text((24, 340), "Rules, menus, HUD, rewind and netplay live in the mod.", font=font(F_BODY, 25), fill=CREAM)
        pd.text((24, 384), "Art, sound and physics come from your ROM.", font=font(F_BODY, 25), fill=CREAM)
        put(canvas, panel, 80, 330, alpha=clamp((local - 4) / 10))
    segs.append(Seg("mod-api", 330, "bands", 30, "Make your own with the OpenGGF Mod API", "local-match + PuttPuttParadiseMod.java",
                    cap="lm", r0=3470, layout=mod_layout, extra=mod_extra, gain=0.9))

    # ---- J. Finale: Tails' last putt through the corkscrew, the signpost, Stage Clear, the tally.
    def finale(canvas, local, r):
        heading(canvas, local, 4, 84, ["THE FINAL PUTT."], 80, 60, size=110, sub="Full power. One shot.")
    segs.append(Seg("finale", 690, "iris", 24, "The final putt: Hole Complete", "ehz2-practice",
                    cap="e2", r0=7030, layout=push_in(84, 40), extra=finale, gain=1.9))

    # ---- K. End card.
    def end_card(local):
        title = row("e1", 380, True)
        backdrop = resample(title, 0, 40, 320, 180, W, H).filter(ImageFilter.GaussianBlur(14))
        canvas = Image.blend(backdrop, Image.new("RGB", (W, H), INK), 0.6)
        # The mod's own title banner and subtitle plate, cut from the captured title screen.
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
        put(canvas, text("Practice \u00b7 Local two-player \u00b7 Online", F_SUB, 56, GOLD, stroke=3, shadow=5), W // 2, 362,
            alpha=clamp((local - 30) / 12), anchor="mt")
        b = badge_img(190)
        put(canvas, b, 450, 500, alpha=clamp((local - 46) / 12))
        put(canvas, text("An example mod for the OpenGGF Mod API", F_BODY, 46, WHITE, stroke=3, shadow=5), 680, 510,
            alpha=clamp((local - 52) / 12))
        put(canvas, text("github.com/OpenGGF/OpenGGF", F_TITLE_IT, 86, WHITE, stroke=5, shadow=7), 680, 572,
            alpha=clamp((local - 60) / 12))
        put(canvas, text("Mod API in development for OpenGGF 0.7", F_BODY, 30, CREAM, stroke=2), 684, 690,
            alpha=clamp((local - 70) / 12))
        put(canvas, text("Fan-made and free. Not affiliated with SEGA. Requires your own Sonic 2 ROM.",
                         F_BODY, 26, (195, 205, 215), stroke=2), W // 2, 980, alpha=clamp((local - 80) / 14), anchor="mt")
        put(canvas, text("Gameplay is real engine footage at normal speed with its own game audio.",
                         F_BODY, 24, (165, 180, 190), stroke=2), W // 2, 1022, alpha=clamp((local - 90) / 14), anchor="mt")
        return canvas
    segs.append(Seg("end", 540, "fade", 30, "Learn more", "end card; editorial Option Screen theme",
                    draw_fn=end_card, audio=[(EDITORIAL / "s2-music-89.wav", 0, 24, 516, 2.1)]))
    return segs


@lru_cache(maxsize=4)
def badge_img(size):
    return Image.open(BADGE).convert("RGBA").resize((size, size), Image.LANCZOS)


def align_beats(segs):
    """Shift an incoming gameplay clip by at most half a beat so Emerald Hill keeps its pulse
    across the cut. Only clips whose music is the zone bed at normal tempo on both sides move."""
    report = []
    for prev, seg in zip(segs, segs[1:]):
        if prev.cap is None or seg.cap is None or prev.title or seg.title:
            continue
        cut = seg.start + seg.tlen // 2
        out_row = prev.r0 + (cut - prev.start)
        in_row = seg.r0 + seg.tlen // 2
        a, b = bar_phase(prev.cap, out_row), bar_phase(seg.cap, in_row)
        if a is None or b is None:
            report.append({"cut_into": seg.name, "aligned": False, "reason": "no normal-tempo zone bed on both sides"})
            continue
        d = ((a - b + BEAT / 2) % BEAT) - BEAT / 2
        seg.shift = int(round(d)); seg.r0 += seg.shift
        report.append({"cut_into": seg.name, "aligned": True, "shift_rows": seg.shift,
                       "beat_phase_out": round(a % BEAT, 2), "beat_phase_in": round(bar_phase(seg.cap, seg.r0 + seg.tlen // 2) % BEAT, 2)})
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
def blend_transition(kind, a, b, u, f):
    """a: outgoing frame, b: incoming frame, u: 0..1 through the overlap."""
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
        out.paste(a.filter(ImageFilter.BoxBlur(18)) if 0.15 < u < 0.85 else a, (-shift, 0))
        out.paste(b.filter(ImageFilter.BoxBlur(18)) if 0.15 < u < 0.85 else b, (W - shift, 0))
        return out
    if kind == "iris":
        # A golf-hole iris: the old shot closes to a cup, the next opens from it.
        r_max = math.hypot(W, H) / 2
        if u < 0.5:
            r, src = r_max * (1 - smooth(u * 2)), a
        else:
            r, src = r_max * smooth((u - 0.5) * 2), b
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        md.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=255)
        out = Image.new("RGB", (W, H), (4, 10, 16))
        out.paste(src, (0, 0), mask)
        d = ImageDraw.Draw(out)
        if r > 2:
            d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=GOLD, width=8)
        if r < 26:
            d.ellipse((W / 2 - 26, H / 2 - 26, W / 2 + 26, H / 2 + 26), fill=(4, 10, 16), outline=GOLD, width=6)
        return out
    if kind == "bands":
        # Sonic 2 title-card homage: a blue band from the left and a gold band from the right meet,
        # then part to reveal the next shot.
        out = (a if u < 0.5 else b).copy()
        d = ImageDraw.Draw(out)
        cover = smooth(u * 2) if u < 0.5 else 1 - smooth((u - 0.5) * 2)
        blue_w = int(cover * (W * 0.62)); gold_w = int(cover * (W * 0.62))
        d.polygon([(0, 0), (blue_w + 160, 0), (blue_w, H), (0, H)], fill=(31, 73, 184))
        d.polygon([(W, 0), (W - gold_w, 0), (W - gold_w - 160, H), (W, H)], fill=(255, 212, 91))
        d.polygon([(W - gold_w - 30, 0), (W - gold_w, 0), (W - gold_w - 160, H), (W - gold_w - 190, H)], fill=RED)
        return out
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
        s = active[0]
        img = s.draw(f - s.start)
    else:
        a, b = active[0], active[1]
        u = (f - b.start + 0.5) / max(1, b.tlen)
        img = blend_transition(b.trans, a.draw(f - a.start), b.draw(f - b.start), u, f)
    if f < 12:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, f / 12)
    end = total_frames()
    if f > end - 20:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, (end - 1 - f) / 20)
    return img.convert("RGB").tobytes()


def mix_audio(path):
    segs = segments()
    n = total_frames() * SPF
    out = np.zeros((n, 2), np.float32)
    cache = {}

    def load(p):
        if p not in cache:
            with wave.open(str(p)) as w:
                assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2, p
                cache[p] = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
        return cache[p]

    placements = []
    for i, s in enumerate(segs):
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        for wav, src0, local0, count, gain in s.audio_pieces():
            data = load(wav)
            a = src0 * SPF
            o = (s.start + local0) * SPF
            length = min(count * SPF, len(data) - a)
            piece = data[a:a + length].copy() * gain
            fin = max(6, s.tlen) * SPF if i else 20 * SPF
            fout = max(6, nxt.tlen) * SPF if nxt else 30 * SPF
            # Equal-power fades at overlaps keep one continuous level through every cut.
            k = np.arange(length, dtype=np.float32)
            env = np.ones(length, np.float32)
            env = np.minimum(env, np.sin(np.clip(k / fin, 0, 1) * np.pi / 2))
            env = np.minimum(env, np.sin(np.clip((length - k) / fout, 0, 1) * np.pi / 2))
            piece *= env[:, None]
            end = min(n, o + length)
            out[o:end] += piece[:end - o]
            placements.append({"segment": s.name, "wav": str(wav), "source_frame": src0, "out_frame": s.start + local0,
                               "frames": length // SPF, "gain": gain})
    raw = BUILD / "soundtrack-raw.wav"
    write_wav(raw, out)
    # Two-pass EBU R128 linear normalisation.
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(raw), "-af",
                            "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-y", "-i", str(raw), "-af",
                    f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
                    f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(path)], check=True)
    return placements, m


def write_wav(path, data):
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def chapters():
    rows, last = [], None
    for s in segments():
        if s.chapter:
            rows.append((s.start, s.chapter))
    return rows


def write_edl():
    segs = segments()
    BUILD.mkdir(exist_ok=True)
    edl = {"fps": FPS, "frames": total_frames(), "seconds": total_frames() / FPS, "segments": [
        {"name": s.name, "start_frame": s.start, "frames": s.frames, "start_s": round(s.start / FPS, 3),
         "end_s": round((s.start + s.frames) / FPS, 3), "transition_in": s.trans, "transition_frames": s.tlen,
         "chapter": s.chapter, "source": s.source,
         "capture": s.cap, "first_row": s.r0 if s.cap else None, "last_row": s.r0 + s.frames - 1 if s.cap else None,
         "beat_shift_rows": s.shift,
         "audio": [{"wav": str(a[0]), "source_frame": a[1], "local_frame": a[2], "frames": a[3], "gain": a[4]} for a in s.audio_pieces()]}
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
            "Opener uses OpenGGF 0.6 Sonic 2 footage; Title/Option themes rendered from the Sonic 2 ROM in editing."]
    for i, (start, name) in enumerate(ch):
        end = ch[i + 1][0] if i + 1 < len(ch) else total_frames()
        meta += ["[CHAPTER]", "TIMEBASE=1/60", f"START={start}", f"END={end}", f"title={name}"]
    (BUILD / "chapters.ffmeta").write_text("\n".join(meta) + "\n")
    return edl


def extract_master():
    for name, first, count in [("ehz", 12, 84), ("cnz", 1218, 78), ("special", 1440, 78), ("sky", 3360, 96)]:
        out = BUILD / "master" / name
        if out.exists() and len(list(out.glob("*.png"))) == count:
            continue
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(MASTER), "-vf",
                        f"select='between(n\\,{first}\\,{first + count - 1})',crop=1920:1080:0:0", "-fps_mode", "passthrough",
                        "-frames:v", str(count), str(out / "%05d.png")], check=True)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    BUILD.mkdir(exist_ok=True)
    extract_master()
    if cmd == "edl":
        e = write_edl(); print(json.dumps({"frames": e["frames"], "seconds": e["seconds"]})); return
    if cmd == "frames":
        out = BUILD / "check"; out.mkdir(exist_ok=True)
        for a in sys.argv[2:]:
            f = int(a)
            Image.frombytes("RGB", (W, H), render_frame(f)).save(out / f"frame-{f:05d}.png")
        return
    if cmd == "sheet":
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        idx = list(range(0, total_frames(), step))
        with Pool(12) as pool:
            imgs = pool.map(render_frame, idx)
        cols = 6; tw, th = 384, 216
        sheet = Image.new("RGB", (cols * tw, ((len(idx) + cols - 1) // cols) * th))
        for k, b in enumerate(imgs):
            im = Image.frombytes("RGB", (W, H), b).resize((tw, th), Image.BILINEAR)
            ImageDraw.Draw(im).text((4, 4), f"{idx[k]} ({idx[k] / FPS:.1f}s)", fill=(255, 255, 0))
            sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
        sheet.save(ROOT / "promo.cuts.png"); return
    if cmd == "audio":
        placements, m = mix_audio(ROOT / "promo.soundtrack.wav")
        (ROOT / "promo.audio.json").write_text(json.dumps({"placements": placements, "loudnorm_first_pass": m}, indent=1) + "\n")
        return
    if cmd == "render":
        out = ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "putt-putt-paradise-promo.mp4")
        write_edl()
        placements, m = mix_audio(ROOT / "promo.soundtrack.wav")
        (ROOT / "promo.audio.json").write_text(json.dumps({"placements": placements, "loudnorm_first_pass": m}, indent=1) + "\n")
        n = total_frames()
        enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-y",
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-i", str(ROOT / "promo.soundtrack.wav"), "-i", str(BUILD / "chapters.ffmeta"),
                                "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", str(out)],
                               stdin=subprocess.PIPE)
        with Pool(12) as pool:
            for k, b in enumerate(pool.imap(render_frame, range(n), chunksize=6)):
                enc.stdin.write(b)
                if k % 600 == 0:
                    print(f"frame {k}/{n}", flush=True)
        enc.stdin.close()
        if enc.wait() != 0:
            raise SystemExit("encoder failed")
        print("wrote", out)


if __name__ == "__main__":
    main()
