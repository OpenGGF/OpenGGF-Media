# Chaos Mode card gallery — revision 3

Opus 5.5 planning input, 2026-10-14. Root will qualify individual sources and adapt setup details to the actual supported native routes. This plan is editorial intent, not completed capture evidence. Prior revisions remain intact.

**Recommendation:** make revision 3 a single still page. One large card on the left plays one effect at a time, and the cards already shown sit frozen in a wall around it. No two clips play at once, the camera never pans, and there are no fast cuts. All 46 effects are labelled, gameplay comes from 12 different zones, the music bed runs throughout, and the ghost finale plays its real recorded sound.

**The cause of the missing ghost sound:** the engine already plays the ghosts' appearance sound. `SozHyudoroBodyObjectInstance` plays sound effect `$92` when a ghost spawns, which matches the ROM's `Hyudoro_init` at `sonic3k.asm:195563`. Revision 2 muted all recorded gameplay audio and then put silence under the ending, so you never heard it.

## Page layout (1920×1080, fixed for the whole video)

- **Background:** plain navy with a faint vignette. No moving background, since the footage now comes from many zones.
- **Wall grid:** each cell is 148×104 px, spaced 156 px apart horizontally and 112 px vertically, starting at (28, 40). There are 12 columns × 9 rows, and the bottom-right cell ends at (1892, 1040).
  - Inside each cell, the top 148×83 is the effect's final frame, shrunk (a 0.37× downscale with area filtering). Below it is a 21 px label band with the effect name at 15 px, in cream `#E8E0C8`.
  - Cells not filled yet show only a 1 px `#1E2A4A` outline.
- **Stage:** the block of columns 0–7 and rows 0–6 (x 28–1268, y 40–816).
  - **Active card:** at 48, 40, the game's 400×224 picture scaled exactly 3× with sharp pixels, giving 1200×672. It has a 2 px gold border, so the in-game Chaos panel is easy to read.
  - **Label plate:** at 48, 724, size 1200×92.
    - The effect name sits on the left, in the plate font at 44 px. Use the mod's own display name exactly as the in-game panel shows it.
    - The right side shows the counter `08 / 46` and the zone name (`ICE CAP ZONE · ACT 1`), both 22 px.
    - An optional caption goes on a second line at 24 px in `#B9C3D9`.
- **Order the wall fills in:**
  - Cards 1–36 fill the right-hand block (columns 8–11), left to right then top to bottom: card *k* goes to column 8+(k mod 4), row ⌊k/4⌋.
  - Cards 37–44 fill row 7, columns 0–7.
  - Cards 45–46 fill row 8, columns 0–1.
  - Row 8, columns 2–7 (928×104 px) hold a dim panel reading `+59 MORE IN THE POOL`, visible from the start.
- **Newest card:** keeps a 2 px gold border until the next card lands.

## Timing (60 fps)

**What happens at each switch, starting at frame T:**
1. Frames T to T+18: the outgoing clip's last frame freezes and slides into its wall cell, easing in and out with no bounce.
2. Frames T+6 to T+18: the label plate crossfades to the next effect.
3. Frames T+18 to T+30: the new clip fades in from navy, already playing at normal speed.

After that nothing moves except the active clip. Each clip is one continuous stretch of footage, `slot − 18` frames long. If the moment the effect switches on matters (head pops, shield, bumper), start the clip half a second before that moment. Otherwise use the start point already approved in revision 2. Pick the end point so the last frame clearly shows the effect, because that frame becomes the wall thumbnail.

**Slot lengths:**

| Length | How many | Used for |
|---|---|---|
| A: 240 frames (4.0 s) | 18 | Effects that read instantly |
| B: 300 frames (5.0 s) | 19 | Effects where something has to happen |
| C: 360 frames (6.0 s) | 8 | Ring Leak, Monitor Breakout and the sidegames |
| Ghost finale: 360 frames | 1 | Ghost party ending |

**Running order** (letter = slot length; zone in brackets = new capture; everything else reuses an existing AIZ1 recording):

1. **Body:** rainbow-player A [CNZ1], afterimages B [LBZ1], bobble-head A [SOZ1], pulse-head A, invisible-player A
2. **View:** upside-down-view A [HCZ1], mirror-view A [MGZ1], negative-world A [ICZ1], squashy-view A [FBZ1], zoom-pulse B, quake-camera A, blueprint-zone A [DEZ1], wrong-zone-scenery B
3. **Motion:** moon-gravity B [MHZ1], gravity-hiccup B, bunny-hop A, fast-forward B [LRZ1], slow-motion B, rolling-rampage B, windy-day B
4. **HUD:** dvd-hud B [SSZ], hud-orbit A, hud-shuffle B, hud-scale A
5. **Rings and power-ups:** ring-rain B, ring-magnet B, ring-orbit A, ring-leak C, flash-flood B, shield-surprise A, ten-second-superstar B
6. **Badniks and visitors:** giant-badniks A, spinning-badniks A, tiny-badniks A, projectile-overdrive B, eggman-blaster B, monitor-breakout C, bumper-ahead B, rescue-buddy B
7. **Sidegames:** ring-pong C [CNZ2], monitor-stack C, ring-snake C, badnik-defence C, sonic-says C, imaginary-chat C
8. **Finale:** soz-ghost-party, using the `ghost-close` recording. The clip runs from 9.75 s, through the death at frame 840, to frame 945.

**Whole video:**

| Part | Length |
|---|---|
| Intro | 300 frames |
| Effect slots | 13,260 frames |
| End card | 420 frames |
| **Total** | **13,980 frames = 3:53** |

