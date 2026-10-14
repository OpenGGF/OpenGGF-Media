# Flappy Tails promo plan (task dir, not in repo)

Target: ~80 s, 1920x1080 @ 60 fps, H.264 + AAC 48 kHz stereo. Over the top: trailer-voice text slams,
impact zooms, flashes, shakes, a slow-mo near miss, fake review quotes, Super Tails climax.

Captures (ExampleModCapture, --scale 5, 2000x1120 -> crop 1920x1080, every tick, game audio):
 A title      : title screen, logo slide-in, Eggman pass, attract flight (0-700)
 B tour       : seed 0x5eed, autopilot CLASSIC from AIZ1 through Super Tails (~6400 ticks)
 C rings      : SONIC RULES, autopilot, rings:40 then autopilot off -> ground hit -> scatter -> on
 D crash      : CLASSIC autopilot to ~23 gates, autopilot off -> crash -> GAME OVER -> tally -> medal -> NEW BEST
 E daring     : autopilot daring 70 for near misses (slow-mo source)

Cards (ROM CardFont rendered 400x224 -> x5 nearest -> crop): IN A WORLD / ONE FOX / ONE BUTTON /
FIVE ZONES / RINGS SAVE YOU / SUPER TAILS / reviews / end card.
