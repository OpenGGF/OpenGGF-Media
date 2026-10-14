# Connected cold SOZ2 route attempt

Native 320-pixel Sonic + Tails, donor off, cold Act 2. Production omitted-title presentation and the initial ProcessSprites setup are consumed before frame 0. No gameplay state is written after boot.

`Input Log.txt` contains the exact full controller sequence. `state.csv` records every frame; `frames/` contains sparse PNGs at 30-frame intervals and command boundaries. The full input log is authoritative if a temporary prefix comment in `tail.script` is stale.

The first 1,500 inputs come from zero-based movie indices 365809–367308 of the original complete-emeralds BK2. Later inputs are authored. The original movie entered Act 2 seamlessly, so this is an adapted cold route, not a native trace replay. Native physics and auxiliary rows informed route planning only and never supplied gameplay state.

Runtime: compiled branch bfce36a2c, comprising root 306d7fe0f plus the final wire swing correction. Later integration fixes are not included in this recording.

The lower guide uses the existing `SozConnectedMechanismRoute` controller algorithm from root aa90938e9, then a temporary input-only recovery variant that returns to platform boarding after a missed jump and jumps immediately at x2830. These decisions produce ordinary controller inputs; every generated input is recorded.

This is bounded route evidence, not Act 2 completion. Failed tails and retries have separate directories. Both sand corks, vertical wrap, lower ascent, and the sand-room exit are connected in the `authored-act2-lower-exit-spikes` prefix through frame 19019.
