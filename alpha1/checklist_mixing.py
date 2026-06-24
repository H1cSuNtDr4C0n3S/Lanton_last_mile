#!/usr/bin/env python3
"""checklist_mixing.py - section 62 checklist hazard/mixing probe.

Reads lock_checklist_probe_rows.csv, deduplicates the D>=80 rows already present
as D>=40 lock attempts, and measures gate-checklist hazard and transition
statistics between consecutive gate attempts.

No simulation is performed; this is a fast analysis layer on top of section 61.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"


def as_int(value: str) -> int | None:
    if value == "":
        return None
    return int(value)


def mean(values: list[int | float]) -> float | None:
    if not values:
        return None
    return float(sum(values) / len(values))


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
        "mean": mean(ordered),
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dedupe_gate_attempts(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Keep one row per (orbit, start, phase, kind), preferring D>=80 over D>=40."""
    best: dict[tuple[int, int, int, str], dict[str, str]] = {}
    for row in rows:
        if row["is_gate"] != "1":
            continue
        key = (int(row["idx"]), int(row["start"]), int(row["phase"]), row["kind"])
        current = best.get(key)
        if current is None or int(row["threshold"]) > int(current["threshold"]):
            best[key] = row

    attempts: list[dict[str, object]] = []
    by_orbit_seen: dict[int, int] = defaultdict(int)
    for row in sorted(best.values(), key=lambda r: (int(r["idx"]), int(r["start"]), int(r["phase"]))):
        idx = int(row["idx"])
        lock_index = by_orbit_seen[idx]
        by_orbit_seen[idx] += 1
        ok = row["kind"] == "entry"
        bad_abs_x = as_int(row["bad_abs_x"])
        bad_abs_y = as_int(row["bad_abs_y"])
        start = int(row["start"])
        attempts.append(
            {
                "idx": idx,
                "lock_index": lock_index,
                "shard": int(row["shard"]),
                "onset": int(row["onset"]),
                "rngstate": int(row["rngstate"]),
                "threshold": int(row["threshold"]),
                "start": start,
                "time_frac": start / int(row["onset"]),
                "kind": row["kind"],
                "ok": int(ok),
                "phase": int(row["phase"]),
                "depth": int(row["depth"]),
                "first_bad_offset": as_int(row["first_bad_offset"]),
                "bad_rel_x": as_int(row["bad_rel_x"]),
                "bad_rel_y": as_int(row["bad_rel_y"]),
                "bad_abs_x": bad_abs_x,
                "bad_abs_y": bad_abs_y,
                "required_black": as_int(row["required_black"]),
                "actual_black": as_int(row["actual_black"]),
                "bad_kind": row["bad_kind"],
                "verdict": row["verdict"],
                "start_mod2": start % 2,
                "start_mod4": start % 4,
                "start_mod8": start % 8,
                "start_mod16": start % 16,
            }
        )
    return attempts


def transition_rows(attempts: list[dict[str, object]]) -> list[dict[str, object]]:
    by_idx: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in attempts:
        by_idx[int(row["idx"])].append(row)

    out: list[dict[str, object]] = []
    for idx, rows in sorted(by_idx.items()):
        rows.sort(key=lambda r: (int(r["start"]), int(r["phase"])))
        for pair_index, (prev, nxt) in enumerate(zip(rows, rows[1:])):
            prev_bad = (prev["bad_abs_x"], prev["bad_abs_y"])
            next_bad = (nxt["bad_abs_x"], nxt["bad_abs_y"])
            both_failed = not int(prev["ok"]) and not int(nxt["ok"])
            if both_failed:
                px, py = int(prev["bad_abs_x"]), int(prev["bad_abs_y"])
                nx, ny = int(nxt["bad_abs_x"]), int(nxt["bad_abs_y"])
                l1: int | str = abs(px - nx) + abs(py - ny)
                same_cell = int(prev_bad == next_bad)
            else:
                l1 = ""
                same_cell = ""
            out.append(
                {
                    "idx": idx,
                    "pair_index": pair_index,
                    "prev_lock_index": prev["lock_index"],
                    "next_lock_index": nxt["lock_index"],
                    "gap": int(nxt["start"]) - int(prev["start"]),
                    "prev_start": prev["start"],
                    "next_start": nxt["start"],
                    "prev_phase": prev["phase"],
                    "next_phase": nxt["phase"],
                    "prev_ok": prev["ok"],
                    "next_ok": nxt["ok"],
                    "prev_bad_kind": prev["bad_kind"],
                    "next_bad_kind": nxt["bad_kind"],
                    "prev_bad_offset": prev["first_bad_offset"],
                    "next_bad_offset": nxt["first_bad_offset"],
                    "same_phase": int(prev["phase"] == nxt["phase"]),
                    "same_bad_kind": "" if int(prev["ok"]) or int(nxt["ok"]) else int(prev["bad_kind"] == nxt["bad_kind"]),
                    "same_critical_cell": same_cell,
                    "critical_l1": l1,
                    "prev_start_mod8": prev["start_mod8"],
                    "next_start_mod8": nxt["start_mod8"],
                    "prev_start_mod16": prev["start_mod16"],
                    "next_start_mod16": nxt["start_mod16"],
                }
            )
    return out


