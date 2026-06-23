# window_automaton.py — Automa a finestra di raggio r (Teorema della Finestra, MORSO_ADDENDUM §39-40)
# Run completa per raggio 3-5 sul PC (Ryzen 7 5800X). Sandbox-validated a r=1,2.
#
# Uso:
#   python window_automaton.py --selftest            # OBBLIGATORIO prima di tutto
#   python window_automaton.py --radius 3
#   python window_automaton.py --radius 4
#   python window_automaton.py --radius 4 --karp     # quantificazione (min tasso assumiB) — costoso O(V*E)
#
# Output: radiusN_summary.json + radiusN_cycles.txt + (se serve full-check) wordN_*.txt per gamma_enum
#
# Semantica (vedi MORSO_ADDENDUM §39):
#   Stato = finestra (2r+1)x(2r+1) attorno alla formica, frame canonico heading=su.
#   Celle: 0=ignota, 1=bianca, 2=nera. Lettura centro -> svolta -> flip -> mossa -> ricanonicalizzazione.
#   Celle che escono dalla finestra vengono dimenticate (leak). Sovra-approssimazione sana:
#   SOLO enunciati "ogni cammino infinito fa X" si trasferiscono alle orbite.
#   Archi: tipo 0 = forzato (centro noto), 1 = assumiW (ignota letta bianca), 2 = assumiB (ignota letta nera).
#
# Teorema atteso (da estendere): il sottografo senza-assumiB ha entropia 0 e la sua parte
# ricorrente e' un'unione di ROTORI (ogni nodo: esattamente 1 arco uscente interno).
# I cicli si classificano: rot % 4 != 0 oppure drift == 0  =>  cammino limitato => B-T;
# i superstiti vanno a gamma_enum check (ammissibilita' eterna).

import argparse, json, sys, time
from collections import deque, defaultdict
import numpy as np

U, W, B = 0, 1, 2

def build(radius, progress_every=200000):
    R = radius
    CELLS = [(x, y) for x in range(-R, R+1) for y in range(-R, R+1)]
    IDX = {c: i for i, c in enumerate(CELLS)}
    NC = len(CELLS)
    C0 = IDX[(0, 0)]
    # precompute mappe di trasformazione: per ogni cella nuova i -> indice cella vecchia o -1
    mapR = np.full(NC, -1, dtype=np.int32)
    mapL = np.full(NC, -1, dtype=np.int32)
    for i, (xp, yp) in enumerate(CELLS):
        ox, oy = yp + 1, -xp          # svolta R: nuove coord -> vecchie
        if -R <= ox <= R and -R <= oy <= R: mapR[i] = IDX[(ox, oy)]
        ox, oy = -yp - 1, xp          # svolta L
        if -R <= ox <= R and -R <= oy <= R: mapL[i] = IDX[(ox, oy)]

    def step(sb, color):
        s = bytearray(sb)
        s[C0] = B if color == W else W           # flip del centro (dopo la lettura)
        m = mapR if color == W else mapL
        new = bytearray(NC)
        for i in range(NC):
            j = m[i]
            new[i] = s[j] if j >= 0 else U
        return bytes(new)

    start = bytes(NC)
    states = {start: 0}
    order = [start]
    src_l, dst_l, ty_l, tn_l = [], [], [], []
    q = deque([0])
    t0 = time.time()
    while q:
        si = q.popleft()
        st = order[si]
        c0 = st[C0]
        opts = ((W, 1), (B, 2)) if c0 == U else ((c0, 0),)
        for col, tipo in opts:
            ns = step(st, col)
            d = states.get(ns)
            if d is None:
                d = len(order); states[ns] = d; order.append(ns); q.append(d)
            src_l.append(si); dst_l.append(d); ty_l.append(tipo); tn_l.append(1 if col == W else 0)
        if len(order) % progress_every < 2 and len(order) > progress_every:
            print(f"  ... {len(order)} stati, {time.time()-t0:.0f}s", flush=True)
    src = np.array(src_l, np.int64); dst = np.array(dst_l, np.int64)
    ty = np.array(ty_l, np.int8); tn = np.array(tn_l, np.int8)
    return order, src, dst, ty, tn

