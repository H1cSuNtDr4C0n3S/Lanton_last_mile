# product_automaton.py — automa-prodotto A(r; m, D): finestra (2r+1)^2 + memoria temporale
# di alternanza (RADIUS §55.4, verbale §56). Lo stato:
#   - finestra nel frame canonico heading=su, celle {0=U, 1=W, 2=B, 3=B*};
#     B* = nera nota SOLO via memoria: la lettura al centro e' forzata (niente menzogna)
#     ma PAGA 1 come assumiB (tariffa = semantica base della 9x9: B* proietta su assumiB).
#     W* collassa su W (stesso costo 0 e stesso successore: il flag non serve).
#   - M = insieme (canonico, ordinato) di celle visitate USCITE dalla finestra: (pos, colore),
#     al piu' m celle, dentro il box ||.||inf <= D; eviction deterministica: si tengono le
#     m piu' vicine (tie-break lessicografico). Quando una cella di M rientra nella finestra
#     viene ripristinata: nera -> B*, bianca -> W.
# Soundness: ogni orbita reale si solleva a un cammino del prodotto (i colori ricordati sono
# veri: una cella in M non puo' cambiare senza essere visitata, e visitarla la riporta al
# centro cioe' dentro la finestra). Dimenticare (eviction) e' solo perdita d'informazione.
# Il costo (ty=2) del prodotto = costo base ESATTO lungo la proiezione (invariante:
# B non-star al centro e' sempre nota anche alla finestra base). Quindi il min cycle mean
# del prodotto e' un lower bound sulla tariffa assumiB-base di OGNI cammino infinito
# auto-consistente — l'alternanza a orizzonte (m,D) e' DENTRO gli stati (chiude il caveat
# aperiodico di RADIUS §55.4).
#
# Con m=0 il prodotto DEVE coincidere ESATTAMENTE con l'automa base (self-test).
#
# Uso:
#   python product_automaton.py --selftest
#   python product_automaton.py --radius 2 --mem 16 --box 8 [--cap N] [--delta]
# Output: build/p{r}m{m}d{D}_{outdeg,edges,tyx}.bin + _rotor_edges.txt + summary json;
# --delta lancia min_assumeB.exe (bisect + verify) e certifica delta^alt(r;m,D).

import argparse, json, os, re, subprocess, sys, time
from collections import deque

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build")
sys.path.insert(0, HERE)
from window_automaton import canon, drift_and_rot, max_power_realizable  # noqa: E402
from altmin_driver import first_conflict  # noqa: E402

U, W, B, BS = 0, 1, 2, 3
EXE = os.path.join(HERE, "min_assumeB.exe")


class Geometry:
    """mappe del frame canonico per raggio r (identiche a window_automaton.build)."""

    def __init__(self, r):
        self.r = r
        S = 2 * r + 1
        self.NC = S * S
        self.CELLS = [(x, y) for x in range(-r, r + 1) for y in range(-r, r + 1)]
        self.IDX = {c: i for i, c in enumerate(self.CELLS)}
        self.C0 = self.IDX[(0, 0)]
        # per ogni cella NUOVA i -> indice cella vecchia (o -1): R: (ox,oy)=(yp+1,-xp); L: (-yp-1,xp)
        self.mapR = [-1] * self.NC
        self.mapL = [-1] * self.NC
        for i, (xp, yp) in enumerate(self.CELLS):
            ox, oy = yp + 1, -xp
            if abs(ox) <= r and abs(oy) <= r:
                self.mapR[i] = self.IDX[(ox, oy)]
            ox, oy = -yp - 1, xp
            if abs(ox) <= r and abs(oy) <= r:
                self.mapL[i] = self.IDX[(ox, oy)]
        # posizione NUOVA di una cella vecchia (ox,oy): R -> (-oy, ox-1); L -> (oy, -ox-1)
        self.fwdR = [(-oy, ox - 1) for (ox, oy) in self.CELLS]
        self.fwdL = [(oy, -ox - 1) for (ox, oy) in self.CELLS]

    @staticmethod
    def fwd_pos(pos, turn_right):
        ox, oy = pos
        return (-oy, ox - 1) if turn_right else (oy, -ox - 1)


