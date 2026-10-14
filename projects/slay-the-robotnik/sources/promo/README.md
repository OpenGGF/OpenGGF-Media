# Slay the Robotnik: promo

`promo.mp4` is an 86-second promo for general audiences. It is 1920x1080 at 60 fps, H.264 with
AAC audio. The chapter list is in `chapters.txt`.

It opens with Sonic 1, 2 and 3 & Knuckles side by side in OpenGGF, then shows off Slay the
Robotnik:
- the title screen, then hero select through to the ROM title card in one take;
- one take of a run: Hydrocity's map, landing on a badnik node, the fight and the victory;
- four bosses dropping in at once in a 2x2 grid;
- the slot machine, then eight more events at once;
- relics, items and upgrades in three rooms side by side, then the numbers;
- the "read from your own ROM" pitch, and the Mod API with the `hello-scene` starter;
- Mecha Sonic and Super Mecha Sonic, the final blow running straight into the victory screen, and
  the end card.

Short pieces share the screen in split layouts instead of being cut together. Banded wipes mark
chapter changes only, with 15 transitions in all.

## Provenance
- **Mod footage.** Recorded headless with `ExampleModCapture` from `feature/ai-slay-the-robotnik`
  at `25b57f886`. Every tick is saved as a lossless 400x224 PNG. Rooms, fights and events start
  from the mod's debug jumps; the title screen and hero select are played from the title.
  - The run take and the final fight use the debug `kill` command to end a fight.
  - Clip audio is sound effects only. The recorder uses copies of the mods in which music is
    stopped. Their visuals are unchanged (`tools/record.py`, `prepare_mods`).
  - Each recording copy also takes an `@act:floor:node` suffix on the debug jump. The stock jump
    starts every event at floor 0 of its earliest act, which is the Angel Island waterfall.
    With the suffix, events, rooms and fights stand deeper into Angel Island, Hydrocity and
    Launch Base, and bosses at the end of their act. Only acts each room can really appear in
    are used.
  - The title footage includes two title-screen fixes, committed on the branch after
    `25b57f886`: Knuckles glides forward, and the menu column's shade has no gap.
- **Engine footage.** Cut from the OpenGGF 0.6 promo masters in `~/Videos/OGGF/S1-0.6`,
  `S2-0.6` and `S3-0.6`, cropped to 16:9.
- **Soundtrack.** Rendered from the S3K ROM by OpenGGF's SMPS driver through a throwaway scene mod
  (`tools/render_audio.py`): Hydrocity Zone Act 2, then the Act Clear jingle, then Data Select
  under the end card.
  - Transitions use ROM sound effects: ring, spin dash, dash, Giant Ring, insta-shield and boss hit.
  - Cuts fall on Hydrocity Act 2's beats (171.1 BPM). Chapters sit on its section changes, found
    by `tools/beats.py` and `tools/novelty.py`.
- **Graphics.**
  - Section headers drop the ROM's own title-card banner (dumped by the scene tests to
    `target/scene-backdrops`), with motion modelled on `ObjArray_TtlCard`.
  - The end-card logo is redrawn from the mod's `art/font.txt` exactly as `TitleScreen.drawLogo`
    draws it.
  - Pixel art is scaled by nearest-neighbour to an integer multiple, then area-filtered to 1080p.

## Rebuild
`./make.sh` rebuilds everything in about five minutes. It:
1. creates a Python venv with numpy and Pillow;
2. renders the music and sound effects;
3. records 37 clips;
4. extracts the engine shots;
5. renders.

The edit itself is `tools/promo.py` (the `build()` timeline, in beats). Its subcommands:
- `sheet [step]` writes a contact sheet;
- `frames N...` writes single frames;
- `audio` mixes the soundtrack only;
- `render` writes the video.

The intermediate frames, stems and rendered tracks were deleted after the render; `make.sh`
regenerates them.
