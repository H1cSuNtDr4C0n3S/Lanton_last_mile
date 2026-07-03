# record_cover_census.py — §90c: censimento delle estensioni che COPRONO (1,1).
#
# La dicotomia §89d si e' biforcata (§90b): un passato di w101 che visita (1,1) o la
# lascia BIANCA (=> parola-arma, burden1=0, ingresso incondizionato: trovata, K=158,
# ma VACUA con D=0) o la lascia NERA (=> il verdetto passa alla parola estesa con
# (1,1) nel footprint). Qui si censiscono MOLTE estensioni coprenti (best-first guidato,
# campione non esaustivo — dichiarato) e per ciascuna si misura:
#   - colore lasciato su (1,1); burden1/onset/residuo della parola estesa (eval_word);
#   - VITALITA': profondita' massima di catena di prepend sopra la parola estesa
#     (early-exit fino a --viab-target; 0 = morta subito, come l'arma).
# Ipotesi da attaccare: TUTTE le coprenti sono backward-morte (=> record-w101 tardivi
# impossibili per orbite a storia lunga, vietanza un-livello-su).
# Uscita: alpha1/record_cover_census_summary.json
import sys, os, json, time, heapq, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_target_hunt import tail_state, TGT
from record_weapon_vitality import Evaluator, chain_dfs, to_bits, SUMMARY
from kwindow_spoiler_census import virtual_walk, to_anchor_frame

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "record_cover_census_summary.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hits", type=int, default=60)
    ap.add_argument("--nodes", type=int, default=2_000_000)
    ap.add_argument("--budget-s", type=int, default=1200)
    ap.add_argument("--viab-target", type=int, default=12)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])

    def cheb(c):
        return max(abs(c[0] - TGT[0]), abs(c[1] - TGT[1]))

    # best-first come §90b ma raccoglie fino a --hits coprenti; i rami coprenti non
    # vengono riespansi (interessa la PRIMA visita all'indietro = ultima visita reale)
    ok, tail0, hit0 = tail_state(w101)
    assert ok and not hit0
    heap = [(cheb(tail0), 0, ())]
    seen = 0
    hits = []
    while heap and seen < args.nodes and len(hits) < args.hits \
            and time.time() - t0 < args.budget_s:
        pri, dep, ext = heapq.heappop(heap)
        if dep >= 200:
            continue
        for bit in (0, 1):
            e2 = (bit,) + ext
            seen += 1
            ok, tail, hit = tail_state(e2 + w101)
            if not ok:
                continue
            if hit:
                hits.append(e2)
                continue
            heapq.heappush(heap, (cheb(tail), dep + 1, e2))
    print(f"raccolte {len(hits)} estensioni coprenti in {seen} nodi "
          f"({time.time()-t0:.0f}s); profondita' {sorted(set(len(h) for h in hits))}",
          flush=True)

    ev = Evaluator()
    rows = []
    n_white = n_black = 0
    viab_hist = {}
    for e2 in hits:
        w2 = e2 + w101
        anchor = to_anchor_frame(*virtual_walk(w2))
        col = anchor[TGT]
        if col == 0:
            n_white += 1
        else:
            n_black += 1
        r = ev(w2)
        # vitalita': profondita' massima raggiungibile sopra w2 (bisezione early-exit)
        dmax = 0
        for k in range(1, args.viab_target + 1):
            wit, _ = chain_dfs(ev, w2, k, 200_000, t0, args.budget_s + 600)
            if wit is None:
                break
            dmax = k
        viab_hist[dmax] = viab_hist.get(dmax, 0) + 1
        rows.append({"depth": len(e2), "colore_11": "W" if col == 0 else "B",
                     "eval": (None if r is None else
                              {"burden1": r[0], "onset": r[1],
                               "residuo": [list(c) for c in r[3]] if r[0] <= 8 else r[0]}),
                     "D_sopra": dmax,
                     "word_ext": "".join("R" if b else "L" for b in e2)})
        print(f"  prof.{len(e2):3d} (1,1)={'W' if col==0 else 'B'} "
              f"burden={'None' if r is None else r[0]} D_sopra={dmax}", flush=True)

    alive = [r for r in rows if r["D_sopra"] >= args.viab_target]
    out = {"campione": len(hits), "nodi_esplorati": seen,
           "bianche": n_white, "nere": n_black,
           "viab_hist": {str(k): v for k, v in sorted(viab_hist.items())},
           "vive_al_target": len(alive),
           "rows": rows, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nSINTESI: {len(hits)} coprenti | bianche {n_white} (armi candidate), "
          f"nere {n_black} | D sopra: {out['viab_hist']} | vive a D>={args.viab_target}: "
          f"{len(alive)}", flush=True)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
