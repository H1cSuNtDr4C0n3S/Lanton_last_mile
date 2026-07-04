# u2_far_closure_hunt.py — §93 (U2-LONTANO): la CACCIA ALLA CHIUSURA DEL LEDGER.
#
# ATTACCO (falsificazionismo prima del certificato): cerca un'estensione
# all'indietro sopra coprente-nera + w101 che
#   (i)  chiuda TUTTI i pending in-palla-R  (pend_in == 0), e
#   (ii) abbia la coda (posa di nascita) FUORI dalla palla (cheb > R).
# Un successo = testimone che UCCIDE la forma-palla di U2-LONTANO al raggio R:
# troncando li' la storia, seme = prime-letture-nere (tutte fuori palla),
# nascita fuori palla, record y-min stretto con suffisso w101 e palla senza seme.
# (Monotonia: successo a R' >= R implica successo a R => falsificare ai raggi
# PICCOLI e' l'attacco piu' forte; impossibilita' a R si eredita a R' >= R.)
#
# METODO (antidoto trappola bb — niente best-first puro):
#   passeggiate casuali PROFONDE con steering verso il pending aperto piu' vicino
#   (in-palla) / verso la palla (se fuori), parametri di politica RANDOMIZZATI per
#   passeggiata (p_steer, p_L, fase wild iniziale, budget passi), multiprocessing
#   BelowNormal. Su celle rivisitate la lettura e' FORZATA (alternanza): i soli
#   punti di scelta sono le celle fresche (R = nessun debito, L = +1 pending).
#
# CONTROLLI NEGATIVI: coprenti confinate (D4/D12) — il muro intero muore a
# profondita' <= 12, la caccia DEVE fallire su di esse (e fallisce per
# enumerazione finita, exact_wall §92); incluse per onesta' del gate.
#
# Uscita: alpha1/u2_far_closure_hunt_summary.json (+ .log append-only)
import sys, os, json, time, random, argparse, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, FREE
from u2_far_ledger import cheb, pend_set
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
CC = os.path.join(HERE, "record_cover_census_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_closure_hunt_summary.json")
LOG = os.path.join(HERE, "u2_far_closure_hunt.log")


def _below_normal():
    """Priorita' BelowNormal (convenzione §4), senza dipendenze esterne."""
    try:
        import ctypes
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, 0x4000)
    except Exception:
        pass


class Walker:
    """Stato del camminatore all'indietro con ledger in-palla e undo esatto."""
    __slots__ = ("c", "h", "req", "pend_in", "R", "bits", "trail")

    def __init__(self, c, h, req, pend_in, R):
        self.c = c; self.h = h
        self.req = dict(req)
        self.pend_in = set(pend_in)
        self.R = R
        self.bits = []
        self.trail = []

    def next_cell(self):
        return (self.c[0] - DX[self.h], self.c[1] - DY[self.h])

    def apply(self, bit):
        """Prepend del bit (DEVE essere lecito). Aggiorna ledger, salva undo."""
        cn = self.next_cell()
        read = 0 if bit == 1 else 1
        old_req = self.req.get(cn, FREE)
        pd = 0
        if cheb(cn) <= self.R:
            if read == 1 and cn not in self.pend_in:
                pd = 1
            elif read == 0 and cn in self.pend_in:
                pd = -1
        self.trail.append((self.c, self.h, cn, old_req, pd))
        self.req[cn] = 1 - read
        if pd == 1:
            self.pend_in.add(cn)
        elif pd == -1:
            self.pend_in.discard(cn)
        self.h = (self.h - 1) & 3 if bit == 1 else (self.h + 1) & 3
        self.c = cn
        self.bits.append(bit)

    def undo(self):
        c_prev, h_prev, cu, old_req, pd = self.trail.pop()
        if old_req is FREE:
            del self.req[cu]
        else:
            self.req[cu] = old_req
        if pd == 1:
            self.pend_in.discard(cu)
        elif pd == -1:
            self.pend_in.add(cu)
        self.c, self.h = c_prev, h_prev
        self.bits.pop()


