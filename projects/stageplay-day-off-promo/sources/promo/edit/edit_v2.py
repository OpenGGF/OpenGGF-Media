#!/usr/bin/env python3
"""Day Off v2: the Stageplay introduction promo, revised (sp-promo-a, 2026-10-24).
Rebuild: tools/run_edit.py render edit/edit_v2.py, then tools/mux_final.py edit/edit_v2.py
(engine develop 81f25c89f, OpenGGF-Editor main dd5ee43; film take scenes/t10.stageplay).

Brief (one line each):
  Audience: Sonic fans and creators who have never seen Stageplay.
  Form and evidence: a staged story (direct Stageplay export) followed by real offscreen
    captures of both editors making it; the route line, Free->Puppet and every UI view are
    captured from the real editors, never mocked. Captions, callouts and titles are editorial.
  Promise: "Your own Sonic films. Real levels. Real physics."
  Story: Green Hill's first Motobug takes a day off and travels through three games.
  Hero moment: the planned route line tracing Green Hill's loop, then Sonic running it.
  Sound: the film's own soundtrack (ROM music, native SFX, synthesized Motobug voice);
    making-of over S3K Competition Menu ($2D, 106.6 BPM, ROM driver render) with the film's
    genuine SFX stem under editor playback; epilogue in the film's audio; S1 GHZ continues
    under the end card (ROM render aligned to the film's own GHZ to the sample).
  Palette: OpenGGF wordmark blue/gold, white type with navy stroke (title card yellow).
  Title face: Fira Sans Compressed Heavy (display) / Heavy Italic (lines); OpenGGF wordmark.
  End card: wordmark, STAGEPLAY, one line, URL, status, disclaimer.
Structure: film (cold open -> title at the hard cut -> story) -> pull-back into the editor
at the same frame -> rewind -> making-of chapters on the bed's beat grid (sets and cast,
Free -> Puppet, world and camera, the route, dialogue, screenplay, export) -> epilogue -> end card.
Revision 2: the making-of was "rushed" by its own pacing check (11 cuts and 12 captions in 20 s):
fewer, longer takes; callouts tied to what changes on screen instead of captions; no editorial
type on native UI (captions over menus sit on an opaque band that replaces the menu's key help).
v2 (after the user picked Day Off "best, no contest"): the film keeps its story and movement and
gains the engine's built-in voices for every speaker (the Motobug as a real speaker with a tail),
logical facing (no more backwards driving), native loop priority (it passes behind the loop's
front pillar) and native floor placement. The making-of is re-captured in the redesigned editor:
the in-level position picker chooses the route destination (floor snap), the voice form and the
fifteen preset voices, and the Object key's Facing row. Sound: voices now come from the engine.
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/tools/media")
from promo_kit import *  # noqa: F401,F403

ROOT = Path("/home/farrell/Videos/OGGF/sp-promo-a")
EDIT = dict(bpm=106.634, first=0.556, fps=60, size=(1920, 1080), out=str(ROOT / "out" / "day-off-stageplay-v2.mp4"),
            work=str(ROOT / "edit" / "build-v2"))

FR = ROOT / "edit" / "frames"
FILM = Frames(FR / "film-v2")             # Stageplay export of t10, 480x270 (x4 = the 1080p export)
ROUTE = Frames(FR / "route-v2")           # in-engine editor, route capture (picker; before-route scene)
TOUR = Frames(FR / "tour-v2")             # in-engine editor, tour of the finished scene
DROUTE = Frames(FR / "desktop-route-v2")  # OpenGGF Editor (desktop), the same route request
A = ROOT / "audio"
WORDMARK = Image.open("/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/src/main/resources/titlescreen/titletext.png").convert("RGBA")
CAMS = {int(k): v for k, v in json.loads((ROOT / "edit" / "film-camera-v2.json").read_text()).items()}  # t10 simulate
SCREENPLAY = json.loads((ROOT / "captures" / "v2" / "editor-tour" / "day-off.screenplay.json").read_text())

# Scene facts (scenes/t10.stageplay; captures/v2/*/events.json; preview frames matched to film frames)
LOOP = 840            # loop shot entry (hard cut)
PULL = 3698           # ledge shot frame shown paused at TOUR frame 0..149
EPI = 4000            # epilogue start (inside the FADE_BLACK at 4018)
FILM_END = 4498
HUD_PREVIEW = (18, 186, 960, 540)          # in-engine editor preview rect at 1920x1080 (2x film)
DESK_PREVIEW = (447, 159, 960, 540)        # desktop editor preview rect (2x film)
ROUTE_PLAY = 2210                          # ROUTE frame where playback starts at scene frame LOOP (exact)
DROUTE_PLAY = 383                          # DROUTE frame where playback starts at scene frame LOOP (exact)
PATROL_PLAY = 626                          # TOUR frame showing scene 225 (playback from 624; matched)
PUSH_PLAY = 1685                           # TOUR frame showing scene 350 (exact)
REPLY_PLAY = 2629                          # TOUR frame showing scene 1280 (exact)

NAVY_STROKE = (6, 14, 48)
BAND = (7, 12, 34)


def line(s, size=66):
    """The film's voice: heavy italic, white, navy stroke, hard shadow (never the game's font)."""
    return text(s, "title_it", size, WHITE, stroke=6, sfill=NAVY_STROKE, shadow=7)


def band_at(top=925):
    """An opaque lower band that replaces native key-help rows under a caption. Its soft edge sits
    above `top`; raise `top` when a list's last row would otherwise be half covered."""
    def band_fn(c, f, o, e):
        a = clamp((f - o.f0) / 8) * (1 - clamp((f - o.f1 + 8) / 8))
        ramp = np.clip((np.arange(top - 22, e.H) - (top - 22)) / 22.0, 0, 1)[:, None, None] * a
        c[top - 22:] = c[top - 22:] * (1 - ramp) + np.array(BAND, np.float32) * ramp
    return band_fn


