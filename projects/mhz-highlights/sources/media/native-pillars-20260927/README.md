# MHZ2 native pillar reference, 27 September 2026

BizHawk 2.11/GPGX, verified locked-on ROM SHA-1 CFBF98C36C776677290A872547AC47C53D2761D6.
Ordinary Sonic/Tails complete-run BK2 continued from native movie save299000 to300700; no RAM writes or positioned setup. Full input/state/emulator/source hashes are in final-reference/host.json.

final-reference/observations.csv has639 chase-window rows. The607 rows with Events_bg+1 active supply3035 checked BG scroll words (lines0/17/30/40/47). All match loc_55552..loc_555FC, including77 early-clear frames. All3710 sampled active helper positions match loc_555D2, with zero mismatches. Current and copied camera words agree on all639 rows. This corroborates arithmetic and world coordinates, not engine full-frame parity.

Near native camera0x417F, line47 is -16663, tall support16928 (0x4220), spike pairs16932/16937/16943. The first DIVU remainder must feed the second quotient. Native320 engine baseline drops it and produces a flat ramp at0x4180; the candidate fixes that and projects widescreen display words separately.

Capture exporter: tools/bizhawk/capture_mhz_pillar_reference.lua in the candidate branch; integration SHA pending. Plan retained in plan.lua. Selected native images f300067.png and f300307.png show the actual encounter. Render-all final capture produces byte-identical observation rows to the initial sparse-render probe. Initial275484..299000 window ended before the chase and was rejected for zero observations; its failed outputs are disposable.
