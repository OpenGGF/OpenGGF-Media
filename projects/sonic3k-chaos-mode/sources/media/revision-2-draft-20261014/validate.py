#!/usr/bin/env python3
"""Complete official change-based smoke selection with an admitted preflight.

Origin: Chaos revision/isolation coordination, 2026-10-14. Selection, batching,
timeouts and diagnostics remain owned by the unchanged repository runner. This
launcher also leases Java version preflight, then yields shared admission between
the runner's ordinary batches while retaining target/ ownership.
"""
from pathlib import Path
import sys

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / 'tools/testing'))
from run_categories import make_plan, policy, preflight, run_plan
from maven_queue import handle_termination, maven_slot, needs_exclusive, worktree_build_slot
from maven_schedule import plan_estimate

BASE = '5b2ff8e7851b99dd40998dfc41fbfd21c80031ef'


def main():
    plan = make_plan(ROOT, policy(ROOT), BASE, [], False, 1)
    print(f"Complete change-based smoke: {len(plan['tests'])} candidates; guards={plan['guards']}", flush=True)
    with handle_termination():
        with worktree_build_slot(ROOT) as tree_fd:
            with maven_slot(ROOT, tree_fd=tree_fd, exclusive=True, estimate=5,
                            kind='category-preflight'):
                preflight(ROOT, plan)
                print('Java25/Lua5.4/PowerShell preflight passed under shared admission.', flush=True)

            def admission(batch_plan, lane):
                return maven_slot(ROOT, tree_fd=tree_fd, exclusive=needs_exclusive([]),
                                  estimate=plan_estimate(batch_plan),
                                  kind='category-batch' if lane == 'ordinary' else 'category-guards')

            return run_plan(ROOT, plan, max_minutes=120,
                            rom_directory=Path('/home/farrell/code/projects/OpenGGF'),
                            admission=admission)


if __name__ == '__main__':
    sys.exit(main())
