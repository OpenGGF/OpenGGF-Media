# MICA & TALON — promo redo (2026-11-12)

Public promo for the official OpenGGF example character mod `examples/mica-and-talon` (MICA, a jade pangolin, and
TALON, a slate falcon). It answers the owner's feedback on the 2026-11-11 production promo and supersedes it.

- `out/master-16x9.mp4` — 1920×1080, 60 fps, H.264 High, yuv420p, AAC 320k, 9 chapters, 124.00 s
- `out/master-9x16.mp4` — 1080×1920, same sound and cut times, every picture recomposed for the tall frame
- `out/chapters.txt`, `out/shot-index.csv` (every capture on screen: entry kind, declared setup, commit, frames
  used in each cut, command), `out/usage-16x9.json`, `out/usage-9x16.json`, `out/verification.json`,
  `out/promo_kit-check.txt`, `out/stinger-levels.json`, `out/viewer-pass.md`, `out/contact-*-2s.jpg`
- `edit/edit.py` — the brief (docstring), the tracked bar grid and both cuts (`MT_VERTICAL=1` selects 9:16);
  it runs on `tools/media/promo_kit.py` from the OpenGGF checkout
- `tools/` — capture driver, music analysis and beat tracking, bed, SFX render, mastering and measurement,
  chapters, usage and overrun audit, contact sheets, checkpoint builders, archive
- `hosts/` — `PromoCapture` capture hosts (`declared`, `starpost`, `original`, `positioned`, `powered`)
- `shots/` — capture batches (`batch1..40.json`); `captures/<id>/provenance.json` holds each take's command
- `checkpoint1/`, `checkpoint2/`, `checkpoint3/` — storyboard, draft and climax reviews with the edit as it stood
- `final/vertical-review.html` — the 9:16 review page for the lead (540 px copy, contact sheet, framing table)

**Sound was checked by measurement only. Nobody listened to these files.**

## Source

- OpenGGF `feature/ai-mt-promo-redo` = `1e0faac123` (the integration build with the art and gameplay fixes).
  No repository changes were made. Example jar sha256
  `449ada47b0e963d9fcc630255fed80f4fbad7b53390bdebd21e35386381abfce`.
- Every capture was shot fresh from that build: `GameplayCaptureTool` (positioned starts or cold title-first
  boots) and the `PromoCapture` hosts, silent, 60 Hz, every frame, surfaceless EGL, no trace input, one JVM at a
  time. 34 captures are on screen; no shot outlives its source in either cut (`out/usage-*.json`).
- ROMs are the user's verified dumps, read in place. No ROM, frame, extracted audio or music file is in any
  repository.

## The owner's feedback and what the film does about it

1. **No zoom at the start.** The film opens on 0.55 s of black and then the Sonic 3 & Knuckles roll-in at its
   whole width, as it ships, with no camera move. No shot in the 16:9 cut zooms or pans inside a take; framing
   changes only on cuts. (The 9:16 cut has three framing cuts inside takes, listed below.)
2. **The music plays from its start without a splice.** The bed is the owner's track from 0 s, untouched, with one
   fade. The film's length follows the music.
3. **Every fixed feature, filmed fresh:** jade trail against gold trail on the same Rhinobot; Gilded glints and
   the animated transformation; Hyper after-images and the one-hit Instagib; Solar embers, flare and animated
   transformation; carry and flight as one character; the Sonic 2 title pop-out; TALON piloting the Tornado in
   Sky Chase and in the ending's front-view pose; lives reading TALON; the new powered designs; TALON at the
   37 px rung framed as a partner of the same size.

## Music

"RUN INTO THE SUNSHINE (Chiptune Remix)", owner-supplied, sha256
`569a921b69983c1a6f2916c6be963bb134a39aaa742b0624044fbe4baf8481ff`. It is in no repository; the archive names it
by title and hash only.

- Measured (`tools/music_analysis.py`, `tools/beat_track.py`, `tools/music_sections.py`): bar 0 at 0.178 s;
  172.2 BPM up to bar 43, easing to 170.2 by bar 80; the pulse breaks down from bar 89 (124.84 s). That is where
  the track "goes off the rails".
- Decision: play bars 0–88 and fade over bars 85–88 (119.136 s to 123.407 s, raised cosine), which is a phrase
  boundary three bars before the breakdown. `tools/build_bed.py` writes `work/bed.wav`; there is no splice.
- The tempo is not constant, so cuts sit on the tracked bars (`work/beat-track.json`, `bar(n, beat)` in the
  edit), not on a fixed grid.
- ROM stingers (`tools/render_sfx.py`, `FmSfxRenderTool --paced`): S3K $B3, $B4, $9F, $6E, $B8, $4A; S2 $CF, $C1,
  $DF; S1 $C1, $CF. Each sits on its event frame from the take's `state.csv`. 29 stingers, between 2.3 dB over
  and 3.8 dB under the music at their own moment, all centred (`out/stinger-levels.json`). The grab on the pair
  catch is 1.4 dB under the music.
