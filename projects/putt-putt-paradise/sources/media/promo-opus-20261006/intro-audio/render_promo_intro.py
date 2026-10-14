#!/usr/bin/env python3
"""Render the Putt Putt Paradise public promo: paced cut + cold open + ROM-rendered soundtrack.

INTRO-AUDIO revision (2026-10-06, after "consider an intro to the promo. Fade in? audio?"):
a copy of ../paced/render_promo_paced.py (unchanged) driven by promo-manifest-intro.json.
Adds: an 'intro' segment kind (real footage on black, fade from black, staged two-part line,
dim kicker, no chrome), a 'build' transition (crossfade used where both sides show the same
source frames, so only the surround changes), and an editorial soundtrack mixed with ffmpeg
from Sonic 2 stems that tools/S2PromoAudioRender.java renders from the user's ROM through
OpenGGF's SMPS driver (manifest 'audio'; --audio-dir). Loudness is normalised two-pass
(EBU R128, linear) and the result is muxed as 48 kHz stereo AAC. --no-audio keeps it silent.

--- earlier header (paced cut) ---

Paced cut (2026-10-06, after user feedback "doesn't leave long enough on each
section, very rushed"): a copy of ../render_promo.py (kept unchanged as the
historical 50 s renderer) driven by promo-manifest-paced.json / source-lock-paced.json.
Changes from the original: online card may open with an original lead-in graphic
before its real title clip (lead_graphic frames; footage is never held), engine-card
bullet stagger and end-card ball/CTA timing come from the manifest, and defaults
point at this directory.

Original purpose: a ~50 s, mute-friendly 1920x1080 promo built only from real OpenGGF
engine footage (4x / 3x / 2x nearest-neighbour, original aspect, every output
frame = one 30 fps source frame, i.e. normal speed) plus original geometric
cards, captions and transitions.

Inputs:  promo-manifest.json (edit decision list, native 60 Hz frame ranges),
         source-lock.json (gameplay-state hashes of every selected range),
         --source-root containing <scenario>-<tag>/{gameplay.mkv,title.mkv,
         state.csv,events.csv} for ehz1-sonic-rewind-final, local-two-player-final
         and ehz2-tails-final.
Outputs: <out>.mp4 plus <out>.edl.json, <out>.chapters.csv, <out>.verify.json
         and <out>.cuts.png (contact sheet of every segment start/middle).

Typical use:
  python3 render_promo_paced.py --source-root ROOT --tag v5 --final --out promo-opus-paced.mp4
  python3 render_promo_paced.py --source-root ROOT --tag v5 --check-only   # lock check
  --dir ehz1=/abs/dir overrides a single scenario directory.
  --lock rewrites source-lock.json from the given sources (only do this on purpose).

Originating task: 2026-10-06 Putt Putt Paradise promo (Opus implementation lane).
"""
import argparse, csv, hashlib, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1920, 1080
FPS = 30
NW, NH = 320, 224
GX, GY = 320, 64            # 4x game window origin; window is 1280x896
GW, GH = NW * 4, NH * 4
BAND_Y = GY + GH            # caption band 960..1080

NAVY = (8, 18, 43); NAVY2 = (15, 33, 72); STRIPE = (14, 30, 64)
YELLOW = (255, 210, 63); GREEN = (43, 212, 125); RED = (255, 77, 94)
SKY = (92, 200, 255); WHITE = (245, 247, 255); DIM = (112, 130, 172)

