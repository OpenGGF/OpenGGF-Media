#!/usr/bin/env python3
"""Day Off: the Stageplay introduction promo (sp-promo-a, 2026-10-24).
Rebuild: tools/run_edit.py render edit/edit.py   (promo_kit compositor, 4 workers)

Brief (one line each):
  Audience: Sonic fans and creators who have never seen Stageplay.
  Form and evidence: a staged story (direct Stageplay export) followed by real offscreen
    captures of both editors making it; the route line, Free->Puppet and every UI view are
    captured from the real editors, never mocked. Captions and the title are editorial.
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
at the same frame -> rewind -> making-of beats on the bed's beat grid -> epilogue -> end card.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/tools/media")
from promo_kit import *  # noqa: F401,F403

ROOT = Path("/home/farrell/Videos/OGGF/sp-promo-a")
EDIT = dict(bpm=106.634, first=0.556, fps=60, size=(1920, 1080), out=str(ROOT / "out" / "day-off-stageplay.mp4"),
            work=str(ROOT / "edit" / "build"))

FR = ROOT / "edit" / "frames"
FILM = Frames(FR / "film")                # Stageplay export, 480x270 (x4 = the 1080p export, pixel-exact)
ROUTE = Frames(FR / "route")              # in-engine editor, route capture (before-route scene)
TOUR = Frames(FR / "tour")                # in-engine editor, tour of the finished scene
DROUTE = Frames(FR / "desktop-route")     # OpenGGF Editor (desktop), route capture
DTOUR = Frames(FR / "desktop-tour")       # OpenGGF Editor (desktop), tour
A = ROOT / "audio"
WORDMARK = Image.open("/home/farrell/code/projects/OpenGGF/.worktrees/sp-promo-a/src/main/resources/titlescreen/titletext.png").convert("RGBA")

# Scene facts (scenes/t06.stageplay; captures/*/events.json)
LOOP = 840            # loop shot entry (hard cut); route playback in ROUTE starts at its frame 1914
PULL = 3698           # ledge shot frame shown paused at TOUR frame 0..149
EPI = 4000            # epilogue start (inside the FADE_BLACK at 4018)
FILM_END = 4498
HUD_PREVIEW = (18, 186, 960, 540)          # in-engine editor preview rect at 1920x1080 (2x film)
DESK_PREVIEW = (447, 159, 960, 540)        # desktop editor preview rect (2x film)
ROUTE_PLAY = 1914                          # ROUTE frame where playback starts at scene frame LOOP
DROUTE_PLAY = 712                          # DROUTE frame where playback starts at scene frame LOOP

NAVY_STROKE = (6, 14, 48)
GOLD_W = (255, 200, 40)


def line(s, size=66):
    """The film's voice: heavy italic, white, navy stroke, hard shadow (never the game's font)."""
    return text(s, "title_it", size, WHITE, stroke=6, sfill=NAVY_STROKE, shadow=7)


def caption(e, f0, f1, s, y=958):
    e.O(Shade(f0, f1, "bottom"))
    e.O(Txt(f0, f1, line(s), e.W / 2, y, enter="up", leave="fade", centre=True, dur=12, out_dur=8))


def label(e, f0, f1, s, x=60, y=56):
    """A pill naming what the shot shows; lighter than a sentence."""
    e.O(Txt(f0 + 4, f1, chip(s, size=42), x, y, enter="left", leave="fade", dur=12, out_dur=8))


def preview_cam(rect, zoom):
    x, y, w, h = rect
    return (x + w / 2, y + h / 2, zoom)


def film_frame(i):
    return FILM.frame(int(clamp(i, 0, FILM_END - 1)))


# ------------------------------------------------------------------------------ custom screens
def pullback(f, s, e):
    """The film, frozen on PULL, shrinks into the editor's preview where the same frame is shown."""
    u = smooth((f - s.f0) / max(1, s.f1 - s.f0))
    bg = arr(TOUR.frame(int(f - s.f0)))
    x, y, w, h = HUD_PREVIEW
    rx, ry = 0 + (x - 0) * u, 0 + (y - 0) * u
    rw, rh = e.W + (w - e.W) * u, e.H + (h - e.H) * u
    pic = resample(film_frame(PULL), 0, 0, 480, 270, int(round(rw)), int(round(rh)))
    c = bg.copy()
    c *= clamp(u * 1.4)                      # the editor emerges around the shrinking film
    rgba = np.concatenate([arr(pic), np.full((pic.height, pic.width, 1), 255, np.float32)], axis=2)
    paste(c, rgba, rx, ry)
    return c


