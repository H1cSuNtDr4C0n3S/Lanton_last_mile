# word_lock.py — §86b: lock di prima-lettura per parole di svolta (estensione del metodo halo).
# Per una parola di svolte W realizzabile da una lettura, la dinamica consulta solo celle lette;
# le celle PRIMO-lette durante W conservano il colore iniziale fino alla loro prima lettura
# (una cella cambia colore solo quando viene letta), quindi:
#   TEOREMA-LOCK (<=>, per calcolo diretto): la parola W parte dalla lettura corrente se e solo
#   se ogni cella primo-letta ha il colore richiesto dalla svolta corrispondente (L=nera,
#   R=bianca) al momento della lettura iniziale. Le riletture sono forzate dall'alternanza
#   (auto-alimentazione) e non aggiungono condizioni.
# Il lock e' quindi: {cella (frame heading-su) -> colore richiesto}, con raggio finito.
# Per (LRRRR)^3 il lock DEVE riprodurre il Teorema Halo §85c: centro nero + 9 celle bianche
# (gate). Per p15 = LLLLRLRRRRLRRRR (il ride puro-coda di §84, unico in ECCESSO x1,9 ai deep)
# il lock rivela quanti NERI extra-centro la parola richiede: se >=1, la dicotomia §84
# (LRRRR evitato totalmente, p15 in eccesso) e' spiegata dal Teorema della Scia §86a —
# il caos maturo uccide le parole che esigono solitudine e tollera quelle che esigono compagnia.
# Verifica: necessita' (ogni flip di cella-lock rompe W), sufficienza (1000 ambienti junk fuori
# dal read-set), coerenza riletture (nessuna contraddizione: W realizzata col solo lock).
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)

WORDS = {
    "LRRRR^3 (p5 x3, halo §85)": "LRRRR" * 3,
    "LLRRRR^3 (p6 rotore r2)": "LLRRRR" * 3,
    "LLRRLLRRRR^3 (p10)": "LLRRLLRRRR" * 3,
    "p15^3 (LLLLRLRRRRLRRRR, puro-coda §84)": "LLLLRLRRRRLRRRR" * 3,
    "p15^1": "LLLLRLRRRRLRRRR",
}

def lock_of(word):
    """Ritorna (lock, first_order, realizzabile). lock: {(dx,dy): 0/1 colore iniziale richiesto}.
    Costruzione: si simula imponendo a ogni prima lettura il colore che produce la svolta
    richiesta; le riletture devono produrre da sole la svolta giusta, altrimenti la parola
    non e' realizzabile da nessuna configurazione iniziale (le riletture sono forzate)."""
    need = [1 if ch == 'L' else 0 for ch in word]
    lock = {}; order = []
    black = set(); seen = set()
    x = y = h = 0
    for i, nb in enumerate(need):
        c = (x, y)
        if c not in seen:
            seen.add(c); lock[c] = nb; order.append(c)
            if nb: black.add(c)
        isb = 1 if c in black else 0
        if isb != nb:
            return lock, order, False          # rilettura contraddittoria: parola irrealizzabile
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        x += DX[h]; y += DY[h]
    return lock, order, True

def sim(black, n):
    w = []
    x = y = h = 0
    for _ in range(n):
        c = (x, y); isb = c in black
        w.append('L' if isb else 'R')
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        x += DX[h]; y += DY[h]
    return ''.join(w)

def verify(word, lock):
    base = {c for c, col in lock.items() if col == 1}
    assert sim(set(base), len(word)) == word, "lock non sufficiente (base)"
    for c in lock:                              # necessita': ogni flip rompe
        b2 = set(base); b2.symmetric_difference_update({c})
        assert sim(b2, len(word)) != word, f"flip {c} non rompe"
    rnd = random.Random(86)
    readset = set(lock)
    for _ in range(1000):                       # sufficienza robusta: junk fuori dal read-set
        junk = {(rnd.randint(-6, 6), rnd.randint(-6, 6)) for _ in range(16)} - readset
        assert sim(base | junk, len(word)) == word, "junk rompe la parola"

def main():
    out = {}
    print(f"{'parola':<40} {'|lock|':>6} {'neri':>5} {'bianchi':>8} {'raggio':>7} {'neri extra-centro':>18}")
    for name, w in WORDS.items():
        lock, order, ok = lock_of(w)
        if not ok:
            print(f"{name:<40}  IRREALIZZABILE da lettura singola (rilettura contraddittoria)")
            out[name] = {"word": w, "realizzabile": False,
                         "lock_parziale": sorted([list(c) + [col] for c, col in lock.items()])}
            continue
        verify(w, lock)
        nb = sum(1 for v in lock.values() if v == 1)
        nw = len(lock) - nb
        rad = max(max(abs(a), abs(b)) for a, b in lock)
        extrab = nb - 1                          # il centro (0,0) e' sempre nero (W parte con L)
        print(f"{name:<40} {len(lock):>6} {nb:>5} {nw:>8} {rad:>7} {extrab:>18}")
        out[name] = {"word": w, "realizzabile": True, "lock_size": len(lock),
                     "neri": nb, "bianchi": nw, "raggio": rad, "neri_extra_centro": extrab,
                     "lock": sorted([list(c) + [col] for c, col in lock.items()]),
                     "verifica": "necessita' tutte + sufficienza 1000 junk OK"}
    # gate: LRRRR^3 deve riprodurre il Teorema Halo §85c
    hl = out["LRRRR^3 (p5 x3, halo §85)"]
    HALO = {(-2,0),(-2,1),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-1),(0,1),(0,2)}
    got_w = {tuple(e[:2]) for e in hl["lock"] if e[2] == 0}
    got_b = {tuple(e[:2]) for e in hl["lock"] if e[2] == 1}
    assert got_b == {(0, 0)} and got_w == HALO, "GATE §85c ROSSO"
    print("\nGATE §85c: lock(LRRRR^3) = {centro nero} + 9 celle halo bianche — VERDE")
    json.dump(out, open(ALPHA / "word_lock_summary.json", "w"), indent=1)
    print(f"scritto {ALPHA / 'word_lock_summary.json'}")

if __name__ == "__main__":
    main()
