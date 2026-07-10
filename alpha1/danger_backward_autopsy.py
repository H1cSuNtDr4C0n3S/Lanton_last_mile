# danger_backward_autopsy.py — §107b F2: autopsia all'indietro delle parole-lock.
#
# OGGETTO (round-2 §107b, riduzione del residuo): per una parola pericolosa w
# (i 2 lock reali §101), classificare TUTTI i passati record-compatibili di
# profondita' <= D per il colore che lasciano alle celle di R_T(w) al record.
#
# SEMANTICA (deduttiva, dal flip di Langton):
#   - una cella di R_T visitata nella finestra estesa ha colore-a-t DECISO
#     dall'ULTIMA visita (la prima incontrata andando all'indietro, perche'
#     R_T ∩ footprint(w) = ∅ e i prepend aggiungono solo visite PIU' VECCHIE):
#     lettura bianca => lasciata NERA (SHIELD), lettura nera => lasciata BIANCA.
#   - la decisione e' STABILE sotto prepend piu' profondi. Classi al cap D:
#     SHIELD:    >=1 cella decisa nera  => rigetto al record GARANTITO.
#     WHITE_ALL: TUTTE le celle decise bianche => LOCK GARANTITO (certificato).
#     OPEN:      celle mai visitate entro D => verdetto oltre-D (G_unk);
#                i lock reali vivono qui (13/14 e 9/9 mai-visitate §105b).
#   NOTA v2 (riparazione in-sessione): la v1 potava il sottoalbero alla prima
#   decisione e riportava conteggi di FOGLIE — misura distorta (una shield-leaf
#   a prof. 1 pesa ~meta' dei passati di prof. D ma contava 1; parente hh/oo).
#   La v2 estende TUTTI i passati validi al cap e classifica al cap; in piu'
#   riporta la distribuzione PER-CELLA dei bit dell'OR-kernel all'orizzonte D.
#
# MACCHINA: DFS all'indietro nel frame del cammino di w. Stato = (posa, heading
# d'arrivo, req: cella -> colore a inizio-finestra). Passo indietro: p_prev =
# p - D[h]; scelta c in {bianco,nero} => h_prev = h-1 / h+1; vincolo alternanza
# c == 1 - req[p_prev] se gia' letta, libera altrimenti; record-compat: p_prev
# con y>=1 nel frame ancora (record y-min stretto). Realizzabilita' = alternanza
# (fresche libere, rivisite forzate, §2 CLAUDE.md).
#
# GATES (in sessione, lente PRIMA del run lungo — lezione §93/§94):
#   GA (lente indipendente): conteggi per profondita' <= 12 bit-identici alla
#       enumerazione naive con virtual_walk sulla parola intera estesa.
#   GB (controllo positivo): il passato REALE dell'episodio deve percorrere la
#       macchina valido a ogni profondita' e MAI classificato SHIELD
#       (LOCKA: 1 cella decisa BIANCA a prof. ~1, 13 open; LOCKB: 9 open).
#   GC: R_T ∩ footprint(w) = ∅ verificata in codice (non assunta).
# Dichiarazioni (trappole w/y/ee/ii): esaustivo fino a D dichiarata, oltre =
# INDECISO; nessuna soglia; il primo sconfinamento e' un dato, non un rosso.
#
# Uscita: alpha1/danger_backward_autopsy_summary.json
import sys, os, json, time, argparse

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from delta4_long_orbits import build_seed
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from speed_limit_theorem import transient_readset_from_germ

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "danger_backward_autopsy_summary.json")
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
K = 101


def inv_rotk(c, k):
    return rotk(c, (4 - k) % 4)


class Machine:
    """Stato della finestra estesa nel frame del cammino di w (start (0,0,h=0))."""

    def __init__(self, w):
        self.w = w
        grid, pose = virtual_walk(w)
        assert grid is not None
        self.pose_end = pose                      # (x0, y0, h0) al record
        x0, y0, h0 = pose
        self.k_rot = (-h0) % 4
        # req = colore a inizio-finestra (PRIMA lettura in w, non colore finale)
        self.req0 = {}
        x = y = 0
        h = 0
        for wbit in w:
            c = (x, y)
            need = 0 if wbit else 1
            if c not in self.req0:
                self.req0[c] = need
            if wbit:
                h = (h + 1) & 3
            else:
                h = (h + 3) & 3
            x += DX[h]
            y += DY[h]
        # R_T in frame ancora -> frame cammino
        r = eval_word(w)
        assert r is not None
        self.onset_germe = r[1]
        rs_anchor = [c for (c, tf) in
                     transient_readset_from_germ(w, self.onset_germe)]
        self.rt_walk = {}
        for ca in rs_anchor:
            cw = inv_rotk(ca, self.k_rot)
            cwa = (cw[0] + x0, cw[1] + y0)
            self.rt_walk[cwa] = ca
        # GC: disgiunzione verificata (req0 = footprint di w)
        for cwa in self.rt_walk:
            assert cwa not in self.req0, f"GC FALLITO: R_T interseca footprint"

    def anchor_y(self, c):
        x0, y0, _ = self.pose_end
        return rotk((c[0] - x0, c[1] - y0), self.k_rot)[1]


