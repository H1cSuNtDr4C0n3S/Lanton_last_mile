# danger_reach_real.py — §107c: il passato REALE dei 2 lock come punto della
# misura dinamica (n=1 per episodio, DESCRITTIVO — dichiarato, trappola qq).
#
# Il passato vero dell'orbita e' UN cammino dell'albero dei prepend (GB §107b
# lo verifica valido). Qui lo si percorre fino al seme (depth = t-K) e si
# registra d_real(cella) = profondita' della PRIMA lettura all'indietro di
# ogni cella di R_T — da confrontare con d_hit-SOVRA (minimo dell'albero):
# quanto tardi il passato reale tocca cio' che l'albero potrebbe toccare a
# d_hit? Le celle MAI lette dal passato reale hanno colore al record = colore
# di seme (bianche se fuori dal seme): sono il deposito antico "puro".
import sys, os, json

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from delta4_long_orbits import build_seed
from record_word_census import run_collect_records
from danger_backward_autopsy import Machine, K

HERE = os.path.dirname(os.path.abspath(__file__))
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")


def main():
    hunt = json.load(open(HUNT))
    out = {"nota": "d_real = prima lettura all'indietro del passato REALE "
                   "(n=1 per episodio, descrittivo); d_hit = minimo SOVRA "
                   "dell'albero; profondita' in passi dal bordo di w",
           "episodi": []}
    reach = {}
    for lock, dep in (("A", 55), ("B", 48)):
        p = os.path.join(HERE, f"danger_reach_c_LOCK{lock}_d{dep}.json")
        reach[lock] = json.load(open(p))
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        lock = "AB"[i]
        seed, _, _ = build_seed(rngs, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        w = tuple(turns[t - K:t])
        m = Machine(w)
        req = dict(m.req0)
        d_real = {}
        p, h = (0, 0), 0
        max_d = t - K
        for d in range(1, max_d + 1):
            bit = turns[t - K - d]
            c = 0 if bit else 1
            p_prev = (p[0] - DX[h], p[1] - DY[h])
            assert m.anchor_y(p_prev) >= 1, f"record-compat viola a {d}"
            if p_prev in req:
                assert c == 1 - req[p_prev], f"alternanza viola a {d}"
            req[p_prev] = c
            if p_prev in m.rt_walk and p_prev not in d_real:
                d_real[p_prev] = d
            h = (h - 1) & 3 if c == 0 else (h + 1) & 3
            p = p_prev
        fh = reach[lock]["first_hit_anchor_rt"]
        print(f"[LOCK{lock}] profondita' del passato reale disponibile: "
              f"{max_d} passi (t={t}, seme a depth {max_d})", flush=True)
        print(f"    cella ancora | d_hit (SOVRA) | d_real | rapporto",
              flush=True)
        tab = {}
        for cw, ca in sorted(m.rt_walk.items(), key=lambda kv: kv[1]):
            dr = d_real.get(cw)
            dh = fh[str(ca)]
            tab[str(ca)] = {"d_hit_sovra": dh, "d_real": dr}
            rap = (f"{dr / dh:.1f}x" if dr is not None and dh else "-")
            print(f"    {str(ca):>8} | {dh:5} | "
                  f"{dr if dr is not None else 'MAI (colore=seme)':>6} | "
                  f"{rap}", flush=True)
        n_mai = sum(1 for v in tab.values() if v["d_real"] is None)
        print(f"[LOCK{lock}] celle MAI lette dal passato reale: "
              f"{n_mai}/{len(tab)}", flush=True)
        out["episodi"].append({"label": f"LOCK{lock}", "t": t,
                               "profondita_reale": max_d,
                               "celle": tab, "mai_lette": n_mai})
    op = os.path.join(HERE, "danger_reach_real.json")
    with open(op, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {op}", flush=True)


if __name__ == "__main__":
    main()
