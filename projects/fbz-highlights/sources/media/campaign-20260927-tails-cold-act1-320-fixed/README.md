# FBZ Tails cold Act 1 — corrected defeat debris

Recorded 2026-09-27 from bugfix/ai-fbz-tails-cold-route, base
6088735c85243c3d4eaaeb2bdfaf8981af666a97 plus the three local defeat-child
corrections and input-only Tails route repair. Integration SHA pending.

GameplayCaptureTool: cold FBZ Act 1, Tails solo, donor off, width320,
--settle1 --frames22449 --capture-from18000 --scale2, stills19000/21100/22448.
Input: src/test/resources/routes/s3k/fbz1-tails-cold-320.bk2 (22448 rows),
from the same candidate tree. No gameplay state seeds. All22448 input-driven
rows match the author on12 common gameplay fields, all22449 captured rows
alive. Actual Act2 reload21836, final player centre(343,1520), control released.

4449 frames,60fps,640x448,74.15s, full ffmpeg decode passes. Fight, defeat and
Act2 stills inspected. Against the base-runtime capture,78 images differ
between21557 and21711: capsule fragments now fall with native MoveSprite
gravity. Whole-world replay separately passes44 windows with two cycles each.
These are engine route/presentation checks, not emulator pixel-parity claims.
