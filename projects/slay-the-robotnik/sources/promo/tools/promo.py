#!/usr/bin/env python3
"""Slay the Robotnik promo: composites recorded mod clips, OpenGGF 0.6 engine footage, motion
typography and transitions into promo.mp4 (1920x1080, 60 fps), with a soundtrack rendered by
OpenGGF's own SMPS driver from the user's Sonic 3 & Knuckles ROM.

The edit is laid out in beats of Hydrocity Zone Act 2 (171.107 BPM, first beat at 0.316 s; see
beats.py and novelty.py), and the chapters sit on that track's section changes.

  promo.py prep              extract the in-game logo and the event picture rectangle
  promo.py sheet [step]      contact sheet of output frames (for checking the layout)
  promo.py frames a b c      write single output frames as PNG
  promo.py audio             mix the soundtrack only
  promo.py render            full render to promo.mp4 (8 worker processes)
"""
import math
import subprocess
import sys
import wave
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "build/frames"
ASSETS = ROOT / "build/assets"
WT = Path("/home/farrell/code/projects/OpenGGF/.worktrees/ai-slay-the-robotnik")
BACKDROPS = WT / "target/scene-backdrops"
BADGE = WT / "src/main/resources/icon/openggf-256.png"
W, H, FPS, SR = 1920, 1080, 60, 48000
SPF = SR // FPS  # audio samples per video frame
PERIOD, FIRST = 60 / 171.107, 0.316

FONT_DIR = "/usr/share/fonts/TTF/"
F_TITLE = "FiraSansCompressed-Heavy.ttf"
F_HEAVY_IT = "FiraSansCompressed-HeavyItalic.ttf"
F_SUB = "FiraSansCondensed-BoldItalic.ttf"
F_BODY = "FiraSans-Bold.ttf"
F_BODY_IT = "FiraSans-BoldItalic.ttf"
F_MONO = "Hack-Regular.ttf"
F_MONO_B = "Hack-Bold.ttf"

WHITE = (255, 255, 255)
YELLOW = (255, 210, 31)
NAVY = (8, 16, 56)
BLUE = (22, 56, 184)
RED = (224, 32, 32)
BLACK = (0, 0, 0)


def bt(k):
    return FIRST + k * PERIOD


def bf(k):
    return int(round(bt(k) * FPS))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def ease_in(u):
    u = clamp(u)
    return u ** 3


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def back(u, s=1.6):
    u = clamp(u) - 1
    return u * u * ((s + 1) * u + s) + 1


# ------------------------------------------------------------------------------------ images

@lru_cache(maxsize=None)
def clip_len(name):
    return len(list((FRAMES / name).glob("frame-*.png")))


@lru_cache(maxsize=160)
def clip_frame(name, i):
    i = int(clamp(i, 0, clip_len(name) - 1))
    return Image.open(FRAMES / name / f"frame-{i:05d}.png").convert("RGB")


@lru_cache(maxsize=40)
def engine_frame(shot, i):
    files = sorted((ROOT / "build/engine" / shot).glob("*.png"))
    return Image.open(files[int(clamp(i, 0, len(files) - 1))]).convert("RGB")


def resample(img, x0, y0, vw, vh, ow, oh):
    """Pixel-art scaling: nearest-neighbour up by an integer factor, then an area filter down to
    the output, so pixels stay square and sharp at any zoom or sub-pixel position."""
    k = max(1, math.ceil(ow / vw - 1e-9))
    ix0, iy0 = math.floor(x0), math.floor(y0)
    ix1, iy1 = min(img.width, math.ceil(x0 + vw)), min(img.height, math.ceil(y0 + vh))
    crop = img.crop((ix0, iy0, ix1, iy1)).resize(((ix1 - ix0) * k, (iy1 - iy0) * k), Image.NEAREST)
    box = ((x0 - ix0) * k, (y0 - iy0) * k, (x0 - ix0 + vw) * k, (y0 - iy0 + vh) * k)
    return crop.resize((ow, oh), Image.BOX, box=box)


def game_view(img, cx=200.0, cy=112.0, zoom=1.0, ow=W, oh=H):
    vh = img.height / zoom
    vw = vh * ow / oh
    if vw > img.width:
        vw = img.width / zoom
        vh = vw * oh / ow
    x0 = clamp(cx - vw / 2, 0, img.width - vw)
    y0 = clamp(cy - vh / 2, 0, img.height - vh)
    return resample(img, x0, y0, vw, vh, ow, oh)


def arr(img):
    return np.asarray(img, dtype=np.float32)


def paste(canvas, rgba, x, y, alpha=1.0):
    """Alpha-composites a float RGBA array onto the float RGB canvas at integer (x, y)."""
    if alpha <= 0:
        return
    x, y = int(round(x)), int(round(y))
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(canvas.shape[1], x + w), min(canvas.shape[0], y + h)
    if x0 >= x1 or y0 >= y1:
        return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = src[..., 3:4] * (alpha / 255.0)
    region = canvas[y0:y1, x0:x1]
    region *= 1 - a
    region += src[..., :3] * a


def scaled(rgba, s):
    """A float RGBA array resized by s (for pops); returned array is float32."""
    if abs(s - 1) < 1e-3:
        return rgba
    im = Image.fromarray(rgba.astype(np.uint8), "RGBA")
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s))
    return arr(im.resize((w, h), Image.BILINEAR))


@lru_cache(maxsize=None)
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


@lru_cache(maxsize=512)
def text(s, fname, size, fill=WHITE, stroke=0, sfill=BLACK, shadow=0, scol=(0, 0, 40, 170)):
    f = font(fname, size)
    l, t, r, b = f.getbbox(s, stroke_width=stroke)
    pad = stroke + 6
    w, h = r - l + 2 * pad + shadow, b - t + 2 * pad + shadow
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + shadow, pad - t + shadow), s, font=f, fill=scol,
                                stroke_width=stroke, stroke_fill=scol)
        base = Image.alpha_composite(base, sh)
    top = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(top).text((pad - l, pad - t), s, font=f, fill=fill + (255,), stroke_width=stroke,
                             stroke_fill=sfill + (255,))
    return arr(Image.alpha_composite(base, top))