STATE_COLS = ["frame", "character", "act", "x", "y", "xvel", "yvel", "gspeed", "air", "rolling",
              "dead", "cam_x", "cam_y", "stage", "owner", "turn", "score", "status", "input"]


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def ease_out(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


# ----------------------------------------------------------------- sources
class Sources:
    def __init__(self, manifest, root, tag, overrides):
        self.m = manifest
        self.dirs = {}
        for key, s in manifest["sources"].items():
            d = Path(overrides[key]) if key in overrides else Path(root) / s["dir"].format(tag=tag)
            self.dirs[key] = d.resolve()
        self.cache = {}

    def path(self, key, which):
        return self.dirs[key] / self.m["sources"][key][which]

    def state_rows(self, key):
        with open(self.dirs[key] / "state.csv", newline="") as f:
            return {int(r["frame"]): r for r in csv.DictReader(f)}

    def events_text(self, key):
        return (self.dirs[key] / "events.csv").read_text()

    def decode(self, key, which, start, end):
        """Return PIL frames [start,end) of the source video (mkv frame indices)."""
        k = (key, which, start, end)
        if k not in self.cache:
            cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(self.path(key, which)), "-vf",
                   f"trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS",
                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
            data = subprocess.run(cmd, check=True, capture_output=True).stdout
            n = len(data) // (NW * NH * 3)
            if n != end - start:
                sys.exit(f"decode {key}/{which} [{start},{end}) gave {n} frames")
            self.cache[k] = [Image.frombytes("RGB", (NW, NH), data[i * NW * NH * 3:(i + 1) * NW * NH * 3])
                             for i in range(n)]
        return self.cache[k]

    def native_clip(self, key, a, b):
        if a % 2 or b % 2 or a >= b:
            sys.exit(f"native range {key} [{a},{b}) must be even and non-empty")
        return self.decode(key, "video", a // 2, b // 2)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                          "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,codec_name",
                          "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    return json.loads(out)["streams"][0]


def native_ranges(manifest):
    """(segment id, role, src, a, b) for every gameplay range in the edit."""
    out = []
    for s in manifest["segments"]:
        if s["kind"] in ("game", "intro"):
            out.append((s["id"], "main", s["src"], *s["native"]))
        elif s["kind"] == "split":
            for side in ("left", "right"):
                out.append((s["id"], side, s[side]["src"], *s[side]["native"]))
        elif s["kind"] == "engine":
            out.append((s["id"], "mini", s["mini"]["src"], *s["mini"]["native"]))
    return out


def range_hash(rows, a, b):
    h = hashlib.sha256()
    for f in range(a, b):
        r = rows.get(f)
        if r is None:
            return None
        h.update(("|".join(r.get(c, "") for c in STATE_COLS) + "\n").encode())
    return h.hexdigest()


def validate_sources(manifest, src, lock_path, write_lock, allow_drift):
    report = {"sources": {}, "ranges": [], "lock": str(lock_path)}
    for key, s in manifest["sources"].items():
        d = src.dirs[key]
        for f in ("state.csv", "events.csv", s["video"], s["title"]):
            if not (d / f).exists():
                sys.exit(f"missing {d / f}")
        v, t = probe(src.path(key, "video")), probe(src.path(key, "title"))
        for name, p in (("video", v), ("title", t)):
            if (p["width"], p["height"], p["r_frame_rate"]) != (NW, NH, "30/1"):
                sys.exit(f"{key}/{name}: unexpected stream {p}")
        rows = src.state_rows(key)
        info = {"dir": str(d), "video_frames": int(v["nb_read_frames"]), "title_frames": int(t["nb_read_frames"]),
                "state_rows": len(rows), "events_sha256": hashlib.sha256(src.events_text(key).encode()).hexdigest()}
        if info["video_frames"] != (len(rows) + 1) // 2:
            sys.exit(f"{key}: {info['video_frames']} video frames vs {len(rows)} native state rows (expected ceil(rows/2))")
        prov = d / "provenance.json"
        if prov.exists():
            info["provenance"] = json.loads(prov.read_text())
        report["sources"][key] = info
    lock = json.loads(lock_path.read_text()) if lock_path.exists() and not write_lock else None
    new_lock = {"columns": STATE_COLS, "events": {}, "ranges": {}}
    problems = []
    for key in manifest["sources"]:
        new_lock["events"][key] = report["sources"][key]["events_sha256"]
        if lock and lock["events"].get(key) != new_lock["events"][key]:
            problems.append(f"{key}: events.csv differs from lock")
    for sid, role, key, a, b in native_ranges(manifest):
        rows = src.state_rows(key)
        hsh = range_hash(rows, a, b)
        if hsh is None:
            problems.append(f"{sid}/{role}: native [{a},{b}) outside {key} state.csv")
        name = f"{sid}/{role}"
        new_lock["ranges"][name] = {"src": key, "native": [a, b], "sha256": hsh}
        ok = (lock is None) or (lock["ranges"].get(name, {}).get("sha256") == hsh)
        if not ok:
            problems.append(f"{name}: gameplay state in {key} native [{a},{b}) differs from lock")
        stages = []
        for f in range(a, b):
            st = rows[f]["stage"] if f in rows else "?"
            if not stages or stages[-1][0] != st:
                stages.append([st, f])
        report["ranges"].append({"segment": sid, "role": role, "src": key, "native": [a, b],
                                 "mkv_frames": [a // 2, b // 2], "seconds": [a / 60, b / 60],
                                 "stage_changes": stages, "state_sha256": hsh, "matches_lock": ok})
    if write_lock:
        lock_path.write_text(json.dumps(new_lock, indent=2) + "\n")
        print(f"wrote {lock_path}")
    elif lock is None:
        problems.append(f"no lock file {lock_path}; run once with --lock on the reference sources")
    report["problems"] = problems
    if problems:
        print("SOURCE CHECK:\n  " + "\n  ".join(problems))
        if not allow_drift:
            sys.exit("source timeline differs from the edit lock; re-cut the edit or pass --allow-state-drift")
    else:
        print("source check: all selected gameplay ranges match the lock")
    return report


# ----------------------------------------------------------------- drawing
class Fonts:
    def __init__(self, paths):
        self.paths = paths
        self.c = {}

    def __call__(self, name, size):
        k = (name, size)
        if k not in self.c:
            self.c[k] = ImageFont.truetype(self.paths[name], size)
        return self.c[k]


def parse_marked(text):
    """'a *b* c' -> [('a ', False), ('b', True), (' c', False)]"""
    parts, acc = [], False
    for i, chunk in enumerate(text.split("*")):
        if chunk:
            parts.append((chunk, i % 2 == 1))
    return parts


def draw_marked(draw, xy, text, font, color=WHITE, accent=YELLOW, anchor_center=True, shadow=True):
    parts = parse_marked(text)
    width = sum(font.getlength(t) for t, _ in parts)
    x, y = xy
    if anchor_center:
        x -= width / 2
    for t, acc in parts:
        if shadow:
            draw.text((x + 4, y + 5), t, font=font, fill=(3, 8, 20, 255))
        draw.text((x, y), t, font=font, fill=accent if acc else color)
        x += font.getlength(t)
    return width


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def with_alpha(layer, k):
    if k >= 0.999:
        return layer
    out = layer.copy()
    a = out.getchannel("A").point(lambda v: int(v * k))
    out.putalpha(a)
    return out


def golf_ball(draw, cx, cy, r, fill=WHITE):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    for dx, dy in ((-0.35, -0.3), (0.2, -0.45), (0.4, 0.05), (-0.1, 0.1), (-0.45, 0.3), (0.15, 0.45)):
        rr = max(2, r * 0.11)
        x, y = cx + dx * r, cy + dy * r
        draw.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(206, 214, 232))


def flag(draw, x, y, h, color=RED):
    draw.rectangle((x, y, x + max(3, h // 16), y + h), fill=WHITE)
    draw.polygon([(x + 4, y), (x + 4 + h * 0.55, y + h * 0.17), (x + 4, y + h * 0.34)], fill=color)


class Renderer:
    def __init__(self, manifest, src, draft_label):
        self.m = manifest
        self.src = src
        self.F = Fonts(manifest["fonts"])
        self.draft = draft_label
        self.features = manifest["features"]
        self._bg_tile = self._make_bg()
        self._layer_cache = {}

    # background -------------------------------------------------------
    def _make_bg(self):
        period = 96
        im = Image.new("RGB", (W + period, H), NAVY)
        d = ImageDraw.Draw(im)
        for y in range(H):  # vertical gradient
            k = y / H
            c = tuple(int(NAVY[i] * (1 - k) + NAVY2[i] * k) for i in range(3))
            d.line((0, y, W + period, y), fill=c)
        for x in range(-H, W + period + H, period):
            d.polygon([(x, 0), (x + 30, 0), (x + 30 - H, H), (x - H, H)], fill=STRIPE)
        return im

    def background(self, t):
        off = int(t * 1.5) % 96
        return self._bg_tile.crop((off, 0, off + W, H)).copy()

    def top_bar(self, frame):
        d = ImageDraw.Draw(frame, "RGBA")
        d.rectangle((0, 0, W, GY - 1), fill=(5, 11, 28, 255))
        d.rectangle((0, GY - 4, W, GY - 1), fill=GREEN)
        flag(d, 30, 14, 36)
        d.text((62, 12), "PUTT PUTT PARADISE", font=self.F("heavy", 36), fill=YELLOW)
        d.text((62 + self.F("heavy", 36).getlength("PUTT PUTT PARADISE") + 18, 20), "Sonic 2 Mini Golf  ·  OpenGGF mod", font=self.F("medium", 24), fill=DIM)
        right = "Real engine footage  ·  normal speed"
        f = self.F("medium", 24)
        d.text((W - 30 - f.getlength(right), 20), right, font=f, fill=WHITE)
        if self.draft:
            f2 = self.F("semi", 24)
            tw = f2.getlength(self.draft)
            x0 = W / 2 - tw / 2 - 18 + 120
            d.rounded_rectangle((x0, 12, x0 + tw + 36, 50), 19, fill=RED)
            d.text((x0 + 18, 17), self.draft, font=f2, fill=WHITE)

    # caption band ------------------------------------------------------
    def caption_layer(self, cap):
        key = ("cap", cap.get("headline"), cap.get("sub"), cap.get("size"))
        if key not in self._layer_cache:
            L = Image.new("RGBA", (W, H - BAND_Y), (0, 0, 0, 0))
            d = ImageDraw.Draw(L)
            size = cap.get("size", 66)
            if cap.get("sub"):
                draw_marked(d, (W / 2, 0), cap["headline"], self.F("heavy", size - 8))
                f = self.F("semi", 28)
                d.text((W / 2 - f.getlength(cap["sub"]) / 2, size - 2), cap["sub"], font=f, fill=SKY)
            else:
                f = self.F("heavy", size)
                draw_marked(d, (W / 2, (H - BAND_Y - size * 1.2) / 2 - 4), cap["headline"], f)
            self._layer_cache[key] = L
        return self._layer_cache[key]

    def card_layer(self, card):
        key = ("card", card["num"], card["title"], card["body"])
        if key not in self._layer_cache:
            L = Image.new("RGBA", (300, 520), (0, 0, 0, 0))
            d = ImageDraw.Draw(L)
            d.rounded_rectangle((0, 0, 279, 500), 22, fill=(5, 11, 28, 230), outline=GREEN, width=3)
            golf_ball(d, 70, 78, 46)
            fn = self.F("heavy", 50)
            d.text((70 - fn.getlength(card["num"]) / 2, 50), card["num"], font=fn, fill=NAVY)
            ft = self.F("heavy", 52)
            y = 146
            for line in wrap(card["title"], ft, 240):
                d.text((24, y), line, font=ft, fill=YELLOW)
                y += 56
            d.rectangle((24, y + 8, 84, y + 13), fill=GREEN)
            fb = self.F("book", 30)
            y += 30
            for line in wrap(card["body"], fb, 236):
                d.text((24, y), line, font=fb, fill=WHITE)
                y += 38
            self._layer_cache[key] = L
        return self._layer_cache[key]

    def tracker(self, frame, active, done):
        d = ImageDraw.Draw(frame, "RGBA")
        x0 = GX + GW + 34
        d.text((x0, 112), "FEATURES", font=self.F("semi", 26), fill=DIM)
        f = self.F("xbold", 36)
        for i, (key, label) in enumerate(self.features):
            y = 160 + i * 84
            on, was = key == active, key in done
            if on:
                d.rounded_rectangle((x0 - 14, y - 10, x0 + 262, y + 58), 14, fill=(52, 50, 40), outline=YELLOW, width=3)
            col = YELLOW if on else (GREEN if was else (70, 86, 124))
            d.ellipse((x0, y + 10, x0 + 28, y + 38), outline=col, width=4, fill=col if (on or was) else None)
            if was and not on:
                d.line((x0 + 7, y + 24, x0 + 12, y + 30, x0 + 22, y + 17), fill=NAVY, width=4)
            d.text((x0 + 44, y + 2), label, font=f, fill=WHITE if on else (col if was else (92, 108, 150)))

    # composition helpers ---------------------------------------------------
    def game_frame(self, base, im, scale=4, xy=(GX, GY)):
        base.paste(im.resize((NW * scale, NH * scale), Image.NEAREST), xy)


def caption_at(seg, i):
    """Active caption, its local age, and (card, card age) for local frame i."""
    cur, card, card_start = None, None, 0
    for c in seg.get("_caps", []):
        if c["_a"] > i:
            break
        if c.get("card"):
            card, card_start = c["card"], c["_a"]
        elif c.get("card_hold"):
            if card is None and seg.get("_inherited_card"):
                card, card_start = seg["_inherited_card"], -999
        else:
            card = None
        if i < c["_b"]:
            cur = c
    if cur is None:
        return None, 0, 0, None, None, 0
    return cur, i - cur["_a"], cur["_b"] - cur["_a"], None, card, i - card_start


# ----------------------------------------------------------------- timeline
def build_timeline(manifest):
    segs = manifest["segments"]
    t = 0
    prev_card = None
    for n, s in enumerate(segs):
        if s["kind"] in ("game", "intro"):
            a, b = s["native"]
            s["_len"] = (b - a) // 2
        elif s["kind"] == "split":
            la = s["left"]["native"]; ra = s["right"]["native"]
            if (la[1] - la[0]) != (ra[1] - ra[0]):
                sys.exit(f"{s['id']}: split sides differ in length")
            s["_len"] = (la[1] - la[0]) // 2
        else:
            s["_len"] = s["frames"][1] - s["frames"][0] + s.get("lead_graphic", 0)
        T = s.get("transition", {}).get("frames", 0) if n else 0
        s["_T"] = T
        s["_start"] = t - T
        if s["_start"] < 0:
            s["_start"] = 0
        t = s["_start"] + s["_len"]
        s["_end"] = t
        caps = []
        for c in s.get("captions", []):
            c = dict(c)
            if "native" in c:
                c["_a"] = (c["native"][0] - s["native"][0]) // 2
                c["_b"] = (c["native"][1] - s["native"][0]) // 2
            else:
                c["_a"], c["_b"] = c["frames"]
            caps.append(c)
        s["_caps"] = caps
        s["_inherited_card"] = prev_card
        for c in caps:
            if c.get("card"):
                prev_card = c["card"]
        if s.get("tracker") is False:
            prev_card = None
    return t


def feature_timeline(manifest, total):
    active = [None] * total
    for s in manifest["segments"]:
        for c in s["_caps"]:
            if c.get("feature"):
                for i in range(c["_a"], c["_b"]):
                    f = s["_start"] + i
                    if 0 <= f < total:
                        active[f] = c["feature"]
    done, seen, out = set(), [], []
    last = None
    for f in range(total):
        if active[f] != last and last is not None:
            done.add(last)
        if active[f] is not None:
            last = active[f]
        out.append((active[f], set(done)))
    return out


# ----------------------------------------------------------------- segment renderers
class SegmentPainter:
    def __init__(self, R, src):
        self.R, self.src = R, src

    def frames_for(self, s):
        if s["kind"] in ("game", "intro"):
            return self.src.native_clip(s["src"], *s["native"])
        if s["kind"] in ("title", "online"):
            return self.src.decode(s["src"], "title", *s["frames"])
        return None

    def paint(self, s, i, t, feat):
        R = self.R
        if s["kind"] == "intro":
            return self.paint_intro(s, i)
        base = R.background(t).convert("RGBA")
        k = s["kind"]
        if k == "game":
            im = self.frames_for(s)[i]
            R.game_frame(base, im)
            d = ImageDraw.Draw(base, "RGBA")
            d.rectangle((GX - 4, GY, GX - 1, GY + GH), fill=GREEN)
            d.rectangle((GX + GW, GY, GX + GW + 3, GY + GH), fill=GREEN)
        elif k == "title":
            R.game_frame(base, self.frames_for(s)[i])
        elif k == "split":
            self.paint_split(base, s, i)
        elif k == "online":
            self.paint_online(base, s, i)
        elif k == "engine":
            self.paint_engine(base, s, i)
        elif k == "end":
            self.paint_end(base, s, i)
        if k in ("game", "title", "split"):
            cap, ci, cl, _, card, cardi = caption_at(s, i)
            if cap is not None and cap.get("headline"):
                L = R.caption_layer(cap)
                kin = 1.0 if cap.get("hold") else ease_out(ci / 8)
                base.alpha_composite(with_alpha(L, kin), (0, BAND_Y + int(22 * (1 - kin))))
            if card is not None and s.get("tracker", True):
                L = R.card_layer(card)
                kk = ease_out(cardi / 10)
                base.alpha_composite(with_alpha(L, kk), (int(20 - 60 * (1 - kk)), 160))
            if s.get("tracker", True):
                R.tracker(base, *feat)
        R.top_bar(base)
        return base

    def paint_intro(self, s, i):
        """Cold open: the real footage alone on black, fading up, with a staged two-part line."""
        R = self.R
        base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        R.game_frame(base, self.frames_for(s)[i])
        T = s["intro_text"]
        a_out, b_out = T["out"]
        k_out = 1.0 if i < a_out else max(0.0, 1 - (i - a_out) / (b_out - a_out))
        d = ImageDraw.Draw(base, "RGBA")
        kick = T.get("kicker")
        if kick and i >= kick["at"]:
            fk = R.F("medium", 24)
            kk = ease_out((i - kick["at"]) / 20) * k_out
            col = tuple(int(c * kk) for c in DIM)
            d.text((W / 2 - fk.getlength(kick["text"]) / 2, 20), kick["text"], font=fk, fill=col)
        f = R.F("heavy", T["size"])
        full = "".join(p["text"] for p in T["parts"])
        width = sum(f.getlength(t) for t, _ in parse_marked(full))
        x = W / 2 - width / 2
        y = BAND_Y + (H - BAND_Y - T["size"] * 1.2) / 2 - 4
        for part in T["parts"]:
            pw = sum(f.getlength(t) for t, _ in parse_marked(part["text"]))
            if i >= part["at"] and k_out > 0:
                kin = ease_out((i - part["at"]) / 10)
                L = Image.new("RGBA", (int(pw) + 20, T["size"] * 2), (0, 0, 0, 0))
                draw_marked(ImageDraw.Draw(L), (0, 0), part["text"], f, anchor_center=False)
                base.alpha_composite(with_alpha(L, kin * k_out), (int(x), int(y + 18 * (1 - kin))))
            x += pw
        fi = s.get("fade_in", 0)
        if i < fi:
            base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - ease(i / fi))))))
        return base

    def paint_split(self, base, s, i):
        R = self.R
        d = ImageDraw.Draw(base, "RGBA")
        L = self.src.native_clip(s["left"]["src"], *s["left"]["native"])[i]
        Rt = self.src.native_clip(s["right"]["src"], *s["right"]["native"])[i]
        ly, ry = GY + 8, GY + GH - NH * 3
        R.game_frame(base, L, 3, (0, ly))
        R.game_frame(base, Rt, 3, (960, ry))
        f = R.F("heavy", 120)
        k = ease_out(i / 10)
        lab_l, lab_r = s["left"]["label"], s["right"]["label"]
        d.text((40 - int(80 * (1 - k)), ly + NH * 3 + 6), lab_l, font=f, fill=SKY)
        d.text((W - 40 - f.getlength(lab_r) + int(80 * (1 - k)), GY + 30), lab_r, font=f, fill=YELLOW)
        golf_ball(d, 960 - 80, ly + NH * 3 + 78, 34)
        golf_ball(d, 960 + 80, GY + 100, 34, fill=(255, 236, 170))

    def paint_online(self, base, s, i):
        R = self.R
        d = ImageDraw.Draw(base, "RGBA")
        lead = s.get("lead_graphic", 0)
        ox, oy = 90, 170
        d.rounded_rectangle((ox - 10, oy - 10, ox + 960 + 9, oy + 672 + 9), 12, fill=(5, 11, 28))
        if i >= lead:
            R.game_frame(base, self.src.decode(s["src"], "title", *s["frames"])[i - lead], 3, (ox, oy))
        if i < lead + 8 and lead:
            # original lead-in graphic (two screens linked), then a short dissolve into the real menu clip
            G = self.online_graphic(R)
            k = 1.0 if i < lead else 1 - (i - lead + 1) / 9
            base.alpha_composite(with_alpha(G, k), (ox, oy))
            d = ImageDraw.Draw(base, "RGBA")
        pulse = 0.5 + 0.5 * math.sin(i / 5)
        for x0, y0, x1, y1 in (s["menu_box_native"] if i >= lead else []):
            w = 5 + int(2 * pulse)
            d.rounded_rectangle((ox + x0 * 3 - w, oy + y0 * 3 - w, ox + x1 * 3 + w, oy + y1 * 3 + w), 10, outline=YELLOW, width=w)
            ax = ox + x1 * 3 + 24
            ay = oy + (y0 + y1) * 3 // 2
            d.polygon([(ax, ay), (ax + 40, ay - 22), (ax + 40, ay + 22)], fill=YELLOW)
            d.rectangle((ax + 40, ay - 7, ax + 120, ay + 7), fill=YELLOW)
        tx = 1150
        T = s["text"]
        k = ease_out(i / 12)
        dx = int(60 * (1 - k))
        d.text((tx + dx, 230), T["kicker"], font=R.F("semi", 34), fill=GREEN)
        draw_marked(d, (tx + dx, 280), T["headline"], R.F("heavy", 104), anchor_center=False)
        y = 430
        for line in wrap(T["body"], R.F("book", 40), 690):
            d.text((tx + dx, y), line, font=R.F("book", 40), fill=WHITE)
            y += 52
        y += 36
        d.rounded_rectangle((tx + dx - 4, y - 8, tx + dx + 700, y + 8 + 36 * len(wrap(T["note"], R.F("medium", 28), 660))), 10,
                            fill=(20, 38, 78), outline=(112, 130, 172), width=2)
        for line in wrap(T["note"], R.F("medium", 28), 660):
            d.text((tx + dx + 14, y), line, font=R.F("medium", 28), fill=DIM)
            y += 36

    def online_graphic(self, R):
        if getattr(self, "_og", None) is None:
            G = Image.new("RGBA", (960, 672), (5, 11, 28, 255))
            g = ImageDraw.Draw(G)
            for n, (cx, lab, col) in enumerate(((240, "HOST", SKY), (720, "JOIN", YELLOW))):
                g.rounded_rectangle((cx - 170, 170, cx + 170, 400), 18, fill=NAVY2, outline=col, width=6)
                g.rectangle((cx - 40, 400, cx + 40, 440), fill=(70, 86, 124))
                g.rectangle((cx - 100, 440, cx + 100, 456), fill=(70, 86, 124))
                golf_ball(g, cx, 285, 50, fill=WHITE if n == 0 else (255, 236, 170))
                f = R.F("heavy", 72)
                g.text((cx - f.getlength(lab) / 2, 480), lab, font=f, fill=col)
            for x in range(430, 540, 26):
                g.ellipse((x - 7, 278, x + 7, 292), fill=GREEN)
            f = R.F("medium", 30)
            t = "Direct connect  ·  two machines"
            g.text((480 - f.getlength(t) / 2, 600), t, font=f, fill=DIM)
            self._og = G
        return self._og

    def paint_engine(self, base, s, i):
        R = self.R
        d = ImageDraw.Draw(base, "RGBA")
        mini = self.src.native_clip(s["mini"]["src"], *s["mini"]["native"])[i]
        mx, my = 1180, 250
        d.rounded_rectangle((mx - 12, my - 12, mx + 640 + 11, my + 448 + 11), 14, fill=(5, 11, 28), outline=GREEN, width=3)
        R.game_frame(base, mini, 2, (mx, my))
        d.text((mx, my + 470), "Recorded in the engine  ·  2× pixels  ·  normal speed", font=R.F("medium", 26), fill=DIM)
        T = s["text"]
        x = 120
        k = ease_out(i / 10)
        d.text((x, 170), T["kicker"], font=R.F("semi", 34), fill=GREEN)
        draw_marked(d, (x - int(50 * (1 - k)), 215), T["headline"], R.F("heavy", 112), anchor_center=False)
        y = 380
        fb = R.F("medium", 36)
        for n, b in enumerate(T["bullets"]):
            kk = ease_out((i - s.get("bullet_start", 14) - n * s.get("bullet_step", 14)) / 10)
            if kk <= 0:
                y += 46 * len(wrap(b, fb, 900)) + 28
                continue
            L = Image.new("RGBA", (1000, 200), (0, 0, 0, 0))
            dl = ImageDraw.Draw(L)
            golf_ball(dl, 18, 26, 14)
            yy = 0
            for line in wrap(b, fb, 900):
                dl.text((52, yy), line, font=fb, fill=WHITE)
                yy += 46
            base.alpha_composite(with_alpha(L, kk), (x + int(40 * (1 - kk)), y))
            y += yy + 28

    def paint_end(self, base, s, i):
        R = self.R
        d = ImageDraw.Draw(base, "RGBA")
        T = s["text"]
        k = ease_out(i / 14)
        fw = R.F("heavy", 168)
        tw = fw.getlength(T["wordmark"])
        y0 = 150 + int(30 * (1 - k))
        d.text((W / 2 - tw / 2 + 7, y0 + 9), T["wordmark"], font=fw, fill=(3, 8, 20))
        d.text((W / 2 - tw / 2, y0), T["wordmark"], font=fw, fill=YELLOW)
        fs = R.F("semi", 40)
        d.text((W / 2 - fs.getlength(T["sub"]) / 2, y0 + 205), T["sub"], font=fs, fill=WHITE)
        kc = ease_out((i - s.get("cta_delay", 12)) / 12)
        if kc > 0:
            fc = R.F("xbold", 56)
            cw = fc.getlength(T["cta"])
            L = Image.new("RGBA", (int(cw) + 90, 100), (0, 0, 0, 0))
            dl = ImageDraw.Draw(L)
            dl.rounded_rectangle((0, 0, cw + 89, 99), 50, fill=GREEN)
            dl.text((45, 14), T["cta"], font=fc, fill=NAVY)
            base.alpha_composite(with_alpha(L, kc), (int(W / 2 - (cw + 90) / 2), 470 + int(20 * (1 - kc))))
        fst = R.F("medium", 32)
        d.text((W / 2 - fst.getlength(T["status"]) / 2, 600), T["status"], font=fst, fill=SKY)
        # original geometric motion graphic: a ball rolls along a green line into the cup
        gy = 820
        d.rectangle((160, gy, W - 160, gy + 10), fill=GREEN)
        cup_x = 1500
        d.rectangle((cup_x - 34, gy, cup_x + 34, gy + 38), fill=NAVY)
        flag(d, cup_x - 3, gy - 150, 150)
        rf = s.get("roll_frames", 70)
        p = ease(i / rf)
        r = 26
        bx = 120 + (cup_x - 120) * p
        by = gy - r + (min(1.0, max(0.0, (i - rf) / 6)) * (r + 14) if i >= rf else 0)
        if i < rf + 8:
            golf_ball(d, bx, by, r)
        else:
            fp = R.F("heavy", 60)
            d.text((cup_x + 60, gy - 120), "IN!", font=fp, fill=YELLOW)
        fd = R.F("book", 24)
        d.text((W / 2 - fd.getlength(T["disclaimer"]) / 2, 1000), T["disclaimer"], font=fd, fill=DIM)
        if T.get("audio_credit"):
            d.text((W / 2 - fd.getlength(T["audio_credit"]) / 2, 964), T["audio_credit"], font=fd, fill=DIM)