- **Intro:** the stage shows `CHAOS MODE` in the ROM title letters, with `46 EFFECTS. ONE AT A TIME, FOR ONCE.` underneath, over an empty wall.
- **End card:** after the ghost card slides into its cell, the stage shows `CHAOS MODE`, `105 EFFECTS. CHOOSE YOUR POOL.` and `AN OPENGGF MOD. YOUR OWN SONIC 3 & KNUCKLES ROM.` beside the full wall.

**About the new captures:** the order above opens with eight zones in the first 12 cards. The badnik group stays in AIZ1 because it relies on the declared Bloominator setup. Every new capture starts at the act's normal starting point, with solo Sonic, the effect alone in its pool, seed 22, and the usual no-placement rules. If a zone fails review, swap in another zone or fall back to the existing AIZ1 recording; keep the slot in the same place.

## Captions

Keep it to these, all deadpan, at most one line each:

| Card | Caption |
|---|---|
| invisible-player | `SONIC IS IN THIS SHOT.` |
| negative-world (Ice Cap) | `STILL COLD.` |
| hud-shuffle | `THE HUD HAS UNIONISED.` |
| ring-rain | `THE ECONOMY IS DOING GREAT.` |
| ring-leak | `PLEASE MIND YOUR BELONGINGS.` |
| giant-badniks | `"FINALLY, THE RIGHT SIZE." — DR. ROBOTNIK` |
| ring-pong (first sidegame) | `WE INTERRUPT THIS PLATFORMER.` |
| ghost finale | `SANDOPOLIS SENDS ITS REGARDS.` |

Each caption appears one second after its label. Drop the score cards, slams and quad grids.

## Audio

- **Music bed:** one ROM track rendered for the whole length (about 240 s; it loops naturally). It plays unbroken with no switch per zone. I suggest the Data Select theme because it fits the calmer pace; look up its ID in the skdisasm constants. If you'd rather keep a known-good track, re-render the HCZ2 bed at this length and lower it 3 dB.
- **Recorded gameplay audio:** muted on cards 1–45. No sound plays when a card slides into the wall. The only sound effects kept are the two already verified on the Ring Leak card (frames 690 and 792), and only if they fall inside its clip.
- **Ghost finale:**
  1. The bed fades out over the last 60 frames of card 45.
  2. Card 46 plays the recording's own audio, untouched apart from one gain setting and a 6-frame fade-in. That includes the AIZ1 music, every ghost-appear `$92` sound, the hurt sound and the death sound.
  3. The recorded audio fades out over 30 frames into the end card.
  4. The bed comes back in over 0.5 s and fades out over the last 3 s.
- **Ghost sound check:** render `$92` on its own (`render_audio.py sfx 0x92`) and line it up against the recording's audio. At least one ghost-appear sound must land inside the window, within one frame of a visible ghost spawn. If it doesn't, start the clip earlier.
- **Loudness:** the final mix should measure −14 LUFS with true peak at or below −1.5 dBTP. Set the finale's level so its short-term loudness matches the bed.

## Delivery

- Put everything under `revision-3/`.
- Read existing recordings only from `../captures/` and `../revision-2/captures/`.
- New captures go in `revision-3/captures/`, and the finished video is `revision-3/out/sonic3k-chaos-mode-demo-v3.mp4`.
- Revision 1 and revision 2 stay exactly as they are.
- Drive the build from one `cards.json`, one entry per card: effect, label, zone, source, in and out frames, slot length, caption and cell. The same file can later feed an optional gallery web page without changes.
- The README should carry revision 2's honesty notes forward, plus one more: each card is a separate capture, and its zone label names the act where it was recorded.


## Accepted implementation adjustments

The final candidate uses48 distinct effects (the prior46 plus Ice Shoes and Spring Legs),14460frames/241seconds. The gallery stays stationary: a gentle18-frame dissolve replaces the proposed flying/sliding transition. Frozen thumbnails use exact1:4 nearest-neighbour reduction; the active picture is3x native400x224. The spare cells say57 MORE IN THE POOL.

Thirty-seven new sources were captured across11non-AIZ zones, with35 used in the candidate. The MHZ1 Right-only bunny take never produced an ordinary airborne transition; it is retained as a rejected demonstration, and the earlier AIZ1 actual hop949 is used instead. Its interval is858..1080, avoiding the old901-frame ghost EOF mistake and every other source EOF. The formerAIZ-only firing actors remain in their proven deeper Bloominator scene. Each card carries its actual host zone.

The large preview is the sole moving region. Completed cards remain frozen. The ghost finale is now a separately captured DeathEgg1 apparition/approach, with genuine mixed gameplayPCM, not the earlier AIZ death stinger. The new source has no observed death, so no death sound or death outcome is invented. The bed is a continuous270s native SMPS HCZ2 render; it is smoothly ducked for the genuine ghost source. Native cue92 is already requested on appearance;8A is requested on fade. Charge has no extra native cue. No engine sound changes were needed.

Qualification is recorded in SHOT_REVIEW.md and out/media-review/summary.json once actual final verification completes; this plan alone is not a pass claim.

The longer Snake excerpt revealed an early exit from the old board. A SOZ2 temple attempt was rejected: the positioned player was attached to a native pulley, so the sidegame correctly did not admit. A separate CNZ1 take uses a continuous32-frame Right/Down/Left/Up rectangle, keeping all selected frames on the actual moving board. This is ordinary authored input, not a score/world-state seed.
