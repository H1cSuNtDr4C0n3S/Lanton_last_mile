#!/usr/bin/env python3
"""door_gf2_rank_gate.py - section 74 GF(2) rank gate for door parities.

Read the §73 pass/fail event table and measure linear rank over GF(2) for
selected door phases and depth batches.  Rows are lock attempts; columns are
exact target T3' reads:

    (offset, period_index, comoving_rel_x, comoving_rel_y, required_black)

The value is either actual_black or fail=(actual_black != required_black).  The
goal is to distinguish full freedom from linear dependencies before building a
larger debt graph.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

from delta4_long_orbits import ALPHA, build_seed  # noqa: E402


DEFAULT_PHASES = "0,103,30,24,102"
DEFAULT_DEPTH_BINS = "all,40:77,78:103,80:,104:,208:,512:"
DEFAULT_MAX_OFFSETS = "77,103,1600"

SUMMARY_FIELDS = (
    "label",
    "phase",
    "depth_lo",
    "depth_hi",
    "max_offset",
    "kind",
    "attempts",
    "columns",
    "events",
    "pass_events",
    "fail_events",
    "c0_zero_events",
    "c0_zero_rate",
    "rank_actual",
    "affine_rank_actual",
    "rank_fail",
    "affine_rank_fail",
    "capacity",
    "capacity_deficit_actual",
    "column_nullity_actual",
    "full_column_rank_actual",
    "constant_actual_columns",
    "duplicate_actual_column_patterns",
    "max_duplicate_actual_pattern",
    "rank_status",
)


def int_field(row: dict[str, str], name: str) -> int:
    value = row.get(name, "")
    if value == "":
        raise ValueError(f"missing integer field {name!r}")
    return int(value)


def parse_ints(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_depth_bins(text: str) -> list[tuple[str, int | None, int | None]]:
    out: list[tuple[str, int | None, int | None]] = []
    for raw in text.split(","):
        item = raw.strip()
        if not item:
            continue
        if item == "all":
            out.append(("all", None, None))
            continue
        if ":" in item:
            left, right = item.split(":", 1)
            lo = int(left) if left.strip() else None
            hi = int(right) if right.strip() else None
        else:
            lo = hi = int(item)
        if lo is None and hi is None:
            raise ValueError("unbounded depth bin must be named all")
        if lo is not None and hi is not None and lo > hi:
            raise ValueError(f"bad decreasing depth bin {item!r}")
        label = f"{'' if lo is None else lo}-{'' if hi is None else hi}"
        out.append((label, lo, hi))
    return out


def in_depth(depth: int, lo: int | None, hi: int | None) -> bool:
    return (lo is None or depth >= lo) and (hi is None or depth <= hi)


def gf2_rank(rows: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    rank = 0
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                rank += 1
                break
    return rank


def affine_rank(rows: list[int]) -> int:
    if len(rows) <= 1:
        return 0
    base = rows[0]
    return gf2_rank(row ^ base for row in rows[1:])


def load_initial_black(orbits_csv: Path, smin: int, smax: int) -> dict[int, set[tuple[int, int]]]:
    out: dict[int, set[tuple[int, int]]] = {}
    with orbits_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = int_field(row, "idx")
            rngstate = int_field(row, "rngstate")
            black, _side, _dens = build_seed(rngstate, smin, smax)
            out[idx] = black
    return out


def load_events(path: Path, initial_black: dict[int, set[tuple[int, int]]]) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = int_field(row, "idx")
            abs_cell = (int_field(row, "abs_x"), int_field(row, "abs_y"))
            required = int_field(row, "required_black")
            actual = int_field(row, "actual_black")
            events.append(
                {
                    "phase": int_field(row, "phase"),
                    "attempt_id": row["attempt_id"],
                    "kind": row["kind"],
                    "depth": int_field(row, "depth"),
                    "offset": int_field(row, "offset"),
                    "period_index": int_field(row, "period_index"),
                    "offset_mod_period": int_field(row, "offset_mod_period"),
                    "comoving_rel_x": int_field(row, "comoving_rel_x"),
                    "comoving_rel_y": int_field(row, "comoving_rel_y"),
                    "required_black": required,
                    "actual_black": actual,
                    "passes": int_field(row, "passes"),
                    "idx": idx,
                    "abs_x": abs_cell[0],
                    "abs_y": abs_cell[1],
                    "c0_black": int(abs_cell in initial_black.get(idx, set())),
                    "fail": actual ^ required,
                }
            )
    return events


def column_key(event: dict[str, object]) -> tuple[int, int, int, int, int]:
    return (
        int(event["offset"]),
        int(event["period_index"]),
        int(event["comoving_rel_x"]),
        int(event["comoving_rel_y"]),
        int(event["required_black"]),
    )


def summarize_batch(
    events: list[dict[str, object]],
    phase: int,
    label: str,
    lo: int | None,
    hi: int | None,
    max_offset: int,
) -> dict[str, object]:
    rows = [
        event
        for event in events
        if event["kind"] == "pre_onset_lock"
        and int(event["phase"]) == phase
        and in_depth(int(event["depth"]), lo, hi)
        and int(event["offset"]) <= max_offset
    ]
    attempts = sorted({str(event["attempt_id"]) for event in rows})
    columns = sorted({column_key(event) for event in rows})
    col_index = {col: i for i, col in enumerate(columns)}

    actual_rows: dict[str, int] = defaultdict(int)
    fail_rows: dict[str, int] = defaultdict(int)
    for event in rows:
        bit = 1 << col_index[column_key(event)]
        attempt_id = str(event["attempt_id"])
        if int(event["actual_black"]):
            actual_rows[attempt_id] ^= bit
        if int(event["fail"]):
            fail_rows[attempt_id] ^= bit

    actual_vectors = [actual_rows[attempt] for attempt in attempts]
    fail_vectors = [fail_rows[attempt] for attempt in attempts]
    rank_actual = gf2_rank(actual_vectors)
    rank_fail = gf2_rank(fail_vectors)
    capacity = min(len(attempts), len(columns))

    column_patterns: list[int] = []
    for col in columns:
        mask = 0
        col_bit = 1 << col_index[col]
        for i, attempt in enumerate(attempts):
            if actual_rows[attempt] & col_bit:
                mask |= 1 << i
        column_patterns.append(mask)
    pattern_counts = Counter(column_patterns)
    constant_patterns = {0, (1 << len(attempts)) - 1}
    constant_columns = sum(count for pattern, count in pattern_counts.items() if pattern in constant_patterns)
    duplicate_columns = sum(count - 1 for count in pattern_counts.values() if count > 1)
    max_duplicate = max(pattern_counts.values(), default=0)

    if not attempts or not columns:
        status = "empty"
    elif rank_actual == capacity:
        status = "full_capacity"
    elif len(attempts) >= len(columns):
        status = "column_dependency"
    else:
        status = "sample_limited_dependency"

    c0_zero = sum(1 - int(event["c0_black"]) for event in rows)
    pass_events = sum(int(event["passes"]) for event in rows)
    fail_events = len(rows) - pass_events
    return {
        "label": label,
        "phase": phase,
        "depth_lo": "" if lo is None else lo,
        "depth_hi": "" if hi is None else hi,
        "max_offset": max_offset,
        "kind": "pre_onset_lock",
        "attempts": len(attempts),
        "columns": len(columns),
        "events": len(rows),
        "pass_events": pass_events,
        "fail_events": fail_events,
        "c0_zero_events": c0_zero,
        "c0_zero_rate": (c0_zero / len(rows)) if rows else "",
        "rank_actual": rank_actual,
        "affine_rank_actual": affine_rank(actual_vectors),
        "rank_fail": rank_fail,
        "affine_rank_fail": affine_rank(fail_vectors),
        "capacity": capacity,
        "capacity_deficit_actual": capacity - rank_actual,
        "column_nullity_actual": len(columns) - rank_actual,
        "full_column_rank_actual": int(rank_actual == len(columns) and len(columns) <= len(attempts)),
        "constant_actual_columns": constant_columns,
        "duplicate_actual_column_patterns": duplicate_columns,
        "max_duplicate_actual_pattern": max_duplicate,
        "rank_status": status,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--events", type=Path, default=ALPHA / "door_comoving_class_passrate_events.csv")
    ap.add_argument("--orbits", type=Path, default=ALPHA / "door_comoving_class_passrate_orbits.csv")
    ap.add_argument("--phases", default=DEFAULT_PHASES)
    ap.add_argument("--depth-bins", default=DEFAULT_DEPTH_BINS)
    ap.add_argument("--max-offsets", default=DEFAULT_MAX_OFFSETS)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "door_gf2_rank_gate")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    phases = parse_ints(args.phases)
    depth_bins = parse_depth_bins(args.depth_bins)
    max_offsets = parse_ints(args.max_offsets)
    initial_black = load_initial_black(args.orbits, args.smin, args.smax)
    events = load_events(args.events, initial_black)

    rows: list[dict[str, object]] = []
    for phase in phases:
        for label, lo, hi in depth_bins:
            for max_offset in max_offsets:
                rows.append(summarize_batch(events, phase, label, lo, hi, max_offset))

    interesting = [
        row
        for row in rows
        if row["rank_status"] == "column_dependency" and int(row["columns"]) > 0
    ]
    payload = {
        "events": str(args.events),
        "orbits": str(args.orbits),
        "phases": phases,
        "depth_bins": [{"label": label, "lo": lo, "hi": hi} for label, lo, hi in depth_bins],
        "max_offsets": max_offsets,
        "batches": len(rows),
        "column_dependency_batches": len(interesting),
        "top_column_dependency_batches": sorted(
            interesting,
            key=lambda row: (int(row["capacity_deficit_actual"]), int(row["columns"])),
            reverse=True,
        )[:12],
        "interpretation": (
            "A column_dependency row has attempts >= columns and rank_actual < columns; "
            "that is a concrete GF(2) deficit on the observed batch, not just too few samples."
        ),
    }

    out_prefix: Path = args.out_prefix
    csv_path = out_prefix.with_name(out_prefix.name + "_batches.csv")
    json_path = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(csv_path, rows, SUMMARY_FIELDS)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"\nCSV batches: {csv_path}")
    print(f"JSON summary: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
