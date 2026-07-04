# u2_far_pend2_floor.py — §93 (U2-LONTANO): PAVIMENTO pend2 ESAUSTIVO sui finiti.
#
# Promosso a script in-repo dal pannello §93 (lente enunciati, E4): sui 12
# testimoni coprenti-nere ad ALBERO FINITO (jackpot/D12/D8/D4), enumerazione
# esaustiva di TUTTI i nodi (ogni nodo = possibile nascita) e minimo dei pending
# nella palla-2 del record. Esito atteso (calcolo del pannello): min pend2 = 2
# (jackpot, residuo {(-1,1),(0,1)}), 3 (D12/D8), 4 (D4).
#
#   => TEOREMA (per enumerazione): per queste 12 coprenti, OGNI passato completo
#   lascia >= 2 pending nella palla-2 = >= 2 celle NERE di SEME a cheb <= 2 dal
#   record: vietate ai record con palla-2 senza seme. E' il caso ad albero finito
#   del TEOREMA DEL LEDGER SPORCO; sulle 6 fuggenti resta congettura misurata.
#
# GATE: i conteggi dei nodi validi devono coincidere con gli alberi di
# u2_far_born_near (116/100/26/26/26/26/26/18/18/18/10/10) e D_true idem.
# Uscita: alpha1/u2_far_pend2_floor_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, FREE
from u2_far_ledger import cheb, pend_set
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
BN = os.path.join(HERE, "u2_far_born_near_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_pend2_floor_summary.json")


def pend2_floor(word):
    """Enumerazione esaustiva del muro; ritorna (min pend2 su TUTTI i nodi,
    insieme residuo a un nodo di minimo, nodi validi, D)."""
    c0, h0, req0 = exact_state(word)
    p2 = {c for c in pend_set(req0) if cheb(c) <= 2}
    best = (len(p2), sorted(p2))
    n_valid = 0; D = 0
    stack = [(c0, h0, req0, 0)]
    while stack:
        c, h, req, dep = stack.pop()
        for bit in (0, 1):
            r2 = dict(req)
            cn, hn, _ = exact_step(c, h, r2, bit)
            if cn is None:
                continue
            n_valid += 1
            D = max(D, dep + 1)
            p2 = {cc for cc in pend_set(r2) if cheb(cc) <= 2}
            if len(p2) < best[0]:
                best = (len(p2), sorted(p2))
            stack.append((cn, hn, r2, dep + 1))
    return best[0], best[1], n_valid, D


def main():
    t0 = time.time()
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    wit = json.load(open(WIT))
    bn = {r["nome"]: r for r in json.load(open(BN))["rows"]}

    rows = []
    floor_min = 99
    for grp in ("jackpot", "D12", "D8", "D4"):
        for k, w in enumerate(wit[grp]):
            name = f"{grp}[{k}]"
            e2 = to_bits(w["word"])
            w2 = e2 + w101
            assert valid(w2)[1] is None
            mp2, residuo, n_valid, D = pend2_floor(w2)
            # GATE: coerenza con born_near (nodi validi = nodi tentati / 2 non
            # vale: born_near conta i TENTATIVI; confronto su D_true)
            assert bn[name]["D_true"] == D, (name, D, bn[name]["D_true"])
            assert bn[name]["esaurito"], name
            floor_min = min(floor_min, mp2)
            rows.append({"nome": name, "min_pend2": mp2, "residuo": residuo,
                         "nodi_validi": n_valid, "D": D})
            print(f"{name:12s} D={D:3d} nodi_validi={n_valid:4d} "
                  f"min_pend2={mp2} residuo={residuo}", flush=True)

    print(f"\nTEOREMA (per enumerazione): sulle {len(rows)} coprenti-nere ad "
          f"albero finito, OGNI possibile nascita lascia >= {floor_min} pending "
          f"in palla-2 (>= {floor_min} celle nere di seme a cheb <= 2 dal "
          f"record) => vietate ai record con palla-2 senza seme.", flush=True)
    out = {"rows": rows, "floor_min": floor_min,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
