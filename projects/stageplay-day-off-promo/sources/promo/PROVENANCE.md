# Day Off: provenance

## Version 2 (`out/day-off-stageplay-v2.mp4`, `out/day-off-film-v2-1080p.mp4`)

- **Engine.** OpenGGF `feature/ai-sp-promo-a` fast-forwarded to develop `81f25c89f` (it
  contains the v1 loop-plane fix). The snapshot jar is `engine/openggf-sp-promo-a-r2.jar`, SHA-256
  `9ead2ed9ed9035bffd629f99c5c2183fabd8ae3a02b14f29797304ea1095486a`. `tools/sp.py` now defaults
  to it; v1 used `-r1.jar`.
- **Desktop editor.** OpenGGF-Editor at `dd5ee43` (origin/main merged), compiled against that
  engine through its private repository.
- **The film.** `scenes/t10.screenplay.json` compiles to `scenes/t10.stageplay` (screenplay v7,
  canonical v8), made by `scenes/build_scene.py`; `build_scene_r1.py` is the v1 generator.
  Variants:
  - `t10-editor` (`--no-route`): the scene before Sonic's route, used by the route captures.
  - `t10-sfx` (`--no-music`): the effects and voices stem.
  - `t10-novoice` (`--voices-off`): a measurement take only.
- **Superseded takes.** `t07`–`t09` and `v2a`/`v2b`. `t07` used the wrong S2 music ID; `t08`
  had the S2 entry-frame fade; `t09` had the 621 route.
- **Floors.** `scenes/ground-floors.json` comes from `stageplay ground` (`probe/ground/*.json` and
  their `*.out.json`): one JVM per set (s1/0/0, s2/0/0, s3k/0/0), run sequentially, with an
  object footprint of 8 / 28 / 14 on path 0.
- **Route.** `scenes/routes/loop-route-v2.json` holds the three commands the in-engine editor
  applied (MOVE_TO 5860, 620 at 844; STOP at 1111; FACE_LEFT at 1119), taken from
  `captures/v2/editor-route/route-applied.stageplay`.
- **Voices.** The engine's built-in PSG defaults; the scene has no `voices` overrides. v1's
  `voice/*.wav` clips are retired.
- **Renders** (`captures/v2/`, cwd `scenes/`):
  - `../tools/sp.py render --scene t10.stageplay --out ../captures/v2/t10-preview.mkv`; add
    `--scale 4` for `day-off-v2-film-1080p.mkv`.
  - `render --scene t10-sfx.stageplay` produces `t10-sfx.mkv`.
  - `simulate --every 1` produces `t10.sim.jsonl` (native telemetry);
    `edit/film-camera-v2.json` is extracted from it and matches v1's camera on every frame.
  - `timeline --every 1` produces `t10.timeline.jsonl`, the authored timeline with the 103
    `speech` events.
- **Editor captures.** All use `tools/EditorCapture2.java`, run as
  `tools/capture_editor.py SCRIPT /tmp/stageplay/day-off.stageplay OUT --tool EditorCapture2.java`
  (plus `--desktop` for the desktop capture), driven sequentially by `tools/v2_chain.sh`. The
  neutral scene folder `/tmp/stageplay` keeps home paths off screen.
  - `editor-route/route.mkv` (in-engine): Plan route form, level picker (5860, snapped to 620),
    Advanced attempt frames 419, Walk failure, Details, Plan another route with the same point
    re-picked, Run/Hard/Left, the checked line, Apply, Play.
  - `editor-tour/tour.mkv` (in-engine): scene list, cast, Free/Puppet playback, Puppet key form
    with Facing, world commands, camera key, push-in, Sonic's line form, the Motobug's voice form
    and the voice presets, the Motobug's reply, export screenplay, import, and Export film. The
    film export is `editor-tour/day-off.mkv` and the screenplay export is
    `editor-tour/day-off.screenplay.json`.
  - `editor-desktop-route/desktop-route.mkv` (desktop chrome): the same request (5860, 620,
    Run/Hard/Left), Apply, Play.