- Mastering (`tools/finish.py`): two-pass linear loudnorm, then the encoded AAC is measured with
  `ffmpeg ebur128=peak=true`.

## Verification (measured on the encoded files)

| | 16:9 | 9:16 |
|---|---|---|
| Duration | 124.00 s | 124.00 s |
| Video | 1920×1080, 60 fps, H.264 High, yuv420p | 1080×1920, 60 fps, H.264 High, yuv420p |
| Audio | AAC, 48 kHz, about 325 kb/s | the same sound track |
| Integrated loudness | −14.0 LUFS | −14.0 LUFS |
| True peak | −1.2 dBTP | −1.2 dBTP |
| Loudness range | 1.7 LU | 1.7 LU |
| Chapters | 9 | 9 |
| Full decode | exit 0 | exit 0 |

Black or still stretches are the opening black (0–0.55 s), the Sonic 2 emblem hold before the drop
(15.88–16.90 s) and the closing fade. `promo_kit check` reports no warnings in either mode (27 shots, mean 4.59 s).
Details are in `out/verification.json`.

## Not filmed as it ships

Everything below differs from a player's continuous session, or hides something the build does.

1. **Positioned starts.** Gameplay shots start mid-act at a declared position with declared rings, time, score and
   emeralds, not from a cold route. Each take's values are in `out/shot-index.csv`. The score is set through the
   public `GameStateManager.addScore` by the `positioned` and `powered` hosts; nothing is painted over the HUD.
   Sky Chase and the Chemical Plant lockstep start at the act's own start; the title screens are cold boots.