def pack_state(win, M, D):
    """chiave canonica: bytes(finestra) + triple ordinate (x+D, y+D, bit nero)."""
    mb = bytearray()
    for (x, y, black) in sorted(M):
        mb += bytes((x + D, y + D, black))
    return bytes(win) + bytes(mb)


def step_product(geo, m, D, win, M, col, black_only=False, black_first=False):
    """un passo del prodotto: lettura del colore col (W/B) al centro, flip, trasformazione,
    travaso finestra<->memoria, eviction. Ritorna (win', M').
    black_only: ricorda SOLO le celle nere uscite (la menzogna gratuita e' solo
    'nera dimenticata letta bianca'; bianca-letta-nera paga comunque assumiB).
    black_first: ricorda entrambe ma le nere hanno priorita' assoluta nell'eviction."""
    r = geo.r
    tmp = bytearray(win)
    tmp[geo.C0] = B if col == W else W          # flip del centro DOPO la lettura (star persa)
    right = (col == W)
    mp = geo.mapR if right else geo.mapL
    fw = geo.fwdR if right else geo.fwdL
    new = bytearray(geo.NC)
    for i in range(geo.NC):
        j = mp[i]
        new[i] = tmp[j] if j >= 0 else U
    # celle vecchie note che escono dalla finestra -> candidate memoria
    cand = []
    for j in range(geo.NC):
        v = tmp[j]
        if v == U or (black_only and v == W):
            continue
        nx, ny = fw[j]
        if abs(nx) > r or abs(ny) > r:
            cand.append((nx, ny, 1 if v != W else 0))
    # memoria esistente: trasforma; chi rientra viene ripristinato nella finestra
    for (x, y, black) in M:
        nx, ny = Geometry.fwd_pos((x, y), right)
        if abs(nx) <= r and abs(ny) <= r:
            i = geo.IDX[(nx, ny)]
            assert new[i] == U, "rientro su cella gia' nota: impossibile"
            new[i] = BS if black else W
        else:
            cand.append((nx, ny, black))
    # eviction: box D, poi le m migliori; nearest puro oppure nere-prima (black_first:
    # le nere non vengono mai sfrattate da bianche — la menzogna gratuita e' solo sul nero)
    cand = [(x, y, b) for (x, y, b) in cand if abs(x) <= D and abs(y) <= D]
    if len(cand) > m:
        if black_first:
            cand.sort(key=lambda e: (1 - e[2], max(abs(e[0]), abs(e[1])), e[0], e[1]))
        else:
            cand.sort(key=lambda e: (max(abs(e[0]), abs(e[1])), e[0], e[1]))
        cand = cand[:m]
    return bytes(new), tuple(sorted(cand))


def out_edges(geo, m, D, win, M, black_only=False, black_first=False):
    """archi uscenti dallo stato: lista (ty, tyx, tn, win', M').
    ty: 0=forzato, 1=assumiW, 2=assumiB/B* (paga). tyx: come ty ma 3=B* (diagnostica)."""
    c0 = win[geo.C0]
    if c0 == U:
        opts = ((W, 1, 1), (B, 2, 2))
    elif c0 == W:
        opts = ((W, 0, 0),)
    elif c0 == B:
        opts = ((B, 0, 0),)
    else:  # B*: lettura forzata nera, ma paga come assumiB
        opts = ((B, 2, 3),)
    res = []
    for col, ty, tyx in opts:
        nw, nM = step_product(geo, m, D, win, M, col, black_only, black_first)
        res.append((ty, tyx, 1 if col == W else 0, nw, nM))
    return res


def build(r, m, D, cap=0, progress_every=200000, black_only=False, black_first=False):
    geo = Geometry(r)
    start_win = bytes(geo.NC)
    start = (start_win, ())
    key0 = pack_state(start_win, (), D)
    states = {key0: 0}
    order = [start]
    src_l, dst_l, ty_l, tyx_l, tn_l = [], [], [], [], []
    q = deque([0])
    t0 = time.time()
    while q:
        si = q.popleft()
        win, M = order[si]
        for ty, tyx, tn, nw, nM in out_edges(geo, m, D, win, M, black_only, black_first):
            k = pack_state(nw, nM, D)
            d = states.get(k)
            if d is None:
                d = len(order)
                states[k] = d
                order.append((nw, nM))
                q.append(d)
                if cap and d >= cap:
                    raise RuntimeError(f"ABORT: superato il cap di {cap} stati")
            src_l.append(si); dst_l.append(d); ty_l.append(ty); tyx_l.append(tyx); tn_l.append(tn)
        if len(order) % progress_every < 2 and len(order) > progress_every:
            print(f"  ... {len(order)} stati, {time.time()-t0:.0f}s", flush=True)
    src = np.array(src_l, np.int64); dst = np.array(dst_l, np.int64)
    ty = np.array(ty_l, np.int8); tyx = np.array(tyx_l, np.int8); tn = np.array(tn_l, np.int8)
    return order, src, dst, ty, tyx, tn