def dfs_census(m, depth_cap, node_budget=60_000_000, budget_s=1800):
    """DFS esaustiva SENZA potatura di classificazione (v2, riparata): ogni
    passato valido viene esteso fino al cap e classificato SOLO al cap.
    (La v1 potava alla prima decisione e contava FOGLIE: misura distorta —
    una shield-leaf a prof. 1 pesa ~meta' dei passati di prof. D ma contava 1.
    Parente delle trappole hh/oo: il conteggio era politica-pesato.)
    Ritorna: conteggi nodi per profondita', classi al cap, istogramma tocchi,
    statistica PER-CELLA dei bit al cap (nero/bianco/indeciso)."""
    t0 = time.time()
    req = dict(m.req0)
    decided = {}                    # cella_walk R_T -> colore a t (0/1)
    stats = {d: {"nodi": 0} for d in range(depth_cap + 1)}
    cap = {"shield": 0, "white_all": 0, "open": 0}
    touch_hist = {}                 # n celle decise al cap -> conteggio
    cell_bits = {ca: [0, 0, 0] for ca in m.rt_walk.values()}  # [nero,bianco,ind]
    nodes = [0]
    truncated = [False]

    def visit(p, h, d):
        if nodes[0] >= node_budget or time.time() - t0 > budget_s:
            truncated[0] = True
            return
        nodes[0] += 1
        stats[d]["nodi"] += 1
        if d == depth_cap:
            n_black = sum(1 for v in decided.values() if v == 1)
            if n_black:
                cap["shield"] += 1
            elif len(decided) == len(m.rt_walk):
                cap["white_all"] += 1
            else:
                cap["open"] += 1
            touch_hist[len(decided)] = touch_hist.get(len(decided), 0) + 1
            for cw, ca in m.rt_walk.items():
                v = decided.get(cw)
                cell_bits[ca][2 if v is None else (0 if v == 1 else 1)] += 1
            return
        p_prev = (p[0] - DX[h], p[1] - DY[h])
        if m.anchor_y(p_prev) < 1:
            return                                    # record-compat viola
        seen = p_prev in req
        for c in (0, 1):
            if seen and c != 1 - req[p_prev]:
                continue
            h_prev = (h - 1) & 3 if c == 0 else (h + 1) & 3
            old = req.get(p_prev)
            req[p_prev] = c
            dec_here = (not seen) and (p_prev in m.rt_walk)
            if dec_here:
                decided[p_prev] = 1 - c
            visit(p_prev, h_prev, d + 1)
            if dec_here:
                del decided[p_prev]
            if seen:
                req[p_prev] = old
            else:
                del req[p_prev]

    sys.setrecursionlimit(depth_cap + 100)
    visit((0, 0), 0, 0)
    return stats, cap, nodes[0], truncated[0], touch_hist, cell_bits


def naive_census(m, depth_cap):
    """Lente indipendente GA (v2, senza potatura come la macchina): enumerazione
    con virtual_walk sull'intera parola estesa, classificazione SOLO al cap."""
    from collections import deque
    stats = {d: {"nodi": 0} for d in range(depth_cap + 1)}
    cap = {"shield": 0, "white_all": 0, "open": 0}
    w = list(m.w)

    def classify(pre):
        """None se invalida; altrimenti (n_nere, n_bianche) decise al record."""
        full = pre + w
        grid, pose = virtual_walk(tuple(full))
        if grid is None:
            return None
        anchor_cells = to_anchor_frame(grid, pose)
        if any(cy < 1 for (_, cy) in anchor_cells):
            return None
        order = {}
        x = y = 0
        h = 0
        for wbit in full:
            c = (x, y)
            order[c] = 0 if wbit else 1        # ultima lettura: colore letto
            if wbit:
                h = (h + 1) & 3
            else:
                h = (h + 3) & 3
            x += DX[h]
            y += DY[h]
        fx, fy, fh = pose
        kk = (-fh) % 4
        rt_anchor = set(m.rt_walk.values())
        n_black = n_white = 0
        for c, lc in order.items():
            ca = rotk((c[0] - fx, c[1] - fy), kk)
            if ca in rt_anchor:
                if 1 - lc == 1:
                    n_black += 1
                else:
                    n_white += 1
        return n_black, n_white

    frontier = deque([[]])
    for d in range(depth_cap + 1):
        nxt = deque()
        for pre in frontier:
            v = classify(pre)
            if v is None:
                continue
            stats[d]["nodi"] += 1
            if d == depth_cap:
                n_black, n_white = v
                if n_black:
                    cap["shield"] += 1
                elif n_black + n_white == len(m.rt_walk):
                    cap["white_all"] += 1
                else:
                    cap["open"] += 1
                continue
            for b in (0, 1):
                nxt.append([b] + pre)
        frontier = nxt
    return stats, cap


