# analyze_radius.py — analisi memory-lean dell'output binario di window_build.c.
# Replica la semantica di window_automaton.analyze() (stessi campi nel summary JSON), ma:
#   - src ricostruito da outdeg (repeat), niente liste Python;
#   - entropia: power iteration su scipy.sparse CSR (stessa iterazione di entropy(): nv[dst]+=v[src]);
#   - SCC: scipy.sparse.csgraph.connected_components(connection='strong') (Tarjan compilato);
#   - rotori/parole: estratti solo sulle (poche) SCC ricorrenti del sottografo senza-assumiB.
# Validazione obbligatoria: --selftest confronta r=1,2,3 con i valori certificati
# (results/radius{1,2,3}_summary.json e MORSO_ADDENDUM §39-40). MAI usare su r>=4 con self-test rossi.
#
# Uso:
#   python analyze_radius.py --selftest                  (builda r=1,2,3 in build/ e confronta)
#   python analyze_radius.py --radius 4 [--outdir build] [--maxiter 6000]

import argparse, json, os, subprocess, sys, time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from window_automaton import canon, drift_and_rot, max_power_realizable  # noqa: E402

BUILDER = os.path.join(HERE, "window_build.exe")


def run_builder(radius, outdir, cap=0):
    os.makedirs(outdir, exist_ok=True)
    args = [BUILDER, str(radius), outdir] + ([str(cap)] if cap else [])
    rc = subprocess.call(args)
    if rc != 0:
        raise RuntimeError(f"window_build fallito (rc={rc})")


def load(radius, outdir):
    deg = np.fromfile(os.path.join(outdir, f"r{radius}_outdeg.bin"), dtype=np.uint8)
    N = len(deg)
    dt = np.dtype([("dst", "<u4"), ("ty", "u1"), ("tn", "u1")])
    e = np.fromfile(os.path.join(outdir, f"r{radius}_edges.bin"), dtype=dt)
    src = np.repeat(np.arange(N, dtype=np.int32), deg)
    dst = e["dst"].astype(np.int32)
    ty = e["ty"].copy()
    tn = e["tn"].copy()
    del e
    assert len(src) == len(dst)
    return N, src, dst, ty, tn


def entropy_sp(src, dst, N, iters=6000, tol=1e-13, patience=50):
    """stessa iterazione di window_automaton.entropy: nv[dst] += v[src]; lam = somma.
    early-stop quando lam e' stabile entro tol per `patience` iterazioni consecutive."""
    if len(src) == 0:
        return float("-inf"), 0
    M = sp.coo_matrix((np.ones(len(src), np.float64), (dst, src)), shape=(N, N)).tocsr()
    v = np.full(N, 1.0 / N, np.float64)
    lam, stable, it = 1.0, 0, 0
    for it in range(1, iters + 1):
        nv = M @ v
        s = nv.sum()
        if s == 0:
            return float("-inf"), it
        v = nv / s
        stable = stable + 1 if abs(s - lam) < tol * max(1.0, abs(s)) else 0
        lam = s
        if stable >= patience:
            break
    return float(np.log2(lam)), it


