"""Character introduction cards and the duo end card, drawn over the edit's frames (edit layer only, no ROM time).

The drawings are Sol's mascot art from the owner's release-promo project, cut out by tools/sol_art.py into this
task's art/ folder. They are never copied into a repository checkout. The card follows the owner's direction for
that film's cards (its tools/animatic.py, introduce() at line 560):
  in:   a field in the character's colours cut by a slanted band; the hero drawing, nearly the height of the
        frame, slides in from its own side and the lettered name from the other;
  out:  the field parts along its slant and slides away first, so the play shows; the drawing and the name stay
        over it for two beats; then the drawing leaves the way it came and the name shrinks into the corner.
Timing is in frames from the bar the card lands on (a bar is about 84 frames at this tempo):
  0 field on (the cut), hero in by 12, name in by 14, line from 16; field parts 42-63; hero leaves 84-98;
  name shrinks 84-100 into a corner plate that stays for the rest of the shot.
Intro(who, W, H).draw(frame, k) returns the composited frame; it works for 1920x1080 and 1080x1920.
Origin: MICA & TALON promo redo, character introductions, 2026-11-12."""
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

T = Path(__file__).resolve().parent.parent
ART = T / 'art'
FONTS = Path(os.environ.get('PROMO_FONT_DIRS', str(Path.home() / 'scratch/agent-tmp/mt-promo-20261110/final/fonts')).split(os.pathsep)[0])
INK, WHITE, YELLOW = (14, 14, 16), (255, 255, 255), (255, 216, 31)
# deep, mid and accent, as on the owner's cards: jade and coral for MICA, slate and amber for TALON
COLOURS = {'mica': ((0, 73, 73), (0, 146, 109), (255, 73, 73)), 'talon': ((36, 36, 73), (109, 109, 146), (255, 182, 36))}
LINES = {'mica': 'JADE PANGOLIN. HOMING STRIKE.', 'talon': 'FALCON. FLIGHT. DIVEBOMB.'}
PART0, PART1, LEAVE = 42, 63, 84          # the field parts over beat 3; the drawing and the name leave on the next bar

_CACHE = {}


