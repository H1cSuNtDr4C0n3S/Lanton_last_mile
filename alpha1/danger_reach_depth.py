# danger_reach_depth.py — §107c: profondita' minima di raggiungibilita' per
# cella — il raggio temporale del "deposito antico" (§107b).
#
# OGGETTO: per i 2 lock reali (§101) — e per OGNI cella toccata dall'albero
# dei prepend — la profondita' minima d_hit alla quale un passato valido
# record-compatibile la legge, contro il lower bound GEOMETRICO D_geo (BFS su
# (posa, heading) con solo y>=1, senza alternanza/req: deduttivo, rilassa i
# vincoli => D_geo <= d_hit sempre). TRIPLA per cella:
#     (D_geo, D_exh, d_hit)
# dove D_exh = profondita' massima con esplorazione ESAUSTIVA completata
# (nessun budget scattato). Cella non colpita a D_exh => IRRAGGIUNGIBILE da
# ogni passato valido di profondita' <= D_exh (enunciato deduttivo che
# TRASFERISCE alle orbite reali: l'albero e' una sovra-approssimazione).
# Ogni d_hit e' etichettato SOVRA finche' non realizzato (trappole c/z).
#
# GATE DEL GAP (preregistrato, confronto a 2 round §107c; metodo §84 baseline
# nulla condizionata, nessuna soglia — qq): per le celle di R_T vs celle
# MATCHED non-R_T fuori-footprint a pari (lato, D_geo), confrontare le
# distribuzioni del gap d_hit - D_geo (censurate a D_exh dichiarato).
# Aspettativa preregistrata: il gap su R_T domina ordinalmente il matched
# (mediana vs mediana, n dichiarato; censura = +inf per il rango).
# Morte dichiarata: se indistinguibile, la tabella e' il Cuneo riscritto
# (terza ri-descrizione) e il fronte passa al consolidamento.
#
# GATES MECCANICI (tutti possono fallire):
#   R0  regressione: dfs_census a depth 28 sui 2 lock == summary §107b
#       (nodi, nodi_per_depth, cap, cell_bits bit-identici).
#   R0b coerenza census<->reach: bits[nero]+bits[bianco]==0 a D=28
#       <=> d_hit assente o > 28.
#   R1  controllo positivo: LOCKA cella ancora (-1,5) d_hit == 1.
#   RG  D_geo(c) <= d_hit(c) per ogni cella colpita.
#
# CONVENZIONE DICHIARATA (caveat §107b.6): onset_germe e' misurato DAL
# RECORD; asse assoluto = og + 101. Unita' di TUTTE le profondita': PASSI
# all'indietro dal bordo di w (trappola nn: in epoche-record possono essere
# recenti; la conversione non e' fatta qui).
#
# Uscita: alpha1/danger_reach_depth_summary.json
import sys, os, json, time, argparse
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from delta4_long_orbits import build_seed
from record_word_census import run_collect_records
from danger_backward_autopsy import Machine, dfs_census, K

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "danger_reach_depth_summary.json")
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
REF = os.path.join(HERE, "danger_backward_autopsy_summary.json")


def to_anchor(m, c):
    x0, y0, _ = m.pose_end
    return rotk((c[0] - x0, c[1] - y0), m.k_rot)


def geo_bfs(m, depth_cap):
    """Lower bound geometrico: BFS all'indietro su (posa, heading) con SOLO
    il vincolo record-compat y>=1 (niente alternanza, niente req). Rilassa i
    vincoli dell'albero vero => per ogni cella D_geo <= d_hit (RG).
    Ritorna: dict posizione_walk -> profondita' minima."""
    dist = {}
    seen = {((0, 0), 0)}
    frontier = deque([((0, 0), 0)])
    d = 0
    while frontier and d < depth_cap:
        d += 1
        nxt = deque()
        for p, h in frontier:
            p_prev = (p[0] - DX[h], p[1] - DY[h])
            if m.anchor_y(p_prev) < 1:
                continue
            if p_prev not in dist:
                dist[p_prev] = d
            for h_prev in ((h - 1) & 3, (h + 1) & 3):
                s = (p_prev, h_prev)
                if s not in seen:
                    seen.add(s)
                    nxt.append(s)
        frontier = nxt
    return dist


