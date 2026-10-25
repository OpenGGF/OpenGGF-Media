#!/usr/bin/env python3
"""Stages the OpenGGF-Media archive for the "Day Off" Stageplay promo locally (sp-promo-a, 2026-10-24).

Writes archive/projects/stageplay-day-off-promo/ (byte copies of the production sources, a
project README and external-assets.json) and archive/catalog-rows/ (rows to merge into the
media repository's catalog/projects.json, roots.json, sources.json and assets.csv). It does
not touch the OpenGGF-Media checkout. Frame directories are hashed as an inventory: SHA-256
over sorted basenames, appending for each file basename NUL byte-length NUL sha256 LF
(the time-attack-promo convention).
Usage: stage_archive.py   (from anywhere; paths are absolute)
"""
import csv
import hashlib
import json
import shutil
from pathlib import Path

PROD = Path("/home/farrell/Videos/OGGF/sp-promo-a")
PID = "stageplay-day-off-promo"
ARCH = PROD / "archive"
PROJ = ARCH / "projects" / PID
SRC = PROJ / "sources" / "promo"
ROOT_ID = f"{PID}/promo"

SOURCES = [
    "DIRECTOR.md", "PROVENANCE.md", "TREATMENTS.md", "STATUS.md",
    "edit/edit.py", "edit/edit-r1.py", "edit/film-camera.json",
    "tools/sp.py", "tools/sp_util.py", "tools/EditorCapture.java", "tools/capture_editor.py",
    "tools/run_edit.py", "tools/mux_final.py", "tools/stage_archive.py",
    "scenes/build_scene.py", "scenes/build_scene_v1.py", "scenes/make_voice.py", "scenes/make_decor.py",
    "scenes/measured.json", "scenes/routes/loop-route.json",
    "scenes/t06.screenplay.json", "scenes/t06.stageplay",
    "scenes/t06-editor.screenplay.json", "scenes/t06-editor.stageplay",
    "scenes/t06-sfx.screenplay.json", "scenes/t06-sfx.stageplay",
    "captures/editor-r2/route.events.json", "captures/editor-r2/route-applied.stageplay",
    "captures/editor-tour2/tour.events.json", "captures/editor-tour2/scene/day-off.stageplay",
    "captures/editor-tour2/scene/day-off.screenplay.json", "captures/editor-tour2/scene/roundtrip.stageplay",
    "captures/desktop-route/desktop-route.events.json", "captures/desktop-route/desktop-route-applied.stageplay",
    "captures/desktop-tour/desktop-tour.events.json",
    "captures/t06/render.json", "captures/t06/render4.json",
    # v2 (engine develop 81f25c89f)
    "edit/edit_v2.py", "edit/film-camera-v2.json", "tools/EditorCapture2.java", "tools/v2_chain.sh",
    "scenes/build_scene_r1.py", "scenes/ground-floors.json", "scenes/routes/loop-route-v2.json",
    "scenes/t10.screenplay.json", "scenes/t10.stageplay", "scenes/t10-editor.screenplay.json",
    "scenes/t10-editor.stageplay", "scenes/t10-sfx.screenplay.json", "scenes/t10-sfx.stageplay",
    "scenes/t10-novoice.screenplay.json", "scenes/t10-novoice.stageplay",
    "probe/ground/ghz.json", "probe/ground/ghz.out.json", "probe/ground/ehz.json", "probe/ground/ehz.out.json",
    "probe/ground/aiz.json", "probe/ground/aiz.out.json", "probe/ground/ghz-path1.json",
    "probe/ground/ghz-path1.out.json", "probe/s2cue/s2cue.screenplay.json", "probe/s2cue/s2cue.stageplay",
    "captures/v2/editor-route/route.events.json", "captures/v2/editor-route/route-applied.stageplay",
    "captures/v2/editor-tour/tour.events.json", "captures/v2/editor-tour/day-off.screenplay.json",
    "captures/v2/editor-desktop-route/desktop-route.events.json",
    "captures/v2/editor-desktop-route/desktop-route-applied.stageplay",
    "captures/v2/t10-render.json", "captures/v2/t10-sim.json", "captures/v2/chain.log",
    "review/route-sheet.png", "review/loop-sheet.png",
]
SUPERSEDED_SCENES = ["take01", "t02", "t02a", "t02a-loop-run", "t03", "t04", "t04-editor", "t05",
                     "v2a", "v2b", "v2b-novoice", "t07", "t07-editor", "t07-sfx", "t08", "t08-editor", "t08-sfx",
                     "t09", "t09-editor", "t09-sfx"]