def caption(e, f0, f1, s, band=None, y=1000, band_top=925):
    """A line at the bottom. band = first frame from which the backing is the opaque band (menus/UI)
    instead of the gradient shade (gameplay); a caption can cross a cut from one to the other."""
    if band is None or band > f0:
        e.O(Shade(f0, f1 if band is None else band + 8, "bottom"))
    if band is not None:
        e.O(Fn(max(f0, band), f1, band_at(band_top)))
    e.O(Txt(f0, f1, line(s), e.W / 2, y, enter="up", leave="fade", centre=True, dur=12, out_dur=8))


def label(e, f0, f1, s, x=60, y=56):
    """A pill naming what the shot shows; lighter than a sentence."""
    e.O(Txt(f0 + 4, f1, chip(s, size=42), x, y, enter="left", leave="fade", dur=12, out_dur=8))


def preview_cam(rect, zoom):
    x, y, w, h = rect
    return (x + w / 2, y + h / 2, zoom)


def hold_move(a, b, u0, u1):
    """Hold camera a until u0, ease to b by u1, then hold b."""
    return lambda u: tuple(a[i] + (b[i] - a[i]) * smooth(clamp((u - u0) / (u1 - u0))) for i in range(3))


def film_frame(i):
    return FILM.frame(int(clamp(i, 0, FILM_END - 1)))


def fill(c, x0, y0, x1, y1, colour, a):
    x0, y0, x1, y1 = (int(round(v)) for v in (x0, y0, x1, y1))
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(c.shape[1], x1), min(c.shape[0], y1)
    if a > 0 and x0 < x1 and y0 < y1:
        c[y0:y1, x0:x1] = c[y0:y1, x0:x1] * (1 - a) + np.array(colour, np.float32) * a


@lru_cache(maxsize=256)
def ring(w, h, t=6, r=14):
    """A rounded outline (yellow with a navy rim) as a float RGBA array."""
    pad = 4
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w + 2 * pad - 1, h + 2 * pad - 1), r + pad, outline=NAVY_STROKE + (255,), width=t + 2 * pad)
    d.rounded_rectangle((pad, pad, w + pad - 1, h + pad - 1), r, outline=YELLOW + (255,), width=t)
    return arr(im)


def callout(x0, y0, x1, y1):
    """A yellow box that lands around something on screen (output pixels)."""
    def fn(c, f, o, e):
        u = ease_out(clamp((f - o.f0) / 10))
        a = clamp((f - o.f0) / 4) * (1 - clamp((f - o.f1 + 8) / 8))
        g = (1 - u) * 26
        w, h = int(x1 - x0 + 2 * g), int(y1 - y0 + 2 * g)
        paste(c, ring(w, h), x0 - g - 4, y0 - g - 4, a)
    return fn


