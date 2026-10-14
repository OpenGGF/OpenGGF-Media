#!/usr/bin/env python3
"""Mutator Lab — complete gameplay showcase: reproducible edit recipe (task mutator-complete-showcase-20261010).

Sources: the seven accepted final takes of task e0603654 (read in place, never copied or modified) plus the
eleven new final takes under ../captures/final-*/capture. Each take is PNG per presented frame plus offline
48 kHz stereo PCM (audio.wav, exactly 800 stereo frames per presented frame). Every segment is an exact frame
range of one take; its audio is the same take's PCM samples [start*800, end*800) of the chosen panel. No
retiming, no interpolation, no synthesized sound. Integer nearest-neighbour scaling (4x full, 3x pair, 2x trio).
Frames are flattened to RGB (the engine framebuffer alpha is not displayed). Edit-level additions only:
blurred margin fill, captions/labels/chips, 10 ms boundary fades, final loudness normalisation.

Run: python3 -I recipe/build_showcase.py   (ffmpeg only; no engine, JVM, display or audio device)
Outputs: out/mutator-lab-complete-showcase.mp4, out/chapters.json, work/ intermediates.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = Path("/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3/captures")
NEW = ROOT / "captures"
WORK = ROOT / "work" / "edit"
OUT = ROOT / "out"
FINAL = OUT / "mutator-lab-complete-showcase.mp4"
BLACK = "/usr/share/fonts/noto/NotoSans-Black.ttf"
BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
SPF = 800  # 48000 Hz / 60 presented frames

GAMES = {"ghz": ("SONIC 1", "GREEN HILL 1"), "syz": ("SONIC 1", "SPRING YARD 1"),
         "ehz": ("SONIC 2", "EMERALD HILL 1"), "aiz": ("SONIC 3 & KNUCKLES", "ANGEL ISLAND 1")}
TAKES = {  # key: (capture dir, game)
    "hero": (OLD / "final-ghz-hero", "ghz"), "ghznat": (OLD / "final-ghz-native", "ghz"),
    "chain": (OLD / "final-syz-chain", "syz"), "syznat": (OLD / "final-syz-native", "syz"),
    "live": (OLD / "final-s2-live", "ehz"), "norings": (OLD / "final-aiz-norings", "aiz"),
    "allon": (OLD / "final-aiz-allon", "aiz"),
    "stealth": (NEW / "final-stealth", "ehz"), "np": (NEW / "final-np", "ghz"), "nc": (NEW / "final-nc", "aiz"),
    "ssyes": (NEW / "final-ss-stock", "ghz"), "ssno": (NEW / "final-ss-deny", "ghz"),
    "bonyes": (NEW / "final-bonus-stock", "aiz"), "bonno": (NEW / "final-bonus-deny", "aiz"),
    "spdlive": (NEW / "final-speed-live", "aiz"), "spd50": (NEW / "final-speed50", "aiz"),
    "spd100": (NEW / "final-speed100", "aiz"), "spd200": (NEW / "final-speed200", "aiz"),
}
# Disclosed setup, drawn under the game label.
NOTES = {"hero": ("Positioned start", "140 rings carried in"), "ghznat": ("Positioned start", "140 rings carried in"),
         "allon": ("Act start", "200 rings carried in"),
         "ssyes": ("Positioned near the goal", "50 rings carried in"), "ssno": ("Positioned near the goal", "50 rings carried in"),
         "bonyes": ("Positioned at the star post", "25 rings carried in"), "bonno": ("Positioned at the star post", "25 rings carried in"),
         "nc": ("Positioned at the star post", "0 rings"),
         "spdlive": ("Act start", "interactive frame pacing"), "spd50": ("Act start", "interactive frame pacing"),
         "spd100": ("Act start", "interactive frame pacing"), "spd200": ("Act start", "interactive frame pacing")}

HERO_PRE = [("RINGFALL", "native 32-ring cap"), ("BIG HEAD", "scales with rings")]
HERO = [("RINGFALL", "full inventory"), ("BIG HEAD", "scales with rings")]
CHAIN_PRE = [("VIOLENT EXPLOSIONS", "150% · cap 12 px/tick"), ("BIG HEAD", "170%")]
CHAIN = [("VIOLENT EXPLOSIONS", "300% · cap 16 px/tick"), ("BIG HEAD", "170%")]
GRAV_OFF, GRAV_ON = [("GRAVITY", "off")], [("GRAVITY", "25%")]
SPD_OFF, SPD_ON = [("GAME SPEED", "off")], [("GAME SPEED", "200%"), ("AUDIO", "follows speed")]
ST_OFF = [("BIG HEAD", "200% fixed"), ("STEALTH", "off")]
ST_ON = [("BIG HEAD", "200% fixed"), ("STEALTH", "leader")]
NP_OFF, NP_PEND, NP_ON = [("NO POWERUPS", "off")], [("NO POWERUPS", "Invincibility · pending restart")], [("NO POWERUPS", "Invincibility removed")]
NR_CHIP = [("BIG HEAD", "scales with rings")]
NC_OFF, NC_PEND, NC_ON = [("NO CHECKPOINTS", "off")], [("NO CHECKPOINTS", "pending death")], [("NO CHECKPOINTS", "on")]
ALL = [("GRAVITY", "25%"), ("VIOLENT EXPLOSIONS", "300% · cap 32 px/tick"), ("BIG HEAD", "scales with rings"), ("RINGFALL", "full inventory")]

S = []
def full(sid, take, a, b, caps=(), chips=(), **kw):
    S.append(dict(id=sid, kind="full", panels=[(take, a)], n=b - a, audio=0, caps=list(caps), chips=list(chips), **kw))
def multi(sid, panels, n, labels, audio, caps=(), note=None):
    """panels: [(take, start)], all n frames; audio = index of the panel whose PCM is used."""
    S.append(dict(id=sid, kind="pair" if len(panels) == 2 else "trio", panels=panels, n=n, audio=audio,
                  labels=list(labels), caps=list(caps), chips=[], note=note))

# ---- Cold open: five real moments, no menus.
full("open-ghz-storm", "hero", 708, 774, [(0.15, 1.1, "173 rings")])
full("open-stealth", "stealth", 466, 560, [(0.1, 1.5, "Invisible Sonic")])
full("open-speed", "spdlive", 616, 676, [(0.1, 0.95, "Double speed")])
full("open-syz-launch", "chain", 372, 440, [(0.15, 1.13, "300% stomp")])
full("open-aiz-storm", "allon", 750, 828, [(0.15, 1.3, "211 rings")])
full("title", "allon", 540, 690, title=True)
# ---- 1. Ring madness: Ringfall full inventory + ring-scaled Big Head (accepted take).
full("hero-menu-option", "hero", 84, 140, [(0.05, 0.93, "Ringfall: drop your WHOLE inventory")], HERO_PRE)
full("hero-menu-resume", "hero", 186, 208, [(0.0, 0.37, "Resume")], HERO)
full("hero-bank", "hero", 470, 632, [(0.3, 2.7, "Bank 173 rings")], HERO)
full("hero-hit", "hero", 632, 790, [(1.0, 1.4, "One hit…"), (1.4, 2.63, "…every ring comes out")], HERO)
full("hero-regrow", "hero", 790, 960, [(0.1, 2.83, "Grab them back — the head regrows")], HERO)
multi("hero-contrast", [("ghznat", 518), ("hero", 702)], 122, ("NATIVE: 32 DROP", "FULL INVENTORY: 173 DROP"), 1,
      [(0.1, 2.03, "Same hit, same input")], note="Both: positioned start, 140 rings carried in")
# ---- 2. Violent Explosions in a badnik-heavy Spring Yard (accepted take).
full("chain-menu-pct", "chain", 84, 128, [(0.05, 0.73, "Violent Explosions: 300% rebound")], CHAIN_PRE)
full("chain-menu-cap", "chain", 150, 206, [(0.05, 0.93, "…and a 16 px/tick speed cap")], CHAIN_PRE)
full("chain-menu-resume", "chain", 236, 250, [], CHAIN)
full("chain-1", "chain", 290, 472, [(1.2, 3.0, "Badniks become launch pads")], CHAIN)
full("chain-2", "chain", 500, 562, [(0.35, 1.03, "×2")], CHAIN)
full("chain-3", "chain", 650, 712, [(0.4, 1.03, "×3")], CHAIN)
full("chain-4", "chain", 795, 852, [(0.35, 0.95, "×4")], CHAIN)
full("chain-5", "chain", 950, 1030, [(0.3, 1.33, "×5 — 2,800 points")], CHAIN)
multi("chain-contrast", [("syznat", 112), ("chain", 359)], 120, ("NATIVE BOUNCE", "300% BOUNCE"), 1, [(0.1, 2.0, "Same stomp")])
# ---- 3. Live physics: Gravity (accepted take) and Game Speed (new, interactive pacing).
full("grav-native", "live", 62, 130, [(0.05, 1.13, "Normal jump")], GRAV_OFF)
full("grav-menu-on", "live", 186, 200, [(0.0, 0.23, "Gravity on…")], GRAV_OFF)
full("grav-menu-slide", "live", 206, 292, [(0.0, 1.43, "…slide it to 25%")], GRAV_OFF)
full("grav-menu-resume", "live", 330, 348, [(0.0, 0.3, "Resume")], GRAV_ON)
full("grav-moon", "live", 348, 540, [(0.3, 3.2, "Moon jump — mid-run, no restart")], GRAV_ON)
full("grav-menu-off", "live", 606, 642, [(0.0, 0.6, "Switch it off")], GRAV_ON)
full("grav-back", "live", 686, 770, [(0.2, 1.4, "Back to normal")], GRAV_OFF)
full("speed-normal", "spdlive", 110, 221, [(0.1, 1.8, "Game Speed: 100%")], SPD_OFF)
full("speed-menu-on", "spdlive", 352, 372, [(0.0, 0.33, "On…")], SPD_OFF)
full("speed-menu-pct", "spdlive", 402, 452, [(0.0, 0.83, "…200%…")], SPD_OFF)
full("speed-menu-audio", "spdlive", 476, 500, [(0.0, 0.4, "…audio follows")], SPD_OFF)
full("speed-menu-resume", "spdlive", 604, 616, [(0.0, 0.2, "Resume")], SPD_ON)
full("speed-fast", "spdlive", 616, 760, [(0.2, 2.35, "Two native ticks per frame — music too")], SPD_ON)
multi("speed-trio", [("spd50", 20), ("spd100", 20), ("spd200", 20)], 172, ("50%", "100%", "200%"), 1,
      [(0.1, 2.85, "Same input, same 2.9 seconds on screen")], note="Act start · audio at normal rate in all three")
# ---- 4. Stealth over a fixed 200% Big Head (new).
full("stealth-visible", "stealth", 30, 80, [(0.0, 0.83, "Big Head: fixed 200%")], ST_OFF)
full("stealth-menu-on", "stealth", 146, 168, [(0.0, 0.37, "Stealth on")], ST_OFF)
full("stealth-menu-resume", "stealth", 258, 269, [], ST_ON)
full("stealth-run", "stealth", 269, 330, [(0.1, 1.0, "Where did he go?")], ST_ON)
full("stealth-proof", "stealth", 440, 600, [(0.1, 1.4, "Still collecting rings…"), (1.45, 2.66, "…still defeating Mashers")], ST_ON)
full("stealth-menu-off", "stealth", 742, 760, [(0.0, 0.3, "Stealth off")], ST_ON)
full("stealth-back", "stealth", 862, 935, [(0.1, 1.2, "Back — head and all")], ST_OFF)
# ---- 5. Build your challenge: full-restart removals.
full("np-run1-rings", "np", 165, 215, [(0.05, 0.83, "Ten-ring monitor")], NP_OFF)
full("np-run1-inv", "np", 372, 440, [(0.05, 1.13, "Invincibility monitor")], NP_OFF)
full("np-menu-page", "np", 690, 712, [(0.0, 0.37, "No Powerups on…")], NP_OFF)
full("np-menu-check", "np", 776, 832, [(0.0, 0.93, "…remove ONLY Invincibility")], NP_PEND)
full("np-menu-restart", "np", 920, 946, [(0.0, 0.43, "Restart from act start")], NP_PEND)
full("np-run2-rings", "np", 1222, 1272, [(0.05, 0.83, "Ten-ring monitor stays")], NP_ON)
multi("np-compare", [("np", 372), ("np", 1429)], 84, ("FIRST RUN", "AFTER RESTART"), 1,
      [(0.1, 1.4, "Same jump: invincibility monitor gone")], note="One take: the act really restarts in between")
full("norings-before", "norings", 250, 318, [(0.05, 1.13, "Rings on the hill…")], NR_CHIP)
full("norings-menu", "norings", 410, 448, [(0.0, 0.63, "No Rings: applies on restart")], NR_CHIP)
full("norings-restart", "norings", 490, 560, [(0.0, 1.17, "Restart from act start")], [("NO RINGS", "pending restart")])
full("norings-after", "norings", 1150, 1202, [(0.0, 0.87, "…gone")], [("NO RINGS", "on")])
full("norings-death", "norings", 1330, 1440, [(0.35, 1.83, "No rings. One hit is fatal.")], [("NO RINGS", "on")])
full("nc-post", "nc", 20, 62, [(0.0, 0.7, "Star post")], NC_OFF)
full("nc-death1", "nc", 150, 200, [(0.1, 0.83, "Zero rings: fatal")], NC_OFF)
full("nc-respawn", "nc", 326, 360, [(0.0, 0.57, "Back at the post")], NC_OFF)
full("nc-menu", "nc", 444, 468, [(0.0, 0.4, "No Checkpoints on")], NC_PEND)
full("nc-death2", "nc", 640, 690, [(0.1, 0.83, "Same mistake…")], NC_PEND)
full("nc-actstart", "nc", 812, 880, [(0.05, 1.13, "…back to the act start")], NC_ON)
# ---- 6. Keep the run moving: stage switches.
full("ss-menu", "ssno", 106, 126, [(0.0, 0.33, "No Special Stages")], [])
multi("ss-compare", [("ssyes", 240), ("ssno", 424)], 84, ("STOCK", "NO SPECIAL STAGES"), 1,
      [(0.1, 1.4, "Same jump into the giant ring")], note="Both: positioned near the goal, 50 rings carried in")
full("ss-stock-stage", "ssyes", 1386, 1470, [(0.05, 1.3, "Stock: Special Stage")], [])
full("ss-deny-clear", "ssno", 700, 750, [(0.05, 0.83, "Switched off: act clear")], [("NO SPECIAL STAGES", "on")])
full("ss-deny-act2", "ssno", 1712, 1768, [(0.05, 0.93, "…straight into Act 2")], [("NO SPECIAL STAGES", "on")])
full("bon-menu", "bonno", 106, 126, [(0.0, 0.33, "No Bonus Stages (S3&K only)")], [])
multi("bon-compare", [("bonyes", 112), ("bonno", 296)], 94, ("STOCK: BONUS STARS", "NO BONUS STAGES: NONE"), 0,
      [(0.1, 1.5, "Stock: bonus stars · switched off: none")], note="Both: positioned at the star post, 25 rings carried in")
full("bon-stock-slots", "bonyes", 318, 384, [(0.05, 1.1, "Stock: Slot Machine")], [])
full("bon-deny-run", "bonno", 540, 640, [(0.05, 1.6, "Switched off: keep running")], [("NO BONUS STAGES", "on")])
# ---- 7. Stack everything (accepted take).
full("finale-menu", "allon", 96, 128, [(0.0, 0.53, "Stack them")], ALL)
full("finale-menu-active", "allon", 190, 206, [(0.0, 0.27, "Resume")], ALL)
full("finale-soar", "allon", 470, 540, [(0.05, 1.17, "25% gravity, giant head")], ALL)
full("finale-approach", "allon", 690, 752, [(0.05, 1.03, "211 rings in the bank…")], ALL)
full("finale-storm", "allon", 752, 860, [(0.2, 1.8, "…one Rhinobot later")], ALL)
full("finale-scramble", "allon", 860, 960, [(0.05, 1.67, "Scramble!")], ALL)
full("outro", "hero", 960, 1140, outro=True)

GROUPS = [("Cold open", "open-"), ("Title", "title"), ("Ringfall + Big Head", "hero-"), ("Violent Explosions", "chain-"),
          ("Gravity", "grav-"), ("Game Speed", "speed-"), ("Stealth", "stealth-"), ("No Powerups", "np-"),
          ("No Rings", "norings-"), ("No Checkpoints", "nc-"), ("No Special Stages", "ss-"), ("No Bonus Stages", "bon-"),
          ("Stack everything", "finale-"), ("Outro", "outro")]
MENU = {"hero-menu-option", "hero-menu-resume", "chain-menu-pct", "chain-menu-cap", "chain-menu-resume", "grav-menu-on",
        "grav-menu-slide", "grav-menu-resume", "grav-menu-off", "speed-menu-on", "speed-menu-pct", "speed-menu-audio",
        "speed-menu-resume", "stealth-menu-on", "stealth-menu-resume", "stealth-menu-off", "np-menu-page", "np-menu-check",
        "np-menu-restart", "norings-menu", "nc-menu", "ss-menu", "bon-menu", "finale-menu", "finale-menu-active"}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:]); raise SystemExit(f"ffmpeg failed: {' '.join(map(str, cmd[:8]))}")


def txt(name, text):
    p = WORK / "text" / f"{name}.txt"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text); return p


def dt(tf, font, size, color, x, y, t0=None, t1=None, border=4):
    s = (f"drawtext=fontfile={font}:textfile={tf}:expansion=none:fontsize={size}:fontcolor={color}:"
         f"x={x}:y={y}:borderw={border}:bordercolor=black@0.85")
    if t0 is not None:
        s += f":enable='between(t,{t0},{t1})':alpha='min(1,min((t-{t0})/0.1,({t1}-t)/0.1))'"
    return s


def chips_filters(sid, chips):
    f = []
    for i, (name, value) in enumerate(chips):
        y = 66 + i * 76
        f.append(f"drawbox=x=1620:y={y}:w=284:h=64:color=0x10203a@0.9:t=fill")
        f.append(f"drawbox=x=1620:y={y}:w=6:h=64:color=0xffcc33@1:t=fill")
        f.append(dt(txt(f"{sid}-chip{i}n", name), BOLD, 20, "white", "1638", f"{y + 7}", border=0))
        f.append(dt(txt(f"{sid}-chip{i}v", value), REG, 19 if len(value) < 24 else 15, "0xffd23f", "1638", f"{y + 35}", border=0))
    return f


def caption_filters(sid, caps, y=968):
    return [dt(txt(f"{sid}-cap{i}", text), BLACK, 62 if len(text) < 34 else 52, "white", "(w-text_w)/2", str(y), t0, t1, border=5)
            for i, (t0, t1, text) in enumerate(caps)]


GEOM = {"full": (1280, 896, [(320, 40)]), "pair": (960, 672, [(0, 150), (960, 150)]),
        "trio": (640, 448, [(0, 220), (640, 220), (1280, 220)])}


def render(sg, idx):
    out = WORK / f"seg{idx:03d}-{sg['id']}.mkv"
    n = sg["n"]; dur = n / 60
    w, h, pos = GEOM[sg["kind"]]
    ins, vf = [], []
    for i, (take, a) in enumerate(sg["panels"]):
        ins += ["-framerate", "60", "-start_number", str(a), "-i", str(TAKES[take][0] / "capture/frames/%05d.png")]
    atake, aa = sg["panels"][sg["audio"]]
    ins += ["-i", str(TAKES[atake][0] / "capture/audio.wav")]
    np_ = len(sg["panels"])
    bgsrc = sg["audio"]
    for i in range(np_):
        if i == bgsrc:
            vf.append(f"[{i}:v]format=rgb24,split[p{i}][bgs]")
        else:
            vf.append(f"[{i}:v]format=rgb24[p{i}]")
    vf.append("[bgs]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:2,eq=brightness=-0.34:saturation=0.7[bg]")
    last = "bg"
    for i in range(np_):
        vf.append(f"[p{i}]scale={w}:{h}:flags=neighbor[s{i}]")
        vf.append(f"[{last}][s{i}]overlay={pos[i][0]}:{pos[i][1]}[o{i}]"); last = f"o{i}"
    take0, game = TAKES[sg["panels"][0][0]][0], TAKES[sg["panels"][0][0]][1]
    g, z = GAMES[game]
    chain = []
    if sg["kind"] == "full":
        chain += [dt(txt(f"{sg['id']}-game", g), BLACK, 34 if len(g) < 12 else 24, "0xffd23f", "40", "70", border=3),
                  dt(txt(f"{sg['id']}-zone", z), BOLD, 22, "white", "40", "118", border=3)]
        key = sg["panels"][0][0]
        if key in NOTES:
            n1, n2 = NOTES[key]
            chain += [dt(txt(f"{sg['id']}-note1", n1), REG, 19, "white@0.8", "40", "168", border=2),
                      dt(txt(f"{sg['id']}-note2", n2), REG, 19, "white@0.8", "40", "194", border=2)]
        chain += chips_filters(sg["id"], sg["chips"])
    else:
        ly = 84 if sg["kind"] == "pair" else 150
        for i, lab in enumerate(sg["labels"]):
            col = "0xffd23f" if i == np_ - 1 else "0xffffff"
            chain.append(dt(txt(f"{sg['id']}-L{i}", lab), BLACK, 46 if sg["kind"] == "pair" else 52, col,
                            f"{pos[i][0]}+({w}-text_w)/2", str(ly)))
        for i in range(1, np_):
            chain.append(f"drawbox=x={pos[i][0] - 2}:y={pos[i][1]}:w=4:h={h}:color=black@1:t=fill")
        chain.append(dt(txt(f"{sg['id']}-game", f"{g} · {z}"), BOLD, 24, "0xffd23f", "(w-text_w)/2", "30", border=3))
        if sg.get("note"):
            ny = pos[0][1] + h + 18
            chain.append(dt(txt(f"{sg['id']}-note", sg["note"]), REG, 22, "white@0.8", "(w-text_w)/2", str(ny), border=2))
    if sg.get("title"):
        chain += ["drawbox=x=320:y=300:w=1280:h=330:color=0x0b1426@0.72:t=fill",
                  "drawbox=x=320:y=300:w=1280:h=6:color=0xffcc33@1:t=fill",
                  dt(txt("title-main", "MUTATOR LAB"), BLACK, 150, "white", "(w-text_w)/2", "330", 0.0, 2.5, border=6),
                  dt(txt("title-sub", "11 mutators. Configure them. Stack them. Toggle them."), BOLD, 44, "0xffd23f", "(w-text_w)/2", "505", 0.15, 2.5, border=3),
                  dt(txt("title-sub2", "An OpenGGF mod for Sonic 1, 2 & 3&K · your own ROMs"), REG, 32, "white", "(w-text_w)/2", "570", 0.3, 2.5, border=3)]
    elif sg.get("outro"):
        names = ["Gravity · Ringfall · Big Head · Stealth · Game Speed · Violent Explosions",
                 "No Powerups · No Rings · No Checkpoints · No Special Stages · No Bonus Stages"]
        chain += ["drawbox=x=220:y=220:w=1480:h=520:color=0x0b1426@0.76:t=fill",
                  "drawbox=x=220:y=220:w=1480:h=6:color=0xffcc33@1:t=fill",
                  dt(txt("outro-main", "MUTATOR LAB"), BLACK, 130, "white", "(w-text_w)/2", "245", 0.1, 3.0, border=6),
                  dt(txt("outro-1", names[0]), BOLD, 36, "0xffd23f", "(w-text_w)/2", "420", 0.25, 3.0, border=3),
                  dt(txt("outro-2", names[1]), BOLD, 36, "0xffd23f", "(w-text_w)/2", "470", 0.35, 3.0, border=3),
                  dt(txt("outro-3", "Sonic 1 · Sonic 2 · Sonic 3 & Knuckles — native levels, music and SFX"), REG, 32, "white", "(w-text_w)/2", "555", 0.45, 3.0, border=3),
                  dt(txt("outro-4", "Bonus stages exist only in Sonic 3 & Knuckles. Bring your own ROMs. Not affiliated with Sega."), REG, 24, "white@0.85", "(w-text_w)/2", "625", 0.55, 3.0, border=2)]
    else:
        chain += ["drawbox=x=0:y=944:w=1920:h=136:color=black@0.55:t=fill"] + caption_filters(sg["id"], sg["caps"], 968)
    vf.append(f"[{last}]" + ",".join(chain) + "[v]")
    a0 = aa * SPF
    fades = f"afade=t=in:d=0.01,afade=t=out:st={dur - 0.01:.4f}:d=0.01"
    vf.append(f"[{np_}:a]atrim=start_sample={a0}:end_sample={a0 + n * SPF},asetpts=PTS-STARTPTS,{fades}[a]")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(vf), "-map", "[v]", "-map", "[a]",
         "-frames:v", str(n), "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p",
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)])
    return out


def main():
    WORK.mkdir(parents=True, exist_ok=True); OUT.mkdir(exist_ok=True)
    only = set(sys.argv[1:])
    chapters, files, t = [], [], 0.0
    for i, sg in enumerate(S):
        out = WORK / f"seg{i:03d}-{sg['id']}.mkv"
        if not only or sg["id"] in only or not out.exists():
            render(sg, i)
        files.append(out)
        w, h, pos = GEOM[sg["kind"]]
        src = [{"take": str(TAKES[k][0]), "frames": [a, a + sg["n"]], "crop": [pos[j][0], pos[j][1], w, h],
                "audio": j == sg["audio"], "audio_samples": [a * SPF, (a + sg["n"]) * SPF] if j == sg["audio"] else None}
               for j, (k, a) in enumerate(sg["panels"])]
        chapters.append({"id": sg["id"], "kind": sg["kind"], "menu": sg["id"] in MENU, "start_s": round(t, 3),
                         "end_s": round(t + sg["n"] / 60, 3), "frames": sg["n"], "sources": src,
                         "captions": [c[2] for c in sg["caps"]], "labels": sg.get("labels", []),
                         "chips": [" ".join(c) for c in sg["chips"]], "note": sg.get("note")})
        t += sg["n"] / 60
        print(f"{i:03d} {sg['id']:22s} {sg['n']:4d}f  t={t:7.2f}s", flush=True)
    lst = WORK / "concat-video.txt"
    lst.write_text("".join(f"file '{f}'\n" for f in files))
    wavs = []
    for f in files:
        w = f.with_suffix(".wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-map", "0:a", "-c:a", "pcm_s16le", str(w)])
        wavs.append(w)
    alst = WORK / "concat-audio.txt"
    alst.write_text("".join(f"file '{w}'\n" for w in wavs))
    pcm = WORK / "audio.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(alst), "-c:a", "pcm_s16le", str(pcm)])
    meta = WORK / "chapters.ffmeta"
    lines = [";FFMETADATA1", "title=Mutator Lab — complete gameplay showcase"]
    for name, pre in GROUPS:
        cs = [c for c in chapters if c["id"].startswith(pre)]
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(round(cs[0]['start_s'] * 1000))}",
                  f"END={int(round(cs[-1]['end_s'] * 1000))}", f"title={name}"]
    meta.write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(pcm), "-i", str(meta),
         "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2", "-vf", "setpts=N/(60*TB)",
         "-fps_mode", "cfr", "-r", "60",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", str(FINAL)])
    menu_s = sum(c["frames"] for c in chapters if c["menu"]) / 60
    groups = [{"title": name, "start_s": [c for c in chapters if c["id"].startswith(pre)][0]["start_s"],
               "end_s": [c for c in chapters if c["id"].startswith(pre)][-1]["end_s"]} for name, pre in GROUPS]
    (OUT / "chapters.json").write_text(json.dumps({"duration_s": round(t, 3), "frames": sum(c["frames"] for c in chapters),
                                                    "menu_s": round(menu_s, 3), "chapters": groups, "segments": chapters},
                                                   indent=1, ensure_ascii=False))
    print("final", FINAL, round(t, 2), "s; menus", round(menu_s, 2), "s")


if __name__ == "__main__":
    main()
