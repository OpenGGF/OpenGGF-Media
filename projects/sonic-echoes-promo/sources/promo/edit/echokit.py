"""Sonic Echoes promo helpers on top of promo_kit: session sidecar access, S2 title-card headers,
the echo-trail logo, the input tape and ROM stinger routing.

Purpose: keep edit.py to creative decisions. Inputs: capture dirs with state.csv + session.csv
(SHOTLIST.md), ROM-rendered SFX WAVs. Origin: Sonic Echoes promo, 2026-10-24.
"""
import csv
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from promo_kit import (Overlay, arr, back, chip, clamp, ease_in, ease_out, paste, smooth, text,
                       WHITE)
import echofont

TASK = Path(__file__).resolve().parent.parent
CAPS = TASK / "captures"
SFX = TASK / "sfx"

# Sonic 2's title card (Putt-Putt Paradise r5 sampled these from a captured TITLE_CARD frame).
CARD_BLUE, CARD_YELLOW, CARD_RED = (48, 87, 206), (255, 226, 30), (232, 22, 30)
INK = (14, 20, 52)
SLOT = echofont.SLOTS
SLOT_NAMES = ["CYAN", "MAGENTA", "GOLD", "LIME", "VIOLET"]


def sfx(name):
    return str(SFX / f"s2-sfx-{name.lower()}-paced.wav")


class Rings:
    """S2 plays RingRight ($B5) and RingLeft ($CE); alternate them as the game alternates its ring
    speaker so no pop sits on one side."""

    def __init__(self):
        self.k = 0

    def __call__(self):
        self.k ^= 1
        return sfx("b5" if self.k else "ce")


# ------------------------------------------------------------------ captures and sidecars

