"""Sonic Echoes' own 5x7 face (EchoUi.GLYPHS in the mod source), rendered in whole glyph pixels.

Purpose: the promo's logo and hub-matching type. Input: the mod's EchoUi.java (read, not copied).
Origin: Sonic Echoes promo, 2026-10-24. The mod's treatment is face + a one-pixel navy drop
(0xD0081028) at (+1,+1); echo trails reuse the mod's five slot colours (EchoUi.colour).
"""
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/home/james/IdeaProjects/OpenGGF/examples/sonic-echoes/src/main/java/echoes/EchoUi.java")
SLOTS = [(0x60, 0xE8, 0xFF), (0xFF, 0x70, 0xD0), (0xFF, 0xD0, 0x30), (0xA0, 0xF0, 0x60), (0xC0, 0x90, 0xFF)]
DROP = (0x08, 0x10, 0x28, 0xD0)
WHITE = (0xF4, 0xF8, 0xFF)


@lru_cache(maxsize=1)
def table():
    src = SRC.read_text()
    chars = re.search(r'CHARS = "([^"]+)"', src).group(1)
    body = src[src.index("GLYPHS ="):src.index(";", src.index("GLYPHS ="))]
    bits = "".join(re.findall(r'"([01]+)"', body))
    return {ch: bits[i * 35:(i + 1) * 35] for i, ch in enumerate(chars)}


def mask(s):
    t = table()
    s = s.upper()
    m = np.zeros((7, max(1, len(s) * 6 - 1)), bool)
    for i, ch in enumerate(s):
        g = t.get(ch)
        if g is None:
            continue
        for r in range(7):
            for c in range(5):
                if g[r * 5 + c] == "1":
                    m[r, i * 6 + c] = True
    return m


def layer(m, rgb, a=255, pad=(0, 0, 0, 0)):
    top, left, bottom, right = pad
    h, w = m.shape
    out = np.zeros((h + top + bottom, w + left + right, 4), np.uint8)
    sub = out[top:top + h, left:left + w]
    sub[m] = tuple(rgb[:3]) + (a,)
    return out


def over(dst, src):
    a = src[..., 3:4].astype(np.float32) / 255
    d = dst.astype(np.float32)
    d[..., :3] = src[..., :3] * a + d[..., :3] * (1 - a)
    d[..., 3:4] = np.maximum(d[..., 3:4], src[..., 3:4])
    return d.astype(np.uint8)


def _dilate(m):
    d = m.copy()
    d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= d[:, :-1].copy(); d[:, :-1] |= d[:, 1:].copy()
    return d


def word(s, rgb=WHITE, trail=0, dx=-2, dy=-2, scale=1, drop=True, trail_alpha=(255, 235, 215, 195, 175)):
    """The word in the mod's face. trail>0 stacks that many echo copies behind it in the slot
    colours, each (dx, dy) glyph pixels further out (the nearest is cyan). Each copy is clipped
    one glyph pixel clear of everything in front of it, so layers stack like cards and no copy
    shows through a nearer letter's counters. Returns float32 RGBA at integer `scale`."""
    m = mask(s)
    ox, oy = max(0, -dx * trail), max(0, -dy * trail)
    H, W = m.shape[0] + oy + max(0, dy * trail) + 1, m.shape[1] + ox + max(0, dx * trail) + 1

    def placed(x, y):
        g = np.zeros((H, W), bool)
        g[y:y + m.shape[0], x:x + m.shape[1]] = m
        return g

    out = np.zeros((H, W, 4), np.uint8)
    front = placed(ox, oy)
    if drop:
        front_d = placed(ox + 1, oy + 1)
        out[front_d] = DROP
        front = front | front_d
    out[placed(ox, oy)] = tuple(rgb[:3]) + (255,)
    occupied = _dilate(front)
    occupied[max(0, oy - 1):oy + m.shape[0] + 2, max(0, ox - 1):ox + m.shape[1] + 2] = True  # peek outside the word only
    for k in range(1, trail + 1):
        g = placed(ox + dx * k, oy + dy * k)
        vis = g & ~occupied
        out[vis] = tuple(SLOTS[(k - 1) % 5]) + (trail_alpha[(k - 1) % 5],)
        occupied |= _dilate(g)
    im = Image.fromarray(out, "RGBA").resize((W * scale, H * scale), Image.NEAREST)
    return np.asarray(im, np.float32)


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    Image.fromarray(word("ECHOES", WHITE, trail=3, scale=20).astype(np.uint8)).save(out / "logo-echoes.png")
    Image.fromarray(word("SONIC", WHITE, scale=12).astype(np.uint8)).save(out / "logo-sonic.png")
