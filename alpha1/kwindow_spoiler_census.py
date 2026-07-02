# kwindow_spoiler_census.py — §87b: il censimento dei GERMI DI FINESTRA-K e il Teorema dello
# Spoiler Vecchio (candidato).
#
# LEMMA DELLA FINESTRA-K (determinazione all'indietro; duale del Replay-Lock §87a).
#   Sia t un istante qualunque di un'orbita qualunque, con t>=K, e sia w = svolte(t-K..t-1)
#   la parola degli ultimi K passi. Allora:
#   (a) w e' REALIZZABILE nel senso di word_lock.py §86b (le riletture sono coerenti);
#   (b) l'insieme F(w) delle celle toccate negli ultimi K passi (footprint, co-moving rispetto
#       alla posa a t) e i loro COLORI al tempo t sono FUNZIONE DI w SOLA.
#   Dimostrazione: ogni lettura della finestra o e' prima-lettura nella finestra (il colore
#   letto e' rivelato dalla svolta stessa) o e' rilettura (colore = ultima scrittura, nota per
#   induzione); ogni scrittura e' il flip della lettura. QED.
#
# COSTRUZIONE. Per ogni parola realizzabile w di lunghezza K:
#   germe(w) = configurazione "colori di F(w) al tempo t" (co-moving, posa finale in origine,
#   heading su) + BIANCO ovunque altrove. Si simula in avanti: se germe(w) entra in autostrada
#   (onset <= cap), allora per il Lemma del Cono (§87a) vale il condizionale ESATTO:
#     in QUALUNQUE orbita, a QUALUNQUE t>=K con svolte recenti w: se tutte le celle di
#     V(w) \ F(w) (il cono del germe, meno il footprint) sono bianche al tempo t, l'orbita
#     entra in autostrada.
#   Contrappositiva (se TUTTI i germi di lunghezza K fanno onset):
#     TEOREMA DELLO SPOILER VECCHIO (scala K): un'orbita eterna non-highway deve avere, in
#     OGNI istante t, almeno una cella nera in V(w(t)) \ F(w(t)) — cioe' un nero NON prodotto
#     dagli ultimi K passi: detrito vecchio, a distanza <= R(w(t)) dalla formica.
#
# Misure:
#   1. numero di parole realizzabili per K (vs 2^K);
#   2. per ogni germe: onset (cap), |V|, raggio del cono, |V \ F|, raggio dello spoiler-set;
#   3. distribuzione onset; QUANTI germi NON fanno onset entro il cap (se >0: il teorema a
#      scala K non chiude — quei germi sono i buchi, da ispezionare);
#   4. il caso w di soli L (la formica ha appena mangiato K neri) e soli R.
#
# SELF-TEST (§5, obbligatori PRIMA del censimento):
#   A. Lemma finestra-K su dati reali: 3 orbite junk casuali, 400 istanti casuali t>=K:
#      i colori predetti da w su F(w) (trasformati sulla posa reale) devono coincidere col
#      campo reale al tempo t. QUALSIASI mismatch = ROSSO.
#   B. gate K=0: germe vuoto = griglia vuota => onset 9977 (riferimento §76).
#   C. coerenza realizzabilita': una parola con rilettura contraddittoria nota deve essere
#      scartata; le parole estratte da corse reali devono essere SEMPRE realizzabili.
#
# Convenzioni: alpha1_engine.c (bianco->R, turns 1=R; DX/DY schermo; onset_verified §87a).
# Uscita: alpha1/kwindow_spoiler_summary.json
import sys, os, json, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, P, onset_verified, simulate, cheb, rotk

