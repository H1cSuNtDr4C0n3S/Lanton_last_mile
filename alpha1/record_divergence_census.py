# record_divergence_census.py — §101: PROFONDITA' DI DIVERGENZA e LOCK W0-LIKE ai record.
#
# Contesto (Link 1, "orbita eterna non-highway => lock W0-like profondi infinite volte"):
# al record profondo t con parola w (ultime K=101 svolte), il germe di w — corsa virtuale
# dal pose-record con i soli colori word-determinati — entra in autostrada a onset_germe(w).
# La corsa REALE esegue le stesse svolte del germe finche' non LEGGE una cella divergente:
#   d(t) = primo indice i con gturns[i] != turns[t+i]   (tempo-germe dal record).
# DEDUTTIVO (Cono §87 + Finestra-K + record y-min stretto): fino alla prima divergenza le
# due corse coincidono; le divergenze possono vivere SOLO sul residuo (prime-letture del
# germe fuori footprint a y_rel>=1): davanti e riga-0 sono mai-visitate (=> bianche, sotto
# il seme) e il footprint e' word-determinato. Quindi:
#   d(t) == min { t_fr(c) : c nel residuo-dagger, reale(c a t) = nero }   (TRIPWIRE T-DIV:
#   due derivazioni indipendenti, per-svolte e per-celle, devono coincidere).
# Se d(t) >= onset_germe, la corsa reale CAVALCA W0 per ride = d - onset_germe passi:
# un LOCK W0-LIKE realizzato dall'orbita. Se d < onset_germe: rigetto nel transiente.
# Se nessuna divergenza entro l'orizzonte: l'ingresso e' in corso (Replay-Lock).
#
# Questo censimento misura, per la prima volta, PER OGNI record (24 orbite, 1639 record
# §89a): d(t), ride(t), classe T/R/E, la cella di prima divergenza (y_rel, cheb, eta',
# ep), il residuo-dagger completo (G-dagger: quota del censimento alla V-daga, §101
# roadmap), min_ep-dagger e min_cheb-dagger per-record (mai censiti), e la direzione di
# drift della highway del germe (verso il vergine o verso il visitato).
#
# Orizzonte: t_dagger(w) = max(2600, onset_germe + 2080) — l'orizzonte della RILEVAZIONE
# (lezione §91/V-daga: onset_verified richiede coda periodica 2080 e t >= 2600).
#
# Gate esterni (assert): n_records == §89a; tripwire-G corto == §89a (1620); somma G
# corta == §89b (225.012); da_seme == §89b (3.722); hist G(0..10) == §89b; hist min_ep
# per-record == §98. Tripwire nuovi: T-DIV (svolte==celle); T-V-DAGGER (G_dagger==0 =>
# t_on - t <= t_dagger: il Replay-Lock alla V-daga); T-SCALA sulla cella di divergenza
# profonda (ep <= y_rel). Ramo degenere CONTATO e riportato (trappola pp).
#
# Uscita: alpha1/record_divergence_census_summary.json (+ per-record CSV).
import sys, os, json, time, bisect, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import DX, DY, P, simulate
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_supply_census import replay_supply

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "record_word_census_summary.json")
DYN = os.path.join(HERE, "record_guilty_dynamics_summary.json")
SUPPLY = os.path.join(HERE, "record_supply_census_summary.json")
OUT = os.path.join(HERE, "record_divergence_census_summary.json")
OUTCSV = os.path.join(HERE, "record_divergence_census_records.csv")
K = 101


