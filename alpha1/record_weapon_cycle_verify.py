# record_weapon_cycle_verify.py — §88: FALSIFICAZIONE del certificato di ciclo.
#
# Il certificato geometrico (record_weapon_cycle.py) e' un'induzione: verifica finita
# m <= M_cert=14 + argomento di traslazione => validita' per OGNI m. Qui si attacca:
#   1. verifica DIRETTA in simulazione di sigma^m + tau + w101 per m = 15..--mmax
#      (ben oltre M_cert): eval_word deve dare non-None; riportiamo burden1/onset/residuo;
#   2. catena lettera-per-lettera fino a m = --mchain (ogni singolo prefisso valido);
#   3. check di traslazione esplicito: footprint anchor di m+1 vs m — le celle nuove
#      devono essere il blocco piu' vecchio traslato di -delta_anchor.
# Un solo rosso = certificato ritirato. Uscita: record_weapon_cycle_verify_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import Evaluator, chain_valid, to_bits, to_str, SUMMARY
from kwindow_spoiler_census import virtual_walk, to_anchor_frame

HERE = os.path.dirname(os.path.abspath(__file__))
CYC = os.path.join(HERE, "record_weapon_cycle_summary.json")
RAIL = os.path.join(HERE, "record_weapon_rail_summary.json")
OUT = os.path.join(HERE, "record_weapon_cycle_verify_summary.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mmax", type=int, default=40)
    ap.add_argument("--mchain", type=int, default=20)
    args = ap.parse_args()
    t0 = time.time()
    ev = Evaluator()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cyc = json.load(open(CYC))
    cert = cyc["certificato"]
    assert cert and cert.get("certificato"), "nessun certificato da verificare"
    rail = json.load(open(RAIL))["rail_oldest_first"]
    i2 = cyc["finestra"][1]
    j = cert["j"]
    sigma = to_bits(cert["sigma"])
    tau = to_bits(rail[i2 - j:])
    base2 = tau + w101
    m_cert = cert["m_cert"]
    da = tuple(cert["delta_anchor"])
    print(f"sigma={cert['sigma']} tau={len(tau)} lettere, M_cert={m_cert}, "
          f"delta_anchor={da}; verifica diretta m={m_cert+1}..{args.mmax}", flush=True)

    # 1. verifica diretta oltre M_cert
    rows = []
    for m in range(m_cert + 1, args.mmax + 1):
        w = sigma * m + base2
        r = ev(w)
        assert r is not None, f"ROSSO: sigma^{m}+tau+w101 NON valida (m>{m_cert})!"
        rows.append({"m": m, "K": len(w), "burden1": r[0], "onset": r[1],
                     "residuo": [list(c) for c in r[3]]})
    b1s = sorted({row["burden1"] for row in rows})
    res = sorted({tuple(map(tuple, row["residuo"])) for row in rows})
    print(f"1. VERDE: m={m_cert+1}..{args.mmax} tutte valide; burden1 in {b1s}; "
          f"residui {[[list(c) for c in r] for r in res]}", flush=True)

    # 2. catena lettera-per-lettera fino a mchain
    assert chain_valid(ev, sigma * args.mchain, base2), "ROSSO: catena lettera-per-lettera!"
    print(f"2. VERDE: catena lettera-per-lettera valida fino a m={args.mchain} "
          f"(K={8*args.mchain+len(base2)})", flush=True)

    # 3. traslazione esplicita del footprint anchor
    ok3 = 0
    for m in (2, 5, 9, 14, 20):
        g1, p1 = virtual_walk(sigma * m + base2)
        g2, p2 = virtual_walk(sigma * (m + 1) + base2)
        a1 = to_anchor_frame(g1, p1)
        a2 = to_anchor_frame(g2, p2)
        assert set(a1) <= set(a2), f"ROSSO m={m}: anchor(m) non contenuto in anchor(m+1)"
        assert all(a2[c] == a1[c] for c in a1), f"ROSSO m={m}: colori cambiati!"
        new = set(a2) - set(a1)
        oldest_prev = {c for c in a1 if c not in
                       to_anchor_frame(*virtual_walk(sigma * (m - 1) + base2))} if m > 1 else None
        shifted = {(c[0] - da[0], c[1] - da[1]) for c in oldest_prev}
        assert new == shifted, f"ROSSO m={m}: nuove celle != blocco precedente traslato"
        assert all(a2[c] == a1[(c[0] + da[0], c[1] + da[1])] for c in new), \
            f"ROSSO m={m}: colori del blocco traslato non corrispondono"
        ok3 += 1
    print(f"3. VERDE: traslazione esplicita del footprint verificata su {ok3} coppie "
          f"(m=2,5,9,14,20)", flush=True)

    out = {"mmax": args.mmax, "mchain": args.mchain, "direct": rows,
           "translation_pairs_ok": ok3, "eval_calls": ev.calls,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"TUTTO VERDE — certificato sopravvissuto alla falsificazione. "
          f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
