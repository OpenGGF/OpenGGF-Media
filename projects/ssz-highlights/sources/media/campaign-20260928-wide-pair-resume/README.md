# SSZ widescreen paired route resume checkpoint

Engine source b5a9990d1, integrated into develop as bdb318227. Cold SSZ Act 1, 800px, Sonic + Tails, donor off; ordinary controller inputs only. These are exploratory prefixes, not accepted complete routes.

- upper-transport: 17,371 inputs; receiving platform at (5376,3276), 98 rings, no deaths, Tails present.
- missing-return-bridge: 18,401 inputs. Resume around 17,876 before the turn, or inspect 18,120–18,140 for Sonic missing the uphill return bridge. Tails crossed and collapsed the diagonal bridges at (6016,2744) and (6144,2712) before Sonic returned. Both native-width and wide probes use layer 0, top bit 12 and side bit 13.

ROM loc_44DEC allows either player to trigger collapse: do not disable Tails. Separately, both engine flat and diagonal bridges derive collapse direction from the leader even when only P2 is riding. ROM loc_44C9C/loc_44CAA and loc_44E02/loc_44E10 select P1 if standing, otherwise P2. That mismatch is documented but unfixed. It does not fully explain this route blocker: the bridges expire before Sonic returns regardless of direction. Next work: focused participant-selection regression/fix and ordinary input authoring to preserve the return path.

The first and second replica videos and their exact inputs are preserved in the sibling campaign-20260928-paired-cold-first-replica-800 and campaign-20260928-paired-cold-second-replica-800 directories. The committed first-replica regression has 40 rewind windows; the full paired widescreen clear remains unfinished. Temporary probes and raw diagnostics were intentionally not archived.

Checkpoint update: first-replica fixture d27dd37c7 integrated as 19bc3ad239; destination TestSszWidePairedColdRouteCapture passed (1 test, 0 failures/errors/skips, 40 two-cycle rewind windows). Verification recorded in dfd74e979. Full paired widescreen clear remains unfinished; restart inputs and findings are in the sibling campaign-20260928-wide-pair-resume directory.
