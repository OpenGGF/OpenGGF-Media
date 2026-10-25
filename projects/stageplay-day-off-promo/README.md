# Day Off: Stageplay introduction promo

Staged on 2026-10-24 and published to OpenGGF-Media on 2026-10-25, after the user approved v2.
Produced by Claude Opus 5.5 in `/home/farrell/Videos/OGGF/sp-promo-a`. Its `probe/` diagnostics were
excluded from the archive and deleted from the production folder at publication.

The delivered external promo is `out/day-off-stageplay.mp4`: 130.2 s, 1920x1080 at 60 fps,
H.264, AAC 256 kbit/s, -15.5 LUFS / -1.3 dBTP after encode, 12 chapters. The standalone film is
`out/day-off-film-1080p.mp4` (74.97 s). The first half is a staged Stageplay story (a Motobug
takes a day off through Sonic 1, Sonic 2 and Sonic 3 & Knuckles). The second half is offscreen
captures of the in-engine and desktop editors directing the same scene, including the route
planner's failed Walk plan, its "needs Run" advice and the checked loop route.

## Version 2 (current)

`out/day-off-stageplay-v2.mp4` (140.03 s, -15.2 LUFS / -1.4 dBTP, 12 chapters) and
`out/day-off-film-v2-1080p.mp4` (74.97 s): engine develop `81f25c89f`, OpenGGF-Editor main
`dd5ee43`, film take `scenes/t10.stageplay`. Built-in voices for every speaker (the Motobug as an
object speaker with a tail), logical facing, native loop priority, `stageplay ground` floors, and
a re-captured making-of in the redesigned editor (level position picker, voice form and presets).
The film's route is the one the editor applied. Edit: [edit_v2.py](sources/promo/edit/edit_v2.py);
capture driver [EditorCapture2.java](sources/promo/tools/EditorCapture2.java) run by
[v2_chain.sh](sources/promo/tools/v2_chain.sh). See the v2 sections of the director's note and
provenance. v1 below is preserved unchanged.

## Sources and authority (v1)

- [Director's note](sources/promo/DIRECTOR.md): idea, least-certain sections, viewer pass,
  limits and Stageplay rough edges. [Provenance](sources/promo/PROVENANCE.md): every shot,
  scene file, command and verification. [Treatments](sources/promo/TREATMENTS.md).
- [Final edit](sources/promo/edit/edit.py) (promo_kit; brief in its docstring) and the superseded
  [first cut](sources/promo/edit/edit-r1.py); [chapters](sources/promo/edit/chapters.txt).
- Rebuild: [run_edit.py](sources/promo/tools/run_edit.py) `render`, then
  [mux_final.py](sources/promo/tools/mux_final.py) (true-peak gain, chapters, mux).
- Capture tools: [EditorCapture.java](sources/promo/tools/EditorCapture.java) (display-free
  editor capture, in-engine HUD or desktop ImGui chrome) run by
  [capture_editor.py](sources/promo/tools/capture_editor.py); [sp.py](sources/promo/tools/sp.py)
  (StageplayTool launcher). Each capture's `events.json` is preserved.
- Scenes: [generator](sources/promo/scenes/build_scene.py), the final
  [screenplay](sources/promo/scenes/t06.screenplay.json) and [scene](sources/promo/scenes/t06.stageplay),
  the before-route and SFX-stem takes, the route plan, measured data, the voice and skins.
  Earlier takes (`take01`, `t02`-`t05`) are superseded.

## Engine references

OpenGGF `feature/ai-sp-promo-a` `0ba60490e` (632a5f8c3 + the Sonic 1 loop-plane route-probe fix,
unmerged); OpenGGF-Editor `feature/ai-sp-promo-a` `146e076`. Snapshot jar hash in
external-assets.json.

## External, not uploaded

[external-assets.json](external-assets.json) hashes the finished films, the lossless captures,
ROM-derived audio, the frame sequences (inventory hashes), native simulation telemetry, the
engine snapshot, superseded captures and the fonts. ROMs are never included.