GLOBS = ["scenes/voice/*.wav", "scenes/voice/cues.json", "scenes/decor/*.png"]
BUILD_FILES = {"edit/build/chapters.txt": "edit/chapters.txt", "edit/build/film-chapters.txt": "edit/film-chapters.txt",
               "edit/build-v2/chapters.txt": "edit/chapters-v2.txt", "edit/build-v2/film-chapters.txt": "edit/film-chapters-v2.txt"}

EXTERNAL = [  # path, kind, notes
    ("out/day-off-stageplay.mp4", "authored native world review or promo", "Final promo, 130.2 s"),
    ("out/day-off-film-1080p.mp4", "authored native world review or promo", "Final standalone film, 74.97 s"),
    ("captures/t06/t06-preview.mkv", "authored native world source movie", "Stageplay export 480x270 FFV1+FLAC"),
    ("captures/t06/day-off-film-1080p.mkv", "authored native world source movie", "Stageplay export --scale 4"),
    ("captures/t06/t06-sfx.mkv", "authored native world source movie", "SFX/voice stem take"),
    ("captures/t06/t06.sim.jsonl", "native LIVE world simulation JSONL", "simulate --every 1, 4498 samples"),
    ("captures/editor-r2/route.mkv", "lossless capture", "In-engine editor route session, FFV1 1080p60"),
    ("captures/editor-tour2/tour.mkv", "lossless capture", "In-engine editor tour, FFV1 1080p60"),
    ("captures/editor-tour2/day-off.editor-export.mkv", "authored native world source movie",
     "The editor's own Export film output; streams identical to t06-preview.mkv"),
    ("captures/desktop-route/desktop-route.mkv", "lossless capture", "Desktop editor route session"),
    ("captures/desktop-tour/desktop-tour.mkv", "lossless capture", "Desktop editor tour; not used in the promo"),
    ("audio/film.wav", "capture audio (ROM-derived)", "t06-preview soundtrack"),
    ("audio/film-sfx.wav", "capture audio (ROM-derived)", "t06-sfx soundtrack"),
    ("audio/s3k-music-2d-paced.wav", "ROM-derived audio", "FmSfxRenderTool --music 2D --paced"),
    ("audio/s3k-music-2f-paced.wav", "ROM-derived audio", "FmSfxRenderTool --music 2F --paced; not used"),
    ("audio/s1-music-81-paced.wav", "ROM-derived audio", "FmSfxRenderTool --music 81 --paced"),
    ("audio/rewind.wav", "ROM-derived audio", "Reversed slice of film.wav"),
    ("engine/openggf-sp-promo-a-r1.jar", "engine build", "Snapshot of feature/ai-sp-promo-a 0ba60490e"),
    # v2
    ("out/day-off-stageplay-v2.mp4", "authored native world review or promo", "Final promo v2, 140.03 s"),
    ("out/day-off-film-v2-1080p.mp4", "authored native world review or promo", "Final standalone film v2, 74.97 s"),
    ("captures/v2/t10-preview.mkv", "authored native world source movie", "Stageplay export of t10, 480x270"),
    ("captures/v2/day-off-v2-film-1080p.mkv", "authored native world source movie", "t10 --scale 4"),
    ("captures/v2/t10-sfx.mkv", "authored native world source movie", "t10 effects and voices stem"),
    ("captures/v2/t10.sim.jsonl", "native LIVE world simulation JSONL", "t10 simulate --every 1"),
    ("captures/v2/t10.timeline.jsonl", "generated state/diagnostic data", "t10 authored timeline with speech events"),
    ("captures/v2/editor-route/route.mkv", "lossless capture", "v2 in-engine route capture (picker)"),
    ("captures/v2/editor-tour/tour.mkv", "lossless capture", "v2 in-engine tour"),
    ("captures/v2/editor-tour/day-off.mkv", "authored native world source movie", "v2 editor Export film; streams = t10-preview"),
    ("captures/v2/editor-desktop-route/desktop-route.mkv", "lossless capture", "v2 desktop route capture"),
    ("audio/film-v2.wav", "capture audio (ROM-derived)", "t10 soundtrack with built-in voices"),
    ("audio/film-sfx-v2.wav", "capture audio (ROM-derived)", "t10 effects and voices stem"),
    ("audio/rewind-v2.wav", "ROM-derived audio", "Reversed slice of film-v2.wav"),
    ("engine/openggf-sp-promo-a-r2.jar", "engine build", "Snapshot of develop 81f25c89f"),
]
FRAME_DIRS = [("edit/frames/film", "frame-sequence"), ("edit/frames/route", "frame-sequence"),
              ("edit/frames/tour", "frame-sequence"), ("edit/frames/desktop-route", "frame-sequence"),
              ("edit/frames/desktop-tour", "frame-sequence"), ("edit/frames/film-v2", "frame-sequence"),
              ("edit/frames/route-v2", "frame-sequence"), ("edit/frames/tour-v2", "frame-sequence"),
              ("edit/frames/desktop-route-v2", "frame-sequence")]
