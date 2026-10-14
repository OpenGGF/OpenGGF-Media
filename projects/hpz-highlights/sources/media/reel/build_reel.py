#!/usr/bin/env python3
"""HPZ bring-up highlights reel.

Builds animated before/after title cards (Pillow), normalises each source clip to a
1920x1080/60fps silent segment (optional slow motion and zoom, labelled halves), then
concatenates and re-encodes once with chapters. Sources live one directory up; every
interval and effect is listed in EDIT below and written to edit_list.csv / chapters.csv.

Usage: python3 build_reel.py            (writes hpz-bring-up-highlights.mp4 beside this file)
"""
import csv
import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent
WORK = ROOT / "work"
OUT = ROOT / "hpz-bring-up-highlights.mp4"
W, H, FPS = 1920, 1080, 60
CARD_FRAMES = 132
BG = (13, 11, 26)

HEAVY = "/usr/share/fonts/TTF/FiraSansCompressed-Heavy.ttf"
XBOLD = "/usr/share/fonts/TTF/FiraSansCompressed-ExtraBold.ttf"
BODY = "/usr/share/fonts/TTF/FiraSans-Medium.ttf"
BOLD = "/usr/share/fonts/TTF/FiraSans-Bold.ttf"

# Chapter palettes: (primary, accent, deep) — HPZ crystal purple, teleporter green,
# Knuckles red, emerald cyan, carnival gold.
THEMES = {
    "arrival": ((124, 92, 255), (255, 214, 64), (34, 22, 78)),
    "teleport": ((60, 220, 150), (255, 255, 255), (10, 60, 52)),
    "knuckles": ((235, 48, 72), (255, 196, 40), (70, 12, 24)),
    "shrine": ((40, 210, 240), (255, 120, 220), (10, 46, 70)),
    "ripple": ((255, 170, 30), (80, 200, 255), (70, 36, 6)),
    "finale": ((255, 214, 64), (124, 92, 255), (40, 24, 8)),
}