def peel(clip, src0, film0, wipe0, wipe_len, rect):
    """Zoomed editor preview (route line, white cross) peeling left-to-right into the clean film."""
    def fn(f, s, e):
        k = f - s.f0
        ed = arr(game_view(clip.frame(src0 + k), *preview_cam(rect, 2.0), e.W, e.H))
        if k < wipe0:
            return ed
        film = arr(game_view(film_frame(film0 + k), None, None, 1.0, e.W, e.H))
        edge = ease_out((k - wipe0) / wipe_len) * (e.W + 120) - 60
        xs, _, _ = e.grids()
        m = (xs < edge)[..., None]
        out = np.where(m, film, ed)
        band = (np.abs(xs - edge) < 7)[..., None]
        return np.where(band, np.array(YELLOW, np.float32), out)
    return fn


def two_editors(r0, d0):
    """Both editors at the same scene frame: each slice shows its editor's preview and chrome."""
    def fn(f, s, e):
        k = f - s.f0
        hud = arr(ROUTE.frame(r0 + k))
        desk = arr(DROUTE.frame(d0 + k))
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
        for label, cx in (("IN-ENGINE EDITOR", e.W / 4), ("OPENGGF EDITOR (DESKTOP)", 3 * e.W / 4)):
            pill = chip(label, size=44)
            paste(c, pill, cx - pill.shape[1] / 2, e.H * 0.875, clamp((k - 8) / 8))
        return c
    return fn