@lru_cache(maxsize=None)
def rom_banner(scale):
    im = Image.open(BACKDROPS / "titlecard-aiz1-0.png").convert("RGBA")
    return arr(im.resize((im.width * scale, im.height * scale), Image.NEAREST))


@lru_cache(maxsize=None)
def badge(size):
    im = Image.open(BADGE).convert("RGBA")
    return arr(im.resize((size, size), Image.NEAREST if size % 256 == 0 else Image.LANCZOS))


@lru_cache(maxsize=None)
def glyphs():
    """The mod's own pixel font, art/font.txt: '= X' then five rows of '#' (ink) and '.'."""
    out, name, rows = {}, None, []
    for line in (WT / "examples/slay-the-robotnik/src/main/resources/art/font.txt").read_text().splitlines():
        if line.startswith("= "):
            name, rows = line[2:3], []
        elif name and line and line[0] in "#.":
            rows.append(line)
            if len(rows) == 5:
                out[name] = rows
    return out


def font_width(s):
    g = glyphs()
    return max(0, sum(4 if ch == " " else len(g[ch][0]) + 1 for ch in s) - 1)


def font_draw(px, s, x, y, colour, scale):
    g = glyphs()
    for ch in s:
        if ch == " ":
            x += 4 * scale
            continue
        for gy, row in enumerate(g[ch]):
            for gx, v in enumerate(row):
                if v == "#":
                    px[y + gy * scale:y + (gy + 1) * scale, x + gx * scale:x + (gx + 1) * scale] = colour
        x += (len(g[ch][0]) + 1) * scale


def logo_pixels(shine=None):
    """The title logo as TitleScreen.drawLogo draws it (without the bob), in game pixels:
    'SLAY THE' outlined at 2x over 'ROBOTNIK' at 4x with a thick navy outline, a dark red drop,
    a red body and a yellow upper half; shine is the x of the sweeping highlight, if any."""
    big, top = "ROBOTNIK", "SLAY THE"
    bw = font_width(big) * 4
    w, h = bw + 8, 16 + 20 + 6
    px = np.zeros((h, w, 4), np.uint8)
    cx, y = w // 2, 2
    tx = cx - font_width(top) * 2 // 2
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                font_draw(px, top, tx + dx, y + dy, (0, 0, 0, 255), 2)
    font_draw(px, top, tx, y, (255, 255, 255, 255), 2)
    bx, by = cx - bw // 2, y + 16
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            font_draw(px, big, bx + dx, by + dy, (0, 0, 0x24, 255), 4)
    font_draw(px, big, bx, by + 2, (0x90, 0, 0, 255), 4)
    font_draw(px, big, bx, by, (0xDA, 0x24, 0x24, 255), 4)
    body = np.zeros_like(px)
    font_draw(body, big, bx, by, (0xFF, 0xDA, 0x24, 255), 4)
    px[by:by + 10][body[by:by + 10, ..., 3] > 0] = body[by:by + 10][body[by:by + 10, ..., 3] > 0]
    if shine is not None:
        x0, x1 = int(bx + shine), int(bx + shine + 6)
        region = px[by:by + 20, max(bx, x0):min(bx + bw, x1)]
        m = region[..., 3] > 0
        region[m, :3] = (region[m, :3] * 0.62 + 255 * 0.38).astype(np.uint8)
    return px


@lru_cache(maxsize=None)
def logo(scale, shine=None):
    px = logo_pixels(shine)
    im = Image.fromarray(px, "RGBA")
    return arr(im.resize((im.width * scale, im.height * scale), Image.NEAREST))


@lru_cache(maxsize=None)
def panel_rect():
    return tuple(int(v) for v in (ASSETS / "panel.txt").read_text().split())


@lru_cache(maxsize=None)
def grids():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    return xs, ys, np.hypot(xs - W / 2, ys - H / 2)


@lru_cache(maxsize=None)
def top_shade():
    """A dark gradient over the upper 30% of the screen, for a line of text across the top."""
    a = np.zeros((H, W, 4), np.float32)
    a[..., 3] = (np.clip(1 - np.arange(H) / (H * 0.3), 0, 1) ** 1.3 * 190)[:, None]
    return a


@lru_cache(maxsize=None)
def bottom_shade():
    """A dark gradient over the lower 45% of the screen, for legibility behind headers."""
    a = np.zeros((H, W, 4), np.float32)
    ramp = np.clip((np.arange(H) - H * 0.55) / (H * 0.45), 0, 1) ** 1.2 * 200
    a[..., 3] = ramp[:, None]
    return a


