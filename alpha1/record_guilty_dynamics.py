# record_guilty_dynamics.py — §89b: la DINAMICA DELLE COLPEVOLI fra record consecutivi.
#
# §89a: a ogni record y-min pre-onset almeno una cella del residuo e' nera (1620/1620);
# in 3 casi UNA sola. Qui si misura il processo G(i) = numero di colpevoli al record i:
#   1. distribuzione e traiettoria di G (quanto spesso scende verso 1? streak bassi?);
#   2. transizioni Delta-G fra record consecutivi (P(discesa), code);
#   3. PERSISTENZA: le colpevoli del record i sono ancora nere al record i+1? sono ancora
#      nel residuo/colpevoli del record i+1? (staffetta di un unico detrito vs celle fresche);
#   4. ETA' delle colpevoli (t - ultima pittura a nero): frazione con eta' >= K=101
#      (scala Spoiler Vecchio §87), mediana, code lunghe (>=10*P), celle di SEME;
#      + geometria (distanza Chebyshev dalla posa record);
#   5. autopsia dei record a G=1 (eta' e posizione della colpevole unica, G al record dopo).
#
# Gate: stessi record e stesso tripwire di §89a (n censiti 1639, G>=1 lontano dall'onset);
# cross-check: la coppia (burden, G) per record deve riprodurre l'istogramma §89a.
# Uscita: alpha1/record_guilty_dynamics_summary.json
import sys, os, json, time, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import DX, DY, P, onset_verified
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_weapon_vitality import SUMMARY, to_bits

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "record_word_census_summary.json")
OUT = os.path.join(HERE, "record_guilty_dynamics_summary.json")
K = 101


def replay_query(seed, turns_ref, queries):
    """Replay; queries {t: iterable di celle} -> {t: {cella: (colore, paint_t)}}.
    paint_t = tempo dell'ultima scrittura a NERO (None se mai scritta: colore da seme o
    vergine). Tripwire: svolte == turns_ref."""
    out = {}
    grid = {}
    paint_black = {}
    x = y = 0
    h = 0
    t_max = max(queries) if queries else -1
    for t in range(t_max + 1):
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
    return out


