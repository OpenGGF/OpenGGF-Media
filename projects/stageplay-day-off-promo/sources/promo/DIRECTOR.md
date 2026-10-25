# Day Off: director's note

## Version 2 (2026-10-24, after "best, no contest")

**Deliverables** (in `out/`; v1 is kept unchanged):

- `day-off-stageplay-v2.mp4`: the promo. 2:20.03, 1080p60, H.264, AAC 256 kbit/s, 12
  chapters. −15.2 LUFS and −1.4 dBTP, measured after the AAC encode.
- `day-off-film-v2-1080p.mp4`: the film by itself. 74.97 s, 6 chapters, one +8.0 dB gain only.
  −16.6 LUFS and −1.4 dBTP.

Engine: develop `81f25c89f`. Desktop editor: OpenGGF-Editor main `dd5ee43`. Film take:
`scenes/t10.stageplay`. Provenance is in [PROVENANCE.md](PROVENANCE.md#version-2-out-day-off-stageplay-v2mp4-out-day-off-film-v2-1080pmp4).

### What changed

The story, movement, jokes, timing, camera and music of v1 are unchanged. The film changed in
these ways:

- **Voices.** Every speaker now uses the engine's built-in voice: Sonic **Soft Cool**, Tails
  **Workshop**, Knuckles **Red Rattle**, the Motobug **Patrol Buzz**. My external `make_voice.py`
  clips are retired. I did not retune anything: the defaults sit 7–9 dB over the music in every
  scene (measurements below), and each character sounds distinct.
- **The Motobug speaks for itself.** It is a real speaker (its object cast role), with a tail that
  follows it.
- **Facing.** Keys use logical `facing`. The Motobug faces the way it drives in every shot. In v1
  it drove backwards in the loop, Emerald Hill and Angel Island shots. It still looks back once on
  Angel Island and faces its friends on the ledge.
- **Loop priority (confirmed in the shot).** The Motobug rolls across the loop's inner bottom,
  slides behind the front pillar (fully hidden around film frame 910) and comes out facing right.
- **Floors.** Floor heights now come from `stageplay ground`: three batched runs, one JVM per set,
  run one after another.
  - Emerald Hill, Angel Island and the ledge sit about 1 px lower than v1, which had floated
    slightly.
  - The loop's exit ramp sits up to 4 px higher.
  - The patrol drop now lands on the real floor (y 945; v1 used 959, off-screen).
- **Sonic's route** is the one the editor planned from the picked point (5860, 620). It has the
  same timing as v1 and stops at the same spot.
- **Emerald Hill music** is cued 8 frames into the shot, still under the wipe (see bug 1).

The making-of was re-captured in the redesigned editor. Paths now show `/tmp/stageplay`, with no
home directory on screen.

- **Route:** the Plan route form, then the **in-level picker**. A crosshair glides past the loop
  and the floor guide snaps to 620. Walk fails. Details gives the planner's reason, "needs Run",
  which I box. Then Run / Hard / Left from the same picked point, the checked line, Apply, both
  editors playing the route, and the wipe into the film.
- **Facing:** the Puppet key's form, with its Facing row boxed.
- **Voices:** a new four-shot beat. Sonic's line form, the Motobug's voice form, the fifteen
  presets with "Motobug / Patrol Buzz (default)" boxed, then its "Day off." playing in the
  editor with tail and voice.
- **Cut:** the second pick and the numeric retyping. The Run form shows the same Position
  (5860, 620), so continuity holds.

### Viewer pass, v2 (one row per ~4 s)

| Time | On screen | The viewer feels / understands |
|---|---|---|
| 0:00–0:08 | The Motobug patrols and stops at the edge. Its lines buzz word by word, with a tail pointing at it | A talking badnik. The tail and buzz make it the speaker beyond doubt. |
| 0:08–0:14 | "Thirty-five years of this." "I need a day off." It drives off, facing the way it goes | The joke lands. Nothing looks wrong (v1's backwards driving is gone). |
| 0:14–0:20 | Hard cut, DAY OFF. The Motobug slips behind the loop's front pillar while Sonic runs the loop | Depth: it is *in* the level. |
| 0:20–0:28 | Sonic's soft hollow voice, the Motobug's buzz: "chasing me?" / "Day off." / "Fair enough." | A real exchange between two voices. |
| 0:28–0:40 | Emerald Hill with its music. Tails chatters letter by letter: "aren't you from Sonic 1?" "Long drive." Wipe | Each character has a sound. 0:36–0:40 is still the softest stretch. |
| 0:40–0:56 | Knuckles glides in and rattles: "No badniks on my island!" … "They do now." Fade | The running gag pays off. |
| 0:56–1:02 | The ledge, facing friends: "Best. Day. Ever." | Warm ending. |
| 1:02–1:05 | Pull-back into the editor, STAGEPLAY, rewind | The reveal. |
| 1:05–1:12 | The shot list, then the cast, now spelled out (Sonic 1 / Sonic 2 / Sonic 3 & K / Object) | Three games, readable without decoding "s3k". |
| 1:12–1:17 | FREE → PUPPET switch, then the Puppet key form with Facing boxed | The central idea, plus the direction it faces as one field. |
| 1:17–1:24 | World commands, the camera key, the brackets push-in | Unchanged from v1. |
| 1:24–1:29 | Plan route, then the picker crosshair gliding past the loop and snapping to the floor. "Pick a spot. It snaps to the floor." | **The new hero idea:** point at the level. |
| 1:29–1:35 | Walk: a red cross, then Details with "needs Run" boxed | Fail, then the reason. |
| 1:35–1:45 | Run / Hard / Left at the same Position, the checked line, Apply | The fix, then the line. |
| 1:45–1:52 | Both editors play it, then the wipe into the film | Unchanged, still strong. |
| 1:52–2:00 | Sonic's line form. The Motobug's voice (Buzz, Word, 69, 80), the 15 presets, its "Day off." with tail. "Every speaker has its own voice" | The voices they have been hearing come from here. |
| 2:00–2:05 | Screenplay excerpt (now y 620.0), Export | Closure. |
| 2:05–2:20 | NEXT MORNING with voices, then the end card | Callback, then where to get it. |

Changed because of the pass:

- The first route capture used the default 300 attempt frames, and its Details had no advice. The
  failure then explained nothing, so I re-captured with v1's 419-frame window for the Walk plan.
  The planner's own Run check then reports "needs Run".
- The picker beat comes first and gets a caption, because it is the easiest new idea to grasp.
- I added the voice beat so the most audible change has a visible source.
- I raised the caption band on the presets shot after a frame check showed it half-covering the
  last list row.

Total length grew from 2:10 to 2:20. Pacing checks still pass: at most 10 cuts and 3 captions in
any 20 s.

### Sound (measured, not heard)

Measured against a voices-off render of the same take (`t10-novoice`):

- **No mixer dips are possible.** The two renders are bit-identical outside the 103 voice blips.
  The voiced film peaks at −9.5 dBFS. The scene mixer only scales a block whose summed peak
  exceeds 30000 (−0.77 dBFS; `AudioManager` scene mixer), so it never engaged.
- **Voice level over the music under it:** Sonic +8.0 dB, Tails +8.7, Knuckles +7.0, the Motobug
  +7.8. The Motobug's first patrol lines play over silence after the takeover's `MUSIC_STOP`.

Promo levels after the AAC encode, by section:

| Section | Loudness | True peak |
|---|---|---|
| Film | −14.2 LUFS | −1.5 dBTP |
| Title | −15.5 LUFS | |
| Making-of | −16.4 LUFS | |
| Epilogue | −13.3 LUFS | |
| End card | −18.9 LUFS | |
| Whole promo | | max −1.4 dBTP |

The mix was mastered to −1.5 dBTP before AAC with one gain (−1.20 dB). I still cannot hear any
of it. Whether the voices are charming at these levels, and whether the Emerald Hill restart under
the wipe is seamless, are unheard.

### What I could and could not check (v2)

- **Verified by measurement or byte comparison:**
  - The editor's Export film is stream-identical to the CLI render.
  - The exported screenplay recompiles byte-identically.
  - The two editors' applied scenes are byte-identical.
  - The 4× export is pixel-exact against the 1× frames.
  - Facing and priority were checked by frame crops.
- **Not checked:** continuous playback at speed, and listening.

### New Stageplay bugs and rough edges (v2)

1. **An S2 music cue on an S2 shot's entry frame fades to silence.**
   - Evidence: `probe/s2cue` renders four Emerald Hill shots after Green Hill ones.
     - Cue at frame 0: fades over about 5 s (−34 → −58 dB, then silence).
     - Cue at frame 8 or 40: steady at about −30 dB.
     - No cue: silent.
   - In my film: t07 (cue at 0) faded; t09/t10 (cue at 8) play normally. S1 and S3K entry cues in
     this film are unaffected.
   - Likely cause: the native S2 level entry's fade-out reaches the authored song. v1 hid this
     because the automatic level playlist restarted EHZ.
2. **S2 `soundId` uses the engine's numbering, not the ROM's.**
   - The shipped ROM's zone music table at `$3EA0` reads `82 82 85 84 …`: EHZ is `$82`, as in
     `s2.constants.asm:834`.
   - The engine's `Sonic2Music` has `EMERALD_HILL = 0x81` and `METROPOLIS = 0x82`, with a
     hardcoded song map. `Sonic2SmpsConstants` notes the reconciliation is pending.
   - Consequence: an author following the disassembly gets the wrong song. I briefly did (t08).
3. **The route Details repeats one diagnosis three times** (job message, result message, reason).
   See `captures/v2/editor-route/route.mkv` frames 877–1097.
4. **The "needs Run" advice depends on Attempt frames.**
   - At the form's default 300, the detour used every node (1024 of 1024), so the reserved Run
     check never ran and the Walk failure explained nothing.
   - At 419 the advice appears (796 nodes).
   - Evidence: the first v2 capture's Details screen (default 300 frames) reads "301 samples,
     1024 nodes, 26686 ticks" with no advice (`review/route-sheet.png`, frame 770; that capture
     was replaced). The final capture (419 frames) reads "413 samples, 796 nodes, 21470 ticks"
     plus the advice (`captures/v2/editor-route/route.mkv` frames 877–1097 and `route.log`).
5. **The HUD side panel truncates the route result.** It shows "Search limit reached;
   reachability is unk…"; the full sentence is only in the status menu and Details.
6. **Fixed since v1 (verified):**
   - the "?" line-break glyph;
   - the route-panel text overlap;
   - EHZ native music leaking into `MUSIC_STOP` stems (the v2 stem is silent there);
   - object speakers and pointers;
   - backwards Motobug art;
   - the loop draw order.

---

## Version 1


**Deliverables** (all in `/home/farrell/Videos/OGGF/sp-promo-a/out/`):

- `day-off-stageplay.mp4`: **the promo**. 130.2 s, 1920×1080, 60 fps, H.264 (CRF 14), 48 kHz stereo
  AAC at 256 kbit/s. −15.5 LUFS integrated and −1.3 dBTP true peak, measured after the AAC
  encode. It has 12 chapters.
- `day-off-film-1080p.mp4`: **the finished film by itself**, as Stageplay exported it. 74.97 s at
  1080p60. It has 6 chapters, one per set. Its only change is a single +8.9 dB audio gain, which
  brings it to −16.7 LUFS and −1.5 dBTP. There is no other processing.

Other files: provenance is in [PROVENANCE.md](PROVENANCE.md), the treatments are in
[TREATMENTS.md](TREATMENTS.md), and the edit is `edit/edit.py`. The locally staged media archive is
in `archive/` (see the end of this note).

## The idea

The first badnik Sonic ever met is tired of patrolling the same ledge after thirty-five years, so it
takes a day off in two other games. The promo plays that film straight through. It then pulls back
into the editor at the exact frame it stopped on and shows how each piece was directed.

The story's turning point is also Stageplay's central idea. The Motobug starts **Free**, running its
own badnik AI. The moment it rebels is the director's **Puppet** key.

### What changed from the treatment

The holiday became a road trip through three games instead of two:

- Green Hill (S1), with Sonic and his skid.
- Emerald Hill (S2), where Tails asks "aren't you from Sonic 1?" "Long drive."
- Angel Island (S3K), where Knuckles glides in using his native glide.
- A final shot of all four on the Angel Island ledge: "Best. Day. Ever."

The next-morning epilogue plays as the film's own ending, before the end card. Its Green Hill music
then carries on under the end card, aligned to the film's own GHZ cue to the sample.

## The least certain sections

### 1. Sixty-two seconds of film before the product is named (0:00–1:02)

Opening on the finished film lets the jokes land before any interface appears. The cost is that a
viewer who does not know Stageplay waits a long time for the reveal. The only early anchor is the
title "DAY OFF / A STAGEPLAY FILM" on the cut into the loop at 0:14.

Alternatives I considered:

- **Editor-first** (treatment B). Rejected: the viewer would get half a minute of UI before caring
  about anyone on screen.
- **A shorter film.** I would have dropped the Emerald Hill leg or trimmed the ledge. Rejected:
  the trip across games *is* the joke. Every leg already delivers a line every 2–5 s, and cutting
  inside a scene breaks the film's own music and dialogue timing.
- **A corner "made with Stageplay" bug over the film.** Rejected: it puts UI language on the
  thing the promo claims is finished.

The promo-kit check still reports the film as "bare gameplay". The kit cannot see in-film dialogue,
title cards or transitions. The viewer pass below shows a new beat every few seconds, except one
soft stretch.

### 2. The making-of was rushed in the first cut (1:05–1:55)

Revision 1 cut 18 shots into 40 s on the bed's beat grid, many of them 1.1 s. It used 12
captions, plus chip labels on top of the menus' own headers. The kit flagged 11 cuts and
12 captions within 20 s. The stills confirmed it: an editor form held for 1.1 s cannot be read, and
the chips sat on native UI text.

Revision 2 has 17 shots in 49.5 s and at most 3 captions in any 20 s. Each idea is shown by a
callout tied to what changes on screen:

- **FREE | PUPPET switch.** It flips on the exact frame of the Motobug's PUPPET key. I matched the
  editor preview to the film frame by frame to find it.
- **Camera-key brackets.** They mark the key's framing and are tracked through the film camera's
  real eased move, using the simulate telemetry. The camera lands inside them at frame 439.
- **A box on "needs Run".** It sits around the route planner's own explanation, after a push-in on
  the HUD text.
- **A box on Sonic's line.** It sits around the dialogue form's text row, straight after the film
  shows that line.

Captions over menus sit on an opaque band that replaces the menu's key-help row, so no editorial
type touches native UI.

Rejected alternatives:

- **Every UI shot as a floating "window" card.** At 2/3 scale the 3× pixel font becomes 2×, and
  the HUD's smaller text drops to about 17 px.
- **Chapter title cards.** They would add another text layer over UI the viewer is trying to read.

Still uncertain: the scene-change list, world commands and the camera form are uncaptioned menus. A
first-time viewer can read "CLEAR_BADNIKS" but may not connect it to the empty levels in the film.

### 3. Both editors during the hero run (1:41–1:48)

Revision 1 played the route full-screen in the in-engine editor and peeled it into the film. It then
replayed the same run later in a split to show "both editors". That put the loop on screen a third
time.

Revision 2 makes the split *be* the playback. Both editors play the applied scene in sync, and a
wipe crosses from the split straight into the film for Sonic's hard stop and line. "Two editors.
One scene file." is literal here. Given the same request, the in-engine and desktop editors wrote
byte-identical `.stageplay` files.

The cost is that the loop run is half-width in each slice during its best seconds. I also considered
splitting on the proposed line before Apply, and rejected it. That moment is static, and only the
in-engine capture pans along the line.

### Also uncertain: the Motobug's voice

No game has a Motobug voice. Dialogue-only typing felt dead in the cold open, and ROM sound effects
would claim game events that are not happening. The Motobug therefore speaks in original
PSG-style square-wave syllables (`scenes/make_voice.py`), one per word. Each syllable is on the
frame its word appears, which I verified against the authored timeline. **I could not hear
whether it is charming or grating.**

## Viewer pass (first-time viewer, one row per ~4 s)

| Time | On screen | The viewer feels / understands / misses |
|---|---|---|
| 0:00–0:04 | GREEN HILL ZONE 9:00 AM. A Motobug patrols, "Patrol... turn. Patrol..." with beeps | A familiar place and a talking badnik: curiosity. They may assume it is a mod or gameplay. |
| 0:04–0:08 | It reaches the edge and stops. The camera eases in. "..." | It is not doing its job, and the push-in says something is coming. |
| 0:08–0:12 | "Thirty-five years of this." "I need a day off." | The joke lands. Older fans get the 1991 arithmetic. |
| 0:12–0:16 | It drives off the edge. Hard cut to the loop. DAY OFF / A STAGEPLAY FILM | The title names a film and a word ("Stageplay") they do not know yet. |
| 0:16–0:20 | Sonic runs the loop, skids to a hard stop and turns back | The action payoff, with Sonic's arrival as a gag. |
| 0:20–0:24 | "Uh... aren't you supposed to be chasing me?" "Day off." | The central joke. Two characters now perform the same scene. |
| 0:24–0:28 | "...Huh. Fair enough." Wipe | The story moves on. |
| 0:28–0:32 | EMERALD HILL ZONE 10:00 AM. Tails: "Wait... aren't you from Sonic 1?" | The cross-game idea registers: a Sonic 1 badnik in Sonic 2. |
| 0:32–0:36 | "Long drive." | A laugh. |
| 0:36–0:40 | The Motobug rolls past Tails. Wipe | **The softest stretch.** Nothing new until the wipe. I kept it because the drive is the gag's tail, and the next set arrives at 0:39. |
| 0:40–0:44 | ANGEL ISLAND ZONE 11:00 AM. The Motobug arrives by the waterfall | A third game. The wait for who lives here is short. |
| 0:44–0:48 | Knuckles glides in on his native glide (frames 2658–2733), lands, and says "Hey! No badniks on my island!" | A move they recognise, and an indignant host. |
| 0:48–0:52 | "Day off." "...Badniks get days off?" | The running gag pays off. |
| 0:52–0:56 | "They do now." Fade. LATER | Warmth. |
| 0:56–1:02 | All four on the ledge. "Best. Day. Ever." | The ending. Some viewers may think the promo is over. |
| 1:02–1:05 | The picture shrinks into an editor's preview at the same frame. OpenGGF STAGEPLAY: "Your own Sonic films. Real levels. Real physics." Rewind | **The reveal:** this was made in that editor. The rewind promises "here's how". |
| 1:05–1:09 | The shot list opens: CUT s1, WIPE s2, WIPE s3k... | It is a timeline of shots. "s1/s2/s3k" may only half-register. |
| 1:09–1:12 | Zoom into the cast: Sonic S1, Tails S2, Knuckles S3K, Motobug S1 object | The cast comes from three games. |
| 1:12–1:16 | The Motobug patrols. FREE is lit, then PUPPET lights and it never turns. "It runs its own badnik AI" → "Now it waits for you" | **The central idea, explained by the switch.** |
| 1:16–1:20 | Its role keys (0 FREE, 327 PUPPET, POSE...). World commands (CLEAR_BADNIKS) | The keys prove the switch. World commands go uncaptioned (see section 2). |
| 1:20–1:24 | The camera-key form (zoom 2), then brackets marking that framing as the camera lands in them | A camera key, shown rather than told. |
| 1:24–1:28 | Route form: destination typed, Walk. "Give Sonic a destination" | Pathfinding starts. |
| 1:28–1:31 | A red cross, then a push-in on the planner's reason with "needs Run" boxed | The planner explains its failure, a small story beat. |
| 1:31–1:34 | Run, Hard Stop, Face Left | The fix, readable as typed. |
| 1:34–1:39 | The proposed line traced through the loop, panned along. "Planned and checked under real physics" | **The hero image.** |
| 1:39–1:41 | "Check inputs and apply route" | Apply happens before playback, as the brief asked. |
| 1:41–1:44 | Both editors play it in sync. "Two editors. One scene file." | Two tools, one file. The run is half-size here (section 3). |
| 1:44–1:48 | Wipe into the film: Sonic stops, faces left and says his line | **The payoff:** the line on screen became the film. |
| 1:48–1:50 | The dialogue form, with the line just heard boxed | Lines are data you edit. |
| 1:50–1:53 | Screenplay excerpt typed: the route and Sonic's line. "Prefer text? The whole film is a screenplay." | A text path for creators. |
| 1:53–1:55 | The export form. "Export the finished film" | Closure for the making-of. |
| 1:55–2:03 | NEXT MORNING. "Patrol... turn." "...Only 364 days to go." | The callback lands harder for having seen the making-of. |
| 2:03–2:10 | Wordmark, STAGEPLAY, the promise, URL, status, disclaimer. The GHZ music carries on | Where to get it and that it is still in development. Seven seconds is enough to read it. |

**Changed because of the pass** (revision 1 → 2): the making-of restructure in sections 2 and 3.

- Its music bed was raised from 0.62 to 0.95 gain, game level. I measured the making-of 4–5 LU
  quieter than the film (−16.9 against −12.7 LUFS), which would have felt like the promo deflating.
  It now sits 1.3 LU below the film.
- The title card over the paused editor became a composed screen rather than "gameplay".
- A screenplay line that overflowed its panel was rewrapped.
- The failure-panel crop moved below two HUD rows that overlap each other. That overlap is a rough
  edge, listed below.

Not changed: the 0:36–0:40 stretch and the uncaptioned menus at 1:05 and 1:16 (reasons above).

## What I could and could not check

- **I cannot hear.** Every sound decision was checked by measurement only:
  - section loudness and true peak after the AAC encode;
  - the voice syllables against word-reveal frames;
  - SFX stems placed by scene frame under editor playback that I matched to the film frame by frame;
  - the GHZ continuation, aligned to the film's GHZ cue.

  Whether the bed suits the making-of, whether the rewind sound reads as a rewind, and whether the
  beeps are pleasant are all unheard judgments.
- **I cannot watch it in real time.** I reviewed contact sheets every 40–90 frames and full-size
  stills at every callout, transition midpoint and camera move. I also checked the encoded MP4's
  pixels at 1:1 and fully decoded both files without errors. Continuous motion was sampled, not
  watched. Fractional-zoom shimmer on the HUD push-ins (2.15× and 2.2×) is possible and unverified.
  Those zooms use the kit's nearest-up/area-down filter.
- I did not check playback on a TV or phone.
- The editor footage shows local file paths that include the home directory name ("/home/farrell/…"),
  for example the export form at 1:53. I left these because they are real UI, but you may prefer to
  blur them before publishing.

## Stageplay bugs and rough edges found

1. **Fixed on my branch (it blocked the route):** the route planner could not plan through Green
   Hill's loop. Its isolated probe launched Sonic as if the loop were a ramp, because
   `Sonic1LoopManager` read the zone and plane tables from the global level rather than the player's
   own (`Sonic_Loops`, `_incObj/01 Sonic.asm:1536-1611`).
   - Fix: commit `0ba60490e` on `feature/ai-sp-promo-a`, with the ROM test
     `TestStageplayPlayerRouteRom#ghzLoopRouteSwitchesNativeLoopPlanesInTheIsolatedProbe`. That test
     fails without the fix.
   - Checks run: `TestStageplayPlayerRouteRom` passes 6/6. The S1 GHZ/SLZ trace replays and
     `TestS1Ghz1Headless` pass. The exception is `TestS1Slz3CompleteRunTraceReplay`, which fails
     identically on the base `632a5f8c3` (27 errors, first at frame 3379 on rings).
   - Not run: the change-based plan selects all smoke categories (3,716 classes). I judged focused
     checks proportionate, because normal gameplay resolves the same level either way.
2. **In-engine menu subtitles cannot break lines.** `StageplayWorkspace.java:1350` builds
   `reason + "\n" + N + " path samples…"`, and the HUD modal draws the `\n` as a "?" glyph
   ("Review, then Apply.?419 path samples"). It is visible at 1:39 in the promo.
3. **HUD text overlap.** While a route status is shown, the selected actor's state line
   ("IDLE x5100.0 y684.0 / airborne") is drawn on top of the route legend ("Cyan: walk  Gold: air /
   takeoff"). This affects route capture frames 524–1914. I cropped around it.
4. **Route form prefill.** "Plan collision route" pre-filled Run from an unrelated later MOVE_TO in
   the same shot. I worked around it by capturing from a before-route copy of the scene
   (`scenes/t06-editor.stageplay`).
5. **A shot entered through a WIPE starts black.** Its first frame is the transition's fully black
   midpoint, so the editor preview at the route window's entry is black. I gave the loop shot a CUT.
6. **The HUD camera cannot zoom a draft below 1×** (integer Q/E zoom). A whole proposed route cannot
   be framed at once, so I panned along it.
7. **Object cast members cannot speak or be pointed at.** `speakerActor` must be a player cast
   member: "Unknown dialogue speaker: moto". The Motobug uses `speakerName` instead and gets no
   tail pointer.
8. **The directed S1 Motobug declares no animation** ("animation: UNDECLARED"). The error is "Part …
   has no pure native animation 1". Its drive is a pose-key cycle every 8 frames, and each POSE key
   also resets its anchor x/y.
9. **Freezing a moving Motobug (PUPPET) leaves a ghost body.** Its exhaust smoke child renders the
   body frame. I placed the PUPPET key during its native ledge wait (frame 327), after the smoke
   has gone.
10. **Telemetry mislabels abilities.** `sample.world` reports S1 Sonic's ability as INSTA_SHIELD and
    S2 Tails' as FLY (`captures/t06/t06.sim.jsonl`). Neither exists in those games. I did not test
    whether they can be triggered.
11. **`MUSIC_STOP` at frame 0 does not silence S2 Emerald Hill's native level music.** In the stem
    render, the EHZ section measures −29.6 dB RMS, the same as the film with music, while the GHZ
    and AIZ sections drop to effects only. The promo never uses the EHZ stem.
12. **`GLIDE_TO` re-glides after arriving** unless a WAIT, STOP or RELEASE follows it.
13. **Tooling.** `FmSfxRenderTool --music` parses hex only: `45` failed and `2D` worked. The
    authoring guide and `moves.md` describe zoom differently.

## The staged archive

The gameplay-highlights skill requires an archive in OpenGGF-Media. As you asked, it is staged
locally in `archive/` and **not committed or pushed**:

- `archive/projects/stageplay-day-off-promo/` is the project directory, laid out like
  `time-attack-promo`.
- `archive/catalog-rows/` holds the rows to add to `catalog/{projects,roots,sources}.json` and
  `assets.csv`.

Delivery is therefore incomplete by the skill's definition: the archive is not published, and
`tools/catalog.py verify` has not run in the media checkout.