def germ_long_run(word, onset_germe):
    """Corsa lunga del germe (stop MAI all'onset): t_dagger passi.
    Ritorna (gturns, fr, t_dagger, drift_rel).
    drift_rel = spostamento del germe in un periodo di highway (frame anchor =
    frame assoluto del record, heading 0): pos(on+2P) - pos(on+P)."""
    vg, pose = virtual_walk(word)
    assert vg is not None
    anchor = to_anchor_frame(vg, pose)
    germ_black = {c for c, col in anchor.items() if col == 1}
    t_dagger = max(2600, onset_germe + 2080)
    gturns, n, _, fr, _ = simulate(germ_black, 0, 0, 0, t_dagger,
                                   stop_at_onset=False, chk=t_dagger + 1)
    assert n == t_dagger
    # traiettoria per drift e per la cella di divergenza
    xs = [0] * (t_dagger + 1)
    ys = [0] * (t_dagger + 1)
    x = y = 0
    h = 0
    for i in range(t_dagger):
        if gturns[i]:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
        xs[i + 1] = x
        ys[i + 1] = y
    assert onset_germe + 2 * P <= t_dagger
    drift = (xs[onset_germe + 2 * P] - xs[onset_germe + P],
             ys[onset_germe + 2 * P] - ys[onset_germe + P])
    return gturns, fr, t_dagger, drift, set(anchor), xs, ys