def main():
    t_start = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    census = json.load(open(CENSUS))
    ev_cache = {}

    def ev(w):
        r = ev_cache.get(w, "MISS")
        if r == "MISS":
            r = eval_word(w)
            ev_cache[w] = r
        return r

    G_all = []
    dG_all = []
    G_traj_low = []                 # (orbita, i, G) con G <= 3
    persist_black = []              # fraz. colpevoli(i) ancora nere a t_{i+1}
    persist_guilty = []             # fraz. colpevoli(i) ancora colpevoli a i+1
    ages = []                       # eta' delle colpevoli (None = seme/mai dipinta)
    age_seed = 0
    cheb_guilty = []
    g1_autopsy = []
    dt_records = []
    n_records = 0
    tripwire = 0

    for od in dumps:
        seed, side, dens = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]

        # residui per record + query ai tempi dei record (residuo corrente + residuo prec.)
        info = []
        for (t, rx, ry) in recs:
            r = ev(tuple(turns[t - K:t]))
            assert r is not None
            res_abs = [(rx + cx, ry + cy) for (cx, cy) in r[3]]
            info.append({"t": t, "pose": (rx, ry), "burden": r[0],
                         "onset_germe": r[1], "res_abs": res_abs})
        queries = {}
        for i, row in enumerate(info):
            q = set(row["res_abs"])
            if i > 0:
                q |= set(info[i - 1]["res_abs"])
            queries[row["t"]] = q
        colors = replay_query(seed, turns, queries)

        prev_guilty = None
        prev_G = None
        for i, row in enumerate(info):
            t = row["t"]
            got = colors[t]
            guilty = [c for c in row["res_abs"] if got[c][0] == 1]
            G = len(guilty)
            n_records += 1
            if t_on - t > row["onset_germe"] + P:
                tripwire += 1
                assert G >= 1, f"ROSSO orb {od.index} t={t}"
            G_all.append(G)
            if G <= 3:
                G_traj_low.append({"orbit": od.index, "i": i, "t": t, "G": G,
                                   "burden": row["burden"]})
            for c in guilty:
                pt = got[c][1]
                if pt is None:
                    age_seed += 1
                    ages.append(None)
                else:
                    ages.append(t - pt)
                px, py = row["pose"]
                cheb_guilty.append(max(abs(c[0] - px), abs(c[1] - py)))
            if prev_guilty is not None:
                dG_all.append(G - prev_G)
                dt_records.append(t - info[i - 1]["t"])
                # persistenza delle colpevoli del record precedente
                still_black = [c for c in prev_guilty if c in got and got[c][0] == 1]
                if prev_guilty:
                    persist_black.append(len(still_black) / len(prev_guilty))
                    persist_guilty.append(
                        len([c for c in prev_guilty if c in set(guilty)])
                        / len(prev_guilty))
            if G == 1:
                c = guilty[0]
                pt = got[c][1]
                px, py = row["pose"]
                nxt = None
                g1_autopsy.append({
                    "orbit": od.index, "t": t, "burden": row["burden"],
                    "cella_rel": [c[0] - px, c[1] - py],
                    "eta": (t - pt) if pt is not None else "seme",
                    "cheb": max(abs(c[0] - px), abs(c[1] - py)),
                    "t_on_meno_t": t_on - t})
            prev_guilty = guilty
            prev_G = G

    assert n_records == sum(o["records_censiti"] for o in census["per_orbit"]), \
        "numero record diverso da §89a!"
    assert tripwire == census["tripwire_checked"], "tripwire count diverso da §89a!"

    aa = [a for a in ages if a is not None]
    frac_old_K = sum(1 for a in aa if a >= K) / len(aa)
    frac_10P = sum(1 for a in aa if a >= 10 * P) / len(aa)
    out = {
        "n_records": n_records,
        "G": {"min": min(G_all), "med": st.median(G_all), "max": max(G_all),
              "hist_low": {g: G_all.count(g) for g in range(0, 11)}},
        "dG": {"med": st.median(dG_all), "p_down": sum(1 for d in dG_all if d < 0) / len(dG_all),
               "p_up": sum(1 for d in dG_all if d > 0) / len(dG_all)},
        "dt_records": {"med": st.median(dt_records), "max": max(dt_records)},
        "persistenza": {"nera_al_record_dopo_med": st.median(persist_black),
                        "colpevole_al_record_dopo_med": st.median(persist_guilty),
                        "nera_mean": st.mean(persist_black),
                        "colpevole_mean": st.mean(persist_guilty)},
        "eta_colpevoli": {"n": len(ages), "da_seme": age_seed,
                          "med": st.median(aa), "frac_eta_ge_K": frac_old_K,
                          "frac_eta_ge_10P": frac_10P,
                          "min": min(aa), "max": max(aa)},
        "cheb_colpevoli": {"med": st.median(cheb_guilty), "max": max(cheb_guilty)},
        "G_le_3": G_traj_low, "G1_autopsy": g1_autopsy,
        "elapsed_s": round(time.time() - t_start, 1)}

    print(f"record {n_records}, G min {out['G']['min']} med {out['G']['med']} "
          f"max {out['G']['max']}; hist bassi {out['G']['hist_low']}", flush=True)
    print(f"transizioni: P(giu') {out['dG']['p_down']:.3f} P(su) {out['dG']['p_up']:.3f} "
          f"dG med {out['dG']['med']}; dt fra record med {out['dt_records']['med']} "
          f"max {out['dt_records']['max']}", flush=True)
    print(f"persistenza colpevoli -> record dopo: ancora nere med "
          f"{out['persistenza']['nera_al_record_dopo_med']:.3f} (mean "
          f"{out['persistenza']['nera_mean']:.3f}), ancora colpevoli med "
          f"{out['persistenza']['colpevole_al_record_dopo_med']:.3f} (mean "
          f"{out['persistenza']['colpevole_mean']:.3f})", flush=True)
    print(f"eta' colpevoli: med {out['eta_colpevoli']['med']}, >=K(101) "
          f"{frac_old_K:.3f}, >=10P {frac_10P:.3f}, da seme {age_seed}, "
          f"max {out['eta_colpevoli']['max']}", flush=True)
    print(f"cheb colpevoli: med {out['cheb_colpevoli']['med']} "
          f"max {out['cheb_colpevoli']['max']}", flush=True)
    print(f"record a G<=3: {len(G_traj_low)}; autopsie G=1: {g1_autopsy}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
