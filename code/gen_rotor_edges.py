# gen_rotor_edges.py — estrae gli archi-rotore (archi interni delle SCC ricorrenti del
# sottografo senza-assumiB) dai binari di window_build.c e li scrive come coppie "src dst",
# input per min_assumeB.c. Replica la definizione di rotor_edges in window_automaton.analyze
# (--karp): TUTTI gli archi (s,d) con s,d nella stessa SCC ricorrente noB.
# Uso: python gen_rotor_edges.py --radius R [--outdir build]

import argparse, os, sys
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("--radius", type=int, required=True)
ap.add_argument("--outdir", default=os.path.join(ROOT, "build"))
a = ap.parse_args()
R, outdir = a.radius, a.outdir

deg = np.fromfile(os.path.join(outdir, f"r{R}_outdeg.bin"), dtype=np.uint8)
N = len(deg)
dt = np.dtype([("dst", "<u4"), ("ty", "u1"), ("tn", "u1")])
e = np.fromfile(os.path.join(outdir, f"r{R}_edges.bin"), dtype=dt)
src = np.repeat(np.arange(N, dtype=np.int32), deg)
dst = e["dst"].astype(np.int32)
ty = e["ty"].copy()
del e

mask = ty != 2
srcB, dstB = src[mask], dst[mask]
G = sp.coo_matrix((np.ones(len(srcB), np.int8), (srcB, dstB)), shape=(N, N)).tocsr()
ncomp, labels = connected_components(G, directed=True, connection="strong")
del G
sizes = np.bincount(labels)
rec = set(np.flatnonzero(sizes > 1).tolist())
rec |= set(labels[srcB[srcB == dstB]].tolist())
rec_arr = np.array(sorted(rec), dtype=labels.dtype)

# archi noB con entrambi gli estremi nella stessa SCC ricorrente
in_rec_s = np.isin(labels[srcB], rec_arr)
cand = np.flatnonzero(in_rec_s)
same = labels[srcB[cand]] == labels[dstB[cand]]
cand = cand[same]
pairs = sorted(set(zip(srcB[cand].tolist(), dstB[cand].tolist())))

fn = os.path.join(outdir, f"r{R}_rotor_edges.txt")
with open(fn, "w") as f:
    for s, d in pairs:
        f.write(f"{s} {d}\n")
print(f"r={R}: SCC ricorrenti noB: {len(rec)} (taglie {sorted(int(sizes[l]) for l in rec)}), "
      f"archi-rotore: {len(pairs)} -> {fn}")
