# Corrected floor contact — diagnostic excerpt

Runtime: c479eea6a plus removal of DezFinalArenaFloor pre-movement proximity support.
Cold DEZ1, ordinary solo Sonic,320px,donoroff,no seeds. Input sonic-final-floor008.bk2
in ../campaign-20260925-solo-input. Full replay ends in a fireball death at55290;
this attempted input is NOT a clear. The original complete route also needs repair.

floor-contact-demo.mp4 extracts source inputs54800–55180 inclusive from capture.mp4:
381 frames at60fps (6.35s), ffmpeg full decode passes. It illustrates the corrected
standing height and ongoing animation, first core hit, floor breakup and landing.
State rows55040/55060/55080/55100 all have grounded Y205 with changing mapping
frames158/1/186/2. The clip excludes the later failed next-button approach.

Production capture uses GameplayCaptureTool with --game s3k --zone dez --act 1
--width 320 --main sonic --sidekick none --donor off --frames 55351
--capture-from 54800 --input <above BK2> and the root s3k.gen ROM.