def real_branch(m, turns, t, depth_cap):
    """GB: percorre il passato reale nella macchina. Ritorna la traccia."""
    req = dict(m.req0)
    decided = {}
    p, h = (0, 0), 0
    trace = []
    for d in range(1, depth_cap + 1):
        j = t - K - d
        assert j >= 0
        bit = turns[j]
        c = 0 if bit else 1
        p_prev = (p[0] - DX[h], p[1] - DY[h])
        assert m.anchor_y(p_prev) >= 1, f"GB: record-compat viola a prof {d}"
        if p_prev in req:
            assert c == 1 - req[p_prev], f"GB: alternanza viola a prof {d}"
        else:
            if p_prev in m.rt_walk:
                decided[p_prev] = 1 - c
        req[p_prev] = c
        h = (h - 1) & 3 if c == 0 else (h + 1) & 3
        p = p_prev
        n_shield = sum(1 for v in decided.values() if v == 1)
        assert n_shield == 0, f"GB FALLITO: passato reale SHIELD a prof {d}"
        trace.append({"d": d, "decise_bianche":
                      sum(1 for v in decided.values() if v == 0),
                      "open": len(m.rt_walk) - len(decided)})
    return trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=28)
    ap.add_argument("--depth-a", type=int, default=36)
    ap.add_argument("--lens-depth", type=int, default=12)
    ap.add_argument("--budget-s", type=int, default=1800)
    ap.add_argument("--baseline", type=int, default=4)
    ap.add_argument("--baseline-depth", type=int, default=22)
    ap.add_argument("--scan-danger", action="store_true")
    ap.add_argument("--scan-depth", type=int, default=22)
    args = ap.parse_args()
    t0 = time.time()
    hunt = json.load(open(HUNT))
    out = {"depth": args.depth, "episodi": []}
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        label = f"LOCK{'AB'[i]}"
        seed, _, _ = build_seed(rngs, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        w = tuple(turns[t - K:t])
        m = Machine(w)
        print(f"[{label}] |R_T|={len(m.rt_walk)} onset_germe={m.onset_germe}",
              flush=True)
        # GB prima (controllo positivo, economico)
        gb = real_branch(m, turns, t, min(args.depth, t - K))
        print(f"[{label}] GB passato reale: OK fino a prof "
              f"{len(gb)} (decise bianche {gb[-1]['decise_bianche']}, "
              f"open {gb[-1]['open']})", flush=True)
        # GA lente indipendente a profondita' ridotta
        lens_d = args.lens_depth
        stats_l, cap_l = naive_census(m, lens_d)
        stats_m, cap_m, nn, trunc, _, _ = dfs_census(m, lens_d,
                                                     budget_s=args.budget_s)
        ga_ok = (cap_l == cap_m and
                 all(stats_l[d] == stats_m[d] for d in range(lens_d + 1)))
        print(f"[{label}] GA lente naive vs macchina (prof <= {lens_d}): "
              f"{'OK bit-identici' if ga_ok else 'FALLITO'} "
              f"(cap {cap_m})", flush=True)
        assert ga_ok, f"GA FALLITO {label}: naive {cap_l} vs macchina {cap_m}"
        # run pieno
        depth = args.depth
        stats, cap, nodes, truncated, touch, cell_bits = dfs_census(
            m, depth, budget_s=args.budget_s)
        n_cap = sum(cap.values())
        print(f"[{label}] depth {depth}, nodi {nodes}"
              f"{' (TRONCATO)' if truncated else ''}: passati validi al cap "
              f"{n_cap} — shield {cap['shield']} "
              f"({cap['shield'] / max(1, n_cap):.4f}), white_all "
              f"{cap['white_all']}, open {cap['open']}; touch {touch}",
              flush=True)
        print(f"[{label}] bit per-cella al cap [nero,bianco,indeciso]:",
              flush=True)
        for ca, bits in sorted(cell_bits.items()):
            print(f"    {ca}: {bits}", flush=True)
        out["episodi"].append({
            "label": label, "rngstate": rngs, "t": t,
            "n_rt": len(m.rt_walk), "onset_germe": m.onset_germe,
            "GB_trace_ultimo": gb[-1], "GA_lens_depth": lens_d,
            "depth": depth, "nodi": nodes, "troncato": truncated,
            "nodi_per_depth": {str(d): stats[d]["nodi"] for d in stats},
            "cap": cap,
            "touch_cap_hist": {str(k): v for k, v in touch.items()},
            "cell_bits": {str(k): v for k, v in sorted(cell_bits.items())}})

    # ---- BASELINE: parole ordinarie (R_T > 50) a onset_germe minimo ----
    # CONFOUND DICHIARATO: R_T grande e' banalmente piu' facile da toccare;
    # la baseline quota il verso del confronto, non lo elimina. Appaiamento
    # imperfetto: le ordinarie a og ~55-65 non esistono (og piccolo <=> R_T
    # piccolo: F0); si prendono le og minime disponibili fra le n>50.
    if args.baseline > 0:
        census = json.load(open(os.path.join(
            HERE, "danger_geometry_census.json")))["per_word"]
        cand = sorted(((inf["onset_germe"], ws) for ws, inf in census.items()
                       if inf["n"] > 50), key=lambda x: x[0])
        for og, ws in cand[:args.baseline]:
            w = tuple(1 if ch == "R" else 0 for ch in ws)
            m = Machine(w)
            stats_l, cap_l = naive_census(m, 8)
            stats_m8, cap_m8, _, _, _, _ = dfs_census(m, 8, budget_s=60)
            ga_ok = (cap_l == cap_m8 and
                     all(stats_l[d] == stats_m8[d] for d in range(9)))
            assert ga_ok, f"GA baseline FALLITO og={og}"
            stats, cap, nodes, truncated, touch, cell_bits = dfs_census(
                m, args.baseline_depth, budget_s=args.budget_s)
            n_cap = sum(cap.values())
            print(f"[BASE og={og} n_rt={len(m.rt_walk)}] depth "
                  f"{args.baseline_depth}, nodi {nodes}"
                  f"{' (TRONCATO)' if truncated else ''}: cap {n_cap} — "
                  f"shield {cap['shield']} "
                  f"({cap['shield'] / max(1, n_cap):.4f}), white_all "
                  f"{cap['white_all']}, open {cap['open']}", flush=True)
            out.setdefault("baseline", []).append({
                "word": ws, "onset_germe": og, "n_rt": len(m.rt_walk),
                "depth": args.baseline_depth, "nodi": nodes,
                "troncato": truncated, "GA_depth8": True, "cap": cap,
                "touch_cap_hist": {str(k): v for k, v in touch.items()},
                "nodi_per_depth": {str(d): stats[d]["nodi"] for d in stats}})
    # ---- SCAN sigma_D sulla classe pericolosa intera (<=50) ----
    # sigma_D(w) = quota shield dei passati validi di profondita' D:
    # funzionale word-decidibile; domanda: i 2 lock sono estremi anche DENTRO
    # la classe (discriminante di (ii) word-side) o tipici (=> fortuna della
    # pre-storia, coerente con §106-T3)?
    if args.scan_danger:
        census = json.load(open(os.path.join(
            HERE, "danger_geometry_census.json")))["per_word"]
        dws = sorted(((inf["n"], ws) for ws, inf in census.items()
                      if inf["n"] <= 50), key=lambda x: x[0])
        lock_ws = {ep["label"]: None for ep in out["episodi"]}
        lock_strings = {}
        for ep in out["episodi"]:
            lock_strings[ep["label"]] = None
        scan = []
        for n_rt, ws in dws:
            w = tuple(1 if ch == "R" else 0 for ch in ws)
            m = Machine(w)
            stats, cap, nodes, truncated, touch, cell_bits = dfs_census(
                m, args.scan_depth, budget_s=120)
            n_cap = sum(cap.values())
            sigma = cap["shield"] / max(1, n_cap)
            n_unreach = sum(1 for b in cell_bits.values()
                            if b[0] + b[1] == 0)
            scan.append({"word": ws, "n_rt": n_rt,
                         "onset_germe": m.onset_germe,
                         "depth": args.scan_depth, "cap": n_cap,
                         "sigma": round(sigma, 5),
                         "celle_irraggiungibili": n_unreach,
                         "troncato": truncated})
            print(f"[SCAN n_rt={n_rt:3d} og={m.onset_germe:4d}] cap {n_cap:8d} "
                  f"sigma {sigma:.4f} irr {n_unreach}/{n_rt}"
                  f"{' TRONCATO' if truncated else ''}", flush=True)
        out["scan_danger"] = scan
        sig = sorted(s["sigma"] for s in scan)
        print(f"sigma_D classe pericolosa: min {sig[0]} med "
              f"{sig[len(sig) // 2]} max {sig[-1]}", flush=True)
    out["elapsed_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
