# Revision 2 captured-shot review

Read-only footage review of the 20 completed sources listed below. Read `PLAN.md`,
`edl.json`, every `output/state.csv`, and relevant provenance/input scripts before
examining the existing 400×224 PNG sequences. Contact sheets preserve the full
400-pixel width. Dense consecutive-frame checks cover shield/stars, monitor break
and Snake exit. No Java, build, capture, ffprobe, movie encoding or runtime probe
was launched. Python/Pillow work was a single bounded process. Sources and assembly
inputs were preserved.

These sources declare commit `ee0400cb3a295d0c4ded8d9336e772c536da3b18`, mod SHA-256
`e5460b29643b176683ba0a62eaeeff413a24d717aed112c9e84294ae36be1d02`, and 60 Hz
presentations / every-frame capture. All 20 CSVs contain 1080 rows, with no hurt or
death. This is visible-shot selection, not all-act or native-control certification.
Giant/Spinning/Tiny/Jelly use the disclosed positioned centre8912,877 setup; the
other sources start native AIZ1 without position/ring/world writes.

Times below are source seconds at 60 fps. Frame intervals are **start inclusive,
end exclusive**; trim within these windows to fit the beat grid.

| Source | Strong window / frames | Observed effect and qualification |
|---|---|---|
| afterimages, first reveal | 11.20–12.60 / [672,756) | Bright, dense overlapping Sonic crowd forms a broad worm across the brown foreground, including a jump arc. Much stronger than revision 1's four faint poses. Avoid the initially compact pile at source10.0. |
| afterimages, hero | 13.00–15.817 / [780,949) | Continuously crowded moving chain up the hill, down through the waterfall and into another curved jump. This is the strongest hero window. |
| rainbow | 10.333–11.75 / [620,705) | Sonic visibly changes purple/magenta/red/green while moving. Later [740,820) supplies distinct green/blue recap footage. |
| upsidedown | 10.00–11.40 / [600,684) | Entire playfield visibly turns upside down while native HUD and Chaos panel remain upright. Native movement follows the same route as the ordinary visual takes. |
| fastforward | 11.00–12.40 / [660,744) | Route and jump/camera advance rapidly; native timer advances substantially faster than the slow-motion source at matching presentation times. Pair with Slowmo at the same source time. No editorial speed change is needed. |
| slowmo | 11.00–12.40 / [660,744) | Slow jump/fall and modest horizontal progress. Actual source600→900 advances only5024→5593, compared with the ordinary moving takes reaching6353. Clearly legible as a pair, less clear as a 0.7s standalone. |
| hudorbit | 10.333–12.333 / [620,740) | Compact plaque travels around the player's on-screen position, including lower/side positions; labels remain attached to counters. Keep whole frame. |
| hudshuffle | 9.833–11.25 / [590,675) | Native Score/Time/Rings order visibly changes to Time/Rings/Score. Once shuffled it stays put; a before/after reveal communicates it better than a late isolated shot. Valid but subtle. |
| hudscale | 10.333–12.333 / [620,740) | Whole compact plaque changes from enlarged to reduced and back while counters remain native. Valid, but less striking than Orbit/DVD; suitable HUD quad spare. |
| shield | 10.033–11.00 / [602,660) | Real lightning shield arcs surround Sonic, first clearly visible at602. The panel's instant label at600 precedes the actual displayed shield. Not a Bubble shield. |
| superstar | 10.033–11.00 / [602,660) | Native white invincibility stars visibly orbit/trail Sonic, starting clearly at602. Bottom status receipt is present; no damage immunity claim is established by this safe route. |
| blueprint | 10.00–11.50 / [600,690) | Native foreground/terrain is replaced by cyan outlines, while Sonic/HUD remain readable. Later [780,880) keeps native green background behind cyan foreground. It is not collision-debug footage. |
| squashy | 10.00–11.667 / [600,700) | Whole gameplay picture changes width/height and black edge bands as input/jump states change; HUD stays readable. Real effect, but restrained, so retain a Full or before/after presentation rather than a narrow slice. |
| giant | 10.00–11.667 / [600,700) | Bloominator at screen≈360 visibly grows, with normal actor visible at600 and enlarged body thereafter. Native shots continue. Clear at400×224 and usable in the quad. |
| spinning | 10.333–12.333 / [620,740) | Bloominator rotates through diagonal, horizontal and upside-down poses while its anchor and native firing remain fixed. Clear at full width. |
| tiny | 10.00–11.667 / [600,700) | Bloominator visibly shrinks. Best fourth badnik panel opposite Giant, where the size comparison makes it immediate. Full-width frame is essential; a320-pixel crop would lose it. |
| jelly | 10.333–13.333 / [620,800) | Bounded squash/stretch affects the flower and left pickup artwork. It is subtle and native flower animation also changes its height; prefer Tiny for the short quad. Do not describe this as a dramatic enlargement. |
| breakout | 10.20–11.80 / [612,708) | Two spawned monitors flank Sonic; spindash charges, right monitor breaks around637–640, explosion/content appear and Sonic rolls out. Ring inventory reaches10. Actual escape is demonstrated, not merely the label. |
| vine | **No accepted swing window** | A small hanging rope/handle does appear above Sonic (especially640), but the script does not jump until760, after passing it. No grab, zip, swing or release was observed. Replace the planned A-tier swing shot. A602–660 preview can show placement only, but must not be counted as successful vine interaction. |
| snake | 10.05–12.50 / [603,750), restricted | Real Snake board appears, three blue segments move/turn, and the native world stays held. Score remains0 throughout. Board disappears at752 and gameplay resumes. No ring eaten or victory: fails PLAN's food-collection acceptance condition, though a clearly limited movement preview is honest. |
| chat | 10.50–13.333 / [630,800) | Readable bottom ticker says SIMULATED CHAT: STUCK THE LANDING! after the first landing. Later [810,900) shows NICE RINGS! following real pickups. Arrival600 initially has no message; use a later in-point. Keep Full and preserve the bottom line. |

