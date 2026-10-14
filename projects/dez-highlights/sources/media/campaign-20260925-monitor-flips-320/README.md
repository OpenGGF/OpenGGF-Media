# Upside-down monitor presentation comparison

Engine b1c00284f plus the monitor presentation correction, 2026-09-25.
S3K ROM CRC32 63522553; native Sonic solo, 320x224, normal gravity.
The FBZ Act 2 start is a clear backdrop, not a claimed placement in the ROM.
After 60 neutral boot frames, seed ring monitors at screen (144,60) upright
and (256,60) Y-flipped. At capture frame90 invoke both production touch
callbacks with the player temporarily in roll animation and zero Y speed,
then restore his original animation/speed. All 240 frames use neutral input
and the normal game loop/renderer. This is a presentation probe, not a route.
The camera stays (0,1420); no deaths; final rings20. The upright icon travels
up and the inverted one down, with the native one-tick reward difference.
Inspected frames60 and121; the MP4 fully decodes with ffmpeg.

The earlier DEZ-corridor composition obscured the icons with foreground;
it was rejected. This final version uses FBZ and elevated monitor positions
so both complete arcs remain visible. Capture source was a temporary
GameplayCaptureSession probe under target; production/test behavior is
preserved in TestSonic3kMonitorObjectInstance and the act matrix.
