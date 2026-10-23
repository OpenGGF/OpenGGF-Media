# Provenance — OpenGGF Multiplayer Time Attack promo (ta-promo-a, 2026-10-23)

Final film: `out/openggf-multiplayer-time-attack-promo.mp4` (1920×1080, 60 fps, H.264 15.5 Mb/s,
AAC 256 kb/s 48 kHz, 81.8 s, 9 chapters, −14.9 LUFS integrated, −1.1 dBTP after AAC, LRA 2.4 LU).

## Source and setup (every capture)

- Engine: worktree `.worktrees/ta-promo-a`, branch `feature/ai-ta-promo-a` at **06cbd7316** (develop merge
  of Time Attack quality of life), clean tree for every capture (`captures/*/source-status.txt` empty).
  Built with `mvn -Dmse=off package -DskipTests` (bundles `time-attack-1.0.0.jar`) and
  `racing/server/build.py`.
- ROMs: the worktree's root `.gen` links; SHA-1 checked — S1 REV01 `69E10285…`, S2 REV01 `8BCA5DCE…`,
  S3&K `CFBF98C3…` (match AGENTS.md).
- Display-free: surfaceless EGL, `DISPLAY`/`WAYLAND_DISPLAY`/`LD_LIBRARY_PATH` unset, isolated cwd per
  capture, no desktop input, no speaker output. All input is synthetic key events or the BK2 movie fed to
  the capture's own `InputHandler`.