def sticker(name, height=None, width=None, edge=True):
    """A cut-out at a size, with the white sticker edge of the owner's cards (lettering keeps its own outline)."""
    key = (name, height, width, edge)
    if key not in _CACHE:
        im = Image.open(ART / f'{name}.png').convert('RGBA')
        if width:
            height = round(im.height * width / im.width)
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
        if edge:
            rim = max(3, height // 60)
            pad = Image.new('RGBA', (im.width + 4 * rim, im.height + 4 * rim), (0, 0, 0, 0))
            pad.paste(im, (2 * rim, 2 * rim))
            grown = pad.getchannel('A').filter(ImageFilter.MaxFilter(2 * rim + 1)).filter(ImageFilter.GaussianBlur(1))
            out = Image.new('RGBA', pad.size, (255, 255, 255, 0))
            out.putalpha(grown)
            out.alpha_composite(pad)
            im = out
        _CACHE[key] = im
    return _CACHE[key]


def label(text, size, fill=WHITE, font='FiraSansExtraCondensed-BlackItalic.ttf', stroke=None):
    f = ImageFont.truetype(str(FONTS / font), size)
    stroke = max(3, size // 9) if stroke is None else stroke
    box = f.getbbox(text, stroke_width=stroke)
    im = Image.new('RGBA', (box[2] - box[0] + 8, box[3] - box[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - box[0], 4 - box[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)
    return im


def fit(text, size, max_w, fill=WHITE, font='FiraSansExtraCondensed-BlackItalic.ttf'):
    """A label at the largest size up to `size` that is no wider than max_w."""
    while True:
        im = label(text, size, fill, font)
        if im.width <= max_w or size <= 24:
            return im
        size -= 2


def ease_out(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Intro:
    """One character's introduction for one frame size. hero_left puts the drawing on the left and the name right."""

    def __init__(self, who, W, H, hero_left=True, plate=True):
        self.who, self.W, self.H, self.left, self.plate_on = who, W, H, hero_left, plate
        deep, mid, accent = COLOURS[who]
        tall = H > W
        flip = (lambda x: W - x) if hero_left else (lambda x: x)
        # the field: deep ground, a slanted band of the mid colour on the hero's side, an accent stripe and an ink line
        a, b = (0.36, 0.58) if not tall else (0.20, 0.86)          # where the slant crosses the top and the bottom edge
        sw, iw = (0.036 * W, 0.010 * W) if not tall else (0.060 * W, 0.016 * W)
        bg = Image.new('RGB', (W, H), deep)
        d = ImageDraw.Draw(bg)
        x0, x1 = W * (1 - a), W * (1 - b)                           # the band is on the right before flipping
        d.polygon([(flip(x0), 0), (flip(W), 0), (flip(W), H), (flip(x1), H)], fill=mid)
        d.polygon([(flip(x0 - sw), 0), (flip(x0), 0), (flip(x1), H), (flip(x1 - sw), H)], fill=accent)
        d.polygon([(flip(x0 - sw - iw), 0), (flip(x0 - sw), 0), (flip(x1 - sw), H), (flip(x1 - sw - iw), H)], fill=INK)
        seam = Image.new('L', (W, H), 0)
        ImageDraw.Draw(seam).polygon([(flip(x0 - sw - iw), 0), (flip(W), 0), (flip(W), H), (flip(x1 - sw - iw), H)], fill=255)
        self.band_side, self.other_side = bg.convert('RGBA'), bg.convert('RGBA')
        self.band_side.putalpha(seam)
        self.other_side.putalpha(ImageChops.invert(seam))
        self.way = -1 if hero_left else 1                           # the band half leaves toward the hero's side
        if not tall:
            self.hero = sticker(f'{who}-hero', height=round(H * 0.965))
            self.hx = 10 if hero_left else W - self.hero.width - 10
            self.hy = (H - self.hero.height) // 2
            self.name = sticker(f'name-{who}', width=round(W * 0.43), edge=False)       # clear of the pointing hand
            self.ncx, self.ncy = (W * 0.755 if hero_left else W * 0.25), H * 0.44
            self.small = sticker(f'name-{who}', width=round(W * 0.215), edge=False)
            self.sub = label(LINES[who], 62)
        else:                                                       # bigger is better: the drawing may run off both sides
            self.hero = sticker(f'{who}-hero', height=round(H * (0.64 if who == 'talon' else 0.60)))
            rim = max(3, self.hero.height // 60)
            # MICA keeps her pointing hand whole and gives up the tip of her tail; TALON's wings run off both sides
            self.hx = W - self.hero.width + 2 * rim - 6 if who == 'mica' else (W - self.hero.width) // 2 - round(W * 0.02)
            self.hy = H - self.hero.height - round(H * 0.035)
            self.name = sticker(f'name-{who}', width=round(W * 0.90), edge=False)
            self.ncx, self.ncy = W / 2, H * 0.175                   # the line under the name stays clear of the head
            self.small = sticker(f'name-{who}', width=round(W * 0.36), edge=False)
            self.sub = label(LINES[who], 70)
        self.hero_away = -self.hero.width - 20 if hero_left else W + 20
        self.name_away = W + 20 if hero_left else -self.name.width - 20
        self.corner = (W - self.small.width / 2 - round(W * 0.022), H - self.small.height / 2 - round(H * 0.03))
        self._sizes = {}

    def _name_at(self, t):
        """The name between its card size (t = 0) and its corner plate (t = 1)."""
        w = round(self.name.width + (self.small.width - self.name.width) * t)
        if w not in self._sizes:
            self._sizes[w] = self.name.resize((w, round(self.name.height * w / self.name.width)), Image.LANCZOS)
        im = self._sizes[w]
        cx = self.ncx + (self.corner[0] - self.ncx) * t
        cy = self.ncy + (self.corner[1] - self.ncy) * t
        return im, round(cx - im.width / 2), round(cy - im.height / 2)

    def draw(self, frame, k, plate_until=None):
        """frame: HxWx3 uint8 of the play at this moment; k: frames since the card's bar. Returns HxWx3 uint8."""
        if k < 0 or (plate_until is not None and k >= plate_until) or (not self.plate_on and k >= LEAVE + 16):
            return frame
        im = Image.fromarray(frame).convert('RGBA')
        if k < PART1 + 1:                                           # the field, parting along its slant from PART0
            p = max(0.0, (k - PART0) / (PART1 - PART0)) ** 3
            off = round(1.25 * max(self.W, self.H) * p)
            dy = round(off * 0.25)
            self._slide(im, self.other_side, -self.way * off, self.way * dy)
            self._slide(im, self.band_side, self.way * off, -self.way * dy)
        if k < LEAVE + 14:                                          # the hero: in over 12 frames, out the way it came
            arrive, leave = ease_out(k / 12), max(0.0, (k - LEAVE) / 14) ** 3
            x = round(self.hero_away + (self.hx - self.hero_away) * (arrive - leave))
            self._slide(im, self.hero, x, self.hy)
        if k >= 4:                                                  # the name: in from the other side, then to its corner
            t = smooth((k - LEAVE) / 16)
            nm, x, y = self._name_at(t)
            if k < LEAVE:
                x = round(self.name_away + (x - self.name_away) * ease_out((k - 4) / 10))
            if k < LEAVE + 16 or self.plate_on:
                if plate_until is not None and k >= plate_until - 8:    # the plate fades with its shot
                    nm = nm.copy(); nm.putalpha(nm.getchannel('A').point(lambda v: round(v * max(0, plate_until - k) / 8)))
                self._slide(im, nm, x, y)
        if 16 <= k < PART0 + 6:                                     # the line under the name, gone as the field parts
            s = self.sub
            if k >= PART0:
                s = s.copy(); s.putalpha(s.getchannel('A').point(lambda v: round(v * (PART0 + 6 - k) / 6)))
            pop = ease_out((k - 16) / 8)
            self._slide(im, s, round(self.ncx - s.width / 2), round(self.ncy + self.name.height / 2 + 18 + (1 - pop) * 30))
        return np.asarray(im.convert('RGB'))

    @staticmethod
    def _slide(im, layer, x, y):
        """alpha_composite that accepts positions partly or wholly outside the frame."""
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(im.width, x + layer.width), min(im.height, y + layer.height)
        if x1 > x0 and y1 > y0:
            im.alpha_composite(layer.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


class EndCard:
    """The duo drawing and the two lettered names for the end card. The backdrop (the pair take in soft focus) and
    the fade belong to the edit; draw() lays the card over it. t: frames since bar 84."""

    def __init__(self, W, H, duo='duo-sunrise'):
        self.W, self.H = W, H
        tall = H > W
        if not tall:
            self.duo = sticker(duo, height=round(H * 0.68))
            self.dx, self.dy = round(W * 0.012), round(H * 0.10)
            col = W * 0.805                                         # the names stand clear of TALON's raised hand
            nw = round(W * 0.31)
            self.names = [(sticker('name-mica', width=nw, edge=False), col, H * 0.16), (sticker('name-talon', width=nw, edge=False), col, H * 0.46)]
            self.amp = (label('&', 150, YELLOW), col, H * 0.315)
            room = 2 * (W - col) - round(W * 0.03)                  # the column's width, with a margin at the frame edge
            self.lines = [(fit('An example character mod', 54, room, WHITE, 'FiraSansCondensed-BoldItalic.ttf'), col, H * 0.635),
                          (fit('for OpenGGF', 54, room, WHITE, 'FiraSansCondensed-BoldItalic.ttf'), col, H * 0.693),
                          (fit('github.com/OpenGGF/OpenGGF', 62, room, YELLOW), col, H * 0.775)]
            self.disc = (label('Fan-made and free. Not affiliated with SEGA. Requires your own ROMs.', 34, WHITE, 'FiraSans-Bold.ttf', stroke=4), W / 2, H * 0.925)
        else:
            self.duo = sticker(duo, width=round(W * 1.02))
            self.dx, self.dy = (W - self.duo.width) // 2, round(H * 0.045)
            col = W / 2
            nw = round(W * 0.74)
            self.names = [(sticker('name-mica', width=nw, edge=False), col, H * 0.50), (sticker('name-talon', width=nw, edge=False), col, H * 0.672)]
            self.amp = (label('&', 150, YELLOW), col, H * 0.588)
            self.lines = [(label('An example character mod', 62, WHITE, 'FiraSansCondensed-BoldItalic.ttf'), col, H * 0.778),
                          (label('for OpenGGF', 62, WHITE, 'FiraSansCondensed-BoldItalic.ttf'), col, H * 0.816),
                          (label('github.com/OpenGGF/OpenGGF', 66, YELLOW), col, H * 0.872)]
            self.disc = (label('Fan-made and free. Not affiliated with SEGA.', 32, WHITE, 'FiraSans-Bold.ttf', stroke=4), col, H * 0.94)
            self.disc2 = (label('Requires your own ROMs.', 32, WHITE, 'FiraSans-Bold.ttf', stroke=4), col, H * 0.962)

    def draw(self, frame, t):
        im = Image.fromarray(frame).convert('RGBA')
        a = ease_out(t / 14)                                        # the duo rises in with the iris
        Intro._slide(im, self.duo, self.dx, round(self.dy + (1 - a) * self.H * 0.5))
        beat = 10
        for n, (nm, cx, cy) in enumerate(self.names):               # MICA, then TALON, a beat apart
            k = t - 12 - 2 * beat * n
            if k >= 0:
                s = 0.8 + 0.2 * ease_out(k / 6)
                m = nm if s >= 0.999 else nm.resize((round(nm.width * s), round(nm.height * s)), Image.LANCZOS)
                Intro._slide(im, m, round(cx - m.width / 2), round(cy - m.height / 2))
        if t >= 12 + beat:
            m, cx, cy = self.amp
            Intro._slide(im, m, round(cx - m.width / 2), round(cy - m.height / 2))
        for n, (m, cx, cy) in enumerate(self.lines):
            k = t - 50 - 10 * n
            if k >= 0:
                m2 = m if k >= 10 else self._fade(m, k / 10)
                Intro._slide(im, m2, round(cx - m.width / 2), round(cy - m.height / 2))
        for m, cx, cy in (self.disc,) + ((self.disc2,) if hasattr(self, 'disc2') else ()):
            if t >= 84:
                m2 = m if t >= 94 else self._fade(m, (t - 84) / 10)
                Intro._slide(im, m2, round(cx - m.width / 2), round(cy - m.height / 2))
        return np.asarray(im.convert('RGB'))

    @staticmethod
    def _fade(m, a):
        m = m.copy()
        m.putalpha(m.getchannel('A').point(lambda v: round(v * max(0.0, min(1.0, a)))))
        return m
