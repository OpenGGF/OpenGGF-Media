#!/usr/bin/env python3
"""Expanded Mutator Lab promo edit recipe.

Purpose: assemble a 1920x1080/60 H.264+AAC promo from retained offscreen
GameplayCaptureTool frames, PCM and CSV under opus-expansion-polish/captures.
Inputs: read-only capture directories (frames/%05d.png, audio.wav, state.csv).
Outputs: work/segs/*.mkv intermediates, out/mutator-lab-expanded-promo.mp4,
out/mutator-lab-expanded-promo-thumb.png, out/chapters.json.
Originating task: 5c24f4a5 opus_expansion_promo_r1 (2026-10-09).
No engine, JVM, display or audio device is used; ffmpeg/magick only.
"""
import json, os, subprocess, sys, textwrap

ROOT = "/home/farrell/scratch/agent-tmp/codex/mutator-lab-expansion-5c24f4a5-76e8-47c7-bc47-4173173d5caa"
CAP = f"{ROOT}/opus-expansion-polish/captures"
P = f"{ROOT}/opus-expansion-promo"
WORK, SEGS, TXT, OUT = f"{P}/work", f"{P}/work/segs", f"{P}/work/txt", f"{P}/out"
BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
FPS = 60
FADE = 0.2
for d in (SEGS, TXT, OUT):
    os.makedirs(d, exist_ok=True)

def frames(c): return f"{CAP}/{c}/capture/frames"
def wav(c): return f"{CAP}/{c}/capture/audio.wav"

_t = 0
def tfile(text, width=None):
    global _t
    _t += 1
    if width:
        text = "\n".join(textwrap.fill(p, width) if p else "" for p in text.split("\n"))
    path = f"{TXT}/{_t:03d}.txt"
    open(path, "w").write(text)
    return path

def dt(path, font, size, color, x, y, extra=""):
    return (f"drawtext=fontfile={font}:textfile={path}:expansion=none:fontsize={size}:"
            f"fontcolor={color}:x={x}:y={y}:line_spacing=10{extra}")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-4000:])
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])}")

ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
       "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]

def chrome(D, header, chip, caption, prov):
    """Background, header bar, side panel text; returns filter tail after [c]."""
    parts = [
        dt(tfile(header), BOLD, 52, "white", 48, 34),
        dt(tfile("OpenGGF  ·  Mutator Lab"), REG, 24, "0x8fa3c8", "w-tw-48", 54),
    ]
    if chip:
        parts.append(dt(tfile(chip), BOLD, 26, "0x46d5ff", 1368, 150))
    if caption:
        parts.append(dt(tfile(caption, 31), REG, 29, "white", 1368, 206))
    if prov:
        parts.append(dt(tfile(prov, 46), REG, 18, "0x7d8db0", 1368, "1032-th"))
    parts.append(f"fade=t=in:st=0:d={FADE},fade=t=out:st={D - FADE:.3f}:d={FADE},format=yuv420p")
    return ",".join(parts)

def bg(D):
    return (f"color=c=0x0b1226:s=1920x1080:r={FPS}:d={D:.3f},"
            "drawbox=x=48:y=116:w=1832:h=3:color=0x3fd0ff@0.75:t=fill,"
            "drawbox=x=42:y=130:w=1292:h=908:color=0x3fd0ff@0.35:t=4")

def afilt(D, idx=1, gain=0.0):
    return (f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain}dB,apad,"
            f"atrim=0:{D:.3f},afade=t=in:d=0.15,afade=t=out:st={D - 0.25:.3f}:d=0.25[a]")

segments = []  # (name, seconds, chapter, description)

