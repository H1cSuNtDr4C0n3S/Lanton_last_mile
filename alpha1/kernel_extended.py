# kernel_extended.py — §107e: KERNEL ESTESO R_{T,L}, forense last-paint,
# ipotesi del last-paint cutset (mossa unica §107d.6, L=104).
#
# DEFINIZIONI (agganciate bit-esatte a §101):
#   germe-tempo i=0 <-> tempo reale t+i;  d(t) = primo i: gturns[i] != turns[t+i].
#   H = onset_germe(w) + L.  KERNEL ESTESO:
#     R_{T,L}(w) = { (c, tf) : prima-lettura del germe fr, tf < H,
#                    c fuori footprint(w), c_y >= 1 }
#   (le esogene a c_y <= 0 sono auto-valide per record y-min stretto sotto il
#   seme — deduzione §101 header; il footprint e' word-determinato).
#
# GATE 1 (equivalenza esatta, T-DIV §101 ESTESO a orizzonte H, per-record):
#   d_b = min { tf : c in R_{T,L}, reale(c al record) = nero }  (None se vuoto)
#   (a) d_b == None  =>  nessun mismatch di svolta in [0, H)   [<= direzione]
#   (b) d_b != None  =>  d_a == d_b                            [=> direzione]
#   (c) kernel interamente compatibile (tutte bianche) <=> ride = d-og >= L.
#   Regressione: d_a == d del CSV §101 su tutti i 1639 canonici; lock: d_a ==
#   324/449, ride == 269/384 (hunt F2).
# GATE 2 (determinacy): il verdetto e' funzione di (parola, colori di R_{T,L}
#   al record); nessun altro input. Fuori orizzonte => UNKNOWN (gate 6), mai
#   classificato.
# GATE 3 (bianco != vergine): la forense usa la STORIA DELLE VISITE dal
#   replay (n_visite, prima/ultima visita, ultimo bianco->nero, in_seed),
#   non il colore.
# GATE 4 (cut definito PRIMA dei verdetti — PREREGISTRAZIONE):
#   CUT = i fronti delle epoche-record (la sequenza dei record y-min
#   dell'orbita); ATTRAVERSAMENTO = evento di ultima pittura last_W2B
#   (cella, tempo) di una cella-scudo (nera al record) del kernel esteso.
#   IPOTESI H-NR (non-riusabilita' STRETTA, falsificabile): nessun evento
#   (cella, last_W2B) scuda i kernel estesi di DUE record distinti.
#   ASPETTATIVA DICHIARATA DI MORTE: §98/§100 (colpevoli condivise dai
#   record consecutivi, min_lag 0) rendono H-NR probabilmente falsa gia'
#   sui consecutivi; il dato utile e' la STRUTTURA del riuso (consecutivo
#   vs lontano) per la versione d'ordine ben fondato.
# GATE 5: un controesempio uccide H-NR (conteggio esatto, esempi salvati).
# GATE 6: record con t+H oltre le svolte disponibili => UNKNOWN, contati.
#
# Unita': profondita' in passi germe-tempo; epoche = indici nella lista
# COMPLETA dei record y-min dell'orbita (convenzione dichiarata).
# Convenzione og: misurato DAL RECORD (asse assoluto og+101, caveat §107b.6).
# Uscita: alpha1/kernel_extended_summary.json
import sys, os, json, time, csv, bisect

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_weapon_hunt import eval_word
from record_divergence_census import germ_long_run
from speed_limit_theorem import transient_readset_from_germ
from record_word_census import run_collect_records

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "kernel_extended_summary.json")
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
CSV101 = os.path.join(HERE, "record_divergence_census_records.csv")
K = 101
L = 104


def word_str(w):
    return "".join("R" if b else "L" for b in w)


def kernel_ext(w, cache):
    """(og, H, kernel=[(cell_anchor, tf), ...]) con regressione sul transiente."""
    ws = word_str(w)
    if ws in cache:
        return cache[ws]
    r = eval_word(w)
    assert r is not None
    og = r[1]
    gturns, fr, t_dag, drift, footprint, xs, ys = germ_long_run(w, og)
    H = og + L
    assert H <= t_dag
    kern = sorted((c, tf) for c, (tf, _) in fr.items()
                  if tf < H and c not in footprint and c[1] >= 1)
    # regressione: restrizione al transiente == macchinario §106 validato
    rs_ref = transient_readset_from_germ(w, og)
    rs_mine = [(c, tf) for (c, tf) in kern if tf < og]
    assert rs_mine == rs_ref, f"R-B FALLITA {ws[:16]}"
    cache[ws] = (og, H, kern, gturns)
    return cache[ws]


