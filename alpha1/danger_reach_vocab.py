# danger_reach_vocab.py — §107d: reach per-cella sulle parole lock-capable.
#
# OGGETTO (roadmap §C.2 dopo §107c): le triple (D_geo, D_exh, d_hit-SOVRA) e
# il gap R_T-vs-matched sulla sottopopolazione sigma<=0.01 del vocabolario
# (59 parole canoniche, P2 §107c): il gap dei lock e' proprieta' dei lock o
# di tutta la sottoclasse lock-capable?
#
# DISCIPLINA:
#   - macchinario GIA' validato §107c (R0/R0b/R1/RG/R2/lente): qui si riusa
#     run_sharded/collect_prefixes/geo_bfs senza modifiche.
#   - profondita' PER-PAROLA scelta dal budget: nodes(28) misurato in Python,
#     estrapolazione col branching misurato (ratio empirico per-parola dagli
#     ultimi livelli), D = min(48, max(36, 28+k)) con proiezione <= NODE_BUDGET.
#     Ogni D dichiarato nel record (mai confronti sotto cap non dichiarati, mm).
#   - d_hit = SOVRA; l'irraggiungibilita' a D_exh trasferisce (deduttiva).
#   - output JSONL append (riprendibile), log timestampato (§4).
import sys, os, json, time, argparse, math

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danger_backward_autopsy import Machine
from danger_reach_depth import geo_bfs, reach_dfs, to_anchor, censored_median
from danger_reach_c_driver import run_sharded

HERE = os.path.dirname(os.path.abspath(__file__))
PERWORD = os.path.join(HERE, "sigma_vocab_perword.jsonl")
OUT = os.path.join(HERE, "reach_vocab_sigma0.jsonl")
LOG = os.path.join(HERE, "reach_vocab_sigma0.log")
NODE_BUDGET = 50_000_000_000


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sigma-max", type=float, default=0.01)
    ap.add_argument("--depth-max", type=int, default=48)
    ap.add_argument("--nprocs", type=int, default=14)
    args = ap.parse_args()
    words = []
    with open(PERWORD, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if not r.get("non_definito") and r.get("sigma", 1) <= args.sigma_max:
                words.append(r)
    words.sort(key=lambda r: (r["n_rt"], r["word"]))
    done = set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                done.add(json.loads(line)["word"])
    log(f"parole sigma<={args.sigma_max}: {len(words)}, gia' fatte {len(done)}")
    for k, r in enumerate(words):
        ws = r["word"]
        if ws in done:
            continue
        w = tuple(1 if ch == "R" else 0 for ch in ws)
        m = Machine(w)
        rt_anchor = set(m.rt_walk.values())
        foot_anchor = {to_anchor(m, c) for c in m.req0}
        # misura del costo: Python a D=28
        t0 = time.time()
        fh28, stats28, n28, tr28 = reach_dfs(m, 28, budget_s=600)
        if tr28:
            rec = {"word": ws, "n_rt": r["n_rt"], "sigma22": r["sigma"],
                   "non_definito": True,
                   "nota": "Python D=28 troncato: parola fuori budget"}
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            log(f"{k + 1}/{len(words)} {ws[:16]}... TRONCATA a 28 — saltata")
            continue
        ratio = max(1.3, (stats28[28] / max(1, stats28[24])) ** 0.25)
        tot28 = sum(stats28)
        extra = int(math.log(NODE_BUDGET / max(1, tot28)) / math.log(ratio))
        depth = max(36, min(args.depth_max, 28 + extra))
        tag = f"VOC{k:03d}_d{depth}"
        npd, fh, tot_c = run_sharded(m, depth, min(24, depth - 4),
                                     args.nprocs, tag)
        geo = geo_bfs(m, depth)
        geo_anchor = {}
        for p, d in geo.items():
            ca = to_anchor(m, p)
            if ca not in geo_anchor or d < geo_anchor[ca]:
                geo_anchor[ca] = d
        fh_anchor = {}
        for p, d in fh.items():
            ca = to_anchor(m, p)
            if ca not in fh_anchor or d < fh_anchor[ca]:
                fh_anchor[ca] = d
        for ca, dh in fh_anchor.items():
            dg = geo_anchor.get(ca)
            assert dg is not None and dg <= dh, f"RG FALLITO {ws[:16]} {ca}"
        pool_by = {}
        for ca, dg in geo_anchor.items():
            if ca in rt_anchor or ca in foot_anchor:
                continue
            side = (ca[0] > 0) - (ca[0] < 0)
            pool_by.setdefault((side, dg), []).append(ca)
        gaps_rt, gaps_mt = [], []
        tripla = {}
        n_unreach = 0
        for ca in sorted(rt_anchor):
            dg = geo_anchor.get(ca)
            dh = fh_anchor.get(ca)
            if dh is None:
                n_unreach += 1
            tripla[str(ca)] = [dg, depth, dh]
            if dg is None:
                continue
            gaps_rt.append(None if dh is None else dh - dg)
            side = (ca[0] > 0) - (ca[0] < 0)
            for cb in pool_by.get((side, dg), []):
                dhb = fh_anchor.get(cb)
                gaps_mt.append(None if dhb is None else dhb - dg)
        med_rt, n_rt_g, cens_rt = censored_median(gaps_rt)
        med_mt, n_mt_g, cens_mt = censored_median(gaps_mt)
        rec = {"word": ws, "n_rt": r["n_rt"], "sigma22": r["sigma"],
               "onset_germe": r["onset_germe"], "depth": depth,
               "nodi_C": tot_c, "tripla": tripla,
               "irraggiungibili_esaustive": n_unreach,
               "gap_rt_mediana": med_rt, "gap_rt_n": n_rt_g,
               "gap_rt_cens": cens_rt,
               "gap_matched_mediana": med_mt, "gap_matched_n": n_mt_g,
               "gap_matched_cens": cens_mt}
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        log(f"{k + 1}/{len(words)} {ws[:16]}... n_rt={r['n_rt']} "
            f"sigma={r['sigma']} D={depth} nodi_C={tot_c} irr={n_unreach} "
            f"gapRT={med_rt} gapM={med_mt} ({time.time() - t0:.0f} s)")
    log("FINITO")


if __name__ == "__main__":
    main()