def rows_by_phase(attempts: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in attempts:
        grouped[int(row["phase"])].append(row)
    out = []
    for phase, rows in sorted(grouped.items()):
        ok = sum(int(r["ok"]) for r in rows)
        failures = len(rows) - ok
        offsets = [int(r["first_bad_offset"]) for r in rows if r["first_bad_offset"] is not None]
        missing = sum(1 for r in rows if r["bad_kind"] == "missing_black")
        frontier = sum(1 for r in rows if r["bad_kind"] == "frontier_black_collision")
        out.append(
            {
                "phase": phase,
                "attempts": len(rows),
                "ok": ok,
                "failures": failures,
                "ok_rate": ok / len(rows),
                "missing_black": missing,
                "frontier_black_collision": frontier,
                "median_bad_offset": "" if not offsets else statistics.median(offsets),
            }
        )
    out.sort(key=lambda r: (-int(r["attempts"]), int(r["phase"])))
    return out


def parity_summary(attempts: list[dict[str, object]], modulus: int) -> list[dict[str, object]]:
    rows = []
    for residue in range(modulus):
        bucket = [r for r in attempts if int(r["start"]) % modulus == residue]
        if not bucket:
            continue
        ok = sum(int(r["ok"]) for r in bucket)
        rows.append(
            {
                "modulus": modulus,
                "residue": residue,
                "attempts": len(bucket),
                "ok": ok,
                "ok_rate": ok / len(bucket),
            }
        )
    return rows


def summarize(attempts: list[dict[str, object]], transitions: list[dict[str, object]]) -> dict[str, object]:
    failures = [r for r in attempts if not int(r["ok"])]
    entries = [r for r in attempts if int(r["ok"])]
    by_idx: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in attempts:
        by_idx[int(row["idx"])].append(row)

    fail_streaks = [sum(1 for r in rows if not int(r["ok"])) for rows in by_idx.values()]
    failed_by_kind = Counter(str(r["bad_kind"]) for r in failures)
    bad_offsets = Counter(int(r["first_bad_offset"]) for r in failures if r["first_bad_offset"] is not None)
    phase_counts = Counter(int(r["phase"]) for r in attempts)
    phase_ok = Counter(int(r["phase"]) for r in entries)

    fail_transitions = [r for r in transitions if not int(r["prev_ok"]) and not int(r["next_ok"])]
    l1_values = [int(r["critical_l1"]) for r in fail_transitions if r["critical_l1"] != ""]
    same_consecutive = sum(int(r["same_critical_cell"]) for r in fail_transitions if r["same_critical_cell"] != "")

    any_pairs = 0
    any_reuse = 0
    for rows in by_idx.values():
        coords = [
            (int(r["bad_abs_x"]), int(r["bad_abs_y"]))
            for r in rows
            if not int(r["ok"]) and r["bad_abs_x"] is not None and r["bad_abs_y"] is not None
        ]
        any_pairs += len(coords) * (len(coords) - 1) // 2
        counts = Counter(coords)
        any_reuse += sum(n * (n - 1) // 2 for n in counts.values())

    kind_trans = Counter(
        (
            str(r["prev_bad_kind"]) if r["prev_bad_kind"] else "OK",
            str(r["next_bad_kind"]) if r["next_bad_kind"] else "OK",
        )
        for r in transitions
    )
    prev_kind_counts = Counter(str(r["prev_bad_kind"]) for r in transitions if r["prev_bad_kind"])
    next_by_prev = {}
    for prev_kind in sorted(prev_kind_counts):
        bucket = [r for r in transitions if r["prev_bad_kind"] == prev_kind]
        denom = len(bucket)
        next_by_prev[prev_kind] = {
            "n": denom,
            "next_ok": sum(int(r["next_ok"]) for r in bucket),
            "next_ok_rate": sum(int(r["next_ok"]) for r in bucket) / denom if denom else None,
            "next_missing_rate": sum(1 for r in bucket if r["next_bad_kind"] == "missing_black") / denom if denom else None,
            "next_frontier_rate": sum(1 for r in bucket if r["next_bad_kind"] == "frontier_black_collision") / denom if denom else None,
        }

    parity = {str(m): parity_summary(attempts, m) for m in (2, 4, 8, 16)}
    return {
        "unique_gate_attempts": len(attempts),
        "failed_gate_attempts": len(failures),
        "ok_entries": len(entries),
        "ok_rate": len(entries) / len(attempts) if attempts else None,
        "orbits": len(by_idx),
        "failure_streaks_before_entry": {
            **quantiles(fail_streaks),
            "population_variance": statistics.pvariance(fail_streaks) if len(fail_streaks) > 1 else 0.0,
            "values": fail_streaks,
        },
        "threshold_counts": dict(sorted(Counter(int(r["threshold"]) for r in attempts).items())),
        "bad_kind_counts": dict(sorted(failed_by_kind.items())),
        "top_bad_offsets": bad_offsets.most_common(16),
        "top_phases": [
            {
                "phase": phase,
                "attempts": count,
                "ok": phase_ok[phase],
                "ok_rate": phase_ok[phase] / count,
            }
            for phase, count in phase_counts.most_common(16)
        ],
        "transitions": {
            "total": len(transitions),
            "to_ok": sum(int(r["next_ok"]) for r in transitions),
            "fail_to_fail": len(fail_transitions),
            "kind_transition_counts": {f"{a}->{b}": n for (a, b), n in sorted(kind_trans.items())},
            "next_by_prev_kind": next_by_prev,
        },
        "critical_cell_reuse": {
            "consecutive_failed_pairs": len(fail_transitions),
            "same_consecutive": same_consecutive,
            "same_consecutive_rate": same_consecutive / len(fail_transitions) if fail_transitions else None,
            "within_orbit_failed_pairs": any_pairs,
            "same_within_orbit": any_reuse,
            "same_within_orbit_rate": any_reuse / any_pairs if any_pairs else None,
            "l1": quantiles(l1_values),
        },
        "parity": parity,
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
    reuse = summary["critical_cell_reuse"]  # type: ignore[index]
    streak = summary["failure_streaks_before_entry"]  # type: ignore[index]
    trans = summary["transitions"]  # type: ignore[index]
    print(
        f"attempts={summary['unique_gate_attempts']} ok={summary['ok_entries']} "
        f"fail={summary['failed_gate_attempts']} ok_rate={float(summary['ok_rate']):.4f}"
    )
    print(
        f"failures/orbit median={streak['median']} mean={float(streak['mean']):.2f} "
        f"var={float(streak['population_variance']):.2f} max={streak['max']}"
    )
    print(
        f"transitions={trans['total']} to_ok={trans['to_ok']} "
        f"fail_to_fail={trans['fail_to_fail']}"
    )
    print(
        f"critical reuse consecutive={reuse['same_consecutive']}/{reuse['consecutive_failed_pairs']} "
        f"within_orbit={reuse['same_within_orbit']}/{reuse['within_orbit_failed_pairs']} "
        f"L1 median={reuse['l1']['median']}"
    )
    print(f"bad kinds: {summary['bad_kind_counts']}")
    print(f"top phases: {summary['top_phases'][:8]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows", type=Path, default=ALPHA / "lock_checklist_probe_rows.csv")
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "checklist_mixing")
    args = ap.parse_args()

    raw = read_rows(args.rows)
    attempts = dedupe_gate_attempts(raw)
    transitions = transition_rows(attempts)
    phase_rows = rows_by_phase(attempts)
    summary = summarize(attempts, transitions)
    summary["source"] = str(args.rows)
    summary["dedupe_key"] = "(idx,start,phase,kind), keep highest threshold"

    out_prefix: Path = args.out_prefix
    attempts_csv = out_prefix.with_name(out_prefix.name + "_attempts.csv")
    transitions_csv = out_prefix.with_name(out_prefix.name + "_transitions.csv")
    phase_csv = out_prefix.with_name(out_prefix.name + "_phase.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")

    write_csv(attempts_csv, attempts)
    write_csv(transitions_csv, transitions)
    write_csv(phase_csv, phase_rows)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print_summary(summary)
    print(f"\nCSV attempts: {attempts_csv}")
    print(f"CSV transitions: {transitions_csv}")
    print(f"CSV phase: {phase_csv}")
    print(f"JSON summary: {summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
