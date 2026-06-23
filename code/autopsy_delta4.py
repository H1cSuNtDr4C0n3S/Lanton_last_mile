# autopsy_delta4.py — autopsia del ciclo testimone delta4 = 2/313 ("il miglior evasore").
# Risponde alle domande di §54: dove e come avvengono i 2 pagamenti assumiB, struttura dei
# morsi, geometria della traiettoria, rivisite interne, fattori comuni con W0 e coi rotori,
# realizzabilita' (quanto a lungo un'orbita reale puo' cavalcarlo).
# Input: build/r4c_delta_cycle.txt (+_annot.txt), build/r4c_nodes.bin, build/r4_pool.bin.

import os, sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
sys.path.insert(0, os.path.join(ROOT, "code"))
from window_automaton import canon, drift_and_rot, max_power_realizable  # noqa: E402

R = 4
S = 2 * R + 1
NC = S * S
KB = (NC + 3) // 4

# --- carica ciclo annotato ---
lines = open(os.path.join(BUILD, "r4c_delta_cycle.txt")).read().split()
p, q, word, types = int(lines[1]), int(lines[3]), lines[5], lines[7]
assert len(word) == q == len(types) and types.count("B") == p
annot = [l.split() for l in open(os.path.join(BUILD, "r4c_delta_cycle_annot.txt"))
         if not l.startswith("#")]
assert len(annot) == q
dstnode = [int(a[3]) for a in annot]
nodes_map = np.fromfile(os.path.join(BUILD, "r4c_nodes.bin"), dtype=np.uint32)
pool = open(os.path.join(BUILD, "r4_pool.bin"), "rb")

def decode_state(reduced_id):
    orig = int(nodes_map[reduced_id])
    pool.seek(orig * KB)
    raw = pool.read(KB)
    cells = [(raw[i >> 2] >> ((i & 3) << 1)) & 3 for i in range(NC)]
    return cells, orig

def show_state(cells, label):
    print(f"  finestra 9x9 ({label}; formica al centro, heading su; .=ignota o=bianca x=nera):")
    for y in range(R, -R - 1, -1):
        row = "".join({0: ".", 1: "o", 2: "x"}[cells[(x + R) * S + (y + R)]] for x in range(-R, R + 1))
        print(f"    {row}")

print(f"=== AUTOPSIA ciclo delta4: p={p}, q={q}, media {p}/{q} = {p/q:.6f} ===\n")
rot, dr = drift_and_rot(word)
print(f"parola (canonica: inizia dallo step 0 dell'estrazione):\n  {word}")
print(f"tipi:\n  {types}")
print(f"rot = {rot:+d} ({'≡' if rot % 4 == 0 else '≢'} 0 mod 4), drift = {dr}")
print(f"conteggi: forzati {types.count('F')}, assumiW {types.count('W')}, assumiB {types.count('B')}")
mp = max_power_realizable(word)
print(f"potenza massima realizzabile della parola: {mp}\n")

# --- i due pagamenti ---
bpos = [i for i, t in enumerate(types) if t == "B"]
gaps = [(bpos[(i + 1) % p] - bpos[i]) % q for i in range(p)]
print(f"pagamenti assumiB agli step {bpos}; gap ciclici tra pagamenti: {gaps}")
for k in bpos:
    src_red = dstnode[(k - 1) % q]      # stato PRIMA dello step k = dst dello step k-1
    cells, orig = decode_state(src_red)
    n_ign = cells.count(0)
    print(f"\nPAGAMENTO allo step {k}: svolta {word[k]} (stato originale #{orig}, "
          f"{n_ign} ignote, {cells.count(1)} bianche, {cells.count(2)} nere)")
    show_state(cells, f"prima dello step {k}")
    ctx = "".join(types[(k + d) % q] for d in range(-12, 13))
    wtx = "".join(word[(k + d) % q] for d in range(-12, 13))
    print(f"  contesto ±12 (tipi):  {ctx[:12]}[{ctx[12]}]{ctx[13:]}")
    print(f"  contesto ±12 (parola): {wtx[:12]}[{wtx[12]}]{wtx[13:]}")

# confronto dei due stati di pagamento
if p == 2:
    c1, o1 = decode_state(dstnode[(bpos[0] - 1) % q])
    c2, o2 = decode_state(dstnode[(bpos[1] - 1) % q])
    print(f"\ni due stati di pagamento sono {'IDENTICI' if c1 == c2 else 'diversi'}")
    if c1 != c2:
        # prova le 4 rotazioni C4 della finestra (heading e' canonico, quindi
        # un'uguaglianza a meno di rotazione indicherebbe lo stesso meccanismo ruotato)
        def rotC4(cells):
            out = [0] * NC
            for x in range(-R, R + 1):
                for y in range(-R, R + 1):
                    out[(y + R) * S + (-x + R)] = cells[(x + R) * S + (y + R)]
            return out
        c = c2
        for k in range(1, 4):
            c = rotC4(c)
            if c == c1:
                print(f"  ... ma coincidono a meno di rotazione C4^{k}")
                break
        else:
            same = sum(1 for a, b in zip(c1, c2) if a == b)
            print(f"  celle uguali {same}/{NC}")

