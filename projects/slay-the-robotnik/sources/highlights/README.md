# Slay the Robotnik highlight reel (2026-10-06)

Task directory for the example mod's highlight reel. Every clip is a positioned
demonstration: it starts from the mod's title screen or from a `debugJump` into a room
(see SlayScene.debugJump), not from a continuous run. Each clip was recorded with
ExampleModCapture (--video/--audio), at 60 fps, with audio from the engine's SMPS driver.

- scripts/<clip>.txt   the input script passed with --script-file
- clips/<clip>.mp4     raw capture, 800x448, 60 fps
- edit.csv             the ordered edit list (clip, title, source in/out seconds)
- reel.mp4             the assembled reel; chapters.txt gives the output times

## Provenance

- Source tree: the str-slots integration worktree, whose example and capture code is identical to
  feature/ai-slay-the-robotnik at 25b57f886 (pushed to PR #211); S3K locked-on ROM (CRC32
  63522553), width 400, scale 2, 60 fps. To re-record, point `W` in `record.sh` at a checkout
  of that branch with its test classes built (`target/test-classes`) instead of the removed
  worktree's overlay.
- Capture driver: `record.sh` (ExampleModCapture with `--video`/`--audio`). Clip 01 starts
  from the mod's title screen with a random seed; every other clip enters a room with
  `SlayScene.debugJump` and a fixed seed (the `# jump:` line of its script). Audio is the
  engine's SMPS rendering of the scene's music and sound effects through the offline capture
  lease, one packet per tick.
- Assembly: `assemble.py` (edit list `edit.csv`, chapter map `chapters.txt`): nearest-neighbour
  x2 into 1920x1080, a 0.2 s fade through black at every cut, captions in the lower bar.
- Known: the Starpost clip is cut before Proceed; the final-boss clips skip two turns of the
  fight between the transformation and the last blow.
