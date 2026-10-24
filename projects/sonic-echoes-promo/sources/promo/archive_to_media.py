#!/usr/bin/env python3
"""Import the Sonic Echoes promo production into an OpenGGF-Media checkout (projects/sonic-echoes-promo).

Byte-copies production text sources, hashes external assets (footage, frame sequences, audio,
sidecars, jars, fonts) into the catalogs, and writes the project README. Run from anywhere:
  python3 archive_to_media.py /path/to/OpenGGF-Media
Origin: Sonic Echoes promo, 2026-10-24.
"""
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

TASK = Path(__file__).resolve().parent
MEDIA = Path(sys.argv[1]).resolve()
PID = "sonic-echoes-promo"
ROOT_ID, FONT_ROOT = f"{PID}/promo", f"{PID}/fonts"
FONT_DIR = Path("/usr/share/fonts/TTF")
DEST = MEDIA / "projects" / PID / "sources" / "promo"

SOURCES = ["SHOTLIST.md", "PROVENANCE.md", "archive_to_media.py",
           "edit/edit.py", "edit/echokit.py", "edit/echofont.py", "edit/master.py", "edit/sheet.py",
           "out/chapters.csv", "out/chapters.ffmeta", "captures/HELPER.md", "captures/HELPER_BUILD.py"]
SHOT_TEXT = ("NOTES.md", "command.txt", "command.json", "inputs.script", "inputs.txt", "actions.txt",
             "recapture.py", "rebuild-action-jar.py", "earn.py", "earn_remaining.py", "notes.py", "run_a.py",
             "tight.py")
shots = sorted(p.name for p in (TASK / "captures").iterdir() if p.is_dir())
for shot in shots:
    for name in SHOT_TEXT:
        if (TASK / "captures" / shot / name).is_file():
            SOURCES.append(f"captures/{shot}/{name}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seq_hash(files):
    h = hashlib.sha256()
    for p in sorted(files, key=lambda q: q.name):
        h.update(f"{p.name}\0{p.stat().st_size}\0{sha(p)}\n".encode())
    return h.hexdigest()


# ---- sources
if DEST.exists():
    shutil.rmtree(DEST)
src_rows = []
for rel in SOURCES:
    s = TASK / rel
    d = DEST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
    src_rows.append({"path": str(d.relative_to(MEDIA)), "root": ROOT_ID, "original_path": rel,
                     "bytes": s.stat().st_size, "sha256": sha(s), "snapshot": "byte-copy"})

# ---- external assets
assets = []


def add(root, rel, kind, path):
    assets.append({"root": root, "path": rel, "kind": kind, "bytes": path.stat().st_size, "files": 1,
                   "sha256": sha(path)})


for shot in shots:
    c = TASK / "captures" / shot
    frames = sorted((c / "frames").glob("*.png"))
    if frames:
        assets.append({"root": ROOT_ID, "path": f"captures/{shot}/frames/*.png", "kind": "frame-sequence",
                       "bytes": sum(p.stat().st_size for p in frames), "files": len(frames),
                       "inventory_sha256": seq_hash(frames)})
    for name in ("state.csv", "session.csv"):
        if (c / name).is_file():
            add(ROOT_ID, f"captures/{shot}/{name}", "generated state/diagnostic data", c / name)
    for p in sorted(c.glob("*.mp4")):
        add(ROOT_ID, f"captures/{shot}/{p.name}", "superseded rough / section preview or capture viewing copy", p)
    for p in sorted(c.glob("*.jar")):
        add(ROOT_ID, f"captures/{shot}/{p.name}", "media dependency", p)
for p in sorted((TASK / "music").glob("*.wav")):
    add(ROOT_ID, f"music/{p.name}", "ROM-derived audio", p)
for p in sorted((TASK / "sfx").glob("*.wav")):
    add(ROOT_ID, f"sfx/{p.name}", "ROM-derived audio", p)
for p in sorted((TASK / "out").glob("*.mp4")):
    add(ROOT_ID, f"out/{p.name}", "video", p)
mix = TASK / "edit/build/render/promo-audio.wav"
add(ROOT_ID, "edit/build/render/promo-audio.wav", "ROM-derived audio", mix)
for name in ("FiraSansCompressed-Heavy.ttf", "FiraSansCompressed-HeavyItalic.ttf", "FiraSansCondensed-BoldItalic.ttf",
             "FiraSans-Bold.ttf", "FiraSans-BoldItalic.ttf"):
    add(FONT_ROOT, name, "external editorial font", FONT_DIR / name)

proj = MEDIA / "projects" / PID
(proj / "external-assets.json").write_text(json.dumps({
    "project": PID, "snapshot_date": "2026-10-24",
    "notes": "External bytes hashed at archive time, not uploaded. Render work (edit/build/render frames and sheets), "
             "capture save roots, compiled helper classes, review stills and the verify-hud diagnostic are excluded.",
    "sequence_hash": "inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append UTF-8 basename + NUL "
                     "+ decimal byte length + NUL + lowercase SHA-256 + LF.",
    "assets": assets}, indent=1) + "\n")

# ---- catalogs
cat = MEDIA / "catalog"
sources = [s for s in json.loads((cat / "sources.json").read_text()) if not s["path"].startswith(f"projects/{PID}/")]
sources += src_rows
(cat / "sources.json").write_text(json.dumps(sources, indent=2, ensure_ascii=False) + "\n")
roots = [r for r in json.loads((cat / "roots.json").read_text()) if not r["id"].startswith(f"{PID}/")]
roots += [{"id": ROOT_ID, "original": str(TASK), "archive": f"projects/{PID}/sources/promo",
           "notes": "Sonic Echoes promo: byte-preserved edit, helpers, shot list, provenance, capture commands, inputs "
                    "and notes. Footage, sidecars, ROM-derived audio and the film remain external."},
          {"id": FONT_ROOT, "original": str(FONT_DIR), "archive": "",
           "notes": "External Fira editorial faces (system install); hashed, not redistributed."}]
(cat / "roots.json").write_text(json.dumps(roots, indent=2) + "\n")
# assets.csv has mixed historical line endings: append rows to the raw text, never rewrite it.
raw = (cat / "assets.csv").read_bytes().decode("utf-8")
keep = [ln for ln in raw.splitlines(keepends=True) if not ln.startswith(f"{PID},")]
text = "".join(keep)
if not text.endswith(("\n", "\r\n")):
    text += "\r\n"
import io
buf = io.StringIO()
w = csv.writer(buf, lineterminator="\r\n")
for a in assets:
    w.writerow([PID, a["root"], a["path"], a["kind"], a["bytes"], a["files"]])
(cat / "assets.csv").write_bytes((text + buf.getvalue()).encode("utf-8"))
projects = [p for p in json.loads((cat / "projects.json").read_text()) if p["id"] != PID]
projects.append({"id": PID, "title": "Sonic Echoes promo",
                 "notes": "The delivered Sonic Echoes (Sonic 2 time-loop puzzle mod) promo: promo_kit edit, helpers, "
                          "master, shot list, provenance and every capture's commands/inputs/notes; film, footage, "
                          "sidecars and ROM-derived audio remain external.",
                 "source_files": len(src_rows), "catalog_entries": len(assets)})
(cat / "projects.json").write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n")
print(f"{len(src_rows)} sources, {len(assets)} external assets")