SUPERSEDED_DIRS = ["captures/t02", "captures/t03", "captures/t04", "captures/t05", "captures/editor-r1",
                   "captures/editor-tour"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def inventory(d):
    h, total, n = hashlib.sha256(), 0, 0
    for p in sorted(d.iterdir(), key=lambda p: p.name):
        if p.is_file():
            size = p.stat().st_size
            h.update(f"{p.name}\0{size}\0{sha(p)}\n".encode())
            total += size
            n += 1
    return h.hexdigest(), total, n


def main():
    if ARCH.exists():
        shutil.rmtree(ARCH)            # only ever this script's own staging output
    files = list(SOURCES)
    for take in SUPERSEDED_SCENES:
        files += [f"scenes/{take}.screenplay.json", f"scenes/{take}.stageplay"]
    for g in GLOBS:
        files += sorted(str(p.relative_to(PROD)) for p in PROD.glob(g))
    rows = []
    for rel in files:
        src = PROD / rel
        if not src.exists():
            continue
        dst = SRC / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        rows.append(dict(path=str(dst.relative_to(ARCH)), root=ROOT_ID, original_path=rel,
                         bytes=src.stat().st_size, sha256=sha(src), snapshot="byte-copy"))
    for b, rel in BUILD_FILES.items():
        dst = SRC / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROD / b, dst)
        rows.append(dict(path=str(dst.relative_to(ARCH)), root=ROOT_ID, original_path=b,
                         bytes=dst.stat().st_size, sha256=sha(dst), snapshot="byte-copy"))
    assets = []
    for rel, kind, notes in EXTERNAL:
        p = PROD / rel
        assets.append(dict(root=ROOT_ID, path=rel, kind=kind, bytes=p.stat().st_size, files=1, sha256=sha(p),
                           notes=notes))
    for rel, kind in FRAME_DIRS:
        h, total, n = inventory(PROD / rel)
        assets.append(dict(root=ROOT_ID, path=rel + "/*.png", kind=kind, bytes=total, files=n, inventory_sha256=h,
                           notes="Frame-exact PNG decode of the matching capture"))
    for rel in SUPERSEDED_DIRS:
        d = PROD / rel
        big = [p for p in sorted(d.rglob("*")) if p.is_file() and p.suffix in (".mkv", ".jsonl", ".wav")]
        for p in big:
            assets.append(dict(root=ROOT_ID, path=str(p.relative_to(PROD)), kind="superseded capture",
                               bytes=p.stat().st_size, files=1, sha256=sha(p), notes="Earlier take or capture attempt"))
    fonts = sorted((PROD / "fonts").glob("*"))
    for p in fonts:
        if p.is_file():
            assets.append(dict(root=f"{PID}/fonts", path=p.name, kind="external editorial font", bytes=p.stat().st_size,
                               files=1, sha256=sha(p), notes="Fira faces (SIL OFL); not redistributed"))
    (PROJ / "external-assets.json").write_text(json.dumps(dict(
        project=PID, snapshot_date="2026-10-24",
        notes="External bytes hashed at staging time, not uploaded. edit/build render work, probe/ diagnostics, "
              "logs and Python caches are excluded.",
        sequence_hash="inventory_sha256 is SHA-256 over sorted PNG basenames; for each file append UTF-8 basename + "
                      "NUL + decimal byte length + NUL + lowercase SHA-256 + LF.",
        assets=assets), indent=1) + "\n")
    (PROJ / "README.md").write_text(README)
    rows.append(dict(path=f"projects/{PID}/README.md", root=ROOT_ID, original_path="(archive index)",
                     bytes=(PROJ / "README.md").stat().st_size, sha256=sha(PROJ / "README.md"), snapshot="written"))
    cat = ARCH / "catalog-rows"
    cat.mkdir(parents=True, exist_ok=True)
    (cat / "sources.json").write_text(json.dumps(rows, indent=1) + "\n")
    (cat / "projects.json").write_text(json.dumps([dict(
        id=PID, title="Day Off: Stageplay introduction promo",
        notes="Staged story film (a Motobug takes a day off across S1, S2 and S3K) followed by offscreen captures of "
              "both editors directing it; edit, capture driver, scenes, telemetry references and the superseded first "
              "cut. Films, captures, audio and frames remain external. Listening and real-time viewing not claimed.",
        source_files=len(rows), catalog_entries=len(assets))], indent=1) + "\n")
    (cat / "roots.json").write_text(json.dumps([
        dict(id=ROOT_ID, original=str(PROD), archive=f"projects/{PID}/sources/promo",
             notes="Day Off promo: byte-preserved edit, capture tools, scenes and records. Footage, ROM-derived audio, "
                   "frames, telemetry and the engine snapshot remain external."),
        dict(id=f"{PID}/fonts", original=str(PROD / "fonts"), archive="",
             notes="External Fira editorial faces; hashed, not redistributed.")], indent=1) + "\n")
    with open(cat / "assets.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["project", "root", "path", "kind", "bytes", "files"])
        for a in assets:
            w.writerow([PID, a["root"], a["path"], a["kind"], a["bytes"], a["files"]])
    print(f"staged {len(rows)} source files, {len(assets)} external asset entries -> {ARCH}")


README = """# Day Off: Stageplay introduction promo

Staged locally on 2026-10-24 for OpenGGF-Media; **not committed or pushed** (the brief asked for
local staging only). Produced by Claude Opus 5.5 in `/home/farrell/Videos/OGGF/sp-promo-a`.

The delivered external promo is `out/day-off-stageplay.mp4`: 130.2 s, 1920x1080 at 60 fps,
H.264, AAC 256 kbit/s, -15.5 LUFS / -1.3 dBTP after encode, 12 chapters. The standalone film is
`out/day-off-film-1080p.mp4` (74.97 s). The first half is a staged Stageplay story (a Motobug
takes a day off through Sonic 1, Sonic 2 and Sonic 3 & Knuckles). The second half is offscreen
captures of the in-engine and desktop editors directing the same scene, including the route
planner's failed Walk plan, its "needs Run" advice and the checked loop route.

## Version 2 (current)

`out/day-off-stageplay-v2.mp4` (140.03 s, -15.2 LUFS / -1.4 dBTP, 12 chapters) and
`out/day-off-film-v2-1080p.mp4` (74.97 s): engine develop `81f25c89f`, OpenGGF-Editor main
`dd5ee43`, film take `scenes/t10.stageplay`. Built-in voices for every speaker (the Motobug as an
object speaker with a tail), logical facing, native loop priority, `stageplay ground` floors, and
a re-captured making-of in the redesigned editor (level position picker, voice form and presets).
The film's route is the one the editor applied. Edit: [edit_v2.py](sources/promo/edit/edit_v2.py);
capture driver [EditorCapture2.java](sources/promo/tools/EditorCapture2.java) run by
[v2_chain.sh](sources/promo/tools/v2_chain.sh). See the v2 sections of the director's note and
provenance. v1 below is preserved unchanged.

## Sources and authority (v1)

- [Director's note](sources/promo/DIRECTOR.md): idea, least-certain sections, viewer pass,
  limits and Stageplay rough edges. [Provenance](sources/promo/PROVENANCE.md): every shot,
  scene file, command and verification. [Treatments](sources/promo/TREATMENTS.md).
- [Final edit](sources/promo/edit/edit.py) (promo_kit; brief in its docstring) and the superseded
  [first cut](sources/promo/edit/edit-r1.py); [chapters](sources/promo/edit/chapters.txt).
- Rebuild: [run_edit.py](sources/promo/tools/run_edit.py) `render`, then
  [mux_final.py](sources/promo/tools/mux_final.py) (true-peak gain, chapters, mux).
- Capture tools: [EditorCapture.java](sources/promo/tools/EditorCapture.java) (display-free
  editor capture, in-engine HUD or desktop ImGui chrome) run by
  [capture_editor.py](sources/promo/tools/capture_editor.py); [sp.py](sources/promo/tools/sp.py)
  (StageplayTool launcher). Each capture's `events.json` is preserved.
- Scenes: [generator](sources/promo/scenes/build_scene.py), the final
  [screenplay](sources/promo/scenes/t06.screenplay.json) and [scene](sources/promo/scenes/t06.stageplay),
  the before-route and SFX-stem takes, the route plan, measured data, the voice and skins.
  Earlier takes (`take01`, `t02`-`t05`) are superseded.

## Engine references

OpenGGF `feature/ai-sp-promo-a` `0ba60490e` (632a5f8c3 + the Sonic 1 loop-plane route-probe fix,
unmerged); OpenGGF-Editor `feature/ai-sp-promo-a` `146e076`. Snapshot jar hash in
external-assets.json.

## External, not uploaded

[external-assets.json](external-assets.json) hashes the finished films, the lossless captures,
ROM-derived audio, the frame sequences (inventory hashes), native simulation telemetry, the
engine snapshot, superseded captures and the fonts. ROMs are never included.
"""

if __name__ == "__main__":
    main()