def entropy_sp(src, dst, N, iters=6000, tol=1e-13, patience=50):
    if len(src) == 0:
        return float("-inf"), 0
    Mx = sp.coo_matrix((np.ones(len(src), np.float64), (dst, src)), shape=(N, N)).tocsr()
    v = np.full(N, 1.0 / N, np.float64)
    lam, stable = 1.0, 0
    it = 0
    for it in range(1, iters + 1):
        nv = Mx @ v
        s = nv.sum()
        if s == 0:
            return float("-inf"), it
        v = nv / s
        stable = stable + 1 if abs(s - lam) < tol * max(1.0, abs(s)) else 0
        lam = s
        if stable >= patience:
            break
    return float(np.log2(lam)), it


def load_c(pfx, outdir):
    """carica i binari prodotti da product_build.exe (validati byte-per-byte vs build())."""
    deg = np.fromfile(os.path.join(outdir, f"{pfx}_outdeg.bin"), dtype=np.uint8)
    N = len(deg)
    edt = np.dtype([("dst", "<u4"), ("ty", "u1"), ("tn", "u1")])
    e = np.fromfile(os.path.join(outdir, f"{pfx}_edges.bin"), dtype=edt)
    src = np.repeat(np.arange(N, dtype=np.int64), deg)
    dst = e["dst"].astype(np.int64)
    ty = e["ty"].astype(np.int8)
    tn = e["tn"].astype(np.int8)
    tyx = np.fromfile(os.path.join(outdir, f"{pfx}_tyx.bin"), dtype=np.uint8).astype(np.int8)
    assert len(src) == len(dst) == len(tyx)
    return N, src, dst, ty, tyx, tn


