# sp-promo-a status (checkpoint, 2026-10-24)

## v2: done

- Deliverables:
  - `out/day-off-stageplay-v2.mp4`: 140.03 s.
  - `out/day-off-film-v2-1080p.mp4`: 74.97 s.
  - v1 files are unchanged. Notes are in the v2 sections of `DIRECTOR.md` and `PROVENANCE.md`.
- Engine:
  - `feature/ai-sp-promo-a` was fast-forwarded to develop `81f25c89f`. There are no new engine
    commits.
  - Snapshot jar: `engine/openggf-sp-promo-a-r2.jar` (sha256 `9ead2ed9…`).
  - OpenGGF-Editor worktree: origin/main `dd5ee43`, merged by fast-forward.
- Film:
  - Take `scenes/t10.stageplay`, made by `scenes/build_scene.py` (v1 generator kept as
    `build_scene_r1.py`).
  - Floors come from `stageplay ground` (`probe/ground`).
  - The route comes from the editor's applied scene (`captures/v2/editor-route`).
- Captures:
  - Made with `tools/EditorCapture2.java` via `tools/v2_chain.sh`, from the neutral scene folder
    `/tmp/stageplay`.
  - Editor export equals the CLI render; the screenplay round trip is byte-identical; the
    desktop and in-engine applied scenes are byte-identical.
- Edit: `edit/edit_v2.py`. Rebuild with `tools/run_edit.py render edit/edit_v2.py`, then
  `tools/mux_final.py edit/edit_v2.py --chapters v2`.
- New rough edges are listed in `DIRECTOR.md` v2: the S2 entry-frame music fade, S2 sound-ID
  numbering, repeated route details, the advice depending on attempt frames, and the truncated
  route sentence.
- No pushes or merges.

## v1 (kept)

- Promo `out/day-off-stageplay.mp4` and film `out/day-off-film-1080p.mp4`.
- Engine fix `0ba60490e` (Sonic 1 loop planes in the route probe), now merged on develop.
