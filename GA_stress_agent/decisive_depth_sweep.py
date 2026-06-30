#!/usr/bin/env python3
"""Decisive-depth sweep (§78.7): does the co-moving period P of the T3' verdict
grow with T or saturate?

For every gate-lock attempt in each long orbit, evaluate the T3' checklist at the
attempt's ACTUAL phase at a LARGE horizon (so the decisive period is not censored
at the §72/§66 cap of 1600 = period 15), and record P = first_bad_offset // 104.

Two views, mirroring §30:
  within-orbit : running-max P vs time_frac; does the last 30% of attempts bring a
                 new running-max (P still rising) -- the §30 kill-shot, but on the
                 RIGHT quantity (co-moving customs depth, not raw stall length).
  cross-orbit  : max P vs onset (T).  Caveat: the 24 orbits are selected for high
                 onset (251k-313k, narrow band) -> survivorship; within-orbit is
                 the cleaner signal.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"
DATA = ROOT / "data"
sys.path.insert(0, str(ALPHA))

from delta4_long_orbits import DX, DY, LOCK_THRESHOLDS, build_seed, load_w0_bits, parse_dumps, simulate_orbit  # noqa: E402
from lock_checklist_probe import (  # noqa: E402
    GATE_PHASES,
    Lock,
    lock_occurrences,
    make_exogenous_schedule,
)
from t3_coreachability_pair_scanner import eval_first_bad  # noqa: E402


def gate_locks_for_orbit(turns, onset, w0_bits, idx):
    seen = {}
    for thr in LOCK_THRESHOLDS:
        for lk in lock_occurrences(turns, onset, w0_bits, thr, idx):
            if not lk.is_gate:
                continue
            k = (lk.start, lk.phase)
            if k not in seen or lk.depth > seen[k].depth:
                seen[k] = lk
    return sorted(seen.values(), key=lambda l: (l.start, l.phase))


def sweep_orbit(orbit, w0_bits, schedules, horizon, smin, smax):
    turns, _deep, _bites, _side, _dens = simulate_orbit(orbit.rngstate, orbit.onset_dump, smin, smax, horizon)
    locks = gate_locks_for_orbit(turns, orbit.onset_dump, w0_bits, orbit.index)
    by_start = defaultdict(list)
    for lk in locks:
        by_start[lk.start].append(lk)

    black, _s, _d = build_seed(orbit.rngstate, smin, smax)
    x = y = h = 0
    rows = []
    for t in range(orbit.onset_dump + 1):
        for lk in by_start.get(t, ()):
            kind = "entry" if lk.start == orbit.onset_dump else "pre_onset"
            fb = eval_first_bad(black, x, y, h, schedules[lk.phase], horizon)
            clears = fb.offset is None
            rows.append({
                "idx": orbit.index,
                "onset": orbit.onset_dump,
                "start": lk.start,
                "time_frac": lk.start / orbit.onset_dump,
                "phase": lk.phase,
                "depth": lk.depth,
                "kind": kind,
                "first_bad_offset": fb.offset,
                "decisive_period": None if clears else fb.offset // 104,
                "clears": int(clears),
            })
        cell = (x, y)
        if cell in black:
            black.discard(cell)
            h = (h + 3) & 3
        else:
            black.add(cell)
            h = (h + 1) & 3
        x += DX[h]
        y += DY[h]
    return rows


def last_frac_kicks(rows, frac=0.30):
    """For one orbit's failing attempts sorted by time, does the last `frac`
    fraction of attempts bring a new running-max decisive_period?"""
    fails = sorted([r for r in rows if r["decisive_period"] is not None], key=lambda r: r["time_frac"])
    if len(fails) < 4:
        return None
    cut = int(len(fails) * (1 - frac))
    head_max = max(r["decisive_period"] for r in fails[:cut])
    tail_max = max(r["decisive_period"] for r in fails[cut:])
    return {
        "n_fail": len(fails),
        "head_max_P": head_max,
        "tail_max_P": tail_max,
        "tail_sets_new_max": int(tail_max > head_max),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--horizon", type=int, default=10400, help="max offset (periods*104); 10400=100 periods")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    ap.add_argument("--out", type=Path, default=ROOT / "GA_stress_agent" / "decisive_depth_summary.json")
    ap.add_argument("--rows-out", type=Path, default=ROOT / "GA_stress_agent" / "decisive_depth_rows.csv")
    args = ap.parse_args()

    w0 = load_w0_bits(DATA / "w0.txt")
    schedules = make_exogenous_schedule(w0, args.horizon + 1)
    dumps = parse_dumps(ALPHA / "dumps_all.txt")

    all_rows = []
    per_orbit = []
    for orbit in dumps:
        rows = sweep_orbit(orbit, w0, schedules, args.horizon, args.smin, args.smax)
        all_rows.extend(rows)
        fails = [r for r in rows if r["decisive_period"] is not None]
        kick = last_frac_kicks(rows)
        per_orbit.append({
            "idx": orbit.index,
            "onset": orbit.onset_dump,
            "n_gate_attempts": len(rows),
            "n_fail": len(fails),
            "max_P": max((r["decisive_period"] for r in fails), default=None),
            "p95_P": (sorted(r["decisive_period"] for r in fails)[int(0.95 * (len(fails) - 1))] if fails else None),
            "kick": kick,
        })

    fails = [r for r in all_rows if r["decisive_period"] is not None]
    Ps = sorted(r["decisive_period"] for r in fails)
    n = len(Ps)
    # censoring check: how many fail beyond period 15 (the old horizon-1600 ceiling)?
    beyond15 = sum(1 for p in Ps if p > 15)
    near_horizon = sum(1 for r in fails if r["first_bad_offset"] is not None and r["first_bad_offset"] > args.horizon - 104)

    # cross-orbit correlation max_P vs onset
    xs = [o["onset"] for o in per_orbit if o["max_P"] is not None]
    ys = [o["max_P"] for o in per_orbit if o["max_P"] is not None]
    if len(xs) >= 3 and len(set(ys)) > 1:
        try:
            corr = statistics.correlation(xs, ys)
        except Exception:
            corr = None
    else:
        corr = None

    kicks = [o["kick"] for o in per_orbit if o["kick"]]
    n_tail_new_max = sum(k["tail_sets_new_max"] for k in kicks)

    summary = {
        "audit": "decisive co-moving depth P sweep (s78.7)",
        "horizon": args.horizon,
        "horizon_periods": args.horizon // 104,
        "n_orbits": len(per_orbit),
        "n_gate_attempts": len(all_rows),
        "n_failing_attempts": n,
        "P_distribution": {
            "min": Ps[0] if n else None,
            "median": Ps[n // 2] if n else None,
            "p95": Ps[int(0.95 * (n - 1))] if n else None,
            "max": Ps[-1] if n else None,
        },
        "censoring_check": {
            "old_ceiling_period": 15,
            "n_fail_beyond_period_15": beyond15,
            "frac_beyond_15": round(beyond15 / n, 4) if n else None,
            "n_fail_near_new_horizon": near_horizon,
            "note": "n_fail_beyond_period_15 > 0 means the §72/§66 horizon-1600 cap WAS censoring P.",
        },
        "within_orbit_kill_shot": {
            "n_orbits_assessed": len(kicks),
            "n_orbits_tail_sets_new_max": n_tail_new_max,
            "frac_tail_sets_new_max": round(n_tail_new_max / len(kicks), 4) if kicks else None,
            "note": "fraction of orbits where the last 30% of attempts pushes a new running-max P (still rising = bad for a uniform cap).",
        },
        "cross_orbit": {
            "onset_range": [min(o["onset"] for o in per_orbit), max(o["onset"] for o in per_orbit)],
            "max_P_per_orbit_range": [min(ys) if ys else None, max(ys) if ys else None],
            "corr_maxP_vs_onset": None if corr is None else round(corr, 3),
            "caveat": "orbits selected for high onset (narrow T band) -> survivorship; treat cross-orbit as weak.",
        },
        "per_orbit": per_orbit,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    # rows csv
    import csv
    with args.rows_out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        w.writerows(all_rows)

    print(json.dumps({
        "horizon_periods": summary["horizon_periods"],
        "n_failing_attempts": n,
        "P_max": summary["P_distribution"]["max"],
        "P_p95": summary["P_distribution"]["p95"],
        "P_median": summary["P_distribution"]["median"],
        "n_fail_beyond_period_15": beyond15,
        "n_fail_near_new_horizon": near_horizon,
        "orbits_tail_sets_new_max": f"{n_tail_new_max}/{len(kicks)}",
        "corr_maxP_vs_onset": summary["cross_orbit"]["corr_maxP_vs_onset"],
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
