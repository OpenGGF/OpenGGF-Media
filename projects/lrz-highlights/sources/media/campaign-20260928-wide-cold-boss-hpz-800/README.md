# Cold widescreen Lava Reef boss to Hidden Palace

Candidate: feature/ai-lrz-wide-act1-clear, base f46863ed002e359137cbe268bea819d204de9dc7.
Source074dafe84; integration46666b019. Destination114 tests pass, zero failures/errors/skips. Pushed develop c901b9a0f (delivery record).

Cold LRZ1, native Sonic+Tails, donor off, 800px, no gameplay seeds. 50659 inputs.
This video shows inputs43880–50658: earned fire shield, arena descent, all14 mine
hits, capsule opening, results, release and playable HPZ. Defeat49177; HPZ load50538.
Final388/2796, three rings, Tails. Zero deaths; no hurt after shielded arena entry.

GameplayCaptureTool --game s3k --rom /home/farrell/code/projects/OpenGGF/s3k.gen
--zone lrz --act 1 --width 800 --main sonic --sidekick tails
--input src/test/resources/routes/s3k/lrz-boss-sonic-tails-cold-hpz-800.bk2
--frames 50659 --capture-from 43880 --scale 2 --out-dir THIS_DIRECTORY

6779 frames, 1600x448,60fps,112.983333s. Full ffmpeg decode passes. Independent
capture matches every CSV field across all50659 authoring rows. Stills49177,
49500,50000,50658 inspected. TestLrzWideBossColdRouteCapture passes71 two-cycle
full-world rewind windows plus real HPZ load-history isolation, zero failures/errors/skips.
Engine presentation evidence; not synchronized emulator pixel parity.