# ------------------------------------------------------------------------------ callout graphics
def role_switch(flip):
    """FREE | PUPPET: the lit half follows the Motobug's role key (scene 327, the PUPPET key)."""
    dim_fg, dim_bg = (150, 160, 196), (14, 22, 62)
    on = {n: chip(n, size=46) for n in ("FREE", "PUPPET")}
    off = {n: chip(n, size=46, fg=dim_fg, bg=dim_bg) for n in ("FREE", "PUPPET")}

    def fn(c, f, o, e):
        a = clamp((f - o.f0) / 8) * (1 - clamp((f - o.f1 + 8) / 8))
        x = 60 - (1 - ease_out(clamp((f - o.f0) / 12))) * 420
        u = clamp((f - flip) / 6)
        paste(c, on["FREE"], x, 52, a * (1 - u))
        paste(c, off["FREE"], x, 52, a * u)
        x2 = x + on["FREE"].shape[1] + 14
        pop = 1 + 0.22 * (1 - ease_out(clamp((f - flip) / 12))) if f >= flip else 1.0
        lit = scaled(on["PUPPET"], pop)
        dx, dy = (lit.shape[1] - on["PUPPET"].shape[1]) / 2, (lit.shape[0] - on["PUPPET"].shape[0]) / 2
        paste(c, off["PUPPET"], x2, 52, a * (1 - u))
        paste(c, lit, x2 - dx, 52 - dy, a * u)
    return fn


def key_brackets(scene0, rect=(586.0, 769.5, 240.0, 135.0), key=439):
    """Corner brackets on the camera key's framing (world rect at zoom 2), tracked through the
    film camera's own move (t06 simulate telemetry) until the camera lands on them at the key."""
    tag = chip("CAMERA KEY  439", size=40)

    def fn(c, f, o, e):
        s = scene0 + (f - o.f0)
        cx, cy, z = CAMS[s]
        k = 4 * z                                       # film pixels -> output (2x preview at zoom 2)
        x0, y0 = (rect[0] - cx) * k, (rect[1] - cy) * k
        x1, y1 = x0 + rect[2] * k, y0 + rect[3] * k
        a = clamp((f - o.f0 - 4) / 10) * (1 - clamp((s - key) / 10))
        if a <= 0:
            return
        L, T = 84, 9
        for X, Y, sx, sy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
            for colour, g in ((NAVY_STROKE, 3), (YELLOW, 0)):
                hx = (X, X + sx * L) if sx > 0 else (X + sx * L, X)
                vy = (Y, Y + sy * L) if sy > 0 else (Y + sy * L, Y)
                hy = (Y, Y + sy * T) if sy > 0 else (Y + sy * T, Y)
                vx = (X, X + sx * T) if sx > 0 else (X + sx * T, X)
                fill(c, hx[0] - g, hy[0] - g, hx[1] + g, hy[1] + g, colour, a)
                fill(c, vx[0] - g, vy[0] - g, vx[1] + g, vy[1] + g, colour, a)
        paste(c, tag, x0, y0 - tag.shape[0] - 10, a * (1 - clamp((s - 425) / 8)))
    return fn


# ------------------------------------------------------------------------------ custom screens
def pullback(f, s, e):
    """The film, frozen on PULL, shrinks into the editor's preview where the same frame is shown."""
    u = smooth((f - s.f0) / max(1, s.f1 - s.f0))
    bg = arr(TOUR.frame(int(f - s.f0)))
    x, y, w, h = HUD_PREVIEW
    rx, ry = x * u, y * u
    rw, rh = e.W + (w - e.W) * u, e.H + (h - e.H) * u
    pic = resample(film_frame(PULL), 0, 0, 480, 270, int(round(rw)), int(round(rh)))
    c = bg.copy()
    c *= clamp(u * 1.4)                      # the editor emerges around the shrinking film
    rgba = np.concatenate([arr(pic), np.full((pic.height, pic.width, 1), 255, np.float32)], axis=2)
    paste(c, rgba, rx, ry)
    return c


