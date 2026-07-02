# spoiler_quadrant_profile.py — §87d: geometria direzionale degli SPOILER-SET (verso i
# pose-record B-T).
#
# Fatto B-T (Bunimovich-Troubetzkoy, gia' agli atti come "unboundedness"): un'orbita eterna
# e' illimitata, quindi ha una direzione (WLOG y-min, per C4-simmetria della regola) in cui
# stabilisce infiniti RECORD. Al passo di un record y-min la formica:
#   - arriva muovendo verso l'alto => heading = su (frame anchor allineato al frame assoluto);
#   - sta su una cella MAI visitata (legge bianco, la svolta al record e' R);
#   - il semipiano APERTO davanti {y_rel < 0} e' interamente mai-visitato => BIANCO;
#   - il footprint F(w) degli ultimi K passi giace in {y_rel >= 0} (nessuna cella sotto il
#     record precedente... piu' precisamente sotto il record CORRENTE).
#
# Conseguenza esatta (censimento §87b + Lemma del Cono §87a): al record, il bianco del
# semipiano davanti e' GRATIS; la condizione di onset del germe(w) si riduce a
#   "spoiler_dietro(w) := (V(w) \ F(w)) ∩ {y_rel >= 0} tutto bianco".
# TEOREMA (condizionale al censimento verde): un'orbita eterna non-highway deve avere, a OGNI
# pose-record, almeno un nero di eta' >= K dentro spoiler_dietro(w(t)).
# Se esistesse una parola realizzabile con spoiler_dietro VUOTO, l'orbita eterna non potrebbe
# MAI presentarla a un record — e se la parola fosse inevitabile ai record, Link 1 CADREBBE.
#
# Misure per ogni parola realizzabile (K=12 e K=14):
#   1. |spoiler|, |spoiler ∩ {y<0}| (davanti), |spoiler ∩ {y>=0}| (fardello-dietro);
#   2. conta parole con fardello-dietro == 0 (ARMA: ispezione immediata);
#   3. distribuzione del fardello-dietro minimo e del suo raggio;
#   4. quadranti vuoti: per ciascuno dei 4 quadranti relativi, quante parole hanno spoiler
#      interamente fuori da quel quadrante (finestre libere per attacchi d'angolo, dove ai
#      VERTICI del rettangolo di bounding un intero QUADRANTE e' fresco);
#   5. profondita' del fardello: max y_rel richiesto (quanto "indietro" serve garantire bianco).
#
# SELF-TEST: ri-verifica 3 gate del censimento (parole campione: onset identico a §87b);
# coerenza: spoiler_davanti + spoiler_dietro == spoiler.
# Uscita: alpha1/spoiler_quadrant_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, P, simulate, cheb
from kwindow_spoiler_census import virtual_walk, to_anchor_frame

