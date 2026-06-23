# morso_census.py — Step 1a: censimento dei morsi e dei contesti inter-morso
# Morso = run massimale di letture fresche-bianche (Lemma del morso: <= 4).
# Tre misure: (A) transienti dinamici famiglia baseline, (B) linguaggio esatto
# uniforme su R(p), (C) riferimento highway dalla maschera F.
import numpy as np, pickle
from collections import Counter, defaultdict

rng = np.random.default_rng(2026)
DX = [0,1,0,-1]; DY = [1,0,-1,0]
W0 = np.load('/home/claude/ant_pkg/W0.npy').astype(np.int8)

# ---------- (A) dinamico ----------
def run_transient(rng, max_steps=60000):
    side = rng.integers(7,16); dens = rng.uniform(0.25,0.55)
    H = 1024; off = H//2
    grid = np.zeros((H,H), np.uint8)
    patch = (rng.random((side,side)) < dens).astype(np.uint8)
    grid[off-side//2:off-side//2+side, off-side//2:off-side//2+side] = patch
    visited = np.zeros((H,H), bool)
    x, y, h = off, off, 0
    turns = np.empty(max_steps, np.int8)
    fresh = np.empty(max_steps, bool)
    color = np.empty(max_steps, np.int8)
    for t in range(max_steps):
        c = grid[y, x]
        fresh[t] = not visited[y, x]
        visited[y, x] = True
        color[t] = c
        if c == 0:
            turns[t] = 1; h = (h+1) & 3
        else:
            turns[t] = 0; h = (h-1) & 3
        grid[y, x] = 1 - c
        x += DX[h]; y += DY[h]
        if not (2 < x < H-3 and 2 < y < H-3):
            return None
    return turns, fresh, color

def detect_onset(turns):
    T = len(turns)
    # minimo N0 tale che turns[N0:] e' 104-periodico, coda >= 520
    tail = turns[T-520:]
    if not np.all(tail[:-104] == tail[104:]): return None
    # retrocedi
    n0 = T-520
    while n0 > 0 and turns[n0-1] == turns[n0-1+104]:
        n0 -= 1
    return n0

def segment_bites(turns, fresh, color, n0):
    """morsi (run fresche-bianche) e gap nel transiente [0, n0)."""
    fw = fresh[:n0] & (color[:n0] == 0)   # fresca-bianca
    fb = fresh[:n0] & (color[:n0] == 1)   # fresca-nera (lettura di seed)
    bites = []   # (start, len)
    gaps  = []   # (start, len, n_freshblack, turnword)
    t = 0
    cur_gap_start = None
    while t < n0:
        if fw[t]:
            if cur_gap_start is not None:
                g0 = cur_gap_start
                gaps.append((g0, t-g0, int(fb[g0:t].sum()),
                             ''.join('R' if u else 'L' for u in turns[g0:t]) if t-g0 <= 24 else None))
                cur_gap_start = None
            l = 0
            while t < n0 and fw[t]: l += 1; t += 1
            bites.append(l)
        else:
            if cur_gap_start is None: cur_gap_start = t
            t += 1
    return bites, gaps, fw, fb

NRUN = 60
all_bites = Counter(); all_gaplen = Counter(); gapwords = defaultdict(Counter)
freshblack_per_gap = Counter(); bite_bigram = Counter()
rates = []; win_min_rates = []
tot_steps = 0; tot_fw = 0; tot_fb = 0
done = 0
while done < NRUN:
    out = run_transient(rng)
    if out is None: continue
    turns, fresh, color = out
    n0 = detect_onset(turns)
    if n0 is None or n0 < 1500: continue
    bites, gaps, fw, fb = segment_bites(turns, fresh, color, n0)
    for b in bites: all_bites[b] += 1
    for i in range(len(bites)-1): bite_bigram[(bites[i], bites[i+1])] += 1
    for g0, gl, nfb, wword in gaps:
        all_gaplen[gl] += 1
        freshblack_per_gap[nfb] += 1
        if wword is not None: gapwords[gl][wword] += 1
    tot_steps += n0; tot_fw += int(fw.sum()); tot_fb += int(fb.sum())
    rates.append(fw.sum()/n0)
    # tasso di morso su finestre scorrevoli di 312: il pavimento
    if n0 > 1000:
        c = np.cumsum(fw)
        wr = (c[312:] - c[:-312]) / 312.0
        win_min_rates.append(float(wr.min()))
    done += 1

print(f"(A) DINAMICO — {done} transienti, {tot_steps} passi")
print(f"    tasso di morso globale: {tot_fw/tot_steps:.4f}  (fresche-nere: {tot_fb/tot_steps:.4f})")
print(f"    distribuzione lunghezze morso: {dict(sorted(all_bites.items()))}")
print(f"    max morso: {max(all_bites)}  (lemma: <=4)")
print(f"    min tasso su finestra 312: media {np.mean(win_min_rates):.4f}, min assoluto {min(win_min_rates):.4f}")
print(f"    fresche-nere per gap: {dict(sorted(freshblack_per_gap.items()))}")
gl = sorted(all_gaplen.items())
print(f"    lunghezze gap (top 12): {gl[:12]}  ... coda: {gl[-3:]}")

# ---------- (B) linguaggio esatto, uniforme su R(p) ----------
def exact_census(p):
    bites_c = Counter(); gap_c = Counter(); leaves = 0
    # DFS iterativo con annotazione freschezza
    lastt = {}
    path = []  # (x,y,h,cellkey,prev_lastt,fresh,turn)
    def rec(depth, x, y, h, seq):
        nonlocal leaves
        if depth == p:
            leaves += 1
            # segmenta fresh-R
            t = 0; prev_gap = 0; first = True
            while t < p:
                if seq[t] == 2:  # fresh-R
                    l = 0
                    while t < p and seq[t] == 2: l += 1; t += 1
                    if l <= 4: bites_c[l] += 1
                    else: bites_c[l] += 1
                    if not first: gap_c[prev_gap] += 1
                    first = False; prev_gap = 0
                else:
                    prev_gap += 1; t += 1
            return
        key = (x, y)
        lt = lastt.get(key, -1)
        if lt == -1:
            for b in (1, 0):
                lastt[key] = b
                nh = (h+1)&3 if b else (h-1)&3
                seq.append(2 if b else 3)  # 2=freshR, 3=freshL
                rec(depth+1, x+DX[nh], y+DY[nh], nh, seq)
                seq.pop()
            del lastt[key]
        else:
            b = 1 - lt
            lastt[key] = b
            nh = (h+1)&3 if b else (h-1)&3
            seq.append(1 if b else 0)  # rivisita
            rec(depth+1, x+DX[nh], y+DY[nh], nh, seq)
            seq.pop()
            lastt[key] = lt
    import sys; sys.setrecursionlimit(10000)
    rec(0, 0, 0, 0, [])
    return leaves, bites_c, gap_c

leaves, bites_c, gap_c = exact_census(20)
tb = sum(k*v for k, v in bites_c.items()); ts = leaves*20
print(f"\n(B) LINGUAGGIO ESATTO p=20 — {leaves} parole (atteso 81498)")
print(f"    tasso di morso medio: {tb/ts:.4f}")
print(f"    distribuzione lunghezze morso: {dict(sorted(bites_c.items()))}")
print(f"    lunghezze gap interne: {sorted(gap_c.items())[:12]}")

# ---------- (C) highway ----------
F = [13,14,15,27,28,29,32,38,45,46,47,55,56,57,60,61,62,70,71,72,75,89]
bursts = []; gapsH = []
i = 0
while i < len(F):
    j = i
    while j+1 < len(F) and F[j+1] == F[j]+1: j += 1
    bursts.append(F[j]-F[i]+1)
    i = j+1
for k in range(len(bursts)):
    pass
# gap ciclici tra raffiche
starts = []; ends = []
i = 0
while i < len(F):
    j = i
    while j+1 < len(F) and F[j+1] == F[j]+1: j += 1
    starts.append(F[i]); ends.append(F[j]); i = j+1
gapsH = [(starts[(k+1) % len(starts)] - ends[k] - 1) % 104 for k in range(len(starts))]
print(f"\n(C) HIGHWAY — raffiche: {bursts} (tasso {sum(bursts)/104:.4f}), gap: {gapsH}")

pickle.dump({'dyn_bites': dict(all_bites), 'dyn_gaplen': dict(all_gaplen),
             'dyn_bigram': dict(bite_bigram), 'dyn_freshblack': dict(freshblack_per_gap),
             'dyn_rate': tot_fw/tot_steps, 'dyn_winmin': win_min_rates,
             'gapwords': {k: dict(v.most_common(20)) for k, v in gapwords.items()},
             'exact_p20': (leaves, dict(bites_c), dict(gap_c)),
             'highway': (bursts, gapsH)},
            open('/home/claude/ant_pkg/morso_census.pkl', 'wb'))
print("\nsalvato morso_census.pkl")
