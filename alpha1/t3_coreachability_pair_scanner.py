#!/usr/bin/env python3
"""t3_coreachability_pair_scanner.py - section 71 co-reachability scanner.

Replay the 24 long alpha1 orbits and look for pairs of reachable anchor states
whose normalized local debris patch is identical at radius R, but whose T3'
checklist value for the same evaluated gate phase differs before horizon L.

A witness is accepted only when the earlier first-bad read is outside B_R.
That is the empirical co-reachability certificate from section 70:
two finite histories agree locally, earlier checklist reads do not distinguish
them, and the first discriminator is genuinely non-local at that radius.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

from delta4_long_orbits import (  # noqa: E402
    ALPHA,
    DATA,
    DX,
    DY,
    LOCK_THRESHOLDS,
    build_seed,
    compare_bites,
    load_w0_bits,
    parse_dumps,
    simulate_orbit,
)
from lock_checklist_probe import (  # noqa: E402
    GATE_PHASES,
    Lock,
    ExogenousRead,
    lock_occurrences,
    make_exogenous_schedule,
    onset_phase,
    rel_to_abs,
)
from checklist_vector_geometry import dedupe_locks  # noqa: E402


@dataclass(frozen=True)
class Anchor:
    anchor_id: str
    idx: int
    shard: int
    onset: int
    rngstate: int
    family: str
    start: int
    time_frac: float
    is_entry: int
    declared_phase: int | str
    threshold: int | str
    depth: int | str
    origin_x: int
    origin_y: int
    heading: int
    observed_turn_bit: int


@dataclass(frozen=True)
class FirstBad:
    offset: int | None
    rel_x: int | None
    rel_y: int | None
    required_black: bool | None
    actual_black: bool | None
    kind: str


@dataclass(frozen=True)
class EvalRec:
    anchor: Anchor
    radius: int
    horizon: int
    eval_phase: int
    patch_hash: str
    h: int
    first_bad: FirstBad


@dataclass
class BucketState:
    count: int
    reps_by_h: dict[int, EvalRec]
    witness_recorded: bool = False


WITNESS_FIELDS = (
    "radius",
    "horizon",
    "eval_phase",
    "observed_turn_bit",
    "patch_hash",
    "patch_bytes",
    "bucket_size_at_detection",
    "n",
    "disc_rel_x",
    "disc_rel_y",
    "disc_l1",
    "disc_linf",
    "required_black",
    "early_actual_black",
    "late_actual_black",
    "bad_kind",
    "h_early",
    "h_late",
    "early_anchor_id",
    "late_anchor_id",
    "early_idx",
    "late_idx",
    "early_family",
    "late_family",
    "early_start",
    "late_start",
    "early_origin_x",
    "early_origin_y",
    "early_heading",
    "late_origin_x",
    "late_origin_y",
    "late_heading",
    "verified_same_local_patch",
    "verified_prior_reads_same_verdict",
    "verified_discriminator_outside_R",
)

ORBIT_FIELDS = (
    "idx",
    "shard",
    "onset",
    "rngstate",
    "gate_anchors",
    "anchors",
    "evals",
    "witnesses_so_far",
)

BUCKET_FIELDS = (
    "radius",
    "horizon",
    "buckets",
    "colliding_buckets",
    "h_divergent_buckets",
    "witnesses_recorded",
    "internal_conflicts_rejected",
)


def parse_ints(text: str) -> tuple[int, ...]:
    vals = tuple(sorted({int(part.strip()) for part in text.split(",") if part.strip()}))
    if not vals or vals[0] <= 0:
        raise ValueError("lista di interi positivi attesa")
    return vals


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str] | None = None) -> None:
    fields = list(fieldnames) if fieldnames is not None else (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as f:
        if not fields:
            return
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def patch_digest(patch: bytes) -> str:
    return hashlib.blake2b(patch, digest_size=16).hexdigest()


def local_patch_bytes(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    radius: int,
) -> bytes:
    bits = bytearray()
    cur = 0
    nbits = 0
    for rel_y in range(-radius, radius + 1):
        for rel_x in range(-radius, radius + 1):
            ax, ay = rel_to_abs(origin_x, origin_y, heading, rel_x, rel_y)
            if (ax, ay) in black:
                cur |= 1 << nbits
            nbits += 1
            if nbits == 8:
                bits.append(cur)
                cur = 0
                nbits = 0
    if nbits:
        bits.append(cur)
    return bytes(bits)


def eval_first_bad(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    schedule: list[ExogenousRead],
    max_horizon: int,
) -> FirstBad:
    for read in schedule:
        if read.offset > max_horizon:
            break
        ax, ay = rel_to_abs(origin_x, origin_y, heading, read.rel_x, read.rel_y)
        actual_black = (ax, ay) in black
        if actual_black == read.required_black:
            continue
        if read.required_black and not actual_black:
            kind = "missing_black"
        elif (not read.required_black) and actual_black:
            kind = "frontier_black_collision"
        else:
            kind = "color_mismatch"
        return FirstBad(
            offset=read.offset,
            rel_x=read.rel_x,
            rel_y=read.rel_y,
            required_black=read.required_black,
            actual_black=actual_black,
            kind=kind,
        )
    return FirstBad(
        offset=None,
        rel_x=None,
        rel_y=None,
        required_black=None,
        actual_black=None,
        kind="",
    )


def h_for_horizon(first_bad: FirstBad, horizon: int) -> int:
    if first_bad.offset is None or first_bad.offset > horizon:
        return horizon + 1
    return first_bad.offset


def anchor_row(anchor: Anchor) -> dict[str, object]:
    return {
        "anchor_id": anchor.anchor_id,
        "idx": anchor.idx,
        "shard": anchor.shard,
        "onset": anchor.onset,
        "rngstate": anchor.rngstate,
        "family": anchor.family,
        "start": anchor.start,
        "time_frac": anchor.time_frac,
        "is_entry": anchor.is_entry,
        "declared_phase": anchor.declared_phase,
        "threshold": anchor.threshold,
        "depth": anchor.depth,
        "origin_x": anchor.origin_x,
        "origin_y": anchor.origin_y,
        "heading": anchor.heading,
        "observed_turn_bit": anchor.observed_turn_bit,
    }


def add_witness_row(
    early: EvalRec,
    late: EvalRec,
    patch_bytes: bytes,
    bucket_size: int,
) -> dict[str, object] | None:
    fb = early.first_bad
    if fb.offset is None or fb.rel_x is None or fb.rel_y is None:
        return None
    if max(abs(fb.rel_x), abs(fb.rel_y)) <= early.radius:
        return None
    return {
        "radius": early.radius,
        "horizon": early.horizon,
        "eval_phase": early.eval_phase,
        "observed_turn_bit": early.anchor.observed_turn_bit,
        "patch_hash": early.patch_hash,
        "patch_bytes": len(patch_bytes),
        "bucket_size_at_detection": bucket_size,
        "n": fb.offset,
        "disc_rel_x": fb.rel_x,
        "disc_rel_y": fb.rel_y,
        "disc_l1": abs(fb.rel_x) + abs(fb.rel_y),
        "disc_linf": max(abs(fb.rel_x), abs(fb.rel_y)),
        "required_black": int(bool(fb.required_black)),
        "early_actual_black": int(bool(fb.actual_black)),
        "late_actual_black": int(not bool(fb.actual_black)),
        "bad_kind": fb.kind,
        "h_early": early.h,
        "h_late": late.h,
        "early_anchor_id": early.anchor.anchor_id,
        "late_anchor_id": late.anchor.anchor_id,
        "early_idx": early.anchor.idx,
        "late_idx": late.anchor.idx,
        "early_family": early.anchor.family,
        "late_family": late.anchor.family,
        "early_start": early.anchor.start,
        "late_start": late.anchor.start,
        "early_origin_x": early.anchor.origin_x,
        "early_origin_y": early.anchor.origin_y,
        "early_heading": early.anchor.heading,
        "late_origin_x": late.anchor.origin_x,
        "late_origin_y": late.anchor.origin_y,
        "late_heading": late.anchor.heading,
        "verified_same_local_patch": 1,
        "verified_prior_reads_same_verdict": int(late.h > fb.offset),
        "verified_discriminator_outside_R": 1,
    }


def maybe_record_witness(
    rec: EvalRec,
    patch_bytes: bytes,
    bucket: BucketState,
    witnesses: list[dict[str, object]],
    witness_limit: int,
    internal_conflicts: Counter,
) -> None:
    if bucket.witness_recorded:
        return
    if len(witnesses) >= witness_limit:
        return
    for other_h, other in sorted(bucket.reps_by_h.items()):
        if other_h == rec.h:
            continue
        early, late = (rec, other) if rec.h < other.h else (other, rec)
        if early.h == early.horizon + 1:
            continue
        fb = early.first_bad
        if fb.rel_x is None or fb.rel_y is None:
            continue
        if max(abs(fb.rel_x), abs(fb.rel_y)) <= early.radius:
            internal_conflicts[(early.radius, early.horizon)] += 1
            continue
        row = add_witness_row(early, late, patch_bytes, bucket.count)
        if row is not None:
            witnesses.append(row)
            bucket.witness_recorded = True
            return


def build_anchor_meta(
    orbit,
    gate_locks: list[Lock],
    include_grid: bool,
    grid_stride: int,
    include_gate_times_in_grid: bool,
) -> dict[int, list[dict[str, object]]]:
    by_time: dict[int, list[dict[str, object]]] = defaultdict(list)
    gate_starts: set[int] = set()
    for lock_index, lock in enumerate(gate_locks):
        kind = "entry" if lock.start == orbit.onset_dump else "gate"
        gate_starts.add(lock.start)
        by_time[lock.start].append(
            {
                "anchor_id": f"{orbit.index}:gate:{lock_index}",
                "family": kind,
                "is_entry": int(kind == "entry"),
                "declared_phase": lock.phase,
                "threshold": lock.threshold,
                "depth": lock.depth,
            }
        )
    if include_grid:
        grid_index = 0
        for start in range(0, orbit.onset_dump, grid_stride):
            if (not include_gate_times_in_grid) and start in gate_starts:
                continue
            by_time[start].append(
                {
                    "anchor_id": f"{orbit.index}:grid:{grid_index}",
                    "family": "grid",
                    "is_entry": 0,
                    "declared_phase": "",
                    "threshold": "",
                    "depth": "",
                }
            )
            grid_index += 1
    return by_time


def phase_list_for_anchor(
    anchor: Anchor,
    phase_mode: str,
    phase_first_bits: dict[int, int],
) -> tuple[int, ...]:
    if phase_mode == "declared":
        if anchor.declared_phase == "":
            return ()
        phase = int(anchor.declared_phase)
        return (phase,) if phase_first_bits[phase] == anchor.observed_turn_bit else ()
    return tuple(phase for phase in GATE_PHASES if phase_first_bits[phase] == anchor.observed_turn_bit)


def process_anchor(
    anchor: Anchor,
    black: set[tuple[int, int]],
    radii: tuple[int, ...],
    horizons: tuple[int, ...],
    phase_mode: str,
    phase_first_bits: dict[int, int],
    schedules: dict[int, list[ExogenousRead]],
    buckets: dict[tuple[int, int, int, int, bytes], BucketState],
    witnesses: list[dict[str, object]],
    witness_limit: int,
    internal_conflicts: Counter,
) -> int:
    max_horizon = max(horizons)
    patches = {
        radius: local_patch_bytes(black, anchor.origin_x, anchor.origin_y, anchor.heading, radius)
        for radius in radii
    }
    patch_hashes = {radius: patch_digest(patch) for radius, patch in patches.items()}
    eval_count = 0
    for phase in phase_list_for_anchor(anchor, phase_mode, phase_first_bits):
        first_bad = eval_first_bad(
            black,
            anchor.origin_x,
            anchor.origin_y,
            anchor.heading,
            schedules[phase],
            max_horizon,
        )
        for horizon in horizons:
            h = h_for_horizon(first_bad, horizon)
            for radius in radii:
                patch = patches[radius]
                rec = EvalRec(
                    anchor=anchor,
                    radius=radius,
                    horizon=horizon,
                    eval_phase=phase,
                    patch_hash=patch_hashes[radius],
                    h=h,
                    first_bad=first_bad,
                )
                key = (radius, horizon, anchor.observed_turn_bit, phase, patch)
                bucket = buckets.get(key)
                if bucket is None:
                    buckets[key] = BucketState(count=1, reps_by_h={h: rec})
                else:
                    bucket.count += 1
                    maybe_record_witness(
                        rec,
                        patch,
                        bucket,
                        witnesses,
                        witness_limit,
                        internal_conflicts,
                    )
                    bucket.reps_by_h.setdefault(h, rec)
                eval_count += 1
    return eval_count


def scan_orbit(
    orbit,
    w0_bits: list[int],
    radii: tuple[int, ...],
    horizons: tuple[int, ...],
    phase_mode: str,
    phase_first_bits: dict[int, int],
    schedules: dict[int, list[ExogenousRead]],
    include_grid: bool,
    grid_stride: int,
    include_gate_times_in_grid: bool,
    smin: int,
    smax: int,
    buckets: dict[tuple[int, int, int, int, bytes], BucketState],
    witnesses: list[dict[str, object]],
    witness_limit: int,
    internal_conflicts: Counter,
) -> tuple[int, int, int]:
    tail_steps = max(max(horizons), max(LOCK_THRESHOLDS), 208)
    turns, _deep, sim_bites, _side, _dens = simulate_orbit(
        orbit.rngstate, orbit.onset_dump, smin, smax, tail_steps
    )
    compare_bites(sim_bites, orbit.bite_times, orbit)
    locks: list[Lock] = []
    for threshold in LOCK_THRESHOLDS:
        locks.extend(lock_occurrences(turns, orbit.onset_dump, w0_bits, threshold, orbit.index))
    entry = Lock(
        orbit_index=orbit.index,
        threshold=0,
        start=orbit.onset_dump,
        phase=onset_phase(turns, orbit.onset_dump, w0_bits),
        depth=max(horizons),
        is_gate=True,
    )
    gate_locks = dedupe_locks(locks, entry)
    anchor_meta = build_anchor_meta(
        orbit,
        gate_locks,
        include_grid,
        grid_stride,
        include_gate_times_in_grid,
    )

    black, _side2, _dens2 = build_seed(orbit.rngstate, smin, smax)
    x = y = h = 0
    anchors_seen = 0
    evals_seen = 0
    for t in range(orbit.onset_dump + 1):
        for meta in anchor_meta.get(t, ()):
            observed_turn_bit = 0 if (x, y) in black else 1
            anchor = Anchor(
                anchor_id=str(meta["anchor_id"]),
                idx=orbit.index,
                shard=orbit.shard,
                onset=orbit.onset_dump,
                rngstate=orbit.rngstate,
                family=str(meta["family"]),
                start=t,
                time_frac=t / orbit.onset_dump,
                is_entry=int(meta["is_entry"]),
                declared_phase=meta["declared_phase"],
                threshold=meta["threshold"],
                depth=meta["depth"],
                origin_x=x,
                origin_y=y,
                heading=h,
                observed_turn_bit=observed_turn_bit,
            )
            anchors_seen += 1
            evals_seen += process_anchor(
                anchor,
                black,
                radii,
                horizons,
                phase_mode,
                phase_first_bits,
                schedules,
                buckets,
                witnesses,
                witness_limit,
                internal_conflicts,
            )
        if t == orbit.onset_dump:
            break
        cell = (x, y)
        if cell in black:
            black.discard(cell)
            h = (h + 3) & 3
        else:
            black.add(cell)
            h = (h + 1) & 3
        x += DX[h]
        y += DY[h]
    return len(gate_locks), anchors_seen, evals_seen


def summarize_buckets(
    buckets: dict[tuple[int, int, int, int, bytes], BucketState],
    witnesses: list[dict[str, object]],
    internal_conflicts: Counter,
) -> dict[str, object]:
    by_rl: dict[tuple[int, int], dict[str, int]] = defaultdict(
        lambda: {"buckets": 0, "colliding_buckets": 0, "h_divergent_buckets": 0}
    )
    for radius, horizon, _obs, _phase, _patch in buckets:
        item = by_rl[(radius, horizon)]
        item["buckets"] += 1
        bucket = buckets[(radius, horizon, _obs, _phase, _patch)]
        if bucket.count > 1:
            item["colliding_buckets"] += 1
        if len(bucket.reps_by_h) > 1:
            item["h_divergent_buckets"] += 1
    witness_counts = Counter((int(w["radius"]), int(w["horizon"])) for w in witnesses)
    return {
        "bucket_summary": [
            {
                "radius": radius,
                "horizon": horizon,
                **payload,
                "witnesses_recorded": witness_counts[(radius, horizon)],
                "internal_conflicts_rejected": internal_conflicts[(radius, horizon)],
            }
            for (radius, horizon), payload in sorted(by_rl.items())
        ]
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit-orbits", type=int, default=0, help="0 = tutte le orbite del dump")
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--radii", default="8,16,24,32,40")
    ap.add_argument("--horizons", default="208,512,1600")
    ap.add_argument("--phase-mode", choices=("compatible", "declared"), default="compatible")
    ap.add_argument("--include-grid", action="store_true")
    ap.add_argument("--grid-stride", type=int, default=1040)
    ap.add_argument("--include-gate-times-in-grid", action="store_true")
    ap.add_argument("--witness-limit", type=int, default=200)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "t3_coreachability_pair_scanner")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()
    if args.grid_stride <= 0:
        raise ValueError("--grid-stride deve essere positivo")

    started = time.perf_counter()
    radii = parse_ints(args.radii)
    horizons = parse_ints(args.horizons)
    dumps = parse_dumps(args.dumps)
    if args.limit_orbits:
        dumps = dumps[: args.limit_orbits]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    phase_first_bits = {phase: w0_bits[phase] for phase in GATE_PHASES}
    schedules = make_exogenous_schedule(w0_bits, max(horizons) + 1)

    buckets: dict[tuple[int, int, int, int, bytes], BucketState] = {}
    witnesses: list[dict[str, object]] = []
    internal_conflicts: Counter = Counter()
    orbit_rows: list[dict[str, object]] = []
    completed = 0
    total_anchors = 0
    total_evals = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP: max-seconds={args.max_seconds:.1f}; completate={completed}")
            break
        gate_anchors, anchors, evals = scan_orbit(
            orbit,
            w0_bits,
            radii,
            horizons,
            args.phase_mode,
            phase_first_bits,
            schedules,
            args.include_grid,
            args.grid_stride,
            args.include_gate_times_in_grid,
            args.smin,
            args.smax,
            buckets,
            witnesses,
            args.witness_limit,
            internal_conflicts,
        )
        completed += 1
        total_anchors += anchors
        total_evals += evals
        orbit_rows.append(
            {
                "idx": orbit.index,
                "shard": orbit.shard,
                "onset": orbit.onset_dump,
                "rngstate": orbit.rngstate,
                "gate_anchors": gate_anchors,
                "anchors": anchors,
                "evals": evals,
                "witnesses_so_far": len(witnesses),
            }
        )
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} "
            f"anchors={anchors:4d} evals={evals:6d} witnesses={len(witnesses):4d}"
        )

    if not orbit_rows:
        print("Nessuna orbita completata; nessun output.")
        return 1

    payload = {
        "source": str(args.dumps),
        "orbits_requested": len(dumps),
        "orbits_completed": completed,
        "radii": radii,
        "horizons": horizons,
        "phase_mode": args.phase_mode,
        "include_grid": args.include_grid,
        "grid_stride": args.grid_stride,
        "include_gate_times_in_grid": args.include_gate_times_in_grid,
        "anchors": total_anchors,
        "evals": total_evals,
        "buckets": len(buckets),
        "witnesses_recorded": len(witnesses),
        "witness_limit": args.witness_limit,
        "elapsed_seconds": time.perf_counter() - started,
        "orbit_summary": orbit_rows,
    }
    payload.update(summarize_buckets(buckets, witnesses, internal_conflicts))

    out_prefix: Path = args.out_prefix
    witnesses_csv = out_prefix.with_name(out_prefix.name + "_witnesses.csv")
    orbit_csv = out_prefix.with_name(out_prefix.name + "_orbits.csv")
    bucket_csv = out_prefix.with_name(out_prefix.name + "_buckets.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(witnesses_csv, witnesses, WITNESS_FIELDS)
    write_csv(orbit_csv, orbit_rows, ORBIT_FIELDS)
    write_csv(bucket_csv, payload["bucket_summary"], BUCKET_FIELDS)
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "orbits_completed": completed,
                "anchors": total_anchors,
                "evals": total_evals,
                "buckets": len(buckets),
                "witnesses_recorded": len(witnesses),
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )
    print(f"\nCSV witnesses: {witnesses_csv}")
    print(f"CSV orbits: {orbit_csv}")
    print(f"CSV buckets: {bucket_csv}")
    print(f"JSON summary: {summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
