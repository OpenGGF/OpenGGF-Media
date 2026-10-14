#!/usr/bin/env python3
"""Sonic3K Chaos Mode revision 3: one still page, one moving card at a time.

External media production script, 2026-10-14. Inputs are qualified, ROM-backed
400x224/60 Hz capture masters and their state CSV/provenance. This script never
launches Java, alters engine state, or modifies previous revisions. The layout
uses integer nearest expansion for the active picture and a 1/4 nearest reduction
for frozen thumbnails. A dissolve changes opacity, never playback speed.

Every mode requires --admission-worktree. The outer shared scheduler lease covers
all ffprobe/ffmpeg children and remains inherited until their process groups exit.

cards.json is either a list or {"cards": [...], "intro_frames": 240,
"end_frames": 360}. Each card contains effect, label, zone, source, in_frame,
clip_frames, slot_frames, thumb_frame, caption and qualified. Source paths are
relative to revision-3; thumb_frame is an ABSOLUTE source frame inside the clip.
slot_frames must equal clip_frames, or clip_frames plus 18 transition frames.
The latter reserves 18 frames before the new continuous clip begins. Only the
last soz-ghost-party card may set allow_death:true and source_audio:true.

audio.json may contain bed (relative path), bed_gain_db, master_gain_db,
ghost_gain_db, ghost_duck_frames (60), ghost_fade_in_frames (6),
ghost_fade_out_frames (30), bed_return_frames (30), end_fade_frames (180),
true_peak_linear (0.84), and cues (see audio_configuration). A short bed is
rejected unless bed_loop supplies a lead-qualified {start_sample,end_sample,
qualified:true} loop at the rendered bed's sample rate. Unqualified file loops
are not used to manufacture a longer coherent track.

Commands: plan; preview --frames 0,300,600; render; audio (reuse own video).
All production output is confined to revision-3/out and revision-3/work.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import signal
import subprocess
import sys
from contextlib import contextmanager
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
ASSETS = TASK / "assets"
OUT = ROOT / "out"
WORK = ROOT / "work"
W, H, FPS, SR = 1920, 1080, 60, 48000
SOURCE_SIZE = (400, 224)
ACTIVE = (48, 40, 1200, 672)
PLATE = (48, 724, 1200, 92)
CELL_W, CELL_H, STEP_X, STEP_Y = 148, 104, 156, 112
TRANSITION = 18
NAVY, GOLD, CREAM = (9, 20, 49), (255, 202, 48), (232, 224, 200)
PALE, OUTLINE, PANEL = (185, 195, 217), (30, 42, 74), (14, 27, 56)
LEASE = None
INHERITED = None
PROCESSES: set[subprocess.Popen] = set()
ZONE_NAMES = {
    "aiz": "ANGEL ISLAND", "hcz": "HYDROCITY", "mgz": "MARBLE GARDEN",
    "cnz": "CARNIVAL NIGHT", "fbz": "FLYING BATTERY", "icz": "ICE CAP",
    "lbz": "LAUNCH BASE", "mhz": "MUSHROOM HILL", "soz": "SANDOPOLIS",
    "lrz": "LAVA REEF", "ssz": "SKY SANCTUARY", "dez": "DEATH EGG",
    "hpz": "HIDDEN PALACE", "ddz": "DOOMSDAY",
}


def normalized_text(value):
    value = str(value).upper()
    for original, replacement in {"\u2014": "-", "\u2013": "-", "\u2018": "'",
                                  "\u2019": "'", "\u201c": '"', "\u201d": '"',
                                  "\u00b7": "-", "\u00a0": " "}.items():
        value = value.replace(original, replacement)
    return value


@lru_cache(maxsize=1)
def fonts():
    small = {}
    rows = (ASSETS / "plate-font.txt").read_text().splitlines()
    for index, row in enumerate(rows):
        if not row.startswith("= "):
            continue
        glyph = Image.new("RGBA", (5, 9))
        draw = ImageDraw.Draw(glyph)
        for y, bits in enumerate(rows[index + 1:index + 10]):
            for x, bit in enumerate(bits[:5]):
                if bit == "#":
                    draw.point((x, y), fill=(*CREAM, 255))
        small[row[2:]] = glyph
    large = {file.stem: Image.open(file).convert("RGBA")
             for file in (ASSETS / "glyphs").glob("?.png")}
    return small, large


def text_picture(text, scale=1, color=CREAM, large=False):
    text = normalized_text(text)
    font = fonts()[1 if large else 0]
    spacing = 2 if large else 1
    space = 10 if large else 6
    missing = set(text) - set(font) - {" "}
    if missing:
        raise ValueError(f"Unsupported ROM plate glyphs {sorted(missing)} in {text!r}")
    width = max(1, sum(space if c == " " else font[c].width + spacing
                       for c in text) - spacing)
    height = max((font[c].height for c in text if c != " "), default=9)
    result = Image.new("RGBA", (width, height))
    x = 0
    for c in text:
        if c == " ":
            x += space
            continue
        glyph = font[c]
        ink = Image.new("RGBA", glyph.size, (*color, 255))
        ink.putalpha(glyph.getchannel("A"))
        result.alpha_composite(ink, (x, 0))
        x += glyph.width + spacing
    if scale != 1:
        result = result.resize((width * scale, height * scale), Image.Resampling.NEAREST)
    return result


def draw_text(canvas, text, xy, scale=1, color=CREAM, max_width=None, center=False,
              large=False):
    picture = text_picture(text, scale, color, large)
    while max_width is not None and picture.width > max_width and scale > 1:
        scale -= 1
        picture = text_picture(text, scale, color, large)
    if max_width is not None and picture.width > max_width:
        raise ValueError(f"Text exceeds its fixed plate: {text!r}")
    x, y = xy
    if center:
        x -= picture.width // 2
    canvas.paste(picture, (x, y), picture)


def wrap(text, max_width, scale=1, max_lines=2):
    words = normalized_text(text).split()
    lines, current = [], ""
    for word in words:
        proposed = f"{current} {word}".strip()
        if text_picture(proposed, scale).width <= max_width:
            current = proposed
        else:
            if not current:
                raise ValueError(f"Word exceeds its fixed label: {word!r}")
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        raise ValueError(f"Label exceeds {max_lines} lines: {text!r}")
    return lines


def cell(index):
    if not 0 <= index < 48:
        raise ValueError("The fixed gallery has 48 cells")
    if index < 36:
        col, row = 8 + index % 4, index // 4
    elif index < 44:
        col, row = index - 36, 7
    else:
        col, row = index - 44, 8
    return (28 + STEP_X * col, 40 + STEP_Y * row, CELL_W, CELL_H)


def inherited():
    if LEASE is None or INHERITED is None:
        raise RuntimeError("Media subprocess attempted without shared admission")
    return INHERITED(LEASE)


def launch(command, **kwargs):
    child = subprocess.Popen(list(map(str, command)), start_new_session=True,
                             **inherited(), **kwargs)
    PROCESSES.add(child)
    return child


def stop(child):
    if child.poll() is None:
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
    PROCESSES.discard(child)


def run(command):
    child = launch(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output, error = child.communicate()
        if child.returncode:
            raise RuntimeError(error.decode(errors="replace")[-4000:])
        return output
    finally:
        stop(child)


@lru_cache(maxsize=128)
def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", path]))


def option(command, flag, default):
    return command[command.index(flag) + 1] if flag in command else default


def source_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(TASK.resolve()) or not path.is_file():
        raise ValueError(f"Source must be an existing master inside this media task: {value}")
    return path


def integer(raw, key, default=None):
    value = raw.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer, got {value!r}")
    return value


def build_plan(file):
    original = json.loads(file.read_text())
    config = original if isinstance(original, dict) else {}
    entries = original.get("cards", []) if isinstance(original, dict) else original
    if not isinstance(entries, list) or not 1 <= len(entries) <= 48:
        raise ValueError("cards.json must contain 1..48 card entries")
    intro = integer(config, "intro_frames", 240)
    end = integer(config, "end_frames", 360)
    if intro < TRANSITION or end < TRANSITION:
        raise ValueError("Intro and end must each retain the 18-frame dissolve")
    result, effects, start = [], set(), intro
    for index, raw in enumerate(entries):
        if raw.get("qualified") is not True:
            raise ValueError(f"Card {index + 1} is not qualified: {raw.get('effect')}")
        effect = raw["effect"]
        if not isinstance(effect, str) or not effect or effect in effects:
            raise ValueError(f"Missing or repeated effect ID: {effect!r}")
        effects.add(effect)
        path = source_path(raw["source"])
        metadata_file = path.parent / "provenance.json"
        states_file = path.parent / "output/state.csv"
        if not metadata_file.is_file() or not states_file.is_file():
            raise ValueError(f"Source provenance/state CSV missing: {path}")
        metadata = json.loads(metadata_file.read_text())
        states = list(csv.DictReader(states_file.open()))
        info = probe(str(path))
        video = next(s for s in info["streams"] if s["codec_type"] == "video")
        if (video["width"], video["height"]) != SOURCE_SIZE:
            raise ValueError(f"Expected native 400x224 master: {path}")
        if Fraction(video["r_frame_rate"]) != FPS or Fraction(video["avg_frame_rate"]) != FPS:
            raise ValueError(f"Expected native 60 Hz master: {path}")
        count = integer(metadata, "frames")
        if count != len(states):
            raise ValueError(f"CSV/provenance frame count differs: {path}: {len(states)} != {count}")
        if float(info["format"]["duration"]) * FPS + 1 < count:
            raise ValueError(f"Master duration is shorter than captured frame count: {path}")
        begin = integer(raw, "in_frame")
        clip = integer(raw, "clip_frames")
        slot = integer(raw, "slot_frames", clip + TRANSITION)
        offset = slot - clip
        if offset not in (0, TRANSITION) or clip < 2 * TRANSITION:
            raise ValueError(f"Card {effect}: slot must equal clip or clip+18; clip must be >=36")
        if begin < 0 or begin + clip > count:
            raise ValueError(f"Source interval outside EOF: {effect}: {begin}+{clip}/{count}")
        visible = states[begin:begin + clip]
        if any(int(row["frame"]) != begin + age for age, row in enumerate(visible)):
            raise ValueError(f"Noncontiguous source CSV: {effect}")
        ghost = index == len(entries) - 1 and effect == "soz-ghost-party"
        allow_death = raw.get("allow_death") is True
        source_audio = raw.get("source_audio") is True
        if (allow_death or source_audio) and not ghost:
            raise ValueError("Only the final soz-ghost-party card may retain death/source audio")
        if any(row.get("dead") == "1" for row in visible) and not allow_death:
            raise ValueError(f"Unexpected death inside {effect}")
        if source_audio and not any(s["codec_type"] == "audio" for s in info["streams"]):
            raise ValueError(f"Ghost master has no retained PCM: {path}")
        command = metadata.get("command", [])
        native_zone = str(option(command, "--zone", metadata.get("zone", "aiz"))).lower()
        native_act = str(option(command, "--act", metadata.get("act", 1)))
        native_game = option(command, "--game", "s3k")
        if native_game != "s3k" or native_zone not in ZONE_NAMES:
            raise ValueError(f"Unexpected game/zone provenance: {effect}: {native_game}/{native_zone}")
        if metadata.get("effect") != effect:
            raise ValueError(f"Effect/provenance mismatch: {effect}/{metadata.get('effect')}")
        label, declared_zone = str(raw["label"]), str(raw["zone"])
        zone = f"{ZONE_NAMES[native_zone]} ZONE - ACT {native_act}"
        # The display always comes from captured provenance, never an invented
        # editorial act name. Retain the caller's zone alongside it for auditing.
        canonical = "".join(c for c in normalized_text(declared_zone) if c.isalnum())
        permitted = {f"{native_zone.upper()}{native_act}",
                     "".join(c for c in zone if c.isalnum()),
                     "".join(c for c in f"{ZONE_NAMES[native_zone]} ACT {native_act}" if c.isalnum()),
                     "".join(c for c in f"{ZONE_NAMES[native_zone]} {native_act}" if c.isalnum())}
        if canonical not in permitted:
            raise ValueError(f"Zone label differs from source provenance: {declared_zone!r}/{zone!r}")
        thumb = integer(raw, "thumb_frame", begin + clip - 1)
        if not begin <= thumb < begin + clip:
            raise ValueError(f"Representative thumbnail is outside the chosen source clip: {effect}")
        caption = str(raw.get("caption", ""))
        text_picture(label)
        wrap(label, 136)
        text_picture(zone)
        if caption:
            if text_picture(caption, 2).width > 824:
                raise ValueError(f"Caption exceeds fixed plate: {caption!r}")
        result.append(dict(index=index, effect=effect, label=label, zone=zone,
                           declared_zone=declared_zone, native_zone=native_zone,
                           native_act=native_act, source=os.path.relpath(path, ROOT),
                           source_path=str(path), source_commit=metadata.get("sourceCommit"),
                           setup=metadata.get("setup"), character=option(command, "--main", "sonic"),
                           sidekick=option(command, "--sidekick", "none"),
                           in_frame=begin, out_frame=begin + clip, clip_frames=clip,
                           slot_frames=slot, clip_offset_frames=offset, thumb_frame=thumb,
                           caption=caption, qualified=True, allow_death=allow_death,
                           source_audio=source_audio, cell=list(cell(index)),
                           output_start_frame=start, output_end_frame=start + slot,
                           clip_output_start_frame=start + offset,
                           death_source_frames=[int(row["frame"]) for row in visible if row.get("dead") == "1"],
                           source_frames=count))
        start += slot
    return dict(width=W, height=H, fps=FPS, intro_frames=intro, end_frames=end,
                total_frames=start + end, end_start_frame=start, cards=result,
                qualified_effect_count=len(effects), captured_zones=sorted({c["native_zone"] for c in result}),
                layout="still gallery; one continuous moving card; frozen accumulated thumbnails",
                audio_policy="continuous ROM bed; final ghost card retains recorded mixed PCM; no synthetic ghost cue")


def write_plan(plan):
    OUT.mkdir(exist_ok=True)
    (OUT / "edit-timeline.json").write_text(json.dumps(plan, indent=2) + "\n")
    with (OUT / "chapters.csv").open("w", newline="") as file:
        fields = ["index", "effect", "label", "zone", "source", "in_frame", "out_frame",
                  "output_start_frame", "output_end_frame", "clip_output_start_frame", "qualified"]
        writer = csv.DictWriter(file, fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(plan["cards"])
    print(f"{plan['qualified_effect_count']} qualified effects, {len(plan['captured_zones'])} zones, "
          f"{plan['total_frames']} frames / {plan['total_frames'] / FPS:.3f}s", flush=True)


def read_exact(pipe, size):
    chunks, remaining = [], size
    while remaining:
        data = pipe.read(remaining)
        if not data:
            raise ValueError(f"Unexpected decoder EOF ({size - remaining}/{size} bytes)")
        chunks.append(data)
        remaining -= len(data)
    return b"".join(chunks)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def video_inputs(plan):
    """Production input identity; not a cached verification/pass receipt."""
    return dict(plan_sha256=hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest(),
                renderer_sha256=sha256(Path(__file__)),
                sources={card["source"]: sha256(card["source_path"]) for card in plan["cards"]})


class Reader:
    def __init__(self, card):
        self.card = card
        self.age = -1
        self.last = None
        self.process = launch(["ffmpeg", "-nostdin", "-loglevel", "error", "-threads", "1",
                               "-i", card["source_path"],
                               "-map", "0:v:0", "-frames:v", card["clip_frames"], "-an",
                               "-vf", f"trim=start_frame={card['in_frame']}:end_frame={card['out_frame']},setpts=PTS-STARTPTS",
                               "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def frame(self, age):
        if not self.age <= age < self.card["clip_frames"]:
            raise ValueError("Decoder age must move forward inside the qualified clip")
        while self.age < age:
            self.last = Image.frombytes("RGB", SOURCE_SIZE,
                                        read_exact(self.process.stdout, 400 * 224 * 3))
            self.age += 1
        return self.last

    def close(self):
        if self.process.stdout:
            self.process.stdout.close()
        stop(self.process)


@lru_cache(maxsize=128)
def source_picture(source, frame):
    path = Path(source)
    png = path.parent / "output/frames" / f"{frame:05d}.png"
    if png.is_file():
        with Image.open(png) as image:
            result = image.convert("RGB")
        if result.size != SOURCE_SIZE:
            raise ValueError(f"Retained native PNG has the wrong dimensions: {png}")
        return result
    output = run(["ffmpeg", "-nostdin", "-loglevel", "error", "-threads", "1",
                  "-i", path, "-map", "0:v:0", "-frames:v", "1",
                  "-vf", f"trim=start_frame={frame}:end_frame={frame + 1},setpts=PTS-STARTPTS",
                  "-an", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"])
    if len(output) != 400 * 224 * 3:
        raise ValueError(f"Representative frame decode failed: {source}:{frame}")
    return Image.frombytes("RGB", SOURCE_SIZE, output)


@lru_cache(maxsize=1)
def background():
    canvas = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        fade = min(1, abs(y - H / 2) / (H / 2))
        color = tuple(round(value - fade * 3) for value in NAVY)
        draw.line((0, y, W - 1, y), fill=color)
    for index in range(48):
        x, y, w, h = cell(index)
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=OUTLINE)
    x, y, width = 28 + 4 * STEP_X, 40 + 8 * STEP_Y, 4 * STEP_X - 8
    draw.rectangle((x, y, x + width - 1, y + CELL_H - 1), fill=PANEL, outline=OUTLINE)
    # The ROM plate face has no '+' glyph. Keep plain supported letters.
    draw_text(canvas, "57 MORE IN THE POOL", (x + width // 2, y + 36),
              scale=4, color=PALE, max_width=width - 32, center=True)
    return canvas


def thumbnail(card, newest=False):
    canvas = Image.new("RGB", (CELL_W, CELL_H), PANEL)
    picture = source_picture(card["source_path"], card["thumb_frame"])
    picture = picture.resize((100, 56), Image.Resampling.NEAREST)
    canvas.paste(picture, (24, 8))
    for line, value in enumerate(wrap(card["label"], 136)):
        draw_text(canvas, value, (CELL_W // 2, 72 + line * 12), center=True)
    ImageDraw.Draw(canvas).rectangle((0, 0, CELL_W - 1, CELL_H - 1),
                                    outline=GOLD if newest else OUTLINE,
                                    width=2 if newest else 1)
    return canvas


def gallery(plan, completed):
    canvas = background().copy()
    for index in range(completed):
        card = plan["cards"][index]
        canvas.paste(thumbnail(card, newest=index == completed - 1), card["cell"][:2])
    return canvas


def label_plate(card, count, caption=False):
    panel = Image.new("RGB", PLATE[2:], PANEL)
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, 0, panel.width - 1, panel.height - 1), outline=GOLD, width=2)
    draw_text(panel, card["label"], (20, 12), scale=5, max_width=824)
    draw_text(panel, f"{card['index'] + 1:02d} / {count:02d}", (1032, 10),
              scale=3, color=GOLD, center=True)
    zone_lines = [ZONE_NAMES[card["native_zone"]] + " ZONE", "ACT " + card["native_act"]]
    for line, text in enumerate(zone_lines):
        draw_text(panel, text, (1032, 41 + line * 20), scale=2, color=PALE, center=True)
    if caption and card["caption"]:
        draw_text(panel, card["caption"], (20, 62), scale=2, color=PALE, max_width=824)
    return panel


def title_stage(plan, end=False):
    picture = Image.new("RGB", ACTIVE[2:], NAVY)
    middle = picture.width // 2
    draw_text(picture, "SONIC3K", (middle, 98), scale=5, color=GOLD, center=True)
    draw_text(picture, "CHAOS", (middle, 200), scale=4, large=True, max_width=1000, center=True)
    draw_text(picture, "MODE", (middle, 354), scale=4, large=True, max_width=1000, center=True)
    if end:
        lines = ["105 EFFECTS. CHOOSE YOUR POOL.", "AN OPENGGF MOD.",
                 "REQUIRES YOUR OWN SONIC 3 & KNUCKLES ROM."]
    else:
        lines = [f"{len(plan['cards'])} EFFECTS. ONE AT A TIME, FOR ONCE.",
                 f"{len(plan['captured_zones'])} ZONES. ONE STABLE PAGE."]
    for index, line in enumerate(lines):
        draw_text(picture, line, (middle, 510 + index * 45), scale=3,
                  color=CREAM if index == 0 else PALE, max_width=1100, center=True)
    return picture


def paste_stage(canvas, picture):
    canvas.paste(picture, ACTIVE[:2])
    x, y, w, h = ACTIVE
    ImageDraw.Draw(canvas).rectangle((x - 2, y - 2, x + w + 1, y + h + 1),
                                    outline=GOLD, width=2)


class GalleryRenderer:
    def __init__(self, plan):
        self.plan = plan
        self.current = None
        self.reader = None
        self.base = gallery(plan, 0)
        self.previous_stage = title_stage(plan)
        self.intro_stage = self.previous_stage
        self.end_stage = title_stage(plan, end=True)
        self.previous_plate = Image.new("RGB", PLATE[2:], NAVY)
        self.plate_cache = {}
        self.previous_card = None

    def close(self):
        if self.reader:
            self.reader.close()
            self.reader = None

    def enter(self, index, decode=True):
        self.close()
        self.current = index
        self.base = gallery(self.plan, index)
        if index:
            previous = self.plan["cards"][index - 1]
            self.previous_stage = source_picture(previous["source_path"], previous["out_frame"] - 1).resize(
                ACTIVE[2:], Image.Resampling.NEAREST)
            self.previous_plate = label_plate(previous, len(self.plan["cards"]), caption=True)
        if decode and index < len(self.plan["cards"]):
            self.reader = Reader(self.plan["cards"][index])

    def frame(self, output_frame, static=False):
        plan = self.plan
        if not 0 <= output_frame < plan["total_frames"]:
            raise ValueError("Preview frame lies outside output")
        if output_frame < plan["intro_frames"]:
            canvas = gallery(plan, 0)
            picture = self.intro_stage
            alpha = min(1, (output_frame + 1) / TRANSITION)
            paste_stage(canvas, Image.blend(Image.new("RGB", ACTIVE[2:], NAVY), picture, alpha))
            return canvas
        if output_frame >= plan["end_start_frame"]:
            index, age = len(plan["cards"]), output_frame - plan["end_start_frame"]
            if self.current != index:
                self.enter(index, decode=False)
            canvas = self.base.copy()
            alpha = min(1, (age + 1) / TRANSITION)
            if alpha < 1:
                previous = plan["cards"][-1]
                x, y, width, height = previous["cell"]
                empty = background().crop((x, y, x + width, y + height))
                canvas.paste(Image.blend(empty, thumbnail(previous, newest=True), alpha), (x, y))
            paste_stage(canvas, Image.blend(self.previous_stage, self.end_stage, alpha))
            canvas.paste(Image.blend(self.previous_plate, Image.new("RGB", PLATE[2:], NAVY), alpha), PLATE[:2])
            return canvas
        index = next(c["index"] for c in plan["cards"]
                     if c["output_start_frame"] <= output_frame < c["output_end_frame"])
        card = plan["cards"][index]
        if self.current != index:
            self.enter(index, decode=not static)
        age = output_frame - card["output_start_frame"]
        source_age = age - card["clip_offset_frames"]
        canvas = self.base.copy()
        # An arriving thumbnail fades in at its final cell. It never flies/slides
        # across the stage, and all previous pictures remain absolutely still.
        alpha = min(1, (age + 1) / TRANSITION)
        if index and alpha < 1:
            previous = plan["cards"][index - 1]
            x, y, width, height = previous["cell"]
            empty = background().crop((x, y, x + width, y + height))
            canvas.paste(Image.blend(empty, thumbnail(previous, newest=True), alpha), (x, y))
        if source_age < 0:
            # Reserved transition frames contain only two stationary pictures.
            # Native progression starts at the exact clip_output_start_frame.
            incoming = source_picture(card["source_path"], card["in_frame"]).resize(
                ACTIVE[2:], Image.Resampling.NEAREST)
            stage = Image.blend(self.previous_stage, incoming, alpha)
        else:
            if static:
                source = source_picture(card["source_path"], card["in_frame"] + source_age)
            else:
                if self.reader is None:
                    self.reader = Reader(card)
                source = self.reader.frame(source_age)
            stage = source.resize(ACTIVE[2:], Image.Resampling.NEAREST)
            if card["clip_offset_frames"] == 0 and source_age < TRANSITION:
                stage = Image.blend(self.previous_stage, stage, min(1, (source_age + 1) / TRANSITION))
        paste_stage(canvas, stage)
        key = (index, age >= FPS)
        if key not in self.plate_cache:
            self.plate_cache[key] = label_plate(card, len(plan["cards"]), caption=age >= FPS)
        panel = self.plate_cache[key]
        if alpha < 1:
            panel = Image.blend(self.previous_plate, panel, alpha)
        canvas.paste(panel, PLATE[:2])
        return canvas


def encode_video(plan, destination):
    identity = video_inputs(plan)
    child = launch(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo",
                    "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", FPS, "-i", "pipe:0",
                    "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-threads", "2", "-movflags", "+faststart", destination],
                   stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    renderer = GalleryRenderer(plan)
    try:
        starts = {card["output_start_frame"]: card for card in plan["cards"]}
        for frame in range(plan["total_frames"]):
            if frame in starts:
                card = starts[frame]
                print(f"card {card['index'] + 1:02d}: {card['label']} / {card['zone']}", flush=True)
            child.stdin.write(renderer.frame(frame).tobytes())
        child.stdin.close()
        child.stdin = None
        _, error = child.communicate()
        if child.returncode:
            raise RuntimeError(error.decode(errors="replace")[-4000:])
        identity["video_sha256"] = sha256(destination)
        (WORK / "gallery-video-inputs.json").write_text(json.dumps(identity, indent=2) + "\n")
    finally:
        renderer.close()
        stop(child)


def audio_configuration(plan):
    file = ROOT / "audio.json"
    config = json.loads(file.read_text()) if file.is_file() else {}
    bed = source_path(config.get("bed", "../revision-2/assets/hcz2-bed.wav"))
    info = probe(str(bed))
    stream = next(s for s in info["streams"] if s["codec_type"] == "audio")
    duration = float(info["format"]["duration"])
    loop = config.get("bed_loop")
    total = plan["total_frames"] / FPS
    if loop:
        if not isinstance(loop, dict) or loop.get("qualified") is not True:
            raise ValueError("Short-bed looping requires lead-qualified native loop boundaries")
        begin, end = integer(loop, "start_sample"), integer(loop, "end_sample")
        if not 0 <= begin < end <= math.floor(duration * int(stream["sample_rate"])):
            raise ValueError("Qualified bed loop lies outside the rendered PCM")
    elif duration + 1 / FPS < total:
        raise ValueError(f"Music bed is {duration:.3f}s but movie is {total:.3f}s; provide a full native render "
                         "or a qualified bed_loop, not an arbitrary file repeat")
    ghosts = [c for c in plan["cards"] if c["source_audio"]]
    if len(ghosts) != 1 or ghosts[0]["index"] != len(plan["cards"]) - 1:
        raise ValueError("Final ghost card must explicitly retain its recorded PCM")
    return config, bed, ghosts[0]


def finish_audio(plan, video, destination):
    config, bed, ghost = audio_configuration(plan)
    total = plan["total_frames"] / FPS
    start = ghost["clip_output_start_frame"] / FPS
    end = (ghost["clip_output_start_frame"] + ghost["clip_frames"]) / FPS
    duck = integer(config, "ghost_duck_frames", 60) / FPS
    return_time = integer(config, "bed_return_frames", 30) / FPS
    if duck <= 0 or return_time <= 0:
        raise ValueError("Bed duck/return must be positive")
    bed_gain = 10 ** (float(config.get("bed_gain_db", -3)) / 20)
    ghost_gain = 10 ** (float(config.get("ghost_gain_db", 0)) / 20)
    master_gain = 10 ** (float(config.get("master_gain_db", 0)) / 20)
    limiter = float(config.get("true_peak_linear", .84))
    if not 0 < limiter <= .84:
        raise ValueError("Configured limiter exceeds the -1.5dB headroom limit")
    inputs = ["-i", str(video), "-i", str(bed), "-i", ghost["source_path"]]
    loop = config.get("bed_loop")
    loop_filter = (f"atrim=start_sample={loop['start_sample']}:end_sample={loop['end_sample']},"
                   f"asetpts=PTS-STARTPTS,aloop=loop=-1:size={loop['end_sample'] - loop['start_sample']},") if loop else ""
    volume = (f"if(lt(t,{start - duck}),1,if(lt(t,{start}),({start}-t)/{duck},"
              f"if(lt(t,{end}),0,min(1,(t-{end})/{return_time}))))")
    fade = min(integer(config, "end_fade_frames", 180) / FPS, plan["end_frames"] / FPS)
    graph = (f"[1:a]{loop_filter}aresample={SR},atrim=duration={total},asetpts=PTS-STARTPTS,"
             f"volume={bed_gain},volume='{volume}':eval=frame,"
             f"afade=t=out:st={total - fade}:d={fade},apad=whole_dur={total}[bed]")
    ghost_duration = ghost["clip_frames"] / FPS
    fade_in = integer(config, "ghost_fade_in_frames", 6) / FPS
    fade_out = integer(config, "ghost_fade_out_frames", 30) / FPS
    if not 0 <= fade_in <= ghost_duration or not 0 <= fade_out <= ghost_duration:
        raise ValueError("Ghost fades exceed actual retained clip duration")
    graph += (f";[2:a]aresample={SR},atrim=start_sample={ghost['in_frame'] * (SR // FPS)}:"
              f"end_sample={ghost['out_frame'] * (SR // FPS)},asetpts=PTS-STARTPTS,volume={ghost_gain},"
              f"afade=t=in:st=0:d={fade_in},afade=t=out:st={ghost_duration - fade_out}:d={fade_out},"
              f"adelay={round(start * SR)}S:all=1[ghost]")
    labels = ["[bed]", "[ghost]"]
    applied = []
    # Optional cues must identify an actual source frame inside the chosen card.
    # This is explicit editorial audio, never represented as isolated capture PCM.
    for number, cue in enumerate(config.get("cues", [])):
        card = next((c for c in plan["cards"] if c["effect"] == cue.get("effect")), None)
        event = integer(cue, "source_frame")
        if card is None or not card["in_frame"] <= event < card["out_frame"] or not cue.get("reason"):
            raise ValueError(f"Editorial cue lacks a qualified source event/reason: {cue}")
        file = source_path(cue["file"])
        timestamp = (card["clip_output_start_frame"] + event - card["in_frame"]) / FPS
        gain = 10 ** (float(cue.get("gain_db", 0)) / 20)
        inputs += ["-i", str(file)]
        graph += (f";[{number + 3}:a]asetpts=PTS-STARTPTS,aresample={SR},volume={gain},"
                  f"adelay={round(timestamp * SR)}S:all=1[cue{number}]")
        labels.append(f"[cue{number}]")
        applied.append(dict(cue, output_seconds=timestamp))
    graph += (";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,atrim=duration={total},"
              f"volume={master_gain},alimiter=limit={limiter}:level=false:latency=true,aresample={SR}[mix]")
    metadata = WORK / "chapters.ffmeta"
    text = (";FFMETADATA1\ntitle=Sonic3K Chaos Mode - revision 3\n"
            "comment=Separate qualified captures; final ghost recorded PCM restored.\n"
            f"[CHAPTER]\nTIMEBASE=1/60\nSTART=0\nEND={plan['intro_frames']}\ntitle=Chaos Mode\n")
    for card in plan["cards"]:
        label = card["label"].replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;").replace("#", "\\#")
        text += (f"[CHAPTER]\nTIMEBASE=1/60\nSTART={card['output_start_frame']}\n"
                 f"END={card['output_end_frame']}\ntitle={label}\n")
    text += (f"[CHAPTER]\nTIMEBASE=1/60\nSTART={plan['end_start_frame']}\n"
             f"END={plan['total_frames']}\ntitle=Choose your pool\n")
    metadata.write_text(text)
    inputs += ["-i", str(metadata)]
    temporary = destination.with_name(destination.stem + ".partial" + destination.suffix)
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *inputs,
         "-filter_complex_threads", "1", "-filter_complex", graph, "-map", "0:v:0", "-map", "[mix]",
         "-map_metadata", str(3 + len(applied)), "-map_chapters", str(3 + len(applied)),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", SR, "-ac", "2",
         "-t", f"{total:.9f}", "-movflags", "+faststart", temporary])
    # Both streams must fully decode before replacing an earlier successful output.
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-xerror", "-err_detect", "explode", "-threads", "1", "-i", temporary,
         "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"])
    temporary.replace(destination)
    (OUT / "audio-mix.json").write_text(json.dumps(dict(config, bed=str(bed),
         source_audio_used=True, ghost_source=ghost["source"], ghost_source_start_frame=ghost["in_frame"],
         ghost_source_frames=ghost["clip_frames"], ghost_output_start_frame=ghost["clip_output_start_frame"],
         ghost_audio_policy="actual recorded mixed PCM; gain/fades only; native speed",
         applied_editorial_cues=applied), indent=2) + "\n")


@contextmanager
def admitted(worktree, estimate=600):
    global LEASE, INHERITED
    queue_root = Path(os.environ.get("OPENGGF_QUEUE_ROOT", "/home/farrell/code/projects/OpenGGF"))
    sys.path.insert(0, str(queue_root / "tools/testing"))
    from maven_queue import handle_termination, inherited_slot, maven_slot
    INHERITED = inherited_slot
    with handle_termination():
        with maven_slot(Path(worktree), exclusive=True, estimate=estimate, kind="chaos-card-gallery-media") as lease:
            LEASE = lease
            try:
                yield
            finally:
                # Kill/wait only known owned children before releasing admission.
                for child in list(PROCESSES):
                    stop(child)
                LEASE = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "preview", "render", "audio"])
    parser.add_argument("--cards", type=Path, default=ROOT / "cards.json")
    parser.add_argument("--frames", default="", help="Absolute output frame numbers for bounded PNG previews")
    parser.add_argument("--admission-worktree", type=Path, required=True)
    args = parser.parse_args()
    estimates = {"plan": 10, "preview": 20, "audio": 25, "render": 600}
    with admitted(args.admission_worktree, estimates[args.command]):
        plan = build_plan(args.cards)
        write_plan(plan)
        OUT.mkdir(exist_ok=True)
        WORK.mkdir(exist_ok=True)
        video = WORK / "gallery-video.mp4"
        destination = OUT / "sonic3k-chaos-mode-demo-v3.mp4"
        if args.command == "preview":
            frames = ([int(value) for value in args.frames.split(",")] if args.frames else
                      [0, plan["intro_frames"] + 90,
                       plan["cards"][len(plan["cards"]) // 2]["output_start_frame"] + 90,
                       plan["end_start_frame"] + 90])
            if len(frames) > 12:
                raise ValueError("Preview is bounded to 12 layout PNGs")
            folder = OUT / "previews"
            folder.mkdir(exist_ok=True)
            renderer = GalleryRenderer(plan)
            try:
                for frame in sorted(set(frames)):
                    renderer.frame(frame, static=True).save(folder / f"frame-{frame:06d}.png")
            finally:
                renderer.close()
        elif args.command in ("render", "audio"):
            audio_configuration(plan)  # Fail missing audio prerequisites before expensive encoding.
            if args.command == "render":
                encode_video(plan, video)
            elif not video.is_file():
                raise ValueError("Audio-only assembly requires this revision's previously rendered video")
            else:
                identity_file = WORK / "gallery-video-inputs.json"
                if not identity_file.is_file():
                    raise ValueError("Audio-only assembly lacks original video input identity; render first")
                expected = json.loads(identity_file.read_text())
                actual = dict(video_inputs(plan), video_sha256=sha256(video))
                if expected != actual:
                    raise ValueError("Video/card/source identity changed; audio-only remux cannot reuse stale picture")
            finish_audio(plan, video, destination)
            print(f"Completed {destination} ({destination.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
