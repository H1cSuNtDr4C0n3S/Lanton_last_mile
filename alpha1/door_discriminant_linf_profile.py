#!/usr/bin/env python3
"""door_discriminant_linf_profile.py - section 72 radius-vs-depth profile.

Profile the first T3' discriminating read from door_defect_profile_rows.csv:
for actual pre-onset lock failures, measure how the relative L-infinity
radius of the first bad cell varies with lock depth.

This is a guardrail before building a recurrent-debt graph.  It reports both
raw relative coordinates and the exact W0 co-moving coordinates obtained by
subtracting full-period phase drift.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


DEFAULT_BINS = "40:77,78:103,104:207,208:511,512:1023,1024:"
PERIOD = 104
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)

ROW_FIELDS = (
    "attempt_id",
    "idx",
    "shard",
    "onset",
    "rngstate",
    "threshold",
    "start",
    "time_frac",
    "actual_phase",
    "depth",
    "first_bad_offset",
    "depth_minus_offset",
    "eval_phase",
    "bad_kind",
    "rel_x",
    "rel_y",
    "l1",
    "linf",
    "period_index",
    "offset_mod_period",
    "phase_drift_x",
    "phase_drift_y",
    "comoving_rel_x",
    "comoving_rel_y",
    "comoving_l1",
    "comoving_linf",
    "linear_linf_residual",
    "required_black",
    "actual_black",
    "origin_x",
    "origin_y",
    "heading",
    "abs_x",
    "abs_y",
    "depth_bin",
    "physical_key",
    "is_physical_first",
)

BIN_FIELDS = (
    "sample",
    "frame",
    "depth_bin",
    "count",
    "depth_min",
    "depth_median",
    "depth_max",
    "linf_min",
    "linf_q25",
    "linf_median",
    "linf_q75",
    "linf_max",
    "linf_mean",
    "l1_median",
    "l1_max",
    "offset_median",
    "offset_max",
    "missing_black",
    "frontier_black_collision",
    "other_bad_kind",
)

DEPTH_FIELDS = (
    "sample",
    "frame",
    "depth",
    "count",
    "linf_min",
    "linf_q25",
    "linf_median",
    "linf_q75",
    "linf_max",
    "linf_mean",
    "l1_max",
    "missing_black",
    "frontier_black_collision",
    "other_bad_kind",
)


def load_w0_bits(path: Path) -> list[int]:
    text = path.read_text(encoding="utf-8").strip()
    bits: list[int] = []
    for ch in text:
        if ch == "R":
            bits.append(1)
        elif ch == "L":
            bits.append(0)
        elif ch in "01":
            bits.append(int(ch))
        elif ch.isspace():
            continue
        else:
            raise ValueError(f"bad W0 character {ch!r} in {path}")
    if len(bits) != PERIOD:
        raise ValueError(f"W0 length must be {PERIOD}, got {len(bits)}")
    return bits


def phase_drifts(w0_bits: list[int]) -> dict[int, tuple[int, int]]:
    out: dict[int, tuple[int, int]] = {}
    for phase in range(PERIOD):
        x = y = h = 0
        for offset in range(PERIOD):
            bit = w0_bits[(phase + offset) % PERIOD]
            if bit:
                h = (h + 1) & 3
            else:
                h = (h + 3) & 3
            x += DX[h]
            y += DY[h]
        if h != 0:
            raise ValueError(f"W0 phase {phase} has nonzero net heading {h}")
        out[phase] = (x, y)
    return out


def int_field(row: dict[str, str], name: str) -> int:
    value = row.get(name, "")
    if value == "":
        raise ValueError(f"missing integer field {name!r} in row {row.get('attempt_id', '<unknown>')}")
    return int(value)


def parse_bins(text: str) -> list[tuple[str, int | None, int | None]]:
    bins: list[tuple[str, int | None, int | None]] = []
    for part in text.split(","):
        item = part.strip()
        if not item:
            continue
        if ":" not in item:
            lo = hi = int(item)
        else:
            left, right = item.split(":", 1)
            lo = int(left) if left.strip() else None
            hi = int(right) if right.strip() else None
        if lo is None and hi is None:
            raise ValueError("unbounded bin is not meaningful")
        if lo is not None and hi is not None and lo > hi:
            raise ValueError(f"invalid decreasing bin {item!r}")
        label = f"{'' if lo is None else lo}-{'' if hi is None else hi}"
        bins.append((label, lo, hi))
    if not bins:
        raise ValueError("--depth-bins produced no bins")
    return bins


def bin_label(depth: int, bins: list[tuple[str, int | None, int | None]]) -> str:
    for label, lo, hi in bins:
        if (lo is None or depth >= lo) and (hi is None or depth <= hi):
            return label
    return "out_of_bins"


def percentile(values: Iterable[int | float], p: float) -> float | None:
    vals = sorted(float(v) for v in values)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * p
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return vals[lo]
    frac = pos - lo
    return vals[lo] * (1.0 - frac) + vals[hi] * frac


def qstats(values: Iterable[int | float]) -> dict[str, float | None]:
    vals = list(values)
    if not vals:
        return {"min": None, "q25": None, "median": None, "q75": None, "max": None, "mean": None}
    return {
        "min": float(min(vals)),
        "q25": percentile(vals, 0.25),
        "median": float(statistics.median(vals)),
        "q75": percentile(vals, 0.75),
        "max": float(max(vals)),
        "mean": float(sum(vals) / len(vals)),
    }


def pearson(xs: list[int], ys: list[int]) -> float | None:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def ranks(values: list[int]) -> list[float]:
    order = sorted(enumerate(values), key=lambda item: item[1])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and order[j][1] == order[i][1]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[order[k][0]] = rank
        i = j
    return out


def spearman(xs: list[int], ys: list[int]) -> float | None:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    return pearson(ranks(xs), ranks(ys))  # type: ignore[arg-type]


def physical_key(row: dict[str, object]) -> str:
    parts = (
        row["idx"],
        row["start"],
        row["actual_phase"],
        row["origin_x"],
        row["origin_y"],
        row["heading"],
        row["first_bad_offset"],
        row["rel_x"],
        row["rel_y"],
        row["bad_kind"],
        row["required_black"],
        row["actual_black"],
    )
    return ":".join(str(part) for part in parts)


def select_rows(
    path: Path,
    horizon: int,
    bins: list[tuple[str, int | None, int | None]],
    drifts: dict[int, tuple[int, int]],
) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    seen_physical: set[str] = set()
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for src in reader:
            if src.get("kind") != "pre_onset_lock":
                continue
            if src.get("is_actual_phase") != "1":
                continue
            if src.get("clear") != "0":
                continue
            if int_field(src, "horizon") != horizon:
                continue
            depth = int_field(src, "depth")
            offset = int_field(src, "first_bad_offset")
            phase = int_field(src, "eval_phase")
            rel_x = int_field(src, "rel_x")
            rel_y = int_field(src, "rel_y")
            period_index = offset // PERIOD
            offset_mod_period = offset % PERIOD
            drift_x, drift_y = drifts[phase]
            comoving_rel_x = rel_x - period_index * drift_x
            comoving_rel_y = rel_y - period_index * drift_y
            row: dict[str, object] = {
                "attempt_id": src["attempt_id"],
                "idx": int_field(src, "idx"),
                "shard": int_field(src, "shard"),
                "onset": int_field(src, "onset"),
                "rngstate": src["rngstate"],
                "threshold": int_field(src, "threshold"),
                "start": int_field(src, "start"),
                "time_frac": float(src["time_frac"]),
                "actual_phase": int_field(src, "actual_phase"),
                "depth": depth,
                "first_bad_offset": offset,
                "depth_minus_offset": depth - offset,
                "eval_phase": phase,
                "bad_kind": src["bad_kind"],
                "rel_x": rel_x,
                "rel_y": rel_y,
                "l1": int_field(src, "l1"),
                "linf": int_field(src, "linf"),
                "period_index": period_index,
                "offset_mod_period": offset_mod_period,
                "phase_drift_x": drift_x,
                "phase_drift_y": drift_y,
                "comoving_rel_x": comoving_rel_x,
                "comoving_rel_y": comoving_rel_y,
                "comoving_l1": abs(comoving_rel_x) + abs(comoving_rel_y),
                "comoving_linf": max(abs(comoving_rel_x), abs(comoving_rel_y)),
                "linear_linf_residual": int_field(src, "linf") - (offset * 2.0 / PERIOD),
                "required_black": int_field(src, "required_black"),
                "actual_black": int_field(src, "actual_black"),
                "origin_x": int_field(src, "origin_x"),
                "origin_y": int_field(src, "origin_y"),
                "heading": int_field(src, "heading"),
                "abs_x": int_field(src, "abs_x"),
                "abs_y": int_field(src, "abs_y"),
                "depth_bin": bin_label(depth, bins),
            }
            key = physical_key(row)
            row["physical_key"] = key
            row["is_physical_first"] = int(key not in seen_physical)
            seen_physical.add(key)
            selected.append(row)
    return selected


def write_csv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def bad_kind_counts(rows: list[dict[str, object]]) -> dict[str, int]:
    counts = Counter(str(row["bad_kind"]) for row in rows)
    return {
        "missing_black": counts.get("missing_black", 0),
        "frontier_black_collision": counts.get("frontier_black_collision", 0),
        "other_bad_kind": sum(v for k, v in counts.items() if k not in {"missing_black", "frontier_black_collision"}),
    }


def metric_names(frame: str) -> tuple[str, str]:
    if frame == "raw":
        return "linf", "l1"
    if frame == "comoving":
        return "comoving_linf", "comoving_l1"
    raise ValueError(f"unknown frame {frame!r}")


def bin_rows(
    sample_name: str,
    frame: str,
    rows: list[dict[str, object]],
    ordered_labels: list[str],
) -> list[dict[str, object]]:
    linf_name, l1_name = metric_names(frame)
    by_bin: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_bin[str(row["depth_bin"])].append(row)

    out: list[dict[str, object]] = []
    for label in ordered_labels:
        bucket = by_bin.get(label, [])
        depths = [int(row["depth"]) for row in bucket]
        linfs = [int(row[linf_name]) for row in bucket]
        l1s = [int(row[l1_name]) for row in bucket]
        offsets = [int(row["first_bad_offset"]) for row in bucket]
        linf_stats = qstats(linfs)
        counts = bad_kind_counts(bucket)
        out.append(
            {
                "sample": sample_name,
                "frame": frame,
                "depth_bin": label,
                "count": len(bucket),
                "depth_min": min(depths) if depths else "",
                "depth_median": statistics.median(depths) if depths else "",
                "depth_max": max(depths) if depths else "",
                "linf_min": linf_stats["min"],
                "linf_q25": linf_stats["q25"],
                "linf_median": linf_stats["median"],
                "linf_q75": linf_stats["q75"],
                "linf_max": linf_stats["max"],
                "linf_mean": linf_stats["mean"],
                "l1_median": statistics.median(l1s) if l1s else "",
                "l1_max": max(l1s) if l1s else "",
                "offset_median": statistics.median(offsets) if offsets else "",
                "offset_max": max(offsets) if offsets else "",
                **counts,
            }
        )
    return out


def depth_rows(sample_name: str, frame: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    linf_name, l1_name = metric_names(frame)
    by_depth: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_depth[int(row["depth"])].append(row)

    out: list[dict[str, object]] = []
    for depth in sorted(by_depth):
        bucket = by_depth[depth]
        linfs = [int(row[linf_name]) for row in bucket]
        l1s = [int(row[l1_name]) for row in bucket]
        linf_stats = qstats(linfs)
        counts = bad_kind_counts(bucket)
        out.append(
            {
                "sample": sample_name,
                "frame": frame,
                "depth": depth,
                "count": len(bucket),
                "linf_min": linf_stats["min"],
                "linf_q25": linf_stats["q25"],
                "linf_median": linf_stats["median"],
                "linf_q75": linf_stats["q75"],
                "linf_max": linf_stats["max"],
                "linf_mean": linf_stats["mean"],
                "l1_max": max(l1s),
                **counts,
            }
        )
    return out


def summarize_sample(rows: list[dict[str, object]], frame: str) -> dict[str, object]:
    linf_name, l1_name = metric_names(frame)
    depths = [int(row["depth"]) for row in rows]
    linfs = [int(row[linf_name]) for row in rows]
    l1s = [int(row[l1_name]) for row in rows]
    offsets = [int(row["first_bad_offset"]) for row in rows]
    max_linf_rows = sorted(
        [row for row in rows if int(row[linf_name]) == max(linfs)] if linfs else [],
        key=lambda row: (int(row["depth"]), int(row["start"]), str(row["attempt_id"])),
    )
    tail_rows = sorted(rows, key=lambda row: (int(row["depth"]), int(row[linf_name])), reverse=True)[:12]
    return {
        "frame": frame,
        "count": len(rows),
        "depth": qstats(depths),
        "linf": qstats(linfs),
        "l1": qstats(l1s),
        "first_bad_offset": qstats(offsets),
        "bad_kind_counts": bad_kind_counts(rows),
        "depth_minus_offset_counts": dict(Counter(int(row["depth_minus_offset"]) for row in rows)),
        "pearson_depth_linf": pearson(depths, linfs),
        "spearman_depth_linf": spearman(depths, linfs),
        "max_linf_rows": max_linf_rows[:12],
        "deepest_rows": tail_rows,
    }


def make_summary(
    args: argparse.Namespace,
    bins: list[tuple[str, int | None, int | None]],
    rows: list[dict[str, object]],
    unique_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "input": str(args.input),
        "horizon": args.horizon,
        "w0": str(args.w0),
        "period": PERIOD,
        "filter": {
            "kind": "pre_onset_lock",
            "is_actual_phase": 1,
            "clear": 0,
            "horizon": args.horizon,
        },
        "depth_bins": [{"label": label, "lo": lo, "hi": hi} for label, lo, hi in bins],
        "attempt_rows": {
            "raw": summarize_sample(rows, "raw"),
            "comoving": summarize_sample(rows, "comoving"),
        },
        "physical_unique_rows": {
            "raw": summarize_sample(unique_rows, "raw"),
            "comoving": summarize_sample(unique_rows, "comoving"),
        },
        "physical_duplicate_rows": len(rows) - len(unique_rows),
        "interpretation": (
            "Compare raw against exact W0 co-moving coordinates before deciding whether "
            "finite recurrent debt classes survive."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("alpha1/door_defect_profile_rows.csv"))
    parser.add_argument("--w0", type=Path, default=Path("data/w0.txt"))
    parser.add_argument("--horizon", type=int, default=1600)
    parser.add_argument("--depth-bins", default=DEFAULT_BINS)
    parser.add_argument("--out-prefix", type=Path, default=Path("alpha1/door_discriminant_linf_profile"))
    args = parser.parse_args()

    bins = parse_bins(args.depth_bins)
    labels = [label for label, _lo, _hi in bins] + ["out_of_bins"]
    drifts = phase_drifts(load_w0_bits(args.w0))
    rows = select_rows(args.input, args.horizon, bins, drifts)
    unique_rows = [row for row in rows if int(row["is_physical_first"])]

    out_prefix: Path = args.out_prefix
    write_csv(out_prefix.with_name(out_prefix.name + "_rows.csv"), rows, ROW_FIELDS)
    write_csv(out_prefix.with_name(out_prefix.name + "_unique_rows.csv"), unique_rows, ROW_FIELDS)
    write_csv(
        out_prefix.with_name(out_prefix.name + "_bins.csv"),
        bin_rows("attempts", "raw", rows, labels)
        + bin_rows("attempts", "comoving", rows, labels)
        + bin_rows("physical_unique", "raw", unique_rows, labels)
        + bin_rows("physical_unique", "comoving", unique_rows, labels),
        BIN_FIELDS,
    )
    write_csv(
        out_prefix.with_name(out_prefix.name + "_depths.csv"),
        depth_rows("attempts", "raw", rows)
        + depth_rows("attempts", "comoving", rows)
        + depth_rows("physical_unique", "raw", unique_rows)
        + depth_rows("physical_unique", "comoving", unique_rows),
        DEPTH_FIELDS,
    )

    summary = make_summary(args, bins, rows, unique_rows)
    with out_prefix.with_name(out_prefix.name + "_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print(
        "door discriminant profile: "
        f"attempts={len(rows)} physical_unique={len(unique_rows)} "
        f"raw_max_linf={summary['attempt_rows']['raw']['linf']['max']} "
        f"comoving_max_linf={summary['attempt_rows']['comoving']['linf']['max']} "
        f"max_depth={summary['attempt_rows']['raw']['depth']['max']}"
    )


if __name__ == "__main__":
    main()
