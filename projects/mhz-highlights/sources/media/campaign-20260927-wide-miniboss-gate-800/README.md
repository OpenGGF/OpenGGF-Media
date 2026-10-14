# MHZ1 800px cold miniboss admission

Candidate on base `5ff400010`, with the uncommitted native-camera projection fix.
Full cold ordinary Sonic solo input, donor off, no position/ring/health seed.
8,620 observed frames, zero deaths; the silent 60fps movie covers inputs
8030–8619 (590 frames, 9.833333 seconds, 1600×448). Full decode passed.

Before the fix, Sonic stopped at x=17344 while the visible camera left x=16944
could never reach the ROM gate $4298. The gate now uses the native viewport
origin, with consistent boss spawn/attack/escape and wrap coordinates.
The movie shows admission and initial boss arrival; it is not a boss defeat
or complete-act demonstration. Independent full fight and replay checks remain.

Runtime candidate integrated as a2fad9a79 (delivery record043d86212). The centered-handoff capture is the current presentation; earlier clips retain the superseded projection lifetime. Integrated focused selection:299 passed,0 skips; guards:672 passed,0 skips.