# ----------------------------------------------------------------- transitions
def transition(kind, A, B, p, frame_no):
    p = max(0.0, min(1.0, p))
    if kind == "build":   # both sides show the same source frames: only the surround dissolves in
        return Image.blend(A, B, ease(p))
    if kind == "flash":
        out = A if p < 0.5 else B
        k = 1 - abs(p - 0.5) * 2
        white = Image.new("RGBA", (W, H), (255, 255, 255, int(220 * k)))
        out = out.copy()
        out.alpha_composite(white)
        return out
    if kind == "iris":
        e = ease(p)
        cx, cy = GX + GW // 2, GY + GH // 2
        r = 4 + e * math.hypot(W, H) * 0.62
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        out = Image.composite(B, A, m)
        d = ImageDraw.Draw(out)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=WHITE, width=14)
        return out
    if kind == "push":
        e = ease(p)
        dx = int(GW * e)
        out = B.copy()
        win_a = A.crop((GX, GY, GX + GW, GY + GH))
        win_b = B.crop((GX, GY, GX + GW, GY + GH))
        strip = Image.new("RGBA", (GW * 2 + 24, GH), (*YELLOW, 255))
        strip.paste(win_a, (0, 0)); strip.paste(win_b, (GW + 24, 0))
        out.paste(strip.crop((dx + int(24 * e), 0, dx + int(24 * e) + GW, GH)), (GX, GY))
        return out
    if kind == "stripes":
        e = ease(p)
        span = W + 900
        lead = -450 + span * e
        m = Image.new("L", (W, H), 0)
        dm = ImageDraw.Draw(m)
        dm.polygon([(-2000, 0), (lead - 300, 0), (lead - 300 - 420, H), (-2000, H)], fill=255)
        out = Image.composite(B, A, m)
        d = ImageDraw.Draw(out)
        for off, col in ((0, YELLOW), (-110, GREEN), (-220, RED)):
            x = lead + off
            d.polygon([(x, 0), (x + 90, 0), (x + 90 - 420, H), (x - 420, H)], fill=col)
        return out
    return B