# kind: "new" (no before), "ba" (before|after halves), "ba_baked" (labels already drawn),
#       "after" (after-only), "triptych" (before|after|native).
EDIT = [
    dict(card=True, chapter="HIDDEN PALACE ZONE", theme="finale", title="THE HIDDEN PALACE BRING-UP",
         sub="Sonic 3 & Knuckles  ·  zone $16 act 2  ·  from blank slot to a route that matches the real game",
         tags=["OPENGGF", "BEFORE  vs  AFTER"], intro=True),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="A PALACE OF ITS OWN",
         sub="Slot $1601 now loads the playable Hidden Palace — not the Super Emerald shrine", tags=["NEW"]),
    dict(src="01-hpz-playable-act-loads.mp4", kind="new", caption="Cold load of $1601: ROM bounds, objects and start"),
    dict(src="08a-hpz-title-card-hidden-palace-no-act.mp4", kind="new", caption="Title card: HIDDEN PALACE, no act number, as in the ROM"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="ENTER, STAGE RIGHT",
         sub="Obj_LevelIntro_PlayerRun walks Sonic in while the camera leads by $B0", tags=["BEFORE", "AFTER"]),
    dict(src="31a-hpz-level-intro-run-in-before-after.mp4", kind="ba", caption="Level start: camera held ahead while the run-in plays"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="LET THERE BE GLOW",
         sub="AnPal_HPZ pulses the crystal wall lights", tags=["BEFORE", "AFTER"]),
    dict(src="02b-hpz-anpal-wall-light-glow-before-after.mp4", kind="ba_baked", caption="Palette cycle: wall light glow"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="TILES THAT TICK",
         sub="AniPLC_HPZ animates the teleporter and waterfall art", tags=["BEFORE", "AFTER"]),
    dict(src="02a-hpz-aniplc-teleporter-tiles-before-after.mp4", kind="ba_baked", caption="Animated tiles"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="THE LIGHTS CHANGE AT $460",
         sub="HPZ's palette control object swaps the zone palette when the camera crosses $460", tags=["NEW"]),
    dict(src="03-hpz-palette-control-camera-460.mp4", kind="new", caption="Palette control at camera Y $460"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="KNUCKLES GETS HIS OWN VIEW",
         sub="HPZ_ScreenInit patches the background for Knuckles' route", tags=["BEFORE", "AFTER"]),
    dict(src="04-hpz-knuckles-background-patch-before-after.mp4", kind="ba_baked", caption="Knuckles background chunks $8E/$8F"),

    dict(card=True, chapter="1 · ARRIVAL", theme="arrival", title="THE SKY WAS MISSING",
         sub="The background wrapped at 512 px — but the clouds don't repeat. Now it reaches the screen edge.",
         tags=["BEFORE", "AFTER"]),
    dict(src="32a-hpz-background-full-width-before-after.mp4", kind="ba", caption="Background: storm clouds and crystals across the full width"),

    dict(card=True, chapter="2 · THE TELEPORTERS", theme="teleport", title="NO MORE LEDGE-HUGGING",
         sub="The pad's sloped edge used the wrong surface height — Sonic now runs past like the ROM",
         tags=["BEFORE", "AFTER", "SLOW-MO ½×"]),
    dict(src="31b-hpz-teleporter-edge-no-landing-before-after.mp4", kind="ba", slow=2, caption="Running past the pad edge (half speed)"),

    dict(card=True, chapter="2 · THE TELEPORTERS", theme="teleport", title="GOING UP",
         sub="Charge, beam, 74-step rise and a 24-frame settle — matched against the real game", tags=["NEW"]),
    dict(src="05-hpz-teleporter-lower-to-upper-pad.mp4", kind="new", caption="Lower pad to the upper floor"),

    dict(card=True, chapter="2 · THE TELEPORTERS", theme="teleport", title="HOLD THAT POSE",
         sub="object_control 3 freezes the rider's frame; the roll resumes mid-spin", tags=["BEFORE", "AFTER", "SLOW-MO ½×"]),
    dict(src="32b-hpz-teleporter-rise-settle-animation-before-after.mp4", kind="ba", slow=2, caption="Rise and settle animation (half speed)"),

    dict(card=True, chapter="2 · THE TELEPORTERS", theme="teleport", title="CAMERA, FOLLOW ME",
         sub="Sonic stays grounded on the pad, so the camera tracks the lift", tags=["AFTER"]),
    dict(src="31c-hpz-teleporter-grounded-lift-camera-follows.mp4", kind="after", caption="Charge, lift and unroll in place"),

    dict(card=True, chapter="2 · THE TELEPORTERS", theme="teleport", title="KNUCKLES' SHORTCUT",
         sub="Knuckles' pad sends him straight to Sky Sanctuary Act 2", tags=["NEW"]),
    dict(src="06-hpz-knuckles-teleporter-exit-to-ssz2.mp4", kind="new", caption="Knuckles route exit"),

    dict(card=True, chapter="3 · KNUCKLES ATTACKS", theme="knuckles", title="GUARDIAN ON THE GLIDE",
         sub="CutsceneKnux_HPZ: 41 routine, hit and defeat transitions on the native frames", tags=["NEW"]),
    dict(src="10-hpz-knuckles-fight-start.mp4", kind="new", caption="Knuckles drops in"),
    dict(src="11-hpz-knuckles-fight-hit.mp4", kind="new", caption="A hit lands"),
    dict(src="12-hpz-knuckles-defeat-dizzy-runs-off.mp4", kind="new", caption="Defeated, dizzy, off he runs"),

    dict(card=True, chapter="3 · KNUCKLES ATTACKS", theme="knuckles", title="THE HEIST",
         sub="Robotnik's crane lifts the Master Emerald and zaps Knuckles", tags=["NEW"]),
    dict(src="13a-hpz-emerald-theft-crane-grab.mp4", kind="new", caption="Crane grab"),
    dict(src="13b-hpz-ship-sparks-zap-knuckles.mp4", kind="new", caption="Sparks"),

    dict(card=True, chapter="3 · KNUCKLES ATTACKS", theme="knuckles", title="A FLASH IN SYNC",
         sub="Palettes now reach the screen at V-int with the sprites — the hit flash lands on the real game's frames",
         tags=["BEFORE", "AFTER", "ZOOM 2×", "SLOW-MO ¼×"]),
    dict(src="34-hpz-ship-hit-flash-phase-before-after.mp4", kind="ba", slow=4, zoom_ba=(330, 0, 450, 360),
         caption="Robotnik's hit flash, zoomed (quarter speed)"),

    dict(card=True, chapter="3 · KNUCKLES ATTACKS", theme="knuckles", title="DON'T LET GO OF JUMP",
         sub="The cutscene locks the pad but keeps the held jump — full height, like the ROM",
         tags=["BEFORE", "AFTER", "SLOW-MO ½×"]),
    dict(src="32c-hpz-altar-jump-held-through-lock-before-after.mp4", kind="ba", slow=2, caption="Held jump through Ctrl_1_locked (half speed)"),

    dict(card=True, chapter="3 · KNUCKLES ATTACKS", theme="knuckles", title="THE FLOOR GIVES WAY",
         sub="Altar collapse, Knuckles' punch, and the exit to Sky Sanctuary", tags=["NEW"]),
    dict(src="14-hpz-altar-floor-collapse.mp4", kind="new", caption="Altar floor collapse"),
    dict(src="15-hpz-knuckles-punches-collapse-block.mp4", kind="new", caption="Knuckles punches the block"),
    dict(src="16-hpz-ending-hold-knuckles-beamed-away.mp4", kind="new", caption="Knuckles is beamed away"),
    dict(src="17-hpz-sonic-teleports-exit-to-ssz.mp4", kind="new", caption="Sonic teleports out"),

    dict(card=True, chapter="4 · THE EMERALD SHRINE", theme="shrine", title="SEVEN SHRINES",
         sub="A Chaos Emerald pedestal arms and opens the Super Emerald stage", tags=["NEW"]),
    dict(src="07-hpz-chaos-pedestal-enters-super-emerald-stage.mp4", kind="new", caption="Pedestal to Super Emerald stage"),

    dict(card=True, chapter="4 · THE EMERALD SHRINE", theme="shrine", title="HYPER, ANNOUNCED",
         sub="Results tally over the rebuilt sanctuary, a ring of stars, and the Hyper message — frame-exact to native",
         tags=["NEW"]),
    dict(src="30a-hpz-results-sanctuary-backdrop-fade-in.mp4", kind="new", caption="Sanctuary backdrop fades in"),
    dict(src="30b-hpz-results-pan-pedestals-star-orbit.mp4", kind="new", caption="Pan to the pedestals, stars converge"),
    dict(src="30c-hpz-results-hyper-message.mp4", kind="new", caption="NOW SONIC CAN BE HYPER SONIC"),

    dict(card=True, chapter="4 · THE EMERALD SHRINE", theme="shrine", title="ONLY THE UNCONVERTED",
         sub="Chaos indicators hide emeralds already turned Super", tags=["BEFORE", "AFTER"]),
    dict(src="30d-hpz-results-indicator-gate-before-after.mp4", kind="ba_baked", caption="Results indicator gate"),

    dict(card=True, chapter="4 · THE EMERALD SHRINE", theme="shrine", title="FADE TO BLACK",
         sub="S3K leaves results silently through black — a new Mod API hook keeps Sonic 1/2's white exit",
         tags=["AFTER", "SLOW-MO ½×"]),
    dict(src="33-hpz-results-exit-fades-to-black.mp4", kind="after", slow=2, caption="Results exit (half speed)"),

    dict(card=True, chapter="5 · RIPPLE EFFECTS", theme="ripple", title="CARNIVAL LIGHTS, ON CUE",
         sub="Palette cycles wait for the 22-frame level fade, as Palette_fade_timer does in the ROM",
         tags=["BEFORE", "AFTER", "NATIVE", "SLOW-MO ½×"]),
    dict(src="35-cnz-palette-cycle-start-before-after-native.mp4", kind="triptych", slow=2,
         caption="Carnival Night 1 start: before · after · real hardware (half speed)"),

    dict(card=True, chapter="THE RESULT", theme="finale", title="FRAME FOR FRAME",
         sub="Recorded Sonic + Tails input from entry to Sky Sanctuary: camera and both players match the real game "
             "on every frame from 441,761 to 448,821",
         tags=["7,060 FRAMES", "0 POSITION MISMATCHES"], outro=True),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def ease_out_back(t):
    c1, c3 = 1.70158, 2.70158
    t = max(0.0, min(1.0, t))
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_in(t):
    t = max(0.0, min(1.0, t))
    return t * t * t


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def tag_colour(tag, theme):
    primary, accent, deep = THEMES[theme]
    upper = tag.upper()
    if upper.startswith("BEFORE"):
        return (120, 120, 140), (255, 255, 255)
    if upper.startswith("AFTER"):
        return primary, (10, 10, 20)
    if upper.startswith("NATIVE"):
        return (255, 255, 255), (10, 10, 20)
    if upper.startswith("NEW"):
        return accent, (10, 10, 20)
    return (255, 255, 255, 40), (255, 255, 255)


