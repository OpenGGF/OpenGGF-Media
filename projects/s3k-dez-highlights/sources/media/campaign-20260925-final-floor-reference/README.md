# DEZ final-floor native comparison — 2026-09-25

Question: Sonic floats above the floor, his animation restarts, and falling blocks appear misplaced.
Engine source: ai-sk-zone-completion, c479eea6a before the floor recovery fix.
ROM SHA1 CFBF98C36C776677290A872547AC47C53D2761D6.
Native BizHawk 2.11/GPGX, existing complete Sonic+Tails movie and movie entry.State
at frame509032. No RAM writes. See native/host.json and native-video/host.json for
exact commands and ROM/movie/exporter/state hashes. Both hosts completed with zero
reported failures; launch logs inspected. The native recording has Super Sonic
and Tails, while the engine route is ordinary solo Sonic: phase-level support and
block-coordinate corroboration, not a matched-input trajectory or pixel-parity claim.

native-reference.mp4 is native frames512000–514200 inclusive:2201 frames,320x224,
60fps, full ffmpeg decode passed. native/floor.csv samples all5168 frames from509033
through514200; native-video/floor.csv repeats those observations with full-rate images
from512000. Sparse stills are in native/; full-rate frames in native-video/.

engine.csv and engine-player.csv observe the unchanged cold64477-input solo route.
Engine frame58700: player4519/186, airfalse, onObjectfalse, radius19, angle0,
animation0, mapping8, renderY186. Adjacent frames alternate airtrue/map7 and
 airfalse/map8, without moving Y. Native grounded samples have centerY205 and
status8 (standing on object). Engine chase later reaches205 with onObjecttrue.
The player drawing has no hidden Y offset here: its physical position is wrong.

Root cause: DezFinalArenaFloor opted into pre-movement proximity support recovery.
The recovery accepted a descending player above the floor, set airfalse/OnObject,
then the actual SolidObjectTop pass rejected contact and cleared the provisional
owner. Removing that override restores landing through the normal inline checkpoint.
Native loc_5A860/loc_5A912 call SolidObjectTop; loc_1E45A requires feet within its
actual landing window and RideObject_SetRide establishes the standing bit.

Falling-worker samples agree with Obj_5A872: centerY240, zero initial velocity,
MoveSprite2 then +26 gravity, X from break request, frame=(X&96)>>5. Example native
512010 has block1872/247, velocity338, camera1805; engine55540 has1776/244,
velocity260, camera1706. These are different falling ages, not a matched frame pair.
Moving support left edge equals the consumed frontier during the escape chase.
Visual floor alignment remains under review; these coordinates alone do not certify it.

Placement follow-up: all135 native and776 engine newborn blocks sampled after
cameraX1312 have X+16==breakFrontier (different route lengths). No independent
spawn-coordinate mismatch was found. Updated full solo and800 videos show the
corrected contact; five full-route cases and164 focused domain checks pass.

Floor repair, repaired inputs and reusable authors committed locally as bac660ab4.
