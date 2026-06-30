"""
entry_seed/germ.py  (sessione §76)

Germe minimo di autostrada per fase (le 22 porte di ANATOMY §12), poi frontiera backward.

GERME MINIMO per fase phi:
  - porto la formica in autostrada profonda da griglia vuota; snapshot a fase phi (formica+griglia);
  - tengo solo le nere entro raggio Chebyshev R dalla formica, sbianco il resto; cerco R minimo
    per cui la simulazione forward resta su W0/Wbar con onset<=2;
  - minimizzazione greedy: tolgo ogni cella finche' l'autostrada regge (onset<=2, classe W/Wbar).
  -> germe localmente minimo, onset~0 (entra in 0 passi). Verifica indipendente su 80 periodi.

Uso:  python entry_seed/germ.py 0 16 21 24 25 26 30 31 72 83 90 91 92 93 94 97 98 99 100 101 102 103
Output: entry_seed/germs_22.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clib
from reverse import run_fwd, inv_step

P = clib.P
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "germs_22.json")
PHI_ENT = [0, 16, 21, 24, 25, 26, 30, 31, 72, 83, 90, 91, 92, 93, 94, 97, 98, 99, 100, 101, 102, 103]


def stays_on_highway(black, x, y, h, periods=40, min_periods=8):
    _, _, turns = run_fwd(black, x, y, h, (periods + 2) * P)
    onset, word = clib.detect_onset(turns, min_periods=min_periods)
    if onset is None:
        return False, None, None
    cls, d = clib.classify_word(word)
    return (d == 0 and cls in ("W", "Wbar")), onset, cls


def deep_highway_snapshot(target_phase, run_steps=16000, settle_periods=30):
    _, _, turns = run_fwd(set(), 0, 0, 0, run_steps)
    onset, _ = clib.detect_onset(turns)
    assert onset is not None
    t_target = onset + settle_periods * P
    t_target += (target_phase - (t_target - onset)) % P
    black, st, _ = run_fwd(set(), 0, 0, 0, t_target)
    return black, st, onset


def radius_truncate(black, x, y):
    pts = np.array(sorted(black), dtype=np.int64)
    dist = np.maximum(np.abs(pts[:, 0] - x), np.abs(pts[:, 1] - y))
    order = np.argsort(dist); pts, dist = pts[order], dist[order]
    return (lambda R: set(map(tuple, pts[dist <= R].tolist()))), int(dist.max())


def minimal_germ(target_phase):
    black, (x, y, h), onset = deep_highway_snapshot(target_phase)
    at_R, Rmax = radius_truncate(black, x, y)
    germ = None
    for R in range(1, Rmax + 1):
        g = at_R(R); ok, ons, _ = stays_on_highway(g, x, y, h)
        if ok and ons is not None and ons <= 2:
            germ, Rmin = set(g), R; break
    if germ is None:
        return None
    changed = True
    while changed:
        changed = False
        for c in sorted(germ):
            ok, ons, _ = stays_on_highway(germ - {c}, x, y, h)
            if ok and ons is not None and ons <= 2:
                germ = germ - {c}; changed = True
    ok, ons, cls = stays_on_highway(germ, x, y, h)
    return {"phase": target_phase, "germ": sorted(map(list, germ)), "ax": x, "ay": y, "ah": h,
            "support": len(germ), "germ_onset": int(ons), "class": cls, "Rmin": Rmin}


if __name__ == "__main__":
    phases = [int(p) for p in sys.argv[1:]] or PHI_ENT
    out = {}
    for phi in phases:
        gi = minimal_germ(phi)
        if gi is None:
            print("fase %d: nessun germe a raggi piccoli" % phi); continue
        ok, ons, cls = stays_on_highway(set(map(tuple, map(tuple, gi["germ"]))),
                                        gi["ax"], gi["ay"], gi["ah"], periods=80, min_periods=20)
        print("GERME fase %3d: supporto=%2d onset=%d classe=%s Rmin=%d | verifica80=%s"
              % (phi, gi["support"], gi["germ_onset"], gi["class"], gi["Rmin"], ok))
        out[str(phi)] = gi
    json.dump(out, open(OUT, "w"), indent=1)
    supports = {k: v["support"] for k, v in out.items()}
    if supports:
        mn = min(supports.values())
        print("MIN GLOBALE: %d celle (fasi %s)" % (mn, [k for k, v in supports.items() if v == mn]))
    print("salvato", OUT)
