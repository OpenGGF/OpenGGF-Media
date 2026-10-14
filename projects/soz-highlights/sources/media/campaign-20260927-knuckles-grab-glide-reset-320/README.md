# Knuckles SOZ2 grab and release correction

Candidate on base 58001b58e, feature/ai-soz-knuckles-act2 (not yet integrated).
ROM: root s3k.gen; native movement, width320, solo Knuckles, donor off, intro enabled.
No position, rings, emeralds or gameplay-state seeds. Input is controller-only.
The captured cold prefix runs through input13680. One final neutral observation
at13681 follows a same-world snapshot restore; the preceding captured prefix is
uninterrupted. Frames13000..13681 at60fps, nearest-neighbour3x,11.366667seconds.
At13324 the hanging mapping is145. The object releases at13325 with
xvel=-512,yvel=-896; the next player pass preserves ordinary jump physics.
This supersedes the stale glide pose/velocity seen before the loc_165AE fix.
All13682 state rows are alive. This is a progress clip, not full Act2 acceptance.
ffprobe confirms960x672,60fps,682 frames; full ffmpeg decode passed.

Input SHA256: ddc625a54c31047b1025c375334951af3b1a011e9b1586db77a161720aeff586
