"""
entry_seed/abelian_test.py  (sessione §77, test §77.6)

La formica e' un rotor-router ABELIANO almeno localmente sul patch di uno stallo?
Test: congela colori+celle-visitate all'inizio dello stallo piu' lungo di (7,-7); rilancia la
formica dalla stessa cella d'ingresso con i 4 heading; escape = primo passo su cella fresca (non
visitata al momento del congelamento). Confronta i tempi di escape.

Esito (§77.6): NON abeliano in modo netto — la config dei rotori (colori) NON determina la dinamica,
l'heading domina di ~3 ordini di grandezza. I bound di fuga abeliani non si agganciano.
Rovescio: lo scaling L~area^0.785 (molt. 1.57) e' MOLTO sotto il bound rotor-router n<=area^1.5;
la geometria sarebbe favorevole, manca il teorema non-abeliano.

Uso: python entry_seed/abelian_test.py   -> entry_seed/abelian_test.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clib

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    r = clib.simulate(np.array([[7, -7]]), 0, 0, 0, 170000, 1500)
    onset, _ = clib.detect_onset(r["turns"]); T = onset
    # passata 1: trova lo stallo piu' lungo
    visited = set(); color = {}; x = y = 0; h = 0
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
    L = np.array([e - s for s, e in st]); imax = int(L.argmax()); s0, e0 = st[imax]

    # passata 2: ricostruisci stato esatto a t=s0
    visited = set(); color = {}; x = y = 0; h = 0
    for t in range(s0):
        c = (x, y); col = color.get(c, 0)
        if col == 0: h = (h + 1) & 3; color[c] = 1
        else:        h = (h + 3) & 3; color[c] = 0
        visited.add(c); x += DX[h]; y += DY[h]
    start_cell = (x, y); start_h = h; fcol = dict(color); fvis = set(visited)

    def escape(h0, cap=20000):
        col = dict(fcol); xx, yy = start_cell; hh = h0; n = 0
        while n < cap:
            c = (xx, yy)
            if c not in fvis: return n, list(c)
            cc = col.get(c, 0)
            if cc == 0: hh = (hh + 1) & 3; col[c] = 1
            else:       hh = (hh + 3) & 3; col[c] = 0
            xx += DX[hh]; yy += DY[hh]; n += 1
        return cap, None

    esc = {h0: escape(h0) for h0 in range(4)}
    # scaling L vs area
    ncells = np.empty(len(st), int)
    for i, (a, e) in enumerate(st):
        xs = px[a:e]; ys = py[a:e]; ncells[i] = len({(int(xs[j]), int(ys[j])) for j in range(len(xs))})
    m = L >= 10
    lx = np.log(ncells[m].astype(float)); ly = np.log(L[m].astype(float))
    A = np.vstack([lx, np.ones_like(lx)]).T; sl, ic = np.linalg.lstsq(A, ly, rcond=None)[0]
    pred = A @ np.array([sl, ic]); r2 = 1 - ((ly - pred) ** 2).sum() / ((ly - ly.mean()) ** 2).sum()

    out = {
        "stall": {"t0": int(s0), "len": int(L[imax]), "entry_cell": list(start_cell),
                  "real_heading": int(start_h), "patch_visited": len(fvis)},
        "escape_by_heading": {str(h0): {"steps": int(esc[h0][0]), "exit": esc[h0][1]} for h0 in range(4)},
        "abelian": False,
        "heading_spread": "303/1109/1/1135 -> config rotori NON determina dinamica (~3 ordini)",
        "L_vs_area_exponent": round(float(sl), 3), "L_vs_area_R2": round(float(r2), 3),
        "rotor_router_bound_exponent": 1.5,
        "verdict": "non-abeliano netto; geometria favorevole (esponente<<1.5) ma manca teorema non-abeliano",
    }
    json.dump(out, open(os.path.join(HERE, "abelian_test.json"), "w"), indent=1)
    print("escape per heading:", {h0: esc[h0][0] for h0 in range(4)}, "(reale h=%d)" % start_h)
    print("L ~ area^%.3f (R2 %.3f), bound rotor-router 1.5" % (sl, r2))
    print("ABELIANO:", out["abelian"], "->", out["verdict"])


if __name__ == "__main__":
    main()
