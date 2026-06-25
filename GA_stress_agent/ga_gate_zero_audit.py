#!/usr/bin/env python3
"""Gate-zero audit for the GA/no-entry stress test.

This script deliberately does not build a new large automaton.  It checks the
first obstruction requested in the handoff: whether the T3' checklist verdict is
determined by a finite abstract state A(r,K,D0).

The audit has two parts:
  1. dynamic_prefix: replay the section 71 co-reachable witness from existing
     long-orbit data.  Two reached histories collapse for r <= 8 and for any
     K,D0 capped at <= 494, but h_g^L differs.
  2. syntactic_prefix: construct two finite debris fields with the same local
     patch and the same capped lock prefix, differing only on one T3' read
     outside the radius.  This is not a reachability claim; it is a sanity check
     for the abstraction itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"
DATA = ROOT / "data"
sys.path.insert(0, str(ALPHA))

from delta4_long_orbits import DX, DY, build_seed, load_w0_bits, parse_dumps, simulate_orbit  # noqa: E402
from lock_checklist_probe import make_exogenous_schedule, rel_to_abs  # noqa: E402
from t3_coreachability_pair_scanner import (  # noqa: E402
    eval_first_bad,
    h_for_horizon,
    local_patch_bytes,
    patch_digest,
)


DEFAULT_ORBIT_INDEX = 5
DEFAULT_PHASE = 98
DEFAULT_ANCHOR_A = 60320
DEFAULT_ANCHOR_B = 60840


@dataclass(frozen=True)
class Snapshot:
    time: int
    origin_x: int
    origin_y: int
    heading: int
    observed_turn_bit: int
    black: frozenset[tuple[int, int]]


def parse_int_list(text: str) -> tuple[int, ...]:
    values = tuple(sorted({int(part.strip()) for part in text.split(",") if part.strip()}))
    if not values:
        raise ValueError("empty integer list")
    return values


def replay_snapshots(
    orbit_index: int,
    times: Iterable[int],
    horizon: int,
    smin: int,
    smax: int,
) -> tuple[object, list[int], dict[int, Snapshot]]:
    times = tuple(sorted(times))
    max_time = max(times)
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    orbit = dumps[orbit_index]
    tail_steps = max(horizon, max(0, max_time - orbit.onset_dump + horizon))
    turns, _deep, _bites, _side, _dens = simulate_orbit(
        orbit.rngstate,
        orbit.onset_dump,
        smin,
        smax,
        tail_steps,
    )

    black, _side2, _dens2 = build_seed(orbit.rngstate, smin, smax)
    x = y = h = 0
    out: dict[int, Snapshot] = {}
    wanted = set(times)
    for t in range(max_time + 1):
        if t in wanted:
            out[t] = Snapshot(
                time=t,
                origin_x=x,
                origin_y=y,
                heading=h,
                observed_turn_bit=0 if (x, y) in black else 1,
                black=frozenset(black),
            )
        if t == max_time:
            break
        cell = (x, y)
        if cell in black:
            black.remove(cell)
            h = (h + 3) & 3
        else:
            black.add(cell)
            h = (h + 1) & 3
        x += DX[h]
        y += DY[h]
    return orbit, turns, out


def phase_match_depth(turns: list[int], start: int, w0_bits: list[int], phase: int, cap: int) -> int:
    depth = 0
    limit = min(len(turns) - start, cap)
    while depth < limit and turns[start + depth] == w0_bits[(phase + depth) % 104]:
        depth += 1
    return depth


def abstract_state(
    snap: Snapshot,
    turns: list[int] | None,
    w0_bits: list[int],
    radius: int,
    phase: int,
    K: int,
    D0: int,
    forced_depth: int | None = None,
) -> dict[str, object]:
    patch = local_patch_bytes(
        set(snap.black),
        snap.origin_x,
        snap.origin_y,
        snap.heading,
        radius,
    )
    if forced_depth is None:
        if turns is None:
            raise ValueError("turns required unless forced_depth is supplied")
        depth = phase_match_depth(turns, snap.time, w0_bits, phase, max(K, D0, 2000) + 1)
    else:
        depth = forced_depth
    return {
        "radius": radius,
        "patch_hash": patch_digest(patch),
        "patch_bytes": len(patch),
        "observed_turn_bit": snap.observed_turn_bit,
        "eval_phase": phase,
        "tail_prefix_cap_K": min(depth, K),
        "lock_depth_cap_D0": min(depth, D0),
        "deep_lock_flag": int(depth >= D0),
    }


def t3_row(
    snap: Snapshot,
    schedule,
    horizons: tuple[int, ...],
) -> dict[str, object]:
    fb = eval_first_bad(
        set(snap.black),
        snap.origin_x,
        snap.origin_y,
        snap.heading,
        schedule,
        max(horizons),
    )
    row: dict[str, object] = {
        "first_bad_offset": fb.offset,
        "first_bad_rel": None if fb.rel_x is None else [fb.rel_x, fb.rel_y],
        "first_bad_linf": None if fb.rel_x is None else max(abs(fb.rel_x), abs(fb.rel_y)),
        "required_black": None if fb.required_black is None else int(bool(fb.required_black)),
        "actual_black": None if fb.actual_black is None else int(bool(fb.actual_black)),
        "bad_kind": fb.kind,
    }
    for horizon in horizons:
        h = h_for_horizon(fb, horizon)
        row[f"h_{horizon}"] = h
        row[f"clear_{horizon}"] = int(h == horizon + 1)
    return row


def dynamic_prefix_audit(args, w0_bits: list[int], schedules) -> dict[str, object]:
    orbit, turns, snaps = replay_snapshots(
        args.orbit_index,
        (args.anchor_a, args.anchor_b),
        max(args.horizons),
        args.smin,
        args.smax,
    )
    snap_a = snaps[args.anchor_a]
    snap_b = snaps[args.anchor_b]
    rows = []
    for radius in args.radii:
        state_a = abstract_state(snap_a, turns, w0_bits, radius, args.phase, args.K, args.D0)
        state_b = abstract_state(snap_b, turns, w0_bits, radius, args.phase, args.K, args.D0)
        rows.append(
            {
                "radius": radius,
                "same_abstract_state": int(state_a == state_b),
                "state_a": state_a,
                "state_b": state_b,
            }
        )
    depth_a = phase_match_depth(turns, snap_a.time, w0_bits, args.phase, max(args.horizons) + 1)
    depth_b = phase_match_depth(turns, snap_b.time, w0_bits, args.phase, max(args.horizons) + 1)
    t3_a = t3_row(snap_a, schedules[args.phase], args.horizons)
    t3_b = t3_row(snap_b, schedules[args.phase], args.horizons)
    return {
        "kind": "dynamic_prefix",
        "claim_scope": (
            "reachable histories; proves non-determinacy of finite T3 prefix h_g^L "
            "for collapsed states, not binary infinite entry/non-entry"
        ),
        "orbit_index": args.orbit_index,
        "rngstate": orbit.rngstate,
        "phase": args.phase,
        "K": args.K,
        "D0": args.D0,
        "anchors": [
            {
                "label": "A",
                "time": snap_a.time,
                "origin": [snap_a.origin_x, snap_a.origin_y],
                "heading": snap_a.heading,
                "observed_turn_bit": snap_a.observed_turn_bit,
                "phase_match_depth": depth_a,
                "t3": t3_a,
            },
            {
                "label": "B",
                "time": snap_b.time,
                "origin": [snap_b.origin_x, snap_b.origin_y],
                "heading": snap_b.heading,
                "observed_turn_bit": snap_b.observed_turn_bit,
                "phase_match_depth": depth_b,
                "t3": t3_b,
            },
        ],
        "state_comparison_by_radius": rows,
    }


def syntactic_prefix_audit(args, w0_bits: list[int], schedules) -> dict[str, object]:
    radius = args.synthetic_radius
    horizon = max(args.horizons)
    schedule = schedules[args.phase]

    chosen = None
    floor_offset = max(radius, args.K, args.D0)
    for read in schedule:
        if read.offset <= floor_offset:
            continue
        if read.offset > horizon:
            break
        if read.required_black:
            continue
        if max(abs(read.rel_x), abs(read.rel_y)) > radius:
            chosen = read
            break
    if chosen is None:
        raise RuntimeError("no synthetic white discriminator found within horizon")

    pass_black: set[tuple[int, int]] = set()
    for read in schedule:
        if read.offset > horizon:
            break
        if read.required_black:
            pass_black.add(rel_to_abs(0, 0, 0, read.rel_x, read.rel_y))
    fail_black = set(pass_black)
    fail_black.add(rel_to_abs(0, 0, 0, chosen.rel_x, chosen.rel_y))

    snap_pass = Snapshot(
        time=0,
        origin_x=0,
        origin_y=0,
        heading=0,
        observed_turn_bit=0 if (0, 0) in pass_black else 1,
        black=frozenset(pass_black),
    )
    snap_fail = Snapshot(
        time=0,
        origin_x=0,
        origin_y=0,
        heading=0,
        observed_turn_bit=0 if (0, 0) in fail_black else 1,
        black=frozenset(fail_black),
    )
    forced_pass_depth = horizon + 1
    forced_fail_depth = chosen.offset
    state_pass = abstract_state(
        snap_pass, None, w0_bits, radius, args.phase, args.K, args.D0, forced_depth=forced_pass_depth
    )
    state_fail = abstract_state(
        snap_fail, None, w0_bits, radius, args.phase, args.K, args.D0, forced_depth=forced_fail_depth
    )
    return {
        "kind": "syntactic_prefix",
        "claim_scope": (
            "finite debris fields; proves the abstraction is blind unless it stores "
            "the relevant T3 cells; not a co-reachability claim"
        ),
        "radius": radius,
        "phase": args.phase,
        "K": args.K,
        "D0": args.D0,
        "horizon": horizon,
        "discriminator": {
            "offset": chosen.offset,
            "rel": [chosen.rel_x, chosen.rel_y],
            "linf": max(abs(chosen.rel_x), abs(chosen.rel_y)),
            "required_black": int(bool(chosen.required_black)),
        },
        "same_abstract_state": int(state_pass == state_fail),
        "state_pass": state_pass,
        "state_fail": state_fail,
        "pass_field_black_cells": len(pass_black),
        "fail_field_black_cells": len(fail_black),
        "t3_pass": t3_row(snap_pass, schedule, args.horizons),
        "t3_fail": t3_row(snap_fail, schedule, args.horizons),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--radii", default="2,3,4,8,9")
    ap.add_argument("--synthetic-radius", type=int, default=8)
    ap.add_argument("--K", type=int, default=80)
    ap.add_argument("--D0", type=int, default=80)
    ap.add_argument("--phase", type=int, default=DEFAULT_PHASE)
    ap.add_argument("--horizons", default="512,1600")
    ap.add_argument("--orbit-index", type=int, default=DEFAULT_ORBIT_INDEX)
    ap.add_argument("--anchor-a", type=int, default=DEFAULT_ANCHOR_A)
    ap.add_argument("--anchor-b", type=int, default=DEFAULT_ANCHOR_B)
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    ap.add_argument("--out", type=Path, default=ROOT / "GA_stress_agent" / "gate_zero_summary.json")
    args = ap.parse_args()

    args.radii = parse_int_list(args.radii)
    args.horizons = parse_int_list(args.horizons)
    if args.K < 0 or args.D0 <= 0:
        raise ValueError("K must be >=0 and D0 must be >0")

    w0_bits = load_w0_bits(DATA / "w0.txt")
    schedules = make_exogenous_schedule(w0_bits, max(args.horizons) + 1)
    payload = {
        "audit": "gate-zero T3 determinacy",
        "state_model": {
            "name": "A0(r,K,D0)",
            "components": [
                "normalized local debris patch B_r",
                "observed turn bit at the anchor",
                "evaluated gate phase g",
                "W0 prefix length capped at K",
                "deep-lock depth capped at D0",
            ],
            "soundness_note": (
                "This is an over-approximate finite abstraction.  A concrete ant "
                "history maps to a state, but outside-patch debris is forgotten."
            ),
        },
        "parameters": {
            "radii": args.radii,
            "synthetic_radius": args.synthetic_radius,
            "K": args.K,
            "D0": args.D0,
            "phase": args.phase,
            "horizons": args.horizons,
        },
        "dynamic_prefix": dynamic_prefix_audit(args, w0_bits, schedules),
        "syntactic_prefix": syntactic_prefix_audit(args, w0_bits, schedules),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(args.out),
        "dynamic_same_r_le_8": [
            row["radius"]
            for row in payload["dynamic_prefix"]["state_comparison_by_radius"]
            if row["same_abstract_state"]
        ],
        "syntactic_same_state": payload["syntactic_prefix"]["same_abstract_state"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
