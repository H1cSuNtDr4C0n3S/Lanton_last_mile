#!/usr/bin/env python3
"""checklist_vector_model.py - section 64 vector checklist model.

Fast analysis layer on top of section 63 outputs.  It does not simulate new
orbits.  The goal is to identify which slices of the exogenous checklist
vector cover failed gate attempts, and how small a mismatch sub-vector can
remain while preserving the observed OK/KO diagonal on the long-orbit sample.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Iterable

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"


Attempt = dict[str, str]
Cell = dict[str, str]


def as_int(value: str) -> int | None:
    if value == "":
        return None
    return int(value)


def mean(values: Iterable[int | float]) -> float | None:
    vals = list(values)
    if not vals:
        return None
    return float(sum(vals) / len(vals))


def quantiles(values: list[int | float]) -> dict[str, int | float | None]:
    if not values:
        return {"min": None, "q25": None, "median": None, "q75": None, "max": None, "mean": None}
    ordered = sorted(values)
    if len(ordered) >= 4:
        qs = statistics.quantiles(ordered, n=4)
        q25, q75 = qs[0], qs[2]
    else:
        q25, q75 = ordered[0], ordered[-1]
    return {
        "min": ordered[0],
        "q25": q25,
        "median": statistics.median(ordered),
        "q75": q75,
        "max": ordered[-1],
        "mean": mean(ordered),
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def offset_bucket(offset: int) -> str:
    if offset <= 44:
        return "00_44_early"
    if offset <= 77:
        return "45_77_mid_gate"
    if offset <= 97:
        return "78_97_late_body"
    if offset <= 99:
        return "98_99_deep_gate"
    if offset <= 103:
        return "100_103_tail"
    if offset <= 207:
        return "104_207_period2"
    return "208_plus"


def sort_key(value: str) -> tuple[int, str]:
    """Human order for composite keys whose first field may be numeric."""
    first = value.split("|", 1)[0]
    try:
        return (int(first), value)
    except ValueError:
        return (10**9, value)


def group_coverage(
    mismatches: list[Cell],
    attempts: dict[str, Attempt],
    key_fn: Callable[[Cell], str],
) -> list[dict[str, object]]:
    by_key: dict[str, set[str]] = defaultdict(set)
    cells_by_key: Counter[str] = Counter()
    first_bad_by_key: Counter[str] = Counter()
    first_bad_attempts: dict[str, set[str]] = defaultdict(set)
    kind_by_key: dict[str, Counter[str]] = defaultdict(Counter)
    phase_by_key: dict[str, Counter[int]] = defaultdict(Counter)

    for cell in mismatches:
        key = key_fn(cell)
        aid = cell["attempt_id"]
        by_key[key].add(aid)
        cells_by_key[key] += 1
        if cell["is_first_bad"] == "1":
            first_bad_by_key[key] += 1
            first_bad_attempts[key].add(aid)
        bad_kind = cell["bad_kind"] or ("missing_black" if cell["required_black"] == "1" else "frontier_black_collision")
        kind_by_key[key][bad_kind] += 1
        phase_by_key[key][int(cell["phase"])] += 1

    rows: list[dict[str, object]] = []
    for key, aids in by_key.items():
        ok_attempts = sum(1 for aid in aids if attempts[aid]["ok"] == "1")
        fail_attempts = sum(1 for aid in aids if attempts[aid]["ok"] == "0")
        rows.append(
            {
                "key": key,
                "attempts": len(aids),
                "failed_attempts": fail_attempts,
                "ok_attempts": ok_attempts,
                "mismatch_cells": cells_by_key[key],
                "first_bad_attempts": len(first_bad_attempts[key]),
                "first_bad_cells": first_bad_by_key[key],
                "missing_black_cells": kind_by_key[key]["missing_black"],
                "frontier_black_collision_cells": kind_by_key[key]["frontier_black_collision"],
                "top_phase": phase_by_key[key].most_common(1)[0][0],
                "phase_support": len(phase_by_key[key]),
            }
        )
    rows.sort(key=lambda r: (-int(r["failed_attempts"]), -int(r["mismatch_cells"]), sort_key(str(r["key"]))))
    return rows


def greedy_cover(
    mismatches: list[Cell],
    attempts: dict[str, Attempt],
    key_fn: Callable[[Cell], str],
    label: str,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    failed = {aid for aid, row in attempts.items() if row["ok"] == "0"}
    ok = {aid for aid, row in attempts.items() if row["ok"] == "1"}
    by_key: dict[str, set[str]] = defaultdict(set)
    cells_by_key: Counter[str] = Counter()
    for cell in mismatches:
        key = key_fn(cell)
        by_key[key].add(cell["attempt_id"])
        cells_by_key[key] += 1

    uncovered = set(failed)
    selected: list[dict[str, object]] = []
    step = 0
    while uncovered:
        best_key = None
        best_gain: set[str] = set()
        for key, aids in by_key.items():
            gain = aids & uncovered
            if len(gain) > len(best_gain):
                best_key = key
                best_gain = gain
            elif len(gain) == len(best_gain) and best_key is not None:
                if cells_by_key[key] > cells_by_key[best_key]:
                    best_key = key
                    best_gain = gain
        if best_key is None or not best_gain:
            break
        step += 1
        selected.append(
            {
                "basis": label,
                "step": step,
                "key": best_key,
                "new_failures_covered": len(best_gain),
                "cumulative_failures_covered": len(failed) - len(uncovered - best_gain),
                "remaining_failures": len(uncovered - best_gain),
                "mismatch_cells": cells_by_key[best_key],
            }
        )
        uncovered -= best_gain

    covered_failures = len(failed) - len(uncovered)
    selected_keys = {str(row["key"]) for row in selected}
    predicted_ko = set()
    for cell in mismatches:
        if key_fn(cell) in selected_keys:
            predicted_ko.add(cell["attempt_id"])
    false_ko_ok = len(predicted_ko & ok)
    false_ok_failures = len(failed - predicted_ko)
    summary = {
        "basis": label,
        "components_selected": len(selected),
        "failures_covered": covered_failures,
        "failures_total": len(failed),
        "failure_coverage_rate": covered_failures / len(failed) if failed else None,
        "false_ok_failures": false_ok_failures,
        "false_ko_ok": false_ko_ok,
        "diagonal_preserved": false_ok_failures == 0 and false_ko_ok == 0,
    }
    return selected, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempts", type=Path, default=ALPHA / "checklist_vector_geometry_attempts.csv")
    parser.add_argument("--cells", type=Path, default=ALPHA / "checklist_vector_geometry_cells.csv")
    parser.add_argument("--summary", type=Path, default=ALPHA / "checklist_vector_model_summary.json")
    parser.add_argument("--features", type=Path, default=ALPHA / "checklist_vector_model_features.csv")
    parser.add_argument("--cover", type=Path, default=ALPHA / "checklist_vector_model_cover.csv")
    args = parser.parse_args()

    attempt_rows = read_csv(args.attempts)
    cell_rows = read_csv(args.cells)
    attempts = {row["attempt_id"]: row for row in attempt_rows}
    failed = {aid for aid, row in attempts.items() if row["ok"] == "0"}
    ok = {aid for aid, row in attempts.items() if row["ok"] == "1"}
    mismatches = [row for row in cell_rows if row["ok"] == "0"]

    attempts_with_mismatch = {row["attempt_id"] for row in mismatches}
    first_bad = [row for row in mismatches if row["is_first_bad"] == "1"]

    feature_specs: list[tuple[str, Callable[[Cell], str]]] = [
        ("bad_kind", lambda c: c["bad_kind"] or ("missing_black" if c["required_black"] == "1" else "frontier_black_collision")),
        ("offset_bucket", lambda c: offset_bucket(int(c["offset"]))),
        ("offset", lambda c: c["offset"]),
        ("phase", lambda c: c["phase"]),
        ("phase_offset", lambda c: f"{c['phase']}|{c['offset']}"),
        ("phase_offset_kind", lambda c: f"{c['phase']}|{c['offset']}|{c['bad_kind'] or ('missing_black' if c['required_black'] == '1' else 'frontier_black_collision')}"),
        ("component", lambda c: f"{c['phase']}|{c['offset']}|{c['rel_x']}|{c['rel_y']}|{c['required_black']}"),
    ]

    feature_rows: list[dict[str, object]] = []
    for label, key_fn in feature_specs:
        for row in group_coverage(mismatches, attempts, key_fn):
            row = {"basis": label, **row}
            feature_rows.append(row)

    cover_rows: list[dict[str, object]] = []
    cover_summaries: list[dict[str, object]] = []
    for label, key_fn in feature_specs:
        selected, cover_summary = greedy_cover(mismatches, attempts, key_fn, label)
        cover_rows.extend(selected)
        cover_summaries.append(cover_summary)

    mismatch_counts_by_failure = Counter(row["attempt_id"] for row in mismatches)
    first_bad_offsets = Counter(int(row["offset"]) for row in first_bad)
    all_bad_offsets = Counter(int(row["offset"]) for row in mismatches)
    first_bad_buckets = Counter(offset_bucket(int(row["offset"])) for row in first_bad)
    all_bad_buckets = Counter(offset_bucket(int(row["offset"])) for row in mismatches)
    first_bad_kinds = Counter(row["bad_kind"] for row in first_bad)
    all_bad_kinds = Counter(row["bad_kind"] or ("missing_black" if row["required_black"] == "1" else "frontier_black_collision") for row in mismatches)
    within_two_periods = {row["attempt_id"] for row in mismatches if int(row["offset"]) <= 207}
    first_bad_after_two_periods = [row for row in first_bad if int(row["offset"]) > 207]
    basis_universe_counts = {
        label: len({key_fn(row) for row in mismatches})
        for label, key_fn in feature_specs
    }

    # Leave-one-bucket ablation: if this bucket is ignored, how many failures remain detected?
    bucket_aids: dict[str, set[str]] = defaultdict(set)
    for row in mismatches:
        bucket_aids[offset_bucket(int(row["offset"]))].add(row["attempt_id"])
    all_detected = set().union(*bucket_aids.values()) if bucket_aids else set()
    bucket_ablation = []
    for bucket in sorted(bucket_aids):
        detected_without = set().union(*(aids for b, aids in bucket_aids.items() if b != bucket))
        missed = failed - detected_without
        bucket_ablation.append(
            {
                "removed_bucket": bucket,
                "failures_missed": len(missed),
                "failures_still_covered": len(failed - missed),
                "missed_attempt_examples": sorted(missed, key=lambda x: tuple(int(p) for p in x.split(":")))[:10],
            }
        )

    summary = {
        "attempts": len(attempts),
        "ok": len(ok),
        "failures": len(failed),
        "mismatch_cells": len(mismatches),
        "attempts_with_mismatch": len(attempts_with_mismatch),
        "full_vector_diagonal": {
            "failures_without_mismatch": len(failed - attempts_with_mismatch),
            "ok_with_mismatch": len(ok & attempts_with_mismatch),
            "preserved": len(failed - attempts_with_mismatch) == 0 and len(ok & attempts_with_mismatch) == 0,
        },
        "two_period_vector": {
            "failures_covered": len(failed & within_two_periods),
            "failures_total": len(failed),
            "failures_missed": len(failed - within_two_periods),
            "failure_coverage_rate": len(failed & within_two_periods) / len(failed) if failed else None,
            "first_bad_after_two_periods": len(first_bad_after_two_periods),
            "first_bad_after_two_period_examples": [
                {
                    "attempt_id": row["attempt_id"],
                    "phase": int(row["phase"]),
                    "offset": int(row["offset"]),
                    "bad_kind": row["bad_kind"],
                }
                for row in sorted(first_bad_after_two_periods, key=lambda r: int(r["offset"]))[:12]
            ],
        },
        "basis_universe_counts": basis_universe_counts,
        "mismatch_count_per_failed_attempt": quantiles([mismatch_counts_by_failure[aid] for aid in failed]),
        "first_bad_kind_counts": dict(first_bad_kinds),
        "all_bad_kind_counts": dict(all_bad_kinds),
        "first_bad_bucket_counts": dict(first_bad_buckets),
        "all_bad_bucket_counts": dict(all_bad_buckets),
        "top_first_bad_offsets": [{"offset": k, "attempts": v} for k, v in first_bad_offsets.most_common(20)],
        "top_all_bad_offsets": [{"offset": k, "mismatch_cells": v} for k, v in all_bad_offsets.most_common(20)],
        "cover_summaries": cover_summaries,
        "bucket_ablation": bucket_ablation,
        "source_attempts": str(args.attempts),
        "source_cells": str(args.cells),
    }

    write_csv(args.features, feature_rows)
    write_csv(args.cover, cover_rows)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
