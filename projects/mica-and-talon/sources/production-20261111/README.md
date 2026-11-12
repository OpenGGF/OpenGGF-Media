# MICA & TALON — production promo (2026-11-11)

Final promo for the official OpenGGF example character mod `examples/mica-and-talon`. It supersedes the
2026-11-10 promo (`mt-promo-20261110`, "a very rough cut" per the owner).

- `out/master-16x9.mp4` — 1920×1080, 60 fps, H.264 High, yuv420p, AAC LC 320k, chapters
- `out/master-9x16.mp4` — 1080×1920, designed vertical cut: stacked comparisons, portrait framings, recomposed lock-up and end card
- `out/chapters.txt`, `out/shot-index.csv` (every capture used: entry kind, declared setup, commit, command),
  `out/verification.json` (ffprobe, full decode, loudness), `out/contact-*-2fps.jpg`, `out/viewer-pass.md`
- `edit/edit.py` — brief (docstring), beat sheet and compositor (`tools/media/promo_kit.py`)
- `tools/` — capture driver, bed splice, SFX render, mastering/measurement, chapters, contact sheets, probes
- `hosts/` — PromoCapture hosts (original/starpost from the 2026-11-10 promo; `declared` adds -Dpromo.rings/-Dpromo.timer)
- `checkpoint1/`, `checkpoint2/` — storyboard and draft checkpoints with the lead's reviews applied

## Source

- OpenGGF `feature/ai-mt-promo-production` = `b088fae95b` (integration `fada66cea4` + TALON S2 title gaze
  `af916788e7`/`b088fae95b`). No repository changes. Example jar sha256 `79796eae301420ff10e625a6434c950131856d61a09567a7f35aae4997a2cf6b`.
- Every capture was re-shot from that build; the S2 title capture was taken after the gaze merge.
- Captures: `GameplayCaptureTool` (positioned starts or title-first boot) and the retained `PromoCapture`
  hosts, silent, 60 Hz, every=1, surfaceless EGL, no trace input. Full commands per capture in
  `captures/<id>/provenance.json` and `out/shot-index.csv`.

## Music

"RUN INTO THE SUNSHINE (Chiptune Remix)", owner-supplied, 48 kHz stereo, 162.8 s,
sha256 `569a921b69983c1a6f2916c6be963bb134a39aaa742b0624044fbe4baf8481ff`. Not in any repository.
172.218 BPM, bar 0 at 0.178 s (the kit's first-beat estimate of 0.002 s is half a beat early; confirmed against the bar-12 and
bar-36 drop onsets). Edit (`tools/build_bed.py`): source bars 8–35 then bars 76–end, one bar-line splice with a 12 ms
equal-power crossfade; the track's own ending (final hit bar 115) is untouched. The film fades to black on the final hit
(93.37 s) and runs on black through the ring-out. ROM stingers rendered with `FmSfxRenderTool --sfx <id> --paced`
(S3K $B3 Big Ring, $B4 Explode, $9F Super Transform; S2 $C1 Explosion, $CF Signpost), each on its event frame from
the capture's state.csv. Mastered to −14 LUFS with two-pass linear loudnorm; measured on the encoded AAC.
**Sound was checked by measurement only.**

## Positioned starts and debug entries (disclosure)

- Gameplay shots are positioned starts with declared rings and timer (`--rings/--timer`, or `-Dpromo.*` on the
  declared host), not continuous cold routes. Powered-up shots declare 70 rings and 7 emeralds, mid-act at 2:00–2:15.
- MGZ2, S1 GHZ2, S2 EHZ2/ARZ homing takes use the `hero` host (solo MICA, positioned).
- Half-pipe: debug-positioned ROM starpost component entry (real ring collision admits SPECIAL_STAGE), neutral steering.
- Continue and S2 ending: debug component entry through the production providers (as in the 2026-11-10 promo).
- Data Select: declared team save slots; title screens: cold title-first production boots with neutral input.

## Known limits (not filmed as it ships, or omitted)

1. **S1 results card fault (engine, not mod).** In S1 GHZ1 the act oval and its blob render over "HAS PASSED" and
   "SCORE". A stock-Sonic control at the same position and input shows the identical fault:
   `checkpoint1/s1-results-mica-vs-stock.png` (control capture `captures/ghz-clear-stock-control`). The promo shows
   S1 to the signpost only; results are shown in S2.
