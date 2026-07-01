# lrrrr_halo_witness.py — §85c: testimone reale + caratterizzazione esatta dell'inizio (LRRRR)^3.
# TEOREMA (locale, esatto, per calcolo diretto): una lettura nera inizia (LRRRR)^3 se e solo se
# le 9 celle-halo HALO (coordinate esplicite nel frame con heading iniziale su, raggio massimo 2)
# sono TUTTE bianche al momento della lettura. La dinamica consulta solo le celle lette; nei
# 15 passi vengono primo-lette esattamente {centro} U HALO, e le L dei periodi 2-3 rileggono
# neri scritti dalla cavalcata stessa (auto-alimentata). Corollari:
#  - il teorema-finestra universale "nessuna lettura nera fuori-memoria inizia (LRRRR)^3"
#    e' FALSO: testimone = nero isolato nel bianco (i 4 sopravvissuti dell'automa sono reali);
#  - motivo potato vuoto (§81) => halo bianco => cavalcata: quindi l'evitamento totale di §84
#    IMPLICA lo 0% di motivi vuoti misurato indipendentemente in §81;
#  - l'evitamento empirico (0 / 2.323.679 deep_1, §85a) e' un invariante AMBIENTALE del regime
#    caotico maturo: i deep-black non sono mai isolati a scala 2 lungo il cammino imminente.
DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
HALO = [(-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, -1), (0, 1), (0, 2)]

def run(black, x=0, y=0, h=0, n=15):
    word = []
    for _ in range(n):
        c = (x, y); isb = c in black
        word.append('L' if isb else 'R')
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        x += DX[h]; y += DY[h]
    return ''.join(word)

if __name__ == "__main__":
    T = "LRRRR" * 3
    # testimone
    assert run({(0, 0)}) == T, "testimone rotto"
    # necessita': ogni singolo nero nell'halo rompe la parola
    for c in HALO:
        assert run({(0, 0), c}) != T, f"flip {c} non rompe la parola"
    # sufficienza robusta: junk nero fuori dall'insieme letto non tocca la cavalcata
    import random
    random.seed(42)
    readset = {(0, 0)} | set(HALO)
    for _ in range(1000):
        junk = {(random.randint(-4, 4), random.randint(-4, 4)) for _ in range(12)} - readset
        assert run({(0, 0)} | junk) == T, "sufficienza rotta"
    print("TEOREMA HALO: testimone OK, necessita' 9/9 OK, sufficienza (1000 ambienti) OK")
    print("halo:", HALO)
