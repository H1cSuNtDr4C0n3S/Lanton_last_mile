# finalize_deltas.py — annota i summary JSON con i delta_r certificati (ciclo esplicito =
# upper bound; fixpoint intero di min_assumeB verify = lower bound) e copia in results/.
import json, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
RES = os.path.join(ROOT, "results")

CERTS = {1: ("r1_delta_cycle.txt", 3, 5), 2: ("r2c_delta_cycle.txt", 1, 7),
         3: ("r3c_delta_cycle.txt", 1, 64), 4: ("r4c_delta_cycle.txt", 2, 313)}

for r, (fn, p, q) in CERTS.items():
    lines = open(os.path.join(BUILD, fn)).read().split()
    cp, cq, word = int(lines[1]), int(lines[3]), lines[5]
    assert (cp, cq) == (p, q), (r, cp, cq)
    assert len(word) == q and word.count("R") + word.count("L") == q, r
    sj = os.path.join(ROOT, f"radius{r}_summary.json")
    out = json.load(open(sj))
    out["min_assumeB_rate_norotor_exact"] = {
        "p": p, "q": q, "value": p / q, "witness_word": word,
        "certificate": "ciclo esplicito (upper) + fixpoint Bellman-Ford intero su DAG noB (lower), min_assumeB.c"}
    json.dump(out, open(sj, "w"), indent=1)
    shutil.copy2(sj, os.path.join(RES, f"radius{r}_summary.json"))
    cyc = os.path.join(ROOT, f"radius{r}_cycles.txt")
    if os.path.exists(cyc):
        shutil.copy2(cyc, os.path.join(RES, f"radius{r}_cycles.txt"))
    print(f"r={r}: delta = {p}/{q} = {p/q:.10f} annotato e copiato in results/")
print("fatto")