@lru_cache(maxsize=None)
def session(shot):
    """frame -> row dict from captures/<shot>/session.csv (strings), plus parsed 'events' list."""
    rows = {}
    p = CAPS / shot / "session.csv"
    with open(p, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["events"] = [e for e in (r.get("events") or "").replace(";", " ").split() if e]
            rows[int(r["frame"])] = r
    return rows


@lru_cache(maxsize=None)
def state(shot):
    rows = {}
    with open(CAPS / shot / "state.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[int(r["frame"])] = r
    return rows


def events(shot, name):
    """Capture frames whose events include `name` (exact, or prefix when name ends with ':')."""
    out = []
    for f, r in sorted(session(shot).items()):
        for e in r["events"]:
            if e == name or (name.endswith(":") and e.startswith(name)):
                out.append(f)
    return out


def first_event(shot, name, after=-1):
    for f in events(shot, name):
        if f > after:
            return f
    raise KeyError(f"{shot}: no {name} after {after}")


@lru_cache(maxsize=None)
def frame_files(shot):
    """Sorted PNG paths of a capture and the capture frame number of each."""
    files = sorted((CAPS / shot / "frames").glob("*.png"))
    return files, [int(p.stem.split("-")[-1]) for p in files]


def clip_index(shot, capf):
    """Index into promo_kit.Frames(captures/<shot>/frames) for a capture frame number."""
    _, nums = frame_files(shot)
    return int(np.searchsorted(nums, capf))


def screen_pos(shot, capf, who):
    """Native screen position (x, y) of 'live' or echo slot N at a capture frame, or None."""
    r = session(shot).get(capf)
    if not r:
        return None
    cx, cy = float(r["camX"]), float(r["camY"])
    if who == "live":
        x, y = r["liveX"], r["liveY"]
    else:
        if r.get(f"e{who}state", "inactive") in ("inactive", ""):
            return None
        x, y = r[f"e{who}x"], r[f"e{who}y"]
    try:
        return float(x) - cx, float(y) - cy
    except ValueError:
        return None


# ------------------------------------------------------------------ S2 title-card header

def zigzag(h, w, teeth=7):
    pts = [(0, 0)]
    step = h / teeth
    for i in range(teeth):
        pts += [(w, i * step), (w - w * 0.45, (i + 0.5) * step)]
    pts += [(w, h), (0, h)]
    return pts


def _alpha(im, a):
    if a >= 0.999:
        return im
    out = im.copy()
    out[..., 3] *= a
    return out


class Card(Overlay):
    """A chapter header in the style of Sonic 2's title card (Putt-Putt Paradise r5): the red
    serrated tab drops, the blue band wipes across behind the heavy italic heading, a yellow strip
    slides in from the far side with the subtitle. Leaves left at double speed over 10 frames."""

    def __init__(self, f0, f1, title, sub=None, x=96, y=96, size=132, sub_size=46):
        super().__init__(f0, f1)
        self.title, self.sub, self.x, self.y = title, sub, x, y
        self.head = text(title, "title_it", size, WHITE, stroke=6, sfill=INK, shadow=7, scol=(0, 0, 30, 190))
        self.subim = text(sub, "sub", sub_size, INK) if sub else None

    def draw(self, c, f, edit):
        age, left = f - self.f0, self.f1 - f
        out = ease_in((10 - left) / 10) if left < 10 else 0.0
        hw, hh = self.head.shape[1], self.head.shape[0]
        band_w, band_h = hw + 90, hh - 4
        sub_h = (self.subim.shape[0] + 6) if self.subim is not None else 0
        W, H = band_w + 300, band_h + sub_h + 60
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        ox, oy = 40, 10
        reveal = ease_out((age - 2) / 13)
        if reveal > 0:
            bw = int(band_w * reveal)
            d.polygon([(ox, oy), (ox + bw + 34, oy), (ox + bw, oy + band_h), (ox, oy + band_h)], fill=CARD_BLUE + (240,))
        if self.subim is not None:
            yu = ease_out((age - 8) / 14)
            if yu > 0:
                yw = self.subim.shape[1] + 70
                sx = ox + 18 + int((1 - yu) * 380)
                d.polygon([(sx, oy + band_h), (sx + yw + 26, oy + band_h), (sx + yw, oy + band_h + sub_h),
                           (sx - 26, oy + band_h + sub_h)], fill=CARD_YELLOW + (250,))
        tu = back(age / 11)
        if tu > 0:
            tab_h = band_h + sub_h + 16
            tab = Image.new("RGBA", (40, tab_h), (0, 0, 0, 0))
            ImageDraw.Draw(tab).polygon(zigzag(tab_h, 40, max(3, tab_h // 26)), fill=CARD_RED + (255,))
            layer.paste(tab, (ox - 34, oy - 8 - int((1 - tu) * 140)), tab)
        def put(im, a, px, py):
            pi = Image.fromarray(np.clip(_alpha(im, a), 0, 255).astype(np.uint8), "RGBA")
            layer.alpha_composite(pi, (max(0, int(px)), max(0, int(py))))

        hu = back((age - 5) / 14)
        ha = clamp((age - 5) / 6)
        if ha > 0:
            put(self.head, ha, ox + 26 - int((1 - hu) * 120), oy - 10)
        if self.subim is not None:
            sa = clamp((age - 13) / 8)
            if sa > 0:
                yu = ease_out((age - 8) / 14)
                put(self.subim, sa, ox + 18 + int((1 - yu) * 380) + 22, oy + band_h + 2)
        L = np.asarray(layer, np.float32)
        dx = -out * (band_w + 340)
        paste(c, L, self.x - ox + dx, self.y - oy, 1 - out * 0.5)


# ------------------------------------------------------------------ logo

class Logo(Overlay):
    """SONIC / ECHOES in the mod's own face. The front word slams in (nearest-neighbour steps),
    then the echo copies fan out behind it one per `step` frames: cyan, magenta, gold."""

    def __init__(self, f0, f1, cx, cy, scale=20, step=26, trail=3, kicker_scale=10, exit_dur=10):
        super().__init__(f0, f1)
        self.cx, self.cy, self.scale, self.step, self.trail = cx, cy, scale, step, trail
        self.exit_dur = exit_dur
        self.words = [echofont.word("ECHOES", echofont.WHITE, trail=k, scale=scale) for k in range(trail + 1)]
        self.kick = echofont.word("SONIC", echofont.WHITE, scale=kicker_scale)
        front = self.words[0]
        self.fx, self.fy = cx - front.shape[1] / 2, cy - front.shape[0] / 2

    def copies(self, f):
        age = f - self.f0
        return int(clamp((age - 10) // self.step + 1, 0, self.trail)) if age >= 10 else 0

    def draw(self, c, f, edit):
        age = f - self.f0
        k = self.copies(f)
        im = self.words[k]
        x, y = self.fx - 2 * k * self.scale, self.fy - 2 * k * self.scale
        a = 1.0
        u = age / 8
        if u < 1:
            s = 1 + 0.6 * (1 - ease_out(u))
            big = Image.fromarray(im.astype(np.uint8), "RGBA").resize(
                (int(im.shape[1] * s), int(im.shape[0] * s)), Image.NEAREST)
            im = np.asarray(big, np.float32)
            x, y = self.cx - im.shape[1] / 2, self.cy - im.shape[0] / 2
            a = clamp(u * 3)
        v = (self.f1 - f) / self.exit_dur
        dx = -(1 - smooth(v)) * edit.W * 0.8 if v < 1 else 0.0
        fade = smooth(v) if v < 1 else 1.0
        paste(c, im, round(x + dx), round(y), a * fade)
        ka = clamp((age - 6) / 8) * fade
        if ka > 0:
            paste(c, self.kick, round(self.cx - self.kick.shape[1] / 2 + dx * 1.15),
                  round(self.fy - 2 * self.trail * self.scale - self.kick.shape[0] - self.scale), ka)


# ------------------------------------------------------------------ input tape

ARROW = {"L": "<", "R": ">", "U": "^", "D": "v"}


def input_letters(mask_str):
    """state.csv input column -> compact glyphs, e.g. 'R' or 'R+J'."""
    s = (mask_str or "").upper()
    parts = []
    for k in "LRUD":
        if k in s:
            parts.append(k)
    if any(j in s for j in ("A", "B", "C", "J")):
        parts.append("J")
    return parts


def tape_tile(sym, colour, size=64):
    """One input glyph tile: a rounded dark key with the symbol drawn as a shape."""
    t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((2, 2, size - 3, size - 3), radius=12, fill=(10, 16, 40, 230), outline=colour + (255,), width=4)
    m = size // 2
    r = size * 0.26
    if sym in "LRUD":
        ang = {"R": 0, "D": 90, "L": 180, "U": 270}[sym]
        import math
        pts = [(m + r * math.cos(math.radians(ang + a)), m + r * math.sin(math.radians(ang + a))) for a in (0, 140, 220)]
        d.polygon(pts, fill=(245, 248, 255, 255))
    else:
        d.ellipse((m - r, m - r, m + r, m + r), fill=colour + (255,))
    return np.asarray(t, np.float32)


class InputTape(Overlay):
    """A row of the live player's (or an echo's) recent inputs, newest at the right, scrolling as
    the footage plays. masks(f) returns the list of input strings for the last n frames up to output
    frame f; the tape collapses runs into one tile per held change, so it reads at a glance."""

    def __init__(self, f0, f1, masks, x, y, label, colour, tiles=7, size=64):
        super().__init__(f0, f1)
        self.masks, self.x, self.y, self.label, self.colour = masks, x, y, label, colour
        self.tiles, self.size = tiles, size
        self.lab = chip(label, 40, INK, colour)

    def draw(self, c, f, edit):
        a = clamp((f - self.f0) / 8) * clamp((self.f1 - f) / 8)
        if a <= 0:
            return
        seq = []
        for m in self.masks(f):
            sym = "+".join(input_letters(m)) or "-"
            if not seq or seq[-1] != sym:
                seq.append(sym)
        seq = [s for s in seq if s != "-"][-self.tiles:]
        paste(c, self.lab, self.x, self.y + (self.size - self.lab.shape[0]) / 2, a)
        x = self.x + self.lab.shape[1] + 16
        for s in seq:
            for part in s.split("+"):
                paste(c, tape_tile(part, self.colour, self.size), x, self.y, a)
                x += self.size + 8
            x += 10