def clip(name, cap, a, b, header, chip, caption, prov, chapter):
    D = (b - a) / FPS
    fc = (f"[0:v]scale=1280:896:flags=neighbor,setsar=1[g];{bg(D)}[bg];"
          f"[bg][g]overlay=48:136:eof_action=pass[c0];[c0]{chrome(D, header, chip, caption, prov)}[v];"
          + afilt(D))
    run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-start_number", str(a),
         "-i", f"{frames(cap)}/%05d.png", "-ss", f"{a / FPS:.4f}", "-t", f"{D:.4f}", "-i", wav(cap),
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{D:.4f}", *ENC,
         f"{SEGS}/{name}.mkv"])
    segments.append(dict(name=name, seconds=D, chapter=chapter, source=cap, frames=[a, b],
                         kind="native clip", header=header, caption=caption))

def hold(name, cap, f, D, header, chip, caption, prov, chapter):
    fc = (f"[0:v]scale=1280:896:flags=neighbor,setsar=1[g];{bg(D)}[bg];"
          f"[bg][g]overlay=48:136[c0];[c0]{chrome(D, header, chip, caption, prov)}[v];" + afilt(D))
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{D:.4f}",
         "-i", f"{frames(cap)}/{f:05d}.png", "-ss", f"{f / FPS:.4f}", "-t", f"{D:.4f}", "-i", wav(cap),
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{D:.4f}", *ENC,
         f"{SEGS}/{name}.mkv"])
    segments.append(dict(name=name, seconds=D, chapter=chapter, source=cap, frames=[f, f],
                         kind="held native UI frame (audio continues from same capture)",
                         header=header, caption=caption))

def card(name, D, bgcap, bgframe, acap, aframe, lines, chapter, gain=-4.0):
    """lines: list of (text, font, size, color, y)"""
    draw = ",".join(dt(tfile(t), fnt, s, col, "(w-tw)/2", y) for t, fnt, s, col, y in lines)
    fc = (f"[0:v]scale=1920:1344:flags=neighbor,crop=1920:1080,boxblur=18:2,eq=brightness=-0.32:saturation=0.8,"
          f"drawbox=x=0:y=0:w=1920:h=1080:color=0x0b1226@0.45:t=fill,{draw},"
          f"fade=t=in:st=0:d={FADE},fade=t=out:st={D - FADE:.3f}:d={FADE},format=yuv420p[v];"
          + afilt(D, gain=gain))
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{D:.4f}",
         "-i", f"{frames(bgcap)}/{bgframe:05d}.png", "-ss", f"{aframe / FPS:.4f}", "-t", f"{D:.4f}",
         "-i", wav(acap), "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{D:.4f}", *ENC,
         f"{SEGS}/{name}.mkv"])
    segments.append(dict(name=name, seconds=D, chapter=chapter, source=f"card over blurred {bgcap}#{bgframe}",
                         audio=f"{acap} from frame {aframe}", kind="title card",
                         text=[l[0] for l in lines]))

# Ring-head grid: screen-space Sonic centre at frame 170 from state.csv (x-cam_x, y-cam_y).
RH = {"s1": (80, 176, "SONIC 1  ·  GREEN HILL 1"), "s2": (96, 96, "SONIC 2  ·  EMERALD HILL 1"),
      "s3k": (152, 138, "SONIC 3 & KNUCKLES  ·  ANGEL ISLAND 1")}
RH_VARIANTS = [("stock0", "Mutator off"), ("0", "0 rings  =  100%"), ("25", "25 rings  =  125%"),
               ("50", "50 rings  =  150%"), ("100", "100 rings  =  200%"), ("150", "150 rings  =  200% (clamped)")]