## Afterimages intensity and hero correction

The source renderer retains24 historical poses and draws them at65–95% opacity,
plus the current actor. The PNGs show a crowded bright chain approximately180–220
native pixels wide, with numerous discernible heads/balls and overlapping bodies.
That is concrete proof of the requested stronger presentation. It is not a reliable
manual count of24 individually visible silhouettes; overlap and clipping obscure
an exact count. A nonnumeric fictional review such as "I COUNTED TOO MANY OF HIM"
avoids pretending the rendered count is an observed head count.

The proposed later hero14.70–17.517 is weaker: the dense arc persists through about
16.5, thins by16.75, and by17.0 the frame contains one stationary Sonic. Use the
13.00–15.817 hero above instead, and rearrange an overlapping recap as necessary.

## EDL and source-reuse pitfalls

- `arrival` means panel admission near600, not necessarily the first visible
  consumer frame: Shield/Stars become clear at602; chat needs the first landing;
  Afterimages needs motion and enough history to separate the crowd.
- Do not include Vine as a demonstrated swing, or claim Snake ate a ring. These
  failures of the planned shot conditions should not inflate a proof-based count.
- AIZ1 moving sources share the same 600-frame idle and repeated jump approach.
  Avoid cutting every shot from600: select the different windows above so the reel
  does not look like the same jump with a new label. The position-seeded badnik
  shots are a distinct disclosed setup, not a native approach clip.
- Afterimages has8s of active captured material (10–18s). The original EDL can ask
  for roughly9.1s across first reveal, split recap, quad, hero and final strip.
  It cannot supply unique frames for all those appearances. Drop/shorten one
  Afterimages recap, or use a different effect. At minimum never repeat an identical
  interval, and disclose/avoid partial overlaps where practicable.
- Crops/slices around Sonic remove the native Bloominator at screen≈360, left
  pickup or HUD/ticker. Giant/Spinning/Tiny/Jelly need whole400-pixel panels.
  HUD first appearances and Chat need whole-frame layouts. Tiny is legible when
  compared with Giant in a quad; Jelly is a weaker short-hit choice.
- The reused bumper/ghost sources in the original EDL are conditional on the
  root-owned donor-palette verdict/recapture. This review does not clear those old
  sources. Likewise old narrow rain and inventory-only leak footage must not be
  used to claim the new viewport rain or physical ring-leak behavior.
- No route deaths/hurt were recorded in these20 sources. Stars in a safe route
  prove visible native invincibility presentation, not immunity to pits/crushes.
- Keep the source-time versus native-time distinction for fast/slow pacing. The
  PNGs are presentation frames; do not apply an editorial speed ramp or treat the
  different native positions as a capture-rate defect.

Review sheets and enlarged inspection frames are temporary editorial aids in
`review-shot-agent/`. They can be discarded after the final selection is locked;
the source PNGs, CSVs, provenance and assembly inputs remain intact.

## Second bounded review: eleven spare sources

Reviewed the existing PNGs, CSVs and scripts for RingOrbit, Zoom, Quake, Defence,
SonicSays, Landmark, Rampage, Buddy, SpringLegs, Bunny and Blaster. All have1080
CSV rows and no hurt/death. Their provenance declares source
`d13f5c2fbfdccb2c62a9437541bfad091228b0bf`, native AIZ1 without seeded position,
rings or world state. This second pass also launched no build, capture, Java,
runtime probe, ffprobe or encoding. Full-width contact sheets and dense checks
of Quake motion, RingOrbit and the Bunny landing/jump use the existing PNGs.