- **Edit.** `edit/edit_v2.py`. The frames are `edit/frames/{film,route,tour,desktop-route}-v2`;
  the audio is `audio/film-v2.wav`, `film-sfx-v2.wav` and `rewind-v2.wav`, plus v1's
  Competition Menu and GHZ beds. Rebuild with `tools/run_edit.py render edit/edit_v2.py`, then
  `tools/mux_final.py edit/edit_v2.py --chapters v2`.

### v2 verification

- **Editor export.** The editor's Export film (`editor-tour/day-off.mkv`) has video and audio
  stream MD5s identical to the CLI render `t10-preview.mkv`, built-in voices included.
- **Screenplay round trip.** Compiling the editor's exported screenplay gives a file
  byte-identical to `t10.stageplay`.
- **Two editors.** The in-engine and desktop applied scenes are byte-identical. The film's route
  commands equal them.
- **Sonic's route.** The new route stops Sonic at (5856.34, 620.64), as in v1.
- **Motobug patrol.** Native Motobug, then PUPPET from frame 327, then POSE from 790, with the
  same native turn and edge frames as v1 (106, 299).
- **Loop priority.** Visual check of `t10`/`v2b` frames 862–946: the Motobug crosses the loop's
  inner bottom, is hidden behind the front pillar (fully hidden around frame 910) and emerges
  facing right.
- **Preview frame mapping.** Push-in tour 1685+k is scene 350+k, reply tour 2629+k is scene
  1280+k, route 2210+k is scene 840+k, and desktop 383+k is scene 840+k. All are exact apart from
  overlays.

### v2 shot list (promo)

| Out | Source | Notes |
|---|---|---|
| 0:00.00–1:01.63 | film-v2 0–3697 | The film (t10) |
| 1:01.63–1:05.38 | composed and tour-v2 0–224 | Pull-back, title, rewind |
| 1:05.38–1:11.57 | tour-v2 250–623 | Scene list; cast push-in |
| 1:11.57–1:17.47 | tour-v2 624–842, 1142–1276 | Free/Puppet playback; Puppet key form (Facing callout) |
| 1:17.47–1:23.67 | tour-v2 1326–1444, 1565–1682, 1688–1822 | World commands; camera key; push-in (brackets from `film-camera-v2.json`) |
| 1:23.67–1:29.28 | route-v2 83–419 | Plan route form, level picker, floor snap |
| 1:29.28–1:38.02 | route-v2 614–799, 890–1058, 1404–1572 | Walk failure; Details ("needs Run" callout); Run/Hard/Left |
| 1:38.02–1:45.05 | route-v2 1590–1893, 2092–2209 | The checked line; Apply |
| 1:45.05–1:51.80 | route-v2 2250 ∥ desktop-route-v2 423, then film-v2 1090–1284 | Both editors, then the film |
| 1:51.80–1:59.67 | tour-v2 1985–2102, 2306–2440, 2452–2552, 2632–2749 | Line form; Motobug voice; presets (Patrol Buzz callout); "Day off." in the preview |
| 1:59.67–2:04.73 | composed; tour-v2 3008–3108 | Screenplay excerpt (real export values); Export film |
| 2:04.73–2:13.03 | film-v2 4000–4497 | Epilogue |
| 2:13.03–2:20.03 | composed | End card |

---

## Version 1

Production directory: `/home/farrell/Videos/OGGF/sp-promo-a` (paths below are relative to it).

## Software and inputs

- **Engine.** OpenGGF `feature/ai-sp-promo-a` at `0ba60490e`. That is `632a5f8c3` plus the
  `Sonic1LoopManager` route-probe fix and its ROM test. All renders, simulations, route plans and
  in-engine editor captures ran from one snapshot jar built from that source:
  `engine/openggf-sp-promo-a-r1.jar`, SHA-256
  `ae173e3165ae9c4a84fe2ffe527d4b46d494bc07b8f8e1e72963887d59d5264f`.
- **Desktop editor.** OpenGGF-Editor `feature/ai-sp-promo-a` at `146e076`, unchanged. Its compiled
  classes and its private-repository imgui-java 1.92.7.1 jars provided `ImGuiEditorChrome` for the
  desktop captures.
