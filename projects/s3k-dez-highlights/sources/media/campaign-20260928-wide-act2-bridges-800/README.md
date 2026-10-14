# DEZ Act 2 widescreen bridge route progress — 2026-09-28

Engine source: ee8e470e4; checkout 8540cdab0 (documentation-only successor).
Cold DEZ Act 1 Sonic solo, 800px, donor off, no position/ring/clock seeds or settling. The supplied 30,450-input BK2 includes both Act 1 boss phases and the real seamless Act 2 load. It extends the independently verified 27,342-input lower-gravity prefix with ordinary controller inputs.

Fresh GameplayCaptureTool replay matches all 30,450 branch-author CSV rows on every exported field; zero death rows. Final centre (4891,2351), 23 rings. The 3,150-frame clip covers inputs 27300–30449 at 60fps, 1600×448, 52.5 seconds. Full ffmpeg decode passed; frames 27950 and 28250 inspected for upper-bridge traversal and inverted gravity presentation.

This is engine route progress, not emulator parity or a completed Act 2 route. New rewind coverage has not yet been added. No runtime code changed. The bridge departure was resynchronised to the actual landing rather than continuing an incorrectly timed native-width input tail. Prior run-up attempts were hit by a hazard before jumping; they do not demonstrate a collision bug.

Later exploratory continuation is target/dez800-act2-middle-tail-20260928/variant-0 on the current main checkout. It reaches x6079, including upper gravity section near (5968,1363), but backtracks and is not yet a certified continuation. Resume input authoring from around 32450, before the upper passage stalls. Keep this distinction from the fresh verified prefix above.
