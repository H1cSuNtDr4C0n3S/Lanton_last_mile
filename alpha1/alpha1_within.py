#!/usr/bin/env python3
"""alpha1_within.py — the selection-bias-free alpha1 test.

The sandbox result (max-stall ~ T^0.73, density ~ T^-0.20) is CONFOUNDED:
high-onset seeds are *selected for starvation*. To remove the bias we stay
INSIDE a single very long transient and ask whether stalls stay bounded as the
orbit proceeds. Cross-seed comparison is replaced by within-orbit running stats.

Input: a dump file from alpha1_engine (line1 "onset nbites", then bite-times).
Outputs:
  (1) running max-stall(t): max bite-gap whose start <= t, vs t.
      -> SATURATES  => stalls bounded within the orbit  (alpha1-favorable)
      -> KEEPS RISING => no uniform bound                (alpha1-unfavorable)
  (2) windowed bite-rate floor: min over windows of length L of (#bites/L),
      scanned across the orbit, for several L. Is liminf rate > 0 and stable?
Usage: python alpha1_within.py dump1.txt [dump2.txt ...]
"""
import sys, numpy as np

def load(path):
    with open(path) as f:
        onset, nb = map(int, f.readline().split())
        t = np.fromstring(f.read(), sep="\n", dtype=np.int64)
    return onset, t

def running_max_stall(onset, times, npts=400):
    gaps = np.diff(times); starts = times[:-1]
    grid = np.linspace(times[5] if len(times)>5 else 0, onset, npts).astype(np.int64)
    out = np.empty(npts)
    for i, T in enumerate(grid):
        m = gaps[starts <= T]
        out[i] = m.max() if len(m) else 0
    return grid, out

def windowed_floor(onset, times, Ls=(1040, 3120, 10400)):
    b = np.zeros(onset, np.int32); b[times[times<onset]] = 1
    c = np.cumsum(b)
    res = {}
    for L in Ls:
        if onset <= L: continue
        rate = (c[L:] - c[:-L]) / float(L)
        res[L] = (float(rate.min()), float(np.median(rate)), float(rate.mean()))
    return res

def main():
    for path in sys.argv[1:]:
        onset, times = load(path)
        if len(times) < 50:
            print(f"{path}: too short"); continue
        grid, ms = running_max_stall(onset, times)
        # is running-max-stall still rising in the last 30% of the orbit?
        tail = ms[int(0.7*len(ms)):]
        head = ms[int(0.4*len(ms)):int(0.7*len(ms))]
        rising = tail.max() > head.max() + 1e-9
        print(f"\n=== {path} : T={onset}, bites={len(times)}, density={len(times)/onset:.4f} ===")
        print(f"  running max-stall: final={ms[-1]:.0f}  (~{ms[-1]/104:.1f} periods)")
        print(f"  still rising in last 30% of orbit? {'YES (unfavorable)' if rising else 'NO -> saturates (favorable)'}")
        for L,(mn,md,mean) in windowed_floor(onset, times).items():
            print(f"  window L={L:>6}: min-rate(floor)={mn:.4f}  median={md:.4f}  mean={mean:.4f}")
    # decisive read: pool the running-max-stall plateau test across the longest dumps
    print("\nDECISIVE: if, on a T>=1e6 orbit, running max-stall SATURATES and the")
    print("L=10400 floor is bounded away from 0, alpha1-as-bounded-stalls survives the")
    print("within-orbit test (selection bias removed). If it keeps rising / floor->0,")
    print("alpha1 in the strong (uniformly-bounded) form is empirically unsupported and")
    print("only the long-window liminf form (#24) can be argued.")

if __name__ == "__main__":
    main()
