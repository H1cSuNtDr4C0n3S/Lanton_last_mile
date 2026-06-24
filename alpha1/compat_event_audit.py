#!/usr/bin/env python3
"""compat_event_audit.py - section 70 pre/post deep-black Phi_compat audit.

This is a deliberately small event-wise audit, not another endpoint scanner.
It reconstructs the same long orbits used by the previous alpha1 probes,
selects a bounded sample of r=4 deep-black reads, and measures h_best^L
immediately before and after the single Langton step that caused the event.

Convention:
  * event time t is the pre-step state used by delta4_long_orbits.py:
    the current cell is black and outside the live r=4 memory window;
  * "pre" evaluates h_best^L at state t, before read/turn/flip/move;
  * "post" evaluates h_best^L at state t+1, after that one step.

Higher h_best is better.  Phi_compat is reported as
0 when h_best == L+1, otherwise exp(-h_best / 104).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

from delta4_long_orbits import (  # noqa: E402
    ALPHA,
    DATA,
    DX,
    DY,
    build_seed,
    compare_bites,
    load_w0_bits,
    parse_dumps,
    simulate_orbit,
)
from lock_checklist_probe import GATE_PHASES, make_exogenous_schedule  # noqa: E402
from potential_segment_scanner import phase_metrics  # noqa: E402


CONVENTION = "pre_state_t_before_step_vs_post_state_t_plus_1_after_step"


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


def select_event_times(
    deep: bytearray,
    max_events: int,
    sample_mode: str,
    include_entry_post: bool,
    min_event_t: int,
) -> tuple[list[int], int]:
    eligible = [
        t
        for t, bit in enumerate(deep)
        if bit and t >= min_event_t and (include_entry_post or t + 1 < len(deep))
    ]
    if max_events <= 0 or len(eligible) <= max_events:
        return eligible, len(eligible)
    if sample_mode == "first":
        return eligible[:max_events], len(eligible)
    if sample_mode == "last":
        return eligible[-max_events:], len(eligible)

    selected_indexes: list[int] = []
    if max_events == 1:
        selected_indexes = [len(eligible) // 2]
    else:
        for i in range(max_events):
            selected_indexes.append(round(i * (len(eligible) - 1) / (max_events - 1)))

    selected: list[int] = []
    seen: set[int] = set()
    for idx in selected_indexes:
        if idx not in seen:
            selected.append(eligible[idx])
            seen.add(idx)
    if len(selected) < max_events:
        for idx, t in enumerate(eligible):
            if idx not in seen:
                selected.append(t)
                seen.add(idx)
                if len(selected) == max_events:
                    break
    selected.sort()
    return selected, len(eligible)


def phi_from_h(h_best: int, horizon: int) -> float:
    return 0.0 if h_best == horizon + 1 else math.exp(-h_best / 104.0)


def best_compat_metrics(
    black: set[tuple[int, int]],
    x: int,
    y: int,
    heading: int,
    schedules,
    phase_first_bits: dict[int, int],
    horizon: int,
) -> dict[str, object]:
    observed_turn_bit = 0 if (x, y) in black else 1
    compatible_rows: list[tuple[int, int, dict[str, object]]] = []
    for phase in GATE_PHASES:
        if phase_first_bits[phase] != observed_turn_bit:
            continue
        metrics = phase_metrics(black, x, y, heading, schedules[phase], horizon)
        compatible_rows.append((phase, int(metrics["h"]), metrics))

    if not compatible_rows:
        raise AssertionError("nessuna fase gate compatibile col primo bit osservato")

    best_phase, h_best, best_metrics = max(compatible_rows, key=lambda item: item[1])
    depths = [h for _phase, h, _metrics in compatible_rows]
    clear_count = sum(1 for h in depths if h == horizon + 1)
    bad_kind_counts = Counter(
        str(metrics["first_bad_kind"]) for _phase, _h, metrics in compatible_rows if metrics["first_bad_kind"]
    )
    return {
        "observed_turn_bit": observed_turn_bit,
        "compatible_phase_count": len(compatible_rows),
        "compatible_clear_phase_count": clear_count,
        "best_phase": best_phase,
        "h_best": h_best,
        "phi_compat": phi_from_h(h_best, horizon),
        "best_bad_kind": str(best_metrics["first_bad_kind"]),
        "best_first_bad_offset": best_metrics["first_bad_offset"],
        "best_first_bad_l1": best_metrics["first_bad_l1"],
        "best_first_bad_linf": best_metrics["first_bad_linf"],
        "compatible_min_h": min(depths),
        "compatible_median_h": statistics.median(depths),
        "missing_black_count": bad_kind_counts["missing_black"],
        "frontier_black_collision_count": bad_kind_counts["frontier_black_collision"],
    }


def advance_one_step(
    black: set[tuple[int, int]],
    x: int,
    y: int,
    heading: int,
) -> tuple[int, int, int, bool]:
    cell = (x, y)
    read_black = cell in black
    if read_black:
        black.discard(cell)
        heading = (heading + 3) & 3
    else:
        black.add(cell)
        heading = (heading + 1) & 3
    x += DX[heading]
    y += DY[heading]
    return x, y, heading, read_black


def collect_event_rows(
    orbit,
    selected_times: list[int],
    eligible_deep_events: int,
    schedules,
    phase_first_bits: dict[int, int],
    horizons: tuple[int, ...],
    smin: int,
    smax: int,
) -> list[dict[str, object]]:
    selected = set(selected_times)
    event_rank = {t: i for i, t in enumerate(selected_times)}
    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    rows: list[dict[str, object]] = []
    x = y = heading = 0

    for t in range(orbit.onset_dump):
        if t in selected:
            event_cell = (x, y)
            pre_x, pre_y, pre_heading = x, y, heading
            pre_read_black = event_cell in black
            if not pre_read_black:
                raise AssertionError(f"evento deep selezionato ma cella non nera: idx={orbit.index} t={t}")

            pre_by_horizon = {
                horizon: best_compat_metrics(black, x, y, heading, schedules, phase_first_bits, horizon)
                for horizon in horizons
            }
            x, y, heading, read_black = advance_one_step(black, x, y, heading)
            if not read_black:
                raise AssertionError(f"evento deep selezionato ma read_black falso: idx={orbit.index} t={t}")
            post_by_horizon = {
                horizon: best_compat_metrics(black, x, y, heading, schedules, phase_first_bits, horizon)
                for horizon in horizons
            }

            for horizon in horizons:
                pre = pre_by_horizon[horizon]
                post = post_by_horizon[horizon]
                h_pre = int(pre["h_best"])
                h_post = int(post["h_best"])
                phi_pre = float(pre["phi_compat"])
                phi_post = float(post["phi_compat"])
                delta_h = h_post - h_pre
                delta_phi = phi_post - phi_pre
                if delta_h > 0:
                    h_relation = "improve"
                elif delta_h < 0:
                    h_relation = "decline"
                else:
                    h_relation = "tie"
                if delta_phi < 0:
                    phi_relation = "improve"
                elif delta_phi > 0:
                    phi_relation = "decline"
                else:
                    phi_relation = "tie"
                rows.append(
                    {
                        "idx": orbit.index,
                        "shard": orbit.shard,
                        "onset": orbit.onset_dump,
                        "rngstate": orbit.rngstate,
                        "eligible_deep_events": eligible_deep_events,
                        "selected_event_index": event_rank[t],
                        "event_t": t,
                        "post_t": t + 1,
                        "time_frac": t / orbit.onset_dump,
                        "post_is_onset": int(t + 1 == orbit.onset_dump),
                        "horizon": horizon,
                        "convention": CONVENTION,
                        "event_cell_x": event_cell[0],
                        "event_cell_y": event_cell[1],
                        "pre_x": pre_x,
                        "pre_y": pre_y,
                        "pre_heading": pre_heading,
                        "post_x": x,
                        "post_y": y,
                        "post_heading": heading,
                        "pre_observed_turn_bit": pre["observed_turn_bit"],
                        "post_observed_turn_bit": post["observed_turn_bit"],
                        "pre_best_phase": pre["best_phase"],
                        "post_best_phase": post["best_phase"],
                        "best_phase_changed": int(pre["best_phase"] != post["best_phase"]),
                        "pre_h_best": h_pre,
                        "post_h_best": h_post,
                        "delta_h_best": delta_h,
                        "h_relation": h_relation,
                        "pre_phi_compat": phi_pre,
                        "post_phi_compat": phi_post,
                        "delta_phi_compat": delta_phi,
                        "phi_relation": phi_relation,
                        "pre_compatible_clear_phase_count": pre["compatible_clear_phase_count"],
                        "post_compatible_clear_phase_count": post["compatible_clear_phase_count"],
                        "pre_best_bad_kind": pre["best_bad_kind"],
                        "post_best_bad_kind": post["best_bad_kind"],
                        "pre_best_first_bad_offset": pre["best_first_bad_offset"],
                        "post_best_first_bad_offset": post["best_first_bad_offset"],
                        "pre_best_first_bad_l1": pre["best_first_bad_l1"],
                        "post_best_first_bad_l1": post["best_first_bad_l1"],
                        "pre_best_first_bad_linf": pre["best_first_bad_linf"],
                        "post_best_first_bad_linf": post["best_first_bad_linf"],
                        "pre_compatible_median_h": pre["compatible_median_h"],
                        "post_compatible_median_h": post["compatible_median_h"],
                        "pre_missing_black_count": pre["missing_black_count"],
                        "post_missing_black_count": post["missing_black_count"],
                        "pre_frontier_black_collision_count": pre["frontier_black_collision_count"],
                        "post_frontier_black_collision_count": post["frontier_black_collision_count"],
                    }
                )
            continue

        x, y, heading, _read_black = advance_one_step(black, x, y, heading)

    return rows


def summarize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    horizons = sorted({int(row["horizon"]) for row in rows})
    for horizon in horizons:
        subset = [row for row in rows if int(row["horizon"]) == horizon]
        deltas = [int(row["delta_h_best"]) for row in subset]
        phi_deltas = [float(row["delta_phi_compat"]) for row in subset]
        phase_changes = sum(int(row["best_phase_changed"]) for row in subset)
        payload: dict[str, object] = {
            "horizon": horizon,
            "events": len(subset),
            "orbits": len({int(row["idx"]) for row in subset}),
            "improve": sum(1 for delta in deltas if delta > 0),
            "non_improve": sum(1 for delta in deltas if delta <= 0),
            "decline": sum(1 for delta in deltas if delta < 0),
            "tie": sum(1 for delta in deltas if delta == 0),
            "post_clear": sum(1 for row in subset if int(row["post_h_best"]) == horizon + 1),
            "pre_clear": sum(1 for row in subset if int(row["pre_h_best"]) == horizon + 1),
            "phi_improve": sum(1 for delta in phi_deltas if delta < 0),
            "phi_non_improve": sum(1 for delta in phi_deltas if delta >= 0),
            "phi_decline": sum(1 for delta in phi_deltas if delta > 0),
            "best_phase_changed": phase_changes,
            "best_phase_changed_rate": phase_changes / len(subset) if subset else None,
        }
        for prefix, values in (
            ("pre_h_best", [int(row["pre_h_best"]) for row in subset]),
            ("post_h_best", [int(row["post_h_best"]) for row in subset]),
            ("delta_h_best", deltas),
            ("delta_phi_compat", phi_deltas),
        ):
            for key, value in quantiles(values).items():
                payload[f"{prefix}_{key}"] = value
        out.append(payload)
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    parser.add_argument("--limit-orbits", type=int, default=2, help="0 = tutte le orbite del dump")
    parser.add_argument("--max-events-per-orbit", type=int, default=30, help="0 = tutti gli eventi eleggibili")
    parser.add_argument("--max-seconds", type=float, default=60.0)
    parser.add_argument("--horizons", default="1600")
    parser.add_argument("--sample-mode", choices=("even", "first", "last"), default="even")
    parser.add_argument("--include-entry-post", action="store_true")
    parser.add_argument("--min-event-t", type=int, default=0)
    parser.add_argument("--out-prefix", type=Path, default=ALPHA / "compat_event_audit")
    parser.add_argument("--witness-limit", type=int, default=50)
    parser.add_argument("--smin", type=int, default=5)
    parser.add_argument("--smax", type=int, default=25)
    args = parser.parse_args()

    started = time.perf_counter()
    horizons = parse_horizons(args.horizons)
    max_horizon = max(horizons)
    dumps = parse_dumps(args.dumps)
    if args.limit_orbits:
        dumps = dumps[: args.limit_orbits]

    w0_bits = load_w0_bits(DATA / "w0.txt")
    phase_first_bits = {phase: w0_bits[phase] for phase in GATE_PHASES}
    schedules = make_exogenous_schedule(w0_bits, max_horizon + 1)

    all_rows: list[dict[str, object]] = []
    orbit_rows: list[dict[str, object]] = []
    completed = 0
    stopped_by_time = False
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            stopped_by_time = True
            print(f"STOP: max-seconds={args.max_seconds:.1f}; completate={completed}")
            break

        turns, deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps=0
        )
        if len(turns) != orbit.onset_dump:
            raise AssertionError("simulate_orbit con tail_steps=0 deve produrre onset turni")
        compare_bites(sim_bites, orbit.bite_times, orbit)

        selected_times, eligible_count = select_event_times(
            deep,
            args.max_events_per_orbit,
            args.sample_mode,
            args.include_entry_post,
            args.min_event_t,
        )
        rows = collect_event_rows(
            orbit,
            selected_times,
            eligible_count,
            schedules,
            phase_first_bits,
            horizons,
            args.smin,
            args.smax,
        )
        all_rows.extend(rows)
        completed += 1
        orbit_rows.append(
            {
                "idx": orbit.index,
                "shard": orbit.shard,
                "onset": orbit.onset_dump,
                "rngstate": orbit.rngstate,
                "eligible_deep_events": eligible_count,
                "selected_deep_events": len(selected_times),
                "first_selected_t": selected_times[0] if selected_times else "",
                "last_selected_t": selected_times[-1] if selected_times else "",
                "rows": len(rows),
            }
        )
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} "
            f"deep_eligible={eligible_count:6d} selected={len(selected_times):3d} rows={len(rows):4d}"
        )

    if not all_rows:
        print("Nessun evento completato; nessun output.")
        return 1

    summary_rows = summarize_rows(all_rows)
    witnesses = sorted(
        [row for row in all_rows if int(row["delta_h_best"]) <= 0],
        key=lambda row: (int(row["delta_h_best"]), -int(row["pre_h_best"]), int(row["event_t"])),
    )[: args.witness_limit]
    payload = {
        "source": str(args.dumps),
        "convention": CONVENTION,
        "orbits_requested": len(dumps),
        "orbits_completed": completed,
        "stopped_by_time": stopped_by_time,
        "horizons": horizons,
        "sample_mode": args.sample_mode,
        "max_events_per_orbit": args.max_events_per_orbit,
        "min_event_t": args.min_event_t,
        "include_entry_post": args.include_entry_post,
        "elapsed_seconds": time.perf_counter() - started,
        "orbit_summary": orbit_rows,
        "summary": summary_rows,
        "top_witnesses": witnesses[:10],
    }

    out_prefix: Path = args.out_prefix
    events_csv = out_prefix.with_name(out_prefix.name + "_events.csv")
    witnesses_csv = out_prefix.with_name(out_prefix.name + "_witnesses.csv")
    summary_csv = out_prefix.with_name(out_prefix.name + "_summary.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(events_csv, all_rows)
    write_csv(witnesses_csv, witnesses)
    write_csv(summary_csv, summary_rows)
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"summary": summary_rows, "elapsed_seconds": payload["elapsed_seconds"]}, indent=2))
    print(f"\nCSV events: {events_csv}")
    print(f"CSV witnesses: {witnesses_csv}")
    print(f"CSV summary: {summary_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits completed={completed}, elapsed={time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
