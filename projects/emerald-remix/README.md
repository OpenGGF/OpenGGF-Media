# Emerald Remix — coached promo

Finished production, 2026-10-22. The delivered external film is
`out/emerald-remix-promo.mp4`: **41.683333 seconds / 2,501 frames,
1920×1080 at 60 fps**, H.264 CRF 20, yuv420p, stereo 48 kHz AAC at a
requested 192 kbit/s. It was produced by **GPT-6.1-Sol under Claude Opus 5.5
coaching**. This source archive preserves the revisions and criticism that led
to the finished edit; archiving approval does not imply approval of every draft.

## Sources and authority

- [Final edit and inline brief](sources/promo/edit.py): authoritative picture edit,
  including all three coach fixes after round 5. Its original rough-only docstring
  is historical; `EDIT.out` now selects the master.
- [Round-5 edit before the coach fixes](sources/promo/edit.r5.py): **superseded**.
- [Round-5 production record](sources/promo/STATUS.md),
  [capture-session record](sources/promo/STATUS.capture-session.md) and
  [planning-session record](sources/promo/STATUS.planning-session.md): preserved
  verbatim. `STATUS.md` predates the final coach fixes, mastering and approved
  archive; its claims that no master/archive was requested are historical.
- [Eleven-shot chapter/edit map](sources/promo/chapters-round5.json) and
  [preview ranges](sources/promo/previews/ranges.json): final shot boundaries;
  post-round-5 fixes change overlays, not these intervals. The chapter named
  “spring and 22 pickups” still describes real source pickups; its added pickup
  panel was removed from the final picture. These are sidecar chapters; the
  supplied final encode command does not embed them.
- [Revised beat sheet](sources/promo/BEAT_SHEET_REVISED.md): **superseded round-4
  treatment**, 2,602 frames / 43.366667 s, not the final 2,501-frame timeline.
- [Original brief](sources/promo/BRIEF.md),
  [original beat sheet](sources/promo/BEAT_SHEET.md),
  [shot list](sources/promo/SHOT_LIST.csv) and
  [capture plan](sources/promo/CAPTURE_PLAN.md): **superseded plans**. Retained
  for intent and decisions, not instructions to overwrite the final production.
  [Research](sources/promo/RESEARCH.md) is historical supporting material.
- [Round-4 edit, status and preview driver](sources/promo/revisions/round4/):
  **superseded / rejected**. Earlier plan/doc writers in
  [scripts](sources/promo/scripts/) are historical and can overwrite later files;
  do not run them over this archive or a finished production.
- [Capture/input/render/analysis scripts](sources/promo/scripts/),
  [exact capture command log](sources/promo/scripts/commands.jsonl),
  [controller scripts and BK2 input logs](sources/promo/inputs/),
  [small measured state CSVs and capture provenance](sources/promo/captures/),
  [music analysis](sources/promo/audio/MUSIC.md) and
  [type sampling](sources/promo/design/revision/type-sampling.json) retain their
  original bytes and layout. BK2s contain only `Header.txt` and `Input Log.txt`;
  they include no emulator save state or ROM.

## Revision history and the user's feedback

The early plan was too restrained: inset footage, a quiet title and establishing
shots before the hero. Coaching moved the unrolled corkscrew tumble to the cold
open, added a flash/stinger/slam title, and required visible proof for the pitch.
Wide stacked original/remix comparisons made TWO versus THREE countable; the
hero's capture was changed from a spindash ball to running tumble poses. Editorial
Clover lettering replaced a native custom-zone card unavailable in shipping defaults.

On **round 3**, the user said **"it's use of palettes with the text is horrible,
particularly around the drop shadow"** and **"the video is just very... boring ...
very lazy with long stretches of level showcased without any accompanyment"**.
The next edit restored the Sonic 2 title glyphs' actual white/grey/black palette,
embedded black shadow and whole-glyph-pixel effects. The double + single ROM-art
assembly explained the triple's construction. However, its small generator
illustration and repeated Clover slogans still left the same long take doing
most of the work. Those captions were an inadequate response to the boredom
feedback, even though the then-current mechanical checker accepted them.

