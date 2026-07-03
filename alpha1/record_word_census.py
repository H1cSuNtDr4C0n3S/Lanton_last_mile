# record_word_census.py — §89a: le parole REALI ai pose-record y-min delle 24 orbite.
#
# §88 ha prodotto il Teorema della Parola Viva: w101 (burden1=1, residuo {(1,1)}, D=inf)
# e' enunciabile per orbite eterne. La domanda §89 (roadmap §88.8-1): quali parole
# OCCORRONO davvero ai record delle orbite reali, e con che fardello? Se parole a burden1
# basso sono inevitabili ai record, il pigeonhole sull'Uno diventa l'attacco a Link 1.
#
# Metodo (per ciascuna delle 24 orbite lunghe, semi da dumps_all.txt):
#   PASSO 1  corsa fino all'onset (convenzione run_to_onset §87c) registrando i RECORD
#            y-min STRETTI pre-onset: t, posa; assert heading=0 all'arrivo (si scende
#            solo muovendo su). Censiti solo i record con y < min_y(seme) (sotto il blob:
#            semipiano davanti garantito bianco, cella record fresca-bianca, svolta R).
#   PASSO 2  per ogni record con t >= K: parola = svolte[t-K..t-1] (convenzione hunter);
#            eval_word => (burden1, onset_germe, residuo). Gate di convenzione: la parola
#            DEVE essere realizzabile e record-compatibile (footprint in {y>=1}).
#   PASSO 3  replay con interrogazione dei colori REALI delle celle-residuo al tempo del
#            record (frame anchor = assoluto traslato: heading 0). Celle COLPEVOLI =
#            residuo non-bianco. TEOREMA-TRIPWIRE: se t_on - t > onset_germe + P, almeno
#            una cella del residuo deve essere colpevole (Cono §87 + Finestra-K + Replay);
#            zero colpevoli a distanza dall'onset = ROSSO (bug o falsificazione).
#   Caccia: match esatto con w101 (copre l'intera famiglia sigma^m*tau*w101, che ha w101
#   come suffisso-101); parole a burden1 = 0 (arma in natura: vietata ai record lontani
#   dall'onset, tripwire); distribuzione di burden1 a K=101 e K=18 (confronto §87d).
#
# Uscita: alpha1/record_word_census_summary.json
import sys, os, json, time, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import DX, DY, P, onset_verified
from record_weapon_hunt import eval_word
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "record_word_census_summary.json")
KS = (18, 101)
KMAIN = 101


def run_collect_records(seed, chk=20000, max_steps=1_500_000):
    """Corsa fino all'onset; ritorna (turns, t_on, records=[(t,x,y),...]).
    Record y-min stretto = visita a y < ogni y precedente (assert heading su)."""
    grid = {}
    x = y = 0
    h = 0
    turns = bytearray()
    t = 0
    y_min = 0
    records = []
    while t < max_steps:
        if y < y_min:
            assert h == 0, f"record a t={t} con heading {h} != 0"
            records.append((t, x, y))
            y_min = y
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
            turns.append(1)
        else:
            h = (h + 3) & 3
            grid[c] = 0
            turns.append(0)
        x += DX[h]
        y += DY[h]
        t += 1
        if t >= 2600 and (t % chk) == 0:
            o = onset_verified(turns, t)
            if o >= 0:
                return turns, o, records
    return turns, onset_verified(turns, t), records


def replay_query_colors(seed, turns_ref, queries):
    """Replay deterministico; queries: {t: [celle assolute]} -> {t: {cella: colore}}.
    Tripwire: svolte == turns_ref."""
    out = {}
    grid = {}
    x = y = 0
    h = 0
    t_max = max(queries) if queries else -1
    for t in range(t_max + 1):
        if t in queries:
            out[t] = {c: (grid[c] if c in grid else (1 if c in seed else 0))
                      for c in queries[t]}
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns_ref[t], f"replay diverge a t={t}"
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += DX[h]
        y += DY[h]
    return out


