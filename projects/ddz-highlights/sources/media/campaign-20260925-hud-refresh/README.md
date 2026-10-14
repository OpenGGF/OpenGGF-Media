# DDZ HUD redraw — 2026-09-25

Native BizHawk2.11/GPGX resumes existing movie save514214; no RAM writes,
movie stopped after loading its own state, then120 neutral updates. host.json
records verified ROM/movie/exporter/state hashes. rings.csv samples native
Ring_count FE20 and Update_HUD_ring_count FE1D after each frame.
Native changes:0/redraw1 at0,0/redraw0 at1,50/redraw0 at24,
49/redraw1 at85,49/redraw0 at86. Screenshots show zero retained through85,
then49 at86. No sampled row is supplied to engine gameplay.

Engine: ordinary GameplayCaptureSession DDZ320/native Sonic solo, declared
seven Super Emeralds, neutral inputs. rings.csv samples live and displayed
values. Initial boot consumes a non-gameplay frame: engine n+1 corresponds
to native n. Engine observations are50/display0 at25,49/display0 at86,
49/display49 at87. Native score/camera fraction are inherited; the fresh
engine setup does not seed them. Full-scene pixel/trajectory parity is not claimed.

comparison.mp4 is121frames at60fps, nearest-neighbour2x, native left/engine
right. Full decode passes and before/after redraw frames are inspected.
The preceding Hyper sparkle queue correction is present in the engine footage.