| Source | Recommended window / frames | Qualified visible evidence and limit |
|---|---|---|
| ringorbit | 16.50–17.80 / [990,1068) | Gold rings visibly loop/drift around the now stationary player; native inventory7→8 during this window. Early600–760 has no nearby rings and demonstrates only the label, so override `arrival`. The late window is the clearer field-effect proof. |
| zoom | 16.00–17.40 / [960,1044) | With Sonic resting, the whole scene visibly zooms out/in, producing changing black inset margins while HUD remains fixed. It is gentle; a Full/Pair makes it clearer than a slice. An alternate moving window is12.00–13.40 / [720,804). |
| quake | 10.10–11.50 / [606,690) | Dense consecutive606–625 shows scenery/floor moving several pixels up/down relative to the fixed HUD. Actual bounded shake, not a dramatic earthquake; whole-frame view communicates it best. |
| defence, original take | **Exclude; no qualifying interval** | No sidegame board, badnik actors, projectiles or score appeared. Repeated A starts at600, and CSV records the player airborne at that admission presentation. The take remains ordinary vertical jumps under a generic Chaos countdown. Root owns a separate recapture with neutral admission; this result does not qualify that future take. |
| sonicsays | 11.00–12.40 / [660,744) | Bottom UI visibly issues `TASK: SONIC SAYS: DUCK (0/1)`. The script never presses Down, so no completion or reward is shown. Honest as an instruction preview, not a successful challenge. Keep the bottom text uncropped. |
| landmark | **Exclude; no qualifying interval** | The top label says Landmark Hunt, but no landmark thumbnail, destination instruction, completion or reward was observed in the sampled sequence. It does not meet the planned visible-landmark condition. |
| rampage | 10.10–11.50 / [606,690) | Sonic changes to a ground roll despite Right-only input, then remains a slow rolling ball. The explicit Down input does not occur until750, so this earlier interval establishes forced rolling. Valid but less spectacular than Blaster. |
| buddy | 10.35–11.75 / [621,705) | A real Tails companion appears and follows/jumps alongside Sonic. Later pickups raise the inventory beyond the solo control route. No carry, lift or rescue is shown: describe this as unexpected companion arrival/following. |
| springlegs | **Do not prefer as the Vine replacement** | Panel names Spring Legs, but the early one-tick A jumps match the ordinary visual takes' small jump heights and positions. The late path differs, but it does not cleanly establish increased jump height; badnik/terrain interaction confounds that comparison. No strong isolated boosted-jump payoff was found in this take. |
| bunny | **15.50–16.45 / [930,987)** | Best replacement for missed Vine. CSV shows a fall from a short ledge, landing948, and a fresh rolling jump949 with native yvel−1664. Every input row contains only Right, never A. Consecutive PNGs948–959 show the landing then upward rolling launch. This is a genuine automatic hop after contact; the earlier600–820 sequence is just running and should not be used as proof of hopping. |
| blaster | 11.15–12.50 / [669,750) | Long outlined horizontal projectile beams visibly cross the playfield, with another firing opportunity at720. Early600–640 contains the effect label but no displayed beam; use a later in-point. The take does not establish a projectile-caused enemy defeat, so avoid that claim. |

Selection recommendation: replace Vine with the Bunny contact/jump window, use
Blaster and Buddy as strong extra glimpses, and optionally Rampage or the real
SonicSays prompt. RingOrbit/Zoom/Quake qualify in the later/specific windows above
but are deliberately gentle. Exclude the original Defence and Landmark takes;
do not increase the demonstrated-effect count from their selected-pool labels.
For a1.4s Vine-slot replacement, broaden Bunny to15.40–16.80 / [924,1008): this
includes the approach/fall, the proven949 hop and its landing, without a speed edit.

## Replacement Defence: qualified board and scoring, no visible bolts

The rejected airborne take was moved out of `captures/defence` (under
`rejected-takes/defence-airborne` before root-owned cleanup). Its rejection above
remains the record of that take only. **The current `captures/defence` is a new
qualified source**, reviewed after it completed1080frames.

Provenance declares source `d13f5c2fbfdccb2c62a9437541bfad091228b0bf`, mod SHA-256
`e5460b29643b176683ba0a62eaeeff413a24d717aed112c9e84294ae36be1d02`, and an owned
normal input configuration binding A=Space, B=X, C=C. Shared user configuration was
not changed. The script waits620presentations, then alternates A/B/C with14neutral
frames between each press. CSV records Sonic fixed at5024,1050, grounded, with no
hurt/death and no native ring award throughout. Native act time remains0:10 while
the sidegame clock and actors advance, showing the held-world behavior.

**Recommended1.4s window:14.00–15.40 / [840,924).** The lane board contains several
moving native-art badniks, spring launcher artwork appears in the selected lanes,
badniks disappear as defences act, and the displayed DEFENCE counter rises2→5.
Consecutive840–898 checks establish that this is changing gameplay and score,
not only an admission label. The full take reaches displayed score8 by1020 and
still has an active board at1079; no victory or reward was shown.

There are **no visible travelling projectile/bolt actors**. This is corroborated
by the source `ChaosSidegame.defence`: charged lane state periodically removes the
closest enemy; its draw branch renders springs and badniks only. Describe the shot
as lane defence, activating launchers or defending/scoring. Do not say the footage
shows a projectile firing across a lane. This limits the claimed mechanics but
does not negate the real board, actor movement, input response and score changes.

Only existing PNG/CSV/provenance/script reads and bounded Pillow sheets were used
for this replacement review. Source media, configuration, inputs and assembly files
remain unchanged.