def stripes(f, c0=(10, 20, 64), c1=(16, 30, 90)):
    xs, ys, _ = grids()
    m = (((xs + ys * 0.6 + f * 2.5) // 70) % 2)[..., None]
    return np.where(m > 0, np.array(c1, np.float32), np.array(c0, np.float32)).astype(np.float32)


@lru_cache(maxsize=None)
def rounded(w, h, r, fill, alpha=255):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill + (alpha,))
    return arr(im)


# ------------------------------------------------------------------------------------- shots

PUNCHES = []  # (frame, amplitude): a quick zoom kick that decays over 12 frames


def punch(f):
    z = 1.0
    for pf, amp in PUNCHES:
        d = f - pf
        if 0 <= d < 14:
            z += amp * (1 - d / 14) ** 2
    return z


class Shot:
    def __init__(self, b0, b1, trans=None, tdur=0):
        self.f0, self.f1 = bf(b0), bf(b1)
        self.trans, self.tdur = trans, tdur

    def u(self, f):
        return (f - self.f0) / max(1, self.f1 - self.f0)


class Game(Shot):
    """A recorded mod clip: src is the clip frame at the shot's first frame; cam(u) gives the
    camera (centre x, centre y, zoom) in game pixels over the shot; hold freezes on a clip frame."""

    def __init__(self, b0, b1, clip, src, cam=None, trans=None, tdur=0, hold=None, stems=1.0, dim=0.0):
        super().__init__(b0, b1, trans, tdur)
        self.clip, self.src, self.cam, self.hold, self.stems, self.dim = clip, src, cam, hold, stems, dim

    def src_frame(self, f):
        i = self.src + (f - self.f0)
        return min(i, self.hold) if self.hold is not None else i

    def image(self, f):
        cx, cy, z = self.cam(self.u(f)) if self.cam else (200, 112, 1.0)
        c = arr(game_view(clip_frame(self.clip, self.src_frame(f)), cx, cy, z * punch(f)))
        if self.dim:
            c *= 1 - self.dim
        return c


class Engine(Shot):
    """OpenGGF 0.6 footage (already 6x pixel-scaled and cropped to 16:9)."""

    def __init__(self, b0, b1, shot, src=0, zoom=(1.0, 1.0), hold=None, trans=None, tdur=0, dim=0.0):
        super().__init__(b0, b1, trans, tdur)
        self.shot, self.src, self.zoom, self.hold, self.dim = shot, src, zoom, hold, dim

    def image(self, f):
        i = self.src + (f - self.f0)
        if self.hold is not None:
            i = min(i, self.hold)
        im = engine_frame(self.shot, i)
        z = (self.zoom[0] + (self.zoom[1] - self.zoom[0]) * smooth(self.u(f))) * punch(f)
        if z > 1.001:
            vw, vh = W / z, H / z
            im = im.resize((W, H), Image.BICUBIC, box=((W - vw) / 2, (H - vh) / 2, (W + vw) / 2, (H + vh) / 2))
        c = arr(im)
        if self.dim:
            c *= 1 - self.dim
        return c


class Custom(Shot):
    def __init__(self, b0, b1, fn, trans=None, tdur=0):
        super().__init__(b0, b1, trans, tdur)
        self.fn = fn

    def image(self, f):
        return self.fn(f, self)


# ---------------------------------------------------------------------------------- overlays

class Overlay:
    def __init__(self, f0, f1):
        self.f0, self.f1 = f0, f1


class Header(Overlay):
    """Section title in the manner of the S3K title card: the ROM's own red banner drops from the
    top at a constant speed while the title and subtitle slide in from the right, then everything
    leaves at double speed (as ObjArray_TtlCard does)."""

    def __init__(self, b_in, b_out, title, sub=None):
        super().__init__(bf(b_in), bf(b_out) + 16)
        self.out = bf(b_out)
        self.title = text(title, F_TITLE, 150, WHITE, stroke=8, shadow=9)
        self.sub = text(sub, F_SUB, 50, YELLOW, stroke=4, shadow=5) if sub else None

    def draw(self, c, f):
        t, e = f - self.f0, f - self.out
        shade = clamp(t / 10) * (1 - clamp(e / 12))
        paste(c, bottom_shade(), 0, 0, shade)
        ban = rom_banner(3)
        y_end = 1012 - ban.shape[0]
        y = min(y_end, -ban.shape[0] + 68 * t)
        if e > 0:
            y = y_end - 140 * e
        paste(c, ban, 72, y)
        x_end = 300
        tx = max(x_end, W + 40 - 125 * (t - 3))
        sx = max(x_end + 8, W + 40 - 125 * (t - 7))
        if e > 0:
            tx = x_end + 260 * max(0, e - 2)
            sx = x_end + 8 + 260 * e
        ty = 1000 - (self.sub.shape[0] if self.sub is not None else 0) - self.title.shape[0] + 26
        paste(c, self.title, tx, ty)
        if self.sub is not None:
            paste(c, self.sub, sx, ty + self.title.shape[0] - 22)


class Txt(Overlay):
    """A pre-rendered text (or image) with an entrance and exit: 'left'/'right' slide, 'pop'
    scale, 'fade', or 'up'. Anchor is the top-left unless centre=True."""

    def __init__(self, f0, f1, img, x, y, enter="fade", leave="fade", centre=False, dur=10, alpha=1.0):
        super().__init__(f0, f1)
        self.img, self.x, self.y, self.enter, self.leave = img, x, y, enter, leave
        self.centre, self.dur, self.alpha = centre, dur, alpha

    def draw(self, c, f):
        img = self.img
        u_in = (f - self.f0) / self.dur
        u_out = (self.f1 - f) / 8
        a = self.alpha
        x, y = self.x, self.y
        s = 1.0
        if u_in < 1:
            if self.enter == "fade":
                a *= smooth(u_in)
            elif self.enter == "left":
                x -= (1 - ease_out(u_in)) * (img.shape[1] + 200)
                a *= clamp(u_in * 3)
            elif self.enter == "right":
                x += (1 - ease_out(u_in)) * 700
                a *= clamp(u_in * 3)
            elif self.enter == "up":
                y += (1 - ease_out(u_in)) * 80
                a *= smooth(u_in)
            elif self.enter == "pop":
                s = 0.4 + 0.6 * back(u_in, 2.2)
                a *= clamp(u_in * 4)
        if u_out < 1:
            if self.leave == "left":
                x -= (1 - smooth(u_out)) * (img.shape[1] + 300)
            elif self.leave == "pop":
                s *= 1 + (1 - u_out) * 0.25
                a *= smooth(u_out)
            else:
                a *= smooth(u_out)
        if s != 1.0:
            img = scaled(img, s)
        if self.centre:
            x, y = x - img.shape[1] / 2, y - img.shape[0] / 2
        paste(c, img, x, y, a)


class Flash(Overlay):
    def __init__(self, f, dur=12, peak=1.0, colour=WHITE):
        super().__init__(f, f + dur)
        self.peak, self.colour = peak, np.array(colour, np.float32)

    def draw(self, c, f):
        a = self.peak * (1 - (f - self.f0) / (self.f1 - self.f0)) ** 2
        c *= 1 - a
        c += self.colour * a


class Fade(Overlay):
    """Fade to (or from) black across [f0, f1)."""

    def __init__(self, f0, f1, out=True):
        super().__init__(f0, f1)
        self.out = out

    def draw(self, c, f):
        u = smooth((f - self.f0) / max(1, self.f1 - self.f0))
        c *= (1 - u) if self.out else u


class Fn(Overlay):
    def __init__(self, f0, f1, fn):
        super().__init__(f0, f1)
        self.fn = fn

    def draw(self, c, f):
        self.fn(c, f, self)


# ------------------------------------------------------------------------------- transitions

def wipe(old, new, f, t0, dur):
    """Three slanted bands, blue, yellow and red, sweep left to right; the new shot follows them."""
    xs, ys, _ = grids()
    u = smooth((f - t0) / dur)
    edge = -500 + (W + 1100) * u
    bound = xs - (edge + 0.42 * (ys - H / 2))
    out = np.where((bound > 0)[..., None], old, new)
    for k, col in enumerate([BLUE, YELLOW, RED]):
        m = (bound <= -k * 70) & (bound > -(k + 1) * 70 - (25 if k == 2 else 0))
        out[m] = np.array(col, np.float32)
    return out


def iris(old, new, f, t0, dur):
    """A Giant Ring opening from the centre: the new shot inside a gold ring that grows."""
    _, _, dist = grids()
    u = ease_out((f - t0) / dur)
    r = 1200 * u
    out = np.where((dist < r)[..., None], new, old)
    ring = (dist >= r - 34) & (dist < r)
    hi = (dist >= r - 22) & (dist < r - 12)
    out[ring] = np.array((232, 168, 16), np.float32)
    out[hi] = np.array((255, 244, 160), np.float32)
    return out


def crossfade(old, new, f, t0, dur):
    u = smooth((f - t0) / dur)
    return old * (1 - u) + new * u


TRANSITIONS = {"wipe": wipe, "iris": iris, "xfade": crossfade}

# ------------------------------------------------------------------------- composite scenes

EVENT_CELLS = [  # clip, picture-animation start, label: spread over Hydrocity, Launch Base and Angel Island
    ("p07-ev-giant_ring", 92, "GIANT RING"),
    ("p07-ev-special_stage", 418, "SPECIAL STAGE WARP"),
    ("p07-ev-emerald_altar", 92, "EMERALD ALTAR"),
    ("p07-ev-robotnik_lab", 92, "ROBOTNIK'S LAB"),
    ("p07-ev-chao_cart", 92, "CHAO CART"),
    ("p07-ev-monitor_row", 92, "MONITOR ROW"),
    ("p07-ev-mirror_monitor", 425, "MIRROR MONITOR"),
    ("p07-ev-robotnik_offer", 92, "ROBOTNIK'S OFFER"),
]
EVENT_LAST = {"p07-ev-special_stage": 560, "p07-ev-mirror_monitor": 560}


def mosaic(f, shot):
    c = stripes(f)
    x0, y0, x1, y1 = panel_rect()
    pw, ph = x1 - x0, y1 - y0
    cw, ch = int(2.5 * pw), int(2.5 * ph)
    gap = 44
    left = (W - 4 * cw - 3 * gap) // 2
    top = 40
    for i, (clip, start, label) in enumerate(EVENT_CELLS):
        appear = bf(115 + i)
        if f < appear:
            continue
        u = (f - appear) / 12
        s = 0.5 + 0.5 * back(u, 2.0) if u < 1 else 1.0
        col, row = i % 4, i // 4
        cx = left + col * (cw + gap) + cw / 2
        cy = top + row * (ch + 96) + ch / 2
        src = min(start + (f - appear), EVENT_LAST.get(clip, 420))
        pic = game_view(clip_frame(clip, src).crop((x0, y0, x1, y1)), pw / 2, ph / 2, 1.0, cw, ch)
        cell = Image.new("RGBA", (cw + 16, ch + 16), YELLOW + (255,))
        cell.paste(pic, (8, 8))
        cell = arr(cell)
        if s != 1.0:
            cell = scaled(cell, s)
        paste(c, cell, cx - cell.shape[1] / 2, cy - cell.shape[0] / 2, clamp(u * 3))
        lab = text(label, F_HEAVY_IT, 40, WHITE, stroke=4, shadow=4)
        paste(c, lab, cx - lab.shape[1] / 2, cy + ch / 2 + 16, clamp((u - 0.3) * 2))
    return c


def rom_wall(f, shot):
    """Three vertical slices of the mod in motion, dimmed, behind the ROM statement."""
    c = np.zeros((H, W, 3), np.float32)
    u = shot.u(f)
    parts = [("p01-title", 1280, 300, 60), ("p06-boss-big_arm", 60, 330, 120), ("p07-ev-special_stage", 420, 75, 108)]
    for k, (clip, src, cx, cy) in enumerate(parts):
        im = game_view(clip_frame(clip, src + (f - shot.f0)), cx - 10 + 20 * u, cy, 1.0 + 0.08 * u, 640, H)
        c[:, k * 640:(k + 1) * 640] = arr(im)
    c *= 0.38
    return c


CODE = [
    ("c", "// A whole mod: register a scene..."),
    ("k", "public final class HelloSceneMod implements GgfMod {"),
    ("k", "    public void register(ModContext context) {"),
    ("n", "        context.registerStartupScene(HelloScene::new);"),
    ("n", "    }"),
    ("n", "}"),
    ("n", ""),
    ("c", "// ...that draws and plays from your ROM:"),
    ("n", "background = rom.zoneBackdrop(0, 0);  // Angel Island"),
    ("n", "sonic = rom.character(\"sonic\");"),
    ("n", "ctx.audio().playSfx(SFX_RING);"),
]
KEYWORDS = ("public", "final", "class", "implements", "void")


@lru_cache(maxsize=None)
def code_panel(chars):
    w, h = 900, 600
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(14, 18, 34, 235), outline=(70, 90, 160, 255), width=3)
    for k, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((22 + k * 30, 18, 40 + k * 30, 36), fill=col)
    d.text((120, 14), "HelloSceneMod.java", font=font(F_MONO, 22), fill=(150, 160, 190))
    f = font(F_MONO, 25)
    left = chars
    y = 66
    for kind, line in CODE:
        shown = line[:max(0, left)]
        left -= len(line) + 1
        x = 26
        if kind == "c":
            d.text((x, y), shown, font=f, fill=(110, 130, 120))
        else:
            for tok in shown.split(" "):
                colour = (255, 150, 70) if tok in KEYWORDS else (120, 190, 255) if tok[:1].isupper() else (225, 230, 240)
                if '"' in tok:
                    colour = (160, 220, 120)
                d.text((x, y), tok, font=f, fill=colour)
                x += f.getlength(tok + " ")
        y += 46
    return arr(im)