def analyze(r, m, D, cap=0, do_delta=False, outdir=BUILD, use_c=False,
            black_only=False, black_first=False):
    mode = 1 if black_only else (2 if black_first else 0)
    tag = {0: "", 1: "b", 2: "h"}[mode]          # b=black-only, h=ibrida nere-prima
    pfx = f"p{r}m{m}d{D}{tag}"
    print(f"== prodotto A(r={r}; m={m}, D={D}) modo={['full','black-only','ibrida'][mode]}"
          f"{' [builder C]' if use_c else ''} ==", flush=True)
    t0 = time.time()
    if use_c:
        exe = os.path.join(HERE, "product_build.exe")
        args = [exe, str(r), str(m), str(D), outdir, str(cap), str(mode)]
        rc = subprocess.call(args)
        if rc != 0:
            raise RuntimeError(f"product_build fallito (rc={rc})")
        N, src, dst, ty, tyx, tn = load_c(pfx, outdir)
    else:
        order, src, dst, ty, tyx, tn = build(r, m, D, cap=cap,
                                             black_only=black_only, black_first=black_first)
        N = len(order)
    cnt = {k: int((tyx == v).sum()) for k, v in
           (("forced", 0), ("assumeW", 1), ("assumeB", 2), ("Bstar", 3))}
    print(f"stati: {N}, archi: {len(src)} (forzati {cnt['forced']}, assumiW {cnt['assumeW']}, "
          f"assumiB {cnt['assumeB']}, B* {cnt['Bstar']}) [{time.time()-t0:.0f}s]", flush=True)

    h_full, itf = entropy_sp(src, dst, N)
    mask = ty != 2
    h_noB, itn = entropy_sp(src[mask], dst[mask], N)
    print(f"entropia piena: {h_full:.4f} ({itf} iter) | senza-pagamenti: {h_noB:.6f} ({itn} iter)",
          flush=True)

    # SCC ricorrenti del sottografo senza-pagamenti + rotori (stessa logica di analyze_radius)
    srcB, dstB, tnB = src[mask], dst[mask], tn[mask]
    G = sp.coo_matrix((np.ones(len(srcB), np.int8), (srcB, dstB)), shape=(N, N)).tocsr()
    ncomp, labels = connected_components(G, directed=True, connection="strong")
    del G
    sizes = np.bincount(labels)
    rec = set(np.flatnonzero(sizes > 1).tolist())
    rec |= set(labels[srcB[srcB == dstB]].tolist())
    rec_arr = np.array(sorted(rec), dtype=labels.dtype)
    rec_sizes = sorted(int(sizes[l]) for l in rec)
    print(f"SCC ricorrenti senza-pagamenti: {len(rec)}, taglie: {rec_sizes[-12:]}", flush=True)

    rotor_pairs = []
    cycles, all_rotors = [], True
    if rec:
        rec_nodes = np.flatnonzero(np.isin(labels, rec_arr))
        sel = np.isin(srcB, rec_nodes)
        es, ed, et = srcB[sel], dstB[sel], tnB[sel]
        internal = labels[es] == labels[ed]
        es, ed, et = es[internal], ed[internal], et[internal]
        rotor_pairs = sorted(set(zip(es.tolist(), ed.tolist())))
        out_e = {}
        for s, d, t in zip(es.tolist(), ed.tolist(), et.tolist()):
            out_e.setdefault(s, []).append((d, t))
        lab_of = labels[rec_nodes]
        o = np.argsort(lab_of, kind="stable")
        groups = np.split(rec_nodes[o], np.flatnonzero(np.diff(lab_of[o])) + 1)
        for grp in groups:
            comp = grp.tolist()
            if any(len(out_e.get(v, [])) != 1 for v in comp):
                all_rotors = False
                print(f"  !! SCC taglia {len(comp)} NON e' un rotore (branching interno)", flush=True)
                continue
            v, word = comp[0], []
            for _ in range(len(comp)):
                d, t = out_e[v][0]
                word.append("R" if t else "L")
                v = d
            assert v == comp[0]
            cycles.append(canon("".join(word)))
    uniq = sorted(set(cycles), key=len)
    print(f"rotori: {all_rotors} | parole cicliche distinte: {len(uniq)}", flush=True)
    verdicts = {}
    for w in uniq:
        rot, dr = drift_and_rot(w)
        if rot % 4 != 0:
            verdicts[w] = f"B-T (rot={rot})"
        elif dr == (0, 0):
            verdicts[w] = "B-T (drift nullo)"
        else:
            verdicts[w] = "DA VERIFICARE con gamma_enum check"
        conf = first_conflict(w)
        alt = "alternanza-OK" if conf is None else f"FANTASMA(d={conf['distanza']})"
        print(f"  p={len(w):3d} {w if len(w) <= 50 else w[:47]+'...'} -> {verdicts[w]} | {alt}")

    # scrittura binari per min_assumeB (stesso formato di window_build.c, prefisso pfx);
    # col builder C i binari sono gia' su disco, serve solo rotor_edges.txt
    os.makedirs(outdir, exist_ok=True)
    if not use_c:
        deg = np.bincount(src, minlength=N)
        assert deg.max() <= 2 and deg.min() >= 1
        deg.astype(np.uint8).tofile(os.path.join(outdir, f"{pfx}_outdeg.bin"))
        edt = np.dtype([("dst", "<u4"), ("ty", "u1"), ("tn", "u1")])
        e = np.zeros(len(src), dtype=edt)
        o = np.argsort(src, kind="stable")
        e["dst"] = dst[o].astype(np.uint32)
        e["ty"] = ty[o].astype(np.uint8)
        e["tn"] = tn[o].astype(np.uint8)
        e.tofile(os.path.join(outdir, f"{pfx}_edges.bin"))
        tyx[o].astype(np.uint8).tofile(os.path.join(outdir, f"{pfx}_tyx.bin"))
    with open(os.path.join(outdir, f"{pfx}_rotor_edges.txt"), "w") as f:
        for s, d in rotor_pairs:
            f.write(f"{s} {d}\n")

    out = {"radius": r, "mem": m, "box": D,
           "mode": ["full", "black-only", "black-first"][mode],
           "states": N, "edges": int(len(src)),
           "edge_types": cnt, "entropy_full": h_full, "entropy_noPay": h_noB,
           "recurrent_sccs_noPay": len(rec), "recurrent_sizes": rec_sizes,
           "all_rotors": all_rotors, "cycle_words": uniq, "verdicts": verdicts,
           "rotor_max_powers": {w: max_power_realizable(w) for w in uniq},
           "seconds": time.time() - t0}

    if do_delta:
        out["delta"] = compute_delta(pfx, outdir)
    fn = os.path.join(ROOT, "results", f"product_{pfx}_summary.json")
    json.dump(out, open(fn, "w"), indent=1)
    print(f"salvato {fn}  [{time.time()-t0:.0f}s]\n", flush=True)
    return out


