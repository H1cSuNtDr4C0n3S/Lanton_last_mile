#!/usr/bin/env python3
"""door_comoving_class_passrate.py - section 73 co-moving class pass rates.

Use the §72 co-moving first-bad classes, then replay the 24 long orbits and
measure every actual T3' read of those classes, including reads that pass.

The target question is not whether first-bad classes recur (they do), but
whether recurrent co-moving classes are always forced to the bad parity or
sometimes pass on other lock attempts.
"""

from __future__ import annotations

import argparse
import csv
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
from door_discriminant_linf_profile import PERIOD, phase_drifts  # noqa: E402
from lock_checklist_probe import (  # noqa: E402
    Lock,
    ExogenousRead,
    lock_occurrences,
    make_exogenous_schedule,
    onset_phase,
    rel_to_abs,
)
from checklist_vector_geometry import dedupe_locks  # noqa: E402


@dataclass(frozen=True)
class ClassKey:
    phase: int
    comoving_rel_x: int
    comoving_rel_y: int
    required_black: int


EVENT_FIELDS = (
    "class_rank",
    "first_bad_count",
    "phase",
    "comoving_rel_x",
    "comoving_rel_y",
    "required_black",
    "idx",
    "attempt_id",
    "kind",
    "threshold",
    "start",
    "depth",
    "actual_phase",
    "horizon",
    "offset",
    "offset_mod_period",
    "period_index",
    "raw_rel_x",
    "raw_rel_y",
    "raw_linf",
    "comoving_linf",
    "abs_x",
    "abs_y",
    "origin_x",
    "origin_y",
    "heading",
    "actual_black",
    "passes",
    "is_first_bad",
    "actual_h",
    "actual_clear",
    "bad_kind",
)

CLASS_FIELDS = (
    "class_rank",
    "phase",
    "comoving_rel_x",
    "comoving_rel_y",
    "required_black",
    "first_bad_count",
    "read_events",
    "pass_events",
    "fail_events",
    "pass_rate",
    "attempts_with_class",
    "attempts_all_pass",
    "attempts_any_fail",
    "attempts_mixed_pass_fail",
    "pre_onset_events",
    "pre_onset_pass_events",
    "pre_onset_fail_events",
    "entry_events",
    "entry_pass_events",
    "entry_fail_events",
    "first_bad_events",
    "unique_abs_cells",
    "first_bad_abs_cells",
    "pass_abs_cells",
    "fail_abs_cells",
    "actual_black_values",
    "offset_mod_values",
    "comoving_linf",
    "raw_linf_min",
    "raw_linf_max",
    "top_abs_cells",
)

ORBIT_FIELDS = (
    "idx",
    "shard",
    "onset",
    "rngstate",
    "attempts",
    "events",
    "pass_events",
    "fail_events",
    "first_bad_events",
)


def int_field(row: dict[str, str], name: str) -> int:
    value = row.get(name, "")
    if value == "":
        raise ValueError(f"missing integer field {name!r}")
    return int(value)


def bad_kind(required_black: bool, actual_black: bool) -> str:
    if required_black and not actual_black:
        return "missing_black"
    if (not required_black) and actual_black:
        return "frontier_black_collision"
    return ""


def class_for_read(
    phase: int,
    read: ExogenousRead,
    drifts: dict[int, tuple[int, int]],
) -> tuple[ClassKey, int, int, int, int]:
    period_index = read.offset // PERIOD
    offset_mod = read.offset % PERIOD
    drift_x, drift_y = drifts[phase]
    cx = read.rel_x - period_index * drift_x
    cy = read.rel_y - period_index * drift_y
    return (
        ClassKey(phase, cx, cy, int(read.required_black)),
        period_index,
        offset_mod,
        max(abs(read.rel_x), abs(read.rel_y)),
        max(abs(cx), abs(cy)),
    )