def bounded_dfs(walker, goal, rng, p_steer, node_budget, best=None):
    """DFS con backtracking dallo stato corrente del walker fino a goal(walker)
    True. Ritorna ('goal', nodi) lasciando il walker SUL goal; ('exhausted', n)
    se l'albero e' finito e nessun nodo soddisfa il goal; ('budget', n) se il
    budget si esaurisce. In caso di non-goal il walker torna allo stato di
    partenza. Ordine rami: steering verso il pending in-palla piu' vicino."""
    depth0 = len(walker.bits)

    def order_bits():
        cn = walker.next_cell()
        if cn[1] < 1:
            return []
        r = walker.req.get(cn, FREE)
        if r != FREE:
            return [1 if r == 0 else 0]
        if walker.pend_in and rng.random() < p_steer:
            tgt = min(walker.pend_in, key=lambda p: abs(p[0] - cn[0])
                      + abs(p[1] - cn[1]))
            sc = []
            for b in (0, 1):
                hn = (walker.h - 1) & 3 if b == 1 else (walker.h + 1) & 3
                cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
                sc.append((abs(cnn[0] - tgt[0]) + abs(cnn[1] - tgt[1]), b))
            sc.sort(reverse=True)          # migliore per ULTIMO (pop dal fondo)
            return [b for _, b in sc]
        first = rng.randrange(2)
        return [1 - first, first]

    nodes = 0
    frames = [order_bits()]
    while frames and nodes < node_budget:
        alts = frames[-1]
        if not alts:
            frames.pop()
            if len(walker.bits) > depth0:
                walker.undo()
            continue
        bit = alts.pop()
        nodes += 1
        walker.apply(bit)
        if best is not None:
            np_ = len(walker.pend_in)
            if np_ < best["min_pend_in"]:
                best["min_pend_in"] = np_
                best["best_cells"] = sorted(walker.pend_in)
            if len(walker.bits) > best["max_depth"]:
                best["max_depth"] = len(walker.bits)
            if cheb(walker.c) > walker.R and (best["min_pend_in_out"] is None
                                              or np_ < best["min_pend_in_out"]):
                best["min_pend_in_out"] = np_
        if goal(walker):
            return "goal", nodes
        frames.append(order_bits())
    if not frames:
        # albero esaurito: torna alla radice (gia' fatto dagli undo)
        return "exhausted", nodes
    # budget: srotola fino alla radice
    while len(walker.bits) > depth0:
        walker.undo()
    return "budget", nodes


def hunt_walks(job):
    """Worker: caccia a MILESTONE sopra w2 = ext+w101 con palla-R.
    Ogni restart: chiudi i pending in-palla UNO ALLA VOLTA (DFS mirato con
    commit greedy), poi cerca l'uscita dalla palla con ledger pulito.
    Ritorna best-tracking, flag di esaurimento albero, testimone se trovato."""
    (name, w2_str, R, seed, n_restarts, node_budget) = job
    _below_normal()
    rng = random.Random(seed)
    w2 = to_bits(w2_str)
    c0, h0, req0 = exact_state(w2)
    pend0_in = {c for c in pend_set(req0) if cheb(c) <= R}
    best = {"min_pend_in": len(pend0_in), "min_pend_in_out": None,
            "steps_done": 0, "deaths_y": 0, "witness": None,
            "max_depth": 0, "best_cells": sorted(pend0_in),
            "tree_exhausted": False, "milestones_ok": 0,
            "fail_budget": 0, "fail_exhausted": 0}

    for rs in range(n_restarts):
        p_steer = rng.choice((0.4, 0.7, 0.9))
        w = Walker(c0, h0, req0, pend0_in, R)
        commits = []                       # lunghezze delle estensioni commit
        repairs = 0
        # fase milestone: riduci len(pend_in) di 1 alla volta, con riparazione
        while w.pend_in:
            n_now = len(w.pend_in)
            len0 = len(w.bits)
            verdict, nodes = bounded_dfs(
                w, lambda wk: len(wk.pend_in) < n_now, rng, p_steer,
                node_budget, best)
            best["steps_done"] += nodes
            if verdict == "goal":
                best["milestones_ok"] += 1
                commits.append(len(w.bits) - len0)
                continue
            if verdict == "exhausted":
                best["fail_exhausted"] += 1
                if not w.bits:
                    # albero INTERO esaurito dalla radice: nessuna estensione
                    # chiude nemmeno UN pending — certificato DFS per questa
                    # coprente a questo raggio
                    best["tree_exhausted"] = True
                    return best
            else:
                best["fail_budget"] += 1
            # riparazione: disfa l'ultimo commit e riprova con altro ordine
            if commits and repairs < 3:
                repairs += 1
                for _ in range(commits.pop()):
                    w.undo()
                p_steer = rng.choice((0.4, 0.7, 0.9))
                continue
            break
        else:
            # tutti i pending chiusi: cerca l'uscita dalla palla a ledger pulito
            verdict, nodes = bounded_dfs(
                w, lambda wk: not wk.pend_in and cheb(wk.c) > wk.R,
                rng, p_steer, node_budget, best)
            best["steps_done"] += nodes
            if verdict == "goal":
                best["witness"] = {"nome": name, "R": R,
                                   "ext_bits": to_str(tuple(reversed(w.bits))),
                                   "passi": len(w.bits)}
                return best
    return best


