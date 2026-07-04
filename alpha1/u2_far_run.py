# u2_far_run.py — §93 (U2-LONTANO): la CORSA INVERSA FORZATA sulle coprenti-nere.
#
# Per ogni coprente-nera reale (testimoni u2_cover_witnesses.json + censimento
# §90c colore B) corre la corsa deterministica fresco=>R (u2_far_ledger.forced_run)
# sopra coprente+w101 e misura, per palle-R centrate sul record (R in RADII):
#   - passo della prima uscita dalla palla e pending IN-PALLA aperti a quel passo;
#   - morte (sempre y<1 o step_cap) e pending totali a fine corsa;
#   - le CELLE pending in-palla lasciate aperte: intersezione e unione tra coprenti
#     (i pending BLOCCATI universali = la parte w101-specifica per il certificato).
#
# LETTURA (senza sovra-interpretare, trappola bb): la corsa forzata e' UN solo
# cammino (zero L-su-fresco); i suoi pending aperti NON dimostrano che ogni corsa
# li lascia aperti — quello e' il lavoro della caccia (u2_far_closure_hunt.py).
# Qui si quantifica: quanto chiude la corsa a costo zero, e cosa resta.
#
# Uscita: alpha1/u2_far_run_summary.json
import sys, os, json, time, argparse
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import anchor_trace, TGT
from u2_far_ledger import forced_run, cheb

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, "record_cover_census_summary.json")
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
OUT_JSON = os.path.join(HERE, "u2_far_run_summary.json")
RADII = (8, 12, 16, 24, 32)


def collect_black_covers(w101):
    """(nome, word_ext) per ogni coprente-nera disponibile, dedup per parola."""
    out = []
    seen = set()
    wit = json.load(open(WIT))
    for grp in ("jackpot", "D12", "D8", "D4", "nere400"):
        for k, w in enumerate(wit[grp]):
            e2 = to_bits(w["word"])
            if e2 in seen:
                continue
            seen.add(e2)
            out.append((f"{grp}[{k}]", e2))
    cc = json.load(open(CC))
    for r in cc["rows"]:
        if r["colore_11"] != "B":
            continue
        e2 = to_bits(r["word_ext"])
        if e2 in seen:
            continue
        seen.add(e2)
        out.append((f"cc90c_prof{r['depth']}", e2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step-cap", type=int, default=100_000)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    covers = collect_black_covers(w101)
    print(f"coprenti-nere raccolte: {len(covers)}", flush=True)

    rows = []
    stuck_union = {R: set() for R in RADII}
    stuck_inter = {R: None for R in RADII}
    for name, e2 in covers:
        w2 = e2 + w101
        assert valid(w2)[1] is None, name
        # gate di forma: coprente vera (unica visita a (1,1) = passo piu' antico)
        tr = anchor_trace(w2)
        assert tr[0][0] == TGT and TGT not in tr[0][1:], name
        assert e2[0] == 1, name + ": non e' nera (primo bit != R)"
        r = forced_run(w2, step_cap=args.step_cap, ball_radii=RADII)
        row = {"nome": name, "prof": len(e2), "pend0": r["pend0"],
               "passi": r["passi"], "causa": r["causa"],
               "L_riv": r["L_riv"], "pend_fine": r["pend_fine"],
               "y_max": r["y_max"], "cheb_max": r["cheb_max"], "balls": {}}
        for R in RADII:
            b = r["balls"][R]
            if b is None:
                # mai uscita dalla palla-R: pending in-palla = pending a morte
                row["balls"][str(R)] = {"esce": False}
            else:
                row["balls"][str(R)] = {"esce": True, "passo": b["passo"],
                                        "pend_in_palla": b["pend_in_palla"]}
                cells = set(map(tuple, b["celle"]))
                stuck_union[R] |= cells
                stuck_inter[R] = cells if stuck_inter[R] is None \
                    else (stuck_inter[R] & cells)
        rows.append(row)
        bstr = " ".join(
            f"R{R}:{row['balls'][str(R)].get('pend_in_palla','-')}"
            f"@{row['balls'][str(R)].get('passo','-')}" for R in RADII)
        print(f"{name:18s} prof{len(e2):4d} pend0={r['pend0']:3d} "
              f"passi={r['passi']:6d} causa={r['causa']:8s} "
              f"L_riv={r['L_riv']:5d} pend_fine={r['pend_fine']:4d} "
              f"ymax={r['y_max']:3d} | {bstr}", flush=True)

    print("\n---- sintesi pending in-palla alla prima uscita ----", flush=True)
    sintesi = {}
    for R in RADII:
        esce = [row for row in rows if row["balls"][str(R)]["esce"]]
        pends = [row["balls"][str(R)]["pend_in_palla"] for row in esce]
        inter = sorted(stuck_inter[R]) if stuck_inter[R] else []
        sintesi[str(R)] = {
            "coprenti_che_escono": len(esce), "su": len(rows),
            "pend_min": min(pends) if pends else None,
            "pend_max": max(pends) if pends else None,
            "celle_unione": len(stuck_union[R]),
            "celle_intersezione": len(inter),
            "intersezione": [list(c) for c in inter]}
        print(f"R={R}: escono {len(esce)}/{len(rows)}; pending in-palla "
              f"min/max {min(pends) if pends else '-'}"
              f"/{max(pends) if pends else '-'}; unione celle "
              f"{len(stuck_union[R])}, INTERSEZIONE {len(inter)}: {inter}",
              flush=True)

    out = {"args": vars(args), "n_coprenti": len(covers), "radii": list(RADII),
           "rows": rows, "sintesi": sintesi,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
