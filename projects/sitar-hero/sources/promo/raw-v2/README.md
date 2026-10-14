# Sitar Hero promo sources (raw-v2)

Captured from the frozen polish candidate (see `provenance.txt` for the exact commit, mod
source hashes, ROM identities and commands). Each scenario is one `ExampleModCapture`
run: a script of inputs or scene debug jumps, a 60 fps 800x448 MP4 (400x224 at 2x,
nearest neighbour) and a WAV of the scene's own audio, one 800-sample packet per tick.

| Scenario | Script | What it shows |
|---|---|---|
| career | `career.script` | Title tableau on Angel Island, menu glide, Career → S3K tour → Angel Island intermission, ROM title card loading, count-in, Sonic on sitar |
| gh-bongos | `gh-bongos.script` | Sonic 1 Green Hill, Knuckles on bongos (Hard) |
| cpz-synth | `cpz-synth.script` | Sonic 2 Chemical Plant, Tails on synth (Hard) |
| lbz-harp | `lbz-harp.script` | Sonic 3 & Knuckles Launch Base 1, Robotnik on harp (Expert) |
| duel | `duel.script` | Local score duel on Sky Sanctuary, Mecha Sonic vs Robotnik on bongos |
| finale | `finale.script` | Sonic 2 Emerald Hill on sitar: Star Power, the end, results tally and jingle |
| outro | `outro.script` | Title tableau after two returns (venue rotation) |

All performances use the scene's tool-only autoplay, which the game labels **DEMO** on
screen and which never saves records. Loading time in these captures is not real time:
the capture loop does not pace ticks to the wall clock while ROM music renders on a
worker, so loading spans are cut. Offline audio shows content and cue timing, not
speaker latency.
