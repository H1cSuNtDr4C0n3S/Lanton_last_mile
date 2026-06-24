#!/usr/bin/env python3
"""debt_lock_2d.py - two-coordinate lock hazard probe.

Uses the same causal convention as debt_lock_hazard.py:
  predictors in [t-Lpred, t), event lock in [t, t+H).

The output grid bins anchors by both r=4 deep-black rate and fresh-white bite
rate.  This tests whether fresh local activity remains predictive after
separating the persistent deep-memory debt measured in §58-§59.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

from delta4_long_orbits import (  # noqa: E402
    ALPHA,
    DATA,
    LOCK_THRESHOLDS,
    compare_bites,
    load_w0_bits,
    lock_depths_over_threshold,
    parse_dumps,
    simulate_orbit,
)
from debt_lock_hazard import (  # noqa: E402
    DEFAULT_BINS,
    HORIZONS,
    LPREDS,
    BinSpec,
    bite_bits_from_times,
    lock_bits_from_depths,
    make_bin_spec,
    prefix_bits,
)


@dataclass
class GridAgg:
    n: int = 0
    events: int = 0
    sum_deep_rate: float = 0.0
    sum_bite_rate: float = 0.0

    def add(self, deep_rate: float, bite_rate: float, event: bool) -> None:
        self.n += 1
        self.sum_deep_rate += deep_rate
        self.sum_bite_rate += bite_rate
        if event:
            self.events += 1


def update_histograms(
    deep_hists: dict[tuple[int, int], list[int]],
    bite_hists: dict[tuple[int, int], list[int]],
    deep: bytearray,
    bite: bytearray,
    stride: int,
) -> None:
    onset = len(deep)
    pref_deep = prefix_bits(deep)
    pref_bite = prefix_bits(bite)
    for L in LPREDS:
        for H in HORIZONS:
            max_anchor = onset - H
            if max_anchor < L:
                continue
            dh = deep_hists[(L, H)]
            bh = bite_hists[(L, H)]
            for t in range(L, max_anchor + 1, stride):
                dh[pref_deep[t] - pref_deep[t - L]] += 1
                bh[pref_bite[t] - pref_bite[t - L]] += 1


def aggregate_orbit(
    aggs: dict[tuple[int, int, int, int, int], GridAgg],
    deep_specs: dict[tuple[int, int], BinSpec],
    bite_specs: dict[tuple[int, int], BinSpec],
    deep: bytearray,
    bite: bytearray,
    lock_bits: dict[int, bytearray],
    stride: int,
) -> None:
    onset = len(deep)
    pref_deep = prefix_bits(deep)
    pref_bite = prefix_bits(bite)
    pref_lock = {thr: prefix_bits(bits) for thr, bits in lock_bits.items()}

    for L in LPREDS:
        for H in HORIZONS:
            max_anchor = onset - H
            if max_anchor < L:
                continue
            dspec = deep_specs[(L, H)]
            bspec = bite_specs[(L, H)]
            for t in range(L, max_anchor + 1, stride):
                deep_count = pref_deep[t] - pref_deep[t - L]
                bite_count = pref_bite[t] - pref_bite[t - L]
                dbin = dspec.value_to_bin[deep_count]
                bbin = bspec.value_to_bin[bite_count]
                if dbin < 0 or bbin < 0:
                    continue
                deep_rate = deep_count / L
                bite_rate = bite_count / L
                for threshold, lpref in pref_lock.items():
                    event = (lpref[t + H] - lpref[t]) > 0
                    aggs.setdefault((L, H, threshold, dbin, bbin), GridAgg()).add(
                        deep_rate, bite_rate, event
                    )


def grid_rows_from_aggs(
    aggs: dict[tuple[int, int, int, int, int], GridAgg],
    deep_specs: dict[tuple[int, int], BinSpec],
    bite_specs: dict[tuple[int, int], BinSpec],
    nbins: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for L in LPREDS:
        for H in HORIZONS:
            dspec = deep_specs[(L, H)]
            bspec = bite_specs[(L, H)]
            for threshold in LOCK_THRESHOLDS:
                for dbin in range(nbins):
                    for bbin in range(nbins):
                        agg = aggs.get((L, H, threshold, dbin, bbin))
                        if agg is None or agg.n == 0:
                            continue
                        dlow, dhigh = dspec.low_count[dbin], dspec.high_count[dbin]
                        blow, bhigh = bspec.low_count[bbin], bspec.high_count[bbin]
                        rows.append(
                            {
                                "Lpred": L,
                                "H": H,
                                "threshold": threshold,
                                "deep_bin": dbin,
                                "bite_bin": bbin,
                                "deep_count_low": dlow,
                                "deep_count_high": dhigh,
                                "deep_rate_low": "" if dlow is None else dlow / L,
                                "deep_rate_high": "" if dhigh is None else dhigh / L,
                                "bite_count_low": blow,
                                "bite_count_high": bhigh,
                                "bite_rate_low": "" if blow is None else blow / L,
                                "bite_rate_high": "" if bhigh is None else bhigh / L,
                                "n": agg.n,
                                "mean_deep_rate": agg.sum_deep_rate / agg.n,
                                "mean_bite_rate": agg.sum_bite_rate / agg.n,
                                "events": agg.events,
                                "hazard": agg.events / agg.n,
                            }
                        )
    return rows


def summarize_grid(rows: list[dict[str, object]], min_cell_n: int) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    groups: dict[tuple[int, int, int], list[dict[str, object]]] = {}
    for row in rows:
        key = (int(row["Lpred"]), int(row["H"]), int(row["threshold"]))
        groups.setdefault(key, []).append(row)

    for (L, H, threshold), group in sorted(groups.items()):
        cells = [r for r in group if int(r["n"]) >= min_cell_n]
        if not cells:
            cells = group
        best = max(cells, key=lambda r: float(r["hazard"]))
        worst = min(cells, key=lambda r: float(r["hazard"]))

        deep_effects = []
        bite_effects = []
        for bbin in sorted({int(r["bite_bin"]) for r in cells}):
            stripe = sorted((r for r in cells if int(r["bite_bin"]) == bbin), key=lambda r: int(r["deep_bin"]))
            if len(stripe) >= 2:
                lo, hi = stripe[0], stripe[-1]
                weight = int(lo["n"]) + int(hi["n"])
                deep_effects.append((float(hi["hazard"]) - float(lo["hazard"]), weight))
        for dbin in sorted({int(r["deep_bin"]) for r in cells}):
            stripe = sorted((r for r in cells if int(r["deep_bin"]) == dbin), key=lambda r: int(r["bite_bin"]))
            if len(stripe) >= 2:
                lo, hi = stripe[0], stripe[-1]
                weight = int(lo["n"]) + int(hi["n"])
                bite_effects.append((float(hi["hazard"]) - float(lo["hazard"]), weight))

        def weighted_mean(items: list[tuple[float, int]]) -> float | str:
            total = sum(w for _, w in items)
            if total == 0:
                return ""
            return sum(x * w for x, w in items) / total

        out.append(
            {
                "Lpred": L,
                "H": H,
                "threshold": threshold,
                "cells": len(group),
                "cells_used": len(cells),
                "min_cell_n": min_cell_n,
                "best_deep_bin": best["deep_bin"],
                "best_bite_bin": best["bite_bin"],
                "best_mean_deep_rate": best["mean_deep_rate"],
                "best_mean_bite_rate": best["mean_bite_rate"],
                "best_hazard": best["hazard"],
                "worst_deep_bin": worst["deep_bin"],
                "worst_bite_bin": worst["bite_bin"],
                "worst_mean_deep_rate": worst["mean_deep_rate"],
                "worst_mean_bite_rate": worst["mean_bite_rate"],
                "worst_hazard": worst["hazard"],
                "weighted_deep_effect_within_bite": weighted_mean(deep_effects),
                "weighted_bite_effect_within_deep": weighted_mean(bite_effects),
                "deep_effect_min": min((x for x, _ in deep_effects), default=""),
                "deep_effect_max": max((x for x, _ in deep_effects), default=""),
                "bite_effect_min": min((x for x, _ in bite_effects), default=""),
                "bite_effect_max": max((x for x, _ in bite_effects), default=""),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str] | None = None) -> None:
    if not rows:
        return
    fields = list(fieldnames) if fieldnames is not None else list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, object]]) -> None:
    print("L H D best(d,b,h) worst(d,b,h) deep_eff bite_eff")
    for r in rows:
        print(
            f"{int(r['Lpred']):4d} {int(r['H']):4d} {int(r['threshold']):2d} "
            f"({r['best_deep_bin']},{r['best_bite_bin']},{float(r['best_hazard']):.4f}) "
            f"({r['worst_deep_bin']},{r['worst_bite_bin']},{float(r['worst_hazard']):.4f}) "
            f"{float(r['weighted_deep_effect_within_bite']):+.4f} "
            f"{float(r['weighted_bite_effect_within_deep']):+.4f}"
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--bins", type=int, default=DEFAULT_BINS)
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--min-cell-n", type=int, default=1000)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "debt_lock_2d")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    if args.bins < 2:
        raise ValueError("--bins must be >= 2")
    if args.stride < 1:
        raise ValueError("--stride must be >= 1")

    started = time.perf_counter()
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")

    deep_hists = {(L, H): [0] * (L + 1) for L in LPREDS for H in HORIZONS}
    bite_hists = {(L, H): [0] * (L + 1) for L in LPREDS for H in HORIZONS}

    completed_hist = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP pass1: max-seconds={args.max_seconds:.1f}, completate={completed_hist}")
            break
        _turns, deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, 208
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)
        bite = bytearray(orbit.onset_dump)
        for t in orbit.bite_times:
            if t < orbit.onset_dump:
                bite[t] = 1
        update_histograms(deep_hists, bite_hists, deep, bite, args.stride)
        completed_hist += 1

    if completed_hist == 0:
        print("Nessuna orbita completata in pass1; nessun output.")
        return 1

    deep_specs = {key: make_bin_spec(hist, args.bins) for key, hist in deep_hists.items()}
    bite_specs = {key: make_bin_spec(hist, args.bins) for key, hist in bite_hists.items()}
    aggs: dict[tuple[int, int, int, int, int], GridAgg] = {}

    completed_agg = 0
    for orbit in dumps[:completed_hist]:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP pass2: max-seconds={args.max_seconds:.1f}, completate={completed_agg}")
            break
        turns, deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, 208
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)
        bite = bite_bits_from_times(orbit.onset_dump, orbit.bite_times)
        depths = lock_depths_over_threshold(turns, orbit.onset_dump, w0_bits, threshold=40)
        locks = {thr: lock_bits_from_depths(orbit.onset_dump, depths, thr) for thr in LOCK_THRESHOLDS}
        aggregate_orbit(aggs, deep_specs, bite_specs, deep, bite, locks, args.stride)
        completed_agg += 1

    grid_rows = grid_rows_from_aggs(aggs, deep_specs, bite_specs, args.bins)
    summary_rows = summarize_grid(grid_rows, args.min_cell_n)

    out_prefix: Path = args.out_prefix
    grid_csv = out_prefix.with_name(out_prefix.name + "_grid.csv")
    summary_csv = out_prefix.with_name(out_prefix.name + "_summary.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")

    write_csv(grid_csv, grid_rows)
    write_csv(summary_csv, summary_rows)
    payload = {
        "source": str(args.dumps),
        "convention": {
            "predictor_window": "[t-Lpred, t)",
            "event_window": "[t, t+H)",
            "anchor_stride": args.stride,
            "bins": args.bins,
            "min_cell_n": args.min_cell_n,
        },
        "orbits_requested": len(dumps),
        "orbits_hist_pass": completed_hist,
        "orbits_agg_pass": completed_agg,
        "lpreds": LPREDS,
        "horizons": HORIZONS,
        "thresholds": LOCK_THRESHOLDS,
        "elapsed_seconds": time.perf_counter() - started,
        "summary": summary_rows,
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print_summary(summary_rows)
    print(f"\nCSV grid: {grid_csv}")
    print(f"CSV summary: {summary_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits pass1={completed_hist}, pass2={completed_agg}, elapsed={time.perf_counter() - started:.2f}s")
    return 0 if completed_agg else 1


if __name__ == "__main__":
    raise SystemExit(main())