def main():
    t_start = time.time()
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    ev_cache = {}

    def ev(w):
        r = ev_cache.get(w, "MISS")
        if r == "MISS":
            r = eval_word(w)
            ev_cache[w] = r
        return r

    orbits_out = []
    pooled = {K: [] for K in KS}
    guilty_hist = {}
    w101_hits = 0
    burden0 = []
    onset_none = 0
    tripwire_checked = 0

    for od in dumps:
        seed, side, dens = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header, f"orb {od.index}: onset {t_on} != header"
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= max(KS)]
        n_skip = len(records) - len(recs)

        rows = []
        queries = {}
        for (t, rx, ry) in recs:
            row = {"t": t, "y": ry}
            for K in KS:
                w = tuple(turns[t - K:t])
                r = ev(w)
                if r is None:
                    onset_none += 1
                    row[f"b{K}"] = None
                    continue
                row[f"b{K}"] = r[0]
                pooled[K].append(r[0])
                if K == KMAIN:
                    row["onset_germe"] = r[1]
                    row["residuo"] = r[3]
                    row["is_w101"] = (w == w101)
                    if row["is_w101"]:
                        w101_hits += 1
                    if r[0] == 0:
                        burden0.append({"orbit": od.index, "t": t, "t_on": t_on})
                    # colori reali del residuo al tempo del record
                    queries.setdefault(t, []).extend(
                        [(rx + cx, ry + cy) for (cx, cy) in r[3]])
            rows.append(row)

        colors = replay_query_colors(seed, turns, queries)
        for row in rows:
            if row.get("residuo") is None or row.get(f"b{KMAIN}") is None:
                continue
            t = row["t"]
            got = colors.get(t, {})
            rx_ry = next((rx, ry) for (tt, rx, ry) in recs if tt == t)
            guilty = [list(c) for c in row["residuo"]
                      if got.get((rx_ry[0] + c[0], rx_ry[1] + c[1]), 0) == 1]
            row["guilty"] = len(guilty)
            g = len(guilty)
            b = row[f"b{KMAIN}"]
            guilty_hist[(b, g)] = guilty_hist.get((b, g), 0) + 1
            # tripwire del teorema: lontano dall'onset serve >= 1 colpevole
            if t_on - t > row["onset_germe"] + P:
                tripwire_checked += 1
                assert g >= 1, (f"ROSSO orb {od.index} t={t}: burden {b}, residuo "
                                f"{row['residuo']} tutto bianco ma t_on-t="
                                f"{t_on - t} > {row['onset_germe'] + P}")
            row["residuo"] = [list(c) for c in row["residuo"]] if b <= 6 else b

        bmain = [r[f"b{KMAIN}"] for r in rows if r.get(f"b{KMAIN}") is not None]
        orbits_out.append({
            "orbit": od.index, "onset": t_on, "records_tot": len(records),
            "records_censiti": len(recs), "records_scartati_early": n_skip,
            "b101_min": min(bmain) if bmain else None,
            "b101_med": st.median(bmain) if bmain else None,
            "rows_low": [r for r in rows
                         if r.get(f"b{KMAIN}") is not None and r[f"b{KMAIN}"] <= 6]})
        print(f"[orb {od.index:2d}] onset {t_on} record {len(recs)} "
              f"(early {n_skip}) b101 min {orbits_out[-1]['b101_min']} "
              f"med {orbits_out[-1]['b101_med']}", flush=True)

    summ = {}
    for K in KS:
        v = pooled[K]
        summ[K] = {"n": len(v), "min": min(v), "med": st.median(v), "max": max(v),
                   "hist_low": {b: v.count(b) for b in range(0, 13)}}
        print(f"K={K}: n={len(v)} burden1 min {min(v)} med {st.median(v)} "
              f"max {max(v)} | <=3: {sum(1 for x in v if x <= 3)}, "
              f"<=6: {sum(1 for x in v if x <= 6)}", flush=True)
    print(f"w101 match esatti: {w101_hits}; burden0 ai record: {len(burden0)}; "
          f"eval senza onset: {onset_none}", flush=True)
    print(f"tripwire teorema (record lontani dall'onset, >=1 colpevole): "
          f"{tripwire_checked} controllati, 0 violazioni", flush=True)
    gh = {f"{b},{g}": n for (b, g), n in sorted(guilty_hist.items())}
    print(f"istogramma (burden101, colpevoli): {gh}", flush=True)

    out = {"KS": list(KS), "per_orbit": orbits_out, "pooled": summ,
           "w101_hits": w101_hits, "burden0_sightings": burden0,
           "onset_none": onset_none, "tripwire_checked": tripwire_checked,
           "guilty_hist": gh, "elapsed_s": round(time.time() - t_start, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