2. **Competition omitted.** The S3K Competition capture reaches player select (still cycling stock portraits there),
   then `GameplayCaptureTool` throws in the arena draw: `IllegalStateException: Native arena has no published VInt
   registers` (`captures/competition/capture.log`).
3. **Slot reels omitted.** They need a positioned slot-machine setup that was not built for this promo.
4. **S2 homing chain.** About 20 positioned probes in EHZ1/EHZ2 found no multi-badnik airborne chain; S2 shows single
   lock-on strikes (EHZ2 Buzzer in the triptych, ARZ Whisp close-up). S3K (MGZ2, three Mantises) and S1 (GHZ2, two
   2-badnik chains) are real chains (native score steps).
5. **Stock art cropped out.** The S3K title's small Tornado fly-by (title src 412–510) and the S2 ending's side-view
   Tornado ("SONIC" decal) are unreplaced stock art; the S3K push stays right of x≈96 from src 408, and the ending
   starts on the front-view pose (src 4080).
6. The S2 title-card glyphs were dropped for editorial type at the lead's request (their split strokes read "/\/\ICA");
   the native "MICA GOT THROUGH ACT" results lettering is kept as it ships.
7. The ending capture's state.csv observes the detached capture loop, not the Engine ending loop.

## Rebuild

Java 25, Python with numpy + Pillow (the 2026-11-10 venv), ffmpeg, fonts: Fira Sans Compressed Heavy / Heavy Italic
(lock-up, headers) and Fira Sans / Hack from the system font path (`/usr/share/fonts/TTF`, `promo_kit.py fonts` shows
no FALLBACK), plus `mt-promo-20261110/final/fonts` (`PROMO_FONT_DIRS`), the user's verified ROMs symlinked in the checkout.

```sh
mvn -q -o -Dmse=off clean compile && python3 examples/mica-and-talon/build.py     # in the checkout
python3 tools/capture.py --checkout <checkout> [--extra extraN.json --only <ids>]   # captures (extra1-6 + base)
python3 tools/render_sfx.py <checkout>; python tools/build_bed.py music/<wav> work/bed.wav
python3 <checkout>/tools/media/promo_kit.py render edit/edit.py                    # 16:9 (MT_VERTICAL=1 for 9:16)
python3 tools/chapters.py; python3 tools/finish.py work/build-h out/master-16x9.mp4 work/chapters.ffmeta
python3 tools/finish.py work/build-v out/master-9x16.mp4 work/chapters.ffmeta
```

## Review history

- Lead checkpoint 1 (storyboard): approved with changes — editorial TTF lock-up instead of S2 card glyphs; half-pipe
  pane needed a subject; crop the S3K title Tornado; record the S1 results fault and the Competition/reels omission;
  rerun `check` after stinger gains; prefer non-green zones (→ ARZ homing, CPZ flight).
- Lead checkpoint 2 (draft): approved — hide the S2 ending's "SONIC" decal and accompany the pose (→ start on the
  front view, punch on the landing, "ENDINGS TOO" pill); punch in on TALON's Solar transformation and release for the
  kill; punch the EHZ pops; queued fixes (stinger sync, $9F level, S2 signpost sound); designed 9:16 cut.
- Lead final review (2026-11-11): 16:9 approved as is; 9:16 fix — the S1/S2 bands of the stacked homing split left a
  ~25% navy strip (side padding meant for the 16:9 slices). 9:16 bands now track MICA full-width with no padding; the
  stacked signposts now fill the 1080 width (3.375×, slide in) instead of a framed 3× panel. Titles, special stages and
  TALON/powered pairs were already full width. `master-9x16.mp4` re-rendered.
- Found during that fix: in the last ~0.3 s of the signpost pair (≈47.1–47.4 s, and through the push) the S1 pane
  showed the faulty S1 results card entering (src ≥ 322). The edit now starts the S1 pane at src 135 (MICA running
  into the signpost) so it ends at src 316. The lead checked the fixed 16:9 at 46.9, 47.15 and 47.35 s and promoted it:
  `out/master-16x9.mp4` is now the fixed render; the earlier approved master is kept as
  `out/superseded/master-16x9-pre-s1fix.mp4` (with its loudness JSON and contact sheet) and contains the 0.3 s leak.
