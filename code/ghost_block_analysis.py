# ghost_block_analysis.py — dimensionamento empirico della memoria del prodotto A(r;m,D).
# Per ogni fantasma del catalogo (results/delta4_alt_catalog.jsonl) simula la semantica di
# memoria del prodotto in COORDINATE ASSOLUTE (equivalente al frame canonico: la norma inf
# e' invariante per rotazione) e verifica se la menzogna del fantasma viene bloccata:
# una cella ricordata si legge FORZATA al colore vero, quindi il primo conflitto di
# alternanza del catalogo diventa un cammino inesistente nel prodotto.
#
# Semantica di memoria (identica al builder del prodotto, da tenere allineata):
#   - celle note = visitate; dentro la finestra (2r+1)^2 si ricordano sempre;
#   - fuori finestra: si dimenticano oltre il box ||.||inf <= D; se le superstiti sono
#     piu' di m, si tengono le m migliori secondo la politica:
#       near   = le piu' vicine (tie-break lessicografico)
#       recent = uscite dalla finestra piu' di recente (tie-break lessicografico)
#   - NB: e' una SOTTO-memoria di quella vera => se blocca qui, blocca anche nel prodotto.
#
# Uso: python ghost_block_analysis.py [--radius 4] [--catalog results/delta4_alt_catalog.jsonl]
# Output: tabella copertura (policy, m, D) -> frazione di fantasmi bloccati + requisiti
# per-fantasma (m minimo a D dato) e check dei testimoni r1/r2/r3.

import argparse, json, os, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
from window_automaton import canon, drift_and_rot  # noqa: E402
from altmin_driver import first_conflict  # noqa: E402

DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
W, B = 1, 2

# Stable base-window delta witnesses. Keep these in source rather than
# build/r*_delta_cycle.txt because build/ is ignored and clean-clone tests use
# them only as fixed words, not as generated certification artifacts.
BASE_DELTA_WITNESSES = {
    1: (3, 5, "LRLLL"),
    2: (1, 7, "RRRRLRL"),
    3: (1, 64, "RRRRLLLLRLRRRRLRRRRLLLLRLLRRRRLLRLRRRRLRRRRLLLLRLRRRRLRRRRLLLLRL"),
}


def canon_rel(wx, wy, h):
    """posizione relativa nel frame canonico (heading=su): CCW applicata h volte.
    DEVE coincidere col tie-break di product_automaton (stessa eviction)."""
    for _ in range(h & 3):
        wx, wy = -wy, wx
    return wx, wy