def collect_targets():
    wit = json.load(open(WIT))
    cc = json.load(open(CC))
    tg = []
    for k, w in enumerate(wit["jackpot"]):
        tg.append((f"jackpot[{k}]", w["word"], "fuga"))
    for k, w in enumerate(wit["nere400"]):
        tg.append((f"nere400[{k}]", w["word"], "fuga"))
    # controlli negativi confinati
    tg.append(("D12[0]", wit["D12"][0]["word"], "confinata"))
    tg.append(("D4[0]", wit["D4"][0]["word"], "confinata"))
    return tg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radii", type=int, nargs="+", default=[8, 12, 16])
    ap.add_argument("--restarts-per-job", type=int, default=8,
                    help="DFS (con politica random) per job")
    ap.add_argument("--jobs-per-cell", type=int, default=6,
                    help="job per (testimone, R)")
    ap.add_argument("--node-budget", type=int, default=300_000,
                    help="nodi DFS per restart")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--seed", type=int, default=930)
    ap.add_argument("--tag", type=str, default="",
                    help="suffisso per i file di uscita (run parallele)")
    args = ap.parse_args()
    t0 = time.time()

    out_json = OUT_JSON.replace(".json", args.tag + ".json")
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    targets = collect_targets()
    log = open(LOG, "a")
    log.write(f"\n==== run {time.strftime('%Y-%m-%d %H:%M:%S')} args={vars(args)}\n")

    jobs = []
    jid = 0
    for name, wstr, kind in targets:
        e2 = to_bits(wstr)
        w2 = e2 + w101
        assert valid(w2)[1] is None, name
        for R in args.radii:
            for j in range(args.jobs_per_cell):
                jobs.append((name, to_str(w2), R,
                             args.seed * 100003 + jid, args.restarts_per_job,
                             args.node_budget))
                jid += 1
    print(f"{len(targets)} testimoni x {args.radii} raggi x "
          f"{args.jobs_per_cell} job = {len(jobs)} job "
          f"({args.restarts_per_job} DFS x {args.node_budget} nodi/job)",
          flush=True)

    agg = {}
    witness_found = None
    with mp.Pool(args.workers, initializer=_below_normal) as pool:
        for job, best in zip(jobs, pool.imap(hunt_walks, jobs, chunksize=1)):
            name, _, R = job[0], job[1], job[2]
            key = (name, R)
            a = agg.setdefault(key, {"min_pend_in": 10**9,
                                     "min_pend_in_out": None,
                                     "steps": 0, "deaths_y": 0, "walks": 0,
                                     "tree_exhausted": False, "milestones_ok": 0,
                                     "fail_budget": 0, "fail_exhausted": 0})
            a["min_pend_in"] = min(a["min_pend_in"], best["min_pend_in"])
            if best["min_pend_in_out"] is not None:
                a["min_pend_in_out"] = (best["min_pend_in_out"]
                                        if a["min_pend_in_out"] is None
                                        else min(a["min_pend_in_out"],
                                                 best["min_pend_in_out"]))
            a["steps"] += best["steps_done"]
            a["deaths_y"] += best["deaths_y"]
            a["walks"] += job[4]
            a["max_depth"] = max(a.get("max_depth", 0), best["max_depth"])
            a["tree_exhausted"] |= best["tree_exhausted"]
            a["milestones_ok"] += best["milestones_ok"]
            a["fail_budget"] += best["fail_budget"]
            a["fail_exhausted"] += best["fail_exhausted"]
            if best["min_pend_in"] <= a["min_pend_in"]:
                a["best_cells"] = best["best_cells"]
            if best["witness"] is not None:
                witness_found = best["witness"]
                print(f"!!! TESTIMONE DI CHIUSURA: {best['witness']}", flush=True)
                log.write(f"WITNESS {json.dumps(best['witness'])}\n")
                break

    print("\n---- caccia: minimi raggiunti (pend_in-palla) ----", flush=True)
    rows = []
    for (name, R), a in sorted(agg.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        e2len = next(len(to_bits(w)) for n, w, k in targets if n == name)
        rows.append({"nome": name, "R": R, **a})
        exh = " ALBERO-ESAURITO" if a["tree_exhausted"] else ""
        print(f"{name:12s} R={R:2d}: min pend_in={a['min_pend_in']:3d} "
              f"(min con posa FUORI palla="
              f"{a['min_pend_in_out'] if a['min_pend_in_out'] is not None else '-'}), "
              f"milestone ok {a['milestones_ok']}, fail budget/esauriti "
              f"{a['fail_budget']}/{a['fail_exhausted']}, "
              f"depth max {a['max_depth']}, {a['steps']} nodi{exh}", flush=True)
        log.write(json.dumps(rows[-1]) + "\n")

    out = {"args": vars(args), "targets": [t[0] for t in targets],
           "rows": rows, "witness": witness_found,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(out_json, "w") as f:
        json.dump(out, f, indent=1)
    log.write(f"done in {out['elapsed_s']}s witness={witness_found is not None}\n")
    log.close()
    print(f"\nscritto {out_json} in {out['elapsed_s']} s "
          f"(testimone: {'TROVATO' if witness_found else 'nessuno'})", flush=True)


if __name__ == "__main__":
    main()
