# danger_reach_c_driver.py — §107c: driver sharded del motore C danger_reach.c.
#
# Sharding per prefissi di scelte libere a profondita' L (§4): Python enumera
# i nodi validi a profondita' L (prefissi), li distribuisce round-robin su N
# job, il C esplora i sottoalberi. I conteggi DEVONO sommare: somma dei NODES
# a profondita' L dei job == conteggio Python a L (assert), e le profondita'
# 0..L-1 vengono dal Python stesso.
#
# GATE R2 (--r2): a profondita' moderata, il risultato aggregato C deve essere
# BIT-IDENTICO al reach_dfs Python puro: nodi_per_depth 0..D e first_hit di
# TUTTE le celle (frame cammino). Il port si usa solo dopo R2 verde (§5).
#
# Convenzione (caveat §107b.6): onset_germe misurato DAL RECORD, asse
# assoluto = og+101; profondita' in PASSI; d_hit = SOVRA.
import sys, os, json, time, argparse, subprocess

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from delta4_long_orbits import build_seed
from record_word_census import run_collect_records
from danger_backward_autopsy import Machine, K
from danger_reach_depth import (geo_bfs, reach_dfs, to_anchor,
                                censored_median)

HERE = os.path.dirname(os.path.abspath(__file__))
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
EXE = os.path.join(HERE, "danger_reach.exe")
JOBDIR = os.path.join(HERE, "reach_jobs")
BELOW_NORMAL = 0x4000


def collect_prefixes(m, L):
    """Enumera i prefissi validi (stringhe di scelte c) a profondita' esatta L,
    con la STESSA transizione di reach_dfs. Ritorna lista di stringhe."""
    req = dict(m.req0)
    out = []
    path = []

    def visit(p, h, d):
        if d == L:
            out.append("".join(path))
            return
        p_prev = (p[0] - DX[h], p[1] - DY[h])
        if m.anchor_y(p_prev) < 1:
            return
        seen = p_prev in req
        for c in (0, 1):
            if seen and c != 1 - req[p_prev]:
                continue
            h_prev = (h - 1) & 3 if c == 0 else (h + 1) & 3
            old = req.get(p_prev)
            req[p_prev] = c
            path.append(str(c))
            visit(p_prev, h_prev, d + 1)
            path.pop()
            if seen:
                req[p_prev] = old
            else:
                del req[p_prev]

    sys.setrecursionlimit(L + 200)
    visit((0, 0), 0, 0)
    return out