- **ROMs.** User-supplied and verified:
  - S1 World REV01, CRC32 `AFE05EEE`
  - S2 World REV01, CRC32 `7B905383`
  - S3&K, CRC32 `63522553`

  All runtime art and sound come from them through the engine's ROM pipeline.
- **Capture environment.** Everything was captured offscreen on surfaceless EGL, with `DISPLAY` and
  `WAYLAND_DISPLAY` removed and offline audio. The tools were `tools/sp.py` (StageplayTool) and
  `tools/capture_editor.py` (which runs `tools/EditorCapture.java`). There was no desktop input and
  no speaker playback.

## Stageplay scene files (authored)

| File | What it is |
|---|---|
| `scenes/build_scene.py` | Generator for every take (story, blocking, dialogue, cues) |
| `scenes/t06.screenplay.json` → `scenes/t06.stageplay` | **The film.** Screenplay v6 compiled to canonical v7. 4498 frames, 480×270, 6 shots |
| `scenes/t06-editor.stageplay` | The same film with Sonic's loop-shot route removed (`--no-route`). It is the "before" scene both route captures start from |
| `scenes/t06-sfx.stageplay` | SFX/voice stem take (`--no-music`). Authored ROM music is replaced by `MUSIC_STOP` |
| `scenes/routes/loop-route.json` | The route helper's verified plan for the loop (MOVE_TO 5860,621; Walk start, Run, Hard stop, Left) |
| `scenes/measured.json` | Measured native data used for blocking: patrol edge/turn frames, floors, Knuckles' glide |
| `scenes/voice/*.wav`, `cues.json`; `scenes/make_voice.py` | The Motobug's synthesized voice. It is original procedural audio, not from a ROM or a voice service |
| `scenes/decor/*.png`; `scenes/make_decor.py` | Original 9-slice dialogue skins |
| `captures/editor-tour2/scene/day-off.stageplay` | The scene the tour opened. Byte-identical to `t06.stageplay` |
| `captures/editor-tour2/scene/day-off.screenplay.json` | The in-engine editor's screenplay export of that scene |
| `captures/editor-tour2/scene/roundtrip.stageplay` | That export, imported back. **Byte-identical to `t06.stageplay`** |
| `captures/editor-r2/route-applied.stageplay` | The scene the in-engine editor saved after Apply |
| `captures/desktop-route/desktop-route-applied.stageplay` | The scene the desktop editor saved after the same request. **Byte-identical to the in-engine file** |

`captures/t06/t06.sim.jsonl` is the **native world simulation telemetry** for the film:
`simulate --every 1`, kind "native shared live-world gameplay", 4498 samples. It is not an
authored timeline. `edit/film-camera.json` is its per-frame camera, extracted for the camera-key
graphic. Native events it confirms, which the film shows:

- The Motobug's Free patrol: the native `Sonic1MotobugBadnikInstance`, with its smoke children,
  runs until frame 326.
- The PUPPET hold: from frame 327 the object is `Stageplay:moto:PUPPET`.
- POSE keys: from frame 790 the object is `Stageplay:moto:POSE`.
- Knuckles' native glide: abilityState 1 from frames 2658–2733, landing slide 2733–2748, landed at
  2748.
- Sonic's route: 5501,550 at frame 1009, then 5840,621 at frame 1100, then stopped at 5856,621.

## Renders and captures (all lossless)

