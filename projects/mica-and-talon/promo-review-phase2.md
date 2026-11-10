# Lead review of promo phase 2 (master-16x9.mp4, 84.8 s)

Overall structure, beat sheet, sound measurements and grid content are good. The following must change for the final cut; each item cites what was seen.

1. **Remove the persistent "POSITIONED GAMEPLAY / EDITORIAL SHOWCASE" strip** from every frame. It sits on the native HUD (`TIME` / `RINGS`), which breaks "keep editorial graphics off the native HUD" and adds a text layer to every shot. Disclosure belongs in the provenance and archive README; the end card may carry one short line.
2. **Title drop: use the real title screens.** The editorial "MICA / TALON" is currently white type over a dimmed results screen, with the results text showing through (≈12 s): busy and unreadable. Title screens with MICA and TALON are now merged (integration `ddb9ff2ea7` or later), so the strongest native title is the game's own:
   - Film the S2 title with MICA and TALON rising over the emblem, cold-opening into the title drop. "Film presentation as it ships."
   - Any editorial title goes on a solid S2 title-card blue band with the red tab, never straight over busy gameplay.
3. **Stray red vertical bars** appear at the left of several shots (≈14 s, 26 s, 36 s, 46 s). They look like the title-card red tab left on screen without its band. Either complete the header treatment (band + tab + yellow strip, entering and leaving) or remove it.
4. **"JADE / HOMING" vs "GILDED / INSTAGIB" split (≈33 s).** The top slice shows only scenery, with MICA outside the slice. The bottom slice's subject is barely readable. Reframe so each slice is centred on MICA mid-strike, padding the source horizontally if needed.
5. **End card:** the title text overlaps the HUD of the gameplay behind it. Blur or darken the background fully, or crop the HUD out.
6. **Carry slot:** use the real carry shot once `bugfix/ai-mt-carry-plc` merges (TALON lifting MICA in S3K).
7. **Check every split and grid still** for the subject inside its pane, and every header for whole-HUD clearance, before rendering.
