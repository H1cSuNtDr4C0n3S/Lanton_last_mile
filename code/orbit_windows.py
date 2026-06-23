# orbit_windows.py — MINIMO (non media) del tasso di letture nere profonde su sliding
# window lunghe, nel transiente reale non-highway. Domanda di Michael: i minimi reali
# stanno molto sopra delta4_auto = 2/313? Se si', la regione economica del grafo non e'
# fisica ma un artefatto del leak. Griglia vuota + configurazioni iniziali finite random.
# Semantica di memoria identica a orbit_debt.py (cella nota solo se letta e mai uscita
# dalla finestra 9x9 da allora).

import random, sys

sys.stdout.reconfigure(encoding="utf-8")
R = 4
DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
WINDOWS = [313, 626, 1000, 5000]
DELTA4 = 2 / 313


def run(black_init, total):
    black = set(black_init)
    known = set()
    x = y = h = 0
    turns = []
    deep_black = []
    for t in range(total):
        c = (x, y)
        cb = c in black
        turns.append('L' if cb else 'R')
        if c not in known and cb:
            deep_black.append(t)
        if cb:
            black.discard(c); h = (h - 1) & 3
        else:
            black.add(c); h = (h + 1) & 3
        known.add(c)
        x += DX[h]; y += DY[h]
        for cell in [(x - 5, y + d) for d in range(-5, 6)] + \
                    [(x + 5, y + d) for d in range(-5, 6)] + \
                    [(x + d, y - 5) for d in range(-5, 6)] + \
                    [(x + d, y + 5) for d in range(-5, 6)]:
            known.discard(cell)
    return turns, deep_black


def onset_of(turns, per=104):
    i = len(turns) - per - 1
    while i >= 0 and turns[i] == turns[i + per]:
        i -= 1
    return i + 1


def analyze(name, black_init, total=22000):
    turns, deep = run(black_init, total)
    onset = onset_of(turns)
    horizon = onset if onset < total - 2 * 104 else total  # se non aggancia: tutto transiente
    is_deep = [0] * (horizon + 1)
    for t in deep:
        if t < horizon:
            is_deep[t] = 1
    pref = [0]
    for v in is_deep[:horizon]:
        pref.append(pref[-1] + v)
    tot_tr = pref[-1]
    print(f"\n{name}: onset={onset if onset < total - 2*104 else 'non agganciato entro ' + str(total)}"
          f", transiente analizzato {horizon} passi, nere profonde {tot_tr} "
          f"({tot_tr/max(horizon,1):.4f}/passo)")
    for L in WINDOWS:
        if horizon < L:
            print(f"  L={L:5d}: transiente troppo corto")
            continue
        counts = [pref[a + L] - pref[a] for a in range(horizon - L + 1)]
        mn = min(counts)
        amn = counts.index(mn)
        floor = L * DELTA4
        print(f"  L={L:5d}: min nere profonde = {mn:4d} (a step {amn}) = {mn/L:.5f}/passo "
              f"= {mn/floor:.1f}x il pavimento delta4_auto ({floor:.1f})")


analyze("griglia vuota", [], 22000)
random.seed(12)
for trial in range(3):
    cells = set()
    while len(cells) < 16:
        cells.add((random.randint(-6, 6), random.randint(-6, 6)))
    analyze(f"IC random #{trial} (16 nere in [-6,6]^2)", cells, 30000)
print("\nfatto")