def reach_dfs(m, depth_cap, node_budget=2_000_000_000, budget_s=7200):
    """DFS esaustiva dell'albero dei prepend validi (stessa transizione della
    macchina F2 validata: alternanza + y>=1), che registra per OGNI posizione
    la profondita' minima di lettura. Nessuna pota, nessuna classificazione.
    Ritorna: first_hit (pos_walk -> prof.min), nodi_per_depth, nodi, troncato."""
    t0 = time.time()
    req = dict(m.req0)
    first_hit = {}
    stats = [0] * (depth_cap + 1)
    nodes = [0]
    truncated = [False]

    def visit(p, h, d):
        if nodes[0] >= node_budget or \
                (nodes[0] & 0xFFFF) == 0 and time.time() - t0 > budget_s:
            truncated[0] = True
            return
        nodes[0] += 1
        stats[d] += 1
        if d == depth_cap:
            return
        p_prev = (p[0] - DX[h], p[1] - DY[h])
        if m.anchor_y(p_prev) < 1:
            return
        seen = p_prev in req
        dn = d + 1
        for c in (0, 1):
            if seen and c != 1 - req[p_prev]:
                continue
            if p_prev not in first_hit or dn < first_hit[p_prev]:
                first_hit[p_prev] = dn
            h_prev = (h - 1) & 3 if c == 0 else (h + 1) & 3
            old = req.get(p_prev)
            req[p_prev] = c
            visit(p_prev, h_prev, dn)
            if seen:
                req[p_prev] = old
            else:
                del req[p_prev]

    sys.setrecursionlimit(depth_cap + 200)
    visit((0, 0), 0, 0)
    return first_hit, stats, nodes[0], truncated[0]


