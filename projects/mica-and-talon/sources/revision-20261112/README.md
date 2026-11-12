# MICA & TALON — promo, pacing revision (2026-11-12)

Public promo for the official OpenGGF example character mod `examples/mica-and-talon` (MICA, a jade pangolin, and
TALON, a falcon). This is the revision the owner asked for after reviewing the 124 s cut delivered earlier the
same day; it supersedes that cut. The delivered cut's README is in the local media archive
(`projects/mica-and-talon/sources/redo-20261112/README.md`).

- `out/master-16x9.mp4` — 1920×1080, 60 fps, H.264 High, yuv420p, AAC 320k, 10 chapters, 124.00 s
- `out/master-9x16.mp4` — 1080×1920, same sound and cut times, every picture recomposed for the tall frame
- `out/chapters.txt`, `out/shot-index.csv` (every take on screen: entry kind, declared setup, the three commits,
  frames used in each cut, command), `out/usage-*.json`, `out/verification.json`, `out/sfx-levels.json` (every
  on-screen hit's captured sound against the music), `out/takes-check.json`, `out/onscreen.txt`, `out/pacing-final.json`,
  `out/promo_kit-check.txt`, `out/contact-16x9-2s.jpg`, `out/contact-9x16-2s.jpg`
- `edit/edit.py` — brief (docstring), timing table, sound plan and both cuts (`MT_VERTICAL=1` selects 9:16);
  `edit/cards.py` — the introduction cards and the duo end card; `edit/edit-delivered-20261112.py` — the cut this replaces
- `tools/` — `final_shots.py` (the capture list), `capture.py`, `takes_check.py`, `mixcheck.py`, `onscreen.py`,
  `pacing.py`, `probes_b.py`, `final_run.sh` (the whole final run), `finish.py`, `usage.py`, `shot_index.py`,
  `verify.py`, `archive_revision.py`, and the checkpoint builders
- `hosts/` — the `PromoCapture` capture hosts; `hosts/common/PromoAudio.java` records their SFX-only audio
- `shots-b/` — capture lists: `final.json` (film), `promo10.json` (clips for the 1.0 release promo), probe batches
- `captures/` — the final takes; `captures-old-art-1e0faac123/` — the delivered cut's takes (see "Folders")
- `checkpoint4/` pacing storyboard, `checkpoint5/` probe results, `checkpoint6/` card previews

**Sound was checked by measurement only. Nobody listened to these files.**

## Commits

The build is a local merge, so every take's `provenance.json` names three commits:

| Field | Commit | What it is |
|---|---|---|
| `mod_commit` | `47e1826b80` | integration `feature/ai-original-character`: the mod and its final art |
| `develop_commit` | `4f885afbd6` | develop, for `GameplayCaptureTool --audio --no-music` (PR #282) |
| `build_commit` | `5313360296` | the local merge of the two on `feature/ai-mt-promo-redo`; not pushed |

`capture.py` refuses to run unless both are ancestors of the build and `examples/mica-and-talon` in the build is
byte-identical to `mod_commit` (`mod_sources_identical_to_mod_commit` in the provenance). Example jar sha256
`a58523d627b701d642b40a19775cf94c790e203f05c803a997776c3aa515cd14`. The merge had one conflict, in
`CHANGELOG.0.8.prerelease.md`; both entries were kept. Nothing was pushed to OpenGGF.

Final art in this build: pastel Hyper jade, TALON's fly and carry re-shade, MICA's inked carried frames, TALON's
walk and run despeckle, and every rotation-derived slope and homing-dive set on the pixel-art rotation. Checked on
screen against the previous builds frame for frame (the game state is identical; only the art changed).

## The owner's review and what changed

1. **"Use the SFX only (no music) option … Then we can just use the src audio."** Every take is captured with
   music volume 0 and its own sound effects. The film uses that audio, cut to the frames on screen. No stinger is
   placed anywhere.
2. **"Hyper Mica's jade is too dark."** and 3. **"carrying Talon sprites are still washed out."** Fixed by the
   art lane; every take here is shot on the final art.
4. **"Timing and general pacing needs improvement. Set scenes could do with improvement when gspeed is low and no
   badnik/boss interactions."** The cut was measured shot by shot (`tools/pacing.py`, `checkpoint4/`) and rebuilt:
   27 shots became 48 (the two cards are overlays on their shots), mean shot 4.6 s became 2.6 s, same 124 s.
   Slow, untouched gameplay went from 11.6 s to 4.0 s (`out/pacing-final.json`, the same measure as the
   storyboard); 0.8 s of that is the Marble Garden lead-in hidden under MICA's card. Every hit is placed on a
   beat by choosing the capture window and the cut, never by moving a sound.

Later in the same review round the owner's 1.0 promo drawings came in: each hero now has a one-bar introduction
card, and the end card carries the duo drawing.

## Music

"RUN INTO THE SUNSHINE (Chiptune Remix)", owner-supplied, sha256
`569a921b69983c1a6f2916c6be963bb134a39aaa742b0624044fbe4baf8481ff`. In no repository; the archive names it by
title and hash only. It plays from its first sample, uncut: bars 0–88 with one raised-cosine fade over bars 85–88
(119.136 s to 123.407 s), a phrase boundary three bars before the track's pulse breaks down. The tempo drifts
(172.2 BPM to 170.2), so cuts sit on tracked bars (`work/beat-track.json`).

## Game sound

- **Source.** `GameplayCaptureTool --audio --no-music` for the tool takes; the hosts call
  `GameplayCaptureSession.enableAudio()` and `silenceMusic()` and drain one presentation packet per frame
  (`hosts/common/PromoAudio.java`). Each host was checked against a music-on control run and against the stock
  tool (`tools/rms_check.py`, `checkpoint5/`): digital silence between effects, audio length equal to the frame
  count, the jump sound on the same sample as the tool's.
- **In the film.** `sound()` in the edit lays each shot's stem under the bed for exactly the frames on screen,
  with 5 ms fades. A split screen mixes its panes a little lower. The lockstep split plays the mod's side only
  (the stock side makes the same sounds). Under an introduction card the take is silent until the field parts.
- **Balance.** One gain for all stems (1.5), with four takes trimmed because the game's own sounds are not
  equally loud: the Death Egg booster (two takes, ×0.6), a spindash release (×0.7) and the Hyper strike (×0.8).
  Measured by `tools/mixcheck.py`: see "Verification".
- **Silent stems.** The S3K title, Data Select, the Continue screen and the Sonic 2 ending make no sound effect,
  so those shots have music only.

## Introductions

`edit/cards.py`. MICA's card lands on bar 14 and TALON's on bar 28, the first bar of each chapter: a field in the
character's colours, the hero drawing nearly the height of the frame from one side and the lettered name from the
other; the field parts on beat 3 and leaves first; drawing and name linger to the bar line; the drawing leaves
and the name shrinks to a corner plate. TALON's plate gives way to the lives inset. The end card has the duo
drawing and both lettered names. The title drop keeps the white lock-up.

The drawings are Sol's, from the owner's release-promo project
(`~/.t3/projects/openggf-release-promo/out/art/sol/`: `mica-hero`, `talon-hero`, `name-mica`, `name-talon`,
`duo-sunrise`). `tools/sol_art.py` cuts them out of their magenta ground into this folder's `art/` with that
project's method. They are not in the OpenGGF repository; the media archive lists the cut-outs by hash.

## Verification (measured on the encoded files)

| | 16:9 | 9:16 |
|---|---|---|
| Duration | 124.00 s | 124.00 s |
| Video | 1920×1080, 60 fps, H.264 High, yuv420p | 1080×1920, 60 fps, H.264 High, yuv420p |
| Integrated loudness | −14.0 LUFS | −14.0 LUFS |
| True peak | −1.5 dBTP | −1.5 dBTP |
| Loudness range | 2.4 LU | 2.4 LU |
| Chapters | 10 | 10 |
| Full decode | exit 0 | exit 0 |

- Loudness: two-pass linear loudnorm, then `ffmpeg ebur128=peak=true` on the encoded AAC (`tools/finish.py`).
- Hits against the music, before mastering (`out/sfx-levels.json`): 24 kills and boss hits sit between 1.0 dB over and 6.2 dB under the bed, median 1.9 dB under; 17 of them land within one frame of a beat (the rest are second hits of a chain); 46 events measured in all, springs, bumpers and transformations included.
- Takes: 61 takes, 0 with problems (`tools/takes_check.py`: complete, three commits named, expected events on the expected frames,
  both lockstep pairs identical in 13 state columns).
- No shot outlives its source in either cut (`out/usage-*.json`). `promo_kit check`: no warnings.
- Black or still stretches: the opening black (0–0.55 s), the Sonic 2 emblem hold before the drop, the closing fade.

## Not filmed as it ships

Everything below differs from a player's continuous session, or hides something the build does.

1. **Positioned starts.** Gameplay takes start mid-act at a declared position with declared rings, time, score and
   emeralds (`out/shot-index.csv`); the score is set through the public `GameStateManager.addScore`. Sky Chase and
   the Chemical Plant lockstep start at the act's own start. The Emerald Hill lockstep pair is positioned mid-act
   with the same declared values on both sides. Titles are cold boots.
2. **Scripted inputs, tuned to the music.** Every take is driven by an input script. Four were tuned by a few
   frames so their hits land on beats (Marble Garden, Sky Chase, the Hyper reveal and kill, the Solar reveal and
   kill), and six were re-staged (the Launch Base duo, the carry swoop, TALON's Whisp, the Solar reveal, the boss
   run-in, the pair). Nothing is re-timed in the edit.
3. **TALON is flown by controller 2** in the carry swoop and the pair shot, and his Solar form in the pair shot is
   asked for by controller 2. A sidekick left to the game's own follow logic does neither.
4. **ONE HIT. covers the revert.** In S3K the Hyper form ends when the HUD timer stops, and the Launch Base 1
   mini-boss stops it when it is destroyed. On the hit frame (#632 of `lbz-boss`) MICA drops out of Hyper and is
   drawn in her normal colours about 15 frames later. She travels right after the hit, under the card, so no
   frame shows her after the form has ended.
5. **White covers the pair's wind-up.** The cut into the pair shot holds white for the 9 frames in which both are
   still in normal colours.
6. **Hyper MICA transforms off camera in the boss take** (#51–76); the shot starts at #548.
7. **The Marble Garden take starts under MICA's card and ends before she is hurt.** Its lead-in could not be
   lengthened (the Mantises are on a timer), so the film holds the take's first frame for the 40 frames before it,
   all of them under the card's opaque field. The take ends at #181; she is hit at #183.
8. **The Hill Top shot ends before TALON outruns the game's camera.** His divebomb reaches 24 px/frame and the
   camera loses him for 50 frames; the shot is one bar and stops while he is on screen.
9. **Debug component entries.** The Sonic 2 half-pipe is entered through a positioned ROM starpost; the Continue
   screen and the Sonic 2 ending through the production providers (`original` host). The Sonic 1 special stage is
   not a debug entry: MICA reaches the giant ring with 55 rings.
10. **Stock art kept off screen by timing or cropping.** The S3K title's stock Tornado fly-by; the Data Select
    "No Save" tile; SEGA marks (the film starts after the SEGA logo; the Sonic 1 emblem plate and the Sonic 2
    copyright row are outside the windows).
11. **Stock art on screen.** The Tornado keeps its stock livery, with "SONIC" on its side, in Sky Chase
    (67.1–69.9 s) and the ending's side view (69.9–71.3 s). Kept at the lead's ruling.
12. **HUD cropped in panes.** Split-screen slices, bands and inset cells crop the HUD out whole. The 9:16 tall
    frame drops the HUD and the lives display; the lives return as an inset in the Spring Yard shot.
13. **The end card's backdrop** is the pair take playing on in soft focus; from its frame 570 it plays back and
    forth, before the flight tires at #593.
14. **Cards are graphics.** The two introduction cards, the title lock-up, ONE HIT., the chapter headers, pills
    and the end card are edit-layer graphics over the footage.
15. **Sound.** The music is the owner's track. The game sound is each take's own SFX-only capture at the gains
    above; the game's music is silent in every take. Split screens mix several takes' sound at once.

Not shown because the build cannot show it, or because the footage failed a check:

- **Sonic 1 results card** (engine draw fault), **Competition** (capture throws in the arena draw), **Mushroom
  Hill and Carnival Night mini-bosses** (missing art), **the Angel Island fire-bombing machine** (scripted, never
  breaks apart), **slot reels** (not attempted).
- **Green Hill 1 run-up to the signpost** in 16:9: the level's bottom boundary holds her at the frame's lower
  edge with her feet cut. Replaced by the Green Hill 2 monitor shot.
- **A second TALON Whisp kill**: 23 probes found no second Whisp in reach.
- **A Scrap Brain duo run**: the usable stretch follows a hit, with 5 rings on the HUD. Not used.
- **Solar TALON's second Angel Island dive**: its last 0.7 s is TALON against a wall. Replaced by Flying Battery.

## The 9:16 cut

Same sound and cut times, no letterboxing: the tall frame (every native row, 126 px wide, never left of x 112, so
the HUD is out whole), stacked bands for comparisons, whole screens on their own ground, tall cards. Two framing
cuts happen inside takes: the Launch Base duo goes from two bands to the tall frame as the spring fires, and the
pair goes from a closer two-shot to the tall frame at the catch. The boss window follows her run-in by up to
28 px and settles before the hit; that is the only camera move in either cut.

## Clips for the 1.0 release promo

Shot with the film, on the same build, with SFX-only audio (`audio.wav`) and the 2026-11-11 recipes
(`shots-b/promo10.json`, each take's `provenance.json`). All are in `captures/`, captured 2026-11-12 between
12:10:40Z and 12:17:24Z:

| id | Frames | Size | Recipe |
|---|---|---|---|
| `title-s2` | 1300 | 320×224 | cold title-first boot, Sonic 2 (also in the film) |
| `s1-ghz2-buzz` | 351 | 320×224 | Green Hill 2, solo MICA, `declared` host |
| `mgz2-chain` | 669 | 320×224 | Marble Garden 2, solo MICA, `declared` host, the 2026-11-10 input log |
| `halfpipe-run` | 1386 | 320×224 | Sonic 2 special stage through the ROM starpost (also in the film) |
| `carry-fly` | 370 | 320×224 | Angel Island 1, MICA + TALON, tool |
| `gilded-clear` | 1416 | 320×224 | Emerald Hill 1, Gilded MICA to the signpost, tool |
| `solar-fly` | 460 | 320×224 | Angel Island 1, Solar TALON, tool |
| `w-title-s2` | 1000 | 400×224 | as `title-s2`, 400 wide |
| `w-s1-ghz2-buzz`, `w-mgz2-chain`, `w-carry-fly`, `w-gilded-clear`, `w-solar-fly` | as above | 400×224 | 400-wide versions |

`halfpipe-run` has no wide version. The 2026-11-11 recipes for `s1-ghz2-buzz` and `mgz2-chain` declare no score,
so their HUD reads SCORE 0, as it did then.

## Folders

- `captures/` — the 61 final takes (50 for the film, 11 more for the 1.0 promo).
- `captures-old-art-1e0faac123/` — the delivered cut's takes and its scouting takes, renamed from `captures/` on
  2026-11-12 before the final run. Nothing was deleted. The media archive of the delivered cut lists them by hash
  under `captures/...`; those paths resolve under this folder (same files, same hashes).
- `probes-b/` — the stage B probes behind `checkpoint5/`. `rehearsal-b/` (the rehearsal takes on `94b5b21864`
  used to build the edit and the mix) was removed after the final run.

## Review history

- Storyboard, draft and climax reviews of the delivered cut: in its README in the media archive.
- **Owner review of the delivered cut**: the four points above.
- **Checkpoint 4, pacing storyboard**: approved (124 s kept, two-bar base with one-bar builds, the cold-open
  swap to the Mushroom Hill loops, Sky Chase beside the ending). The 2.5 s mean is not a target; reveals must stay
  readable.
- **Checkpoint 5, probes**: six re-stages and three tunes approved; the pair moved to the lower bridge.
- **Checkpoint 6, cards**: approved; white lock-up kept on the title; "Requires your own ROMs."; `duo-sunrise`.
- **Found on the rehearsal takes and reported**: the Hill Top shot shortened, the Green Hill 1 run dropped, the
  Marble Garden lead-in handled under the card; later the Flying Battery swap.
- **Rejected along the way**: the lettered names in the title band (they read poorly on the card blue); a card on
  the cold open's duo shot; lengthening the Marble Garden lead-in; the Scrap Brain duo run.

## Rebuild

Java 25, Python with numpy and Pillow (scipy for `sol_art.py`), ffmpeg, the fonts in `PROMO_FONT_DIRS`, the
user's verified ROMs in the checkout root.

```sh
git merge <integration sha>                     # into the local build branch, which already has develop 4f885afbd6
mvn -q -o -Dmse=off clean compile && mvn -q -o -Dmse=off dependency:build-classpath -Dmdep.outputFile=target/mica-classpath.txt
python3 examples/mica-and-talon/build.py
javac -cp "target/classes:$(cat target/mica-classpath.txt)" -d hosts/common hosts/common/PromoAudio.java   # then each host with hosts/common on the classpath
tools/final_run.sh <integration sha> 4f885afbd6       # captures, checks, both masters, reports
python3 tools/archive_revision.py --media <OpenGGF-Media worktree>
```
