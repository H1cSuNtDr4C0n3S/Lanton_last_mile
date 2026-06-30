"""
entry_seed/stall_geometry.py  (sessione §77)

Geometria degli stalli del morso sulla fase caotica dell'orbita-record (7,-7), onset 106258.
Stallo = run massimale di b(t)=0 (b=1 ⟺ lettura di cella fresca). Misura, per ogni stallo:
lunghezza, bbox (diametro Chebyshev), celle distinte visitate, molteplicita' (passi/cella),
eta' delle celle lette. Fit di scaling bbox~len^alpha; molteplicita' mediana.

Scopo: distinguere stallo-corridoio (1D, alpha~1) da stallo-rotore-puntiforme (molteplicita' alta)
da stallo area-filling (alpha~0.5, molteplicita' bassa ~costante). Verdetto §77: area-filling a
molteplicita' limitata su detrito invecchiato = firma di rotor-router walk.

NB: lo stallo del MORSO (b=0 run) e' il livello #24/#30 (DECLASSATO come pavimento-del-morso),
NON la "stallo" di α1 (fallimento eterno di ingresso). Questo script caratterizza la TESSITURA
del caos, non attacca α1/Link 1.

Uso:  python entry_seed/stall_geometry.py
Output: entry_seed/stall_geometry.json, entry_seed/stall_footprint.png
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clib

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
HERE = os.path.dirname(os.path.abspath(__file__))


def run_chaos(seed=((7, -7),), cap=170000, Hgrid=1500):
    r = clib.simulate(np.array(seed), 0, 0, 0, cap, Hgrid)
    onset, _ = clib.detect_onset(r["turns"])
    T = onset
    visited = set(); color = {}; last_mod = {}
    x = y = 0; h = 0
    b = np.zeros(T, dtype=np.uint8); age = np.zeros(T, dtype=np.int64)
    px = np.zeros(T, dtype=np.int64); py = np.zeros(T, dtype=np.int64)
    for t in range(T):
        px[t] = x; py[t] = y; c = (x, y)
        fresh = c not in visited
        b[t] = 0 if fresh else 1  # tenuto come "revisita" per chiarezza; b_morso=1-questo
        b[t] = 1 if fresh else 0
        age[t] = 0 if fresh else (t - last_mod[c])
        col = color.get(c, 0)
        if col == 0: h = (h + 1) & 3; color[c] = 1
        else:        h = (h + 3) & 3; color[c] = 0
        visited.add(c); last_mod[c] = t; x += DX[h]; y += DY[h]
    return T, onset, b, age, px, py


def stalls_of(b, T):
    out = []; t0 = None
    for t in range(T):
        if b[t] == 0:
            if t0 is None: t0 = t
        elif t0 is not None:
            out.append((t0, t)); t0 = None
    if t0 is not None: out.append((t0, T))
    return out


def analyze():
    T, onset, b, age, px, py = run_chaos()
    N = np.cumsum(b); Z = np.arange(1, T + 1) - N + 1
    st = stalls_of(b, T)
    L = np.array([t1 - t0 for t0, t1 in st])
    bbox = np.empty(len(st), int); ncells = np.empty(len(st), int); amax = np.empty(len(st), int)
    for i, (a, e) in enumerate(st):
        xs = px[a:e]; ys = py[a:e]
        bbox[i] = max(xs.max() - xs.min(), ys.max() - ys.min())
        ncells[i] = len({(int(xs[j]), int(ys[j])) for j in range(len(xs))})
        amax[i] = int(age[a:e].max())

    def fit(yy, mask):
        lx = np.log(L[mask].astype(float)); ly = np.log(np.maximum(yy[mask], 1).astype(float))
        A = np.vstack([lx, np.ones_like(lx)]).T
        sl, ic = np.linalg.lstsq(A, ly, rcond=None)[0]
        pred = A @ np.array([sl, ic]); r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()
        return float(sl), float(r2)

    m = L >= 10
    a_bbox, r2_bbox = fit(bbox, m)
    mult = L[m].astype(float) / np.maximum(ncells[m], 1)
    res = {
        "orbit": "(7,-7)", "onset": int(onset),
        "Z_slope_chaos": round(float((Z[-1] - Z[0]) / T), 4),
        "bite_rate_chaos": round(float(N[-1] / T), 4),
        "n_stalls": len(st), "len_max": int(L.max()), "len_median": int(np.median(L)),
        "bbox_vs_len_exponent": round(a_bbox, 3), "bbox_vs_len_R2": round(r2_bbox, 3),
        "multiplicity_median": round(float(np.median(mult)), 3),
        "multiplicity_q90": round(float(np.percentile(mult, 90)), 3),
        "longest_stall": {"len": int(L.max()),
                          "bbox": int(bbox[int(L.argmax())]),
                          "ncells": int(ncells[int(L.argmax())]),
                          "age_max": int(amax[int(L.argmax())])},
    }
    json.dump(res, open(os.path.join(HERE, "stall_geometry.json"), "w"), indent=1)

    # footprint dello stallo piu' lungo
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from collections import Counter
    i = int(L.argmax()); a, e = st[i]
    xs = px[a:e] - px[a:e].min(); ys = py[a:e] - py[a:e].min()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(xs, ys, '-', lw=0.5, color='#888', alpha=0.6)
    for (cx, cy), k in Counter(zip(xs.tolist(), ys.tolist())).items():
        ax.add_patch(plt.Rectangle((cx - .5, cy - .5), 1, 1, color=plt.cm.viridis(min(k / 4, 1)), zorder=2))
    ax.plot(xs[0], ys[0], '^', color='red', ms=10, zorder=5)
    ax.plot(xs[-1], ys[-1], '*', color='lime', ms=14, zorder=5)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Stallo piu' lungo: area-filling su detrito vecchio\nlen=%d, %d celle, bbox=%d, molt.=%.2f"
                 % (L[i], ncells[i], bbox[i], L[i] / ncells[i]))
    fig.savefig(os.path.join(HERE, "stall_footprint.png"), dpi=130, bbox_inches="tight")
    for k, v in res.items():
        print(k, "=", v)
    return res


if __name__ == "__main__":
    analyze()