def replay_forense(seed, turns, rec_targets, T_max):
    """Replay forward con stats per-cella e snapshot ai tempi-record.
    rec_targets: t -> lista (cell_abs, cell_anchor, tf).
    Ritorna t -> lista (cell_anchor, tf, colore, in_seed, n_vis, first_vis,
    last_vis, last_W2B) — stats calcolate PRIMA del passo t (gate 3)."""
    grid = {}
    stats = {}                     # cell_abs -> [n_vis, first, last, lastW2B]
    x = y = 0
    h = 0
    snap = {}
    for t in range(T_max):
        if t in rec_targets:
            rows = []
            for (ca_abs, ca, tf) in rec_targets[t]:
                col = grid[ca_abs] if ca_abs in grid else (
                    1 if ca_abs in seed else 0)
                s = stats.get(ca_abs)
                rows.append((ca, tf, col, ca_abs in seed,
                             0 if s is None else s[0],
                             None if s is None else s[1],
                             None if s is None else s[2],
                             None if s is None else s[3]))
            snap[t] = rows
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns[t], f"replay diverge a t={t}"
        s = stats.get(c)
        if s is None:
            s = [0, t, t, None]
            stats[c] = s
        s[0] += 1
        s[2] = t
        if color == 0:
            s[3] = t                                  # letta bianca -> nera
            h = (h + 1) & 3
            grid[c] = 1
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += (0, 1, 0, -1)[h]
        y += (-1, 0, 1, 0)[h]
    return snap


def process_orbit(label, seed, turns, t_on, records, recs, wcache, csv_d,
                  detail_full):
    """recs: [(t, rx, ry)] da classificare. Ritorna (rows, unknown, eventi)."""
    rec_targets = {}
    meta = {}
    unknown = []
    rec_times = [r[0] for r in records]           # epoche = lista COMPLETA
    for (t, rx, ry) in recs:
        w = tuple(turns[t - K:t])
        og, H, kern, gturns = kernel_ext(w, wcache)
        if t + H > len(turns):
            unknown.append({"t": t, "og": og, "H": H,
                            "disponibili": len(turns) - t})
            continue
        rec_targets[t] = [((rx + cx, ry + cy), (cx, cy), tf)
                          for ((cx, cy), tf) in kern]
        meta[t] = (word_str(w), og, H, gturns, rx, ry)
    snap = replay_forense(seed, turns, rec_targets,
                          max(rec_targets) + 1 if rec_targets else 0)
    rows = []
    eventi = {}                                    # (cell_abs, lastW2B) -> [t]
    for t in sorted(rec_targets):
        ws, og, H, gturns, rx, ry = meta[t]
        # d_a: prima divergenza di svolta entro H
        d_a = None
        for i in range(H):
            if gturns[i] != turns[t + i]:
                d_a = i
                break
        cells = snap[t]
        blacks = [(tf, ca, ab) for (ca, tf, col, isd, nv, fv, lv, lw), ab in
                  ((c, (rx + c[0][0], ry + c[0][1])) for c in cells)
                  if col == 1]
        d_b = min(tf for (tf, _, _) in blacks) if blacks else None
        # ---- GATE 1 ----
        if d_b is None:
            assert d_a is None, \
                f"GATE1(a) FALLITO {label} t={t}: kernel bianco ma d_a={d_a}"
        else:
            assert d_a == d_b, \
                f"GATE1(b) FALLITO {label} t={t}: d_a={d_a} d_b={d_b}"
        d = d_a if d_a is not None else H          # censored a H
        ride = d - og
        compat = (d_b is None)
        assert compat == (ride >= L), f"GATE1(c) FALLITO {label} t={t}"
        if csv_d is not None:
            ref = csv_d.get(t)
            if ref is not None and d_a is not None:
                assert d_a == ref, \
                    f"REGRESSIONE §101 FALLITA {label} t={t}: {d_a} vs {ref}"
        ep_rec = bisect.bisect_right(rec_times, t) - 1
        # ---- forense delle celle scudo (nere) + eventi cutset ----
        shields = []
        for (ca, tf, col, isd, nv, fv, lv, lw) in cells:
            if col != 1:
                continue
            ab = (rx + ca[0], ry + ca[1])
            if lw is not None:
                key = (ab, lw)
                eventi.setdefault(key, []).append(t)
                ep_paint = bisect.bisect_right(rec_times, lw) - 1
            else:
                ep_paint = None
                assert isd, (f"GATE3 FALLITO {label} t={t} {ca}: nera, mai "
                             f"dipinta W2B, non seme")
            shields.append({"cella": list(ca), "tf": tf, "in_seed": isd,
                            "n_vis": nv, "ultima_visita": lv,
                            "ultimo_W2B": lw,
                            "eta_paint": None if lw is None else t - lw,
                            "ep_paint": ep_paint, "gap_ep":
                            None if ep_paint is None else ep_rec - ep_paint})
        # forense bianche (gate 3, solo nel dettaglio): vergine vs pari-visite
        whites = None
        if detail_full:
            whites = [{"cella": list(ca), "tf": tf, "n_vis": nv,
                       "vergine": nv == 0 and not isd,
                       "in_seed": isd, "ultima_visita": lv}
                      for (ca, tf, col, isd, nv, fv, lv, lw) in cells
                      if col == 0]
        first_bad = None
        if d_b is not None:
            first_bad = next(s for s in shields if s["tf"] == d_b)
        rows.append({"t": t, "word": ws, "og": og, "H": H,
                     "n_kernel": len(cells), "n_shield": len(shields),
                     "d": d if d_a is not None else None,
                     "censurato_a_H": d_a is None, "ride": ride,
                     "compat": compat, "ep_record": ep_rec,
                     "first_bad": first_bad,
                     "shields": shields if detail_full else None,
                     "whites": whites})
    return rows, unknown, eventi


