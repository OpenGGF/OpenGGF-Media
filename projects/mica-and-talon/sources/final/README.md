# MICA & TALON — final promo pass

Mod Showcase: an example built with OpenGGF's mod framework. Not a release or download announcement. Engine source a64655fe97 (carry take from b8c105a986); all selected captures rebuilt and recorded against final art. No engine commits, stash, hook bypass, ROM modifications or pushes.

## Review history and fixes

User: final art everywhere, no stock Sonic/Tails art, both aspect ratios, measurement-based sound qualification, local archive only. The earlier native-pose reference is replaced with model sheet → GPT drawing → final sprite; the boot-logo Sonic animation and stock ending photos are excluded.

Lead phase-2 review:
1. Persistent positioned/editorial strip removed; setup remains in provenance here.
2. Results-backed editorial title replaced with real S2 title, neutral capture through full MICA/TALON rise. Source frames 510 onward exclude the boot sequence. End names sit on opaque designed plate.
3. Stray tabs removed. Complete blue bands with red tab and yellow baseline enter and leave together below the HUD.
4. Jade/Gilded and flight panes follow native CSV player position within padded source viewports. Both subjects remain in their panes, including strikes.
5. End plate is fully opaque: no HUD/results show through.
6. Carry: the fix merged into integration as b8c105a986 after this lane stopped. The lead captured `carry` (S3K AIZ, positioned, TALON grabs and lifts MICA) against that build into captures/carryfix, copied it to captures/final/carry and set the TOGETHER chapter's full-frame take to it (`edit.py` line 162, source frame 40). Team footage remains in the TOGETHER/SOLAR pair.
7. Both splits and grids inspected; S1 switched to a cold-start shot with visible MICA, HUD cell reframed to retain full TALON name, signpost interval limited to its spin and final branded face before results cover it. Grid cells use exactly 3× native pixels; they are subject crops, not full viewports.

## Evidence and limits

Positioned starts and declared rings/emeralds are demonstrations, not legitimate continuous acquisitions. Gilded climax is one uninterrupted positioned EHZ take through combat, signpost and results. MGZ2 chain source score changes at 65,82,104 show airborne three-Mantis defeats. Half-pipe is debug positioned ROM-starpost component entry after checkpoint reset; actual native collision admits SPECIAL_STAGE. Continue and ending use debug production-provider entry; ending selects TALON piloting the plane and excludes stock photos. Ending state.csv observes the detached capture loop, not the separately bound Engine ending loop. Data Select uses declared team save slots; stock No Save tile is excluded. These shots certify selected surfaces only.

Sound was checked by measurement only. One paced DAC-enabled S3K LBZ1 bed; Giant Ring is an editorial title-slam cue at the exact picture transition. Ambiguous ring accents removed; no fabricated jump or pickup sounds. See check and AAC loudness results in verification.json. Every source is silent; no unsynced native track is mixed under the bed.

## Rebuild and relocate

Java 25, Python with numpy/Pillow, ffmpeg/ffprobe, provided fonts, user's verified ROMs, final example jar. Build `python3 examples/mica-and-talon/build.py`. `recapture.py` replays phase-2 per-shot provenance against final engine/classes and recompiles retained Java presentation hosts; keep original phase2 root available. `safe_run.py` supplies cold GHZ; `title_full.py` supplies complete title. Scripts record exact commands and jar hashes beside each capture. Relocate checkout constants, retained source root, font/music symlinks and historical GPT drawing path. No ROM/art/audio/build/environment bytes are in this archive.

Run `venv/bin/python render_all.py --checkout <engine> --take final`; it checks/sheets/renders both layouts, masters AAC, ffprobes, measures encoded true peak and fully decodes. `chapters.json`, `selected-shots.csv`, and `edit/edit.py` supply chapter map, source intervals, brief and beat sheet. Source frame sequences, artwork, fonts, PCM, packaged jar and finished reels stay external at the catalogued production root; cataloguing is not uploading. Media branch is local only for lead publication after user review.
