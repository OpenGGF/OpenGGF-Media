# Integrated cold replay attempt

Runtime a66e14bf5. Native S3K Sonic + Tails, width320, coldAct2. Production omitted-title lifecycle and pending initial ProcessSprites consumed before recorded input0. No gameplay state hydration, teleports, or mechanics writes. Full Input Log.txt is authoritative.

Replayed first25468 inputs from authored-act2-fourth-wire. First physical drift from its bfce36a2c recording occurs at frame3953: old2755/910 airborne yvel56, new2755/908 grounded yvel0. Old downstream inputs therefore no longer traverse the same route. Replay remainsalive but ends checkpoint1 near firstdoor at3037/940. One additional80-input jump/right attempt ends25548 at2995/930 alive. Capture stopped pending another parent integration fix before fresh route authoring.

This is a failed input-prefix replay, not a regression test, parity claim, or completed route. PNGs every30frames and command boundaries; CSV everyframe. Runtime behavior differences need source-owned diagnosis before being called defects.
