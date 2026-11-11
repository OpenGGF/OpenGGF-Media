# MICA & TALON production promo — storyboard checkpoint (1)

Branch `feature/ai-mt-promo-production` = `b088fae95b` (TALON S2 gaze merged, fast-forward); jar sha256 `79796eae…a2cf6b`.
All captures re-shot from this build (S2 title shots after the gaze merge). Edit: `edit/edit.py` (brief in its docstring).

## Music edit plan

Track: "RUN INTO THE SUNSHINE (Chiptune Remix)", sha256 `569a921b…8481ff`, 162.8 s.
- Tempo 172.218 BPM (`promo_kit beats`). Phase: kit reported first beat 0.002 s, but the two big drops
  (riser into bar 12, breakdown exit into bar 36) hit at 16.90 s and 50.35 s, i.e. half a beat later:
  **bar 0 = 0.178 s** in the source. Bar line = 1.3936 s.
- Source sections (bars): 0–7 intro · 8–11 riser · 12–27 A (8-bar phrase played twice) · 28–35 breakdown ·
  36–59 B/bridge (stabs 44–47) · 60–75 chorus · 76–88 lift (peak 83–85) · 95–97 breakdown · 98–110 return/reprise
  (dark bar 104) · 111 break · 112–114 outro · **115 final hit (160.44 s)**, ring-out to ~161.7 s.
- Edit: **source bars 8–35, then bars 76–end** (one splice). 12 ms equal-power crossfade on the bar line; 4 ms
  head fade. The track's own ending and decay are untouched; nothing fades mid-phrase.
