# Revision2 media assembly

`assemble.py` reads the approved beat EDL, exact source metadata/CSV, and root-owned `source-selections.json`. It writes only revision2 media. The first reel and masters stay unchanged.

The implementation rounds absolute 171.107BPM /0.316s beat boundaries to60fps. Launch expands from4 to10beats (source19.8–23.3) and all later boundaries shift6beats; total4864frames /81.067s. FULL preserves400×224 at4×; PAIR/QUAD preserve the complete frame at944×528 using integer nearest then area filtering. Player-centred12-degree slices are reserved for visibly suitable recaps. FULL→QUAD retains the same running source while shrinking over6native frames. All source PCM is muted. HCZ2 is continuous until the endcard, with explicit editorial ROM cues and silence under the stinger.

Root copies/edits `source-selections.example.json` to `source-selections.json` and approves only actually visible/qualified effects. New rain, leak, bumper and ghosts cannot fall back to first-reel masters. Counts use explicit qualified flags, never labels alone. Vine is omitted because its take never grabs/swings; fallback HUDScale (or reviewed SpringLegs/Bunny) occupies that slot. Snake is moving-board footage, with0score and no food/win claim. Bright Afterimages appears only in disjoint11.2–12.6 and13.0–15.817 intervals; weaker crowd recaps are replaced. Bloominator appears in whole-frame grids, not player-centred slices.

- `python3 assemble.py plan --allow-pending`: metadata/interval validation and resolvedtimeline.
- `python3 layout_scout.py`: small Python/Pillow geometry/card scouts from retained new PNGs; stand-ins are explicitly prototypes, never final shot proof.
- `python3 assemble.py snapshot --shot N --frame F`: actual EDL frame, when the selected source PNGs still exist. Consumed old PNGs require a decoder; use admitted preview instead.
- `python3 assemble.py preview --shots8,10,12 --admission-worktree /lead/provided/worktree`: short960×540 moving geometry preview under the shared scheduler.
- `python3 assemble.py render --admission-worktree /lead/provided/worktree`: only after root source approval/native integration. Holds normal exclusive `maven_slot(kind=chaos-reel-encode,estimate=180)` and inherits its leaseFDs into child decoders/encoder. Frames stream directly into one video encoder; no fullRGB sequence is materialized. Two threads, bounded per-source reader caches. Root may alternatively import `normalized_plan`, `ShotRenderer`, `encode_video`, and `finish_audio` under its own lease, setting moduleLEASE/moduleINHERITED to that exact lease/hook. Do not nest leases.

`editorial-cues.json` may supply additional verified ROM cue files with time/gain/reason. No guessed bumper/shield/leak cue is automatically added. Gameplay sound effects are ROM SFX placed editorially at the frames where the engine shows each event; source gameplay audio is not used. Root owns actual event/ROM cue identity approval, final moving-cut review, loudness verification and delivery.

Current state: assembler syntax and13PNG layout/card prototypes checked; source inputs and final qualification remain pending. No full/revision2 video was encoded by this assembler pass. Actual final decode and renderedmovie evidence remain required.
