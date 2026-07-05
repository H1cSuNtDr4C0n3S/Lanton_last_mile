# record_supply_census.py — §98a: l'ANELLO DI OCCORRENZA in unita' di EPOCHE-RECORD.
#
# Contesto (scala a Link 1, §91c punto 4): il Muro vieta w101 ai record lontani, ma
# nessuna orbita la presenta (0/1639, §89a). La cattura richiede una famiglia
# INEVITABILE ai record. §89a ha riformulato l'osservabile: il conteggio delle
# colpevoli G. Qui si cambia UNITA' DI MISURA: non i passi, le EPOCHE-RECORD.
#
# LEMMA DELLA SCALA (deduttivo, §98a). A un record y-min stretto la posa e' alla riga
# y_min-1 mai visitata prima; i record scendono di UNA riga alla volta (mosse unitarie)
# => la riga assoluta -m (m>=1) e' visitata per la PRIMA volta esattamente al record
# di indice m-1 della scala. Corollario: a un record censito (riga sotto il seme), ogni
# cella-residuo con riga assoluta r < y_seed_min:
#   (i)  non e' cella di SEME (il seme vive a righe >= y_seed_min): se e' nera, e' stata
#        DIPINTA dall'orbita (ultima visita = svolta R) — AUTOFORNITURA;
#   (ii) la sua riga e' stata aperta al record della riga => paint_t >= t_record(riga);
#   (iii) in epoche: il numero di record in (paint_t, t] e' <= y_rel della cella.
# => TUTTO il rifornimento dei record profondi e' auto-dipinto NELLE ULTIME k_max
# epoche-record (k_max = estensione verticale del residuo), qualunque sia l'eta' in
# passi. La "pre-semina antica" ai record profondi NON ESISTE come risorsa separata:
# esiste solo il rifornimento continuo, epoca per epoca.
#
# Censimento (24 orbite, stessi 1639 record e stesso K=101 di §89a/b, gate incrociati):
#   - tripwire T1 (autofornitura): cella-colpevole profonda mai di seme, sempre dipinta;
#   - tripwire T2 (scala, passi): paint_t >= t_record(riga della cella);
#   - tripwire T3 (terra): prima visita della riga -m == t del record m-1 (misurata nel
#     replay, non assunta);
#   - tripwire T4 (scala, epoche): #record in (paint_t, t] <= y_rel;
#   - MISURE: distribuzione di ep (eta' in epoche), y_rel, k_max per record, lag di
#     pittura dalla apertura della riga (paint_t - t_record(riga)): quota "discesa"
#     (<= P) vs "escursione" (>> P), eta' in passi (confronto §89b), G ai record
#     interamente profondi (dove l'autofornitura e' totale).
#
# Gate esterni: n record, tripwire count == §89a; n colpevoli, da_seme, hist G == §89b.
# Uscita: alpha1/record_supply_census_summary.json
import sys, os, json, time, bisect, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import P
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "record_word_census_summary.json")
DYN = os.path.join(HERE, "record_guilty_dynamics_summary.json")
OUT = os.path.join(HERE, "record_supply_census_summary.json")
K = 101
DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)


def replay_supply(seed, turns_ref, queries):
    """Replay deterministico. queries: {t: iterable celle assolute}.
    Ritorna (out, first_row): out {t: {cella: (colore, paint_t|None)}} con paint_t =
    ultima scrittura a NERO al tempo della query; first_row {riga: prima t con posa
    sulla riga} per ogni riga visitata (righe < 0 comprese). Tripwire: svolte == ref."""
    out = {}
    grid = {}
    paint_black = {}
    first_row = {}
    x = y = 0
    h = 0
    t_max = max(queries) if queries else -1
    for t in range(t_max + 1):
        if y not in first_row:
            first_row[y] = t
        if t in queries:
            out[t] = {}
            for c in queries[t]:
                col = grid[c] if c in grid else (1 if c in seed else 0)
                out[t][c] = (col, paint_black.get(c))
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns_ref[t], f"replay diverge a t={t}"
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
            paint_black[c] = t
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += DX[h]
        y += DY[h]
    return out, first_row


