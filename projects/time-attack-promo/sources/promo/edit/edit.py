#!/usr/bin/env python3
"""OpenGGF Multiplayer Time Attack promo (ta-promo-a, 2026-10-23).
Rebuild: python3 edit/prep.py && PROMO_FONT_DIRS=fonts python3 <OpenGGF>/tools/media/promo_kit.py render edit/edit.py

Audience: people who follow OpenGGF and Sonic fans who like racing; nobody outside has seen it.
Form/evidence: gameplay showcase of real engine captures driven through the real Time Attack UI
  (display-free); every rival is a loopback protocol test client replaying a recorded GHZ1 route.
Promise: "Race together. Live." -- a whole room of named, coloured ghosts in your level, every attempt.
Story: one race told end to end -- you name yourself, pick a colour, wait in a lobby you can play,
  die at the first badnik while the pack leaps it, are back in 3.8 s, and lose a photo finish by
  0.03 s; then everyone votes and the next zone loads. Breadth (3 games, 256 slots) is shown in
  passing, labelled.
Proof per claim: ghosts + nameplates (live pack footage, 4x2 grid of tracked nameplates); any script
  (in-game name prompt typing 疾風の刃, names in 8 scripts); own look (profile presets on the beat ->
  the Ember hero in all three games' race starts); lobby is a level (menu over HPZ -> ready -> menu
  hides -> play with ghosts -> menu back; GHZ/EHZ/HPZ lobbies); no lives (natural death on 0 rings,
  jump-skip, reload without title card, 3-2-1, measured death->GO); vote (live tally, Marble Zone
  card); 256 (capacity-test browser row 255/256, title-card ROOM 256 PLAYERS, HUD /252 SEEN).
Hero moment: the photo finish -- the pack hits the GHZ1 signpost together; standings 0:53.63 vs
  0:53.66. A fragment of the pack at speed opens the film.
Sound: one bed, S3K Azure Lake (Competition) via OpenGGF's SMPS driver, 150.0 BPM, first beat
  0.21 s, bars on beats 2+4n, phrases 2/34/66/98/130, loop restart 138, B section again at 170.
  ROM SFX stingers only at real events (GO, death, digits, finish) and pops; no clip audio.
Palette: nameplate fill #101828 (GhostRenderer), player name colours from PlayerAppearance.nameArgb,
  hero Ember; wipe bands in the S2/S3K title-card blue/yellow/red.
Title face: the engine's own NameFont (Fusion Pixel 10px + Unifont), the face of every ghost's
  nameplate, at integer scale on a nameplate plate. (S2 card font rejected: split-stroke M reads
  "TI/ME" at display size.)
End card: badge, ONE MORE GO?, URL, status, disclaimer + honesty line; over blurred Marble Zone.
"""
import csv
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/ta-promo-a/tools/media")
from promo_kit import *  # noqa: F401,F403
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CAPS = ROOT / "captures"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capmap  # noqa: E402  (edit frame numbers onto re-captured takes)
CLIPS = ROOT / "edit/build/clips"
MUS = ROOT / "music/clean"
PLATES = ROOT / "design/plates"
TYPED = ROOT / "design/plates-typed"
BADGE = Path("/home/farrell/code/projects/OpenGGF/.worktrees/ta-promo-a/src/main/resources/icon/openggf-256.png")

EDIT = dict(bpm=150.0, first=0.21, fps=60, size=(1920, 1080), out=str(ROOT / "out/openggf-time-attack-promo.mp4"),
            work=str(ROOT / "edit/build/render"))

FILL = (16, 24, 40)          # GhostRenderer NAMEPLATE_FILL_RGB, alpha 0xD8
FILL_A = 0xD8
STOCK_NAME = (0xF5, 0xF8, 0xFF)


def md_rgb(c):
    r, g, b = ((c >> 1) & 7) * 255 + 3, ((c >> 5) & 7) * 255 + 3, ((c >> 9) & 7) * 255 + 3
    return r // 7, g // 7, b // 7


def name_rgb(c):
    """PlayerAppearance.nameArgb: the base colour lifted until it reads on the dark plate."""
    r, g, b = md_rgb(c)
    for _ in range(8):
        if (r * 299 + g * 587 + b * 114) // 1000 >= 150:
            break
        r, g, b = r + (255 - r) // 3 + 1, g + (255 - g) // 3 + 1, b + (255 - b) // 3 + 1
    return min(255, r), min(255, g), min(255, b)


