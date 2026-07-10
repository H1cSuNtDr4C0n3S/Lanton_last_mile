# danger_sigma_vocab_agg.py — §107c P2: aggregatore dello scan sigma_D.
#
# Legge alpha1/sigma_vocab_shard*.jsonl (dedup per parola), verifica la
# copertura contro il censimento F0, e riporta:
#   - quota di parole DEDUTTIVAMENTE SICURE (sigma=1 esatto, cap>0, non
#     troncate): rigetto garantito a ogni record che le presenti, a
#     profondita' dichiarata D=22 (fatto esatto per-parola, nessuna soglia).
#   - distribuzione di sigma per bande di |R_T| (la classe <=50 vs il resto).
#   - cross-check di regressione: le 66 parole della classe <=50 devono
#     riprodurre i numeri dello scan §107b (stessa macchina, stesso D).
#   - parole NON-DEFINITE (troncate, trappola mm) contate a parte, mai
#     mescolate alle misurate.
import sys, os, json, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


def main():
    census = json.load(open(os.path.join(
        HERE, "danger_geometry_census.json")))["per_word"]
    ref = json.load(open(os.path.join(
        HERE, "danger_backward_autopsy_summary.json")))
    rows = {}
    for fp in glob.glob(os.path.join(HERE, "sigma_vocab_shard*.jsonl")):
        with open(fp, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                rows.setdefault(r["word"], r)
    missing = [w for w in census if w not in rows]
    extra = [w for w in rows if w not in census]
    print(f"parole: censimento {len(census)}, misurate {len(rows)}, "
          f"mancanti {len(missing)}, extra {len(extra)}")
    assert not missing and not extra, "copertura incompleta"
    errs = [r for r in rows.values() if "errore" in r]
    nondef = [r for r in rows.values()
              if r.get("non_definito") and "errore" not in r]
    good = [r for r in rows.values()
            if not r.get("non_definito") and "errore" not in r]
    print(f"misurate esatte {len(good)}, NON-DEFINITE (troncate) "
          f"{len(nondef)}, errori {len(errs)}")
    for r in errs[:5]:
        print(f"  ERR {r['word'][:20]}...: {r['errore']}")

    # cross-check regressione vs scan §107b (classe <=50, D=22)
    ref_scan = {s["word"]: s for s in ref["scan_danger"]}
    mism = 0
    for ws, s in ref_scan.items():
        r = rows.get(ws)
        if r is None or r.get("non_definito"):
            mism += 1
            continue
        if (r["cap"] != s["cap"] or
                abs(r["sigma"] - s["sigma"]) > 5e-5 or
                r["celle_irraggiungibili"] != s["celle_irraggiungibili"]):
            mism += 1
            print(f"  MISMATCH §107b {ws[:20]}...: cap {r['cap']} vs "
                  f"{s['cap']}, sigma {r['sigma']} vs {s['sigma']}")
    print(f"regressione vs scan §107b: {len(ref_scan) - mism}/{len(ref_scan)} "
          f"riprodotte{' — FALLITA' if mism else ' — OK'}")
    assert mism == 0

    bands = [(0, 15, "<=15"), (16, 50, "16-50"), (51, 100, "51-100"),
             (101, 300, "101-300"), (301, 10 ** 9, "301+")]
    print("\nbanda |R_T| | n | sigma=1 esatto | sigma<=0.01 | sigma med | "
          "cap med | irr>0")
    out_bands = []
    for lo, hi, lab in bands:
        sel = [r for r in good if lo <= r["n_rt"] <= hi]
        if not sel:
            continue
        n1 = sum(1 for r in sel if r["sigma_uno_esatto"])
        n0 = sum(1 for r in sel if r["sigma"] <= 0.01)
        nirr = sum(1 for r in sel if r["celle_irraggiungibili"] > 0)
        row = {"banda": lab, "n": len(sel), "sigma1_esatto": n1,
               "sigma_le_001": n0,
               "sigma_med": med([r["sigma"] for r in sel]),
               "cap_med": med([r["cap"] for r in sel]),
               "irr_gt0": nirr}
        out_bands.append(row)
        print(f"{lab:>8} | {len(sel):4d} | {n1:4d} ({n1 / len(sel):.3f}) | "
              f"{n0:4d} ({n0 / len(sel):.3f}) | {row['sigma_med']:.4f} | "
              f"{row['cap_med']:8d} | {nirr}")
    tot1 = sum(1 for r in good if r["sigma_uno_esatto"])
    tot0 = sum(1 for r in good if r["sigma"] <= 0.01)
    print(f"\nTOTALE vocabolario: {len(good)} esatte — sigma=1 esatto "
          f"{tot1} ({tot1 / len(good):.3f}), sigma<=0.01 {tot0} "
          f"({tot0 / len(good):.3f}), sigma med "
          f"{med([r['sigma'] for r in good]):.4f}")
    out = {"n_censimento": len(census), "n_misurate_esatte": len(good),
           "n_non_definite": len(nondef), "n_errori": len(errs),
           "regressione_107b_ok": mism == 0,
           "sigma1_esatto_tot": tot1, "sigma_le_001_tot": tot0,
           "bande": out_bands, "depth": 22,
           "convenzione": "sigma=1 esatto = rigetto garantito a ogni record "
                          "che presenta la parola, a profondita' D=22 "
                          "dichiarata; og dal record (asse assoluto og+101)",
           "non_definite": [r["word"] for r in nondef],
           "errori": [{"word": r["word"], "errore": r["errore"]}
                      for r in errs]}
    op = os.path.join(HERE, "sigma_vocab_summary.json")
    with open(op, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {op}")


if __name__ == "__main__":
    main()
