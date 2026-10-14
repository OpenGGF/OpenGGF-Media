# SSZ MTZ touch correction — final upper route

Runtime and controller inputs committed as `95b478717` (develop). Native Sonic + Tails,
320px, cold SSZ1 start through production GameplayCaptureSession/GameLoop.
No position/velocity/rings/health/emerald seeds. S3K ROM SHA1:cfbf98c36c776677290a872547ac47c53d2761d6.
Input SHA256:ccb2542b478f308878120d9985b3a55b5c59dc6e574b8fc532c02f7be9c0a6f8. The copied script and BK2 are the committed source pair.

GameplayCaptureTool --game s3k --zone ssz --act 1 --main sonic --sidekick tails
--width 320 --input input.bk2 --frames 11051 --capture-from 8600 --scale 2,
with --rom /home/farrell/code/projects/OpenGGF/s3k.gen, a fresh --out-dir,
and native DISPLAY=:0.

state.csv covers all11051 stepped inputs; zero deaths. Video has2451
frames,60fps,640x448, nearest-neighbour2x, and fully decodes. Additional neutral
inputs after the BK2:0. The complete route actually loads DEZ at19456;
its first framebuffer is black during the transition fade, with visible DEZ
entrance by19550. Fight frame9378 and spiral18600 were visually inspected in
the applicable capture. This is engine reachability/presentation evidence,
not a frame-aligned native parity recording. See the sibling native orb audit.
