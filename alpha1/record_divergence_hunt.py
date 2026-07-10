# record_divergence_hunt.py — §101b: caccia preregistrata al bordo spaziale e ai lock.
#
# ============================ PREREGISTRAZIONE (§101, fissata PRIMA della run) ============
# Il censimento §101a (record_divergence_census.py, 24 orbite canoniche) misura:
#   min_cheb-dagger <= 8 su 1639/1639 (med 3);  classe T su 1639/1639 (zero ride);
#   min_ep-dagger <= 5 su 813/813.
# Trappola (qq): le soglie dell'orologio-record sono quantili con data di scadenza.
# Caccia su semi freschi NON selezionati, catena-3 DISGIUNTA dalle catene 1 (§99) e 2 (§100):
#   BASE3 = xs(BASE ^ 0x94D049BB133111EB), s0 = xs(xs(BASE3)), s_{i+1} = xs(xs(s_i ^ GOLD)).
#
# FALSIFICATORI (dichiarati con aspettativa):
#   F1 (bordo spaziale): record con G_dagger>=1 e min_cheb_dagger > 8.
#      ASPETTATIVA: MORTE del bordo (i violatori d'orizzonte §99 divergono a cheb 21/25).
#   F2 (lock ai record): record di classe R con ride = d - onset_germe >= P (un periodo
#      pieno di cavalcata W0 reale). ASPETTATIVA: raro ma >0 (tasso ~7e-5 dai §99).
#   P3 (predizione sulla classe dei falsificatori, falsificabile): ogni falsificatore F1
#      ha classe R oppure min_ep_dagger >= 4 (fascia alta §100 = ingressi mancati).
#   V-DAGGER (tripwire, mai silenzioso — trappola pp): record profondo con G_dagger = 0
#      e t_on - t > t_dagger = violazione del Replay-Lock alla V-daga: CENSITA e riportata
#      (0 attese; una violazione qui e' un ROSSO di teoria, non di campione).
#
# POTENZA ASSERITA: >= 5000 record con G_dagger>=1 censiti; sotto, dichiarare
# SOTTOPOTENZA (nessun verdetto). Default 8000 semi (~2x i record di §99).
#
# GATE (controllo positivo, obbligatorio): la stessa pipeline sui 24 semi canonici deve
# riprodurre BIT-IDENTICI i per_orbit del censimento §101a (records/T/R/E/ride_max/
# G_dag_sum) e gli istogrammi globali min_cheb_dagger e min_ep_dagger.
# ==========================================================================================
#
# Uscita: alpha1/record_divergence_hunt_summary.json (+ .log via tee esterno)
import sys, os, json, time, bisect, argparse, statistics as st
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, xs, ALPHA
from onset_cone_lock import DX, DY, P, simulate
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_supply_census import replay_supply

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS101 = os.path.join(HERE, "record_divergence_census_summary.json")
OUT = os.path.join(HERE, "record_divergence_hunt_summary.json")
K = 101
BASE = 0x9E3779B97F4A7C15
GOLD = 0xBF58476D1CE4E5B9
MASK = (1 << 64) - 1


def fresh_states(n, base=None):
    s = xs(xs(BASE if base is None else base))
    out = []
    for _ in range(n):
        out.append(s)
        s = xs(xs(s ^ GOLD))
    return out


def germ_run_light(word, onset_germe):
    """Corsa lunga del germe senza trattenere la traiettoria (RAM, trappola g).
    Ritorna (gturns, fr, t_dagger, footprint)."""
    vg, pose = virtual_walk(word)
    assert vg is not None
    anchor = to_anchor_frame(vg, pose)
    germ_black = {c for c, col in anchor.items() if col == 1}
    t_dagger = max(2600, onset_germe + 2080)
    gturns, n, _, fr, _ = simulate(germ_black, 0, 0, 0, t_dagger,
                                   stop_at_onset=False, chk=t_dagger + 1)
    assert n == t_dagger
    return gturns, fr, t_dagger, set(anchor)


def walk_to(gturns, d):
    x = y = 0
    h = 0
    for i in range(d + 1):
        if i == d:
            return x, y
        if gturns[i]:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
    return x, y


