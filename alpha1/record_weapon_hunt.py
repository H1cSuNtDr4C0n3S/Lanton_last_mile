# record_weapon_hunt.py — §87e: caccia alla PAROLA-ARMA ai record.
#
# Bersaglio: una parola w* di lunghezza K qualunque, REALIZZABILE e RECORD-COMPATIBILE
# (footprint ⊆ {y_rel >= 1}), con burden1(w*) = |(V \ F) ∩ {y_rel >= 1}| = 0.
# Se esiste, per il Lemma del Cono vale INCONDIZIONATAMENTE (dato il singolo onset di germe(w*)):
#   a un pose-record y-min, se le ultime K svolte sono w*, l'orbita entra in autostrada.
#   (Davanti e riga-0: mai visitate al record => bianche gratis. Footprint: colori = germe(w*)
#   per il Lemma della Finestra-K. Burden1 = 0: nient'altro da chiedere.)
# Contrappositiva: NESSUNA orbita eterna non-highway puo' presentare w* a un record. La prima
# parola vietata ai record — non fa cadere Link 1 da sola, ma e' l'attacco giusto reso oggetto.
#
# Metodo: beam search. Stato = parola (suffisso temporale fisso: la parola e' svolte(t-K..t-1));
# espansione = PREPEND di L/R (passi piu' vecchi; il suffisso relativo all'anchor non cambia,
# il footprint cresce all'indietro e puo' solo COPRIRE celle di spoiler trasformandole in
# footprint — ma il germe cambia colori, quindi onset e burden vanno RI-simulati, niente
# monotonia assunta). Pota: irrealizzabile, o footprint fuori {y>=1} (vincolo VERO del record:
# TUTTE le posizioni passate di un record stretto stanno a y >= y_record + 1, quindi la pota
# e' sound a ogni profondita').
#
# Semina: le migliori record-compatibili del profilo §87d (K=12/14/16) + tutte le realizzabili
# record-compatibili a K=10.
# Gate/tripwire: per ogni candidato ri-verifica indipendente (onset del germe, burden ricontato).
# Uscita: alpha1/record_weapon_summary.json (traiettoria best-per-K, arma se trovata).
import sys, os, json, time, argparse
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, P, simulate, cheb
from kwindow_spoiler_census import virtual_walk, to_anchor_frame

def eval_word(word, cap=2_000_000):
    """Ritorna None se irrealizzabile o non record-compatibile; altrimenti
    (burden1, onset, |spoiler|, celle_burden1)."""
    vg, pose = virtual_walk(word)
    if vg is None:
        return None
    anchor = to_anchor_frame(vg, pose)
    if any(cy < 1 for (_, cy) in anchor):
        return None
    germ_black = {c for c, col in anchor.items() if col == 1}
    footprint = set(anchor)
    turns, n, onset, fr, _ = simulate(germ_black, 0, 0, 0, cap, chk=2600)
    if onset < 0:
        return None                      # (non atteso; il censimento non ha mai visto buchi)
    t_end = onset + P
    V = {c for c, (t, _) in fr.items() if t < t_end}
    spoiler = V - footprint
    deep1 = sorted(c for c in spoiler if c[1] >= 1)
    return len(deep1), onset, len(spoiler), deep1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beam", type=int, default=300)
    ap.add_argument("--kmax", type=int, default=40)
    ap.add_argument("--budget-s", type=int, default=1200)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 1) - 1),
                    help="processi paralleli per la valutazione dei candidati (default: core-1)")
    args = ap.parse_args()
    t0 = time.time()

    # semina: tutte le record-compatibili a K=10
    seeds = []
    K0 = 10
    pool = mp.Pool(args.workers) if args.workers > 1 else None
    words0 = [tuple((widx >> i) & 1 for i in range(K0)) for widx in range(1 << K0)]
    res0 = pool.map(eval_word, words0, chunksize=16) if pool else [eval_word(w) for w in words0]
    for word, r in zip(words0, res0):
        if r is not None:
            seeds.append((r[0], word, r[1]))
    seeds.sort(key=lambda x: x[0])
    print(f"semina K={K0}: {len(seeds)} record-compatibili, burden1 min {seeds[0][0]}",
          flush=True)

    best_per_K = {K0: {"burden1": seeds[0][0],
                       "word": "".join("R" if b else "L" for b in seeds[0][1]),
                       "onset": seeds[0][2]}}
    frontier = seeds[:args.beam]
    weapon = None
    K = K0
    while K < args.kmax and weapon is None and time.time() - t0 < args.budget_s:
        K += 1
        cands = [(bit,) + word for _, word, _ in frontier for bit in (0, 1)]
        res = pool.map(eval_word, cands, chunksize=8) if pool else [eval_word(w) for w in cands]
        nxt = [(r[0], w2, r[1], r[3]) for w2, r in zip(cands, res) if r is not None]
        if not nxt:
            print(f"K={K}: frontiera vuota (pota totale), stop", flush=True)
            break
        nxt.sort(key=lambda x: x[0])
        b1, bw, bo, bcells = nxt[0]
        best_per_K[K] = {"burden1": b1,
                         "word": "".join("R" if b else "L" for b in bw),
                         "onset": bo,
                         "cells": [list(c) for c in bcells] if b1 <= 12 else None}
        print(f"K={K}: candidati {len(nxt)}, burden1 min {b1} "
              f"({best_per_K[K]['word']}, onset {bo})"
              + (f" celle {best_per_K[K]['cells']}" if b1 <= 6 else ""), flush=True)
        if b1 == 0:
            # RI-VERIFICA indipendente
            r2 = eval_word(bw)
            assert r2 is not None and r2[0] == 0, "ri-verifica arma fallita"
            weapon = best_per_K[K]
            print(f"!!! PAROLA-ARMA TROVATA a K={K}: {weapon['word']} "
                  f"(onset {weapon['onset']})", flush=True)
        frontier = [(b, w, o) for (b, w, o, _) in nxt[:args.beam]]

    if pool:
        pool.close(); pool.join()
    out = {"beam": args.beam, "kmax": args.kmax, "workers": args.workers,
           "best_per_K": best_per_K, "weapon": weapon,
           "elapsed_s": round(time.time() - t0, 1)}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "record_weapon_summary.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path} in {out['elapsed_s']} s")

if __name__ == "__main__":
    main()
