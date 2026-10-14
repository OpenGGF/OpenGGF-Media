# SSZ MTZ touch correction — final complete route

Runtime and controller inputs committed as `95b478717` (develop). Native Sonic + Tails,
320px, cold SSZ1 start through production GameplayCaptureSession/GameLoop.
No position/velocity/rings/health/emerald seeds. S3K ROM SHA1:cfbf98c36c776677290a872547ac47c53d2761d6.
Input SHA256:a879fc7d5d60419c9a13a4208e67a80561f3ea0c02eeb88faf25cc1fe535fcfa. The copied script and BK2 are the committed source pair.

GameplayCaptureTool --game s3k --zone ssz --act 1 --main sonic --sidekick tails
--width 320 --input input.bk2 --frames 19600 --capture-from 16900 --scale 2,
with --rom /home/farrell/code/projects/OpenGGF/s3k.gen, a fresh --out-dir,
and native DISPLAY=:0.

state.csv covers all19600 stepped inputs; zero deaths. Video has2700
frames,60fps,640x448, nearest-neighbour2x, and fully decodes. Additional neutral
inputs after the BK2:143. The complete route actually loads DEZ at19456;
its first framebuffer is black during the transition fade, with visible DEZ
entrance by19550. Fight frame9378 and spiral18600 were visually inspected in
the applicable capture. This is engine reachability/presentation evidence,
not a frame-aligned native parity recording. See the sibling native orb audit.
