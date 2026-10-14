# Cold Tails MHZ2 completion

Runtime source efd892fc9, based on 2f298ba9e; captured from its development
build before commit. Native 320, Tails solo, donor off, cold MHZ1 entry, no
position/health/ring/clock seeds and no debug completion. Canonical inputs:
src/test/resources/routes/s3k/mhz2-tails-incoming-320.script/.bk2 (35,814 frames).

GameplayCaptureTool flags: --game s3k --zone mhz --act 1 --width 320
--main tails --sidekick none --capture-from 31800 --scale 2
--stills 32120,32900,33145,33700,35000,35800. The input is the canonical BK2.
4014 video frames, 60fps, 640x448, 66.9 seconds. Full FFmpeg decode passed;
stills at defeat33145 and ship35000 were inspected. State CSV has35,814 rows,
zero deaths and zero follower rows. FBZ loads at35453; final row35813 is
released ordinary movement in FBZ at(211,1211),3rings.

The full33,146-row boss-author overlap and35,454-row exit-branch overlap match
fresh capture on every state field except the deliberately different input-text
representation. Exploration used ordinary P1 buttons and engine rewind snapshots,
not native trace state. The first trial exposed a real palette-fade reconstruction
failure, fixed by restoring its target array shape. A later trial's4px steering
limit could not catch the chase;8px desired steering in the input author completed
all nine hits. No engine movement speed was changed.

The committed test verifies both Sonic and Tails whole-world restore/forward
replay at admission, weather fade/deletion, chase hit, last hit, defeat, results,
ship, carry and released FBZ; Tails additionally covers pulley and upper flight.
This capture is engine presentation/route evidence, not native-emulator parity.