def compute_delta(pfx, outdir=BUILD, maxrounds=2000):
    """bisect (localizzatore) + estrazione ciclo + verify INTERO (certificato)."""
    print(f"  delta^alt({pfx}): bisezione min_assumeB...", flush=True)
    res = subprocess.run([EXE, outdir, pfx, "bisect", str(maxrounds)],
                         capture_output=True, text=True)
    if res.returncode == 4:
        print("  !! noB-senza-rotori NON e' un DAG: fatto strutturale falsificato nel prodotto")
        return {"error": "noDAG"}
    if res.returncode != 0:
        print(f"  !! bisect rc={res.returncode}\n{res.stdout[-2000:]}")
        return {"error": f"rc{res.returncode}"}
    mm = re.search(r"media p/q=(\d+)/(\d+)", res.stdout)
    if not mm:
        print(f"  !! parsing fallito:\n{res.stdout[-2000:]}")
        return {"error": "parse"}
    p, q = int(mm.group(1)), int(mm.group(2))
    cyc = open(os.path.join(outdir, f"{pfx}_delta_cycle.txt")).read().split()
    word = cyc[5]
    conf = first_conflict(word)
    rot, dr = drift_and_rot(word)
    ver = subprocess.run([EXE, outdir, pfx, "verify", str(p), str(q)],
                         capture_output=True, text=True)
    certified = "fixpoint INTERO" in ver.stdout
    print(f"  delta^alt = {p}/{q} = {p/q:.6f} | certificato lower bound: {certified} | "
          f"testimone: rot={rot:+d} drift={dr} "
          f"{'alternanza-OK' if conf is None else 'ancora FANTASMA (d=%d)' % conf['distanza']}",
          flush=True)
    return {"p": p, "q": q, "value": p / q, "verified": certified,
            "witness_word": word, "witness_conflict": conf,
            "witness_rot": rot, "witness_drift": list(dr)}


# ---------------------------------------------------------------- validazione

def walk_word(word, r, m, D, max_steps, black_only=False, black_first=False):
    """cammina la parola come cammino del prodotto nel FRAME CANONICO.
    Ritorna (step del blocco o None, costo accumulato, n. letture per tipo)."""
    geo = Geometry(r)
    win, M = bytes(geo.NC), ()
    cost = 0
    counts = {"forced": 0, "assumeW": 0, "assumeB": 0, "Bstar": 0}
    L = len(word)
    for t in range(max_steps):
        want = word[t % L]
        c0 = win[geo.C0]
        if c0 == U:
            col = W if want == "R" else B
            counts["assumeW" if col == W else "assumeB"] += 1
            cost += (col == B)
        else:
            col = W if c0 == W else B
            forced = "R" if col == W else "L"
            if forced != want:
                return t, cost, counts
            counts["Bstar" if c0 == BS else "forced"] += 1
            cost += (c0 == BS)
        win, M = step_product(geo, m, D, win, M, col, black_only, black_first)
    return None, cost, counts


def simulate_langton(steps):
    """formica vera su griglia vuota (bianca): ritorna la parola delle svolte.
    Convenzioni CLAUDE.md §2: bianco->R, nero->L, flip, mossa; heading 0=su."""
    DXh = [0, 1, 0, -1]; DYh = [1, 0, -1, 0]
    grid = {}
    x = y = h = 0
    word = []
    for _ in range(steps):
        c = grid.get((x, y), W)
        if c == W:
            word.append("R"); h = (h + 1) & 3; grid[(x, y)] = B
        else:
            word.append("L"); h = (h - 1) & 3; grid[(x, y)] = W
        x += DXh[h]; y += DYh[h]
    return "".join(word)


