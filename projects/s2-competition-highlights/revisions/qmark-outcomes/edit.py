#!/usr/bin/env python3
"""S2 two-player "?" monitor outcomes. Rebuild: python3 prep.py; python3 edit.py (soundtrack);
python3 <OpenGGF>/tools/media/promo_kit.py render edit.py; ./finish.sh.

Brief:
  audience: Farrell (visual check) and James; evidence reel, not a promo.
  form/evidence: eight cold frozen-route replays, one per "?" content, each beside the same
    route on native Sonic 2 REV01 in BizHawk 2.11 (ENGINE + BIZHAWK qualified, no native lag).
  promise: every outcome of the 2P "?" box, activated and held so it can be checked by eye.
  layout: outcomes that only touch the breaker (Sonic) stack his half, engine over native at 2x,
    with the text in a right-hand column; Tails 1-up and Teleport use engine | native panels
    (whole 2P picture, square-pixel 640x448 -> 900x630); a header
    names the item and the frame-counter arithmetic that chose it; a yellow outline flags the
    break frame; one line says what to look for.
  sound: the engine's own mix of each take, short crossfades; no bed or stingers.
  type: Fira Sans Compressed Heavy with navy stroke (editorial voice, distinct from the HUD).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, "/home/farrell/code/projects/OpenGGF/.worktrees/s2-competition-parity/tools/media")
sys.path.insert(0, str(ROOT))
from promo_kit import *  # noqa: E402,F403
from shots import LEAD, HOLD, OUTCOMES  # noqa: E402

EDIT = dict(bpm=120, first=0.0, fps=60, size=(1920, 1080), out=str(ROOT / "out/s2-qmark-outcomes.mp4"),
            work=str(ROOT / "build"))
INTRO, SHOT, END = 270, LEAD + HOLD, 300
PX = ((40, "OPENGGF", YELLOW), (980, "SONIC 2 REV01 · BIZHAWK", SKY))


def clip(name):
    return Frames(ROOT / "frames" / name)


def panels(e, f, eng, nat, flag):
    c = stripes(e, f)
    for (x, label, colour), img in zip(PX, (eng, nat)):
        if flag > 0:
            c[292:938, x - 8:x + 908] = np.array(YELLOW, np.float32) * flag + c[292:938, x - 8:x + 908] * (1 - flag)
        c[300:930, x:x + 900] = arr(resample(img, 0, 0, 640, 448, 900, 630))
        paste(c, chip(label, 36, NAVY, colour), x, 236)
    return c


def stacked(e, f, eng, nat, flag):
    """The breaker's (top) half: engine above native, 2x (1280x448 each), text column on the right."""
    c = stripes(e, f)
    # Rows 0-215 only: the split seam is at progressive line 216 (known-discrepancies U-3).
    for y, img in ((72, eng), (588, nat)):
        if flag > 0:
            c[y - 8:y + 440, 32:1328] = np.array(YELLOW, np.float32) * flag + c[y - 8:y + 440, 32:1328] * (1 - flag)
        c[y:y + 432, 40:1320] = arr(resample(img, 0, 0, 640, 216, 1280, 432))
    return c


def line(s, size=110, colour=WHITE):
    return text(s, "title", size, colour, stroke=8, sfill=NAVY, shadow=9)


