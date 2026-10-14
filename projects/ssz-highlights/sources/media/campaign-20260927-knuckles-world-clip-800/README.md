# SSZ2 Knuckles, corrected world clipping,800px

Candidate based on develop58001b58e. Full command and input hash in provenance.json.
Cold Knuckles solo, donor off, emeralds3333333, V-int410766.
8,704 inputs, no deaths, through both fights to the accepted pre-ending stop.
60fps,8,704 frames,145.066667s; full decode passed.
The complete state.csv is byte-identical to the prior same-input800 capture.
The shared finite-world clipping correction restores Plane A cloud texture wrapping while retaining physical world-edge clipping. Inspected4658/8156 have clouds and no black island gap.
This supersedes campaign-20260927-knuckles-glide-reset-800 for presentation. Native whole-scene pixel parity remains outside this engine recording.

Source integration: `49586cd86` on develop; integrated verification completed and pushed.

Delivery: runtime `49586cd86`, wide-route tests/inputs `38f799053`, pushed to develop.
Integrated full ordinary: 25,086 tests, no failures/errors, 29 reviewed skips;
guards: 672 tests, no failures/errors/skips. Permanent native/800px SOZ checks:
2 tests, no failures/errors/skips, 48 replay windows plus 18 semantic events each.
Task worktree and local branch removed after preserving final evidence.
