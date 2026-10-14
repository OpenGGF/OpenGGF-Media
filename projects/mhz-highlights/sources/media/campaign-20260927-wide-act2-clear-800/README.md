# Cold MHZ 800px Act 2 completion — 2026-09-27

Engine commit: 760a228929246a5f2101f174204b4d050d506e1f (local integrated develop).
Native S3&K ROM; Sonic solo; 800px; cold MHZ1; no position/health/clock seeds.
Input: src/test/resources/routes/s3k/mhz2-sonic-incoming-800.bk2 in the
ai-mhz2-wide-route candidate, with its readable .script. Includes production
setup input; no additional settling step. 25,548 inputs, capture from 22,000,
scale 2, stills 22,350 / 23,500 / 25,397 / 25,547.

Actual fresh FBZ load at input 25,397; final centre (117,1900), control released.
All 25,548 state rows alive. All 25,398 prefix rows match winning author on
x/y/velocities/ground speed/air/rolling/hurt/dead/rings/camera coordinates.
3,548 frames, 60fps, 1600x448, 59.133 seconds; full ffmpeg decode succeeds.
The black 25,397 still is the real load fade; 25,547 shows released FBZ movement.

This recording does not invoke rewind. A subsequently discovered omitted
persistent twisted-vine rider set is repaired in the candidate and tested with
short and full-route snapshot restoration; it does not alter forward physics.
Native pixel parity and broader character/donor products remain open.

Audio: silent PNG-derived gameplay capture; no replacement soundtrack.

Delivery: corresponding route/rewind changes integrated through f411b75db and
pushed to develop; campaign verification record 8ec5aa0fa. Original recording
runtime remains 760a22892, as above.