def censored_median(gaps):
    """Mediana ordinale con censure (None = mai colpita entro D_exh) trattate
    come +inf, DICHIARATO. Ritorna (mediana_o_'cens', n, n_censurate)."""
    n = len(gaps)
    if n == 0:
        return None, 0, 0
    n_cens = sum(1 for g in gaps if g is None)
    fin = sorted(g for g in gaps if g is not None)
    mid = n // 2
    if mid < len(fin):
        return fin[mid], n, n_cens
    return "cens", n, n_cens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth-a", type=int, default=36)
    ap.add_argument("--depth-b", type=int, default=32)
    ap.add_argument("--budget-s", type=int, default=3600)
    ap.add_argument("--skip-r0", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    hunt = json.load(open(HUNT))
    ref = json.load(open(REF))
    out = {"convenzione": "onset_germe misurato DAL RECORD (asse assoluto = "
                          "og+101); profondita' in PASSI all'indietro dal "
                          "bordo di w; d_hit = etichetta SOVRA "
                          "(sovra-approssimazione, non realizzato)",
           "episodi": []}
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        label = f"LOCK{'AB'[i]}"
        depth = args.depth_a if i == 0 else args.depth_b
        seed, _, _ = build_seed(rngs, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        w = tuple(turns[t - K:t])
        m = Machine(w)
        rt_anchor = set(m.rt_walk.values())
        foot_anchor = {to_anchor(m, c) for c in m.req0}
        print(f"[{label}] |R_T|={len(m.rt_walk)} og={m.onset_germe} "
              f"depth_run={depth}", flush=True)

        # ---- R0: regressione bit-identica vs summary §107b (depth 28) ----
        if not args.skip_r0:
            t_r0 = time.time()
            stats28, cap28, n28, tr28, _, bits28 = dfs_census(
                m, 28, budget_s=args.budget_s)
            r = ref["episodi"][i]
            ok = (not tr28 and n28 == r["nodi"] and cap28 == r["cap"] and
                  {str(d): stats28[d]["nodi"] for d in stats28} ==
                  r["nodi_per_depth"] and
                  {str(k): v for k, v in sorted(bits28.items())} ==
                  r["cell_bits"])
            dt = time.time() - t_r0
            print(f"[{label}] R0 regressione D=28: "
                  f"{'OK bit-identica' if ok else 'FALLITA'} "
                  f"({n28} nodi, {dt:.1f} s, {dt / max(1, n28) * 1e9:.0f} "
                  f"ns/nodo)", flush=True)
            assert ok, f"R0 FALLITO {label}"
        else:
            bits28 = None

        # ---- geometria: D_geo ----
        geo = geo_bfs(m, depth)
        # ---- reach ----
        t_r = time.time()
        first_hit, stats, nodes, truncated = reach_dfs(
            m, depth, budget_s=args.budget_s)
        dt = time.time() - t_r
        d_exh = depth if not truncated else None
        print(f"[{label}] reach D={depth}: nodi {nodes} in {dt:.1f} s "
              f"({dt / max(1, nodes) * 1e9:.0f} ns/nodo)"
              f"{' TRONCATO (niente esaustivita a questo cap)' if truncated else ''}",
              flush=True)
        assert not truncated, (f"{label}: run troncata a D={depth} — "
                               f"abbassare la profondita' (D_exh non valido)")

        # ---- gate R1/R0b/RG ----
        fh_anchor = {}
        for p, d in first_hit.items():
            ca = to_anchor(m, p)
            if ca not in fh_anchor or d < fh_anchor[ca]:
                fh_anchor[ca] = d
        if i == 0:
            assert fh_anchor.get((-1, 5)) == 1, \
                f"R1 FALLITO: (-1,5) d_hit={fh_anchor.get((-1, 5))}"
            print(f"[{label}] R1 OK: (-1,5) d_hit=1", flush=True)
        if bits28 is not None:
            for ca, bits in bits28.items():
                unreached28 = (bits[0] + bits[1] == 0)
                hit28 = ca in fh_anchor and fh_anchor[ca] <= 28
                assert unreached28 == (not hit28), \
                    f"R0b FALLITO {label} {ca}: bits={bits} " \
                    f"d_hit={fh_anchor.get(ca)}"
            print(f"[{label}] R0b OK: census<->reach coerenti a D=28",
                  flush=True)
        geo_anchor = {}
        for p, d in geo.items():
            ca = to_anchor(m, p)
            if ca not in geo_anchor or d < geo_anchor[ca]:
                geo_anchor[ca] = d
        for ca, dh in fh_anchor.items():
            dg = geo_anchor.get(ca)
            assert dg is not None and dg <= dh, \
                f"RG FALLITO {ca}: D_geo={dg} d_hit={dh}"
        print(f"[{label}] RG OK: D_geo <= d_hit su {len(fh_anchor)} celle",
              flush=True)

        # ---- tripla per cella di R_T ----
        tripla = {}
        for ca in sorted(rt_anchor):
            tripla[str(ca)] = {"D_geo": geo_anchor.get(ca),
                               "D_exh": d_exh,
                               "d_hit_sovra": fh_anchor.get(ca)}
        print(f"[{label}] TRIPLA (D_geo, D_exh={d_exh}, d_hit-SOVRA):",
              flush=True)
        n_unreach = 0
        for ca in sorted(rt_anchor):
            tr = tripla[str(ca)]
            if tr["d_hit_sovra"] is None:
                n_unreach += 1
            print(f"    {ca}: D_geo={tr['D_geo']} "
                  f"d_hit={tr['d_hit_sovra'] if tr['d_hit_sovra'] is not None else f'>{d_exh} (IRRAGGIUNGIBILE-ESAUSTIVO)'}",
                  flush=True)
        print(f"[{label}] irraggiungibili-esaustive a D={d_exh}: "
              f"{n_unreach}/{len(rt_anchor)}", flush=True)

        # ---- gate del GAP vs matched (preregistrato, ordinale) ----
        # pool matched: celle con D_geo definito, non-R_T, fuori-footprint,
        # stesso lato (sign x ancora) e stesso D_geo della cella R_T.
        gaps_rt, gaps_mt = [], []
        pool_by = {}
        for ca, dg in geo_anchor.items():
            if ca in rt_anchor or ca in foot_anchor:
                continue
            side = (ca[0] > 0) - (ca[0] < 0)
            pool_by.setdefault((side, dg), []).append(ca)
        n_match_tot = 0
        for ca in sorted(rt_anchor):
            dg = geo_anchor.get(ca)
            if dg is None:
                continue  # fuori dal raggio geometrico a questo depth: contato
            dh = fh_anchor.get(ca)
            gaps_rt.append(None if dh is None else dh - dg)
            side = (ca[0] > 0) - (ca[0] < 0)
            for cb in pool_by.get((side, dg), []):
                dhb = fh_anchor.get(cb)
                gaps_mt.append(None if dhb is None else dhb - dg)
                n_match_tot += 1
        med_rt, n_rt_g, cens_rt = censored_median(gaps_rt)
        med_mt, n_mt_g, cens_mt = censored_median(gaps_mt)
        print(f"[{label}] GAP gate: R_T mediana={med_rt} (n={n_rt_g}, "
              f"cens={cens_rt}) vs MATCHED mediana={med_mt} (n={n_mt_g}, "
              f"cens={cens_mt})", flush=True)

        out["episodi"].append({
            "label": label, "rngstate": rngs, "t": t,
            "n_rt": len(m.rt_walk), "onset_germe": m.onset_germe,
            "depth": depth, "d_exh": d_exh, "nodi": nodes,
            "ns_per_nodo": round(dt / max(1, nodes) * 1e9, 1),
            "nodi_per_depth": {str(d): stats[d] for d in range(depth + 1)},
            "tripla_rt": tripla,
            "irraggiungibili_esaustive": n_unreach,
            "gap_rt": [g if g is not None else "cens" for g in gaps_rt],
            "gap_matched_n": n_mt_g, "gap_matched_cens": cens_mt,
            "gap_rt_mediana": med_rt, "gap_matched_mediana": med_mt,
            "first_hit_anchor_rt": {str(ca): fh_anchor.get(ca)
                                    for ca in sorted(rt_anchor)},
            "gates": {"R0": not args.skip_r0, "R0b": bits28 is not None,
                      "R1": i == 0, "RG": True}})

    out["elapsed_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
