# SOZ2 connected mechanisms at 352px

Source: `f4c2aafbd` on develop. No runtime changes in this slice.
S3K ROM SHA-1: `cfbf98c36c776677290a872547ac47c53d2761d6`.

Positioned starts; Sonic solo in lower, Sonic + Tails in upper/rock/switch; native movement, no donor, 99 starting rings. The controller is the committed `SozConnectedMechanismRoute`; the renderer is `TestSozConnectedMechanismCapture`. These are engine presentation checks, not emulator parity or full-act routes.

Queued Java21 / DISPLAY=:0 capture: `-Dtest=TestSozConnectedMechanismCapture -Dsoz.connected.width=352 -Dsoz.connected.stride=1 -Dsoz.connected.capture=<this directory>`, explicit root S3K ROM. Four passing capture cases, zero skips.

60fps, every engine frame, nearest-neighbour 2x scale. Every MP4 decoded completely with ffmpeg. Stills inspected at upper596 and lower1500/3056. Upper wraps at596; lower exits background collision and reaches routine0x20 at3056.

- `lower/capture.mp4`: 3057 frames, 704x448, zero deaths; per-frame state and PNGs retained alongside it.
- `rock/capture.mp4`: 240 frames, 704x448, zero deaths; per-frame state and PNGs retained alongside it.
- `switch/capture.mp4`: 180 frames, 704x448, zero deaths; per-frame state and PNGs retained alongside it.
- `upper/capture.mp4`: 680 frames, 704x448, zero deaths; per-frame state and PNGs retained alongside it.