| File | Command (cwd `scenes/` unless noted) | Notes |
|---|---|---|
| `captures/t06/t06-preview.mkv` | `../tools/sp.py render --scene t06.stageplay --out ../captures/t06/t06-preview.mkv` | FFV1 480×270 + FLAC. Source of all film frames in the promo |
| `captures/t06/day-off-film-1080p.mkv` | the same with `--scale 4` | Pixel-identical to nearest ×4 of the 1× render. Source of `out/day-off-film-1080p.mp4` |
| `captures/t06/t06-sfx.mkv` | `render --scene t06-sfx.stageplay` | Audio-only use: `audio/film-sfx.wav` |
| `captures/t06/t06.sim.jsonl` | `simulate --scene t06.stageplay --every 1` | Telemetry (above) |
| `captures/editor-r2/route.mkv` (+ `.events.json`) | `tools/capture_editor.py route scenes/t06-editor.stageplay captures/editor-r2` (cwd production root) | In-engine HUD editor, 1920×1080, 60 fps. The route session |
| `captures/editor-tour2/tour.mkv` (+ events) | `tools/capture_editor.py tour captures/editor-tour2/scene/day-off.stageplay captures/editor-tour2` | In-engine HUD editor. The tour, ending with Export film |
| `captures/editor-tour2/day-off.editor-export.mkv` | Written by the editor's own **Export film** during the tour | Video and audio stream MD5s identical to `t06-preview.mkv` (re-checked 2026-10-24) |
| `captures/desktop-route/desktop-route.mkv` | `tools/capture_editor.py --desktop desktop-route scenes/t06-editor.stageplay captures/desktop-route` | OpenGGF Editor (desktop chrome). The same route request |
| `captures/desktop-tour/desktop-tour.mkv` | `--desktop desktop-tour …` | Captured but **not used** in the promo |

Edit frames: `edit/frames/{film,route,tour,desktop-route}` are frame-exact PNG decodes of the four
captures above (film from `t06-preview.mkv`).

Each editor capture's `events.json` lists every scripted step with its output frame, scene frame
and the editor's status line. The scripts drive the editors through the same workspace calls as
their key and menu handlers. Text is typed into fields through the input handler's code-point path.

## Audio sources

| File | Source |
|---|---|
| `audio/film.wav` | The film's own soundtrack (from `t06-preview.mkv`): ROM music cues, native SFX from the shared world, and the VOICE cues |
| `audio/film-sfx.wav` | The stem take's soundtrack. Used only under GHZ editor playback, where it is effects and voice only (see rough edge 11 for EHZ) |
| `audio/s3k-music-2d-paced.wav` | `FmSfxRenderTool --music 2D --paced` (S3K Competition Menu, 106.634 BPM, first beat 0.556 s), from the S3K ROM's driver |
| `audio/s1-music-81-paced.wav` | `FmSfxRenderTool --music 81 --paced` (S1 Green Hill). Placed so it continues the film's own GHZ cue from frame 4018 |
| `audio/rewind.wav` | The film's last 5 s before frame 3698, reversed, ×4, low-passed at 7 kHz |

## Shot by shot (promo `out/day-off-stageplay.mp4`)

"Authored" means directed in Stageplay: the scene's keys, cues, routes and commands. Everything
inside the film is a staged performance in real levels, not ordinary gameplay. The physics,
collision, badnik AI before the PUPPET key, and Knuckles' glide are the native engine.

