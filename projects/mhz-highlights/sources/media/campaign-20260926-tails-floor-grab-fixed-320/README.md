# Solo Tails floor-grab correction

Runtime source e373c4d9f (based on c28823fdf), integrated into develop. Change:
CutsceneKnucklesMhz2Instance selects RawAni_65EB0 by character identity,
not participant slot (ROM sub_65E72/loc_65E9E).

Cold MHZ1 Tails solo, donor off, native320; canonical
src/test/resources/routes/s3k/mhz1-tails-cold-complete-320.bk2 (24121 inputs),
then600 neutral inputs. No state seeds. GameplayCaptureTool --frames24721
--capture-from23700 --scale3 --stills23930,23932,24060,24100,24500 (flags take
separate arguments).1021 frames at60fps960x672. Full ffmpeg decode passed;
both raw-pose phases inspected. All shared24121 rows match the prior capture
except124 mapping_frame values in23929..24052:180/181→167/168. No deaths.
This supersedes the prior movie's floor-grab pose, not its route evidence.
