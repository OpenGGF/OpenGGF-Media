# Director's note — "One more go" (OpenGGF Multiplayer Time Attack, 81.8 s)

Film: `out/openggf-multiplayer-time-attack-promo.mp4`. Provenance: `PROVENANCE.md`.

## The idea

One race, told from your side: you type your name (in Japanese, 疾風の刃), pick a colour, wait in a
lobby you can actually play, die at the very first badnik while the pack leaps it, are racing again
3.8 seconds later, and lose a photo finish by 0.03 s — then everyone votes and the next zone is already
counting down. The end card asks the only question the film is built to make you answer: *One more go?*

Everything on screen is the real game driven through its real UI; every piece of type is the game's own
nameplate font (the face that floats over every ghost), so the title literally reads as a nameplate.

## The three sections I was least sure of

**1. Names in any language (13.8–26.6 s).**
- *Tried first:* a 4×2 grid of live crops, each tracking one rival's ghost through the race from the
  logged screen positions, labelled with the language. Rendered and rejected — the pack runs so tight that
  every cell showed the same clump of eight names; a viewer couldn't tell whose cell it was.
- *Considered:* per-beat punch-ins on each nameplate in full-screen race footage (eight names at 0.4–0.8 s
  each reads as frantic, the archive's most common rejection), and an editorial "name wall" typeset in the
  font (shows typography, not the game).
- *Chose:* a dedicated capture — eight relay peers stand in a line across the Sonic 1 lobby, each name in a
  different script above a differently coloured Sonic, the Ember hero in the middle, and each hero jump
  ripples outward down the line once per bar. Preceded by the game's own first-run prompt with 疾風の刃
  being typed (the prompt itself says "Other racers see it"), so the chain is *type it → everyone sees it*.
  The ripple is staged by the fixture (lobby presence replays the hero's poses with delays) and is recorded
  as such in the provenance. I first tried this over LAN; LAN hosts take four connections per address,
  so the line-up goes through the master relay, as a big real room would.

**2. Title face (7.4 s).**
- *Tried:* the Sonic 2 title-card font from the ROM (game-native, complete A–Z). At display size its
  split-stroke **M** reads "TI/ME" — the exact hazard the promo skill warns about.
- *Considered:* a heavy condensed TTF — clean, but generic and unrelated to the feature.
- *Chose:* the engine's `NameFont`, glyph-exact at 22× on a nameplate plate with the profile page's
  colour bar. It is the feature's own visual identity (names drawn in the game's pixel style), and the
  whole film's type system follows from it.

**3. "Your own look" and "the lobby is a level" (26.6–45.8 s).**
- The look beat's proof had a trap: in the profile take the lobby character keeps its old colours after
  SAVE (the look applies at the next run launch), so "save → watch your Sonic change in place" is not
  available. *Chose:* presets flicking one per beat (captured at 24-frame intervals so they land on the
  150-BPM grid) landing on Ember, then a slanted split of the hero in Ember at the S1, S2 and S3&K race
  starts — the claim "your look, in every game" is exactly what is on screen.
- *For lobby breadth I tried* full-width stacked strips (moving, jumping sprites leave a thin band, the hero
  kept leaving it) and briefly a second slanted split (too close to the look beat). *Chose:* three framed
  cells at about 2.1× that drop in on the beat, each showing the hero plus named ghosts in GHZ, EHZ and
  Hidden Palace, after one continuous take of the HPZ lobby: menu over the level → ready → the menu
  hides on the downbeat → play with the ghosts.

## Viewer pass (first-time viewer, final film)

How I watched: every 0.5 s of the final encode in contact sheets, full-resolution frames at each beat that
matters, every transition midpoint, and loudness/peak measurements. I cannot listen to audio or watch in
real time, so sound is judged by measurement and placement, not by ear — please give it one listen.

| Time | What's new on screen | What a first-time viewer feels / understands / might miss |
|---|---|---|
| 0–4 | A swarm of coloured Sonics with names in several scripts tearing through Green Hill; cut to black, the room panel "ROOM 9 PLAYERS / GET READY" pushes in. | Energy, then held breath. Understands "lots of racers, a room". Can't yet tell which Sonic is "you". |
| 4–8 | GO: the pack bursts off the line; "RACE TOGETHER. LIVE." | The promise lands at ~5 s. |
| 8–12 | Flash + Big Ring sting: MULTIPLAYER / TIME ATTACK / OpenGGF as a giant nameplate over the race. | Knows what this is and whose project. |
| 12–16 | Race continues, band wipe to the game's name prompt, 疾風の刃 typed letter by letter. | "You name yourself — in Japanese." |
| 16–20 | Nine Sonics in a row, eight names in eight scripts, language tags pop left→right, the first jump ripples. | Delight; the international point is obvious without reading a caption. |
| 20–24 | Header "YOUR NAME. ANY SCRIPT."; two more ripples. | Might linger slightly long; the ripple on each bar keeps it alive. |
| 24–28 | Back in the race, nameplates everywhere; wipe to the profile page; colours change on every beat. | Rhythm is satisfying; reads "pick a colour". |
| 28–32 | Lands on Ember; the orange Sonic drops in at Green Hill, Emerald Hill, Angel Island. | "My colour, in every game." Now knows the orange Sonic is *you*. |
| 32–36 | Hidden Palace lobby menu; the menu vanishes on the downbeat; "THE LOBBY IS A LEVEL". | The reveal works because the menu was in the way first. |
| 36–40 | Running and jumping around with three named ghosts in Hidden Palace. | Understands waiting is play. |
| 40–44 | Three lobby cells drop in: Sonic 1 / 2 / 3 & Knuckles. | Breadth; cells are smaller, so it's a glance, which is enough. |
| 44–48 | "NO LIVES. GO AGAIN."; hero (orange) racing in the pack. | Expectation: something is about to go wrong. |
| 48–52 | Rivals jump the Motobug, the hero doesn't — death; "JUMP SKIPS THE DEATH"; black; 3 · 2 · 1 with a timer counting. | Laughs at the death; the timer makes the speed concrete. |
| 52–56 | GO at "BACK IN 3.77s" with flash; hero chases; wipe to the room browser "255/256". | "That was fast." Switch to scale. |
| 56–60 | "ROOM 256 PLAYERS", a grey swarm of Bot nameplates, counter 256, CAPACITY TEST tag. | Gets "rooms can be huge" and that this was a test. |
| 60–64 | Gold-ring iris into the final stretch; "YOU" tag over the orange Sonic in the pack. | Knows where to look for the finish. |
| 64–68 | The whole pack piles toward the signpost. | Tension. |
| 68–72 | Flash at the signpost; push-in to "YOU 6/9 … NEW BEST"; standings: 风之子 0:53.63, 疾風の刃 0:53.66, "0.03s". | Lost by three hundredths — the hook. |
| 72–76 | Vote tally counting up; MARBLE ZONE card slams in with the room countdown. | "And the next one's already starting." |
| 76–82 | Badge, ONE MORE GO?, URL, status, disclaimer and the honesty line; fade. | Clear call to action; knows rivals were test clients. |

What I changed because of the passes:
- Replaced the tracked-crop names grid with the line-up capture (cells were indistinguishable).
- Re-timed the rival schedule (no drift) and re-captured the race so the finish is a real pack, not an
  empty signpost; the hero's colour changed from Violet to Ember because Violet read as stock blue.
- Shortened "Nguyễn Thị Hoa" to "Nguyễn Hoa" in all takes — the full name hit the 72-px nameplate limit
  and showed an ellipsis that looked like a glitch.
- Cold open: zoomed into the room's GET READY panel instead of holding a mostly black title card.
- Moved headers off the UI they covered (profile page → top right; lobby header now arrives when the menu
  hides), retimed "JUMP SKIPS THE DEATH" to appear while Sonic is dying rather than on the black reload.
- Name prompt framing no longer clips the first letter; the shot ends before the menu returns.
- 256 chapter: browser row framed full-width, CAPACITY TEST tag moved off the HUD, counter no longer
  under the header.
- Added the "YOU" tag in the line-up and the finish (the hero has no nameplate of their own).
- Mix: first master was +0.1 dBTP after AAC; final is two-pass loudnorm to −14.9 LUFS / −1.1 dBTP.

Known limits: the film was never watched at 1× or heard; the rival ripple, ghost timing and finishes are
fixture-driven (disclosed on the end card and in the provenance); compositor push-ins enlarge captured
frames (integer nearest-neighbour then area filter), so pixel edges soften slightly during the moves.

## Later revisions

The note above describes the first delivered cut. After review the editorial captions moved to a
separate display face, so the film's own voice no longer reads as game UI. The lobby, race HUD
(one TIME row with hundredths and a full-width progress bar) and every source take were also
re-captured against later engine builds. `PROVENANCE.md` records each revision and its reasons.