def grid(name, game, a, b, chapter):
    D = (b - a) / FPS
    sx, sy, chip = RH[game]
    cx, cy = max(0, min(320 - 128, sx - 64)), max(0, min(224 - 112, sy - 72))
    if game == "s2":
        cy = 52  # keep the S2 HUD rows (y<56) out of the crop; head stays in frame
    inputs, fc = [], []
    for i, (v, _) in enumerate(RH_VARIANTS):
        inputs += ["-framerate", str(FPS), "-start_number", str(a), "-i", f"{frames(f'{game}-ringhead-{v}')}/%05d.png"]
        fc.append(f"[{i}:v]crop=128:112:{cx}:{cy},scale=384:336:flags=neighbor,setsar=1[p{i}]")
    inputs += ["-ss", f"{a / FPS:.4f}", "-t", f"{D:.4f}", "-i", wav(f"{game}-ringhead-100")]
    chain = f"{bg(D).replace(',drawbox=x=42:y=130:w=1292:h=908:color=0x3fd0ff@0.35:t=4', '')}[b0]"
    fc.append(chain)
    last = "b0"
    for i, (v, label) in enumerate(RH_VARIANTS):
        x = 88 + (i % 3) * 408
        y = 168 + (i // 3) * 432
        col = "0x8fa3c8" if v == "stock0" else "0x3fd0ff"
        fc.append(f"[{last}][p{i}]overlay={x}:{y}:eof_action=pass,"
                  f"drawbox=x={x - 3}:y={y - 3}:w=390:h=342:color={col}@0.6:t=3,"
                  + dt(tfile(label), BOLD, 26, "white" if v != "stock0" else "0xb8c4dc",
                       f"{x}+(384-tw)/2", y + 350) + f"[o{i}]")
        last = f"o{i}"
    caption = ("Optional ‘Scale with rings’. Fixed size stays the default.\n\n"
               "0 rings is native 100%; growth is linear to the configured maximum (here 200%) "
               "at 100 rings and clamps above. Losing rings shrinks the head again.\n\n"
               "Rings here are a starting inventory set by the capture tool, not collected.")
    prov = (f"Same frames {a}–{b} of six offscreen captures; one crop window around "
            "Sonic's native head pixels, 3x nearest-neighbour. Body, feet and collision unchanged.")
    fc.append(f"[{last}]{chrome(D, 'NEW  ·  Big Head scales with rings', chip, caption, prov)}[v]")
    fc.append(afilt(D, idx=6))
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]",
         "-map", "[a]", "-t", f"{D:.4f}", *ENC, f"{SEGS}/{name}.mkv"])
    segments.append(dict(name=name, seconds=D, chapter=chapter, source=[f"{game}-ringhead-{v}" for v, _ in RH_VARIANTS],
                         frames=[a, b], kind="native clip grid (starting inventory)", header="Big Head scales with rings"))

PROV = "Offscreen GameplayCaptureTool · one native tick per frame · native PCM from the same run"

