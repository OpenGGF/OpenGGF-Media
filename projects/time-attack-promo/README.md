# Multiplayer Time Attack promo ("One more go")

Finished production, 2026-10-23. The delivered external film is
`out/openggf-multiplayer-time-attack-promo.mp4`: **81.817 seconds**, 1920×1080 at
60 fps, H.264, stereo 48 kHz AAC 256 kbit/s, loudness-normalised to −15 LUFS /
−1.5 dBTP, with nine embedded chapters. It shows the multiplayer Time Attack
bundled mod on OpenGGF develop. It was produced by **Claude Opus 5.5**
as "Film A", one of two competing takes on the same brief. The user chose it and
then refined it over several review rounds. The other take ("Film B", by
GPT-6.1-Sol) is not part of this archive.

Every shot is the real engine driven through its real UI by a display-free
capture driver. The rivals are test clients replaying recorded runs, and the
256-player chapter is a capacity test; the end card says both.

## Sources and authority

- [Final edit](sources/promo/edit/edit.py) (promo_kit; the brief is in its
  docstring) and [frame mapping](sources/promo/edit/capmap.py): authoritative.
  The edit's source frames were written against the earlier takes;
  `capmap.py` shifts each one by its chapter's delta into the current take
  (`captures/*/edit-chapters.csv` against `captures-v3/*/chapters.csv`).
- [Clip extraction](sources/promo/edit/prep.py) and
  [master](sources/promo/edit/finalize.sh): two-pass loudnorm, chapters and
  faststart mux.
- [Director's note](sources/promo/DIRECTOR.md): the idea and the three least-certain
  sections, written for the first cut, followed by a short note on later revisions.
- [Provenance](sources/promo/PROVENANCE.md): shot-by-shot sources, fixtures and
  every review revision with the user's words and the response (audio balance and
  PCM, picture and cue timing, new lobby UI, editorial type, re-capture against
  the precise timer and full-width progress bar, the stack cap and framing).
- **Superseded edits**: `edit.v1-audio.py` … `edit.v5-before-recapture-framing.py`
  and `prep.v3-oldlobby.py` are kept in order for comparison, not for rendering.
- [Capture driver](sources/promo/scripts/driver/): `PromoCapture` and `PromoPeers`
  (package `openggf.racing.server.tools`, compiled against the engine and
  `racing/server/build.py` classpath; never committed to the engine),
  `NameplateDump`, and the audio probes `LiveMusicRender` and `DacProbe`.
- [Capture runners](sources/promo/scripts/): `run-promo-v3.sh` and
  `capture-all-v3.sh` for the current takes; `run-promo.sh` and
  `run-promo-newui.sh` for the superseded ones.
- Capture records (`captures-v3/<take>/`, `captures/superseded/<take>/`): args,
  chapters, source commit and status, result, audio rate and Time Attack settings.
  Current takes keep their per-frame `state.csv`.
- [Route](sources/promo/route/ghz1.route) and the editorial plate index
  (`design/plates/index.tsv`).

## Engine references

Current takes: OpenGGF develop `62521a43a` (lobby, names and profile) and
`f829713b1` (all three races, after the progress-bar stack cap). Each take's
`source-commit.txt` is authoritative. Engine work delivered alongside this film:
the race lobby redesign, the DEZ launcher countdown cues, the in-engine
hundredths timer, the full-width progress bar with hurt flash and stacking, and
the promo-direction skill revision.

## External, not uploaded

[external-assets.json](external-assets.json) hashes the final film and its
pre-normalisation picture, the lossless FFV1 captures and their PCM, ROM-derived
music and SFX renders, the editorial plates and fonts. Fonts are not
redistributed. Frame and PNG directories are hashed as sequences. Render work
(`edit/build`), capture working directories and profiles, compiled classes and
the earlier local staging tree are excluded.

Rebuild: build the engine at each take's commit (`mvn -Dmse=off package -DskipTests`,
then `python3 racing/server/build.py`), compile the driver against
`target/racing-server/java-args.txt`'s classpath into `scripts/driver/classes`, and run
`scripts/capture-all-v3.sh`. Then run `edit/prep.py`, `promo_kit.py render edit/edit.py`
(with `PROMO_FONT_DIRS` set to the fonts) and `edit/finalize.sh`. Paths are absolute
to `/home/farrell/Videos/OGGF/ta-promo-a`; to relocate, edit `ROOT`/`P` at the top
of each script.
