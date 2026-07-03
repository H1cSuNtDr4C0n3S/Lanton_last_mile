# record_weapon_cycle.py — §88 (chiusura): CERTIFICATO DI CICLO sul binario dietro w101.
#
# Il binario (record_weapon_rail.py) mostra un regime interno periodico (blocchi ~RLLRLLLL)
# ma lo scan "eventuale" fallisce perche' le lettere PIU' VECCHIE del testimone DFS possono
# deviare dal regime (sono le meno vincolate: qualsiasi continuazione valida chiude il target).
# Qui: (1) trovo il periodo p e la finestra interna [i1,i2) di massima persistenza
# sull'autocorrelazione del binario; (2) per ogni allineamento j = 0..p-1 costruisco
#   base2 = tau_j + w101   (tau_j = lettere recenti del binario, dal bordo della finestra)
#   sigma_j = blocco di p lettere subito prima di tau_j
# e tento il certificato geometrico certify_cycle(sigma_j, base2): se verde per UN j,
# D(w101) = infinito (realizzabilita' + record-compatibilita' per ogni m; onset empirico
# fino a M_cert, dichiarato). Uscita: alpha1/record_weapon_cycle_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import (Evaluator, chain_valid, certify_cycle,
                                    to_bits, to_str, SUMMARY)

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = os.path.join(HERE, "record_weapon_rail_summary.json")
OUT = os.path.join(HERE, "record_weapon_cycle_summary.json")


def best_periodic_window(s, pmax):
    """(p, i1, i2): periodo e finestra [i1,i2) massima con s[i]==s[i+p] su tutta la finestra."""
    best = (0, 0, 0)
    n = len(s)
    for p in range(1, pmax + 1):
        i = 0
        while i < n - p:
            if s[i] == s[i + p]:
                j = i
                while j < n - p and s[j] == s[j + p]:
                    j += 1
                if j - i > best[2] - best[1]:
                    best = (p, i, j)
                i = j + 1
            else:
                i += 1
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmax", type=int, default=60)
    args = ap.parse_args()
    t0 = time.time()
    ev = Evaluator()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    rail = json.load(open(RAIL))["rail_oldest_first"]
    n = len(rail)

    p, i1, i2 = best_periodic_window(rail, args.pmax)
    span = i2 - i1
    print(f"finestra periodica massima sul binario ({n} lettere): periodo {p}, "
          f"[{i1},{i2}) = {span} lettere = {span/p:.1f} periodi", flush=True)
    assert span >= 3 * p, "finestra troppo corta per tentare un ciclo (metodo §84)"
    print(f"blocco: {rail[i1:i1+p]} (regime: profondita' {n-i2}..{n-i1} dal recente)",
          flush=True)

    # allineamenti: tau parte dal bordo recente della finestra, con slack di j lettere
    results = []
    found = None
    for j in range(p):
        cut = i2 - j                    # rail[cut:] = tau_j (parte recente tenuta come base)
        if cut - p < i1:
            break
        tau = to_bits(rail[cut:])
        sigma = to_bits(rail[cut - p:cut])
        base2 = tau + w101
        r = ev(base2)
        if r is None:
            results.append({"j": j, "esito": "base2 non valida (inatteso)"})
            continue
        c = certify_cycle(ev, sigma, base2)
        c["j"] = j
        c["tau_len"] = len(tau)
        results.append(c)
        print(f"  j={j}: sigma={c.get('sigma')} -> {c.get('esito')}", flush=True)
        if c.get("certificato"):
            found = c
            break

    if found:
        base2 = to_bits(rail[i2 - found['j']:]) + w101
        bprof = found.get("burden_per_periodo")
        print(f"\nD(w101) = INFINITO (certificato geometrico): sigma={found['sigma']}, "
              f"q={found['q']}, delta_walk={found['delta_walk']}, "
              f"delta_anchor={found['delta_anchor']}, g_max={found['g_max']}, "
              f"M_cert={found['m_cert']}, tau={found['tau_len']} lettere, "
              f"burden per periodo={bprof}", flush=True)
    else:
        print("\nNESSUN certificato su questa finestra (vedere esiti sopra)", flush=True)

    out = {"pmax": args.pmax, "periodo": p, "finestra": [i1, i2], "span": span,
           "blocco": rail[i1:i1 + p], "tentativi": results, "certificato": found,
           "eval_calls": ev.calls, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s ({ev.calls} eval)", flush=True)


if __name__ == "__main__":
    main()