# ----------------------------------------------------------------- main render
def render(manifest, src, out_mp4, draft_label, preview=None):
    total = build_timeline(manifest)
    feats = feature_timeline(manifest, total)
    R = Renderer(manifest, src, draft_label)
    P = SegmentPainter(R, src)
    segs = manifest["segments"]
    meta = out_mp4.with_suffix(".ffmeta")
    lines = [";FFMETADATA1", "title=" + manifest["title"] + (" [" + draft_label + "]" if draft_label else ""),
             "comment=" + manifest.get("_comment", "Real OpenGGF engine footage from a user-supplied Sonic 2 ROM, normal speed, silent. Edit list: .edl.json")]
    for s in segs:
        lines += ["[CHAPTER]", "TIMEBASE=1/30", f"START={s['_start']}", f"END={s['_end']}", "title=" + s["chapter"]]
    meta.write_text("\n".join(lines) + "\n")
    frames = range(total) if preview is None else preview
    enc = None
    if preview is None:
        tmp = out_mp4.with_name(out_mp4.stem + ".partial.mp4")
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(meta),
                                "-map", "0:v:0", "-map_metadata", "1", "-map_chapters", "1", "-an",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-tune", "animation",
                                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                                "-color_trc", "bt709", "-movflags", "+faststart", str(tmp)], stdin=subprocess.PIPE)
    stills = {}
    for f in frames:
        active = [s for s in segs if s["_start"] <= f < s["_end"]]
        imgs = []
        for s in active:
            imgs.append((s, P.paint(s, f - s["_start"], f, feats[f])))
        if len(imgs) == 1:
            out = imgs[0][1]
        else:
            (sa, A), (sb, B) = imgs[0], imgs[1]
            p = (f - sb["_start"] + 0.5) / sb["_T"]
            out = transition(sb["transition"]["type"], A, B, p, f)
        for s in segs:
            fo = s.get("fade_out")
            if fo and s["_end"] - fo <= f < s["_end"] and s in active:
                k = (f - (s["_end"] - fo) + 1) / fo
                out = out.copy(); out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * k))))
        out = out.convert("RGB")
        if preview is not None or f in sheet_frames(segs):
            stills[f] = out
        if enc:
            enc.stdin.write(out.tobytes())
        if f % 150 == 0:
            print(f"  frame {f}/{total}", flush=True)
    if enc:
        enc.stdin.close()
        if enc.wait():
            sys.exit("ffmpeg encode failed")
        tmp.replace(out_mp4)
    meta.unlink(missing_ok=True)
    return total, stills