def dimmed(clip, src, amount):
    """The editor, held and darkened behind the product title (a title card, not gameplay)."""
    def fn(f, s, e):
        k = f - s.f0
        return arr(clip.frame(src + k)) * (1 - amount * clamp((k - 4) / 10))
    return fn


def split_frame(r, d, k, e, chips_until):
    """Both editors at the same scene frame: each slice shows its editor's preview and chrome."""
    hud = arr(ROUTE.frame(r))
    desk = arr(DROUTE.frame(d))
    xs, ys, _ = e.grids()
    edge = e.W / 2 + 0.18 * (ys - e.H / 2)
    left_dx = HUD_PREVIEW[0] + HUD_PREVIEW[2] / 2 - e.W / 4           # HUD preview centre -> W/4
    right_dx = DESK_PREVIEW[0] + DESK_PREVIEW[2] / 2 - 3 * e.W / 4    # desktop preview centre -> 3W/4
    c = np.zeros((e.H, e.W, 3), np.float32)
    hx = np.clip((xs + left_dx).astype(int), 0, e.W - 1)
    dx = np.clip((xs + right_dx).astype(int), 0, e.W - 1)
    yi = ys.astype(int)
    drop = int(round(-(1 - ease_out(k / 16)) * e.H)) if k < 16 else 0
    left = xs < edge
    c[left] = hud[yi[left], hx[left]]
    right = ~left & (ys >= -drop)
    yd = np.clip(yi + drop, 0, e.H - 1)
    c[right] = desk[yd[right], dx[right]]
    c[np.abs(xs - edge) < 7] = np.array(YELLOW, np.float32)
    a = clamp((k - 8) / 8) * (1 - clamp((k - chips_until + 8) / 8))
    for name, cx in (("IN-ENGINE EDITOR", e.W / 4), ("OPENGGF EDITOR (DESKTOP)", 3 * e.W / 4)):
        pill = chip(name, size=44)
        paste(c, pill, cx - pill.shape[1] / 2, 752, a)       # in the empty band under both previews
    return c


def split_then_film(r0, d0, film0, wipe0, wipe_len):
    """Route playback in both editors, then a left-to-right wipe into the clean film."""
    def fn(f, s, e):
        k = f - s.f0
        ed = split_frame(r0 + k, d0 + k, k, e, wipe0)
        if k < wipe0:
            return ed
        film = arr(game_view(film_frame(film0 + k), None, None, 1.0, e.W, e.H))
        edge = ease_out((k - wipe0) / wipe_len) * (e.W + 120) - 60
        xs, _, _ = e.grids()
        out = np.where((xs < edge)[..., None], film, ed)
        return np.where((np.abs(xs - edge) < 7)[..., None], np.array(YELLOW, np.float32), out)
    return fn


def screenplay_lines():
    """A real excerpt of the editor's screenplay export: the loop shot's route and Sonic's line."""
    shot = SCREENPLAY["shots"][1]
    mv = [a for a in shot["actions"]["sonic"] if a["kind"] == "MOVE_TO"][0]
    m = mv["motion"]
    dl = shot["dialogue"][0]
    s = shot["set"]
    return [("c", "// day-off.screenplay.json, exported by the editor (excerpt)"),
            ("n", '"id" : "%s",  "set" : { "gameId" : "%s", "zone" : %d, "act" : %d },' % (shot["id"], s["gameId"], s["zone"], s["act"])),
            ("n", '"actions" : { "sonic" : [ {'),
            ("n", '    "kind" : "%s",  "frame" : %d,  "x" : %.1f,  "y" : %.1f,' % (mv["kind"], mv["frame"], mv["x"], mv["y"])),
            ("n", '    "motion" : { "startingAction" : "%s",  "travelSpeed" : "%s",' % (m["startingAction"], m["travelSpeed"])),
            ("n", '                 "endingAction" : "%s",  "endingFacing" : "%s" } },' % (m["endingAction"], m["endingFacing"])),
            ("n", '    ... ] },'),
            ("n", '"dialogue" : [ {'),
            ("n", '    "startFrame" : %d,  "speakerActor" : "%s",' % (dl["startFrame"], dl["speakerActor"])),
            ("n", '    "text" : "%s" }, ... ]' % dl["text"])]


LINES = screenplay_lines()


