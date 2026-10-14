# SSZ MTZ laser priority follow-up

Source: bugfix/ai-ssz-laser-priority from develop 3afe6c3c0; owner-local high tile
priority and native trailing subtype correction. No timing or movement changes.
GameplayCaptureTool: S3K, SSZ act1, Sonic solo, donor off, width320, checkpoint
(0x1700,0x420), rings355, 2100 frames, capture-from1600, every1, scale2.
Input: ../native-mtz-normal-20260926/engine-laser-input.txt, ordinary controller
columns reconstructed from historical raw-35-ssz-mtz-laser/state.csv.
ROM: /home/farrell/code/projects/OpenGGF/s3k.gen.
All2100 state rows exactly match campaign-20260926-mtz-laser-320.
MP4: 500 frames, 60fps, 640x448, full ffmpeg decode passed. Frame1800 inspected.
This is positioned engine presentation, not aligned native parity. The current
view does not establish a visible before/after difference; native art bits and
the production regression establish the fixed property.