def load_target_classes(path: Path, top_classes: int) -> tuple[dict[ClassKey, int], dict[ClassKey, int]]:
    counts: Counter[ClassKey] = Counter()
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = ClassKey(
                int_field(row, "eval_phase"),
                int_field(row, "comoving_rel_x"),
                int_field(row, "comoving_rel_y"),
                int_field(row, "required_black"),
            )
            counts[key] += 1

    ranked = counts.most_common(top_classes if top_classes > 0 else None)
    rank_by_key = {key: i + 1 for i, (key, _count) in enumerate(ranked)}
    return dict(ranked), rank_by_key


def first_defect(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    schedule: list[ExogenousRead],
    horizon: int,
    phase: int,
    drifts: dict[int, tuple[int, int]],
) -> tuple[int, int, ClassKey | None]:
    for read in schedule:
        if read.offset > horizon:
            break
        ax, ay = rel_to_abs(origin_x, origin_y, heading, read.rel_x, read.rel_y)
        actual_black = (ax, ay) in black
        if actual_black != read.required_black:
            key, _period_index, _offset_mod, _raw_linf, _comoving_linf = class_for_read(phase, read, drifts)
            return read.offset, 0, key
    return horizon + 1, 1, None


def attempt_kind(lock: Lock, onset: int) -> str:
    return "entry" if lock.start == onset else "pre_onset_lock"


