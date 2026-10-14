# DDZ Hyper sparkle phase — 2026-09-25

Native: BizHawk 2.11/GPGX, locked-on verified S3K ROM, existing movie-entry
save514214. No gameplay RAM writes; movie stopped after loading its own state,
then neutral input through180 updates. Native host.json identifies all sources.
Native slot rows observe post-frame state at CD7C + child*$4A.
Engine: ordinary GameplayCaptureSession DDZ boot, native Sonic solo,320px,
seven Super Emeralds declared before stepping, neutral inputs. No native rows
feed engine state. Gameplay boot consumes one initial non-gameplay step;
engine pass n+1 is aligned with native pass n. The native save carries its
camera fraction and score; this fresh engine setup does not. No whole-scene
pixel or trajectory parity claim.

engine/ is before the fix; engine-queued/ is with the real module submission
and init-only readiness gate. Native first child starts at52, others53/54/55.
506 initialized child rows match frame, timer, angle and both accumulators
exactly after the fix. The native queue is nonempty on50, ready by51; Init
first observes completion on52. The pre-fix engine ran two gameplay ticks early.

comparison.mp4: native left, corrected engine right,180frames at60fps (3sec),
nearest-neighbour2x. Full decode checked. Selected moving-sequence frames were
inspected; HUD score/rings differences remain visible and are outside this fix.
Exporter and temporary Java probe are diagnostic artifacts, not runtime assets.
