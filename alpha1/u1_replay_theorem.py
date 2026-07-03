# u1_replay_theorem.py — §91a: U1 e' un TEOREMA (Teorema del Rigioco Bianco).
#
# ENUNCIATO. Sia w101 la Parola Viva (§88: residuo = {(1,1)}, certificato). Ogni
# estensione all'indietro realizzabile e record-compatibile che visita (1,1) e la lascia
# BIANCA produce una parola con burden1 = 0 e onset 160 (PAROLA-ARMA).
#
# DIMOSTRAZIONE (Replay-Lock §87a + residuo certificato §88 — versione V-DAGA, riparata
# dopo il buco d'orizzonte trovato dal pannello §91: la rilevazione dell'onset legge fino
# a t=2600, non fino a onset+P):
#   1. il verdetto onset_verified e la V della corsa sono funzione delle SVOLTE fino
#      all'orizzonte di rilevazione T=2600; per Replay-Lock le svolte fino a T dipendono
#      solo dai colori iniziali di V-DAGA = prime letture della corsa entro T (576 celle);
#   2. residuo(w101) = {(1,1)} (certificato §88) e — CHECK G1b, nuovo — V-DAGA INT
#      {y>=1} SUB F U {(1,1)}: la corsa, oltre l'onset, legge solo celle a y<=0
#      fuori dal footprint;
#   3. ogni estensione record-compatibile ha footprint in {y>=1}: le celle nuove
#      dell'estensione intersecano V-DAGA al piu' in {(1,1)} (le celle a y<=0 sono
#      intoccabili per definizione di record stretto);
#   4. sulle celle di F i colori finali del germe esteso coincidono con quelli di w101
#      (le visite dell'estensione sono tutte piu' antiche della finestra: le ultime
#      scritture su F sono della finestra, identica per ogni estensione);
#   5. se l'ultima visita a (1,1) la lascia BIANCA (= colore vergine letto dalla corsa),
#      il germe esteso ristretto a V-DAGA e' identico ==> svolte identiche fino a T ==>
#      stesso verdetto di rilevazione (onset 160) e stessa V;
#   6. residuo(esteso) = (V \ F') INT {y>=1} con F' ⊇ F U {(1,1)} ==> VUOTO. QED.
#
# Questo script verifica MECCANICAMENTE gli ingredienti e attacca il teorema:
#   G1  residuo(w101) = {(1,1)} e V INT {y>=1} SUB F U {(1,1)} (ricalcolo indipendente);
#   G2  punto 4: colori finali su F identici per le 60 estensioni del censimento §90c;
#   G3  30/30 coprenti-bianche del campione: burden 0, onset 160, V identica a quella
#       di w101 (non solo burden: l'intera corsa);
#   G4  attacco: cerca coprenti-bianche FRESCHE in regioni diverse dell'albero (random
#       restart della caccia guidata) e ri-testa; un solo controesempio = ROSSO.
# Uscita: alpha1/u1_replay_theorem_summary.json
import sys, os, json, time, heapq, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import P, simulate
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_target_hunt import tail_state, TGT
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, "record_cover_census_summary.json")
OUT = os.path.join(HERE, "u1_replay_theorem_summary.json")


def germ_run(word):
    anchor = to_anchor_frame(*virtual_walk(word))
    gb = {c for c, col in anchor.items() if col == 1}
    turns, n, onset, fr, _ = simulate(gb, 0, 0, 0, 2_000_000, chk=2600)
    V = {c for c, (t, _) in fr.items() if t < onset + P}
    return anchor, onset, V


