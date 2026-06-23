# morso_automaton.py — Step 1b: automa a finestra di raggio 1 (sovra-approssimazione sana)
# Stato = finestra 3x3 attorno alla formica, frame canonico heading=su.
# Valori cella: 0=ignota (mai vista nella memoria di finestra), 1=bianca, 2=nera.
# Transizione: lettura del centro -> svolta -> flip -> mossa -> ri-canonicalizzazione.
# Celle che escono dalla finestra vengono DIMENTICATE (leak: rientrano come ignote).
# Il linguaggio dell'automa CONTIENE il linguaggio realizzabile (sovra-approssimazione).
import numpy as np, pickle
from collections import deque, defaultdict

CELLS = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
IDX = {c: i for i, c in enumerate(CELLS)}
U, W, B = 0, 1, 2

def transform_R(xp, yp):   # nuove coord -> vecchie (svolta R)
    return (yp + 1, -xp)
def transform_L(xp, yp):
    return (-yp - 1, xp)

def step(state, color):
    """color in {W,B} = colore letto al centro. Ritorna (turn, newstate)."""
    s = list(state)
    s[IDX[(0, 0)]] = B if color == W else W      # flip del centro
    inv = transform_R if color == W else transform_L
    new = []
    for (xp, yp) in CELLS:
        ox, oy = inv(xp, yp)
        if -1 <= ox <= 1 and -1 <= oy <= 1:
            new.append(s[IDX[(ox, oy)]])
        else:
            new.append(U)                         # leak: cella nuova/dimenticata
    turn = 1 if color == W else 0
    return turn, tuple(new)

# ---- BFS ----
start = tuple([U]*9)
states = {start: 0}
edges = []          # (src, dst, turn, tipo)  tipo: 0=forzata, 1=assumiW, 2=assumiB
order = [start]
q = deque([start])
while q:
    st = q.popleft()
    si = states[st]
    c0 = st[IDX[(0, 0)]]
    if c0 == U:
        for col, tipo in ((W, 1), (B, 2)):
            t, ns = step(st, col)
            if ns not in states:
                states[ns] = len(order); order.append(ns); q.append(ns)
            edges.append((si, states[ns], t, tipo))
    else:
        t, ns = step(st, c0)
        if ns not in states:
            states[ns] = len(order); order.append(ns); q.append(ns)
        edges.append((si, states[ns], t, 0))

N = len(order)
print(f"stati raggiungibili: {N} (su 3^9 = 19683)")
tipo_count = defaultdict(int)
for e in edges: tipo_count[e[3]] += 1
print(f"archi: {len(edges)} | forzati {tipo_count[0]}, assumiW {tipo_count[1]}, assumiB {tipo_count[2]}")

# ---- conteggio cammini vs R(n): dove inizia il leak ----
Rn = {2:4,4:16,5:28,6:50,7:88,8:154,10:448,12:1300,14:3680,16:10412,18:29128,20:81498,22:226538,24:630112}
adj = defaultdict(list)
for s, d, t, ty in edges: adj[s].append(d)
v = np.zeros(N, dtype=object); v[0] = 1
counts = {}
for n in range(1, 25):
    nv = np.zeros(N, dtype=object)
    for s in range(N):
        if v[s]:
            for d in adj[s]: nv[d] += v[s]
    v = nv
    counts[n] = int(v.sum())
print("\nn : cammini_automa vs R(n)  [leak = eccesso]")
for n in sorted(Rn):
    c = counts[n]
    print(f"{n:3d}: {c:>9d} vs {Rn[n]:>7d}   eccesso {c-Rn[n]:>7d}  ({(c/Rn[n]-1)*100:.2f}%)")

# ---- entropia (raggio spettrale) ----
M = np.zeros((N, N))
for s, d, t, ty in edges: M[s, d] += 1
x = np.ones(N)/N
for _ in range(3000):
    y = M.T @ x; lam = y.sum(); x = y/lam
print(f"\nentropia automa: log2(lambda) = {np.log2(lam):.4f}  (realizzabile esatto: 0.734)")

# entropia del sottografo senza assumiB (consumo solo-vergine + memoria locale)
M2 = np.zeros((N, N))
for s, d, t, ty in edges:
    if ty != 2: M2[s, d] += 1