def sheet_frames(segs):
    s = set()
    for seg in segs:
        s.add(seg["_start"] + seg["_T"])                    # first clean frame
        s.add(seg["_start"] + (seg["_T"] + seg["_len"]) // 2)  # middle
        if seg["_T"]:
            s.add(seg["_start"] + seg["_T"] // 2)             # mid-transition
    return s


def contact_sheet(stills, path, cols=6):
    keys = sorted(stills)
    tw, th = 480, 270
    rows = (len(keys) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 24)), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for n, f in enumerate(keys):
        x, y = (n % cols) * tw, (n // cols) * (th + 24)
        sheet.paste(stills[f].resize((tw, th), Image.BILINEAR), (x, y + 24))
        d.text((x + 4, y + 4), f"out {f}  t={f / FPS:.2f}s", fill=(255, 255, 0))
    sheet.save(path)


def verify_output(path, total, nchapters):
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_chapters",
                                    "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    pts = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time",
                          "-of", "csv=p=0", str(path)], check=True, capture_output=True, text=True).stdout.split()
    pts = [float(x.strip(",")) for x in pts if x.strip(",")]
    deltas = [b - a for a, b in zip(pts, pts[1:])]
    dec = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
    res = {"width": v["width"], "height": v["height"], "avg_frame_rate": v["avg_frame_rate"], "codec": v["codec_name"],
           "pix_fmt": v["pix_fmt"], "nb_frames": int(v.get("nb_frames", 0)), "decoded_frames": len(pts),
           "duration": float(pr["format"]["duration"]), "audio_streams": sum(s["codec_type"] == "audio" for s in pr["streams"]),
           "chapters": [[float(c["start_time"]), float(c["end_time"]), c["tags"]["title"]] for c in pr["chapters"]],
           "pts_delta_min": min(deltas), "pts_delta_max": max(deltas), "full_decode_ok": dec.returncode == 0 and not dec.stderr.strip()}
    res["ok"] = (res["width"], res["height"]) == (W, H) and res["avg_frame_rate"] == "30/1" and \
        res["nb_frames"] == total == res["decoded_frames"] and len(res["chapters"]) == nchapters and \
        abs(res["pts_delta_min"] - 1 / 30) < 1e-3 and abs(res["pts_delta_max"] - 1 / 30) < 1e-3 and res["full_decode_ok"]
    return res


