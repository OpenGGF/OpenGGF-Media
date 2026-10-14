# Chaos Mode promo, revision 2: editorial plan

Design pass, 2026-10-14. Read-only research; nothing built or captured. The machine-readable
EDL is `edl.json` (beats, seconds, layouts, effect IDs, sources, in-points, conditions,
fallbacks). This file gives the reasoning, layouts, audio, captions and capture list.

The first reel (`../out/sonic3k-chaos-mode-demo.mp4`, `../edit.json`, `../captures/`) stays
untouched. Read reused masters from `../captures/<name>/source.mkv`. Write new captures to
`revision-2/captures/<name>/` and the product to `revision-2/out/`.

## Shape

The cut runs 78.96 s: 74.66 s on the beat bed, then a 4.3 s stinger. Effects are no longer
introduced one at a time. Cuts land every 2–4 beats (0.70–1.40 s). Splits land on section beats,
and four 8-beat (2.8 s) payoffs let the eye rest. Twenty-eight of the 36 A-tier effects appear
in the first 50 s.

| Act | Beats | Seconds | Idea |
|---|---|---|---|
| 0 Cold open | 0–20 | 0–7.3 | Quiet AIZ with the diegetic CHAOS countdown; head pops on b8; three ROM-glyph slams |
| 1 Player/view | 20–56 | 7.3–20.0 | Body and camera effects; first PAIR; DVD HUD shrinks into a HUD quad |
| 2 Economy | 56–88 | 20.0–31.2 | Power-ups, a bumper/wind/ghost triple, rain payoff, then a hard cut to Leak (the joke) |
| 3 World | 88–132 | 31.2–46.6 | Blueprint/scenery slice, badnik quad, set pieces, menu breather |
| 4 Sidegames | 132–156 | 46.6–55.0 | Sidegame quad, Imaginary Chat, fictional critics |
| 5 Crescendo | 156–196 | 55.0–69.0 | 2-beat flurry, slices, quad, hero Too-Many-Sonics run, 4-strip slice, flash |
| End | 196–212 | 69.0–74.7 | End card; bed fades out over b204–212 |
| Stinger | — | 74.7–79.0 | Silence, then the ghost party kills Sonic (or a Leak fallback) |

Beat grid: Hydrocity Zone Act 2, 171.107 BPM, beat 0.350664 s, first beat 0.316 s
(`t(b) = 0.316 + b × 0.350664`). The grid and the 16/36/56/88/132/149/161/197 phrase boundaries
come from the Slay promo's `tools/beats.py`/`phrases.py` results. Re-run `phrases.py` on the bed
before cutting, and snap act boundaries to bars that it confirms. Moving a boundary by 4 beats
is fine. The EDL is beat-relative, so regenerating seconds is mechanical.

## Effects shown (36 A-tier, up to 46 with B slots)

- **Reuse (17, existing masters):** bobble-head, pulse-head, invisible-player, negative-world,
  mirror-view, moon-gravity, gravity-hiccup, dvd-hud, bumper-ahead\*, windy-day,
  soz-ghost-party\*, ring-magnet, wrong-zone-scenery, projectile-overdrive, flash-flood,
  ring-pong, monitor-stack. (\*Depends on the donor-colour verdict below.)
- **Re-capture after the mod changes (3):** afterimages (much stronger crowded bright echoes),
  ring-rain (full viewport, slight diagonal), ring-leak (real lost rings left behind).
- **New, A-tier (16):** rainbow-player, upside-down-view, fast-forward, slow-motion, hud-orbit,
  hud-shuffle, shield-surprise, ten-second-superstar, blueprint-zone, squashy-view,
  giant-badniks, spinning-badniks, monitor-breakout, vine-time, ring-snake, imaginary-chat.
- **B slots (swap in only if the capture is reliable; each has a fallback in the EDL):**
  hud-scale or shy-hud, ring-orbit, tiny-badniks or jelly-objects, zoom-pulse, quake-camera,
  badnik-defence or shield-beat, sonic-says, landmark-hunt, rolling-rampage, rescue-buddy.
  Further spares: blink-step (a frame-exact teleport makes a good jump-cut gag), bunny-hop,
  spring-legs, block-staircase, falling-debris, bumper-behind.
