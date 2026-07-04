# u2_far_core_block.py — §93 (U2-LONTANO): il NUCLEO BLOCCATO {(-1,1),(0,1)}.
#
# La caccia §93 (u2_far_closure_hunt) trova che a R=2 TUTTI gli 8 fuggenti+jackpot
# si fermano con ESATTAMENTE 2 pending aperti: (-1,1) e (0,1) — le celle della
# scia d'arrivo di w101 (§86), adiacenti, in riga y=1 contro il muro dei record.
# Qui la sonda mirata, per ogni coprente fuggente/jackpot:
#   A. caccia alla RIVISITA di (0,1): DFS con steering e budget largo, goal =
#      visitare la cella (qualunque visita CHIUDE il pending: req(0,1) alla
#      copertura e' bianco-forzato);
#   B. idem per (-1,1);
#   C. caccia alla PULIZIA CONGIUNTA: goal = pending(-1,1) e pending(0,1)
#      entrambi chiusi nello stesso istante (e' il minimo mai visto = 2);
#   D. enumerazione ESAUSTIVA in-box (celle dell'estensione tutte con cheb <= B):
#      se esaurita con zero visite al nucleo, ogni rivisita deve prima USCIRE
#      dal box-B (eta'/detour bound alla Blocco Antico §89d).
# Uscita: alpha1/u2_far_core_block_summary.json
import sys, os, json, time, random, argparse, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, anchor_trace, FREE
from u2_far_ledger import cheb, pend_set
from u2_far_closure_hunt import Walker, bounded_dfs, _below_normal, collect_targets
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "u2_far_core_block_summary.json")
CORE = ((-1, 1), (0, 1))


def probe_job(job):
    (name, w2_str, goal_kind, seed, n_restarts, node_budget) = job
    _below_normal()
    rng = random.Random(seed)
    w2 = to_bits(w2_str)
    c0, h0, req0 = exact_state(w2)
    pend0 = pend_set(req0)
    R = 2                                   # ledger in palla-2 (il nucleo)
    pend0_in = {c for c in pend0 if cheb(c) <= R}

    if goal_kind == "visita_01":
        goal = lambda wk: wk.c == (0, 1)
    elif goal_kind == "visita_m11":
        goal = lambda wk: wk.c == (-1, 1)
    else:                                   # congiunta
        goal = lambda wk: ((-1, 1) not in wk.pend_in
                           and (0, 1) not in wk.pend_in)

    res = {"nome": name, "goal": goal_kind, "trovato": None,
           "verdetti": {"goal": 0, "exhausted": 0, "budget": 0}, "nodi": 0}
    for rs in range(n_restarts):
        w = Walker(c0, h0, req0, pend0_in, R)
        # steering verso il nucleo: sostituisci pend_in con il target per il
        # calcolo della distanza (bounded_dfs steera verso pend_in)
        verdict, nodes = bounded_dfs(w, goal, rng,
                                     rng.choice((0.4, 0.7, 0.9)),
                                     node_budget)
        res["nodi"] += nodes
        res["verdetti"][verdict] += 1
        if verdict == "goal":
            res["trovato"] = {"prof": len(w.bits),
                              "ext_bits": to_str(tuple(reversed(w.bits))),
                              "pend_in_al_goal": sorted(w.pend_in)}
            return res
    return res


def box_exhaustive(w2, B, targets, node_cap=50_000_000, depth_cap=100_000):
    """Enumerazione esaustiva del sottoalbero le cui celle stanno TUTTE nel
    box cheb <= B. Uscita dal box = foglia potata (contata). Ritorna
    (esaurito?, nodi, visite ai target, uscite, profondita' max)."""
    from u2_pocket_certificate import exact_step
    c0, h0, req0 = exact_state(w2)
    nodes = 0; visits = {t: 0 for t in targets}; exits = 0; maxdep = 0
    stack = [(c0, h0, req0, 0)]
    while stack:
        if nodes >= node_cap:
            return False, nodes, visits, exits, maxdep
        c, h, req, dep = stack.pop()
        if dep >= depth_cap:
            return False, nodes, visits, exits, maxdep
        for bit in (0, 1):
            nodes += 1
            r2 = dict(req)
            cn, hn, _ = exact_step(c, h, r2, bit)
            if cn is None:
                continue
            if cheb(cn) > B:
                exits += 1
                continue                    # potato: esce dal box
            if cn in visits:
                visits[cn] += 1
            maxdep = max(maxdep, dep + 1)
            stack.append((cn, hn, r2, dep + 1))
    return True, nodes, visits, exits, maxdep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--node-budget", type=int, default=4_000_000)
    ap.add_argument("--restarts", type=int, default=6)
    ap.add_argument("--boxes", type=int, nargs="+", default=[6, 8, 10])
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--seed", type=int, default=931)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    targets = [(n, w, k) for (n, w, k) in collect_targets() if k == "fuga"]

    # diagnostica: chi legge il nucleo in coprente+w101, e a che profondita'?
    diag = {}
    for name, wstr, _ in targets:
        w2 = to_bits(wstr) + w101
        tr = anchor_trace(w2)
        pos = tr[0]
        info = {}
        for t in CORE:
            idxs = [i for i, p in enumerate(pos) if p == t]
            # indice 0 = passo piu' antico; parola = ext(prof) + w101(101)
            info[str(t)] = {"prima_visita_idx": idxs[0] if idxs else None,
                            "visite_in_parola": len(idxs),
                            "prima_lettura": tr[2].get(t)}
        diag[name] = info
    print("diagnostica nucleo (prima visita = indice dal passo piu' antico):",
          flush=True)
    for name, info in diag.items():
        print(f"  {name}: {info}", flush=True)

    jobs = []
    jid = 0
    for name, wstr, _ in targets:
        w2 = to_bits(wstr) + w101
        assert valid(w2)[1] is None
        for gk in ("visita_01", "visita_m11", "congiunta"):
            jobs.append((name, to_str(w2), gk, args.seed * 7919 + jid,
                         args.restarts, args.node_budget))
            jid += 1
    print(f"\n{len(jobs)} job mirati ({args.restarts} DFS x "
          f"{args.node_budget} nodi)", flush=True)

    rows = []
    with mp.Pool(args.workers, initializer=_below_normal) as pool:
        for res in pool.imap(probe_job, jobs, chunksize=1):
            rows.append(res)
            got = res["trovato"]
            print(f"{res['nome']:12s} {res['goal']:10s}: "
                  f"{'TROVATO prof ' + str(got['prof']) if got else 'niente'} "
                  f"({res['nodi']} nodi, verdetti {res['verdetti']})",
                  flush=True)

    # D. enumerazione esaustiva in-box
    box_rows = []
    for name, wstr, _ in targets:
        w2 = to_bits(wstr) + w101
        for B in args.boxes:
            exh, nodes, visits, exits, maxdep = box_exhaustive(w2, B, CORE)
            box_rows.append({"nome": name, "B": B, "esaurito": exh,
                             "nodi": nodes, "visite_core":
                             {str(k): v for k, v in visits.items()},
                             "uscite": exits, "prof_max": maxdep})
            print(f"box {name:12s} B={B:2d}: "
                  f"{'ESAURITO' if exh else 'CAP'} nodi={nodes} "
                  f"visite core={visits} uscite={exits} prof_max={maxdep}",
                  flush=True)

    out = {"args": vars(args), "diagnostica": diag, "rows": rows,
           "box": box_rows, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