def entropy(src, dst, N, iters=6000):
    v = np.ones(N) / N
    lam = 1.0
    for _ in range(iters):
        nv = np.zeros(N)
        np.add.at(nv, dst, v[src])
        s = nv.sum()
        if s == 0: return float('-inf')
        v = nv / s; lam = s
    return float(np.log2(lam))

def tarjan_sccs(N, adj):
    """SCC iterativo. adj: lista di liste di nodi. Ritorna lista di componenti."""
    index = np.full(N, -1, np.int64); low = np.zeros(N, np.int64)
    onstk = np.zeros(N, bool); stk = []; sccs = []; cnt = 0
    for root in range(N):
        if index[root] != -1: continue
        work = [(root, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index[v] = low[v] = cnt; cnt += 1
                stk.append(v); onstk[v] = True
            advanced = False
            nb = adj[v]
            for i in range(pi, len(nb)):
                w = nb[i]
                if index[w] == -1:
                    work[-1] = (v, i + 1); work.append((w, 0)); advanced = True; break
                elif onstk[w]:
                    low[v] = min(low[v], index[w])
            if advanced: continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stk.pop(); onstk[w] = False; comp.append(w)
                    if w == v: break
                sccs.append(comp)
            work.pop()
            if work:
                pv = work[-1][0]; low[pv] = min(low[pv], low[v])
    return sccs


def realizable(word):
    """la parola (lineare) e' realizzabile da QUALCHE configurazione finita?
    fresche: scelta libera; rivisite: svolta forzata dall'alternanza."""
    DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
    lastt = {}; x = y = h = 0
    for c in word:
        t = 1 if c == 'R' else 0
        lt = lastt.get((x, y))
        if lt is not None and t != 1 - lt:
            return False
        lastt[(x, y)] = t
        h = (h + 1) & 3 if t else (h - 1) & 3
        x += DX[h]; y += DY[h]
    return True

def max_power_realizable(word, cap=50):
    for k in range(1, cap + 1):
        if not realizable(word * k):
            return k - 1
    return cap

def canon(word):
    """rotazione lessicograficamente minima (parola ciclica canonica)"""
    return min(word[i:] + word[:i] for i in range(len(word)))

def drift_and_rot(word):
    rot = sum(1 if c == 'R' else -1 for c in word)
    h = 0; x = y = 0
    DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
    for c in word:
        h = (h + 1) & 3 if c == 'R' else (h - 1) & 3
        x += DX[h]; y += DY[h]
    return rot, (x, y)

def analyze(radius, do_karp=False):
    print(f"== raggio {radius} ==")
    t0 = time.time()
    order, src_, dst_, ty, tn = build(radius)
    N = len(order)
    print(f"stati: {N}, archi: {len(src_)} (forzati {(ty==0).sum()}, assumiW {(ty==1).sum()}, assumiB {(ty==2).sum()}) [{time.time()-t0:.0f}s]")

    h_full = entropy(src_, dst_, N)
    mask = ty != 2
    h_noB = entropy(src_[mask], dst_[mask], N)
    print(f"entropia piena: {h_full:.4f} | senza-assumiB: {h_noB:.6f}  (esatto realizzabile: 0.734)")

    # sottografo senza-assumiB: SCC ricorrenti, verifica rotori, parole dei cicli
    adjAB = defaultdict(list); lblAB = {}
    for s, d, t in zip(src_[mask], dst_[mask], tn[mask]):
        adjAB[int(s)].append(int(d)); lblAB[(int(s), int(d))] = 'R' if t else 'L'
    adj_list = [adjAB.get(i, []) for i in range(N)]
    sccs = tarjan_sccs(N, adj_list)
    rec = [c for c in sccs if len(c) > 1 or any(d == c[0] for d in adj_list[c[0]])]
    print(f"SCC ricorrenti senza-assumiB: {len(rec)}, taglie: {sorted(len(c) for c in rec)[-12:]}")

    cycles = []
    all_rotors = True
    for comp in rec:
        cs = set(comp)
        internal = {v: [d for d in adj_list[v] if d in cs] for v in comp}
        if any(len(o) != 1 for o in internal.values()):
            all_rotors = False
            print(f"  !! SCC taglia {len(comp)} NON e' un rotore (branching interno) — "
                  f"l'argomento 'eventualmente periodico' va rifatto per questa componente")
            continue
        v = comp[0]; word = []
        for _ in range(len(comp)):
            d = internal[v][0]; word.append(lblAB[(v, d)]); v = d
        cycles.append(canon(''.join(word)))
    uniq = sorted(set(cycles), key=len)
    print(f"rotori: {all_rotors} | parole cicliche distinte: {len(uniq)}")

    verdicts = {}
    need_check = []
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
        fn = f"radius{radius}_word{i}.txt"
        open(fn, 'w').write(w)
        print(f"  scritto {fn}: eseguire ./gamma_enum check {fn}")

    out = {'radius': radius, 'states': N, 'edges': int(len(src_)),
           'edge_types': {'forced': int((ty==0).sum()), 'assumeW': int((ty==1).sum()), 'assumeB': int((ty==2).sum())},
           'entropy_full': h_full, 'entropy_noassumeB': h_noB,
           'recurrent_sccs_noB': len(rec), 'all_rotors': all_rotors,
           'cycle_words': uniq, 'verdicts': verdicts, 'seconds': time.time()-t0}

    if do_karp:
        # Quantificazione del teorema. I rotori senza-assumiB rendono banale (=0) il min
        # cycle mean sul grafo pieno, quindi: (a) misuriamo quanto a lungo i rotori sono
        # cavalcabili REALIZZABILMENTE (potenze massime); (b) min cycle mean dopo la
        # rimozione degli archi dei cicli-rotore. Caveat (sovra-approssimazione): il
        # risultato e' una proprieta' del grafo ridotto; il passaggio a liminf di orbita
        # usa (a) per limitare le cavalcate dei rotori.
        rotor_edges = set()
        for comp in rec:
            cs = set(comp)
            for v in comp:
                for d in adj_list[v]:
                    if d in cs: rotor_edges.add((v, d))
        for w in uniq:
            print(f"  rotore {w}: potenza massima realizzabile = {max_power_realizable(w)}")
        keep = np.array([ (int(s), int(d)) not in rotor_edges for s, d in zip(src_, dst_) ])
        srcK, dstK, wgtK = src_[keep], dst_[keep], (ty[keep] == 2).astype(np.float64)
        print(f"  min cycle mean assumiB SENZA archi-rotore ({keep.sum()} archi)...", flush=True)
        def has_negcycle(mu):
            wp = wgtK - mu
            dist = np.zeros(N)
            for it in range(N):
                nd = dist.copy()
                np.minimum.at(nd, dstK, dist[srcK] + wp)
                if np.array_equal(nd, dist): return False
                dist = nd
            return True
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2
            if has_negcycle(mid): hi = mid
            else: lo = mid
        print(f"  min tasso assumiB per passo (grafo senza rotori): {hi:.6f}")
        out['min_assumeB_rate_norotor'] = float(hi)
        out['rotor_max_powers'] = {w: max_power_realizable(w) for w in uniq}

    json.dump(out, open(f"radius{radius}_summary.json", 'w'), indent=1)
    open(f"radius{radius}_cycles.txt", 'w').write('\n'.join(uniq))
    print(f"salvati radius{radius}_summary.json, radius{radius}_cycles.txt\n")
    return out

def selftest():
    print("SELF-TEST (valori certificati in sandbox, MORSO_ADDENDUM §39-40)")
    r1 = analyze(1)
    assert r1['states'] == 15, r1['states']
    assert abs(r1['entropy_full'] - 0.8114) < 2e-3, r1['entropy_full']
    assert r1['cycle_words'] == [canon('RRRRL')], r1['cycle_words']
    assert r1['all_rotors']
    r2 = analyze(2)
    assert r2['states'] == 403, r2['states']
    assert abs(r2['entropy_full'] - 0.7594) < 2e-3, r2['entropy_full']
    assert sorted(r2['cycle_words'], key=len) == sorted([canon('RRRLLR'), canon('RRRLLRRRRLLR'), canon('RRRRLRRRRLLLLRL')], key=len), r2['cycle_words']
    assert r2['all_rotors']
    rot, dr = drift_and_rot('RRRLLRRRRLLR')
    assert rot % 4 == 0 and dr == (0, 0)   # il ciclo p=12 muore per drift nullo
    print("SELF-TEST: TUTTO OK — procedere con --radius 3/4/5")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--radius', type=int, default=None)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--karp', action='store_true')
    a = ap.parse_args()
    if a.selftest: selftest()
    elif a.radius: analyze(a.radius, do_karp=a.karp)
    else: ap.print_help()
