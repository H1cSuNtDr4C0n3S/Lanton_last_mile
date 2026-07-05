# record_minep_hunt.py — §99a: min_ep <= 5 e' STRUTTURA o CAMPIONE?
#
# §98 ha misurato min_ep <= 5 su 1174/1174 record profondi — ma sulle 24 orbite lunghe,
# SELEZIONATE per onset alto (trappola h: survivorship temporale). Qui la caccia al
# falsificatore su orbite NON selezionate: semi freschi riproducibili (catena xorshift
# dichiarata, stesso generatore di alpha1_engine.c / build_seed), corsa fino all'onset,
# stessi filtri di §98 (record y-min stretti, t < t_on, y < y_seed_min, t >= K=101,
# record interamente profondi), per ogni record profondo min_ep / min_age / min_lag.
#
# TESTIMONE = record profondo con min_ep > 5: se esiste, il "5" era campione (e il
# testimone va a verbale con parola e residuo); se su un campione largo e non
# selezionato non esiste, il "5" sale a candidato-struttura (resta empirico, trappola i).
#
# GATE (controllo positivo, obbligatorio prima della caccia): la stessa pipeline sui 24
# semi canonici deve riprodurre BIT-IDENTICI i per_orbit di §98
# (records, deep_records, colpevoli_profonde, ep_sum, ep_max, G_sum).
#
# Onesta' del campione: i semi senza onset entro il cap (1.5M) vengono CONTATI e
# dichiarati (0 attesi; un no-onset sarebbe esso stesso notizia); niente filtro
# sull'onset: si tiene TUTTO cio' che ha onset (il campione §98 aveva onset 250-313k,
# qui la mediana attesa e' ~10-30k: bias di selezione sterilizzato).
#
# Uscita: alpha1/record_minep_hunt_summary.json (+ .log via tee esterno)
import sys, os, json, time, bisect, argparse, statistics as st
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, xs, ALPHA
from onset_cone_lock import P
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_supply_census import replay_supply

HERE = os.path.dirname(os.path.abspath(__file__))
SUPPLY = os.path.join(HERE, "record_supply_census_summary.json")
OUT = os.path.join(HERE, "record_minep_hunt_summary.json")
K = 101
BASE = 0x9E3779B97F4A7C15          # catena semi: s0 = xs(xs(BASE)), s_{i+1} = xs(xs(s_i ^ GOLD))
GOLD = 0xBF58476D1CE4E5B9
BASE2 = None                        # catena-2 §100 (preregistrata a §99d): xs(BASE ^ 0xD1B54A32D192ED03)

_ev_cache = {}


def ev(w):
    r = _ev_cache.get(w, "MISS")
    if r == "MISS":
        r = eval_word(w)
        _ev_cache[w] = r
    return r


def fresh_states(n, base=None):
    s = xs(xs(BASE if base is None else base))
    out = []
    for _ in range(n):
        out.append(s)
        s = xs(xs(s ^ GOLD))
    return out


