# SOZ Act1 solo cold clear — 2026-09-27

Source: implementation `bd1625cdb`, integrated verification `653082073`, base `057fb498e`.
Both commits are pushed to develop. Integrated focused verification:64 tests, zero failures/errors/skips.
Canonical inputs: `src/test/resources/routes/s3k/soz1-cold-sonic.bk2` (31,671 frames).
Fresh production GameLoop/render replay, native320 solo Sonic, donor off, intro enabled.
No position, ring, health, phase or timing seeds. Zero deaths and no follower.

Capture: `TestSozColdAct1Capture`, input override above, empty `soz.cold.followers`,
`soz.cold.act1.capture-from=27300`, `soz.cold.act1.stride=1`, explicit root S3K ROM.
MP4:4371 frames at60fps,960×672,72.85s. FFmpeg full decode verified.
All31,671 state rows match the author on movement, rings, animation, camera, act and boss state.
Golem sinking starts at30063 (46.05s); playable Act2 at31490 (69.83s).
This is engine route/presentation evidence, not native-emulator parity.
