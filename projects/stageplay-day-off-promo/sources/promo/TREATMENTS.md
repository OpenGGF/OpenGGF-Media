# Stageplay introduction film — treatments

Written 2026-10-24, before production, from the Stageplay skills, the authoring guide,
the editor picture tests and a scouting render of Green Hill 1, Angel Island 1 and
Emerald Hill 1. Engine worktree `feature/ai-sp-promo-a` at 632a5f8c3.

## A. "Day Off" — the first badnik takes the day off (chosen)

**Story.** Green Hill Zone, 9:00 AM. A Motobug, the first badnik Sonic ever met,
runs its patrol: forward, turn, forward, turn. Then it stops dead. "Thirty-five years
of this. I need a day off." It rolls off its beat and wanders away through the hills.
Sonic tears through the loop behind it, skids to a stop, turns back and stares:
"Aren't you supposed to be chasing me?" "Day off." "...Fair." He runs on. Wipe to
Sonic 3's Angel Island beach: the Motobug has gone on holiday to another game. The
island's guardian, Knuckles, drops in to throw it out ("No badniks on my island!"),
hears the answer, and grudgingly lets it stay. It ends at the water's edge with the
music swelling. A post-credits epilogue returns to Green Hill the next morning:
"Patrol. Turn. Patrol..." **How it introduces Stageplay.** The story's turning point
*is* Stageplay's central idea: the badnik starts **Free** (its real ROM AI patrolling
the real level) and the moment it rebels is the moment the director takes it over as
a **Puppet**. The vacation is the cross-game cast (an S1 object and S3K Knuckles on
an S3K set, or an S2 set if the object cast cannot cross games), and Sonic's
skid-and-turn gag is literally the route form's *Run / Hard stop / Face left*.
**Editor and film.** The promo opens on the finished film, uninterrupted, so the jokes
land first. On its last frame the picture shrinks back into the in-engine editor's
preview pane at the same frame ("every frame you just saw was directed here"), the
timeline rewinds, and one continuous director's session walks forward through the
same scene: the set, the cast and object clears, the Free→Puppet key, the camera
push, a dialogue line and its skin, the screenplay round trip and the desktop editor
open on the same file, then Export. The epilogue plays under the end card.
**Route line.** In the editor session Sonic's route is first planned at Walk: the line
climbs into the loop and ends in a red failure cross with the planner's own advice.
Switched to Run / Hard stop / Face left, the cyan line traces the whole loop; Apply,
Play, and Sonic runs exactly along it with the white actual-centre cross riding the
line, skids at the diamond and turns. The editor chrome then peels away at the same
frame into the clean film version of that run, with its sound.

## B. "Guest Star" — Knuckles lost in another game

**Story.** Sonic 3's Knuckles lands, bewildered, in Sonic 2's Emerald Hill. Sonic 2's
Tails finds him ("Angel Island? That's a whole game away!") and offers to walk him
home. A Buzzer blocks the path; Knuckles glides straight through it and a freed Flicky
flutters off. Tails takes the fast way through the loop; Knuckles, unimpressed,
glides over it. A wipe carries them to Angel Island, where Sonic skids up: "Where
have you two been?" **How it introduces Stageplay.** It is built on the brief's own
example: S3K Knuckles and S2 Tails sharing an S2 set, each moving under his own game's
rules, plus a native badnik interaction and two sets from two games. **Editor and film.**
Editor first: the promo builds the scene in the editor beat by beat (set, cast, glide
intent, route, dialogue), then hits Export and plays the finished film as the payoff.
**Route line.** Tails' loop route is planned and drawn, applied and played in the editor
before the film shows the same run full-screen. Not chosen: the build-up spends the
first half of the film on UI before the viewer cares about the characters, and a
"lost hero goes home" story is warmer but less memorable than A.

## C. "Scenic Route" — Sonic is late across three games

**Story.** Tails and Knuckles wait at the goal; Sonic is late because he took the
scenic route through Green Hill, Emerald Hill and Angel Island. Each leg is a quick
cross-game run; he finally skids in: "What? I took the scenic route." **How it
introduces Stageplay.** Three games' sets, a mixed cast and repeated route planning.
**Editor and film.** A split screen for the whole film: the editor plans each leg on the
left while the finished film runs it on the right. **Route line.** Every leg's line is
drawn before it is run. Not chosen: it is a race with a punchline rather than a story,
it repeats the same plan-then-run beat three times (the pattern the 2026-10-22
tutorial review rejected), and a permanent split leaves the editor too small to read.

## Why A

A has the strongest single idea a first-time viewer will remember (the oldest badnik
in Sonic wants a day off), and that idea is a true Stageplay mechanism rather than a
caption about one: Free is the ROM's own AI, Puppet is the director's hand. The film
plays first, so its jokes and reactions land before any interface appears; the
pull-back into the editor at the same frame then names the relationship between film
and editor in one continuous shot. Its route moment has a natural mini-story of its
own (fail, advice, fix, success) and its most striking picture, a planned line tracing
a loop, comes straight from Green Hill's real terrain.

Risks to check before committing, with fallbacks: whether an S1 object can be cast
on an S3K set (fallback: the holiday is in Sonic 2's Emerald Hill, or stays within
Green Hill); whether the route planner verifies a Run through the loop (fallback: a
hill crossing with a jump, drawn in gold); and how the Motobug's ROM animation reads
while directed (fallback: held frames and explicit facing keys).
