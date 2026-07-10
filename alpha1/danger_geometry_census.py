# danger_geometry_census.py — §107b FASE 0: geometria word-side della classe pericolosa.
#
# DOMANDA (falsificabile, word-decidibile, ZERO occorrenza): le parole a |R_T|
# piccolo hanno geometria del read-set SEGREGATA rispetto alle ordinarie?
# Osservabili per parola (tutte funzioni della sola parola-101, via germe):
#   theta(cella) = |x| + k  per (x,k) in R_T(w), k = y_rel >= 1
#       (= eta' minima della riga k perche' la cella sia visitabile, Lemma del
#        Cuneo §106: Delta_k < theta ==> garantita-vergine).
#   theta_min(w) = min theta su R_T = lentezza minima che la discesa deve avere
#       perche' ALMENO una cella dello scudo sia visitabile. Parola "pericolosa
#       geometricamente" = theta_min alto (forza lentezza).
#   ATTENZIONE CONFOUND (dichiarato): theta_min cresce banalmente al calare di
#       |R_T| (min su meno celle). Correzione: P_iid(w) = (1 - F_ctrl(theta_min^-))^n
#       con F_ctrl = ecdf delle theta per-cella del pool di controllo: probabilita'
#       che n estrazioni iid dal pool diano un minimo >= theta_min osservato.
#       Se le pericolose hanno P_iid sistematicamente piccola, la geometria
#       segrega OLTRE l'effetto-taglia.
#   Coerenza laterale: frazione di celle di R_T con sign(x) == sign(net_x del
#       transiente word-forzato) e == sign(drift_x della highway del germe).
#
# SHIFT-SCAN (|R_T| e' proprieta' della coppia (flusso, taglio), round-2 §107b):
#   s in -12..+12 sui record della classe <=50 e sui 2 lock: |R_T(w_s)| con
#   w_s = turns[t-K+s : t+s] (None se irrealizzabile/non-record-compat).
#
# GATES (possono fallire — un gate che non puo' fallire e' vacuo, trappola bb):
#   G0: ogni cella di R_T fuori dal footprint (ricalcolato INDIPENDENTEMENTE da
#       virtual_walk+to_anchor_frame, non dal return di germ_long_run) e y>=1.
#   G1: istogramma per-record |R_T| identico ad alpha1/danger_class_sizes.json.
#   G2: i 2 lock (rngstate §101): (|R_T|, onset_germe) word-side == valori della
#       lente reale §101e/§105b (lock_hole_autopsy_summary.json: 14/55 e 9/65) —
#       gate cross-macchinario (germe da parola vs germe da griglia reale).
#   G3 (gate di morte di F0). STORIA DELLA RIPARAZIONE (a verbale, trappola pp):
#       i criteri della prima run — (a) rango di theta_min via bisect_left,
#       (b) P_iid=(1-F)^n — hanno SPARATO SPURIO su una distribuzione DEGENERE:
#       theta_min = 2 quasi ovunque (ogni parola, pericolosa o no, tiene una
#       cella scudabile a |x|+k <= 4 vicino alla posa: il Cuneo non forza MAI
#       l'intero read-set vergine word-side — fatto onesto di F0). Criteri
#       theta_min dichiarati VUOTI. Criterio riparato: coerenza laterale
#       coh_traj con mid-rank sui ties + TABELLA DEL GRADIENTE DI TAGLIA
#       (bin di n): la classe segrega OLTRE la taglia solo se il suo mid-rank
#       esce da [0.35,0.65] DENTRO il proprio bin di taglia — altrimenti la
#       geometria e' riparametrizzazione di |R_T| e la saldatura H1<->H3 NON
#       e' un manico indipendente.
# Nessuna soglia ENUNCIATA come fatto (trappola qq): i criteri sopra sono
# decisioni del gate (riparazione dichiarata), le distribuzioni sono il dato.
#
# Uscita: alpha1/danger_geometry_census.json
import sys, os, json, time, statistics as st

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_weapon_hunt import eval_word
from record_divergence_census import germ_long_run
from record_word_census import run_collect_records
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from speed_limit_theorem import transient_readset_from_germ

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "danger_geometry_census.json")
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
DANGER_HIST = os.path.join(HERE, "danger_class_sizes.json")
K = 101
KAPPA = 50            # parametro di classe (dato §107a), non soglia enunciata
SHIFTS = range(-12, 13)


def word_str(w):
    return "".join("R" if b else "L" for b in w)


