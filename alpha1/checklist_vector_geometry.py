#!/usr/bin/env python3
"""checklist_vector_geometry.py - section 63 checklist vector + gate geometry.

This is a one-shot extension of lock_checklist_probe.py.  It re-simulates the
24 long alpha1 orbits, extracts per-alignment gate locks, deduplicates D>=80
duplicates of D>=40 attempts, and records:

  * ant origin and heading at the gate;
  * the exogenous checklist vector at the gate;
  * geometry between consecutive gate attempts.

For failed locks, the vector is evaluated up to at least --vector-horizon and
always through the death offset.  For entry controls it is evaluated through
--entry-horizon.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
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


@dataclass(frozen=True)
class GateAttempt:
    idx: int
    shard: int
    onset: int
    rngstate: int
    threshold: int
    start: int
    kind: str
    ok: bool
    phase: int
    depth: int
    origin_x: int
    origin_y: int
    heading: int
    check_horizon: int


def quantiles(values: list[int | float]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "q25": None, "median": None, "q75": None, "max": None, "mean": None}
    ordered = sorted(values)
    if len(ordered) >= 4:
        qs = statistics.quantiles(ordered, n=4)
        q25, q75 = qs[0], qs[2]
    else:
        q25 = ordered[0]
        q75 = ordered[-1]
    return {
        "min": ordered[0],
        "q25": q25,
        "median": statistics.median(ordered),
        "q75": q75,
        "max": ordered[-1],
        "mean": sum(ordered) / len(ordered),
    }


def dedupe_locks(locks: list[Lock], entry: Lock) -> list[Lock]:
    best: dict[tuple[int, int, str], Lock] = {}
    for lock in locks:
        if not lock.is_gate:
            continue
        key = (lock.start, lock.phase, "pre_onset_lock")
        current = best.get(key)
        if current is None or lock.threshold > current.threshold:
            best[key] = lock
    best[(entry.start, entry.phase, "entry")] = entry
    return sorted(best.values(), key=lambda l: (l.start, l.phase, l.threshold))


def cell_status(
    black: set[tuple[int, int]],
    attempt: GateAttempt,
    read: ExogenousRead,
) -> dict[str, object]:
    ax, ay = rel_to_abs(attempt.origin_x, attempt.origin_y, attempt.heading, read.rel_x, read.rel_y)
    actual_black = (ax, ay) in black
    ok = actual_black == read.required_black
    if ok:
        bad_kind = ""
    elif read.required_black and not actual_black:
        bad_kind = "missing_black"
    elif (not read.required_black) and actual_black:
        bad_kind = "frontier_black_collision"
    else:
        bad_kind = "color_mismatch"
    return {
        "offset": read.offset,
        "rel_x": read.rel_x,
        "rel_y": read.rel_y,
        "abs_x": ax,
        "abs_y": ay,
        "required_black": int(read.required_black),
        "actual_black": int(actual_black),
        "ok": int(ok),
        "bad_kind": bad_kind,
    }


def summarize_attempt_cells(attempt: GateAttempt, cell_rows: list[dict[str, object]]) -> dict[str, object]:
    bad = [r for r in cell_rows if not int(r["ok"])]
    first_bad = bad[0] if bad else None
    missing = sum(1 for r in bad if r["bad_kind"] == "missing_black")
    frontier = sum(1 for r in bad if r["bad_kind"] == "frontier_black_collision")
    required_black = sum(int(r["required_black"]) for r in cell_rows)
    actual_black = sum(int(r["actual_black"]) for r in cell_rows)
    prefix_rows = [r for r in cell_rows if int(r["offset"]) <= attempt.depth]
    prefix_bad = [r for r in prefix_rows if not int(r["ok"])]
    return {
        "idx": attempt.idx,
        "shard": attempt.shard,
        "onset": attempt.onset,
        "rngstate": attempt.rngstate,
        "threshold": attempt.threshold,
        "start": attempt.start,
        "time_frac": attempt.start / attempt.onset,
        "kind": attempt.kind,
        "ok": int(attempt.ok),
        "phase": attempt.phase,
        "depth": attempt.depth,
        "death_step": "" if attempt.ok else attempt.start + attempt.depth,
        "origin_x": attempt.origin_x,
        "origin_y": attempt.origin_y,
        "heading": attempt.heading,
        "check_horizon": attempt.check_horizon,
        "exogenous_checked": len(cell_rows),
        "required_black_count": required_black,
        "actual_black_count": actual_black,
        "mismatch_count": len(bad),
        "missing_black_count": missing,
        "frontier_black_collision_count": frontier,
        "prefix_checked_to_death": len(prefix_rows),
        "prefix_mismatch_to_death": len(prefix_bad),
        "first_bad_offset": "" if first_bad is None else first_bad["offset"],
        "first_bad_rel_x": "" if first_bad is None else first_bad["rel_x"],
        "first_bad_rel_y": "" if first_bad is None else first_bad["rel_y"],
        "first_bad_abs_x": "" if first_bad is None else first_bad["abs_x"],
        "first_bad_abs_y": "" if first_bad is None else first_bad["abs_y"],
        "first_bad_kind": "" if first_bad is None else first_bad["bad_kind"],
        "first_bad_is_death": "" if first_bad is None or attempt.ok else int(int(first_bad["offset"]) == attempt.depth),
    }


def collect_orbit(
    orbit,
    locks: list[Lock],
    schedules: dict[int, list[ExogenousRead]],
    vector_horizon: int,
    entry_horizon: int,
    smin: int,
    smax: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_start: dict[int, list[Lock]] = defaultdict(list)
    for lock in locks:
        by_start[lock.start].append(lock)

    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    attempts: list[dict[str, object]] = []
    cells: list[dict[str, object]] = []
    lock_index = 0
    x = y = h = 0
    for t in range(orbit.onset_dump + 1):
        for lock in by_start.get(t, ()):
            kind = "entry" if lock.start == orbit.onset_dump else "pre_onset_lock"
            check_horizon = entry_horizon if kind == "entry" else max(vector_horizon, lock.depth)
            attempt_id = f"{orbit.index}:{lock_index}"
            attempt = GateAttempt(
                idx=orbit.index,
                shard=orbit.shard,
                onset=orbit.onset_dump,
                rngstate=orbit.rngstate,
                threshold=lock.threshold,
                start=lock.start,
                kind=kind,
                ok=(kind == "entry"),
                phase=lock.phase,
                depth=lock.depth,
                origin_x=x,
                origin_y=y,
                heading=h,
                check_horizon=check_horizon,
            )
            attempt_cells = []
            for read in schedules[lock.phase]:
                if read.offset > check_horizon:
                    break
                row = cell_status(black, attempt, read)
                row.update(
                    {
                        "attempt_id": attempt_id,
                        "idx": orbit.index,
                        "lock_index": lock_index,
                        "start": lock.start,
                        "kind": kind,
                        "phase": lock.phase,
                    }
                )
                attempt_cells.append(row)
            summary = summarize_attempt_cells(attempt, attempt_cells)
            summary["attempt_id"] = attempt_id
            summary["lock_index"] = lock_index
            for row in attempt_cells:
                row["is_first_bad"] = int(row["offset"] == summary["first_bad_offset"])
            attempts.append(summary)
            cells.extend(attempt_cells)
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
    return attempts, cells


def geometry_rows(attempts: list[dict[str, object]]) -> list[dict[str, object]]:
    by_idx: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in attempts:
        by_idx[int(row["idx"])].append(row)
    out: list[dict[str, object]] = []
    for idx, rows in sorted(by_idx.items()):
        rows.sort(key=lambda r: int(r["start"]))
        for a, b in zip(rows, rows[1:]):
            origin_l1 = abs(int(a["origin_x"]) - int(b["origin_x"])) + abs(int(a["origin_y"]) - int(b["origin_y"]))
            origin_linf = max(abs(int(a["origin_x"]) - int(b["origin_x"])), abs(int(a["origin_y"]) - int(b["origin_y"])))
            if a["first_bad_abs_x"] != "" and b["first_bad_abs_x"] != "":
                critical_l1: int | str = abs(int(a["first_bad_abs_x"]) - int(b["first_bad_abs_x"])) + abs(
                    int(a["first_bad_abs_y"]) - int(b["first_bad_abs_y"])
                )
                same_critical: int | str = int(
                    int(a["first_bad_abs_x"]) == int(b["first_bad_abs_x"])
                    and int(a["first_bad_abs_y"]) == int(b["first_bad_abs_y"])
                )
            else:
                critical_l1 = ""
                same_critical = ""
            out.append(
                {
                    "idx": idx,
                    "prev_attempt_id": a["attempt_id"],
                    "next_attempt_id": b["attempt_id"],
                    "gap_steps": int(b["start"]) - int(a["start"]),
                    "prev_phase": a["phase"],
                    "next_phase": b["phase"],
                    "same_phase": int(a["phase"] == b["phase"]),
                    "prev_ok": a["ok"],
                    "next_ok": b["ok"],
                    "origin_l1": origin_l1,
                    "origin_linf": origin_linf,
                    "same_origin": int(a["origin_x"] == b["origin_x"] and a["origin_y"] == b["origin_y"]),
                    "heading_delta_mod4": (int(b["heading"]) - int(a["heading"])) & 3,
                    "critical_l1": critical_l1,
                    "same_critical_cell": same_critical,
                }
            )
    return out


def summarize(attempts: list[dict[str, object]], cells: list[dict[str, object]], geom: list[dict[str, object]]) -> dict[str, object]:
    failures = [r for r in attempts if not int(r["ok"])]
    entries = [r for r in attempts if int(r["ok"])]
    mismatch_counts = [int(r["mismatch_count"]) for r in failures]
    origin_l1 = [int(r["origin_l1"]) for r in geom]
    critical_l1 = [int(r["critical_l1"]) for r in geom if r["critical_l1"] != ""]
    bad_kind = Counter(str(r["first_bad_kind"]) for r in failures if r["first_bad_kind"])
    phase_counts = Counter(int(r["phase"]) for r in attempts)
    phase_ok = Counter(int(r["phase"]) for r in entries)
    depth_mismatch = sum(1 for r in failures if r["first_bad_is_death"] != 1)
    same_origin = sum(int(r["same_origin"]) for r in geom)
    same_critical = sum(int(r["same_critical_cell"]) for r in geom if r["same_critical_cell"] != "")
    return {
        "attempts": len(attempts),
        "entries": len(entries),
        "failures": len(failures),
        "cells": len(cells),
        "first_bad_not_at_death": depth_mismatch,
        "bad_kind_counts": dict(sorted(bad_kind.items())),
        "mismatch_count_after_vector_horizon": quantiles(mismatch_counts),
        "origin_l1": quantiles(origin_l1),
        "critical_l1": quantiles(critical_l1),
        "same_origin_consecutive": same_origin,
        "same_origin_rate": same_origin / len(geom) if geom else None,
        "same_critical_consecutive": same_critical,
        "same_critical_rate": same_critical / len(critical_l1) if critical_l1 else None,
        "heading_delta_counts": dict(sorted(Counter(int(r["heading_delta_mod4"]) for r in geom).items())),
        "top_phases": [
            {
                "phase": phase,
                "attempts": count,
                "ok": phase_ok[phase],
                "ok_rate": phase_ok[phase] / count,
            }
            for phase, count in phase_counts.most_common(16)
        ],
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str] | None = None) -> None:
    if not rows:
        return
    fields = list(fieldnames) if fieldnames is not None else list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(summary: dict[str, object]) -> None:
    print(
        f"attempts={summary['attempts']} entries={summary['entries']} failures={summary['failures']} "
        f"cells={summary['cells']} first_bad_not_at_death={summary['first_bad_not_at_death']}"
    )
    print(
        f"origin L1 median={summary['origin_l1']['median']} q25={summary['origin_l1']['q25']} "
        f"q75={summary['origin_l1']['q75']} max={summary['origin_l1']['max']}"
    )
    print(
        f"critical L1 median={summary['critical_l1']['median']} same={summary['same_critical_consecutive']} "
        f"origin same={summary['same_origin_consecutive']}"
    )
    print(f"bad kinds: {summary['bad_kind_counts']}")
    print(f"heading deltas: {summary['heading_delta_counts']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--entry-horizon", type=int, default=1248)
    ap.add_argument("--vector-horizon", type=int, default=208)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "checklist_vector_geometry")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    started = time.perf_counter()
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    tail_steps = max(args.entry_horizon, args.vector_horizon, max(LOCK_THRESHOLDS), 208)

    all_attempts: list[dict[str, object]] = []
    all_cells: list[dict[str, object]] = []
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
            depth=args.entry_horizon,
            is_gate=True,
        )
        gate_locks = dedupe_locks(locks, entry)
        max_check = max([args.entry_horizon, args.vector_horizon] + [lock.depth for lock in gate_locks])
        schedules = make_exogenous_schedule(w0_bits, max_check + 1)
        attempts, cells = collect_orbit(
            orbit, gate_locks, schedules, args.vector_horizon, args.entry_horizon, args.smin, args.smax
        )
        all_attempts.extend(attempts)
        all_cells.extend(cells)
        completed += 1
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} attempts={len(attempts):3d} "
            f"cells={len(cells):5d} entry_phase={entry.phase}"
        )

    if not all_attempts:
        print("Nessuna orbita completata; nessun output.")
        return 1

    geom = geometry_rows(all_attempts)
    summary = summarize(all_attempts, all_cells, geom)
    summary.update(
        {
            "source": str(args.dumps),
            "orbits_requested": len(dumps),
            "orbits_completed": completed,
            "vector_horizon": args.vector_horizon,
            "entry_horizon": args.entry_horizon,
            "elapsed_seconds": time.perf_counter() - started,
        }
    )

    out_prefix: Path = args.out_prefix
    attempts_csv = out_prefix.with_name(out_prefix.name + "_attempts.csv")
    cells_csv = out_prefix.with_name(out_prefix.name + "_cells.csv")
    geometry_csv = out_prefix.with_name(out_prefix.name + "_geometry.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(attempts_csv, all_attempts)
    write_csv(cells_csv, all_cells)
    write_csv(geometry_csv, geom)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print_summary(summary)
    print(f"\nCSV attempts: {attempts_csv}")
    print(f"CSV cells: {cells_csv}")
    print(f"CSV geometry: {geometry_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits completed={completed}, elapsed={time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
