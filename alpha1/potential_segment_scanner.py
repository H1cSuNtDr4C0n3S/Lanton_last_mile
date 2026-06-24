#!/usr/bin/env python3
"""potential_segment_scanner.py - section 67 rough Phi falsifier.

This scanner is intentionally empirical and destructive: it defines a few crude
finite-horizon proxies for a global debris potential Phi and tries to falsify
monotone decrement on segments with deep-black events.

Two anchor families are measured:
  * gate anchors: the deduplicated gate attempts used in sections 63/66;
  * grid anchors: fixed-stride, non-gate times before onset.

For every anchor and horizon L, the scanner evaluates all 22 gate phases and
builds finite proxies where lower is "closer to entry":
  * phi_best_deficit: (L+1) - best compatible h_g;
  * phi_top3_deficit: sum of the top 3 compatible deficits;
  * phi_sum_deficit: sum of all compatible deficits.

A segment falsifies a proxy when it contains at least one deep-black event,
contains no entry endpoint, and Phi(next) >= Phi(prev).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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
    lock_depths_over_threshold,
    lower_bound,
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


PHI_COLUMNS = (
    "phi_actual_depth",
    "phi_actual_mass_104",
    "phi_actual_mass_208",
    "phi_best22_depth",
    "phi_best22_mass_104",
    "phi_best22_mass_208",
    "phi_best_deficit",
    "phi_top3_deficit",
    "phi_sum_deficit",
)


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


def region_count_times(values: tuple[int, ...], a: int, b: int) -> int:
    return lower_bound(values, b) - lower_bound(values, a)


def phase_metrics(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    schedule: list[ExogenousRead],
    horizon: int,
) -> dict[str, object]:
    first_bad_offset: int | None = None
    first_bad_kind = ""
    first_bad_l1: int | str = ""
    first_bad_linf: int | str = ""
    mismatch_count = 0
    mass_104 = 0.0
    mass_208 = 0.0
    checked = 0
    for read in schedule:
        if read.offset > horizon:
            break
        checked += 1
        ax, ay = rel_to_abs(origin_x, origin_y, heading, read.rel_x, read.rel_y)
        actual_black = (ax, ay) in black
        if actual_black != read.required_black:
            mismatch_count += 1
            mass_104 += math.exp(-read.offset / 104.0)
            mass_208 += math.exp(-read.offset / 208.0)
            if first_bad_offset is None:
                first_bad_offset = read.offset
                first_bad_l1 = abs(read.rel_x) + abs(read.rel_y)
                first_bad_linf = max(abs(read.rel_x), abs(read.rel_y))
                if read.required_black and not actual_black:
                    first_bad_kind = "missing_black"
                elif (not read.required_black) and actual_black:
                    first_bad_kind = "frontier_black_collision"
                else:
                    first_bad_kind = "color_mismatch"
    h = horizon + 1 if first_bad_offset is None else first_bad_offset
    return {
        "h": h,
        "clear": int(first_bad_offset is None),
        "first_bad_offset": "" if first_bad_offset is None else first_bad_offset,
        "first_bad_kind": first_bad_kind,
        "first_bad_l1": first_bad_l1,
        "first_bad_linf": first_bad_linf,
        "mismatch_count": mismatch_count,
        "max_offset_saved": horizon,
        "mass_104": mass_104,
        "mass_208": mass_208,
        "checked": checked,
    }


def phi_rows_for_anchor(
    meta: dict[str, object],
    black: set[tuple[int, int]],
    x: int,
    y: int,
    h: int,
    schedules: dict[int, list[ExogenousRead]],
    phase_first_bits: dict[int, int],
    horizons: tuple[int, ...],
) -> list[dict[str, object]]:
    observed_turn_bit = 0 if (x, y) in black else 1
    out: list[dict[str, object]] = []
    for horizon in horizons:
        phase_rows: list[tuple[int, int, str, bool]] = []
        phase_payloads: dict[int, dict[str, object]] = {}
        for phase in GATE_PHASES:
            compatible = phase_first_bits[phase] == observed_turn_bit
            metrics = phase_metrics(black, x, y, h, schedules[phase], horizon)
            depth = int(metrics["h"])
            kind = str(metrics["first_bad_kind"])
            phase_rows.append((phase, depth, kind, compatible))
            phase_payloads[phase] = metrics
        compatible_rows = [row for row in phase_rows if row[3]]
        compatible_depths = sorted((depth for _phase, depth, _kind, _compatible in compatible_rows), reverse=True)
        best_phase, best_h, best_kind, _ = max(compatible_rows, key=lambda row: row[1])
        best_depth_proxy = 0.0 if best_h == horizon + 1 else math.exp(-best_h / 104.0)
        best22_mass_104 = min(float(phase_payloads[phase]["mass_104"]) for phase, _depth, _kind, _compatible in compatible_rows)
        best22_mass_208 = min(float(phase_payloads[phase]["mass_208"]) for phase, _depth, _kind, _compatible in compatible_rows)
        deficits = [(horizon + 1) - depth for depth in compatible_depths]
        top3 = deficits[:3]
        clear_count = sum(1 for depth in compatible_depths if depth == horizon + 1)
        bad_kind_counts = Counter(kind for _phase, _depth, kind, _compatible in compatible_rows if kind)
        gate_phase = meta.get("gate_phase", "")
        actual_metrics = phase_payloads.get(int(gate_phase)) if gate_phase != "" else None
        if actual_metrics is None:
            phi_actual_depth: float | str = ""
            phi_actual_mass_104: float | str = ""
            phi_actual_mass_208: float | str = ""
            actual_h: int | str = ""
            actual_first_bad_offset: int | str = ""
            actual_first_bad_kind = ""
            actual_first_bad_l1: int | str = ""
            actual_first_bad_linf: int | str = ""
            actual_mismatch_count: int | str = ""
            actual_max_offset_saved: int | str = ""
        else:
            actual_h = int(actual_metrics["h"])
            phi_actual_depth = 0.0 if actual_h == horizon + 1 else math.exp(-actual_h / 104.0)
            phi_actual_mass_104 = float(actual_metrics["mass_104"])
            phi_actual_mass_208 = float(actual_metrics["mass_208"])
            actual_first_bad_offset = actual_metrics["first_bad_offset"]
            actual_first_bad_kind = str(actual_metrics["first_bad_kind"])
            actual_first_bad_l1 = actual_metrics["first_bad_l1"]
            actual_first_bad_linf = actual_metrics["first_bad_linf"]
            actual_mismatch_count = int(actual_metrics["mismatch_count"])
            actual_max_offset_saved = int(actual_metrics["max_offset_saved"])
        row = {
            **meta,
            "horizon": horizon,
            "observed_turn_bit": observed_turn_bit,
            "compatible_phase_count": len(compatible_rows),
            "best_phase": best_phase,
            "best_h": best_h,
            "best_bad_kind": best_kind,
            "compatible_clear_phase_count": clear_count,
            "any_compatible_clear": int(clear_count > 0),
            "compatible_median_h": statistics.median(depth for _phase, depth, _kind, _compatible in compatible_rows),
            "compatible_min_h": min(depth for _phase, depth, _kind, _compatible in compatible_rows),
            "actual_h": actual_h,
            "actual_first_bad_offset": actual_first_bad_offset,
            "actual_first_bad_kind": actual_first_bad_kind,
            "actual_first_bad_l1": actual_first_bad_l1,
            "actual_first_bad_linf": actual_first_bad_linf,
            "actual_mismatch_count": actual_mismatch_count,
            "actual_max_offset_saved": actual_max_offset_saved,
            "phi_actual_depth": phi_actual_depth,
            "phi_actual_mass_104": phi_actual_mass_104,
            "phi_actual_mass_208": phi_actual_mass_208,
            "phi_best22_depth": best_depth_proxy,
            "phi_best22_mass_104": best22_mass_104,
            "phi_best22_mass_208": best22_mass_208,
            "phi_best_deficit": (horizon + 1) - best_h,
            "phi_top3_deficit": sum(top3),
            "phi_sum_deficit": sum(deficits),
            "missing_black_count": bad_kind_counts["missing_black"],
            "frontier_black_collision_count": bad_kind_counts["frontier_black_collision"],
        }
        out.append(row)
    return out


def gate_anchor_meta(orbit, gate_locks: list[Lock]) -> dict[int, list[dict[str, object]]]:
    out: dict[int, list[dict[str, object]]] = {}
    for lock_index, lock in enumerate(gate_locks):
        kind = "entry" if lock.start == orbit.onset_dump else "pre_onset_lock"
        out.setdefault(lock.start, []).append(
            {
            "anchor_id": f"{orbit.index}:gate:{lock_index}",
            "idx": orbit.index,
            "anchor_family": "gate",
            "start": lock.start,
            "time_frac": lock.start / orbit.onset_dump,
            "is_gate_anchor": 1,
            "is_entry": int(kind == "entry"),
            "gate_phase": lock.phase,
            "threshold": lock.threshold,
            "gate_depth": lock.depth,
            }
        )
    return out


def grid_anchor_meta(
    orbit,
    stride: int,
    gate_starts: set[int],
    include_gate_times: bool,
) -> dict[int, list[dict[str, object]]]:
    out: dict[int, list[dict[str, object]]] = {}
    grid_index = 0
    for start in range(0, orbit.onset_dump, stride):
        if (not include_gate_times) and start in gate_starts:
            continue
        out.setdefault(start, []).append(
            {
                "anchor_id": f"{orbit.index}:grid:{grid_index}",
                "idx": orbit.index,
                "anchor_family": "grid",
                "start": start,
                "time_frac": start / orbit.onset_dump,
                "is_gate_anchor": int(start in gate_starts),
                "is_entry": 0,
                "gate_phase": "",
                "threshold": "",
                "gate_depth": "",
            }
        )
        grid_index += 1
    return out


def collect_anchor_rows(
    orbit,
    anchor_meta_by_time: dict[int, list[dict[str, object]]],
    schedules: dict[int, list[ExogenousRead]],
    phase_first_bits: dict[int, int],
    horizons: tuple[int, ...],
    depths: dict[int, int],
    smin: int,
    smax: int,
) -> list[dict[str, object]]:
    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    rows: list[dict[str, object]] = []
    x = y = h = 0
    for t in range(orbit.onset_dump + 1):
        metas = anchor_meta_by_time.get(t)
        if metas is not None:
            for meta in metas:
                full_meta = {
                    **meta,
                    "onset": orbit.onset_dump,
                    "rngstate": orbit.rngstate,
                    "shard": orbit.shard,
                    "origin_x": x,
                    "origin_y": y,
                    "heading": h,
                    "D_ge_40": depths.get(t, 0),
                }
                rows.extend(phi_rows_for_anchor(full_meta, black, x, y, h, schedules, phase_first_bits, horizons))
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
    return rows


def segment_rows(
    anchor_rows: list[dict[str, object]],
    deep: bytearray,
    bite_times: tuple[int, ...],
) -> list[dict[str, object]]:
    by_key: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in anchor_rows:
        by_key[(str(row["anchor_family"]), int(row["horizon"]))].append(row)

    out: list[dict[str, object]] = []
    for (family, horizon), rows in sorted(by_key.items()):
        rows.sort(key=lambda row: int(row["start"]))
        for prev, nxt in zip(rows, rows[1:]):
            a = int(prev["start"])
            b = int(nxt["start"])
            deep_count = sum(deep[a:b])
            bite_count = region_count_times(bite_times, a, b)
            has_entry_endpoint = int(nxt["is_entry"])
            payload: dict[str, object] = {
                "idx": prev["idx"],
                "anchor_family": family,
                "horizon": horizon,
                "prev_anchor_id": prev["anchor_id"],
                "next_anchor_id": nxt["anchor_id"],
                "prev_start": a,
                "next_start": b,
                "gap_steps": b - a,
                "deep_black_count": deep_count,
                "fresh_bite_count": bite_count,
                "has_entry_endpoint": has_entry_endpoint,
                "prev_D_ge_40": prev["D_ge_40"],
                "next_D_ge_40": nxt["D_ge_40"],
                "prev_any_compatible_clear": prev["any_compatible_clear"],
                "next_any_compatible_clear": nxt["any_compatible_clear"],
            }
            for name in PHI_COLUMNS:
                if prev[name] == "" or nxt[name] == "":
                    payload[f"prev_{name}"] = ""
                    payload[f"next_{name}"] = ""
                    payload[f"delta_{name}"] = ""
                    payload[f"violates_{name}"] = ""
                    continue
                prev_value = float(prev[name])
                next_value = float(nxt[name])
                delta = next_value - prev_value
                payload[f"prev_{name}"] = prev_value
                payload[f"next_{name}"] = next_value
                payload[f"delta_{name}"] = delta
                payload[f"violates_{name}"] = int(deep_count > 0 and not has_entry_endpoint and delta >= 0)
            out.append(payload)
    return out


def summarize(anchor_rows: list[dict[str, object]], segments: list[dict[str, object]], horizons: tuple[int, ...]) -> dict[str, object]:
    by_family_horizon: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in anchor_rows:
        by_family_horizon[(str(row["anchor_family"]), int(row["horizon"]))].append(row)
    anchor_summary = []
    for (family, horizon), rows in sorted(by_family_horizon.items()):
        anchor_summary.append(
            {
                "anchor_family": family,
                "horizon": horizon,
                "anchors": len(rows),
                "any_compatible_clear": sum(int(r["any_compatible_clear"]) for r in rows),
                "any_compatible_clear_rate": sum(int(r["any_compatible_clear"]) for r in rows) / len(rows),
                "best_h": quantiles(int(r["best_h"]) for r in rows),
                "phi_best_deficit": quantiles(int(r["phi_best_deficit"]) for r in rows),
                "phi_top3_deficit": quantiles(int(r["phi_top3_deficit"]) for r in rows),
                "phi_sum_deficit": quantiles(int(r["phi_sum_deficit"]) for r in rows),
            }
        )

    by_segment_key: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in segments:
        by_segment_key[(str(row["anchor_family"]), int(row["horizon"]))].append(row)
    segment_summary = []
    for (family, horizon), rows in sorted(by_segment_key.items()):
        eligible = [r for r in rows if int(r["deep_black_count"]) > 0 and not int(r["has_entry_endpoint"])]
        payload: dict[str, object] = {
            "anchor_family": family,
            "horizon": horizon,
            "segments": len(rows),
            "eligible_deep_no_entry": len(eligible),
            "deep_black_count": quantiles(int(r["deep_black_count"]) for r in rows),
            "fresh_bite_count": quantiles(int(r["fresh_bite_count"]) for r in rows),
        }
        for name in PHI_COLUMNS:
            measurable = [r for r in eligible if r[f"violates_{name}"] != ""]
            violations = sum(int(r[f"violates_{name}"]) for r in measurable)
            top_violations = sorted(
                (r for r in measurable if int(r[f"violates_{name}"])),
                key=lambda r: (-int(r["deep_black_count"]), -float(r[f"delta_{name}"])),
            )[:10]
            payload[f"{name}_violations"] = violations
            payload[f"{name}_measurable"] = len(measurable)
            payload[f"{name}_violation_rate"] = violations / len(measurable) if measurable else None
            payload[f"delta_{name}"] = quantiles(float(r[f"delta_{name}"]) for r in measurable)
            payload[f"{name}_top_violations"] = [
                {
                    "idx": row["idx"],
                    "prev_anchor_id": row["prev_anchor_id"],
                    "next_anchor_id": row["next_anchor_id"],
                    "prev_start": row["prev_start"],
                    "next_start": row["next_start"],
                    "deep_black_count": row["deep_black_count"],
                    "fresh_bite_count": row["fresh_bite_count"],
                    f"delta_{name}": row[f"delta_{name}"],
                    f"prev_{name}": row[f"prev_{name}"],
                    f"next_{name}": row[f"next_{name}"],
                }
                for row in top_violations
            ]
        segment_summary.append(payload)

    return {
        "horizons": horizons,
        "phi_columns": PHI_COLUMNS,
        "anchors": len(anchor_rows),
        "segments": len(segments),
        "anchor_summary": anchor_summary,
        "segment_summary": segment_summary,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--horizons", default="208,512,1600")
    ap.add_argument("--grid-stride", type=int, default=1040)
    ap.add_argument("--include-gate-times-in-grid", action="store_true")
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "potential_segment_scanner")
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
    schedules = make_exogenous_schedule(w0_bits, max_horizon + 1)
    tail_steps = max(max_horizon, max(LOCK_THRESHOLDS), 208)

    all_anchor_rows: list[dict[str, object]] = []
    all_segment_rows: list[dict[str, object]] = []
    completed = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP: max-seconds={args.max_seconds:.1f}; completate={completed}")
            break
        turns, deep, sim_bites, _side, _dens = simulate_orbit(
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
        gate_meta = gate_anchor_meta(orbit, gate_locks)
        grid_meta = grid_anchor_meta(
            orbit, args.grid_stride, set(gate_meta), include_gate_times=args.include_gate_times_in_grid
        )
        depths = lock_depths_over_threshold(turns, orbit.onset_dump, w0_bits, threshold=40)

        orbit_anchor_rows: list[dict[str, object]] = []
        for meta_by_time in (gate_meta, grid_meta):
            orbit_anchor_rows.extend(
                collect_anchor_rows(
                    orbit, meta_by_time, schedules, phase_first_bits, horizons, depths, args.smin, args.smax
                )
            )
        orbit_segments = segment_rows(orbit_anchor_rows, deep, orbit.bite_times)
        all_anchor_rows.extend(orbit_anchor_rows)
        all_segment_rows.extend(orbit_segments)
        completed += 1
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} "
            f"gate_anchors={sum(len(v) for v in gate_meta.values()):3d} "
            f"grid_anchors={sum(len(v) for v in grid_meta.values()):3d} "
            f"segments={len(orbit_segments):4d}"
        )

    if not all_anchor_rows:
        print("Nessuna orbita completata; nessun output.")
        return 1

    payload = summarize(all_anchor_rows, all_segment_rows, horizons)
    payload.update(
        {
            "source": str(args.dumps),
            "orbits_requested": len(dumps),
            "orbits_completed": completed,
            "grid_stride": args.grid_stride,
            "include_gate_times_in_grid": args.include_gate_times_in_grid,
            "elapsed_seconds": time.perf_counter() - started,
        }
    )

    out_prefix: Path = args.out_prefix
    anchors_csv = out_prefix.with_name(out_prefix.name + "_anchors.csv")
    segments_csv = out_prefix.with_name(out_prefix.name + "_segments.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(anchors_csv, all_anchor_rows)
    write_csv(segments_csv, all_segment_rows)
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nCSV anchors: {anchors_csv}")
    print(f"CSV segments: {segments_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits completed={completed}, elapsed={time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
