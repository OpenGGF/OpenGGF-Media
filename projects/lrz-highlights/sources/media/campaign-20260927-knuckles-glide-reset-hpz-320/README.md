# Knuckles LRZ glide-reset route repair

Captured from feature/ai-soz-knuckles-act2 at base58001b58e.
Corresponding source integrated on develop as49586cd86; verified and pushed to develop.
ROM-backed loc_165AE object-control glide reset plus reauthored controller inputs.
Cold LRZ Act1, native320 solo Knuckles, donor off, no state seeds.
Input SHA-256: 9f6962af70fcb2cfe47e891e9ee402e5fe60825059c5794e8ff910dddad2d1f5

GameplayCaptureTool --frames49526 --capture-from45700 --scale3,60fps.
This is an independent uninterrupted cold replay. All49,526 state rows are alive.
Video covers the repaired ceiling/wall transfer, final passage and real HPZ load
at input49286, followed by playable movement to(1069,748). Input and full CSV included.
Selected stills:45730,45800,49286,49525. Engine capture, not emulator pixel parity.

Delivery: runtime `49586cd86`, wide-route tests/inputs `38f799053`, pushed to develop.
Integrated full ordinary: 25,086 tests, no failures/errors, 29 reviewed skips;
guards: 672 tests, no failures/errors/skips. Permanent native/800px SOZ checks:
2 tests, no failures/errors/skips, 48 replay windows plus 18 semantic events each.
Task worktree and local branch removed after preserving final evidence.