def analyze_word(w, cache):
    """Osservabili word-side. Ritorna None se eval_word boccia."""
    ws = word_str(w)
    if ws in cache:
        return cache[ws]
    r = eval_word(w)
    if r is None:
        cache[ws] = None
        return None
    onset_g = r[1]
    rs = transient_readset_from_germ(w, onset_g)
    # G0: footprint INDIPENDENTE (virtual_walk, non germ_long_run)
    vg, pose = virtual_walk(w)
    assert vg is not None
    fp_ind = set(to_anchor_frame(vg, pose))
    for (c, tf) in rs:
        assert c not in fp_ind, f"G0 FALLITO: {c} nel footprint di {ws[:20]}..."
        assert c[1] >= 1, f"G0 FALLITO: y_rel<1 in {ws[:20]}..."
    # traiettoria del transiente (word-forzata) + drift highway
    gturns, fr, t_dag, drift, footprint, xs, ys = germ_long_run(w, onset_g)
    net_x = xs[onset_g] - xs[0]
    thetas = sorted(abs(cx) + cy for ((cx, cy), tf) in rs)
    n = len(rs)
    def sgn(v):
        return (v > 0) - (v < 0)
    coh_traj = (sum(1 for ((cx, _), _) in rs if sgn(cx) == sgn(net_x)) / n
                if n and net_x else None)
    coh_drift = (sum(1 for ((cx, _), _) in rs if sgn(cx) == sgn(drift[0])) / n
                 if n and drift[0] else None)
    info = {"n": n, "onset_germe": onset_g,
            "theta_min": thetas[0] if thetas else None,
            "theta_med": thetas[n // 2] if thetas else None,
            "thetas": thetas,
            "net_x": net_x, "drift_x": drift[0],
            "coh_traj": coh_traj, "coh_drift": coh_drift}
    cache[ws] = info
    return info


def ecdf_rank(x, pool_sorted):
    """Frazione del pool < x (rango ecdf, ties a sinistra)."""
    import bisect
    return bisect.bisect_left(pool_sorted, x) / len(pool_sorted)


def main():
    t0 = time.time()
    cache = {}
    dumps = parse_dumps(ALPHA / "dumps_all.txt")

    per_record = []           # (orb, t, word_str, n)
    hist = {}
    danger_records = []       # per lo shift-scan: (label, turns, t, t_on)
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]
        for (t, rx, ry) in recs:
            w = tuple(turns[t - K:t])
            info = analyze_word(w, cache)
            assert info is not None
            per_record.append((od.index, t, word_str(w), info["n"]))
            hist[info["n"]] = hist.get(info["n"], 0) + 1
            if info["n"] <= KAPPA:
                danger_records.append((f"orb{od.index}_t{t}", turns, t, t_on))
        print(f"[orb {od.index:2d}] record {len(recs)}, parole uniche cumul. "
              f"{len(cache)}", flush=True)

    # ---- G1: istogramma bit-identico a §107a ----
    ref = json.load(open(DANGER_HIST))["per_record_sizes_hist"]
    ref = {int(k): v for k, v in ref.items()}
    g1_ok = (ref == hist)
    print(f"G1 istogramma |R_T| == §107a: {'OK' if g1_ok else 'FALLITO'}",
          flush=True)
    assert g1_ok, "G1 FALLITO: istogramma diverso da danger_class_sizes.json"

    # ---- G2 + shift-scan dei 2 lock ----
    hunt = json.load(open(HUNT))
    lens = [e for e in json.load(open(os.path.join(
        HERE, "lock_hole_autopsy_summary.json"))) if e["label"].startswith("LOCK")]
    lock_words = []
    lock_scan = []
    g2_ok = True
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        seed, _, _ = build_seed(rngs, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        w = tuple(turns[t - K:t])
        info = analyze_word(w, cache)
        lock_words.append({"rngstate": rngs, "t": t, "word": word_str(w),
                           **{k: v for k, v in info.items() if k != "thetas"},
                           "thetas": info["thetas"]})
        danger_records.append((f"LOCK{'AB'[i]}_rng{rngs}", turns, t, t_on))
        ref = next(le for le in lens if int(le["rngstate"]) == rngs
                   and int(le["t"]) == t)
        ok = (info["n"] == ref["readset_n"]
              and info["onset_germe"] == ref["onset_germe"])
        g2_ok = g2_ok and ok
        print(f"G2 lock rng {rngs} t={t}: word-side (|R_T|={info['n']}, "
              f"og={info['onset_germe']}) vs lente reale "
              f"({ref['readset_n']}, {ref['onset_germe']}): "
              f"{'OK' if ok else 'FALLITO'}", flush=True)
    assert g2_ok, "G2 FALLITO: lock non riprodotti word-side"

    # ---- shift-scan (classe <=50 + 2 lock) ----
    for (label, turns, t, t_on) in danger_records:
        row = {"label": label, "scan": []}
        for s in SHIFTS:
            a, b = t - K + s, t + s
            if a < 0 or b > t_on:
                row["scan"].append([s, "fuori-flusso"])
                continue
            info = analyze_word(tuple(turns[a:b]), cache)
            row["scan"].append([s, info["n"] if info else None])
        lock_scan.append(row)
    print(f"shift-scan completato su {len(lock_scan)} record "
          f"({len(danger_records) - 2} classe<= {KAPPA} + 2 lock)", flush=True)

    # ---- G3: segregazione classe <=50 vs controlli appaiati ----
    words = {ws: cache[ws] for ws in {w for (_, _, w, _) in per_record}}
    danger_ws = {w for (_, _, w, n) in per_record if n <= KAPPA}
    onset_cap = max(words[w]["onset_germe"] for w in danger_ws)
    ctrl_ws = {w for w, inf in words.items()
               if w not in danger_ws and inf["onset_germe"] <= onset_cap}
    print(f"classe pericolosa: {len(danger_ws)} parole uniche "
          f"(onset_germe max {onset_cap}); controlli appaiati "
          f"(onset_germe <= {onset_cap}): {len(ctrl_ws)}", flush=True)
    import bisect

    def midrank(x, pool_sorted):
        lo = bisect.bisect_left(pool_sorted, x)
        hi = bisect.bisect_right(pool_sorted, x)
        return (lo + hi) / 2 / len(pool_sorted)

    # theta_min: dichiarazione di degenerazione (dato, non criterio)
    all_tm = [inf["theta_min"] for inf in words.values()]
    tm_mode_frac = max(all_tm.count(v) for v in set(all_tm)) / len(all_tm)
    theta_min_degenere = tm_mode_frac > 0.8

    # gradiente di taglia della coerenza (bin di n) su TUTTE le parole
    bins = [(1, 15), (16, 50), (51, 100), (101, 200), (201, 400),
            (401, 800), (801, 4000)]
    gradiente = []
    for a, b in bins:
        grp = sorted(inf["coh_traj"] for inf in words.values()
                     if a <= inf["n"] <= b and inf["coh_traj"] is not None)
        if grp:
            gradiente.append({"bin_n": [a, b], "parole": len(grp),
                              "coh_traj_med": grp[len(grp) // 2]})

    # mid-rank della coerenza pericolosa DENTRO il proprio bin di taglia:
    # per la classe <=50 il bin proprio e' (16,50)+(1,15) = la classe stessa,
    # quindi il confronto oltre-taglia usa il bin adiacente (51,100) come
    # riferimento DICHIARATO (non esistono ordinarie a n<=50 per costruzione).
    ref_pool = sorted(inf["coh_traj"] for inf in words.values()
                      if 51 <= inf["n"] <= 100 and inf["coh_traj"] is not None)
    coh_danger = sorted(words[w]["coh_traj"] for w in danger_ws
                        if words[w]["coh_traj"] is not None)
    med_coh_rank = midrank(coh_danger[len(coh_danger) // 2], ref_pool)
    step_gradiente = not (0.35 <= med_coh_rank <= 0.65)
    g3 = {"criterio": "riparato in-sessione (vedi testa file, trappola pp)",
          "n_danger_words": len(danger_ws), "n_ctrl_words": len(ctrl_ws),
          "onset_germe_cap": onset_cap,
          "theta_min_degenere": theta_min_degenere,
          "theta_min_moda_frac": round(tm_mode_frac, 4),
          "theta_med_danger_med": sorted(
              words[w]["theta_med"] for w in danger_ws)[len(danger_ws) // 2],
          "theta_med_ctrl_med": sorted(
              words[w]["theta_med"] for w in ctrl_ws)[len(ctrl_ws) // 2],
          "coh_traj_med_danger": coh_danger[len(coh_danger) // 2],
          "gradiente_taglia": gradiente,
          "coh_midrank_vs_bin_51_100": med_coh_rank,
          "step_gradiente_sotto_50": step_gradiente,
          "VERDETTO_G3": ("il gradiente taglia->coerenza CONTINUA sotto n=50 "
                          "(step vs bin adiacente confermato)" if step_gradiente
                          else "gradiente piatto sotto n=50"),
          "nota_onesta": "oltre-taglia NON separabile word-side: la classe "
                         "pericolosa E' il fondo della scala di taglia "
                         "(classe ≡ n piccolo ≡ direzionale ≡ transiente "
                         "corto: quattro facce dello stesso oggetto); la "
                         "saldatura H1<->H3 word-side e' una RI-DESCRIZIONE, "
                         "non un manico indipendente"}
    print(json.dumps(g3, indent=1), flush=True)

    out = {"gates": {"G0": "ok (assert per-parola)", "G1": g1_ok, "G2": g2_ok,
                     "G3": g3},
           "lock_words": lock_words,
           "shift_scan": lock_scan,
           "per_word": {w: {k: v for k, v in words[w].items() if k != "thetas"}
                        for w in words},
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