def make_your_own(f, shot):
    c = stripes(f, (8, 14, 46), (12, 22, 66))
    chars = int((f - shot.f0) * 7.5)
    paste(c, code_panel(min(chars, 400)), 60, 300)
    view = arr(game_view(clip_frame("p12-hello", 40 + (f - shot.f0)), 200, 112, 1.0, 880, 493))
    frame = np.zeros((493 + 16, 880 + 16, 4), np.float32)
    frame[..., :3] = YELLOW
    frame[..., 3] = 255
    frame[8:-8, 8:-8, :3] = view
    paste(c, frame, 990, 352)
    return c


def end_card(f, shot):
    src = 1300 + (f - shot.f0)
    bg = clip_frame("p01-title", src).filter(ImageFilter.GaussianBlur(3))
    c = arr(game_view(bg, 290, 110, 1.35)) * 0.42
    return c



# ----------------------------------------------------------------- multi-panel compositions

SLANT = 0.22  # the split-screen dividers lean like the title card's speed lines
CLASSICS = [  # engine clip, appears at beat, label
    ("s1", 4, "SONIC THE HEDGEHOG"),
    ("s2", 8, "SONIC THE HEDGEHOG 2"),
    ("s3", 12, "SONIC 3 & KNUCKLES"),
]


@lru_cache(maxsize=None)
def slice_masks():
    xs, ys, _ = grids()
    d1 = 640 + SLANT * (ys - H / 2)
    d2 = 1280 + SLANT * (ys - H / 2)
    return (xs < d1, (xs >= d1) & (xs < d2), xs >= d2,
            np.abs(xs - d1) < 7, np.abs(xs - d2) < 7)


