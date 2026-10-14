# DDZ bring-up media (feature/ai-ddz-bring-up)

Reel: `reel/ddz-bring-up-highlights.mp4` (96.9 s, 1920x1080/60, silent, 13 chapters). Rebuild: `python3 reel/build_reel.py`;
edit list and chapter map beside it. Clips: `sh make_clips.sh` (sources and frame ranges inside).

| Source | Commit | Setup | Status |
| --- | --- | --- | --- |
| `raw-00-baseline-before-work` | `832554260` | DDZ cold load, no Doomsday code; Sonic falls and dies | baseline |
| `raw-01-controller-first` | `6145ccce3` | first controller capture | superseded |
| `raw-10-seeded-route-320` | `42653d028` | GameplayCaptureTool, Sonic, 7 Super Emeralds, complete-run BK2 from movie 514214, `--settle 1`, `--vint-run-count 512489 --camera-x-sub 0x2700` (seeded diagnostic entry); exact to native rows 1-10058 | superseded (no boss explosions) |
| `raw-11-seeded-route-320-explosions` | `42653d028` + explosion art | same | superseded (bombs culled on wrap) |
| `raw-14-seeded-route-320-final` | `bf9cf7f7b` | same; exact to native rows 1-10058; `$D01` load at 10080 | superseded (boss chunks in the asteroid field, extra defeat cluster, dark phase-2 jets) |
| `raw-12-seeded-route-800` | `42653d028` | same input at 800 px; diverges from native (wider load windows), rings out and dies at 6340 | superseded (predates explosion art) |
| `raw-17-seeded-route-320-visual-fixes` | `92c1abba0` | same seeded route; exact to native rows 1-10058 | final (clips 00-11, 20, 30-33) |
| `raw-18-seeded-route-800-visual-fixes` | `92c1abba0` | 800 px, frames 3400-3999 | final (clip 40) |
| `native/pass1`, `native/probe-*` | — | BizHawk 2.11 native, `tools/bizhawk/capture_ddz_route_reference.lua`; `probe-vid-*` every frame for side-by-sides; `probe-slots*` slot histories | native reference |

Engine frame f corresponds to native movie frame 514214 + f. No audio captured.
A discarded S2-donor Tails capture started at a wrong position (capture-tool donor re-registration); not used.

## Incoming DEZ2 completion — 2026-09-23

campaign-20260923-incoming-dez2-completion-800/capture.mp4: replay all31531inputs from positioned DEZ2 boss through the final arena and both DDZ phases; film30000..31530. Zero deaths/followers,7finalrings; full decode passed; stills30369/31291/31530 inspected (last is white exit fade). Only initial200rings/sevenSuperEmeralds declared; no reseed at either load. Input/provenance alongside. Not cold DEZ2 or native parity.
