#!/usr/bin/env python3
"""door_defect_profile.py - section 66 profile of defects over the 22 gates.

For every deduplicated gate attempt from section 63, evaluate all 22 admissible
gateway phases against the debris field at the attempt time.  For each horizon L
we record h_g(L), the first bad exogenous read for phase g, or L+1 if the phase
is clear through L.

This is deliberately a measurement tool, not a proof.  It turns the §65
non-locality diagnosis into a global profile over moving doors.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
from collections import Counter, defaultdict
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


def parse_horizons(text: str) -> tuple[int, ...]:
    values = tuple(sorted({int(part.strip()) for part in text.split(",") if part.strip()}))
    if not values or values[0] <= 0:
        raise ValueError("--horizons deve contenere interi positivi")
    return values


def quantiles(values: Iterable[int | float]) -> dict[str, int | float | None]:
    vals = sorted(values)
    if not vals:
        return {"min": None, "q25": None, "median": None, "q75": None, "max": None, "mean": None}
    if len(vals) >= 4:
        qs = statistics.quantiles(vals, n=4)
        q25, q75 = qs[0], qs[2]
    else:
        q25, q75 = vals[0], vals[-1]
    return {
        "min": vals[0],
        "q25": q25,
        "median": statistics.median(vals),
        "q75": q75,
        "max": vals[-1],
        "mean": sum(vals) / len(vals),
    }


def bad_kind(required_black: bool, actual_black: bool) -> str:
    if required_black and not actual_black:
        return "missing_black"
    if (not required_black) and actual_black:
        return "frontier_black_collision"
    return "color_mismatch"


def first_defect(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    schedule: list[ExogenousRead],
    horizon: int,
) -> dict[str, object]:
    checked = 0
    for read in schedule:
        if read.offset > horizon:
            break
        ax, ay = rel_to_abs(origin_x, origin_y, heading, read.rel_x, read.rel_y)
        actual_black = (ax, ay) in black
        checked += 1
        if actual_black != read.required_black:
            return {
                "h": read.offset,
                "clear": 0,
                "first_bad_offset": read.offset,
                "bad_kind": bad_kind(read.required_black, actual_black),
                "rel_x": read.rel_x,
                "rel_y": read.rel_y,
                "abs_x": ax,
                "abs_y": ay,
                "l1": abs(read.rel_x) + abs(read.rel_y),
                "linf": max(abs(read.rel_x), abs(read.rel_y)),
                "required_black": int(read.required_black),
                "actual_black": int(actual_black),
                "exogenous_reads_checked": checked,
            }
    return {
        "h": horizon + 1,
        "clear": 1,
        "first_bad_offset": "",
        "bad_kind": "",
        "rel_x": "",
        "rel_y": "",
        "abs_x": "",
        "abs_y": "",
        "l1": "",
        "linf": "",
        "required_black": "",
        "actual_black": "",
        "exogenous_reads_checked": checked,
    }


def attempt_kind(lock: Lock, onset: int) -> str:
    return "entry" if lock.start == onset else "pre_onset_lock"


def collect_orbit(
    orbit,
    gate_locks: list[Lock],
    schedules: dict[int, list[ExogenousRead]],
    phase_first_bits: dict[int, int],
    horizons: tuple[int, ...],
    smin: int,
    smax: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    by_start: dict[int, list[Lock]] = defaultdict(list)
    for lock in gate_locks:
        by_start[lock.start].append(lock)

    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    profile_rows: list[dict[str, object]] = []
    attempt_rows: list[dict[str, object]] = []
    attempt_meta: list[dict[str, object]] = []
    x = y = h = 0
    lock_index = 0

    for t in range(orbit.onset_dump + 1):
        for lock in by_start.get(t, ()):
            kind = attempt_kind(lock, orbit.onset_dump)
            attempt_id = f"{orbit.index}:{lock_index}"
            observed_turn_bit = 0 if (x, y) in black else 1
            meta = {
                "attempt_id": attempt_id,
                "idx": orbit.index,
                "shard": orbit.shard,
                "onset": orbit.onset_dump,
                "rngstate": orbit.rngstate,
                "threshold": lock.threshold,
                "start": lock.start,
                "time_frac": lock.start / orbit.onset_dump,
                "kind": kind,
                "actual_ok": int(kind == "entry"),
                "actual_phase": lock.phase,
                "depth": lock.depth,
                "death_step": "" if kind == "entry" else lock.start + lock.depth,
                "origin_x": x,
                "origin_y": y,
                "heading": h,
                "observed_turn_bit": observed_turn_bit,
            }
            attempt_meta.append(meta)

            rows_by_horizon: dict[int, list[dict[str, object]]] = defaultdict(list)
            for eval_phase in GATE_PHASES:
                eval_turn_bit = phase_first_bits[eval_phase]
                for horizon in horizons:
                    defect = first_defect(black, x, y, h, schedules[eval_phase], horizon)
                    row = {
                        **meta,
                        "horizon": horizon,
                        "eval_phase": eval_phase,
                        "eval_turn_bit": eval_turn_bit,
                        "turn_compatible": int(eval_turn_bit == observed_turn_bit),
                        "is_actual_phase": int(eval_phase == lock.phase),
                        **defect,
                    }
                    profile_rows.append(row)
                    rows_by_horizon[horizon].append(row)

            for horizon in horizons:
                rows = rows_by_horizon[horizon]
                best_h = max(int(r["h"]) for r in rows)
                best = [r for r in rows if int(r["h"]) == best_h]
                compatible_rows = [r for r in rows if int(r["turn_compatible"])]
                compatible_best_h = max(int(r["h"]) for r in compatible_rows)
                compatible_best = [r for r in compatible_rows if int(r["h"]) == compatible_best_h]
                actual = next(r for r in rows if int(r["is_actual_phase"]))
                clear_rows = [r for r in rows if int(r["clear"])]
                compatible_clear_rows = [r for r in compatible_rows if int(r["clear"])]
                attempt_rows.append(
                    {
                        **meta,
                        "horizon": horizon,
                        "actual_h": actual["h"],
                        "actual_clear": actual["clear"],
                        "actual_bad_kind": actual["bad_kind"],
                        "actual_first_bad_offset": actual["first_bad_offset"],
                        "best_h": best_h,
                        "best_phase": best[0]["eval_phase"],
                        "best_phase_count": len(best),
                        "actual_is_best": int(any(int(r["is_actual_phase"]) for r in best)),
                        "compatible_phase_count": len(compatible_rows),
                        "compatible_best_h": compatible_best_h,
                        "compatible_best_phase": compatible_best[0]["eval_phase"],
                        "compatible_best_phase_count": len(compatible_best),
                        "actual_is_compatible_best": int(any(int(r["is_actual_phase"]) for r in compatible_best)),
                        "compatible_clear_phase_count": len(compatible_clear_rows),
                        "clear_phase_count": len(clear_rows),
                        "any_clear": int(bool(clear_rows)),
                        "median_h": statistics.median(int(r["h"]) for r in rows),
                        "compatible_median_h": statistics.median(int(r["h"]) for r in compatible_rows),
                        "min_h": min(int(r["h"]) for r in rows),
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

    return profile_rows, attempt_rows, attempt_meta


def summarize_groups(rows: list[dict[str, object]], key_fields: tuple[str, ...]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[field] for field in key_fields)].append(row)

    out: list[dict[str, object]] = []
    for key, vals in sorted(groups.items()):
        payload = dict(zip(key_fields, key))
        best_h = [int(r["best_h"]) for r in vals]
        actual_h = [int(r["actual_h"]) for r in vals]
        payload.update(
            {
                "attempts": len(vals),
                "entries": sum(int(r["actual_ok"]) for r in vals),
                "failures": sum(1 - int(r["actual_ok"]) for r in vals),
                "any_clear": sum(int(r["any_clear"]) for r in vals),
                "any_clear_rate": sum(int(r["any_clear"]) for r in vals) / len(vals),
                "actual_is_best": sum(int(r["actual_is_best"]) for r in vals),
                "actual_is_best_rate": sum(int(r["actual_is_best"]) for r in vals) / len(vals),
                "clear_phase_count_total": sum(int(r["clear_phase_count"]) for r in vals),
                "best_h": quantiles(best_h),
                "actual_h": quantiles(actual_h),
            }
        )
        out.append(payload)
    return out


def summarize_profile(profile_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[int, str], list[dict[str, object]]] = defaultdict(list)
    for row in profile_rows:
        if int(row["is_actual_phase"]):
            bucket = "actual_phase"
        elif int(row["turn_compatible"]):
            bucket = "compatible_off_phase_baseline"
        else:
            bucket = "incompatible_off_phase_baseline"
        groups[(int(row["horizon"]), bucket)].append(row)
    out: list[dict[str, object]] = []
    for (horizon, bucket), rows in sorted(groups.items()):
        h_vals = [int(r["h"]) for r in rows]
        clear = sum(int(r["clear"]) for r in rows)
        bad_kinds = Counter(str(r["bad_kind"]) for r in rows if r["bad_kind"])
        out.append(
            {
                "horizon": horizon,
                "bucket": bucket,
                "rows": len(rows),
                "clear": clear,
                "clear_rate": clear / len(rows),
                "h": quantiles(h_vals),
                "bad_kind_counts": dict(sorted(bad_kinds.items())),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str] | None = None) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(fieldnames) if fieldnames is not None else list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--horizons", default="208,512,1600")
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "door_defect_profile")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    started = time.perf_counter()
    horizons = parse_horizons(args.horizons)
    max_horizon = max(horizons)
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    phase_first_bits = {phase: w0_bits[phase] for phase in GATE_PHASES}
    tail_steps = max(max_horizon, max(LOCK_THRESHOLDS), 208)
    schedules = make_exogenous_schedule(w0_bits, max_horizon + 1)

    all_profile_rows: list[dict[str, object]] = []
    all_attempt_rows: list[dict[str, object]] = []
    all_attempt_meta: list[dict[str, object]] = []
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
            depth=max_horizon,
            is_gate=True,
        )
        gate_locks = dedupe_locks(locks, entry)
        profile_rows, attempt_rows, attempt_meta = collect_orbit(
            orbit, gate_locks, schedules, phase_first_bits, horizons, args.smin, args.smax
        )
        all_profile_rows.extend(profile_rows)
        all_attempt_rows.extend(attempt_rows)
        all_attempt_meta.extend(attempt_meta)
        completed += 1
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} attempts={len(attempt_meta):3d} "
            f"profile_rows={len(profile_rows):5d} entry_phase={entry.phase}"
        )

    if not all_attempt_rows:
        print("Nessuna orbita completata; nessun output.")
        return 1

    horizon_summary = summarize_groups(all_attempt_rows, ("horizon",))
    orbit_summary = summarize_groups(all_attempt_rows, ("idx", "horizon"))
    profile_summary = summarize_profile(all_profile_rows)
    payload = {
        "source": str(args.dumps),
        "orbits_requested": len(dumps),
        "orbits_completed": completed,
        "horizons": horizons,
        "gate_phases": GATE_PHASES,
        "attempts": len(all_attempt_meta),
        "attempt_horizon_rows": len(all_attempt_rows),
        "profile_rows": len(all_profile_rows),
        "horizon_summary": horizon_summary,
        "profile_summary": profile_summary,
        "elapsed_seconds": time.perf_counter() - started,
    }

    out_prefix: Path = args.out_prefix
    profile_csv = out_prefix.with_name(out_prefix.name + "_rows.csv")
    attempts_csv = out_prefix.with_name(out_prefix.name + "_attempts.csv")
    orbits_csv = out_prefix.with_name(out_prefix.name + "_orbits.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(profile_csv, all_profile_rows)
    write_csv(attempts_csv, all_attempt_rows)
    write_csv(orbits_csv, orbit_summary)
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nCSV rows: {profile_csv}")
    print(f"CSV attempts: {attempts_csv}")
    print(f"CSV orbits: {orbits_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits completed={completed}, elapsed={time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
