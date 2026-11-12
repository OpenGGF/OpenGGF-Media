# MICA & TALON promo: lead direction (draft 2026-11-10)

Status: the brief for the promo lane, which starts after all art lanes have merged.

- **Audience:** general Sonic fans and would-be modders.
- **Form:** gameplay showcase. Every claim about play is shown in native-engine gameplay captured with `GameplayCaptureTool --mod <jar>`. The "how it was made" beat is editorial and is labelled as such.
- **Framing:** "an example built with OpenGGF's mod framework". It is not a release, and nothing says "download" ([[example-mods-are-framework-demos-not-releases]]). Use the post tag "Mod Showcase:".
- **Promise:** two original heroes, drawn frame by frame, playable in Sonic 1, 2 and 3&K.

## Selling points and their moving proof
1. **Original, not a recolour.**
   - Beat: a native Sonic pose enlarges, dissolves into the GPT redraw, then reduces to MICA's sprite, which starts running.
   - Then a three-step strip: model sheet → enlarged pose → sprite.
   - This is the mod's idea; give it a memorable beat of about 6 s.
2. **One character in three games.**
   - Slanted three-way split, with MICA running S1 GHZ / S2 EHZ / S3K AIZ.
   - Pill labels, slices dropping in on beats.
   - Pad and centre each slice on her (S1 slice lesson).
3. **MICA's homing attack.**
   - First use full screen: a reticle locks, then the missile-shaped dive.
   - Hero: a homing chain across several badniks, deep in an act, never at a level start.
   - Gilded Instagib only where 50+ rings is legitimate.
4. **TALON flies.**
   - Flapping flight, then hold down → reticle, then down+jump divebomb onto a badnik.
   - Solar form doubles the lift.
5. **A team.** MICA leads and TALON follows; S3K flight carry with TALON lifting MICA.
6. **They own every screen.**
   - A 4×2 grid popping one beat apart: HUD, signpost spin, results, S2 half-pipe, Blue Sphere, continue, data select, ending.
   - Cells must be at least 2.3× native scale.
7. **Built on the Mod API.**
   - A code panel typing `context.registerCharacter("mica", …)` beside the live view.
   - About 6 s.

## Shape
- **Cold open, 6 s:** the homing-chain fragment, then the line "Two new heroes."
- **Title drop:** a flash, Giant Ring stinger and slam. The title is set in the S3K title-card face, or the S2 one if S3K's lacks letters.
- **Chapters:** points 1–7 in that order, with ROM title-card banner headers and banded wipes only at chapter changes.
- **Climax:** Gilded MICA plus TALON clearing a section in one take into the act clear, with the results showing MICA's name.
- **End card:** the logo in game letterforms; "An example built with OpenGGF's mod framework"; the URL; "Fan-made and free. Not affiliated with SEGA. Requires your own ROM."

## Sound and format
- **Sound:**
  - One bed, rendered with `FmSfxRenderTool --paced`, S3K for the DAC drums. Candidate: S3K Launch Base 1 or Angel Island 2; pick by beat analysis.
  - Stingers at game level.
  - Jump sounds only on real take-offs.
- **Palette:** sampled from the model sheets (MICA jade #00926D, coral #FF4949; TALON slate #6D6D92, amber #FFB624) plus the S3K title-card band.
- **Format:**
  - A 16:9 master, about 75–90 s.
  - A separately composed 9:16 cut, with splits stacked vertically.
  - Archive both in OpenGGF-Media under `projects/mica-and-talon/`.

## Prepared by the lead (2026-11-10)
- **Venv** with numpy and Pillow: `~/scratch/agent-tmp/mt-promo-20261110/venv`.
- **Fonts:** `~/scratch/agent-tmp/mt-promo-20261110/fonts`, exported as `PROMO_FONT_DIRS`. Every role reports ok.
- **Beds**, rendered with `FmSfxRenderTool --paced` (DAC on), in `~/scratch/agent-tmp/mt-promo-20261110/music/`:

  | Track | BPM | First beat | Strong section changes |
  |---|---|---|---|
  | S3K LBZ1 (0D), **chosen** | 163.255 | 0.362 s | 12.86 s, 16.17 s, 61.74 s, 65.41 s, 73.13 s |
  | AIZ2 (02), alternative | 137.7 | | |

  LBZ1 is energetic and has strong intro→main and late-climax changes.
- **Capture recipe:** see `~/scratch/agent-tmp/mica-ingame-20261109/capture.py`.
  - Run `java -cp target/classes:<classpath> com.openggf.tools.GameplayCaptureTool --game G --zone Z --act N --main mica-and-talon:mica [--sidekick mica-and-talon:talon] --mod target/mica-and-talon/mica-and-talon.jar --input <log> ...` under surfaceless EGL.
  - Inputs are authored with `InputLogAuthorTool --script`.
  - The jar is built by `python3 examples/mica-and-talon/build.py`.
