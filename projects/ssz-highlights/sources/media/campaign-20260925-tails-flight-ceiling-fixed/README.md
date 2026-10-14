# Tails signed flight ceiling correction — 2026-09-25

Cold SSZ1, native320, Tails alone, donor off, no gameplay seeds. Input is the
2,556-frame variant-2 from campaign-20260925-tails-branch002, now preserved as
ssz1-tails-solo-cold-flight-320. Old code stalls at1205/3087 at2345 and dies2545.
The fixed replay reaches1317/3007 at2345 and2085/2954 at2555 without dying.
A read-only live probe confirms Camera_min_Y=-256 while the old flight stalls.
ROM loc_14892 adds16 in a word and uses signed cmp.w/blt; the engine formerly
used unsigned coordinates and an unwrapped sum. Unit tests reproduce both errors.

Capture frames2225–2555:331 frames at60fps, full ffmpeg decode passed. Still2345
inspected. This is engine presentation, not a native matched-input comparison.
The route is an opening frontier only; it does not complete Tails SSZ.
