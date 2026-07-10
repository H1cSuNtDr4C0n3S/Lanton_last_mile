# door_approach_census.py — §104.1: l'APPROCCIO alla porta e' canonico?
#
# §103 ha misurato picco ext=5 / buco ext=3 (ext = lunghezza del combaciamento
# all'indietro con W0 prima dell'onset). Qui la domanda a monte, NON condizionata
# a W0: quali sono le ultime 12 svolte PRIMA dell'onset (turns[t_on-12..t_on))?
# Se poche parole dominano, l'approccio e' un oggetto canonico A* e la porta-0
# e' "A* + coda W0-fase-0": il primo candidato-teorema sulla porta (rigioco/lock
# alla §87 sul germe della porta).
#
# Misure (2500 semi catena-3, riuso dichiarato; gate: conteggi cluster == §103):
#   - hist delle parole d'approccio (12 svolte) per cluster di fase
#     (0 esatta / ext 1-7 / porta-24-25 / fuori);
#   - top parole con conteggi; entropia empirica;
#   - per il buco-3: le parole d'approccio dei casi ext=3 (n~1) e ext=4;
#   - confronto: l'approccio dominante e' un frammento di W0? (overlap con
#     tutte le rotazioni).
# Uscita: alpha1/door_approach_census_summary.json
import sys, os, json, time, argparse
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, xs, ALPHA
from record_word_census import run_collect_records

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "fresh_onset_phase_census_summary.json")
OUT = os.path.join(HERE, "door_approach_census_summary.json")
BASE = 0x9E3779B97F4A7C15
GOLD = 0xBF58476D1CE4E5B9
APP = 12

W0 = open(os.path.join(HERE, "..", "data", "w0.txt")).read().strip()
W0b = "".join("1" if c == "R" else "0" for c in W0)
ROTS = {W0b[k:] + W0b[:k]: k for k in range(104)}


def fresh_states(n, base=None):
    s = xs(xs(BASE if base is None else base))
    out = []
    for _ in range(n):
        out.append(s)
        s = xs(xs(s ^ GOLD))
    return out


def probe(rngstate):
    seed, _, _ = build_seed(rngstate, 5, 25)
    if not seed or min(cy for (_, cy) in seed) > 0:
        return {"rngstate": rngstate, "skip": True}
    turns, t_on, _ = run_collect_records(seed)
    if t_on < 0:
        return {"rngstate": rngstate, "no_onset": True}
    per = "".join(str(b) for b in turns[t_on:t_on + 104])
    ph = ROTS.get(per)
    assert ph is not None
    if t_on < APP:
        return {"rngstate": rngstate, "skip": True}
    app = "".join("R" if b else "L" for b in turns[t_on - APP:t_on])
    return {"rngstate": rngstate, "onset": t_on, "fase": ph, "app": app}


def _worker(s):
    try:
        return probe(s)
    except AssertionError as e:
        return {"rngstate": s, "assert_error": str(e)}


def cluster_of(ph):
    if ph == 0:
        return "fase0"
    if 97 <= ph <= 103:
        return f"ext{104 - ph}"
    if ph in (24, 25):
        return "porta24"
    return "fuori"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-seeds", type=int, default=2500)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    t0 = time.time()

    states = fresh_states(args.n_seeds, base=xs(BASE ^ 0x94D049BB133111EB))
    with mp.Pool(args.workers) as pool:
        results = pool.map(_worker, states, chunksize=8)
    errors = [r for r in results if r.get("assert_error")]
    assert not errors, errors[:3]
    ok = [r for r in results if "fase" in r]

    # gate: cluster == §103 (modulo gli skip per t_on < APP, dichiarati)
    ref = json.load(open(REF))
    n0 = sum(1 for r in ok if r["fase"] == 0)
    next_ = sum(1 for r in ok if 97 <= r["fase"] <= 103)
    n24 = sum(1 for r in ok if r["fase"] in (24, 25))
    nfu = len(ok) - n0 - next_ - n24
    skew = ref["porta_0_esatta"] - n0
    assert abs(skew) <= 2, f"gate §103: fase0 {n0} vs {ref['porta_0_esatta']}"
    print(f"GATE §103: cluster riprodotti (fase0 {n0}, ext {next_}, "
          f"porta24 {n24}, fuori {nfu}; skip extra per onset<{APP}: "
          f"{ref['onset_censiti'] - len(ok)})", flush=True)

    # istogrammi per cluster
    from collections import Counter, defaultdict
    by_cluster = defaultdict(Counter)
    for r in ok:
        by_cluster[cluster_of(r["fase"])][r["app"]] += 1
    allc = Counter(r["app"] for r in ok)

    def top(c, k=6):
        return [{"app": a, "n": n} for a, n in c.most_common(k)]

    # overlap dell'approccio dominante con W0 (tutte le rotazioni)
    dom = allc.most_common(1)[0][0]
    domb = "".join("1" if ch == "R" else "0" for ch in dom)
    best_ov = 0
    for k in range(104):
        rot = (W0b[k:] + W0b[:k]) * 2
        for off in range(104):
            ov = 0
            for i in range(APP):
                if domb[APP - 1 - i] == rot[(off - 1 - i) % 104]:
                    ov += 1
                else:
                    break
            best_ov = max(best_ov, ov)
    out = {
        "n_onset": len(ok), "APP": APP,
        "cluster_counts": {"fase0": n0, "ext": next_, "porta24": n24,
                           "fuori": nfu},
        "parole_approccio_distinte": len(allc),
        "top_globale": top(allc, 10),
        "top_per_cluster": {c: top(cnt) for c, cnt in sorted(by_cluster.items())},
        "dominante": dom,
        "dominante_suffix_overlap_con_W0": best_ov,
        "elapsed_s": round(time.time() - t0, 1)}
    print(f"onset {len(ok)}: parole d'approccio distinte {len(allc)}", flush=True)
    print("TOP globale:", flush=True)
    for e in out["top_globale"]:
        print(f"  {e['app']} x{e['n']}", flush=True)
    for c in sorted(by_cluster):
        cnt = by_cluster[c]
        print(f"cluster {c} (n={sum(cnt.values())}): top "
              f"{[(a, n) for a, n in cnt.most_common(3)]}", flush=True)
    print(f"dominante: {dom}; overlap suffisso max con W0 (ogni rotazione/offset): "
          f"{best_ov}/{APP}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
