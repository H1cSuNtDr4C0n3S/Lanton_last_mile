# orbit_debt.py — test del debito su un'orbita REALE (griglia vuota): replica la semantica
# di memoria della finestra 9x9 dell'automa (una cella e' nota solo se letta e mai uscita
# dalla finestra da allora) e classifica ogni lettura:
#   forzata (cella nota) | profonda bianca prima-visita | profonda bianca rivisita |
#   profonda nera rivisita (il "detrito" — da griglia vuota le prime-visite nere non esistono)
# Misura il tasso di letture nere profonde nel transiente (per finestre di eta') e sulla
# highway (per periodo 104), da confrontare con delta4 = 2/313 ~ 0.00639.
# Convenzioni: CLAUDE.md §2 (bianco->R, flip, mossa; heading 0=su). Onset atteso N0=9977.

import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
R = 4
TOTAL = 9977 + 104 * 20   # transiente completo + 20 periodi di highway

DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
black = set()           # celle nere
last_read = {}          # cella -> ultimo step di lettura
known = set()           # celle lette e rimaste nella finestra 9x9 da allora
x = y = h = 0
turns = []
events = []             # (step, classe, eta')  per le letture non forzate
deep_black_steps = []

for t in range(TOTAL):
    c = (x, y)
    col_black = c in black
    turns.append('L' if col_black else 'R')
    if c in known:
        cls = "forzata"
    else:
        prev = last_read.get(c)
        if col_black:
            cls = "nera_profonda_rivisita" if prev is not None else "nera_profonda_PRIMA"
            deep_black_steps.append(t)
        else:
            cls = "bianca_profonda_rivisita" if prev is not None else "bianca_prima_visita"
        events.append((t, cls, None if prev is None else t - prev))
    # flip + nota + mossa
    if col_black:
        black.discard(c); h = (h - 1) & 3
    else:
        black.add(c); h = (h + 1) & 3
    last_read[c] = t
    known.add(c)
    x += DX[h]; y += DY[h]
    # dimentica le celle uscite dalla finestra: stanno sul bordo opposto al moto
    gone = [cell for cell in
            ((x - 5, y + d) for d in range(-5, 6)) if cell in known]
    gone += [cell for cell in ((x + 5, y + d) for d in range(-5, 6)) if cell in known]
    gone += [cell for cell in ((x + d, y - 5) for d in range(-5, 6)) if cell in known]
    gone += [cell for cell in ((x + d, y + 5) for d in range(-5, 6)) if cell in known]
    for cell in gone:
        if max(abs(cell[0] - x), abs(cell[1] - y)) > R:
            known.discard(cell)

# nota: il filtro 'gone' sopra controlla solo l'anello a distanza 5 (l'unico da cui si puo'
# uscire muovendosi di 1), piu' il check esplicito di Chebyshev per sicurezza.
# Verifica di coerenza: nessuna cella in known deve essere fuori finestra.
assert all(max(abs(cx - x), abs(cy - y)) <= R for cx, cy in known), "leak di known!"

# --- onset della highway (verifica della convenzione) ---
per = 104
i = TOTAL - per - 1
while i >= 0 and turns[i] == turns[i + per]:
    i -= 1
onset = i + 1
print(f"passi totali {TOTAL}; 104-periodicita' delle svolte da step {onset} "
      f"(atteso ~9977; coda di {TOTAL-onset} passi periodici)")

# --- classificazione globale ---
cnt = Counter(cls for _, cls, _ in events)
nforced = TOTAL - len(events)
print(f"\nletture: forzate {nforced} ({nforced/TOTAL*100:.1f}%), profonde {len(events)}")
for k, v in cnt.most_common():
    print(f"  {k}: {v}")

# --- transiente: tasso di nere profonde per finestra di eta' ---
print("\ntasso letture nere profonde nel transiente (finestre da 1000 passi):")
for a in range(0, onset, 1000):
    b = min(a + 1000, onset)
    nb = sum(1 for s in deep_black_steps if a <= s < b)
    print(f"  [{a:5d},{b:5d}): {nb:3d}  ({nb/(b-a):.4f} per passo)")
tr_b = sum(1 for s in deep_black_steps if s < onset)
print(f"  TOTALE transiente: {tr_b} nere profonde / {onset} passi = {tr_b/onset:.4f}")

# eta' del detrito (nere profonde, transiente): quanto era vecchia l'ultima lettura
ages = [age for s, cls, age in events if cls == "nera_profonda_rivisita" and s < onset]
if ages:
    ages.sort()
    print(f"  eta' delle nere profonde (transiente): min {ages[0]}, mediana "
          f"{ages[len(ages)//2]}, max {ages[-1]}; quartili "
          f"{ages[len(ages)//4]}, {ages[3*len(ages)//4]}")

# --- highway: pattern esatto per periodo ---
hw = [s for s in deep_black_steps if s >= onset]
per_period = Counter((s - onset) // per for s in hw)
phases = sorted(set((s - onset) % per for s in hw))
nper = (TOTAL - onset) // per
print(f"\nhighway ({nper} periodi interi): nere profonde per periodo: "
      f"{sorted(per_period.values())[:3]}...{sorted(per_period.values())[-3:]} "
      f"(media {len(hw)/((TOTAL-onset)/per):.2f})")
print(f"fasi (mod 104) delle nere profonde sulla highway: {phases}")
rate_hw = len(hw) / (TOTAL - onset)
print(f"tasso highway: {rate_hw:.5f} per passo  (delta4 = 2/313 = {2/313:.5f}; "
      f"rapporto {rate_hw/(2/313):.2f}x)")
ages_hw = sorted(age for s, cls, age in events
                 if cls == "nera_profonda_rivisita" and s >= onset + per)
if ages_hw:
    print(f"eta' delle nere profonde in highway: min {ages_hw[0]}, mediana "
          f"{ages_hw[len(ages_hw)//2]}, max {ages_hw[-1]}")
print("fatto")
