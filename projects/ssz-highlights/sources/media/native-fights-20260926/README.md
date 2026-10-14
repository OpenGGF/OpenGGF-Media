# SSZ native fight survey — 2026-09-26

Read-only BizHawk 2.11/GPGX playback of the original recorded movies. No gameplay
RAM writes. See run1/host.json and act2/host.json for exact commands, ROM/movie,
exporter/plan/emulator hashes, fixture-state hashes and successful host results.
ROM identity was checked against the independent repository SHA1.

Act1: state frame448920; observe452000..467450 inclusive (15,451 continuous
rows, 66,936 object rows, 7,726 PNGs). This movie also enters a bonus stage in
that interval. It is not continuous SSZ-only footage. Act2: state412502;
observe413300..419844 (6,545 continuous rows, 23,101 object rows, 3,273 PNGs),
stopping before the excluded ending. Native screenshots retain all original pixels.

Movies sample every second emulator frame and encode at30fps, 2x nearest-neighbour.
Act2 sources have a348x240 border; video crops320x224 at14,8 before enlargement.
Full FFmpeg decode passes for native-act1.mp4 (7726 frames,257.533333s),
native-act2.mp4 (3273 frames,109.1s), and native-power-down.mp4 (195 frames,6.5s).
The short clip starts94.333333s into native-act2.mp4: source frame418960.
Framebuffer-content probes pass for453000 and419272; that check alone is not parity.

Observed body attributes: GHZ art052E/bucket4, MTZ art052E/bucket3;
Mecha artA3F4/bucket5 throughout both acts, observed power-down and defeat.
Viewed453000/453040 (cloud/ship),455300/455400 (MTZ),466000 (Mecha),
419252/419272 (island overlap). Hyper Sonic defeats MTZ during descent, before
its normal hover/late orb/laser phases. Those phases remain uncorroborated here.

Current engine comparison at3d0c32eec is in sibling directories
campaign-20260926-full-fights-320 and campaign-20260926-knuckles-fights-declared-320.
Different inputs/timing/HUD/cameras mean phase comparisons only; no matched pixel
or trajectory parity is claimed. No new runtime priority change was necessary.