2. **ONE HIT. covers the revert.** In S3K the Hyper form ends when the HUD timer stops
   (`SuperStateController.runSuperFrameWork`, after the ROM's `Sonic_Super` check of `Update_HUD_timer`). The
   Launch Base 1 mini-boss stops the timer when it is destroyed, so on the kill frame (#648) MICA drops out of
   Hyper: she is drawn gold for frames 651–660 and in her normal jade from 663. The card slides in over her side
   of the frame from the hit, so no frame after the hit shows her looking like normal MICA. The lead chose to
   keep this.
3. **TALON's Solar form in the pair shot is asked for by controller 2.** In the pair take MICA is on pad 1 and
   TALON on pad 2; both press jump twice. A sidekick left to the game's own follow logic does not transform.
4. **White covers the pair's wind-up.** The cut into the pair shot holds white for 9 frames, over the frames in
   which both heroes are still in their normal forms, and clears onto the two silhouettes.
5. **Jade in the pair shot is Hyper's own palette.** Hyper MICA's Prism Gilt cycle has two 0.35 s jade phases;
   both are left in, at the lead's decision.
6. **The pair take's clock was declared so it follows the boss take.** The boss take ends at 3:10 on the HUD; the
   pair take was re-captured with a declared 3:12 (`d-lbz-pair-312`, otherwise identical to `d-lbz-pair`: the same
   rings, score, emeralds, starpost and inputs, and identical in 19 state columns over 820 frames).
7. **Hyper MICA transforms off camera in the boss take** (frames 51–96 of `d-lbz-boss`); the shot starts at #564.
8. **The Marble Garden take ends before she is hurt** (#183). The shot is two bars long for that reason.
9. **The Death Egg fragment at 11.3 s is repeated in the Hyper shot at 105.7 s.** Both are `d-dez1-hyper`: the
   fragment plays #101–#268 as a taste of the climax, and the later shot plays #54–#266 from the transformation.
10. **Debug component entries.** The Sonic 2 half-pipe is entered through a positioned ROM starpost (a real ring
    collision admits the special stage; steering is neutral). The Continue screen and the Sonic 2 ending are
    entered through the production providers by the `original` host, not by playing to them. (The Sonic 1 special
    stage is not a debug entry: MICA reaches the signpost with 55 rings and jumps into the real giant ring.)
11. **Stock art kept off screen by timing or cropping.** The S3K title's stock Tornado fly-by (title frames
    412–505 and 696–775, recurring) is avoided by timing in the roll-in and in the 9:16 titles stack, and lies
    outside the slice in the 16:9 titles triptych. The Data Select "No Save" tile carries
    stock art and is outside the window. SEGA marks are not shown: the film starts after the SEGA logo, and the
    Sonic 1 emblem plate and the Sonic 2 copyright row are outside the windows.
12. **Stock art on screen.** The Tornado keeps its stock livery, including the word "SONIC" on its side. It is
    readable in Sky Chase (30.8–36.4 s) and in the ending's side view (76.9–79.0 s). The 2026-11-11 cut cropped
    it out; this cut shows the plane whole because TALON piloting it is one of the features to show.
13. **HUD cropped in panes.** Triptych slices, bands and inset cells crop the HUD out whole; some of their takes
    have no declared score for that reason (`out/shot-index.csv`). No frame shows a partly cut HUD.
14. **The end card's backdrop** is the pair take playing on in soft focus; after its frame 620 it plays back and
    forth, under the fade.
15. **Sound.** Captures are silent. The music is the owner's track and the game sounds are ROM stingers placed on
    the event frames.

Omitted because the build cannot show them yet (engine, not the mod):

- **Sonic 1 results card.** It draws the act oval over its own lettering; a stock control shows the same fault.
  Sonic 1 is shown to the signpost only; the results card is Sonic 2's.
- **Competition.** The capture throws in the arena draw (`IllegalStateException: Native arena has no published
  VInt registers`).
- **Mushroom Hill and Carnival Night mini-boss acts** draw a white rectangle (missing art), so the boss shot is
  Launch Base 1.
- **The Angel Island fire-bombing machine** is a scripted set piece that never breaks apart, so it was dropped
  as the "one hit" boss.
- **Slot reels** were not attempted.

## The 9:16 cut

Same sound, same cut times, no letterboxing. Its grammar:

- **Tall frame** (`pv`): the full native height at 8.57×, 126 native pixels wide, never left of x 112, so the
  HUD (x 16–110) is out whole. The lives display (x 17–62) is out with it; where the lives matter (TALON in
  Spring Yard) they come back as an inset.
- **Stacked bands** (`bands_v`, `band`, `band_right`) for the triptychs, the lockstep split and the pairs.
- **Whole screens on their own ground** for the title screens, the tally and the ending, extended with the
  picture's own flat colour.
- **Cards** (`card_block`, `CardHeaderV`) for the lock-up, the headers, ONE HIT. and the end card, with the
  lock-up stacked as MICA / & TALON.

Three framing cuts happen inside takes, each on a beat or on the event:

| Time | Take | Cut |
|---|---|---|
| 5.05 s | Launch Base duo | Two bands (one hero each, the same size) until TALON takes off, then the tall frame for his flight over MICA. The vertical plays this take from #26 to #193; the 16:9 plays #62 to #229. |
| 6.2 s | The carry | A closer two-shot until the catch, then the tall frame for the climb. |
| 113.4 s | The pair | A closer two-shot (native x 111–217, rows 0–188) for the twin transformation, then the tall frame from the catch. |

ONE HIT. is an upright card beside the boss; the boss window is fixed at native x 140.

## Review history

- **Storyboard (checkpoint 1).** Approved: full length to the fade, tracked bar grid, no camera moves, Chemical
  Plant lockstep split, powered chapter on bars 60–84, the Sky Chase chain, the real giant-ring special stage,
  no widescreen. Fixes: no SEGA logo; plausible declared scores instead of "SCORE 0" on mid-act starts; TALON's
  first full shot in Sonic 1 with terrain (Spring Yard); a readable ONE HIT; a brighter end-card backdrop.
- **Draft (checkpoint 2).** Accepted the Launch Base boss, the removal of SEGA marks throughout and the Marble
  Garden, Solar-kill and Blue Sphere re-shoots. Blocking: the hero moment ended on what read as normal MICA (state
  evidence showed the game reverts her, item 2 above); the results tally on bars 80–84 was replaced by the pair
  shot; the grid was cut a bar earlier.
- **Climax check (checkpoint 3).** Approved. Decisions: keep the card over the revert; keep both jade phases;
  TALON transformed by controller 2 is fine and is stated here. Fixes: the pair take's declared time (item 6) and
  the grab level on the catch.
- **Final.** The 9:16 cut went to the lead for a framing review (`final/vertical-review.html`). Two vertical
  framings were corrected before that page was built: the pair's close two-shot (it took rows 58–224 and cut
  both heads while they were in the air) and the Launch Base duo (TALON flew out of his band and his tag hung
  over empty air).
- **Rejected along the way**, with the evidence in the checkpoint files: the Angel Island machine as the boss
  (scripted, never breaks apart; `edit/edit-aiz-boss-version.py`), a results tally as the last shot, a
  widescreen capture width, and a zoom into the roll-in.

## Rebuild

Java 25, Python with numpy and Pillow, ffmpeg, the fonts in `PROMO_FONT_DIRS`, the user's verified ROMs in the
checkout root.

```sh
mvn -q -o -Dmse=off clean compile && python3 examples/mica-and-talon/build.py      # in the checkout
python3 tools/capture.py --checkout <checkout> --shots shots/batch*.json            # sequential, one JVM
python3 tools/render_sfx.py <checkout>
python3 tools/beat_track.py <wav>; python3 tools/build_bed.py <wav> work/bed.wav
python3 <checkout>/tools/media/promo_kit.py render edit/edit.py                     # MT_VERTICAL=1 for 9:16
python3 tools/chapters.py
python3 tools/finish.py work/build-h out/master-16x9.mp4 work/chapters.ffmeta
python3 tools/finish.py work/build-v out/master-9x16.mp4 work/chapters.ffmeta
python3 tools/usage.py out/usage-16x9.json; MT_VERTICAL=1 python3 tools/usage.py out/usage-9x16.json
python3 tools/shot_index.py; python3 tools/verify.py
```
