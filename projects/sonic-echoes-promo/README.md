# Sonic Echoes promo ("Team up with yourself")

Finished production, 2026-10-24, awaiting user review. The delivered external film is
`out/sonic-echoes-promo-final.mp4`: **74.3 seconds**, 1920×1080 at 60 fps, H.264, stereo 48 kHz
AAC 256 kbit/s, −16.1 LUFS integrated, −3.5 dBTP true peak (measured on the encoded file), eight
embedded chapters, faststart. It shows Sonic Echoes, a Sonic 2 time-loop puzzle example mod on the
OpenGGF `feature/ai-sonic-echoes` branch (`5fca08819f` for footage; fixes found while filming in
`364d7d02a0`). Edit and assembly by **Claude Opus 5.5**; footage captured by two **GPT-6.1-Sol**
workers to the lead's shot list.

Every shot is a display-free engine capture of the real mod driven by the rooms' authored reference
inputs; Echo/Reset presses are scheduled at authored loop frames. One half-speed moment is labelled
on screen. See [provenance](sources/promo/PROVENANCE.md) for entry methods, measurements and review
rounds.

## Sources and authority

- [Final edit](sources/promo/edit/edit.py) (promo_kit; the brief is in its docstring): authoritative.
  [echokit.py](sources/promo/edit/echokit.py) holds the S2 title-card header, logo, input tape,
  sidecar access and stinger routing; [echofont.py](sources/promo/edit/echofont.py) renders the mod's
  own 5×7 face (read from the mod's `EchoUi.java`) with its echo-contour trail.
- [Master](sources/promo/edit/master.py): two-pass loudnorm and limiter, video stream copied;
  chapters from [chapters.ffmeta](sources/promo/out/chapters.ffmeta) ([CSV](sources/promo/out/chapters.csv)).
- [Shot list and capture rules](sources/promo/SHOTLIST.md), including the per-frame `session.csv`
  sidecar specification every edit sync reads.
- Per-take [capture records](sources/promo/captures/): command lines, input scripts and logs,
  scheduled actions and NOTES with event-frame tables. [HELPER.md](sources/promo/captures/HELPER.md)
  documents the test-only capture jar; the helpers themselves are committed in the engine repository
  (`examples/sonic-echoes/src/test/java/echoes/Promo*CaptureMod.java`, builder
  `examples/sonic-echoes/tools/build_capture_jar.py`).
- [Import script](sources/promo/archive_to_media.py) that produced this directory and its catalog rows.

## Rebuilding

Requires an OpenGGF checkout with `tools/media/promo_kit.py`, numpy, Pillow, ffmpeg, the Fira
editorial faces and the external captures/audio listed in [external-assets.json](external-assets.json).
The edit's paths are absolute to the original task directory (`/home/james/tmp/sonic-echoes-promo`)
and the engine checkout; relocate `TASK` and the `sys.path` entries in `edit.py` / `echofont.py`.
Then `promo_kit.py render edit/edit.py` and `python3 edit/master.py`, then mux chapters.

## External

Lossless captures (eleven frame sequences), state/session sidecars, capture previews and jars, the
ROM-derived Chemical Plant bed and SFX stingers, the PCM mix, the rendered, mastered and final films,
and fonts are hashed in [external-assets.json](external-assets.json); none of their bytes are here.
