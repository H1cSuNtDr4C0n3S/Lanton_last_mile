# lrrrr_avoidance_certificate.py — §85b: certificato via automa finestra dell'enunciato
# universale "nessuna lettura nera fuori dalla memoria di finestra di raggio r inizia una
# cavalcata (LRRRR)^3".
#
# Fondamento (trappola-c compliant): l'automa finestra e' una SOVRA-approssimazione dei cammini
# reali; ogni lettura nera reale di cella non tracciata nella finestra-r corrisponde a un arco
# assumeB (tipo=2). Se nell'automa NESSUN cammino che parte da un arco assumeB puo' realizzare
# le 14 svolte successive RRRR LRRRR LRRRR (la L iniziale e' l'arco assumeB stesso), allora
# nessuna orbita reale puo' farlo: enunciato "per ogni cammino", che trasferisce.
# Se invece un cammino sopravvive, il verdetto e' INCONCLUSIVO a quel raggio (fantasma o reale).
#
# Proprieta' chiave: seguire una parola di svolte forzata e' DETERMINISTICO — per ogni stato e
# colore richiesto c'e' al piu' un arco (forzato se il centro e' noto, assume* se e' U).
# Il costo e' quindi |archi assumeB| x 14 passi.
#
# Output per ogni raggio: numero di archi assumeB, istogramma della profondita' di
# sopravvivenza (quante lettere della coda RRRR(LRRRR)^inf si realizzano prima di morire),
# massimo prefisso realizzabile, e VERDETTO per (LRRRR)^2 (9 lettere di coda) e (LRRRR)^3 (14).
#
# Validazione: la build deve riprodurre i conteggi noti (r1: 15 stati; r2: 403 stati, selftest
# gia' verde in sessione) e i tipi di arco devono combaciare con radius*_summary.json se presente.
import sys, os, json, time, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from window_automaton import build, W, B, U
from delta4_long_orbits import ALPHA

TAIL = bytes([0, 0, 0, 0] + [1, 0, 0, 0, 0] * 2)   # RRRR LRRRR LRRRR (dopo la L iniziale), R=0/L=1... 
# NOTA CONVENZIONE: nel builder tn=1 se colore=W (svolta R), tn=0 se colore=B (svolta L).
# Qui codifichiamo la coda in termini di tn richiesto: R->tn=1, L->tn=0.
TAIL_TN = bytes([1, 1, 1, 1] + [0, 1, 1, 1, 1] * 2)  # 14 svolte: RRRR LRRRR LRRRR
CUT2 = 9    # prefisso che completa (LRRRR)^2 (L + 9 = 10 svolte)
CUT3 = 14   # prefisso che completa (LRRRR)^3

def certify(radius):
    t0 = time.time()
    order, src, dst, ty, tn = build(radius)
    N = len(order)
    print(f"r={radius}: {N} stati, {len(src)} archi "
          f"(forced {int((ty==0).sum())}, assumeW {int((ty==1).sum())}, assumeB {int((ty==2).sum())}), "
          f"build {time.time()-t0:.1f}s")
    # lookup deterministico (stato, tn richiesto) -> stato successivo
    nxt = {}
    for s, d, tt in zip(src.tolist(), dst.tolist(), tn.tolist()):
        key = (s, tt)
        assert key not in nxt or nxt[key] == d, "transizione non deterministica a parita' di colore"
        nxt[key] = d
    ab_edges = [(s, d) for s, d, t2 in zip(src.tolist(), dst.tolist(), ty.tolist()) if t2 == 2]
    depth_hist = {}
    survivors3 = []
    max_depth = 0
    for s0, d0 in ab_edges:
        cur = d0; depth = 0
        for i in range(CUT3):
            nx = nxt.get((cur, TAIL_TN[i]))
            if nx is None:
                break
            cur = nx; depth += 1
        depth_hist[depth] = depth_hist.get(depth, 0) + 1
        if depth > max_depth: max_depth = depth
        if depth >= CUT3:
            survivors3.append((s0, d0))
    surv2 = sum(v for k, v in depth_hist.items() if k >= CUT2)
    surv3 = len(survivors3)
    print(f"  archi assumeB: {len(ab_edges)}; istogramma profondita' sopravvivenza (svolte della coda realizzate):")
    for k in sorted(depth_hist):
        print(f"    {k:>2}: {depth_hist[k]}")
    print(f"  massimo prefisso realizzabile dopo la L iniziale: {max_depth}/{CUT3}")
    v2 = "CERTIFICATO" if surv2 == 0 else f"INCONCLUSIVO ({surv2} sopravvissuti)"
    v3 = "CERTIFICATO" if surv3 == 0 else f"INCONCLUSIVO ({surv3} sopravvissuti)"
    print(f"  (LRRRR)^2 dopo assumeB: {v2}")
    print(f"  (LRRRR)^3 dopo assumeB: {v3}")
    return {"radius": radius, "states": N, "edges": len(src),
            "assumeB_edges": len(ab_edges),
            "depth_hist": {str(k): v for k, v in sorted(depth_hist.items())},
            "max_prefix": max_depth,
            "survivors_2per": surv2, "survivors_3per": surv3,
            "verdict_2per": surv2 == 0, "verdict_3per": surv3 == 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radii", default="1,2,3")
    ap.add_argument("--out", default=str(ALPHA / "lrrrr_certificate_summary.json"))
    a = ap.parse_args()
    out = []
    for r in [int(s) for s in a.radii.split(",")]:
        out.append(certify(r))
        print()
    json.dump({"results": out, "tail_tn": list(TAIL_TN),
               "statement": "nessuna lettura nera fuori dalla memoria di finestra di raggio r "
                            "inizia (LRRRR)^k, per i k con verdetto CERTIFICATO"},
              open(a.out, "w"), indent=1)
    print(f"scritto {a.out}")

if __name__ == "__main__":
    main()