def orbit_stats(rngstate, collect_testimoni=True):
    """Pipeline §98 su un seme: ritorna dict con i campi per_orbit di §98 + minimi
    per-record profondo + eventuali testimoni min_ep > 5 (dettagli completi)."""
    seed, side, dens = build_seed(rngstate, 5, 25)
    if not seed:
        return {"rngstate": rngstate, "empty_seed": True}
    y_seed_min = min(cy for (_, cy) in seed)
    if y_seed_min > 0:
        # seme interamente sopra l'origine: le righe [0, y_seed_min) non sono
        # righe-record e la scala non si applica alle celle li' — scartato e contato
        return {"rngstate": rngstate, "empty_seed": True}
    turns, t_on, records = run_collect_records(seed)
    if t_on < 0:
        return {"rngstate": rngstate, "no_onset": True}
    rows_rec = [ry for (_, _, ry) in records]
    assert rows_rec == list(range(-1, -len(records) - 1, -1)), "scala non consecutiva"
    rec_times = [t for (t, _, _) in records]
    t_rec_of_row = {ry: t for (t, _, ry) in records}
    recs = [(t, x, y) for (t, x, y) in records
            if t < t_on and y < y_seed_min and t >= K]

    info = []
    queries = {}
    eval_none = 0
    for (t, rx, ry) in recs:
        r = ev(tuple(turns[t - K:t]))
        if r is None:
            eval_none += 1
            continue
        res_abs = [(rx + cx, ry + cy) for (cx, cy) in r[3]]
        kmax = max(cy for (cx, cy) in r[3]) if r[3] else 0
        info.append({"t": t, "pose": (rx, ry), "burden": r[0],
                     "onset_germe": r[1], "res_abs": res_abs, "kmax": kmax})
        queries[t] = set(res_abs)
    colors, first_row = replay_supply(seed, turns, queries)

    # T3 di §98 (terra): prima visita riga == record, entro l'orizzonte del replay
    t_horiz = max(queries) if queries else -1
    for (t_r, _, ry_r) in records:
        if t_r > t_horiz:
            continue
        assert first_row[ry_r] == t_r, f"T3: riga {ry_r} apre a {first_row[ry_r]} != {t_r}"

    ob = {"rngstate": rngstate, "onset": t_on, "records": 0, "deep_records": 0,
          "colpevoli_profonde": 0, "ep_sum": 0, "ep_max": 0, "G_sum": 0,
          "eval_none": eval_none, "mins": [], "testimoni": [], "g0_deep": []}
    for row in info:
        t = row["t"]
        rx, ry = row["pose"]
        got = colors[t]
        guilty = [c for c in row["res_abs"] if got[c][0] == 1]
        G = len(guilty)
        ob["records"] += 1
        ob["G_sum"] += G
        deep_record = (ry + row["kmax"] < y_seed_min)
        if deep_record:
            ob["deep_records"] += 1
        cell_vals = []
        for c in guilty:
            if c[1] >= y_seed_min:
                continue                  # cella shallow (record misto): come §98
            col, paint_t = got[c]
            y_rel = c[1] - ry
            assert c not in seed and paint_t is not None, "colpevole profonda anomala"
            t_row = t_rec_of_row[c[1]]
            assert paint_t >= t_row, "pittura prima dell'apertura riga"
            lo = bisect.bisect_right(rec_times, paint_t)
            hi = bisect.bisect_right(rec_times, t)
            ep = hi - lo
            assert 1 <= ep <= y_rel, "ep fuori scala"
            ob["colpevoli_profonde"] += 1
            ob["ep_sum"] += ep
            ob["ep_max"] = max(ob["ep_max"], ep)
            cell_vals.append((t - paint_t, ep, paint_t - t_row, c))
        if not deep_record:
            continue
        assert len(cell_vals) == G, "record profondo con colpevoli shallow?!"
        if not cell_vals:
            # record profondo a G=0: MAI silenzioso (riparazione pannello §99,
            # lente 2). Lontano dall'onset e' una VIOLAZIONE dell'orizzonte
            # V(onset+P) — il caveat 2 di §98c realizzato: censita, non assert.
            ob["g0_deep"].append({
                "t": t, "burden": row["burden"], "onset_germe": row["onset_germe"],
                "t_on_meno_t": t_on - t,
                "oltre_orizzonte": (t_on - t) > row["onset_germe"] + P})
            continue
        m_age = min(v[0] for v in cell_vals)
        m_ep = min(v[1] for v in cell_vals)
        m_lag = min(v[2] for v in cell_vals)
        ob["mins"].append((m_ep, m_age, m_lag))
        if collect_testimoni and m_ep > 5:
            word = "".join("R" if b else "L" for b in turns[t - K:t])
            i_rec = bisect.bisect_right(rec_times, t) - 1
            dt_burst = [rec_times[j] - rec_times[j - 1]
                        for j in range(max(1, i_rec - 8), i_rec + 1)]
            ob["testimoni"].append({
                "rngstate": rngstate, "t": t, "t_on": t_on, "pose": [rx, ry],
                "min_ep": m_ep, "min_age": m_age, "min_lag": m_lag, "G": G,
                "burden": row["burden"], "word": word, "dt_burst": dt_burst,
                "guilty": [{"cella": list(c), "ep": ep_, "age": age_, "lag": lag_}
                           for (age_, ep_, lag_, c) in sorted(cell_vals,
                                                              key=lambda v: v[1])[:12]]})
    return ob


def _worker(rngstate):
    try:
        return orbit_stats(rngstate)
    except AssertionError as e:
        return {"rngstate": rngstate, "assert_error": str(e)}


