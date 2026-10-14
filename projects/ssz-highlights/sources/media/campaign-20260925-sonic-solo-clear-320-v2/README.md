# Solo Sonic SSZ full clear — 2026-09-25

Runtime 15d712413. Cold native 320 SSZ1, Sonic alone, donor off, no gameplay seeds.
Input sonic-complete002.bk2, 21,286 frames including an extended DEZ tail.
The canonical ssz1-sonic-solo-cold-complete-320 input stops at 19,845 frames:
actual DEZ1 load at frame 19,844 (48,2476). No deaths or follower anywhere.
The first 18,286 capture rows match the snapshot-forked author on all 20 state
fields; raw input strings differ in formatting only after the cold prefix.
Video frames 16,276–21,285: 5,010 frames at 60fps, full ffmpeg decode passed.
Inspected frames 17,506 (last attack approach) and 18,285 (defeat explosions).
This is independent engine route/presentation evidence, not native pixel parity.

Controller method: after 16,276 ordinary cold inputs, twelve movement/jump/roll
policies are trialled from an engine-owned full-registry snapshot for 180 inputs.
The highest survival/damage score supplies the next 30 controller inputs; repeat.
The external held-input state is restored alongside every registry restoration.
No native observation or gameplay value is injected. Final route verification
replays only the selected buttons from a fresh boot, without any search or restores.

The first fresh replay failed at 2,556 because the temporary button serializer
omitted B/C from the inherited prefix. Its first mismatch was input 426. Restoring
those original recorded buttons fixes the replay; no runtime adjustment was made.
The author was stopped after the boss defeat before any level-load trial restore.
A 3,000-neutral-input tail independently completes collapse, results and handoff.
The new final-route regression covers 41 further restore/replay windows and the
actual outgoing/incoming history boundary. Both solo tests pass: 2 tests,
0 failures/errors/skips, 42.345s Maven on Java 21 with the explicit S3K ROM.
