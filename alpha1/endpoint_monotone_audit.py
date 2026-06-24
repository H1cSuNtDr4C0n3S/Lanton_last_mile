#!/usr/bin/env python3
"""endpoint_monotone_audit.py - section 68 audit over section 67 CSVs.

This script does not resimulate the ant.  It reads the outputs produced by
potential_segment_scanner.py and extracts witness-level evidence for the
endpoint-monotone no-go discussed in section 68.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable


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

DEFAULT_FOCUS = (
    ("gate", 1600, "phi_actual_depth"),
    ("gate", 1600, "phi_actual_mass_104"),
    ("gate", 1600, "phi_actual_mass_208"),
    ("gate", 1600, "phi_best22_depth"),
    ("grid", 1600, "phi_best22_depth"),
    ("grid", 1600, "phi_best22_mass_104"),
    ("grid", 1600, "phi_best22_mass_208"),
    ("grid", 1600, "phi_best_deficit"),
    ("grid", 1600, "phi_top3_deficit"),
    ("grid", 1600, "phi_sum_deficit"),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fnum(value: str) -> float | None:
    if value == "" or value is None:
        return None
    return float(value)


def truth(value: str) -> bool:
    return value in {"1", "True", "true", "yes"}


def quantile_breaks(values: list[float], bins: int = 4) -> list[float]:
    if not values:
        return []
    values = sorted(values)
    breaks: list[float] = []
    for i in range(1, bins):
        idx = int(round(i * (len(values) - 1) / bins))
        breaks.append(values[idx])
    return breaks


def bin_label(value: float, breaks: list[float]) -> str:
    low: float | None = None
    for high in breaks:
        if value <= high:
            return f"{low if low is not None else '-inf'}..{high:g}"
        low = high
    return f"{low:g}..inf"


def binned_summary(rows: list[dict[str, str]], phi: str, field: str) -> list[dict[str, object]]:
    values = [float(r[field]) for r in rows]
    breaks = quantile_breaks(values)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[bin_label(float(row[field]), breaks)].append(row)

    out: list[dict[str, object]] = []
    for label in sorted(grouped, key=lambda item: float(item.split("..")[0]) if not item.startswith("-inf") else -10**100):
        bucket = grouped[label]
        deltas = [float(r[f"delta_{phi}"]) for r in bucket]
        out.append(
            {
                "bin": label,
                "n": len(bucket),
                "violations_nondec": sum(1 for d in deltas if d >= 0.0),
                "violations_strict": sum(1 for d in deltas if d > 0.0),
                "equal": sum(1 for d in deltas if d == 0.0),
                "delta_min": min(deltas),
                "delta_median": sorted(deltas)[len(deltas) // 2],
                "delta_max": max(deltas),
            }
        )
    return out


def phi_anchor_fields(phi: str) -> tuple[str, str]:
    if phi.startswith("phi_actual_"):
        return "actual_h", "actual_first_bad_kind"
    return "best_h", "best_bad_kind"


def parse_anchor_id(anchor_id: str) -> tuple[int, str, str]:
    orbit, family, local = anchor_id.split(":", 2)
    return int(orbit), family, local


def summarize_phi(rows: list[dict[str, str]], phi: str) -> dict[str, object]:
    delta_key = f"delta_{phi}"
    deltas = [float(r[delta_key]) for r in rows if r[delta_key] != ""]
    return {
        "eligible": len(deltas),
        "violations_nondec": sum(1 for d in deltas if d >= 0.0),
        "violations_strict": sum(1 for d in deltas if d > 0.0),
        "equal": sum(1 for d in deltas if d == 0.0),
        "improvements": sum(1 for d in deltas if d < 0.0),
        "delta_min": min(deltas) if deltas else None,
        "delta_median": sorted(deltas)[len(deltas) // 2] if deltas else None,
        "delta_max": max(deltas) if deltas else None,
        "by_deep_black_quantile": binned_summary(rows, phi, "deep_black_count") if deltas else [],
        "by_gap_steps_quantile": binned_summary(rows, phi, "gap_steps") if deltas else [],
    }


def witness_rows(
    rows: list[dict[str, str]],
    anchors: dict[tuple[str, str], dict[str, str]],
    phi: str,
    limit: int,
) -> list[dict[str, object]]:
    prev_field = f"prev_{phi}"
    next_field = f"next_{phi}"
    delta_field = f"delta_{phi}"
    h_field, kind_field = phi_anchor_fields(phi)
    violating = [r for r in rows if r[delta_field] != "" and float(r[delta_field]) >= 0.0]
    violating.sort(key=lambda r: (-int(r["deep_black_count"]), -float(r[delta_field]), r["prev_anchor_id"]))

    out: list[dict[str, object]] = []
    for row in violating[:limit]:
        orbit, family, prev_local = parse_anchor_id(row["prev_anchor_id"])
        _, _, next_local = parse_anchor_id(row["next_anchor_id"])
        horizon = row["horizon"]
        prev_anchor = anchors[(row["prev_anchor_id"], horizon)]
        next_anchor = anchors[(row["next_anchor_id"], horizon)]
        out.append(
            {
                "anchor_family": family,
                "horizon": int(horizon),
                "phi": phi,
                "orbit": orbit,
                "from_anchor": prev_local,
                "to_anchor": next_local,
                "t0": int(row["prev_start"]),
                "t1": int(row["next_start"]),
                "gap_steps": int(row["gap_steps"]),
                "deep_black_count": int(row["deep_black_count"]),
                "fresh_bite_count": int(row["fresh_bite_count"]),
                "next_status": "entry_or_clear" if truth(row["next_any_compatible_clear"]) else "defect",
                "phi_prev": fnum(row[prev_field]),
                "phi_next": fnum(row[next_field]),
                "delta_phi": fnum(row[delta_field]),
                "h_prev": int(prev_anchor[h_field]) if prev_anchor[h_field] else None,
                "h_next": int(next_anchor[h_field]) if next_anchor[h_field] else None,
                "bad_kind_prev": prev_anchor[kind_field],
                "bad_kind_next": next_anchor[kind_field],
            }
        )
    return out


def write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchors", default="alpha1/potential_segment_scanner_anchors.csv")
    parser.add_argument("--segments", default="alpha1/potential_segment_scanner_segments.csv")
    parser.add_argument("--out-prefix", default="alpha1/endpoint_monotone_audit")
    parser.add_argument("--witness-limit", type=int, default=10)
    args = parser.parse_args()

    anchor_rows = read_csv(Path(args.anchors))
    segment_rows_all = read_csv(Path(args.segments))
    anchors = {(r["anchor_id"], r["horizon"]): r for r in anchor_rows}

    summary: dict[str, object] = {
        "source_anchors": args.anchors,
        "source_segments": args.segments,
        "anchor_rows": len(anchor_rows),
        "segment_rows": len(segment_rows_all),
        "focus": [],
    }
    all_witnesses: list[dict[str, object]] = []

    for family, horizon, phi in DEFAULT_FOCUS:
        rows = [
            r
            for r in segment_rows_all
            if r["anchor_family"] == family
            and int(r["horizon"]) == horizon
            and r[f"delta_{phi}"] != ""
            and int(r["deep_black_count"]) > 0
            and not truth(r["has_entry_endpoint"])
        ]
        phi_summary = summarize_phi(rows, phi)
        witnesses = witness_rows(rows, anchors, phi, args.witness_limit)
        summary["focus"].append(
            {
                "anchor_family": family,
                "horizon": horizon,
                "phi": phi,
                **phi_summary,
                "top_witnesses": witnesses,
            }
        )
        all_witnesses.extend(witnesses)

    out_prefix = Path(args.out_prefix)
    json_path = out_prefix.with_name(out_prefix.name + "_summary.json")
    csv_path = out_prefix.with_name(out_prefix.name + "_witnesses.csv")
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(csv_path, all_witnesses)
    print(f"wrote {json_path}")
    print(f"wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