def screenplay_panel(f, s, e):
    c = arr(TOUR.frame(2440 + (f - s.f0) // 3)) * 0.35
    return c


def end_card(f, s, e):
    c = blurred(film_frame(FILM_END - 1), e, radius=2, dim=0.40, zoom=1.15)
    return c


def build(e):
    b = e.bf
    t = 0
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
    e.bed(A / "film.wav", 0, 1.0, src_seconds=0, length=(PULL + 250) / 60, fade_out=1.2)
    t = PULL
    # ---------------------------------------------------------------- B. pull-back + product title
    e.S(Custom(t, t + 60, pullback))
    hold0 = t + 60
    e.S(Game(hold0, hold0 + 90, TOUR, src=60))
    e.O(Fn(hold0 + 4, hold0 + 90, lambda c, f, o, ed: c.__imul__(1 - 0.55 * clamp((f - o.f0) / 10))))
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
    e.X(t, A / "rewind.wav", 0.55)
    t += 75
    # ---------------------------------------------------------------- D. making-of, on the bed's beats
    d0 = t
    e.bed(A / "s3k-music-2d-paced.wav", d0, 0.62, src_seconds=0.0, length=44.0, fade_in=0.15, fade_out=1.4)
    beat = 60 * 60 / EDIT["bpm"]
    first = 0.556 * 60

    def at(k):  # output frame of bed beat k (k may be fractional)
        return int(round(d0 + first + k * beat))

    k = 0

    def seg(beats, clip, src, cam=None, cap=None, cap_delay=6):
        nonlocal k
        f0 = d0 if k == 0 else at(k)
        f1 = at(k + beats)
        e.S(Game(f0, f1, clip, src=src, cam=cam))
        if cap:
            caption(e, f0 + cap_delay, f1, cap)
        k += beats
        return f0, f1

    seg(4, TOUR, 290)
    f0, f1 = seg(3, TOUR, 482)
    caption(e, d0 + 8, f1, "Real levels. A cast from any game.")
    f0, f1 = seg(6, TOUR, 629, cam=cam_static(*preview_cam(HUD_PREVIEW, 1.6)))
    turn = f0 + (359 - 225)              # the native turn the director withholds (scene frame 359)
    caption(e, f0 + 6, turn - 4, "FREE: the badnik runs its own ROM AI")
    caption(e, turn, f1, "PUPPET: now it waits for you")
    f0, f1 = seg(2, TOUR, 1060)
    label(e, f0, f1, "FREE  ·  PUPPET  ·  POSE  KEYS")
    f0, f1 = seg(2, TOUR, 1380)
    label(e, f0, f1, "CLEAR BADNIKS  ·  REMOVE OBJECTS")
    seg(3, ROUTE, 410, cap="Ask for a destination")
    seg(5, ROUTE, 524, cap="Walking can't make the loop. It says why.")
    seg(4, ROUTE, 1245, cap="Run. Hard stop. Face left.")
    f0, f1 = seg(9, ROUTE, 1393, cam=cam_move((960, 540, 1.0), (*preview_cam(HUD_PREVIEW, 2.0)[:2], 2.0),
                                                  ease=lambda u: smooth(clamp(u * 2.2))))
    caption(e, f0 + 40, f1, "Planned and checked under real physics")
    # playback: zoomed preview with the line and the white actual-position cross, then the peel
    p0, p1 = at(k), at(k + 9)
    src0 = ROUTE_PLAY + 60
    wipe = at(k + 5)
    e.S(Custom(p0, p1, peel(ROUTE, src0, LOOP + 60, wipe - p0, 26, HUD_PREVIEW)))
    caption(e, p0 + 6, wipe - 2, "Then Sonic runs it")
    label(e, wipe + 4, p1, "FILM", x=60)
    e.stem(A / "film-sfx.wav", LOOP + 60, p0, p1 - p0, gain=1.0)
    k += 9
    f0, f1 = seg(2, TOUR, 1590)
    label(e, f0, at(k + 2), "CAMERA KEYS")
    seg(2, TOUR, 1716, cam=cam_static(*preview_cam(HUD_PREVIEW, 2.0)))
    f0, f1 = seg(2, TOUR, 2040)
    label(e, f0, at(k + 3), "DIALOGUE  ·  TYPING  ·  VOICES")
    f0, f1 = seg(3, TOUR, 2282, cam=cam_static(*preview_cam(HUD_PREVIEW, 2.0)))
    e.stem(A / "film-sfx.wav", 1140 + (2282 - 2258), f0, f1 - f0, gain=1.0)
    # screenplay round trip: the real exported JSON beside the export form
    s0, s1 = at(k), at(k + 5)
    e.S(Custom(s0, s1, screenplay_panel))
    js = json.loads((ROOT / "captures" / "editor-tour2" / "scene" / "day-off.screenplay.json").read_text())
    loop_shot = js["shots"][1]
    mv = [a for a in loop_shot["actions"]["sonic"] if a["kind"] == "MOVE_TO"][0]
    lines = [("c", "// day-off.screenplay.json  (exported by the editor)"),
             ("n", '"kind" : "MOVE_TO",  "frame" : %d,' % mv["frame"]),
             ("n", '"x" : %.1f,  "y" : %.1f,' % (mv["x"], mv["y"])),
             ("n", '"motion" : {'),
             ("n", '  "startingAction" : "%s",' % mv["motion"]["startingAction"]),
             ("n", '  "travelSpeed" : "%s",' % mv["motion"]["travelSpeed"]),
             ("n", '  "endingAction" : "%s",' % mv["motion"]["endingAction"]),
             ("n", '  "endingFacing" : "%s" }' % mv["motion"]["endingFacing"])]
    e.O(Typed(s0 + 4, s1, lines, 170, 170, w=1000, h=480, cps=60, title="screenplay v6"))
    caption(e, s0 + 10, s1, "Edit it as a screenplay. It round-trips.")
    k += 5
    # both editors, same scene frame (route playback in each)
    q0, q1 = at(k), at(k + 6)
    e.S(Custom(q0, q1, two_editors(ROUTE_PLAY + 120, DROUTE_PLAY + 120)))
    caption(e, q0 + 14, q1, "One scene file. Both editors.", y=120)
    k += 6
    f0, f1 = seg(2, TOUR, 2690)
    label(e, f0, at(k + 2), "EXPORT FILM")
    seg(2, TOUR, 2950)
    t = at(k)
    # ---------------------------------------------------------------- E. epilogue (the film's own ending)
    e0 = t
    e.S(Game(e0, e0 + (FILM_END - EPI), FILM, src=EPI, trans="xfade", tdur=20))
    e.bed(A / "film.wav", e0, 1.0, src_seconds=EPI / 60, length=(FILM_END - EPI) / 60, fade_in=0.3, fade_out=0.02)
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
