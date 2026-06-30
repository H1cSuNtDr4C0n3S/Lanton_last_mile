"""
entry_seed/escape_scaling.py  (sessione §77, probe §77.7)

Prova di viabilita' della strada rotor-router NON abeliana: l'esponente gamma in L~area^gamma
(L = lunghezza bite-stallo, area = celle distinte del patch) e' stabile sotto il bound abeliano
1.5 attraverso orbite e scale, o deriva verso l'alto?

Esito (§77.7): deriva verso l'alto (curvatura positiva: esp. locale 0.81->1.10->1.39->1.68 da
area 15 a 120, attraversa 1.5 ~area 100) e la coda grande e' troppo rara a T~1e5 per inchiodarlo.
Inoltre: i bite-stalli sono LIMITATI ~303 fino a T~1e5 (non crescono 10k->106k), quindi sono una
quantita' DIVERSA dallo stallo crescente di #30 -- da riconciliare. Probe tira CONTRO la strada.

Uso: python entry_seed/escape_scaling.py  -> entry_seed/escape_scaling.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clib

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
HERE = os.path.dirname(os.path.abspath(__file__))


def bite_stalls(seed, cap=240000, H=2200):
    r = clib.simulate(np.array([seed]), 0, 0, 0, cap, H)
    onset, _ = clib.detect_onset(r["turns"])
    if onset is None or onset < 8000:
        return None
    T = onset; visited = set(); color = {}; x = y = 0; h = 0
    b = np.zeros(T, np.uint8); px = np.zeros(T, np.int64); py = np.zeros(T, np.int64)
    for t in range(T):
        px[t] = x; py[t] = y; c = (x, y); b[t] = 0 if c in visited else 1
        col = color.get(c, 0)
        if col == 0: h = (h + 1) & 3; color[c] = 1
        else:        h = (h + 3) & 3; color[c] = 0
        visited.add(c); x += DX[h]; y += DY[h]
    st = []; t0 = None
    for t in range(T):
        if b[t] == 0:
            if t0 is None: t0 = t
        elif t0 is not None: st.append((t0, t)); t0 = None
    L = np.array([e - s for s, e in st]); nc = np.empty(len(st), int)
    for i, (a, e) in enumerate(st):
        xs = px[a:e]; ys = py[a:e]; nc[i] = len({(int(xs[j]), int(ys[j])) for j in range(len(xs))})
    return int(onset), L, nc


def gamma(L, nc, lo=10):
    m = L >= lo
    if m.sum() < 30: return None
    lx = np.log(nc[m].astype(float)); ly = np.log(L[m].astype(float))
    A = np.vstack([lx, np.ones_like(lx)]).T
    sl = np.linalg.lstsq(A, ly, rcond=None)[0][0]
    return float(sl), int(m.sum())


def main():
    out = {"bound_abelian_exponent": 1.5, "cross_orbit": {}, "curvature": {}, "sparsity": {}}
    # cross-orbit (alcuni semi cella-singola = griglia vuota; lo notiamo)
    for s in [(7, -7), (0, -14), (10, -10), (11, 8)]:
        res = bite_stalls(s)
        if res is None: continue
        onset, L, nc = res; g = gamma(L, nc)
        if g: out["cross_orbit"][str(s)] = {"onset": onset, "n": g[1], "gamma_global": round(g[0], 3),
                                            "stall_max": int(L.max())}
    # griglia vuota equivalente
    ev = bite_stalls((10000, 10000))
    if ev: out["empty_grid_equiv"] = {"onset": ev[0], "stall_max": int(ev[1].max())}
    # curvatura su (7,-7): fit quadratico log L vs log area + esponenti locali
    o7, L7, nc7 = bite_stalls((7, -7))
    m = L7 >= 10; lx = np.log(nc7[m].astype(float)); ly = np.log(L7[m].astype(float))
    q, lin, c = np.linalg.lstsq(np.vstack([lx ** 2, lx, np.ones_like(lx)]).T, ly, rcond=None)[0]
    out["curvature"] = {"quad_coeff": round(float(q), 3),
                        "local_exponent": {str(a): round(float(2 * q * np.log(a) + lin), 2)
                                           for a in [15, 30, 60, 120]},
                        "interpretation": "quad_coeff>0 => esponente CRESCE con la scala, attraversa 1.5 ~area 100"}
    out["sparsity"] = {f"[{lo},{hi})": int(((nc7 >= lo) & (nc7 < hi)).sum())
                       for lo, hi in [(10, 20), (20, 40), (40, 80), (80, 160), (160, 10 ** 9)]}
    out["verdict"] = ("esponente non scala-stabile (deriva su, attraversa 1.5); coda grande troppo rara "
                      "a T~1e5 => premessa non de-riscabile a buon mercato; bite-stall limitato ~303 "
                      "(quantita' diversa da #30). Tira CONTRO la strada non-abeliana come bet immediato.")
    json.dump(out, open(os.path.join(HERE, "escape_scaling.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