def selftest():
    print("SELF-TEST prodotto A(r;m,D)")
    # 1) m=0 deve coincidere ESATTAMENTE con l'automa base (certificati r=1,2)
    cert = {1: (15, 26, 4, 11, 0.8114, [canon("RRRRL")]),
            2: (403, 554, 252, 151, 0.7594,
                sorted([canon("RRRLLR"), canon("RRRLLRRRRLLR"), canon("RRRRLRRRRLLLLRL")], key=len))}
    for r, (Nc, Ec, Fc, Ac, hc, words) in cert.items():
        out = analyze(r, 0, r + 1)
        assert out["states"] == Nc, (r, out["states"])
        assert out["edges"] == Ec, (r, out["edges"])
        assert out["edge_types"]["forced"] == Fc, out["edge_types"]
        assert out["edge_types"]["assumeW"] == Ac == out["edge_types"]["assumeB"], out["edge_types"]
        assert out["edge_types"]["Bstar"] == 0
        assert abs(out["entropy_full"] - hc) < 2e-3
        assert out["cycle_words"] == words, (r, out["cycle_words"])
    print("  [1] m=0 == automa base (r=1,2): OK")

    # 2) sollevamento delle orbite reali: la formica vera NON viene mai bloccata,
    #    e il costo e' INVARIANTE in (m,D) (= tariffa base: B* converte assumiB, non li crea)
    wlang = simulate_langton(3000)
    base = walk_word(wlang, 2, 0, 3, 3000)
    assert base[0] is None, f"orbita reale bloccata a m=0?! step {base[0]}"
    for (m, D) in ((4, 6), (16, 8), (32, 12)):
        blocked, cost, cnts = walk_word(wlang, 2, m, D, 3000)
        assert blocked is None, f"orbita reale bloccata da A(2;{m},{D}) a step {blocked}"
        assert cost == base[1], (cost, base[1], m, D)
    print(f"  [2] orbita reale (3000 passi, r=2): mai bloccata, costo invariante = {base[1]}: OK")

    # 3) identita' incrociata col simulatore in coordinate assolute (ghost_block_analysis):
    #    stesso step di blocco sui testimoni-fantasma r1/r2/r3, per piu' (m,D)
    from ghost_block_analysis import product_blocks_word
    for rr in (1, 2, 3):
        toks = open(os.path.join(BUILD, f"r{rr}_delta_cycle.txt")).read().split()
        wd = toks[5]
        for (m, D) in ((2, 4), (8, 8), (16, 8)):
            t_abs = product_blocks_word(wd, rr, m, D, "near", 50 * len(wd))
            t_can = walk_word(wd, rr, m, D, 50 * len(wd))[0]
            assert t_abs == t_can, (rr, m, D, t_abs, t_can)
    print("  [3] frame canonico == coordinate assolute (blocco identico su testimoni r1-r3): OK")

    # 4) i fantasmi del catalogo r=4 muoiono TUTTI nel walker canonico a (m=32, D=8)
    cat = os.path.join(ROOT, "results", "delta4_alt_catalog.jsonl")
    n = killed = 0
    for line in open(cat):
        rec = json.loads(line)
        if not rec.get("conflitto") or rec.get("dup"):
            continue
        n += 1
        t = walk_word(rec["word"], 4, 32, 8, rec["conflitto"]["step"] + 1)[0]
        killed += t is not None
    assert killed == n, (killed, n)
    print(f"  [4] catalogo fantasmi r=4: {killed}/{n} bloccati da A(4;32,8) nel frame canonico: OK")
    print("SELF-TEST PRODOTTO: TUTTO OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--radius", type=int)
    ap.add_argument("--mem", type=int, default=16)
    ap.add_argument("--box", type=int, default=8)
    ap.add_argument("--cap", type=int, default=0)
    ap.add_argument("--delta", action="store_true")
    ap.add_argument("--use-c", action="store_true", help="BFS con product_build.exe (validato)")
    ap.add_argument("--black-only", action="store_true", help="memoria solo celle nere")
    ap.add_argument("--black-first", action="store_true", help="eviction con priorita' alle nere")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.radius is not None:
        analyze(a.radius, a.mem, a.box, cap=a.cap, do_delta=a.delta, use_c=a.use_c,
                black_only=a.black_only, black_first=a.black_first)
    else:
        ap.print_help()
