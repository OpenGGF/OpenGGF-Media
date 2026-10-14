# Corrected final-floor cold solo clear — 2026-09-25

Runtime: c479eea6a plus final-floor contact fix. Native320 ordinary solo Sonic,
donoroff,cold DEZ1,no state seeds. Canonical input:
src/test/resources/routes/s3k/dez-sonic-solo-cold-ending-320.bk2 (60920 inputs).
Final load50993; last core hit57758; last ship hit60632; ending load60919.
No deaths/follower. Every capture row matches the read-only author's20 state fields.

Video54500–60919:6420frames at60fps,107s, full ffmpeg decode passes. Stills55000,
55110,57758 inspected: grounded Sonic hasY205, feet at visible floor; animation
continues. The short floor-contact-demo from floor008-core is an earlier failed
input trial and is superseded for complete route evidence by this capture.

TestDezIncomingFinalRouteCapture#coldOrdinarySoloSonicClearsAllFinalPhasesAndLoadsEnding:
1test,0failures/errors/skips,1:53 Maven. All preserved registry restore/replay spots
pass. This is engine route and rewind evidence, not a native whole-scene parity claim.
Native support/block comparisons are in ../campaign-20260925-final-floor-reference.

Reproduction uses GameplayCaptureTool, root s3k.gen, --game s3k --zone dez --act 1
--width 320 --main sonic --sidekick none --donor off --frames 60920
--capture-from 54500 --input <canonical BK2> --out-dir <new directory>.
Integration/push and the campaign's combined validation are still outstanding.

Floor repair, repaired inputs and reusable authors committed locally as bac660ab4.