def build(e):
    # intro: the rule, over the first outcome's opening frames, dimmed
    first = clip(OUTCOMES[0][0])
    e.S(Custom(0, INTRO, lambda f, s, ed: panels(ed, f, first.frame(0), clip(OUTCOMES[0][0] + "-native").frame(0), 0)
               * 0.35))
    e.O(Txt(12, INTRO, line('THE TWO-PLAYER "?" BOX', 150), e.W / 2, 330, enter="pop", centre=True))
    e.O(Txt(60, INTRO, line("PICKS ONE OF EIGHT ITEMS FROM THE FRAME COUNTER", 72, YELLOW), e.W / 2, 520,
            enter="up", centre=True))
    e.O(Txt(110, INTRO, text("item = (Level_frame_counter & 7) + 1   ·   Obj2E_Init, s2.asm:25755-25776",
                             "mono_b", 40, WHITE, stroke=3, sfill=NAVY), e.W / 2, 650, enter="fade", centre=True))
    t = INTRO
    for content, n, title, lfc, brk, note, layout in OUTCOMES:
        eng, nat = clip(content), clip(f"{content}-native")
        draw = stacked if layout == "half" else panels

        def fn(f, s, ed, eng=eng, nat=nat, t=t, draw=draw):
            i = f - t
            flag = max(0.0, 1 - abs(i - LEAD) / 10)
            return draw(ed, f, eng.frame(i), nat.frame(i), flag)

        e.S(Custom(t, t + SHOT, fn, trans="wipe", tdur=14))
        rule = chip(f"counter {lfc}  →  ({lfc} & 7) + 1 = {n}", 34 if layout == "half" else 40, NAVY, YELLOW)
        if layout == "half":
            e.O(Txt(t + 10, t + SHOT, line(str(n), 150, YELLOW), 1370, 40, enter="right", leave="left"))
            e.O(Txt(t + 14, t + SHOT, line(title, 84), 1370, 220, enter="right", leave="left"))
            e.O(Txt(t + 22, t + SHOT, rule, 1370, 340, enter="right", leave="left"))
            e.O(Txt(t + 30, t + SHOT, chip("▲ OPENGGF", 36, NAVY, YELLOW), 1370, 440, enter="right", leave="left"))
            e.O(Txt(t + 30, t + SHOT, chip("▼ SONIC 2 REV01 · BIZHAWK", 36, NAVY, SKY), 1370, 580, enter="right",
                    leave="left"))
            for k, part in enumerate(note.split("|")):
                e.O(Txt(t + LEAD + 4 * k, t + SHOT, text(part, "sub", 48, WHITE, stroke=4, sfill=NAVY, shadow=5),
                        1370, 760 + 70 * k, enter="up"))
        else:
            e.O(Txt(t + 10, t + SHOT, line(f"{n} · {title}", 120), 60, 52, enter="right", leave="left"))
            e.O(Txt(t + 22, t + SHOT, rule, 1880 - rule.shape[1], 70, enter="right", leave="left"))
            e.O(Txt(t + LEAD, t + SHOT, text(note, "sub", 54, WHITE, stroke=4, sfill=NAVY, shadow=5), e.W / 2, 1000,
                    enter="up", centre=True))
        t += SHOT
    last = clip(OUTCOMES[-1][0])

    def card(f, s, ed):
        return blurred(last.frame(len(last) - 1), ed, dim=0.35)

    e.S(Custom(t, t + END, card, trans="xfade", tdur=24))
    e.O(Txt(t + 20, t + END, line("ALL EIGHT, FRAME FOR FRAME.", 130), e.W / 2, 400, enter="pop", centre=True))
    e.O(Txt(t + 60, t + END, text("Each outcome is a frozen route checked cold in BizHawk 2.11 (OpenGGF PR #273)",
                                  "sub", 50, YELLOW, stroke=4, sfill=NAVY, shadow=5), e.W / 2, 560, enter="up",
            centre=True))
    e.O(Txt(t + 90, t + END, text("Fan-made and free. Not affiliated with SEGA. Requires your own ROM.", "body", 34,
                                  WHITE, stroke=3, sfill=NAVY), e.W / 2, 940, enter="fade", centre=True))
    e.O(Fade(t + END - 40, t + END))
    e.bed(str(ROOT / "build/soundtrack.wav"), 0, 1.0)
    return t + END


def soundtrack():
    """Engine audio of each take (its break-LEAD row onward), 0.15 s crossfades; the first take's
    EHZ music under the intro and the last take's continuation under the end card, faded."""
    spf, xf = SR // 60, SR * 15 // 100
    total = INTRO + SHOT * len(OUTCOMES) + END
    out = np.zeros((total * spf + SR, 2), np.float32)

    def place(a, at, fade_tail=False):
        a = a.copy()
        r = np.linspace(0, 1, xf)[:, None]
        a[:xf] *= r
        a[-xf:] *= r[::-1]
        if fade_tail:
            a *= np.linspace(1, 0, len(a))[:, None]
        at = max(0, at - xf // 2)
        out[at:at + len(a)] += a

    first = read_wav(ROOT / "audio" / f"{OUTCOMES[0][0]}.wav")
    s0 = (OUTCOMES[0][4] - LEAD - INTRO) * spf
    place(first[s0 - xf // 2:s0 + INTRO * spf + xf // 2], 0)
    t = INTRO
    for content, n, title, lfc, brk, note, layout in OUTCOMES:
        a = read_wav(ROOT / "audio" / f"{content}.wav")
        s = (brk - LEAD) * spf
        place(a[s - xf // 2:s + SHOT * spf + xf // 2], t * spf)
        t += SHOT
    s = (OUTCOMES[-1][4] - LEAD + SHOT) * spf
    place(a[s:s + END * spf], t * spf, fade_tail=True)
    (ROOT / "build").mkdir(exist_ok=True)
    write_wav(ROOT / "build/soundtrack.wav", out[:total * spf])
    print("soundtrack", total / 60, "s")


if __name__ == "__main__":
    soundtrack()