@lru_cache(maxsize=None)
def chip(name, size=50):
    t = Image.fromarray(text(name, F_HEAVY_IT, size, NAVY).astype(np.uint8), "RGBA")
    pill = Image.fromarray(rounded(t.width + 44, t.height + 12, 14, YELLOW).astype(np.uint8), "RGBA")
    pill.alpha_composite(t, (22, 6))
    return arr(pill)


def classics(f, shot):
    """Sonic 1, 2 and 3 & Knuckles side by side in three slanted slices that drop in on the beat."""
    c = stripes(f)
    masks = slice_masks()
    ys = grids()[1]
    for i, (clip, b, label) in enumerate(CLASSICS):
        t0 = bf(b)
        if f < t0:
            continue
        drop = int(round(-(1 - ease_out((f - t0) / 16)) * H))
        src = arr(engine_frame(clip, f - t0))
        shift = (320, 960, 1600)[i] - 900  # bring the middle of the game screen into the slice
        src = np.roll(np.roll(src, shift, axis=1), drop, axis=0)
        m = masks[i] & (ys < H + drop)
        c[m] = src[m]
        if i:
            c[masks[2 + i] & (ys < H + drop)] = np.array(YELLOW, np.float32)
        pill = chip(label)
        cx = (320, 960, 1600)[i] + SLANT * (985 - H / 2)
        paste(c, pill, cx - pill.shape[1] / 2, 960 + drop, clamp((f - t0 - 8) / 8))
    return c


BOSSES = [  # clip, appears at beat; each lands on clip frame 44, two beats after it appears
    ("p06-boss-flame_craft", 88),
    ("p06-boss-big_shaker", 91),
    ("p06-boss-big_arm", 94),
    ("p06-boss-beam_rocket", 97),
]
PANEL_W, PANEL_H = 930, 521


@lru_cache(maxsize=None)
def framed(w, h, border=5, colour=(108, 144, 218)):
    a = np.zeros((h + 2 * border, w + 2 * border, 4), np.float32)
    a[..., :3] = colour
    a[..., 3] = 255
    return a


def panel(c, img, x, y, f, t0, label=None):
    """A game view in a light-blue frame that pops in at t0, with an optional label beneath."""
    u = (f - t0) / 10
    fr = framed(img.width, img.height).copy()
    fr[5:-5, 5:-5, :3] = arr(img)
    s = 0.86 + 0.14 * back(u, 2.0) if u < 1 else 1.0
    if s != 1.0:
        fr = scaled(fr, s)
    w, h = img.width + 10, img.height + 10
    paste(c, fr, x + (w - fr.shape[1]) / 2, y + (h - fr.shape[0]) / 2, clamp(u * 3))
    if label:
        lab = text(label, F_HEAVY_IT, 44, WHITE, stroke=4, shadow=4)
        paste(c, lab, x + w / 2 - lab.shape[1] / 2, y + h + 10, clamp((u - 0.4) * 2))


