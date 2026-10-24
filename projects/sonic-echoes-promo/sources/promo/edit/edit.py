#!/usr/bin/env python3
"""Sonic Echoes promo (2026-10-24).
Rebuild: python3 <OpenGGF>/tools/media/promo_kit.py render edit/edit.py   (fonts: promo_kit.py fonts)

Audience: Sonic fans and OpenGGF followers who have never seen the mod.
Form/evidence: gameplay showcase; every shot is a display-free GameplayCaptureTool take of the real
  mod (ROM physics, real objects) driven by the rooms' authored reference inputs; Echo presses are
  scheduled at the authored loop frames (= pressing E). One labelled half-speed moment.
Promise: "Run it. Loop it. Team up with yourself." -- every attempt comes back as a physical echo.
Proof per claim: the loop (1-1 in one take: attempt -> rewind flash -> the cyan echo holds the door);
  echoes replay inputs exactly (two loops stacked, measured 0 px drift); echoes are real (native HTZ
  seesaw launches, CPZ spring, an echo popping a Buzzer); Paradox (3-1: the live run opens a gate the
  recording was blocked by; the echo runs on, measured drift 0 -> 46 px -> fracture); progress (hub
  tour on an honestly earned 33/36 save, landing on the unplayed finale); climax.
Relationship named once: "SAME BUTTONS. SAME SONIC." then its inverse "SAME BUTTONS. NEW WORLD."
Hero moment: 3-4 The Last Loop's final loop -- four coloured echoes hold three plates and clear the
  Spiny while the live Sonic runs through; fragment opens the film.
Sound: one bed, Sonic 2 Chemical Plant (SMPS render, --paced), 139.441 BPM, first beat 0.211 s; the
  song loops every 128 beats, and the finale starts on b128 where the music itself loops. ROM SFX only
  on their real events (the mod's rewind $BC, Paradox $C6, star pops $CE/$A1, springs $CC, badnik $C1,
  hub blips $CD / confirm $A1) plus ring pops alternating $B5/$CE on graphics.
Palette: the mod's slot colours (cyan 60E8FF, magenta FF70D0, gold FFD030, lime A0F060), its HUD
  navy 0A1535, S2 title-card blue/yellow/red for chapter headers.
Title face: the mod's own 5x7 face (EchoUi.GLYPHS) with its navy drop and an echo-contour trail in
  slot colours; editorial lines in Fira Sans Compressed Heavy Italic with navy stroke + hard shadow.
End card: logo, one line, URL, status, disclaimer; over a blurred hero frame.
"""
import sys
from functools import lru_cache

sys.path.insert(0, "/home/james/IdeaProjects/OpenGGF/tools/media")
sys.path.insert(0, "/home/james/tmp/sonic-echoes-promo/edit")
from promo_kit import *  # noqa: F401,F403
from PIL import Image, ImageDraw
import echokit as K
from echokit import Card, Logo, SLOT, sfx, events, first_event, session, CAPS
import echofont

TASK = "/home/james/tmp/sonic-echoes-promo"
EDIT = dict(bpm=139.441, first=0.211, fps=60, size=(1920, 1080), out=f"{TASK}/out/sonic-echoes-promo.mp4",
            work=f"{TASK}/edit/build/render")

NAVY = (10, 21, 53)
INK = K.INK
CYAN, MAGENTA, GOLD, LIME = SLOT[0], SLOT[1], SLOT[2], SLOT[3]

# Mod HUD extents in native rows (measured): top panel to y=45, first-loop control strip 182-217,
# timeline from 204. A header crop keeps rows 48..179 so all three are wholly out, never sliced.
NO_HUD = dict(cy=113.5, z=1.7)


def clip(shot):
    return Frames(CAPS / shot / "frames")


def line(s, size=86, colour=WHITE):
    return text(s, "title_it", size, colour, stroke=6, sfill=INK, shadow=7, scol=(0, 0, 30, 190))


def view_rect(cx, cy, z, ow, oh, iw=400, ih=224):
    cx = iw / 2 if cx is None else cx
    cy = ih / 2 if cy is None else cy
    vh = ih / z
    vw = vh * ow / oh
    if vw > iw:
        vw = iw / z
        vh = vw * oh / ow
    return clamp(cx - vw / 2, 0, iw - vw), clamp(cy - vh / 2, 0, ih - vh), vw, vh