def analyze(radius, outdir, do_build=True, maxiter=6000, cap=0):
    print(f"== raggio {radius} (pipeline C) ==", flush=True)
    t0 = time.time()
    if do_build:
        run_builder(radius, outdir, cap)
    N, src, dst, ty, tn = load(radius, outdir)
    n_forced, n_w, n_b = int((ty == 0).sum()), int((ty == 1).sum()), int((ty == 2).sum())
    print(f"stati: {N}, archi: {len(src)} (forzati {n_forced}, assumiW {n_w}, assumiB {n_b}) "
          f"[{time.time()-t0:.0f}s]", flush=True)

    h_full, it_full = entropy_sp(src, dst, N, iters=maxiter)
    mask = ty != 2
    srcB, dstB, tnB = src[mask], dst[mask], tn[mask]
    h_noB, it_noB = entropy_sp(srcB, dstB, N, iters=maxiter)
    print(f"entropia piena: {h_full:.4f} ({it_full} iter) | senza-assumiB: {h_noB:.6f} ({it_noB} iter)",
          flush=True)

    # SCC del sottografo senza-assumiB (Tarjan compilato di scipy)
    G = sp.coo_matrix((np.ones(len(srcB), np.int8), (srcB, dstB)), shape=(N, N)).tocsr()
    ncomp, labels = connected_components(G, directed=True, connection="strong")
    del G
    sizes = np.bincount(labels)
    rec_labels = set(np.flatnonzero(sizes > 1).tolist())
    selfloop = srcB == dstB
    rec_labels |= set(labels[srcB[selfloop]].tolist())
    rec_labels = sorted(rec_labels)
    rec_sizes = sorted(int(sizes[l]) for l in rec_labels)
    print(f"SCC ricorrenti senza-assumiB: {len(rec_labels)}, taglie: {rec_sizes[-12:]}", flush=True)

    # estrazione rotori e parole cicliche (solo sui nodi ricorrenti: pochi).
    # NB: niente scansioni per-componente di `labels` (a r=4 ci sono ~67k componenti su
    # 27M nodi): un solo argsort sui nodi ricorrenti e poi split per label.
    rec_arr = np.array(rec_labels, dtype=labels.dtype)
    rec_nodes = np.flatnonzero(np.isin(labels, rec_arr))
    lab_of = labels[rec_nodes]
    o = np.argsort(lab_of, kind="stable")
    sorted_nodes, sorted_labs = rec_nodes[o], lab_of[o]
    cuts = np.flatnonzero(np.diff(sorted_labs)) + 1
    groups = np.split(sorted_nodes, cuts)            # in ordine di label crescente
    assert len(groups) == len(rec_labels)
    sel = np.isin(srcB, rec_nodes)
    es, ed, et = srcB[sel], dstB[sel], tnB[sel]
    internal = labels[es] == labels[ed]
    es, ed, et = es[internal], ed[internal], et[internal]
    out_edges = {}
    for s, d, t in zip(es.tolist(), ed.tolist(), et.tolist()):
        out_edges.setdefault(s, []).append((d, t))
    cycles, all_rotors = [], True
    for grp in groups:
        comp = grp.tolist()
        if any(len(out_edges.get(v, [])) != 1 for v in comp):
            all_rotors = False
            print(f"  !! SCC taglia {len(comp)} NON e' un rotore (branching interno) — "
                  f"l'argomento 'eventualmente periodico' va rifatto per questa componente", flush=True)
            continue
        v, word = comp[0], []
        for _ in range(len(comp)):
            d, t = out_edges[v][0]
            word.append("R" if t else "L")
            v = d
        assert v == comp[0], "il cammino del rotore non si chiude"
        cycles.append(canon("".join(word)))
    uniq = sorted(set(cycles), key=len)
    print(f"rotori: {all_rotors} | parole cicliche distinte: {len(uniq)}", flush=True)

    verdicts, need_check = {}, []
    for w in uniq:
        rot, dr = drift_and_rot(w)
        if rot % 4 != 0:
            verdicts[w] = f"B-T (rot={rot} non mult. 4 => limitato)"
        elif dr == (0, 0):
            verdicts[w] = "B-T (drift nullo => limitato)"
        else:
            verdicts[w] = "DA VERIFICARE con gamma_enum check"
            need_check.append(w)
        print(f"  p={len(w):3d} rot={rot:+3d} drift={dr}  {w if len(w)<=60 else w[:57]+'...'}  -> {verdicts[w]}")
    for i, w in enumerate(need_check):
        fn = os.path.join(ROOT, f"radius{radius}_word{i}.txt")
        open(fn, "w").write(w)
        print(f"  scritto {fn}: eseguire gamma_enum check su questo file")

    out = {"radius": radius, "states": int(N), "edges": int(len(src)),
           "edge_types": {"forced": n_forced, "assumeW": n_w, "assumeB": n_b},
           "entropy_full": h_full, "entropy_noassumeB": h_noB,
           "entropy_iters": {"full": it_full, "noB": it_noB},
           "recurrent_sccs_noB": len(rec_labels), "recurrent_sizes": rec_sizes,
           "all_rotors": all_rotors, "cycle_words": uniq, "verdicts": verdicts,
           "rotor_max_powers": {w: max_power_realizable(w) for w in uniq},
           "builder": "C (window_build.c)", "seconds": time.time() - t0}
    json.dump(out, open(os.path.join(ROOT, f"radius{radius}_summary.json"), "w"), indent=1)
    open(os.path.join(ROOT, f"radius{radius}_cycles.txt"), "w").write("\n".join(uniq))
    print(f"salvati radius{radius}_summary.json, radius{radius}_cycles.txt  [{time.time()-t0:.0f}s]\n",
          flush=True)
    return out


def selftest(outdir, maxiter):
    """la pipeline C+scipy deve riprodurre ESATTAMENTE i certificati r=1,2,3."""
    print("SELF-TEST pipeline C (confronto con results/radius{1,2,3}_summary.json)", flush=True)
    certified = {
        1: {"states": 15, "edges": 26, "forced": 4, "assume": 11, "h": 0.8114,
            "sccs": 1, "sizes": [5], "words": [canon("RRRRL")]},
        2: {"states": 403, "edges": 554, "forced": 252, "assume": 151, "h": 0.7594,
            "sccs": 8, "sizes": [6, 12, 12, 12, 12, 12, 12, 15],
            "words": sorted([canon("RRRLLR"), canon("RRRLLRRRRLLR"), canon("RRRRLRRRRLLLLRL")], key=len)},
        3: {"states": 45971, "edges": 59508, "forced": 32434, "assume": 13537, "h": 0.7441,
            "sccs": 1, "sizes": [15], "words": [canon("RRRRLRRRRLLLLRL")]},
    }
    for r, c in certified.items():
        out = analyze(r, outdir, maxiter=maxiter)
        assert out["states"] == c["states"], (r, out["states"])
        assert out["edges"] == c["edges"], (r, out["edges"])
        assert out["edge_types"]["forced"] == c["forced"], (r, out["edge_types"])
        assert out["edge_types"]["assumeW"] == c["assume"] == out["edge_types"]["assumeB"], (r, out["edge_types"])
        assert abs(out["entropy_full"] - c["h"]) < 2e-3, (r, out["entropy_full"])
        assert abs(out["entropy_noassumeB"]) < 1e-9, (r, out["entropy_noassumeB"])
        assert out["recurrent_sccs_noB"] == c["sccs"], (r, out["recurrent_sccs_noB"])
        assert out["recurrent_sizes"] == c["sizes"], (r, out["recurrent_sizes"])
        assert out["cycle_words"] == c["words"], (r, out["cycle_words"])
        assert out["all_rotors"], r
    print("SELF-TEST PIPELINE C: TUTTO OK — procedere con --radius 4", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, default=None)
    ap.add_argument("--outdir", default=os.path.join(ROOT, "build"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-build", action="store_true", help="riusa i binari gia' presenti in outdir")
    ap.add_argument("--maxiter", type=int, default=6000)
    ap.add_argument("--cap", type=int, default=0, help="abort esplicito oltre questo numero di stati")
    a = ap.parse_args()
    if a.selftest:
        selftest(a.outdir, a.maxiter)
    elif a.radius:
        analyze(a.radius, a.outdir, do_build=not a.no_build, maxiter=a.maxiter, cap=a.cap)
    else:
        ap.print_help()
