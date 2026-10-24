# Sonic Echoes promo — provenance

Finished production, 2026-10-24. Delivered film: `out/sonic-echoes-promo-final.mp4`, 74.3 s,
1920×1080 at 60 fps, H.264 + stereo 48 kHz AAC 256 kbit/s, −16.1 LUFS integrated, −3.5 dBTP true
peak (measured on the encoded file), eight chapters, faststart. Edit and assembly by Claude Opus 5.5;
footage captured by two Codex GPT-6.1-Sol workers (medium reasoning) to the lead's shot list.

## Engine and mod

- Mod: Sonic Echoes (`examples/sonic-echoes`), OpenGGF `feature/ai-sonic-echoes`.
- Footage was captured at `5fca08819f` (first mod commit) plus the then-uncommitted test-only
  capture helpers `PromoCaptureMod` / `PromoActionCaptureMod`, committed afterwards in `364d7d02a0`.
- `364d7d02a0` also fixes two defects found while filming (see the design doc's "Promo capture and
  fixes found while filming"): per-frame wrapper allocation that aborted room sessions longer than
  about a minute, and the stock HUD drawing over the room HUD for ~1 s of each room entry. The film
  uses no room-entry frames from the takes recorded before the HUD fix (a1, a4 cut from the hub
  confirm to the room's first playable frames), and no take ran long enough to hit the abort.
- ROM: Sonic 2 World REV01, SHA-1 `8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9` (user-supplied, not archived).

## Source kind and honesty

Every shot is a display-free (`surfaceless-egl`, no DISPLAY/WAYLAND) `GameplayCaptureTool` take of
the real mod: ROM physics, native objects (Obj14 seesaws, Obj41 springs, Buzzer, Spiny), driven by
the rooms' authored reference inputs (`rooms/*.properties`, the same routes `RoomSolutionsTest`
replays). Entry methods: **cold title boot** for a1 (title → hub → 1-1 par clear → hub → 1-1 shard
clear → hub) and a4 (hub tour on a save honestly earned by replaying reference routes, 33/36, room
3-4 unplayed); **pre-boot room selection** for every other take. Echo/Reset presses that the routes
need before the loop clock expires are scheduled at the authored loop frames through
`RoomSession.command` (equivalent to pressing E/R). No teleports, forced positions or forced drift.

Editorial time: shots are cut and re-ordered; one **labelled ½-speed** window (frame-doubled) covers
the Paradox divergence. The four-loop grid repeats each loop's capture while it is on screen.
Measured overlays read the session sidecars: "DRIFT 0 PX" values are world-coordinate differences
between a live run and the echo replaying it (verified 0 across 217 samples in 1-4 and 240 in 3-1's
corrected loop); the Paradox counter is the same measurement (0 until frame 540, then 19/41/46 px,
fracture at 552 when it passes 48).

## Shots used (capture frames)

| Chapter | Take | What it proves |
|---|---|---|
| Cold open | b5-last-loop (final loop, Spiny kill 1101), a1-chain (commit 1262, rewind flash), b1-double-bounce (launch) | Four echoes at once; the loop; a native seesaw |
| Title | b5 loop 3 (dimmed, slam-out), a1-chain title → hub → confirm 961 | The mod's own ECHOES title and hub |
| The loop | a1-chain 1-1 par visit (commit 1262, restore 1274, clear 1437, stars 1449/1467) | An attempt becomes the cyan echo that holds the door |
| Same buttons | a3-escort loop 2 live (Buzzer kill 374) beside loop 3 magenta echo (kill 604) | Same inputs, same jump, same pop, 0 px drift |
| Echoes are real | b1 (launches 1778/1960), b3 (echo spring 1757), b6 (latches 2527/2566/2588, clear 2606) | Native seesaw, spring and timed latches react to echoes |
| Paradox | b4-paradox (blocked recording, rewind 420–432, early plate, fracture 552; post-Reset corrected loop, clear 1721) | The live run opens a gate the recording was blocked by; the echo breaks; waiting fixes it |
| Hub | a4-hub-tour (moves 961–1091, confirm 1152 on b128) | Earned progress lands on the unplayed finale |
| The Last Loop | b5 loops 1–4 in a 2×2 grid, then the final loop (restore 975, plates 1024/1068/1093, Spiny 1101, clear 1193, stars 1205/1223) | Hero moment |

Unused takes (kept as sources): a2-two-hands, b2-counterweight; a-helper-proof is the helper's proof run.

## Sound

Bed: Sonic 2 Chemical Plant ($8C) rendered through OpenGGF's SMPS driver
(`FmSfxRenderTool --game s2 --music 8C --rate 48000 --paced`), 139.441 BPM, first beat 0.211 s; the
song loops every 128 beats (55.08 s) and the finale chapter starts on b128. Stingers: ROM SFX rendered
the same way (`--sfx <id> --paced`), placed on their real event frames from the sidecars: the mod's
rewind $BC, Paradox $C6, star pops (RingRight $B5 folded to centre), springs/seesaw $CC, badnik $C1,
hub $CD / $A1, Giant Ring $C3 under the iris; ring pops on graphics alternate $B5/$CE (right/left).
Master: `edit/master.py` (two-pass loudnorm to −16 LUFS, −4.4 dBFS limiter) because the FM bed
overshot to +2.7 dBTP after AAC with promo_kit's −0.7 dBFS PCM mix. Sound was checked by measurement
only (loudness, true peak, stinger level/panning via `promo_kit check`); nobody listened to it.

## Review rounds (lead, before delivery)

1. First sheet: chapter 1 used the wrong 1-1 visit; cold-open words collided with the mod's LOOP
   banner; stacked strips sliced the control strip and lost Sonic → fixed; split rebuilt as two
   tracked panes.
2. CPZ floor sits under the HUD-free window, so the split moved to 1-4 (higher floor, same Buzzer pop
   in both loops); badnik proof moved there, Clockwork joined chapter 2.
3. Spring/escort timing, header crops (measured control strip 182–217), tracked final-loop labels
   staggered, hub chip removed (native UI already carries the text), lone left ring centred.
4. Viewer pass: 44–50 s was a caption over idle play → Paradox take trimmed 1.5 s after the
   fracture; the time went to the corrected loop with a live "ECHO 1 · DRIFT 0 PX" tag.
5. Audio: +2.7 dBTP after AAC → mastered (above).

Known limits: `promo_kit check` still notes four captions in the first 20 s (the RUN IT / LOOP IT /
TEAM UP promise stack plus the genre line), kept deliberately. No user review yet.