def virtual_walk(word):
    """Cammino virtuale di len(word) passi da (0,0,0) con prime-letture assegnate dalla
    parola (R=1 => letta bianca, L=0 => letta nera). Ritorna None se irrealizzabile
    (rilettura contraddittoria), altrimenti (grid: cella->colore al tempo finale,
    end_pose (x,y,h))."""
    grid = {}
    x = y = 0; h = 0
    for wbit in word:
        need = 0 if wbit else 1          # colore che la svolta dichiara di aver letto
        c = (x, y)
        if c in grid:
            if grid[c] != need:
                return None, None        # irrealizzabile
        # prima lettura: il colore iniziale era 'need' (rivelato dalla svolta)
        if wbit:
            h = (h + 1) & 3; grid[c] = 1
        else:
            h = (h + 3) & 3; grid[c] = 0
        x += DX[h]; y += DY[h]
    return grid, (x, y, h)

def to_anchor_frame(grid, pose):
    """Trasla la posa finale in origine e ruota l'heading a 0 (su).
    Rotazione oraria k volte: (x,y)->(-y,x) manda heading h in h+k; serve k=(-h)%4."""
    x0, y0, h0 = pose
    k = (-h0) % 4
    out = {}
    for (cx, cy), col in grid.items():
        out[rotk((cx - x0, cy - y0), k)] = col
    return out