- **Excluded because nothing visible happens on screen:** reverse-controls, delayed-controls,
  grounded, jukebox-surprise, clang-landings (the source audio is muted anyway), badnik-truce,
  badnik-blind-spot, and the starpost relocations (they need activated posts).

The in-game Chaos panel names every effect, for example `CHAOS 3S / TOO MANY SONICS 18S`. That
panel is the effect label, so most shots carry no editorial caption. It must stay legible: use
FULL or PAIR for the first appearance of any effect, and keep QUAD panels at 2.36× or larger.

## Layouts (1920×1080, navy field and darkened `aiz-background.png` as before)

- **FULL:** the whole 400×224 frame, nearest-neighbour at 4× to 1600×896, centred. Full native
  HUD. This is the default.
- **PAIR:** two whole frames side by side, each nearest-neighbour at 4× then area-filtered to
  944×528 (2.36×, the Slay method), with 16 px gutters and a 2 px gold rule. The right panel
  lands one or two beats after the left. Both full HUDs stay visible.
- **SLICE-2:** two 4× frames divided by a 12° diagonal gold edge. Each side is cropped around
  Sonic using `x − cam_x` from `state.csv`. The edge either sweeps across the shot (b30, b88) or
  sits fixed for 2-beat hits (b164–172). This is the "slice the screen" look; some HUD is lost,
  so use it only for effects already seen or self-evident.
- **TRIPLE:** three slanted slices, each about 640 px wide (160 source px around Sonic), as in
  Slay's S1/S2/S3K opener. Slices drop in on successive beats.
- **QUAD:** a 2×2 grid of whole frames at 944×528. Panels drop in on b, b+1, b+2, b+3. The
  FULL→QUAD shots (b48 DVD, b96 Overdrive) keep the running FULL clip continuous as it shrinks
  into the top-left over 6 frames. If a B panel is missing, leave that cell navy with the
  caption there rather than showing a duplicate.
- **SLICE-4:** four diagonal strips, one added every 2 beats, ending in a 2-frame white flash
  on b196.

Alignment rule: the effect's arrival frame goes on a beat, and every instant contact goes on a
beat (shield appearance b56, bumper contact b61, head pop b8). The arrival frame is the first
frame where the Chaos panel names the effect. In existing captures it is near source 9.75–10.0 s
(active clock 600). Read it from the frames; do not assume it.

## Captions and cards (deliberately few)

Use the plate font for small lower-third captions. ROM title glyphs are for card words only,
and only where every letter exists in the ROM set: ONE HEDGEHOG, NO RULES, CHAOS MODE and
FICTIONAL CRITICS check out. "3", "&", "K" (in context) and all small text use the plate font.
The ROM set has no J, Q, W, X, Z or digits.

1. b0–7, over quiet AIZ: `ANGEL ISLAND, 10:00 AM. NOTHING TO REPORT.` The head pops on b8.
2. b53–56, HUD quad: `THE HUD HAS UNIONISED.`
3. b64–72, ring rain: `THE ECONOMY IS DOING GREAT.`
4. b77–84, ring leak (hard cut from rain): `...PLEASE MIND YOUR BELONGINGS.`
5. b101–108, badnik quad: `THE BADNIKS ARE GOING THROUGH SOMETHING.`
6. b124–132, menu: `CHOOSE YOUR PROBLEMS.` then `THEN PLAY THE ACTUAL GAME.`
7. b132–140, sidegame quad: `WE INTERRUPT THIS PLATFORMER.`
8. Stinger: `SANDOPOLIS SENDS ITS REGARDS.`

**Fictional critics card (b148–156, 2.8 s).** It is headed FICTIONAL CRITICS. Each review slams
in on b148, b150 or b152, rated in ROM ring glyphs, and all three hold to b156. It earns its time
by doubling as the mid-reel breath before the crescendo.

- TAILS: "I COUNTED ELEVEN OF HIM. NOT ONE OFFERED TO CARRY ME." (5 rings)
- KNUCKLES: "THE RINGS FELL SIDEWAYS. NOBODY TOLD ME." (3 rings)
- DR. ROBOTNIK: "FINALLY, MY BADNIKS ARE THE RIGHT SIZE." (5 rings)

The last line pays off the giant-badniks panel. If the new Too Many Sonics capture shows fewer
than about eight echoes, change "ELEVEN" to the number actually visible.