def collect_orbit(
    orbit,
    gate_locks: list[Lock],
    schedules: dict[int, list[ExogenousRead]],
    drifts: dict[int, tuple[int, int]],
    target_counts: dict[ClassKey, int],
    rank_by_key: dict[ClassKey, int],
    horizon: int,
    smin: int,
    smax: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_start: dict[int, list[Lock]] = defaultdict(list)
    for lock in gate_locks:
        by_start[lock.start].append(lock)

    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    events: list[dict[str, object]] = []
    attempts = 0
    x = y = h = 0
    lock_index = 0

    for t in range(orbit.onset_dump + 1):
        for lock in by_start.get(t, ()):
            attempts += 1
            kind = attempt_kind(lock, orbit.onset_dump)
            attempt_id = f"{orbit.index}:{lock_index}"
            phase = lock.phase
            schedule = schedules[phase]
            actual_h, actual_clear, first_bad_key = first_defect(
                black, x, y, h, schedule, horizon, phase, drifts
            )

            for read in schedule:
                if read.offset > horizon:
                    break
                key, period_index, offset_mod, raw_linf, comoving_linf = class_for_read(phase, read, drifts)
                if key not in target_counts:
                    continue
                ax, ay = rel_to_abs(x, y, h, read.rel_x, read.rel_y)
                actual_black = (ax, ay) in black
                passes = int(actual_black == read.required_black)
                events.append(
                    {
                        "class_rank": rank_by_key[key],
                        "first_bad_count": target_counts[key],
                        "phase": key.phase,
                        "comoving_rel_x": key.comoving_rel_x,
                        "comoving_rel_y": key.comoving_rel_y,
                        "required_black": key.required_black,
                        "idx": orbit.index,
                        "attempt_id": attempt_id,
                        "kind": kind,
                        "threshold": lock.threshold,
                        "start": lock.start,
                        "depth": lock.depth,
                        "actual_phase": phase,
                        "horizon": horizon,
                        "offset": read.offset,
                        "offset_mod_period": offset_mod,
                        "period_index": period_index,
                        "raw_rel_x": read.rel_x,
                        "raw_rel_y": read.rel_y,
                        "raw_linf": raw_linf,
                        "comoving_linf": comoving_linf,
                        "abs_x": ax,
                        "abs_y": ay,
                        "origin_x": x,
                        "origin_y": y,
                        "heading": h,
                        "actual_black": int(actual_black),
                        "passes": passes,
                        "is_first_bad": int((not passes) and read.offset == actual_h and key == first_bad_key),
                        "actual_h": actual_h,
                        "actual_clear": actual_clear,
                        "bad_kind": "" if passes else bad_kind(read.required_black, actual_black),
                    }
                )
            lock_index += 1

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

    orbit_row = {
        "idx": orbit.index,
        "shard": orbit.shard,
        "onset": orbit.onset_dump,
        "rngstate": orbit.rngstate,
        "attempts": attempts,
        "events": len(events),
        "pass_events": sum(int(row["passes"]) for row in events),
        "fail_events": sum(1 - int(row["passes"]) for row in events),
        "first_bad_events": sum(int(row["is_first_bad"]) for row in events),
    }
    return events, orbit_row


def compact_values(values: Iterable[object], limit: int = 20) -> str:
    vals = sorted({str(v) for v in values})
    if len(vals) <= limit:
        return ";".join(vals)
    return ";".join(vals[:limit]) + f";...(+{len(vals) - limit})"


def summarize_classes(events: list[dict[str, object]], target_counts: dict[ClassKey, int], rank_by_key: dict[ClassKey, int]) -> list[dict[str, object]]:
    groups: dict[ClassKey, list[dict[str, object]]] = defaultdict(list)
    for row in events:
        key = ClassKey(
            int(row["phase"]),
            int(row["comoving_rel_x"]),
            int(row["comoving_rel_y"]),
            int(row["required_black"]),
        )
        groups[key].append(row)

    out: list[dict[str, object]] = []
    for key in sorted(target_counts, key=lambda k: rank_by_key[k]):
        rows = groups.get(key, [])
        attempts: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in rows:
            attempts[str(row["attempt_id"])].append(row)
        pass_events = sum(int(row["passes"]) for row in rows)
        fail_events = len(rows) - pass_events
        pre = [row for row in rows if row["kind"] == "pre_onset_lock"]
        entries = [row for row in rows if row["kind"] == "entry"]
        abs_cells = [(int(row["abs_x"]), int(row["abs_y"])) for row in rows]
        first_bad_abs = [(int(row["abs_x"]), int(row["abs_y"])) for row in rows if int(row["is_first_bad"])]
        pass_abs = [(int(row["abs_x"]), int(row["abs_y"])) for row in rows if int(row["passes"])]
        fail_abs = [(int(row["abs_x"]), int(row["abs_y"])) for row in rows if not int(row["passes"])]
        top_abs = Counter(abs_cells).most_common(8)
        out.append(
            {
                "class_rank": rank_by_key[key],
                "phase": key.phase,
                "comoving_rel_x": key.comoving_rel_x,
                "comoving_rel_y": key.comoving_rel_y,
                "required_black": key.required_black,
                "first_bad_count": target_counts[key],
                "read_events": len(rows),
                "pass_events": pass_events,
                "fail_events": fail_events,
                "pass_rate": pass_events / len(rows) if rows else "",
                "attempts_with_class": len(attempts),
                "attempts_all_pass": sum(int(all(int(r["passes"]) for r in vals)) for vals in attempts.values()),
                "attempts_any_fail": sum(int(any(not int(r["passes"]) for r in vals)) for vals in attempts.values()),
                "attempts_mixed_pass_fail": sum(
                    int(any(int(r["passes"]) for r in vals) and any(not int(r["passes"]) for r in vals))
                    for vals in attempts.values()
                ),
                "pre_onset_events": len(pre),
                "pre_onset_pass_events": sum(int(row["passes"]) for row in pre),
                "pre_onset_fail_events": sum(1 - int(row["passes"]) for row in pre),
                "entry_events": len(entries),
                "entry_pass_events": sum(int(row["passes"]) for row in entries),
                "entry_fail_events": sum(1 - int(row["passes"]) for row in entries),
                "first_bad_events": sum(int(row["is_first_bad"]) for row in rows),
                "unique_abs_cells": len(set(abs_cells)),
                "first_bad_abs_cells": len(set(first_bad_abs)),
                "pass_abs_cells": len(set(pass_abs)),
                "fail_abs_cells": len(set(fail_abs)),
                "actual_black_values": compact_values(row["actual_black"] for row in rows),
                "offset_mod_values": compact_values(row["offset_mod_period"] for row in rows),
                "comoving_linf": max(abs(key.comoving_rel_x), abs(key.comoving_rel_y)),
                "raw_linf_min": min((int(row["raw_linf"]) for row in rows), default=""),
                "raw_linf_max": max((int(row["raw_linf"]) for row in rows), default=""),
                "top_abs_cells": ";".join(f"{cell[0]},{cell[1]}:{count}" for cell, count in top_abs),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--class-rows", type=Path, default=ALPHA / "door_discriminant_linf_profile_rows.csv")
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "door_comoving_class_passrate")
    ap.add_argument("--horizon", type=int, default=1600)
    ap.add_argument("--top-classes", type=int, default=0, help="0 means all first-bad classes")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    target_counts, rank_by_key = load_target_classes(args.class_rows, args.top_classes)
    if not target_counts:
        raise ValueError("no target classes loaded")

    started = time.perf_counter()
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    drifts = phase_drifts(w0_bits)
    schedules = make_exogenous_schedule(w0_bits, args.horizon + 1)
    tail_steps = max(args.horizon, max(LOCK_THRESHOLDS), 208)

    all_events: list[dict[str, object]] = []
    orbit_rows: list[dict[str, object]] = []
    completed = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP: max-seconds={args.max_seconds:.1f}; completate={completed}")
            break
        turns, _deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps
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
            depth=args.horizon,
            is_gate=True,
        )
        gate_locks = dedupe_locks(locks, entry)
        events, orbit_row = collect_orbit(
            orbit,
            gate_locks,
            schedules,
            drifts,
            target_counts,
            rank_by_key,
            args.horizon,
            args.smin,
            args.smax,
        )
        all_events.extend(events)
        orbit_rows.append(orbit_row)
        completed += 1
        print(
            f"idx={orbit.index:2d} attempts={orbit_row['attempts']:3d} "
            f"events={orbit_row['events']:4d} pass={orbit_row['pass_events']:4d} "
            f"fail={orbit_row['fail_events']:4d}"
        )

    class_rows = summarize_classes(all_events, target_counts, rank_by_key)
    classes_with_events = [row for row in class_rows if int(row["read_events"])]
    classes_any_pass = [row for row in classes_with_events if int(row["pass_events"])]
    classes_zero_pass = [row for row in classes_with_events if not int(row["pass_events"])]
    classes_zero_pass_ge10_first_bad = [
        row for row in classes_zero_pass if int(row["first_bad_count"]) >= 10
    ]
    classes_mixed = [row for row in classes_with_events if int(row["pass_events"]) and int(row["fail_events"])]
    first_bad_events = sum(int(row["is_first_bad"]) for row in all_events)
    payload = {
        "source": str(args.dumps),
        "class_rows": str(args.class_rows),
        "orbits_requested": len(dumps),
        "orbits_completed": completed,
        "horizon": args.horizon,
        "attempts": sum(int(row["attempts"]) for row in orbit_rows),
        "target_classes": len(target_counts),
        "target_first_bad_rows": sum(target_counts.values()),
        "events": len(all_events),
        "pass_events": sum(int(row["passes"]) for row in all_events),
        "fail_events": sum(1 - int(row["passes"]) for row in all_events),
        "first_bad_events": first_bad_events,
        "pass_rate": (sum(int(row["passes"]) for row in all_events) / len(all_events)) if all_events else None,
        "classes_with_events": len(classes_with_events),
        "classes_any_pass": len(classes_any_pass),
        "classes_zero_pass": len(classes_zero_pass),
        "classes_zero_pass_ge10_first_bad": len(classes_zero_pass_ge10_first_bad),
        "classes_mixed_pass_fail": len(classes_mixed),
        "top_classes": class_rows[:12],
        "elapsed_seconds": time.perf_counter() - started,
    }

    out_prefix: Path = args.out_prefix
    events_csv = out_prefix.with_name(out_prefix.name + "_events.csv")
    classes_csv = out_prefix.with_name(out_prefix.name + "_classes.csv")
    orbits_csv = out_prefix.with_name(out_prefix.name + "_orbits.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(events_csv, all_events, EVENT_FIELDS)
    write_csv(classes_csv, class_rows, CLASS_FIELDS)
    write_csv(orbits_csv, orbit_rows, ORBIT_FIELDS)
    summary_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"\nCSV events: {events_csv}")
    print(f"CSV classes: {classes_csv}")
    print(f"CSV orbits: {orbits_csv}")
    print(f"JSON summary: {summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