def to_out(px, py, cam, ow=1920, oh=1080, ox=0, oy=0):
    x0, y0, vw, vh = view_rect(*cam, ow, oh)
    return ox + (px - x0) * ow / vw, oy + (py - y0) * oh / vh


def framecam(f0, f1, fn):
    """A Game camera given per output frame instead of shot progress."""
    return lambda u: fn(f0 + u * (f1 - f0))


def header_cam(f0, f1, hdr_end, cx=None):
    """HUD cropped out while the chapter card is up, then a hard cut to the full frame."""
    return framecam(f0, f1, lambda f: (cx, NO_HUD["cy"], NO_HUD["z"]) if f < hdr_end else (None, None, 1.0))


def sync(e, shot, capf, src0, out0):
    """Output frame of capture frame capf in a shot that starts at out0 showing capture src0."""
    return out0 + (capf - src0)


def build(e):
    b = e.bf
    ring = K.Rings()
    e.bed(f"{TASK}/music/s2-music-8c-paced.wav", 0, 0.75, length=b(172) / 60 + 0.2, fade_out=1.6)

    hero, chain, seesaw = clip("b5-last-loop"), clip("a1-chain"), clip("b1-double-bounce")
    spring, escort, para, hub = clip("b3-spring-relay"), clip("a3-escort"), clip("b4-paradox"), clip("a4-hub-tour")

    def at(shot, capf, out0, src0):
        return out0 + capf - src0

    # ------------------------------------------------ A. cold open (b0-b16)
    # A1: the hero fragment -- four echoes at work, the fourth popping the Spiny on b3.
    kill = first_event("b5-last-loop", "badnik_kill:echo3")
    a1s = kill - b(3)
    e.S(Game(0, b(6), hero, src=a1s))
    e.punches.append((b(3), 0.07))
    e.X(b(3), sfx("c1"), 1.0)
    # A2: the loop itself -- 1-1's first attempt, the mod's rewind flash on b8, the echo appears.
    commit = first_event("a1-chain", "commit")
    a2s = commit - (b(8) - b(6))
    e.S(Game(b(6), b(13), chain, src=a2s))
    e.X(b(8), sfx("bc"), 1.0)
    e.punches.append((b(8), 0.05))
    for word, t0, t1, size in [("RUN IT.", 6.25, 8, 130), ("LOOP IT.", 8, 10, 130),
                               ("TEAM UP WITH YOURSELF.", 10, 13, 108)]:
        e.O(Txt(b(t0), b(t1) - 3, line(word, size), e.W / 2, 790, enter="pop", leave="fade", centre=True,
                dur=9, out_dur=6))
    # A3: a native seesaw launch lands on b15, into the title drop.
    launch = events("b1-double-bounce", "seesaw_launch:")[-2]
    e.S(Game(b(13), b(16), seesaw, src=launch - (b(15) - b(13))))
    e.X(b(15), sfx("cc"), 0.9)
    e.punches.append((b(15), 0.08))

    # ------------------------------------------------ B. title drop (b16-b32)
    # Over the third loop of the finale (three echoes running), dimmed, slamming out.
    l3 = [f for f in events("b5-last-loop", "restore")][1]
    e.S(Game(b(16), b(24), hero, src=l3 + 20, cam=cam_slam(1.35, 26, b(24) - b(16)), dim=0.5))
    e.O(Flash(b(16), 20))
    e.X(b(16), sfx("bc"), 1.0)
    logo = Logo(b(16), b(24) - 2, e.W / 2, 600, scale=20, step=int(round(b(17) - b(16))), trail=3, kicker_scale=10)
    e.O(logo)
    for k in range(1, 4):  # each echo contour fans out on a beat
        e.X(b(16) + 10 + (k - 1) * int(round(b(17) - b(16))), ring(), 0.8)
    e.O(Txt(b(20), b(24) - 4, text("A TIME-LOOP PUZZLE MOD FOR SONIC 2", "sub", 50, WHITE, stroke=4, sfill=INK,
                                     shadow=5), e.W / 2, 880, enter="up", leave="fade", centre=True))
    # B2: the stock title with the mod's ECHOES wordmark, Start, the Echo Engine hub, confirm on b31.
    confirm = first_event("a1-chain", "hub_confirm")
    b2s = confirm - (b(31) - b(24))
    e.S(Game(b(24), b(32), chain, src=b2s, trans="push", tdur=12, tdir="left"))
    e.X(b(31), sfx("a1"), 0.9)

    # ------------------------------------------------ C. the loop (b32-b64)
    # C1: 1-1 in one take from the room's first playable frames to its stars.
    ready = [f for f, r in sorted(session("a1-chain").items()) if confirm < f < commit and r["phase"] == "READY"]
    c1s = ready[-1] - 6 if ready else confirm + 140
    c1s = max(c1s, commit - 150)
    e.S(Game(b(32), b(48), chain, src=c1s, cam=header_cam(b(32), b(48), b(38)), trans="wipe", tdur=16))
    e.O(Card(b(32) + 4, b(38), "THE LOOP", "WORLD 1 · EMERALD HILL"))
    e.X(at("a1", commit, b(32), c1s), sfx("bc"), 1.0)
    for k, sf in enumerate(f for f in events("a1-chain", "star:") if f < 1600):
        e.X(at("a1", sf, b(32), c1s), sfx("ringc"), 1.0)
    # C2: SAME BUTTONS. SAME SONIC. -- 1-4's second loop (the live jump that pops the Buzzer) beside
    # its third loop, where the magenta echo replays it: the same jump, the same pop, 0 px apart.
    rows = session("a3-escort")
    kill_live = first_event("a3-escort", "badnik_kill:live")
    L = rows[kill_live]["loop"]
    M = str(int(L) + 1)
    loopL = [f for f, r in sorted(rows.items()) if r["loop"] == L and r["phase"] == "PLAYING"]
    loopM = [f for f, r in sorted(rows.items()) if r["loop"] == M and r["phase"] == "PLAYING"]
    a0, a1 = loopL[0], loopM[0]
    kill_lf = int(rows[kill_live]["loopFrame"])
    K0 = kill_lf - int(round(b(51) - b(48)))       # both pops land on b51

    @lru_cache(maxsize=None)
    def subj(capf, who):
        p = K.screen_pos("a3-escort", capf, who)
        return p if p else (200, 110)

    def smooth_track(capf, who, n=9):
        pts = [subj(max(0, capf + d), who) for d in range(-n // 2, n // 2 + 1)]
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)

    PW = 954  # two panes and a 12 px divider

    def pane(img, sx, ed):
        vh = 131.0                           # native rows 48..179: no HUD, no control strip
        vw = vh * PW / ed.H
        x0 = clamp(sx - vw / 2, 0, 400 - vw)
        return arr(resample(img, x0, 48, vw, vh, PW, ed.H))

    def same_split(f, s, ed):
        c = np.zeros((ed.H, ed.W, 3), np.float32) + np.array(NAVY, np.float32)
        lf = f - s.f0
        k = clamp(lf + K0, 0, min(len(loopL), len(loopM)) - 1)
        top_f, bot_f = a0 + int(k), a1 + int(k)
        sx0, _ = smooth_track(top_f, "live")
        sx1, _ = smooth_track(bot_f, "1")
        c[:, :PW] = pane(escort.frame(top_f), sx0, ed)
        right = pane(escort.frame(bot_f), sx1, ed)
        u = ease_out(lf / 16)                # the echo's pane drops in on the beat
        dy = int(round(-(1 - u) * ed.H))
        if dy == 0:
            c[:, PW + 12:] = right
        else:
            c[:ed.H + dy, PW + 12:] = right[-dy:]
        c[:, PW:PW + 12] = np.array(K.CARD_YELLOW, np.float32)
        for x, label, colour in ((40, f"LOOP {int(L) + 1} · YOU", WHITE), (PW + 52, f"LOOP {int(M) + 1} · ECHO 2", MAGENTA)):
            pill = chip(label, 58, INK, colour)
            paste(c, pill, x, ed.H - pill.shape[0] - 48, clamp((lf - 6) / 8))
        r0, r1 = rows[top_f], rows[bot_f]
        if r1["e1x"]:
            d = abs(int(r0["liveX"]) - int(r1["e1x"])) + abs(int(r0["liveY"]) - int(r1["e1y"]))
            tag = chip(f"DRIFT {d} PX", 64, INK, CYAN if d == 0 else (255, 90, 90))
            paste(c, tag, ed.W / 2 - tag.shape[1] / 2, 560, clamp((lf - 16) / 8))
        return c

    e.S(Custom(b(48), b(56), same_split, trans="push", tdur=12, tdir="left"))
    e.O(Txt(b(48) + 10, b(56) - 2, line("SAME BUTTONS. SAME SONIC.", 100), e.W / 2, 150, enter="down", leave="fade",
            centre=True))
    e.X(b(51), sfx("c1"), 1.0)               # the two pops are the same frame of the same jump
    e.punches.append((b(51), 0.08))

    # ------------------------------------------------ D. echoes are real (b56-b88)
    launches = events("b1-double-bounce", "seesaw_launch:")
    l_first, l_second = launches[-2], launches[-1]
    d1s = l_first - (b(60) - b(56))
    e.S(Game(b(56), b(70), seesaw, src=d1s, cam=header_cam(b(56), b(70), b(62)), trans="wipe", tdur=16))
    e.O(Card(b(56) + 4, b(62), "ECHOES ARE REAL", "WORLD 2 · HILL TOP · REAL SEESAWS"))
    for lf in (l_first, l_second):
        t = at("b1", lf, b(56), d1s)
        if t < b(70):
            e.X(t, sfx("cc"), 0.9)
            e.punches.append((t, 0.07))
    sp = [f for f in events("b3-spring-relay", "spring:") if f > 1700][0]
    d2s = sp - (b(71) - b(70))
    e.S(Game(b(70), b(74), spring, src=d2s, trans="push", tdur=10, tdir="left"))
    e.X(b(71), sfx("cc"), 0.9)
    e.punches.append((b(71), 0.07))
    e.O(Txt(b(70) + 6, b(74) - 2, chip("SPRINGS", 60, INK, MAGENTA), 1460, 270, enter="pop", leave="fade"))
    # D3: Clockwork's final loop -- three echoes file through three timed latches, then the stars.
    cw_rows = session("b6-clockwork")
    latches = [f for f in events("b6-clockwork", "plate_on:") if f > 2400]
    cw_clear = [f for f in events("b6-clockwork", "clear") if f > 2400][0]
    d3s = cw_clear - (b(84) - b(74))
    clock = clip("b6-clockwork")
    e.S(Game(b(74), b(88), clock, src=d3s, trans="push", tdur=10, tdir="left"))
    e.O(Txt(b(74) + 6, b(80), chip("TIMED LATCHES", 60, INK, GOLD), 1300, 270, enter="pop", leave="fade"))
    for lt in latches[:3]:
        t = at("b6", lt, b(74), d3s)
        e.X(t, ring(), 0.8)
    for k, sf in enumerate(f for f in events("b6-clockwork", "star:") if f > cw_clear):
        t = at("b6", sf, b(74), d3s)
        if t < b(88):
            e.X(t, sfx("ringc"), 1.0)

    # ------------------------------------------------ E. paradox (b88-b120)
    frac = first_event("b4-paradox", "fracture:0")
    prow = session("b4-paradox")
    rec = {int(r["loopFrame"]): (int(r["liveX"]), int(r["liveY"])) for f, r in sorted(prow.items())
           if r["loop"] == "0" and r["phase"] == "PLAYING" and f < 430}
    SLOW0, SLOW1 = frac - 22, frac + 4          # the divergence, at half speed
    slow_out0 = b(97)
    e1s = SLOW0 - (slow_out0 - b(88))           # src at b88
    slow_len = (SLOW1 - SLOW0) * 2

    def p_src(f):
        if f < slow_out0:
            return e1s + (f - b(88))
        if f < slow_out0 + slow_len:
            return SLOW0 + (f - slow_out0) // 2
        return SLOW1 + (f - slow_out0 - slow_len)

    pend = b(102)                                # cut 1.5 s after the fracture

    def paradox(f, s, ed):
        capf = p_src(f)
        hdr = f < b(93)
        cam = (None, NO_HUD["cy"], NO_HUD["z"]) if hdr else (None, None, 1.0)
        c = arr(game_view(para.frame(capf), cam[0], cam[1], cam[2] * ed.punch(f), ed.W, ed.H))
        r = prow.get(capf)
        if r and r["loop"] == "1" and r["e0x"] and not hdr and capf <= frac + 40:
            k = int(r["loopFrame"])
            camx, camy = float(r["camX"]), float(r["camY"])
            if k in rec:
                rx, ry = rec[k][0] - camx, rec[k][1] - camy
                ex, ey = int(r["e0x"]) - camx, int(r["e0y"]) - camy
                d = ((rec[k][0] - int(r["e0x"])) ** 2 + (rec[k][1] - int(r["e0y"])) ** 2) ** 0.5
                if r["e0state"] == "fractured":
                    d = 48.0
                    ex = ex
                show = capf >= frac - 60
                if show:
                    a = clamp((capf - (frac - 60)) / 10)
                    ox, oy = to_out(rx, ry, cam)
                    L = Image.new("RGBA", (ed.W, ed.H), (0, 0, 0, 0))
                    dr = ImageDraw.Draw(L)
                    w, h = 15 * 4.82, 22 * 4.82
                    dr.rounded_rectangle((ox - w, oy - h, ox + w, oy + h), radius=18,
                                         outline=(255, 255, 255, int(230 * a)), width=6)
                    if r["e0state"] != "fractured":
                        ex2, ey2 = to_out(ex, ey, cam)
                        dr.line((ox, oy - h - 30, ex2, oy - h - 30), fill=CYAN + (int(255 * a),), width=8)
                    L = np.asarray(L, np.float32)
                    paste(c, L, 0, 0)
                    lab = chip("RECORDED", 40, INK, WHITE)
                    paste(c, lab, ox - lab.shape[1] / 2, oy + h + 16, a)
                    col = (255, 90, 90) if d >= 30 else WHITE
                    num = text(f"DRIFT {int(round(d))} PX" if d < 48 else "48 PX: PARADOX", "title_it", 66, col,
                               stroke=5, sfill=INK, shadow=6, scol=(0, 0, 30, 190))
                    paste(c, num, ox - num.shape[1] / 2 - 120, oy - h - 30 - num.shape[0] - 10, a)
        if slow_out0 <= f < slow_out0 + slow_len:
            tag = chip("½ SPEED", 40, INK, GOLD)
            paste(c, tag, ed.W - tag.shape[1] - 40, 250)
        return c

    e.S(Custom(b(88), pend, paradox, trans="wipe", tdur=16))
    e.O(Card(b(88) + 4, b(93), "PARADOX", "WORLD 3 · CHEMICAL PLANT"))
    frac_out = slow_out0 + (frac - SLOW0) * 2
    e.X(frac_out, sfx("c6"), 1.0)
    e.punches.append((frac_out, 0.09))
    e.O(Flash(frac_out, 10, 0.45))
    e.O(Txt(frac_out + 16, pend - 4, line("SAME BUTTONS. NEW WORLD.", 92), e.W / 2, 790, enter="up", leave="fade",
            centre=True))
    # E2: the fix -- re-record after Reset, wait for the runner, and the echo holds its path (measured
    # against the post-Reset recording, 0 px every frame) all the way to the clear.
    pclear = [f for f in events("b4-paradox", "clear") if f > 1500][0]
    reset_at = [f for f, r in sorted(prow.items()) if 600 < f < 906 and r["phase"] == "PLAYING"][0]
    rec2 = {int(r["loopFrame"]): (int(r["liveX"]), int(r["liveY"])) for f, r in sorted(prow.items())
            if reset_at <= f < 906 and r["phase"] == "PLAYING"}
    e2s = pclear - (b(116) - pend)
    e.S(Game(pend, b(120), para, src=e2s, trans="push", tdur=10, tdir="left"))
    for k, sf in enumerate(f for f in events("b4-paradox", "star:") if f > pclear):
        t = at("b4", sf, pend, e2s)
        if t < b(120):
            e.X(t, sfx("ringc"), 1.0)

    def held_path(c, f, o, ed):
        capf = e2s + (f - pend)
        r = prow.get(capf)
        if not r or capf >= pclear or not r["e0x"] or r["phase"] != "PLAYING":
            return
        k = int(r["loopFrame"])
        if k not in rec2:
            return
        d = abs(int(r["e0x"]) - rec2[k][0]) + abs(int(r["e0y"]) - rec2[k][1])
        p = K.screen_pos("b4-paradox", capf, "0")
        if not p or not (-10 < p[0] < 410):
            return
        x, y = to_out(p[0], p[1] - 34, (None, None, 1.0))
        pill = chip(f"ECHO 1 · DRIFT {d} PX", 46, INK, CYAN if d == 0 else (255, 90, 90))
        paste(c, pill, clamp(x - pill.shape[1] / 2, 12, ed.W - pill.shape[1] - 12), y - pill.shape[0],
              clamp((f - o.f0) / 8) * clamp((pclear - capf) / 8))

    e.O(Fn(pend + 12, b(120), held_path))

    # ------------------------------------------------ F. progress (b120-b128): onto the finale
    hc = first_event("a4-hub-tour", "hub_confirm")
    fs = hc - (b(128) - b(120))
    e.S(Game(b(120), b(128), hub, src=fs, trans="wipe", tdur=16))
    for mv in events("a4-hub-tour", "hub_move"):
        t = at("a4", mv, b(120), fs)
        if b(120) <= t < b(128):
            e.X(t, sfx("cd"), 0.9)
    last_move = events("a4-hub-tour", "hub_move")[-1]
    hl0 = at("a4", last_move, b(120), fs)

    def finale_ring(c, f, o, ed):  # gold pulse around the unplayed finale card once selected
        x0, y0 = to_out(207, 152, (None, None, 1.0))
        x1, y1 = to_out(387, 202, (None, None, 1.0))
        pulse = 0.5 + 0.5 * np.cos((f - o.f0) / 26 * 2 * np.pi)
        L = Image.new("RGBA", (ed.W, ed.H), (0, 0, 0, 0))
        ImageDraw.Draw(L).rounded_rectangle((x0 - 10, y0 - 10, x1 + 10, y1 + 10), radius=16,
                                            outline=GOLD + (int(150 + 105 * pulse),), width=10)
        paste(c, np.asarray(L, np.float32), 0, 0, clamp((f - o.f0) / 6))

    e.O(Fn(hl0, b(128), finale_ring))
    e.X(b(128), sfx("a1"), 0.9)

    # ------------------------------------------------ G. the last loop (b128-b156)
    restores = events("b5-last-loop", "restore")
    commits = events("b5-last-loop", "commit")
    hero_rows = session("b5-last-loop")
    hero_first = min(f for f, r in hero_rows.items() if r["loop"] == "0" and r["phase"] == "PLAYING")
    starts = [hero_first] + [r + 16 for r in restores[:3]]   # loop k's live run (camera settled)
    ends = commits[:4]

    def loops_grid(f, s, ed):
        c = stripes(ed, f, (8, 14, 36), (12, 22, 52))
        cw, ch, gap = 940, 526, 12
        left, top = (ed.W - 2 * cw - gap) / 2, (ed.H - 2 * ch - gap) / 2
        for i in range(4):
            t0 = b(131 + i)
            if f < t0:
                continue
            span = ends[i] - starts[i]
            capf = starts[i] + (f - t0) % span              # each loop repeats, as the room does
            img = hero.frame(capf)
            v = arr(resample(img, 0, 0, 400, 224, cw - 12, ch - 12))
            u = (f - t0) / 10
            sc = 0.86 + 0.14 * back(u, 2.0) if u < 1 else 1.0
            x, y = left + (i % 2) * (cw + gap), top + (i // 2) * (ch + gap)
            frame = np.zeros((ch, cw, 4), np.float32)
            frame[..., :3] = SLOT[i]
            frame[..., 3] = 255
            frame[6:-6, 6:-6, :3] = v
            if sc != 1.0:
                frame = scaled(frame, sc)
            paste(c, frame, x + (cw - frame.shape[1]) / 2, y + (ch - frame.shape[0]) / 2, clamp(u * 3))
            if u >= 0.5:
                pill = chip(f"LOOP {i + 1}", 44, INK, SLOT[i])
                paste(c, pill, x + cw / 2 - pill.shape[1] / 2, y + ch / 2 + 18, clamp((u - 0.5) * 3))
        return c

    e.S(Custom(b(128), b(142), loops_grid, trans="wipe", tdur=16))
    e.O(Card(b(128) + 4, b(131), "THE LAST LOOP", "FOUR LOOPS. FOUR ECHOES.", x=520, y=400, size=150, sub_size=52))
    for i in range(4):
        e.X(b(131 + i), ring(), 0.85)
    # G2: the final loop, full screen, through ROOM CLEAR. Each echo's job is labelled above it,
    # in its own colour, from the frame it starts that job while it is on screen.
    g2s = restores[3] + 14
    clear = first_event("b5-last-loop", "clear")
    e.S(Game(b(142), b(156), hero, src=g2s, trans="iris", tdur=18))
    e.X(b(142), sfx("c3"), 0.8)
    jobs = [("plate_on:cyan", 0, "HOLDS A PLATE"), ("plate_on:magenta", 1, "HOLDS A PLATE"),
            ("plate_on:gold", 2, "HOLDS A PLATE"), ("badnik_kill:echo3", 3, "POPS THE SPINY")]
    job_at = []
    for name, slot, label in jobs:
        jf = [f for f in events("b5-last-loop", name) if f > restores[3]][0]
        job_at.append((jf, slot, chip(f"ECHO {slot + 1}: {label}", 44, INK, SLOT[slot])))
        t = at("b5", jf, b(142), g2s)
        e.X(t, sfx("c1") if "kill" in name else ring(), 0.9)
        if "kill" in name:
            e.punches.append((t, 0.08))

    def job_tags(c, f, o, ed):
        capf = g2s + (f - b(142))
        if capf >= clear:
            return
        for jf, slot, pill in job_at:
            if not jf <= capf < jf + 80:       # each label lives 80 frames from the start of its job
                continue
            p = K.screen_pos("b5-last-loop", capf, str(slot))
            if not p or not (-10 < p[0] < 410):
                continue
            # neighbours alternate between two heights so adjacent echoes' labels never touch
            x, y = to_out(p[0], p[1] - 34 - (16 if slot % 2 else 0), (None, None, 1.0))
            a = clamp((capf - jf) / 8) * clamp((jf + 80 - capf) / 10) * clamp((clear - capf) / 8)
            paste(c, pill, clamp(x - pill.shape[1] / 2, 12, ed.W - pill.shape[1] - 12), y - pill.shape[0], a)

    e.O(Fn(b(142), b(156), job_tags))
    tclear = at("b5", clear, b(142), g2s)
    e.punches.append((tclear, 0.06))
    for k, sf in enumerate(f for f in events("b5-last-loop", "star:") if f > clear):
        e.X(at("b5", sf, b(142), g2s), sfx("ringc"), 1.0)

    # ------------------------------------------------ H. end card (b156-b172)
    end_src = clear + 140

    def end_card(f, s, ed):
        c = blurred(hero.frame(1095), ed, radius=4, dim=0.45)
        u = ease_out((f - s.f0) / 18)
        lg = logo_end
        paste(c, lg, ed.W / 2 - (lg.shape[1] - 2 * 3 * 15) / 2 - 2 * 3 * 15, 150 - (1 - u) * 50, clamp((f - s.f0) / 10))
        rows_ = [(line("TEAM UP WITH YOURSELF.", 84), 520, 8),
                 (text("github.com/OpenGGF/OpenGGF", "sub", 56, WHITE, stroke=4, sfill=INK, shadow=5), 650, 16),
                 (text("Example mod for Sonic 2 · OpenGGF 0.7 development line", "body_it", 38, (205, 215, 235),
                       stroke=3, sfill=INK, shadow=4), 745, 22),
                 (text("Fan-made and free. Not affiliated with SEGA. Requires your own ROM.", "body", 30,
                       (175, 185, 205), stroke=2, sfill=INK, shadow=3), 900, 28)]
        for im, y, d in rows_:
            paste(c, im, ed.W / 2 - im.shape[1] / 2, y, clamp((f - s.f0 - d) / 10))
        return c

    logo_end = echofont.word("ECHOES", echofont.WHITE, trail=3, scale=15)
    kick = echofont.word("SONIC", echofont.WHITE, scale=7)

    def end_kicker(c, f, o, ed):
        paste(c, kick, ed.W / 2 - kick.shape[1] / 2, 70, clamp((f - o.f0 - 4) / 10))

    e.S(Custom(b(156), b(172), end_card, trans="xfade", tdur=18))
    e.O(Fn(b(156), b(172), end_kicker))
    e.X(b(156), sfx("bc"), 0.7)
    e.O(Fade(b(172) - 54, b(172)))
    return b(172)