**End card (b196–212):** `CHAOS MODE` in ROM glyphs, then the plate-font lines
`105 EFFECTS. CHOOSE YOUR POOL.` and `AN OPENGGF MOD. YOUR OWN SONIC 3 & KNUCKLES ROM.` Do not
claim availability or a release date; the Mod API is unpublished.

## Audio: one bed, honest effects

- **Bed:** `/home/farrell/Videos/OGGF/slay-the-robotnik-promo/audio/m-hcz2.wav`. It is HCZ2
  rendered from the ROM by OpenGGF's SMPS driver (`tools/render_audio.py`), 100 s long, already
  beat-mapped. Copy it into `revision-2/assets/` with its SHA-256 and that provenance. Play it
  from 0 to b212 continuously, with no cuts in the music, and fade over b204–212. Mix about
  −16 LUFS-equivalent with the Slay soft knee.
- **Why HCZ2 rather than AIZ2:** it is ready, verified at 171.1 BPM, and has the energy for
  2-beat cutting. AIZ2 (render with `render_audio.py music <AIZ2 id> 100 m-aiz2.wav`, then run
  `beats.py`) is a reasonable swap if the user minds sharing a track with the Slay promo. Every
  beat number in the EDL then needs re-snapping to its grid.
- **Source audio is muted everywhere.** The capture PCM is native AIZ1 music plus SFX in one
  mix. Pulling the SFX out of it would be fake source separation, and the Chaos mod has no
  music-off setting, so Slay's "no-music recording copy" trick is not available without a mod
  change. Do not add one for the promo.
- **Effect SFX are editorial, and labelled so.** Use ROM SFX rendered offline through the same
  SMPS driver (`render_audio.py sfx <ids>`, plus the existing `../assets/audio/*.wav`). Place
  each on the frame where the visible event happens in that source's `state.csv`, and only for
  FULL shots or the panel that has just dropped in:
  - rings +Δ: `ring.wav`, at most one per 6 frames, gain −9 dB;
  - leak −Δ: the SFX ID the mod actually issues for a leaked ring (read it from the mod code;
    `ringloss.wav` only if it is that ID);
  - bumper contact: sfx_Bumper;
  - shield: the matching shield SFX;
  - death frame: `death.wav`;
  - cards: `boom`, `skid`, `dash`, `ring` as before.

  Resolve the IDs from the skdisasm sound constants; do not guess them. Write this sentence into
  the README: "Gameplay sound effects are ROM SFX placed editorially at the frames where the
  engine shows each event; source gameplay audio is not used."
- **Stinger:** the bed has ended. Play silence, then only the death SFX at the death frame.

## Capture list (root runs; same rules as `../capture.py`)

Every capture uses: native AIZ1 direct level, solo Sonic, width 400, singleton selected pool,
interval 5, duration 1× (`durationQuarters=4`), seed 22, 1080 frames, `--every 1
--interactive-pacing --audio`, surfaceless EGL, no display variables, no position, ring or world
writes. Overdrive-family shots are the only exception (see below). Use a fresh jar built from
the updated mod, record its SHA-256, and keep the old jar for reused masters.

`MOVING` = `600 -; repeat 6 { 1 R+A; 59 R }; 120 -` (x 5024 → about 6350 by tick 900, 6 rings).