# --- morsi (run massimali di W) e ritmo dei tipi ---
runs, cur = [], 0
t2 = types + types  # ciclico: trova le run sul doppio e tieni quelle che iniziano nel primo giro
i = 0
runsW = []
while i < q:
    if types[i] == "W":
        j = i
        ln = 0
        while t2[j] == "W":
            ln += 1; j += 1
        runsW.append((i, ln)); i += ln
    else:
        i += 1
from collections import Counter
print(f"\nmorsi (run di assumiW): {len(runsW)} run, lunghezze {Counter(l for _, l in runsW)}")
print(f"posizioni morsi (start, len): {runsW}")

# --- traiettoria spaziale su un periodo ---
DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
x = y = h = 0
visits = {}
traj = []
deep_cells = {}
for k, c in enumerate(word):
    visits.setdefault((x, y), []).append(k)
    traj.append((x, y))
    if types[k] == "B":
        deep_cells[k] = (x, y)
    h = (h + 1) & 3 if c == "R" else (h - 1) & 3
    x += DX[h]; y += DY[h]
ncells = len(visits)
multi = {c: v for c, v in visits.items() if len(v) > 1}
xs = [c[0] for c in visits]; ys = [c[1] for c in visits]
print(f"\ntraiettoria su 1 periodo: {ncells} celle distinte in {q} passi "
      f"(rivisite interne: {q - ncells} = {(q-ncells)/q*100:.1f}%)")
print(f"bounding box: x [{min(xs)},{max(xs)}], y [{min(ys)},{max(ys)}]")
print(f"celle multi-visita: {len(multi)}; visite max su una cella: "
      f"{max(len(v) for v in visits.values())}")
for k, cell in deep_cells.items():
    prev = [t for t in visits[cell] if t < k]
    print(f"pagamento step {k} sulla cella {cell}: visite precedenti nello stesso periodo: "
          f"{prev if prev else 'NESSUNA (il nero viene da fuori dal periodo)'}")

# il ciclo ripetuto: i pagamenti del periodo n cadono su celle scritte dal periodo n-1?
x = y = h = 0
seen_at = {}
hits = []
for rep in range(3):
    for k, c in enumerate(word):
        if types[k] == "B" and (x, y) in seen_at and seen_at[(x, y)][0] < rep:
            hits.append((rep, k, (x, y), seen_at[(x, y)]))
        seen_at[(x, y)] = (rep, k)
        h = (h + 1) & 3 if c == "R" else (h - 1) & 3
        x += DX[h]; y += DY[h]
print(f"\npagamenti su celle visitate in periodi PRECEDENTI (3 ripetizioni): "
      f"{[(r, k, cell, prev) for r, k, cell, prev in hits] if hits else 'nessuno'}")

# --- fattori comuni (ciclici) con W0 e coi rotori ---
def longest_common_factor_cyclic(a, b):
    """massimo fattore della parola ciclica a presente nella parola ciclica b"""
    A, B = a + a, b + b
    best = ""
    for i in range(len(a)):
        lo, hi = len(best), min(len(a), len(b))
        for L in range(len(best) + 1, hi + 1):
            if A[i:i + L] in B:
                best = A[i:i + L]
            else:
                break
    return best

w0 = open(os.path.join(ROOT, "data", "w0.txt")).read().strip().replace("\n", "")
rotors = {"p10": "LLRRLLRRRR", "p20": "LLRRLLRRRR" * 2,
          "p74": "LLLLRLLLLRLRRRRLRRRRLLLLRLRRRRLRRRRLLLLRLLRRRRLLRLRRRRLRRRRLLLLRLRRRRLRRRR",
          "p15(r3)": "LLLLRLRRRRLRRRR"}
print(f"\nW0 (periodo {len(w0)}): fattore comune ciclico piu' lungo col ciclo delta4:")
f = longest_common_factor_cyclic(word, w0)
print(f"  len {len(f)}: {f}")
for name, rw in rotors.items():
    f = longest_common_factor_cyclic(rw, word)
    print(f"rotore {name} (p={len(rw)}): fattore comune con delta4 len {len(f)}"
          f"{' = INTERO rotore' if len(f) >= len(rw) else ''}: {f if len(f) <= 80 else f[:77]+'...'}")
# copertura del ciclo con fattori di W0: lunghezza massima di fattore W0 che copre ogni posizione
W2 = w0 + w0
cov = []
for i in range(q):
    L = 0
    while L < q and (word + word)[i:i + L + 1] in W2:
        L += 1
    cov.append(L)
print(f"\ncopertura W0: fattore-W0 massimo che parte da ogni posizione: "
      f"min {min(cov)}, mediana {sorted(cov)[q//2]}, max {max(cov)}")
print("fatto")