x = np.ones(N)/N
for _ in range(3000):
    y = M2.T @ x; l2 = y.sum()
    if l2 == 0: break
    x = y/l2
print(f"entropia sottografo senza assumiB: {np.log2(l2):.4f}")

# ---- SCC (Tarjan iterativo) ----
adj2 = defaultdict(list)
for s, d, t, ty in edges: adj2[s].append((d, ty))
index = [None]*N; low = [0]*N; onstk = [False]*N; stk = []; sccs = []; cnt = [0]
for root in range(N):
    if index[root] is not None: continue
    work = [(root, 0)]
    while work:
        v0, pi = work[-1]
        if pi == 0:
            index[v0] = low[v0] = cnt[0]; cnt[0] += 1
            stk.append(v0); onstk[v0] = True
        recurse = False
        nbrs = adj2[v0]
        for i in range(pi, len(nbrs)):
            wv = nbrs[i][0]
            if index[wv] is None:
                work[-1] = (v0, i+1); work.append((wv, 0)); recurse = True; break
            elif onstk[wv]:
                low[v0] = min(low[v0], index[wv])
        if recurse: continue
        if low[v0] == index[v0]:
            comp = []
            while True:
                wv = stk.pop(); onstk[wv] = False; comp.append(wv)
                if wv == v0: break
            sccs.append(comp)
        work.pop()
        if work:
            pv = work[-1][0]; low[pv] = min(low[pv], low[v0])

big = [c for c in sccs if len(c) > 1]
print(f"\nSCC: {len(sccs)} totali, non banali: {len(big)}, taglie: {sorted(len(c) for c in big)[-10:]}")
# per la SCC gigante: tipi di archi interni, cicli solo-forzati?
scc_id = [0]*N
for i, c in enumerate(sccs):
    for v0 in c: scc_id[v0] = i
for c in sorted(big, key=len, reverse=True)[:3]:
    cid = scc_id[c[0]]; inside = defaultdict(int); cs = set(c)
    forced_adj = defaultdict(list)
    for s, d, t, ty in edges:
        if s in cs and d in cs:
            inside[ty] += 1
            if ty == 0: forced_adj[s].append(d)
    # cicli solo-forzati dentro la SCC?
    # Tarjan sul sottografo forzato ristretto
    idx2 = {}; low2 = {}; on2 = set(); st2 = []; ncyc = 0; cnt2 = [0]
    selfloop = any(s == d for s, d, t, ty in edges if ty == 0 and s in cs and d in cs)
    def has_forced_cycle():
        for r in cs:
            if r in idx2: continue
            work = [(r, 0)]
            while work:
                v0, pi = work[-1]
                if pi == 0:
                    idx2[v0] = low2[v0] = cnt2[0]; cnt2[0] += 1; st2.append(v0); on2.add(v0)
                rec = False
                nb = forced_adj.get(v0, [])
                for i in range(pi, len(nb)):
                    wv = nb[i]
                    if wv not in idx2:
                        work[-1] = (v0, i+1); work.append((wv, 0)); rec = True; break
                    elif wv in on2:
                        low2[v0] = min(low2[v0], idx2[wv])
                if rec: continue
                if low2[v0] == idx2[v0]:
                    comp = []
                    while True:
                        wv = st2.pop(); on2.discard(wv); comp.append(wv)
                        if wv == v0: break
                    if len(comp) > 1: return True
                work.pop()
                if work:
                    pv = work[-1][0]; low2[pv] = min(low2[pv], low2[v0])
        return False
    fc = selfloop or has_forced_cycle()
    print(f"SCC taglia {len(c)}: archi interni forzati {inside[0]}, assumiW {inside[1]}, assumiB {inside[2]} | ciclo solo-forzato: {fc}")

pickle.dump({'N': N, 'edges_by_type': dict(tipo_count), 'counts': counts, 'Rn': Rn,
             'entropy': float(np.log2(lam)), 'entropy_noB': float(np.log2(l2)),
             'scc_sizes': sorted(len(c) for c in sccs if len(c) > 1)},
            open('morso_automaton.pkl', 'wb'))
print("\nsalvato morso_automaton.pkl")
