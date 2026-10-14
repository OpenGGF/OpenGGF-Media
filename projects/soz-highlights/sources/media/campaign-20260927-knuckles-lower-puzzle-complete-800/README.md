# SOZ2 lower puzzle — knuckles, 800px

Source runtime: develop dc0f466bc, unchanged by this route-validation task.
Production GameplayCaptureTool: --game s3k --zone soz --act 2 --main knuckles
--sidekick none --donor off --width 800 --x 0x4940 --y 0x430 --rings 37
--emeralds 0000000 --frames 2839 --every 1 --scale 2 --input input.bk2
--rom /home/farrell/code/projects/OpenGGF/s3k.gen --out-dir this-directory.

Positioned start is declared. All subsequent movement is ordinary controller
input, including the real cork floor replacement, scorpion encounter, rock-held
switch and raised door. This is not a cold full-act or synchronized native
parity claim. Canonical source input: soz2-lower-rock-knuckles-320.script/.bk2.

2839 frames at60fps, nearest-neighbor2x encode, full ffmpeg decode passed.
Final player (19061,1452), 37 rings, no death rows.
Hurt rows: 0. PNGs and full CSV are retained.
The committed TestSozLowerRockPuzzleCapture covers both characters at all five
current presets and157 whole-registry replay windows. See the SOZ2 coverage
matrix and campaign audit for exact checks, integration and limits.

Fixture/test commit89600ccf6; delivery record39b04d1b5. Integrated develop
verification:69 focused tests, zero failures/errors/skips, including all157
puzzle replay windows. Pushed to origin/develop; task worktree removed.
