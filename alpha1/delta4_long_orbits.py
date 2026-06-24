#!/usr/bin/env python3
"""delta4_long_orbits.py - short reproducible delta_r -> beta probe.

Reads the 24 long-orbit entries in dumps_all.txt, rebuilds each seed from its
rngstate with the same xorshift generator used by alpha1_engine.c, and measures:
  * r=4 deep black reads (black cell outside the live 9x9 memory window);
  * fresh-white bite rates from the existing dumps;
  * sliding-window floors for L = 313, 1040, 10400;
  * simple W0-like lock depth counts, D(t) >= 40 and D(t) >= 80.

No search is performed. The default wall-clock guard is 290 seconds.
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

ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "alpha1"
DATA = ROOT / "data"

RADIUS = 4
WINDOWS = (313, 1040, 10400)
LOCK_THRESHOLDS = (40, 80)
CORE_FRAC = 0.70
DELTA4_AUTO = 2.0 / 313.0
MASK64 = (1 << 64) - 1

DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)  # alpha1_engine.c convention


@dataclass(frozen=True)
class OrbitDump:
    index: int
    shard: int
    onset_header: int
    rngstate: int
    onset_dump: int
    bite_times: tuple[int, ...]


def xs(state: int) -> int:
    state ^= (state << 13) & MASK64
    state ^= state >> 7
    state ^= (state << 17) & MASK64
    return state & MASK64


def build_seed(rngstate: int, smin: int, smax: int) -> tuple[set[tuple[int, int]], int, float]:
    state = xs(rngstate)
    side = smin + int(state % (smax - smin + 1))
    state = xs(state)
    dens = 0.25 + (state % 1000) / 1000.0 * 0.35
    half = side // 2
    black: set[tuple[int, int]] = set()
    for x in range(-half, half + 1):
        for y in range(-half, half + 1):
            state = xs(state)
            if (state % 1000) / 1000.0 < dens:
                black.add((x, y))
    return black, side, dens


def parse_dumps(path: Path) -> list[OrbitDump]:
    out: list[OrbitDump] = []
    with path.open("r", encoding="utf-8") as f:
        lines = iter(f)
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if not (line.startswith("===") and line.endswith("===")):
                raise ValueError(f"header atteso, trovato: {line!r}")
            parts = line.strip("= ").split()
            if len(parts) != 3:
                raise ValueError(f"header malformato: {line!r}")
            shard, onset_header, rngstate = map(int, parts)
            onset_dump, nbites = map(int, next(lines).split())
            bites = []
            for _ in range(nbites):
                bites.append(int(next(lines)))
            if onset_header != onset_dump:
                raise ValueError(
                    f"onset header/dump non coincide per blocco {len(out)}: "
                    f"{onset_header} vs {onset_dump}"
                )
            out.append(
                OrbitDump(
                    index=len(out),
                    shard=shard,
                    onset_header=onset_header,
                    rngstate=rngstate,
                    onset_dump=onset_dump,
                    bite_times=tuple(bites),
                )
            )
    return out


def forget_outside_ring(known: set[tuple[int, int]], x: int, y: int) -> None:
    r1 = RADIUS + 1
    candidates = []
    candidates.extend((x - r1, y + d) for d in range(-r1, r1 + 1))
    candidates.extend((x + r1, y + d) for d in range(-r1, r1 + 1))
    candidates.extend((x + d, y - r1) for d in range(-r1, r1 + 1))
    candidates.extend((x + d, y + r1) for d in range(-r1, r1 + 1))
    for cx, cy in candidates:
        if (cx, cy) in known and max(abs(cx - x), abs(cy - y)) > RADIUS:
            known.discard((cx, cy))


def simulate_orbit(
    rngstate: int,
    onset: int,
    smin: int,
    smax: int,
    tail_steps: int,
) -> tuple[list[int], bytearray, tuple[int, ...], int, float]:
    black, side, dens = build_seed(rngstate, smin, smax)
    visited: set[tuple[int, int]] = set()
    known: set[tuple[int, int]] = set()
    turns: list[int] = []
    deep = bytearray(onset)
    bites: list[int] = []
    x = y = h = 0
    horizon = onset + tail_steps

    for t in range(horizon):
        cell = (x, y)
        is_black = cell in black
        if t < onset:
            if is_black and cell not in known:
                deep[t] = 1
            if (not is_black) and cell not in visited:
                bites.append(t)
        visited.add(cell)

        if is_black:
            black.discard(cell)
            h = (h + 3) & 3
            turns.append(0)  # L
        else:
            black.add(cell)
            h = (h + 1) & 3
            turns.append(1)  # R

        known.add(cell)
        x += DX[h]
        y += DY[h]
        forget_outside_ring(known, x, y)

    if not all(max(abs(cx - x), abs(cy - y)) <= RADIUS for cx, cy in known):
        raise AssertionError("known contiene celle fuori dalla finestra 9x9")
    return turns, deep, tuple(bites), side, dens


def region_count(bits: bytearray | tuple[int, ...] | list[int], a: int, b: int) -> int:
    if isinstance(bits, bytearray):
        return sum(bits[a:b])
    # tuple/list of event times, sorted
    lo = lower_bound(bits, a)
    hi = lower_bound(bits, b)
    return hi - lo


def lower_bound(values: tuple[int, ...] | list[int], needle: int) -> int:
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < needle:
            lo = mid + 1
        else:
            hi = mid
    return lo


def rate_row(bits: bytearray | tuple[int, ...], onset: int, prefix: str) -> dict[str, float | int]:
    split = int(onset * CORE_FRAC)
    total = region_count(bits, 0, onset)
    core = region_count(bits, 0, split)
    tail = region_count(bits, split, onset)
    return {
        f"{prefix}_total": total,
        f"{prefix}_rate": total / onset,
        f"{prefix}_core": core,
        f"{prefix}_core_rate": core / max(split, 1),
        f"{prefix}_tail": tail,
        f"{prefix}_tail_rate": tail / max(onset - split, 1),
    }


def sliding_stats(bits: bytearray, onset: int, L: int) -> dict[str, float | int]:
    if onset < L:
        return {
            "min_count": "",
            "min_start": "",
            "min_rate": "",
            "median_rate": "",
            "mean_rate": "",
        }
    cur = sum(bits[:L])
    counts = [cur]
    min_count = cur
    min_start = 0
    for start in range(1, onset - L + 1):
        cur += bits[start + L - 1] - bits[start - 1]
        counts.append(cur)
        if cur < min_count:
            min_count = cur
            min_start = start
    counts_sorted = sorted(counts)
    n = len(counts_sorted)
    if n & 1:
        med = counts_sorted[n // 2]
    else:
        med = 0.5 * (counts_sorted[n // 2 - 1] + counts_sorted[n // 2])
    return {
        "min_count": min_count,
        "min_start": min_start,
        "min_rate": min_count / L,
        "median_rate": med / L,
        "mean_rate": sum(counts) / (len(counts) * L),
    }


def w0_factor_map(w0_bits: list[int], k: int) -> dict[int, list[int]]:
    factors: dict[int, list[int]] = {}
    doubled = w0_bits * ((k // len(w0_bits)) + 2)
    for phase in range(len(w0_bits)):
        key = 0
        for bit in doubled[phase : phase + k]:
            key = (key << 1) | bit
        factors.setdefault(key, []).append(phase)
    return factors


def lock_depths_over_threshold(
    turns: list[int],
    onset: int,
    w0_bits: list[int],
    threshold: int = 40,
) -> dict[int, int]:
    """Return exact D(t) only for t with D(t) >= threshold."""
    if len(turns) < threshold:
        return {}
    factors = w0_factor_map(w0_bits, threshold)
    mask = (1 << threshold) - 1
    key = 0
    depths: dict[int, int] = {}
    for t, bit in enumerate(turns):
        key = ((key << 1) | bit) & mask
        start = t - threshold + 1
        if start < 0 or start >= onset:
            continue
        phases = factors.get(key)
        if not phases:
            continue
        best = 0
        for phase in phases:
            d = threshold
            while start + d < len(turns) and turns[start + d] == w0_bits[(phase + d) % 104]:
                d += 1
            if d > best:
                best = d
        depths[start] = best
    return depths


def threshold_region_stats(depths: dict[int, int], onset: int, threshold: int, a: int, b: int) -> dict[str, int | float]:
    positions = [t for t, d in depths.items() if a <= t < b and d >= threshold]
    positions.sort()
    runs = 0
    prev = None
    for t in positions:
        if prev is None or t != prev + 1:
            runs += 1
        prev = t
    max_d = max((depths[t] for t in positions), default=0)
    max_start = min((t for t in positions if depths[t] == max_d), default="")
    span = max(b - a, 1)
    return {
        "steps": len(positions),
        "rate": len(positions) / span,
        "runs": runs,
        "maxD": max_d,
        "maxD_start": max_start,
    }


def lock_rows(depths: dict[int, int], onset: int) -> dict[str, int | float | str]:
    split = int(onset * CORE_FRAC)
    out: dict[str, int | float | str] = {}
    for threshold in LOCK_THRESHOLDS:
        for name, a, b in (
            ("all", 0, onset),
            ("core", 0, split),
            ("tail", split, onset),
        ):
            stats = threshold_region_stats(depths, onset, threshold, a, b)
            for key, value in stats.items():
                out[f"D{threshold}_{name}_{key}"] = value
    return out


def compare_bites(sim: tuple[int, ...], dump: tuple[int, ...], orbit: OrbitDump) -> None:
    if sim == dump:
        return
    n = min(len(sim), len(dump))
    first = next((i for i in range(n) if sim[i] != dump[i]), n)
    raise AssertionError(
        f"morso mismatch orbita {orbit.index}: sim={len(sim)} dump={len(dump)}, "
        f"prima differenza indice {first}, sim={sim[first:first+3]}, dump={dump[first:first+3]}"
    )


def load_w0_bits(path: Path) -> list[int]:
    w0 = path.read_text(encoding="utf-8").strip()
    if len(w0) != 104 or any(ch not in "LR" for ch in w0):
        raise ValueError(f"W0 malformato in {path}")
    return [1 if ch == "R" else 0 for ch in w0]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    ap.add_argument("--limit", type=int, default=0, help="analyze only the first N dump blocks")
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "delta4_long_orbits")
    ap.add_argument("--no-locks", action="store_true", help="skip W0-like D(t) statistics")
    args = ap.parse_args()

    started = time.perf_counter()
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    tail_steps = max(208, max(LOCK_THRESHOLDS))

    orbit_rows: list[dict[str, object]] = []
    window_rows: list[dict[str, object]] = []

    print(
        "idx onset deep_rate bite_rate deep_tail/core bite_tail/core "
        "min313 min1040 min10400 D40runs D80runs maxD"
    )
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP: superato max-seconds={args.max_seconds:.1f}; orbite completate={len(orbit_rows)}")
            break
        turns, deep, sim_bites, side, dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)

        onset = orbit.onset_dump
        split = int(onset * CORE_FRAC)
        row: dict[str, object] = {
            "idx": orbit.index,
            "shard": orbit.shard,
            "onset": onset,
            "rngstate": orbit.rngstate,
            "seed_side": side,
            "seed_density": f"{dens:.6f}",
            "delta4_auto": f"{DELTA4_AUTO:.12f}",
        }
        row.update(rate_row(deep, onset, "deep_black"))
        row.update(rate_row(orbit.bite_times, onset, "fresh_bite"))

        for L in WINDOWS:
            ds = sliding_stats(deep, onset, L)
            bs_bits = bytearray(onset)
            for t in orbit.bite_times:
                if t < onset:
                    bs_bits[t] = 1
            bs = sliding_stats(bs_bits, onset, L)
            window_rows.append(
                {
                    "idx": orbit.index,
                    "onset": onset,
                    "kind": "deep_black",
                    "L": L,
                    **ds,
                }
            )
            window_rows.append(
                {
                    "idx": orbit.index,
                    "onset": onset,
                    "kind": "fresh_bite",
                    "L": L,
                    **bs,
                }
            )
            row[f"deep_L{L}_min_count"] = ds["min_count"]
            row[f"deep_L{L}_min_rate"] = ds["min_rate"]
            row[f"deep_L{L}_min_start"] = ds["min_start"]
            row[f"bite_L{L}_min_count"] = bs["min_count"]
            row[f"bite_L{L}_min_rate"] = bs["min_rate"]
            row[f"bite_L{L}_min_start"] = bs["min_start"]

        if args.no_locks:
            depths = {}
        else:
            depths = lock_depths_over_threshold(turns, onset, w0_bits, threshold=40)
            row.update(lock_rows(depths, onset))

        orbit_rows.append(row)
        deep_tail_core = row["deep_black_tail_rate"] / max(row["deep_black_core_rate"], 1e-12)  # type: ignore[operator]
        bite_tail_core = row["fresh_bite_tail_rate"] / max(row["fresh_bite_core_rate"], 1e-12)  # type: ignore[operator]
        d40_runs = row.get("D40_all_runs", "")
        d80_runs = row.get("D80_all_runs", "")
        maxD = row.get("D40_all_maxD", "")
        print(
            f"{orbit.index:2d} {onset:6d} "
            f"{row['deep_black_rate']:.4f} {row['fresh_bite_rate']:.4f} "
            f"{deep_tail_core:5.2f} {bite_tail_core:5.2f} "
            f"{row['deep_L313_min_rate']:.4f} {row['deep_L1040_min_rate']:.4f} "
            f"{row['deep_L10400_min_rate']:.4f} {d40_runs:>4} {d80_runs:>4} {maxD:>4}"
        )

    out_prefix: Path = args.out_prefix
    summary_csv = out_prefix.with_name(out_prefix.name + "_summary.csv")
    windows_csv = out_prefix.with_name(out_prefix.name + "_windows.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")

    if orbit_rows:
        write_csv(summary_csv, orbit_rows, orbit_rows[0].keys())
        write_csv(windows_csv, window_rows, window_rows[0].keys())
        payload = {
            "source": str(args.dumps),
            "orbits_requested": len(dumps),
            "orbits_completed": len(orbit_rows),
            "windows": WINDOWS,
            "core_fraction": CORE_FRAC,
            "delta4_auto": DELTA4_AUTO,
            "lock_thresholds": LOCK_THRESHOLDS,
            "elapsed_seconds": time.perf_counter() - started,
            "rows": orbit_rows,
        }
        summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nCSV summary: {summary_csv}")
        print(f"CSV windows: {windows_csv}")
        print(f"JSON summary: {summary_json}")
    else:
        print("Nessuna orbita completata; nessun output scritto.")
        return 1
    print(f"elapsed {time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
