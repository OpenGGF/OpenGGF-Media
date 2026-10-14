Starpost Valley promo — Seasons, Promo and Docs lane (2026-10-10)
Executable source: d3d1afbd6, feature/ai-starpost-promo.
Authoritative inputs: each segment .txt; write_scripts.py is an earlier rehearsal.
Capture driver: StarpostPromoCapture.java; capture.sh <segment> <frame-count>.
Requires Java 21 compiled engine/test classes, target/test-classpath.txt,
packaged mods/starpost-valley.jar, supplied absolute Sonic 1/S3K ROMs, and GL.
Source frames/counts: story 1080; grow 1560; seasons 1080; neighbours 1050;
hunt 1140; race 1140; parade 520; flickies 520; snowboard 1050; marble 600;
labyrinth 520; scrap 520; lake 1500; orchard-museum 780; finale 1080.
Reassembly: python3 assemble_final.py (uses cuts.txt and emits chapters.json).
Scene and native act frames use the production GameLoop with live ROM audio.
Final: /home/farrell/Videos/OGGF/starpost-valley/starpost-valley-promo.mp4
119.8 s, H.264 800x448 60 fps, AAC stereo 48 kHz.
Visual QA: final-review.png, final-filmstrip.png and final-stills/.
Chapter map and exact queued verification commands: design document section 26.