@lru_cache(maxsize=64)
def code_panel(chars, w=1560, h=650):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(12, 16, 32, 240), outline=(72, 96, 170, 255), width=3)
    for k, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((24 + k * 32, 20, 44 + k * 32, 40), fill=col)
    d.text((140, 15), "screenplay v6", font=font("mono", 26), fill=(150, 160, 190))
    f = font("mono", 31)
    left, y = chars, 78
    for kind, ln in LINES:
        shown = ln[:max(0, left)]
        left -= len(ln) + 1
        if kind == "c":
            d.text((32, y), shown, font=f, fill=(112, 136, 124))
        else:
            x = 32
            for tok in shown.split(" "):
                colour = (160, 220, 120) if '"' in tok else (120, 190, 255) if tok[:1].isdigit() else (225, 230, 240)
                d.text((x, y), tok, font=f, fill=colour)
                x += f.getlength(tok + " ")
        y += 54
    return arr(im)


def screenplay(f, s, e):
    k = f - s.f0
    c = blurred(film_frame(1190), e, radius=4, dim=0.42, zoom=1.15)
    chars = int(k * 330 / 60) // 6 * 6                    # typed fast; quantised so panels cache
    panel = code_panel(chars)
    paste(c, panel, (e.W - panel.shape[1]) / 2, 150 + (1 - ease_out(clamp(k / 14))) * 40, clamp(k / 8))
    return c


def end_card(f, s, e):
    return blurred(film_frame(FILM_END - 1), e, radius=2, dim=0.40, zoom=1.15)


