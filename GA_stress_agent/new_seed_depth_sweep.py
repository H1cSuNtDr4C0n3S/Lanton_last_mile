#!/usr/bin/env python3
"""Decisive-depth sweep on harvested NEW high-onset seeds (§78.11).

Tail-envelope stress test for the budget P: does P exceed 15 on an INDEPENDENT
sample, outside the 24 onset-selected orbits?

Seeds come from `new_high_onset_seeds.csv` (harvested by alpha1_engine `search`,
validated: empty grid -> onset 9977, (7,-7) -> onset 106258).  Each row is
(onset, side, dens, rngstate); the Python pipeline reproduces the orbit from
rngstate (same build_seed / xorshift as the C engine).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "alpha1"))
sys.path.insert(0, str(ROOT / "GA_stress_agent"))

from delta4_long_orbits import load_w0_bits  # noqa: E402
from lock_checklist_probe import make_exogenous_schedule  # noqa: E402
from decisive_depth_sweep import sweep_orbit  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds", type=Path, default=ROOT / "GA_stress_agent" / "new_high_onset_seeds.csv")
    ap.add_argument("--top", type=int, default=70, help="evaluate the N highest-onset seeds")
    ap.add_argument("--horizon", type=int, default=5200)
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    ap.add_argument("--out", type=Path, default=ROOT / "GA_stress_agent" / "new_seeds_depth_summary.json")
    args = ap.parse_args()

    seeds = []
    with args.seeds.open() as f:
        for row in csv.DictReader(f):
            seeds.append((int(row["onset"]), int(row["side"]), float(row["dens"]), int(row["rngstate"])))
    seeds.sort(reverse=True)
    seeds = seeds[: args.top]

    w0 = load_w0_bits(ROOT / "data" / "w0.txt")
    sched = make_exogenous_schedule(w0, args.horizon + 1)

    Ps = []
    per_seed = []
    for i, (onset, side, dens, rng) in enumerate(seeds):
        orbit = SimpleNamespace(index=10000 + i, shard=0, onset_dump=onset, rngstate=rng)
        rows = sweep_orbit(orbit, w0, sched, args.horizon, args.smin, args.smax)
        fails = [r["decisive_period"] for r in rows if r["decisive_period"] is not None]
        Ps.extend(fails)
        per_seed.append({"rngstate": rng, "onset": onset, "n_fail": len(fails),
                         "max_P": max(fails, default=None)})

    Ps.sort()
    n = len(Ps)
    summary = {
        "audit": "decisive-depth on NEW high-onset seeds (s78.11)",
        "horizon": args.horizon,
        "n_seeds": len(seeds),
        "onset_range": [seeds[-1][0], seeds[0][0]],
        "n_failing_attempts": n,
        "P_distribution": {"min": Ps[0], "median": Ps[n // 2], "p95": Ps[int(0.95 * (n - 1))], "max": Ps[-1]},
        "n_fail_beyond_period_15": sum(1 for p in Ps if p > 15),
        "period_histogram": dict(sorted(Counter(Ps).items())),
        "per_seed": per_seed,
    }
    args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in
                      ("n_seeds", "onset_range", "n_failing_attempts", "P_distribution",
                       "n_fail_beyond_period_15", "period_histogram")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