def draw_card(entry, index, out_dir):
    theme = entry["theme"]
    primary, accent, deep = THEMES[theme]
    out_dir.mkdir(parents=True, exist_ok=True)
    f_chapter = font(XBOLD, 40)
    f_title = font(HEAVY, 150 if len(entry["title"]) < 22 else 118)
    f_sub = font(BODY, 38)
    f_tag = font(BOLD, 34)
    for frame in range(CARD_FRAMES):
        t = frame / CARD_FRAMES
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img, "RGBA")
        # Background: deep gradient.
        for y in range(0, H, 6):
            d.rectangle([0, y, W, y + 6], fill=lerp(deep, BG, y / H))
        # S3K-style slanted bars sweeping in, then out at the end.
        exit_t = ease_in((frame - (CARD_FRAMES - 16)) / 16)
        bars = [(primary, 0, 210), (accent, 5, 90), ((255, 255, 255), 9, 34)]
        for colour, delay, thick in bars:
            p = ease_out_back((frame - delay) / 26)
            x_off = int((1 - p) * -1400 - exit_t * 2600)
            top = 150 + delay * 14
            poly = [(x_off - 300, top), (x_off + 1500, top), (x_off + 1500 - 90, top + thick), (x_off - 390, top + thick)]
            d.polygon(poly, fill=colour + (235,))
        # Drifting sparkles.
        for k in range(26):
            sx = (k * 173 + frame * (3 + k % 4)) % W
            sy = 480 + (k * 97) % 560
            r = 2 + (k % 3)
            alpha = int(120 + 120 * math.sin(frame / 7 + k))
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=accent + (max(0, alpha),))
        # Chapter label.
        ca = max(0, min(1, (frame - 6) / 14)) * (1 - exit_t)
        d.text((150, 88), entry["chapter"], font=f_chapter, fill=(255, 255, 255, int(255 * ca)))
        # Title with overshoot slide from the right and hard shadow.
        tp = ease_out_back((frame - 10) / 30)
        tx = int(150 + (1 - tp) * 1500 + exit_t * 2200)
        ty = 420
        d.text((tx + 8, ty + 8), entry["title"], font=f_title, fill=(0, 0, 0, 170))
        d.text((tx, ty), entry["title"], font=f_title, fill=(255, 255, 255))
        # Underline sweep.
        ul = max(0, min(1, (frame - 26) / 20))
        bbox = d.textbbox((tx, ty), entry["title"], font=f_title)
        d.rectangle([150, bbox[3] + 22, 150 + int((bbox[2] - 150) * ul), bbox[3] + 34], fill=accent)
        # Subtitle typewriter.
        chars = int(len(entry["sub"]) * max(0, min(1, (frame - 34) / 40)))
        sub = entry["sub"][:chars]
        lines = wrap(d, sub, f_sub, W - 300)
        sa = 1 - exit_t
        for i, line in enumerate(lines):
            d.text((152, bbox[3] + 70 + i * 52), line, font=f_sub, fill=(230, 230, 245, int(255 * sa)))
        # Tag chips pop in one by one.
        cx = 150
        cy = 900
        for i, tag in enumerate(entry.get("tags", [])):
            pop = ease_out_back((frame - 50 - i * 8) / 16)
            if pop <= 0:
                continue
            bgc, fg = tag_colour(tag, theme)
            tw = d.textbbox((0, 0), tag, font=f_tag)[2]
            w = int((tw + 56) * pop)
            hgt = 64
            if w > 10:
                d.rounded_rectangle([cx, cy, cx + w, cy + hgt], radius=32,
                                    fill=(bgc if len(bgc) == 4 else bgc + (int(255 * (1 - exit_t)),)))
                if pop > 0.7:
                    d.text((cx + 28, cy + 13), tag, font=f_tag, fill=fg)
            if i + 1 < len(entry["tags"]) and tag.upper() == "BEFORE" and entry["tags"][i + 1].upper().startswith("AFTER") and pop > 0.9:
                d.text((cx + tw + 70, cy + 6), "→", font=font(BOLD, 44), fill=(255, 255, 255))
                cx += 60
            cx += tw + 56 + 22
        # Card number corner.
        d.text((W - 230, H - 90), f"{index:02d}", font=font(HEAVY, 70), fill=(255, 255, 255, 60))
        img.save(out_dir / f"{frame:04d}.png")


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textbbox((0, 0), trial, font=fnt)[2] > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,nb_frames:format=duration", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    j = json.loads(out)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), float(j["format"]["duration"])


