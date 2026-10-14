#!/usr/bin/env python3
"""ROM-lettered editorial cards for the Sonic3K Chaos Mode demo, 2026-10-14.

Task-local media tool. Inputs are preserved in assets/ with provenance; output is
400x224 RGB PNG sequences at60fps, a timing manifest and a contact sheet. These
cards are editorial graphics, never gameplay or game-speed evidence.

Run: python3 card_renderer.py [--background /path/to/actual-capture.png]
Assembly: cards/<name>/f%04d.png at60fps; scale nearest then pad/crop to output.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
WIDTH, HEIGHT, FPS = 400, 224, 60
GOLD = (255, 202, 48, 255)
WHITE = (250, 252, 255, 255)
PALE = (175, 199, 231, 255)
NAVY = (9, 20, 49, 255)

CARD_SPECS = {
    "one": dict(frames=72, lines=["ONE", "HEDGEHOG"]),
    "no": dict(frames=72, lines=["NO", "RULES"]),
    "chaos": dict(frames=120, lines=["CHAOS", "MODE"],
                  subtitle="SONIC 3 AND KNUCKLES"),
    "side": dict(frames=72, lines=["SIDE", "EFFECTS"]),
    "optional": dict(frames=90, lines=["OPTIONAL", "SIDEGAMES"],
                     subtitle="YOUR ADVENTURE MAY BE INTERRUPTED"),
    "reviews": dict(frames=270, lines=[]),
    "end": dict(frames=300, lines=["CHAOS", "MODE"]),
    "post": dict(frames=120, lines=["GOOD", "LUCK"]),
}
REVIEWS = [
    (["I PREFERRED", "THE PILLARS."], "KNUCKLES"),
    (["FINALLY", "SOME HELP."], "ROBOTNIK"),
    (["WHERE DID", "THE FLOOR GO?"], "SONIC"),
]


def load_fonts():
    large = {f.stem: Image.open(f).convert("RGBA")
             for f in (ASSETS / "glyphs").glob("?.png")}
    small = {}
    lines = (ASSETS / "plate-font.txt").read_text().splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("= "):
            continue
        name = line[2:]
        glyph = Image.new("RGBA", (5, 9), (0, 0, 0, 0))
        ink = ImageDraw.Draw(glyph)
        for y, row in enumerate(lines[i + 1:i + 10]):
            for x, bit in enumerate(row):
                if bit == "#":
                    ink.point((x, y), fill=WHITE)
        small[name] = glyph
    for spec in CARD_SPECS.values():
        for line in spec["lines"]:
            missing = set(line) - set(large) - {" "}
            if missing:
                raise ValueError(f"Unsupported native title letters: {missing} in {line}")
    return large, small


LARGE, SMALL = load_fonts()


def text_width(text, font, spacing):
    return max(0, sum((6 if font is SMALL else 10) if c == " "
                      else font[c].width + spacing for c in text) - spacing)


def text_image(text, *, small=False, color=None):
    font, spacing = (SMALL, 1) if small else (LARGE, 2)
    w = text_width(text, font, spacing)
    h = 9 if small else max((font[c].height for c in text if c != " "), default=24)
    result = Image.new("RGBA", (max(1, w), h), (0, 0, 0, 0))
    x = 0
    for c in text:
        if c == " ":
            x += 6 if small else 10
            continue
        if c not in font:
            raise ValueError(f"Unsupported character {c!r} in {text!r}")
        glyph = font[c]
        if color:
            tinted = Image.new("RGBA", glyph.size, color)
            tinted.putalpha(glyph.getchannel("A"))
            glyph = tinted
        result.alpha_composite(glyph, (x, 0))
        x += glyph.width + spacing
    return result


def label(image, text, y, *, scale=2, small=False, color=None, dx=0, band=False):
    glyphs = text_image(text, small=small, color=color)
    w = max(1, round(glyphs.width * scale))
    h = max(1, round(glyphs.height * scale))
    glyphs = glyphs.resize((w, h), Image.Resampling.NEAREST)
    x = round((WIDTH - w) / 2 + dx)
    if band:
        # Retain the native title face's familiar dark horizontal label band.
        ImageDraw.Draw(image).rectangle((x - 5, y + round(8 * scale),
                                         x + w + 5, y + round(24 * scale)),
                                        fill=(20, 25, 40, 240))
    image.alpha_composite(glyphs, (x, round(y)))


def plate(image, text, y, scale=2, color=WHITE):
    fit = min(scale, 364 / max(1, text_width(text, SMALL, 1)))
    label(image, text, y, scale=fit, small=True, color=color)


def background(source, t):
    # Preserve the capture aspect. 320px screenshots have navy40px side rails.
    base = Image.new("RGBA", (WIDTH, HEIGHT), NAVY)
    image = source.copy().convert("RGBA")
    scale = min(WIDTH / image.width, HEIGHT / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    image = image.resize(size, Image.Resampling.NEAREST)
    base.alpha_composite(image, ((WIDTH - size[0]) // 2, (HEIGHT - size[1]) // 2))
    base.alpha_composite(Image.new("RGBA", base.size, (5, 10, 30, 205)))
    d = ImageDraw.Draw(base)
    # Tiny moving editorial motes make cards feel alive; source remains a still.
    for i in range(16):
        x = round((i * 67 + t * .6) % 410) - 5
        y = round((i * 37 + t * .18) % 200) + 7
        d.rectangle((x, y, x + 1, y + 1), fill=(107, 166, 224, 75))
    # Four-pixel inset survives the reference edit's5x ->1080p centre crop.
    d.rectangle((0, 0, WIDTH - 1, 3), fill=NAVY)
    d.rectangle((0, 4, WIDTH - 1, 7), fill=GOLD)
    d.rectangle((0, 201, WIDTH - 1, HEIGHT - 1), fill=NAVY)
    d.rectangle((0, 216, WIDTH - 1, 219), fill=GOLD)
    return base


def flash(image, age, opacity=120):
    if age < 3:
        image.alpha_composite(Image.new("RGBA", image.size,
                                       (255, 255, 255, max(0, opacity - age * 45))))


def title(image, lines, t, y0=50, target=1.8):
    fit = min(target, *(350 / max(1, text_width(line, LARGE, 2)) for line in lines))
    overshoot = max(0, 8 - t) * .20
    bounce = math.sin((t - 8) * .6) * .04 * math.exp(-max(0, t - 8) / 10) if t >= 8 else 0
    scale = fit + overshoot + bounce
    shake = math.sin(t * 2.7) * max(0, 10 - t) * .35
    for j, line in enumerate(lines):
        label(image, line, y0 + j * 54 - overshoot * 5, scale=scale,
              dx=shake, band=True)
    flash(image, t)


def reviews(image, t):
    index, age = min(2, t // 90), t % 90
    lines, author = REVIEWS[index]
    ring = Image.open(ASSETS / "glyphs" / f"ring-{(t // 6) % 4}.png").convert("RGBA")
    ring = ring.resize((25, 25), Image.Resampling.NEAREST)
    for i in range(5):
        current = ring.copy()
        if age < 4 + i * 5:
            current.putalpha(current.getchannel("A").point(lambda a: a // 4))
        image.alpha_composite(current, (116 + i * 34, 28))
    for j, line in enumerate(lines):
        plate(image, line, 77 + j * 24, 2, WHITE)
    plate(image, author, 142, 2, GOLD)
    plate(image, "FIVE RINGS OUT OF FIVE", 177, 1, PALE)
    plate(image, "FICTIONAL CRITICS", 206, 1, GOLD)
    flash(image, age, 90)


def frame(name, t, source):
    image = background(source, t)
    spec = CARD_SPECS[name]
    if name == "reviews":
        reviews(image, t)
    elif name == "end":
        title(image, spec["lines"], t, y0=19, target=1.5)
        # Always visible long enough to read; no tiny disclaimers flashing at the end.
        if t >= 18:
            plate(image, "105 EFFECTS. CHOOSE YOUR POOL.", 125, 1.5, GOLD)
        if t >= 27:
            plate(image, "SONIC 3 AND KNUCKLES", 147, 1.2, WHITE)
        if t >= 36:
            plate(image, "REQUIRES YOUR OWN S3K ROM", 169, 1.1, PALE)
        if t >= 45:
            plate(image, "INDEPENDENT FAN PROJECT", 187, 1.1, PALE)
            plate(image, "AN OPENGGF EXAMPLE MOD", 206, 1, GOLD)
    else:
        title(image, spec["lines"], t)
        if spec.get("subtitle"):
            plate(image, spec["subtitle"], 172, 1.3, GOLD)
        plate(image, "SONIC3K CHAOS MODE", 206, 1, GOLD)
    return image.convert("RGB")


def caption(text):
    """Transparent400x224 native pixel caption asset for the parent assembler."""
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 201, 399, 223), fill=NAVY)
    draw.rectangle((0, 201, 399, 202), fill=GOLD)
    plate(image, text.upper(), 207, 1.2)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, default=ASSETS / "aiz-background.png")
    args = parser.parse_args()
    source = Image.open(args.background).convert("RGBA")
    out = ROOT / "cards"
    out.mkdir(exist_ok=True)
    manifest = []
    sheet = Image.new("RGB", (800, 1004), (9, 20, 49))
    draw = ImageDraw.Draw(sheet)
    for index, (name, spec) in enumerate(CARD_SPECS.items()):
        folder = out / name
        folder.mkdir(exist_ok=True)
        for tick in range(spec["frames"]):
            frame(name, tick, source).save(folder / f"f{tick:04d}.png")
        manifest.append(dict(name=name, frames=spec["frames"], fps=FPS,
                             duration_seconds=spec["frames"] / FPS,
                             pattern=f"cards/{name}/f%04d.png",
                             lines=spec["lines"], editorial=True))
        representative = min(spec["frames"] - 1, 80 if name == "end" else 35)
        x, y = (index % 2) * WIDTH, (index // 2) * 251
        sheet.paste(frame(name, representative, source), (x, y))
        draw.text((x + 8, y + 233), f"{name.upper()}  {spec['frames']/FPS:.1f}s  400x224 / 60fps", fill=GOLD[:3])
        print(name, spec["frames"], flush=True)
    (ROOT / "card-manifest.json").write_text(json.dumps(dict(
        background=str(args.background.resolve()), native_size=[WIDTH, HEIGHT],
        fps=FPS, reviews=REVIEWS, cards=manifest), indent=2) + "\n")
    sheet.save(ROOT / "card-contact-sheet.png")
    captions = ROOT / "captions"
    captions.mkdir(exist_ok=True)
    for name, text in {
        "normal": "A NORMAL DAY ON ANGEL ISLAND.",
        "looks": "LOOKING GOOD.",
        "hud": "THE HUD HAS PLACES TO BE.",
        "gravity": "GRAVITY HAS RESIGNED.",
        "company": "EVERYTHING WANTS TO MEET YOU.",
        "pool": "CHOOSE YOUR PROBLEMS.",
        "sidegames": "SIDE EFFECTS MAY INCLUDE OTHER GAMES.",
        "post": "ONE MORE THING.",
    }.items():
        caption(text).save(captions / f"{name}.png")
    print("Rendered editorial cards, captions and manifest.", flush=True)


if __name__ == "__main__":
    main()