def run_sharded(m, depth, L, nprocs, tag):
    """Esegue il C sharded. Ritorna (nodi_per_depth 0..depth, first_hit walk)."""
    os.makedirs(JOBDIR, exist_ok=True)
    x0, y0, _ = m.pose_end
    head = [f"{depth} {x0} {y0} {m.k_rot}", f"{len(m.req0)}"]
    head += [f"{c[0]} {c[1]} {v}" for c, v in sorted(m.req0.items())]
    # lato Python: profondita' 0..L-1 + first_hit fino a L
    t0 = time.time()
    fh_py, stats_py, n_py, trunc_py = reach_dfs(m, L)
    assert not trunc_py
    prefixes = collect_prefixes(m, L)
    assert len(prefixes) == stats_py[L], \
        f"prefissi {len(prefixes)} != nodi Python a L {stats_py[L]}"
    print(f"[{tag}] prefissi a L={L}: {len(prefixes)} "
          f"({time.time() - t0:.1f} s)", flush=True)
    jobs = [[] for _ in range(nprocs)]
    for i, pf in enumerate(prefixes):
        jobs[i % nprocs].append(pf)
    procs = []
    for j, pfl in enumerate(jobs):
        if not pfl:
            continue
        jp = os.path.join(JOBDIR, f"{tag}_job{j}.txt")
        op = os.path.join(JOBDIR, f"{tag}_out{j}.txt")
        with open(jp, "w") as f:
            f.write("\n".join(head) + f"\n{len(pfl)}\n")
            f.write("\n".join(pfl) + "\n")
        pr = subprocess.Popen([EXE, jp, op],
                              creationflags=BELOW_NORMAL)
        procs.append((pr, op, j))
    t1 = time.time()
    npd = {d: stats_py[d] for d in range(L)}
    for d in range(L, depth + 1):
        npd[d] = 0
    fh = dict(fh_py)
    tot_c = 0
    for pr, op, j in procs:
        rc = pr.wait()
        assert rc == 0, f"job {j} rc={rc}"
        with open(op) as f:
            for line in f:
                p = line.split()
                if p[0] == "NODES":
                    npd[int(p[1])] += int(p[2])
                elif p[0] == "HIT":
                    c = (int(p[1]), int(p[2]))
                    d = int(p[3])
                    if c not in fh or d < fh[c]:
                        fh[c] = d
                elif p[0] == "DONE":
                    tot_c += int(p[1])
    print(f"[{tag}] C: {len(procs)} job, {tot_c} nodi in "
          f"{time.time() - t1:.1f} s "
          f"({(time.time() - t1) / max(1, tot_c) * 1e9 * len(procs):.0f} "
          f"ns/nodo/core)", flush=True)
    assert npd[L] == stats_py[L], \
        f"somma shard a L: {npd[L]} != Python {stats_py[L]}"
    return npd, fh, tot_c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lock", choices=["A", "B"], required=True)
    ap.add_argument("--depth", type=int, required=True)
    ap.add_argument("--shard-depth", type=int, default=24)
    ap.add_argument("--nprocs", type=int, default=14)
    ap.add_argument("--r2", action="store_true",
                    help="gate R2: confronto bit-identico col Python puro")
    args = ap.parse_args()
    t0 = time.time()
    hunt = json.load(open(HUNT))
    i = 0 if args.lock == "A" else 1
    e = hunt["F2"][i]
    rngs, t = int(e["rngstate"]), int(e["t"])
    tag = f"LOCK{args.lock}_d{args.depth}"
    seed, _, _ = build_seed(rngs, 5, 25)
    turns, _, _ = run_collect_records(seed)
    w = tuple(turns[t - K:t])
    m = Machine(w)
    rt_anchor = set(m.rt_walk.values())
    print(f"[{tag}] |R_T|={len(m.rt_walk)} og={m.onset_germe}", flush=True)

    L = min(args.shard_depth, args.depth)
    npd, fh, tot_c = run_sharded(m, args.depth, L, args.nprocs, tag)

    if args.r2:
        t1 = time.time()
        fh_py, stats_py, n_py, trunc = reach_dfs(m, args.depth)
        assert not trunc
        ok_n = all(npd[d] == stats_py[d] for d in range(args.depth + 1))
        ok_h = fh == fh_py
        print(f"[{tag}] R2 nodi_per_depth 0..{args.depth}: "
              f"{'BIT-IDENTICI' if ok_n else 'MISMATCH'}; first_hit "
              f"({len(fh)} celle vs {len(fh_py)}): "
              f"{'BIT-IDENTICI' if ok_h else 'MISMATCH'} "
              f"(python {time.time() - t1:.1f} s)", flush=True)
        assert ok_n and ok_h, "R2 FALLITO"

    # ---- tripla + gap (stessa logica del tool Python, D_exh = depth) ----
    geo = geo_bfs(m, args.depth)
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
        assert dg is not None and dg <= dh, f"RG FALLITO {ca}"
    foot_anchor = {to_anchor(m, c) for c in m.req0}
    n_unreach = 0
    print(f"[{tag}] TRIPLA (D_geo, D_exh={args.depth}, d_hit-SOVRA):",
          flush=True)
    tripla = {}
    for ca in sorted(rt_anchor):
        dh = fh_anchor.get(ca)
        if dh is None:
            n_unreach += 1
        tripla[str(ca)] = {"D_geo": geo_anchor.get(ca),
                           "D_exh": args.depth, "d_hit_sovra": dh}
        print(f"    {ca}: D_geo={geo_anchor.get(ca)} "
              f"d_hit={dh if dh is not None else f'>{args.depth} (IRRAGGIUNGIBILE-ESAUSTIVO)'}",
              flush=True)
    print(f"[{tag}] irraggiungibili-esaustive a D={args.depth}: "
          f"{n_unreach}/{len(rt_anchor)}", flush=True)
    pool_by = {}
    for ca, dg in geo_anchor.items():
        if ca in rt_anchor or ca in foot_anchor:
            continue
        side = (ca[0] > 0) - (ca[0] < 0)
        pool_by.setdefault((side, dg), []).append(ca)
    gaps_rt, gaps_mt = [], []
    for ca in sorted(rt_anchor):
        dg = geo_anchor.get(ca)
        if dg is None:
            continue
        dh = fh_anchor.get(ca)
        gaps_rt.append(None if dh is None else dh - dg)
        side = (ca[0] > 0) - (ca[0] < 0)
        for cb in pool_by.get((side, dg), []):
            dhb = fh_anchor.get(cb)
            gaps_mt.append(None if dhb is None else dhb - dg)
    med_rt, n_rt_g, cens_rt = censored_median(gaps_rt)
    med_mt, n_mt_g, cens_mt = censored_median(gaps_mt)
    print(f"[{tag}] GAP gate: R_T mediana={med_rt} (n={n_rt_g}, "
          f"cens={cens_rt}) vs MATCHED mediana={med_mt} (n={n_mt_g}, "
          f"cens={cens_mt})", flush=True)
    out = {"tag": tag, "lock": args.lock, "depth": args.depth,
           "shard_depth": L, "nprocs": args.nprocs,
           "nodi_totali_C": tot_c, "r2": bool(args.r2),
           "convenzione": "og dal record (asse assoluto og+101); "
                          "profondita' in passi; d_hit SOVRA",
           "nodi_per_depth": {str(d): npd[d] for d in sorted(npd)},
           "tripla_rt": tripla, "irraggiungibili_esaustive": n_unreach,
           "gap_rt_mediana": med_rt, "gap_rt_n": n_rt_g,
           "gap_rt_cens": cens_rt,
           "gap_matched_mediana": med_mt, "gap_matched_n": n_mt_g,
           "gap_matched_cens": cens_mt,
           "first_hit_anchor_rt": {str(ca): fh_anchor.get(ca)
                                   for ca in sorted(rt_anchor)},
           "elapsed_s": round(time.time() - t0, 1)}
    op = os.path.join(HERE, f"danger_reach_c_{tag}.json")
    with open(op, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {op} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