def write_edl(manifest, src_report, path_json, path_csv, out_mp4, draft_label):
    segs = []
    for s in manifest["segments"]:
        e = {"id": s["id"], "chapter": s["chapter"], "kind": s["kind"],
             "out_frames": [s["_start"], s["_end"]], "out_seconds": [s["_start"] / FPS, s["_end"] / FPS],
             "transition_in": s.get("transition") if s["_T"] else None}
        def rng(key, a, b):
            return {"src": key, "dir": src_report["sources"][key]["dir"], "file": "gameplay.mkv",
                    "native_frames": [a, b], "mkv_frames": [a // 2, b // 2],
                    "mkv_seconds": [a / 60, b / 60]}
        if s["kind"] in ("game", "intro"):
            e["source"] = rng(s["src"], *s["native"])
            if s["kind"] == "intro":
                e["fade_in_frames"] = s.get("fade_in", 0)
        elif s["kind"] == "split":
            e["source_left"] = rng(s["left"]["src"], *s["left"]["native"])
            e["source_right"] = rng(s["right"]["src"], *s["right"]["native"])
        elif s["kind"] in ("title", "online"):
            a, b = s["frames"]
            e["source"] = {"src": s["src"], "dir": src_report["sources"][s["src"]]["dir"], "file": "title.mkv",
                           "frames": [a, b], "seconds": [a / FPS, b / FPS], "lead_graphic_frames": s.get("lead_graphic", 0)}
        elif s["kind"] == "engine":
            e["source_mini"] = rng(s["mini"]["src"], *s["mini"]["native"])
        e["captions"] = [{k: c[k] for k in ("headline", "sub", "feature") if k in c} |
                         {"out_frames": [s["_start"] + c["_a"], s["_start"] + c["_b"]]} for c in s["_caps"]]
        segs.append(e)
    doc = {"output": str(out_mp4), "draft_label": draft_label, "fps": FPS, "canvas": [W, H],
           "total_frames": manifest["_total"], "segments": segs, "source_check": src_report}
    path_json.write_text(json.dumps(doc, indent=2) + "\n")
    with open(path_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["chapter", "out_start_s", "out_end_s", "source", "native_start", "native_end", "mkv_start_s", "mkv_end_s", "transition_in"])
        for e in segs:
            for k in ("source", "source_left", "source_right", "source_mini"):
                if k in e:
                    r = e[k]
                    if "native_frames" in r:
                        w.writerow([e["chapter"] + ("" if k == "source" else f" ({k[7:]})"), f"{e['out_seconds'][0]:.3f}", f"{e['out_seconds'][1]:.3f}",
                                    f"{Path(r['dir']).name}/{r['file']}", *r["native_frames"], f"{r['mkv_seconds'][0]:.3f}", f"{r['mkv_seconds'][1]:.3f}",
                                    (e["transition_in"] or {}).get("type", "")])
                    else:
                        w.writerow([e["chapter"], f"{e['out_seconds'][0]:.3f}", f"{e['out_seconds'][1]:.3f}",
                                    f"{Path(r['dir']).name}/{r['file']}", "", "", f"{r['seconds'][0]:.3f}", f"{r['seconds'][1]:.3f}",
                                    (e["transition_in"] or {}).get("type", "")])
            if not any(k in e for k in ("source", "source_left", "source_mini")):
                w.writerow([e["chapter"], f"{e['out_seconds'][0]:.3f}", f"{e['out_seconds'][1]:.3f}", "card (original graphics)", "", "", "", "",
                            (e["transition_in"] or {}).get("type", "")])


# ----------------------------------------------------------------- soundtrack (editorial)
def wav_seconds(path):
    import wave
    with wave.open(str(path)) as w:
        if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (48000, 2, 2):
            sys.exit(f"{path}: expected 48 kHz 16-bit stereo")
        return w.getnframes() / w.getframerate()


def resolve_audio(manifest, audio_dir, total):
    """Resolve manifest['audio'] anchors to absolute placements (seconds in the output)."""
    A = manifest["audio"]
    segs = {s["id"]: s for s in manifest["segments"]}
    end_s = total / FPS
    def at(anchor):
        sid, local = anchor
        return (segs[sid]["_start"] + local) / FPS
    out = []
    for ev in A["events"]:
        path = Path(audio_dir) / A["stems"][ev["stem"]]
        if not path.exists():
            sys.exit(f"missing stem {path}; render it with tools/render_stems.sh")
        stem_len = wav_seconds(path)
        place = at(ev["anchor"]) - ev.get("align_stem_s", 0.0)   # output time of stem 0
        s0 = max(0.0, -place)                                    # stem start actually used
        s1 = ev.get("stem_end_s", stem_len)
        if "until_anchor" in ev:
            s1 = min(s1, at(ev["until_anchor"]) - place)
        if ev.get("until_end"):
            s1 = min(s1, end_s - ev.get("end_pad_s", 0.0) - place)
        if s1 > stem_len + 1e-6:
            sys.exit(f"{ev['stem']}: needs {s1:.2f} s but the stem is {stem_len:.2f} s; render a longer stem")
        out.append({"stem": ev["stem"], "id": A["stem_ids"][ev["stem"]], "file": str(path), "why": ev.get("why", ""),
                    "out_start_s": round(place + s0, 4), "out_end_s": round(place + s1, 4),
                    "stem_range_s": [round(s0, 4), round(s1, 4)], "gain": ev.get("gain", 1.0),
                    "fade_in_s": ev.get("fade_in_s", 0.0), "fade_out_s": ev.get("fade_out_s", 0.0),
                    "stem_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return out


def loudness(path, extra_filter=""):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn", "-af",
                        (extra_filter + "," if extra_filter else "") + "ebur128=peak=true:framelog=quiet",
                        "-f", "null", "-"], capture_output=True, text=True)
    txt = r.stderr[r.stderr.rfind("Summary:"):]
    import re
    g = lambda k: float(re.search(k + r":\s+(-?[\d.]+|-inf)", txt).group(1).replace("-inf", "-200"))
    return {"integrated_lufs": g("I"), "lra_lu": g("LRA"), "true_peak_dbfs": g("Peak")}


def mix_soundtrack(manifest, placements, total, out_wav):
    """Mix the placements with ffmpeg, then two-pass EBU R128 normalisation (linear when possible)."""
    end_s = total / FPS
    args, chains = ["ffmpeg", "-nostdin", "-v", "error", "-y"], []
    for n, pl in enumerate(placements):
        args += ["-i", pl["file"]]
        s0, s1 = pl["stem_range_s"]
        dur = s1 - s0
        f = [f"atrim=start={s0:.5f}:end={s1:.5f}", "asetpts=PTS-STARTPTS"]
        if pl["fade_in_s"]:
            f.append(f"afade=t=in:st=0:d={pl['fade_in_s']}:curve=qsin")
        if pl["fade_out_s"]:
            f.append(f"afade=t=out:st={max(0.0, dur - pl['fade_out_s']):.5f}:d={pl['fade_out_s']}:curve=qsin")
        f.append(f"volume={pl['gain']}")
        ms = int(round(pl["out_start_s"] * 1000))
        f.append(f"adelay={ms}|{ms}")
        chains.append(f"[{n}:a]" + ",".join(f) + f"[a{n}]")
    graph = ";".join(chains) + ";" + "".join(f"[a{n}]" for n in range(len(placements))) + \
        f"amix=inputs={len(placements)}:normalize=0:duration=longest,apad=whole_dur={end_s:.5f},atrim=end={end_s:.5f}[mix]"
    raw = out_wav.with_name(out_wav.stem + ".premix.wav")
    subprocess.run(args + ["-filter_complex", graph, "-map", "[mix]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", str(raw)], check=True)
    L = manifest["audio"]["loudness"]
    target = f"I={L['integrated_lufs']}:TP={L['true_peak_dbtp']}:LRA={L['lra']}"
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(raw), "-af", f"loudnorm={target}:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    meas = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm={target}:linear=true:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:print_format=json")
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-y", "-i", str(raw), "-af", ln + f",aresample=48000,atrim=end={end_s:.5f}",
                        "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)], capture_output=True, text=True, check=True)
    second = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    premix = loudness(raw)
    raw.unlink()
    return {"premix": premix, "loudnorm_pass1": meas, "loudnorm_pass2_type": second.get("normalization_type"),
            "final_wav": loudness(out_wav)}