| Out (s) | Kind | Source (frames) | Game / set | Notes |
|---|---|---|---|---|
| 0.00–61.63 | Film | film 0–3697 | S1 GHZ1 → S2 EHZ1 → S3K AIZ1 → S3K AIZ1 ledge | Authored story. Its in-film title cards, transitions and dialogue are Stageplay's. Editorial: "DAY OFF / A STAGEPLAY FILM" title at 14.0 s |
| 61.63–62.63 | Composed | film 3698 shrinking onto tour 0–59 | — | The pull-back. The paused editor shows the same frame (tour 0–149 hold scene frame 3698) |
| 62.63–64.13 | Composed | tour 60–149, darkened | — | Product title (editorial) |
| 64.13–65.38 | Editor | tour 150–224 | in-engine HUD | The editor scrubs back to frame 0 |
| 65.38–69.32 | Editor | tour 258–493 | HUD | Scene changes / transitions list |
| 69.32–71.57 | Editor | tour 494–628, push-in to 2.15× on the cast panel | HUD | Cast |
| 71.57–75.22 | Editor | tour 629–847, preview at 2× | S1 GHZ1 in the preview | Patrol playback, scene 225–446 (playback from scene 225 at tour 629). The FREE/PUPPET switch is editorial and flips at scene 327 |
| 75.22–77.20 | Editor | tour 1062–1180 | HUD | Object mode keys |
| 77.20–79.72 | Editor | tour 1386–1536 | HUD | World commands |
| 79.72–81.70 | Editor | tour 1578–1696 | HUD | Camera key form, frame 439 |
| 81.70–83.95 | Editor | tour 1700–1834, preview at 2× | GHZ1 | Push-in playback, scene 353–487. Brackets are editorial, computed from `film-camera.json`. Film SFX stem from scene 353 |
| 83.95–87.32 | Editor | route 312–513 | HUD | Route form at Walk |
| 87.32–90.70 | Editor | route 516–718, push-in to 2.2× on the panel | HUD | The planner's failure and its reason. The "needs Run" box is editorial |
| 90.70–93.78 | Editor | route 1195–1379 | HUD | Run / Hard Stop / Left |
| 93.78–98.85 | Editor | route 1393–1696, zoom to the 2× preview | HUD | The proposed, natively checked line, panned by the editor's camera mode |
| 98.85–100.83 | Editor | route 1795–1913 | HUD | "Check inputs and apply route", then "Route applied" |
| 100.83–104.33 | Split | route 1954–2163 ∥ desktop-route 752–961 | both editors | Both play the applied scene, scene 880–1089. The split stays visible under the wipe until 104.77 |
| 104.33–107.58 | Film | film 1090–1284, wiped in left to right over 26 frames | GHZ1 | The same moment in the finished film. Film SFX stem from scene 880 under the whole split + film shot |
| 107.58–109.83 | Editor | tour 2034–2168 | HUD | Sonic's dialogue line form. The box is editorial |
| 109.83–113.20 | Composed | blurred film 1190 + typed panel | — | Editorial rendering of a real excerpt of `day-off.screenplay.json` (values read from the file) |
| 113.20–114.90 | Editor | tour 2680–2781 | HUD | Export film form |
| 114.90–123.20 | Film | film 4000–4497 (20-frame crossfade in) | S1 GHZ1 | The film's epilogue |
| 123.20–130.20 | Composed | blurred film 4497 | — | End card (editorial). GHZ continues from the film's cue |

Editorial elements are compositor graphics, not Stageplay output:

- titles and captions;
- the FREE/PUPPET switch;
- the camera-key brackets and tag;
- the callout boxes;
- the editor-name chips and the FILM chip;
- the screenplay panel and the end card.

## Verification record

- **Route.** The film's loop-shot route commands are the same three commands both editors
  applied (`route.move.0` MOVE_TO at 844, `route.stop.0` at 1111, `route.face.0` at 1119). The
  two editors' saved scenes are byte-identical (`cmp`).
- **Round trip.** Screenplay export and re-import gives a byte-identical canonical scene.
- **Export.** The editor's Export film output matches the CLI render (video/audio MD5s).
- **Frame matching.** Editor preview frames match film frames: tour 1697+k is scene 350+k with
  0.0 mean difference, and route 1914+k is scene 840+k (residual is only the route overlay).
  Patrol playback: tour 632+k is scene 225+k (residual 1.6/255, which is the selection overlay).
- **Promo file.**
  - Format: 130.200 s, 7812 frames at 60 fps, 1920×1080, H.264 yuv420p (BT.709), AAC 48 kHz
    stereo at 256 kbit/s, 12 chapters, fast start. Full decode `ffmpeg -v error -xerror …`
    exited 0.
  - Audio after the AAC encode: −15.5 LUFS integrated and −1.3 dBTP. Sections: film −15.0,
    title −15.2, making-of −16.3, epilogue −13.5, end card −18.5 LUFS.
- **Film file.** 74.967 s, 4498 frames, 6 chapters, full decode exited 0, −16.7 LUFS and
  −1.5 dBTP.
- **Rebuild.**
  1. `tools/run_edit.py render edit/edit.py` (video, niced, x264 capped at 6 threads).
  2. `tools/mux_final.py edit/edit.py` (true-peak gain, chapters, mux).

  Both run with the venv at `.worktrees/sp-promo-a/target/promo-venv`. `edit/edit-r1.py` is the
  superseded first cut.
