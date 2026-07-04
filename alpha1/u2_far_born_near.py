# u2_far_born_near.py — §93 (U2-LONTANO): LEMMA DELLA NASCITA VICINA, per-coprente.
#
# LEMMA (deduttivo, dato il ledger §93 + wall_depth §92). Sia e2+w101 una
# coprente-nera il cui albero dei prepend e' FINITO (enumerazione esaustiva senza
# cap raggiunti: profondita' massima D_true, celle del muro con cheb <= r_wall).
# Allora OGNI passato completo che presenta questa coprente a un record y-min
# stretto ha:
#   (i)  nascita entro D_true passi sopra la copertura — e la NASCITA puo' essere
#        in QUALSIASI nodo dell'albero (non solo alle foglie: il passato
#        semplicemente FINISCE alla nascita, nessuna morte richiesta);
#   (ii) prime-letture-della-vita = prime-letture-della-parola-completa; le NERE
#        sono le celle NERE del SEME (GATE L1 di u2_far_ledger): seme_nero =
#        pending ALLA NASCITA, tutti con cheb <= r_seed = max(r_foot, r_wall)
#        (r_foot = raggio del footprint INTERO di coprente+w101: l'estensione
#        puo' riaprire pending anche su celle di parola fuori da pend0);
#   (iii) SE min_{nodi dell'albero} #pending > 0 (verificato PER ENUMERAZIONE,
#        il conteggio puro non basta: jackpot pend0=52 con D=56), il seme nero
#        e' NON vuoto e interseca la palla di raggio r_seed attorno al record.
# Quindi la coprente e' PRESENTABILE SOLO a record con seme entro r_seed —
# VIETATA a ogni record y-min stretto con palla-(r_seed) priva di seme.
# (Vale per ogni orbita, eterna o no; nessun bound uniforme su D richiesto.)
#
# NOTE dalla lente nascita-vicina (pannello, §94b — tutto REGGE, 3/3 esche):
#   - "enumerazione esaustiva" richiede depth_cap >= D_true+1 (un albero con
#     D_true == depth_cap risulterebbe fuggente: direzione conservativa, mai
#     falsi certificati; il check node_cap a pop-time e' cosmetico);
#   - il ramo esaurito-ma-min-pend-0 manterrebbe comunque la GAMBA 1 (vietanza
#     ai record con palla priva della sola ORIGINE): qui non si emette nessun
#     certificato in quel caso per RINUNCIA, non per necessita' (0 occorrenze
#     su 42 testimoni + 273.459 del censimento §94).
#
# Questo lemma SCARICA tutte le coprenti-nere ad albero finito; il campo di
# battaglia di U2-LONTANO resta SOLO la classe fuggente (nere400 & co.).
#
# Per ogni coprente-nera §92: enumerazione DFS con budget largo; se esaurita =>
# certificato (D_true, r_wall, r_seed); se cap raggiunto => "fuggente" (niente
# certificato qui: tocca alla caccia/certificato di palla §93+).
# Uscita: alpha1/u2_far_born_near_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, anchor_trace, FREE
from u2_far_ledger import cheb, pend_set
from u2_far_run import collect_black_covers
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "u2_far_born_near_summary.json")


def wall_exhaustive(word, node_cap=3_000_000, depth_cap=300):
    """DFS esaustivo del muro dei prepend. Ritorna (esaurito?, D_true, r_wall,
    nodi, min_pend): esaurito=True <=> TUTTO l'albero enumerato senza toccare i
    cap; min_pend = minimo di #pending su TUTTI i nodi (radice inclusa) — ogni
    nodo e' una possibile NASCITA."""
    c0, h0, req0 = exact_state(word)
    p0 = len(pend_set(req0))
    maxdep = 0; rmax = 0; nodes = 0
    min_pend = p0
    stack = [(c0, h0, req0, 0, p0)]
    while stack:
        if nodes >= node_cap:
            return False, maxdep, rmax, nodes, min_pend
        c, h, req, dep, p = stack.pop()
        if dep >= depth_cap:
            return False, maxdep, rmax, nodes, min_pend
        for bit in (0, 1):
            nodes += 1
            read = 0 if bit == 1 else 1
            cn_peek = (c[0] - DX[h], c[1] - DY[h])
            rb = req.get(cn_peek, FREE)
            r2 = dict(req)
            cn, hn, _ = exact_step(c, h, r2, bit)
            if cn is None:
                continue
            if read == 1:
                p2 = p + (0 if rb == 0 else 1)     # L apre/riapre (se non gia')
            else:
                p2 = p - (1 if rb == 0 else 0)     # R chiude un pending
            min_pend = min(min_pend, p2)
            maxdep = max(maxdep, dep + 1)
            rmax = max(rmax, cheb(cn))
            stack.append((cn, hn, r2, dep + 1, p2))
    return True, maxdep, rmax, nodes, min_pend


