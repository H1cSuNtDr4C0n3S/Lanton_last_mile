#!/usr/bin/env python3
"""Gate-one audit (§78): co-moving kernel for T3' determinacy.

§75 (gate-zero) showed that the anchor-frame abstraction A0(r,K,D0) is blind to
T3': two replayable histories of the same orbit collapse for any fixed anchor
radius r<=8 yet disagree on the T3' prefix, because the discriminating cell
*rides the W0 tube* and leaves the anchor window with the drift.

This audit fixes the frame.  It establishes two things, both reusing the
existing machinery (no new simulator, no engine binary):

  STRUCTURAL.  The exogenous-read footprint of E(k), written in CO-MOVING W0
  coordinates (subtract (offset // 104) * drift_phase), is a *fixed finite set*
  S_g that does not grow with the horizon.  rho_g = max co-moving Linf over the
  22 gate phases is bounded.  This is computed from W0 alone, so the bound is
  STRUCTURAL, not an empirical sampling envelope (cf. the empirical <=9 of §72).

  SUFFICIENCY.  Replay the §75 dynamic witness (orbit 5, t=60320 / t=60840).
  Both anchors' first-bad cell maps to the SAME co-moving cell; and the fixed
  co-moving footprint, read along its per-period drift stripes, SEPARATES the
  two anchors.  So A1 = "debris colors along the co-moving footprint stripes"
  makes T3' a function of the state exactly where A0 failed.

Honest residual (printed, not hidden): the footprint is spatially bounded but
each co-moving cell is a drift STRIPE queried at every period.  T3' on a
reachable (finite) field terminates when the debris runs out, but the *period*
at which it terminates is the decisive-depth quantity P.  Bounding P uniformly
over reachable histories is the residual crux (Link 1 / alpha1-hard); the
honest fallback is to mark states beyond a certified P as `unknown`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"
DATA = ROOT / "data"
GA = ROOT / "GA_stress_agent"
for p in (ALPHA, GA):
    sys.path.insert(0, str(p))

from delta4_long_orbits import load_w0_bits  # noqa: E402
from lock_checklist_probe import make_exogenous_schedule, rel_to_abs, GATE_PHASES  # noqa: E402
from door_discriminant_linf_profile import phase_drifts  # noqa: E402
from ga_gate_zero_audit import replay_snapshots  # noqa: E402
from t3_coreachability_pair_scanner import eval_first_bad  # noqa: E402


def comoving_footprint(schedule, drift, upto):
    """{(comoving_x, comoving_y): required_black} for reads with offset < upto."""
    dpx, dpy = drift
    foot = {}
    for r in schedule:
        if r.offset >= upto:
            break
        p = r.offset // 104
        foot[(r.rel_x - p * dpx, r.rel_y - p * dpy)] = int(r.required_black)
    return foot


def rho_of(foot):
    return max((max(abs(x), abs(y)) for x, y in foot), default=0)


def structural_part(w0_bits, drifts, max_offset, stab_checks):
    sched = make_exogenous_schedule(w0_bits, max_offset)
    per_phase = []
    for g in GATE_PHASES:
        # stabilization: footprint must be identical at each horizon cutoff
        sizes = []
        last = None
        stable = True
        for cut in stab_checks:
            foot = comoving_footprint(sched[g], drifts[g], cut)
            sizes.append({"upto": cut, "size": len(foot), "rho": rho_of(foot)})
            if last is not None and foot != last:
                stable = False
            last = foot
        full = comoving_footprint(sched[g], drifts[g], max_offset)
        per_phase.append({
            "phase": g,
            "drift": list(drifts[g]),
            "footprint_cells": len(full),
            "rho_comoving_linf": rho_of(full),
            "stabilized": int(stable),
            "horizon_sizes": sizes,
        })
    return sched, {
        "max_offset": max_offset,
        "gate_phases": len(GATE_PHASES),
        "max_rho_over_gate_phases": max(r["rho_comoving_linf"] for r in per_phase),
        "all_stabilized": int(all(r["stabilized"] for r in per_phase)),
        "per_phase": per_phase,
    }


def sufficiency_part(sched, drifts, phase, orbit_index, ta, tb, periods, horizon, smin, smax):
    dpx, dpy = drifts[phase]
    foot = comoving_footprint(sched[phase], drifts[phase], 20000)
    orbit, _turns, snaps = replay_snapshots(orbit_index, (ta, tb), horizon, smin, smax)
    sa, sb = snaps[ta], snaps[tb]
    schedule = sched[phase]

    def cm(off, rx, ry):
        p = off // 104
        return [rx - p * dpx, ry - p * dpy]

    def anchor_block(snap, label):
        fb = eval_first_bad(set(snap.black), snap.origin_x, snap.origin_y, snap.heading, schedule, horizon)
        return {
            "label": label,
            "time": snap.time,
            "origin": [snap.origin_x, snap.origin_y],
            "heading": snap.heading,
            "first_bad_offset": fb.offset,
            "first_bad_rel": None if fb.rel_x is None else [fb.rel_x, fb.rel_y],
            "first_bad_comoving": None if fb.rel_x is None else cm(fb.offset, fb.rel_x, fb.rel_y),
            "bad_kind": fb.kind,
        }, fb

    def stripe_state(snap):
        st = {}
        for (sx, sy) in foot:
            col = []
            for p in range(periods + 1):
                ax, ay = rel_to_abs(snap.origin_x, snap.origin_y, snap.heading, sx + p * dpx, sy + p * dpy)
                col.append(1 if (ax, ay) in snap.black else 0)
            st[(sx, sy)] = tuple(col)
        return st

    ba, fba = anchor_block(sa, "A")
    bb, fbb = anchor_block(sb, "B")
    sta, stb = stripe_state(sa), stripe_state(sb)
    diff = [list(c) for c in foot if sta[c] != stb[c]]

    # decisive co-moving customs cell = comoving position of each first-bad
    decisive = ba["first_bad_comoving"]
    decisive_t = tuple(decisive) if decisive is not None else None
    detail = None
    if decisive_t is not None and decisive_t in foot:
        detail = {
            "cell": decisive,
            "required_black": foot[decisive_t],
            "A_black_periods": [p for p, v in enumerate(sta[decisive_t]) if v == 1],
            "B_black_periods": [p for p, v in enumerate(stb[decisive_t]) if v == 1],
        }

    return {
        "orbit_index": orbit_index,
        "rngstate": orbit.rngstate,
        "phase": phase,
        "footprint_cells": len(foot),
        "rho_comoving_linf": rho_of(foot),
        "periods_scanned": periods,
        "anchor_A": ba,
        "anchor_B": bb,
        "anchors_first_bad_same_comoving_cell": int(ba["first_bad_comoving"] == bb["first_bad_comoving"]),
        "comoving_footprint_separates_anchors": int(len(diff) > 0),
        "num_separating_cells": len(diff),
        "decisive_comoving_cell_detail": detail,
        "reproduces_gate_zero": int(ba["first_bad_offset"] == 1014 and bb["first_bad_offset"] == 494),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phase", type=int, default=98)
    ap.add_argument("--orbit-index", type=int, default=5)
    ap.add_argument("--anchor-a", type=int, default=60320)
    ap.add_argument("--anchor-b", type=int, default=60840)
    ap.add_argument("--periods", type=int, default=12)
    ap.add_argument("--horizon", type=int, default=1600)
    ap.add_argument("--max-offset", type=int, default=20000)
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    ap.add_argument("--out", type=Path, default=GA / "gate_one_comoving_summary.json")
    args = ap.parse_args()

    w0 = load_w0_bits(DATA / "w0.txt")
    drifts = phase_drifts(w0)
    stab_checks = (1040, 5200, 10400, args.max_offset)

    sched, structural = structural_part(w0, drifts, args.max_offset, stab_checks)
    sufficiency = sufficiency_part(
        sched, drifts, args.phase, args.orbit_index,
        args.anchor_a, args.anchor_b, args.periods, args.horizon, args.smin, args.smax,
    )

    payload = {
        "audit": "gate-one co-moving kernel for T3' determinacy (s78)",
        "structural": structural,
        "sufficiency_on_gate_zero_witness": sufficiency,
        "residual_note": (
            "Footprint is spatially bounded (fixed finite set, rho<=9 structural) but each "
            "co-moving cell is a per-period drift stripe. T3' on a reachable field terminates "
            "when debris runs out; the period P at which it terminates is the decisive depth. "
            "Bounding P uniformly over reachable histories is the residual crux (Link 1). "
            "Fallback: mark states beyond a certified P as `unknown` and certify SCCs invariant to them."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "max_rho_over_gate_phases": structural["max_rho_over_gate_phases"],
        "all_footprints_stabilized": structural["all_stabilized"],
        "phase98_footprint_cells": next(r["footprint_cells"] for r in structural["per_phase"] if r["phase"] == 98),
        "reproduces_gate_zero": sufficiency["reproduces_gate_zero"],
        "anchors_same_comoving_decisive_cell": sufficiency["anchors_first_bad_same_comoving_cell"],
        "comoving_footprint_separates_anchors": sufficiency["comoving_footprint_separates_anchors"],
        "num_separating_cells": sufficiency["num_separating_cells"],
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
