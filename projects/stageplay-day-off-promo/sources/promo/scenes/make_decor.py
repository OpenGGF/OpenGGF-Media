#!/usr/bin/env python3
"""Original nine-slice dialogue frames for "Day Off" (sp-promo-a, 2026-10-24).

Each 24x24 PNG has a 6-pixel border (decorationBorder 6) and a transparent middle so the
skin's panel colour shows through. Drawn procedurally here: no ROM art is copied.
"""
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent / "decor"
FRAMES = {
    #           outline    dark band   main band   light edge  stud
    "moto":     ("#06080E", "#5A6270", "#A8B0BC", "#E8ECF2", "#E04838"),
    "sonic":    ("#06080E", "#1A3A9A", "#3D6CE0", "#9CC0FF", "#FFD23A"),
    "knuckles": ("#06080E", "#7A1022", "#D83050", "#FF9AAA", "#F4F1E8"),
    "tails":    ("#06080E", "#8A5208", "#F0A020", "#FFE08A", "#F4F1E8"),
}

def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)

def frame(colours):
    outline, dark, main, light, stud = map(rgb, colours)
    size = 24
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    for y in range(size):
        for x in range(size):
            d = min(x, y, size - 1 - x, size - 1 - y)   # distance from the outer edge
            if d == 0:
                px[x, y] = outline
            elif d == 1:
                # bevel: light on top/left, dark on bottom/right
                px[x, y] = light if (x == 1 or y == 1) and x < size - 2 and y < size - 2 else dark
            elif d in (2, 3):
                px[x, y] = main
            elif d == 4:
                px[x, y] = dark
            elif d == 5:
                px[x, y] = outline
    # corner studs: 2x2 with a 1px highlight
    for cx, cy in ((2, 2), (size - 4, 2), (2, size - 4), (size - 4, size - 4)):
        for dy in range(2):
            for dx in range(2):
                px[cx + dx, cy + dy] = stud
        px[cx, cy] = light
    return img

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, colours in FRAMES.items():
        frame(colours).save(OUT / f"{name}.png")
        print(OUT / f"{name}.png")
