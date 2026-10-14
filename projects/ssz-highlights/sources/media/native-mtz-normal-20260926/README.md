# Native SSZ MTZ normal-phase observations

BizHawk2.11, locked-on S3K SHA1 CFBF98C36C776677290A872547AC47C53D2761D6.
Each output's host.json records actual arguments and source identities; setup.csv
records all checkpoint, character selection and initial40-ring writes. The ROM
performs the restart; subsequent behavior uses ordinary controller input only.
No boss, health, phase or velocity writes. These are positioned native experiments,
not cold routes or aligned engine comparisons.

run4: observer-v4.lua, Sonic alone, jumping away at one HP.2397 rows, phases0/A/C/E,
954 laser-phase frames. patrol: observer-patrol.lua, Tails periodic flight,4677rows,
phases0/2/4/6/8, unchanged8HP/7orbs. Together cover all normal dispatch phases.
Earlier run1 attacks interrupted the cycle; idle/grounded run2/run3 died early.
laser-replay failed its incorrect449087 frame assertion; normal-entry.State is
frame449086. replay-fixed.lua corrects the assertion; laser-replay-fixed reproduces
all2397 run4 rows. replay-lasers.lua / laser-state additionally logs child art and
motion, still reproducing all2397 common rows. Inputs alone are replayed; no state
rows hydrate gameplay. Source inputs are in replay-plan.lua and laser-state-plan.lua.

native-laser-60fps.mp4 uses957 unaltered gameplay PNGs from steps1440..2396,
nearest-neighbour2x640x448 at60fps. Full ffmpeg decode passed. Children have art
A41F, priority words280/100, subtypes0/2, trailing motion delayed8frames. Pair births
1570/1616/1662 and1959/2005/2051 corroborate46-frame intra-burst spacing.
Native arm-cycle frame1080 and laser frames1600/1800/2000 inspected.
See the committed2026-09-22 S&K campaign audit for conclusions and limits.