def main():
    t0 = time.time()
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])

    # G1
    anchor0, onset0, V0 = germ_run(w101)
    F0 = set(anchor0)
    res0 = sorted(c for c in (V0 - F0) if c[1] >= 1)
    assert res0 == [TGT], f"G1 ROSSO: residuo {res0}"
    assert all(c in F0 or c == TGT for c in V0 if c[1] >= 1), "G1 ROSSO: inclusione"
    print(f"G1 VERDE: residuo(w101) = [(1,1)]; V INT {{y>=1}} SUB F U {{(1,1)}} "
          f"(|V|={len(V0)}, onset {onset0})", flush=True)

    # G1b (riparazione del buco d'orizzonte, pannello §91): l'inclusione vale anche per
    # V-DAGA = prime letture fino all'orizzonte di rilevazione T=2600
    from onset_cone_lock import DX, DY
    gb = {c for c, col in anchor0.items() if col == 1}
    grid = {}
    x = y = 0
    h = 0
    Vdag = set()
    for t in range(2600):
        c = (x, y)
        col = grid[c] if c in grid else (1 if c in gb else 0)
        if c not in grid:
            Vdag.add(c)
        if col == 0:
            h = (h + 1) & 3
            grid[c] = 1
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += DX[h]
        y += DY[h]
    extra = [c for c in Vdag if c[1] >= 1 and c not in F0 and c != TGT]
    assert not extra, f"G1b ROSSO: {extra}"
    print(f"G1b VERDE: V-DAGA (|{len(Vdag)}| prime letture fino a T=2600) INT {{y>=1}} "
          f"SUB F U {{(1,1)}} — zero celle extra", flush=True)

    # G2 + G3 sul censimento
    cc = json.load(open(CC))
    n_white = 0
    for r in cc["rows"]:
        w2 = to_bits(r["word_ext"]) + w101
        anchor2 = to_anchor_frame(*virtual_walk(w2))
        assert all(anchor2[c] == anchor0[c] for c in F0), \
            f"G2 ROSSO a prof.{r['depth']}: colori su F cambiati"
        if r["colore_11"] == "W":
            n_white += 1
            a2, o2, V2 = germ_run(w2)
            assert o2 == onset0 and V2 == V0, f"G3 ROSSO a prof.{r['depth']}"
            res2 = sorted(c for c in (V2 - set(a2)) if c[1] >= 1)
            assert res2 == [], f"G3 ROSSO: residuo non vuoto a prof.{r['depth']}"
    print(f"G2 VERDE: colori finali su F identici per 60/60 estensioni", flush=True)
    print(f"G3 VERDE: {n_white}/{n_white} coprenti-bianche rigiocano identiche "
          f"(onset, V) e hanno residuo vuoto", flush=True)

    # G4: caccia fresca con restart casuali (bussola rumorosa)
    rng = random.Random(91)
    fresh = 0
    tested = 0
    t1 = time.time()
    for trial in range(6):
        heap = [(0, 0, ())]
        seen = 0
        while heap and seen < 250_000 and time.time() - t1 < 300:
            pri, dep, ext = heapq.heappop(heap)
            if dep >= 200:
                continue
            for bit in (0, 1):
                e2 = (bit,) + ext
                seen += 1
                ok, tail, hit = tail_state(e2 + w101)
                if not ok:
                    continue
                if hit:
                    w2 = e2 + w101
                    anchor2 = to_anchor_frame(*virtual_walk(w2))
                    if anchor2[TGT] == 0:
                        a2, o2, V2 = germ_run(w2)
                        res2 = sorted(c for c in (V2 - set(a2)) if c[1] >= 1)
                        assert o2 == onset0 and res2 == [], \
                            f"G4 ROSSO: controesempio {''.join('R' if b else 'L' for b in e2)}"
                        fresh += 1
                    tested += 1
                    continue
                c = max(abs(tail[0] - TGT[0]), abs(tail[1] - TGT[1]))
                heapq.heappush(heap, (c + rng.random() * 3, dep + 1, e2))
    print(f"G4 VERDE: {fresh} coprenti-bianche FRESCHE (restart rumorosi, {tested} "
          f"coprenti totali) — nessun controesempio", flush=True)

    out = {"G1": {"residuo": [list(TGT)], "V": len(V0), "onset": onset0},
           "G2_ok": 60, "G3_ok": n_white, "G4_fresh_white": fresh,
           "G4_tested": tested, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"U1: TEOREMA DEL RIGIOCO BIANCO — ingredienti verdi, attacco fallito. "
          f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()

