#!/usr/bin/env python3
"""compat_endpoint_audit.py - section 69 endpoint Phi_compat audit.

This script reads the section 67 CSVs and does not resimulate the ant.  It
recasts the already measured best compatible prefix length, h_best^L, as the
endpoint version of Phi_compat and extracts witnesses where many deep-black
events occur but h_best does not improve between consecutive anchors.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable


FOCUS = (("gate", 1600), ("grid", 1600))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def truth(value: str) -> bool:
    return value in {"1", "True", "true", "yes"}


def parse_anchor_id(anchor_id: str) -> tuple[int, str, str]:
    orbit, family, local = anchor_id.split(":", 2)
    return int(orbit), family, local


def quantile_breaks(values: list[int], bins: int = 4) -> list[int]:
    values = sorted(values)
    out: list[int] = []
    for i in range(1, bins):
        idx = int(round(i * (len(values) - 1) / bins))
        out.append(values[idx])
    return out


def bin_label(value: int, breaks: list[int]) -> str:
    low: int | None = None
    for high in breaks:
        if value <= high:
            return f"{low if low is not None else '-inf'}..{high}"
        low = high
    return f"{low}..inf"


def binned(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    values = [int(r[field]) for r in rows]
    breaks = quantile_breaks(values)
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[bin_label(int(row[field]), breaks)].append(row)
    ordered = sorted(groups, key=lambda label: float(label.split("..")[0]) if not label.startswith("-inf") else -10**100)
    out: list[dict[str, object]] = []
    for label in ordered:
        bucket = groups[label]
        deltas = sorted(int(r["delta_h_best"]) for r in bucket)
        out.append(
            {
                "bin": label,
                "n": len(bucket),
                "non_improve": sum(1 for d in deltas if d <= 0),
                "strict_decline": sum(1 for d in deltas if d < 0),
                "tie": sum(1 for d in deltas if d == 0),
                "improve": sum(1 for d in deltas if d > 0),
                "delta_min": deltas[0],
                "delta_median": deltas[len(deltas) // 2],
                "delta_max": deltas[-1],
            }
        )
    return out


def summarize(rows: list[dict[str, object]], witness_limit: int) -> dict[str, object]:
    deltas = [int(r["delta_h_best"]) for r in rows]
    witnesses = sorted(
        [r for r in rows if int(r["delta_h_best"]) <= 0],
        key=lambda r: (-int(r["deep_black_count"]), int(r["delta_h_best"]), r["prev_anchor_id"]),
    )[:witness_limit]
    return {
        "eligible": len(rows),
        "non_improve": sum(1 for d in deltas if d <= 0),
        "strict_decline": sum(1 for d in deltas if d < 0),
        "tie": sum(1 for d in deltas if d == 0),
        "improve": sum(1 for d in deltas if d > 0),
        "delta_min": min(deltas) if deltas else None,
        "delta_median": sorted(deltas)[len(deltas) // 2] if deltas else None,
        "delta_max": max(deltas) if deltas else None,
        "by_deep_black_quantile": binned(rows, "deep_black_count") if rows else [],
        "by_gap_steps_quantile": binned(rows, "gap_steps") if rows else [],
        "top_witnesses": witnesses,
    }


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
    parser.add_argument("--out-prefix", default="alpha1/compat_endpoint_audit")
    parser.add_argument("--witness-limit", type=int, default=20)
    args = parser.parse_args()

    anchor_rows = read_csv(Path(args.anchors))
    segment_rows = read_csv(Path(args.segments))
    anchors = {(r["anchor_id"], r["horizon"]): r for r in anchor_rows}

    summary: dict[str, object] = {
        "source_anchors": args.anchors,
        "source_segments": args.segments,
        "anchor_rows": len(anchor_rows),
        "segment_rows": len(segment_rows),
        "focus": [],
    }
    all_witnesses: list[dict[str, object]] = []

    for family, horizon in FOCUS:
        rows: list[dict[str, object]] = []
        for segment in segment_rows:
            if segment["anchor_family"] != family or int(segment["horizon"]) != horizon:
                continue
            if int(segment["deep_black_count"]) <= 0 or truth(segment["has_entry_endpoint"]):
                continue
            prev_anchor = anchors[(segment["prev_anchor_id"], segment["horizon"])]
            next_anchor = anchors[(segment["next_anchor_id"], segment["horizon"])]
            h_prev = int(prev_anchor["best_h"])
            h_next = int(next_anchor["best_h"])
            orbit, _family, prev_local = parse_anchor_id(segment["prev_anchor_id"])
            _orbit2, _family2, next_local = parse_anchor_id(segment["next_anchor_id"])
            row = {
                "anchor_family": family,
                "horizon": horizon,
                "orbit": orbit,
                "prev_anchor_id": segment["prev_anchor_id"],
                "next_anchor_id": segment["next_anchor_id"],
                "from_anchor": prev_local,
                "to_anchor": next_local,
                "t0": int(segment["prev_start"]),
                "t1": int(segment["next_start"]),
                "gap_steps": int(segment["gap_steps"]),
                "deep_black_count": int(segment["deep_black_count"]),
                "fresh_bite_count": int(segment["fresh_bite_count"]),
                "h_best_prev": h_prev,
                "h_best_next": h_next,
                "delta_h_best": h_next - h_prev,
                "prev_best_phase": int(prev_anchor["best_phase"]),
                "next_best_phase": int(next_anchor["best_phase"]),
                "prev_best_bad_kind": prev_anchor["best_bad_kind"],
                "next_best_bad_kind": next_anchor["best_bad_kind"],
                "next_any_compatible_clear": int(next_anchor["any_compatible_clear"]),
            }
            rows.append(row)
        focus_summary = summarize(rows, args.witness_limit)
        summary["focus"].append(
            {
                "anchor_family": family,
                "horizon": horizon,
                **focus_summary,
            }
        )
        all_witnesses.extend(focus_summary["top_witnesses"])

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