HERO = name_rgb(0x006E)                                    # Ember
RIVAL = [name_rgb(c) for c in (0x04C2, 0x022E, 0x0AA0, 0x0A6E, 0x0E46, 0x00CE, 0x0E62, 0x0AAA)]
GOLDEN = (255, 214, 64)


# ------------------------------------------------------------------ nameplate type (engine NameFont)

@lru_cache(maxsize=None)
def mask(key, typed=False):
    im = Image.open((TYPED if typed else PLATES) / f"{key}.png").convert("RGBA")
    return np.asarray(im)[..., 3] > 0


def glyph_mask(s):
    """A NameFont mask for a digit/time string built from dumped single glyphs."""
    parts = [mask({".": "ddot", "s": "dsec", " ": None}.get(ch) or f"d{ch}") if ch != " " else np.zeros((13, 3), bool)
             for ch in s]
    h = max(p.shape[0] for p in parts)
    out = np.zeros((h, sum(p.shape[1] - 2 for p in parts) + 2), bool)
    x = 0
    for p in parts:
        w = p.shape[1] - 2
        out[:p.shape[0], x:x + p.shape[1]] |= p
        x += w
    return out


@lru_cache(maxsize=None)
def plate_m(m_key, scale, colour, fill=True, bar=None, pad=2):
    """A ghost nameplate drawn at native size then enlarged: dark plate, text in the player's colour,
    optional ProfileView-style colour bar on the left (3 px). Returns float RGBA."""
    m = glyph_mask(m_key[1:]) if m_key.startswith("#") else mask(*m_key.split("|")) if "|" in m_key else mask(m_key)
    h, w = m.shape
    left = pad + (4 if bar else 0)
    W, H = w - 2 + left + pad, h
    px = np.zeros((H, W, 4), np.uint8)
    if fill:
        px[...] = FILL + (FILL_A,)
    if bar:
        px[:, 0:3] = bar + (255,)
    sub = px[:, left:left + w]
    sub[m[:, :sub.shape[1]]] = colour + (255,)
    im = Image.fromarray(px, "RGBA").resize((W * scale, H * scale), Image.NEAREST)
    return np.asarray(im, np.float32)


# Editorial type must never look like the game's own UI (user, 2026-10-23: "I don't know if the
# promo is talking to me, or the game displays that text in normal play"). Player names, the typed
# name and the captured game footage keep the engine's name font; everything the film itself says
# (headers, lines, labels, counters, the end card) uses the display face with a stroke and a hard
# shadow, and labels sit on pills. None of it uses the HUD's dark translucent plate.
LABELS = {row.split("\t")[0]: row.split("\t")[3]
          for row in (PLATES / "index.tsv").read_text(encoding="utf-8").splitlines() if row.count("\t") >= 3}
NAME_KEYS = {"hero"} | {f"r{i}" for i in range(8)}
PILL_KEYS = {f"l{i}" for i in range(8)} | {"you", "s1", "s2", "s3k", "captest"}
INK = (14, 20, 52)


def editorial(label, scale, colour=STOCK_NAME, pill=False, pill_colour=None):
    """The film's own voice: Fira Sans Extra Condensed Black Italic, white or the given colour,
    navy stroke and hard shadow; a pill for short labels. Sized like the nameplate it replaces."""
    size = max(24, round(13 * scale * 0.95))
    if pill:
        return chip(label, size, INK, tuple(pill_colour or YELLOW))
    return text(label, "title_it", size, tuple(colour), stroke=max(3, scale), sfill=INK,
                shadow=max(4, scale + 2), scol=(0, 0, 30, 190))


def plate(key, scale, colour=STOCK_NAME, fill=True, bar=None):
    if key in LABELS and key not in NAME_KEYS and not key.startswith("d") and key != "ddot" and key != "dsec":
        return editorial(LABELS[key], scale, colour, key in PILL_KEYS, bar if key in PILL_KEYS else None)
    return plate_m(key, scale, colour, fill, bar)


def counter(s, scale, colour):
    """A number the film shows (a measured time, a count), in the display face."""
    return editorial(s, scale, colour)


def typed_plate(n, scale, colour, bar=None):
    """The title's MULTIPLAYER typed letter by letter, in the film's own display face."""
    return editorial(LABELS["multi"][:max(1, n)], scale, colour)


