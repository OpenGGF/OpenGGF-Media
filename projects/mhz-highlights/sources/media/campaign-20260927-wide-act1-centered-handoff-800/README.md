# MHZ 800px centered results handoff

Base develop 5ff400010 plus the uncommitted feature/ai-mhz-wide-route candidate. Sonic solo, donor off, cold MHZ1 start, fixed controller-only input. No position, ring, health or event seeds.

10,330 observed frames; no deaths. Movie covers frames 8,100–10,329 (2,230 frames, 37.166667s at 60fps, 1600×448, silent). Full ffmpeg decode and ffprobe passed. Actual Act 2 reload is frame 9,260. Frame 9,340 shows centered results. The native maximum $98 retains widescreen projection until Change_Act2Sizes expands it.

Known inherited presentation gap: reload frame 9,260 has garbled sprite art, with absent sprites on the following frame. The unchanged 320px baseline reproduces this at frame 8,469; see sibling campaign-20260927-native-handoff-baseline-320. This capture is route/presentation evidence, not ROM parity certification.

Focused runtime checks: 194 tests passed, zero failures/errors/skips, including the cold native and wide routes. Additional viewport lifecycle cases: 10 passed, zero failures/errors/skips. Combined delivery validation and integration remain pending.

Runtime candidate integrated as a2fad9a79 (delivery record043d86212). The centered-handoff capture is the current presentation; earlier clips retain the superseded projection lifetime. Integrated focused selection:299 passed,0 skips; guards:672 passed,0 skips.