def boss_grid(f, shot):
    c = stripes(f)
    for i, (clip, b) in enumerate(BOSSES):
        t0 = bf(b)
        if f < t0:
            continue
        x, y = (14 + (i % 2) * (PANEL_W + 30), 9 + (i // 2) * (PANEL_H + 18))
        panel(c, game_view(clip_frame(clip, 2 + f - t0), 200, 112, 1.0, PANEL_W, PANEL_H), x, y, f, t0)
    return c


ROOMS = [  # clip, first clip frame, appears at beat, label
    ("p08-capsule", 20, 132, "EGG CAPSULES HOLD RELICS"),
    ("p08-starpost", 40, 133.5, "STARPOSTS HEAL OR UPGRADE"),
    ("p08-shop", 100, 135, "THE SHOP SELLS EVERYTHING"),
]
ROOM_W, ROOM_H = 592, 331


def rooms(f, shot):
    c = stripes(f)
    for i, (clip, src, b, label) in enumerate(ROOMS):
        t0 = bf(b)
        if f < t0:
            continue
        x = 26 + i * (ROOM_W + 32)
        panel(c, game_view(clip_frame(clip, src + f - t0), 200, 112, 1.0, ROOM_W, ROOM_H), x, 120, f, t0, label)
    return c

# ------------------------------------------------------------------------------------- edit

def cam_static(cx=200, cy=112, z=1.0):
    return lambda u: (cx, cy, z)


def cam_move(a, b, ease=smooth):
    return lambda u: tuple(a[k] + (b[k] - a[k]) * ease(u) for k in range(3))


def slam(z0=1.25, frames=24, total=1, cx=200, cy=112):
    return lambda u: (cx, cy, 1 + (z0 - 1) * (1 - ease_out(u * total * FPS / frames)) if u * total * FPS < frames else 1.0)


SHOTS = []
OVERLAYS = []
SFX = []  # (frame, sfx id, gain)
STEMS = []  # (clip, first clip frame, output frame, frames, gain): effects under multi-panel shots


def build():
    for lst in (SHOTS, OVERLAYS, SFX, PUNCHES, STEMS):
        lst.clear()
    S, O, X = SHOTS.append, OVERLAYS.append, SFX.append
    # ---- A. cold open: OpenGGF and the three games it plays, side by side
    S(Engine(0, 4, "e1", 0, zoom=(1.0, 1.05), dim=0.45))
    O(Txt(bf(0), bf(4), badge(512), W / 2, 450, enter="pop", leave="fade", centre=True, dur=16))
    O(Txt(bf(0) + 14, bf(4), text("THE OPEN-SOURCE ENGINE FOR CLASSIC SONIC", F_BODY, 44, WHITE, shadow=4), W / 2, 790,
          enter="up", centre=True))
    S(Custom(4, 16, classics))
    for _, b, _ in CLASSICS:
        X((bf(b), 0x33, 0.45))
    O(Fn(bf(5), bf(16), lambda c, f, o: paste(c, top_shade(), 0, 0, clamp((f - o.f0) / 10) * (1 - clamp((f - o.f1 + 8) / 8)))))
    O(Txt(bf(5), bf(16), text("Rebuilt from scratch in Java, faithful to the originals", F_HEAVY_IT, 74, WHITE,
                              stroke=6, shadow=7), W / 2, 90, enter="up", leave="fade", centre=True, dur=14))
    S(Engine(16, 20, "e8", 0, zoom=(1.0, 1.2), hold=50))
    O(Fn(bf(16), bf(20), lambda c, f, o: c.__imul__(1 - 0.45 * smooth((f - o.f0) / 40))))
    for k, word in enumerate(["NOW,", "SOMETHING", "NEW."]):
        O(Txt(bf(16 + k * 1.33), bf(20), text(word, F_TITLE, 190, WHITE, stroke=9, shadow=10), W / 2,
              300 + k * 210, enter="pop", leave="fade", centre=True, dur=10))
        X((bf(16 + k * 1.33), 0xAB, 0.75))
    # ---- B. title drop
    S(Game(20, 36, "p01-title", 760, cam=slam(1.3, 26, 16 * PERIOD), stems=0))
    O(Flash(bf(20), 18))
    X((bf(20), 0xB6, 1.0))
    tag = text("A SONIC DECK-BUILDING ROGUELIKE", F_HEAVY_IT, 92, YELLOW, stroke=7, shadow=8)
    tag2 = text("An example mod for the OpenGGF engine", F_BODY_IT, 46, WHITE, stroke=4, shadow=5)
    O(Fn(bf(23.5), bf(35), lambda c, f, o: paste(c, bottom_shade(), 0, 0, clamp((f - o.f0) / 12) * (1 - clamp((f - o.f1 + 10) / 10)))))
    O(Txt(bf(23.5), bf(35), tag, 1880 - tag.shape[1], 835, enter="right", leave="fade", dur=14))
    O(Txt(bf(25.5), bf(35), tag2, 1880 - tag2.shape[1], 950, enter="right", leave="fade", dur=14))
    # ---- C1. heroes, the spin-dash off and Angel Island's title card, in one take
    S(Game(36, 56, "p02-select", 110, cam=cam_move((200, 112, 1.06), (200, 112, 1.0)), trans="wipe", tdur=16))
    X((bf(36) - 6, 0x42, 0.8))
    O(Header(36.5, 42.5, "CHOOSE YOUR HERO", "Sonic, Tails or Knuckles: three decks, three ways to play"))
    # ---- C2. one take of a run: Hydrocity's map, a badnik node, the fight, the victory
    def journey_cam(u):
        src = 95 + u * (bf(88) - bf(56))
        if src < 200:  # the map: drift across it
            k = (src - 95) / 105
            return (150 + 100 * k, 112, 1.3)
        return (200, 112, 1.0)
    S(Game(56, 88, "p13-journey", 95, cam=journey_cam, trans="wipe", tdur=14))
    X((bf(56) - 6, 0x42, 0.7))
    O(Header(56.3, 59.3, "CHART YOUR PATH", "Angel Island  /  Hydrocity  /  Launch Base  /  Sky Sanctuary"))
    O(Header(62, 67, "PLAY YOUR CARDS", "139 cards across three heroes"))
    # ---- C4. bosses, four at once
    S(Custom(88, 103, boss_grid, trans="wipe", tdur=14))
    X((bf(88) - 6, 0x42, 0.7))
    for clip, b in BOSSES:
        STEMS.append((clip, 2, bf(b), bf(103) - bf(b), 0.7))
    O(Header(88.3, 92.6, "BOSSES DROP IN", "Built from the original games' own sprites"))
    # ---- C5. events: the slot machine, then eight more at once
    S(Game(103, 115, "p07-ev-slot_machine", 118, cam=cam_move((150, 104, 1.25), (120, 108, 1.5)),
           trans="wipe", tdur=14, stems=0.55))
    X((bf(103) - 6, 0x42, 0.7))
    O(Header(103.5, 109.5, "22 EVENTS", "The slot machine spins the bonus stage's real reels"))
    S(Custom(115, 132, mosaic, trans="xfade", tdur=14))
    for i in range(len(EVENT_CELLS)):
        X((bf(115 + i), 0x33, 0.35))
    O(Txt(bf(123), bf(131.5), text("Every choice plays out with the game's own objects and sounds", F_HEAVY_IT, 54,
                                   YELLOW, stroke=5, shadow=5), W / 2, 1028, enter="up", centre=True, dur=12))
    # ---- C6. relics, items and upgrades: three rooms at once, then the numbers
    S(Custom(132, 149, rooms, trans="wipe", tdur=14))
    X((bf(132) - 6, 0x42, 0.7))
    for clip, src, b, _ in ROOMS:
        STEMS.append((clip, src, bf(b), bf(149) - bf(b), 0.6))
    O(Header(132.4, 138, "RELICS, ITEMS & UPGRADES"))
    stats = [("139", "CARDS"), ("55", "RELICS"), ("16", "ITEM MONITORS"), ("45", "ENCOUNTERS")]
    for k, (num, label) in enumerate(stats):
        start = bf(140) + k * 8
        cx = 240 + k * 480

        def counter(c, f, o, num=int(num), cx=cx, label=label, start=start):
            u = clamp((f - start) / 26)
            v = int(round(num * ease_out(u)))
            a = clamp((f - start) / 6)
            n_img = text(str(v), F_TITLE, 190, YELLOW, stroke=8, shadow=8)
            paste(c, n_img, cx - n_img.shape[1] / 2, 620, a)
            l_img = text(label, F_HEAVY_IT, 50, WHITE, stroke=5, shadow=5)
            paste(c, l_img, cx - l_img.shape[1] / 2, 860, a)

        O(Fn(start, bf(149), counter))
        X((start, 0x33, 0.3))
    # ---- D. the engine underneath
    S(Custom(149, 161, rom_wall))
    O(Flash(bf(149), 10, 0.6))
    for k, word in enumerate(["EVERY SPRITE.", "EVERY SOUND.", "EVERY STAGE."]):
        O(Txt(bf(149 + k * 1.5), bf(160.5), text(word, F_TITLE, 150, WHITE, stroke=8, shadow=9), W / 2,
              230 + k * 170, enter="pop", leave="fade", centre=True, dur=9))
        X((bf(149 + k * 1.5), 0x6E, 0.4))
    O(Txt(bf(154), bf(160.5), text("Read live from your own Sonic 3 & Knuckles ROM.", F_HEAVY_IT, 70, YELLOW,
                                   stroke=6, shadow=6), W / 2, 790, enter="up", centre=True, dur=12))
    O(Txt(bf(155.5), bf(160.5), text("The mod ships no images and no sound: it is only code.", F_BODY_IT, 44, WHITE,
                                     stroke=4, shadow=4), W / 2, 880, enter="up", centre=True, dur=12))
    S(Custom(161, 169, make_your_own, trans="iris", tdur=20))
    X((bf(161), 0xB3, 0.9))
    O(Txt(bf(161) + 8, bf(169), text("MAKE YOUR OWN", F_TITLE, 130, WHITE, stroke=8, shadow=9), 60, 70,
          enter="left", leave="fade", dur=12))
    O(Txt(bf(161) + 14, bf(169), text("With the OpenGGF Mod API, a scene mod starts with two small Java classes.",
                                      F_BODY_IT, 40, YELLOW, stroke=3, shadow=4), 64, 232, enter="left", dur=12))
    # ---- E. the final fight in three takes (Mecha Sonic lands on clip frame 44)
    S(Game(169, 181, "p09-final", 2, cam=cam_move((220, 100, 1.1), (230, 98, 1.15))))
    O(Flash(bf(169), 16))
    X((bf(169), 0xB6, 1.0))
    PUNCHES.append((bf(169) + 42, 0.1))
    O(Header(169.5, 175.5, "THE FINAL FIGHT", "Mecha Sonic guards the Master Emerald"))
    S(Game(181, 197, "p09-final", 372, cam=cam_move((240, 98, 1.2), (250, 98, 1.3))))
    O(Txt(bf(191), bf(197), text("...AND THEN HE GOES SUPER.", F_HEAVY_IT, 84, YELLOW, stroke=7, shadow=7), 90, 900,
          enter="left", leave="fade", dur=12))
    # ---- F. the final blow runs straight on into the victory screen under the Act Clear jingle
    S(Game(197, 225, "p09-final", 1380, cam=cam_move((230, 100, 1.12), (200, 112, 1.0))))
    PUNCHES.append((bf(197) + 64, 0.08))
    end0 = bf(225)
    end1 = end0 + 420
    SHOTS.append(Custom(225, 225, end_card, trans="xfade", tdur=24))
    SHOTS[-1].f1 = end1

    def end_logo(c, f, o):
        u = (f - o.f0) / 18
        img = logo(7, int((f - o.f0) * 3) % (font_width("ROBOTNIK") * 4 + 120) - 60)
        if u < 1:
            img = scaled(img, 0.4 + 0.6 * back(u, 2.2))
        paste(c, img, W / 2 - img.shape[1] / 2, 250 - img.shape[0] / 2, clamp(u * 4) * (1 - clamp((f - end1 + 50) / 50)))

    O(Fn(end0 + 10, end1, end_logo))
    O(Txt(end0 + 30, end1, text("A Sonic deck-building roguelike", F_HEAVY_IT, 66, YELLOW, stroke=6, shadow=6),
          W / 2, 450, enter="up", centre=True, dur=14))
    O(Txt(end0 + 44, end1, badge(256), 560, 680, enter="pop", centre=True, dur=16))
    O(Txt(end0 + 54, end1, text("An example mod for the OpenGGF Mod API", F_BODY, 46, WHITE, stroke=4, shadow=4),
          720, 580, enter="left", dur=14))
    O(Txt(end0 + 62, end1, text("github.com/OpenGGF/OpenGGF", F_HEAVY_IT, 72, WHITE, stroke=6, shadow=6),
          720, 650, enter="left", dur=14))
    O(Txt(end0 + 70, end1, text("Mod API in development for OpenGGF 0.7", F_BODY_IT, 38, (180, 200, 255), stroke=3,
                                shadow=4), 720, 760, enter="left", dur=14))
    O(Txt(end0 + 80, end1, text("Fan-made and free. Not affiliated with SEGA. Requires your own Sonic 3 & Knuckles ROM.",
                                F_BODY, 28, (200, 205, 220), stroke=2, shadow=3), W / 2, 1010, enter="fade",
          centre=True, dur=20))
    X((end0 + 10, 0x33, 0.6))
    O(Fade(end1 - 50, end1 + 1))
    SHOTS[0].f0 = 0  # the footage runs from the very first frame; the first beat is at 0.316 s
    return end1


def shot_at(f):
    cur = None
    for s in SHOTS:
        if s.f0 <= f < s.f1:
            cur = s
    return cur


def render_frame(f):
    s = shot_at(f)
    c = s.image(f)
    if s.trans and f < s.f0 + s.tdur:
        prev = SHOTS[SHOTS.index(s) - 1]
        c = TRANSITIONS[s.trans](prev.image(f), c, f, s.f0, s.tdur)
    for o in OVERLAYS:
        if o.f0 <= f < o.f1:
            o.draw(c, f)
    return np.clip(c, 0, 255).astype(np.uint8)


# -------------------------------------------------------------------------------------- audio

def read_wav(path):
    w = wave.open(str(path))
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768
    return a - a.mean(axis=0)


SFX_BANK = "33 AB B6 B3 AF B4 B8 63 6E 9F 3C 42 B1 6A AC 9C 62 4E".split()


def mix(total):
    out = np.zeros((total * SPF + SR, 2), np.float32)

    def add(a, at, gain=1.0, fin=0, fout=0):
        at = int(at)
        if at < 0:
            a, at = a[-at:], 0
        a = a[:len(out) - at].copy()
        if fin:
            a[:fin] *= np.linspace(0, 1, fin)[:, None]
        if fout:
            a[-fout:] *= np.linspace(1, 0, fout)[:, None]
        out[at:at + len(a)] += a * gain

    hcz = read_wav(ROOT / "audio/m-hcz2.wav")
    add(hcz[:int(bt(211) * SR)], 0, 1.0, fout=480)
    clear = read_wav(ROOT / "audio/m-actclear.wav")
    add(clear[:int(5.2 * SR)], (bt(211) - 0.082) * SR, 1.0, fout=2400)
    data = read_wav(ROOT / "audio/m-dataselect.wav")
    end0 = bf(225)
    add(data[:int(7.5 * SR)], end0 * SPF, 0.75, fin=SR, fout=int(2.4 * SR))
    for s in SHOTS:
        if isinstance(s, Game) and s.stems:
            stem = read_wav(ROOT / "clips" / f"{s.clip}.wav")
            a0 = s.src_frame(s.f0) * SPF
            n = (s.f1 - s.f0) * SPF
            seg = stem[a0:a0 + n]
            add(seg, s.f0 * SPF, 0.9 * s.stems, fin=240, fout=240)
    for clip, src, at, n, gain in STEMS:
        stem = read_wav(ROOT / "clips" / f"{clip}.wav")
        add(stem[src * SPF:(src + n) * SPF], at * SPF, gain, fin=240, fout=240)
    bank = read_wav(ROOT / "audio/sfx-bank.wav")
    for f, sid, gain in SFX:
        k = SFX_BANK.index(f"{sid:02X}")
        add(bank[k * 3 * SR:k * 3 * SR + int(2.6 * SR)], f * SPF, gain, fout=2400)
    out = out[:total * SPF]
    rms = np.sqrt((out ** 2).mean())
    out *= 10 ** (-16 / 20) / rms
    knee = 0.80
    over = np.abs(out) > knee
    out[over] = np.sign(out[over]) * (knee + (1 - knee) * np.tanh((np.abs(out[over]) - knee) / (1 - knee)))
    out *= 0.93
    return out


def write_wav(path, a):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


# ----------------------------------------------------------------------------------- commands

def prep():
    ASSETS.mkdir(parents=True, exist_ok=True)
    # The in-game logo: the pixels that stay constant while the title's fly-through scrolls by.
    ks = [100, 300, 500, 700, 900, 1000, 1150, 1300, 1450]
    stack = np.stack([np.asarray(clip_frame("p01-title", k), np.int16)[0:60, 0:220] for k in ks])
    still = (stack.max(axis=0) - stack.min(axis=0)).max(axis=2) == 0
    ys, xs = np.nonzero(still)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    rgba[..., :3] = stack[0, y0:y1, x0:x1]
    rgba[..., 3] = still[y0:y1, x0:x1] * 255
    Image.fromarray(rgba, "RGBA").save(ASSETS / "logo.png")
    # The event picture panel: the light-blue frame in the event screen's left column.
    fr = np.asarray(clip_frame("p07-ev-slot_machine", 60), np.int16)
    m = np.all(fr == (108, 144, 218), axis=2)
    cols = [x for x in range(150) if m[:, x].sum() > 100]  # the panel's left and right edges
    rows = [y for y in range(H) if y < m.shape[0] and m[y, :150].sum() > 100]
    (ASSETS / "panel.txt").write_text(f"{cols[0] + 1} {rows[0] + 1} {cols[-1]} {rows[-1]}")
    print("logo", (x0, y0, x1, y1), "panel", (ASSETS / "panel.txt").read_text())


def init_worker():
    build()


def frame_bytes(f):
    return render_frame(f).tobytes()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    if cmd == "prep":
        prep()
        return
    total = build()
    if cmd == "frames":
        for a in sys.argv[2:]:
            Image.fromarray(render_frame(int(a))).save(ROOT / "build" / f"out-{int(a):05d}.png")
        return
    if cmd == "sheet":
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        first = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        last = int(sys.argv[4]) if len(sys.argv) > 4 else total
        fs = list(range(first, min(last, total), step))
        with Pool(8, initializer=init_worker) as pool:
            ims = pool.map(render_frame, fs)
        cols = 5
        sheet = Image.new("RGB", (384 * cols, 216 * ((len(fs) + cols - 1) // cols)))
        for i, (f, im) in enumerate(zip(fs, ims)):
            t = Image.fromarray(im).resize((384, 216), Image.BILINEAR)
            ImageDraw.Draw(t).text((4, 2), f"{f} ({f / FPS:.2f}s)", fill="yellow")
            sheet.paste(t, ((i % cols) * 384, (i // cols) * 216))
        sheet.save(ROOT / "build" / f"promo-sheet-{first}.png")
        print(ROOT / "build" / f"promo-sheet-{first}.png", len(fs))
        return
    audio = mix(total)
    write_wav(ROOT / "build/promo-audio.wav", audio)
    print(f"audio: {len(audio) / SR:.2f}s, peak {np.abs(audio).max():.3f}")
    if cmd == "audio":
        return
    video = ROOT / "build/promo-video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
                            "-tune", "animation", "-pix_fmt", "yuv420p", str(video)], stdin=subprocess.PIPE)
    with Pool(8, initializer=init_worker) as pool:
        for k, b in enumerate(pool.imap(frame_bytes, range(total), chunksize=12)):
            enc.stdin.write(b)
            if k % 600 == 0:
                print(f"frame {k}/{total}", flush=True)
    enc.stdin.close()
    enc.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(ROOT / "build/promo-audio.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest",
                    str(ROOT / "promo.mp4")], check=True)
    print(ROOT / "promo.mp4", f"{total / FPS:.2f}s")


if __name__ == "__main__":
    main()