def main():
    t0 = time.time()
    wcache = {}
    # CSV §101 per la regressione su d
    csv_by_orbit = {}
    with open(CSV101, newline="") as f:
        for r in csv.DictReader(f):
            csv_by_orbit.setdefault(int(r["orbit"]), {})[int(r["t"])] = \
                int(r["d"])
    out = {"L": L, "orbite": [], "lock": [], "unknown": []}
    all_rows = []
    all_eventi = {}
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]
        rows, unk, eventi = process_orbit(
            f"orb{od.index}", seed, turns, t_on, records, recs, wcache,
            csv_by_orbit.get(od.index), detail_full=False)
        for r in rows:
            r["orbit"] = od.index
        all_rows.extend(rows)
        for k, v in eventi.items():
            all_eventi.setdefault((od.index,) + k, []).extend(v)
        out["unknown"].extend({"orbit": od.index, **u} for u in unk)
        print(f"[orb {od.index:2d}] record {len(recs)}, classificati "
              f"{len(rows)}, unknown {len(unk)}", flush=True)

    # ---- lock ----
    hunt = json.load(open(HUNT))
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        label = f"LOCK{'AB'[i]}"
        seed, _, _ = build_seed(rngs, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        rec = next(r for r in records if r[0] == t)
        assert rec[2] < y_seed_min
        rows, unk, eventi = process_orbit(
            label, seed, turns, t_on, records, [rec], wcache, None,
            detail_full=True)
        assert not unk, f"{label} UNKNOWN?!"
        r = rows[0]
        # regressione su d PIENO (oltre H: il gate censura a H per disegno —
        # per ride >= L la divergenza vera sta oltre l'orizzonte del kernel)
        w = tuple(turns[t - K:t])
        og, H, kern, gturns = kernel_ext(w, wcache)
        d_full = None
        for i in range(min(len(gturns), len(turns) - t)):
            if gturns[i] != turns[t + i]:
                d_full = i
                break
        assert d_full == int(e["d"]), \
            f"REGRESSIONE hunt FALLITA {label}: d_full={d_full} vs {e['d']}"
        assert d_full - og == int(e["ride"])
        assert r["censurato_a_H"] and (d_full >= H), \
            f"{label}: censura incoerente (d_full={d_full}, H={H})"
        assert r["compat"], f"{label}: kernel esteso NON compatibile?!"
        r["d_full"] = d_full
        r["ride_full"] = d_full - og
        n_verg = sum(1 for c in r["whites"] if c["vergine"])
        n_pari = sum(1 for c in r["whites"]
                     if c["n_vis"] > 0 and not c["in_seed"])
        print(f"[{label}] d={r['d']} ride={r['ride']} kernel {r['n_kernel']} "
              f"celle: VERGINI {n_verg}, visitate-pari {n_pari}, "
              f"in_seed {sum(1 for c in r['whites'] if c['in_seed'])}",
              flush=True)
        r["label"] = label
        out["lock"].append(r)

    # ---- riepilogo classi + gate ----
    n = len(all_rows)
    n_T = sum(1 for r in all_rows if r["ride"] < 0 or
              (r["d"] is not None and r["d"] < r["og"]))
    n_Rshort = sum(1 for r in all_rows
                   if r["d"] is not None and 0 <= r["ride"] < L)
    n_comp = sum(1 for r in all_rows if r["compat"])
    print(f"\nGATE 1 (equivalenza estesa): certificata su {n} canonici + 2 "
          f"lock; classi: d<og {n_T}, 0<=ride<{L} {n_Rshort}, "
          f"compat {n_comp}; unknown {len(out['unknown'])}", flush=True)

    # ---- H-NR (gate 5): riuso degli attraversamenti ----
    reuse = {k: v for k, v in all_eventi.items() if len(v) >= 2}
    nonconsec = 0
    esempi = []
    for (orb, ab, lw), ts in sorted(reuse.items(), key=lambda kv: -len(kv[1])):
        rec_ts = sorted(set(ts))
        canon = sorted(r["t"] for r in all_rows if r["orbit"] == orb)
        idxs = [bisect.bisect_left(canon, tt) for tt in rec_ts]
        if max(idxs) - min(idxs) >= 2 or (len(idxs) >= 2 and
                                          idxs[-1] - idxs[0] >= 2):
            nonconsec += 1
        if len(esempi) < 10:
            esempi.append({"orbit": orb, "cella_abs": list(ab),
                           "last_W2B": lw, "records": rec_ts})
    n_ev = len(all_eventi)
    print(f"H-NR: eventi-scudo {n_ev}, riusati da >=2 record "
          f"{len(reuse)} ({'UCCISA' if reuse else 'regge'}), di cui "
          f"non-consecutivi {nonconsec}", flush=True)

    # ---- forense aggregata (first_bad dei canonici) ----
    fb = [r["first_bad"] for r in all_rows if r["first_bad"] is not None]
    ages = sorted(s["eta_paint"] for s in fb if s["eta_paint"] is not None)
    gaps = sorted(s["gap_ep"] for s in fb if s["gap_ep"] is not None)
    nvis = sorted(s["n_vis"] for s in fb)
    seed_fb = sum(1 for s in fb if s["ultimo_W2B"] is None)
    print(f"first-bad ({len(fb)}): da-seme-mai-dipinte {seed_fb}; "
          f"eta_paint med {ages[len(ages) // 2] if ages else None} "
          f"max {ages[-1] if ages else None}; gap_ep med "
          f"{gaps[len(gaps) // 2] if gaps else None} max "
          f"{gaps[-1] if gaps else None}; n_vis med "
          f"{nvis[len(nvis) // 2] if nvis else None}", flush=True)

    out["gate1"] = {"n_canonici": n, "n_T": n_T, "n_R_short": n_Rshort,
                    "n_compat": n_comp, "regressione_csv": True,
                    "regressione_hunt": True}
    out["hnr"] = {"eventi": n_ev, "riusati": len(reuse),
                  "non_consecutivi": nonconsec, "verdetto":
                  "UCCISA (gate 5)" if reuse else "regge sul campione",
                  "esempi": esempi}
    out["first_bad_agg"] = {
        "n": len(fb), "da_seme": seed_fb,
        "eta_paint_med": ages[len(ages) // 2] if ages else None,
        "eta_paint_max": ages[-1] if ages else None,
        "gap_ep_hist": {str(g): gaps.count(g) for g in sorted(set(gaps))},
        "n_vis_med": nvis[len(nvis) // 2] if nvis else None}
    out["per_record"] = [{k: v for k, v in r.items()
                          if k not in ("shields", "whites")}
                         for r in all_rows]
    out["elapsed_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
