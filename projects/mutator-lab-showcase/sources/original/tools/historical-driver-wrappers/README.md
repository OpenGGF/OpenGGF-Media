# Complete Mutator Lab showcase — recipe

1. Build (in the worktree, build-only): `python3 examples/example-mutators/build.py`.
2. Compile the scratch adapter: `javac --release 21 -cp "$W/target/classes:$(cat $W/target/mutators-classpath.txt)"
   -d tools/driver/classes tools/driver/src/com/openggf/tools/ShowcaseCapture.java`.
3. Shoot: `sh tools/finals.sh` (eleven display-free takes via `tools/cap.py`; `--paced` = interactive pacing).
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
