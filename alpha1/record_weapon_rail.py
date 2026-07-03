# record_weapon_rail.py — §88 (seguito): il BINARIO FORZATO dietro w101.
#
# La vitalita' (record_weapon_vitality.py) ha mostrato che il muro dei prepend sopra w101
# ha UN SOLO sopravvissuto per livello da prof. 2 in poi (esaustivo fino a 14): il passato
# record-compatibile di w101 e' un binario unico. Questo script:
#   1. estende il binario in profondita' (DFS early-exit, target --target, default 416)
#      e registra il profilo burden1 lungo il binario;
#   2. ri-verifica l'UNICITA' in esaustivo fino a --uniq-depth (default 30);
#   3. cerca la periodicita' EVENTUALE dei prepend (nell'ordine di prepend = dal piu'
#      recente al piu' vecchio): esiste (t, p) con rev[i] = rev[i+p] per ogni i >= t?
#   4. se esiste, tenta il certificato geometrico di ciclo (certify_cycle) con
#      sigma = blocco periodico allineato e base = transiente + w101:
#      se verde, D(w101) = INFINITO certificato (realizzabilita' + record-compat).
#
# Uscita: alpha1/record_weapon_rail_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import (Evaluator, chain_dfs, enumerate_wall, chain_valid,
                                    certify_cycle, to_bits, to_str, SUMMARY)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "record_weapon_rail_summary.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=416)     # 4 periodi di prepend
    ap.add_argument("--uniq-depth", type=int, default=30)
    ap.add_argument("--max-period", type=int, default=120)
    ap.add_argument("--max-transient", type=int, default=120)
    ap.add_argument("--nodes", type=int, default=2_000_000)
    ap.add_argument("--budget-s", type=int, default=1800)
    args = ap.parse_args()
    t0 = time.time()
    ev = Evaluator()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    r = ev(w101)
    assert r is not None and r[0] == 1 and r[3] == [(1, 1)], "GATE w101 fallito"

    # 1. binario profondo
    wit, nodes = chain_dfs(ev, w101, args.target, args.nodes, t0, args.budget_s)
    depth = args.target if wit is not None else None
    if wit is None:
        # scendi a bisezione per trovare la profondita' massima raggiungibile nel budget
        lo, hi = 0, args.target
        while lo < hi:
            mid = (lo + hi + 1) // 2
            w, _ = chain_dfs(ev, w101, mid, args.nodes, t0, args.budget_s)
            if w is not None:
                lo = mid; wit = w
            else:
                hi = mid - 1
        depth = lo
    ext = tuple(wit)                               # dal piu' vecchio al piu' recente
    assert chain_valid(ev, ext, w101), "testimone non valido al ricontrollo!"
    prof = [ev(ext[j:] + w101)[0] for j in range(len(ext) - 1, -1, -1)]
    cells_last = ev(ext + w101)[3]
    print(f"binario: profondita' {depth} ({nodes} nodi), burden lungo il binario "
          f"min {min(prof)} max {max(prof)}, residuo in fondo {cells_last}", flush=True)
    rail = to_str(ext)
    print(f"binario (dal piu' vecchio): {rail}", flush=True)

    # 2. unicita' esaustiva fino a uniq-depth
    levels, counts, trunc = enumerate_wall(ev, w101, args.uniq_depth, 10000, t0,
                                           args.budget_s)
    cnts = [counts[k] for k in sorted(counts)]
    uniq_from = 1 if all(c == 1 for c in cnts[1:]) else None
    print(f"unicita' esaustiva fino a prof. {max(counts)}: {cnts} "
          f"{'(binario unico da prof. 2)' if cnts[1:] and all(c == 1 for c in cnts[1:]) else ''}",
          flush=True)

    # 3. periodicita' eventuale nell'ordine di prepend (dal recente al vecchio)
    rev = rail[::-1]
    found = None
    for p in range(1, min(args.max_period, len(rev) // 3) + 1):
        for t in range(0, min(args.max_transient, len(rev) - 3 * p) + 1):
            if all(rev[i] == rev[i + p] for i in range(t, len(rev) - p)):
                found = (p, t)
                break
        if found:
            break
    resper = {"periodo": None, "transiente": None}
    cert = None
    if found:
        p, t = found
        resper = {"periodo": p, "transiente": t,
                  "copertura": len(rev) - t, "periodi_osservati": (len(rev) - t) / p}
        print(f"PERIODICITA' EVENTUALE: periodo {p}, transiente {t} "
              f"({resper['periodi_osservati']:.1f} periodi osservati)", flush=True)
        # 4. certificato: sigma = blocco periodico, base = transiente + w101
        #    rev = rail rovesciato: transiente = ultime t lettere di rail (le piu' recenti)
        base2 = (to_bits(rail[len(rail) - t:]) + w101) if t > 0 else w101
        sigma_rev = rev[t:t + p]                   # blocco nell'ordine recente->vecchio
        sigma = to_bits(sigma_rev[::-1])           # in ordine di parola (vecchio->recente)
        assert chain_valid(ev, sigma + (() if t == 0 else to_bits(rail[len(rail)-t:])), w101)
        cert = certify_cycle(ev, sigma, base2)
        print(f"certificato ciclo su base transiente+w101: {cert.get('esito')}", flush=True)
        if cert.get("certificato"):
            print(f"  => D(w101) = INFINITO certificato: sigma={cert['sigma']} "
                  f"q={cert['q']} delta_anchor={cert['delta_anchor']} "
                  f"M_cert={cert['m_cert']} burden/periodo={cert['burden_per_periodo']}",
                  flush=True)
    else:
        print(f"NESSUNA periodicita' eventuale (p<={args.max_period}, "
              f"transiente<={args.max_transient}) sul binario di {len(rail)}", flush=True)

    out = {"args": vars(args), "depth": depth, "nodes": nodes,
           "burden_min": min(prof), "burden_max": max(prof),
           "burden_profile_changes": [[i + 1, b] for i, b in enumerate(prof)
                                      if i == 0 or prof[i - 1] != b],
           "residuo_fondo": [list(c) for c in cells_last],
           "rail_oldest_first": rail,
           "uniqueness_counts": cnts, "uniqueness_truncated": trunc,
           "periodicita": resper, "certificato_ciclo": cert,
           "eval_calls": ev.calls, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s ({ev.calls} eval)", flush=True)


if __name__ == "__main__":
    main()