def build(e):
    # ---------------------------------------------------------------- A. the film
    e.S(Game(0, PULL, FILM, src=0))
    # Title on the cold open's hard cut (the drop off the hill -> the loop). The film's own GHZ
    # restart on that cut is the stinger; an editorial hit would collide with its soundtrack.
    e.O(Flash(LOOP, 8, peak=0.45))
    e.O(Shade(LOOP, LOOP + 175, "top"))
    e.O(Txt(LOOP + 4, LOOP + 175, text("DAY", "title", 210, YELLOW, stroke=10, sfill=NAVY_STROKE, shadow=11),
            e.W / 2 - 190, 205, enter="pop", leave="fade", centre=True, dur=12, out_dur=10))
    e.O(Txt(LOOP + 14, LOOP + 175, text("OFF", "title", 210, YELLOW, stroke=10, sfill=NAVY_STROKE, shadow=11),
            e.W / 2 + 190, 205, enter="pop", leave="fade", centre=True, dur=12, out_dur=10))
    e.O(Txt(LOOP + 26, LOOP + 175, text("A  STAGEPLAY  FILM", "title_it", 44, WHITE, stroke=4, sfill=NAVY_STROKE,
                                        shadow=5, tracking=10), e.W / 2, 362, enter="up", leave="fade", centre=True))
    e.bed(A / "film-v2.wav", 0, 1.0, src_seconds=0, length=(PULL + 250) / 60, fade_out=1.2)
    t = PULL
    # ---------------------------------------------------------------- B. pull-back + product title
    e.S(Custom(t, t + 60, pullback))
    hold0 = t + 60
    e.S(Custom(hold0, hold0 + 90, dimmed(TOUR, 60, 0.55)))
    wm = arr(WORDMARK.resize((WORDMARK.width * 2 // 3, WORDMARK.height * 2 // 3), Image.NEAREST))
    e.O(Txt(hold0 + 6, hold0 + 90, wm, e.W / 2, 330, enter="pop", leave="fade", centre=True, dur=12))
    e.O(Txt(hold0 + 14, hold0 + 90, text("STAGEPLAY", "title", 190, YELLOW, stroke=9, sfill=NAVY_STROKE, shadow=10),
            e.W / 2, 520, enter="pop", leave="fade", centre=True, dur=12))
    e.O(Txt(hold0 + 30, hold0 + 90, line("Your own Sonic films. Real levels. Real physics.", 60),
            e.W / 2, 690, enter="up", leave="fade", centre=True, dur=14))
    e.O(Flash(hold0 + 6, 10, peak=0.5))
    t = hold0 + 90
    # ---------------------------------------------------------------- C. rewind (the editor scrubs back)
    e.S(Game(t, t + 75, TOUR, src=150))
    e.X(t, A / "rewind-v2.wav", 0.55)
    t += 75
    # ---------------------------------------------------------------- D. making-of, on the bed's beats
    d0 = t
    beat = 60 * 60 / EDIT["bpm"]
    first = 0.556 * 60

    def at(k):  # output frame of bed beat k (k may be fractional)
        return int(round(d0 + first + k * beat))

    k = 0

    def seg(beats, clip, src=None, cam=None, end=None):
        """A shot of `beats` beats; `end` pins the clip frame at the outgoing cut instead of src."""
        nonlocal k
        f0 = d0 if k == 0 else at(k)
        f1 = at(k + beats)
        if end is not None:
            src = end - (f1 - f0)
        e.S(Game(f0, f1, clip, src=src, cam=cam))
        k += beats
        return f0, f1

    # 1. Sets and cast: the shot list across all three games, then the cast it calls on
    seg(6, TOUR, end=486)                                  # menu opens, walks the shot list, closes
    seg(4, TOUR, end=624, cam=hold_move((960, 540, 1.0), (1450, 430, 2.15), 0.16, 0.4))
    # 2. Free -> Puppet: the badnik's own AI until frame 327, then held, so its native turn never comes
    f0, f1 = seg(6.5, TOUR, 624, cam=cam_static(*preview_cam(HUD_PREVIEW, 2.0)))
    flip = f0 + PATROL_PLAY + (327 - 225) - 624
    e.O(Fn(f0 + 4, f1, role_switch(flip)))
    caption(e, f0 + 8, flip - 2, "It runs its own badnik AI")
    g0, g1 = seg(4, TOUR, 1142)                            # the PUPPET key: mode and its facing
    caption(e, flip, g1, "Now it waits for you", band=g0)
    e.O(Fn(g0 + 40, g1, callout(872, 544, 1236, 594)))     # Facing  Left / Right (logical direction)
    # 3. World and camera: clear the level's badniks; key a push-in and watch the camera land on it
    seg(3.5, TOUR, 1326)                                   # world commands
    seg(3.5, TOUR, end=1683)                               # camera key at frame 439: zoom 2
    f0, f1 = seg(4, TOUR, PUSH_PLAY + 3, cam=cam_static(*preview_cam(HUD_PREVIEW, 2.0)))
    e.O(Fn(f0, f1, key_brackets(350 + 3)))
    e.stem(A / "film-sfx-v2.wav", 350 + 3, f0, f1 - f0, gain=1.0)
    # 4. The route: pick the spot in the level, fail with a reason, fix it, see the checked line, apply
    f0, f1 = seg(10, ROUTE, end=420)                       # form -> picker crosshair -> floor snap -> form
    caption(e, f0 + 52, f1, "Pick a spot. It snaps to the floor.", band=f0)
    seg(5.5, ROUTE, end=800)                               # Find route at Walk: the red cross, one-line result
    f0, f1 = seg(5, ROUTE, 890)                            # Details: the planner's reason
    e.O(Fn(f0 + 30, f1, callout(276, 416, 556, 470)))      # "needs Run" (row 424..463, x 288..545 measured)
    seg(5, ROUTE, end=1573)                                # Run, Hard, Left (same picked point)
    f0, f1 = seg(9, ROUTE, 1590, cam=cam_move((960, 540, 1.0), (*preview_cam(HUD_PREVIEW, 2.0)[:2], 2.0),
                                              ease=lambda u: smooth(clamp(u * 2.2))))
    caption(e, f0 + 40, f1, "Planned and checked under real physics")
    seg(3.5, ROUTE, end=ROUTE_PLAY)                        # Apply route
    # playback in both editors (byte-identical applied scene files), then the wipe into the film
    p0, p1 = at(k), at(k + 12)
    lead = 40                                              # scene 880
    wipe0 = 210                                            # scene 1090: Sonic is out of the loop
    e.S(Custom(p0, p1, split_then_film(ROUTE_PLAY + lead, DROUTE_PLAY + lead, LOOP + lead, wipe0, 26)))
    e.O(Txt(p0 + 14, p0 + wipe0 - 2, line("Two editors. One scene file."), e.W / 2, 112, enter="down",
            leave="fade", centre=True, dur=12, out_dur=8))
    label(e, p0 + wipe0 + 10, p1, "FILM")
    e.stem(A / "film-sfx-v2.wav", LOOP + lead, p0, p1 - p0, gain=1.0)
    k += 12
    # 5. Lines and voices: the line Sonic just said, then the Motobug's own voice and the presets
    f0, f1 = seg(3.5, TOUR, 1985)
    e.O(Fn(f0 + 16, f1, callout(848, 281, 1772, 404)))
    f0, f1 = seg(4, TOUR, 2306)                            # Motobug / voice: Buzz, Word, pitch 69, level 80
    caption(e, f0 + 10, at(k + 3), "Every speaker has its own voice", band=f0, band_top=912)   # hides the presets' last row whole
    f0, f1 = seg(3, TOUR, 2452)                            # the fifteen voices; the Motobug's default
    e.O(Fn(f0 + 12, f1, callout(58, 734, 975, 789)))
    f0, f1 = seg(3.5, TOUR, REPLY_PLAY + 3, cam=cam_static(*preview_cam(HUD_PREVIEW, 2.0)))
    e.stem(A / "film-sfx-v2.wav", 1280 + 3, f0, f1 - f0, gain=1.0)   # "Day off." with its voice and tail
    # 6. The whole scene as text, then export
    s0, s1 = at(k), at(k + 6)
    e.S(Custom(s0, s1, screenplay))
    e.O(Txt(s0 + 30, s1, line("Prefer text? The whole film is a screenplay."), e.W / 2, 1000, enter="up",
            leave="fade", centre=True, dur=12, out_dur=8))
    k += 6
    f0, f1 = seg(3, TOUR, 3008)                            # export film
    caption(e, f0 + 8, f1, "Export the finished film", band=f0)
    t = f1
    e.bed(A / "s3k-music-2d-paced.wav", d0, 0.95, src_seconds=0.0, length=(t - d0) / 60 + 0.35,
          fade_in=0.15, fade_out=1.2)
    # ---------------------------------------------------------------- E. epilogue (the film's own ending)
    e0 = t
    e.S(Game(e0, e0 + (FILM_END - EPI), FILM, src=EPI, trans="xfade", tdur=20))
    e.bed(A / "film-v2.wav", e0, 1.0, src_seconds=EPI / 60, length=(FILM_END - EPI) / 60, fade_in=0.3, fade_out=0.02)
    t = e0 + (FILM_END - EPI)
    # ---------------------------------------------------------------- F. end card
    ghz_pos = (FILM_END - 4018) / 60            # song position where the film's GHZ ends (cue at 4018)
    e.bed(A / "s1-music-81-paced.wav", t, 0.775, src_seconds=ghz_pos, length=7.0, fade_out=2.6)
    e.S(Custom(t, t + 420, end_card, trans="xfade", tdur=24))
    wm2 = arr(WORDMARK)
    e.O(Txt(t + 10, t + 420, wm2, e.W / 2, 290, enter="pop", leave="fade", centre=True, dur=14))
    e.O(Txt(t + 22, t + 420, text("STAGEPLAY", "title", 150, YELLOW, stroke=8, sfill=NAVY_STROKE, shadow=9),
            e.W / 2, 470, enter="up", leave="fade", centre=True, dur=14))
    e.O(Txt(t + 34, t + 420, line("Your own Sonic films. Real levels. Real physics.", 56), e.W / 2, 600,
            enter="up", leave="fade", centre=True, dur=14))
    e.O(Txt(t + 46, t + 420, text("github.com/OpenGGF/OpenGGF", "body", 44, WHITE, stroke=3, sfill=NAVY_STROKE,
                                  shadow=4), e.W / 2, 700, enter="fade", leave="fade", centre=True))
    e.O(Txt(t + 52, t + 420, text("Stageplay is in development for OpenGGF 0.7", "body", 34, (200, 210, 235),
                                  stroke=2, sfill=NAVY_STROKE), e.W / 2, 770, enter="fade", leave="fade", centre=True))
    e.O(Txt(t + 58, t + 420, text("Fan-made and free. Not affiliated with SEGA. Requires your own ROM.", "body", 30,
                                  (180, 190, 215), stroke=2, sfill=NAVY_STROKE), e.W / 2, 980, enter="fade",
            leave="fade", centre=True))
    e.O(Fade(t + 380, t + 420))
    return t + 420
