# SOZ2 cold lower rising-room input repair

Runtime base: 7a00b2915defee9e5cdd4f9d5da74e708cf82769; no production edits.
Native320 Sonic + Tails, donor off, cold Act2 with intro enabled; no position,
ring, object or event seeds. Input Log.txt records every controller input from
boot through the normal-background return at input18262 (background routine32).
The input prefix repairs the older paired recording; test-only controller decisions
finish the lower rising room. Source worktree: feature/ai-soz-cold-route-replay,
TestSozColdLowerRoomAuthor (temporary authoring probe, not delivered).

Fresh run: queued Java21 DISPLAY=:0 TestSozColdLowerRoomAuthor,
soz.lower.prefix=15800, soz.lower.phase=3, soz.lower.threshold=100,
soz.lower.stride=1; input was the repaired rock-jump variant.
One test passed, zero failures/errors/skips. This is partial cold-route progress,
not Act2 completion or emulator parity. The final boss and remaining traversal
are still under revalidation.

Video covers inputs15800..18262 inclusive,2463 frames at60fps, nearest-neighbour
3x scale (960x672). Full ffmpeg decode passed. state.csv contains all18263 rows,
including the cold prefix. The local phase values choose controller input only.