def orbit_divergence(rngstate):
    """Pipeline §101a su un seme fresco. Cache germi PER-SEME (reset a fine seme)."""
    seed, side, dens = build_seed(rngstate, 5, 25)
    if not seed:
        return {"rngstate": rngstate, "empty_seed": True}
    y_seed_min = min(cy for (_, cy) in seed)
    if y_seed_min > 0:
        return {"rngstate": rngstate, "empty_seed": True}
    turns, t_on, records = run_collect_records(seed)
    if t_on < 0:
        return {"rngstate": rngstate, "no_onset": True}
    n_real = len(turns)
    rows_rec = [ry for (_, _, ry) in records]
    assert rows_rec == list(range(-1, -len(records) - 1, -1)), "scala non consecutiva"
    rec_times = [t for (t, _, _) in records]
    recs = [(t, x, y) for (t, x, y) in records
            if t < t_on and y < y_seed_min and t >= K]

    ev_cache = {}
    germ_cache = {}

    info = []
    queries = {}
    eval_none = 0
    for (t, rx, ry) in recs:
        w = tuple(turns[t - K:t])
        r = ev_cache.get(w, "MISS")
        if r == "MISS":
            r = eval_word(w)
            ev_cache[w] = r
        if r is None:
            eval_none += 1
            continue
        g = germ_cache.get(w)
        if g is None:
            g = germ_run_light(w, r[1])
            germ_cache[w] = g
        gturns, fr, t_dag, footprint = g
        res_dag = [c for c, (tf, _) in fr.items()
                   if tf < t_dag and c not in footprint and c[1] >= 1]
        info.append({"t": t, "pose": (rx, ry), "word": w, "burden": r[0],
                     "onset_germe": r[1], "res_dag": res_dag, "t_dag": t_dag})
        queries[t] = {(rx + cx, ry + cy) for (cx, cy) in res_dag}
    colors, first_row = replay_supply(seed, turns, queries)

    ob = {"rngstate": rngstate, "onset": t_on, "records": 0,
          "T": 0, "R": 0, "E": 0, "ride_max": 0, "G_dag_sum": 0,
          "eval_none": eval_none, "rows": [], "F1": [], "F2": [],
          "vdagger_violazioni": [], "g0_fisiologici": 0}
    for row in info:
        t = row["t"]
        rx, ry = row["pose"]
        w = row["word"]
        gturns, fr, t_dag, footprint = germ_cache[w]
        onset_germe = row["onset_germe"]
        got = colors[t]
        ob["records"] += 1

        guilty_dag = []
        for (cx, cy) in row["res_dag"]:
            ca = (rx + cx, ry + cy)
            col, paint_t = got[ca]
            if col == 1:
                guilty_dag.append(((cx, cy), fr[(cx, cy)][0], paint_t))
        Gd = len(guilty_dag)
        ob["G_dag_sum"] += Gd
        kmax_d = max((cy for (cx, cy) in row["res_dag"]), default=0)
        deep_dag = (ry + kmax_d < y_seed_min) and bool(row["res_dag"])
        min_cheb = min((max(abs(cx), abs(cy)) for ((cx, cy), _, _) in guilty_dag),
                       default=None)
        min_ep_d = None
        if deep_dag and guilty_dag:
            eps = []
            for ((cx, cy), tf, paint_t) in guilty_dag:
                assert paint_t is not None, "colpevole-dagger profonda di seme?!"
                lo = bisect.bisect_right(rec_times, paint_t)
                hi = bisect.bisect_right(rec_times, t)
                eps.append(hi - lo)
            min_ep_d = min(eps)

        L = min(t_dag, n_real - t)
        d = None
        for i in range(L):
            if gturns[i] != turns[t + i]:
                d = i
                break
        d_cell = min((tf for (_, tf, _) in guilty_dag), default=None)
        if d is not None:
            assert d_cell == d, f"T-DIV rosso: d_svolte={d} d_celle={d_cell}"
        else:
            assert d_cell is None or d_cell >= L
        if Gd == 0:
            assert d is None
            if t_on - t > t_dag:
                ob["vdagger_violazioni"].append(
                    {"t": t, "t_on_meno_t": t_on - t, "t_dagger": t_dag,
                     "onset_germe": onset_germe, "burden": row["burden"],
                     "word": "".join("R" if b else "L" for b in w)})
            else:
                ob["g0_fisiologici"] += 1

        if d is None:
            classe = "E"
            ride = None
        elif d < onset_germe:
            classe = "T"
            ride = 0
        else:
            classe = "R"
            ride = d - onset_germe
            ob["ride_max"] = max(ob["ride_max"], ride)
        ob[classe] += 1

        ob["rows"].append((d if d is not None else -1, classe,
                           ride if ride is not None else -1, Gd,
                           min_cheb if min_cheb is not None else -1,
                           min_ep_d if min_ep_d is not None else -1,
                           onset_germe, 1 if deep_dag else 0))

        base_tst = {"rngstate": rngstate, "t": t, "t_on": t_on,
                    "pose": [rx, ry], "onset_germe": onset_germe,
                    "burden": row["burden"], "G_dagger": Gd,
                    "min_cheb": min_cheb, "min_ep_dagger": min_ep_d,
                    "d": d, "classe": classe, "ride": ride,
                    "word": "".join("R" if b else "L" for b in w)}
        if min_cheb is not None and min_cheb > 8:
            tst = dict(base_tst)
            tst["guilty_vicine"] = [
                {"cella": list(c), "fr": tf,
                 "cheb": max(abs(c[0]), abs(c[1]))}
                for (c, tf, _) in sorted(guilty_dag,
                                         key=lambda v: max(abs(v[0][0]),
                                                           abs(v[0][1])))[:6]]
            ob["F1"].append(tst)
        if classe == "R" and ride >= P:
            ob["F2"].append(base_tst)
    return ob


