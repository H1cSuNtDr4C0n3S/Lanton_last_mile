# gen_reduced.py — riduzione del grafo per min_assumeB: rimuove gli archi-rotore e poi
# restringe alle SCC non banali del grafo rimanente (i cicli, e quindi il min cycle mean,
# vivono tutti li'). Scrive un'istanza compatta r<R>c_* per min_assumeB.c con id rinumerati.
# Il min tasso assumiB del grafo ridotto e' IDENTICO a quello del grafo pieno senza rotori
# (riduzione conservativa: si eliminano solo nodi/archi che non stanno su alcun ciclo).
# Validazione: su r=2,3 deve riprodurre delta2=1/7, delta3=1/64.
# Uso: python gen_reduced.py --radius R [--outdir build]

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
src = np.repeat(np.arange(N, dtype=np.int64), deg)
dst = e["dst"].astype(np.int64)
ty, tn = e["ty"].copy(), e["tn"].copy()
del e, deg
E = len(src)

# 1) rimozione archi-rotore (stessa semantica del --karp: ogni arco con coppia (s,d) rotore)
rot = np.loadtxt(os.path.join(outdir, f"r{R}_rotor_edges.txt"), dtype=np.int64).reshape(-1, 2)
keymul = np.int64(1) << np.int64(32)
ekey = src * keymul + dst
rkey = rot[:, 0] * keymul + rot[:, 1]
keep = ~np.isin(ekey, rkey)
del ekey, rkey
src, dst, ty, tn = src[keep], dst[keep], ty[keep], tn[keep]
print(f"r={R}: archi {E} -> senza rotori {len(src)}")

# 2) SCC del grafo rimanente; tengo solo nodi in SCC non banale (taglia>1 o cappio)
G = sp.coo_matrix((np.ones(len(src), np.int8), (src, dst)), shape=(N, N)).tocsr()
ncomp, labels = connected_components(G, directed=True, connection="strong")
del G
sizes = np.bincount(labels)
good = sizes > 1
selfloop_labels = np.unique(labels[src[src == dst]])
good[selfloop_labels] = True
node_keep = good[labels]
intra = node_keep[src] & (labels[src] == labels[dst])
src, dst, ty, tn = src[intra], dst[intra], ty[intra], tn[intra]
nodes = np.flatnonzero(node_keep)
newid = np.full(N, -1, np.int64)
newid[nodes] = np.arange(len(nodes))
src, dst = newid[src], newid[dst]
Nc = len(nodes)
print(f"r={R}: nodi {N} -> parte ciclica {Nc} ({100*Nc/N:.2f}%), archi -> {len(src)}")

# 3) scrittura istanza compatta (outdeg via bincount; archi ordinati per src)
o = np.argsort(src, kind="stable")
src, dst, ty, tn = src[o], dst[o], ty[o], tn[o]
outdeg = np.bincount(src, minlength=Nc)
assert outdeg.max() <= 255
outdeg.astype(np.uint8).tofile(os.path.join(outdir, f"r{R}c_outdeg.bin"))
rec = np.zeros(len(src), dtype=dt)
rec["dst"] = dst.astype(np.uint32)
rec["ty"] = ty
rec["tn"] = tn
rec.tofile(os.path.join(outdir, f"r{R}c_edges.bin"))
open(os.path.join(outdir, f"r{R}c_rotor_edges.txt"), "w").close()  # gia' rimossi
nodes.astype(np.uint32).tofile(os.path.join(outdir, f"r{R}c_nodes.bin"))  # id originale per id ridotto
print(f"scritti r{R}c_outdeg.bin, r{R}c_edges.bin, r{R}c_rotor_edges.txt (vuoto), r{R}c_nodes.bin")