On **round 4**, the user said **"minimal effort has been put in to achieve the
goals"**. Round 5 replaced the slogans with an event-led spring/landing/pickup,
complete-jump and goal sequence, trimming empty travel at native speed. A full
landscape and the entire 5,120-pixel route build from the actual Clover pixel
function, then open into gameplay through a gold-ring iris. Native lettering
sits on Sonic 2 blue bands with red tabs and yellow footers. Its entrance was
coupled to the backing after review caught exposed letters during the transition.
State CSVs locate the spring, landing and ring changes; the edit adds aligned
punches and ROM cues. Rejected alternatives and their reasons remain in `STATUS.md`.

On **round 5**, the user said **"notable improvements"**. The final edit adds
three coach corrections after that reviewed round:

1. The “A ZONE DRAWN BY CODE” header exits before the CLOVER VALLEY band arrives,
   preventing stacked blue headers.
2. The extra pickup panel is removed because the native RINGS HUD already counts
   rings. The event-led cuts, spring/landing accents and ring blips remain.
3. The end-card status is **“Development example”**, replacing “Development
   example · free”. The separate fan-made/ROM disclaimer remains.

`edit.r5.py` preserves the exact pre-fix edit; `edit.py` is the corrected master
source. The final film is encoded from `out/emerald-remix-master.mp4` with the
explicit loudness-normalisation pass below.

## Engine and coaching references