class Plate(Overlay):
    """Nameplate type with whole-pixel motion only (no scaling): enter from the right or drop from
    the top, leave to the right at double speed; 'type' reveals a dumped prefix per step."""

    def __init__(self, f0, f1, img, x, y, enter="right", leave="right", centre=False, dur=12, out_dur=8, alpha=1.0):
        super().__init__(f0, f1)
        self.img, self.x, self.y, self.enter, self.leave = img, x, y, enter, leave
        self.centre, self.dur, self.out_dur, self.alpha = centre, dur, out_dur, alpha

    def draw(self, c, f, edit):
        img = self.img(f) if callable(self.img) else self.img
        x, y = self.x, self.y
        if self.centre:
            x, y = x - img.shape[1] / 2, y - img.shape[0] / 2
        u = (f - self.f0) / self.dur
        a = self.alpha
        if u < 1:
            if self.enter == "right":
                x += (1 - ease_out(u)) * (edit.W - x + 40)
            elif self.enter == "drop":
                y -= (1 - ease_out(u)) * (y + img.shape[0] + 40)
            elif self.enter == "up":
                y += (1 - ease_out(u)) * 90
                a *= smooth(u)
            elif self.enter == "cut":
                pass
        v = (self.f1 - f) / self.out_dur
        if v < 1:
            if self.leave == "right":
                x += (1 - smooth(v)) * (edit.W - x + 40)
            elif self.leave == "fade":
                a *= smooth(v)
        paste(c, img, round(x / 4) * 4, round(y / 4) * 4, a)


def header(e, f0, f1, key, colour=STOCK_NAME, bar=HERO, y=900):
    """Chapter header: a big nameplate slides in from the right to the lower left, leaves right."""
    e.O(Plate(f0, f1, plate(key, 7, colour, True, bar), 96, y, enter="right", leave="right", dur=14, out_dur=8))


# ------------------------------------------------------------------ clips, tracking, views

def clip(name):
    return Frames(CLIPS / name)


def first_src(name):
    return int((CLIPS / name / "source.txt").read_text().split()[1])