def overlay_png(entry, layout, path):
    """Caption bar plus BEFORE/AFTER/NATIVE labels positioned over the displayed halves."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    theme = entry["theme"]
    primary, accent, _ = THEMES[theme]
    ox, oy, dw, dh = layout
    d.rectangle([0, H - 96, W, H], fill=(8, 7, 18, 235))
    d.rectangle([0, H - 96, 14, H], fill=primary + (255,))
    d.text((46, H - 76), entry["caption"], font=font(BOLD, 40), fill=(255, 255, 255, 255))
    d.text((W - 520, H - 70), "OpenGGF · Hidden Palace", font=font(BODY, 30), fill=(200, 200, 220, 200))
    labels = []
    if entry["kind"] == "ba":
        labels = [("BEFORE", ox + dw // 4), ("AFTER", ox + 3 * dw // 4)]
    elif entry["kind"] == "triptych":
        labels = [("BEFORE", ox + dw // 6), ("AFTER", ox + dw // 2), ("NATIVE", ox + 5 * dw // 6)]
    elif entry["kind"] == "after":
        labels = [("AFTER", ox + dw // 2)]
    elif entry["kind"] == "new":
        labels = [("NEW", ox + dw // 2)]
    f_tag = font(BOLD, 36)
    for text, cx in labels:
        bgc, fg = tag_colour(text, theme)
        tw = d.textbbox((0, 0), text, font=f_tag)[2]
        y = max(12, oy - 70) if oy > 80 else oy + 16
        d.rounded_rectangle([cx - tw // 2 - 28, y, cx + tw // 2 + 28, y + 60], radius=30, fill=bgc[:3] + (240,))
        d.text((cx - tw // 2, y + 10), text, font=f_tag, fill=fg)
    badges = [b for b in (("SLOW-MO " + {2: "½×", 4: "¼×"}.get(entry["slow"], f"1/{entry['slow']}×")) if entry.get("slow") else None,
                          "ZOOM 2×" if entry.get("zoom_ba") else None) if b]
    bx = W - 40
    for b in badges:
        tw = d.textbbox((0, 0), b, font=font(BOLD, 30))[2]
        d.rounded_rectangle([bx - tw - 40, 20, bx, 76], radius=28, fill=accent + (235,))
        d.text((bx - tw - 20, 30), b, font=font(BOLD, 30), fill=(10, 10, 20))
        bx -= tw + 60
    img.save(path)


def encode_card(frames_dir, out):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "%04d.png"),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-video_track_timescale", "60000", str(out)], check=True)


def encode_clip(entry, out, overlay):
    src = SRC / entry["src"]
    sw, sh, dur = probe(src)
    chain = []
    if entry.get("zoom_ba"):
        x, y, cw, ch = entry["zoom_ba"]
        half = sw // 2
        chain.append(f"split[a][b];[a]crop={cw}:{ch}:{x}:{y}[l];[b]crop={cw}:{ch}:{x + half}:{y}[r];[l][r]hstack")
        sw, sh = cw * 2, ch
        chain.append(f"scale={sw * 2}:{sh * 2}:flags=neighbor")
        sw, sh = sw * 2, sh * 2
    if entry.get("slow"):
        chain.append(f"setpts=PTS*{entry['slow']},fps={FPS}")
    max_w, max_h = W - 40, H - 96 - 110
    scale = min(max_w / sw, max_h / sh)
    dw, dh = int(sw * scale) // 2 * 2, int(sh * scale) // 2 * 2
    ox = (W - dw) // 2
    oy = 90 + (max_h - dh) // 2
    chain.append(f"scale={dw}:{dh}:flags=neighbor")
    chain.append(f"pad={W}:{H}:{ox}:{oy}:color=0x0d0b1a")
    layout = (ox, oy, dw, dh)
    overlay_png(entry, layout, overlay)
    graph = "[0:v]" + ",".join(chain) + "[v];[v][1:v]overlay=0:0,format=yuv420p[out]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-loop", "1", "-i", str(overlay),
                    "-filter_complex", graph, "-map", "[out]", "-t", str(dur * entry.get("slow", 1)),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS),
                    "-video_track_timescale", "60000", "-an", str(out)], check=True)
    return dur


def main():
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    segments, edit_rows = [], []
    theme = "finale"
    chapter_title = None
    card_no = 0
    for i, entry in enumerate(EDIT):
        if entry.get("card"):
            theme = entry["theme"]
            card_no += 1
            chapter_title = entry["title"]
            frames = WORK / f"card{i:03d}"
            draw_card(entry, card_no, frames)
            out = WORK / f"seg{i:03d}.mp4"
            encode_card(frames, out)
            shutil.rmtree(frames)
            segments.append((out, chapter_title, True))
            edit_rows.append([entry["chapter"], i, entry["title"], "(title card)", "", "", "", ""])
        else:
            entry["theme"] = theme
            out = WORK / f"seg{i:03d}.mp4"
            dur = encode_clip(entry, out, WORK / f"overlay{i:03d}.png")
            segments.append((out, chapter_title, False))
            edit_rows.append([chapter_title, i, entry["caption"], entry["src"], "0.000", f"{dur:.3f}",
                              entry.get("slow", 1), "zoom2x" if entry.get("zoom_ba") else ""])
    manifest = WORK / "concat.txt"
    manifest.write_text("".join(f"file '{p.name}'\n" for p, _, _ in segments))
    # Chapters: one per title card, spanning its card and the clips after it.
    meta = [";FFMETADATA1"]
    chapters, t, current = [], 0.0, None
    for path, title, is_card in segments:
        _, _, d = probe(path)
        if is_card:
            if current:
                current[2] = t
                chapters.append(current)
            current = [title, t, None]
        t += d
    current[2] = t
    chapters.append(current)
    for title, start, end in chapters:
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}", f"title={title}"]
    (WORK / "chapters.txt").write_text("\n".join(meta) + "\n")
    tmp = ROOT / "hpz-bring-up-highlights.new.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(manifest),
                    "-i", str(WORK / "chapters.txt"), "-map_metadata", "1", "-map_chapters", "1",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-movflags", "+faststart", "-an", str(tmp)], cwd=WORK, check=True)
    with open(ROOT / "edit_list.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["chapter", "order", "title", "source", "source_start_seconds", "source_end_seconds", "slow_factor", "effect"])
        w.writerows(edit_rows)
    with open(ROOT / "chapters.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "output_start_seconds", "output_end_seconds"])
        for title, start, end in chapters:
            w.writerow([title, f"{start:.3f}", f"{end:.3f}"])
    tmp.replace(OUT)
    print(OUT, f"{t:.1f}s", len(chapters), "chapters")


if __name__ == "__main__":
    main()
