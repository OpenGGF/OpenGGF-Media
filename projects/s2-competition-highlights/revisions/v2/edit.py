#!/usr/bin/env python3
"""S2 Competition highlights for James, v2 (both players racing at once). Rebuild: python3 prep.py; python3 edit.py (soundtrack);
python3 tools/media/promo_kit.py render edit.py.

Creative brief:
  audience: James, who wrote the original S2 Competition branch that was lost months ago.
  form/evidence: gameplay highlights from cold frozen-route replays on the PR #273 head, with
    engine audio; one labelled engine-vs-native BizHawk split for parity.
  promise: "Remember that competition branch I deleted? So I rebuilt it."
  hero moment: both players through the act-1 loops at once, and the 1-1 tie fading to white
    into the two-player special stage.
  sound: the engine's own mix of each take (title, EHZ 2P, results, CNZ 2P, special stage),
    short crossfades at cuts; no editorial bed or stingers (the game's music is the story).
  palette: S2 title-card blue/red/yellow; navy stripes in the gutters.
  title face: Fira Sans Compressed Heavy, white with navy stroke and hard shadow (editorial voice,
    distinct from the game's HUD); the ROM's own title card carries the zone names.
  end card: apology line, what it is, PR number, fan-made disclaimer.
  layout: the 2P picture stays whole at full height (640x448 square-pixel, 1543x1080); gutters
    carry player labels. v2 (user: "both players playing at once rather than alternating") uses
    the simultaneous route, so every race shot shows both halves moving.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/s2-competition-parity/tools/media")
sys.path.insert(0, str(ROOT))
from promo_kit import *  # noqa: E402,F403
from shots import CLIPS, SHOTS  # noqa: E402

EDIT = dict(bpm=120, first=0.0, fps=60, size=(1920, 1080), out=str(ROOT / "out/s2-competition-highlights.mp4"),
            work=str(ROOT / "build"))

END_CARD = 390
WIPES = {"title": 14, "cnz-card": 16, "act2-race": 16}
GW, GH, GX = 1543, 1080, (1920 - 1543) // 2


def timeline():
    t, out = 0, []
    for name, clip, row, n, layout in SHOTS:
        out.append((name, clip, row, n, layout, t))
        t += n
    return out, t


def clip(name):
    return Frames(ROOT / "frames" / name)


def full(e, f, img, labels=True):
    c = stripes(e, f)
    c[:, GX:GX + GW] = arr(resample(img, 0, 0, 640, 448, GW, GH))
    if labels:
        paste(c, chip("SONIC", 34, NAVY, SKY), 18, 250)
        paste(c, chip("TAILS", 34, NAVY, YELLOW), 18, 790)
    return c


def half(e, f, img, which, label, colour):
    c = stripes(e, f)
    y0 = 0 if which == "top" else 224
    c[204:876] = arr(resample(img, 0, y0, 640, 224, 1920, 672))
    paste(c, chip(label, 40, NAVY, colour), 60, 132 if which == "top" else 892)
    return c


def parity(e, f, eng, nat):
    c = stripes(e, f)
    for x, img, label, colour in ((40, eng, "OPENGGF", YELLOW), (980, nat, "SONIC 2 REV01 · BIZHAWK", SKY)):
        c[300:930, x:x + 900] = arr(resample(img, 0, 0, 640, 448, 900, 630))
        paste(c, chip(label, 40, NAVY, colour), x, 226)
    return c


def build(e):
    shots, total = timeline()
    for name, key, row, n, layout, t in shots:
        if layout == "parity":
            eng, nat = clip(name), clip(f"{name}-native")
            fn = (lambda eng, nat, t: lambda f, s, ed: parity(ed, f, eng.frame(f - t), nat.frame(f - t)))(eng, nat, t)
        elif layout in ("top", "bottom"):
            src = clip(name)
            label, colour = ("PLAYER 1 · SONIC", SKY) if layout == "top" else ("PLAYER 2 · TAILS", YELLOW)
            fn = (lambda src, t, w, l, col: lambda f, s, ed: half(ed, f, src.frame(f - t), w, l, col))(
                src, t, layout, label, colour)
        else:
            src = clip(name)
            fn = (lambda src, t, lab: lambda f, s, ed: full(ed, f, src.frame(f - t), lab))(src, t, layout == "full")
        e.S(Custom(t, t + n, fn, trans="wipe" if name in WIPES else None, tdur=WIPES.get(name, 0)))
    at = {name: t for name, *_, t in shots}

    def line(s, size=110, colour=WHITE):
        return text(s, "title", size, colour, stroke=8, sfill=NAVY, shadow=9)

    # cold open: both players loop at once; two lines on shades at the top and bottom
    t = at["open-loops"]
    e.O(Shade(t + 14, t + 300, "top"))
    e.O(Shade(t + 90, t + 300, "bottom"))
    e.O(Txt(t + 20, t + 292, line("REMEMBER THAT COMPETITION BRANCH", 100), e.W / 2, 80, enter="pop", centre=True,
            dur=12))
    e.O(Txt(t + 95, t + 292, line("I ACCIDENTALLY DELETED?", 100, YELLOW), e.W / 2, 1000, enter="pop", centre=True,
            dur=12))
    # title drop on the real title screen
    t = at["title"]
    e.O(Flash(t, 18))
    e.O(Shade(t, t + 240, "bottom"))
    e.O(Txt(t + 6, t + 236, line("SO I REBUILT IT.", 190), e.W / 2, 900, enter="slam", centre=True))
    # signpost callout as it spins with the two-player face art
    t = at["finish1"] + 80
    sign = chip("2P SIGNPOST ART", 40, NAVY, YELLOW)
    e.O(Txt(t, t + 170, sign, 1900 - sign.shape[1], 380, enter="right", leave="right"))
    # parity screen
    t = at["parity"]
    e.O(Txt(t + 12, t + 440, line("SAME INPUTS, SAME FRAMES", 120), e.W / 2, 112, enter="down", centre=True, out_dur=8))
    e.O(Txt(t + 70, t + 440, text("Both racing at once: positions match native Sonic 2 on every frame here",
                                   "sub", 50, WHITE, stroke=4, sfill=NAVY, shadow=5), e.W / 2, 1000, enter="up",
            centre=True))
    # the tie
    t = at["results2"]
    e.O(Txt(t + 40, t + 236, line("ONE ACT EACH...", 110), e.W / 2, 70, enter="pop", centre=True))
    t = at["ss-entry"]
    e.O(Txt(t + 26, t + 90, text("...SO THE SPECIAL STAGE DECIDES.", "title", 84, NAVY, shadow=8,
                                  scol=(120, 140, 200, 160)), e.W / 2, e.H / 2, enter="pop", centre=True))
    t = at["ss-start"] + 260
    e.O(Txt(t, t + 200, chip("NOW WITH THE ROM'S SLOWDOWN", 40, NAVY, SKY), e.W / 2, 520, enter="pop", centre=True))
    # end card over the last special-stage frame
    last = clip("ss-start")
    t = total

    def card(f, s, ed):
        c = blurred(last.frame(len(last) - 1), ed, dim=0.35)
        return c

    e.S(Custom(t, t + END_CARD, card, trans="xfade", tdur=24))
    e.O(Txt(t + 20, t + END_CARD, line("SORRY ABOUT THE BRANCH, JAMES.", 120), e.W / 2, 400, enter="pop", centre=True))
    e.O(Txt(t + 60, t + END_CARD, text("Sonic 2 Competition, rebuilt in OpenGGF  ·  PR #273", "sub", 60, YELLOW,
                                        stroke=4, sfill=NAVY, shadow=5), e.W / 2, 560, enter="up", centre=True))
    e.O(Txt(t + 90, t + END_CARD, text("Fan-made and free. Not affiliated with SEGA. Requires your own ROM.", "body",
                                        34, WHITE, stroke=3, sfill=NAVY), e.W / 2, 940, enter="fade", centre=True))
    e.O(Fade(t + END_CARD - 40, t + END_CARD))
    e.bed(str(ROOT / "build/soundtrack.wav"), 0, 1.0)
    return t + END_CARD


def soundtrack():
    """Engine audio of each take in order, 0.15 s crossfades at cuts; the 2P results theme under the end card."""
    shots, total = timeline()
    spf, xf = SR // 60, SR * 15 // 100
    out = np.zeros(((total + END_CARD) * spf + SR, 2), np.float32)
    cache = {}
    for name, key, row, n, layout, t in shots:
        if key not in cache:
            cache[key] = read_wav(ROOT / "audio" / f"{CLIPS[key]}.wav")
        a = cache[key][max(0, row * spf - xf // 2):(row + n) * spf + xf // 2].copy()
        ramp = np.linspace(0, 1, xf)[:, None]
        a[:xf] *= ramp
        a[-xf:] *= ramp[::-1]
        at = max(0, t * spf - xf // 2)
        out[at:at + len(a)] += a
    end = total * spf
    # The 2P results theme under the end card (the reel's capture ends inside the special stage).
    tail = cache["T"][4259 * spf:(4259 + END_CARD) * spf].copy()
    tail[:xf] *= np.linspace(0, 1, xf)[:, None]
    tail[-SR:] *= np.linspace(1, 0, SR)[:, None]
    out[end:end + len(tail)] += tail
    (ROOT / "build").mkdir(exist_ok=True)
    write_wav(ROOT / "build/soundtrack.wav", out[:(total + END_CARD) * spf])
    print("soundtrack", (total + END_CARD) / 60, "s")


if __name__ == "__main__":
    soundtrack()