def _worker(rngstate):
    try:
        return orbit_divergence(rngstate)
    except AssertionError as e:
        return {"rngstate": rngstate, "assert_error": str(e)}


def gate_canonici():
    ref = json.load(open(CENSUS101))
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    mc_hist = {}
    me_hist = {}
    for od, rref in zip(dumps, ref["per_orbit"]):
        ob = orbit_divergence(od.rngstate)
        assert ob["onset"] == od.onset_header, f"orb {od.index}: onset != header"
        for k in ("records", "T", "R", "E", "ride_max", "G_dag_sum"):
            assert ob[k] == rref[k], f"orb {od.index}: {k} {ob[k]} != §101a {rref[k]}"
        for (d, classe, ride, Gd, mc, me, og, deep) in ob["rows"]:
            if mc >= 0:
                mc_hist[str(mc)] = mc_hist.get(str(mc), 0) + 1
            if me >= 0 and deep:
                me_hist[str(me)] = me_hist.get(str(me), 0) + 1
    assert mc_hist == ref["min_cheb_dagger"]["hist"], \
        f"hist min_cheb {mc_hist} != §101a"
    assert me_hist == ref["min_ep_dagger"]["hist"], \
        f"hist min_ep_dagger {me_hist} != §101a"
    print("GATE canonici: 24/24 orbite bit-identiche a §101a (6 campi per-orbita "
          "+ hist min_cheb_dagger + hist min_ep_dagger)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-seeds", type=int, default=8000)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--skip-gate", action="store_true")
    args = ap.parse_args()
    t0 = time.time()

    if not args.skip_gate:
        gate_canonici()

    base3 = xs(BASE ^ 0x94D049BB133111EB)
    states = fresh_states(args.n_seeds, base=base3)
    ch1 = set(fresh_states(5000))
    base2 = xs(BASE ^ 0xD1B54A32D192ED03)
    ch2 = set(fresh_states(25000, base=base2))
    overlap = (set(states) & ch1) | (set(states) & ch2)
    assert not overlap, f"catena-3 NON disgiunta: {len(overlap)} collisioni"
    print(f"catena-3 (BASE3={base3}): {args.n_seeds} semi, disgiunzione verificata "
          f"contro catena-1 (5000) e catena-2 (25000)", flush=True)

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

    rows = [row for r in ok for row in r["rows"]]
    F1 = [t for r in ok for t in r["F1"]]
    F2 = [t for r in ok for t in r["F2"]]
    vdag = [dict(v, rngstate=r["rngstate"]) for r in ok
            for v in r["vdagger_violazioni"]]
    g0_fis = sum(r["g0_fisiologici"] for r in ok)
    n_rec = sum(r["records"] for r in ok)
    n_T = sum(r["T"] for r in ok)
    n_R = sum(r["R"] for r in ok)
    n_E = sum(r["E"] for r in ok)
    with_g = [row for row in rows if row[3] >= 1]
    mc_all = [row[4] for row in with_g if row[4] >= 0]
    me_all = [row[5] for row in rows if row[5] >= 0]
    d_all = [row[0] for row in rows if row[0] >= 0]
    rides = [row[2] for row in rows if row[1] == "R"]

    def hist_of(vals):
        h = {}
        for v in vals:
            h[v] = h.get(v, 0) + 1
        return {str(k): h[k] for k in sorted(h)}

    # ---- VERDETTO PREREGISTRATO (criteri fissati in testa al file) ----
    potenza_ok = len(with_g) >= 5000
    if not potenza_ok:
        verdetto = f"SOTTOPOTENZIATO ({len(with_g)} record con G_dagger>=1 < 5000)"
    else:
        v1 = (f"F1 REALIZZATO: {len(F1)} falsificatori min_cheb>8 (max "
              f"{max(mc_all)})" if F1 else
              "F1 VUOTO CON POTENZA: min_cheb<=8 regge (resta quantile, trappola i)")
        v2 = (f"F2 REALIZZATO: {len(F2)} lock ai record (ride max "
              f"{max(rides) if rides else 0})" if F2 else
              "F2 VUOTO: nessun ride >= P ai record freschi")
        p3_viol = [t for t in F1 if not (t["classe"] == "R" or
                                         (t["min_ep_dagger"] is not None
                                          and t["min_ep_dagger"] >= 4))]
        v3 = (f"P3 FALSIFICATA: {len(p3_viol)} F1 shallow a min_ep<4"
              if p3_viol else "P3 regge sui falsificatori F1")
        verdetto = v1 + " | " + v2 + " | " + v3

    out = {
        "preregistrazione": {
            "catena": 3, "base3": base3, "n_seeds": args.n_seeds,
            "F1": "record G_dagger>=1 con min_cheb_dagger > 8 (aspettativa: morte)",
            "F2": "record classe R con ride >= P (aspettativa: raro ma >0)",
            "P3": "ogni F1 ha classe R oppure min_ep_dagger >= 4",
            "potenza": ">= 5000 record con G_dagger >= 1"},
        "n_seeds": args.n_seeds, "no_onset": len(no_onset),
        "empty_seed": len(empty), "orbite_ok": len(ok),
        "records": n_rec, "classi": {"T": n_T, "R": n_R, "E": n_E},
        "records_con_G": len(with_g),
        "g0_fisiologici": g0_fis,
        "VDAGGER_VIOLAZIONI": vdag,
        "d": {"med": st.median(d_all) if d_all else None,
              "max": max(d_all) if d_all else None},
        "min_cheb": {"med": st.median(mc_all) if mc_all else None,
                     "max": max(mc_all) if mc_all else None,
                     "hist": hist_of(mc_all)},
        "min_ep_dagger": {"med": st.median(me_all) if me_all else None,
                          "max": max(me_all) if me_all else None,
                          "hist": hist_of(me_all)},
        "ride": {"n": len(rides), "max": max(rides) if rides else None},
        "F1": F1, "F2": F2,
        "VERDETTO_PREREGISTRATO": verdetto,
        "elapsed_s": round(time.time() - t0, 1)}

    print(f"semi {args.n_seeds}: ok {len(ok)}, no-onset {len(no_onset)}, vuoti "
          f"{len(empty)}; record {n_rec} (con G {len(with_g)}); classi T={n_T} "
          f"R={n_R} E={n_E}; g0 fisiologici {g0_fis}", flush=True)
    print(f"V-DAGGER violazioni: {len(vdag)}", flush=True)
    for v in vdag[:8]:
        print(f"  !!! V-DAGGER: rngstate {v['rngstate']} t={v['t']} "
              f"t_on-t={v['t_on_meno_t']} > t_dagger={v['t_dagger']}", flush=True)
    print(f"d: med {out['d']['med']} max {out['d']['max']}", flush=True)
    print(f"min_cheb: med {out['min_cheb']['med']} MAX {out['min_cheb']['max']} "
          f"hist {out['min_cheb']['hist']}", flush=True)
    print(f"min_ep_dagger: med {out['min_ep_dagger']['med']} MAX "
          f"{out['min_ep_dagger']['max']}", flush=True)
    print(f"F1 (min_cheb>8): {len(F1)}", flush=True)
    for t in F1[:12]:
        print(f"  !!! F1 rngstate {t['rngstate']} t={t['t']} min_cheb={t['min_cheb']} "
              f"classe={t['classe']} d={t['d']} onset_germe={t['onset_germe']} "
              f"min_ep={t['min_ep_dagger']} ride={t['ride']}", flush=True)
    print(f"F2 (ride>=P): {len(F2)}", flush=True)
    for t in F2[:12]:
        print(f"  !!! F2 rngstate {t['rngstate']} t={t['t']} ride={t['ride']} "
              f"({t['ride']/P:.1f} periodi) onset_germe={t['onset_germe']}", flush=True)
    print(f"VERDETTO PREREGISTRATO: {verdetto}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