- Capture driver: **temporary, not committed** — `scripts/driver/openggf/racing/server/tools/
  PromoCapture.java` + `PromoPeers.java`, assembled from `TimeAttackCapacityVideoTool`,
  `TimeAttackLobbyVideoTool` and `TimeAttackVideoPeers`, compiled outside the repo
  (`scripts/driver/classes`) and run by `scripts/run-promo.sh`. It drives the real first boot →
  master title → Extras → Time Attack UI with key events, writes every presentation frame losslessly
  (FFV1 320×224, 60 fps), the live SMPS mix as 48 kHz PCM, and a per-frame `state.csv` (hero position,
  camera, every ghost's screen position/opacity, countdown digit, rank). Pacing is wall-clock 60 Hz
  because the relay's rate limits are wall-clock.
- **Every rival is a test client, not a person.** Rival "players" are authenticated loopback protocol
  clients (`RaceClient`/master relay) with fixture names and looks. In races their ghost streams replay one
  recorded ROM-backed GHZ1 route (`route/ghz1.route`, `TimeAttackRouteTool` from `ghz1_fullrun.bk2`
  row 840; 3230 poses) retimed by a cosmetic schedule; their finishes are synthetic. In lobbies their lobby
  presence replays the hero's own recent poses at fixed offsets/delays. Nothing they send changes the
  hero's simulation. The hero's race inputs are the maintained `ghz1_fullrun.bk2` movie (row 840 on),
  except where noted.

## Captures used (all under `captures/`)

| Capture | Mode / args | What it is | Peers / fixtures |
|---|---|---|---|
| `race-clean3` | `race … 75 clean intl 9` | Browse → relay room "Green Hill Sprint" → lobby (4 chat lines from peers in VI/RU/EL/KO) → round start → GHZ1 title card with room countdown → BK2 route to a **natural** signpost finish (frame 4553, rank 6/9, 0:53.66) → in-act results/standings → round end → vote (peers vote staggered, hero presses 2 at 6747) → Marble Zone 1 launches (title card 7473+). | 8 relay peers: Nguyễn Hoa (Emerald), Дмитрий (Crimson), Ωμέγα (Teal), 소닉팬 (Rose), Zoë Ñandú (Violet), 风之子 (Gold), Çağrı Öztürk (Azure), Łukasz (Silver). Schedule: no drift, offset = A·(sin(2πt/P+φ) − sin φ), A = 8…35 frames, P = 640…1160 frames (`PromoPeers.sourceFrame`). Room owner peer 0 sends the voted round. Hero: 疾風の刃, look Ember (`lookBase=06E`). |
| `race-death` | `race … 120 death intl 9` | Same room flow; the hero **holds Right from GO** and dies on the first Motobug with 0 rings (natural death, frame 1515), presses jump after 42 dead frames (skip, 1557), the act reloads with no title card, the fast-restart lead-in and **3-2-1** (digits at 1561/1621/1681), GO at 1741, then the BK2 route from row 840. Death → GO measured 226 frames = 3.77 s. | Same 8 peers; this take used the earlier swirl schedule *with drift* (offset += (0.012 + 0.006·(pair mod 4))·t, A = 18…60, P = 900…1580). Hero Ember. |
| `race-256` | `race … 75 clean bots 256` | Browser row "Full Capacity Time Attack 255/256", lobby "PLAYERS 1/128", title card "ROOM 256 PLAYERS GET READY", GHZ1 race with the HUD "AHEAD n / 252 SEEN", natural finish. | **Capacity test**: 255 relay protocol clients named "Capture Host"/"Bot NNN", stock look, original `GhostPackSchedule`. Hero "Capture Player", stock look. |
| `names-relay` | `namesrelay` | Relay room lobby (S1 lobby level = GHZ1 start). Hero hides the menu, walks to x≈0xF3 and jumps every 96 frames. | 8 relay peers (same names/looks) streaming **lobby presence** that replays the hero's poses at x offsets ±0x24…±0x90 with delays 6…30 frames growing with distance — the "ripple" is staged by this fixture. |
| `lobby-s3k-profile` | `lobby s3k profile` | Fresh profile: **first-run name prompt**, 疾風の刃 typed one code point every 14 frames (GLFW char path `MenuInput.handleCharEvent`), Enter; host LAN room for S3K → HPZ lobby level; PROFILE page: Left ×8, one press per 24 frames (one beat at 150 BPM), Classic → … → Ember, SAVE; ready, Enter hides the menu, run/jump, menu back, START ROUND → AIZ1 launch (Ember hero, title card, countdown). | 3 LAN peers (Nguyễn Hoa, Дмитрий, 소닉팬) whose lobby presence replays the hero's poses. Note: the saved look applies at the next run launch (AIZ), not to the already-running lobby character. |
| `lobby-s1`, `lobby-s2` | `lobby s1`, `lobby s2` | LAN room lobby levels (GHZ1 / EHZ1 start), ready, menu hidden, run, menu back, round start → race launch with title card. | 3 LAN peers as above; hero Ember from settings. |

Superseded/experimental (kept, not in the film): `captures/superseded/` — first lobby/race takes (violet
hero too close to stock blue; "Nguyễn Thị Hoa" truncated with an ellipsis by the 72-px nameplate limit),
`race-clean`/`race-clean2` (drifting pack left the finish empty), names line-ups v1/v2 (camera clamp
crowding; hero walked into the Motobug — the lobby's own fast restart then reloaded it).

## Edit list (output time → source)

| Output | Shot | Source |
|---|---|---|
| 0.00–2.62 | Cold open: pack at speed | race-clean3 2110–2266 (mid-race; shown first editorially) |
| 2.62–4.22 | GHZ1 title card, room panel ROOM 9 PLAYERS / GET READY (compositor push-in) | race-clean3 1228–1323 |
| 4.22–7.42 | GO, the pack bursts; line "RACE TOGETHER. LIVE." | race-clean3 1324–1515 |
| 7.42–13.82 | Title drop (flash, Big Ring SFX, compositor slam) over the race | race-clean3 1516–1899 |
| 13.82–16.22 | First-run name prompt, 疾風の刃 typed | lobby-s3k-profile 563–706 |
| 16.22–23.42 | Name line-up (8 scripts), jump ripples; language callouts | names-relay 1159–1590 |
| 23.42–26.62 | Pack with nameplates | race-clean3 2100–2291 |
| 26.62–30.62 | PROFILE presets on the beat → Ember | lobby-s3k-profile 1312–1551 |
| 30.62–33.82 | Split: Ember hero at S1 GHZ1 / S2 EHZ1 / S3K AIZ1 race starts | lobby-s1 1780+, lobby-s2 1700+, lobby-s3k-profile 2405+ (≈190 frames each) |
| 33.82–40.22 | HPZ lobby: menu → ready → menu hides → play with ghosts | lobby-s3k-profile 1682–2065 |
| 40.22–45.82 | Three lobby levels in cells | lobby-s1 1165+, lobby-s2 1095+, lobby-s3k-profile 1800+ (336 frames each) |
| 45.82–55.42 | Death on 0 rings, skip, reload, 3-2-1, GO; "BACK IN" timer (measured) | race-death 1357–1932 |
| 55.42–57.02 | Browser row 255/256 (labelled CAPACITY TEST) | race-256 ≈700–795 |
| 57.02–61.82 | 256-player room race start; counter "256 / 255 TEST CLIENTS + 1 PLAYER" | race-256 1199–1486 |
| 61.82–68.22 | Run-in to the signpost with the pack; "YOU" tag | race-clean3 4169–4552 |
| 68.22–71.02 | Photo finish, HUD "YOU 6/9 … NEW BEST" (compositor push-in) | race-clean3 4553–4720 |
| 71.02–73.02 | In-act standings panel (5. 风之子 0:53.63 / 6. 疾風の刃 0:53.66) + "0.03s" | race-clean3 5600+ |
| 73.02–74.62 | Vote tally | race-clean3 6685+ |
| 74.62–76.22 | Marble Zone 1 title card with room countdown | race-clean3 7528–7623 |
| 76.22–81.82 | End card over blurred Marble Zone | race-clean3 7700+ |

All gameplay plays at recorded speed (one capture frame per output frame); there is no freeze or
retiming. Compositor camera moves (push-ins, slam, punches) are editorial; source frames are untouched.

## Editorial graphics and sound (staged / added in the edit)

- Every title, header, label, the "YOU" tag, timers and counters are editorial overlays drawn with the
  engine's own `NameFont` glyphs (dumped 1:1 by `scripts/driver/promo/NameplateDump.java`, plate colour
  `#101828`/0xD8 from `GhostRenderer`, name colours by `PlayerAppearance.nameArgb`). The "BACK IN" timer
  counts the measured 226 frames from the death frame to GO; "0.03s" is the difference of the two
  standings times on screen; "256" is the room size shown by the game's own browser/title card.
- Music: S3K Azure Lake (`$20`) rendered from the user's ROM by OpenGGF's `FmSfxRenderTool`, 150 BPM,
  first beat 0.21 s (onset fit), one bed, no clip audio. Stingers (ROM SFX via `FmSfxRenderTool`):
  S3K ring/big ring/starpost/jump/dash/register, S1 ring/death/signpost — editorial punctuation placed on
  the real in-game events (GO, death, digits, finish) or on graphic pops; they are not a recording of
  the game's audio.
- Honesty line on the end card: "Rivals shown are test clients replaying recorded runs. 256-player
  room: capacity test." The 256 chapter carries a CAPACITY TEST tag and "255 TEST CLIENTS + 1 PLAYER".

## Reproduce

```
scripts/run-promo.sh <capture> <mode> …     # see captures/*/args.txt (classes = scripts/driver/classes)
python3 edit/prep.py                          # extract the used frame ranges (edit/build/clips)
PROMO_FONT_DIRS=fonts <venv>/python <OpenGGF>/tools/media/promo_kit.py render edit/edit.py
edit/finalize.sh                              # loudnorm, chapters, faststart -> out/
```

Note: the driver evolved during the session; `race-death` was taken with the earlier drift schedule
(formula above). The final driver reproduces every other capture.

## Observations about the feature (not changed — engine/mod code was out of scope)

- The lobby vote panel shows the header and only **two of the three** options:
  `RaceLobbyView.drawHistoryOrVote` takes `lines.subList(0, 3)` of `voteLines`, which already includes
  the header line. The film shows the two visible options and makes no "three tracks" claim.
- A look saved on the PROFILE page in a lobby recolours the player's character from the next run launch;
  the lobby character keeps the old look until then.
- The first-run name prompt's hint is cut by the 320-px screen ("Other racers see it. Any sc…").
- LAN hosts accept 4 connections per address (`JdkHostLimits.DEFAULT_MAX_CONNECTIONS_PER_IP`), so a
  loopback capture can only host 3 LAN peers; larger fixture rooms must go through the master relay.

## Audio revision (2026-10-23, after user listening review)

User heard: music far louder than SFX, no PCM drums, ring stuck on the right channel.
- PCM: `FmSfxRenderTool` renders through the legacy physical policy with direct reads, so the S3K
  idle-loop DAC enable (`2Bh=80h`, Z80 Sound Driver.asm:4264-4276) is never written. 0 enables in
  `music/s3k-20/*-ym-writes.txt`. The bed is now `music/live/s3k-music-20-live.wav` from
  `scripts/driver/audio/LiveMusicRender.java` (production-paced `LiveSceneMusic`, game policy):
  126 enables and 277,042 DAC bytes in 30 s (`DacProbe.java`); FM6/DAC alone measured at −32.7 dBFS.
  It is delayed 800 samples (one frame) to match the fitted beat grid (cross-correlation lag).
- Ring: S3K alternates Sound33/34 through `zRingSpeaker` (:1919-1925); the edit used 33 only.
  Rings now alternate 33/34. The S1 ring tick ($B5, right-only in S1) is downmixed to centre.
- Balance: bed gain 1.0 → 0.75; every stinger ×2.2 (capped at 1.0), about +9 dB relative.
- Re-mastered with `edit/finalize.sh`: −15.0 LUFS, −1.3 dBFS peak. Picture unchanged.
  Original kept as `edit/build/render/promo-v1.mp4`; previous edit as `edit/edit.v1-audio.py`.

## Picture and cue revision (2026-10-23, second listening review)

- Colour split, S1 pane: the camera clamped at the level's left edge, so the slice showed x≈83-166
  while Sonic stood at x≈80. The pane now centres on him over a padded frame and starts at capture
  1797, after the GHZ title card clears. Split labels drop to scale 4 so S3K's fits its pane.
- Name-entry ticks now land on each glyph's first frame (623 + 14k, clip-measured); they were 36 frames early.
- Jump sounds only on the hero's real take-offs (state.csv y): S1 jump $A0 at names-relay 1273/1369/1465/1561,
  S3K jump $62 at lobby-s3k-profile 1789/1879. A had them on the beat (≈31 frames late, on the apex) and
  one editorial hit on the lobby header. GO hits moved from 2 frames early to exactly GO.
- Language callouts: scale 4, white text with the rival's colour bar, laid out so none touch, entering once
  the line-up has settled (b46-b54) instead of while the pack walks in.

## New lobby UI revision (2026-10-23, after the race lobby redesign, develop 3d23cab3f)

The race lobby was redesigned as cards over the lobby level (commit 49cfd5fc2). Only two shots showed
the lobby UI, so only their sources were re-captured with the same driver (`scripts/run-promo-newui.sh`,
ROOT .worktrees/ta-lobby-gui at 49cfd5fc2): `lobby-s3k-profile-newui` (Hidden Palace lobby; +5 frames
after the lobby load against the original take) and `race-clean3-newui` (standings, vote, next card and
end card; +3 frames). Edit constants moved with them: HIDE 1783, take-offs 1794/1884, lobby row 1805,
standings 5603, VOTE0 6548+140, NEXT_CARD 7531, END_SRC 7703. The vote shot now crops the lobby's vote
card (native 4,152 167x53), which shows all three tracks. The Hidden Palace shot frames the top of the
screen while the cards are up, so the header card stays whole, then eases down when the menu hides.
Every other shot keeps its original capture. Unused new takes of lobby-s1, lobby-s2 and names-relay
are in captures/superseded/*-newui-unused; the replaced originals stay in place for the other shots.

## Editorial type revision (2026-10-23)

User: "sometimes the text and display used e.g 'no more lives go again' is exactly the same as the hud
style. So I don't know if the promo is talking to me, or the game displays that text in normal play."
Every editorial caption, header, counter, the title's MULTIPLAYER/TIME ATTACK/OpenGGF and the end card now
use Fira Sans Extra Condensed Black Italic with a navy stroke and hard shadow (`editorial()` in edit.py);
labels (languages, YOU, game names, CAPACITY TEST) are pills, the language pills in each player's colour.
Player names, the typed name and all captured game UI keep the engine's name font. Previous edit kept as
edit/edit.v4-hudtype.py.

## Re-capture and race HUD revision (2026-10-23, develop 62521a43a then f829713b1)

The precise timer (one TIME row with hundredths) and the full-width progress bar replaced the TA panel's
duplicate TIME, so every source was re-captured into `captures-v3/` with `scripts/run-promo-v3.sh`
(ROOT .worktrees/ta-promo-capture). `captures/<name>` now links each take there; `edit-chapters.csv`
keeps the chapters the edit's frame constants were written against, and `edit/capmap.py` shifts every
source frame by the per-chapter delta to the new take (lobby-s3k-profile 0..4, lobby-s1 +2, lobby-s2 +16,
names-relay −1, race-clean3 0..2, race-death 0, race-256 1..2 before the stack-cap re-take). The race
takes were taken again at f829713b1, after progress-bar columns were capped at five segments under a
count, so the 256-bot chapter no longer stacks up the screen. Race shots frame at native y 94 so the new
top TIME row stays whole in the 16:9 crop; the S2 split pane re-centres on Sonic (user: "Sonic 2 sonic
is off-centre"), the S1 pane stops just above the progress bar, and all three game labels sit below the
heroes' feet; the standings crop moved with the HUD. A 256 room's TA panel runs to native row ~51 and
the bar starts at ~205, so no 16:9 crop shows both whole: the capacity shot is now the whole native
screen on the stripe ground, with the CAPACITY TEST pill and the 256 count beside it, above the bar. Previous edit kept as
edit/edit.v5-before-recapture-framing.py.