| Pri | Name | Effect ID | Script / setup | Accept when |
|---|---|---|---|---|
| P0 | afterimages | afterimages | MOVING | Panel names it; at least 6 bright echoes trail clearly in at least 2 s of the run; a jump arc is visible |
| P0 | rain | ring-rain | `780 -; 1 A; 119 -; 180 R` (as before) | Rings cover the whole viewport, falling with a slight diagonal; real pickups raise the ring count |
| P0 | leak | ring-leak | `repeat 9 { 1 R+A; 59 R }; 60 -; 180 -; 300 R` (collect rings before 600, stand while leaking, walk away) | Counter falls one ring at a time; dropped rings stay in the world behind Sonic; at least one ring kept. If rings < 2 at clock 600, lengthen the pre-roll |
| P0 | (investigation) | bumper/ghost donor colours | see below | Verdict recorded before any bumper or ghost shot is locked |
| P1 | rainbow, upsidedown, fastforward, slowmo, hudorbit, hudshuffle, superstar, blueprint, squashy | rainbow-player, upside-down-view, fast-forward, slow-motion, hud-orbit, hud-shuffle, ten-second-superstar, blueprint-zone, squashy-view | MOVING | Panel names it; the effect is obvious at 2.36× scale |
| P1 | shield | shield-surprise | MOVING | Shield visibly appears near clock 600 (whichever type seed 22 samples) |
| P1 | chat | imaginary-chat | MOVING | Messages are readable and labelled simulated by the mod |
| P1 | giant, spinning | giant-badniks, spinning-badniks | Positioned centre 8912,877 near the native Bloominator (9072,892), `1080 -`. This is the same disclosed approach bypass as the overdrive master | The Bloominator is visibly enlarged or spinning while firing |
| P1 | breakout | monitor-breakout | `600 -; 90 -;` then spindash: hold D, tap A three times over 30 ticks, release, `200 R` | The cage appears on flat ground at the start; Sonic breaks out. If it does not qualify there, drop it to B |
| P1 | vine | vine-time | MOVING; if the grab is missed, try `600 -; 60 -; 1 A; 59 -; 360 R` | Sonic visibly swings on the placed vine and releases |
| P1 | snake | ring-snake | `600 -; repeat 6 { 20 U; 20 R; 20 D; 20 R }` | Snake moves and eats at least one ring on screen |
| P2 | B list | as EDL | MOVING; tiny/jelly at the Bloominator; defence/shield-beat with a sidegame pad pattern | Same tests; a failure costs nothing because every slot has a fallback |

Optional variety: one or two B-tier shots (or a second afterimages take) from **native HCZ1**
(`--zone hcz --act 1`, native start, same settings) would break up the all-green palette in
quads. Use them only if the effect qualifies there and the panel shows it. Never place the
player there.

Check every capture with the existing `verify.py` and `lossless-source-checks.json` pattern.
Also check that the panel text names the effect at the chosen in-point; a singleton pool that
fails qualification shows nothing. Check there is no unintended death; `state.csv dead` must stay
0 except in the stinger source. Keep the scripts, `input.txt`, `state.csv`, settings and
provenance as before.

## Bumper/ghost donor colours: what the code says

- `NativeMutatorRuntime` spawns `CnzBumperObjectInstance` (art key `CNZ_BUMPER`) and
  `NativeGhostEncounterObjectInstance` (`SOZ_GHOSTS`). It loads art through
  `Sonic3kObjectArtProvider.ensureEncounterArtLoaded`, which loads patterns only and makes no
  palette change.
- `Sonic3kPlcArtRegistry` registers the bumper on **palette line 2** (`ArtTile_CNZMisc+$13`,
  palette 2, `Obj_Bumper`) and the ghosts on **line 1**.
- In AIZ1 those lines hold AIZ colours. Both objects therefore render with host palette lines,
  not CNZ or SOZ colours. Current frames show a blue ring with a gold star (bumper) and pale cyan
  ghosts. That is plausible but unverified.
- **To decide:** take one native reference frame each: a CNZ1 bumper (engine capture
  `--zone cnz --act 1` near a bumper, or `bizhawk-native-reference-capture`) and SOZ2 ghosts.
  Compare them with the AIZ spawn.
- **If they differ:** this is a mod or runtime fix (donor palette load or remap through the
  existing host palette path), owned by whoever is changing the mod. Re-capture afterwards.
  **Never recolour in post.** Until there is a verdict, the bumper and ghost slots (b60 triple,
  b120, the crescendo panels, the stinger) are conditional, and their EDL fallbacks keep the
  timing intact.

## Constraints carried forward

- Every frame of gameplay is an unmodified production capture at real presentation speed. There
  are no editorial spawns, overlays that imitate effects, or speed ramps. Freeze frames appear
  only at the stinger's end. Do not change speed in post; fast-forward and slow-motion are the
  engine's own.
- Never repeat an identical source interval. Recaps use later in-points.
- Only AIZ1 plus the optional HCZ1 appears. The README must say this does not certify every
  effect, team or act, and repeat the first reel's scope notes: Pong shows a return, not a win;
  Stack shows placements; Flood is local.
- Chapters, `edit-timeline.json` and verification are the same deliverables as the first reel,
  under `revision-2/out/`.