def build():
    card("01-intro", 3.5, "s3k-play-03", 520, "s3k-play-03", 1000, [
        ("OpenGGF", BOLD, 40, "0x46d5ff", 330),
        ("Mutator Lab", BOLD, 128, "white", 384),
        ("11 optional mutators for native Sonic 1, Sonic 2 and Sonic 3 & Knuckles", REG, 40, "white", 560),
        ("Example creator mod  ·  every effect off by default  ·  your own ROMs", REG, 30, "0xb8c4dc", 640),
    ], "Intro")
    clip("02-hub-s1", "s1-play-03", 450, 600, "Three games, one hub", "SONIC 1  ·  TITLE SCREEN",
         "Mutator Lab opens from each game's own title screen.", PROV, "Three games")
    clip("03-hub-s2", "s2-play-03", 560, 697, "Three games, one hub", "SONIC 2  ·  TITLE SCREEN",
         "Start, configure, or read how to play.", PROV, "Three games")
    clip("04-hub-s3k", "s3k-play-03", 430, 590, "Three games, one hub", "SONIC 3 & KNUCKLES  ·  TITLE",
         "Native ROM play; the menu cues are the games' own sound effects.", PROV, "Three games")
    cat = "The catalogue  ·  11 mutators"
    cprov = "Native Mutator Lab option page, Sonic 1 (held still). Audio continues from the same capture."
    clip("05-gravity", "s1-explore-04", 3430, 3610, cat, "1 · GRAVITY",
         "25–200% dry fall acceleration for ordinary Sonic. Jumps, water, hurt and scripted motion stay native.",
         "Live slider edit, Sonic 1 catalogue. " + PROV, "Catalogue")
    pages = [
        ("06-ringfall", 1083, "2 · RINGFALL MANIPULATOR",
         "When hurt you still lose every held ring; only 10–100% scatter back as recoverable rings, with an optional 1–32 cap."),
        ("07-bighead", 1254, "3 · BIG HEAD",
         "100–200% about the neck on reviewed native Sonic head pixels. Feet, body and collisions unchanged."),
        ("08-stealth", 1482, "4 · STEALTH",
         "Hides the player sprite. Gameplay, HUD, sound and world effects stay native."),
        ("09-nopowerups", 1596, "5 · NO POWERUPS",
         "Per-type monitor filters, applied on the next full LOAD. Types a game lacks show Unavailable."),
        ("10-nocheckpoints", 1710, "6 · NO CHECKPOINTS",
         "Death returns to the act start. Death banking is independent of stage-entry triggers."),
        ("11-norings", 1881, "7 · NO RINGS",
         "Removes main-level rings and ring rewards on a full load. Main play only."),
        ("12-gamespeed", 2109, "8 · GAME SPEED",
         "25–400% in whole native steps, with optional audio follow. (Not visible in this video: the capture tool runs one tick per frame.)"),
        ("13-nospecial", 2166, "9 · NO SPECIAL STAGES",
         "Denies new special-stage entry. A transition already admitted finishes normally."),
        ("14-nobonus", 2337, "10 · NO BONUS STAGES",
         "Sonic 3 & Knuckles only. Sonic 1 and 2 show it Unavailable."),
        ("15-violent", 2565, "11 · VIOLENT EXPLOSIONS",
         "150–300% vertical badnik-defeat rebound with a speed cap. Not radial blasts; bosses unaffected."),
    ]
    for name, f, chip, cap in pages:
        hold(name, "s1-explore-04", f, 1.6, cat, chip, cap, cprov, "Catalogue")
    clip("16-s1-bighead", "s1-play-03", 920, 1200, "Native play", "SONIC 1  ·  GREEN HILL 1",
         "Big Head at a fixed 150%, the default mode. The enlarged head is Sonic's own reviewed head pixels; the body underneath is untouched.",
         PROV, "Native play")
    clip("17-s1-live", "s1-play-03", 1250, 1540, "LIVE edits apply on Resume", "SONIC 1  ·  PLAY HELD",
         "Start holds play. Edits stay pending until Resume: Stealth on, Game Speed 200%. No Powerups waits for a restart or death.",
         PROV, "LIVE vs LOAD")
    clip("18-s1-stealth", "s1-play-03", 1541, 1780, "LIVE edits apply on Resume", "SONIC 1  ·  RESUMED",
         "Stealth: Sonic is hidden. Camera, HUD, rings and sound carry on natively.", PROV, "LIVE vs LOAD")
    clip("19-s1-load", "s1-play-03", 1830, 2100, "LOAD edits apply on restart", "SONIC 1  ·  LOAD: RESTART",
         "Restart rebuilds the act through native assembly, so LOAD-time monitor filters take effect.",
         PROV, "LIVE vs LOAD")
    clip("20-s2-bighead", "s2-play-03", 880, 1120, "Sonic 2", "SONIC 2  ·  EMERALD HILL 1",
         "Same mutators, same hub, Sonic 2's own engine rules and art.", PROV, "Sonic 2")
    clip("21-s2-stealth", "s2-play-03", 1541, 1720, "Sonic 2", "SONIC 2  ·  STEALTH",
         "After Resume the player sprite is hidden; the world keeps running.", PROV, "Sonic 2")
    clip("22-s3k-ball", "s3k-play-03", 2470, 2648, "Sonic 3 & Knuckles", "S3&K  ·  ANGEL ISLAND 1",
         "Big Head on standing art. Curled, unreviewed, powered or non-Sonic art keeps the stock sprite.",
         PROV, "Sonic 3 & Knuckles")
    clip("23-s3k-stealth", "s3k-play-03", 2941, 3180, "Sonic 3 & Knuckles", "S3&K  ·  STEALTH",
         "Stealth targets the leader: Sonic vanishes while Tails, the sidekick, stays visible.", PROV,
         "Sonic 3 & Knuckles")
    grid("24-rh-s1", "s1", 20, 200, "Ring-scaled head")
    grid("25-rh-s2", "s2", 20, 200, "Ring-scaled head")
    grid("26-rh-s3k", "s3k", 20, 200, "Ring-scaled head")
    clip("27-rh-earned", "s3k-ringhead-title", 2840, 3200, "NEW  ·  Big Head scales with rings",
         "S3&K  ·  RINGS EARNED IN PLAY",
         "Collected in play, 0 to 11 rings. The LIVE menu reports the head at 111% for 11 rings (max 200%).",
         PROV, "Ring-scaled head")
    card("28-outro", 4.5, "s1-ringhead-100", 170, "s3k-play-03", 1400, [
        ("Mutator Lab", BOLD, 96, "white", 300),
        ("Defaults off  ·  LIVE edits on Resume  ·  LOAD edits on native restart", REG, 36, "white", 450),
        ("Sonic 1  ·  Sonic 2  ·  Sonic 3 & Knuckles", BOLD, 36, "0x46d5ff", 510),
        ("Example mod jar prepared at JVM boot  ·  all game assets from your own ROMs", REG, 28, "0xb8c4dc", 590),
        ("OpenGGF is an independent fan research project, not affiliated with Sega.", REG, 24, "0x8fa3c8", 900),
    ], "Outro")