def gate_canonici():
    """Controllo positivo: pipeline bit-identica ai per_orbit di §98 + istogramma
    per-record min_ep (riparazione pannello §99: le somme non bastano, un bug dei
    minimi che le preservi passerebbe) + zero G=0 profondi sui canonici."""
    supply = json.load(open(SUPPLY))
    ref = supply["per_orbit"]
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    minep_hist = {}
    n_g0 = 0
    for od, rref in zip(dumps, ref):
        ob = orbit_stats(od.rngstate, collect_testimoni=True)
        assert ob["onset"] == od.onset_header, f"orb {od.index}: onset != header"
        for k in ("records", "deep_records", "colpevoli_profonde", "ep_sum",
                  "ep_max", "G_sum"):
            assert ob[k] == rref[k], (f"orb {od.index}: {k} {ob[k]} != §98 {rref[k]}")
        assert not ob["testimoni"], f"orb {od.index}: testimone nei canonici?!"
        n_g0 += len(ob["g0_deep"])
        for (m_ep, _, _) in ob["mins"]:
            minep_hist[str(m_ep)] = minep_hist.get(str(m_ep), 0) + 1
    ref_hist = supply["per_record_deep"]["min_ep"]["hist"]
    assert minep_hist == ref_hist, f"hist min_ep {minep_hist} != §98 {ref_hist}"
    assert n_g0 == 0, f"G=0 profondi nei canonici: {n_g0} (§98 ne aveva 0)"
    print(f"GATE canonici: 24/24 orbite bit-identiche a §98 (6 campi + hist "
          f"per-record min_ep {ref_hist}), zero testimoni, zero G=0 profondi",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-seeds", type=int, default=600)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--skip-gate", action="store_true")
    ap.add_argument("--chain2", action="store_true",
                    help="§100: catena semi DISGIUNTA preregistrata a §99d "
                         "(BASE2 = xs(BASE ^ 0xD1B54A32D192ED03)); output separato; "
                         "verdetto preregistrato coda doppia (min_ep>8 E min_age>1040)")
    args = ap.parse_args()
    t0 = time.time()

    if not args.skip_gate:
        gate_canonici()

    if args.chain2:
        base2 = xs(BASE ^ 0xD1B54A32D192ED03)
        states = fresh_states(args.n_seeds, base=base2)
        # disgiunzione dichiarata e VERIFICATA contro la catena-1 di §99 (5000 semi)
        overlap = set(states) & set(fresh_states(5000))
        assert not overlap, f"catene NON disgiunte: {len(overlap)} collisioni"
        print(f"catena-2 (BASE2={base2}): {args.n_seeds} semi, disgiunzione "
              f"verificata contro i 5000 di §99", flush=True)
    else:
        states = fresh_states(args.n_seeds)
    if args.workers > 1:
        with mp.Pool(args.workers) as pool:
            results = pool.map(_worker, states, chunksize=4)
    else:
        results = [_worker(s) for s in states]

    no_onset = [r["rngstate"] for r in results if r.get("no_onset")]
    empty = [r for r in results if r.get("empty_seed")]
    errors = [r for r in results if r.get("assert_error")]
    ok = [r for r in results if "records" in r]
    assert not errors, f"assert nei worker: {errors[:3]}"

    onsets = [r["onset"] for r in ok]
    mins = [v for r in ok for v in r["mins"]]
    min_ep_all = [v[0] for v in mins]
    min_age_all = [v[1] for v in mins]
    min_lag_all = [v[2] for v in mins]
    testimoni = [tst for r in ok for tst in r["testimoni"]]
    n_deep = sum(r["deep_records"] for r in ok)
    n_rec = sum(r["records"] for r in ok)
    eval_none = sum(r["eval_none"] for r in ok)
    g0_deep = [dict(g, rngstate=r["rngstate"], onset=r["onset"])
               for r in ok for g in r["g0_deep"]]
    violazioni = [g for g in g0_deep if g["oltre_orizzonte"]]

    hist_minep = {str(k): min_ep_all.count(k) for k in sorted(set(min_ep_all))}
    nn = len(min_ep_all)
    out = {
        "n_seeds": args.n_seeds, "no_onset": len(no_onset), "empty_seed": len(empty),
        "orbite_ok": len(ok), "eval_none": eval_none,
        "onset": {"med": st.median(onsets), "min": min(onsets), "max": max(onsets)},
        "records_censiti": n_rec, "deep_records": n_deep,
        "deep_con_colpevoli": nn, "deep_G0": len(g0_deep),
        "VIOLAZIONI_ORIZZONTE": violazioni,
        "g0_entro_orizzonte": len(g0_deep) - len(violazioni),
        "min_ep": {"hist": hist_minep,
                   "max": max(min_ep_all) if min_ep_all else None,
                   "med": st.median(min_ep_all) if min_ep_all else None},
        "min_age": {"med": st.median(min_age_all) if min_age_all else None,
                    "max": max(min_age_all) if min_age_all else None,
                    "frac_le_2K": (sum(1 for a in min_age_all if a <= 2 * K) / nn)
                    if nn else None},
        "min_lag": {"med": st.median(min_lag_all) if min_lag_all else None,
                    "frac_le_P": (sum(1 for v in min_lag_all if v <= P) / nn)
                    if nn else None},
        "coda_doppia": {
            "n_ep_gt5": sum(1 for v in mins if v[0] > 5),
            "n_ep_gt5_age_gt2K": sum(1 for v in mins if v[0] > 5 and v[1] > 2 * K),
            "n_ep_gt5_age_gt5P": sum(1 for v in mins if v[0] > 5 and v[1] > 5 * P),
            "n_ep_gt5_age_gt10P": sum(1 for v in mins if v[0] > 5 and v[1] > 10 * P)},
        "TESTIMONI_minep_gt5": testimoni,
        "elapsed_s": round(time.time() - t0, 1)}

    if args.chain2:
        # ---- VERDETTO PREREGISTRATO §99d (fissato PRIMA di questa run) ----
        n_fals = sum(1 for v in mins if v[0] > 8 and v[1] > 10 * P)
        n_pow = sum(1 for v in mins if v[0] > 5)
        if n_fals > 0:
            verdetto = "CODA DOPPIA REALIZZATA (falsificata la candidata-struttura)"
        elif n_pow >= 20:
            verdetto = ("VUOTA CON POTENZA (candidata-struttura: ep>8 => age<=10P; "
                        "resta empirica, trappola i)")
        else:
            verdetto = f"SOTTOPOTENZIATO (testimoni ep>5 = {n_pow} < 20)"
        out["PREREGISTRATO"] = {
            "falsificatore": "record profondo G>=1 con min_ep>8 E min_age>1040",
            "n_falsificatori": n_fals, "n_testimoni_ep_gt5": n_pow,
            "soglia_potenza": 20, "verdetto": verdetto}
        # parole ripetute (gamba 3): confronto interno + vs catena-1 §99
        words2 = [t["word"] for t in testimoni]
        rep_int = len(words2) - len(set(words2))
        words1 = []
        if os.path.exists(OUT):
            try:
                words1 = [t["word"] for t in
                          json.load(open(OUT))["TESTIMONI_minep_gt5"]]
            except Exception:
                pass
        cross = sorted(set(words2) & set(words1))
        out["parole_ripetute"] = {
            "n_testimoni": len(words2), "distinte": len(set(words2)),
            "ripetizioni_interne": rep_int,
            "in_comune_con_catena1": len(cross), "parole_comuni": cross}

    print(f"semi {args.n_seeds}: ok {len(ok)}, no-onset {len(no_onset)}, "
          f"vuoti {len(empty)}; onset med {out['onset']['med']} "
          f"[{out['onset']['min']}..{out['onset']['max']}]", flush=True)
    print(f"record censiti {n_rec}, profondi {n_deep} (con colpevoli {nn}, "
          f"G=0 {len(g0_deep)} di cui OLTRE-ORIZZONTE {len(violazioni)})", flush=True)
    for v in violazioni[:8]:
        print(f"  ORIZZONTE: rngstate {v['rngstate']} t={v['t']} burden={v['burden']} "
              f"t_on-t={v['t_on_meno_t']} >> {v['onset_germe']}+P", flush=True)
    print(f"min_ep: hist {hist_minep} MAX {out['min_ep']['max']}", flush=True)
    print(f"min_age: med {out['min_age']['med']} frac<=2K "
          f"{out['min_age']['frac_le_2K']}", flush=True)
    print(f"min_lag: med {out['min_lag']['med']} frac<=P "
          f"{out['min_lag']['frac_le_P']}", flush=True)
    print(f"CODA DOPPIA: ep>5 {out['coda_doppia']['n_ep_gt5']}; "
          f"& age>2K {out['coda_doppia']['n_ep_gt5_age_gt2K']}; "
          f"& age>5P {out['coda_doppia']['n_ep_gt5_age_gt5P']}; "
          f"& age>10P {out['coda_doppia']['n_ep_gt5_age_gt10P']}", flush=True)
    print(f"TESTIMONI min_ep>5: {len(testimoni)}", flush=True)
    for tst in testimoni[:30]:
        print(f"  !!! rngstate {tst['rngstate']} t={tst['t']} min_ep={tst['min_ep']} "
              f"min_age={tst['min_age']} G={tst['G']} burden={tst['burden']}", flush=True)
    if args.chain2:
        print(f"VERDETTO PREREGISTRATO: {out['PREREGISTRATO']['verdetto']} "
              f"(falsificatori {out['PREREGISTRATO']['n_falsificatori']}, "
              f"testimoni ep>5 {out['PREREGISTRATO']['n_testimoni_ep_gt5']})", flush=True)
        print(f"parole ripetute: {out['parole_ripetute']['n_testimoni']} testimoni, "
              f"{out['parole_ripetute']['distinte']} distinte, comuni con catena-1 "
              f"{out['parole_ripetute']['in_comune_con_catena1']}", flush=True)
    path_out = OUT.replace(".json", "2.json") if args.chain2 else OUT
    with open(path_out, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path_out} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