def product_blocks_word(word, r, m, D, policy, max_steps):
    """cammina la parola ciclica con la memoria del prodotto; ritorna lo step del primo
    blocco (lettura forzata contraddetta dalla parola) o None se la parola sopravvive."""
    x = y = h = 0
    K = {}          # cella -> colore corrente (W/B), solo celle ricordate
    exit_t = {}     # cella -> step dell'ultima uscita dalla finestra (per policy recent)
    L = len(word)
    for t in range(max_steps):
        tt = 1 if word[t % L] == "R" else 0
        pos = (x, y)
        col = K.get(pos)
        if col is not None:
            forced = 1 if col == W else 0      # bianco -> R
            if forced != tt:
                return t                        # menzogna bloccata
            K[pos] = B if col == W else W       # flip
        else:
            # lettura assunta: R => era bianca, L => era nera; poi flip
            K[pos] = B if tt == 1 else W
        exit_t.pop(pos, None)
        h = (h + 1) & 3 if tt else (h - 1) & 3
        nx, ny = x + DX[h], y + DY[h]
        # gestione memoria rispetto alla NUOVA posizione della formica
        outside = []
        for (cx, cy), c in K.items():
            d = max(abs(cx - nx), abs(cy - ny))
            if d <= r:
                continue
            # appena uscita? (era dentro rispetto alla vecchia posizione)
            if max(abs(cx - x), abs(cy - y)) <= r and (cx, cy) not in exit_t:
                exit_t[(cx, cy)] = t
            elif (cx, cy) not in exit_t:
                exit_t[(cx, cy)] = t
            outside.append((cx, cy, d))
        # rientri: celle fuori che ora sono dentro perdono il timestamp di uscita
        for cell in [c for c in exit_t if max(abs(c[0] - nx), abs(c[1] - ny)) <= r]:
            exit_t.pop(cell)
        drop = [(cx, cy) for cx, cy, d in outside if d > D]
        keepable = [(cx, cy, d) for cx, cy, d in outside if d <= D]
        if len(keepable) > m:
            if policy == "near":
                keepable.sort(key=lambda e: (e[2],) + canon_rel(e[0] - nx, e[1] - ny, h))
            else:  # recent: exit_t piu' alto = piu' recente
                keepable.sort(key=lambda e: (-exit_t[(e[0], e[1])],) + canon_rel(e[0] - nx, e[1] - ny, h))
            drop += [(cx, cy) for cx, cy, _ in keepable[m:]]
        for cell in drop:
            K.pop(cell, None)
            exit_t.pop(cell, None)
        x, y = nx, ny
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, default=4)
    ap.add_argument("--catalog", default=os.path.join(ROOT, "results", "delta4_alt_catalog.jsonl"))
    a = ap.parse_args()
    r = a.radius

    print("== testimoni dei minimi r1/r2/r3: sono fantasmi? ==")
    for rr, (p, q, w) in BASE_DELTA_WITNESSES.items():
        conf = first_conflict(w)
        rot, dr = drift_and_rot(w)
        bt = "B-T" if (rot % 4 != 0 or dr == (0, 0)) else "NO-B-T"
        print(f"  r={rr}: delta={p}/{q} parola {w if len(w)<=40 else w[:37]+'...'} "
              f"rot={rot:+d} drift={dr} {bt} -> "
              f"{'FANTASMA (conflitto step %d, dist %d)' % (conf['step'], conf['distanza']) if conf else 'alternanza-CONSISTENTE'}")

    ghosts = []
    for line in open(a.catalog):
        rec = json.loads(line)
        if rec.get("conflitto") and not rec.get("dup"):
            ghosts.append(rec)
    print(f"\n== catalogo: {len(ghosts)} fantasmi (non-dup, con conflitto) ==")

    Ms = [2, 4, 8, 16, 32, 64, 128]
    Ds = [6, 8, 12, 16, 24, 32]
    results = {}
    for policy in ("near", "recent"):
        for D in Ds:
            for m in Ms:
                blocked = 0
                for g in ghosts:
                    cs = g["conflitto"]["step"]
                    horizon = cs + 1
                    if product_blocks_word(g["word"], r, m, D, policy, horizon) is not None:
                        blocked += 1
                results[(policy, m, D)] = blocked
        print(f"\npolicy={policy}: bloccati su {len(ghosts)} (righe m, colonne D)")
        print("   m\\D " + "".join(f"{D:>6}" for D in Ds))
        for m in Ms:
            print(f"  {m:4d} " + "".join(f"{results[(policy, m, D)]:>6}" for D in Ds))

    # requisiti per-fantasma: m minimo che blocca, a D=32 (box largo), per policy
    print("\n== m minimo per fantasma (D=32) ==")
    for policy in ("near", "recent"):
        need = []
        unblocked = []
        for g in ghosts:
            cs = g["conflitto"]["step"]
            got = None
            for m in Ms:
                if product_blocks_word(g["word"], r, m, 32, policy, cs + 1) is not None:
                    got = m
                    break
            if got is None:
                unblocked.append(g["iter"])
            else:
                need.append(got)
        hist = defaultdict(int)
        for v in need:
            hist[v] += 1
        print(f"  policy={policy}: istogramma m minimo {dict(sorted(hist.items()))}"
              f"{' | NON bloccati: iter ' + str(unblocked) if unblocked else ' | tutti bloccati'}")


if __name__ == "__main__":
    main()