def finish():
    lst = f"{WORK}/concat.txt"
    open(lst, "w").write("".join(f"file '{SEGS}/{s['name']}.mkv'\n" for s in segments))
    out = f"{OUT}/mutator-lab-expanded-promo.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.2",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "120", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", out])
    t = 0.0
    chapters = []
    for s in segments:
        s["start"] = round(t, 3)
        t += s["seconds"]
        s["end"] = round(t, 3)
        if not chapters or chapters[-1]["title"] != s["chapter"]:
            chapters.append(dict(title=s["chapter"], start=s["start"]))
    json.dump(dict(video=out, duration=round(t, 3), chapters=chapters, segments=segments),
              open(f"{OUT}/chapters.json", "w"), indent=1)
    print(out, round(t, 3))

def thumb():
    # 1280x720: ring-head 100 vs mutator off, native pixels, title text.
    f = 170
    a = f"{frames('s1-ringhead-0')}/{f:05d}.png"
    b = f"{frames('s1-ringhead-100')}/{f:05d}.png"
    c = f"{frames('s1-play-03')}/{1000:05d}.png"
    run(["ffmpeg", "-v", "error", "-y", "-i", c, "-i", a, "-i", b, "-filter_complex",
         "[0:v]scale=1280:896:flags=neighbor,crop=1280:720:0:88,boxblur=12:2,eq=brightness=-0.3[bg];"
         "[1:v]crop=96:96:32:104,scale=384:384:flags=neighbor[l];"
         "[2:v]crop=96:96:32:104,scale=384:384:flags=neighbor[r];"
         "[bg][l]overlay=150:250,drawbox=x=147:y=247:w=390:h=390:color=0x8fa3c8@0.8:t=3[x];"
         "[x][r]overlay=746:250,drawbox=x=743:y=247:w=390:h=390:color=0x3fd0ff@0.9:t=3,"
         + dt(tfile("Mutator Lab"), BOLD, 92, "white", "(w-tw)/2", 40) + ","
         + dt(tfile("11 mutators  ·  Sonic 1 · 2 · 3&K  ·  NEW ring-scaled Big Head"), BOLD, 34, "0x46d5ff", "(w-tw)/2", 160) + ","
         + dt(tfile("0 rings"), BOLD, 28, "white", 150 + 192 - 50, 650) + ","
         + dt(tfile("100 rings"), BOLD, 28, "white", 746 + 192 - 64, 650),
         "-frames:v", "1", f"{OUT}/mutator-lab-expanded-promo-thumb.png"])

if __name__ == "__main__":
    build()
    finish()
    thumb()
