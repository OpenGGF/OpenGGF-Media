# Complete Mutator Lab showcase — recipe

1. Build (in the worktree, build-only): `python3 examples/example-mutators/build.py`.
2. For reproducing historical receipts only, compile the scratch adapter: `javac --release 21 -cp "$W/target/classes:$(cat $W/target/mutators-classpath.txt)"
   -d tools/driver/classes tools/driver/src/com/openggf/tools/ShowcaseCapture.java`.
3. Original source takes are retained; `tools/finals.sh` names those existing outputs and deliberately refuses overwriting. For a new take, use a fresh name via `tools/cap.py`. It now defaults to the retained PR checkout and maintained `MutatorGameplayCaptureTool --showcase`; `--paced` selects `--interactive-pacing`. Override `OPENGGF_PROMO_ENGINE_ROOT` for another compiled checkout. `--scratch-adapter` is the historical filming adapter; `tools/historical-driver-wrappers/` preserves the original wrapper/recipe.
   `tools/prefs.py` writes preference seeds; `tools/sweep.py` runs route variants 3 at a time;
   `tools/events.py` summarises observe/observe2 events. Read CSVs before frames (`tools/sheet.py`).
4. Edit: `python3 -I recipe/build_showcase.py [segment ids to re-render]` (ffmpeg only).
5. Verify: `python3 -I tools/verify_showcase.py` → `out/verify.json`; `tools/filmsheet.py` for frame review.

## Lessons / rejected attempts
- S1 GHZ1 positioned at (0x2342,0x458) dies instantly (fresh-load bottom boundary); (0x2100,0x370) works.
- AIZ starpost ledge needs y=0x250 at x=0x2740; x=0x2680 falls to the lower path.
- No Bonus Stages suppresses star spawn at the post itself (`shouldSpawnBonusStars`), so a deny take never logs a touch.
- Paced (keyboard) menus: P1_C is not "back"; use the "Back to mutators" row.
- `GameplayCaptureSession` renders SPECIAL_STAGE as level planes; the adapter adds Engine's stage draw order.
- Lab reopens at row 1; LOAD edits show "Pending restart or death".
- Holding Right from S1 GHZ1 start dies at the first Motobug with 0 rings; hop pattern breaks the ring monitor.

## Final edit and maintained method

The root edit adds twenty native frames to each stage-denial menu excerpt (`[106,146)`) so checked On is readable. Original cut/evidence: `out/review-r1/`; final video: 5,453 frames/90.883 seconds. Current `out/chapters.json` is the authority for source ranges and samples, and `out/verify.json` records the final bounded whole-video decode, 243 source-frame checks and offline PCM/alignment checks. No editorial speed change.

The maintained method is documented in `tools/media/README.md#mutator-gameplay-showcase-captures` in the engine checkout. Its default route remains canonical; showcase/pacing are opt-in. Matched source comparisons prove canonical 32 frames, 180 native 200% presentations, and 1,480 frames through natural S1 giant-ring entry reproduce the original CSV, PNG and PCM. Original adapter/input/prefs/receipt identity remains intact. Rebuild the checkout and Lab package before a fresh capture; no display or user audio device is used.

Root final verification used `tools/verify_final_edit.py` (Python with NumPy and Pillow): one bounded full decode supplies all sampled panels, then checks native PCM and twelve A/V windows. The original standard-library `tools/verify_showcase.py` is also retained. Generated segment/edit files can be rebuilt from the chapter recipe; final source takes are authoritative.