def gate_cross(word):
    """GATE di terra per gli alberi ESAURITI: rienumera TUTTO l'albero usando
    SOLO valid() (nessun exact_step) e per ogni nodo ricomputa i pending da
    anchor_trace. Ritorna (n_nodi_validi, D, min_pend). Da confrontare
    bit-identico con wall_exhaustive."""
    n_valid = 0
    D = 0
    tr = anchor_trace(word)
    min_pend = sum(1 for g in tr[2].values() if g == 1)
    level = [()]
    dep = 0
    while level:
        dep += 1
        nxt = []
        for pref in level:
            for bit in (0, 1):
                p2 = (bit,) + pref
                if valid(p2 + word)[1] is not None:
                    continue
                n_valid += 1
                D = dep
                tr2 = anchor_trace(p2 + word)
                min_pend = min(min_pend,
                               sum(1 for g in tr2[2].values() if g == 1))
                nxt.append(p2)
        level = nxt
    return n_valid, D, min_pend


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--node-cap", type=int, default=3_000_000)
    ap.add_argument("--depth-cap", type=int, default=300)
    ap.add_argument("--cross-validate", action="store_true",
                    help="rienumera gli alberi esauriti con valid() di terra")
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    covers = collect_black_covers(w101)

    rows = []
    n_cert = 0; n_fug = 0
    r_seed_max = 0
    for name, e2 in covers:
        w2 = e2 + w101
        assert valid(w2)[1] is None
        tr = anchor_trace(w2)
        pend0 = sorted(c for c, g in tr[2].items() if g == 1)
        r_foot = max(cheb(c) for c in tr[0])
        exh, D_true, r_wall, nodes, min_pend = wall_exhaustive(
            w2, args.node_cap, args.depth_cap)
        if exh and min_pend > 0:
            if args.cross_validate:
                nv, Dv, mpv = gate_cross(w2)
                # wall_exhaustive conta anche i tentativi non validi: confronto
                # su (D, min_pend) e sui nodi VALIDI (nv*2 <= nodi tentati)
                assert Dv == D_true and mpv == min_pend, \
                    (name, Dv, D_true, mpv, min_pend)
            n_cert += 1
            r_seed = max(r_foot, r_wall)
            r_seed_max = max(r_seed_max, r_seed)
            verdict = "NASCITA-VICINA"
        elif exh:
            r_seed = None
            verdict = "esaurito-ma-min-pend-0 (NO certificato)"
        else:
            n_fug += 1
            r_seed = None
            verdict = "fuggente"
        rows.append({"nome": name, "prof": len(e2), "pend0": len(pend0),
                     "r_foot": r_foot, "esaurito": exh, "D_true": D_true,
                     "r_wall": r_wall, "min_pend_nodi": min_pend,
                     "r_seed": r_seed, "nodi": nodes, "verdetto": verdict})
        print(f"{name:18s} prof{len(e2):4d} pend0={len(pend0):3d} "
              f"r_foot={r_foot:2d} | albero "
              f"{'ESAURITO' if exh else 'CAP     '} D={D_true:3d} "
              f"r_wall={r_wall:2d} min_pend={min_pend:3d} nodi={nodes:8d} "
              f"=> {verdict}"
              + (f" (r_seed={r_seed})" if r_seed is not None else ""),
              flush=True)

    print(f"\nLEMMA DELLA NASCITA VICINA: {n_cert}/{len(covers)} coprenti-nere "
          f"CERTIFICATE vietate ai record con palla senza seme di raggio > "
          f"{r_seed_max}; {n_fug} fuggenti restano il campo di battaglia.",
          flush=True)
    out = {"args": vars(args), "rows": rows,
           "certificate": n_cert, "fuggenti": n_fug,
           "r_seed_max_sui_certificati": r_seed_max,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
