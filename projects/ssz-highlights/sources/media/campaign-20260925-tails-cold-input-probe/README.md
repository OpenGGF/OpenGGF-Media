# Solo Tails SSZ cold input frontier — 2026-09-25

Runtime 30a3537d0, unchanged by pending FBZ test-only edits. Native320, Tails
alone, donor off, cold SSZ1 with no position/ring/health seeds. Reused the
certified ssz1-sonic-solo-cold-complete-320.bk2 as a diagnostic only.
Tails dies at input1940 (1184,3152), before reaching any boss; final capture
stops at2001 rows after the 60-frame death grace. This does not establish a
runtime bug: the Sonic controller route is not valid for Tails unchanged.
No video was requested;17 sparse PNGs and state.csv are preserved.
Next route work should branch before the opening hazard, not restart boss work.