def main():
    t_start = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    census = json.load(open(CENSUS))
    dyn = json.load(open(DYN))
    ev_cache = {}

    def ev(w):
        r = ev_cache.get(w, "MISS")
        if r == "MISS":
            r = eval_word(w)
            ev_cache[w] = r
        return r

    n_records = 0
    tripwire = 0
    n_deep_records = 0          # record con TUTTE le righe-residuo sotto il seme
    G_all = []
    G_deep_records = []
    guilty_tot = 0
    guilty_deep = 0
    guilty_shallow_seed = 0
    guilty_shallow_paint = 0
    ep_hist = {}                # eta' in epoche (record in (paint_t, t]), celle profonde
    yrel_hist = {}
    kmax_list = []              # estensione verticale del residuo per record
    lag_list = []               # paint_t - t_record(riga), celle profonde
    esp_frac = []               # (ep-1)/(y_rel-1) se y_rel>1: 1=pittura all'apertura
    q_hist = {}                 # quota di rientro alla pittura (righe sopra il minimo)
    age_deep = []
    # per-record (SOLO record interamente profondi): minimi sulle colpevoli
    # — riparazione pannello §98e (lente C): il no-go va giudicato a livello
    # ESISTE->=1-per-record, non sulle frazioni per-cella
    rec_min_age = []
    rec_min_ep = []
    rec_min_lag = []
    ages_all = []               # per gate §89b (tutte le colpevoli, None=seme)
    lag_le_P = 0
    lag_le_2P = 0
    lag_le_10P = 0
    t1 = t2 = t3 = t4 = 0       # tripwire superati
    per_orbit = []              # per la lente indipendente del pannello

    for od in dumps:
        seed, side, dens = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        assert y_seed_min <= 0, f"orb {od.index}: seme tutto sopra l'origine?!"
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header, f"orb {od.index}: onset != header"
        # scala: righe dei record consecutive -1,-2,...
        rows_rec = [ry for (_, _, ry) in records]
        assert rows_rec == list(range(-1, -len(records) - 1, -1)), \
            f"orb {od.index}: scala non consecutiva"
        rec_times = [t for (t, _, _) in records]
        t_rec_of_row = {ry: t for (t, _, ry) in records}

        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]

        info = []
        queries = {}
        for (t, rx, ry) in recs:
            r = ev(tuple(turns[t - K:t]))
            assert r is not None
            res_abs = [(rx + cx, ry + cy) for (cx, cy) in r[3]]
            kmax = max(cy for (cx, cy) in r[3])
            info.append({"t": t, "pose": (rx, ry), "burden": r[0],
                         "onset_germe": r[1], "res_abs": res_abs, "kmax": kmax})
            queries[t] = set(res_abs)
        colors, first_row = replay_supply(seed, turns, queries)

        # T3 (terra): prima visita della riga -m == t del record m-1, per ogni riga < 0
        # entro l'orizzonte del replay (il replay si ferma all'ultima query)
        t_horiz = max(queries) if queries else -1
        for (t_r, _, ry) in records:
            if t_r > t_horiz:
                continue
            assert first_row[ry] == t_r, \
                f"orb {od.index}: riga {ry} prima visita {first_row[ry]} != record {t_r}"
            t3 += 1

        ob = {"orbit": od.index, "records": 0, "deep_records": 0,
              "colpevoli_profonde": 0, "ep_sum": 0, "ep_max": 0, "G_sum": 0}
        for row in info:
            t = row["t"]
            rx, ry = row["pose"]
            got = colors[t]
            guilty = [c for c in row["res_abs"] if got[c][0] == 1]
            G = len(guilty)
            n_records += 1
            G_all.append(G)
            kmax_list.append(row["kmax"])
            ob["records"] += 1
            ob["G_sum"] += G
            deep_record = (ry + row["kmax"] < y_seed_min)
            if deep_record:
                n_deep_records += 1
                G_deep_records.append(G)
                ob["deep_records"] += 1
            if t_on - t > row["onset_germe"] + P:
                tripwire += 1
                assert G >= 1, f"ROSSO orb {od.index} t={t}: residuo tutto bianco"
            cell_vals = []      # (age, ep, lag) delle colpevoli profonde del record
            for c in guilty:
                guilty_tot += 1
                col, paint_t = got[c]
                y_rel = c[1] - ry
                assert y_rel >= 1
                ages_all.append((t - paint_t) if paint_t is not None else None)
                if c[1] < y_seed_min:
                    # cella PROFONDA: lemma della scala attivo
                    guilty_deep += 1
                    assert c not in seed and paint_t is not None, \
                        f"orb {od.index} t={t}: colpevole profonda {c} di seme?!"
                    t1 += 1
                    t_row = t_rec_of_row[c[1]]
                    assert paint_t >= t_row, \
                        f"orb {od.index} t={t}: paint {paint_t} < apertura riga {t_row}"
                    t2 += 1
                    lo = bisect.bisect_right(rec_times, paint_t)
                    hi = bisect.bisect_right(rec_times, t)
                    ep = hi - lo          # record in (paint_t, t]
                    assert 1 <= ep <= y_rel, \
                        f"orb {od.index} t={t}: ep {ep} fuori [1,{y_rel}]"
                    t4 += 1
                    ob["colpevoli_profonde"] += 1
                    ob["ep_sum"] += ep
                    ob["ep_max"] = max(ob["ep_max"], ep)
                    ep_hist[ep] = ep_hist.get(ep, 0) + 1
                    yrel_hist[y_rel] = yrel_hist.get(y_rel, 0) + 1
                    lag = paint_t - t_row
                    lag_list.append(lag)
                    if lag <= P:
                        lag_le_P += 1
                    if lag <= 2 * P:
                        lag_le_2P += 1
                    if lag <= 10 * P:
                        lag_le_10P += 1
                    if y_rel > 1:
                        esp_frac.append((ep - 1) / (y_rel - 1))
                    age_deep.append(t - paint_t)
                    # quota di rientro: altezza della riga dipinta sopra il minimo
                    # corrente al momento della pittura (y_min(tau) = -#record <= tau)
                    ymin_at_paint = -bisect.bisect_right(rec_times, paint_t)
                    q = c[1] - ymin_at_paint
                    assert q >= 0, f"pittura sotto il minimo corrente?! q={q}"
                    q_hist[q] = q_hist.get(q, 0) + 1
                    cell_vals.append((t - paint_t, ep, lag))
                else:
                    if paint_t is None:
                        guilty_shallow_seed += 1
                    else:
                        guilty_shallow_paint += 1
            if deep_record:
                # record interamente profondo => tutte le colpevoli sono profonde
                assert len(cell_vals) == G
                rec_min_age.append(min(v[0] for v in cell_vals))
                rec_min_ep.append(min(v[1] for v in cell_vals))
                rec_min_lag.append(min(v[2] for v in cell_vals))
        per_orbit.append(ob)
        print(f"[orb {od.index:2d}] record {ob['records']} (profondi "
              f"{ob['deep_records']}) colpevoli-profonde {ob['colpevoli_profonde']} "
              f"ep_max {ob['ep_max']}", flush=True)

    # ---- gate esterni: §89a e §89b devono essere riprodotti esattamente ----
    assert n_records == sum(o["records_censiti"] for o in census["per_orbit"]), \
        "n record != §89a"
    assert tripwire == census["tripwire_checked"], "tripwire != §89a"
    assert guilty_tot == dyn["eta_colpevoli"]["n"], \
        f"n colpevoli {guilty_tot} != §89b {dyn['eta_colpevoli']['n']}"
    assert guilty_shallow_seed == dyn["eta_colpevoli"]["da_seme"], \
        f"da_seme {guilty_shallow_seed} != §89b {dyn['eta_colpevoli']['da_seme']}"
    for g in range(0, 11):
        assert G_all.count(g) == dyn["G"]["hist_low"][str(g)], f"hist G({g}) != §89b"
    aa = [a for a in ages_all if a is not None]
    assert st.median(aa) == dyn["eta_colpevoli"]["med"] and max(aa) == \
        dyn["eta_colpevoli"]["max"], "eta' (med,max) != §89b"

    nd = guilty_deep
    out = {
        "n_records": n_records, "n_deep_records": n_deep_records,
        "tripwire_G": tripwire,
        "tripwires": {"T1_autofornitura": t1, "T2_paint_dopo_apertura": t2,
                      "T3_prima_visita_riga_eq_record": t3, "T4_ep_le_yrel": t4},
        "colpevoli": {"tot": guilty_tot, "profonde": guilty_deep,
                      "shallow_seme": guilty_shallow_seed,
                      "shallow_dipinte": guilty_shallow_paint},
        "kmax_residuo": {"med": st.median(kmax_list), "max": max(kmax_list)},
        "G_deep_records": {"n": len(G_deep_records),
                           "min": min(G_deep_records) if G_deep_records else None,
                           "med": st.median(G_deep_records) if G_deep_records else None},
        "ep": {"med": st.median([e for e, n in ep_hist.items() for _ in range(n)]),
               "max": max(ep_hist), "hist": {str(k): v for k, v in sorted(ep_hist.items())}},
        "y_rel": {"med": st.median([e for e, n in yrel_hist.items() for _ in range(n)]),
                  "max": max(yrel_hist),
                  "hist_low": {str(k): yrel_hist.get(k, 0) for k in range(1, 16)}},
        "lag_pittura_da_apertura_riga": {
            "med": st.median(lag_list), "max": max(lag_list),
            "frac_le_P": lag_le_P / nd, "frac_le_2P": lag_le_2P / nd,
            "frac_le_10P": lag_le_10P / nd},
        "esp_frac_apertura": {"med": st.median(esp_frac),
                              "frac_eq_1": sum(1 for v in esp_frac if v == 1.0) / len(esp_frac)},
        "eta_passi_profonde": {"med": st.median(age_deep), "max": max(age_deep),
                               "frac_ge_10P": sum(1 for a in age_deep if a >= 10 * P) / nd,
                               "frac_le_2K": sum(1 for a in age_deep if a <= 2 * K) / nd,
                               "frac_le_5P": sum(1 for a in age_deep if a <= 5 * P) / nd},
        "ep_cum": {str(m): sum(v for k, v in ep_hist.items() if k <= m) / nd
                   for m in (1, 2, 3, 5, 8, 13, 21, 31)},
        "quota_rientro": {"med": st.median([k for k, n in q_hist.items()
                                            for _ in range(n)]),
                          "max": max(q_hist), "min": min(q_hist),
                          "cum": {str(m): sum(v for k, v in q_hist.items()
                                              if k <= m) / nd
                                  for m in (1, 3, 5, 8, 13, 21, 34, 55)}},
        "per_record_deep": {
            "n": len(rec_min_age),
            "min_age": {"med": st.median(rec_min_age), "max": max(rec_min_age),
                        "frac_le_2K": sum(1 for a in rec_min_age if a <= 2 * K)
                        / len(rec_min_age),
                        "frac_le_5P": sum(1 for a in rec_min_age if a <= 5 * P)
                        / len(rec_min_age),
                        "frac_le_10P": sum(1 for a in rec_min_age if a <= 10 * P)
                        / len(rec_min_age)},
            "min_ep": {"med": st.median(rec_min_ep), "max": max(rec_min_ep),
                       "hist": {str(k): rec_min_ep.count(k)
                                for k in sorted(set(rec_min_ep))}},
            "min_lag": {"med": st.median(rec_min_lag),
                        "frac_le_P": sum(1 for v in rec_min_lag if v <= P)
                        / len(rec_min_lag),
                        "frac_le_10P": sum(1 for v in rec_min_lag if v <= 10 * P)
                        / len(rec_min_lag)}},
        "per_orbit": per_orbit,
        "elapsed_s": round(time.time() - t_start, 1)}

    print(f"record {n_records} (profondi {n_deep_records}), tripwire G {tripwire}; "
          f"T1={t1} T2={t2} T3={t3} T4={t4} — zero violazioni", flush=True)
    print(f"colpevoli {guilty_tot}: profonde {guilty_deep}, shallow-seme "
          f"{guilty_shallow_seed}, shallow-dipinte {guilty_shallow_paint}", flush=True)
    print(f"k_max residuo: med {out['kmax_residuo']['med']} max {out['kmax_residuo']['max']}",
          flush=True)
    print(f"ETA' IN EPOCHE (profonde): med {out['ep']['med']} max {out['ep']['max']}",
          flush=True)
    print(f"y_rel: med {out['y_rel']['med']} max {out['y_rel']['max']}", flush=True)
    print(f"lag pittura da apertura riga: med {out['lag_pittura_da_apertura_riga']['med']} "
          f"max {out['lag_pittura_da_apertura_riga']['max']}; <=P "
          f"{out['lag_pittura_da_apertura_riga']['frac_le_P']:.3f}, <=2P "
          f"{out['lag_pittura_da_apertura_riga']['frac_le_2P']:.3f}, <=10P "
          f"{out['lag_pittura_da_apertura_riga']['frac_le_10P']:.3f}", flush=True)
    print(f"esp (pittura all'apertura=1): med {out['esp_frac_apertura']['med']:.3f}, "
          f"frac==1 {out['esp_frac_apertura']['frac_eq_1']:.3f}", flush=True)
    print(f"eta' in passi (profonde): med {out['eta_passi_profonde']['med']} "
          f"max {out['eta_passi_profonde']['max']} >=10P "
          f"{out['eta_passi_profonde']['frac_ge_10P']:.3f}", flush=True)
    print(f"G ai record profondi: n {out['G_deep_records']['n']} min "
          f"{out['G_deep_records']['min']} med {out['G_deep_records']['med']}", flush=True)
    print(f"QUOTA DI RIENTRO alla pittura: med {out['quota_rientro']['med']} "
          f"min {out['quota_rientro']['min']} max {out['quota_rientro']['max']}; "
          f"cum {out['quota_rientro']['cum']}", flush=True)
    prd = out["per_record_deep"]
    print(f"PER-RECORD (n={prd['n']} profondi): min_age med {prd['min_age']['med']} "
          f"max {prd['min_age']['max']}; ha-giovane<=2K {prd['min_age']['frac_le_2K']:.3f}, "
          f"<=5P {prd['min_age']['frac_le_5P']:.3f}, <=10P {prd['min_age']['frac_le_10P']:.3f}",
          flush=True)
    print(f"PER-RECORD min_ep: med {prd['min_ep']['med']} max {prd['min_ep']['max']} "
          f"hist {prd['min_ep']['hist']}", flush=True)
    print(f"PER-RECORD min_lag: med {prd['min_lag']['med']}; ha-discesa<=P "
          f"{prd['min_lag']['frac_le_P']:.3f}, <=10P {prd['min_lag']['frac_le_10P']:.3f}",
          flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