def mux_audio(video, wav, out_mp4, comment):
    tmp = out_mp4.with_name(out_mp4.stem + ".mux.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(video), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0",
                    "-map_metadata", "0", "-map_chapters", "0", "-metadata", "comment=" + comment,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-shortest",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(out_mp4)


def verify_audio(path, total):
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
                                   check=True, capture_output=True, text=True).stdout)
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    res = {"audio_streams": len(a)}
    if a:
        a = a[0]
        pk = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "packet=pts_time,duration_time",
                             "-of", "csv=p=0", str(path)], check=True, capture_output=True, text=True).stdout.split()
        last = [float(x) for x in pk[-1].split(",") if x]
        res.update({"codec": a["codec_name"], "sample_rate": int(a["sample_rate"]), "channels": a["channels"],
                    "audio_end_s": round(sum(last), 4), "video_end_s": round(total / FPS, 4)})
        res.update(loudness(path))
        st = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn", "-af", "astats=measure_perchannel=none",
                             "-f", "null", "-"], capture_output=True, text=True).stderr
        import re
        res["sample_peak_dbfs"] = float(re.findall(r"Peak level dB:\s+(-?[\d.]+)", st)[-1])
        res["clipped_samples"] = int(float(re.findall(r"Number of clipped samples?:\s+(\d+)", st)[-1])) if \
            re.findall(r"Number of clipped samples?:\s+(\d+)", st) else None
        # quiet edges: first and last 0.2 s
        for name, opt in (("head_0_0.2s", ["-t", "0.2"]), ("tail_last_0.2s", ["-ss", f"{total / FPS - 0.2:.3f}"])):
            st = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + (opt if name.startswith("tail") else []) + ["-i", str(path)] +
                                (opt if name.startswith("head") else []) + ["-vn", "-af", "astats=measure_perchannel=none", "-f", "null", "-"],
                                capture_output=True, text=True).stderr
            m = re.findall(r"Peak level dB:\s+(-?[\d.]+|-inf)", st)
            res[name + "_peak_dbfs"] = float(m[-1].replace("-inf", "-200")) if m else None
        res["ok"] = res["codec"] == "aac" and res["sample_rate"] == 48000 and res["channels"] == 2 and \
            abs(res["audio_end_s"] - res["video_end_s"]) < 0.05 and res["true_peak_dbfs"] <= -1.0 and \
            res["head_0_0.2s_peak_dbfs"] < -40 and res["tail_last_0.2s_peak_dbfs"] < -40
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source-root", required=True, help="directory holding the scenario capture directories")
    ap.add_argument("--tag", default=None, help="capture suffix substituted into manifest dirs (v4, v5, ...)")
    ap.add_argument("--dir", action="append", default=[], metavar="KEY=PATH", help="override one scenario dir (ehz1/local/ehz2)")
    ap.add_argument("--manifest", default=str(HERE / "promo-manifest-intro.json"))
    ap.add_argument("--lock-file", default=str(HERE / "source-lock-intro.json"))
    ap.add_argument("--audio-dir", default=str(HERE / "audio"), help="directory holding the rendered Sonic 2 stems")
    ap.add_argument("--no-audio", action="store_true", help="render silent (as the paced cut)")
    ap.add_argument("--lock", action="store_true", help="(re)write the state lock from these sources")
    ap.add_argument("--allow-state-drift", action="store_true", help="render even if selected ranges no longer match the lock")
    ap.add_argument("--final", action="store_true", help="omit the DRAFT label (refused for v4 footage)")
    ap.add_argument("--out", default=None, help="output mp4 (default promo-opus-<tag>[-draft].mp4 next to this script)")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--preview", default=None, help="comma list of output frames to write as PNG stills only")
    args = ap.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    tag = args.tag or manifest["default_tag"]
    overrides = dict(x.split("=", 1) for x in args.dir)
    if args.final and tag == "v4" and not overrides:
        sys.exit("v4 footage has the idle-Tails visibility defect; it can only be rendered as a draft")
    src = Sources(manifest, args.source_root, tag, overrides)
    report = validate_sources(manifest, src, Path(args.lock_file), args.lock, args.allow_state_drift)
    if args.check_only:
        print(json.dumps(report["problems"], indent=2))
        return
    draft = None if args.final else f"DRAFT  ·  {tag} footage"
    if args.allow_state_drift and report["problems"]:
        draft = (draft or "") + "  ·  UNLOCKED TIMELINE"
    out = Path(args.out) if args.out else HERE / f"promo-opus-{tag}{'' if args.final else '-draft'}.mp4"
    if args.preview:
        pv = [int(x) for x in args.preview.split(",")]
        _, stills = render(manifest, src, out, draft, preview=pv)
        for f, im in stills.items():
            p = out.with_name(f"{out.stem}.preview-{f:04d}.png")
            im.save(p)
            print(p)
        return
    with_audio = "audio" in manifest and not args.no_audio
    if with_audio:
        manifest["_comment"] = ("Real OpenGGF engine footage from a user-supplied Sonic 2 ROM, normal speed, recorded silent. "
                                "Editorial soundtrack: Sonic 2 music/effects rendered from the ROM by OpenGGF's SMPS driver "
                                "and added in editing (not synchronised gameplay audio). Edit list: .edl.json")
    total, stills = render(manifest, src, out, draft)
    manifest["_total"] = total
    contact_sheet(stills, out.with_suffix(".cuts.png"))
    if with_audio:
        placements = resolve_audio(manifest, args.audio_dir, total)
        wav = out.with_suffix(".soundtrack.wav")
        levels = mix_soundtrack(manifest, placements, total, wav)
        mux_audio(out, wav, out, manifest["_comment"])
        aud = verify_audio(out, total)
        out.with_suffix(".audio.json").write_text(json.dumps({"placements": placements, "mix": levels, "verify": aud}, indent=2) + "\n")
        print(json.dumps(aud))
        if not aud.get("ok"):
            sys.exit("audio verification failed; see audio.json")
    ver = verify_output(out, total, len(manifest["segments"]))
    out.with_suffix(".verify.json").write_text(json.dumps(ver, indent=2) + "\n")
    write_edl(manifest, report, out.with_suffix(".edl.json"), out.with_suffix(".chapters.csv"), out, draft)
    print(json.dumps({k: ver[k] for k in ("ok", "nb_frames", "decoded_frames", "duration", "pts_delta_min", "pts_delta_max", "full_decode_ok")}))
    if not ver["ok"]:
        sys.exit("output verification failed; see verify.json")
    print(f"wrote {out} ({total / FPS:.2f} s)")


if __name__ == "__main__":
    main()