def selftest_A(n_orbits=3, n_probes=150, K=12, rng_seed=87):
    rng = random.Random(rng_seed)
    for oi in range(n_orbits):
        # orbita junk: blob casuale
        seed = set()
        side = rng.randrange(7, 15)
        for cx in range(-side // 2, side // 2 + 1):
            for cy in range(-side // 2, side // 2 + 1):
                if rng.random() < 0.4:
                    seed.add((cx, cy))
        # corsa reale con storia di pose
        grid = {}; x = y = 0; h = 0
        turns = []
        hist = []                        # (x,y,h) PRIMA del passo t
        T = 20000
        for t in range(T):
            hist.append((x, y, h))
            c = (x, y)
            color = grid[c] if c in grid else (1 if c in seed else 0)
            if color == 0:
                h = (h + 1) & 3; grid[c] = 1; turns.append(1)
            else:
                h = (h + 3) & 3; grid[c] = 0; turns.append(0)
            x += DX[h]; y += DY[h]
        # sonde
        for _ in range(n_probes):
            t = rng.randrange(K, T)
            w = tuple(turns[t - K:t])
            vg, pose = virtual_walk(w)
            if vg is None:
                return False, f"parola reale irrealizzabile a t={t} orbita {oi}"
            anchor = to_anchor_frame(vg, pose)
            # posa reale a t (PRIMA della lettura t)
            ax, ay, ah = hist[t]
            # replay fino a t per il campo al tempo t (lento ma e' un test)
            g2 = {}; x2 = y2 = 0; h2 = 0
            for s in range(t):
                c2 = (x2, y2)
                col2 = g2[c2] if c2 in g2 else (1 if c2 in seed else 0)
                if col2 == 0:
                    h2 = (h2 + 1) & 3; g2[c2] = 1
                else:
                    h2 = (h2 + 3) & 3; g2[c2] = 0
                x2 += DX[h2]; y2 += DY[h2]
            for rc, col in anchor.items():
                wc = rotk(rc, ah)
                cabs = (wc[0] + ax, wc[1] + ay)
                real = g2.get(cabs, 1 if cabs in seed else 0)
                if real != col:
                    return False, (f"mismatch colore a t={t} orbita {oi} cella rel {rc}: "
                                   f"predetto {col} reale {real}")
    return True, "OK"

def census(K, cap, verbose_every=500):
    """Enumera le parole realizzabili di lunghezza K e per ognuna misura l'onset del germe."""
    t0 = time.time()
    rows = []
    n_real = 0
    n_onset = 0
    no_onset = []
    for widx in range(1 << K):
        word = tuple((widx >> i) & 1 for i in range(K))
        vg, pose = virtual_walk(word)
        if vg is None:
            continue
        n_real += 1
        anchor = to_anchor_frame(vg, pose)
        germ_black = {c for c, col in anchor.items() if col == 1}
        footprint = set(anchor)
        turns, n, onset, fr, _ = simulate(germ_black, 0, 0, 0, cap, chk=2600)
        if onset >= 0:
            n_onset += 1
            t_end = onset + P
            V = {c for c, (t, _) in fr.items() if t < t_end}
            spoiler = V - footprint
            rows.append({
                "word": "".join("R" if b else "L" for b in word),
                "n_trail_black": len(germ_black), "footprint": len(footprint),
                "onset": onset,
                "V": len(V), "cone_radius": max(map(cheb, V)),
                "spoiler_cells": len(spoiler),
                "spoiler_radius": max(map(cheb, spoiler)) if spoiler else 0,
            })
        else:
            no_onset.append("".join("R" if b else "L" for b in word))
        if verbose_every and n_real % verbose_every == 0:
            print(f"  ... {n_real} parole realizzabili, {n_onset} onset, "
                  f"{time.time()-t0:.0f}s", flush=True)
    return rows, n_real, no_onset

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, nargs="+", default=[8, 10, 12])
    ap.add_argument("--cap", type=int, default=2_000_000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    print("SELF-TEST B (K=0 => griglia vuota, onset 9977):", flush=True)
    turns, n, onset, fr, _ = simulate(set(), 0, 0, 0, 4_000_000)
    assert onset == 9977, f"gate vuota fallito: {onset}"
    print("  OK")

    print("SELF-TEST C (irrealizzabile nota / parole reali realizzabili):", flush=True)
    # LLRRRR e' irrealizzabile come parola di PRIMA lettura? Attenzione: qui il criterio e'
    # solo la coerenza delle riletture della camminata: testiamo una contraddizione certa:
    # RRRR = quadrato orario che rilegge la cella iniziale scritta nera... verifica diretta:
    bad = None
    for widx in range(1 << 6):
        w = tuple((widx >> i) & 1 for i in range(6))
        if virtual_walk(w)[0] is None:
            bad = w
            break
    assert bad is not None, "nessuna parola irrealizzabile a K=6? sospetto"
    print(f"  irrealizzabile trovata a K=6: {''.join('R' if b else 'L' for b in bad)} — OK")

    print("SELF-TEST A (lemma finestra-K su 3 orbite junk, 150 sonde, K=12):", flush=True)
    okA, msgA = selftest_A()
    print(f"  {msgA}")
    assert okA, msgA

    out = {"selftests": {"A": msgA, "B": "onset 9977", "C": "ok"},
           "cap": args.cap, "levels": []}
    for K in args.K:
        print(f"CENSIMENTO K={K} (2^{K} = {1<<K} parole):", flush=True)
        rows, n_real, no_onset = census(K, args.cap)
        onsets = [r["onset"] for r in rows]
        sprad = [r["spoiler_radius"] for r in rows]
        lev = {
            "K": K, "words_total": 1 << K, "words_realizable": n_real,
            "germs_onset": len(rows), "germs_no_onset": len(no_onset),
            "no_onset_words": no_onset[:50],
            "onset_min": min(onsets) if onsets else None,
            "onset_med": sorted(onsets)[len(onsets) // 2] if onsets else None,
            "onset_max": max(onsets) if onsets else None,
            "spoiler_radius_min": min(sprad) if sprad else None,
            "spoiler_radius_med": sorted(sprad)[len(sprad) // 2] if sprad else None,
            "spoiler_radius_max": max(sprad) if sprad else None,
            "all_L": next((r for r in rows if set(r["word"]) == {"L"}), None),
            "all_R": next((r for r in rows if set(r["word"]) == {"R"}), None),
            "rows": rows,
        }
        out["levels"].append(lev)
        print(f"  realizzabili {n_real}/{1<<K}; onset {len(rows)}; NO-onset {len(no_onset)}"
              f" | onset min/med/max {lev['onset_min']}/{lev['onset_med']}/{lev['onset_max']}"
              f" | raggio-spoiler min/med/max {lev['spoiler_radius_min']}/"
              f"{lev['spoiler_radius_med']}/{lev['spoiler_radius_max']}", flush=True)
        if no_onset:
            print(f"  !! parole senza onset entro cap: {no_onset[:10]}", flush=True)

    path = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "kwindow_spoiler_summary.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path}")

if __name__ == "__main__":
    main()
