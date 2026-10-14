# Sonic3K Chaos Mode demo reel

`out/sonic3k-chaos-mode-demo.mp4` is an89.4-second promotional edit:1920×1080,
60fps H.264, stereo48kHz AAC. It follows the earlier Flappy Tails and Typing of
the Hedgehog trailer language: ROM-lettered slams, navy/gold graphics, deadpan
captions, explicitly fictional character reviews, native sound stings and a
post-credit bumper gag. Slay the Robotnik informed the feature-led structure.

Every gameplay shot is a production OpenGGF capture at real presentation speed.
Gameplay has its synchronous native PCM. Cards use editorial S3K music and
sound stings, with their original provenance in `assets/README.md`. No commentary
voice or unrelated soundtrack was generated. Full400×224 game frames are kept
at4× integer nearest-neighbour scale within the1080p canvas; the HUD stays in view.

## Sources and scope

- Engine source: `ea8c9c6275a91f3ae3f875f2e57cc2d680f0ea31` on develop.
- Mod: `artifacts/sonic3k-chaos-mode.jar`, SHA256
  `954b580e8566cca2803bc8e11d59f229e41f1b4559a64797e63e1e6877165ba1`.
- S3K ROM: CRC32`63522553`, SHA1`CFBF98C36C776677290A872547AC47C53D2761D6`.
  The user's existing ROM supplied native assets; no ROM is bundled here.
- Direct-level shots start from native AIZ1 with solo Sonic. Each selected pool
  contains one effect, interval5s, duration1×, seed22. That seed's first severity
  ticket is99; it admits the first effect through the normal scheduler at active
  clock600. Rarity, qualification and cooldown rules remain active. This is a
  curated feature reel, not one continuous random session or the default30s rate.
- Overdrive alone uses declared centre8912,877, near the native Bloominator at
 9072,892. Its approach is bypassed; no rings, checkpoints or event state are seeded.
- The menu shot uses a fresh preference root, actual controller navigation,
  native No Save/team selection and a native Sonic launch. It adds one available
  effect, removes Bobble Head, and shows the actual lists/timing controls.
- Ghost Party supplies an actual death at source frame840. Pong shows one return,
  not a completed win; Monitor Stack shows placements, not a cleared line. Flash
  Flood is a local fluid circle. The invisibility cut ends before a native vine
  interaction which restores that native object's player presentation authority.
- All shots are AIZ1; this edit does not certify other acts/teams, every105 effect,
  hub return or future streamer voting. No engine/mod code changed for the reel.

Each capture retains `input.script`, round-tripped BizHawk `input.txt`, full
`output/state.csv`, source PCM, saved preferences, `provenance.json` and a compact
lossless RGB master. `out/lossless-source-checks.json` records exact decoded RGB
equality PNG→FFV1→RGB-H264 and unchanged native PCM/frame cadence. Redundant raw
PNG frames and temporary encodes were removed after verification.

## Rebuild

Requires the pinned source checkout compiled with Java25, the user's verified
S3K ROM, ffmpeg/ffprobe and Python with Pillow. Use an isolated checkout's own
target directory, following repository build/queue guidance.

```sh
python3 examples/sonic3k-chaos-mode/build.py
OPENGGF_WORKTREE=/absolute/checkout \
OPENGGF_S3K_ROM='/absolute/Sonic and Knuckles & Sonic 3 (W) [!].gen' \
CHAOS_MEDIA_ROOT=/absolute/new-capture-root \
python3 /path/to/this-folder/capture.py dvd heads wind bumper ghosts gravity \
  trails moon mirror negative scenery magnet pong stack menu bobble invisible \
  flood ghost-close overdrive pong-play rain
```

The archived jar is used by default; `CHAOS_MOD_JAR` can select a new package.
The capture uses surfaceless EGL and removes display variables; it never sends
keyboard/focus events to the shared desktop. Existing source masters are retained.
For a new cut, copy this task folder or use a versioned output location so earlier
user-delivered products stay intact. From this folder:

```sh
python3 card_renderer.py
python3 assemble.py
```

`edit.json` is the maintained edit decision list. `out/chapters.csv`,
`out/edit-timeline.json` and `out/chapters.txt` map every final shot to its source
interval. `--resume` only reuses unchanged per-shot edit rows; discard `work/`
if source media, fonts or renderer code changes. `compact_sources.py` is the
verified lossless archival step after new captures. A rebuild from retained
masters does not need to run the engine again.

The final file was checked for dimensions, codec/cadence, exact duration/frame
count, all30 chapter boundaries, audio levels and complete error-free decode.
Consecutive-frame strips cover effect arrival, motion, Pong return and ghost
death; `out/reel-contact-sheet.png` supplies the editorial overview.
