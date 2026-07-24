# danger_wedge_map.py — §107d P1b (meta' empirica): la mappa del deposito
# antico in frame ancora, normalizzata al lato del drift.
#
# OGGETTO: F3 ha mostrato ricchezza-scudo ~1/3 PIATTA in sigma (lo scudo e'
# antico e word-indipendente). Qui si mappa DOVE sta: densita' di nero
# per cella ancora (cx, cy) pooled sui 1639 record canonici, con x
# NORMALIZZATA al lato del drift del germe (wx = cx * sign(drift_x); il
# cuneo del drift §105b e' sempre a wx < 0 dopo la normalizzazione... il
# segno si legge dal dato, non si assume). Il fronte del cono passato §87
# diventa un oggetto misurato: la zona a densita' ~0 e' il cuneo vergine,
# i lock sono read-set interamente dentro quella zona.
#
# GATES:
#   GW0: somma nb sulla mappa == somma nb di F3 (stesso replay, stessa
#        selezione — bit-identico).
#   GW1: replay bit-per-bit (come GF1).
#   GW2: celle garantite-vergini del Lemma del Cuneo §106 (theta > Delta_k,
#        via eta' della riga: Delta_k = t - t_apertura(riga k)) — qui NON
#        ricalcolate: si usa il fatto §106-T2 (0 nere su 6055) come vincolo
#        di coerenza atteso sulla coda della mappa (dichiarato, non gate
#        meccanico).
#   I 2 lock: overlay dichiarato (read-set nel cuneo, nb=0 — GF2 F3).
# Nessuna soglia (qq): la mappa e' il dato; enunciati solo descrittivi.
#
# Uscita: alpha1/danger_wedge_map.json
import sys, os, json, time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_word_census import run_collect_records
from danger_shield_calibration import rt_cache_get, replay_measure

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "danger_wedge_map.json")
CENSUS = os.path.join(HERE, "danger_geometry_census.json")
CALIB = os.path.join(HERE, "danger_shield_calibration.json")
K = 101


def replay_cells(seed, turns, targets):
    """Come replay_measure ma ritorna t -> lista di colori per cella."""
    grid = {}
    x = y = 0
    h = 0
    res = {}
    T = max(targets) + 1 if targets else 0
    for t in range(T):
        if t in targets:
            res[t] = [grid[c] if c in grid else (1 if c in seed else 0)
                      for c in targets[t]]
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns[t], f"GW1 FALLITO: replay diverge a t={t}"
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += (0, 1, 0, -1)[h]
        y += (-1, 0, 1, 0)[h]
    return res


def main():
    t0 = time.time()
    census = json.load(open(CENSUS))["per_word"]
    rt_cache = {}
    # densita' per cella ancora normalizzata (wx, cy): [nere, viste]
    dens = {}
    dens_raw = {}
    nb_tot = 0
    n_rec = 0
    drift0 = 0
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]
        targets = {}
        meta = {}
        for (t, rx, ry) in recs:
            w = tuple(turns[t - K:t])
            ws, rt = rt_cache_get(w, rt_cache)
            targets[t] = [(rx + cx, ry + cy) for (cx, cy) in rt]
            meta[t] = (ws, rt)
        cols = replay_cells(seed, turns, targets)
        for t in sorted(targets):
            ws, rt = meta[t]
            dx = census[ws]["drift_x"]
            if dx == 0:
                drift0 += 1
                continue
            s = 1 if dx > 0 else -1
            n_rec += 1
            for (cx, cy), col in zip(rt, cols[t]):
                nb_tot += col
                key = (cx * s, cy)
                d = dens.setdefault(key, [0, 0])
                d[0] += col
                d[1] += 1
                dr = dens_raw.setdefault((cx, cy), [0, 0])
                dr[0] += col
                dr[1] += 1
        print(f"[orb {od.index:2d}] ok", flush=True)

    # GW0: coerenza con F3 (somma nere sui record inclusi)
    calib = json.load(open(CALIB))
    nb_f3 = sum(d["ricchezza"] * d["pres"] * d["n_rt"]
                for d in calib["per_word"].values())
    nb_all = sum(v[0] for v in dens_raw.values())
    print(f"GW0: nb mappa (drift!=0) {nb_tot}, nb totale raw {nb_all}, "
          f"nb F3 (arrotond.) {nb_f3:.0f}; record con drift_x=0 esclusi: "
          f"{drift0}", flush=True)
    assert abs(nb_all - nb_f3) < max(2, 0.001 * nb_f3), "GW0 FALLITO"

    # ---- profilo laterale: densita' per wx (pooled su cy) ----
    prof_wx = {}
    for (wx, cy), (nb, nv) in dens.items():
        p = prof_wx.setdefault(wx, [0, 0])
        p[0] += nb
        p[1] += nv
    print("\nprofilo laterale (wx = x * sign(drift_x); wx<0 = lato OPPOSTO "
          "al drift, wx>0 = lato del drift):", flush=True)
    print("  wx | viste | densita' nero", flush=True)
    prof_out = []
    for wx in sorted(prof_wx):
        nb, nv = prof_wx[wx]
        if nv < 30:
            continue
        prof_out.append({"wx": wx, "viste": nv, "dens": round(nb / nv, 4)})
        print(f"  {wx:3d} | {nv:6d} | {nb / nv:.4f}", flush=True)

    # ---- profilo per riga (cy), pooled su wx ----
    prof_cy = {}
    for (wx, cy), (nb, nv) in dens.items():
        p = prof_cy.setdefault(cy, [0, 0])
        p[0] += nb
        p[1] += nv
    prof_cy_out = [{"cy": cy, "viste": v[1], "dens": round(v[0] / v[1], 4)}
                   for cy, v in sorted(prof_cy.items()) if v[1] >= 30]

    out = {"gates": {"GW0": True, "GW1": "bit-per-bit", "drift0_esclusi":
                     drift0},
           "n_record_mappa": n_rec,
           "profilo_wx": prof_out, "profilo_cy": prof_cy_out,
           "mappa": {f"{wx},{cy}": [nb, nv] for (wx, cy), (nb, nv)
                     in sorted(dens.items()) if nv >= 10},
           "convenzione": "wx = cx*sign(drift_x del germe); densita' = "
                          "quota nere fra le viste in quella cella ancora; "
                          "og dal record (asse assoluto og+101)",
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
