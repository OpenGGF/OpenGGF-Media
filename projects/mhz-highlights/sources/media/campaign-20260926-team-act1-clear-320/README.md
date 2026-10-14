# Native-pair MHZ1 completion and MHZ2 introduction

Captured 2026-09-26 from forward behavior at 7efb20721. Sonic + Tails,
S3&K locked-on ROM, native 320-pixel viewport, no donor. Cold MHZ1 entry;
ordinary P1 input, neutral P2, no gameplay seeds or debug writes.

Reproducible inputs are committed at f06669105:
`src/test/resources/routes/s3k/mhz1-team-cold-complete-320.bk2`
and its source `.script`. GameplayCaptureTool played all 27,985 inputs;
recording starts at input 24,900. Output is 3,085 frames, 60fps, 640x448,
51.416667 seconds. `state.csv` covers the full route.

Six-hit defeat: frame 25584; actual Act2 rebase: 26015; paired floor grab:
26894..27017 (see frames/26900.png). Final Sonic centre (2080,1436), three
rings, alive and in released Act2 traversal. No Sonic death or missing
follower rows. All 25,585 overlapping author rows match apart from input
text representation. Full FFmpeg decode passed; defeat, introduction and
floor-grab frames were inspected. This is engine presentation evidence,
not emulator pixel-parity evidence or completion of the paired Act2 route.

The subsequent f06669105 repair restores horizontal-bar holder aliasing
after rewind. This uninterrupted movie does not exercise restore; it was
captured before that restore-only fix. The committed cold-route regression
exercises full-world restore/replay at nine route spots. Candidate and main
integration each passed 100 focused tests without failures/errors/skips;
seven focused rewind guards passed in a separate candidate JVM.
