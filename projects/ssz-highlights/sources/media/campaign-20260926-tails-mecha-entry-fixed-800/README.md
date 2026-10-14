# SSZ final arena entry, 800px

Runtime source7afd827fb; native S3K, solo Tails, donor off, cold SSZ1 start.
Canonical input:src/test/resources/routes/s3k/ssz1-tails-solo-cold-complete-800.bk2.
GameplayCaptureTool: --game s3k --zone ssz --act 1 --width 800 --main tails
--donor off --rom /home/farrell/code/projects/OpenGGF/s3k.gen --frames 13400
--capture-from 13160 --stills 13190,13212,13245 --scale 2.

All13400 state.csv rows exactly match the complete fresh clear replay.
240 video frames at60fps,1600x448; full FFmpeg decode passed. Inspected frames
before activation, approaching the final platform and after lock/boss allocation.
The fixed-X policy projects native$19A0 to visible6320; automatic bounds-derived
mask behavior is unchanged. The complete fight/exit is in the adjacent
campaign-20260926-tails-cold-clear-fixed-800 task directory.
