#!/usr/bin/env python3
"""lock_checklist_probe.py - §61 lock -> T3' checklist probe.

For the 24 long alpha1 orbits, extract per-alignment left-maximal W0-like
locks and test the T3' read-only checklist directly from the state at the lock.

The checklist is reconstructed from W0: for a candidate phase k, every first
visit of the would-be highway segment is exogenous and must already have the
color required for turn W0[k+offset].  A bad exogenous read should occur exactly
at the observed death offset of a gate lock.  True onsets are evaluated as
positive controls.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
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
    parse_dumps,
    simulate_orbit,
    w0_factor_map,
)


R_MUTE: dict[int, int] = {
    1: 19,
    2: 7,
    3: 7,
    4: 3,
    5: 3,
    6: 75,
    7: 27,
    8: 27,
    9: 91,
    10: 11,
    11: 7,
    12: 7,
    13: 3,
    14: 3,
    15: 11,
    17: 7,
    18: 7,
    19: 3,
    20: 3,
    22: 79,
    23: 79,
    27: 3,
    28: 3,
    29: 87,
    32: 7,
    33: 3,
    34: 3,
    35: 7,
    36: 67,
    37: 3,
    38: 3,
    39: 67,
    40: 75,
    41: 63,
    42: 63,
    43: 39,
    44: 7,
    45: 3,
    46: 3,
    47: 7,
    48: 59,
    49: 3,
    50: 3,
    51: 27,
    52: 27,
    53: 55,
    54: 11,
    55: 3,
    56: 3,
    57: 91,
    58: 79,
    59: 7,
    60: 3,
    61: 3,
    62: 7,
    63: 91,
    64: 3,
    65: 3,
    66: 43,
    67: 43,
    68: 79,
    69: 115,
    70: 3,
    71: 3,
    73: 107,
    74: 107,
    75: 15,
    76: 11,
    77: 11,
    78: 7,
    79: 7,
    80: 3,
    81: 3,
    82: 15,
    84: 11,
    85: 11,
    86: 7,
    87: 7,
    88: 3,
    89: 3,
    95: 107,
    96: 107,
}
GATE_PHASES = tuple(k for k in range(104) if k not in R_MUTE)


@dataclass(frozen=True)
class Lock:
    orbit_index: int
    threshold: int
    start: int
    phase: int
    depth: int
    is_gate: bool


@dataclass(frozen=True)
class ExogenousRead:
    offset: int
    rel_x: int
    rel_y: int
    required_black: bool


@dataclass
class EvalResult:
    first_bad_offset: int | None
    first_bad_rel: tuple[int, int] | None
    first_bad_abs: tuple[int, int] | None
    required_black: bool | None
    actual_black: bool | None
    exogenous_reads_checked: int


def rotate_clockwise(x: int, y: int, h: int) -> tuple[int, int]:
    h &= 3
    if h == 0:
        return x, y
    if h == 1:
        return -y, x
    if h == 2:
        return -x, -y
    return y, -x


def rel_to_abs(origin_x: int, origin_y: int, heading: int, rel_x: int, rel_y: int) -> tuple[int, int]:
    rx, ry = rotate_clockwise(rel_x, rel_y, heading)
    return origin_x + rx, origin_y + ry


def make_exogenous_schedule(w0_bits: list[int], max_offset: int) -> dict[int, list[ExogenousRead]]:
    schedules: dict[int, list[ExogenousRead]] = {}
    for phase in range(104):
        x = y = h = 0
        seen: set[tuple[int, int]] = set()
        reads: list[ExogenousRead] = []
        for offset in range(max_offset):
            cell = (x, y)
            bit = w0_bits[(phase + offset) % 104]
            if cell not in seen:
                reads.append(ExogenousRead(offset, x, y, required_black=(bit == 0)))
                seen.add(cell)
            if bit:
                h = (h + 1) & 3
            else:
                h = (h + 3) & 3
            x += DX[h]
            y += DY[h]
        schedules[phase] = reads
    return schedules


def lock_occurrences(
    turns: list[int],
    onset: int,
    w0_bits: list[int],
    threshold: int,
    orbit_index: int,
) -> list[Lock]:
    factors = w0_factor_map(w0_bits, threshold)
    mask = (1 << threshold) - 1
    key = 0
    out: list[Lock] = []
    for t, bit in enumerate(turns):
        key = ((key << 1) | bit) & mask
        start = t - threshold + 1
        if start < 1 or start >= onset:
            continue
        phases = factors.get(key)
        if not phases:
            continue
        for phase in phases:
            if turns[start - 1] == w0_bits[(phase - 1) % 104]:
                continue
            depth = threshold
            while start + depth < len(turns) and turns[start + depth] == w0_bits[(phase + depth) % 104]:
                depth += 1
            if depth >= threshold:
                out.append(
                    Lock(
                        orbit_index=orbit_index,
                        threshold=threshold,
                        start=start,
                        phase=phase,
                        depth=depth,
                        is_gate=(phase in GATE_PHASES),
                    )
                )
    out.sort(key=lambda l: (l.start, l.phase, l.threshold))
    return out


def onset_phase(turns: list[int], onset: int, w0_bits: list[int]) -> int:
    best_phase = -1
    best_depth = -1
    for phase in range(104):
        depth = 0
        while onset + depth < len(turns) and turns[onset + depth] == w0_bits[(phase + depth) % 104]:
            depth += 1
        if depth > best_depth:
            best_phase = phase
            best_depth = depth
    if best_depth < 104:
        raise AssertionError(f"onset phase not certified: depth={best_depth}")
    return best_phase


def eval_checklist(
    black: set[tuple[int, int]],
    origin_x: int,
    origin_y: int,
    heading: int,
    schedule: list[ExogenousRead],
    max_offset: int,
) -> EvalResult:
    checked = 0
    for read in schedule:
        if read.offset > max_offset:
            break
        ax, ay = rel_to_abs(origin_x, origin_y, heading, read.rel_x, read.rel_y)
        actual_black = (ax, ay) in black
        checked += 1
        if actual_black != read.required_black:
            return EvalResult(
                first_bad_offset=read.offset,
                first_bad_rel=(read.rel_x, read.rel_y),
                first_bad_abs=(ax, ay),
                required_black=read.required_black,
                actual_black=actual_black,
                exogenous_reads_checked=checked,
            )
    return EvalResult(
        first_bad_offset=None,
        first_bad_rel=None,
        first_bad_abs=None,
        required_black=None,
        actual_black=None,
        exogenous_reads_checked=checked,
    )


def simulate_and_evaluate(
    orbit,
    locks: list[Lock],
    entry_lock: Lock,
    schedules: dict[int, list[ExogenousRead]],
    entry_horizon: int,
    smin: int,
    smax: int,
) -> list[dict[str, object]]:
    all_locks = locks + [entry_lock]
    by_start: dict[int, list[Lock]] = defaultdict(list)
    for lock in all_locks:
        by_start[lock.start].append(lock)

    black, _side, _dens = build_seed(orbit.rngstate, smin, smax)
    rows: list[dict[str, object]] = []
    x = y = h = 0
    horizon = orbit.onset_dump + 1
    for t in range(horizon):
        for lock in by_start.get(t, ()):
            max_offset = entry_horizon if lock.start == orbit.onset_dump else lock.depth
            ev = eval_checklist(black, x, y, h, schedules[lock.phase], max_offset)
            if lock.start == orbit.onset_dump:
                verdict = "entry_ok" if ev.first_bad_offset is None else "entry_bad"
            elif not lock.is_gate:
                if lock.depth == R_MUTE.get(lock.phase):
                    verdict = "mute_threshold_death"
                else:
                    verdict = "mute_early_death"
            elif ev.first_bad_offset == lock.depth:
                verdict = "gate_exact_death"
            elif ev.first_bad_offset is None:
                verdict = "gate_no_bad_before_death"
            elif ev.first_bad_offset < lock.depth:
                verdict = "gate_bad_before_death"
            else:
                verdict = "gate_bad_after_death"

            bad_kind = ""
            if ev.first_bad_offset is not None:
                if ev.required_black and not ev.actual_black:
                    bad_kind = "missing_black"
                elif (not ev.required_black) and ev.actual_black:
                    bad_kind = "frontier_black_collision"
                else:
                    bad_kind = "color_mismatch"

            rows.append(
                {
                    "idx": orbit.index,
                    "shard": orbit.shard,
                    "onset": orbit.onset_dump,
                    "rngstate": orbit.rngstate,
                    "threshold": lock.threshold,
                    "start": lock.start,
                    "kind": "entry" if lock.start == orbit.onset_dump else "pre_onset_lock",
                    "phase": lock.phase,
                    "is_gate": int(lock.is_gate),
                    "depth": lock.depth,
                    "death_step": "" if lock.start == orbit.onset_dump else lock.start + lock.depth,
                    "first_bad_offset": "" if ev.first_bad_offset is None else ev.first_bad_offset,
                    "bad_rel_x": "" if ev.first_bad_rel is None else ev.first_bad_rel[0],
                    "bad_rel_y": "" if ev.first_bad_rel is None else ev.first_bad_rel[1],
                    "bad_abs_x": "" if ev.first_bad_abs is None else ev.first_bad_abs[0],
                    "bad_abs_y": "" if ev.first_bad_abs is None else ev.first_bad_abs[1],
                    "required_black": "" if ev.required_black is None else int(ev.required_black),
                    "actual_black": "" if ev.actual_black is None else int(ev.actual_black),
                    "bad_kind": bad_kind,
                    "exogenous_reads_checked": ev.exogenous_reads_checked,
                    "verdict": verdict,
                }
            )

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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Iterable[str] | None = None) -> None:
    if not rows:
        return
    fields = list(fieldnames) if fieldnames is not None else list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    pre = [r for r in rows if r["kind"] == "pre_onset_lock"]
    entries = [r for r in rows if r["kind"] == "entry"]
    by_thr = Counter(int(r["threshold"]) for r in pre)
    gate_by_thr = Counter(int(r["threshold"]) for r in pre if int(r["is_gate"]))
    verdicts = Counter(str(r["verdict"]) for r in rows)
    bad_kind = Counter(str(r["bad_kind"]) for r in pre if r["bad_kind"])
    phase_gate = Counter(int(r["phase"]) for r in pre if int(r["is_gate"]))
    offset_gate = Counter(int(r["first_bad_offset"]) for r in pre if int(r["is_gate"]) and r["first_bad_offset"] != "")
    mute_saturation = Counter(str(r["verdict"]) for r in pre if not int(r["is_gate"]))

    gate_rows = [r for r in pre if int(r["is_gate"])]
    gate_exact = sum(1 for r in gate_rows if r["verdict"] == "gate_exact_death")
    entry_ok = sum(1 for r in entries if r["verdict"] == "entry_ok")

    return {
        "rows": len(rows),
        "pre_onset_locks": len(pre),
        "entry_controls": len(entries),
        "pre_onset_by_threshold": dict(sorted(by_thr.items())),
        "gate_pre_onset_by_threshold": dict(sorted(gate_by_thr.items())),
        "gate_exact_deaths": gate_exact,
        "gate_deaths_total": len(gate_rows),
        "gate_exact_fraction": gate_exact / len(gate_rows) if gate_rows else None,
        "entry_ok": entry_ok,
        "entry_controls_total": len(entries),
        "entry_ok_fraction": entry_ok / len(entries) if entries else None,
        "verdicts": dict(sorted(verdicts.items())),
        "bad_kind": dict(sorted(bad_kind.items())),
        "mute_verdicts": dict(sorted(mute_saturation.items())),
        "top_gate_phases": phase_gate.most_common(12),
        "top_gate_bad_offsets": offset_gate.most_common(12),
    }


def print_summary(payload: dict[str, object]) -> None:
    print(
        "pre_locks={pre_onset_locks} gate_deaths={gate_deaths_total} "
        "gate_exact={gate_exact_deaths} ({gate_exact_fraction:.4f}) "
        "entry_ok={entry_ok}/{entry_controls_total} ({entry_ok_fraction:.4f})".format(**payload)
    )
    print(f"by threshold: {payload['pre_onset_by_threshold']}")
    print(f"gate by threshold: {payload['gate_pre_onset_by_threshold']}")
    print(f"verdicts: {payload['verdicts']}")
    print(f"bad_kind: {payload['bad_kind']}")
    print(f"top gate phases: {payload['top_gate_phases']}")
    print(f"top gate bad offsets: {payload['top_gate_bad_offsets']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dumps", type=Path, default=ALPHA / "dumps_all.txt")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-seconds", type=float, default=290.0)
    ap.add_argument("--entry-horizon", type=int, default=1248)
    ap.add_argument("--out-prefix", type=Path, default=ALPHA / "lock_checklist_probe")
    ap.add_argument("--smin", type=int, default=5)
    ap.add_argument("--smax", type=int, default=25)
    args = ap.parse_args()

    started = time.perf_counter()
    dumps = parse_dumps(args.dumps)
    if args.limit:
        dumps = dumps[: args.limit]
    w0_bits = load_w0_bits(DATA / "w0.txt")
    tail_steps = max(args.entry_horizon, max(LOCK_THRESHOLDS), 208)

    all_rows: list[dict[str, object]] = []
    completed = 0
    for orbit in dumps:
        if time.perf_counter() - started > args.max_seconds:
            print(f"STOP: max-seconds={args.max_seconds:.1f}; completate={completed}")
            break
        turns, _deep, sim_bites, _side, _dens = simulate_orbit(
            orbit.rngstate, orbit.onset_dump, args.smin, args.smax, tail_steps
        )
        compare_bites(sim_bites, orbit.bite_times, orbit)
        locks: list[Lock] = []
        for threshold in LOCK_THRESHOLDS:
            locks.extend(lock_occurrences(turns, orbit.onset_dump, w0_bits, threshold, orbit.index))
        max_depth = max((l.depth for l in locks), default=0)
        phase = onset_phase(turns, orbit.onset_dump, w0_bits)
        entry_lock = Lock(
            orbit_index=orbit.index,
            threshold=0,
            start=orbit.onset_dump,
            phase=phase,
            depth=args.entry_horizon,
            is_gate=(phase in GATE_PHASES),
        )
        schedules = make_exogenous_schedule(w0_bits, max(max_depth + 1, args.entry_horizon + 1))
        rows = simulate_and_evaluate(orbit, locks, entry_lock, schedules, args.entry_horizon, args.smin, args.smax)
        all_rows.extend(rows)
        completed += 1
        gate_exact = sum(1 for r in rows if r["verdict"] == "gate_exact_death")
        gate_total = sum(1 for r in rows if r["kind"] == "pre_onset_lock" and int(r["is_gate"]))
        print(
            f"idx={orbit.index:2d} onset={orbit.onset_dump:6d} locks={len(locks):4d} "
            f"gate={gate_total:4d} exact={gate_exact:4d} entry_phase={phase}"
        )

    if not all_rows:
        print("Nessuna orbita completata; nessun output.")
        return 1

    summary = summarize(all_rows)
    summary.update(
        {
            "source": str(args.dumps),
            "orbits_requested": len(dumps),
            "orbits_completed": completed,
            "thresholds": LOCK_THRESHOLDS,
            "gate_phases": GATE_PHASES,
            "entry_horizon": args.entry_horizon,
            "elapsed_seconds": time.perf_counter() - started,
        }
    )

    out_prefix: Path = args.out_prefix
    rows_csv = out_prefix.with_name(out_prefix.name + "_rows.csv")
    summary_json = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(rows_csv, all_rows)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print_summary(summary)
    print(f"\nCSV rows: {rows_csv}")
    print(f"JSON summary: {summary_json}")
    print(f"orbits completed={completed}, elapsed={time.perf_counter() - started:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