def main():
    t_start = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    census = json.load(open(CENSUS))
    dyn = json.load(open(DYN))
    supply = json.load(open(SUPPLY))

    ev_cache = {}
    germ_cache = {}

    def germ_data(w):
        g = germ_cache.get(w)
        if g is None:
            r = ev_cache.get(w)
            if r is None:
                r = eval_word(w)
                ev_cache[w] = r
            assert r is not None
            g = germ_long_run(w, r[1]) + (r,)
            germ_cache[w] = g
        return g

    n_records = 0
    tripwire_short = 0
    guilty_tot_short = 0
    da_seme_short = 0
    G_all_short = []
    rec_min_ep_short = []          # per gate §98 (record interamente profondi, corto)
    t_div = t_vdag = t_scala = 0   # tripwire nuovi superati
    n_classe = {"T": 0, "R": 0, "E": 0}
    n_E_troncati = 0               # E con L_avail < t_dagger (orizzonte non coperto)
    rows_csv = []
    per_orbit = []

    for od in dumps:
        seed, side, dens = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header, f"orb {od.index}: onset != header"
        n_real = len(turns)
        rows_rec = [ry for (_, _, ry) in records]
        assert rows_rec == list(range(-1, -len(records) - 1, -1))
        rec_times = [t for (t, _, _) in records]
        t_rec_of_row = {ry: t for (t, _, ry) in records}

        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]

        # -- prepara query: residuo-dagger assoluto per ogni record --
        info = []
        queries = {}
        for (t, rx, ry) in recs:
            w = tuple(turns[t - K:t])
            gturns, fr, t_dag, drift, footprint, xs, ys, r = germ_data(w)
            burden, onset_germe, _, deep1_short = r
            res_dag = sorted(c for c, (tf, _) in fr.items()
                             if tf < t_dag and c not in footprint and c[1] >= 1)
            res_abs = {(rx + cx, ry + cy) for (cx, cy) in res_dag}
            info.append({"t": t, "pose": (rx, ry), "word": w,
                         "burden": burden, "onset_germe": onset_germe,
                         "res_dag": res_dag, "res_short": set(deep1_short),
                         "t_dag": t_dag, "drift": drift})
            queries[t] = res_abs
        colors, first_row = replay_supply(seed, turns, queries)

        ob = {"orbit": od.index, "records": 0, "R": 0, "T": 0, "E": 0,
              "ride_max": 0, "G_dag_sum": 0}
        for row in info:
            t = row["t"]
            rx, ry = row["pose"]
            w = row["word"]
            gturns, fr, t_dag, drift, footprint, xs, ys, r = germ_data(w)
            onset_germe = row["onset_germe"]
            got = colors[t]
            n_records += 1
            ob["records"] += 1

            # ---- lato corto (gate §89a/§89b/§98) ----
            guilty_short = [c for c in row["res_short"]
                            if got[(rx + c[0], ry + c[1])][0] == 1]
            Gs = len(guilty_short)
            G_all_short.append(Gs)
            guilty_tot_short += Gs
            kmax_s = max((cy for (_, cy) in row["res_short"]), default=0)
            deep_record_s = (ry + kmax_s < y_seed_min) and row["res_short"]
            if t_on - t > onset_germe + P:
                tripwire_short += 1
                assert Gs >= 1, f"orb {od.index} t={t}: residuo corto tutto bianco"
            ep_list_s = []
            for (cx, cy) in guilty_short:
                ca = (rx + cx, ry + cy)
                col, paint_t = got[ca]
                if ca[1] >= y_seed_min:
                    if paint_t is None:
                        da_seme_short += 1
                elif paint_t is not None:
                    lo = bisect.bisect_right(rec_times, paint_t)
                    hi = bisect.bisect_right(rec_times, t)
                    ep_list_s.append(hi - lo)
            if deep_record_s:
                assert len(ep_list_s) == Gs
                rec_min_ep_short.append(min(ep_list_s))

            # ---- residuo-dagger: G_dagger, min_ep_dag, min_cheb_dag ----
            guilty_dag = []
            for (cx, cy) in row["res_dag"]:
                ca = (rx + cx, ry + cy)
                col, paint_t = got[ca]
                if col == 1:
                    tf = fr[(cx, cy)][0]
                    guilty_dag.append(((cx, cy), tf, paint_t))
            Gd = len(guilty_dag)
            ob["G_dag_sum"] += Gd
            kmax_d = max((cy for (_, cy) in row["res_dag"]), default=0)
            deep_record_d = (ry + kmax_d < y_seed_min) and bool(row["res_dag"])
            min_cheb_d = min((max(abs(cx), abs(cy)) for ((cx, cy), _, _)
                              in guilty_dag), default=None)
            min_ep_d = None
            if deep_record_d and guilty_dag:
                eps = []
                for ((cx, cy), tf, paint_t) in guilty_dag:
                    assert paint_t is not None, \
                        f"orb {od.index} t={t}: colpevole-dagger profonda di seme?!"
                    lo = bisect.bisect_right(rec_times, paint_t)
                    hi = bisect.bisect_right(rec_times, t)
                    eps.append(hi - lo)
                min_ep_d = min(eps)

            # ---- divergenza per-svolte ----
            L = min(t_dag, n_real - t)
            d = None
            for i in range(L):
                if gturns[i] != turns[t + i]:
                    d = i
                    break

            # ---- tripwire T-DIV: derivazione per-celle ----
            d_cell = min((tf for (_, tf, _) in guilty_dag), default=None)
            if d is not None:
                assert d_cell is not None and d_cell == d, \
                    (f"orb {od.index} t={t}: T-DIV rosso, d_svolte={d} "
                     f"d_celle={d_cell}")
                t_div += 1
            else:
                # nessuna divergenza entro L: ogni colpevole-dagger deve avere
                # prima-lettura >= L (coerenza), e se L copre tutto l'orizzonte
                # allora G_dagger == 0 e vale il Replay-Lock alla V-daga
                assert d_cell is None or d_cell >= L
                if L >= t_dag:
                    assert Gd == 0
                else:
                    n_E_troncati += 1
            if Gd == 0:
                assert d is None, "G_dagger=0 ma svolte divergenti?!"
                assert t_on - t <= t_dag, \
                    (f"orb {od.index} t={t}: VIOLAZIONE V-DAGGER, G_dag=0 ma "
                     f"t_on-t={t_on - t} > t_dagger={t_dag}")
                t_vdag += 1

            # ---- classe e cella di divergenza ----
            if d is None:
                classe = "E"
                ride = None
                div_cell = None
            elif d < onset_germe:
                classe = "T"
                ride = 0
            else:
                classe = "R"
                ride = d - onset_germe
                ob["ride_max"] = max(ob["ride_max"], ride)
            n_classe[classe] += 1
            ob[classe] += 1

            div_info = {}
            if d is not None:
                cx, cy = xs[d], ys[d]
                ca = (rx + cx, ry + cy)
                assert (cx, cy) not in footprint
                assert cy >= 1, f"divergenza a y_rel {cy} < 1?!"
                col, paint_t = got[ca]
                assert col == 1
                div_info = {"y_rel": cy, "cheb": max(abs(cx), abs(cy)),
                            "pre_onset_germe": d < onset_germe}
                if ca[1] < y_seed_min:
                    assert paint_t is not None
                    lo = bisect.bisect_right(rec_times, paint_t)
                    hi = bisect.bisect_right(rec_times, t)
                    ep = hi - lo
                    assert 1 <= ep <= cy, \
                        f"orb {od.index} t={t}: T-SCALA rosso su divergenza"
                    t_scala += 1
                    div_info["ep"] = ep
                    div_info["age"] = t - paint_t
                    div_info["origine"] = "dipinta"
                else:
                    div_info["origine"] = ("SEME" if paint_t is None
                                           else "dipinta_shallow")

            rows_csv.append({
                "orbit": od.index, "t": t, "t_on_meno_t": t_on - t,
                "burden": row["burden"], "onset_germe": onset_germe,
                "t_dagger": t_dag, "L_avail": L,
                "G_short": Gs, "G_dagger": Gd,
                "res_short": len(row["res_short"]),
                "res_dagger": len(row["res_dag"]),
                "deep_record_short": bool(deep_record_s),
                "deep_record_dagger": bool(deep_record_d),
                "min_ep_short": (min(ep_list_s) if (deep_record_s and ep_list_s)
                                 else None),
                "min_ep_dagger": min_ep_d, "min_cheb_dagger": min_cheb_d,
                "d": d, "classe": classe, "ride": ride,
                "ride_periodi": (round(ride / P, 2) if ride is not None else None),
                "drift_dx": row["drift"][0], "drift_dy": row["drift"][1],
                "div_y_rel": div_info.get("y_rel"),
                "div_cheb": div_info.get("cheb"),
                "div_ep": div_info.get("ep"),
                "div_age": div_info.get("age"),
                "div_origine": div_info.get("origine"),
                "word": "".join("R" if b else "L" for b in w),
            })
        per_orbit.append(ob)
        print(f"[orb {od.index:2d}] record {ob['records']}: T={ob['T']} R={ob['R']} "
              f"E={ob['E']} ride_max={ob['ride_max']} "
              f"({time.time() - t_start:.0f}s)", flush=True)

    # ---- gate esterni ----
    assert n_records == sum(o["records_censiti"] for o in census["per_orbit"]), \
        "n record != §89a"
    assert tripwire_short == census["tripwire_checked"], "tripwire != §89a"
    assert guilty_tot_short == dyn["eta_colpevoli"]["n"], \
        f"somma G corta {guilty_tot_short} != §89b"
    assert da_seme_short == dyn["eta_colpevoli"]["da_seme"], \
        f"da_seme {da_seme_short} != §89b"
    for g in range(0, 11):
        assert G_all_short.count(g) == dyn["G"]["hist_low"][str(g)], \
            f"hist G({g}) != §89b"
    hist_me = {str(k): rec_min_ep_short.count(k) for k in sorted(set(rec_min_ep_short))}
    assert hist_me == supply["per_record_deep"]["min_ep"]["hist"], \
        f"hist min_ep corto != §98: {hist_me}"

    # ---- aggregati nuovi ----
    d_list = [r["d"] for r in rows_csv if r["d"] is not None]
    rides = [r["ride"] for r in rows_csv if r["classe"] == "R"]
    deep_rows = [r for r in rows_csv if r["deep_record_dagger"]]
    minep_d = [r["min_ep_dagger"] for r in deep_rows if r["min_ep_dagger"] is not None]
    mincheb = [r["min_cheb_dagger"] for r in rows_csv
               if r["min_cheb_dagger"] is not None]
    Gd_pos = [r["G_dagger"] for r in rows_csv]
    drift_up = sum(1 for r in rows_csv if r["drift_dy"] > 0)
    drift_down = sum(1 for r in rows_csv if r["drift_dy"] < 0)

    def hist_of(vals):
        h = {}
        for v in vals:
            h[v] = h.get(v, 0) + 1
        return {str(k): h[k] for k in sorted(h)}

    out = {
        "n_records": n_records,
        "classi": n_classe, "E_troncati": n_E_troncati,
        "tripwires": {"T_DIV_svolte_eq_celle": t_div,
                      "T_VDAGGER_G0_implica_ingresso": t_vdag,
                      "T_SCALA_divergenza": t_scala},
        "d": {"med": st.median(d_list), "max": max(d_list),
              "min": min(d_list)},
        "ride": {"n": len(rides), "med": st.median(rides) if rides else None,
                 "max": max(rides) if rides else None,
                 "frac_ge_P": sum(1 for v in rides if v >= P) / n_records,
                 "frac_ge_2P": sum(1 for v in rides if v >= 2 * P) / n_records,
                 "frac_ge_5P": sum(1 for v in rides if v >= 5 * P) / n_records,
                 "hist_periodi": hist_of([int(v // P) for v in rides])},
        "classe_R_frac": n_classe["R"] / n_records,
        "G_dagger": {"med": st.median(Gd_pos), "max": max(Gd_pos),
                     "zeri": sum(1 for v in Gd_pos if v == 0)},
        "min_ep_dagger": {"n": len(minep_d), "med": st.median(minep_d),
                          "max": max(minep_d), "hist": hist_of(minep_d)},
        "min_cheb_dagger": {"n": len(mincheb), "med": st.median(mincheb),
                            "max": max(mincheb), "hist": hist_of(mincheb)},
        "drift_germe": {"dy_pos_verso_visitato": drift_up,
                        "dy_neg_verso_vergine": drift_down,
                        "dy_zero": n_records - drift_up - drift_down},
        "per_orbit": per_orbit,
        "elapsed_s": round(time.time() - t_start, 1),
    }

    print(f"\nrecord {n_records}: classi {n_classe} (E troncati {n_E_troncati})",
          flush=True)
    print(f"tripwire: T-DIV {t_div}, T-VDAGGER {t_vdag}, T-SCALA {t_scala} "
          f"— zero violazioni", flush=True)
    print(f"d: med {out['d']['med']} min {out['d']['min']} max {out['d']['max']}",
          flush=True)
    print(f"RIDE (lock W0-like): n {out['ride']['n']} med {out['ride']['med']} "
          f"max {out['ride']['max']}; frac record con ride>=P "
          f"{out['ride']['frac_ge_P']:.4f}, >=2P {out['ride']['frac_ge_2P']:.4f}, "
          f">=5P {out['ride']['frac_ge_5P']:.4f}", flush=True)
    print(f"G_dagger: med {out['G_dagger']['med']} max {out['G_dagger']['max']} "
          f"zeri {out['G_dagger']['zeri']}", flush=True)
    print(f"min_ep_dagger (record interamente profondi alla daga, n={len(minep_d)}): "
          f"med {out['min_ep_dagger']['med']} max {out['min_ep_dagger']['max']} "
          f"hist {out['min_ep_dagger']['hist']}", flush=True)
    print(f"min_cheb_dagger: med {out['min_cheb_dagger']['med']} "
          f"max {out['min_cheb_dagger']['max']}", flush=True)
    print(f"drift germe: verso visitato {drift_up}, verso vergine {drift_down}",
          flush=True)

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    import csv
    with open(OUTCSV, "w", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(rows_csv[0].keys()))
        wcsv.writeheader()
        for r in rows_csv:
            wcsv.writerow(r)
    print(f"scritto {OUT} e {OUTCSV} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