@lru_cache(maxsize=None)
def race_state(cap):
    """Per capture frame: hero screen position and ghost screen positions (from the driver's state.csv)."""
    out = {}
    with open(CAPS / cap / "state.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = dict(kv.split("=", 1) for kv in r["extra"].split(" ") if "=" in kv)
            cam = d.get("cam", "")
            hero = None
            if cam and r["x"] != "-1":
                cx, cy = map(int, cam.split(":"))
                hero = (int(r["x"]) - cx, int(r["y"]) - cy)
            ghosts = {}
            for g in d.get("ghosts", "").split(";"):
                if g:
                    n, p = g.rsplit("@", 1)
                    gx, gy, op = p.split(":")
                    ghosts[n] = (int(gx), int(gy), float(op))
            out[capmap.to_edit(CAPS / cap, int(r["frame"]))] = (hero, ghosts)
    return out


@lru_cache(maxsize=None)
def track(cap, who, f0, f1, window=21):
    """Smoothed screen position of a ghost (or 'hero') over capture frames f0..f1, holding the last
    seen position while it is off-screen."""
    st = race_state(cap)
    raw, last = [], (160, 120)
    for f in range(f0, f1):
        hero, ghosts = st.get(f, (None, {}))
        p = hero if who == "hero" else (ghosts.get(who) or (None,))[:2]
        if p and p[0] is not None and -40 < p[0] < 360 and -40 < p[1] < 264:
            last = p
        raw.append(last)
    a = np.array(raw, np.float32)
    k = np.ones(window) / window
    pad = np.pad(a, ((window // 2, window // 2), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, i], k, mode="valid") for i in range(2)], 1)


def pad_x(img, p):
    """Native frame widened by p black columns each side, so a camera can centre a subject that
    stands near the level edge; the padding stays outside the narrow split slice."""
    out = Image.new("RGB", (img.width + 2 * p, img.height))
    out.paste(img, (p, 0))
    return out


def view_rect(img_w, img_h, cx, cy, z, ow, oh):
    """The source rectangle game_view shows (x0, y0, vw, vh)."""
    cx = img_w / 2 if cx is None else cx
    cy = img_h / 2 if cy is None else cy
    vh = img_h / z
    vw = vh * ow / oh
    if vw > img_w:
        vw = img_w / z
        vh = vw * oh / ow
    return clamp(cx - vw / 2, 0, img_w - vw), clamp(cy - vh / 2, 0, img_h - vh), vw, vh


def crop(img, x0, y0, w, h, ow, oh):
    return arr(resample(img, x0, y0, w, h, ow, oh))


def rect(c, x, y, w, h, col, a=255):
    q = np.zeros((int(h), int(w), 4), np.float32)
    q[..., :3] = col
    q[..., 3] = a
    paste(c, q, x, y)


def framed_view(c, img_arr, x, y, border=6, colour=GOLDEN):
    h, w = img_arr.shape[:2]
    rect(c, x - border, y - border, w + 2 * border, h + 2 * border, colour)
    rgba = np.concatenate([img_arr, np.full((h, w, 1), 255, np.float32)], axis=2)
    paste(c, rgba, x, y)


# ------------------------------------------------------------------ the film

RACE_CY = 94


def build(e):
    b = e.bf
    sfx = lambda n: str(MUS / f"{n}.wav")  # noqa: E731
    # Audio fix 2026-10-23: the bed is the production-paced LiveSceneMusic render (DAC drums
    # present; FmSfxRenderTool's legacy path never enabled the S3K DAC), delayed one 48 kHz
    # frame to keep the fitted beat grid. Stingers sit +7 dB nearer game balance against it.
    e.bed(MUS / "bed-alz-live.wav", 0, 0.75, length=b(204) / 60, fade_out=1.2)
    ring_side = [0]

    def ring():
        # zPlaySound_CheckRing toggles zRingSpeaker on every ring request and picks
        # Sound34 (left) / Sound33 (right) (skdisasm Z80 Sound Driver.asm:1919-1925).
        ring_side[0] ^= 1
        return sfx("s3k-sfx-33" if ring_side[0] else "s3k-sfx-34")

    rc_open, rc_names, rc_fin, rc_after = clip("open"), clip("names"), clip("finish"), clip("after")
    o_src, n_src, f_src, a_src = (first_src(k) for k in ("open", "names", "finish", "after"))

    # ---- A. cold open (b0-b18): the pack at speed, then the start line and GO
    S_FRAG = 2110
    # Race framing (2026-10-23 HUD): the 16:9 crop keeps 180 of 224 rows. RACE_CY keeps the native
    # TIME/RINGS rows, the best panel and the room panel whole and leaves the bottom progress bar
    # wholly out; the capacity chapter frames the bottom instead, where the bar's stacks are the story.
    e.S(Game(0, b(6), rc_open, src=S_FRAG - o_src, cam=cam_static(160, RACE_CY, 1.0)))
    e.punches.append((b(2), 0.05))
    GO = 1324
    # the start line: the room's own GET READY panel on the title card, then GO
    e.S(Game(b(6), b(10), rc_open, src=GO - (b(10) - b(6)) - o_src, cam=cam_move((262, 16, 3.4), (240, 24, 2.4)),
             trans="slash", tdur=8))
    e.S(Game(b(10), b(18), rc_open, src=GO - o_src, cam=cam_static(160, RACE_CY, 1.0)))
    e.punches.append((b(10), 0.10))
    e.X(b(10), sfx("s3k-sfx-b6"), 1)
    e.O(Plate(b(12), b(18) - 4, plate("promise", 8, STOCK_NAME, True, HERO), e.W / 2, 860, enter="up", centre=True,
              dur=12, leave="fade"))

    # ---- B. title drop (b18-b34)
    e.S(Game(b(18), b(34), rc_open, src=GO + (b(18) - b(10)) - o_src, cam=cam_slam(1.3, 26, b(34) - b(18), 160, RACE_CY),
             dim=0.0))
    e.O(Fn(b(18), b(29), lambda c, f, o, ed: c.__imul__(1 - 0.5 * clamp((f - o.f0) / 4) * (1 - clamp((f - o.f1 + 12) / 12)))))
    e.O(Flash(b(18), 20))
    e.X(b(18), sfx("s3k-sfx-b3"), 1)
    title = plate("title", 22, STOCK_NAME, True, HERO)
    e.O(Plate(b(18), b(28), title, e.W / 2, 520, enter="cut", centre=True, leave="right", out_dur=10))
    e.O(Plate(b(19), b(28) - 2, lambda f: typed_plate(int(clamp((f - b(19)) / 3 + 1, 1, 11)), 8, HERO),
              e.W / 2 - title.shape[1] / 2 + 8, 520 - title.shape[0] / 2 - 128, enter="cut", leave="right", out_dur=10))
    e.O(Plate(b(22), b(28) - 4, plate("openggf", 6, STOCK_NAME), e.W / 2 + title.shape[1] / 2 - plate("openggf", 6).shape[1],
              520 + title.shape[0] / 2 + 28, enter="up", leave="right", out_dur=10))

    # ---- C. names (b34-b66): the in-game prompt, then every rival's nameplate, tracked live
    pr = clip("prompt")
    TYPE0 = 623  # first code point typed (capture frame)
    e.S(Game(b(34), b(40), pr, src=563 - first_src("prompt"), cam=cam_static(153, 62, 1.25),
             trans="wipe", tdur=16))
    for k in range(4):  # one tick per glyph, on the frame it appears (TYPE0 + 14k, clip-measured)
        e.X(b(34) + (TYPE0 - 563) + 14 * k, sfx("s1-sfx-b5-centre"), 0.4)

    # the line-up: eight relay peers' lobby presence spread across the S1 lobby, each with its own
    # name and colour; the hero mid-line. Their jumps replay the hero's own jump, delayed with distance,
    # so each jump ripples outwards (one jump per bar).
    lu = clip("lineup")
    JUMP0 = 1303
    e.S(Game(b(40), b(58), lu, src=JUMP0 - (b(46) - b(40)) - first_src("lineup"), cam=cam_static(160, 130, 1.0),
             trans="push", tdur=12, tdir="left"))
    for capf in (1273, 1369, 1465, 1561):  # hero take-offs (state.csv y), every 96 frames
        at = b(46) + capf - JUMP0
        e.punches.append((at + 30, 0.035))
        e.X(at, sfx("s1-sfx-a0"), 0.7)
    # language callouts under each runner, left to right, one per beat
    order = [(0, 16), (2, 52), (4, 88), (6, 124), (1, 196), (3, 232), (5, 268), (7, 304)]
    x0v, y0v, vwv, vhv = view_rect(320, 224, 160, 122, 1.0, e.W, e.H)
    hx = (160 - x0v) * e.W / vwv
    yt = plate("you", 3.3, (255, 255, 255), True, HERO)
    # each callout centred under its runner, then nudged apart left to right so none touch
    tags = [(sx - x0v) * e.W / vwv for _, sx in order[:4]] + [hx] + [(sx - x0v) * e.W / vwv for _, sx in order[4:]]
    ims = [plate(f"l{r}", 3.3, (255, 255, 255), True, RIVAL[r]) for r, _ in order[:4]] + [yt] + \
          [plate(f"l{r}", 3.3, (255, 255, 255), True, RIVAL[r]) for r, _ in order[4:]]
    xs = [cx - im.shape[1] / 2 for cx, im in zip(tags, ims)]
    xs[0] = max(16, xs[0])
    for i in range(1, len(xs)):
        xs[i] = max(xs[i], xs[i - 1] + ims[i - 1].shape[1] + 12)
    xs[-1] = min(xs[-1], e.W - ims[-1].shape[1] - 16)
    for i in range(len(xs) - 2, -1, -1):
        xs[i] = min(xs[i], xs[i + 1] - ims[i].shape[1] - 12)
    if xs[0] < 16:  # still too wide: start at the margin and keep the left-to-right spacing
        shift = 16 - xs[0]
        xs = [x + shift for x in xs]
    starts = [b(47 + k) for k in range(4)] + [b(46)] + [b(51 + k) for k in range(4)]
    for t0, im, x in zip(starts, ims, xs):
        e.O(Plate(t0, b(58), im, x, 976, enter="up", leave="fade", dur=10))
        if im is not yt:
            e.X(t0, ring(), 0.62)
    e.O(Plate(b(49), b(58) - 2, plate("h_names", 7, STOCK_NAME, True, HERO), e.W / 2, 160, enter="drop", centre=True))
    # the release: back to full screen, every name in one level
    e.S(Game(b(58), b(66), rc_open, src=2100 - o_src, trans="push", tdur=12, tdir="left",
             cam=cam_static(160, RACE_CY, 1.0)))

    # ---- D. colours (b66-b84): preset per beat on the profile page, then the hero in three games
    pf = clip("profile")
    PRESS0 = 1336  # first preset press (capture frame); presses every 24 frames = one beat
    e.S(Game(b(66), b(76), pf, src=PRESS0 - (b(67) - b(66)) - first_src("profile"), cam=cam_static(160, 100, 1.0),
             trans="wipe", tdur=16))
    e.O(Plate(b(66), b(75), plate("h_look", 7, STOCK_NAME, True, HERO), 1100, 40, enter="right", leave="right", dur=14))
    for k in range(8):
        e.X(b(67 + k), sfx("s3k-sfx-63"), 0.35 if k < 7 else 0.88)
    gl, el, al = clip("ghzlobby"), clip("ehzlobby"), clip("aizhero")

    def look_split(f, s, ed):
        panes = [(b(76), lambda lf: arr(game_view(pad_x(gl.frame(1797 - first_src("ghzlobby") + lf), 64), 80 + 64, 137, 1.6, ed.W, ed.H)), None),
                 (b(77), lambda lf: arr(game_view(pad_x(el.frame(1700 - first_src("ehzlobby") + lf), 64), 96 + 64, 110, 1.6, ed.W, ed.H)), None),
                 (b(78), lambda lf: arr(game_view(al.frame(2405 - first_src("aizhero") + lf), 150, 130, 1.6, ed.W, ed.H)), None)]
        c = slanted_split(ed, f, panes)
        for i, key in enumerate(("s1", "s2", "s3k")):
            t0 = b(76 + i)
            if f >= t0 + 6:
                p = plate(key, 4, STOCK_NAME, True, HERO)
                cx = (i + 0.5) * ed.W / 3 + 0.22 * (ed.H * 0.925 - ed.H / 2)
                x = min(cx - p.shape[1] / 2, ed.W - p.shape[1] - 24)
                paste(c, p, round(x), round(ed.H * 0.925), clamp((f - t0 - 6) / 6))
        return c

    e.S(Custom(b(76), b(84), look_split, trans="push", tdur=10, tdir="left"))
    e.O(Plate(b(79), b(84) - 2, plate("everywhere", 6, HERO, True, HERO), e.W / 2, 70, enter="drop", centre=True))

    # ---- E. the lobby is a level (b84-b114)
    hp = clip("hpz")
    HIDE = 1783  # Enter hides the menu (lobby-s3k-profile-newui frame; the original take was 5 earlier)
    # While the lobby's cards are up, frame the top of the screen so its header card stays whole;
    # once the menu hides (b88) ease down to the players.
    hide_u = (b(88) - b(84)) / (b(100) - b(84))
    e.S(Game(b(84), b(100), hp, src=HIDE - (b(88) - b(84)) - first_src("hpz"), trans="wipe", tdur=16,
             cam=lambda u: (160, 90 + 22 * smooth(clamp((u - hide_u) / 0.12)), 1.0)))
    for k in range(4):  # the hero's jumps (Space every 45 frames from HIDE + 10), ghosts echo them
        e.punches.append((b(88) + 10 + 45 * k + 4, 0.04))
    header(e, b(88), b(96), "h_lobby")
    e.punches.append((b(88), 0.08))
    for capf in (1794, 1884):  # hero take-offs (state.csv y)
        e.X(b(88) + capf - HIDE, sfx("s3k-sfx-62"), 0.7)
    l1, l2 = clip("ghzlobby"), clip("ehzlobby")

    def lobby_row(f, s, ed):
        c = stripes(ed, f, (8, 14, 30), (12, 20, 44))
        cw, ch, gap = 608, 456, 20
        left = (ed.W - 3 * cw - 2 * gap) / 2
        top = (ed.H - ch - 90) / 2
        cells = [(l1, 1165, "ghzlobby", "s1"), (l2, 1095, "ehzlobby", "s2"), (hp, 1805, "hpz", "s3k")]
        for i, (cl, s0, name, key) in enumerate(cells):
            t0 = b(100 + i)
            if f < t0:
                continue
            img = cl.frame(s0 - first_src(name) + f - b(100))
            x0, y0, vw, vh = view_rect(320, 224, 160, 124, 1.12, cw, ch)
            v = crop(img, x0, y0, vw, vh, cw, ch)
            u = ease_out((f - t0) / 12)
            x, y = left + i * (cw + gap), top - (1 - u) * ed.H
            framed_view(c, v, round(x), round(y), 6, HERO)
            p = plate(key, 5, STOCK_NAME, True, HERO)
            paste(c, p, round(x + cw / 2 - p.shape[1] / 2), round(y + ch + 24), clamp((f - t0 - 6) / 6))
        return c

    e.S(Custom(b(100), b(114), lobby_row, trans="push", tdur=10, tdir="left"))
    for i in range(3):
        e.X(b(100 + i), ring(), 0.66)

    # ---- F. no lives (b114-b138): death on 0 rings, jump-skip, reload, 3-2-1, GO on the section
    dt = clip("death")
    D_GO, D_DEAD, D_SKIP = 1741, 1515, 1557
    d0 = D_GO - (b(130) - b(114))
    out = lambda capf: b(114) + (capf - d0)  # noqa: E731
    e.S(Game(b(114), b(138), dt, src=d0 - first_src("death"), trans="wipe", tdur=16,
             cam=cam_static(160, RACE_CY, 1.0)))
    header(e, b(114), b(121), "h_retry")
    e.X(out(D_DEAD), sfx("s1-sfx-a3"), 1)
    e.punches.append((out(D_DEAD), 0.07))
    e.O(Plate(out(D_DEAD) + 14, out(D_SKIP) + 40, plate("skip", 6, STOCK_NAME, True, (255, 255, 255)),
              e.W / 2, 300, enter="up", centre=True, leave="fade"))
    for k, capf in enumerate((1561, 1621, 1681)):
        e.punches.append((out(capf), 0.06))
        e.X(out(capf), sfx("s3k-sfx-63"), 0.66)
    e.punches.append((b(130), 0.12))
    e.O(Flash(b(130), 10, 0.5))
    e.X(b(130), sfx("s3k-sfx-b6"), 1)

    def stopwatch(c, f, o, ed):
        t = min(f, b(130)) - out(D_DEAD)
        s = f"{t / 60:.2f}s"
        lab = plate("back", 5, STOCK_NAME, True, HERO)
        num = counter(s, 9, HERO if f >= b(130) else STOCK_NAME)
        a = clamp((f - o.f0) / 6) * (1 - clamp((f - o.f1 + 8) / 8))
        x = ed.W - num.shape[1] - 90
        paste(c, lab, ed.W - lab.shape[1] - 90, 690, a)
        paste(c, num, x, 690 + lab.shape[0] + 8, a)

    e.O(Fn(out(D_DEAD), b(136), stopwatch))

    # ---- G. 256 per room (b138-b154), capacity test
    cp = clip("cap")
    c_src = first_src("cap")
    def browser(f, s, ed):
        img = cp.frame(700 - c_src + f - s.f0)
        c = stripes(ed, f, (8, 14, 30), (12, 20, 44))
        v = crop(img, 0, 6, 320, 56, 1800, 315)
        framed_view(c, v, 60, 300, 6, GOLDEN)
        return c

    e.S(Custom(b(138), b(142), browser, trans="wipe", tdur=16))
    C_GO = 1247
    # The whole native screen: a 256 room's TA panel runs to row ~51 and the progress bar starts at ~205,
    # so no 16:9 crop shows both whole.
    def cap_screen(f, s, ed):
        img = cp.frame(C_GO - (b(144) - b(142)) - c_src + f - s.f0)
        c = stripes(ed, f, (8, 14, 30), (12, 20, 44))
        framed_view(c, crop(img, 0, 0, 320, 224, 1440, 1008), 240, 36, 6, GOLDEN)
        return c

    e.S(Custom(b(142), b(154), cap_screen, trans="push", tdur=10, tdir="left"))
    header(e, b(138), b(145), "h_cap")
    # Above the browser card, then above the count once the race screen is up (clear of TIME and the TA panel).
    e.O(Plate(b(139), b(142), plate("captest", 5, (255, 255, 255), True, (230, 60, 60)), 110, 200, enter="drop",
              leave="fade"))
    e.O(Plate(b(142), b(153), plate("captest", 5, (255, 255, 255), True, (230, 60, 60)), 110, 392, enter="drop",
              leave="fade"))

    def big_count(c, f, o, ed):
        u = ease_out((f - o.f0) / 30)
        n = int(round(256 * u))
        num = counter(str(n), 16, GOLDEN)
        lab = plate("players", 5, STOCK_NAME, True, GOLDEN)
        a = clamp((f - o.f0) / 6) * (1 - clamp((f - o.f1 + 8) / 8))
        # y 470 keeps the block above the progress bar's columns and their in-game counts
        paste(c, num, 96, 470, a)
        paste(c, lab, 96, 470 + num.shape[0] + 8, a)
        sub = plate("cap2", 4, (200, 210, 230), True, None)
        paste(c, sub, 96, 470 + num.shape[0] + lab.shape[0] + 20, a)

    e.O(Fn(b(146), b(154) - 1, big_count))

    # ---- H. climax (b154-b190): the pack to the signpost, the photo finish, standings, vote, next zone
    FIN = 4553
    e.S(Game(b(154), b(170), rc_fin, src=FIN - (b(170) - b(154)) - f_src, cam=cam_move((160, RACE_CY, 1.0), (165, 88, 1.08)),
             trans="iris", tdur=18))
    e.X(b(154), sfx("s3k-sfx-b3"), 0.88)

    def you_tag(c, f, o, ed):
        capf = FIN - (b(170) - f)
        tr = track("race-clean3", "hero", FIN - (b(170) - b(154)), FIN + 1, 9)
        hx, hy = tr[clamp(capf - (FIN - (b(170) - b(154))), 0, len(tr) - 1)]
        s = o.cam_shot
        cx, cy, z = s.cam(s.u(f))
        z *= ed.punch(f)
        x0, y0, vw, vh = view_rect(320, 224, cx, cy, z, ed.W, ed.H)
        sx, sy = (hx - x0) * ed.W / vw, (hy - 30 - y0) * ed.H / vh
        p = plate("you", 6, HERO, True, HERO)
        a = clamp((f - o.f0) / 8) * (1 - clamp((f - o.f1 + 6) / 6))
        paste(c, p, round(sx - p.shape[1] / 2), round(sy - p.shape[0]), a)

    tag = Fn(b(155), b(170), you_tag)
    tag.cam_shot = e.shots[-1]
    e.O(tag)
    e.punches.append((b(170), 0.14))
    e.O(Flash(b(170), 14, 0.7))
    e.X(b(170), sfx("s1-sfx-cf"), 1)
    # the finish and the HUD verdict
    e.S(Game(b(170), b(177), rc_fin, src=FIN - f_src, cam=cam_move((160, 120, 1.0), (240, 186, 2.1))))
    # standings: 0.03 s
    def standings_view(f, s, ed):
        img = rc_after.frame(5603 - a_src + f - s.f0)
        c = arr(game_view(img, 160, 112, 1.0, ed.W, ed.H)) * 0.35
        v = crop(img, 199, 23, 118, 44, 1416, 528)  # the room panel's standings rows, top-right since 2026-10-23
        u = ease_out((f - s.f0) / 12)
        framed_view(c, v, 110, round(170 + (1 - u) * 60), 6, HERO)
        return c

    e.S(Custom(b(177), b(182), standings_view, trans="push", tdur=10, tdir="left"))
    e.O(Fn(b(178), b(182) - 2, lambda c, f, o, ed: paste(c, counter("0.03s", 9, GOLDEN), 1510, 440,
                                                          clamp((f - o.f0) / 6))))
    # vote: the live tally
    VOTE0 = 6548 + 140  # race-clean3-newui (new lobby UI) runs 3 frames behind the original take

    def vote_view(f, s, ed):
        img = rc_after.frame(VOTE0 - a_src + f - s.f0)
        c = arr(game_view(img, 160, 112, 1.0, ed.W, ed.H)) * 0.12
        v = crop(img, 4, 152, 167, 53, 1002, 318)  # the lobby's vote card
        u = ease_out((f - s.f0) / 12)
        framed_view(c, v, 459, round(440 + (1 - u) * 60), 6, GOLDEN)
        return c

    e.S(Custom(b(182), b(186), vote_view, trans="push", tdur=10, tdir="left"))
    e.O(Plate(b(182), b(186), plate("h_vote", 7, STOCK_NAME, True, GOLDEN), e.W / 2, 330, enter="drop", centre=True))
    NEXT_CARD = 7531
    e.S(Game(b(186), b(190), rc_after, src=NEXT_CARD - a_src, cam=cam_slam(1.25, 20, b(190) - b(186), 165, RACE_CY)))
    e.O(Flash(b(186), 12, 0.6))
    e.X(b(186), sfx("s3k-sfx-b0"), 0.99)

    # ---- I. end card (b190-b204)
    END_SRC = 7703 - a_src

    def end_card(f, s, ed):
        c = blurred(rc_after.frame(END_SRC + f - s.f0), ed, radius=4, dim=0.35)
        u = ease_out((f - s.f0) / 18)
        bd = Image.open(BADGE).convert("RGBA").resize((320, 320), Image.LANCZOS)
        paste(c, arr(bd), ed.W / 2 - 160, 70 - (1 - u) * 60, clamp((f - s.f0) / 10))
        rows = [("endline", 9, HERO, 430, 6), ("url", 6, STOCK_NAME, 610, 16), ("status", 5, (200, 210, 230), 712, 22),
                ("disc", 3, (170, 180, 200), 880, 30), ("honest", 3, (170, 180, 200), 940, 34)]
        for key, sc, col, y, d in rows:
            p = plate(key, sc, col, key in ("endline", "url"), HERO if key == "endline" else None)
            paste(c, p, round(ed.W / 2 - p.shape[1] / 2), y, clamp((f - s.f0 - d) / 10))
        return c

    e.S(Custom(b(190), b(204), end_card, trans="xfade", tdur=14))
    e.O(Fade(b(204) - 50, b(204)))
    return b(204)
