#!/usr/bin/env python3
"""Render promo captions in Sitar Hero's own 5x7 pixel font.

Purpose: caption cards for the Sitar Hero promo that match the mod's menus exactly.
Inputs: the mod's SitarUi.java (glyph tables are parsed from it, never copied), text,
integer scale and colours. Output: RGBA PIL images with the mod's INK outline.
Origin: Sitar Hero presentation polish task, 2026-10-08 (feature/ai-sitar-hero-polish).
"""
import re
from pathlib import Path

from PIL import Image


def load_font(sitar_ui: Path):
    source = sitar_ui.read_text()

    def constant(name):
        return re.search(name + r'\s*=\s*"([^"]*)"', source).group(1)

    return {
        "alphabet": constant("ALPHABET"),
        "glyphs": constant("GLYPHS"),
        "punctuation": constant("PUNCTUATION"),
        "punctuation_glyphs": constant("PUNCTUATION_GLYPHS"),
    }


def glyph_rows(font, ch):
    ch = ch.upper()
    index = font["alphabet"].find(ch)
    if index >= 0:
        data = font["glyphs"][index * 14:index * 14 + 14]
    else:
        p = font["punctuation"].find(ch)
        if p < 0:
            p = font["punctuation"].find("?")
        data = font["punctuation_glyphs"][p * 14:p * 14 + 14]
    return [int(data[r * 2:r * 2 + 2], 16) for r in range(7)]


def text_width(text, scale):
    return 0 if not text else len(text) * 6 * scale - scale


def render(font, text, scale, color, outline=(8, 19, 45, 255), shadow=True):
    """One line, scale x scale pixels per font pixel, outlined like SitarUi.text/big."""
    width = text_width(text, scale) + 2 * scale + (scale if shadow else 0)
    height = 7 * scale + 2 * scale + (scale if shadow else 0)
    image = Image.new("RGBA", (max(1, width), height), (0, 0, 0, 0))
    pixels = image.load()

    def plot(ox, oy, rgba):
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            rows = glyph_rows(font, ch)
            for r, bits in enumerate(rows):
                for c in range(5):
                    if bits & (16 >> c):
                        x0 = ox + i * 6 * scale + c * scale
                        y0 = oy + r * scale
                        for yy in range(y0, y0 + scale):
                            for xx in range(x0, x0 + scale):
                                if 0 <= xx < width and 0 <= yy < height:
                                    pixels[xx, yy] = rgba

    base = scale
    for dy in (-scale, 0, scale):
        for dx in (-scale, 0, scale):
            plot(base + dx, base + dy, outline)
    if shadow:
        plot(base + scale, base + scale, outline)
    plot(base, base, color)
    return image
