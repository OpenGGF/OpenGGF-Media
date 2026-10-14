# Last-checkpoint shortcut to SOZ2 boss

Production setup: native Sonic + Tails, 400×224, SOZ Act 2, skipped title
presentation, audio off. Boot at the ordinary start, step 90 neutral frames,
call the real C shortcut helper, and step neutral input until the production
reload replaces the object manager. Step 120 more neutral frames and supply
99 rings to keep the boss visible through contact. No event, position, camera,
terrain or collision state is edited.

Then replay the 1,200 rows in `Input Log.txt`. `state.csv` records those same
inputs and live event state; the log begins after the reload setup, so it is
not a cold-start movie. PNGs sample every fourth gameplay frame; `capture.mp4`
plays them at 15 fps for normal speed. The room event starts at frame 689,
background mode 40 at frame 718, and the shell is visible at frame 760.

Source implementation: `116d542a9`, integrated as `7bdb0fc41`.
The repository regression checks the shortcut at 320/400/800 pixels, preserves
lives and isolates rewind history. Broader native parity remains separate.
