# SSZ bridge checkpoint — 800px

Source: 485e23cfc (bridge selector correction and committed reproduction test).
Reproduction owner: TestSszBridgeCheckpointCapture, native Sonic+CPU Tails,
no donation, cold SSZ1. Temporary capture adapter writes each session.render()
result and live player/camera/checkpoint/bridge/history observations around the
unchanged test procedure. No state is imported from traces or emulators.

The declared destructive stimulus is applyPitDeath(), twice, after the actual
bridge-written checkpoint. These are lifecycle demonstrations, not ordinary-input
death routes. Arrival and post-reload movement use ordinary controller input.
The test asserts checkpoint persistence, no replayed arrival, fresh runtime and
live-history isolation, roster/art retention and bridge dispatch/offset.

2483 frames at60fps, nearest-neighbor2x encode, no audio. Full movie decoded
successfully with ffmpeg. Input1380 shows the finishing bridge; input1900 shows
Sonic over the restored bridge after the first reload. The second restart ends
at player(1019,3180), alive, beyond the bridge. state.csv and frames/ are the
continuous source. Native framebuffer/timing parity is not claimed.

Integrated develop485e23cfc:111 focused checks, zero failures/errors/skips.
Documentation dc0f466bc; both commits pushed to origin/develop.
