# speed_limit_theorem.py — §106: TEOREMA DEL LIMITE DI VELOCITA' (terra-check).
#
# LEMMA DEL CUNEO (deduttivo). A un record y-min stretto t (posa sotto il seme),
# per ogni riga y_rel = k >= 1 sia Delta_k = t - t_open(riga) (eta' in passi;
# t_open = record che ha aperto la riga, Scala/T3). Ogni cella (x, k) VISITATA
# prima di t soddisfa |x| + k <= Delta_k (velocita' L1: dalla visita alla posa
# corrente passano al piu' Delta_k passi). Quindi:
#     |x| + k > Delta_k  ==>  (x, k) MAI VISITATA  ==>  (sotto il seme) BIANCA.
#
# TEOREMA DEL LIMITE DI VELOCITA' (composizione con §101). Se w e' la parola del
# record (ipotesi A: onset_germe finito) e OGNI cella del read-set del transiente
# R_T(w) (prime-letture < onset_germe, non-footprint, y_rel >= 1) e' garantita-
# vergine dal Lemma del Cuneo, allora ogni lettura del transiente combacia
# (Lemma 1 §101) e d(t) >= onset_germe: l'orbita CAVALCA (classe R o E).
# CONTRAPPOSITIVA (il dente): un'orbita che NON cavalca al record t (classe T —
# le eterne ai record profondi, dato che (E) e' loro vietata) DEVE avere almeno
# una cella (x,k) del read-set con |x| + k <= Delta_k: un VINCOLO DI LENTEZZA
# della discesa, per-parola e word-decidibile.
#
# TERRA-CHECK (questo strumento):
#   T1: su TUTTI i record canonici di classe T (1639/1639 a §101), esiste almeno
#       una cella del read-set sotto-seme con |x|+k <= Delta_k (zero violazioni
#       attese: una violazione falsificherebbe il teorema).
#   T2 (piu' forte, del Lemma del Cuneo): ogni cella garantita-vergine e'
#       davvero BIANCA nel reale (query replay; zero violazioni attese).
#   T3 (episodi §101/§105b): quota garantita-vs-fortunata delle celle vergini
#       dei 2 lock (quanto del buco era FORZATO dalla velocita' di discesa).
# Uscita: alpha1/speed_limit_theorem_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_weapon_hunt import eval_word
from record_divergence_census import germ_long_run
from record_word_census import run_collect_records
from record_supply_census import replay_supply

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "speed_limit_theorem_summary.json")
K = 101


def transient_readset_from_germ(w, onset_germe):
    gturns, fr, t_dag, drift, footprint, xs, ys = germ_long_run(w, onset_germe)
    return sorted((c, tf) for c, (tf, _) in fr.items()
                  if tf < onset_germe and c not in footprint and c[1] >= 1)


def main():
    t0 = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    t1_checked = t1_viol = 0
    t2_checked = t2_viol = 0
    margini = []          # min su read-set di (Delta_k - (|x|+k)) — <0 = tutte garantite
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        t_rec_of_row = {ry: t for (t, _, ry) in records}
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]
        ev_cache = {}
        queries = {}
        info = []
        for (t, rx, ry) in recs:
            w = tuple(turns[t - K:t])
            r = ev_cache.get(w)
            if r is None:
                r = eval_word(w)
                ev_cache[w] = r
            assert r is not None
            rs = transient_readset_from_germ(w, r[1])
            # celle sotto-seme con eta' di riga definita
            cells = []
            for ((cx, cy), tf) in rs:
                row_abs = ry + cy
                if row_abs >= y_seed_min:
                    continue
                t_open = t_rec_of_row[row_abs]
                delta = t - t_open
                guaranteed = (abs(cx) + cy) > delta
                cells.append(((cx, cy), guaranteed, delta))
            info.append({"t": t, "pose": (rx, ry), "cells": cells})
            queries[t] = {(rx + cx, ry + cy) for ((cx, cy), g, d) in cells if g}
        colors, _ = replay_supply(seed, turns, queries)
        for row in info:
            t = row["t"]
            rx, ry = row["pose"]
            cells = row["cells"]
            if not cells:
                continue
            # T1: classe T (tutti i canonici) => almeno una cella NON garantita
            t1_checked += 1
            n_free = sum(1 for (_, g, _) in cells if not g)
            if n_free == 0:
                t1_viol += 1
                print(f"!!! T1 VIOLAZIONE orb {od.index} t={t}: read-set tutto "
                      f"garantito-vergine ma classe T?!", flush=True)
            margini.append(min((d - (abs(cx) + cy))
                               for ((cx, cy), _, d) in cells))
            # T2: garantite-vergini => bianche
            for ((cx, cy), g, d) in cells:
                if g:
                    t2_checked += 1
                    if colors[t][(rx + cx, ry + cy)][0] != 0:
                        t2_viol += 1
                        print(f"!!! T2 VIOLAZIONE orb {od.index} t={t} cella "
                              f"({cx},{cy})", flush=True)
        print(f"[orb {od.index:2d}] T1 {t1_checked} (viol {t1_viol}), "
              f"T2 {t2_checked} (viol {t2_viol})", flush=True)

    # T3: episodi lock — quota garantita
    hunt = json.load(open(os.path.join(HERE, "record_divergence_hunt_summary.json")))
    t3 = []
    for e in [hunt["F2"][0], hunt["F2"][1]]:
        rngs = int(e["rngstate"])
        t = int(e["t"])
        seed, _, _ = build_seed(rngs, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        t_rec_of_row = {ry: tt for (tt, _, ry) in records}
        rec = next(r for r in records if r[0] == t)
        _, rx, ry = rec
        w = tuple(turns[t - K:t])
        r = eval_word(w)
        rs = transient_readset_from_germ(w, r[1])
        gar = lucky = 0
        for ((cx, cy), tf) in rs:
            row_abs = ry + cy
            if row_abs >= y_seed_min or row_abs not in t_rec_of_row:
                continue
            delta = t - t_rec_of_row[row_abs]
            if (abs(cx) + cy) > delta:
                gar += 1
            else:
                lucky += 1
        t3.append({"rngstate": rngs, "t": t, "readset": len(rs),
                   "garantite_vergini": gar, "fortunate": lucky})
        print(f"T3 lock rng {rngs} t={t}: read-set {len(rs)}, garantite {gar}, "
              f"fortunate {lucky}", flush=True)

    import statistics as st
    out = {"T1": {"checked": t1_checked, "violazioni": t1_viol},
           "T2": {"checked": t2_checked, "violazioni": t2_viol},
           "margine_lentezza": {"min": min(margini), "med": st.median(margini),
                                "neg (tutte garantite)": sum(1 for m in margini
                                                             if m < 0)},
           "T3_episodi": t3,
           "elapsed_s": round(time.time() - t0, 1)}
    assert t1_viol == 0 and t2_viol == 0
    print(f"\nT1: {t1_checked} record, 0 violazioni — il vincolo di lentezza "
          f"REGGE su tutti i record reali di classe T", flush=True)
    print(f"T2: {t2_checked} celle garantite-vergini, 0 nere — Lemma del Cuneo "
          f"terra-verificato", flush=True)
    print(f"margine di lentezza min {out['margine_lentezza']['min']} med "
          f"{out['margine_lentezza']['med']}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