def profile_level(K, cap=2_000_000, ref_rows=None):
    t0 = time.time()
    rows = []
    weapon = []
    quad_free = [0, 0, 0, 0]      # spoiler interamente fuori dal quadrante q
    QS = ((lambda x, y: x < 0 and y < 0),   # davanti-sinistra
          (lambda x, y: x >= 0 and y < 0),  # davanti-destra
          (lambda x, y: x < 0 and y >= 0),  # dietro-sinistra
          (lambda x, y: x >= 0 and y >= 0)) # dietro-destra
    n_real = 0
    ref = {r["word"]: r["onset"] for r in (ref_rows or [])}
    n_ref_ok = 0
    for widx in range(1 << K):
        word = tuple((widx >> i) & 1 for i in range(K))
        vg, pose = virtual_walk(word)
        if vg is None:
            continue
        n_real += 1
        anchor = to_anchor_frame(vg, pose)
        germ_black = {c for c, col in anchor.items() if col == 1}
        footprint = set(anchor)
        # record-compatibilita': a un record y-min stretto TUTTE le celle gia' visitate
        # (footprint incluso) giacciono a y_rel >= 1; una parola col footprint che tocca
        # y_rel <= 0 non puo' MAI presentarsi a un record.
        rec_ok = all(cy >= 1 for (_, cy) in footprint)
        turns, n, onset, fr, _ = simulate(germ_black, 0, 0, 0, cap, chk=2600)
        assert onset >= 0, f"K={K}: parola senza onset?! {word}"
        wstr = "".join("R" if b else "L" for b in word)
        if ref and wstr in ref:
            assert ref[wstr] == onset, f"onset diverso dal censimento per {wstr}"
            n_ref_ok += 1
        t_end = onset + P
        V = {c for c, (t, _) in fr.items() if t < t_end}
        spoiler = V - footprint
        ahead = [c for c in spoiler if c[1] < 0]
        behind = [c for c in spoiler if c[1] >= 0]
        deep1 = [c for c in behind if c[1] >= 1]   # fardello VERO ai record: la riga
        # y_rel=0 e' interamente mai-visitata a un record y-min (record stretto), quindi
        # bianca gratis come il semipiano davanti.
        assert len(ahead) + len(behind) == len(spoiler)
        for q, inq in enumerate(QS):
            if not any(inq(cx, cy) for (cx, cy) in spoiler):
                quad_free[q] += 1
        row = {"word": wstr, "onset": onset, "record_compatible": rec_ok,
               "spoiler": len(spoiler), "ahead": len(ahead), "behind": len(behind),
               "burden1": len(deep1),
               "burden1_cells": [list(c) for c in sorted(deep1)] if len(deep1) <= 12 else None,
               "behind_radius": max(map(cheb, behind)) if behind else 0,
               "behind_depth": max((cy for (_, cy) in behind), default=0)}
        rows.append(row)
        if rec_ok and not deep1:
            weapon.append(row)
    beh = sorted(r["behind"] for r in rows)
    bd1 = sorted(r["burden1"] for r in rows)
    rec = [r for r in rows if r["record_compatible"]]
    rb1 = sorted(r["burden1"] for r in rec) or [None]
    dep = sorted(r["behind_depth"] for r in rows)
    lev = {"K": K, "words_realizable": n_real, "ref_checked": n_ref_ok,
           "weapon_zero_burden1": len(weapon), "weapon_words": weapon[:20],
           "behind_min": beh[0], "behind_med": beh[len(beh) // 2], "behind_max": beh[-1],
           "burden1_min": bd1[0], "burden1_med": bd1[len(bd1) // 2], "burden1_max": bd1[-1],
           "record_compatible": len(rec),
           "rec_burden1_min": rb1[0], "rec_burden1_med": rb1[len(rb1) // 2] if rb1[0] is not None else None,
           "behind_depth_min": dep[0], "behind_depth_med": dep[len(dep) // 2],
           "behind_depth_max": dep[-1],
           "quad_free_counts": {"davanti-sx": quad_free[0], "davanti-dx": quad_free[1],
                                 "dietro-sx": quad_free[2], "dietro-dx": quad_free[3]},
           "min_burden1_words": sorted(rows, key=lambda r: r["burden1"])[:10],
           "min_rec_burden1_words": sorted(rec, key=lambda r: r["burden1"])[:10],
           "elapsed_s": round(time.time() - t0, 1)}
    return lev

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, nargs="+", default=[12, 14])
    ap.add_argument("--ref", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "kwindow_spoiler_summary.json"))
    args = ap.parse_args()
    ref = json.load(open(args.ref))
    ref_by_K = {lev["K"]: lev["rows"] for lev in ref["levels"]}
    out = {"levels": []}
    for K in args.K:
        lev = profile_level(K, ref_rows=ref_by_K.get(K))
        out["levels"].append(lev)
        print(f"K={K}: parole {lev['words_realizable']} (gate onset vs §87b: {lev['ref_checked']} OK)"
              f" | ARMA burden1==0: {lev['weapon_zero_burden1']}"
              f" | fardello y>=0 min/med/max {lev['behind_min']}/{lev['behind_med']}/{lev['behind_max']}"
              f" | BURDEN1 (y>=1) min/med/max {lev['burden1_min']}/{lev['burden1_med']}/{lev['burden1_max']}"
              f" | quadranti liberi {lev['quad_free_counts']}", flush=True)
        if lev["weapon_zero_burden1"]:
            print("  !! PAROLE-ARMA (burden1==0):",
                  [w["word"] for w in lev["weapon_words"]], flush=True)
        print(f"    record-compatibili: {lev['record_compatible']} | burden1 min/med "
              f"{lev['rec_burden1_min']}/{lev['rec_burden1_med']}", flush=True)
        for r in lev["min_rec_burden1_words"][:4]:
            print(f"    [REC] {r['word']} onset {r['onset']} burden1 {r['burden1']} "
                  f"celle {r['burden1_cells']}", flush=True)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "spoiler_quadrant_summary.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path}")

if __name__ == "__main__":
    main()
