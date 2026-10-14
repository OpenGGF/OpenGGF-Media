#!/usr/bin/env python3
"""Mutator Lab gameplay promo — reproducible edit recipe (task e0603654, opus_gameplay_promo_r1).

Inputs: the final offscreen captures under ../captures/final-*/capture (PNG per native frame,
offline PCM audio.wav at 48 kHz, 800 samples per frame). Every segment is an exact frame range of
one take; its audio is the same take's PCM samples [start*800, end*800). No retiming, no frame
interpolation, integer 4x (full) or 3x (split) nearest-neighbour scaling, no synthesized SFX.
Frames are flattened to RGB first (the engine framebuffer's alpha is not displayed).
Edit-level additions only: blurred margin fill, caption/label text, final loudness normalisation.

Run: python3 -I recipe/build_promo.py   (ffmpeg only; no engine, JVM, display or audio device)
Outputs: out/mutator-lab-gameplay-promo.mp4, out/chapters.json, work/ intermediates.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "captures"
WORK = ROOT / "work"
OUT = ROOT / "out"
BLACK = "/usr/share/fonts/noto/NotoSans-Black.ttf"
BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
SPF = 800  # 48000 Hz / 60 fps

GAMES = {"ghz": ("SONIC 1", "GREEN HILL 1"), "syz": ("SONIC 1", "SPRING YARD 1"),
         "s2": ("SONIC 2", "EMERALD HILL 1"), "aiz": ("SONIC 3 & KNUCKLES", "ANGEL ISLAND 1")}
TAKES = {"hero": ("final-ghz-hero", "ghz"), "ghznat": ("final-ghz-native", "ghz"),
         "chain": ("final-syz-chain", "syz"), "syznat": ("final-syz-native", "syz"),
         "live": ("final-s2-live", "s2"), "norings": ("final-aiz-norings", "aiz"),
         "allon": ("final-aiz-allon", "aiz")}

# Disclosed setup: these takes begin from a positioned start with a carried-in ring budget.
NOTES = {"hero": ("Positioned start", "140 rings carried in"), "ghznat": ("Positioned start", "140 rings carried in"),
         "allon": ("Act start", "200 rings carried in")}
HERO_CHIPS = [("RINGFALL", "full inventory"), ("BIG HEAD", "scales with rings")]
HERO_CHIPS_PRE = [("RINGFALL", "native 32-ring cap"), ("BIG HEAD", "scales with rings")]
CHAIN_CHIPS = [("VIOLENT EXPLOSIONS", "300% · cap 16 px/tick"), ("BIG HEAD", "170%")]
CHAIN_CHIPS_PRE = [("VIOLENT EXPLOSIONS", "150% · cap 12 px/tick"), ("BIG HEAD", "170%")]
ALL_CHIPS = [("GRAVITY", "25%"), ("VIOLENT EXPLOSIONS", "300% · cap 32 px/tick"), ("BIG HEAD", "scales with rings"), ("RINGFALL", "full inventory")]

# (id, take, start, end, captions[(t0, t1, text)], chips, extra)
FULL = "full"
S = []
def seg(sid, take, a, b, caps=(), chips=(), kind=FULL, **kw):
    S.append(dict(id=sid, take=take, a=a, b=b, caps=list(caps), chips=list(chips), kind=kind, **kw))

# Cold open: three real moments, no menus.
seg("open-ghz-storm", "hero", 708, 774, [(0.15, 1.1, "173 rings")])
seg("open-syz-launch", "chain", 372, 440, [(0.15, 1.13, "300% stomp")])
seg("open-aiz-storm", "allon", 750, 828, [(0.15, 1.3, "211 rings")])
# Title over the stacked S3K soar (moving gameplay; title only, no prose).
seg("title", "allon", 540, 660, title=True)
# Hero: Ringfall full inventory + ring-scaled Big Head, in one continuous native take.
seg("hero-menu-option", "hero", 84, 140, [(0.05, 0.93, "Ringfall: drop your WHOLE inventory")], HERO_CHIPS_PRE)
seg("hero-menu-resume", "hero", 186, 208, [(0.0, 0.37, "Resume")], HERO_CHIPS)
seg("hero-bank", "hero", 440, 632, [(0.6, 3.2, "Bank 173 rings")], HERO_CHIPS)
seg("hero-hit", "hero", 632, 790, [(1.0, 1.4, "One hit…"), (1.4, 2.63, "…every ring comes out")], HERO_CHIPS)
seg("hero-regrow", "hero", 790, 960, [(0.1, 2.83, "Grab them back — the head regrows")], HERO_CHIPS)
seg("hero-contrast", ("ghznat", "hero"), 518, 640, [(0.1, 2.03, "Same hit, same input")], kind="split",
    offset=184, labels=("NATIVE: 32 DROP", "FULL INVENTORY: 173 DROP"))
# Violent Explosions: configure, then a five-badnik stomp chain.
seg("chain-menu-pct", "chain", 84, 128, [(0.05, 0.73, "Violent Explosions: 300% rebound")], CHAIN_CHIPS_PRE)
seg("chain-menu-cap", "chain", 150, 206, [(0.05, 0.93, "…and a 16 px/tick speed cap")], CHAIN_CHIPS_PRE)
seg("chain-menu-resume", "chain", 236, 250, [], CHAIN_CHIPS)
seg("chain-1", "chain", 250, 472, [(1.9, 3.7, "Badniks become launch pads")], CHAIN_CHIPS)
seg("chain-2", "chain", 500, 562, [(0.35, 1.03, "×2")], CHAIN_CHIPS)
seg("chain-3", "chain", 650, 712, [(0.4, 1.03, "×3")], CHAIN_CHIPS)
seg("chain-4", "chain", 795, 852, [(0.35, 0.95, "×4")], CHAIN_CHIPS)
seg("chain-5", "chain", 950, 1030, [(0.3, 1.33, "×5 — 2,800 points")], CHAIN_CHIPS)
seg("chain-contrast", ("syznat", "chain"), 112, 232, [(0.1, 2.03, "Same stomp")], kind="split",
    offset=247, labels=("NATIVE BOUNCE", "300% BOUNCE"))
# Live toggle: change gravity mid-run, Resume applies it, switch it off again.
seg("live-native", "live", 62, 130, [(0.05, 1.13, "Normal jump")], [("GRAVITY", "off")])
seg("live-menu-on", "live", 186, 200, [(0.0, 0.23, "Gravity on…")], [("GRAVITY", "off")])
seg("live-menu-slide", "live", 206, 292, [(0.0, 1.43, "…slide it to 25%")], [("GRAVITY", "off")])
seg("live-menu-resume", "live", 330, 348, [(0.0, 0.3, "Resume")], [("GRAVITY", "25%")])
seg("live-moon", "live", 348, 540, [(0.3, 3.2, "Moon jump — mid-run, no restart")], [("GRAVITY", "25%")])
seg("live-menu-off", "live", 606, 642, [(0.0, 0.6, "Switch it off")], [("GRAVITY", "25%")])
seg("live-menu-resume2", "live", 686, 696, [], [("GRAVITY", "off")])
seg("live-back", "live", 696, 770, [(0.1, 1.23, "Back to normal")], [("GRAVITY", "off")])
# Challenge: No Rings is a LOAD rule, so it takes effect through a real act restart.
seg("norings-before", "norings", 250, 318, [(0.05, 1.13, "Rings on the hill…")], [("BIG HEAD", "scales with rings")])
seg("norings-menu", "norings", 410, 448, [(0.0, 0.63, "No Rings: applies on restart")], [("BIG HEAD", "scales with rings")])
seg("norings-restart", "norings", 490, 560, [(0.0, 1.17, "Restart from act start")], [("NO RINGS", "pending restart")])
seg("norings-after", "norings", 1150, 1202, [(0.0, 0.87, "…gone")], [("NO RINGS", "on")])
seg("norings-death", "norings", 1330, 1440, [(0.35, 1.83, "No rings. One hit is fatal.")], [("NO RINGS", "on")])
# Finale: everything stacked in Angel Island.
seg("finale-menu", "allon", 96, 128, [(0.0, 0.53, "Stack them")], ALL_CHIPS)
seg("finale-menu-active", "allon", 190, 206, [(0.0, 0.27, "Resume")], ALL_CHIPS)
seg("finale-soar", "allon", 470, 540, [(0.05, 1.17, "25% gravity, giant head")], ALL_CHIPS)
seg("finale-approach", "allon", 690, 752, [(0.05, 1.03, "211 rings in the bank…")], ALL_CHIPS)
seg("finale-storm", "allon", 752, 860, [(0.2, 1.8, "…one Rhinobot later")], ALL_CHIPS)
seg("finale-scramble", "allon", 860, 960, [(0.05, 1.67, "Scramble!")], ALL_CHIPS)
# Outro card over moving gameplay.
seg("outro", "hero", 960, 1100, outro=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:]); raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])}")


def txt(name, text):
    p = WORK / "text" / f"{name}.txt"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text); return p


def dt(tf, font, size, color, x, y, t0=None, t1=None, border=4, extra=""):
    s = (f"drawtext=fontfile={font}:textfile={tf}:expansion=none:fontsize={size}:fontcolor={color}:"
         f"x={x}:y={y}:borderw={border}:bordercolor=black@0.85{extra}")
    if t0 is not None:
        s += f":enable='between(t,{t0},{t1})':alpha='min(1,min((t-{t0})/0.1,({t1}-t)/0.1))'"
    return s


def chips_filters(sid, chips):
    f = []
    for i, (name, value) in enumerate(chips):
        y = 66 + i * 76
        f.append(f"drawbox=x=1620:y={y}:w=280:h=64:color=0x10203a@0.9:t=fill")
        f.append(f"drawbox=x=1620:y={y}:w=6:h=64:color=0xffcc33@1:t=fill")
        f.append(dt(txt(f"{sid}-chip{i}n", name), BOLD, 20, "white", "1638", f"{y + 7}", border=0))
        f.append(dt(txt(f"{sid}-chip{i}v", value), REG, 19, "0xffd23f", "1638", f"{y + 35}", border=0))
    return f


def caption_filters(sid, caps, y=968):
    f = []
    for i, (t0, t1, text) in enumerate(caps):
        f.append(dt(txt(f"{sid}-cap{i}", text), BLACK, 62, "white", "(w-text_w)/2", str(y), t0, t1, border=5))
    return f


def render(sg, idx):
    out = WORK / f"seg{idx:02d}-{sg['id']}.mkv"
    n = sg["b"] - sg["a"]; dur = n / 60
    fades = f"afade=t=in:d=0.01,afade=t=out:st={dur - 0.01:.4f}:d=0.01"
    if sg["kind"] == "split":
        left, right = (TAKES[t][0] for t in sg["take"])
        ra = sg["a"] + sg["offset"]
        game = TAKES[sg["take"][1]][1]
        ins = ["-framerate", "60", "-start_number", str(sg["a"]), "-i", str(CAP / left / "capture/frames/%05d.png"),
               "-framerate", "60", "-start_number", str(ra), "-i", str(CAP / right / "capture/frames/%05d.png"),
               "-i", str(CAP / right / "capture/audio.wav")]
        L, R = sg["labels"]
        vf = [f"[1:v]format=rgb24,split[r1][r2]",
              f"[r1]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:2,eq=brightness=-0.34:saturation=0.7[bg]",
              f"[0:v]format=rgb24,scale=960:672:flags=neighbor[l]", f"[r2]scale=960:672:flags=neighbor[r]",
              f"[l][r]hstack=2[pair]", f"[bg][pair]overlay=0:150[v0]"]
        chain = ["drawbox=x=0:y=944:w=1920:h=136:color=black@0.55:t=fill",
                 dt(txt(f"{sg['id']}-L", L), BLACK, 46, "0xffffff", "(960-text_w)/2", "84"),
                 dt(txt(f"{sg['id']}-R", R), BLACK, 46, "0xffd23f", "960+(960-text_w)/2", "84"),
                 "drawbox=x=958:y=150:w=4:h=672:color=black@1:t=fill"] + caption_filters(sg["id"], sg["caps"], 970)
        if sg["take"][1] in NOTES:
            chain.append(dt(txt(f"{sg['id']}-note", "Both: " + NOTES[sg["take"][1]][0].lower() + ", " + NOTES[sg["take"][1]][1]),
                            REG, 22, "white@0.8", "(w-text_w)/2", "872", border=2))
        vf.append("[v0]" + ",".join(chain) + "[v]")
        amap = "2:a"; vframes = n
    else:
        take, game = TAKES[sg["take"]]
        ins = ["-framerate", "60", "-start_number", str(sg["a"]), "-i", str(CAP / take / "capture/frames/%05d.png"),
               "-i", str(CAP / take / "capture/audio.wav")]
        vf = [f"[0:v]format=rgb24,split[a1][a2]",
              f"[a1]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:2,eq=brightness=-0.34:saturation=0.7[bg]",
              f"[a2]scale=1280:896:flags=neighbor[fg]", f"[bg][fg]overlay=320:40[v0]"]
        g, z = GAMES[game]
        chain = [dt(txt(f"{sg['id']}-game", g), BLACK, 34 if len(g) < 12 else 24, "0xffd23f", "40", "70", border=3),
                 dt(txt(f"{sg['id']}-zone", z), BOLD, 22, "white", "40", "118", border=3)]
        if sg["take"] in NOTES:
            n1, n2 = NOTES[sg["take"]]
            chain += [dt(txt(f"{sg['id']}-note1", n1), REG, 19, "white@0.8", "40", "168", border=2),
                      dt(txt(f"{sg['id']}-note2", n2), REG, 19, "white@0.8", "40", "194", border=2)]
        chain += chips_filters(sg["id"], sg["chips"])
        if sg.get("title"):
            chain += ["drawbox=x=320:y=300:w=1280:h=330:color=0x0b1426@0.72:t=fill",
                      "drawbox=x=320:y=300:w=1280:h=6:color=0xffcc33@1:t=fill",
                      dt(txt("title-main", "MUTATOR LAB"), BLACK, 150, "white", "(w-text_w)/2", "330", 0.0, 2.0, border=6),
                      dt(txt("title-sub", "Stackable mutators for Sonic 1, 2 & 3&K"), BOLD, 46, "0xffd23f", "(w-text_w)/2", "505", 0.15, 2.0, border=3),
                      dt(txt("title-sub2", "An OpenGGF mod · your own ROMs"), REG, 32, "white", "(w-text_w)/2", "570", 0.3, 2.0, border=3)]
        elif sg.get("outro"):
            chain += ["drawbox=x=320:y=250:w=1280:h=440:color=0x0b1426@0.74:t=fill",
                      "drawbox=x=320:y=250:w=1280:h=6:color=0xffcc33@1:t=fill",
                      dt(txt("outro-main", "MUTATOR LAB"), BLACK, 140, "white", "(w-text_w)/2", "280", 0.1, 2.34, border=6),
                      dt(txt("outro-1", "11 mutators · configure · stack · toggle live"), BOLD, 44, "0xffd23f", "(w-text_w)/2", "450", 0.25, 2.34, border=3),
                      dt(txt("outro-2", "Sonic 1 · Sonic 2 · Sonic 3 & Knuckles — native levels, music and SFX"), REG, 32, "white", "(w-text_w)/2", "520", 0.4, 2.34, border=3),
                      dt(txt("outro-3", "Bring your own ROMs. Not affiliated with Sega."), REG, 26, "white@0.85", "(w-text_w)/2", "590", 0.5, 2.34, border=2)]
        else:
            chain += ["drawbox=x=0:y=944:w=1920:h=136:color=black@0.55:t=fill"] + caption_filters(sg["id"], sg["caps"])
        vf.append("[v0]" + ",".join(chain) + "[v]")
        amap = "1:a"; vframes = n
    a0 = (sg["a"] + (sg.get("offset", 0) if sg["kind"] == "split" else 0)) * SPF
    af = f"[{amap}]atrim=start_sample={a0}:end_sample={a0 + n * SPF},asetpts=PTS-STARTPTS,{fades}[a]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(vf) + ";" + af, "-map", "[v]", "-map", "[a]",
           "-frames:v", str(vframes), "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p",
           "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)]
    run(cmd)
    return out, n


def main():
    WORK.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    chapters, files, t = [], [], 0.0
    for i, sg in enumerate(S):
        f, n = render(sg, i)
        files.append(f)
        take = sg["take"]
        src = ([{"take": TAKES[take[0]][0], "frames": [sg["a"], sg["b"]]},
                {"take": TAKES[take[1]][0], "frames": [sg["a"] + sg["offset"], sg["b"] + sg["offset"]], "audio": True}]
               if sg["kind"] == "split" else [{"take": TAKES[take][0], "frames": [sg["a"], sg["b"]], "audio": True}])
        chapters.append({"id": sg["id"], "start_s": round(t, 3), "end_s": round(t + n / 60, 3), "frames": n,
                         "sources": src, "captions": [c[2] for c in sg["caps"]], "chips": [" ".join(c) for c in sg["chips"]]})
        t += n / 60
        print(f"{i:02d} {sg['id']:22s} {n:4d}f  t={t:6.2f}s", flush=True)
    # Concatenate video and PCM separately: each segment is exactly n frames and n*800 samples, so the
    # two streams stay frame-locked without the demuxer padding a boundary with a duplicate frame.
    lst = WORK / "concat-video.txt"
    lst.write_text("".join(f"file '{f}'\n" for f in files))
    pcm = WORK / "audio.wav"
    alst = WORK / "concat-audio.txt"
    wavs = []
    for f in files:
        w = f.with_suffix(".wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-map", "0:a", "-c:a", "pcm_s16le", str(w)])
        wavs.append(w)
    alst.write_text("".join(f"file '{w}'\n" for w in wavs))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(alst), "-c:a", "pcm_s16le", str(pcm)])
    meta = WORK / "chapters.ffmeta"
    groups = [("Cold open", "open-"), ("Title", "title"), ("Ringfall + Big Head", "hero-"), ("Violent Explosions", "chain-"),
              ("Live toggle", "live-"), ("No Rings restart", "norings-"), ("Stack everything", "finale-"), ("Outro", "outro")]
    lines = [";FFMETADATA1", "title=Mutator Lab — gameplay promo"]
    for name, pre in groups:
        cs = [c for c in chapters if c["id"].startswith(pre)]
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(cs[0]['start_s'] * 1000)}", f"END={int(cs[-1]['end_s'] * 1000)}", f"title={name}"]
    meta.write_text("\n".join(lines) + "\n")
    final = OUT / "mutator-lab-gameplay-promo.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(pcm), "-i", str(meta),
         "-map", "0:v", "-map", "1:a", "-map_metadata", "2", "-map_chapters", "2", "-vf", "setpts=N/(60*TB)",
         "-fps_mode", "cfr", "-r", "60",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", str(final)])
    (OUT / "chapters.json").write_text(json.dumps({"duration_s": round(t, 3), "segments": chapters}, indent=1, ensure_ascii=False))
    print("final", final, round(t, 2), "s")


if __name__ == "__main__":
    main()