- Why that join: harmonic match end-of-bar-35 → start-of-bar-76 = 0.940 (the track's own 35→36 is 0.955, 75→76
  is 0.946); bar-similarity at the join 0.85–0.87 (= the track's ordinary bar-to-bar 0.85); onset flux at the
  join 344 vs. the track's own section entries 291–318. Measured, not heard.
- Output: 95.7 s audio; bar n out = source n+8 (n<28) / n+48 (n≥28). Final hit at **93.37 s**; fade to black
  lands on it; film ends ≈95.4 s on black during the ring-out.
- Mastering plan: kit mix (bed 0.75, ROM stingers ~1.6–2.0 so `check` sees none >9 dB under), then ffmpeg
  two-pass loudnorm to −14 LUFS, TP ≤ −1.0 dBTP, re-measured on the encoded AAC with `ebur128=peak=true`.

## Beat sheet (output time; bar = 1.3936 s)

| Time | Bars | Section | Shot | Proves | Accompaniment |
|---|---|---|---|---|---|
| 0.00–4.18 | 0–2 | Cold open (riser) | S3K title roll-in from the ball (native #258), camera chases it out to 1.0×, native white flash, logo drop, wink; slow push | The S3K intro is MICA, motion-blur smears and all | Hard start on the bar-8 downbeat; native flash ≈1.0 s; logo drop; wink ≈3.4 s; Tornado fly-by |
| 4.18–5.57 | 3 | Cold open | Gilded MICA Instagib flight (hero fragment, HUD whole) | Hero preview | Beam + rope swing motion |
| 5.57–11.15 | 4–7 | **Title drop** (drop) | S2 title as it ships, slam-out 1.3→1.0; MICA & TALON rise; native flash on bar 6; lock-up band "MICA & TALON" (S2 card blue, red tab, yellow strip, S2 card glyphs) enters after the flash, covers the native menu rows whole, exits left | The game's own title is the title | Flash + S3K Big Ring ($B3) on bar 4; native flash bar 6; band motion |
| 11.15–16.72 | 8–11 | **Ch1 HOMING ATTACK** | Banded wipe + card header; MGZ2 airborne three-Mantis chain, 1.65× tracked close-up (HUD and lives cropped whole) | Native chain scoring 100→200→500 | Punch-in + S3K explode ($B4) on hits #65/#82/#104 and #273; "1/2/3" counter + CHAIN pill |
| 16.72–22.30 | 12–15 | Ch1 | Slanted triptych: S1 GHZ2 / S2 EHZ2 / S3K AIZ, each slice drops a beat-pair apart and lands its own strike 40 frames later | Same move in all three games (S1 is a 2-badnik chain) | Slice drops; $B4/$C1 on each strike |
| 22.30–27.87 | 16–19 | Ch1 | S2 EHZ2 lock-on reticle → Buzzer strike, close-up | Reticle/lock is native UI | Punch + S2 explosion ($C1) at #281 |
| 27.87–33.44 | 20–23 | **Ch2 TALON** (breakdown) | Wipe + header "TALON / FLIGHT CARRY DIVEBOMB"; S3K carry: TALON grabs MICA, climbs through AIZ palms to the sea | Carry, hands/feet aligned | Climb is continuous camera motion |
| 33.44–39.02 | 24–27 | Ch2 | Stacked pair: S2 flight / S3K flight→divebomb on a Rhinobot | Same character in two games | Strip slide-ins; divebomb kill |
| 39.02–44.59 | 28–31 | **Ch3 THREE GAMES** (lift, after splice) | Wipe + header "THREE GAMES / EVERY SCREEN REDRAWN"; slanted title triptych S1/S2/S3K | Three art styles, one cast | Slices drop on beats |
| 44.59–47.38 | 32–33 | Ch3 | Pair at exact 3×: S1 and S2 signposts spin to MICA | Same moment, two games | Pop-in pair, spins |
| 47.38–52.95 | 34–37 (peak) | Ch3 | Slanted pair: S2 half-pipe (MICA runs the walls, TALON follows) / S3K Blue Sphere turn + jump | Special stages, posed per game | Native turns/tilt, ring pickups |
| 52.95–58.53 | 38–41 | Ch3 | 2×2 grid, cells pop a beat apart: Continue (S2), Data Select (S3K, stock No Save tile cropped out), special-stage HUD names, S1 lives icon | Breadth, every cell moving | Pops on beats |
| 58.53–61.32 | 42–43 | Ch3 | S2 ending: MICA flies beside the Tornado (TALON piloting) | Endings too | Sky fly-by |
| 61.32–65.49 | 44–46 | Ch3 | S2 ending close: the Tornado swoops in with MICA posed on the wing; slow push | Ending pose | Plane entrance |
| 65.49–69.67 | 47–49 | **Ch4 POWERED UP** (breakdown) | Wipe + header "POWERED UP / 70 RINGS, MID-ACT"; Solar TALON, full frame with HUD whole (RINGS 70, 2:00) | 50+ rings, plausible time | Divebomb kill, flight |
| 69.67–75.25 | 50–53 | Ch4 **hero** (return downbeat) | Gilded MICA transformation lands ON the downbeat → Instagib strike → beam flight, HUD whole | Hero moment on the biggest lift | Flash + S3K Super Transform ($9F) on the downbeat; small flash + $B4 on the kill |
| 75.25–79.43 | 54–56 | Ch4 | Stacked pair: GILDED MICA / SOLAR TALON in flight | Both powered forms | Strip slide-ins |
| 79.43–89.19 | 57–63 | Ch4 climax (reprise) | S2 EHZ1 end: Gilded MICA + TALON run, pops, signpost spins to MICA, "MICA GOT THROUGH ACT" tally | One take into the victory | Flash cut on the reprise; signpost; tally count |
| 89.19–95.4 | 64–67 + ring-out | **End card** | Iris; S2-card lock-up, "An example character mod for OpenGGF", github.com/OpenGGF/OpenGGF, disclaimer, over blurred/darkened S2 title (no HUD) | — | Big Ring ($B3) under the iris; fade to black on the final hit 93.37 s |

Pacing (kit): 19 shots, mean 5.0 s, busiest 20 s window 5 cuts, 2 cuts in the last 20 s, longest bare 0 s,
captions over gameplay ≤1 per chapter (the header subs). Stinger levels fixed after the first `check`.

## Files

- `keyframe-1-title-drop.png`, `keyframe-2-titles-triptych.png` (+ `keyframe-2b-special-stages.png`), `keyframe-3-end-card.png`
- `in-points-contact-sheet.png` — native source frame at each chosen in-point/event, with capture and frame number
- `edit-contact-sheet-every-0.5s.png` — the whole composed edit, one frame per 0.5 s
- `cold-open-frame0.png`, `s1-results-mica-vs-stock.png`

## Findings / decisions for the lead

1. **S1 results card is broken in the engine, not the mod.** The act oval and its blob render over "HAS",
   "PASSED" and "SCORE"; a stock-Sonic control at the same position/input shows the identical fault
   (`s1-results-mica-vs-stock.png`, capture `captures/ghz-clear-stock-control`). I keep S1 to the signpost spin
   and show results only in S2. Not filmed as it ships → listed as a known limit.
2. **S2 card glyph "M" reads as "/\/\"** at display scale ("/\/\ICA", same split strokes as the card's own
   "E/MERALD"). It is the native letterform. Options: (a) keep native (current), (b) native glyphs at a smaller
   scale, (c) MICA/TALON in the heavy condensed TTF on the same band. I recommend (a) for authenticity unless you
   find it misreads — your call.
3. **Competition and slot reels are not in the cut.** S3K Competition capture reaches the player-select (still
   cycling stock portraits) then `GameplayCaptureTool` throws in the arena draw
   (`Native arena has no published VInt registers`); reels need a positioned slot setup I did not build.
4. S2 homing chains: ~18 positioned probes in EHZ1/EHZ2 found no multi-badnik chain; the S2 shot is a single
   lock-on strike. S3K (3-chain) and S1 (two 2-chains) are true chains.
5. The S3K title's small Tornado fly-by (~20 px, visible ≈2.5–4 s) looks like the stock plane with an orange
   pilot; it is unreplaced native art at that size. Tell me if you want it cropped out of the push.
6. Positioned starts/declared rings+timer throughout (listed per capture in `provenance.json`); half-pipe,
   continue and ending use the retained debug component hosts, as in the previous promo.

Stopping here for review. Next after your reply: fixes, full 16:9 draft render, viewer pass, `check`, loudness.
