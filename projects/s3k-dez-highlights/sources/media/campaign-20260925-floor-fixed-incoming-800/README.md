# Corrected final-floor incoming widescreen check — 2026-09-25

Runtime c479eea6a plus final-floor fix;800px,solo Sonic,donoroff. Declared positioned
DEZ2 start($34B0,$300),200 rings,seven Super Emeralds, no reseeding at final/DDZ loads.
Canonical input dez2-through-ddz-800.bk2. Capture17001 inputs,video13000–17000:
4001frames at60fps. Its first16761 rows match the read-only final author on20 state
fields; all17001 rows have zero deaths. The tail shows the actual DDZ handoff.
This clip is positioned continuity, not a cold main-act route or native pixel parity.
The full27224-input movie has separately passed the incoming complete-DDZ test and
11 registry restore/replay spots.

GameplayCaptureTool flags: --game s3k --zone dez --act 2 --width 800 --main sonic
--sidekick none --donor off --x 0x34B0 --y 0x300 --rings 200 --emeralds 3333333
--frames 17001 --capture-from 13000 --stills 13599,16474,16760
--input src/test/resources/routes/s3k/dez2-through-ddz-800.bk2
Root s3k.gen,Java21,DISPLAY=:0. Capture folder is the out-dir.

Floor repair, repaired inputs and reusable authors committed locally as bac660ab4.

All4001 video frames fully decode;13599 and16474 stills inspected.
