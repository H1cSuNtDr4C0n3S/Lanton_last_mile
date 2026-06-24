#!/usr/bin/env python3
"""debt_lock_hazard.py - short probe: deep debt -> future W0-like lock.

Convention:
  anchor t uses a causal past predictor window [t-Lpred, t).
  event is "there exists a W0-like lock with D >= threshold in [t, t+H)".

The script uses the same 24 long-orbit dump blocks as delta4_long_orbits.py,
rebuilds each seed from rngstate, validates fresh-white bite times against
dumps_all.txt, and aggregates hazard by quantile-like bins of predictor rates.

No onset search is performed. No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import defaultdict
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

LPREDS = (313, 1040, 3120)
HORIZONS = (312, 1040)
PREDICTORS = ("deep_black", "fresh_bite")
DEFAULT_BINS = 5


@dataclass
class BinSpec:
    value_to_bin: list[int]
    low_count: list[int | None]
    high_count: list[int | None]
    mass: list[int]


@dataclass
class Agg:
    n: int = 0
    sum_deep_rate: float = 0.0
    sum_bite_rate: float = 0.0
    events: int = 0

    def add(self, deep_rate: float, bite_rate: float, event: bool) -> None:
        self.n += 1
        self.sum_deep_rate += deep_rate
        self.sum_bite_rate += bite_rate
        if event:
            self.events += 1


def prefix_bits(bits: bytearray) -> list[int]:
    pref = [0] * (len(bits) + 1)
    s = 0
    for i, bit in enumerate(bits):
        s += bit
        pref[i + 1] = s
    return pref


def bite_bits_from_times(onset: int, bite_times: tuple[int, ...]) -> bytearray:
    bits = bytearray(onset)
    for t in bite_times:
        if 0 <= t < onset:
            bits[t] = 1
    return bits


def update_histograms(
    hists: dict[tuple[str, int, int], list[int]],
    deep: bytearray,
    bite: bytearray,
    lpreds: Iterable[int],
    horizons: Iterable[int],
    stride: int,
) -> None:
    onset = len(deep)
    pref_deep = prefix_bits(deep)
    pref_bite = prefix_bits(bite)
    prefs = {"deep_black": pref_deep, "fresh_bite": pref_bite}

    for L in lpreds:
        for H in horizons:
            max_anchor = onset - H
            if max_anchor < L:
                continue
            for predictor in PREDICTORS:
                hist = hists[(predictor, L, H)]
                pref = prefs[predictor]
                for t in range(L, max_anchor + 1, stride):
                    cnt = pref[t] - pref[t - L]
                    hist[cnt] += 1


def make_bin_spec(hist: list[int], nbins: int) -> BinSpec:
    total = sum(hist)
    if total <= 0:
        return BinSpec([-1] * len(hist), [None] * nbins, [None] * nbins, [0] * nbins)

    value_to_bin = [-1] * len(hist)
    low: list[int | None] = [None] * nbins
    high: list[int | None] = [None] * nbins
    mass = [0] * nbins
    targets = [total * i / nbins for i in range(1, nbins)]
    bin_idx = 0
    cumulative_before = 0

    for value, count in enumerate(hist):
        if count == 0:
            continue
        while bin_idx < nbins - 1 and cumulative_before >= targets[bin_idx]:
            bin_idx += 1
        value_to_bin[value] = bin_idx
        if low[bin_idx] is None:
            low[bin_idx] = value
        high[bin_idx] = value
        mass[bin_idx] += count
        cumulative_before += count

    return BinSpec(value_to_bin, low, high, mass)


def lock_bits_from_depths(onset: int, depths: dict[int, int], threshold: int) -> bytearray:
    bits = bytearray(onset)
    for t, d in depths.items():
        if t < onset and d >= threshold:
            bits[t] = 1
    return bits


def aggregate_orbit(
    aggs: dict[tuple[str, int, int, int, int], Agg],
    specs: dict[tuple[str, int, int], BinSpec],
    deep: bytearray,
    bite: bytearray,
    lock_bits: dict[int, bytearray],
    lpreds: Iterable[int],
    horizons: Iterable[int],
    stride: int,
) -> None:
    onset = len(deep)
    pref_deep = prefix_bits(deep)
    pref_bite = prefix_bits(bite)
    pref_lock = {thr: prefix_bits(bits) for thr, bits in lock_bits.items()}
    pred_prefs = {"deep_black": pref_deep, "fresh_bite": pref_bite}

    for L in lpreds:
        for H in horizons:
            max_anchor = onset - H
            if max_anchor < L:
                continue
            for t in range(L, max_anchor + 1, stride):
                deep_count = pref_deep[t] - pref_deep[t - L]
                bite_count = pref_bite[t] - pref_bite[t - L]
                deep_rate = deep_count / L
                bite_rate = bite_count / L
                pred_counts = {"deep_black": deep_count, "fresh_bite": bite_count}
                for threshold, lpref in pref_lock.items():
                    event = (lpref[t + H] - lpref[t]) > 0
                    for predictor in PREDICTORS:
                        cnt = pred_counts[predictor]
                        b = specs[(predictor, L, H)].value_to_bin[cnt]
                        if b < 0:
                            continue
                        key = (predictor, L, H, threshold, b)
                        aggs.setdefault(key, Agg()).add(deep_rate, bite_rate, event)


def rows_from_aggs(
    aggs: dict[tuple[str, int, int, int, int], Agg],
    specs: dict[tuple[str, int, int], BinSpec],
    nbins: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for predictor in PREDICTORS:
        for L in LPREDS:
            for H in HORIZONS:
                spec = specs[(predictor, L, H)]
                for threshold in LOCK_THRESHOLDS:
                    for b in range(nbins):
                        agg = aggs.get((predictor, L, H, threshold, b), Agg())
                        if agg.n == 0:
                            continue
                        low = spec.low_count[b]
                        high = spec.high_count[b]
                        rows.append(
                            {
                                "predictor": predictor,
                                "Lpred": L,
                                "H": H,
                                "threshold": threshold,
                                "bin": b,
                                "bin_count_low": low,
                                "bin_count_high": high,
                                "bin_rate_low": "" if low is None else low / L,
                                "bin_rate_high": "" if high is None else high / L,
                                "n": agg.n,
                                "mean_deep_rate": agg.sum_deep_rate / agg.n,
                                "mean_bite_rate": agg.sum_bite_rate / agg.n,
                                "events": agg.events,
                                "hazard": agg.events / agg.n,
                            }
                        )
    return rows


def summary_from_bin_rows(bin_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, int, int, int], list[dict[str, object]]] = defaultdict(list)
    for row in bin_rows:
        grouped[(row["predictor"], row["Lpred"], row["H"], row["threshold"])].append(row)  # type: ignore[index]

    out: list[dict[str, object]] = []
    for (predictor, L, H, threshold), rows in sorted(grouped.items()):
        rows.sort(key=lambda r: int(r["bin"]))
        bottom = rows[0]
        top = rows[-1]
        bh = float(bottom["hazard"])
        th = float(top["hazard"])
        ratio: float | str = "inf" if bh == 0.0 and th > 0 else (th / bh if bh > 0 else "")
        out.append(
            {
                "predictor": predictor,
                "Lpred": L,
                "H": H,
                "threshold": threshold,
                "bins": len(rows),
                "n_total": sum(int(r["n"]) for r in rows),
                "bottom_bin": bottom["bin"],
                "top_bin": top["bin"],
                "bottom_mean_deep_rate": bottom["mean_deep_rate"],
                "top_mean_deep_rate": top["mean_deep_rate"],
                "bottom_mean_bite_rate": bottom["mean_bite_rate"],
                "top_mean_bite_rate": top["mean_bite_rate"],
                "bottom_hazard": bh,
                "top_hazard": th,
                "hazard_ratio_top_bottom": ratio,
                "hazard_delta_top_minus_bottom": th - bh,
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


def print_summary(summary_rows: list[dict[str, object]]) -> None:
    print("pred L H D bottom_h top_h ratio delta bottom_deep top_deep bottom_bite top_bite")
    for r in summary_rows:
        ratio = r["hazard_ratio_top_bottom"]
        ratio_s = "inf" if ratio == "inf" else ("" if ratio == "" else f"{float(ratio):.2f}")
        print(
            f"{r['predictor'][:5]:>5} {int(r['Lpred']):4d} {int(r['H']):4d} "
            f"{int(r['threshold']):2d} "
            f"{float(r['bottom_hazard']):.4f} {float(r['top_hazard']):.4f} "
            f"{ratio_s:>6} {float(r['hazard_delta_top_minus_bottom']):+.4f} "
            f"{float(r['bottom_mean_deep_rate']):.4f} {float(r['top_mean_deep_rate']):.4f} "
            f"{float(r['bottom_mean_bite_rate']):.4f} {float(r['top_mean_bite_rate']):.4f}"
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--bins", type=int, default=DEFAULT_BINS)
    ap.add_argument("--stride", type=int, default=4, help="sample every N anchors; use 1 for all anchors")
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "debt_lock_hazard")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    started = time.perf_counter()
    if args.bins < 2:
        raise ValueError("--bins must be >= 2")
    if args.stride < 1:
        raise ValueError("--stride must be >= 1")

    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    tail_steps = 208

    hists: dict[tuple[str, int, int], list[int]] = {}
    for predictor in PREDICTORS:
        for L in LPREDS:
            for H in HORIZONS:
                hists[(predictor, L, H)] = [0] * (L + 1)

    completed_hist = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP pass1: max-seconds={args.max_seconds:.1f}, completate={completed_hist}")
            break
        _turns, deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)
        bite = bite_bits_from_times(orbit.onset_dump, orbit.bite_times)
        update_histograms(hists, deep, bite, LPREDS, HORIZONS, args.stride)
        completed_hist += 1

    if completed_hist == 0:
        print("Nessuna orbita completata in pass1; nessun output.")
        return 1

    specs = {key: make_bin_spec(hist, args.bins) for key, hist in hists.items()}
    aggs: dict[tuple[str, int, int, int, int], Agg] = {}

    completed_agg = 0
    for orbit in dumps[:completed_hist]:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP pass2: max-seconds={args.max_seconds:.1f}, completate={completed_agg}")
            break
        turns, deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)
        bite = bite_bits_from_times(orbit.onset_dump, orbit.bite_times)
        depths = lock_depths_over_threshold(turns, orbit.onset_dump, w0_bits, threshold=40)
        locks = {
            threshold: lock_bits_from_depths(orbit.onset_dump, depths, threshold)
            for threshold in LOCK_THRESHOLDS
        }
        aggregate_orbit(aggs, specs, deep, bite, locks, LPREDS, HORIZONS, args.stride)
        completed_agg += 1

    bin_rows = rows_from_aggs(aggs, specs, args.bins)
    summary_rows = summary_from_bin_rows(bin_rows)

    out_prefix: Path = args.out_prefix
    summary_csv = out_prefix.with_name(out_prefix.name + "_summary.csv")
    bins_csv = out_prefix.with_name(out_prefix.name + "_bins.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")

    write_csv(summary_csv, summary_rows)
    write_csv(bins_csv, bin_rows)
    payload = {
        "source": str(args.dumps),
        "convention": {
            "predictor_window": "[t-Lpred, t)",
            "event_window": "[t, t+H)",
            "anchor_stride": args.stride,
        },
        "orbits_requested": len(dumps),
        "orbits_hist_pass": completed_hist,
        "orbits_agg_pass": completed_agg,
        "lpreds": LPREDS,
        "horizons": HORIZONS,
        "thresholds": LOCK_THRESHOLDS,
        "bins_requested": args.bins,
        "elapsed_seconds": time.perf_counter() - started,
        "summary": summary_rows,
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print_summary(summary_rows)
    print(f"\nCSV summary: {summary_csv}")
    print(f"CSV bins: {bins_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits pass1={completed_hist}, pass2={completed_agg}, elapsed={time.perf_counter() - started:.2f}s")
    return 0 if completed_agg else 1


if __name__ == "__main__":
    raise SystemExit(main())