The compositor imported by the edit is `tools/media/promo_kit.py` from
`/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`, branch
`feature/ai-promo-skill-coaching`, at
[`7d7246fbe0913683b88d114b4081d73fc039b80a`](https://github.com/OpenGGF/OpenGGF/commit/7d7246fbe0913683b88d114b4081d73fc039b80a).
The following coaching/tool/skill commits are preserved by reference to that
checkout's Git log (the final checkout was clean when inspected for this archive):

| Commit | Coaching response / tool or skill change |
| --- | --- |
| [`f11ad311f`](https://github.com/OpenGGF/OpenGGF/commit/f11ad311fa66016a1729435db21de655aa153600) | Showcase defaults, visible proof, hero-first plan and correct music/SFX paths. |
| [`2f18020da`](https://github.com/OpenGGF/OpenGGF/commit/2f18020dae5ad9b1c59918cc5d15c474a9bb10ba) | Wide stacked split, countable comparison, running pose and shipping-card lessons. |
| [`369332604`](https://github.com/OpenGGF/OpenGGF/commit/3693326049c0d61cc637246541ed6017e1772c9a) | Keep type clear of native HUD; judge bitmap letters at final size. |
| [`c6d96fb37`](https://github.com/OpenGGF/OpenGGF/commit/c6d96fb37ac372663a3a4b284945e064d58e1eea) | Detect bare gameplay, preserve bitmap palettes/pixel effects and fix CLI class identity. |
| [`7d7246fbe`](https://github.com/OpenGGF/OpenGGF/commit/7d7246fbe0913683b88d114b4081d73fc039b80a) | Captions no longer satisfy accompaniment; require stronger treatments and viewer pass. |

These commits' trailers credit Claude Opus 5.5. The production authorship is
GPT-6.1-Sol under that coaching, as supplied in the archive brief. Capture source
commits remain those in each original `provenance.json`; the final compositor
commit is not retroactively assigned to older footage. Final-selected captures
come from `f11ad311f` and `2f18020da`. The archive does not assert the engine branch
has already merged to develop or been pushed.

## Final film and mastering

Fresh archive-time `ffprobe` inspection confirmed 2,501 video frames, 60/1 fps,
1920×1080 yuv420p H.264 and stereo 48 kHz AAC. File size is **68,182,054 bytes**;
its SHA-256 is in [external-assets.json](external-assets.json). The pre-normalisation
master is **117,057,278 bytes**. The exact supplied command, run in `out/`, is:

```sh
ffmpeg -i emerald-remix-master.mp4 -c:v libx264 -preset slow -crf 20 -tune animation -pix_fmt yuv420p -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-13.35:measured_TP=-1.62:measured_LRA=1.70:measured_thresh=-23.44:offset=0.14:linear=true,aresample=48000" -c:a aac -b:a 192k -movflags +faststart emerald-remix-promo.mp4
```

Archive-time full-file decode and `ebur128=peak=true` measurement of the **final
encoded AAC** reported **−13.9 LUFS integrated, 1.6 LU range and −2.3 dB true
peak**. This is distinct from the historical rough's −13.2 LUFS and from the
normaliser's supplied master-input measurements. [Archive provenance](archive-provenance.json)
records the commands, values and final-source hash. No edit or film was rendered
again for this source archive. Physical listening, a new visual acceptance pass,
gameplay parity and a fresh engine suite are not claimed. The historical motion,
cut, source-interval and full-decode review scope remains in `STATUS.md`.

## Provenance limits and rebuild

This is edited native-speed gameplay with scripted controller inputs and clearly
editorial art diagrams. Corkscrew sources and the closing tail have positioned
entries; stock/remix openings and the retained Clover route use cold direct-act
loads. The finished selection does not establish a continuous EHZ-to-Clover run,
an uninterrupted Clover completion or ROM parity. The landscape build is an
explanatory graphic from the real generator, not an editor UI recording. Original
capture preferences record `mods.skipModZoneTitleCards: true`; the blue Clover
name band is editorial, not evidence of a repaired native custom-name card.

The original production root is
`/home/farrell/Videos/OGGF/emerald-remix-promo`, mapped to
`sources/promo/` by `emerald-remix/promo` in [roots.json](../../catalog/roots.json).
[Source hashes](../../catalog/sources.json) cover each imported production file.
[assets.csv](../../catalog/assets.csv) lists external dependencies; the compact
[external hash inventory](external-assets.json) adds per-file SHA-256 and
content-addressed frame-set inventory hashes, with the exact set-hash algorithm.
It includes captures/PNG sequences, design/glyph artwork and extracted glyph
text, ROM music/SFX, preview/review images and films, master and final films, and
separately supplied editorial fonts. Build/render scratch, Python caches and
compiled dependencies are excluded. Fonts were hashed from the current installed
files; their render-time file identity was not recorded. No media, ROM bytes,
ROM-extracted art/audio, frame dumps or credentials are committed here.

Rebuild in a **new writable production copy**, never in the archive:

1. Restore `sources/promo/` as the production root; relink the external dependencies
   using the catalogs. Preserve original relative paths and filenames.
2. Use an isolated engine checkout at the pinned compositor revision, its
   `examples/emerald-remix` and Java 25. Supply your own Sonic 2 World REV01 ROM
   (original SHA-1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`). Rewrite the original
   absolute checkout, ROM, Java, Maven classpath and production paths in the
   writable copy, including `edit.py`, scripts and capture preferences. Original
   paths in JSON/command logs are provenance, not portable shell commands.
3. Supply Python with NumPy/Pillow, ffmpeg/ffprobe and the external Fira faces.
   The kit resolves font roles by installed filename; use `PROMO_FONT_DIRS` and
   its `fonts` command to check those choices. Regenerate absent ROM glyphs with
   `scripts/extract_title_font.py` and audio via the retained render scripts.
   `prepare_revision.py` and `prepare_round5.py` generate the diagram assets from
   retained captures and the example's real generator.
4. The final edit's `EDIT.out` points to the master; use the pinned kit's `render`
   command with the copied `edit.py`. `render_round5.py` explicitly writes rough
   previews and `verify_revision.py` verifies those rough outputs; neither is a
   final-mastering command. Apply the exact final encode above to a new output
   and verify its decode/intervals, chapters, audio and moving cuts anew.

See [archive policy](../../docs/archive-policy.md),
[rebuilding guidance](../../docs/rebuilding.md) and
[engine references](../../docs/source-references.md) for scope and rights.
Catalog entries identify local external files; they are not downloads.
