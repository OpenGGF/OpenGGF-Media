# Native SSZ MTZ orb lifecycle excerpt

Source: ../native-fights-20260926/run1, read-only BizHawk 2.11/GPGX original
movie playback; exact provenance remains in that archive's host.json and README.
No gameplay RAM writes. frames.txt lists original screenshots455110..455800,
every second emulator frame, encoded30fps at2x nearest-neighbour. FFmpeg concat
rounding holds the final image for one extra output frame (347 total). Full decode
passes. This is native evidence, not an updated engine recording or parity claim.

objects.csv uses decimal code pointers. Orb code0x7AD8A: routine2 orbit,
4 launched,8 pop. Orbit counts7,6,5,4,3,2,1,0 at frames455111,455252,455297,
455341,455387,455433,455478,455524. Last two launchers pop455572, gone455573.
Escaping ship code0x7AC92 is last present455755. Its earlier wait routine is
outside the exporter filter; absent rows there must not be read as deletion.
